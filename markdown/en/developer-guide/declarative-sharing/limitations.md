# Declarative Sharing in Native Apps: Limitations

Feature — Generally Available

Support for Snowflake Declarative Native Apps is available to all accounts.

Declarative sharing is a feature in Snowflake Native Apps that allows providers to quickly define and share objects across multiple
databases using a simple YAML configuration file. While this feature significantly simplifies data sharing workflows, it has limitations
that providers should understand before implementation.

## Supported object types

Declarative sharing supports these object types:

- **Workspaces**
- **Notebooks** (deprecated)
- **Tables**, including:

  - Dynamic tables
  - Apache Iceberg tables
- **Views**, including:

  - Semantic views
- **Stored procedures**
- **User-defined functions (UDFs)**
- **Cortex Agents**
- **Streams**

All other object types are not supported for sharing in Declarative Sharing in Native Apps.

## Shared objects

Object limit
:   A maximum of 10,000 objects can be defined in the shared content section of
    the `manifest.yml` file. To raise this limit, contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Streams
:   The provider’s source object must have `CHANGE_TRACKING = TRUE` enabled.

## Workspace limitations

Notebook service scope
:   To run a notebook in a shared workspace, a consumer needs a
    [Snowflake-managed notebook service](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-compute-setup)
    in their own account. That service is scoped to a single application instance. It can’t be used by
    workspaces that aren’t bound to an app, or by workspaces in a different app instance.

PDF files
:   You can’t include `.pdf` files in a workspace. The framework rejects them when you build, commit,
    or release the application package, and again when a consumer installs the app.

Read-only for consumers
:   Consumers can’t edit, rename, or delete files in a shared workspace, and they can’t add files to
    it. They also can’t copy files out of a shared workspace into their own workspaces.

Source directory
:   The `source` path must be a directory that contains at least one file. It must end with a slash
    (`/`) and must not start with one. You can’t point a workspace at an individual file.

Network access
:   Notebooks in a shared workspace can’t access external endpoints or consumer data when running in
    consumer accounts. They run with
    [restricted caller’s rights](/developer-guide/restricted-callers-rights) and can only reach objects
    the app shares.

Re-sharing
:   Consumers can’t share a workspace from an app outside their organization, or share individual files
    in the workspace. Access follows the app roles assigned to the workspace.

## Notebook limitations

Deprecated

Sharing individual notebooks with `application_content.notebooks` shares
[Legacy Notebooks](/user-guide/ui-snowsight/notebooks), and is deprecated. Starting
August 18, 2026, you can’t create new application packages that share notebooks this way. Starting
November 2026, Legacy Notebooks can no longer be run or edited. For the full timeline, see
[Disable Legacy Notebook creations](/release-notes/bcr-bundles/un-bundled/bcr-disable-legacy-notebooks).

Share [Snowflake Notebooks in Workspaces](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-overview)
in a workspace instead. Consumers can run and interact with those notebooks the same way, and a
workspace can also share documentation, images, and sample data files. For more information, see
[Share a workspace in a Declarative Native App](/developer-guide/declarative-sharing/workspaces).

Read-only for consumers
:   Consumers can’t edit provider notebooks in place, nor can they clone them.

Network access
:   Notebooks can’t access external endpoints or consumer data when running in consumer accounts.

Specialized libraries
:   Geospatial and other third-party libraries aren’t guaranteed to work out-of-the-box in notebooks.

External dependencies
:   Declarative Sharing apps have limited support for external libraries (Snowflake Anaconda channel and Python files in code stage).

Non-interactive execution
:   Notebooks that are part of Native Apps cannot be executed non-interactively by
    worksheets or SQL commands.

## Security and access control

Role definition
:   All application roles referenced in the shared content must be predefined in the `roles` field in the manifest.

Object-level roles
:   Object roles must be subsets of their parent schema roles.

Missing role validation
:   Validating the manifest returns an error if roles referenced in the sharing configuration don’t exist.

Minimum privileges
:   The provider role committing the `shared_content.yaml` file must have at least the same privileges on shared objects as those being granted to consumers.

No REFERENCE\_USAGE required
:   Unlike traditional data sharing, providers don’t need to grant REFERENCE\_USAGE privileges to the application package.

## Migration and compatibility

Declarative Sharing migration
:   Migration support for switching from data shares to Declarative Sharing in the Native App framework is unavailable.

## Naming and configuration constraints

No wildcards
:   Object names must be explicitly specified; wildcard or regular expression matching is not supported.

Name collision prevention
:   No two shared objects can have the same DOMAIN and name.

Schema mapping
:   Schema mapping is not supported. Overlapping schema names from multiple databases are not allowed.

Schemas for data objects and logic objects
:   You must use separate schemas for data objects (shared by reference: tables and views) and logic objects (shared by copy: UDFs, stored procedures, Cortex Agents). For example, you can use a schema named `DATA_SCHEMA` for tables and views, and a schema named `LOGIC_SCHEMA` for UDFs.

## Monitoring

Auditability
:   Declarative Native Apps don’t provide monitoring resources (such as audit trails) to let the provider receive information from the consumer about how the shared data is being used. If a consumer has compliance or regulatory requirements that require auditing, the consumer must work with the provider to implement their own monitoring solutions.

## Cortex Agents

Execution environment
:   When creating a Cortex Agent for sharing that uses Cortex Analyst and semantic views, you must explicitly define the `execution_environment` with an empty string for the warehouse (`warehouse: ""`). You can’t omit this field, nor can you specify a specific warehouse name.

Tools
:   All tools must be in the same database as the Agent. While procedures and UDFs are shared by copy and may be in the same schema as the Agent, semantic views and Cortex Search-based tools must be in a different schema.
