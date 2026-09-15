# All commands (alphabetical)

This topic provides a list of all DDL and DML commands, as well as the SELECT command and other related commands, in alphabetical order.

| Command Name | Summary |
| --- | --- |
| **A** |  |
| [ALTER <object>](/sql-reference/sql/alter) | Modifies the metadata of an account-level or database object, or the parameters for a session. |
| [ALTER ACCOUNT](/sql-reference/sql/alter-account) | Modifies an account. |
| [ALTER AGENT](/sql-reference/sql/alter-agent) | Modifies the properties or specification for an existing [Cortex Agent](/user-guide/snowflake-cortex/cortex-agents). |
| [ALTER AGGREGATION POLICY](/sql-reference/sql/alter-aggregation-policy) | Replaces the existing rules or comment of an [aggregation policy](/user-guide/aggregation-policies). |
| [ALTER ALERT](/sql-reference/sql/alter-alert) | Modifies the properties of an existing alert and suspends or resumes an existing [alert](/user-guide/alerts). |
| [ALTER API INTEGRATION](/sql-reference/sql/alter-api-integration) | Modifies the properties of an existing API integration. |
| [ALTER APPLICATION](/sql-reference/sql/alter-application) | Modifies the properties of an installed Snowflake Native App. |
| [ALTER APPLICATION DROP SPECIFICATION](/sql-reference/sql/alter-application-drop-app-spec) | Drops an app specification from an app. |
| [ALTER APPLICATION DROP CONFIGURATION DEFINITION](/sql-reference/sql/alter-application-drop-configuration-definition) | Deletes the [app configuration definition](/developer-guide/native-apps/inter-app-communication) for a Snowflake Native App. |
| [ALTER APPLICATION PACKAGE](/sql-reference/sql/alter-application-package) | Modifies the properties of an existing application package. |
| [ALTER APPLICATION PACKAGE … MODIFY RELEASE CHANNEL](/sql-reference/sql/alter-application-package-release-channel) | Modifies the release channels defined for an existing application package. |
| [ALTER APPLICATION PACKAGE … RELEASE DIRECTIVE (Legacy)](/sql-reference/sql/alter-application-package-release-directive) | Modifies the properties of an existing application package. |
| [ALTER APPLICATION PACKAGE … VERSION](/sql-reference/sql/alter-application-package-version) | Modifies the versioning of an existing application package in the Snowflake Native App Framework. |
| [ALTER APPLICATION ROLE](/sql-reference/sql/alter-application-role) | Modifies the properties for an existing application role. |
| [ALTER APPLICATION … { APPROVE | DECLINE} SPECIFICATION](/sql-reference/sql/alter-application-sequence-number) | Approves or declines an [app specification](/developer-guide/native-apps/requesting-app-specs) using the specified sequence number. |
| [ALTER APPLICATION SET SPECIFICATION](/sql-reference/sql/alter-application-set-app-spec) | Creates or updates an [app specification](/developer-guide/native-apps/requesting-app-specs) for a Snowflake Native App. |
| [ALTER APPLICATION SET CONFIGURATION DEFINITION](/sql-reference/sql/alter-application-set-configuration-definition) | Creates or updates an [app configuration](/developer-guide/native-apps/inter-app-communication) for a Snowflake Native App. |
| [ALTER APPLICATION SET CONFIGURATION VALUE](/sql-reference/sql/alter-application-set-configuration-value) | Sets a value in an [app configuration definition](/developer-guide/native-apps/inter-app-communication) for a Snowflake Native App. |
| [ALTER APPLICATION UNSET CONFIGURATION](/sql-reference/sql/alter-application-unset-configuration) | Unsets an [app configuration definition](/developer-guide/native-apps/inter-app-communication) for a Snowflake Native App. |
| [ALTER AUTHENTICATION POLICY](/sql-reference/sql/alter-authentication-policy) | Modifies the properties of an [authentication policy](/user-guide/authentication-policies). |
| [ALTER BACKUP POLICY](/sql-reference/sql/alter-backup-policy) | Modifies the properties of a [backup](/user-guide/backups) policy. |
| [ALTER BACKUP SET](/sql-reference/sql/alter-backup-set) | Modifies the properties for a [backup](/user-guide/backups) set. |
| [ALTER CATALOG INTEGRATION](/sql-reference/sql/alter-catalog-integration) | Modifies the properties of an existing [catalog integration](/user-guide/tables-iceberg#label-tables-iceberg-catalog-integration-def). |
| [ALTER COMPUTE POOL](/sql-reference/sql/alter-compute-pool) | Modifies the properties of an existing [compute pool](/developer-guide/snowpark-container-services/working-with-compute-pool). |
| [ALTER CONNECTION](/sql-reference/sql/alter-connection) | Modifies the properties for an existing [connection](/user-guide/client-redirect). |
| [ALTER CONTACT](/sql-reference/sql/alter-contact) | Modifies the properties of an existing [contact](/user-guide/contacts-using). |
| [ALTER CORTEX SEARCH SERVICE](/sql-reference/sql/alter-cortex-search) | Suspends, resumes, or modifies the properties of an existing [Cortex Search service](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview). |
| [ALTER DATABASE](/sql-reference/sql/alter-database) | Modifies the properties for an existing database. |
| [ALTER DATABASE (catalog-linked)](/sql-reference/sql/alter-database-catalog-linked) | Modifies the properties for an existing [catalog-linked database](/user-guide/tables-iceberg-catalog-linked-database). |
| [ALTER DATABASE ROLE](/sql-reference/sql/alter-database-role) | Modifies the properties for an existing database role. |
| [ALTER DATASET](/sql-reference/sql/alter-dataset) | Modifies a dataset by adding or dropping dataset versions. |
| [ALTER DATASET … ADD VERSION](/sql-reference/sql/alter-dataset-add-version) | Adds a version to a dataset. |
| [ALTER DATASET … DROP VERSION](/sql-reference/sql/alter-dataset-drop-version) | Drops a dataset version. |
| [ALTER DBT PROJECT](/sql-reference/sql/alter-dbt-project) | Modifies the properties of an existing [dbt project object](/user-guide/data-engineering/dbt-projects-on-snowflake). |
| [ALTER DCM PROJECT](/sql-reference/sql/alter-dcm-project) | Modifies the properties of an existing [DCM project](/user-guide/dcm-projects/dcm-projects-overview). |
| [ALTER DYNAMIC TABLE](/sql-reference/sql/alter-dynamic-table) | Modifies the properties of a [dynamic table](/user-guide/dynamic-tables/overview). |
| [ALTER EXPERIMENT](/sql-reference/sql/alter-experiment) | Modifies the properties of an existing [experiment](/developer-guide/snowflake-ml/experiments). |
| [ALTER EXTERNAL AGENT](/sql-reference/sql/alter-external-agent) | Modifies the properties of an existing [external agent](/user-guide/snowflake-cortex/ai-observability). |
| [ALTER EXTERNAL ACCESS INTEGRATION](/sql-reference/sql/alter-external-access-integration) | Modifies the properties of an existing [external access integration](/developer-guide/external-network-access/creating-using-external-network-access). |
| [ALTER EXTERNAL TABLE](/sql-reference/sql/alter-external-table) | Modifies the properties, columns, or constraints for an existing external table. |
| [ALTER EXTERNAL VOLUME](/sql-reference/sql/alter-external-volume) | Modifies the properties for an existing [external volume](/user-guide/tables-iceberg#label-tables-iceberg-external-volume-def). |
| [ALTER FAILOVER GROUP](/sql-reference/sql/alter-failover-group) | Modifies the properties for an existing [failover group](/user-guide/account-replication-intro#label-replication-and-failover-groups). |
| [ALTER FEATURE POLICY](/sql-reference/sql/alter-feature-policy) | Alters or renames a [feature policy](/developer-guide/native-apps/ui-consumer-feature-policies). |
| [ALTER FILE FORMAT](/sql-reference/sql/alter-file-format) | Modifies the properties for an existing file format object. |
| [ALTER FUNCTION](/sql-reference/sql/alter-function) | Modifies the properties of an existing user-defined or external function. |
| [ALTER FUNCTION (DMF)](/sql-reference/sql/alter-function-dmf) | Modifies the properties of an existing data metric function (DMF). |
| [ALTER FUNCTION (Snowpark Container Services)](/sql-reference/sql/alter-function-spcs) | Modifies the properties of an existing [service function](/developer-guide/snowpark-container-services/working-with-services#label-snowpark-containers-service-communicating-service-function). |
| [ALTER GATEWAY](/sql-reference/sql/alter-gateway) | Modifies the configuration of an existing [gateway](/developer-guide/snowpark-container-services/gateway). |
| [ALTER GIT REPOSITORY](/sql-reference/sql/alter-git-repository) | Modifies the properties of a Snowflake [Git repository clone](/developer-guide/git/git-overview). |
| [ALTER ICEBERG TABLE](/sql-reference/sql/alter-iceberg-table) | Modifies properties such as clustering options and tags for an existing [Apache Iceberg™ table](/user-guide/tables-iceberg). |
| [ALTER ICEBERG TABLE … ALTER COLUMN … SET DATA TYPE (structured types)](/sql-reference/sql/alter-iceberg-table-alter-column-set-data-type) | Modifies (evolves) a [structured type](/sql-reference/data-types-structured) column in a Snowflake-managed [Apache Iceberg™ table](/user-guide/tables-iceberg). |
| [ALTER ICEBERG TABLE … CONVERT TO MANAGED](/sql-reference/sql/alter-iceberg-table-convert-to-managed) | Converts an [Apache Iceberg™ table](/user-guide/tables-iceberg) that uses an external Iceberg catalog into a table that uses Snowflake as the catalog (a Snowflake-managed Iceberg table). |
| [ALTER ICEBERG TABLE … REFRESH](/sql-reference/sql/alter-iceberg-table-refresh) | Refreshes the metadata for an [Apache Iceberg™ table](/user-guide/tables-iceberg) that uses an external Iceberg catalog. |
| [ALTER INTEGRATION](/sql-reference/sql/alter-integration) | Modifies the properties for an existing integration. |
| [ALTER JOIN POLICY](/sql-reference/sql/alter-join-policy) | Replaces the existing rules or comment for a [join policy](/user-guide/join-policies). |
| [ALTER LISTING](/sql-reference/sql/alter-listing) | Modifies the properties of a [listings](/collaboration/collaboration-listings-about) with an inline YAML manifest, or from a file located in a stage location. |
| [ALTER MAINTENANCE POLICY](/sql-reference/sql/alter-maintenance-policy) | Modifies an existing [maintenance policy](/developer-guide/native-apps/consumer-maintenance-policies). |
| [ALTER MASKING POLICY](/sql-reference/sql/alter-masking-policy) | Replaces the existing masking policy rules with new rules or a new comment and allows the renaming of a masking policy. |
| [ALTER MATERIALIZED VIEW](/sql-reference/sql/alter-materialized-view) | Alters a materialized view in the current/specified schema. |
| [ALTER MODEL](/sql-reference/sql/alter-model) | Modifies the properties for an existing model, including its name, tags, default version, or comment. |
| [ALTER MODEL … ADD VERSION](/sql-reference/sql/alter-model-add-version) | Adds a new version to an existing model from an existing model version. |
| [ALTER MODEL … DROP VERSION](/sql-reference/sql/alter-model-drop-version) | Removes a version from the specified machine learning model. |
| [ALTER MODEL … MODIFY VERSION](/sql-reference/sql/alter-model-modify-version) | Modifies a version of a model, changing the version’s comment or metadata. |
| [ALTER MODEL MONITOR](/sql-reference/sql/alter-model-monitor) | Modifies the properties of a [model monitor](/developer-guide/snowflake-ml/model-registry/model-observability). |
| [ALTER NETWORK POLICY](/sql-reference/sql/alter-network-policy) | Modifies the properties for an existing network policy. |
| [ALTER NETWORK RULE](/sql-reference/sql/alter-network-rule) | Modifies an existing network rule. |
| [ALTER NOTEBOOK](/sql-reference/sql/alter-notebook) | Modifies the properties of an existing [notebook](/user-guide/ui-snowsight/notebooks). |
| [ALTER NOTIFICATION INTEGRATION](/sql-reference/sql/alter-notification-integration) | Modifies the properties for an existing notification integration. |
| [ALTER NOTIFICATION INTEGRATION (email)](/sql-reference/sql/alter-notification-integration-email) | Modifies the properties for an existing notification integration for [sending email messages](/user-guide/notifications/email-notifications). |
| [ALTER NOTIFICATION INTEGRATION (inbound from an Azure Event Grid topic)](/sql-reference/sql/alter-notification-integration-queue-inbound-azure) | Modifies the properties for an existing notification integration for receiving messages from an Azure Event Grid topic. |
| [ALTER NOTIFICATION INTEGRATION (inbound from a Google Pub/Sub topic)](/sql-reference/sql/alter-notification-integration-queue-inbound-gcp) | Modifies the properties for an existing notification integration for receiving messages from a Google Pub/Sub topic. |
| [ALTER NOTIFICATION INTEGRATION (outbound to an Amazon SNS topic)](/sql-reference/sql/alter-notification-integration-queue-outbound-aws) | Modifies the properties for an existing notification integration for [sending a message to an Amazon SNS topic](/user-guide/notifications/creating-notification-integration-amazon-sns). |
| [ALTER NOTIFICATION INTEGRATION (outbound to an Azure Event Grid topic)](/sql-reference/sql/alter-notification-integration-queue-outbound-azure) | Modifies the properties for an existing notification integration for [sending a message to an Azure Event Grid topic](/user-guide/notifications/creating-notification-integration-azure-event-grid). |
| [ALTER NOTIFICATION INTEGRATION (outbound to a Google Pub/Sub topic)](/sql-reference/sql/alter-notification-integration-queue-outbound-gcp) | Modifies the properties for an existing notification integration for [sending a message to a Google Pub/Sub topic](/user-guide/notifications/creating-notification-integration-google-pubsub). |
| [ALTER NOTIFICATION INTEGRATION (webhooks)](/sql-reference/sql/alter-notification-integration-webhooks) | Modifies the properties for an existing notification integration for a [webhook](/user-guide/notifications/webhook-notifications). |
| [ALTER OPENFLOW DATA PLANE](/sql-reference/sql/alter-oflow-data-plane) | Modifies an Openflow data plane integration. |
| [ALTER ONLINE FEATURE TABLE](/sql-reference/sql/alter-online-feature-table) | Modifies the properties of an existing [online feature table](/sql-reference/sql/create-online-feature-table). |
| [ALTER ORGANIZATION ACCOUNT](/sql-reference/sql/alter-organization-account) | Modifies the properties of an existing [organization account](/user-guide/organization-accounts). |
| [ALTER ORGANIZATION PROFILE](/sql-reference/sql/alter-organization-profile) | Modifies the properties of an [organization profile](/user-guide/collaboration/organization-profiles/org-profiles-create-manage) using an inline YAML manifest, or using a YAML manifest file located in a stage location. |
| [ALTER ORGANIZATION USER](/sql-reference/sql/alter-organization-user) | Modifies the properties of an existing [organization user](/user-guide/organization-users). |
| [ALTER ORGANIZATION USER GROUP](/sql-reference/sql/alter-organization-user-group) | Modifies the properties of an existing [organization user group](/user-guide/organization-users#label-org-users-groups). |
| [ALTER PACKAGES POLICY](/sql-reference/sql/alter-packages-policy) | Modifies the properties for an existing [packages policy](/developer-guide/udf/python/packages-policy). |
| [ALTER PASSWORD POLICY](/sql-reference/sql/alter-password-policy) | Modifies the properties for an existing password policy. |
| [ALTER PIPE](/sql-reference/sql/alter-pipe) | Modifies a limited set of properties for an existing pipe object. |
| [ALTER POSTGRES INSTANCE](/sql-reference/sql/alter-postgres-instance) | Modifies the properties of an existing [Snowflake Postgres instance](/user-guide/snowflake-postgres/about). |
| [ALTER PRIVACY POLICY](/sql-reference/sql/alter-privacy-policy) | Modifies the properties of an existing [privacy policy](/user-guide/diff-privacy/differential-privacy-admin-privacy-policies). |
| [ALTER PROCEDURE](/sql-reference/sql/alter-procedure) | Modifies the properties for an existing stored procedure. |
| [ALTER PROJECTION POLICY](/sql-reference/sql/alter-projection-policy) | Replaces the existing [projection policy](/user-guide/projection-policies) rules with new rules or a new comment and allows the renaming of a projection policy. |
| [ALTER REPLICATION GROUP](/sql-reference/sql/alter-replication-group) | Modifies the properties for an existing [replication group](/user-guide/account-replication-intro#label-replication-and-failover-groups). |
| [ALTER RESOURCE MONITOR](/sql-reference/sql/alter-resource-monitor) | Modifies the properties and triggers for an existing [resource monitor](/user-guide/resource-monitors). |
| [ALTER RESTRICTED SESSION SCOPE](/sql-reference/sql/alter-restricted-session-scope) | Modifies the properties of an existing [restricted session scope](/user-guide/restricted-session-scope). |
| [ALTER ROLE](/sql-reference/sql/alter-role) | Modifies the properties for an existing [custom role](/user-guide/security-access-control-overview#label-access-control-overview-roles-custom). |
| [ALTER ROW ACCESS POLICY](/sql-reference/sql/alter-row-access-policy) | Modifies the properties for an existing row access policy, including renaming the policy or replacing the policy rules. |
| [ALTER SCHEMA](/sql-reference/sql/alter-schema) | Modifies the properties for an existing schema, including renaming the schema or swapping it with another schema, and changing the Time Travel data retention period (if you are using Snowflake Enterprise Edition or higher). |
| [ALTER SECRET](/sql-reference/sql/alter-secret) | Modifies the properties of an existing secret. |
| [ALTER SECURITY INTEGRATION](/sql-reference/sql/alter-security-integration) | Modifies the properties for an existing security integration. |
| [ALTER SECURITY INTEGRATION (External API Authentication)](/sql-reference/sql/alter-security-integration-api-auth) | Modifies the properties of an existing security integration created for External API Authentication. |
| [ALTER SECURITY INTEGRATION (AWS IAM Authentication)](/sql-reference/sql/alter-security-integration-aws-iam) | Modifies the properties of an existing security integration created for authenticating with AWS IAM. |
| [ALTER SECURITY INTEGRATION (External OAuth)](/sql-reference/sql/alter-security-integration-oauth-external) | Modifies the properties of an existing security integration created for External OAuth. |
| [ALTER SECURITY INTEGRATION (Snowflake OAuth)](/sql-reference/sql/alter-security-integration-oauth-snowflake) | Modifies the properties of an existing security integration created for a Snowflake OAuth client. |
| [ALTER SECURITY INTEGRATION (SAML2)](/sql-reference/sql/alter-security-integration-saml2) | Modifies the properties of an existing SAML2 security integration. |
| [ALTER SECURITY INTEGRATION (SCIM)](/sql-reference/sql/alter-security-integration-scim) | Modifies the properties of an existing SCIM security integration. |
| [ALTER SEMANTIC VIEW](/sql-reference/sql/alter-semantic-view) | Modifies the comment for an existing [semantic view](/user-guide/views-semantic/overview) or renames a semantic view. |
| [ALTER SEQUENCE](/sql-reference/sql/alter-sequence) | Modifies the properties for an existing sequence. |
| [ALTER SERVICE](/sql-reference/sql/alter-service) | Modifies [Snowpark Container Services service](/developer-guide/snowpark-container-services/working-with-services) configuration, upgrades the code for the service, and allows you to suspend or resume a service. |
| [ALTER SESSION](/sql-reference/sql/alter-session) | Sets parameters that change the behavior for the current session. |
| [ALTER SESSION POLICY](/sql-reference/sql/alter-session-policy) | Modifies the properties for an existing session policy. |
| [ALTER SHARE](/sql-reference/sql/alter-share) | Modifies the properties for an existing [share](/user-guide/data-sharing-intro). |
| [ALTER SNAPSHOT](/sql-reference/sql/alter-snapshot) | Modifies the properties of an existing [snapshot of a block storage volume](/developer-guide/snowpark-container-services/block-storage-volume). |
| [ALTER SNAPSHOT POLICY — Deprecated](/sql-reference/sql/alter-snapshot-policy) | Modifies the properties of a [snapshot](/user-guide/backups) policy. |
| [ALTER SNAPSHOT SET — Deprecated](/sql-reference/sql/alter-snapshot-set) | Modifies the properties for a [snapshot](/user-guide/backups) set. |
| [ALTER STAGE](/sql-reference/sql/alter-stage) | Modifies the properties for an existing named internal or external stage. |
| [ALTER STORAGE INTEGRATION](/sql-reference/sql/alter-storage-integration) | Modifies the properties for an existing storage integration. |
| [ALTER STORAGE LIFECYCLE POLICY](/sql-reference/sql/alter-storage-lifecycle-policy) | Modifies the properties of an existing [storage lifecycle policy](/user-guide/storage-management/storage-lifecycle-policies). |
| [ALTER STREAM](/sql-reference/sql/alter-stream) | Modifies the properties, columns, or constraints for an existing [stream](/user-guide/streams-intro). |
| [ALTER STREAMLIT](/sql-reference/sql/alter-streamlit) | Modifies the properties of an existing Streamlit object. |
| [ALTER TABLE](/sql-reference/sql/alter-table) | Modifies the properties, columns, or constraints for an existing table. |
| [ALTER TABLE … ALTER COLUMN](/sql-reference/sql/alter-table-column) | This topic describes how to modify one or more column properties for a table using an `ALTER COLUMN` clause in a [ALTER TABLE](/sql-reference/sql/alter-table) statement. |
| [ALTER TABLE (event tables)](/sql-reference/sql/alter-table-event-table) | Modifies the properties, columns, or constraints for an existing [event table](/developer-guide/logging-tracing/event-table-setting-up). |
| [ALTER TAG](/sql-reference/sql/alter-tag) | Modifies the properties for an existing tag, including renaming the tag and setting a masking policy on a tag. |
| [ALTER TASK](/sql-reference/sql/alter-task) | Modifies the properties for an existing task. |
| [ALTER TYPE](/sql-reference/sql/alter-type) | Modifies the properties for an existing [user-defined type](/sql-reference/data-types-user-defined). |
| [ALTER USER](/sql-reference/sql/alter-user) | Modifies the properties and object/session parameters for an existing user in the system. |
| [ALTER USER … ADD KEY PAIR](/sql-reference/sql/alter-user-add-key-pair) | Registers a named [key pair](/user-guide/key-pair-auth) for a user. |
| [ALTER USER … ADD PROGRAMMATIC ACCESS TOKEN (PAT)](/sql-reference/sql/alter-user-add-programmatic-access-token) | Creates a [programmatic access token](/user-guide/programmatic-access-tokens) for a user. |
| [ALTER USER … MODIFY KEY PAIR](/sql-reference/sql/alter-user-modify-key-pair) | Changes the name of a [key pair](/user-guide/key-pair-auth) or a property of the key pair. |
| [ALTER USER … MODIFY PROGRAMMATIC ACCESS TOKEN (PAT)](/sql-reference/sql/alter-user-modify-programmatic-access-token) | Changes the name of a [programmatic access token](/user-guide/programmatic-access-tokens) or a property of the token. |
| [ALTER USER … REMOVE KEY PAIR](/sql-reference/sql/alter-user-remove-key-pair) | Removes a named [key pair](/user-guide/key-pair-auth) from a user. |
| [ALTER USER … REMOVE PROGRAMMATIC ACCESS TOKEN (PAT)](/sql-reference/sql/alter-user-remove-programmatic-access-token) | Revokes a [programmatic access token](/user-guide/programmatic-access-tokens) for a user. |
| [ALTER USER … ROTATE KEY PAIR](/sql-reference/sql/alter-user-rotate-key-pair) | Rotates a [key pair](/user-guide/key-pair-auth) by replacing the stored public key with a new public key. |
| [ALTER USER … ROTATE PROGRAMMATIC ACCESS TOKEN (PAT)](/sql-reference/sql/alter-user-rotate-programmatic-access-token) | Rotates [programmatic access token](/user-guide/programmatic-access-tokens), generating a new token secret with an extended expiration time, and expiring the existing token secret. |
| [ALTER VIEW](/sql-reference/sql/alter-view) | Modifies the properties for an existing view. |
| [ALTER WAREHOUSE](/sql-reference/sql/alter-warehouse) | Suspends or resumes a [virtual warehouse](/user-guide/warehouses-overview), or aborts all queries (and other SQL statements) for a warehouse. |
| **B** |  |
| [BEGIN](/sql-reference/sql/begin) | Begins a transaction in the current session. |
| **C** |  |
| [CALL](/sql-reference/sql/call) | Calls a [stored procedure](/developer-guide/stored-procedure/stored-procedures-overview). |
| [CALL (with anonymous procedure)](/sql-reference/sql/call-with) | Creates and calls an anonymous procedure that is like a [stored procedure](/developer-guide/stored-procedure/stored-procedures-overview) but is not stored for later use. |
| [COMMENT](/sql-reference/sql/comment) | Adds a comment or overwrites an existing comment for an existing object. |
| [COMMIT](/sql-reference/sql/commit) | Commits an open transaction in the current session. |
| [COPY FILES](/sql-reference/sql/copy-files) | Copy files from a source location to an output stage. |
| [COPY INTO <location>](/sql-reference/sql/copy-into-location) | Unloads data from a table (or query) into one or more files in one of the following locations. |
| [COPY INTO <table>](/sql-reference/sql/copy-into-table) | Loads data from files to an existing table. |
| [CREATE <object>](/sql-reference/sql/create) | Creates a new object of the specified type. |
| [CREATE ACCOUNT](/sql-reference/sql/create-account) | Creates a new account in your organization. |
| [CREATE AGENT](/sql-reference/sql/create-agent) | Creates a new [Cortex Agent](/user-guide/snowflake-cortex/cortex-agents) object with the specified attributes and specification. |
| [CREATE AGGREGATION POLICY](/sql-reference/sql/create-aggregation-policy) | Creates a new [aggregation policy](/user-guide/aggregation-policies) in the current/specified schema or replaces an existing aggregation policy. |
| [CREATE ALERT](/sql-reference/sql/create-alert) | Creates a new [alert](/user-guide/alerts) in the current schema. |
| [CREATE API INTEGRATION](/sql-reference/sql/create-api-integration) | Creates a new API integration object in the account or replaces an existing API integration. |
| [CREATE APPLICATION](/sql-reference/sql/create-application) | Creates a Snowflake Native App based on an application package or listing. |
| [CREATE APPLICATION PACKAGE](/sql-reference/sql/create-application-package) | Creates a new application package that contains the data content and application logic of Snowflake Native App. |
| [CREATE APPLICATION ROLE](/sql-reference/sql/create-application-role) | Creates a new application role or replaces an existing application role. |
| [CREATE AUTHENTICATION POLICY](/sql-reference/sql/create-authentication-policy) | Creates a new [authentication policy](/user-guide/authentication-policies) in the current or specified schema or replaces an existing authentication policy. |
| [CREATE BACKUP POLICY](/sql-reference/sql/create-backup-policy) | Creates a [backup](/user-guide/backups) policy. |
| [CREATE BACKUP SET](/sql-reference/sql/create-backup-set) | Creates a [backup](/user-guide/backups) set for a table, a schema, or a database. |
| [CREATE CATALOG INTEGRATION](/sql-reference/sql/create-catalog-integration) | Creates a new [catalog integration](/user-guide/tables-iceberg#label-tables-iceberg-catalog-integration-def) for [Apache Iceberg™ tables](/user-guide/tables-iceberg) in the account or replaces an existing catalog integration. |
| [CREATE CATALOG INTEGRATION (AWS Glue)](/sql-reference/sql/create-catalog-integration-glue) | Creates a new [catalog integration](/user-guide/tables-iceberg#label-tables-iceberg-catalog-integration-def) in the account or replaces an existing catalog integration for [Apache Iceberg™ tables](/user-guide/tables-iceberg) that use AWS Glue as the catalog. |
| [CREATE CATALOG INTEGRATION (Object storage)](/sql-reference/sql/create-catalog-integration-object-storage) | Creates a new [catalog integration](/user-guide/tables-iceberg#label-tables-iceberg-catalog-integration-def) in the account or replaces an existing catalog integration for the following sources. |
| [CREATE CATALOG INTEGRATION (Snowflake Open Catalog)](/sql-reference/sql/create-catalog-integration-open-catalog) | Creates a new [catalog integration](/user-guide/tables-iceberg#label-tables-iceberg-catalog-integration-def) for [Apache Iceberg™ tables](/user-guide/tables-iceberg) that integrate with [Snowflake Open Catalog](https://other-docs.snowflake.com/en/opencatalog/overview) in the account or replaces an existing catalog integration. |
| [CREATE CATALOG INTEGRATION (Apache Iceberg™ REST)](/sql-reference/sql/create-catalog-integration-rest) | Creates a new [catalog integration](/user-guide/tables-iceberg#label-tables-iceberg-catalog-integration-def) in the account or replaces an existing catalog integration for [Apache Iceberg™ tables](/user-guide/tables-iceberg) managed in a remote catalog that complies with the open source [Apache Iceberg™ REST OpenAPI specification](https://github.com/apache/iceberg/blob/main/open-api/rest-catalog-open-api.yaml). |
| [CREATE <object> … CLONE](/sql-reference/sql/create-clone) | Creates a copy of an existing object in the system. |
| [CREATE COMPUTE POOL](/sql-reference/sql/create-compute-pool) | Creates a new [compute pool](/developer-guide/snowpark-container-services/working-with-compute-pool) in the current account. |
| [CREATE CONNECTION](/sql-reference/sql/create-connection) | Creates a new [connection](/user-guide/client-redirect) in the account. |
| [CREATE CONTACT](/sql-reference/sql/create-contact) | Creates a new [contact](/user-guide/contacts-using) or replaces an existing contact. |
| [CREATE CORTEX SEARCH SERVICE](/sql-reference/sql/create-cortex-search) | Creates a new [Cortex Search service](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview) or replaces an existing one. |
| [CREATE DATA METRIC FUNCTION](/sql-reference/sql/create-data-metric-function) | Creates a new data metric function (DMF) in the current or specified schema, or replaces an existing data metric function. |
| [CREATE DATABASE](/sql-reference/sql/create-database) | Creates a new database in the system. |
| [CREATE DATABASE (catalog-linked)](/sql-reference/sql/create-database-catalog-linked) | Creates a new [catalog-linked database](/user-guide/tables-iceberg-catalog-linked-database) for Apache Iceberg™ tables that use an external Iceberg REST catalog. |
| [CREATE DATABASE ROLE](/sql-reference/sql/create-database-role) | Create a new [database role](/user-guide/security-access-control-considerations#label-access-control-considerations-database-roles) or replace an existing database role in the system. |
| [CREATE DATASET](/sql-reference/sql/create-dataset) | Creates a new [machine learning dataset](/developer-guide/snowflake-ml/dataset) in the current schema or the schema that you specify. |
| [CREATE DBT PROJECT](/sql-reference/sql/create-dbt-project) | Creates a new [dbt project object](/user-guide/data-engineering/dbt-projects-on-snowflake) or replaces an existing dbt project. |
| [CREATE DCM PROJECT](/sql-reference/sql/create-dcm-project) | Creates a new [DCM project](/user-guide/dcm-projects/dcm-projects-overview) or replaces an existing DCM project. |
| [CREATE DYNAMIC TABLE](/sql-reference/sql/create-dynamic-table) | Creates a [dynamic table](/user-guide/dynamic-tables/overview), based on a specified query. |
| [CREATE EVENT TABLE](/sql-reference/sql/create-event-table) | Creates an [event table](/developer-guide/logging-tracing/event-table-setting-up) that captures events, including logged messages from functions and procedures. |
| [CREATE EXPERIMENT](/sql-reference/sql/create-experiment) | Creates a new [experiment](/developer-guide/snowflake-ml/experiments) or replaces an existing experiment. |
| [CREATE EXTERNAL AGENT](/sql-reference/sql/create-external-agent) | Creates a new [external agent](/user-guide/snowflake-cortex/ai-observability) for use with AI Observability. |
| [CREATE EXTERNAL ACCESS INTEGRATION](/sql-reference/sql/create-external-access-integration) | Creates an [external access integration](/developer-guide/external-network-access/creating-using-external-network-access) for access to external network locations from a UDF or procedure handler. |
| [CREATE EXTERNAL FUNCTION](/sql-reference/sql/create-external-function) | Creates a new [external function](/sql-reference/external-functions). |
| [CREATE EXTERNAL TABLE](/sql-reference/sql/create-external-table) | Creates a new [external table](/user-guide/tables-external-intro) in the current or specified schema or replaces an existing external table. |
| [CREATE EXTERNAL VOLUME](/sql-reference/sql/create-external-volume) | Creates a new [external volume](/user-guide/tables-iceberg#label-tables-iceberg-external-volume-def) for [Apache Iceberg™ tables](/user-guide/tables-iceberg) in the account or replaces an existing external volume. |
| [CREATE FAILOVER GROUP](/sql-reference/sql/create-failover-group) | Creates a new [failover group](/user-guide/account-replication-intro#label-replication-and-failover-groups) of specified objects in the system. |
| [CREATE FEATURE POLICY](/sql-reference/sql/create-feature-policy) | Creates a new [feature policy](/developer-guide/native-apps/ui-consumer-feature-policies). |
| [CREATE FILE FORMAT](/sql-reference/sql/create-file-format) | Creates a named file format that describes a set of staged data to access or load into Snowflake tables. |
| [CREATE FUNCTION](/sql-reference/sql/create-function) | Creates a new [UDF (user-defined function)](/developer-guide/udf/udf-overview). |
| [CREATE FUNCTION (Snowpark Container Services)](/sql-reference/sql/create-function-spcs) | Creates a [service function](/developer-guide/snowpark-container-services/working-with-services#label-snowpark-containers-service-communicating-service-function). |
| [CREATE GATEWAY](/sql-reference/sql/create-gateway) | Creates a new [gateway](/developer-guide/snowpark-container-services/gateway) in the current schema. |
| [CREATE GIT REPOSITORY](/sql-reference/sql/create-git-repository) | Creates a Snowflake Git repository clone in the schema or replaces an existing Git repository clone. |
| [CREATE HYBRID TABLE](/sql-reference/sql/create-hybrid-table) | Creates a new hybrid table in the current/specified schema or replaces an existing table. |
| [CREATE ICEBERG TABLE](/sql-reference/sql/create-iceberg-table) | Creates or replaces an [Apache Iceberg™ table](/user-guide/tables-iceberg) in the current/specified schema. |
| [CREATE ICEBERG TABLE (AWS Glue as the Iceberg catalog)](/sql-reference/sql/create-iceberg-table-aws-glue) | Creates or replaces an [Apache Iceberg™ table](/user-guide/tables-iceberg) in the current/specified schema using an Iceberg table that is registered in the AWS Glue Data Catalog. |
| [CREATE ICEBERG TABLE (Delta files in object storage)](/sql-reference/sql/create-iceberg-table-delta) | Creates or replaces an [Apache Iceberg™ table](/user-guide/tables-iceberg) in the current/specified schema using Delta table files in object storage (external cloud storage). |
| [CREATE ICEBERG TABLE (Iceberg files in object storage)](/sql-reference/sql/create-iceberg-table-iceberg-files) | Creates or replaces an [Apache Iceberg™ table](/user-guide/tables-iceberg) in the current/specified schema using Iceberg files in object storage (external cloud storage). |
| [CREATE ICEBERG TABLE (Iceberg REST catalog)](/sql-reference/sql/create-iceberg-table-rest) | Creates or replaces an [Apache Iceberg™ table](/user-guide/tables-iceberg) in the current/specified schema for an Iceberg REST catalog. |
| [CREATE ICEBERG TABLE (Snowflake as the Iceberg catalog)](/sql-reference/sql/create-iceberg-table-snowflake) | Creates or replaces an [Apache Iceberg™ table](/user-guide/tables-iceberg) that uses [Snowflake as the Iceberg catalog](/user-guide/tables-iceberg#label-tables-iceberg-snowflake-as-catalog) in the current/specified schema. |
| [CREATE IMAGE REPOSITORY](/sql-reference/sql/create-image-repository) | Creates a new [image repository](/developer-guide/snowpark-container-services/working-with-registry-repository) in the current schema. |
| [CREATE INDEX](/sql-reference/sql/create-index) | Creates a new secondary index in an existing [hybrid table](/user-guide/tables-hybrid) and populates the index with data. |
| [CREATE INTEGRATION](/sql-reference/sql/create-integration) | Creates a new integration in the system or replaces an existing integration. |
| [CREATE INTERACTIVE TABLE](/sql-reference/sql/create-interactive-table) | Creates a new [interactive table](/user-guide/interactive) in the current/specified schema or replaces an existing table. |
| [CREATE INTERACTIVE WAREHOUSE](/sql-reference/sql/create-interactive-warehouse) | Creates a new interactive [virtual warehouse](/user-guide/warehouses-overview) optimized for low-latency, high-concurrency workloads with interactive tables. |
| [CREATE JOIN POLICY](/sql-reference/sql/create-join-policy) | Creates a new [join policy](/user-guide/join-policies) in the current/specified schema or replaces an existing join policy. |
| [CREATE LISTING](/sql-reference/sql/create-listing) | Create a free listing to share directly with specific consumers, with an inline YAML manifest, or from a file located in a stage location. |
| [CREATE MAINTENANCE POLICY](/sql-reference/sql/create-maintenance-policy) | Creates a new [maintenance policy](/developer-guide/native-apps/consumer-maintenance-policies) in the current or specified schema. |
| [CREATE MANAGED ACCOUNT](/sql-reference/sql/create-managed-account) | Creates a new managed account. |
| [CREATE MASKING POLICY](/sql-reference/sql/create-masking-policy) | Creates a new masking policy in the current/specified schema or replaces an existing masking policy. |
| [CREATE MATERIALIZED VIEW](/sql-reference/sql/create-materialized-view) | Creates a new materialized view in the current/specified schema, based on a query of an existing table, and populates the view with data. |
| [CREATE MCP SERVER](/sql-reference/sql/create-mcp-server) | Creates a new MCP (Model Context Protocol) server or replaces an existing MCP server. |
| [CREATE MODEL](/sql-reference/sql/create-model) | Creates a new machine learning model in the current/specified schema or replaces an existing model. |
| [CREATE MODEL MONITOR](/sql-reference/sql/create-model-monitor) | Create or replace a [model monitor](/developer-guide/snowflake-ml/model-registry/model-observability) in the current or specified schema. |
| [CREATE NETWORK POLICY](/sql-reference/sql/create-network-policy) | Creates a network policy or replaces an existing network policy. |
| [CREATE NETWORK RULE](/sql-reference/sql/create-network-rule) | Creates a network rule or replaces an existing network rule. |
| [CREATE NOTEBOOK](/sql-reference/sql/create-notebook) | Creates a new [Snowflake notebook](/user-guide/ui-snowsight/notebooks) or replaces an existing notebook. |
| [CREATE NOTEBOOK PROJECT](/sql-reference/sql/create-notebook-project) |  |
| [CREATE NOTIFICATION INTEGRATION](/sql-reference/sql/create-notification-integration) | Creates a new notification integration in the account or replaces an existing integration. |
| [CREATE NOTIFICATION INTEGRATION (email)](/sql-reference/sql/create-notification-integration-email) | Creates a new notification integration in the account or replaces an existing integration for [sending email messages](/user-guide/notifications/email-notifications). |
| [CREATE NOTIFICATION INTEGRATION (inbound from an Azure Event Grid topic)](/sql-reference/sql/create-notification-integration-queue-inbound-azure) | Creates a new notification integration in the account or replaces an existing integration for receiving messages from an Azure Event Grid topic. |
| [CREATE NOTIFICATION INTEGRATION (inbound from a Google Pub/Sub topic)](/sql-reference/sql/create-notification-integration-queue-inbound-gcp) | Creates a new notification integration in the account or replaces an existing integration for receiving messages from a Google Pub/Sub topic. |
| [CREATE NOTIFICATION INTEGRATION (outbound to an Amazon SNS topic)](/sql-reference/sql/create-notification-integration-queue-outbound-aws) | Creates a new notification integration in the account or replaces an existing integration for [sending a message to an Amazon SNS topic](/user-guide/notifications/creating-notification-integration-amazon-sns). |
| [CREATE NOTIFICATION INTEGRATION (outbound to an Azure Event Grid topic)](/sql-reference/sql/create-notification-integration-queue-outbound-azure) | Creates a new notification integration in the account or replaces an existing integration for [sending a message to an Azure Event Grid topic](/user-guide/notifications/creating-notification-integration-azure-event-grid). |
| [CREATE NOTIFICATION INTEGRATION (outbound to a Google Pub/Sub topic)](/sql-reference/sql/create-notification-integration-queue-outbound-gcp) | Creates a new notification integration in the account or replaces an existing integration for [sending a message to a Google Pub/Sub topic](/user-guide/notifications/creating-notification-integration-google-pubsub). |
| [CREATE NOTIFICATION INTEGRATION (webhooks)](/sql-reference/sql/create-notification-integration-webhooks) | Creates a new notification integration or replaces an existing integration for a [webhook](/user-guide/notifications/webhook-notifications). |
| [CREATE ONLINE FEATURE TABLE](/sql-reference/sql/create-online-feature-table) | Creates a new online feature table in the current/specified schema or replaces an existing table. |
| [CREATE OR ALTER <object>](/sql-reference/sql/create-or-alter) | CREATE OR ALTER commands are DDL commands that combine the functionality of the CREATE command and the ALTER command, enabling you to define an object using the syntax supported by the CREATE <object> command with the limitations of the ALTER <object> command. |
| [CREATE ORGANIZATION ACCOUNT](/sql-reference/sql/create-organization-account) | Creates a new [organization account](/user-guide/organization-accounts). |
| [CREATE ORGANIZATION LISTING](/sql-reference/sql/create-organization-listing) | Create an organization listing to share data products securely within your organization. |
| [CREATE ORGANIZATION PROFILE](/sql-reference/sql/create-organization-profile) | Create the organization profile that forms part of the Uniform Listing Locator (ULL) used to publish organizational listings or query organizational listing information without mounting the listing. |
| [CREATE ORGANIZATION USER](/sql-reference/sql/create-organization-user) | Creates a new [organization user](/user-guide/organization-users). |
| [CREATE ORGANIZATION USER GROUP](/sql-reference/sql/create-organization-user-group) | Creates a new [organization user group](/user-guide/organization-users#label-org-users-groups). |
| [CREATE PACKAGES POLICY](/sql-reference/sql/create-packages-policy) | Creates a new [packages policy](/developer-guide/udf/python/packages-policy) or replaces an existing packages policy. |
| [CREATE PASSWORD POLICY](/sql-reference/sql/create-password-policy) | Creates a new password policy or replaces an existing password policy. |
| [CREATE PIPE](/sql-reference/sql/create-pipe) | Creates a new pipe in the system for defining the [COPY INTO <table>](/sql-reference/sql/copy-into-table) statement used by [Snowpipe](/user-guide/data-load-snowpipe-intro) to load data from an ingestion queue, or by [Snowpipe Streaming with high-performance architecture](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-overview) to load data from a streaming source directly into tables. |
| [CREATE POSTGRES INSTANCE](/sql-reference/sql/create-postgres-instance) | Creates a new [Snowflake Postgres instance](/user-guide/snowflake-postgres/about) or creates a fork of an existing instance. |
| [CREATE PRIVACY POLICY](/sql-reference/sql/create-privacy-policy) | Creates a new [privacy policy](/user-guide/diff-privacy/differential-privacy-admin-privacy-policies) or replaces an existing privacy policy. |
| [CREATE PROCEDURE](/sql-reference/sql/create-procedure) | Creates a new [stored procedure](/developer-guide/stored-procedure/stored-procedures-usage). |
| [CREATE PROJECTION POLICY](/sql-reference/sql/create-projection-policy) | Creates a new [projection policy](/user-guide/projection-policies) in the current/specified schema or replaces an existing projection policy. |
| [CREATE PROVISIONED THROUGHPUT](/sql-reference/sql/create-provisioned-throughput) | Creates a new [Provisioned Throughput resource](/user-guide/snowflake-cortex/provisioned-throughput) or replaces an existing one. |
| [CREATE REPLICATION GROUP](/sql-reference/sql/create-replication-group) | Creates a new [replication group](/user-guide/account-replication-intro#label-replication-and-failover-groups) of specified objects in the system. |
| [CREATE RESOURCE MONITOR](/sql-reference/sql/create-resource-monitor) | Creates a new [resource monitor](/user-guide/resource-monitors). |
| [CREATE RESTRICTED SESSION SCOPE](/sql-reference/sql/create-restricted-session-scope) | Creates a new [restricted session scope](/user-guide/restricted-session-scope). |
| [CREATE ROLE](/sql-reference/sql/create-role) | Create a new role or replace an existing role in the system. |
| [CREATE ROW ACCESS POLICY](/sql-reference/sql/create-row-access-policy) | Creates a new row access policy in the current/specified schema or replaces an existing row access policy. |
| [CREATE SCHEMA](/sql-reference/sql/create-schema) | Creates a new schema in the current database. |
| [CREATE SECRET](/sql-reference/sql/create-secret) | Creates a new secret in the current or specified schema or replaces an existing secret. |
| [CREATE SECURITY INTEGRATION](/sql-reference/sql/create-security-integration) | Creates a new security integration in the account or replaces an existing integration. |
| [CREATE SECURITY INTEGRATION (External API Authentication)](/sql-reference/sql/create-security-integration-api-auth) | Creates a new security integration for external API Authentication in the account or replaces an existing integration. |
| [CREATE SECURITY INTEGRATION (AWS IAM Authentication)](/sql-reference/sql/create-security-integration-aws-iam) | Creates a new security integration for external authentication using Amazon Web Services (AWS) Identity and Access Management (IAM). |
| [CREATE SECURITY INTEGRATION (External OAuth)](/sql-reference/sql/create-security-integration-oauth-external) | Creates a new External OAuth security integration in the account or replaces an existing integration. |
| [CREATE SECURITY INTEGRATION (Snowflake OAuth)](/sql-reference/sql/create-security-integration-oauth-snowflake) | Creates a new Snowflake OAuth security integration in the account or replaces an existing integration. |
| [CREATE SECURITY INTEGRATION (SAML2)](/sql-reference/sql/create-security-integration-saml2) | Creates a new SAML2 security integration in the account or replaces an existing integration. |
| [CREATE SECURITY INTEGRATION (SCIM)](/sql-reference/sql/create-security-integration-scim) | Creates a new SCIM security integration in the account or replaces an existing integration. |
| [CREATE SEMANTIC VIEW](/sql-reference/sql/create-semantic-view) | Creates a new [semantic view](/user-guide/views-semantic/overview) in the current/specified schema. |
| [CREATE SEQUENCE](/sql-reference/sql/create-sequence) | Creates a new sequence, which can be used for generating sequential, unique numbers. |
| [CREATE SERVICE](/sql-reference/sql/create-service) | Creates a new [Snowpark Container Services service](/developer-guide/snowpark-container-services/working-with-services) in the current schema. |
| [CREATE SESSION POLICY](/sql-reference/sql/create-session-policy) | Creates a new session policy or replaces an existing session policy. |
| [CREATE SHARE](/sql-reference/sql/create-share) | Creates a new, empty [share](/user-guide/data-sharing-intro). |
| [CREATE SNAPSHOT](/sql-reference/sql/create-snapshot) | Creates or replaces a [snapshot of a block storage volume](/developer-guide/snowpark-container-services/block-storage-volume#label-snowpark-containers-block-storage-manage-snapshots) for a specified volume and service instance. |
| [CREATE SNAPSHOT POLICY — Deprecated](/sql-reference/sql/create-snapshot-policy) | Creates a [snapshot](/user-guide/backups) policy. |
| [CREATE SNAPSHOT SET — Deprecated](/sql-reference/sql/create-snapshot-set) | Creates a [snapshot](/user-guide/backups) set for a table, a schema, or a database. |
| [CREATE STAGE](/sql-reference/sql/create-stage) | Creates a new named *internal* or *external* stage to use for loading data from files into Snowflake tables and unloading data from tables into files. |
| [CREATE STORAGE INTEGRATION](/sql-reference/sql/create-storage-integration) | Creates a new storage integration in the account or replaces an existing integration. |
| [CREATE STORAGE LIFECYCLE POLICY](/sql-reference/sql/create-storage-lifecycle-policy) | Creates a new [storage lifecycle policy](/user-guide/storage-management/storage-lifecycle-policies) in the current or specified schema, or replaces an existing policy. |
| [CREATE STREAM](/sql-reference/sql/create-stream) | Creates a new stream in the current/specified schema or replaces an existing [stream](/user-guide/streams-intro). |
| [CREATE STREAMLIT](/sql-reference/sql/create-streamlit) | Creates a new Streamlit object in Snowflake or replaces an existing Streamlit object in the same schema. |
| [CREATE TABLE](/sql-reference/sql/create-table) | Creates a new table in the current/specified schema, replaces an existing table, or alters an existing table. |
| [CREATE | ALTER TABLE … CONSTRAINT](/sql-reference/sql/create-table-constraint) | This topic describes how to create constraints by specifying a CONSTRAINT clause in a [CREATE TABLE](/sql-reference/sql/create-table), [CREATE HYBRID TABLE](/sql-reference/sql/create-hybrid-table), or [ALTER TABLE](/sql-reference/sql/alter-table) statement. |
| [CREATE TAG](/sql-reference/sql/create-tag) | Creates a new tag or replaces an existing tag in the system. |
| [CREATE TASK](/sql-reference/sql/create-task) | Creates a new [task](/user-guide/tasks-intro) in the current/specified schema or replaces an existing task. |
| [CREATE TYPE](/sql-reference/sql/create-type) | Creates a [user-defined type](/sql-reference/data-types-user-defined). |
| [CREATE USER](/sql-reference/sql/create-user) | Creates a new user or replaces an existing user in the system. |
| [CREATE OR ALTER VERSIONED SCHEMA](/sql-reference/sql/create-versioned-schema) | Creates a new versioned schema or modifies an existing versioned schema. |
| [CREATE VIEW](/sql-reference/sql/create-view) | Creates a new view in the current/specified schema, based on a query of one or more existing tables (or any other valid query expression). |
| [CREATE WAREHOUSE](/sql-reference/sql/create-warehouse) | Creates a new [virtual warehouse](/user-guide/warehouses-overview) in the system. |
| **D** |  |
| [DELETE](/sql-reference/sql/delete) | Remove rows from a table. |
| [DESCRIBE <object>](/sql-reference/sql/desc) | Describes the details for the specified object. |
| [DESCRIBE AGENT](/sql-reference/sql/desc-agent) | Describes the properties of a [Cortex Agent](/user-guide/snowflake-cortex/cortex-agents). |
| [DESCRIBE AGGREGATION POLICY](/sql-reference/sql/desc-aggregation-policy) | Describes the details about an [aggregation policy](/user-guide/aggregation-policies), including the creation date, name, and the SQL expression. |
| [DESCRIBE ALERT](/sql-reference/sql/desc-alert) | Describes the properties of an [alert](/user-guide/alerts). |
| [DESCRIBE APPLICATION](/sql-reference/sql/desc-application) | Displays information about a Snowflake Native App. |
| [DESCRIBE APPLICATION PACKAGE](/sql-reference/sql/desc-application-package) | Displays information about an application package. |
| [DESCRIBE AUTHENTICATION POLICY](/sql-reference/sql/desc-authentication-policy) | Describes the properties of an [authentication policy](/user-guide/authentication-policies). |
| [DESCRIBE AVAILABLE LISTING](/sql-reference/sql/desc-available-listing) | Describes the columns in the listings that are available to the user who runs the command. |
| [DESCRIBE AVAILABLE ORGANIZATION PROFILE](/sql-reference/sql/desc-available-organization-profile) | Describes the active organization profile that can be associated with organizational listings. |
| [DESCRIBE BACKUP POLICY](/sql-reference/sql/desc-backup-policy) | Describes a specific [backup policy](/user-guide/backups). |
| [DESCRIBE BACKUP SET](/sql-reference/sql/desc-backup-set) | Describes a specific [backup set](/user-guide/backups). |
| [DESCRIBE CATALOG INTEGRATION](/sql-reference/sql/desc-catalog-integration) | Describes the properties of a [catalog integration](/user-guide/tables-iceberg#label-tables-iceberg-catalog-integration-def). |
| [DESCRIBE COMPUTE POOL](/sql-reference/sql/desc-compute-pool) | Describes the properties of a [compute pool](/developer-guide/snowpark-container-services/working-with-compute-pool). |
| [DESCRIBE CONFIGURATION](/sql-reference/sql/desc-configuration) | Describes the properties of a [configuration](/developer-guide/native-apps/inter-app-communication). |
| [DESCRIBE CORTEX SEARCH SERVICE](/sql-reference/sql/desc-cortex-search) | Describes the properties of a [Cortex Search service](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview). |
| [DESCRIBE DATABASE](/sql-reference/sql/desc-database) | Describes the database. |
| [DESCRIBE DBT PROJECT](/sql-reference/sql/desc-dbt-project) | Describes the properties of a [dbt project object](/user-guide/data-engineering/dbt-projects-on-snowflake). |
| [DESCRIBE DCM PROJECT](/sql-reference/sql/desc-dcm-project) | Describes the properties of a [DCM project](/user-guide/dcm-projects/dcm-projects-overview). |
| [DESCRIBE DYNAMIC TABLE](/sql-reference/sql/desc-dynamic-table) | Describes the columns in a [dynamic table](/user-guide/dynamic-tables/overview). |
| [DESCRIBE EVENT TABLE](/sql-reference/sql/desc-event-table) | Describes the columns in an [event table](/developer-guide/logging-tracing/event-table-setting-up). |
| [DESCRIBE EXTERNAL AGENT](/sql-reference/sql/desc-external-agent) | Describes the properties of an [external agent](/user-guide/snowflake-cortex/ai-observability). |
| [DESCRIBE EXTERNAL TABLE](/sql-reference/sql/desc-external-table) | Describes the VALUE column and virtual columns in an external table. |
| [DESCRIBE EXTERNAL VOLUME](/sql-reference/sql/desc-external-volume) | Describes the properties of an [external volume](/user-guide/tables-iceberg#label-tables-iceberg-external-volume-def). |
| [DESCRIBE FEATURE POLICY](/sql-reference/sql/desc-feature-policy) | Describes the properties of a [feature policy](/developer-guide/native-apps/ui-consumer-feature-policies). |
| [DESCRIBE FILE FORMAT](/sql-reference/sql/desc-file-format) | Describes the property type (for example, *String* or *Integer*), the defined value of the property, and the default value for each property in a file format object definition. |
| [DESCRIBE FUNCTION](/sql-reference/sql/desc-function) | Describes the specified user-defined function (UDF) or external function, including the signature (i.e. arguments), return value, language, and body (i.e. definition). |
| [DESCRIBE FUNCTION (DMF)](/sql-reference/sql/desc-function-dmf) | Describes the specified data metric function (DMF), including the signature (arguments), return value, language, and body (definition). |
| [DESCRIBE FUNCTION (Snowpark Container Services)](/sql-reference/sql/desc-function-spcs) | Describes the specified [service function](/developer-guide/snowpark-container-services/working-with-services#label-snowpark-containers-service-communicating-service-function), including the signature (arguments), return value, language, and body (path to the Snowpark Container Services service). |
| [DESCRIBE GATEWAY](/sql-reference/sql/desc-gateway) | Describes the properties of a [gateway](/developer-guide/snowpark-container-services/gateway). |
| [DESCRIBE GIT REPOSITORY](/sql-reference/sql/desc-git-repository) | Describes an existing Snowflake [Git repository clone](/developer-guide/git/git-overview). |
| [DESCRIBE ICEBERG TABLE](/sql-reference/sql/desc-iceberg-table) | Describes either the columns in an [Apache Iceberg™ table](/user-guide/tables-iceberg) or the current values, as well as the default values, for the properties of an Iceberg table. |
| [DESCRIBE INTEGRATION](/sql-reference/sql/desc-integration) | Describes the properties of an integration. |
| [DESCRIBE JOIN POLICY](/sql-reference/sql/desc-join-policy) | Describes the details about a [join policy](/user-guide/join-policies), including the creation date, name, and the SQL expression. |
| [DESCRIBE LISTING](/sql-reference/sql/desc-listing) | Describes the columns in a [listing](/collaboration/collaboration-listings-about). |
| [DESCRIBE MAINTENANCE POLICY](/sql-reference/sql/desc-maintenance-policy) | Shows the details of a [maintenance policy](/developer-guide/native-apps/consumer-maintenance-policies). |
| [DESCRIBE MASKING POLICY](/sql-reference/sql/desc-masking-policy) | Describes the details about a masking policy, including the creation date, name, data type, and SQL expression. |
| [DESCRIBE MATERIALIZED VIEW](/sql-reference/sql/desc-materialized-view) | Describes the columns in a materialized view. |
| [DESCRIBE MCP SERVER](/sql-reference/sql/desc-mcp-server) | Describes the properties of an MCP (Model Context Protocol) server. |
| [DESCRIBE MODEL MONITOR](/sql-reference/sql/desc-model-monitor) | Displays information about a specific [model monitor](/developer-guide/snowflake-ml/model-registry/model-observability). |
| [DESCRIBE NETWORK POLICY](/sql-reference/sql/desc-network-policy) | Describes the properties specified for a network policy. |
| [DESCRIBE NETWORK RULE](/sql-reference/sql/desc-network-rule) | Describes the properties specified for a network rule. |
| [DESCRIBE NOTEBOOK](/sql-reference/sql/desc-notebook) | Describes the properties of a [notebook](/user-guide/ui-snowsight/notebooks). |
| [DESCRIBE NOTIFICATION INTEGRATION](/sql-reference/sql/desc-notification-integration) | Describes the properties of a notification integration. |
| [DESCRIBE OPENFLOW DATA PLANE INTEGRATION](/sql-reference/sql/desc-oflow-data-plane-integration) | Describes the columns in an Openflow data plane integration. |
| [DESCRIBE ONLINE FEATURE TABLE](/sql-reference/sql/desc-online-feature-table) | Describes the columns in an [online feature table](/sql-reference/sql/create-online-feature-table). |
| [DESCRIBE ORGANIZATION PROFILE](/sql-reference/sql/desc-organization-profile) | Describes the properties of an organization profile. |
| [DESCRIBE PACKAGES POLICY](/sql-reference/sql/desc-packages-policy) | Describes the details about a packages policy. |
| [DESCRIBE PASSWORD POLICY](/sql-reference/sql/desc-password-policy) | Describes the details about a password policy. |
| [DESCRIBE PIPE](/sql-reference/sql/desc-pipe) | Describes the properties specified for a pipe, as well as the default values of the properties. |
| [DESCRIBE POSTGRES INSTANCE](/sql-reference/sql/desc-postgres-instance) | Describes the properties of a [Snowflake Postgres instance](/user-guide/snowflake-postgres/about). |
| [DESCRIBE PRIVACY POLICY](/sql-reference/sql/desc-privacy-policy) | Describes the properties of a [privacy policy](/user-guide/diff-privacy/differential-privacy-admin-privacy-policies). |
| [DESCRIBE PROCEDURE](/sql-reference/sql/desc-procedure) | Describes the specified stored procedure, including the stored procedure’s signature (i.e. arguments), return value, language, and body (i.e. definition). |
| [DESCRIBE PROJECTION POLICY](/sql-reference/sql/desc-projection-policy) | Describes the details about a [projection policy](/user-guide/projection-policies), including the creation date, name, and the SQL expression. |
| [DESCRIBE RESULT](/sql-reference/sql/desc-result) | Describes the columns in the result of a query. |
| [DESCRIBE RESTRICTED SESSION SCOPE](/sql-reference/sql/desc-restricted-session-scope) | Describes the properties of a [restricted session scope](/user-guide/restricted-session-scope). |
| [DESCRIBE ROW ACCESS POLICY](/sql-reference/sql/desc-row-access-policy) | Describes a row access policy, including the creation date, name, data type, and SQL expression. |
| [DESCRIBE SCHEMA](/sql-reference/sql/desc-schema) | Describes the schema. |
| [DESCRIBE SEARCH OPTIMIZATION](/sql-reference/sql/desc-search-optimization) | Describes the [search optimization configuration](/user-guide/search-optimization/enabling#label-search-optimization-service-add-to-table) for a specified table and its columns. |
| [DESCRIBE SECRET](/sql-reference/sql/desc-secret) | Describes the properties of a secret. |
| [DESCRIBE SEMANTIC VIEW](/sql-reference/sql/desc-semantic-view) | Describes the properties of the logical tables, dimensions, facts, and metrics that make up a [semantic view](/user-guide/views-semantic/overview). |
| [DESCRIBE SEQUENCE](/sql-reference/sql/desc-sequence) | Describes a sequence, including the sequence’s interval. |
| [DESCRIBE SERVICE](/sql-reference/sql/desc-service) | Describes the properties of a [Snowpark Container Services service](/developer-guide/snowpark-container-services/working-with-services) (including job services). |
| [DESCRIBE SESSION POLICY](/sql-reference/sql/desc-session-policy) | Describes the details about a session policy. |
| [DESCRIBE SHARE](/sql-reference/sql/desc-share) | Describes the data objects that are included in a [share](/user-guide/data-sharing-intro). |
| [DESCRIBE SNAPSHOT](/sql-reference/sql/desc-snapshot) | Describes the properties of a [snapshot of a block storage volume](/developer-guide/snowpark-container-services/block-storage-volume). |
| [DESCRIBE SNAPSHOT POLICY](/sql-reference/sql/desc-snapshot-policy) | Describes a specific [snapshot policy](/user-guide/backups). |
| [DESCRIBE SNAPSHOT SET](/sql-reference/sql/desc-snapshot-set) | Describes a specific [snapshot set](/user-guide/backups). |
| [DESCRIBE SPECIFICATION](/sql-reference/sql/desc-specification) | Describes the details about an [app specification](/developer-guide/native-apps/requesting-app-specs). |
| [DESCRIBE STAGE](/sql-reference/sql/desc-stage) | Describes the values specified for the properties in a stage (file format, copy, and location), as well as the default values for each property. |
| [DESCRIBE STORAGE LIFECYCLE POLICY](/sql-reference/sql/desc-storage-lifecycle-policy) | Describes the properties of a [storage lifecycle policy](/user-guide/storage-management/storage-lifecycle-policies). |
| [DESCRIBE STREAM](/sql-reference/sql/desc-stream) | Describes the properties specified for a stream. |
| [DESCRIBE STREAMLIT](/sql-reference/sql/desc-streamlit) | Describes the columns in a Streamlit object. |
| [DESCRIBE TABLE](/sql-reference/sql/desc-table) | Describes either the columns in a table or the set of stage properties for the table (current values and default values). |
| [DESCRIBE TASK](/sql-reference/sql/desc-task) | Shows information about a task. |
| [DESCRIBE TRANSACTION](/sql-reference/sql/desc-transaction) | Describes the [transaction](/sql-reference/transactions), including the start time and the state (running, committed, rolled back). |
| [DESCRIBE TYPE](/sql-reference/sql/desc-type) | Describes a [user-defined type](/sql-reference/data-types-user-defined). |
| [DESCRIBE USER](/sql-reference/sql/desc-user) | Describes a [user](/user-guide/admin-user-management), including the current and default values of the properties of the user. |
| [DESCRIBE VIEW](/sql-reference/sql/desc-view) | Describes the columns in a view (or table). |
| [DESCRIBE WAREHOUSE](/sql-reference/sql/desc-warehouse) | Describes a [virtual warehouse](/user-guide/warehouses-overview). |
| [DROP <object>](/sql-reference/sql/drop) | Removes the specified object from the system. |
| [DROP ACCOUNT](/sql-reference/sql/drop-account) | Drops an account, which initiates the process of [deleting the account](/user-guide/organizations-manage-accounts-delete). |
| [DROP AGENT](/sql-reference/sql/drop-agent) | Removes the specified [Cortex Agent](/user-guide/snowflake-cortex/cortex-agents) with the specified name from the current or specified database and schema. |
| [DROP AGGREGATION POLICY](/sql-reference/sql/drop-aggregation-policy) | Removes an [aggregation policy](/user-guide/aggregation-policies) from the current/specified schema. |
| [DROP ALERT](/sql-reference/sql/drop-alert) | Drops an existing [alert](/user-guide/alerts). |
| [DROP APPLICATION](/sql-reference/sql/drop-application) | Removes an application from the system in the Native Apps Framework. |
| [DROP APPLICATION PACKAGE](/sql-reference/sql/drop-application-package) | Removes an application package from the system in the Native Apps Framework. |
| [DROP APPLICATION ROLE](/sql-reference/sql/drop-application-role) | Removes the specified application role from the system. |
| [DROP AUTHENTICATION POLICY](/sql-reference/sql/drop-authentication-policy) | Removes an [authentication policy](/user-guide/authentication-policies) from the system. |
| [DROP BACKUP POLICY](/sql-reference/sql/drop-backup-policy) | Deletes a [backup](/user-guide/backups) policy. |
| [DROP BACKUP SET](/sql-reference/sql/drop-backup-set) | Deletes a [backup](/user-guide/backups) set. |
| [DROP CATALOG INTEGRATION](/sql-reference/sql/drop-catalog-integration) | Removes a [catalog integration](/user-guide/tables-iceberg#label-tables-iceberg-catalog-integration-def) from the account. |
| [DROP COMPUTE POOL](/sql-reference/sql/drop-compute-pool) | Removes the specified [compute pool](/developer-guide/snowpark-container-services/working-with-compute-pool) from the account. |
| [DROP CONNECTION](/sql-reference/sql/drop-connection) | Removes a connection from the account. |
| [DROP CONTACT](/sql-reference/sql/drop-contact) | Removes the specified [contact](/user-guide/contacts-using) from the current schema. |
| [DROP CORTEX SEARCH SERVICE](/sql-reference/sql/drop-cortex-search) | Removes the specified [Cortex Search service](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview) from the current schema. |
| [DROP DATABASE](/sql-reference/sql/drop-database) | Removes a database from the system. |
| [DROP DATABASE ROLE](/sql-reference/sql/drop-database-role) | Removes the specified database role from the system. |
| [DROP DBT PROJECT](/sql-reference/sql/drop-dbt-project) | Removes the specified [dbt project object](/user-guide/data-engineering/dbt-projects-on-snowflake) from the current or specified schema. |
| [DROP DCM PROJECT](/sql-reference/sql/drop-dcm-project) | Removes the specified [DCM project](/user-guide/dcm-projects/dcm-projects-overview) from the current/specified schema. |
| [DROP DYNAMIC TABLE](/sql-reference/sql/drop-dynamic-table) | Removes a [dynamic table](/user-guide/dynamic-tables/overview) from the current/specified schema. |
| [DROP EXPERIMENT](/sql-reference/sql/drop-experiment) | Removes the specified [experiment](/developer-guide/snowflake-ml/experiments) from the current/specified schema. |
| [DROP EXTERNAL AGENT](/sql-reference/sql/drop-external-agent) | Removes the specified [external agent](/user-guide/snowflake-cortex/ai-observability) from the current/specified schema. |
| [DROP EXTERNAL TABLE](/sql-reference/sql/drop-external-table) | Removes an external table from the current or specified schema. |
| [DROP EXTERNAL VOLUME](/sql-reference/sql/drop-external-volume) | Removes an [external volume](/user-guide/tables-iceberg#label-tables-iceberg-external-volume-def) from the account, but retains a version of the external volume so that it can be recovered using [UNDROP EXTERNAL VOLUME](/sql-reference/sql/undrop-external-volume). |
| [DROP FAILOVER GROUP](/sql-reference/sql/drop-failover-group) | Removes a [failover group](/user-guide/account-replication-intro#label-replication-and-failover-groups) from the account. |
| [DROP FEATURE POLICY](/sql-reference/sql/drop-feature-policy) | Removes the specified [feature policy](/developer-guide/native-apps/ui-consumer-feature-policies). |
| [DROP FILE FORMAT](/sql-reference/sql/drop-file-format) | Removes the specified file format from the current/specified schema. |
| [DROP FUNCTION](/sql-reference/sql/drop-function) | Removes the specified user-defined function (UDF) or external function from the current/specified schema. |
| [DROP FUNCTION (DMF)](/sql-reference/sql/drop-function-dmf) | Removes the specified data metric function (DMF) from the current or specified schema. |
| [DROP FUNCTION (Snowpark Container Services)](/sql-reference/sql/drop-function-spcs) | Removes the specified [service function](/developer-guide/snowpark-container-services/working-with-services#label-snowpark-containers-service-communicating-service-function). |
| [DROP GATEWAY](/sql-reference/sql/drop-gateway) | Removes the specified [gateway](/developer-guide/snowpark-container-services/gateway) from the current or specified schema. |
| [DROP GIT REPOSITORY](/sql-reference/sql/drop-git-repository) | Removes the specified Snowflake Git repository clone from the current/specified schema. |
| [DROP ICEBERG TABLE](/sql-reference/sql/drop-iceberg-table) | Removes an [Apache Iceberg™ table](/user-guide/tables-iceberg) from the current/specified schema, but retains a version of the Iceberg table so that it can be recovered using [UNDROP ICEBERG TABLE](/sql-reference/sql/undrop-iceberg-table). |
| [DROP IMAGE REPOSITORY](/sql-reference/sql/drop-image-repository) | Removes the specified [image repository](/developer-guide/snowpark-container-services/tutorials/tutorial-1) from the current or specified schema. |
| [DROP INDEX](/sql-reference/sql/drop-index) | Drops a secondary index. |
| [DROP INTEGRATION](/sql-reference/sql/drop-integration) | Removes an integration from the account. |
| [DROP JOIN POLICY](/sql-reference/sql/drop-join-policy) | Removes a [join policy](/user-guide/join-policies) from the current/specified schema. |
| [DROP LISTING](/sql-reference/sql/drop-listing) | Removes the specified [listing](/collaboration/collaboration-listings-about) from the system and immediately revokes access for all consumers. |
| [DROP MAINTENANCE POLICY](/sql-reference/sql/drop-maintenance-policy) | Removes a [maintenance policy](/developer-guide/native-apps/consumer-maintenance-policies) from the current or specified schema. |
| [DROP MANAGED ACCOUNT](/sql-reference/sql/drop-managed-account) | Removes a managed account, including all objects created in the account, and immediately restricts access to the account. |
| [DROP MASKING POLICY](/sql-reference/sql/drop-masking-policy) | Removes a masking policy from the system. |
| [DROP MATERIALIZED VIEW](/sql-reference/sql/drop-materialized-view) | Removes the specified materialized view from the current/specified schema. |
| [DROP MCP SERVER](/sql-reference/sql/drop-mcp-server) | Removes the specified MCP (Model Context Protocol) server from the current/specified schema. |
| [DROP MODEL](/sql-reference/sql/drop-model) | Removes a machine learning model from the current/specified schema. |
| [DROP MODEL MONITOR](/sql-reference/sql/drop-model-monitor) | Removes the specified [model monitor](/developer-guide/snowflake-ml/model-registry/model-observability) from the current or specified schema. |
| [DROP NETWORK POLICY](/sql-reference/sql/drop-network-policy) | Removes the specified network policy from the system. |
| [DROP NETWORK RULE](/sql-reference/sql/drop-network-rule) | Removes the specified network rule from the system. |
| [DROP NOTEBOOK](/sql-reference/sql/drop-notebook) | Removes the specified [notebook](/user-guide/ui-snowsight/notebooks) from the current/specified schema, but retains a version of the notebook so that it can be recovered using [UNDROP NOTEBOOK](/sql-reference/sql/undrop-notebook). |
| [DROP ONLINE FEATURE TABLE](/sql-reference/sql/drop-online-feature-table) | Removes the specified [online feature table](/sql-reference/sql/create-online-feature-table) from the current/specified schema. |
| [DROP ORGANIZATION PROFILE](/sql-reference/sql/drop-organization-profile) | Removes an organization profile. |
| [DROP ORGANIZATION USER](/sql-reference/sql/drop-organization-user) | Removes an [organization user](/user-guide/organization-users) from the organization. |
| [DROP ORGANIZATION USER GROUP](/sql-reference/sql/drop-organization-user-group) | Removes an [organization user group](/user-guide/organization-users#label-org-users-groups) from the organization. |
| [DROP PACKAGES POLICY](/sql-reference/sql/drop-packages-policy) | Removes a packages policy from the system. |
| [DROP PASSWORD POLICY](/sql-reference/sql/drop-password-policy) | Removes a password policy from the system. |
| [DROP PIPE](/sql-reference/sql/drop-pipe) | Removes the specified pipe from the current/specified schema. |
| [DROP POSTGRES INSTANCE](/sql-reference/sql/drop-postgres-instance) | Removes the specified [Snowflake Postgres instance](/user-guide/snowflake-postgres/about) from the account. |
| [DROP PRIVACY POLICY](/sql-reference/sql/drop-privacy-policy) | Removes the specified [privacy policy](/user-guide/diff-privacy/differential-privacy-admin-privacy-policies) from the current/specified schema. |
| [DROP PROCEDURE](/sql-reference/sql/drop-procedure) | Removes the specified stored procedure from the current/specified schema. |
| [DROP PROJECTION POLICY](/sql-reference/sql/drop-projection-policy) | Removes a [projection policy](/user-guide/projection-policies) from the current/specified schema. |
| [DROP REPLICATION GROUP](/sql-reference/sql/drop-replication-group) | Removes a [replication group](/user-guide/account-replication-intro#label-replication-and-failover-groups) from the account. |
| [DROP RESOURCE MONITOR](/sql-reference/sql/drop-resource-monitor) | Removes the specified [resource monitor](/user-guide/resource-monitors) from the system. |
| [DROP RESTRICTED SESSION SCOPE](/sql-reference/sql/drop-restricted-session-scope) | Removes the specified [restricted session scope](/user-guide/restricted-session-scope) from the current/specified schema. |
| [DROP ROLE](/sql-reference/sql/drop-role) | Removes the specified role from the system. |
| [DROP ROW ACCESS POLICY](/sql-reference/sql/drop-row-access-policy) | Removes a row access policy from the system. |
| [DROP SCHEMA](/sql-reference/sql/drop-schema) | Removes a schema from the current/specified database. |
| [DROP SECRET](/sql-reference/sql/drop-secret) | Removes a secret from the system. |
| [DROP SEMANTIC VIEW](/sql-reference/sql/drop-semantic-view) | Removes the specified [semantic view](/user-guide/views-semantic/overview) from the current/specified schema. |
| [DROP SEQUENCE](/sql-reference/sql/drop-sequence) | Removes a sequence from the current/specified schema. |
| [DROP SERVICE](/sql-reference/sql/drop-service) | Removes the specified [Snowpark Container Services service](/developer-guide/snowpark-container-services/working-with-services) from the current or specified schema. |
| [DROP SESSION POLICY](/sql-reference/sql/drop-session-policy) | Removes a session policy from the system. |
| [DROP SHARE](/sql-reference/sql/drop-share) | Removes the specified [share](/user-guide/data-sharing-intro) from the system and immediately revokes access for all consumers (i.e. accounts who have created a database from the share). |
| [DROP SNAPSHOT](/sql-reference/sql/drop-snapshot) | Removes a [snapshot of a block storage volume](/developer-guide/snowpark-container-services/block-storage-volume). |
| [DROP SNAPSHOT POLICY — Deprecated](/sql-reference/sql/drop-snapshot-policy) | Deletes a [snapshot](/user-guide/backups) policy. |
| [DROP SNAPSHOT SET — Deprecated](/sql-reference/sql/drop-snapshot-set) | Deletes a [snapshot](/user-guide/backups) set. |
| [DROP STAGE](/sql-reference/sql/drop-stage) | Removes the specified named internal or external stage from the current/specified schema. |
| [DROP STORAGE LIFECYCLE POLICY](/sql-reference/sql/drop-storage-lifecycle-policy) | Removes the specified [storage lifecycle policy](/user-guide/storage-management/storage-lifecycle-policies) from the current or specified schema. |
| [DROP STREAM](/sql-reference/sql/drop-stream) | Removes a stream from the current/specified schema. |
| [DROP STREAMLIT](/sql-reference/sql/drop-streamlit) | Removes the specified Streamlit object from the current/specified schema. |
| [DROP TABLE](/sql-reference/sql/drop-table) | Removes a table from the current or specified schema, but retains a version of the table so that it can be recovered by using [UNDROP TABLE](/sql-reference/sql/undrop-table). |
| [DROP TAG](/sql-reference/sql/drop-tag) | Removes a tag from the system. |
| [DROP TASK](/sql-reference/sql/drop-task) | Removes a task from the current/specified schema. |
| [DROP TYPE](/sql-reference/sql/drop-type) | Removes a [user-defined type](/sql-reference/data-types-user-defined). |
| [DROP USER](/sql-reference/sql/drop-user) | Removes the specified user from the system. |
| [DROP VIEW](/sql-reference/sql/drop-view) | Removes the specified view from the current/specified schema. |
| [DROP WAREHOUSE](/sql-reference/sql/drop-warehouse) | Removes the specified [virtual warehouse](/user-guide/warehouses-overview) from the system. |
| **E** |  |
| [EXECUTE ALERT](/sql-reference/sql/execute-alert) | Manually executes an [alert](/user-guide/alerts) independent of the schedule for the alert. |
| [EXECUTE DBT PROJECT](/sql-reference/sql/execute-dbt-project) | Executes the specified [dbt project object](/user-guide/data-engineering/dbt-projects-on-snowflake) or the dbt project in a Snowflake workspace using the dbt command and command-line options specified. |
| [EXECUTE DCM PROJECT](/sql-reference/sql/execute-dcm-project) | Executes one of the following actions on a [DCM project](/user-guide/dcm-projects/dcm-projects-overview). |
| [EXECUTE IMMEDIATE](/sql-reference/sql/execute-immediate) | Executes a string that contains a SQL statement or a [Snowflake Scripting statement](/developer-guide/snowflake-scripting/blocks). |
| [EXECUTE IMMEDIATE FROM](/sql-reference/sql/execute-immediate-from) | EXECUTE IMMEDIATE FROM executes the SQL statements specified in a file in a stage. |
| [EXECUTE INFERENCE JOB SERVICE](/sql-reference/sql/execute-inference-job-service) | Runs batch inference on a model in the Snowflake Model Registry as a Snowpark Container Services job. |
| [EXECUTE JOB SERVICE](/sql-reference/sql/execute-job-service) | Executes a Snowpark Container Services service as a job. |
| [EXECUTE NOTEBOOK](/sql-reference/sql/execute-notebook) | Executes the notebook outside the Notebook Editor. |
| [EXECUTE NOTEBOOK PROJECT](/sql-reference/sql/execute-notebook-project) | Executes a notebook stored in a notebook project (NPO). |
| [EXECUTE TASK](/sql-reference/sql/execute-task) | Manually triggers an asynchronous single run of a task (either a standalone task or the root task in a [task graph](/user-guide/tasks-graphs#label-task-dag)) independent of the schedule defined for the task. |
| [EXPLAIN](/sql-reference/sql/explain) | Returns the logical execution plan for the specified SQL statement. |
| **G** |  |
| [GET](/sql-reference/sql/get) | Downloads data files from one of the following [internal stage](/user-guide/data-load-overview#label-data-load-overview-internal-stages) types to a local directory or folder on a client machine. |
| [GRANT APPLICATION ROLE](/sql-reference/sql/grant-application-role) | Assigns an application role to an account role, another application role, an application, or a user. |
| [GRANT CALLER](/sql-reference/sql/grant-caller) | Grants [caller grants](/developer-guide/restricted-callers-rights#label-restricted-callers-rights-about-grants) to a role. |
| [GRANT DATABASE ROLE](/sql-reference/sql/grant-database-role) | Assigns a database role to an [account role, another database role](/user-guide/security-access-control-overview#label-access-control-overview-role-types), or a user. |
| [GRANT DATABASE ROLE … TO SHARE](/sql-reference/sql/grant-database-role-share) | Grants a database role to a share. |
| [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) | Transfers ownership of an object or all objects of a specified type in a schema from one role to another role. |
| [GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege) | Grants one or more access privileges on a securable object to a role or database role. |
| [GRANT <privileges> … TO APPLICATION](/sql-reference/sql/grant-privilege-application) | Grants one or more access privileges on a securable object to an application. |
| [GRANT <privileges> … TO APPLICATION ROLE](/sql-reference/sql/grant-privilege-application-role) | Grants one or more access privileges on a securable schema-level object to an application role. |
| [GRANT <privilege> … TO SHARE](/sql-reference/sql/grant-privilege-share) | Grants access privileges for databases and other supported database objects (schemas, UDFs, tables, and views) to a share. |
| [GRANT <privileges> … TO USER](/sql-reference/sql/grant-privilege-user) | Grants one or more access privileges on a securable object to a user. |
| [GRANT ROLE](/sql-reference/sql/grant-role) | Assigns a role to a user or another role. |
| [GRANT SERVICE ROLE](/sql-reference/sql/grant-service-role) | Assigns a service role to an account role, application role, or database role. |
| **I** |  |
| [INSERT](/sql-reference/sql/insert) | Updates a table by inserting one or more rows into the table. |
| [INSERT (multi-table)](/sql-reference/sql/insert-multi-table) | Updates multiple tables by inserting one or more rows with column values (from a query) into the tables. |
| **L** |  |
| [LIST](/sql-reference/sql/list) | Returns a list of files from one of the following Snowflake storage features. |
| **M** |  |
| [MERGE](/sql-reference/sql/merge) | Inserts, updates, and deletes values in a table that are based on values in a second table or a subquery. |
| **P** |  |
| [PUT](/sql-reference/sql/put) | Uploads one or more data files from a local file system onto an [internal stage](/user-guide/data-load-local-file-system-create-stage). |
| **R** |  |
| [REMOVE](/sql-reference/sql/remove) | Removes files from either an external (external cloud storage) or internal (i.e. Snowflake) stage. |
| [REVOKE APPLICATION ROLE](/sql-reference/sql/revoke-application-role) | Revokes an application role from an account role or another application role. |
| [REVOKE CALLER](/sql-reference/sql/revoke-caller) | Revokes privileges that were previously granted to an executable owner using a [caller grant](/developer-guide/restricted-callers-rights#label-restricted-callers-rights-about-grants). |
| [REVOKE DATABASE ROLE](/sql-reference/sql/revoke-database-role) | Revokes a database role from an [account role or another database role](/user-guide/security-access-control-overview#label-access-control-overview-role-types). |
| [REVOKE DATABASE ROLE … FROM SHARE](/sql-reference/sql/revoke-database-role-share) | Revokes a database role from a share. |
| [REVOKE <privileges> … FROM ROLE](/sql-reference/sql/revoke-privilege) | Removes one or more privileges on a securable object from a role or database role. |
| [REVOKE <privileges> … FROM APPLICATION](/sql-reference/sql/revoke-privilege-application) | Revokes one or more access privileges on a securable object from an application. |
| [REVOKE <privileges> … FROM APPLICATION ROLE](/sql-reference/sql/revoke-privilege-application-role) | Revokes one or more access privileges on a securable schema-level object from an application role. |
| [REVOKE <privilege> … FROM SHARE](/sql-reference/sql/revoke-privilege-share) | Revokes access privileges for databases and other supported database objects (schemas, tables, and views) from a share. |
| [REVOKE <privileges> … FROM USER](/sql-reference/sql/revoke-privilege-user) | Removes one or more privileges on a securable object from a user. |
| [REVOKE ROLE](/sql-reference/sql/revoke-role) | Removes a role from another role or a user. |
| [REVOKE SERVICE ROLE](/sql-reference/sql/revoke-service-role) | Revokes a service role from an account role, application role, or database role. |
| [ROLLBACK](/sql-reference/sql/rollback) | Rolls back an open transaction in the current session. |
| **S** |  |
| [SELECT](/sql-reference/sql/select) | SELECT can be used as either a statement or as a clause within other statements. |
| [SET](/sql-reference/sql/set) | Initializes the value of a [session variable](/sql-reference/session-variables) to the result of a SQL expression. |
| [SHOW <objects>](/sql-reference/sql/show) | Lists the existing objects for the specified object type. |
| [SHOW ACCOUNTS](/sql-reference/sql/show-accounts) | Lists all the accounts in your organization, excluding [managed accounts](/user-guide/data-sharing-reader-create). |
| [SHOW AGENTS](/sql-reference/sql/show-agents) | Lists the [Cortex Agents](/user-guide/snowflake-cortex/cortex-agents) for which you have access privileges. |
| [SHOW AGGREGATION POLICIES](/sql-reference/sql/show-aggregation-policies) | Lists information about existing [aggregation policies](/user-guide/aggregation-policies), including the creation date, database and schema names, owner, and any available comments. |
| [SHOW ALERTS](/sql-reference/sql/show-alerts) | Lists the [alerts](/user-guide/alerts) for which you have access privileges. |
| [SHOW APPLICATION PACKAGES](/sql-reference/sql/show-application-packages) | Lists the application packages for which you have access privileges across your entire account in the Native Apps Framework. |
| [SHOW APPLICATION ROLES](/sql-reference/sql/show-application-roles) | Lists the application roles in the specified app for which you have access privileges. |
| [SHOW APPLICATIONS](/sql-reference/sql/show-applications) | Lists the Snowflake Native Apps that you have access privileges for across your entire account. |
| [SHOW AUTHENTICATION POLICIES](/sql-reference/sql/show-authentication-policies) | Lists [authentication policy](/user-guide/authentication-policies) information, including the creation date, database and schema names, owner, and any available comments. |
| [SHOW AVAILABLE LISTINGS](/sql-reference/sql/show-available-listings) | Lists the listings that are available to the user who runs the command. |
| [SHOW AVAILABLE OFFERS](/sql-reference/sql/show-available-offers) | Lists the [offers](/user-guide/collaboration/listings/pricing-plans-offers/pricing-plans-and-offers#label-listings-offers) that are available to the user who runs the command. |
| [SHOW AVAILABLE ORGANIZATION PROFILES](/sql-reference/sql/show-available-organization-profiles) | Lists the organization profiles available in the user’s organization. |
| [SHOW BACKUP POLICIES](/sql-reference/sql/show-backup-policies) | Lists all the [backup](/user-guide/backups) policies in your account for which you have access privileges. |
| [SHOW BACKUP SETS](/sql-reference/sql/show-backup-sets) | Lists all the [backup](/user-guide/backups) sets for which you have access privileges. |
| [SHOW BACKUPS IN BACKUP SET](/sql-reference/sql/show-backups-in-backup-set) | Lists all the [backups](/user-guide/backups) in a backup set. |
| [SHOW CALLER GRANTS](/sql-reference/sql/show-caller-grants) | Lists the [caller grants](/developer-guide/restricted-callers-rights#label-restricted-callers-rights-about-grants) being used to implement restricted caller’s rights. |
| [SHOW CATALOG INTEGRATIONS](/sql-reference/sql/show-catalog-integrations) | Lists the [catalog integrations](/user-guide/tables-iceberg#label-tables-iceberg-catalog-integration-def) in your account. |
| [SHOW CHANNELS](/sql-reference/sql/show-channels) | Lists the [Snowpipe Streaming channels](/user-guide/snowpipe-streaming/data-load-snowpipe-streaming-overview) for which you have access privileges. |
| [SHOW CLASSES](/sql-reference/sql/show-classes) | Lists all available classes. |
| [SHOW COLUMNS](/sql-reference/sql/show-columns) | Lists the columns in the tables or views and the dimensions, facts, and metrics in the [semantic views](/user-guide/views-semantic/overview) for which you have access privileges. |
| [SHOW COMPUTE POOL INSTANCE FAMILIES](/sql-reference/sql/show-compute-pool-instance-families) | Lists the available [compute pool instance families](/developer-guide/snowpark-container-services/working-with-compute-pool#label-spcs-working-with-compute-pools-instance-family-table) that you can use to create a compute pool. |
| [SHOW COMPUTE POOLS](/sql-reference/sql/show-compute-pools) | Lists the [compute pools](/developer-guide/snowpark-container-services/working-with-compute-pool) in your account for which you have access privileges. |
| [SHOW CONFIGURATIONS](/sql-reference/sql/show-configurations) | Lists the [configurations](/developer-guide/native-apps/inter-app-communication) in the specified app for which you have access privileges. |
| [SHOW CONNECTIONS](/sql-reference/sql/show-connections) | Lists the [connections](/user-guide/client-redirect) for which you have access privileges. |
| [SHOW CONTACTS](/sql-reference/sql/show-contacts) | Lists the [contacts](/user-guide/contacts-using) for which you have access privileges. |
| [SHOW CORTEX SEARCH SERVICES](/sql-reference/sql/show-cortex-search) | Lists the [Cortex Search services](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview) for which you have access privileges. |
| [SHOW DATA METRIC FUNCTIONS](/sql-reference/sql/show-data-metric-functions) | Lists the [data metric functions](/user-guide/data-quality-intro) (DMFs) for which you have access privileges. |
| [SHOW DATABASE ROLES](/sql-reference/sql/show-database-roles) | Lists all the database roles in the specified database. |
| [SHOW DATABASES](/sql-reference/sql/show-databases) | Lists the databases for which you have access privileges across your entire account, including dropped databases that are still within the Time Travel retention period and, therefore, can be undropped. |
| [SHOW DATABASES IN FAILOVER GROUP](/sql-reference/sql/show-databases-in-failover-group) | Lists databases in a [failover group](/user-guide/account-replication-intro#label-replication-and-failover-groups). |
| [SHOW DATABASES IN REPLICATION GROUP](/sql-reference/sql/show-databases-in-replication-group) | Lists databases in a [replication group](/user-guide/account-replication-intro#label-replication-and-failover-groups). |
| [SHOW DATASETS](/sql-reference/sql/show-datasets) | Displays information about the datasets in your account. |
| [SHOW DBT PROJECTS](/sql-reference/sql/show-dbt-projects) | Lists the [dbt project objects](/user-guide/data-engineering/dbt-projects-on-snowflake) for which you have access privileges. |
| [SHOW DCM PROJECTS](/sql-reference/sql/show-dcm-projects) | Lists the [DCM projects](/user-guide/dcm-projects/dcm-projects-overview) for which you have at least READ privilege. |
| [SHOW DELEGATED AUTHORIZATIONS](/sql-reference/sql/show-delegated-authorizations) | Lists the active delegated authorizations for which you have access privileges. |
| [SHOW DEPLOYMENTS IN DCM PROJECT](/sql-reference/sql/show-deployments-in-dcm-project) | Shows all deployments for the specified [DCM project](/user-guide/dcm-projects/dcm-projects-overview). |
| [SHOW DYNAMIC TABLES](/sql-reference/sql/show-dynamic-tables) | Lists the [dynamic tables](/user-guide/dynamic-tables/overview) for which you have access privileges. |
| [SHOW ENDPOINTS](/sql-reference/sql/show-endpoints) | Lists the endpoints in a [Snowpark Container Services service](/developer-guide/snowpark-container-services/working-with-services) (or a job service). |
| [SHOW ENTITIES IN DCM PROJECT](/sql-reference/sql/show-entities-in-dcm-project) | Shows all Snowflake objects that are currently managed by a specified [DCM project](/user-guide/dcm-projects/dcm-projects-overview). |
| [SHOW EVENT TABLES](/sql-reference/sql/show-event-tables) | Lists the [event tables](/developer-guide/logging-tracing/event-table-setting-up) for which you have access privileges, including dropped tables that are still within the Time Travel retention period and, therefore, can be undropped. |
| [SHOW EXPERIMENTS](/sql-reference/sql/show-experiments) | Lists the [experiments](/developer-guide/snowflake-ml/experiments) for which you have access privileges. |
| [SHOW EXTERNAL AGENTS](/sql-reference/sql/show-external-agents) | Lists the [external agents](/user-guide/snowflake-cortex/ai-observability) for which you have access privileges. |
| [SHOW EXTERNAL FUNCTIONS](/sql-reference/sql/show-external-functions) | Lists all the external functions created for your account. |
| [SHOW EXTERNAL TABLES](/sql-reference/sql/show-external-tables) | Lists the external tables for which you have access privileges. |
| [SHOW EXTERNAL VOLUMES](/sql-reference/sql/show-external-volumes) | Lists the [external volumes](/user-guide/tables-iceberg#label-tables-iceberg-external-volume-def) in your account for which you have access privileges. |
| [SHOW FAILOVER GROUPS](/sql-reference/sql/show-failover-groups) | Lists the primary and secondary [failover groups](/user-guide/account-replication-intro#label-replication-and-failover-groups) in your account, as well as the failover groups in other accounts that are associated with your account. |
| [SHOW FEATURE POLICIES](/sql-reference/sql/show-feature-policies) | Lists the [feature policies](/developer-guide/native-apps/ui-consumer-feature-policies) for which you have access privileges. |
| [SHOW FILE FORMATS](/sql-reference/sql/show-file-formats) | Lists the file formats for which you have access privileges. |
| [SHOW FUNCTIONS](/sql-reference/sql/show-functions) | Lists all functions that you have privileges to access, including built-in, user-defined, and external functions. |
| [SHOW FUNCTIONS IN MODEL](/sql-reference/sql/show-functions-in-model) | Lists functions defined in machine learning models. |
| [SHOW GATEWAYS](/sql-reference/sql/show-gateways) | Lists the [gateway](/developer-guide/snowpark-container-services/gateway) for which you have access privileges. |
| [SHOW GIT BRANCHES](/sql-reference/sql/show-git-branches) | Lists the branches in the specified Snowflake Git repository clone. |
| [SHOW GIT REPOSITORIES](/sql-reference/sql/show-git-repositories) | Lists the [Git repository clones](/developer-guide/git/git-overview) that you have privileges to access. |
| [SHOW GIT TAGS](/sql-reference/sql/show-git-tags) | Lists the tags in the specified Snowflake [Git repository clone](/developer-guide/git/git-overview). |
| [SHOW GLOBAL ACCOUNTS](/sql-reference/sql/show-global-accounts) | Lists all the accounts in your organization that are enabled for replication and indicates the Snowflake Region in which each account is located. |
| [SHOW GRANTS](/sql-reference/sql/show-grants) | Lists all access control privileges that have been explicitly granted to roles, users, and shares. |
| [SHOW GRANTS IN DCM PROJECT](/sql-reference/sql/show-grants-in-dcm-project) | `SHOW GRANTS IN DCM PROJECT` lists all grants deployed and managed by the specified [DCM project](/user-guide/dcm-projects/dcm-projects-overview). |
| [SHOW HYBRID TABLES](/sql-reference/sql/show-hybrid-tables) | Lists the [hybrid tables](/user-guide/tables-hybrid) for which you have access privileges. |
| [SHOW ICEBERG TABLES](/sql-reference/sql/show-iceberg-tables) | Lists the [Apache Iceberg™ tables](/user-guide/tables-iceberg) for which you have access privileges. |
| [SHOW IMAGE REPOSITORIES](/sql-reference/sql/show-image-repositories) | Lists the [image repositories](/developer-guide/snowpark-container-services/tutorials/tutorial-1) for which you have access privileges. |
| [SHOW IMAGES IN IMAGE REPOSITORY](/sql-reference/sql/show-images-in-image-repository) | Lists the images in an [image repository](/developer-guide/snowpark-container-services/working-with-registry-repository). |
| [SHOW INDEXES](/sql-reference/sql/show-indexes) | Lists all the indexes in your account for which you have access privileges. |
| [SHOW INTEGRATIONS](/sql-reference/sql/show-integrations) | Lists the integrations in your account. |
| [SHOW JOIN POLICIES](/sql-reference/sql/show-join-policies) | Lists information about existing [join policies](/user-guide/join-policies), including the creation date, database and schema names, owner, and any available comments. |
| [SHOW LISTINGS](/sql-reference/sql/show-listings) | Lists the [listings](/collaboration/collaboration-listings-about) that you have privileges to access. |
| [SHOW LISTINGS IN FAILOVER GROUP](/sql-reference/sql/show-listings-in-failover-group) | Shows the listings in a [failover group](/user-guide/account-replication-intro#label-replication-and-failover-groups). |
| [SHOW LOCKS](/sql-reference/sql/show-locks) | Lists all running transactions that have locks on resources. |
| [SHOW MAINTENANCE POLICIES](/sql-reference/sql/show-maintenance-policies) | Lists the [maintenance policies](/developer-guide/native-apps/consumer-maintenance-policies) applied to the specified account or app. |
| [SHOW MANAGED ACCOUNTS](/sql-reference/sql/show-managed-accounts) | Lists the managed accounts created for your account. |
| [SHOW MASKING POLICIES](/sql-reference/sql/show-masking-policies) | Lists masking policy information, including the creation date, database and schema names, owner, and any available comments. |
| [SHOW MATERIALIZED VIEWS](/sql-reference/sql/show-materialized-views) | Lists the materialized views that you have privileges to access. |
| [SHOW MCP SERVERS](/sql-reference/sql/show-mcp-servers) | Lists the MCP (Model Context Protocol) servers for which you have access privileges. |
| [SHOW MFA METHODS](/sql-reference/sql/show-mfa-methods) | Lists the [second factors of authentication](/user-guide/security-mfa-second-factor) that a user enrolled in multi-factor authentication uses to sign in to Snowflake. |
| [SHOW MODEL MONITORS](/sql-reference/sql/show-model-monitors) | Lists all [model monitor](/developer-guide/snowflake-ml/model-registry/model-observability) that you can access in the current or specified schema and displays information about each one. |
| [SHOW MODELS](/sql-reference/sql/show-models) | Lists the machine learning models that you have privileges to access. |
| [SHOW NETWORK POLICIES](/sql-reference/sql/show-network-policies) | Lists all network policies defined in the system. |
| [SHOW NETWORK RULES](/sql-reference/sql/show-network-rules) | Lists all network rules defined in the system. |
| [SHOW NOTEBOOK PROJECTS](/sql-reference/sql/show-notebook-projects) | Lists the notebook projects (Snowflake `NOTEBOOK` objects) visible to the current role. |
| [SHOW NOTEBOOKS](/sql-reference/sql/show-notebooks) | Lists the [notebooks](/user-guide/ui-snowsight/notebooks) for which you have access privileges. |
| [SHOW NOTIFICATION INTEGRATIONS](/sql-reference/sql/show-notification-integrations) | Lists the notification integrations in your account. |
| [SHOW OBJECTS](/sql-reference/sql/show-objects) | Lists the tables and views for which you have access privileges. |
| [SHOW OBJECTS OWNED BY APPLICATION](/sql-reference/sql/show-objects-owned-by-application) | Lists the objects owned by an app that exists outside the app. |
| [SHOW OFFERS](/sql-reference/sql/show-offers) | Provides information about all [offers](/user-guide/collaboration/listings/pricing-plans-offers/pricing-plans-and-offers#label-listings-offers) added to a listing. |
| [SHOW OPENFLOW DATA PLANE INTEGRATIONS](/sql-reference/sql/show-oflow-data-plane-integration) | List OPENFLOW DATA PLANE INTEGRATIONS. |
| [SHOW ONLINE FEATURE TABLES](/sql-reference/sql/show-online-feature-tables) | Lists the [online feature tables](/sql-reference/sql/create-online-feature-table) for which you have access privileges. |
| [SHOW ORGANIZATION ACCOUNTS](/sql-reference/sql/show-organization-accounts) | Lists the [organization account](/user-guide/organization-accounts) of the organization. |
| [SHOW ORGANIZATION PROFILES](/sql-reference/sql/show-organization-profiles) | Lists the organization profiles for which you have access privileges. |
| [SHOW ORGANIZATION USER GROUPS](/sql-reference/sql/show-organization-user-groups) | Lists [organization user groups](/user-guide/organization-users#label-org-users-groups). |
| [SHOW ORGANIZATION USERS](/sql-reference/sql/show-organization-users) | Lists [organization users](/user-guide/organization-users). |
| [SHOW PACKAGES POLICIES](/sql-reference/sql/show-packages-policies) | Lists packages policy information. |
| [SHOW PARAMETERS](/sql-reference/sql/show-parameters) | Lists all the account, session, and object parameters that can be set, as well as the current and default values for each parameter. |
| [SHOW PASSWORD POLICIES](/sql-reference/sql/show-password-policies) | Lists password policy information, including the creation date, database and schema names, owner, and any available comments. |
| [SHOW PIPES](/sql-reference/sql/show-pipes) | Lists the pipes for which you have access privileges. |
| [SHOW POSTGRES INSTANCES](/sql-reference/sql/show-postgres-instances) | Lists the [Snowflake Postgres instances](/user-guide/snowflake-postgres/about) for which you have access privileges. |
| [SHOW PRICING PLANS](/sql-reference/sql/show-pricing-plans) | Lists visible and hidden [pricing plans](/user-guide/collaboration/listings/pricing-plans-offers/pricing-plans-and-offers#label-listings-pricing-plans). |
| [SHOW PRIMARY KEYS](/sql-reference/sql/show-primary-keys) | Lists primary keys for one or more tables. |
| [SHOW PRIVACY POLICIES](/sql-reference/sql/show-privacy-policies) | Lists the [privacy policies](/user-guide/diff-privacy/differential-privacy-admin-privacy-policies) for which you have access privileges. |
| [SHOW PRIVILEGES](/sql-reference/sql/show-privileges) | Lists the privileges granted to an application. |
| [SHOW PROCEDURES](/sql-reference/sql/show-procedures) | Lists all stored procedures that you have privileges to access, including built-in and user-defined procedures. |
| [SHOW PROJECTION POLICIES](/sql-reference/sql/show-projection-policies) | Lists [projection policy](/user-guide/projection-policies) information, including the creation date, database and schema names, owner, and any available comments. |
| [SHOW REFERENCES](/sql-reference/sql/show-references) | Lists the references defined for an application in the manifest file and the references the consumer has associated to the application. |
| [SHOW REGIONS](/sql-reference/sql/show-regions) | Lists all the [regions](/user-guide/intro-regions) in which accounts can be created. |
| [SHOW RELEASE CHANNELS](/sql-reference/sql/show-release-channels) | Lists the [release channels](/developer-guide/native-apps/release-channels) for an application package or listing. |
| [SHOW RELEASE DIRECTIVES](/sql-reference/sql/show-release-directives) | Lists the release directives defined for an application package. |
| [SHOW REPLICATION ACCOUNTS](/sql-reference/sql/show-replication-accounts) | Lists all the accounts in your organization that are enabled for replication and indicates the [region](/user-guide/intro-regions) in which each account is located. |
| [SHOW REPLICATION DATABASES](/sql-reference/sql/show-replication-databases) | Lists all the primary and secondary databases (that is to say, all the databases for which replication has been enabled) in your account and indicates the [region](/user-guide/intro-regions) in which each account is located. |
| [SHOW REPLICATION GROUPS](/sql-reference/sql/show-replication-groups) | Displays information about [replication groups and failover groups](/user-guide/account-replication-intro#label-replication-and-failover-groups). |
| [SHOW RESOURCE MONITORS](/sql-reference/sql/show-resource-monitors) | Lists all the resource monitors in your account for which you have access privileges. |
| [SHOW RESTRICTED SESSION SCOPES](/sql-reference/sql/show-restricted-session-scopes) | Lists [restricted session scope](/user-guide/restricted-session-scope) objects for which you have access privileges. |
| [SHOW ROLES](/sql-reference/sql/show-roles) | Lists all the roles which you can view across your entire account, including the system-defined roles and any custom roles that exist. |
| [SHOW ROLES IN SERVICE](/sql-reference/sql/show-roles-in-service) | Lists all the service roles associated with a service. |
| [SHOW ROW ACCESS POLICIES](/sql-reference/sql/show-row-access-policies) | Lists the row access policies for which you have access privileges. |
| [SHOW RUN … IN EXPERIMENT](/sql-reference/sql/show-run-in-experiment) | Displays logged parameters or metrics for [experiment runs](/developer-guide/snowflake-ml/experiments). |
| [SHOW RUNS IN EXPERIMENT](/sql-reference/sql/show-runs-in-experiment) | Lists the runs in an [experiment](/developer-guide/snowflake-ml/experiments). |
| [SHOW SCHEMAS](/sql-reference/sql/show-schemas) | Lists the schemas for which you have access privileges, including dropped schemas that are still within the Time Travel retention period and, therefore, can be undropped. |
| [SHOW SECRETS](/sql-reference/sql/show-secrets) | Lists the secrets for which you have rights to see. |
| [SHOW SEMANTIC DIMENSIONS](/sql-reference/sql/show-semantic-dimensions) | Lists the dimensions in the [semantic views](/user-guide/views-semantic/overview) for which you have access privileges. |
| [SHOW SEMANTIC DIMENSIONS FOR METRIC](/sql-reference/sql/show-semantic-dimensions-for-metric) | Lists the dimensions that you can return when querying a specific metric in a [semantic view](/user-guide/views-semantic/overview). |
| [SHOW SEMANTIC FACTS](/sql-reference/sql/show-semantic-facts) | Lists the facts in the [semantic views](/user-guide/views-semantic/overview) for which you have access privileges. |
| [SHOW SEMANTIC METRICS](/sql-reference/sql/show-semantic-metrics) | Lists the metrics in the [semantic views](/user-guide/views-semantic/overview) for which you have access privileges. |
| [SHOW SEMANTIC VIEWS](/sql-reference/sql/show-semantic-views) | Lists the [semantic views](/user-guide/views-semantic/overview) for which you have access privileges. |
| [SHOW SEQUENCES](/sql-reference/sql/show-sequences) | Lists all the sequences for which you have access privileges. |
| [SHOW SERVICE CONTAINERS IN SERVICE](/sql-reference/sql/show-service-containers-in-service) | Lists the containers in all instances of a [service](/developer-guide/snowpark-container-services/working-with-services). |
| [SHOW SERVICE INSTANCES IN SERVICE](/sql-reference/sql/show-service-instances-in-service) | Lists instances of a [service](/developer-guide/snowpark-container-services/working-with-services). |
| [SHOW SERVICE VOLUMES IN SERVICE](/sql-reference/sql/show-service-volumes-in-service) | Lists the storage volumes for all instances of a [service](/developer-guide/snowpark-container-services/working-with-services). |
| [SHOW SERVICES](/sql-reference/sql/show-services) | Lists the [Snowpark Container Services services](/developer-guide/snowpark-container-services/working-with-services) (including job services) for which you have access privileges. |
| [SHOW SESSION POLICIES](/sql-reference/sql/show-session-policies) | Lists session policy information, including the creation date, database and schema names, owner, and any available comments. |
| [SHOW SHARED CONTENT IN APPLICATION PACKAGE](/sql-reference/sql/show-shared-content) | Shows all of the objects for which you have access privileges that have been shared from a Declarative Native App application package. |
| [SHOW SHARES](/sql-reference/sql/show-shares) | Lists all [shares](/user-guide/data-sharing-intro) available in the system. |
| [SHOW SHARES IN FAILOVER GROUP](/sql-reference/sql/show-shares-in-failover-group) | Lists shares in a [failover group](/user-guide/account-replication-intro#label-replication-and-failover-groups). |
| [SHOW SHARES IN REPLICATION GROUP](/sql-reference/sql/show-shares-in-replication-group) | Lists shares in a [replication group](/user-guide/account-replication-intro#label-replication-and-failover-groups). |
| [SHOW SNAPSHOT POLICIES — Deprecated](/sql-reference/sql/show-snapshot-policies) | Lists all the [snapshot](/user-guide/backups) policies in your account for which you have access privileges. |
| [SHOW SNAPSHOT SETS — Deprecated](/sql-reference/sql/show-snapshot-sets) | Lists all the [snapshot](/user-guide/backups) sets for which you have access privileges. |
| [SHOW SNAPSHOTS](/sql-reference/sql/show-snapshots) | Lists the [snapshots of block storage volumes](/developer-guide/snowpark-container-services/block-storage-volume) for which you have access privileges. |
| [SHOW SNAPSHOTS IN SNAPSHOT SET — Deprecated](/sql-reference/sql/show-snapshots-in-snapshot-set) | Lists all the [snapshots](/user-guide/backups) in a snapshot set. |
| [SHOW SPECIFICATIONS](/sql-reference/sql/show-specifications) | Lists the app specifications that have been defined for an app. |
| [SHOW STAGES](/sql-reference/sql/show-stages) | Lists all the stages for which you have access privileges. |
| [SHOW STORAGE LIFECYCLE POLICIES](/sql-reference/sql/show-storage-lifecycle-policies) | Lists the [storage lifecycle policies](/user-guide/storage-management/storage-lifecycle-policies) for which you have access privileges. |
| [SHOW STREAMLITS](/sql-reference/sql/show-streamlits) | Lists the Streamlit objects for which you have access privileges. |
| [SHOW STREAMS](/sql-reference/sql/show-streams) | Lists the streams for which you have access privileges. |
| [SHOW TABLES](/sql-reference/sql/show-tables) | Lists the tables for which you have access privileges, including dropped tables that are still within the Time Travel retention period and, therefore, can be undropped. |
| [SHOW TAGS](/sql-reference/sql/show-tags) | Lists the tag information. |
| [SHOW TASKS](/sql-reference/sql/show-tasks) | Lists the tasks for which you have access privileges. |
| [SHOW TELEMETRY EVENT DEFINITIONS](/sql-reference/sql/show-telemetry-event-definitions) | Lists the [event definitions](/developer-guide/native-apps/event-definition) for the specified app. |
| [SHOW TRANSACTIONS](/sql-reference/sql/show-transactions) | List all running transactions. |
| [SHOW TYPES](/sql-reference/sql/show-types) | Lists the [user-defined types](/sql-reference/data-types-user-defined) for which you have access privileges. |
| [SHOW USER FUNCTIONS](/sql-reference/sql/show-user-functions) | Lists all user-defined functions (UDFs) for which you have access privileges. |
| [SHOW USER KEY PAIRS](/sql-reference/sql/show-user-key-pairs) | Lists the named [key pairs](/user-guide/key-pair-auth) associated with a user. |
| [SHOW USER PROCEDURES](/sql-reference/sql/show-user-procedures) | Lists all user-defined procedures for which you have access privileges. |
| [SHOW USER PROGRAMMATIC ACCESS TOKENS](/sql-reference/sql/show-user-programmatic-access-tokens) | Lists the [programmatic access tokens](/user-guide/programmatic-access-tokens) associated with a user. |
| [SHOW USER WORKLOAD IDENTITY AUTHENTICATION METHODS](/sql-reference/sql/show-user-workload-identity-authentication-methods) | **Related Topics** |
| [SHOW USERS](/sql-reference/sql/show-users) | Lists all [users](/user-guide/admin-user-management) in the system. |
| [SHOW VARIABLES](/sql-reference/sql/show-variables) | Lists all [variables](/sql-reference/session-variables) defined in the current session. |
| [SHOW VERSIONS IN APPLICATION PACKAGE](/sql-reference/sql/show-versions) | Lists the versions defined in the specified application package. |
| [SHOW VERSIONS IN DATASET](/sql-reference/sql/show-versions-in-dataset) | Displays information about the datasets in your account at either the schema or database level. |
| [SHOW VERSIONS IN DBT PROJECT](/sql-reference/sql/show-versions-in-dbt-project) | Displays a list of all versions of a [dbt project object](/user-guide/data-engineering/dbt-projects-on-snowflake). |
| [SHOW VERSIONS IN LISTING](/sql-reference/sql/show-versions-in-listing) | Lists and provides details of all listing versions. |
| [SHOW VERSIONS IN MODEL](/sql-reference/sql/show-versions-in-model) | Lists the versions in a machine learning model. |
| [SHOW VERSIONS IN ORGANIZATION PROFILE](/sql-reference/sql/show-versions-in-organization-profile) | Lists the organization profile versions for which you have access privileges. |
| [SHOW VIEWS](/sql-reference/sql/show-views) | Lists the views, including secure views, for which you have access privileges. |
| [SHOW WAREHOUSES](/sql-reference/sql/show-warehouses) | Lists all the [virtual warehouses](/user-guide/warehouses-overview) in your account for which you have access privileges. |
| [SHOW WORKSPACES](/sql-reference/sql/show-workspaces) | Lists the [workspaces](/user-guide/ui-snowsight/workspaces) for which you have access privileges. |
| **T** |  |
| [TRUNCATE MATERIALIZED VIEW](/sql-reference/sql/truncate-materialized-view) | Removes all rows from a materialized view, but leaves the view intact (including all privileges and constraints on the materialized view). |
| [TRUNCATE TABLE](/sql-reference/sql/truncate-table) | Removes all rows from a table but leaves the table intact (including all privileges and constraints on the table). |
| **U** |  |
| [UNDROP <object>](/sql-reference/sql/undrop) | Restores the specified object to the system. |
| [UNDROP ACCOUNT](/sql-reference/sql/undrop-account) | Restores a [dropped account](/user-guide/organizations-manage-accounts-delete) that has not yet been permanently deleted (a dropped account that is within its grace period). |
| [UNDROP DATABASE](/sql-reference/sql/undrop-database) | Restores the most recent version of a dropped database. |
| [UNDROP DYNAMIC TABLE](/sql-reference/sql/undrop-dynamic-table) | Restores the most recent version of a dropped [dynamic table](/user-guide/dynamic-tables/overview). |
| [UNDROP EXTERNAL VOLUME](/sql-reference/sql/undrop-external-volume) | Restores the most recent version of a dropped [external volume](/user-guide/tables-iceberg#label-tables-iceberg-external-volume-def). |
| [UNDROP ICEBERG TABLE](/sql-reference/sql/undrop-iceberg-table) | Restores the most recent version of a dropped [Apache Iceberg™ table](/user-guide/tables-iceberg). |
| [UNDROP NOTEBOOK](/sql-reference/sql/undrop-notebook) | Restores the most recent version of a dropped notebook. |
| [UNDROP SCHEMA](/sql-reference/sql/undrop-schema) | Restore the most recent version of a dropped schema. |
| [UNDROP SNAPSHOT](/sql-reference/sql/undrop-snapshot) | Restores a previously removed [snapshot of a block storage volume](/developer-guide/snowpark-container-services/block-storage-volume). |
| [UNDROP STREAMLIT](/sql-reference/sql/undrop-streamlit) | Restores the most recent version of a dropped Streamlit object. |
| [UNDROP TABLE](/sql-reference/sql/undrop-table) | Restores the most recent version of a dropped table. |
| [UNDROP TAG](/sql-reference/sql/undrop-tag) | Restores the most recent version of a tag to the system. |
| [UNDROP TYPE](/sql-reference/sql/undrop-type) | Restores the most recent version of a [user-defined type](/sql-reference/data-types-user-defined). |
| [UNSET](/sql-reference/sql/unset) | Drops a [session variable](/sql-reference/session-variables). |
| [UPDATE](/sql-reference/sql/update) | Updates specified rows in the target table with new values. |
| [USE <object>](/sql-reference/sql/use) | Specifies the role, warehouse, database, or schema to use for the current session. |
| [USE DATABASE](/sql-reference/sql/use-database) | Specifies the active/current database for the session. |
| [USE ROLE](/sql-reference/sql/use-role) | Specifies the active/current primary role for the session. |
| [USE SCHEMA](/sql-reference/sql/use-schema) | Specifies the active/current schema for the session. |
| [USE SECONDARY ROLES](/sql-reference/sql/use-secondary-roles) | Specifies the active/current secondary roles for the session. |
| [USE WAREHOUSE](/sql-reference/sql/use-warehouse) | Specifies the active/current [virtual warehouse](/user-guide/warehouses-overview) for the session. |

Expand

Show lessSee more
