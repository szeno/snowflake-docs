# Jul 16, 2026: DCM Projects: New capabilities (*Preview*)

DCM Projects now supports the following capabilities in preview:

- **PLAN DELTA**: A faster variant of PLAN that only evaluates definitions that changed since the last deployment, and any downstream definitions that depend on them. Use it during active development for faster feedback on incremental changes, but always run a full PLAN to review all changes before deploying.
- **Python and Java functions and procedures**: DEFINE FUNCTION and DEFINE PROCEDURE now support Python and Java handlers, in addition to SQL.
- **ATTACH TAG**: Declaratively assign Snowflake object tags, including to table and view columns, to any DCM Projects-managed entity. DCM Projects reconciles the declared tag assignments on every deployment.
- **Inherited grants**: Use the `INHERITED` keyword in a GRANT statement to declaratively define a single grant on an account, database, or schema that automatically applies to every current and future object of a specified type within that container. This requires enabling a behavior-change parameter at the account level, independent of DCM Projects; see [Managing access with inherited grants](/user-guide/inherited-grants-intro) for details.
- **Container-level MANAGE GRANTS**: Delegate grant administration for a specific database or schema by granting `MANAGE GRANTS` on that container, without requiring account-level `SECURITYADMIN` privileges.
- **Target state for DEFINE ALERT**: Specify a target state of `STARTED` or `SUSPENDED` for an alert, the same way you already can for a task.
- **EXECUTE AS ROLE for ATTACH DATA METRIC FUNCTION**: Attach a data metric function to a table or column that isn’t defined within the DCM project, such as an upstream source table managed by another project, by specifying the role that the DMF runs with.
- **DEFINE NETWORK RULE**: Define network rules that control network traffic for network policies, external access integrations, and other network-aware objects.
- **DEFINE NETWORK POLICY**: Define network policies that restrict account, user, or integration access to specific IP addresses using network rules.
- **DEFINE MASKING POLICY**: Define masking policies to manage their lifecycle (CREATE, ALTER, DROP) as part of a DCM project. Attaching a masking policy to a table or view column isn’t yet supported.

For more information, see [Supported object types in DCM Projects](/user-guide/dcm-projects/dcm-projects-supported-entities) and [Deploy and manage DCM Projects](/user-guide/dcm-projects/dcm-projects-use).
