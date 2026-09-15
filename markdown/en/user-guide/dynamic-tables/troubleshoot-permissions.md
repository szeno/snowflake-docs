# Troubleshoot dynamic table permission issues

This page helps you diagnose and resolve permission-related dynamic table failures.
For refresh failures unrelated to permissions, see [Troubleshoot dynamic table refresh issues](/user-guide/dynamic-tables/troubleshoot-refreshes).
For creation-time issues, see [Troubleshoot dynamic table creation issues](/user-guide/dynamic-tables/troubleshoot-creation).

## Refresh fails because secondary roles are not used

A query that succeeds interactively can fail during refresh because refreshes use only the owner role: secondary roles are not activated.

Typical error messages:

```
SQL access control error: Insufficient privileges to operate on table 'MY_DB.OTHER_SCHEMA.LOOKUP_TABLE'.
```

```
SQL compilation error: Object 'MY_DB.OTHER_SCHEMA.LOOKUP_TABLE' does not exist or not authorized.
```

1. Identify which objects the refresh can’t access. Check the refresh history for the error details:

   Copy code

   ```
   SELECT name, state, state_message, query_id
   FROM TABLE(INFORMATION_SCHEMA.DYNAMIC_TABLE_REFRESH_HISTORY(
       NAME_PREFIX => 'mydb.myschema.dt_orders',
       ERROR_ONLY => TRUE
   ))
   ORDER BY refresh_start_time DESC
   LIMIT 1;
   ```
2. Grant the missing privileges directly to the dynamic table’s owner role:

   Copy code

   ```
   -- Find the owner role
   SHOW DYNAMIC TABLES LIKE 'dt_orders' IN SCHEMA mydb.myschema;
   -- Check the "owner" column in the output

   -- Grant the missing privilege to the owner role
   GRANT SELECT ON TABLE mydb.other_schema.lookup_table TO ROLE transform_role;
   GRANT USAGE ON SCHEMA mydb.other_schema TO ROLE transform_role;
   ```
3. If the privileges come from a database role, grant that database role to the
   dynamic table’s owner role.

Important

Do not rely on secondary roles for dynamic table access. Every object referenced in the definition
must be accessible through the owner role’s primary grants.

## Refresh fails after ownership transfer

When you transfer ownership of a dynamic table to a different role (using `GRANT OWNERSHIP`),
the new owner role might not have all the privileges that the original owner had. Refreshes
start failing because the new role can’t access the warehouse, base tables, or functions.

```
SQL access control error: Insufficient privileges to operate on warehouse 'TRANSFORM_WH'.
```

1. Check which role now owns the dynamic table:

   Copy code

   ```
   SHOW DYNAMIC TABLES LIKE 'dt_orders' IN SCHEMA mydb.myschema;
   ```

   ```
   +------------+-------+------------------+
   | name       | owner | ...              |
   +------------+-------+------------------+
   | DT_ORDERS | NEW_ROLE | ...           |
   +------------+-------+------------------+
   ```
2. Grant the new owner role all privileges needed to refresh the dynamic table:

   Copy code

   ```
   -- Warehouse access
   GRANT USAGE ON WAREHOUSE transform_wh TO ROLE new_role;

   -- Base table access
   GRANT SELECT ON TABLE mydb.myschema.raw_orders TO ROLE new_role;

   -- If the definition uses UDFs
   GRANT USAGE ON FUNCTION mydb.myschema.my_udf(VARCHAR) TO ROLE new_role;

   -- Database and schema access
   GRANT USAGE ON DATABASE mydb TO ROLE new_role;
   GRANT USAGE ON SCHEMA mydb.myschema TO ROLE new_role;
   ```
3. After granting the privileges, resume the dynamic table if it was auto-suspended due to
   consecutive failures:

   Copy code

   ```
   ALTER DYNAMIC TABLE mydb.myschema.dt_orders RESUME;
   ```

Tip

Before transferring ownership, run `SHOW GRANTS TO ROLE <current_owner>` to capture the
full list of grants. Replicate those grants to the new owner role before the transfer.

Note

Policy-related refresh issues (row access policies, masking policies, projection policies) are documented on
[Troubleshoot dynamic table refresh issues](/user-guide/dynamic-tables/troubleshoot-refreshes).

## Can’t see dynamic table metadata

If `SHOW DYNAMIC TABLES` or `INFORMATION_SCHEMA.DYNAMIC_TABLES()` returns no rows for a dynamic
table you know exists, the issue is a missing privilege.

1. Verify that the dynamic table exists and your role can see it:

   Copy code

   ```
   SHOW DYNAMIC TABLES LIKE 'dt_orders' IN SCHEMA mydb.myschema;
   ```

   If this returns no rows, your role may also need USAGE on the database and schema.
2. Check whether your role has the MONITOR privilege on the dynamic table:

   Copy code

   ```
   SHOW GRANTS ON DYNAMIC TABLE mydb.myschema.dt_orders;
   ```

   ```
   +-------------------------------+-----------+---------------+------------+------------+--------------+
   | created_on                    | privilege | granted_on    | name       | granted_to | grantee_name |
   +-------------------------------+-----------+---------------+------------+------------+--------------+
   | 2025-01-15 08:00:00.000 -0800 | MONITOR   | DYNAMIC_TABLE | DT_ORDERS | ROLE       | ANALYST_ROLE |
   +-------------------------------+-----------+---------------+------------+------------+--------------+
   ```
3. If your role doesn’t have MONITOR, ask the dynamic table owner to grant it:

   Copy code

   ```
   GRANT MONITOR ON DYNAMIC TABLE mydb.myschema.dt_orders TO ROLE analyst_role;
   ```

For the full list of privileges required for dynamic table operations, see
[Dynamic table access control](/user-guide/dynamic-tables/privileges).

## Refresh fails with EXECUTE AS USER permission errors

When a dynamic table uses `EXECUTE AS USER`, refreshes can fail if the required privileges or
user configuration are missing.

**Missing IMPERSONATE privilege.** The dynamic table’s owner role must hold IMPERSONATE on the
target user. If this privilege is missing or was revoked, refreshes fail with a permission error.
Grant IMPERSONATE on the target user to the dynamic table’s owner role:

Copy code

```
GRANT IMPERSONATE ON USER service_user TO ROLE transform_role;
```

**User does not exist.** The user specified in EXECUTE AS USER must exist. If the user was dropped
or never created, refreshes fail. Recreate the user and ensure it holds the dynamic table’s owner
role:

Copy code

```
CREATE USER IF NOT EXISTS service_user;
GRANT ROLE transform_role TO USER service_user;
```

After resolving the issue, resume the dynamic table if it was auto-suspended:

Copy code

```
ALTER DYNAMIC TABLE mydb.myschema.dt_orders RESUME;
```

## What’s next

- To troubleshoot refresh failures on an existing dynamic table, see
  [Troubleshoot dynamic table refresh issues](/user-guide/dynamic-tables/troubleshoot-refreshes).
- To troubleshoot creation-time issues, see
  [Troubleshoot dynamic table creation issues](/user-guide/dynamic-tables/troubleshoot-creation).
- For the complete privilege reference, see
  [Dynamic table access control](/user-guide/dynamic-tables/privileges).
- To set up monitoring and alerts, see
  [Monitor dynamic tables](/user-guide/dynamic-tables/monitoring).
