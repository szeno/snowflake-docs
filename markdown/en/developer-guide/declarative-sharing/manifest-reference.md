# Declarative Native App manifest reference

Feature — Generally Available

Support for Snowflake Declarative Native Apps is available to all accounts.

A manifest file is a text-based [YAML](https://yaml.org/spec/) file with the filename: `manifest.yml`. The manifest file is used to define a Declarative Native App and its associated data and logic. It also defines [app roles](/developer-guide/declarative-sharing/app-roles), which app owners can use to share a subset of the app’s data and features to teams in their organization by role.

Providers create a manifest file as part of a [package](/developer-guide/declarative-sharing/package). This topic describes the structure and fields of the manifest file.

For information about developing an application package, see [Application Packages in Declarative Sharing in the Native Application Framework](/developer-guide/declarative-sharing/package).

## Declarative Native App manifest

The general format of a Declarative Native App manifest is:

Copy code

```
manifest_version:    # required manifest version; added automatically by Snowflake - do not include
roles:               # optional app roles referenced by shared objects
shared_content:      # required shared data and logic (databases, schemas, and objects)
application_content: # optional app logic (for example, workspaces) shared by the app
```

## Manifest fields

Declarative Native App manifests include the following fields. Each section describes a field’s purpose, structure, and an example.

### `manifest_version` field

The `manifest_version` field (Integer, required) specifies the version number of the manifest file. This field is added automatically to the manifest file when you release a new version of an application package.

Don’t include this field when creating a manifest file to include in an application package. Editing this field manually is not supported.

For more information about versioning, see [Package Versions in Declarative Sharing in the Native Application Framework](/developer-guide/declarative-sharing/versioning).

### `roles` field

The `roles` field (list, optional) defines a list of [app roles](/developer-guide/declarative-sharing/app-roles). These roles let app owners provide access to shared objects in an app, such as schemas, tables, views, and workspaces, to their organization.

Each named role can optionally contain a `comment`, which appears as a description when the app owner lists the roles in the application.

These roles are referenced in the manifest by shared objects at the named `workspace`, `notebook`, `schema`, `table`, `view`, `semantic_view`, and `cortex_agent` level. For objects in `shared_content` (schemas, tables, views, semantic views, functions, procedures, and Cortex Agents), the roles you assign must be defined in the top-level `roles` list and must be a subset of the roles assigned to the parent schema (either directly on the schema or inherited from the database). For workspaces and notebooks in `application_content`, the roles must be defined in the top-level `roles` list but are not tied to a shared schema.

Note

- All content in the manifest is accessible to the app owner, the ACCOUNTADMIN, and to roles that are granted [IMPORTED PRIVILEGES](/developer-guide/declarative-sharing/consumer/install#label-dsna-share-access-to-all-data) to the app.
- The object name defined in this manifest file is used for the runtime object resolution. If the provider changes the object name without updating the manifest file with a new version, consumers will lose access to the object.

#### `roles` field example

Copy code

```
roles:
  - SALES
  - MARKETING

shared_content:
  databases:
    - SALES:
        schemas:
          - ORDERS:
              roles: [SALES, MARKETING]
              tables:
                - JANUARY_2025:      # App owners/assignees only
                - FEBRUARY_2025:
                    roles: [SALES]   # Accessible to SALES only
                - MARCH_2025:
                    roles: [MARKETING]  # Accessible to MARKETING only
    - CUSTOMER_INFO:
        schemas:
          - CUSTOMER_CONTACT:
              roles: [CUSTOMER_SUPPORT]
              views:
                - CUSTOMER_ADDRESS:
                    roles: [CUSTOMER_SUPPORT]  # Accessible to CUSTOMER_SUPPORT
                - CUSTOMER_DETAILS:
                    roles: []                  # App owners/assignees only

application_content:
  workspaces:
    - SALES_WORKSPACE:
        source: sales/
        roles: [SALES, MARKETING]
        comment: Sales and marketing workspace
```

For more information about roles, see [app roles](/developer-guide/declarative-sharing/app-roles).

### `shared_content` field

The `shared_content` field (list, required) defines a list of databases declaratively shared by the app. Each database includes a list of named `schemas`. Each schema can include a list of named entities grouped by type.

This field includes a single `databases` field and an optional `required_databases` field:

- `shared_content.databases` (list, required): A list of named database instances and the underlying objects to share.

#### `shared_content.databases.{named database}` field

Each named database supports the following name value pairs:

- `schemas` (list, required): A list of schemas within the database.

#### `shared_content.required_databases.{named database}` field

The `required_databases` field (list, optional) defines a list of databases that
are dependencies of the shared databases. These databases are referenced by
views in the shared databases, but are not shared directly. For more information
about managing cross-database dependencies, see [Dependency databases: Managing cross-database references](/developer-guide/declarative-sharing/dependency-databases).

When your application shares data from multiple databases, you must explicitly list all
additional databases that are referenced by objects in your shared content under
the `required_databases` field. This ensures that the application can be
deployed successfully in other regions where these databases may not exist by
default.

Including a database in the `required_databases` field is similar to
referencing a database using the REFERENCE\_USAGE privilege in traditional
Secure Data Sharing. For information about the REFERENCE\_USAGE privilege and how
dependent databases are shared in traditional data sharing, see
[Share data from multiple databases](/user-guide/data-sharing-multiple-db).

#### `schemas.{named schema}` field

Each named schema supports the following name value pairs:

- `tables` (list, [[OneOfRequired]](#citation-oneofrequired)): A list of named tables, which can include [dynamic tables](/user-guide/dynamic-tables/overview) and [Apache Iceberg tables](/user-guide/tables-iceberg).
- `views` (list, [[OneOfRequired]](#citation-oneofrequired)): A list of named views.
- `semantic_views` (list, [[OneOfRequired]](#citation-oneofrequired)): A list of named semantic views.
- `functions` (list, [[OneOfRequired]](#citation-oneofrequired)): A list of named user-defined functions (UDFs).
- `procedures` (list, [[OneOfRequired]](#citation-oneofrequired)): A list of named stored procedures.
- `cortex_agents` (list, [[OneOfRequired]](#citation-oneofrequired)): A list of named [Cortex Agents](/user-guide/snowflake-cortex/cortex-agents).
- `roles` (list, optional): A list of app roles that the objects in the schema can use, for example, `[SALES, MARKETING]`. When this field is empty (`[]`) or omitted, then only app owners and roles with [granted IMPORTED PRIVILEGES](/developer-guide/declarative-sharing/consumer/install#label-dsna-share-access-to-all-data) receive access. The included roles must be defined in the [top-level roles field](#label-dsna-manifest-roles-top).

[oneofrequired]
at least one of `tables`, `views`, `semantic_views`, `functions`, `procedures`, or `cortex_agents` is required.

Important

You must enforce schema separation between data objects (objects shared by reference: `tables`, `views`, and `semantic_views`) and logic objects (objects shared by copy: `functions`, `procedures`, and `cortex_agents`). You can’t mix data and logic objects in the same schema.

#### `tables.{named table}` field

Each named standard table, [dynamic table](/user-guide/dynamic-tables/overview), and [Apache Iceberg table](/user-guide/tables-iceberg) (list, required [[OneOfRequired]](#citation-oneofrequired) ) supports the following name value pair:

- `roles` (list, optional): A list of app roles that can access the table; for example, `[SALES]`. When this field is empty (`[]`) or omitted, then only app owners and roles with [granted IMPORTED PRIVILEGES](/developer-guide/declarative-sharing/consumer/install#label-dsna-share-access-to-all-data) receive access. The included roles must be defined in the [top-level roles field](#label-dsna-manifest-roles-top) and included in the [{named schema}.roles](#label-dsna-manifest-schemas) field.

Note

Shared [dynamic tables](/user-guide/dynamic-tables/overview) and [Apache Iceberg tables](/user-guide/tables-iceberg) replicated to remote regions are read-only and do not refresh automatically. Data freshness depends on the replication frequency from the source, and underlying source objects do not need to be replicated. For details, see [Replication considerations](/user-guide/account-replication-considerations).

Note

To allow consumers to create streams on this shared object (for change data capture or incremental loading), you must enable `CHANGE_TRACKING = TRUE` on the source table in your provider account using standard SQL commands (for example, `ALTER TABLE ... SET CHANGE_TRACKING = TRUE`). This setting can’t be changed by the consumer on the shared object; it must be set on the source.

#### `views.{named view}` field

Each named view (list, required [[OneOfRequired]](#citation-oneofrequired)) supports the following name value pair:

- `roles` (list, optional): A list of app roles that can access the view; for example, `[MARKETING]`. When this field is empty (`[]`) or omitted, then only app owners and roles with [granted IMPORTED PRIVILEGES](/developer-guide/declarative-sharing/consumer/install#label-dsna-share-access-to-all-data) receive access. The included roles must be defined in the [top-level roles field](#label-dsna-manifest-roles-top) and included in the [{named schema}.roles](#label-dsna-manifest-schemas) field.

Note

To allow consumers to create streams on this shared object (for change data capture or incremental loading), you must enable `CHANGE_TRACKING = TRUE` on the source table in your provider account using standard SQL commands (for example, `ALTER TABLE ... SET CHANGE_TRACKING = TRUE`). This setting can’t be changed by the consumer on the shared object; it must be set on the source.

#### `semantic_views.{named semantic view}` field

Each named semantic view (list, required [[OneOfRequired]](#citation-oneofrequired)) supports the following name value pair:

- `roles` (list, optional): A list of app roles that can access the semantic view; for example, `[SALES]`. Note that, when sharing a semantic view, its referenced tables or views must be shared as well. When this field is empty (`[]`) or omitted, then only app owners and roles with [granted IMPORTED PRIVILEGES](/developer-guide/declarative-sharing/consumer/install#label-dsna-share-access-to-all-data) receive access. The included roles must be defined in the [top-level roles field](#label-dsna-manifest-roles-top) and included in the [{named schema}.roles](#label-dsna-manifest-schemas) field.

#### `functions.{named function}` field

Each named function (list, required [[OneOfRequired]](#citation-oneofrequired)) supports the following name value pair:

- `roles` (list, optional): A list of app roles that can access the function; for example, `[ANALYST]`. When this field is empty (`[]`) or omitted, then only app owners and roles with [granted IMPORTED PRIVILEGES](/developer-guide/declarative-sharing/consumer/install#label-dsna-share-access-to-all-data) receive access. The included roles must be defined in the [top-level roles field](#label-dsna-manifest-roles-top) and included in the [{named schema}.roles](#label-dsna-manifest-schemas) field.

#### `procedures.{named procedure}` field

Each named stored procedure (list, required [[OneOfRequired]](#citation-oneofrequired)) supports the following name value pair:

- `roles` (list, optional): A list of app roles that can access the procedure; for example, `[ANALYST]`. When this field is empty (`[]`) or omitted, then only app owners and roles with [granted IMPORTED PRIVILEGES](/developer-guide/declarative-sharing/consumer/install#label-dsna-share-access-to-all-data) receive access. The included roles must be defined in the [top-level roles field](#label-dsna-manifest-roles-top) and included in the [{named schema}.roles](#label-dsna-manifest-schemas) field.

#### `cortex_agents.{named cortex agent}` field

Each named [Cortex Agent](/user-guide/snowflake-cortex/cortex-agents) (list, required [[OneOfRequired]](#citation-oneofrequired)) supports the following name value pair:

- `roles` (list, optional): A list of app roles that can access the Cortex Agent; for example, `[APP_USER]`. When this field is empty (`[]`) or omitted, then only app owners and roles with [granted IMPORTED PRIVILEGES](/developer-guide/declarative-sharing/consumer/install#label-dsna-share-access-to-all-data) receive access. The included roles must be defined in the [top-level roles field](#label-dsna-manifest-roles-top) and included in the [{named schema}.roles](#label-dsna-manifest-schemas) field.

#### `shared_content` field example

In this example, two databases are exposed: **SALES** and **CUSTOMER\_INFO**.
Within these databases the **ORDERS.[JANUARY\_2025|FEBRUARY\_2025]** tables are exposed
as well as the **CUSTOMER\_CONTACT.CUSTOMER\_ADDRESS** view.

Two required databases are also exposed: **SALES\_PROJECTIONS** and **CUSTOMER\_ANALYTICS**.
These databases can be referenced by views in the shared databases, but are not shared directly.

Copy code

```
roles:
  - SALES
  - MARKETING
  - CUSTOMER_SUPPORT

shared_content:
  required_databases:
    - SALES_PROJECTIONS
    - CUSTOMER_ANALYTICS

  databases:
    - SALES:
        schemas:
          - ORDERS:
              roles: [SALES, MARKETING]
              tables:
                - JANUARY_2025:      # App owners/assignees only
                - FEBRUARY_2025:
                    roles: [SALES]   # Accessible to SALES only
                - MARCH_2025:
                    roles: [MARKETING]  # Accessible to MARKETING only

    - CUSTOMER_INFO:
        schemas:
          - CUSTOMER_CONTACT:
              roles: [CUSTOMER_SUPPORT]
              views:
                - CUSTOMER_ADDRESS:
                    roles: [CUSTOMER_SUPPORT]  # Accessible to CUSTOMER_SUPPORT
                - CUSTOMER_DETAILS:
                    roles: []                  # App owners/assignees only
```

### `application_content` field

The `application_content` field (list, optional) defines bundled content declaratively shared by the app.

This field includes the following fields:

- `application_content.notebooks` (list, optional): A list of named [notebooks](/user-guide/ui-snowsight/notebooks). Deprecated. Share notebooks in a workspace instead.
- `application_content.workspaces` (list, optional): A list of named [workspaces](/developer-guide/declarative-sharing/workspaces).

#### `application_content.notebooks.{named notebook}` field

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

Each named notebook supports the following name value pairs:

- `main_file` (string, required) the path to the interactive Python notebook (.ipynb) file, relative to the root of the package version.
- `comment` (string, optional): A comment describing the notebook.
- `runtime_environment_version` (string, optional): Specifies a particular [runtime environment version](/user-guide/ui-snowsight/notebooks#label-notebook-runtime-descriptions)
  for the notebook execution context, if applicable within the platform.
- `roles` (list, optional): A list of app roles that can grant access to the notebook, for example, `[SALES, MARKETING]`. When this field is empty (`[]`) or omitted, then only app owners and roles with [granted IMPORTED PRIVILEGES](/developer-guide/declarative-sharing/consumer/install#label-dsna-share-access-to-all-data) receive access. The included roles must be defined in the [top-level roles field](#label-dsna-manifest-roles-top).

Note

The `main_file` path is always relative to the root of the package
version (the `snow://package/<DECL_SHARE_APP_PKG>/versions/<version>` prefix).
For example, if the full path to the notebook file is
`snow://package/<DECL_SHARE_APP_PKG>/versions/LIVE/NOTEBOOK.ipynb`,
then specify `main_file` as just `NOTEBOOK.ipynb`.

##### `application_content` field example

In this example, a single notebook, **SALESBOOK**, is defined using the
notebook file **NOTEBOOK1.ipynb** which uses the known runtime **stable**
and provides access to those granted either the **SALES** or **MARKETING** roles.

Copy code

```
roles:
  - SALES
  - MARKETING

application_content:
  notebooks:
    - SALESBOOK:
        roles: [SALES, MARKETING]
        main_file: NOTEBOOK1.ipynb
        comment: "Notebook1: Sales and marketing notebook"
        runtime_environment_version: stable
```

#### `application_content.workspaces.{named workspace}` field

Each named workspace shares a directory of files and folders with consumers as a read-only
[workspace](/user-guide/ui-snowsight/workspaces). Use a workspace to share
[Snowflake Notebooks in Workspaces](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-overview),
documentation, images, and sample data files together.

Each named workspace supports the following name value pairs:

- `source` (string, required): The path to the directory whose files make up the workspace,
  relative to the root of the package version. The path must not start with a slash (`/`), must end
  with a slash (`/`), and must point to a directory that contains at least one file.
- `comment` (string, optional): A comment describing the workspace.
- `roles` (list, optional): A list of app roles that can access the workspace, for example,
  `[SALES, MARKETING]`. When this field is empty (`[]`) or omitted, then only app owners and roles
  with [granted IMPORTED PRIVILEGES](/developer-guide/declarative-sharing/consumer/install#label-dsna-share-access-to-all-data) receive access. The
  included roles must be defined in the [top-level roles field](#label-dsna-manifest-roles-top).
  Unlike objects in `shared_content`, a workspace isn’t tied to a shared schema, so its roles don’t
  need to be a subset of a parent schema’s roles.

Note

You can’t include `.pdf` files in a workspace. The framework rejects them when you build, commit,
or release the application package, and again when a consumer installs the app.

For more information about sharing a workspace, see [Share a workspace in a Declarative Native App](/developer-guide/declarative-sharing/workspaces).

##### `application_content.workspaces` field example

In this example, a single workspace, **ANALYSIS\_WORKSPACE**, shares every file in the
*workspace\_content/* directory of the package version with the **ANALYST** role.

Copy code

```
roles:
  - ANALYST

application_content:
  workspaces:
    - ANALYSIS_WORKSPACE:
        source: workspace_content/
        roles: [ANALYST]
        comment: Notebooks and reference material for the shared population data
```

## Manifest file example

The following code block is an example of a Declarative Native App manifest file.

Note that data and code objects must be in different schemas.

Copy code

```
manifest_version: 2

roles:
  - VIEWER:
      comment: "Can view summary data and dashboards."
  - ANALYST:
      comment: "Can query detailed tables, views, and semantic views."
  - APP_USER:
      comment: "Can run in-app agents."

shared_content:
  required_databases:
    - REF_DATA_DB

  databases:
    - POPULATION_APP_DB:
        schemas:
          - DATA_SCHEMA:
              roles: [VIEWER, ANALYST, APP_USER]

              tables:
                - COUNTRY_POP_BY_YEAR:
                    roles: [ANALYST]
                - POPULATION_DYNAMIC_TABLE:
                    roles: [ANALYST]
                - MANAGED_POPULATION_ICEBERG_TABLE:
                    roles: [ANALYST]

              views:
                - COUNTRY_POP_BY_YEAR_2000:
                    roles: [VIEWER, ANALYST]

              semantic_views:
                - POPULATION_METRICS_SEMANTIC_VIEW:
                    roles: [ANALYST]

          - LOGIC_SCHEMA:
              roles: [ANALYST]

              functions:
                - POPULATION_ANALYSIS_FUNCTION(NUMBER):
                    roles: [ANALYST]

              procedures:
                - POPULATION_ANALYSIS_PROCEDURE():
                    roles: [ANALYST]

          - AGENT_SCHEMA:
              roles: [APP_USER]

              cortex_agents:
                - POPULATION_ASSISTANT_AGENT:
                    roles: [APP_USER]

application_content:
  workspaces:
    - INTRO_WORKSPACE:
        source: intro/
        roles: [VIEWER, ANALYST]
        comment: "Read-only overview of shared population data."

    - ANALYST_WORKSPACE:
        source: analysis/notebooks/
        roles: [ANALYST]
        comment: "Analysis notebooks for detailed population metrics."
```
