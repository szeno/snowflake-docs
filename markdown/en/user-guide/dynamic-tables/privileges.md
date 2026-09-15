# Dynamic table access control

This page explains the privileges required to create, query, manage, monitor, and drop dynamic tables. Anyone who sets
up or manages dynamic table pipelines needs these grants.

The following example grants a role the minimum privileges to create a dynamic table in a specific schema:

Copy code

```
GRANT USAGE ON DATABASE mydb TO ROLE transform_role;
GRANT USAGE ON SCHEMA mydb.myschema TO ROLE transform_role;
GRANT USAGE ON WAREHOUSE transform_wh TO ROLE transform_role;
GRANT CREATE DYNAMIC TABLE ON SCHEMA mydb.myschema TO ROLE transform_role;
GRANT SELECT ON TABLE mydb.myschema.raw_orders TO ROLE transform_role;
```

After these grants, the role can create a dynamic table and query it as the owner. For a complete example, see
[Grant privileges to create a dynamic table](#label-dynamic-tables-privileges-create).

Note

The role names in these examples (such as `transform_role` and `analyst_role`) are placeholders. Replace them with
your own role names. These are not built-in Snowflake roles.

For a full overview of the Snowflake privilege model, see [Overview of Access Control](/user-guide/security-access-control-overview) and
[Access control privileges](/user-guide/security-access-control-privileges).

## Privilege quick reference

When a role creates a dynamic table, that role becomes the **owner**. Snowflake uses the owner role to run
background refreshes, so the owner role must keep USAGE and SELECT on all referenced objects at all times. If the
owner role loses these privileges, refreshes fail. For details, see
[Understand the owner-role refresh model](#label-dynamic-tables-privileges-owner-role-refresh).

Every operation on a dynamic table requires USAGE on the containing database, schema, and (for operations that run
queries) a warehouse. The examples below include these grants each time so you can copy any section independently.

The following table maps each operation to the required privilege:

| Operation | Required privilege | Granted on |
| --- | --- | --- |
| [Create a dynamic table](#label-dynamic-tables-privileges-create) | CREATE DYNAMIC TABLE | Schema |
| [Query a dynamic table](#label-dynamic-tables-privileges-select) | SELECT | Dynamic table |
| [Suspend, resume, refresh, or change warehouse/target lag](#label-dynamic-tables-privileges-operate) | OPERATE | Dynamic table |
| [View refresh history and scheduling state](#label-dynamic-tables-privileges-monitor) | MONITOR | Dynamic table |
| [Drop or rename a dynamic table](#label-dynamic-tables-privileges-ownership) | OWNERSHIP | Dynamic table |
| [Transfer ownership](#label-dynamic-tables-privileges-ownership) | OWNERSHIP | Dynamic table |

Expand

Show lessSee more

OWNERSHIP includes all capabilities of OPERATE and MONITOR.

## Grant privileges to create a dynamic table

To create a dynamic table, a role needs CREATE DYNAMIC TABLE on the schema, SELECT on every base table or view
referenced in the definition (the SELECT query), and USAGE on the database, schema, and refresh
warehouse.

Copy code

```
-- Grant a role the privileges to create dynamic tables in a schema
GRANT USAGE ON DATABASE mydb TO ROLE transform_role;
GRANT USAGE ON SCHEMA mydb.myschema TO ROLE transform_role;
GRANT CREATE DYNAMIC TABLE ON SCHEMA mydb.myschema TO ROLE transform_role;
GRANT SELECT ON TABLE mydb.myschema.raw_orders TO ROLE transform_role;
GRANT USAGE ON WAREHOUSE transform_wh TO ROLE transform_role;
```

After these grants, the role can create a dynamic table. For the full `dt_orders` definition, see [Create a dynamic table](/user-guide/dynamic-tables/create).

Note

If you create a dynamic table that depends on another dynamic table and you set INITIALIZE = ON\_CREATE, the creating
role also needs OPERATE on all upstream dynamic tables that are referenced directly in the definition, except those
referenced through [DYNAMIC\_TABLE\_REFRESH\_BOUNDARY()](/user-guide/dynamic-tables/data-consistency). This is not
required when using INITIALIZE = ON\_SCHEDULE.

- If you use INITIALIZE = ON\_SCHEDULE with a secondary role that has USAGE on the warehouse, the dynamic table
  won’t successfully refresh if the primary role lacks this privilege.

### Set up future grants

Grants on existing dynamic tables don’t apply to dynamic tables created later. Use FUTURE grants so that new dynamic
tables automatically inherit the correct privileges:

Copy code

```
GRANT SELECT ON FUTURE DYNAMIC TABLES IN SCHEMA mydb.myschema TO ROLE analyst_role;
GRANT MONITOR ON FUTURE DYNAMIC TABLES IN SCHEMA mydb.myschema TO ROLE ops_role;
```

These grants also apply to dynamic Iceberg tables. For more information, see
[Grant access with future grants](/user-guide/dynamic-tables/create-iceberg#label-dynamic-tables-create-iceberg-grants).

## Grant privileges to query a dynamic table

To read from a dynamic table without the ability to create one, a role needs SELECT on the dynamic table and USAGE on
the database, schema, and a query warehouse:

Copy code

```
GRANT USAGE ON DATABASE mydb TO ROLE analyst_role;
GRANT USAGE ON SCHEMA mydb.myschema TO ROLE analyst_role;
GRANT USAGE ON WAREHOUSE analytics_wh TO ROLE analyst_role;
GRANT SELECT ON DYNAMIC TABLE mydb.myschema.dt_orders TO ROLE analyst_role;
```

Note

When granting privileges on a dynamic table, specify the object type as DYNAMIC TABLE, not TABLE. Grants on TABLE
don’t apply to dynamic tables.

With these grants, the role can query the dynamic table like any other table:

Copy code

```
USE ROLE analyst_role;

SELECT order_id, product_name, line_total
FROM mydb.myschema.dt_orders
LIMIT 5;
```

```
+----------+--------------+------------+
| ORDER_ID | PRODUCT_NAME | LINE_TOTAL |
+----------+--------------+------------+
|     1001 | WIDGET A     |      89.97 |
|     1002 | WIDGET B     |      49.99 |
|     1003 | WIDGET A     |      59.98 |
|     1004 | GADGET X     |      62.50 |
+----------+--------------+------------+
```

To grant SELECT on every existing dynamic table in a schema at once:

Copy code

```
GRANT SELECT ON ALL DYNAMIC TABLES IN SCHEMA mydb.myschema TO ROLE analyst_role;
```

## Grant OPERATE to manage a dynamic table

The OPERATE privilege lets a role suspend, resume, and manually refresh a dynamic table without giving it full
OWNERSHIP. Grant OPERATE to roles that need to manage the refresh lifecycle, for example
`GRANT OPERATE ON DYNAMIC TABLE mydb.myschema.dt_orders TO ROLE pipeline_admin_role`.

With OPERATE, the role can suspend, resume, and trigger a manual refresh:

Copy code

```
USE ROLE pipeline_admin_role;

ALTER DYNAMIC TABLE mydb.myschema.dt_orders SUSPEND;
ALTER DYNAMIC TABLE mydb.myschema.dt_orders RESUME;
ALTER DYNAMIC TABLE mydb.myschema.dt_orders REFRESH;
```

OPERATE also allows changing the warehouse or target lag. Changing the warehouse requires USAGE on the new warehouse:

Copy code

```
GRANT USAGE ON WAREHOUSE transform_wh_xl TO ROLE pipeline_admin_role;

ALTER DYNAMIC TABLE mydb.myschema.dt_orders SET
  WAREHOUSE = transform_wh_xl
  TARGET_LAG = '5 minutes';
```

## Grant MONITOR to view metadata

The MONITOR privilege provides read-only access to operational metadata without the ability to alter the dynamic table.
Grant MONITOR to roles that need observability, for example
`GRANT MONITOR ON DYNAMIC TABLE mydb.myschema.dt_orders TO ROLE ops_role`.

With MONITOR, the role can view scheduling state in `SHOW DYNAMIC TABLES`, refresh history, and graph history:

Copy code

```
USE ROLE ops_role;

-- View scheduling state and configuration
SHOW DYNAMIC TABLES LIKE 'dt_orders' IN SCHEMA mydb.myschema;

-- View recent refresh history
SELECT name, state, refresh_trigger, refresh_action
FROM TABLE(INFORMATION_SCHEMA.DYNAMIC_TABLE_REFRESH_HISTORY(
  NAME => 'mydb.myschema.dt_orders',
  DATA_TIMESTAMP_START => DATEADD('hour', -1, CURRENT_TIMESTAMP())
));

-- View graph history for the current state of all dynamic tables
SELECT *
FROM TABLE(INFORMATION_SCHEMA.DYNAMIC_TABLE_GRAPH_HISTORY())
WHERE qualified_name = 'mydb.myschema.dt_orders';
```

Without MONITOR, the following fields are hidden when you query a dynamic table with only SELECT: `text`, `warehouse`,
`scheduling_state`, `last_suspended_on`, and `suspend_reason_code` (Snowsight only).

MONITOR is read-only: it can’t suspend, resume, or refresh the table.

## Grant OWNERSHIP to transfer full control

OWNERSHIP grants full control over a dynamic table, including the ability to drop/undrop, rename, swap, set comments, change
clustering keys, and manage governance policies. Only one role can hold OWNERSHIP at a time.

You can transfer ownership using SQL or Snowsight.

SQLSnowsight

Copy code

```
GRANT OWNERSHIP ON DYNAMIC TABLE mydb.myschema.dt_orders
  TO ROLE pipeline_admin_role;
```

To transfer ownership of all future dynamic tables in a schema:

Copy code

```
GRANT OWNERSHIP ON FUTURE DYNAMIC TABLES IN SCHEMA mydb.myschema
  TO ROLE pipeline_admin_role;
```

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Transformation** » **Dynamic tables**.
3. Find your dynamic table in the list and then select [![More options](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png) » **Transfer Ownership**.
4. Select the role to transfer ownership to.

## Understand the owner-role refresh model

Snowflake runs background refreshes using the dynamic table’s **owner role**. This means the owner role must retain
the following privileges at all times, or scheduled refreshes fail:

| Privilege | Object |
| --- | --- |
| SELECT | Every base table, view, or dynamic table referenced in the definition |
| USAGE | The databases and schemas containing those base objects |
| USAGE | The warehouse assigned to the dynamic table |

Expand

Show lessSee more

When you transfer ownership, the **new** owner role must already have these privileges. If it doesn’t, refreshes fail
and the dynamic table may be automatically suspended after repeated errors.

### Diagnose a privilege error after ownership transfer

If you transfer ownership to a role that lacks USAGE on the refresh warehouse, the next scheduled refresh fails:

Copy code

```
-- Transfer ownership to a role that lacks warehouse USAGE
GRANT OWNERSHIP ON DYNAMIC TABLE mydb.myschema.dt_orders
  TO ROLE new_owner_role;
```

The refresh fails with an error similar to:

```
SQL compilation error: Failed to refresh dynamic table with refresh_trigger SCHEDULED
at data_timestamp <ts> because of the error: SQL compilation error: Target table
failed to refresh: Dynamic Table 'MYDB.MYSCHEMA.DT_ORDERS' could not be refreshed
because warehouse 'TRANSFORM_WH' is missing.
```

To fix this, grant the missing privilege to the new owner role:

Copy code

```
GRANT USAGE ON WAREHOUSE transform_wh TO ROLE new_owner_role;
GRANT SELECT ON TABLE mydb.myschema.raw_orders TO ROLE new_owner_role;
GRANT USAGE ON DATABASE mydb TO ROLE new_owner_role;
GRANT USAGE ON SCHEMA mydb.myschema TO ROLE new_owner_role;
```

Then resume the dynamic table:

Copy code

```
ALTER DYNAMIC TABLE mydb.myschema.dt_orders RESUME;
```

## Refresh with specific user privileges (EXECUTE AS USER)

Most dynamic table setups don’t need EXECUTE AS USER. Read this section only if your dynamic tables use row-access
policies, masking policies, or need secondary roles for refresh.

By default, Snowflake refreshes a dynamic table as an internal SYSTEM user using the owner role. The EXECUTE AS USER
option changes this so that refreshes run on behalf of a named user. The primary role is still the dynamic table’s owner
role, but the named user’s secondary roles are also activated.

Use EXECUTE AS USER when:

- **Row-access or masking policies reference CURRENT\_USER().** The default SYSTEM user doesn’t match policy conditions.
  Setting EXECUTE AS USER causes CURRENT\_USER() to evaluate as the named user during refresh.
- **Secondary roles are needed.** The owner role alone can’t reach all required objects, but a user’s secondary roles
  can.
- **Audit attribution matters.** Refreshes are attributed to the named user instead of the SYSTEM user.

### Grant privileges for EXECUTE AS USER

The owner role must have IMPERSONATE on the target user, and the target user must hold the dynamic table’s owner role:

Copy code

```
-- Grant IMPERSONATE so the owner role can act on behalf of the service user
GRANT IMPERSONATE ON USER service_user TO ROLE transform_role;

-- The service user must also hold the owner role
GRANT ROLE transform_role TO USER service_user;
```

Then create or alter the dynamic table with the `EXECUTE AS USER` clause:

Copy code

```
CREATE OR REPLACE DYNAMIC TABLE mydb.myschema.dt_orders
  TARGET_LAG = '10 minutes'
  WAREHOUSE = transform_wh
  EXECUTE AS USER service_user
AS
  SELECT ... FROM mydb.myschema.raw_orders ...;
```

To grant the refresh access to all roles assigned to the specified user (not just the user’s
default role), add `USE SECONDARY ROLES ALL`:

Copy code

```
CREATE OR REPLACE DYNAMIC TABLE dt_orders
    TARGET_LAG = '10 minutes'
    WAREHOUSE = transform_wh
    EXECUTE AS USER service_user
        USE SECONDARY ROLES ALL
AS
    SELECT ... FROM raw_orders;
```

For the full `dt_orders` definition, see [Create a dynamic table](/user-guide/dynamic-tables/create).

To change the user on an existing dynamic table, run
`ALTER DYNAMIC TABLE <name> SET EXECUTE AS USER <user>`. To revert to the default SYSTEM user, run
`ALTER DYNAMIC TABLE <name> UNSET EXECUTE AS USER`.

Important

If the IMPERSONATE privilege is revoked after the dynamic table is created, refreshes fail and the dynamic table may be
automatically suspended.

### Cross-product considerations for EXECUTE AS USER

- **Data masking and row-access policies.** Policies that use CURRENT\_USER() evaluate as the named user, not the SYSTEM
  user.
- **Replication and failover.** The user name and role name are replicated to secondary deployments. If the user or
  role isn’t available on the secondary, the user is marked as INVALID and refreshes fail until the user and role are
  recreated.

## Privileges for dual warehouses

When using INITIALIZATION\_WAREHOUSE, all privilege requirements match those for WAREHOUSE. The role needs USAGE on both
warehouses:

| Operation | Required privilege |
| --- | --- |
| CREATE DYNAMIC TABLE with INITIALIZATION\_WAREHOUSE | CREATE DYNAMIC TABLE and USAGE on both WAREHOUSE and INITIALIZATION\_WAREHOUSE |
| ALTER DYNAMIC TABLE SET or UNSET INITIALIZATION\_WAREHOUSE | OWNERSHIP or OPERATE on the dynamic table and USAGE on the applicable warehouse |
| ALTER DYNAMIC TABLE REFRESH (with INITIALIZATION\_WAREHOUSE) | OPERATE on the dynamic table and USAGE on the applicable warehouse |

Expand

Show lessSee more

For more information, see [Choose and size warehouses for dynamic tables](/user-guide/dynamic-tables/warehouse-selection).

## What’s next

- To configure warehouses for refresh, see [Choose and size warehouses for dynamic tables](/user-guide/dynamic-tables/warehouse-selection).
- To monitor refresh health, see [Monitor dynamic tables](/user-guide/dynamic-tables/monitoring).
- To troubleshoot refresh failures, see [Troubleshoot dynamic table refresh issues](/user-guide/dynamic-tables/troubleshoot-refreshes).
- To revoke privileges, see [REVOKE <privileges> … FROM ROLE](/sql-reference/sql/revoke-privilege).
