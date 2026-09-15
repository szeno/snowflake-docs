# Apr 2, 2026: Performance Explorer granular access aligned with your privileges

Performance Explorer now applies granular access control that aligns visibility with your privileges on
warehouses, databases, and [Snowflake database roles](/sql-reference/snowflake-db-roles) in the
shared `SNOWFLAKE` database. Snowflake grants the `SNOWFLAKE.PERFORMANCE_EXPLORER_PUBLIC_USER`
application role to the `PUBLIC` role so that more users can open Performance Explorer; charts and tables
show account activity that your roles are allowed to see, and some sections require elevated privileges
(such as `GOVERNANCE_VIEWER` for table-level metrics).

Users who have full account visibility today keep it if **any** role granted to them is
[ACCOUNTADMIN](/user-guide/security-access-control-overview#label-access-control-overview-roles-system), has `IMPORTED PRIVILEGES` on the
`SNOWFLAKE` database, or has the `SNOWFLAKE.PERFORMANCE_EXPLORER_USER` application role.

Privilege changes can take a few hours to appear in Performance Explorer.

For more information, see [Analyzing query workloads with Performance Explorer](/user-guide/performance-explorer) and
[Required privileges for Performance Explorer](/user-guide/performance-explorer#label-performance-explorer-required-privileges).
