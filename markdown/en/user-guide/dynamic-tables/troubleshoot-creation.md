# Troubleshoot dynamic table creation issues

This page helps you diagnose and resolve problems that occur when you create a dynamic table.
For refresh failures on an existing dynamic table, see [Troubleshoot dynamic table refresh issues](/user-guide/dynamic-tables/troubleshoot-refreshes).
For permission-related failures, see [Troubleshoot dynamic table permission issues](/user-guide/dynamic-tables/troubleshoot-permissions).

## CREATE fails with SQL compilation error

If creation fails with a ‘context function not supported’ error, the definition uses a function that requires a live user session. Dynamic table refreshes run asynchronously without one.

Common error messages:

```
SQL compilation error: Unsupported context function 'CURRENT_SESSION' used in dynamic table definition.
```

Dynamic tables do not support `CURRENT_SESSION` in the definition because refreshes run asynchronously without a user session.

To resolve this:

1. Remove the unsupported function from the definition.
2. If you need user-level filtering, apply it in a view or policy on top of the
   dynamic table rather than inside the definition itself.
3. For a full list of supported and unsupported constructs, see
   [Supported queries for dynamic tables](/user-guide/dynamic-tables/supported-queries).

## CREATE fails with “insufficient privileges”

When `CREATE DYNAMIC TABLE` fails with an insufficient privileges error, the executing role
is missing one or more required grants.

```
SQL access control error: Insufficient privileges to operate on schema 'MY_DB.MY_SCHEMA'.
```

The minimum privileges required to create a dynamic table are:

| Privilege | Object | Purpose |
| --- | --- | --- |
| CREATE DYNAMIC TABLE | Schema | Allows creating dynamic tables in the schema |
| USAGE | Warehouse | Allows running refreshes |
| SELECT | Base tables | Allows reading from base tables or views |
| USAGE | Database | Allows accessing the database |
| USAGE | Schema | Allows accessing the schema |

Expand

Show lessSee more

1. Check what privileges your role currently has:

   Copy code

   ```
   SHOW GRANTS TO ROLE transform_role;
   ```
2. Grant the missing privileges:

   Copy code

   ```
   GRANT CREATE DYNAMIC TABLE ON SCHEMA mydb.myschema TO ROLE transform_role;
   GRANT USAGE ON WAREHOUSE transform_wh TO ROLE transform_role;
   GRANT SELECT ON TABLE mydb.myschema.raw_orders TO ROLE transform_role;
   ```

For the full privilege reference, see [Dynamic table access control](/user-guide/dynamic-tables/privileges).

## Dynamic table shows no data after creation

With the default `INITIALIZE = ON_CREATE`, the CREATE statement blocks until the initial refresh completes.

If the table returns zero rows after successful creation, the most common cause is a row access policy on a base table that filters out all data when evaluated under the dynamic table’s owner role (which runs without secondary roles). Also verify that the definition’s WHERE clause and JOIN logic return rows when executed as the owner role.

With `INITIALIZE = ON_SCHEDULE`, the table is empty until the initial refresh. Queries return a `Dynamic table is not initialized` error. To populate immediately, run `ALTER DYNAMIC TABLE <name> REFRESH`.

## Refresh mode resolves to FULL when you expected INCREMENTAL

When you create a dynamic table with `REFRESH_MODE = AUTO` (the default), Snowflake evaluates the
definition at creation time and chooses INCREMENTAL or FULL. This decision is permanent and can’t
be changed with ALTER. If the definition contains constructs that do not support incremental refresh,
AUTO resolves to FULL without a warning.

1. Check the resolved refresh mode:

   Copy code

   ```
   SHOW DYNAMIC TABLES LIKE 'dt_orders' IN SCHEMA mydb.myschema;

   SELECT "name", "refresh_mode"
   FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()));
   ```

   ```
   +------------+--------------+
   | name       | refresh_mode |
   +------------+--------------+
   | DT_ORDERS | FULL         |
   +------------+--------------+
   ```
2. If you need incremental refresh, set `REFRESH_MODE = INCREMENTAL` explicitly. This causes
   creation to fail if the definition contains unsupported constructs, rather than falling
   back to FULL without a warning:

   Copy code

   ```
   CREATE OR REPLACE DYNAMIC TABLE mydb.myschema.dt_orders
       TARGET_LAG = '10 minutes'
       WAREHOUSE = transform_wh
       REFRESH_MODE = INCREMENTAL
   AS
       SELECT order_id, customer_id, order_date
       FROM mydb.myschema.raw_orders;
   ```
3. If creation fails with `REFRESH_MODE = INCREMENTAL`, review the error message to identify which
   construct is unsupported. For a list of constructs that support incremental refresh, see
   [Supported queries for dynamic tables](/user-guide/dynamic-tables/supported-queries).

Tip

Always set `REFRESH_MODE` explicitly to avoid unexpected costs from full refreshes.
Use `REFRESH_MODE = INCREMENTAL` to get a clear error at creation time if your definition
is not incrementally refreshable.

## EXECUTE AS USER errors

When you use the `EXECUTE AS USER` clause in `CREATE DYNAMIC TABLE`, Snowflake refreshes the
dynamic table on behalf of the named user instead of the internal SYSTEM user. The following
errors can occur during setup.

**Missing IMPERSONATE privilege:**

```
SQL access control error: Insufficient privileges to operate on user '<USER>'.
```

The owner role must have the IMPERSONATE privilege on the target user. Grant it with:

Copy code

```
GRANT IMPERSONATE ON USER service_user TO ROLE transform_role;
```

The target user must also hold the dynamic table’s owner role:

Copy code

```
GRANT ROLE transform_role TO USER service_user;
```

**User does not exist:**

```
SQL compilation error: User '<USER>' does not exist or not authorized.
```

Verify that the user name in the `EXECUTE AS USER` clause is spelled correctly and that the
user has not been dropped. Check existing users with:

Copy code

```
SHOW USERS LIKE 'service_user';
```

For more information about EXECUTE AS USER privileges and configuration, see
[EXECUTE AS USER](/user-guide/dynamic-tables/privileges#label-dynamic-tables-privileges-execute-as-user).

## Dynamic Iceberg table creation issues

When creating a dynamic Iceberg table, additional configuration is required beyond a standard
dynamic table. Common errors relate to the external volume, catalog, or base location.

**External volume errors:**

```
SQL compilation error: External volume '<VOLUME>' does not exist or not authorized.
```

Verify that the external volume exists and the creating role has USAGE on it:

Copy code

```
SHOW EXTERNAL VOLUMES;
GRANT USAGE ON EXTERNAL VOLUME my_ext_volume TO ROLE transform_role;
```

**Catalog integration errors:**

```
SQL compilation error: Catalog integration '<CATALOG>' does not exist or not authorized.
```

Verify that the catalog integration exists if you are using one. For Snowflake-managed Iceberg
tables, you typically do not need a catalog integration.

**Base location errors:**

```
SQL compilation error: Invalid base location '<LOCATION>'.
```

The `BASE_LOCATION` must be a valid relative path within the external volume. Verify that the
path is correctly formatted and does not contain invalid characters.

For the full creation syntax, see [Create a dynamic Apache Iceberg™ table](/user-guide/dynamic-tables/create-iceberg).

## Change tracking not enabled on base tables

Incremental refresh requires change tracking on all base tables referenced by the definition.
Snowflake enables change tracking automatically when you create an incremental dynamic table,
provided that the creating role has OWNERSHIP on the base tables.

```
Change tracking is not enabled on table '<TABLE>'.
```

1. If you own the base tables, Snowflake enables change tracking for you. No action is required.
2. If another role owns the base tables, ask the owner to enable change tracking:

   Copy code

   ```
   ALTER TABLE mydb.myschema.raw_orders SET CHANGE_TRACKING = TRUE;
   ```
3. Alternatively, grant OWNERSHIP on the base table to the creating role, create the dynamic
   table (which auto-enables change tracking), and then transfer OWNERSHIP back.

Note

Views that reference tables without change tracking also cause this error. Enable change tracking
on the base tables that the view references.

## Warehouse not appearing in query history during initialization

After creating a dynamic table, the initialization query does not appear in the warehouse’s
query history immediately. This happens because the initial scheduling and setup work runs in
Snowflake’s Cloud Services layer, which does not consume warehouse compute credits.

1. Check if the initialization is running:

   Copy code

   ```
   SELECT name, state, refresh_action
   FROM TABLE(INFORMATION_SCHEMA.DYNAMIC_TABLE_REFRESH_HISTORY(
       NAME_PREFIX => 'mydb.myschema.dt_orders'
   ))
   ORDER BY refresh_start_time DESC
   LIMIT 1;
   ```
2. The warehouse is only used when the actual data computation starts. Small initialization
   tasks (metadata setup, scheduling registration) run entirely in Cloud Services. Once the
   INITIALIZE refresh moves to EXECUTING state, the warehouse resumes and the query appears in
   the query history. If the dynamic table’s data volume is small enough to be handled within
   the Cloud Services compute allocation, the warehouse may not resume at all.

For more information about Cloud Services compute, see
[Understanding compute cost](/user-guide/cost-understanding-compute).

## What’s next

- To troubleshoot refresh failures on an existing dynamic table, see
  [Troubleshoot dynamic table refresh issues](/user-guide/dynamic-tables/troubleshoot-refreshes).
- To troubleshoot permission-related issues, see
  [Troubleshoot dynamic table permission issues](/user-guide/dynamic-tables/troubleshoot-permissions).
- To understand refresh modes and how AUTO resolves, see
  [Dynamic table refresh modes](/user-guide/dynamic-tables/refresh-modes).
- To set up monitoring and alerts, see
  [Monitor dynamic tables](/user-guide/dynamic-tables/monitoring).
