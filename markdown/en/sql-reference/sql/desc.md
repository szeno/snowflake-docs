# DESCRIBE *<object>*

Describes the details for the specified object.

DESCRIBE can be abbreviated to DESC.

See also:
:   [CREATE <object>](/sql-reference/sql/create) , [SHOW <objects>](/sql-reference/sql/show)

## DESCRIBE commands

For specific syntax, usage notes, and examples, see:

**Session/Query Operations:**

> - [DESCRIBE RESULT](/sql-reference/sql/desc-result)
> - [DESCRIBE TRANSACTION](/sql-reference/sql/desc-transaction)

**Account Objects:**

> - [DESCRIBE APPLICATION](/sql-reference/sql/desc-application)
> - [DESCRIBE APPLICATION PACKAGE](/sql-reference/sql/desc-application-package)
> - [DESCRIBE CATALOG INTEGRATION](/sql-reference/sql/desc-catalog-integration)
> - [DESCRIBE COMPUTE POOL](/sql-reference/sql/desc-compute-pool)
> - [DESCRIBE DATABASE](/sql-reference/sql/desc-database)
> - [DESCRIBE EXTERNAL VOLUME](/sql-reference/sql/desc-external-volume)
> - [DESCRIBE INTEGRATION](/sql-reference/sql/desc-integration)
> - [DESCRIBE OPENFLOW DATA PLANE INTEGRATION](/sql-reference/sql/desc-oflow-data-plane-integration)
> - [DESCRIBE NETWORK POLICY](/sql-reference/sql/desc-network-policy)
> - [DESCRIBE NOTIFICATION INTEGRATION](/sql-reference/sql/desc-notification-integration)
> - [DESCRIBE ORGANIZATION PROFILE](/sql-reference/sql/desc-organization-profile)
> - [DESCRIBE POSTGRES INSTANCE](/sql-reference/sql/desc-postgres-instance)
> - [DESCRIBE SHARE](/sql-reference/sql/desc-share)
> - [DESCRIBE SPECIFICATION](/sql-reference/sql/desc-specification)
> - [DESCRIBE USER](/sql-reference/sql/desc-user)
> - [DESCRIBE WAREHOUSE](/sql-reference/sql/desc-warehouse)

**Database Objects:**

> - [DESCRIBE AGENT](/sql-reference/sql/desc-agent)
> - [DESCRIBE AGGREGATION POLICY](/sql-reference/sql/desc-aggregation-policy)
> - [DESCRIBE ALERT](/sql-reference/sql/desc-alert)
> - [DESCRIBE AUTHENTICATION POLICY](/sql-reference/sql/desc-authentication-policy)
> - [DESCRIBE BACKUP POLICY](/sql-reference/sql/desc-backup-policy)
> - [DESCRIBE BACKUP SET](/sql-reference/sql/desc-backup-set)
> - [DESCRIBE CONFIGURATION](/sql-reference/sql/desc-configuration)
> - [DESCRIBE CORTEX SEARCH SERVICE](/sql-reference/sql/desc-cortex-search)
> - [DESCRIBE DATA MOVEMENT POLICY](/sql-reference/sql/desc-data-movement-policy)
> - [DESCRIBE DATA MOVEMENT RULE](/sql-reference/sql/desc-data-movement-rule)
> - [DESCRIBE DBT PROJECT](/sql-reference/sql/desc-dbt-project)
> - [DESCRIBE DCM PROJECT](/sql-reference/sql/desc-dcm-project)
> - [DESCRIBE DYNAMIC TABLE](/sql-reference/sql/desc-dynamic-table)
> - [DESCRIBE EVENT TABLE](/sql-reference/sql/desc-event-table)
> - [DESCRIBE EXTERNAL AGENT](/sql-reference/sql/desc-external-agent)
> - [DESCRIBE EXTERNAL TABLE](/sql-reference/sql/desc-external-table)
> - [DESCRIBE FEATURE POLICY](/sql-reference/sql/desc-feature-policy)
> - [DESCRIBE FILE FORMAT](/sql-reference/sql/desc-file-format)
> - [DESCRIBE FUNCTION](/sql-reference/sql/desc-function)
> - [DESCRIBE GATEWAY](/sql-reference/sql/desc-gateway)
> - [DESCRIBE GIT REPOSITORY](/sql-reference/sql/desc-git-repository)
> - [DESCRIBE ICEBERG TABLE](/sql-reference/sql/desc-iceberg-table)
> - [DESCRIBE JOIN POLICY](/sql-reference/sql/desc-join-policy)
> - [DESCRIBE LISTING](/sql-reference/sql/desc-listing)
> - [DESCRIBE MAINTENANCE POLICY](/sql-reference/sql/desc-maintenance-policy)
> - [DESCRIBE MASKING POLICY](/sql-reference/sql/desc-masking-policy)
> - [DESCRIBE MATERIALIZED VIEW](/sql-reference/sql/desc-materialized-view)
> - [DESCRIBE MCP SERVER](/sql-reference/sql/desc-mcp-server)
> - [DESCRIBE MODEL MONITOR](/sql-reference/sql/desc-model-monitor)
> - [DESCRIBE NETWORK RULE](/sql-reference/sql/desc-network-rule)
> - [DESCRIBE NOTEBOOK](/sql-reference/sql/desc-notebook)
> - [DESCRIBE ONLINE FEATURE TABLE](/sql-reference/sql/desc-online-feature-table)
> - [DESCRIBE PACKAGES POLICY](/sql-reference/sql/desc-packages-policy)
> - [DESCRIBE PASSWORD POLICY](/sql-reference/sql/desc-password-policy)
> - [DESCRIBE PIPE](/sql-reference/sql/desc-pipe)
> - [DESCRIBE PRIVACY POLICY](/sql-reference/sql/desc-privacy-policy)
> - [DESCRIBE PROCEDURE](/sql-reference/sql/desc-procedure)
> - [DESCRIBE PROJECTION POLICY](/sql-reference/sql/desc-projection-policy)
> - [DESCRIBE RESTRICTED SESSION SCOPE](/sql-reference/sql/desc-restricted-session-scope)
> - [DESCRIBE ROW ACCESS POLICY](/sql-reference/sql/desc-row-access-policy)
> - [DESCRIBE SCHEMA](/sql-reference/sql/desc-schema)
> - [DESCRIBE SECRET](/sql-reference/sql/desc-secret)
> - [DESCRIBE SEMANTIC VIEW](/sql-reference/sql/desc-semantic-view)
> - [DESCRIBE SEQUENCE](/sql-reference/sql/desc-sequence)
> - [DESCRIBE SERVICE](/sql-reference/sql/desc-service)
> - [DESCRIBE SESSION POLICY](/sql-reference/sql/desc-session-policy)
> - [DESCRIBE SNAPSHOT](/sql-reference/sql/desc-snapshot)
> - [DESCRIBE SNAPSHOT POLICY](/sql-reference/sql/desc-snapshot-policy) (deprecated; prefer [DESCRIBE BACKUP POLICY](/sql-reference/sql/desc-backup-policy))
> - [DESCRIBE SNAPSHOT SET](/sql-reference/sql/desc-snapshot-set) (deprecated; prefer [DESCRIBE BACKUP SET](/sql-reference/sql/desc-backup-set))
> - [DESCRIBE SPECIFICATION](/sql-reference/sql/desc-specification)
> - [DESCRIBE STAGE](/sql-reference/sql/desc-stage)
> - [DESCRIBE STORAGE LIFECYCLE POLICY](/sql-reference/sql/desc-storage-lifecycle-policy)
> - [DESCRIBE STREAMLIT](/sql-reference/sql/desc-streamlit)
> - [DESCRIBE STREAM](/sql-reference/sql/desc-stream)
> - [DESCRIBE TABLE](/sql-reference/sql/desc-table)
> - [DESCRIBE TASK](/sql-reference/sql/desc-task)
> - [DESCRIBE TYPE](/sql-reference/sql/desc-type)
> - [DESCRIBE VIEW](/sql-reference/sql/desc-view)
