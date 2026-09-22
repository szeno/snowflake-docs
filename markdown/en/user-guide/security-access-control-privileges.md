# Access control privileges

This topic describes the privileges that are available in the Snowflake access control model. Privileges are granted to roles, and roles are
granted to users, to specify the operations that the users can perform on objects in the system.

Tip

To obtain a definitive list of all possible privileges for one or more objects, call the
[EXPLAIN\_GRANTABLE\_PRIVILEGES](/sql-reference/functions/explain_grantable_privileges) function.

## All privileges (alphabetical)

The following privileges are available in the Snowflake access control model. The meaning of each privilege varies depending on the object type
to which it is applied, and not all objects support all privileges:

| Privilege | Object Type | Description |
| --- | --- | --- |
| ALL [ PRIVILEGES ] | All | Grants all the privileges for the specified object type. |
| APPLY | Policy, Tag | Grants the ability to assign a policy or tag to an object that can be tagged or protected by a policy. |
| APPLYBUDGET | Database, Schema, Table, event table, hybrid table, Apache Iceberg™ table, Warehouse, Task, Pipe, Materialized View | Grants the ability to add or remove an object to or from a [budget](/user-guide/budgets). |
| APPLY AGGREGATION POLICY | Global | Grants the ability to add and drop an aggregation policy on a table or view. |
| APPLY AUTHENTICATION POLICY | Global | Grants the ability to add or drop an authentication policy on the Snowflake account or a user in the Snowflake account. |
| APPLY BACKUP POLICY | Global | Grants the ability to add [backup](/user-guide/backups) policies to backup sets that don’t already have a policy. This privilege is granted to the ACCOUNTADMIN role and can be delegated. |
| APPLY BACKUP RETENTION LOCK | Global | Grants the ability to create and apply [backup](/user-guide/backups) policies with retention lock. This privilege is granted to the ACCOUNTADMIN role and can be delegated. |
| APPLY CONTACT | Global | Grants the ability to associate or detach a [contact](/user-guide/contacts-using) with an object. |
| APPLY DATA MOVEMENT POLICY | Global | Grants the ability to set a [data movement policy](/user-guide/data-movement-policies) on a tag or on the account. |
| APPLY FEATURE POLICY | Global | Grants the ability to apply a feature policy for an account or on a specific object. |
| APPLY JOIN POLICY | Global | Grants the ability to add and drop a join policy on a table or view. |
| APPLY LEGAL HOLD | Global | Grants the ability to add and remove legal holds from [WORM backups](/user-guide/backups) for Snowflake databases, schemas, and tables. |
| APPLY MASKING POLICY | Global | Grants the ability to set a Column-level Security masking policy on a table or view column and to set a masking policy on a tag. This global privilege also allows executing the DESCRIBE operation on tables and views. |
| APPLY PACKAGES POLICY | Global | Grants the ability to add or drop a packages policy on the Snowflake account. |
| APPLY PASSWORD POLICY | Global | Grants the ability to add or drop a password policy on the Snowflake account or a user in the Snowflake account. |
| APPLY PRIVACY POLICY | Global | Grants the ability to add and drop a privacy policy on a table or view. |
| APPLY PROJECTION POLICY | Global | Grants the ability to add and drop a projection policy on a table or view. |
| APPLY ROW ACCESS POLICY | Global | Grants the ability to add and drop a row access policy on a table or view. This global privilege also allows executing the DESCRIBE operation on tables and views. |
| APPLY SESSION POLICY | Global | Grants the ability to set or unset a session policy on an account or user. |
| APPLY SNAPSHOT RETENTION LOCK — *Deprecated* | Global | Grants the ability to create and apply [snapshot](/user-guide/backups) policies with retention lock. This privilege is granted to the ACCOUNTADMIN role and can be delegated. Deprecated: use APPLY BACKUP RETENTION LOCK instead. |
| APPLY STORAGE LIFECYCLE POLICY | Global | Grants the ability to add or drop a [storage lifecycle policy](/user-guide/storage-management/storage-lifecycle-policies) on a table. This global privilege also allows executing the DESCRIBE operation on all storage lifecycle policies. |
| APPLY TAG | Global | Grants the ability to add or drop a tag on a Snowflake object. |
| ATTACH POLICY | Global | Grants the ability to activate a network policy by associating it with your account. |
| AUDIT | Global | Grants the ability to set the [ENABLE\_UNREDACTED\_QUERY\_SYNTAX\_ERROR](/sql-reference/parameters#label-enable-unredacted-query-syntax-error) and [ENABLE\_UNREDACTED\_SECURE\_OBJECT\_ERROR](/sql-reference/parameters#label-enable-unredacted-secure-object-error) user parameters. |
| BIND SERVICE ENDPOINT | Global | Enables the ability to create a service that supports public endpoints. For more information about public endpoints, see [Ingress: Using a service from outside Snowflake](/developer-guide/snowpark-container-services/working-with-services#label-snowpark-containers-service-communicating-ingress). |
| CANCEL QUERY | Global | Grants the ability to cancel queries executed by any user in the account. |
| CREATE *<object\_type>* | Global, Database, Schema | Grants the ability to create an object of *<object\_type>* (e.g. CREATE TABLE grants the ability to create a table within a schema). |
| DELETE | Table, event table, hybrid table, Iceberg table | Grants the ability to execute a [DELETE](/sql-reference/sql/delete) command on the table. |
| DROP | Service | Grants the ability to drop a Snowpark Container Services service. |
| EVOLVE SCHEMA | Table | Grants the ability for [schema evolution](/user-guide/data-load-schema-evolution) to occur on a table when loading data. |
| EXECUTE ALERT | Global | Grants the ability to execute alerts owned by the role. For serverless alerts to run, the role that has the OWNERSHIP privilege on the alert must also have the global EXECUTE MANAGED ALERT privilege. |
| EXECUTE AUTO CLASSIFICATION | Global, Database, Schema | Grants the ability to set a classification profile on a database or schema to implement [sensitive data classification](/user-guide/classify-intro). |
| EXECUTE DATA METRIC FUNCTION | Global | Enables using serverless compute resources when calling a data metric function. |
| EXECUTE MANAGED ALERT | Global | Grants the ability to create alerts that rely on serverless compute resources. Only required to create serverless alerts. The role that has the OWNERSHIP privilege on a serverless alert must have both the EXECUTE MANAGED ALERT and the EXECUTE ALERT privilege for the alert to run. |
| EXECUTE MANAGED TASK | Global | Grants the ability to create tasks that rely on serverless compute resources. Only required to create serverless tasks. The role that has the OWNERSHIP privilege on a task must have both the EXECUTE MANAGED TASK and the EXECUTE TASK privilege for the task to run. |
| EXECUTE TASK | Global | Grants the ability to run tasks owned by the role. For serverless tasks to run, the role that has the OWNERSHIP privilege on the task must also have the global EXECUTE MANAGED TASK privilege. |
| FAILOVER | Failover Group, Connection | Grants the ability to promote a secondary failover group or secondary connection to serve as the primary. |
| IMPORT ORGANIZATION LISTING | Global | Enables a consumer to install an organizational listing, or to query an organizational listing without installing it. |
| IMPORT ORGANIZATION USER GROUPS | Global | Grants the ability to add an [organization user group](/user-guide/organization-users#label-org-users-groups) to a regular account, which imports users into the account. |
| IMPORT SHARE | Global | Applies to data consumers. Grants the ability to view shares shared with your account. Also grants the ability to create databases from the shares; requires the global CREATE DATABASE privilege. |
| OVERRIDE SHARE RESTRICTIONS | Global | Grants the ability to set value for the SHARE\_RESTRICTIONS parameter on a share. For more details, see [Direct share restrictions](/user-guide/direct-share-restrictions). |
| IMPERSONATE | User | Runs a task or dynamic table on behalf of a specified user account. |
| IMPORTED PRIVILEGES | Database, Data Exchange | Grants the ability to enable roles other than the owning role to access a shared database or manage a Snowflake Marketplace / Data Exchange. |
| INGEST TELEMETRY | Event table | Grants the ability to ingest telemetry data into an event table. |
| INSERT | Table, hybrid table, Iceberg table | Grants the ability to execute an [INSERT](/sql-reference/sql/insert) command on the table. |
| MANAGE ACCOUNT SUPPORT CASES | Global | Grants the ability to view, comment on, and manage all Support cases for the current account in Snowsight. |
| MANAGE ACCOUNTS | Global | Grants the ability to manage the lifecycle of accounts in an organization. |
| MANAGE APPLICATION SPECIFICATIONS | Global | Grants the ability to approve app specifications. |
| MANAGE CALLER GRANTS | Global | Grants the ability to manage [caller grants](/developer-guide/restricted-callers-rights) in the account. |
| MANAGE GRANTS | Global, Database, Schema | Grants the ability to grant or revoke privileges on any object as if the invoking role were the owner of the object. When granted on a database or schema, the ability is limited to that container and the objects in it. For details, see [Delegating grant management with container-level MANAGE GRANTS](/user-guide/container-manage-grants-intro). |
| MANAGE LISTING AUTO FULFILLMENT | Global | Grants the ability to publish listings to remote regions using [Cross-Cloud Auto-Fulfillment](/collaboration/provider-listings-auto-fulfillment) and manage auto-fulfillment settings for listings. |
| MANAGE ORGANIZATION ACCESS | Global | Grants the ability to manage organizational access to a given account. |
| MANAGE ORGANIZATION CONTACTS | Global | Grants the ability to manage the contacts for an organization. |
| MANAGE ORGANIZATION SUPPORT CASES | Global | Grants the ability to view, comment on, and manage all Support cases that were opened by the current user in Snowsight. |
| MANAGE ORGANIZATION TERMS | Global | Grants the ability to manage the legal terms for an organization. |
| MANAGE ORGANIZATION USERS | Global | Grants the ability to manage [organization users](/user-guide/organization-users). |
| MANAGE ORGANIZATION USER GROUPS | Global | Grants the ability to manage [organization user groups](/user-guide/organization-users#label-org-users-groups). |
| MANAGE SERVICE CALLER ACCESS | Global | Grants the ability to set the [SERVICE\_CALLER\_TOKEN\_VALIDITY\_SECS](/sql-reference/parameters#service-caller-token-validity-secs) parameter, which controls the lifetime of caller’s rights login tokens for Snowpark Container Services. |
| MANAGE SHARE TARGET | Global | Grants the ability to manage (ALTER) share targets. |
| MANAGE USER SUPPORT CASES | Global | Grants the ability to view, comment on, and manage all Support cases for the current user in Snowsight. |
| MANAGE VISIBILITY | Global | Grants the ability to set the OBJECT\_VISIBILITY property, which controls the [discoverability of the objects](/user-guide/ui-snowsight/object-visibility-universal-search) in the account. |
| MANAGE WAREHOUSES | Global | Grants the ability to perform operations that require the [MODIFY, MONITOR, and OPERATE privileges on warehouses](#label-warehouse-privileges) in the same account. |
| MODIFY | Resource Monitor, Warehouse, Data Exchange Listing, Database, Schema, Failover Group, Replication Group, Compute Pool | Grants the ability to change the settings or properties of an object (for example, on a virtual warehouse, provides the ability to change the size of a virtual warehouse). |
| MODIFY EVENT TABLE | Global | Grants the ability to set the [EVENT\_TABLE](/sql-reference/parameters#label-event-table) parameter on any object in the account. |
| MODIFY LOG EVENT LEVEL | Global | Enables setting the level of log events captured for stored procedures and UDFs in the current account. For more information, see [LOG\_EVENT\_LEVEL](/sql-reference/parameters#label-log-event-level). |
| MODIFY LOG LEVEL | Global | Enables setting the level of log messages captured for stored procedures and UDFs in the current account. For more information, see [LOG\_LEVEL](/sql-reference/parameters#label-log-level). |
| MODIFY METRIC LEVEL | Global | Enables setting the level of metrics data captured for stored procedures and UDFs in the current account. For more information, see [METRIC\_LEVEL](/sql-reference/parameters#label-metric-level). |
| MODIFY PROGRAMMATIC AUTHENTICATION METHODS | User | Grants the ability to create, modify, delete, rotate, and view information about the [programmatic access tokens](/user-guide/programmatic-access-tokens) and [key pairs](/user-guide/key-pair-auth) for the user. |
| MODIFY SESSION LOG EVENT LEVEL | Global | Enables setting the level of log events captured for stored procedures and UDFs invoked in the current session. For more information, see [LOG\_EVENT\_LEVEL](/sql-reference/parameters#label-log-event-level). |
| MODIFY SESSION LOG LEVEL | Global | Enables setting the level of log messages captured for stored procedures and UDFs invoked in the current session. For more information, see [LOG\_LEVEL](/sql-reference/parameters#label-log-level). |
| MODIFY SESSION METRIC LEVEL | Global | Enables setting the level of metrics data captured for stored procedures and UDFs invoked in the current session. For more information, see [METRIC\_LEVEL](/sql-reference/parameters#label-metric-level). |
| MODIFY SESSION TRACE LEVEL | Global | Enables setting the level of trace events captured for stored procedures and UDFs invoked in the current session. When tracing events, you must also set the LOG\_LEVEL parameter to one of its supported values. For more information, see [TRACE\_LEVEL](/sql-reference/parameters#label-trace-level). |
| MODIFY TRACE LEVEL | Global | Enables setting the level of trace events captured for stored procedures and UDFs in the current account. When tracing events, you must also set the LOG\_LEVEL parameter to one of its supported values. For more information, see [TRACE\_LEVEL](/sql-reference/parameters#label-trace-level). |
| MONITOR | User, Resource Monitor, Warehouse, Database, Schema, Task, Failover Group, Replication Group, Alert, Compute Pool, Service, Dynamic Table, Semantic View, Snowflake Native App, Agent, dbt Projects on Snowflake | Grants the ability to see details within an object (for example, queries and usage within a warehouse).     For semantic views, the MONITOR privilege also allows you to view Cortex Analyst [monitoring and observability data](/user-guide/snowflake-cortex/cortex-analyst/admin-observability). |
| MONITOR EXECUTION | Global | Grants the ability to monitor pipes (Snowpipe) or tasks in the account. |
| MONITOR ROLE | Global | Grants the ability to view roles in the account. |
| MONITOR SECURITY | Global | Grants the ability to call system functions pertaining to [Customer-managed keys](/user-guide/security-encryption-manage#label-customer-managed-keys). |
| MONITOR USAGE | Global | Grants the ability to monitor account-level usage and historical information for databases and warehouses; for more details, see [Enabling non-account administrators to monitor usage and billing history](/user-guide/security-access-control-configure#label-allow-other-users-to-monitor-usage-billing-history). Additionally grants the ability to view managed accounts using [SHOW MANAGED ACCOUNTS](/sql-reference/sql/show-managed-accounts). |
| MONITOR USER | Global | Grants the ability to view users and all their properties in the account. |
| OPERATE | Warehouse, Task, Dynamic table, Alert, Compute Pool, Service | Grants the ability to start, stop, suspend, or resume a virtual warehouse. Grants the ability to suspend or resume a task. Grants the ability to suspend, resume, or refresh a dynamic table. Grants the ability to suspend or resume a compute pool. Grants the ability to suspend or resume a Snowpark Container Services service, upgrade service, set, and unset service properties. |
| OWNERSHIP | All | Grants the ability to drop, alter, and grant or revoke access to an object. Required to rename an object and create a temporary object with the same name as the object itself. OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role or any role with the MANAGE GRANTS privilege. |
| PURCHASE DATA EXCHANGE LISTING | Global | Grants the ability to purchase a paid listing. |
| READ | Stage (internal only), Compute Pool, Git Repository, Image Repository | Grants the ability to perform any operations that require reading from an internal stage ([GET](/sql-reference/sql/get), [LIST](/sql-reference/sql/list), [COPY INTO <table>](/sql-reference/sql/copy-into-table), etc.). Grants the ability to download an image from an image repository. READ privilege on stage and image repository is required to create a Snowpark Container Services service. For models, READ grants the ability to run inference methods along with read-only access to the model’s underlying artifacts and metadata. |
| READ SESSION | Global | Grants the ability to read session context. |
| READ UNREDACTED AI OBSERVABILITY EVENTS TABLE | Global | Grants the ability to read the unredacted data in an AI observability events table. |
| READ UNREDACTED ERROR TABLE | Global | Grants the ability to read the unredacted data in an error table. Required when the error table is associated with a base table that has security policies, such as a [masking policy](/user-guide/security-column-intro). For more information about error tables, see [DML error logging](/user-guide/data-load-overview#label-data-load-overview-dml-error-logging). |
| REFERENCES | Table, event table, hybrid table, Iceberg table, external table, interactive table, view, materialized view, semantic view | Grants the ability to view the structure of an object (but not the data).     For tables, the privilege also grants the ability to reference the object as the unique/primary key table for a foreign key constraint. |
| REPLICATE | Global, Replication Group, Failover Group | At the account level, grants the ability to change the REPLICABLE\_WITH\_FAILOVER\_GROUPS setting for databases and schemas. For replication groups and failover groups, grants the ability to refresh a secondary replication or failover group. |
| RESOLVE ALL | Global | Grants the ability to resolve all objects in the account, which outputs the object in the corresponding [SHOW <objects>](/sql-reference/sql/show) command. |
| SELECT | Table, hybrid table, Iceberg table, event table, external table, interactive table, view, materialized view, semantic view, stream | Grants the ability to execute a [SELECT](/sql-reference/sql/select) statement on the table/view. |
| SELECT ERROR TABLE | Table | Grants the ability to execute a [SELECT](/sql-reference/sql/select) statement on the error table associated with a base table. For more information, see [DML error logging](/user-guide/data-load-overview#label-data-load-overview-dml-error-logging). |
| TRUNCATE | Table, hybrid table, event table, Iceberg table | Grants the ability to execute a [TRUNCATE TABLE](/sql-reference/sql/truncate-table) command on the table. |
| UPDATE | Table, hybrid table, Iceberg table | Grants the ability to execute an [UPDATE](/sql-reference/sql/update) command on the table. |
| USE AI FUNCTION <name> | Global | Grants the ability to use a specific Snowflake Cortex AI function (for example, `GRANT USE AI FUNCTION AI_COMPLETE ON ACCOUNT`). For the list of supported per-function privilege names, see [USE AI FUNCTION <name> — per-function privileges](/user-guide/snowflake-cortex/aisql-privileges-and-access#label-cortex-ai-function-per-function-privileges). |
| USE AI FUNCTIONS | Global | Grants the ability to use Snowflake Cortex AI Functions. Users need both the USE AI FUNCTIONS account privilege and the CORTEX\_USER database role to use all Snowflake Cortex AI Functions. For more information, see [Snowflake Cortex AI Functions (including LLM functions)](/user-guide/snowflake-cortex/aisql). |
| USAGE | Warehouse, Dataset, Data Exchange Listing, Integration, Database, Schema, Stage (external only), File Format, Sequence, Stored Procedure, User-Defined Types, User-Defined Function, External Function, Compute Pool, Snapshot, Backup Policy, Backup Set, Model, dbt project object, Agent, MCP Server | Grants the ability to execute a [USE <object>](/sql-reference/sql/use) command on the object. Also grants the ability to execute a [SHOW <objects>](/sql-reference/sql/show) command on the object. Usage on a compute pool is required to create a Snowpark Container Services service. For models, USAGE grants the ability to run inference methods. It doesn’t grant access to the model’s underlying artifacts. For dbt Projects on Snowflake, grants the ability to SHOW, DESCRIBE, view execution history, and execute the dbt project object. |
| VIEW LINEAGE | Global | Grants the [ability to view data lineage](/user-guide/ui-snowsight-lineage), including upstream and downstream lineage objects and dependencies. |
| WRITE | Stage (internal only), image repository, Git Repository | Grants the ability to perform any operations that require writing to an internal stage ([PUT](/sql-reference/sql/put), [REMOVE](/sql-reference/sql/remove), [COPY INTO <location>](/sql-reference/sql/copy-into-location), etc.). Grants the ability to upload an image to an image repository. |

Expand

Show lessSee more

The remaining sections in this topic describe the specific privileges available for each type of object and their usage.

## Global privileges (account privileges)

| Privilege | Usage | Notes |
| --- | --- | --- |
| APPLY AGGREGATION POLICY | Grants the ability to add and drop an aggregation policy on a table or view. | This global privilege also allows executing the DESCRIBE operation on tables and views. |
| APPLY AUTHENTICATION POLICY | Grants the ability to add or drop an authentication policy on the Snowflake account or a user in the Snowflake account. |  |
| APPLY BACKUP RETENTION LOCK | Grants the ability to create and apply backup policies with retention lock. This privilege is granted to the ACCOUNTADMIN role and can be delegated. |  |
| APPLY CONTACT | Grants the ability to associate or detach a [contact](/user-guide/contacts-using) with an object. |  |
| APPLY DATA MOVEMENT POLICY | Grants the ability to set a [data movement policy](/user-guide/data-movement-policies) on a tag or on the account. |  |
| APPLY FEATURE POLICY | Grants the ability to apply a feature policy for an account or on a specific object. |  |
| APPLY JOIN POLICY | Grants the ability to add and drop a join policy on a table or view. | This global privilege also allows executing the DESCRIBE operation on tables and views. |
| APPLY MASKING POLICY | Grants the ability to set a Column-level Security masking policy on a table or view column and to set a masking policy on a tag. | This global privilege also allows executing the DESCRIBE operation on tables and views. |
| APPLY ROW ACCESS POLICY | Grants the ability to add and drop a row access policy on a table or view. | This global privilege also allows executing the DESCRIBE operation on tables and views. |
| APPLY PACKAGES POLICY | Grants the ability to add or drop a packages policy on the Snowflake account. |  |
| APPLY PASSWORD POLICY | Grants the ability to add or drop a password policy on the Snowflake account or a user in the Snowflake account. |  |
| APPLY PRIVACY POLICY | Grants the ability to add and drop a privacy policy on a table or view. | This global privilege also allows executing the DESCRIBE operation on tables and views. |
| APPLY PROJECTION POLICY | Grants the ability to add and drop a projection policy on a table or view. | This global privilege also allows executing the DESCRIBE operation on tables and views. |
| APPLY SESSION POLICY | Grants the ability to set or unset a session policy on an account or user. |  |
| APPLY SNAPSHOT RETENTION LOCK — *Deprecated* | Grants the ability to create and apply snapshot policies with retention lock. This privilege is granted to the ACCOUNTADMIN role and can be delegated.     Deprecated: use APPLY BACKUP RETENTION LOCK instead. |  |
| APPLY STORAGE LIFECYCLE POLICY | Grants the ability to add or drop a [storage lifecycle policy](/user-guide/storage-management/storage-lifecycle-policies) on a table. This privilege also allows executing the DESCRIBE operation on all storage lifecycle policies.     Global privileges aren’t required to use storage lifecycle policies. |  |
| APPLY TAG | Grants the ability to add or drop a tag on a Snowflake object. |  |
| ATTACH POLICY | Grants the ability to activate a network policy by associating it with your account. |  |
| AUDIT | Grants the ability to set the [ENABLE\_UNREDACTED\_QUERY\_SYNTAX\_ERROR](/sql-reference/parameters#label-enable-unredacted-query-syntax-error) and [ENABLE\_UNREDACTED\_SECURE\_OBJECT\_ERROR](/sql-reference/parameters#label-enable-unredacted-secure-object-error) user parameters. |  |
| BIND SERVICE ENDPOINT | Enables the ability to create a service that supports public endpoints. For more information about public endpoints, see [Ingress: Using a service from outside Snowflake](/developer-guide/snowpark-container-services/working-with-services#label-snowpark-containers-service-communicating-ingress) | Must be granted by the ACCOUNTADMIN role. |
| CANCEL QUERY | Grants the ability to cancel queries executed by any user in the account. |  |
| CREATE AGENT | Enables creating a new Cortex Agent. |  |
| CREATE ACCOUNT | Enables a data provider to create a new managed account (i.e. reader account). For more details, see [Manage reader accounts](/user-guide/data-sharing-reader-create). | Must be granted by the ACCOUNTADMIN role. |
| CREATE APPLICATION | Enables creating a new [Snowflake Native App](/developer-guide/native-apps/native-apps-about) from an application package or listing. | Must be granted by the ACCOUNTADMIN role. |
| CREATE APPLICATION PACKAGE | Enables creating a new [application package](/developer-guide/native-apps/creating-app-package) to develop a Snowflake Native App. | Must be granted by the ACCOUNTADMIN role. |
| CREATE PREVIEW APPLICATION | Enables creating a Snowflake Native App from a non-default release channel (`QA` or `ALPHA`). Not required when installing from the `DEFAULT` release channel. | Must be granted by the ACCOUNTADMIN role. |
| CREATE COMPUTE POOL | Enables creating a compute pool to run a Snowpark Container Services service. | Must be granted by the ACCOUNTADMIN role. |
| CREATE DATABASE | Enables creating a new [database](/guides-overview-db). | Must be granted by the ACCOUNTADMIN role. |
| CREATE DATA CONNECTIVITY PROXY | Enables creating a [Data Connectivity Proxy](/user-guide/data-connectivity-proxy) object so Snowflake can reach private data sources through an outbound agent tunnel. | Must be granted by the ACCOUNTADMIN role. |
| CREATE EXTERNAL VOLUME | Enables creating a new external volume for [Apache Iceberg™ tables](/user-guide/tables-iceberg). |  |
| CREATE EXTERNAL ACCESS INTEGRATION | Grants a Snowflake Native App the ability to create an external access integration. |  |
| CREATE FEATURE POLICY | Enables creating a new feature policy. |  |
| CREATE FAILOVER GROUP | Enables creating a new [failover group](/user-guide/account-replication-intro#label-replication-and-failover-groups). | Must be granted by the ACCOUNTADMIN role. |
| CREATE GATEWAY | Enables creating a new gateway. |  |
| CREATE REPLICATION GROUP | Enables creating a new [replication group](/user-guide/account-replication-intro#label-replication-and-failover-groups). | Must be granted by the ACCOUNTADMIN role. |
| CREATE ROLE | Enables creating a new role. |  |
| CREATE USER | Enables creating a new user. |  |
| CREATE LISTING | Enables creating a new Data Exchange listing. | Must be granted by the ACCOUNTADMIN role. |
| CREATE INTEGRATION | Enables creating an integration of any type. To let a role create only one type of integration, grant the corresponding granular privilege instead, such as CREATE NOTIFICATION INTEGRATION or CREATE STORAGE INTEGRATION. | Must be granted by the ACCOUNTADMIN role. |
| CREATE NOTIFICATION INTEGRATION | Enables creating a new notification integration. This privilege does not grant the ability to create other types of integrations. | Must be granted by the ACCOUNTADMIN role. |
| CREATE STORAGE INTEGRATION | Enables creating a new storage integration. This privilege does not grant the ability to create other types of integrations. | Must be granted by the ACCOUNTADMIN role. |
| CREATE NETWORK POLICY | Enables creating a new network policy. |  |
| CREATE ORGANIZATION LISTING | Enables creating a new organization listing. |  |
| CREATE ORGANIZATION PROFILE | Enables creating a new organization profile. |  |
| CREATE ORGANIZATION USER | Enables creating a new [organization user](/user-guide/organization-users). | Must be granted by the GLOBALORGADMIN role in the organization account. |
| CREATE ORGANIZATION USER GROUP | Enables creating a new [organization user group](/user-guide/organization-users#label-org-users-groups). | Must be granted by the GLOBALORGADMIN role in the organization account. |
| CREATE SECURITY INTEGRATION | Grants a Snowflake Native App the ability to create a security integration. |  |
| CREATE SHARE | Enables a data provider to create a new share. For more details, see [Enable non-ACCOUNTADMIN roles to perform data sharing tasks](/user-guide/security-access-privileges-shares). | Must be granted by the ACCOUNTADMIN role. |
| CREATE WAREHOUSE | Enables creating a new virtual warehouse. | Must be granted by the ACCOUNTADMIN role. |
| EXECUTE ALERT | Grants the ability to execute alerts owned by the role. For serverless alerts to run, the role that has the OWNERSHIP privilege on the alert must also have the global EXECUTE MANAGED ALERT privilege. | Must be granted by the ACCOUNTADMIN role. |
| EXECUTE AUTO CLASSIFICATION | Grants the ability to set a classification profile on a schema to implement [sensitive data classification](/user-guide/classify-intro). | Must be granted by the ACCOUNTADMIN role. |
| EXECUTE DATA METRIC FUNCTION | Enables using serverless compute resources when calling a data metric function. |  |
| EXECUTE MANAGED ALERT | Grants the ability to create alerts that rely on serverless compute resources. Only required to create serverless alerts. The role that has the OWNERSHIP privilege on a serverless alert must have both the EXECUTE MANAGED ALERT and the EXECUTE ALERT privilege for the alert to run. |  |
| EXECUTE MANAGED TASK | Grants the ability to create tasks that rely on serverless compute resources. Only required for serverless tasks. The role that has the OWNERSHIP privilege on a task must have both the EXECUTE MANAGED TASK and the EXECUTE TASK privilege for the task to run. | Must be granted by the ACCOUNTADMIN role. |
| EXECUTE TASK | Grants the ability to run tasks owned by the role. For serverless tasks to run, the role that has the OWNERSHIP privilege on the task must also have the global EXECUTE MANAGED TASK privilege. | Must be granted by the ACCOUNTADMIN role. |
| IMPORT SHARE | Enables a data consumer to view shares shared with their account. Also grants the ability to create databases from shares; requires the global CREATE DATABASE privilege. For more details, see [Enable non-ACCOUNTADMIN roles to perform data sharing tasks](/user-guide/security-access-privileges-shares). | Must be granted by the ACCOUNTADMIN role. |
| IMPORT ORGANIZATION LISTING | Enables a consumer to install an organizational listing, or to query an organizational listing without installing it. |  |
| IMPORT ORGANIZATION USER GROUPS | Grants the ability to add an [organization user group](/user-guide/organization-users#label-org-users-groups) to a regular account, which imports users into the account. | Must be granted by the ACCOUNTADMIN role. |
| MANAGE ACCOUNTS | Grants the ability to manage the lifecycle of accounts (for example, creating and deleting). | Must be granted by the GLOBALORGADMIN role in the [organization account](/user-guide/organization-accounts). |
| MANAGE ACCOUNT SUPPORT CASES | Grants the ability to view, comment on, and manage all Support cases for the current account in Snowsight. |  |
| MANAGE APPLICATION SPECIFICATIONS | Grants the ability to approve app specifications. |  |
| MANAGE CALLER GRANTS | Grants the ability to manage [caller grants](/developer-guide/restricted-callers-rights) in the account. |  |
| MANAGE GRANTS | Enables granting or revoking privileges on objects for which the role is not the owner. MANAGE GRANTS can also be granted on a database or schema to limit the ability to that container; see [Delegating grant management with container-level MANAGE GRANTS](/user-guide/container-manage-grants-intro). | Must be granted by a role that holds MANAGE GRANTS WITH GRANT OPTION on the account or, for a database or schema, on that container or a higher container. The SECURITYADMIN role holds account-level MANAGE GRANTS by default. For details, see [How to obtain MANAGE GRANTS on a container](/user-guide/container-manage-grants-using#label-container-manage-grants-using-obtain). |
| MANAGE LISTING AUTO FULFILLMENT | Grants the ability to publish listings to remote regions using [Cross-Cloud Auto-Fulfillment](/collaboration/provider-listings-auto-fulfillment) and manage auto-fulfillment settings for listings. | In the [organization account](/user-guide/organization-accounts), must be granted by the GLOBALORGADMIN role. In all other accounts, must be granted by the ACCOUNTADMIN role after that role has been [delegated privileges by the ORGADMIN role](/collaboration/provider-listings-auto-fulfillment-manage-privileges#label-delegate-laf-privileges). |
| MANAGE ORGANIZATION ACCESS | Grants the ability to manage organizational access to a given account. |  |
| MANAGE ORGANIZATION CONTACTS | Grants the ability to manage the contacts of an organization. | Must be granted by the GLOBALORGADMIN role in the [organization account](/user-guide/organization-accounts). |
| MANAGE ORGANIZATION SUPPORT CASES | Grants the ability to view, comment on, and manage all Support cases that were opened by the current user in Snowsight. |  |
| MANAGE ORGANIZATION TERMS | Grants the ability to manage the legal terms for an organization. | Must be granted by the GLOBALORGADMIN role in the [organization account](/user-guide/organization-accounts). |
| MANAGE ORGANIZATION USERS | Grants the ability to manage [organization users](/user-guide/organization-users). | Must be granted by the GLOBALORGADMIN role in the organization account. |
| MANAGE ORGANIZATION USER GROUPS | Grants the ability to manage [organization user groups](/user-guide/organization-users#label-org-users-groups). | Must be granted by the GLOBALORGADMIN role in the organization account. |
| MANAGE SERVICE CALLER ACCESS | Grants the ability to set the [SERVICE\_CALLER\_TOKEN\_VALIDITY\_SECS](/sql-reference/parameters#service-caller-token-validity-secs) parameter, which controls the lifetime of caller’s rights login tokens for Snowpark Container Services. | Must be granted by the ACCOUNTADMIN or SECURITYADMIN role. |
| MANAGE SHARE TARGET | Grants the ability to manage (ALTER) share targets. |  |
| MANAGE USER SUPPORT CASES | Grants the ability to view, comment on, and manage all Support cases for the current user in Snowsight. |  |
| MANAGE WAREHOUSES | Grants the ability to perform operations that require [MODIFY, MONITOR, and OPERATE privileges on warehouses](#label-warehouse-privileges) in the same account. | Must be granted by the ACCOUNTADMIN role. |
| MODIFY EVENT TABLE | Grants the ability to set the EVENT\_TABLE parameter on any object in the account. |  |
| MODIFY LOG EVENT LEVEL | Enables setting the level of log events captured for stored procedures and UDFs in the current account. | For more information, see [LOG\_EVENT\_LEVEL](/sql-reference/parameters#label-log-event-level). |
| MODIFY LOG LEVEL | Enables setting the level of log messages captured for stored procedures and UDFs in the current account. | For more information, see [LOG\_LEVEL](/sql-reference/parameters#label-log-level). |
| MODIFY METRIC LEVEL | Enables setting the level of metrics data captured for stored procedures and UDFs in the current account. | For more information, see [METRIC\_LEVEL](/sql-reference/parameters#label-metric-level). |
| MODIFY SESSION LOG EVENT LEVEL | Enables setting the level of log events captured for stored procedures and UDFs invoked in the current session. | For more information, see [LOG\_EVENT\_LEVEL](/sql-reference/parameters#label-log-event-level). |
| MODIFY SESSION LOG LEVEL | Enables setting the level of log messages captured for stored procedures and UDFs invoked in the current session. | For more information, see [LOG\_LEVEL](/sql-reference/parameters#label-log-level). |
| MODIFY SESSION METRIC LEVEL | Enables setting the level of metrics data captured for stored procedures and UDFs invoked in the current session. | For more information, see [METRIC\_LEVEL](/sql-reference/parameters#label-metric-level). |
| MODIFY TRACE LEVEL | Enables setting the level of trace events captured for stored procedures and UDFs in the current account. | When tracing events, you must also set the LOG\_LEVEL parameter to one of its supported values. For more information, see [TRACE\_LEVEL](/sql-reference/parameters#label-trace-level). |
| MODIFY SESSION TRACE LEVEL | Enables setting the level of trace events captured for stored procedures and UDFs invoked in the current session. | When tracing events, you must also set the LOG\_LEVEL parameter to one of its supported values. For more information, see [TRACE\_LEVEL](/sql-reference/parameters#label-trace-level). |
| MONITOR EXECUTION | Grants the ability to monitor any pipes or tasks in the account. | Must be granted by the ACCOUNTADMIN role. The USAGE privilege is also required on each database and schema that stores these objects. |
| MONITOR | Grants the ability to describe connections, resolve any object and session, and show capacity groups, locks, login events, query history by warehouse, REST history events, task history, and transactions. |  |
| MONITOR ROLE | Grants the ability to view roles in the account. |  |
| MONITOR SECURITY | Grants the ability to call system functions pertaining to [Customer-managed keys](/user-guide/security-encryption-manage#label-customer-managed-keys). |  |
| MONITOR USAGE | Grants the ability to monitor account-level usage and historical information for databases and warehouses; for more details, see [Enabling non-account administrators to monitor usage and billing history](/user-guide/security-access-control-configure#label-allow-other-users-to-monitor-usage-billing-history). Additionally grants the ability to view managed accounts using [SHOW MANAGED ACCOUNTS](/sql-reference/sql/show-managed-accounts). | Must be granted by the ACCOUNTADMIN role. |
| MONITOR USER | Grants the ability to view users and all their properties in the account. |  |
| OVERRIDE SHARE RESTRICTIONS | Grants the ability to set value for the SHARE\_RESTRICTIONS parameter on a share. | For more details, see [Direct share restrictions](/user-guide/direct-share-restrictions). |
| PURCHASE DATA EXCHANGE LISTING | Grants the ability to purchase a paid listing. | See [Pay for Snowflake Marketplace listings](/collaboration/consumer-listings-paying). |
| READ SESSION | Grants the ability to read session context. | Must be granted by the ACCOUNTADMIN role. |
| READ UNREDACTED AI OBSERVABILITY EVENTS TABLE | Grants the ability to read the unredacted data in an AI observability events table. | Must be granted by the ACCOUNTADMIN role. |
| READ UNREDACTED ERROR TABLE | Grants the ability to read the unredacted data in an error table. Required when the error table is associated with a base table that has security policies, such as a [masking policy](/user-guide/security-column-intro). For more information about error tables, see [DML error logging](/user-guide/data-load-overview#label-data-load-overview-dml-error-logging). | Must be granted by the ACCOUNTADMIN role. |
| REPLICATE | Grants the ability to change the REPLICABLE\_WITH\_FAILOVER\_GROUPS setting for databases and schemas. |  |
| RESOLVE ALL | Grants the ability to resolve all objects in the account, which outputs the object in the corresponding [SHOW <objects>](/sql-reference/sql/show) command. |  |
| USE AI FUNCTION <name> | Grants the ability to use a specific Snowflake Cortex AI function (for example, `GRANT USE AI FUNCTION AI_COMPLETE ON ACCOUNT`). For the list of supported per-function privilege names, see [USE AI FUNCTION <name> — per-function privileges](/user-guide/snowflake-cortex/aisql-privileges-and-access#label-cortex-ai-function-per-function-privileges). |  |
| USE AI FUNCTIONS | Grants the ability to use Snowflake Cortex AI Functions. Users need both the USE AI FUNCTIONS account privilege and the CORTEX\_USER database role to use all Snowflake Cortex AI Functions. | For more information, see [Snowflake Cortex AI Functions (including LLM functions)](/user-guide/snowflake-cortex/aisql). |
| VIEW LINEAGE | Grants the ability to view data lineage, including upstream and downstream lineage objects and dependencies. For more information, see [Data Lineage](/user-guide/ui-snowsight-lineage). |  |
| ALL [ PRIVILEGES ] | Grants all global privileges. |  |

Expand

Show lessSee more

## User privileges

| Privilege | Usage |
| --- | --- |
| IMPERSONATE | Runs a task or dynamic table on behalf of a specified user account. |
| MODIFY PROGRAMMATIC AUTHENTICATION METHODS | Grants the ability to create, modify, delete, rotate, and view information about the [programmatic access tokens](/user-guide/programmatic-access-tokens) and [key pairs](/user-guide/key-pair-auth) for the user. |
| MONITOR | Grants the ability to view the login history for the user. |
| OWNERSHIP | Grants full control over a user/role. Only a single role can hold this privilege on a specific object at a time. |
| ALL [ PRIVILEGES ] | Grants all privileges, except OWNERSHIP, on the user. |

Expand

Show lessSee more

## Role privileges

| Privilege | Usage |
| --- | --- |
| OWNERSHIP | Grants full control over a role. Only a single role can hold this privilege on a specific object at a time. Note that the owner role does not inherit any permissions granted to the owned role. To inherit permissions from a role, that role must be granted to another role, creating a parent-child relationship in a role hierarchy. |

Expand

Show lessSee more

## Resource monitor privileges

| Privilege | Usage |
| --- | --- |
| MODIFY | Enables altering any properties of a resource monitor, such as changing the monthly credit quota. |
| MONITOR | Enables viewing a resource monitor. |
| ALL [ PRIVILEGES ] | Grants all privileges, except OWNERSHIP, on the resource monitor. |

Expand

Show lessSee more

## Virtual warehouse privileges

| Privilege | Usage |
| --- | --- |
| APPLYBUDGET | Enables adding or removing a warehouse from a budget. |
| MANAGE ATTACHED TABLES | Enables using `ALTER WAREHOUSE ... ADD TABLES` and `ALTER WAREHOUSE ... DROP TABLES` on an interactive warehouse to manage which tables are cached by the warehouse. Grants access to these cache operations only and does not grant other warehouse modification operations such as resizing or reconfiguring. Applies to interactive warehouses only. |
| MODIFY | Enables altering any properties of a warehouse, including changing its size.     Required to assign a warehouse to a resource monitor. Note that only the ACCOUNTADMIN role can assign warehouses to resource monitors. |
| MONITOR | Enables viewing current and past queries executed on a warehouse as well as usage statistics on that warehouse. |
| OPERATE | Enables changing the state of a warehouse (stop, start, suspend, resume). In addition, enables viewing current and past queries executed on a warehouse and aborting any executing queries. |
| USAGE | Enables using a virtual warehouse and, as a result, executing queries on the warehouse. If the warehouse is configured to auto-resume when a SQL statement (e.g. query) is submitted to it, the warehouse resumes automatically and executes the statement. |
| OWNERSHIP | Grants full control over a warehouse. Only a single role can hold this privilege on a specific object at a time. |
| ALL [ PRIVILEGES ] | Grants all privileges, except OWNERSHIP, on the warehouse. |

Expand

Show lessSee more

Tip

The granting of the global MANAGE WAREHOUSES privilege is equivalent to granting the MODIFY, MONITOR, and OPERATE
privileges on all warehouses in an account. You can grant this
privilege to a role whose purpose includes managing a warehouse to simplify your Snowflake access control management.

For details, refer to [Delegating warehouse management](/user-guide/warehouses-tasks#label-grant-manage-warehouses-privilege).

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Connection privileges

| Privilege | Usage |
| --- | --- |
| FAILOVER | Grants the ability to promote a secondary connection to serve as the primary connection. |

Expand

Show lessSee more

## External volume privileges

| Privilege | Usage |
| --- | --- |
| USAGE | Enables referencing the external volume when executing other commands that use the external volume, and grants the ability to view details for an external volume in a SHOW or DESCRIBE command. |
| OWNERSHIP | Grants full control over an external volume. Only a single role can hold this privilege on a specific object at a time. |

Expand

Show lessSee more

## Failover group privileges

| Privilege | Usage |
| --- | --- |
| MODIFY | Enables altering any properties of a failover group. |
| MONITOR | Enables viewing details of a failover group. |
| OWNERSHIP | Grants full control over a failover group. Only a single role can hold this privilege on a specific object at a time. |
| FAILOVER | Enables promoting a secondary failover group to serve as primary failover group. |
| REPLICATE | Enables refreshing a secondary failover group. |
| ALL [ PRIVILEGES ] | Grants all privileges, except OWNERSHIP, on the failover group. |

Expand

Show lessSee more

## Replication group privileges

| Privilege | Usage |
| --- | --- |
| MODIFY | Enables altering any properties of a replication group. |
| MONITOR | Enables viewing details of a replication group. |
| OWNERSHIP | Grants full control over a replication group. Only a single role can hold this privilege on a specific object at a time. |
| REPLICATE | Enables refreshing a secondary replication group. |
| ALL [ PRIVILEGES ] | Grants all privileges, except OWNERSHIP, on the replication group. |

Expand

Show lessSee more

## Integration privileges

| Privilege | Usage |
| --- | --- |
| USAGE | Enables referencing the integration when executing other commands that use the integration. For more information, see access control requirements for [CREATE STAGE](/sql-reference/sql/create-stage#label-create-stage-privileges) and [CREATE EXTERNAL ACCESS INTEGRATION](/sql-reference/sql/create-external-access-integration#label-create-external-access-integration-privileges). |
| USE\_ANY\_ROLE | Allows an OAuth client or user to switch roles only if this privilege is granted to the client or user. Configure the External OAuth security integration to use the `EXTERNAL_OAUTH_ANY_ROLE_MODE` parameter using [CREATE SECURITY INTEGRATION](/sql-reference/sql/create-security-integration-oauth-external) or [ALTER SECURITY INTEGRATION](/sql-reference/sql/alter-security-integration-oauth-external), or configure the Snowflake OAuth security integration to use the `OAUTH_ANY_ROLE_MODE` parameter using [CREATE SECURITY INTEGRATION](/sql-reference/sql/create-security-integration-oauth-snowflake) or [ALTER SECURITY INTEGRATION](/sql-reference/sql/alter-security-integration-oauth-snowflake). |
| OWNERSHIP | Grants full control over an integration. Only a single role can hold this privilege on a specific object at a time. |
| ALL [ PRIVILEGES ] | Grants all privileges, except OWNERSHIP, on the integration. |

Expand

Show lessSee more

## Authentication Policy privileges

| Privilege | Usage |
| --- | --- |
| OWNERSHIP | Transfers ownership of an authentication policy, which grants full control over the authentication policy. Required to alter most properties of an authentication policy. |

Expand

Show lessSee more

## Network Rule privileges

| Privilege | Usage |
| --- | --- |
| OWNERSHIP | Grants full control over the network rule. |

Expand

Show lessSee more

## Network policy privileges

| Privilege | Usage |
| --- | --- |
| OWNERSHIP | Grants full control over the network policy. Only a single role can hold this privilege on a specific object at a time. |
| USAGE | Grants the ability to apply a network policy. |

Expand

Show lessSee more

## Packages policy privileges

| Privilege | Usage |
| --- | --- |
| OWNERSHIP | Transfers ownership of a packages policy, which grants full control over the packages policy. Required to alter most properties of a packages policy. |
| USAGE | Grants the ability to view the contents of a packages policy in a SHOW or DESCRIBE command. |

Expand

Show lessSee more

## Password policy privileges

| Privilege | Usage |
| --- | --- |
| OWNERSHIP | Transfers ownership of a password policy, which grants full control over the password policy. Required to alter most properties of a password policy. |

Expand

Show lessSee more

## Provisioned Throughput privileges

| Privilege | Usage |
| --- | --- |
| OWNERSHIP | Grants full control over a provisioned throughput. Only one role at a time can hold this privilege on a specific object. |
| USE | Enables inference with a provisioned throughput. |
| MONITOR | Enables performing DESCRIBE and SHOW commands on a provisioned throughput. |

Expand

Show lessSee more

## Session policy privileges

| Privilege | Usage |
| --- | --- |
| OWNERSHIP | Transfers ownership of a session policy, which grants full control over the session policy. Required to alter most properties of a session policy. |

Expand

Show lessSee more

## Restricted session scope privileges

| Privilege | Usage |
| --- | --- |
| USAGE | Enables viewing a restricted session scope with SHOW RESTRICTED SESSION SCOPES and DESCRIBE RESTRICTED SESSION SCOPE. |
| MODIFY | Enables altering the definition or properties of a restricted session scope with ALTER RESTRICTED SESSION SCOPE. |
| OWNERSHIP | Transfers ownership of a restricted session scope, which grants full control over the object. Required to drop a restricted session scope. |

Expand

Show lessSee more

## Data exchange privileges

| Privilege | Usage |
| --- | --- |
| IMPORTED PRIVILEGES | Enables roles other than the owning role to manage a Data Exchange. |

Expand

Show lessSee more

## Listing privileges

| Privilege | Usage |
| --- | --- |
| MODIFY | Enables roles other than the owning role to modify a listing. |
| USAGE | Enables viewing a listing. |
| OWNERSHIP | Grants full control over a listing. Only a single role can hold this privilege on a specific object at a time. |
| ALL [ PRIVILEGES ] | Grants all privileges, except OWNERSHIP, on a listing. |

Expand

Show lessSee more

## Organization profile privileges

| Privilege | Usage |
| --- | --- |
| MODIFY | Enables roles other than the owning role to modify an organization profile. |
| OWNERSHIP | Grants full control over an organization profile. Only a single role can hold this privilege on a specific object at a time. |

Expand

Show lessSee more

## Share privileges

| Privilege | Usage |
| --- | --- |
| OWNERSHIP | Grants full control over a share. Only a single role can hold this privilege on a specific object at a time. Cannot be transferred. |

Expand

Show lessSee more

## Database privileges

| Privilege | Usage |
| --- | --- |
| APPLYBUDGET | Enables adding or removing a database from a budget. |
| MANAGE GRANTS | Enables granting and revoking privileges on the database and on objects in it, including objects created later, as if the role were the owner of those objects. Owning a database does not confer this privilege; it must be granted explicitly. Add WITH GRANT OPTION to allow the role to delegate MANAGE GRANTS on the database or on schemas in it. For details, see [Delegating grant management with container-level MANAGE GRANTS](/user-guide/container-manage-grants-intro). |
| MODIFY | Enables altering any settings of a database. |
| MONITOR | Enables performing the DESCRIBE command on the database. |
| USAGE | Enables using a database, including returning the database details in the [SHOW DATABASES](/sql-reference/sql/show-databases) command output. Additional privileges are required to view or take actions on objects in a database. |
| REFERENCE\_USAGE | Enables using an object (e.g. secure view in a share) when the object references another object in a different database. Grant the privilege on the other database to the share. You cannot grant this privilege on a database to any kind of role. For details, see [GRANT <privilege> … TO SHARE](/sql-reference/sql/grant-privilege-share) and [Share data from multiple databases](/user-guide/data-sharing-multiple-db). |
| CREATE DATABASE ROLE | Enables creating a new database role in a database. |
| CREATE SCHEMA | Enables creating a new schema in a database, including cloning a schema. |
| EXECUTE AUTO CLASSIFICATION | Grants the ability to set a classification profile on a database in order to implement [sensitive data classification](/user-guide/classify-intro). |
| IMPORTED PRIVILEGES | Enables roles other than the owning role to access a shared database; applies only to shared databases. |
| OWNERSHIP | Grants full control over the database. Only a single role can hold this privilege on a specific object at a time. |
| ALL [ PRIVILEGES ] | Grants all privileges, except OWNERSHIP, on a database. |

Expand

Show lessSee more

Note

- Changing the properties of a database requires the OWNERSHIP privilege for the database.

  Updating the COMMENT property only requires the MODIFY privilege for the database.
- If any database privilege is granted to a role, that role can take SQL actions on objects in a schema using fully-qualified
  names. The role must have the USAGE privilege on the schema as well as the required privilege or privileges on the object. To make a
  database the active database in a user session, the USAGE privilege on the database is required.
- An account-level role (i.e. `r1`) with the OWNERSHIP privilege on the database can grant the CREATE DATABASE ROLE privilege to a
  different account-level role (i.e. `r2`). Similarly, `r1` can also revoke the CREATE DATABASE ROLE privilege from another
  account-level role.

  In this scenario, `r2` must have the USAGE privilege on the database to create a new database role in that database.
- When you create a database role, the USAGE privilege on the database that contains the database role is automatically granted to the
  database role.

## Schema privileges

| Privilege | Usage |
| --- | --- |
| APPLYBUDGET | Enables adding or removing a schema from a budget. |
| MANAGE GRANTS | Enables granting and revoking privileges on the schema and on objects in it, including objects created later, as if the role were the owner of those objects. Owning a schema does not confer this privilege; it must be granted explicitly. Add WITH GRANT OPTION to allow the role to delegate MANAGE GRANTS on the schema. For details, see [Delegating grant management with container-level MANAGE GRANTS](/user-guide/container-manage-grants-intro). |
| MODIFY | Enables altering any settings of a schema. |
| MONITOR | Enables performing the DESCRIBE command on the schema. |
| USAGE | Enables using a schema, including returning the schema details in the [SHOW SCHEMAS](/sql-reference/sql/show-schemas) command output.     To execute [SHOW <objects>](/sql-reference/sql/show) commands for objects (tables, views, stages, file formats, sequences, pipes, types, or functions) in the schema, a role must have at least one privilege granted on the object. |
| CREATE AGENT | Enables creating a new [agent](/user-guide/snowflake-cortex/cortex-agents) in a schema. |
| CREATE APPLICATION SERVICE | Enables creating a new [Application Service](/developer-guide/snowflake-app-runtime/about-snowflake-app-runtime) in a schema. |
| CREATE ARTIFACT REPOSITORY | Enables creating a new [artifact repository](/sql-reference/sql/create-artifact-repository) in a schema. |
| CREATE AUTHENTICATION POLICY | Enables creating a new authentication policy in a schema. |
| CREATE BACKUP POLICY | Grants the ability to create a backup policy in a schema. The role granting this privilege must have the OWNERSHIP privilege on the schema. |
| CREATE BACKUP SET | Grants the ability to create a backup set in a schema. The role granting this privilege must have the OWNERSHIP privilege on the schema. |
| CREATE CONTACT | Enables creating a new [contact](/user-guide/contacts-using) in a schema. |
| CREATE DATASET | Enables creating a new [machine learning dataset](/developer-guide/snowflake-ml/dataset) in a schema. |
| CREATE DATA METRIC FUNCTION | Enables creating a new data metric function in a schema. |
| CREATE DATA MOVEMENT POLICY | Enables creating a new [data movement policy](/user-guide/data-movement-policies) in a schema. |
| CREATE DATA MOVEMENT RULE | Enables creating a new [data movement rule](/user-guide/data-movement-policies) in a schema. |
| CREATE DBT PROJECT | Enables creating a new dbt project object in a schema. |
| CREATE EXPERIMENT | Enables creating a new [machine learning experiment](/developer-guide/snowflake-ml/experiments) in a schema. |
| CREATE TABLE | Enables creating a new table in a schema, including by cloning.     This privilege is not required to create temporary tables, which are scoped to the current user session and are automatically dropped when the session ends. |
| CREATE DYNAMIC TABLE | Enables creating a new [dynamic table](/user-guide/dynamic-tables/overview) in a schema. |
| CREATE EVENT TABLE | Enables creating a new [event table](/developer-guide/logging-tracing/logging-tracing-overview) in a schema. |
| CREATE EXTERNAL TABLE | Enables creating a new external table in a schema. |
| CREATE GIT REPOSITORY | Enables creating a new [Git repository](/developer-guide/git/git-overview) stage in a schema. |
| CREATE HYBRID TABLE | Enables creating a new [hybrid table](/user-guide/tables-hybrid) in a schema. |
| CREATE ICEBERG TABLE | Enables creating a new [Iceberg table](/user-guide/tables-iceberg) in a schema. |
| CREATE INTERACTIVE TABLE | Enables creating a new [interactive table](/user-guide/interactive) in a schema. |
| CREATE VIEW | Enables creating a new view in a schema. |
| CREATE MASKING POLICY | Enables creating a new masking policy in a schema. |
| CREATE MATERIALIZED VIEW | Enables creating a new materialized view in a schema. |
| CREATE MCP SERVER | Enables creating a new [MCP server](/user-guide/snowflake-cortex/cortex-agents-mcp) in a schema. |
| CREATE NETWORK RULE | Enables creating a new network rule in a schema. |
| CREATE NOTEBOOK | Enables creating a new notebook in a schema. |
| CREATE ONLINE FEATURE TABLE | Enables creating a new [online feature table](/sql-reference/sql/create-online-feature-table) in a schema. |
| CREATE RESTRICTED SESSION SCOPE | Enables creating a new [restricted session scope](/user-guide/restricted-session-scope) in a schema. |
| CREATE ROW ACCESS POLICY | Enables creating a new row access policy in a schema. |
| CREATE SECRET | Enables creating a new secret in the current/specified schema or replaces an existing secret. |
| CREATE SEMANTIC VIEW | Enables creating a new semantic view in a schema. |
| CREATE SESSION POLICY | Enables creating a new session policy in a schema. |
| CREATE SNAPSHOT POLICY — *Deprecated* | Grants the ability to create a snapshot policy in a schema. The role granting this privilege must have the OWNERSHIP privilege on the schema. Deprecated: use CREATE BACKUP POLICY instead. |
| CREATE SNAPSHOT SET — *Deprecated* | Grants the ability to create a snapshot set in a schema. The role granting this privilege must have the OWNERSHIP privilege on the schema. Deprecated: use CREATE BACKUP SET instead. |
| CREATE STAGE | Enables creating a new stage in a schema, including cloning a stage. |
| CREATE STORAGE LIFECYCLE POLICY | Enables creating a new [storage lifecycle policy](/user-guide/storage-management/storage-lifecycle-policies) in a schema. |
| CREATE STREAMLIT | Enables creating a new Streamlit app in a schema. |
| CREATE FILE FORMAT | Enables creating a new file format in a schema, including cloning a file format. |
| CREATE TYPE | Enables creating a new [user-defined type](/sql-reference/data-types-user-defined) in a schema. |
| CREATE SEQUENCE | Enables creating a new sequence in a schema, including cloning a sequence. |
| CREATE FUNCTION | Enables creating a new UDF or external function in a schema. |
| CREATE PACKAGES POLICY | Enables creating a new packages policy in a schema. |
| CREATE PASSWORD POLICY | Enables creating a new password policy in a schema. |
| CREATE PIPE | Enables creating a new pipe in a schema. |
| CREATE STREAM | Enables creating a new stream in a schema, including cloning a stream. |
| CREATE TAG | Enables creating a new [tag key](/user-guide/object-tagging/introduction) in a schema. |
| CREATE TASK | Enables creating a new task in a schema, including cloning a task. |
| CREATE PROCEDURE | Enables creating a new stored procedure in a schema. |
| CREATE ALERT | Enables creating a new alert in a schema. |
| CREATE CORTEX SEARCH SERVICE | Enables creating new [Cortex search services](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview) on a schema. |
| CREATE SNOWFLAKE.CORE.BUDGET | Enables creating new [budget](/user-guide/budgets) on a schema. |
| CREATE SNOWFLAKE.DATA\_PRIVACY.CLASSIFICATION\_PROFILE | Enables creating new [classification profile](/user-guide/classify-auto) instances on a schema to implement sensitive data classification. |
| CREATE SNOWFLAKE.DATA\_PRIVACY.CUSTOM\_CLASSIFIER | Enables creating new [custom classifier](/user-guide/classify-custom) instances on a schema. |
| CREATE SNOWFLAKE.ML.ANOMALY\_DETECTION | Enables creating new [anomaly detection](/user-guide/ml-functions/anomaly-detection) model instances on a schema. |
| CREATE SNOWFLAKE.ML.CLASSIFICATION | Enables creating new [classification](/user-guide/ml-functions/classification) model instances on a schema. |
| CREATE SNOWFLAKE.ML.FORECAST | Enables creating new [forecast](/user-guide/ml-functions/forecasting) model instances on a schema. |
| CREATE SNOWFLAKE.ML.TOP\_INSIGHTS | Enables creating new [Top Insights](/user-guide/ml-functions/top-insights) instances on a schema. |
| CREATE MODEL | Enables creating a [machine learning model](/developer-guide/snowflake-ml/model-registry/overview) on a schema. |
| CREATE MODEL MONITOR | Enables creating a [model monitor](/developer-guide/snowflake-ml/model-registry/model-observability) on a schema. |
| CREATE IMAGE REPOSITORY | Enables creating a Snowpark Container Services [image repository](/developer-guide/snowpark-container-services/working-with-registry-repository) on a schema. |
| CREATE SERVICE | Enables creating a Snowpark Container Services [service](/developer-guide/snowpark-container-services/working-with-services) on a schema. |
| CREATE SNAPSHOT | Enables creating a Snowpark Container Services [snapshot](/developer-guide/snowpark-container-services/block-storage-volume) on a schema. |
| CREATE WORKSPACE | Enables creating a new [Snowflake Workspace](/user-guide/ui-snowsight/workspaces) in a schema. |
| EXECUTE AUTO CLASSIFICATION | Grants the ability to set a classification profile on a schema in order to implement [sensitive data classification](/user-guide/classify-intro). Schema owner has this privilege by default. |
| ADD SEARCH OPTIMIZATION | Enables [adding search optimization](/user-guide/search-optimization-service) to a table in a schema. |
| OWNERSHIP | Grants full control over the schema. Only a single role can hold this privilege on a specific object at a time. |
| ALL [ PRIVILEGES ] | Grants all privileges, except OWNERSHIP, on a schema. |

Expand

Show lessSee more

Note

- Changing the properties of a schema requires the OWNERSHIP privilege for the database.
- Operating on a schema also requires at least one privilege on the parent database.

## Table privileges

| Privilege | Usage |
| --- | --- |
| SELECT | Enables executing a [SELECT](/sql-reference/sql/select) statement on a table and [classifying](/user-guide/classify-intro) a table. |
| SELECT ERROR TABLE | Enables executing a [SELECT](/sql-reference/sql/select) statement on the error table associated with a base table. For more information, see [DML error logging](/user-guide/data-load-overview#label-data-load-overview-dml-error-logging). |
| INSERT | Enables executing an [INSERT](/sql-reference/sql/insert) command on a table. Also enables using the [ALTER TABLE](/sql-reference/sql/alter-table) command with a `RECLUSTER` clause to manually recluster a table with a clustering key. |
| UPDATE | Enables executing an [UPDATE](/sql-reference/sql/update) command on a table. |
| TRUNCATE | Enables executing a [TRUNCATE TABLE](/sql-reference/sql/truncate-table) command on a table. |
| DELETE | Enables executing a [DELETE](/sql-reference/sql/delete) command on a table. |
| EVOLVE SCHEMA | Enables [schema evolution](/user-guide/data-load-schema-evolution) to occur on a table when loading data. |
| REFERENCES | Enables referencing a table as the unique/primary key table for a foreign key constraint. Also enables viewing the structure of a table (but not the data) via the DESCRIBE or SHOW command or by querying the Information Schema. |
| APPLYBUDGET | Enables adding or removing a table from a budget. |
| OWNERSHIP | Grants full control over the table. Required to alter most properties of a table, with the exception of reclustering. Only a single role can hold this privilege on a specific object at a time. |
| ALL [ PRIVILEGES ] | Grants all privileges, except OWNERSHIP, on a table. |

Expand

Show lessSee more

Note

- Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.
- A role must be granted or inherit the OWNERSHIP privilege on the object to create a temporary object that has the same name as the object
  that already exists in the schema.

## Dynamic table privileges

| Privilege | Usage |
| --- | --- |
| SELECT | Enables executing a [SELECT](/sql-reference/sql/select) statement on a dynamic table. The SELECT privilege on a dynamic table allows you to view it in the output of the [SHOW DYNAMIC TABLES](/sql-reference/sql/show-dynamic-tables) command.  If you have the SELECT privilege but don’t have the MONITOR privilege, the following fields are hidden: `text`, `warehouse`, `scheduling_state`, `last_suspended_on`, and `suspend_reason_code` (only hidden in Snowsight). |
| OPERATE | Enables altering the properties of a dynamic table.  If you do not have this privilege on a dynamic table, you can’t use the ALTER DYNAMIC TABLE command, which enables you to:   - Suspend a dynamic table using [ALTER … SUSPEND](/sql-reference/sql/alter-dynamic-table#label-alter-dynamic-table-suspend-resume). - Resume a dynamic table using [ALTER … RESUME](/sql-reference/sql/alter-dynamic-table#label-alter-dynamic-table-suspend-resume). - Refresh a dynamic table using [ALTER … REFRESH](/sql-reference/sql/alter-dynamic-table#label-alter-dynamic-table-refresh). - Set or change the warehouse and/or target lag using [ALTER … SET](/sql-reference/sql/alter-dynamic-table#label-alter-dynamic-table-set-property).   Additionally, if you lack this privilege on a dynamic table, you cannot execute `CREATE DYNAMIC TABLE ... INITIALIZE = ON_CREATE` to create a new dynamic table that consumes from it. |
| MONITOR | Enables accessing the metadata for a dynamic table through Snowsight and SQL commands and functions.  While the OPERATE privilege grants this access, it also includes the capability to alter dynamic tables, making MONITOR the more suitable option for scenarios where a user does not need to alter a dynamic table. For example, roles held by data scientists.  If you have the MONITOR privilege on a dynamic table, you can do the following:   - Call the [DYNAMIC\_TABLE\_GRAPH\_HISTORY](/sql-reference/functions/dynamic_table_graph_history) table function to view   graph history of that dynamic table. - Call the [DYNAMIC\_TABLE\_REFRESH\_HISTORY](/sql-reference/functions/dynamic_table_refresh_history) table function to view   refresh history for that dynamic table. - View that dynamic table in the output of the [SHOW DYNAMIC TABLES](/sql-reference/sql/show-dynamic-tables) command. - View that dynamic table’s metadata in the output of the [DESCRIBE DYNAMIC TABLE](/sql-reference/sql/desc-dynamic-table) command or the Snowsight dynamic tables   details page.   - If you have the SELECT privilege but don’t have the MONITOR privilege, the following fields are hidden:     `text`, `warehouse`, `scheduling_state`, `last_suspended_on`, and `suspend_reason_code` (only hidden in Snowsight). |
| OWNERSHIP | Grants full control over the dynamic table. Only a single role can hold this privilege on a specific object at a time.  Required to drop a dynamic table. |
| ALL [ PRIVILEGES ] | Grants all privileges, except OWNERSHIP, on the dynamic table. |

Expand

Show lessSee more

## Event table privileges

Some privileges typically supported for tables are disallowed on event tables (and as a result aren’t listed here) because the
[event table structure](/developer-guide/logging-tracing/event-table-columns) is predefined and immutable.

| Privilege | Usage |
| --- | --- |
| ALL [ PRIVILEGES ] | Grants all privileges, except OWNERSHIP, on the event table. |
| APPLYBUDGET | Enables adding or removing an event table from a [budget](/user-guide/budgets). |
| DELETE | Enables executing a [DELETE](/sql-reference/sql/delete) command on an event table. |
| INGEST TELEMETRY | Grants the ability to ingest telemetry data into the event table. |
| OWNERSHIP | Grants full control over the event table. Required to alter the event table. In conjunction with OWNERSHIP of the account, grants the ability to associate an account with an event table. |
| REFERENCES | Grants the ability to view the structure of an event table (but not the data). |
| SELECT | Enables executing a [SELECT](/sql-reference/sql/select) statement on an event table. |
| TRUNCATE | Enables executing a [TRUNCATE TABLE](/sql-reference/sql/truncate-table) command on the event table. |

Expand

Show lessSee more

Note

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

## External table privileges

| Privilege | Usage |
| --- | --- |
| SELECT | Enables executing a [SELECT](/sql-reference/sql/select) statement on an external table and [classifying](/user-guide/classify-intro) an external table. |
| REFERENCES | Enables viewing the structure of an external table (but not the data) via the DESCRIBE or SHOW command or by querying the Information Schema. |
| OWNERSHIP | Grants full control over the external table; required to refresh an external table. Only a single role can hold this privilege on a specific object at a time. Note that in a [managed access schema](/user-guide/security-access-control-configure#label-managed-access-schemas), only the schema owner (i.e. the role with the OWNERSHIP privilege on the schema) or a role with the MANAGE GRANTS privilege can grant or revoke privileges on objects in the schema, including future grants. |
| ALL [ PRIVILEGES ] | Grants all privileges, except OWNERSHIP, on an external table. |

Expand

Show lessSee more

Note

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

## Hybrid table privileges

| Privilege | Usage |
| --- | --- |
| SELECT | Enables executing a [SELECT](/sql-reference/sql/select) statement on a hybrid table. |
| INSERT | Enables executing an [INSERT](/sql-reference/sql/insert) command on a hybrid table. |
| UPDATE | Enables executing an [UPDATE](/sql-reference/sql/update) command on a hybrid table. |
| TRUNCATE | Enables executing a [TRUNCATE TABLE](/sql-reference/sql/truncate-table) command on a hybrid table. |
| DELETE | Enables executing a [DELETE](/sql-reference/sql/delete) command on a hybrid table. |
| REFERENCES | Enables referencing a hybrid table as the unique/primary key table for a foreign key constraint. Also enables viewing the structure of a hybrid table (but not the data) via the DESCRIBE or SHOW command or by querying the Information Schema. |
| APPLYBUDGET | Enables adding or removing a hybrid table from a budget. |
| OWNERSHIP | Grants full control over the hybrid table. Required to alter most properties of a hybrid table. Only a single role can hold this privilege on a specific object at a time. |
| ALL [ PRIVILEGES ] | Grants all privileges, except OWNERSHIP, on a hybrid table. |

Expand

Show lessSee more

Note

- Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.
- The following privileges have no effect when granted on a hybrid table that uses a catalog integration: INSERT, UPDATE, DELETE. Hybrid tables that
  use a catalog integration are read-only.

## Iceberg table privileges

| Privilege | Usage |
| --- | --- |
| SELECT | Enables executing a [SELECT](/sql-reference/sql/select) statement on an Iceberg table. |
| INSERT | Enables executing an [INSERT](/sql-reference/sql/insert) command on an Iceberg table. |
| UPDATE | Enables executing an [UPDATE](/sql-reference/sql/update) command on an Iceberg table. |
| TRUNCATE | Enables executing a [TRUNCATE TABLE](/sql-reference/sql/truncate-table) command on an Iceberg table. |
| DELETE | Enables executing a [DELETE](/sql-reference/sql/delete) command on an Iceberg table. |
| REFERENCES | Enables referencing an Iceberg table as the unique/primary key table for a foreign key constraint. Also enables viewing the structure of an Iceberg table (but not the data) via the DESCRIBE or SHOW command or by querying the Information Schema. |
| APPLYBUDGET | Enables adding or removing an Iceberg table from a budget. |
| OWNERSHIP | Grants full control over the Iceberg table. Required to alter most properties of an Iceberg table. Only a single role can hold this privilege on a specific object at a time. |
| ALL [ PRIVILEGES ] | Grants all privileges, except OWNERSHIP, on an Iceberg table. |

Expand

Show lessSee more

Note

- Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.
- The following privileges have no effect when granted on an Iceberg table that uses an external catalog: INSERT, UPDATE, DELETE. Iceberg tables that
  use an external catalog are read-only.

## Interactive table privileges

These privileges apply to [interactive tables](/user-guide/interactive).

| Privilege | Usage |
| --- | --- |
| SELECT | Enables executing a [SELECT](/sql-reference/sql/select) statement on an interactive table. |
| MONITOR | Grants the ability to access metadata for an interactive table through Snowsight and SQL. You can monitor interactive table refresh progress using the [DYNAMIC\_TABLE\_REFRESH\_HISTORY](/sql-reference/functions/dynamic_table_refresh_history) table function. |
| REFERENCES | Enables referencing an interactive table as the unique/primary key table for a foreign key constraint. Also enables viewing the structure of an interactive table (but not the data) via the DESCRIBE or SHOW command or by querying the Information Schema. |
| OWNERSHIP | Grants full control over the interactive table. Required to rename the interactive table. Only a single role can hold this privilege on a specific object at a time. |
| ALL [ PRIVILEGES ] | Grants all privileges, except OWNERSHIP, on an interactive table. |

Expand

Show lessSee more

Note

- Operating on an interactive table also requires USAGE or any other privilege on the parent database and schema.
- Interactive tables don’t support DML operations such as INSERT, UPDATE, and DELETE.
  For information about ingesting data into interactive tables, see [Snowflake interactive analytics](/user-guide/interactive).

## View privileges

| Privilege | Usage |
| --- | --- |
| SELECT | Enables executing a [SELECT](/sql-reference/sql/select) statement on a view and [classifying](/user-guide/classify-intro) a view.     This privilege is sufficient to query a view; the SELECT privilege is not required on the objects from which the view is created. |
| REFERENCES | Enables viewing the structure of a view (but not the data) via the DESCRIBE or SHOW command or by querying the Information Schema. |
| OWNERSHIP | Grants full control over the view. Required to alter a view. Only a single role can hold this privilege on a specific object at a time. Note that in a [managed access schema](/user-guide/security-access-control-configure#label-managed-access-schemas), only the schema owner (i.e. the role with the OWNERSHIP privilege on the schema) or a role with the MANAGE GRANTS privilege can grant or revoke privileges on objects in the schema, including future grants. |
| ALL [ PRIVILEGES ] | Grants all privileges, except OWNERSHIP, on a view. |

Expand

Show lessSee more

Note

- Table DML privileges such as INSERT, UPDATE, and DELETE can be granted on views; however, because views are read-only, these privileges
  have no effect.
- Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.
- A role must be granted or inherit the OWNERSHIP privilege on the object to create a temporary object that has the same name as the object
  that already exists in the schema.

## Materialized view privileges

| Privilege | Usage |
| --- | --- |
| SELECT | Enables executing a [SELECT](/sql-reference/sql/select) statement on a view and [classifying](/user-guide/classify-intro) a materialized view.     Note that this privilege is sufficient to query a view. The SELECT privilege is not required on the underlying objects for a view. |
| REFERENCES | Enables viewing the structure of a view (but not the data) via the DESCRIBE or SHOW command or by querying the Information Schema. |
| APPLYBUDGET | Enables adding or removing a materialized view from a budget. |
| OWNERSHIP | Grants full control over the view. Required to alter a view. Only a single role can hold this privilege on a specific object at a time. Note that in a [managed access schema](/user-guide/security-access-control-configure#label-managed-access-schemas), only the schema owner (i.e. the role with the OWNERSHIP privilege on the schema) or a role with the MANAGE GRANTS privilege can grant or revoke privileges on objects in the schema, including future grants. |
| ALL [ PRIVILEGES ] | Grants all privileges, except OWNERSHIP, on a view. |

Expand

Show lessSee more

Note

- Table DML privileges such as INSERT, UPDATE, and DELETE can be granted on views; however, because views are read-only, these privileges
  have no effect.
- Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.
- A role must be granted or inherit the OWNERSHIP privilege on the object to create a temporary object that has the same name as the object
  that already exists in the schema.

## Semantic view privileges

| Privilege | Usage |
| --- | --- |
| SELECT | Enables executing a [SELECT](/sql-reference/sql/select) statement on a semantic view.     This privilege is sufficient to query a semantic view; the SELECT privilege is not required on the objects from which the semantic view is created.     Also enables executing [DESCRIBE SEMANTIC VIEW](/sql-reference/sql/desc-semantic-view) for the semantic view. |
| REFERENCES | Enables viewing the structure of a semantic view (but not the data) by querying the Information Schema views that provide information about the semantic view or by executing a DESCRIBE or SHOW command. This includes the DESCRIBE and SHOW commands for the underlying entities, calculations and relationships. Also enables calling the [GET\_DDL](/sql-reference/functions/get_ddl) function for the semantic view. |
| MONITOR | Grants the ability to view details about the semantic view (using SHOW commands, DESC commands, and INFORMATION\_SCHEMA views) and Cortex Analyst [monitoring and observability data](/user-guide/snowflake-cortex/cortex-analyst/admin-observability). |
| OWNERSHIP | Grants full control over the semantic view. Only a single role can hold this privilege on a specific object at a time. Note that in a [managed access schema](/user-guide/security-access-control-configure#label-managed-access-schemas), only the schema owner (i.e. the role with the OWNERSHIP privilege on the schema) or a role with the MANAGE GRANTS privilege can grant or revoke privileges on objects in the schema, including future grants.     Required to replace a view. Your role must also be granted the CREATE SEMANTIC VIEW privilege on the schema containing the view. |
| ALL [ PRIVILEGES ] | Grants all privileges, except OWNERSHIP, on a semantic view. |

Expand

Show lessSee more

Note

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

## Notebook privileges

| Privilege | Usage |
| --- | --- |
| OWNERSHIP | Grants full control over the notebook. Only a single role can hold this privilege on a specific object at a time. Note that in a [managed access schema](/user-guide/security-access-control-configure#label-managed-access-schemas), only the schema owner (i.e. the role with the OWNERSHIP privilege on the schema) or a role with the MANAGE GRANTS privilege can grant or revoke privileges on objects in the schema, including future grants. |
| USAGE | Grants the ability to reference and view the notebook in [SHOW <objects>](/sql-reference/sql/show) commands. |

Expand

Show lessSee more

## Online Feature Table privileges

| Privilege | Usage |
| --- | --- |
| MONITOR | Grants the ability to view details about the online feature table using [SHOW ONLINE FEATURE TABLES](/sql-reference/sql/show-online-feature-tables) and view refresh history using the [ONLINE\_FEATURE\_TABLE\_REFRESH\_HISTORY](/sql-reference/functions/online-feature-table-refresh-history) function. |
| SELECT | Grants the ability to query data from the online feature table. |
| OWNERSHIP | Grants full control over the online feature table. Only a single role can hold this privilege on a specific object at a time. Note that in a [managed access schema](/user-guide/security-access-control-configure#label-managed-access-schemas), only the schema owner (i.e. the role with the OWNERSHIP privilege on the schema) or a role with the MANAGE GRANTS privilege can grant or revoke privileges on objects in the schema, including future grants. |
| ALL [ PRIVILEGES ] | Grants all applicable privileges, except OWNERSHIP, on the online feature table. |

Expand

Show lessSee more

Note

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

## Stage privileges

| Privilege | Usage |
| --- | --- |
| USAGE | Enables using an external stage object in a SQL statement and includes the READ and WRITE privileges; not applicable to internal stages. |
| READ | Enables performing any operations that require reading from a stage (for example, [file staging commands](/sql-reference/commands-file) and [COPY INTO <table>](/sql-reference/sql/copy-into-table)). |
| WRITE | Enables performing any operations that require writing to a stage (for example, [file staging commands](/sql-reference/commands-file) and [COPY INTO <location>](/sql-reference/sql/copy-into-location)). |
| OWNERSHIP | Grants full control over the stage. Only a single role can hold this privilege on a specific object at a time. Note that in a [managed access schema](/user-guide/security-access-control-configure#label-managed-access-schemas), only the schema owner (i.e. the role with the OWNERSHIP privilege on the schema) or a role with the MANAGE GRANTS privilege can grant or revoke privileges on objects in the schema, including future grants. |
| ALL [ PRIVILEGES ] | Grants all applicable privileges, except OWNERSHIP, on the stage (internal or external). |

Expand

Show lessSee more

Note

- When granting both the READ and WRITE privileges for a stage, the READ privilege must be granted before or at the same time as
  the WRITE privilege.
- When revoking both the READ and WRITE privileges for a stage, the WRITE privilege must be revoked before or at the same time as
  the READ privilege.
- Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.
- To run the following commands on an external stage that uses a storage integration,
  you must use a role that has been granted or inherits the USAGE privilege on the storage integration (unless the stage-owning
  role has this privilege):

  - [LIST](/sql-reference/sql/list)
  - [REMOVE](/sql-reference/sql/remove)
  - [COPY INTO <table>](/sql-reference/sql/copy-into-table)
  - [COPY INTO <location>](/sql-reference/sql/copy-into-location)
- A role must be granted or inherit the OWNERSHIP privilege on the object to create a temporary object that has the same name as the object
  that already exists in the schema.

### Directory table privileges

The following table summarizes the stage [privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) that you need to execute common
SQL commands when you work with a [directory table](/user-guide/data-load-dirtables) on a stage.

| Operation | Object Type | Privilege Required |
| --- | --- | --- |
| Retrieve file URLs from a directory table using a SELECT FROM DIRECTORY statement. | Stage | One of the following, depending on the type of stage:   - Internal stage: An account role or database role with the READ privilege on the stage. - External stage: An account role or database role with either the READ or USAGE privilege on the stage. |
| Upload data using the [PUT](/sql-reference/sql/put) command. | Stage (internal only) | An account role or database role with the WRITE privilege on the stage. |
| Remove files using the [REMOVE](/sql-reference/sql/remove) command. | Stage | One of the following, depending on the type of stage:   - Internal stage: An account role or database role with the WRITE privilege on the stage. - External stage: An account role or database role with either the WRITE or USAGE privilege on the stage. |
| Refresh the metadata using the [ALTER STAGE](/sql-reference/sql/alter-stage) command. | Stage | One of the following, depending on the type of stage:   - Internal stage: An account role or database role with the WRITE privilege on the stage. - External stage: An account role or database role with either the WRITE or USAGE privilege on the stage. |

Expand

Show lessSee more

## Snowflake Git repository clone privileges

| Privilege | Usage |
| --- | --- |
| READ | Enables performing any operations that require reading from a Git repository clone. |
| WRITE | Enables performing operations that require writing to a Git repository clone, such as changing the object’s properties or performing a FETCH from the remote repository. |
| OWNERSHIP | Grants full control over the Git repository clone. Only a single role can hold this privilege on a specific object at a time. Note that in a [managed access schema](/user-guide/security-access-control-configure#label-managed-access-schemas), only the schema owner (i.e. the role with the OWNERSHIP privilege on the schema) or a role with the MANAGE GRANTS privilege can grant or revoke privileges on objects in the schema, including future grants. |
| ALL [ PRIVILEGES ] | Grants all applicable privileges, except OWNERSHIP, on the Git repository clone. |

Expand

Show lessSee more

## File format privileges

| Privilege | Usage |
| --- | --- |
| USAGE | Enables using a file format in a SQL statement. |
| OWNERSHIP | Grants full control over the file format. Required to alter a file format. Only a single role can hold this privilege on a specific object at a time. Note that in a [managed access schema](/user-guide/security-access-control-configure#label-managed-access-schemas), only the schema owner (i.e. the role with the OWNERSHIP privilege on the schema) or a role with the MANAGE GRANTS privilege can grant or revoke privileges on objects in the schema, including future grants. |
| ALL [ PRIVILEGES ] | Grants all privileges, except OWNERSHIP, on the file format. |

Expand

Show lessSee more

Note

- Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.
- A role must be granted or inherit the OWNERSHIP privilege on the object to create a temporary object that has the same name as the object
  that already exists in the schema.

## Pipe privileges

Pipe objects are created and managed to load data using Snowpipe.

| Privilege | Usage |
| --- | --- |
| APPLYBUDGET | Enables adding or removing a pipe from a budget. |
| MONITOR | Enables viewing details for the pipe (using DESCRIBE PIPE or SHOW PIPES). |
| OPERATE | Enables viewing details for the pipe (using DESCRIBE PIPE or SHOW PIPES), pausing or resuming the pipe, and refreshing the pipe. |
| OWNERSHIP | Grants full control over the pipe. Only a single role can hold this privilege on a specific object at a time. Note that in a [managed access schema](/user-guide/security-access-control-configure#label-managed-access-schemas), only the schema owner (i.e. the role with the OWNERSHIP privilege on the schema) or a role with the MANAGE GRANTS privilege can grant or revoke privileges on objects in the schema, including future grants. |
| ALL [ PRIVILEGES ] | Grants all privileges, except OWNERSHIP, on the pipe. |

Expand

Show lessSee more

Note

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

## Database role privileges

| Privilege | Usage |
| --- | --- |
| OWNERSHIP | Grants full control over a database role. Only a single role can hold this privilege on a specific object at a time. Note that the owner role does not inherit any permissions granted to the owned database role. To inherit permissions from a database role, that database role must be granted to another role, creating a parent-child relationship in a role hierarchy. |

Expand

Show lessSee more

## Stream privileges

| Privilege | Usage |
| --- | --- |
| SELECT | Enables executing a [SELECT](/sql-reference/sql/select) statement on a stream, which also allows you to view the stream in the output of the SHOW STREAMS command. To view the `table_name` and `base_tables` columns, you need at least one access privilege on the stream’s source object. |
| OWNERSHIP | Grants full control over the stream. Only a single role can hold this privilege on a specific object at a time. Note that in a [managed access schema](/user-guide/security-access-control-configure#label-managed-access-schemas), only the schema owner (i.e. the role with the OWNERSHIP privilege on the schema) or a role with the MANAGE GRANTS privilege can grant or revoke privileges on objects in the schema, including future grants. |
| ALL [ PRIVILEGES ] | Grants all privileges, except OWNERSHIP, on the stream. |

Expand

Show lessSee more

## Task privileges

| Privilege | Usage |
| --- | --- |
| APPLYBUDGET | Enables adding or removing a task from a budget. |
| MONITOR | Enables viewing details for the task (using DESCRIBE TASK or SHOW TASKS). |
| OPERATE | Enables viewing details for the task (using DESCRIBE TASK or SHOW TASKS) and resuming or suspending the task. |
| OWNERSHIP | Grants full control over the task. Only a single role can hold this privilege on a specific object at a time. Note that in a [managed access schema](/user-guide/security-access-control-configure#label-managed-access-schemas), only the schema owner (i.e. the role with the OWNERSHIP privilege on the schema) or a role with the MANAGE GRANTS privilege can grant or revoke privileges on objects in the schema, including future grants. |
| ALL [ PRIVILEGES ] | Grants all privileges, except OWNERSHIP, on the task. |

Expand

Show lessSee more

## dbt project object privileges

| Privilege | Usage |
| --- | --- |
| USAGE | Enables executing a dbt project object, retrieving files from the dbt project object, viewing details (using DESCRIBE DBT PROJECT and SHOW DBT PROJECT), and viewing execution history. |
| MONITOR | Enables viewing a dbt project object in Snowsight and retrieving dbt artifacts from recent executions with `SYSTEM$DBT_GET_LAST_SUCCESSFUL_RUN_TARGET`, `SYSTEM$DBT_GET_LAST_FAILED_RUN_TARGET`, or `SYSTEM$DBT_GET_LAST_RUN_TARGET`. Without this privilege, you can’t access the project details, run history, monitoring information, or artifacts returned by those functions. |
| OWNERSHIP | Grants full control over the dbt project object, including executing and monitoring. Only a single role can hold this privilege on a specific object at a time. Note that in a [managed access schema](/user-guide/security-access-control-configure#label-managed-access-schemas), only the schema owner (i.e. the role with the OWNERSHIP privilege on the schema) or a role with the MANAGE GRANTS privilege can grant or revoke privileges on objects in the schema, including future grants. |
| ALL [ PRIVILEGES ] | Grants all privileges, except OWNERSHIP, on the dbt project object. |

Expand

Show lessSee more

To separate deployment from execution, you can use one role to deploy the dbt project object with `snow dbt deploy --no-auto-compile` and
another role to execute it. For role and privilege requirements, see
[Optionally separate deployment from execution](/user-guide/data-engineering/dbt-projects-on-snowflake-access-control#label-dbt-project-separate-deployment-execution).

## Secret privileges

| Privilege | Usage |
| --- | --- |
| READ | Enables a UDF or stored procedure that uses a secret to access the credentials that are stored in the secret. For details, see [Creating a secret to represent credentials](/developer-guide/external-network-access/creating-using-external-network-access#label-creating-using-external-access-integration-secret). |
| USAGE | Enables using a secret. |
| MODIFY | Required to update OAuth tokens in a secret using SYSTEM$START\_OAUTH\_FLOW and SYSTEM$FINISH\_OAUTH\_FLOW. Also required to alter other secret properties via ALTER SECRET. |
| OWNERSHIP | Transfers ownership of a secret, which grants full control over the secret. Required to drop a secret from the system. |

Expand

Show lessSee more

## Aggregation policy privileges

| Privilege | Usage |
| --- | --- |
| APPLY | Enables executing the unset and set operations for an aggregation policy on a table or view.  Note that granting the global APPLY AGGREGATION POLICY privilege (i.e. APPLY AGGREGATION POLICY on ACCOUNT) enables executing the DESCRIBE operation on tables and views. |
| OWNERSHIP | Grants full control over the aggregation policy. Required to alter most properties of an aggregation policy. Only a single role can hold this privilege on a specific object at a time. Note that in a [managed access schema](/user-guide/security-access-control-configure#label-managed-access-schemas), only the schema owner (i.e. the role with the OWNERSHIP privilege on the schema) or a role with the MANAGE GRANTS privilege can grant or revoke privileges on objects in the schema, including future grants. |

Expand

Show lessSee more

Note

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

## Join policy privileges

| Privilege | Usage |
| --- | --- |
| APPLY | Enables executing the unset and set operations for a join policy on a table or view.  Note that granting the global APPLY JOIN POLICY privilege (i.e. APPLY JOIN POLICY on ACCOUNT) enables executing the DESCRIBE operation on tables and views. |
| OWNERSHIP | Grants full control over the join policy. Required to alter most properties of a join policy. Only a single role can hold this privilege on a specific object at a time. Note that in a [managed access schema](/user-guide/security-access-control-configure#label-managed-access-schemas), only the schema owner (i.e. the role with the OWNERSHIP privilege on the schema) or a role with the MANAGE GRANTS privilege can grant or revoke privileges on objects in the schema, including future grants. |

Expand

Show lessSee more

Note

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

## Masking policy privileges

| Privilege | Usage |
| --- | --- |
| APPLY | Enables executing the unset and set operations for a [masking policy](/user-guide/security-column-intro) on a column.  Note that granting the global APPLY MASKING POLICY privilege (i.e. APPLY MASKING POLICY on ACCOUNT) enables executing the DESCRIBE operation on tables and views.  For syntax examples, see [Masking policy privileges](/user-guide/security-column-intro#label-security-column-privileges-masking-policies). |
| OWNERSHIP | Grants full control over the masking policy. Required to alter most properties of a masking policy. Only a single role can hold this privilege on a specific object at a time. Note that in a [managed access schema](/user-guide/security-access-control-configure#label-managed-access-schemas), only the schema owner (i.e. the role with the OWNERSHIP privilege on the schema) or a role with the MANAGE GRANTS privilege can grant or revoke privileges on objects in the schema, including future grants. |

Expand

Show lessSee more

Note

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

## Privacy policy privileges

| Privilege | Usage |
| --- | --- |
| APPLY | Enables executing the unset and set operations for a privacy policy on a table or view.  Note that granting the global APPLY PRIVACY POLICY privilege (that is, APPLY PRIVACY POLICY on ACCOUNT) enables executing the DESCRIBE operation on tables and views. |
| OWNERSHIP | Grants full control over the privacy policy. Required to alter most properties of a privacy policy. Only a single role can hold this privilege on a specific object at a time. Note that in a [managed access schema](/user-guide/security-access-control-configure#label-managed-access-schemas), only the schema owner (i.e. the role with the OWNERSHIP privilege on the schema) or a role with the MANAGE GRANTS privilege can grant or revoke privileges on objects in the schema, including future grants. |

Expand

Show lessSee more

Note

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

## Projection policy privileges

| Privilege | Usage |
| --- | --- |
| APPLY | Enables executing the unset and set operations for a projection policy on a column.  Note that granting the global APPLY PROJECTION POLICY privilege (i.e. APPLY PROJECTION POLICY on ACCOUNT) enables executing the DESCRIBE operation on tables and views. |
| OWNERSHIP | Grants full control over the projection policy. Required to alter most properties of a projection policy. Only a single role can hold this privilege on a specific object at a time. Note that in a [managed access schema](/user-guide/security-access-control-configure#label-managed-access-schemas), only the schema owner (i.e. the role with the OWNERSHIP privilege on the schema) or a role with the MANAGE GRANTS privilege can grant or revoke privileges on objects in the schema, including future grants. |

Expand

Show lessSee more

Note

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

## Row access policy privileges

| Privilege | Usage |
| --- | --- |
| APPLY | Enables executing the add and drop operations for the [row access policy](/user-guide/security-row-intro) on a table or view.  Note that granting the global APPLY ROW ACCESS POLICY privilege (i.e. APPLY ROW ACCESS POLICY on ACCOUNT) enables executing the DESCRIBE operation on tables and views.  For syntax examples, see [Summary of DDL commands, operations, and privileges](/user-guide/security-row-intro#label-security-row-privilege-command-summary). |
| OWNERSHIP | Grants full control over the row access policy. Required to alter most properties of a row access policy. Only a single role can hold this privilege on a specific object at a time. Note that in a [managed access schema](/user-guide/security-access-control-configure#label-managed-access-schemas), only the schema owner (i.e. the role with the OWNERSHIP privilege on the schema) or a role with the MANAGE GRANTS privilege can grant or revoke privileges on objects in the schema, including future grants. |

Expand

Show lessSee more

Note

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

## Tag privileges

| Privilege | Usage |
| --- | --- |
| APPLY | Enables executing the add and drop operations for the tag on a Snowflake object. |
| READ | Enables a data sharing consumer to view shared tag assignments using a [SHOW TAGS](/sql-reference/sql/show-tags) command. The data sharing provider grants this privilege to a database role or directly to the share. |
| OWNERSHIP | Grants full control over the tag. Required to alter most properties of a tag. Only a single role can hold this privilege on a specific object at a time. Note that in a [managed access schema](/user-guide/security-access-control-configure#label-managed-access-schemas), only the schema owner (i.e. the role with the OWNERSHIP privilege on the schema) or a role with the MANAGE GRANTS privilege can grant or revoke privileges on objects in the schema, including future grants. |

Expand

Show lessSee more

Note

Tags are stored at the schema level.

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

## Sequence privileges

| Privilege | Usage |
| --- | --- |
| USAGE | Enables using a sequence in a SQL statement. |
| ALL [ PRIVILEGES ] | Grants all privileges, except OWNERSHIP, on the sequence. |
| OWNERSHIP | Grants full control over the sequence; required to alter the sequence. Only a single role can hold this privilege on a specific object at a time. Note that in a [managed access schema](/user-guide/security-access-control-configure#label-managed-access-schemas), only the schema owner (i.e. the role with the OWNERSHIP privilege on the schema) or a role with the MANAGE GRANTS privilege can grant or revoke privileges on objects in the schema, including future grants. |

Expand

Show lessSee more

Note

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

## User-defined types

| Privilege | Usage |
| --- | --- |
| USAGE | Enables *explicitly* using a user-defined type in a SQL statement. |
| ALL [ PRIVILEGES ] | Grants all privileges, except OWNERSHIP, on the user-defined type. |
| OWNERSHIP | Grants full control over the user-defined type; required to alter the user-defined type. Only a single role can hold this privilege on a specific object at a time. Note that in a [managed access schema](/user-guide/security-access-control-configure#label-managed-access-schemas), only the schema owner (i.e. the role with the OWNERSHIP privilege on the schema) or a role with the MANAGE GRANTS privilege can grant or revoke privileges on objects in the schema, including future grants. |

Expand

Show lessSee more

Note

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

Explicit use of a user-defined type means specifying the type by name in a SQL statement or code. The
following are examples of explicit use of a user-defined type:

- An explicit cast to the user-defined type.
- A type definition in a DML statement, stored procedure code, or user-defined function code that
  specifies the user-defined type.

USAGE privilege isn’t required on a user-defined type if it isn’t explicitly used. For example, if a table
column, stored procedure argument, or function argument is defined with a user-defined type, users
can query the table or call the stored procedure or function without USAGE privilege on the user-defined
type.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Stored procedure privileges

| Privilege | Usage |
| --- | --- |
| USAGE | Enables calling a stored procedure. |
| ALL [ PRIVILEGES ] | Grants all privileges, except OWNERSHIP, on the stored procedure. |
| OWNERSHIP | Grants full control over the stored procedure; required to alter the stored procedure. Only a single role can hold this privilege on a specific object at a time. Note that in a [managed access schema](/user-guide/security-access-control-configure#label-managed-access-schemas), only the schema owner (i.e. the role with the OWNERSHIP privilege on the schema) or a role with the MANAGE GRANTS privilege can grant or revoke privileges on objects in the schema, including future grants. |

Expand

Show lessSee more

Note

- Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.
- If a stored procedure runs with caller’s rights, the user who calls the stored procedure must have privileges on the database
  objects (e.g. tables) accessed by the stored procedure. For details, see [Understanding caller’s rights and owner’s rights stored procedures](/developer-guide/stored-procedure/stored-procedures-rights).

## User-defined function (UDF) and external function privileges

| Privilege | Usage |
| --- | --- |
| USAGE | Enables calling a UDF or external function. |
| ALL [ PRIVILEGES ] | Grants all privileges, except OWNERSHIP, on the UDF or external function. |
| OWNERSHIP | Grants full control over the UDF or external function; required to alter the UDF or external function. Only a single role can hold this privilege on a specific object at a time. Note that in a [managed access schema](/user-guide/security-access-control-configure#label-managed-access-schemas), only the schema owner (i.e. the role with the OWNERSHIP privilege on the schema) or a role with the MANAGE GRANTS privilege can grant or revoke privileges on objects in the schema, including future grants. |

Expand

Show lessSee more

Note

- Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.
- The owner of a UDF must have privileges on the objects accessed by the function; the user who calls a UDF does not need those
  privileges. For details, see [Security/privilege requirements for SQL UDFs](/developer-guide/udf/sql/udf-sql-introduction#label-udf-privilege-requirements).
- The owner of an external function must have the USAGE privilege on the API integration object associated with the external
  function. For details, see [Access control](/sql-reference/external-functions-security#label-external-functions-access-control) in the documentation on external functions.

## Data metric function (DMF) privileges

| Privilege | Usage |
| --- | --- |
| USAGE | Enables calling the DMF. |
| OWNERSHIP | Transfers ownership of the data metric function, which grants full control over the data metric function. Required to alter most properties of the data metric function. |
| ALL [ PRIVILEGES ] | Grants all privileges, except OWNERSHIP, on the DMF. |

Expand

Show lessSee more

## Alert privileges

| Privilege | Usage |
| --- | --- |
| MONITOR | Enables viewing details for the alert (using [DESCRIBE ALERT](/sql-reference/sql/desc-alert) or [SHOW ALERTS](/sql-reference/sql/show-alerts)). |
| OPERATE | Enables viewing details for the alert (using DESCRIBE ALERT or SHOW ALERTS) and resuming or suspending the alert (using [ALTER ALERT](/sql-reference/sql/alter-alert)). |
| OWNERSHIP | Grants full control over the alert. Only a single role can hold this privilege on a specific object at a time. Note that in a [managed access schema](/user-guide/security-access-control-configure#label-managed-access-schemas), only the schema owner (i.e. the role with the OWNERSHIP privilege on the schema) or a role with the MANAGE GRANTS privilege can grant or revoke privileges on objects in the schema, including future grants. |
| ALL [ PRIVILEGES ] | Grants all privileges, except OWNERSHIP, on the alert. |

Expand

Show lessSee more

## Compute Pool privileges

| Privilege | Usage |
| --- | --- |
| OPERATE | Enables suspending or resuming a compute pool. |
| MODIFY | Enables altering compute pool and setting properties. |
| USAGE | Enables running a service or a job. It enables communicating with the service (create a service function, use public endpoints, and connect from another service). |
| MONITOR | Enables viewing compute pool usage (number of services and jobs running), properties, and listing compute pools in the account for which the role has access privileges. |
| OWNERSHIP | Grants full control over the compute pool. Only a single role can hold this privilege on a specific compute pool object at a time. |

Expand

Show lessSee more

## Image Repository privileges

| Privilege | Usage |
| --- | --- |
| OWNERSHIP | Enables full control over the image repository. The role with this privilege can also delete an image repository. |
| READ | Enables listing and downloading images from an image repository. |
| WRITE | Enables listing and downloading images from a repository. Also enables pushing images in the repository. |

Expand

Show lessSee more

## Service privileges

| Privilege | Usage |
| --- | --- |
| DROP | Enables dropping a Snowpark Container Services service. |
| OPERATE | Enables suspending or resuming a service, upgrading service, and modifying service properties. |
| OWNERSHIP | Enables full control over the service. The role with this privilege can also remove a service from a schema. |
| MONITOR | Enables monitoring a service and getting runtime status. |

Expand

Show lessSee more

## Application Service privileges

| Privilege | Usage |
| --- | --- |
| OWNERSHIP | Enables full control over the Application Service, including dropping it. The owning role implicitly has every other privilege on the service. |
| USAGE | Enables accessing the public endpoints exposed by the service. |
| OPERATE | Enables suspending, resuming, upgrading, and modifying the service using [ALTER APPLICATION SERVICE](/sql-reference/sql/alter-application-service). |
| MONITOR | Enables viewing runtime status and reading container logs using [SYSTEM$GET\_APPLICATION\_SERVICE\_LOGS](/sql-reference/functions/system_get_application_service_logs). |

Expand

Show lessSee more

## Artifact repository privileges

| Privilege | Usage |
| --- | --- |
| OWNERSHIP | Enables full control over the artifact repository, including dropping it and publishing new package versions. |
| READ | Enables downloading packages and artifacts from the repository. Required to reference an artifact repository in [CREATE APPLICATION SERVICE](/sql-reference/sql/create-application-service). |

Expand

Show lessSee more

## Cortex Search Service privileges

| Privilege | Usage |
| --- | --- |
| OWNERSHIP | Enables full control over the Cortex Search service. The role with this privilege can also remove a service from a schema. |
| OPERATE | Enables inspecting, suspending or resuming a Cortex Search service and modifying service properties. |
| USAGE | Enables invoking the service. |
| ALL [ PRIVILEGES ] | Grants all privileges, except OWNERSHIP, on the service. |

Expand

Show lessSee more

## Snapshot privileges (for block storage volume snapshots)

These privileges apply to block storage volume snapshots.

| Privilege | Usage |
| --- | --- |
| OWNERSHIP | Enables full control over the snapshot. The role with this privilege can also remove a snapshot from a schema. |
| USAGE | Enables listing and describing snapshots. |

Expand

Show lessSee more

## Backup policy privileges

These privileges apply to [backup](/user-guide/backups) policies for Snowflake databases, schemas,
and tables.

| Privilege | Usage |
| --- | --- |
| OWNERSHIP | Enables full control over backup policies. |
| USAGE | Enables listing and describing backup policies. |

Expand

Show lessSee more

## Backup set privileges

These privileges apply to [backup](/user-guide/backups) sets for Snowflake databases, schemas,
and tables.

| Privilege | Usage |
| --- | --- |
| OWNERSHIP | Enables full control over backup sets. |
| USAGE | Enables listing and describing backup sets. |

Expand

Show lessSee more

## Snapshot policy privileges (for WORM snapshots) — *Deprecated*

Note

These privileges are deprecated. Use backup policy privileges instead.

These privileges apply to [Write Once Read Many (WORM) snapshots](/user-guide/backups) for Snowflake databases, schemas,
and tables.

| Privilege | Usage |
| --- | --- |
| OWNERSHIP | Enables full control over snapshot policies. |
| USAGE | Enables listing and describing snapshot policies. |

Expand

Show lessSee more

## Snapshot set privileges (for WORM snapshots) — *Deprecated*

Note

These privileges are deprecated. Use backup set privileges instead.

These privileges apply to [Write Once Read Many (WORM) snapshots](/user-guide/backups) for Snowflake databases, schemas,
and tables.

| Privilege | Usage |
| --- | --- |
| OWNERSHIP | Enables full control over snapshot sets. |
| USAGE | Enables listing and describing snapshot sets. |

Expand

Show lessSee more

## Storage lifecycle policy privileges

These privileges apply to [storage lifecycle policies](/user-guide/storage-management/storage-lifecycle-policies).

| Privilege | Usage |
| --- | --- |
| OWNERSHIP | Grants full control of the storage lifecycle policy. This privilege is required to alter the policy. Only one role can have this privilege per lifecycle policy object. |
| APPLY | Allows the grantee to add or drop the storage lifecycle policy on a table. To add the policy to a table, you must also have the OWNERSHIP privilege for the table or the global `APPLY STORAGE LIFECYCLE POLICY` privilege on the account. |

Expand

Show lessSee more

Note

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

## Streamlit privileges

| Privilege | Usage |
| --- | --- |
| OWNERSHIP | Grants full control over the Streamlit object; required to alter the Streamlit object. Only a single role can hold this privilege on a specific object at a time. |
| USAGE | Enables viewing and running a Streamlit app, as well as displaying information about the Streamlit object. This privilege does not allow users to see the Streamlit app code or the artifacts that define the Streamlit app. |
| EMBED | Enables generating an embed URL for a Streamlit app, so that the app can be rendered in an external web page. This privilege is required in addition to USAGE, and is not implied by OWNERSHIP. For more information, see [embedding apps in external pages](/developer-guide/streamlit/features/embedding/overview). |

Expand

Show lessSee more

## Model privileges

| Privilege | Usage |
| --- | --- |
| OWNERSHIP | Enables full control over the model. Only one role at a time can hold this privilege on a given model. |
| USAGE | Enables displaying information about a model and invoking its methods. It does not allow users to see model weights or the artifacts that define the model. This privilege is also supported `ON FUTURE MODELS`. |

Expand

Show lessSee more

## Application package privileges

| Privilege | Usage |
| --- | --- |
| ATTACH LISTING | Associates a listing with an application package or share. |
| DEVELOP | Grants the ability to create an application in development mode from the application package. |
| INSTALL | Grants the ability to create an instance from the application package. |
| MANAGE RELEASES | Grants the ability to manage release directives in the application package. |
| MANAGE VERSIONS | Grants the ability to manage versions and release directives in the application package. |
| OWNERSHIP | Grants full control over the application package. |

Expand

Show lessSee more

## Application instance privileges

| Privilege | Usage |
| --- | --- |
| OWNERSHIP | Grants full control over the application instance, including dropping it. Only a single role can hold this privilege on a specific application at a time. |

Expand

Show lessSee more

## Contact privileges

| Privilege | Usage |
| --- | --- |
| APPLY | Enables the ability to associate and detach a contact with a Snowflake object. |
| MODIFY | Enables the ability to modify a contact. |
| OWNERSHIP | Grants full control over the contact. Required to alter most properties of a contact. Only a single role can hold this privilege on a specific object at a time. Note that in a [managed access schema](/user-guide/security-access-control-configure#label-managed-access-schemas), only the schema owner (i.e. the role with the OWNERSHIP privilege on the schema) or a role with the MANAGE GRANTS privilege can grant or revoke privileges on objects in the schema, including future grants. |

Expand

Show lessSee more

## Dataset privileges

| Privilege | Usage |
| --- | --- |
| OWNERSHIP | Enables full control over the dataset. |
| USAGE | Enables displaying information about a dataset and invoking its methods. |

Expand

Show lessSee more

## Cortex Agent privileges

| Privilege | Usage |
| --- | --- |
| OWNERSHIP | Enables full control over the Cortex Agent. The role with this privilege can also remove an agent from a schema. |
| MODIFY | Enables the ability to modify a Cortex Agent. |
| MONITOR | Enables the ability to view threads, logs, and traces of the Cortex Agent. |
| USAGE | Enables querying the Cortex Agent to generate responses. |

Expand

Show lessSee more

## Machine Learning Experiment privileges

| Privilege | Usage |
| --- | --- |
| OWNERSHIP | Enables full control over the experiment. The role with this privilege can also remove an experiment from a schema. |
| MODIFY | Enables the ability to modify an experiment and its runs. |
| USAGE | Enables examining the run information contained within an experiment. |

Expand

Show lessSee more

## MCP Server privileges

| Privilege | Usage |
| --- | --- |
| OWNERSHIP | Enables full control over the MCP Server. The role with this privilege can also remove an MCP Server from a schema. |
| MODIFY | Enables the ability to modify an MCP Server. |
| USAGE | Enables querying the MCP Server to discover tools and invoke them. |

Expand

Show lessSee more

## Gateway privileges

| Privilege | Usage |
| --- | --- |
| OWNERSHIP | Enables full control over the gateway. The role with this privilege can also remove a gateway from a schema. |
| MODIFY | Enables the ability to modify a gateway. |
| USAGE | Enables using the gateway. |

Expand

Show lessSee more

## Workspace privileges

| Privilege | Usage |
| --- | --- |
| READ | Grants read-only access to the workspace and its files. |
| WRITE | Grants the ability to create, edit, and delete files in the workspace. Granting WRITE also grants READ access. You do not need to grant READ separately. |
| OWNERSHIP | Grants full control over the workspace. Only a single role can hold this privilege on a specific object at a time. Note that in a [managed access schema](/user-guide/security-access-control-configure#label-managed-access-schemas), only the schema owner (i.e. the role with the OWNERSHIP privilege on the schema) or a role with the MANAGE GRANTS privilege can grant or revoke privileges on objects in the schema, including future grants. |
| ALL [ PRIVILEGES ] | Grants all applicable privileges, except OWNERSHIP, on the workspace. |

Expand

Show lessSee more

For information about creating and sharing workspaces, see [Shared workspaces](/user-guide/ui-snowsight/workspaces-shared).
