# August 7, 2026: DCM Projects (*General availability*)

DCM Projects are now generally available and are no longer in [Preview](/release-notes/preview-features). DCM Projects enable a declarative approach to managing Snowflake objects as code. You define the desired target state of your databases, tables, tasks, and other Snowflake objects in definition files, and Snowflake determines and applies the necessary changes to reach that state.

DCM Projects support version-controlled, idempotent deployments across environments (such as development, staging, and production) using a plan-then-deploy workflow. Key capabilities include:

- **Declarative definitions**: Use DEFINE statements in SQL files to describe the desired state of your Snowflake objects. Snowflake determines the changes needed and applies them automatically.
- **Jinja templating**: Parameterize your definitions with variables, loops, conditions, and macros to reduce repetition and support multi-environment deployments.
- **Plan-then-deploy workflow**: Reliably preview planned changes before deploying them to catch unintended modifications.
- **Broad object support**: Manage a wide variety of Snowflake object types across infrastructure, data pipeline, and governance use cases.
- **Pipeline management**: Build, test, and deploy data pipelines using dynamic tables, tasks, and data quality expectations.

DCM Projects can be managed using Snowsight, Snowflake CLI, SQL, or Cortex Code CLI. Project definition files can be stored in a Snowflake Workspace, a remote Git repository, or a local directory.

The following related capabilities remain in [Preview](/release-notes/preview-features):

- TEST and PREVIEW commands
- GitHub Actions for DCM Projects
- `DEFINE PIPE`
- `DEFINE STREAM`
- `DEFINE MASKING POLICY`
- `DEFINE ROW ACCESS POLICY`
- `ATTACH TAG`
- Inherited grants and container-level `MANAGE GRANTS` in DCM Projects definitions

For more information, see [Snowflake DCM Projects](/user-guide/dcm-projects/dcm-projects-overview).
