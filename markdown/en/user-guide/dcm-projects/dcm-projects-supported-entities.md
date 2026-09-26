# Supported entities in DCM Projects

DCM Projects definition files support three types of statements:

- **[Objects](#label-dcm-projects-objects)** — `DEFINE` statements that create and manage Snowflake objects
- **[Grants](#label-dcm-projects-grants)** — `GRANT` statements that assign privileges and roles
- **[Attachments](#label-dcm-projects-attachments)** — `ATTACH` statements that associate objects with other objects

You can also reference additional files that your definitions need as [project assets](#label-dcm-project-assets) by specifying paths relative to the folder that contains `manifest.yml`.

Note

For objects, grants, and attachments in preview, the changeset format in `plan_results.json` and `deploy_results.json` can be subject to change.

**Objects:**

- [Alert](#label-dcm-projects-object-type-alert)
- [Code Bundle](#label-dcm-projects-object-type-code-bundle)
- [Database](#label-dcm-projects-object-type-database)
- [Dynamic table](#label-dcm-projects-object-type-dynamic-table)
- [File format](#label-dcm-projects-object-type-file-format)
- [Functions](#label-dcm-projects-object-type-function)
  - [Data metric functions](#label-dcm-projects-object-type-dmf-function)
- [Network rule](#label-dcm-projects-object-type-network-rule)
- [Pipe](#label-dcm-projects-object-type-pipe)
- [Policies](/user-guide/dcm-projects/dcm-projects-supported-entities#label-dcm-projects-object-type-policies)
  - [Authentication policy](/sql-reference/sql/create-authentication-policy)
  - [Masking policy](/sql-reference/sql/create-masking-policy)
  - [Network policy](/user-guide/network-policies)
  - [Row access policy](/user-guide/security-row-intro)
- [Procedures](#label-dcm-projects-object-type-procedure)
- [Roles](#label-dcm-projects-object-type-role)
  - [Database role](#label-dcm-projects-object-type-database-role)
- [Schema](#label-dcm-projects-object-type-schema)
- [Semantic view](#label-dcm-projects-object-type-semantic-view)
- [Sequence](#label-dcm-projects-object-type-sequence)
- [Share](#label-dcm-projects-object-type-share)
- [Stages](#label-dcm-projects-object-type-stage)
  - [External stage](#label-dcm-projects-object-type-external-stage)
  - [Internal stage](#label-dcm-projects-object-type-internal-stage)
- [Stream](#label-dcm-projects-object-type-stream)
- [Streamlit](#label-dcm-projects-object-type-streamlit)
- [Table](#label-dcm-projects-object-type-table)
- [Tag](#label-dcm-projects-object-type-tag)
- [Task](#label-dcm-projects-object-type-task)
- [View](#label-dcm-projects-object-type-view)
- [Warehouse](#label-dcm-projects-object-type-warehouse)

**Assets:**

- [Project assets](#label-dcm-project-assets)

**Grants:**

- [GRANT](#label-dcm-projects-object-type-grant)
- [OWNERSHIP grants](#label-dcm-projects-object-type-grant-ownership)
- [Inherited grants](#label-dcm-projects-inherited-grants)
- [Container-level MANAGE GRANTS](#label-dcm-projects-container-manage-grants)

**Attachments:**

- [ATTACH Data Metric Function](#label-dcm-projects-object-type-dmf)
- [ATTACH Tag](#label-dcm-projects-attach-tag)

## Objects

DCM Projects uses `DEFINE` statements to create and manage Snowflake objects. A `DEFINE` statement runs as a
[CREATE OR ALTER](/sql-reference/sql/create-or-alter) command for the corresponding object type, so all `CREATE OR ALTER` usage
notes and limitations for that object type apply, even where not called out again below. The following object types are
supported.

### Alert

DCM Projects supports defining alerts that run a SQL statement on a schedule and notify you when a condition is met. For more
information, see [Setting up alerts based on data in Snowflake](/user-guide/alerts).

Newly deployed alerts are suspended by default.

**Target state:**

You can specify a target state of `STARTED` or `SUSPENDED` for each alert in your definitions. Place the target state keyword
immediately before the `IF` keyword in the `DEFINE ALERT` statement. If you define an alert as `STARTED`, Snowflake resumes the
alert after deployment. This property is independent of other changes to the alert definition. If you define an alert as
`STARTED` and then suspend it outside of DCM Projects, the next deployment of that same definition starts the alert again.

Note

The target state is a DCM Projects-specific property. It won’t be visible in the DDL of the deployed alert.

Copy code

```
DEFINE ALERT MY_DB.MY_SCHEMA.ALRT_CHECK_ORDER_VOLUME
    WAREHOUSE = 'MY_WH'
    SCHEDULE = '60 MINUTE'
    STARTED
    IF (EXISTS (
      SELECT 1 FROM MY_DB.MY_SCHEMA.ORDERS WHERE ORDER_COUNT > 1000
    ))
    THEN
      CALL SYSTEM$SEND_EMAIL(
        'my_notification_integration', 'ops@example.com', 'High order volume', 'Order volume exceeded 1000 orders.'
      )
;
```

**Limitations:**

- `PLAN` only validates that the alert can be created successfully. It doesn’t check whether the alert will run
  successfully, as alert logic is compiled at runtime.

### Code Bundle

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

You can define [Code Bundles](/developer-guide/code-bundles/code-bundles) directly in DCM Projects. Code Bundles package and run
non-SQL jobs, such as Python, on Snowflake compute. DCM Projects manages the bundle lifecycle (`CREATE`, `ALTER`, and `DROP`) across
environments using Jinja templating.

Place the bundle source files inside the DCM project root folder but outside `sources/`. A bundle folder contains the
`code_bundle.yml` specification, the notebook that serves as the entry point, and any Python helper modules that the notebook
imports:

```
my_dcm_project/
├── manifest.yml
├── sources/
│   └── definitions/
│       └── jobs.sql              ← DEFINE CODE BUNDLE statement
└── code_bundles/
    └── my_job/                   ← path imported as the my_job asset
        ├── my_job.ipynb          ← entry point
        ├── helpers.py
        └── code_bundle.yml
```

Declare the source folder as a [project asset](#label-dcm-project-assets), then reference its asset name in the
`DEFINE CODE BUNDLE` statement:

Copy code

```
assets:
  my_job:
    path: 'code_bundles/my_job/**/*'
```

Copy code

```
DEFINE CODE BUNDLE DEMO{{env_suffix}}.JOBS.MY_JOB
  FROM 'asset://my_job'
  COMMENT = 'Python job managed by DCM';
```

The contents of the asset become the root of the bundle version, so `code_bundle.yml` and the entry point must be at the top of
the asset. Point the pattern at the bundle folder itself (`'code_bundles/my_job/**/*'`), not its parent
(`'code_bundles/**/*'`). DCM Projects doesn’t validate this layout. A bundle assembled with the wrong pattern deploys successfully but
fails when you execute it.

The entry point is specified when you execute the bundle, for example from a task:

Copy code

```
EXECUTE CODE BUNDLE DEMO{{env_suffix}}.JOBS.MY_JOB
  ENTRYPOINT = 'my_job.ipynb';
```

`PLAN` and `PLAN DELTA` detect changes to the `DEFINE CODE BUNDLE` statement and its referenced assets.

**Limitations:**

- A Code Bundle’s source must be a project asset. A relative path in the `FROM` clause fails at compile time.
- DCM Projects can’t adopt a Code Bundle that already exists outside the project because a bundle can be deployed only from the stage
  where it was created. Drop the existing bundle and let the project create it, or remove the `DEFINE` statement.
- A Code Bundle can’t be detached from the project that manages it. Drop the bundle, or remove its `DEFINE` statement and let
  the project drop it on the next deployment.
- Removing the `DEFINE CODE BUNDLE` statement drops the bundle and all its versions on the next deployment.
- A DCM project that manages a Code Bundle can’t be dropped or replaced. Run
  `EXECUTE DCM PROJECT <name> PURGE` to drop the managed objects, then drop the project.
- `PLAN` validates that the Code Bundle object can be created, but doesn’t check whether the bundled code runs successfully.

### Database

DCM Projects supports defining databases.

### Dynamic table

**Supported changes:**

Without a full refresh:

- Warehouse
- Target lag

With re-initialization or a full refresh:

- Refresh mode
- Any changes to the body, including:
  - Dropping columns
  - Adding columns at the end

**Immutable attributes:**

- `INITIALIZE`

**Limitations:**

- Adding comments to dynamic table columns isn’t supported.
- Reordering columns of existing dynamic tables is not supported.
- The `PREVIEW` command doesn’t support custom incremental dynamic tables.

### File format

DCM Projects supports defining file formats.

### Functions

DCM Projects supports defining functions in every handler language:

- SQL
- Java
- JavaScript
- Python
- Scala

**Limitations:**

- `PLAN` only validates that the function can be created or altered successfully. It doesn’t check whether it will run
  successfully, as function logic is compiled at runtime.
- For non-SQL handlers, `PLAN` treats a changed handler body as a full replace, the same way it
  handles SQL handlers. There’s no diff of the handler source code in the `PLAN` output.
- Inline handler bodies (`AS $$...$$`), staged imports (`IMPORTS`), and Artifactory references (`ARTIFACT_REPOSITORY`)
  are supported for Python and Java handlers.
- Staged files referenced in `IMPORTS` must be uploaded to that stage outside of DCM Projects. DCM Projects doesn’t support
  uploading files into user stages.

#### Data metric functions

DCM Projects supports defining user-defined data metric functions (UDMFs) using `DEFINE DATA METRIC FUNCTION`. For more information, see
[Use SQL to set up data metric functions](/user-guide/data-quality-working).

Copy code

```
DEFINE DATA METRIC FUNCTION DCM_DEMO.TESTS.INVENTORY_SPREAD(
  TABLE_NAME TABLE(
    COLUMN_VALUE number
  )
)
  RETURNS number
AS
$$
  SELECT
    MAX(COLUMN_VALUE) - MIN(COLUMN_VALUE)
  FROM
    TABLE_NAME
  WHERE
    COLUMN_VALUE IS NOT NULL
$$;
```

To attach a UDMF (or a system DMF) to a table, view, or dynamic table, see
[ATTACH Data Metric Function](#label-dcm-projects-object-type-dmf).

### Network rule

DCM Projects supports defining network rules, which control network traffic for network policies, external access integrations, and
other network-aware objects. For more information, see [Network rules](/user-guide/network-rules).

**Limitations:**

- The `TYPE` and `MODE` properties can’t be changed after creation. To change either property, remove the `DEFINE` statement,
  deploy, then redefine the network rule with the new value.
- Setting or unsetting a tag on a network rule isn’t supported.

### Pipe

DCM Projects supports defining Snowflake pipes. DCM Projects manages the pipe lifecycle (`CREATE`, `ALTER`, `DROP`) across environments using Jinja
templating. All pipe properties supported by [CREATE PIPE](/sql-reference/sql/create-pipe) are available in `DEFINE PIPE`.

**Limitations:**

- Only the pipe `COMMENT` can be changed after creation. The `COPY INTO` body and all other pipe properties are immutable.
- `AUTO_INGEST = TRUE` requires an S3/Azure/GCS event notification to be configured outside of DCM Projects. DCM Projects creates the pipe
  but doesn’t configure the cloud-side notification.

### Policies

DCM Projects supports defining the following types of policies:

- [Authentication policy](/sql-reference/sql/create-authentication-policy)
- [Masking policy](/sql-reference/sql/create-masking-policy) (Public Preview)
- [Network policy](/user-guide/network-policies)
- [Row access policy](/user-guide/security-row-intro) (Public Preview)

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

**Limitations:**

- `DEFINE MASKING POLICY` and `DEFINE ROW ACCESS POLICY` are still in Public Preview.
- **Masking policy:** Attaching a masking policy to a table or view column as part of a DCM project definition isn’t yet
  supported; see [Attachments](#label-dcm-projects-attachments).
- **Network policy:**
  - You can’t replace an existing network policy while it’s assigned to an account, security integration, or user. Unassign
    the policy before redeploying a replacement.
  - Assigning the policy to an account, user, or integration must be done outside of DCM Projects, using `ALTER ACCOUNT`,
    `ALTER USER`, or `ALTER SECURITY INTEGRATION`.
- **Row access policy:** Attaching a row access policy to a table or view as part of a DCM project definition isn’t yet
  supported; see
  [Attachments](#label-dcm-projects-attachments).

### Procedures

DCM Projects supports defining stored procedures in every handler language:

- SQL (Snowflake Scripting)
- Java
- JavaScript
- Python
- Scala

**Limitations:**

- `PLAN` only validates that the procedure can be created or altered successfully. It doesn’t check whether it will run
  successfully, as procedure logic is compiled at runtime.
- For non-SQL handlers, `PLAN` treats a changed handler body as a full replace, the same way it
  handles SQL handlers. There’s no diff of the handler source code in the `PLAN` output.
- Inline handler bodies (`AS $$...$$`) and staged imports (`IMPORTS`) are supported for Python and Java handlers.
- Staged files referenced in `IMPORTS` must be uploaded to that stage outside of DCM Projects. DCM Projects doesn’t support
  uploading files into user stages.

### Roles

DCM Projects supports defining roles and database roles.

**Unsupported types:**

- Application Role

#### Database role

Database roles are scoped to a specific database and can be granted to account roles or other database roles within the same database.

### Schema

DCM Projects supports defining schemas.

### Semantic view

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

DCM Projects supports defining [semantic views](/user-guide/views-semantic/overview). Every deployment of a definition change reconciles the full semantic view definition: tables, relationships, facts, dimensions, metrics, AI instructions, and verified queries.

Copy code

```
DEFINE SEMANTIC VIEW DEMO{{env_suffix}}.ANALYTICS.SALES_METRICS
  TABLES (
    orders AS DEMO{{env_suffix}}.SALES.ORDERS
      PRIMARY KEY (ORDER_ID),
    customers AS DEMO{{env_suffix}}.SALES.CUSTOMERS
      PRIMARY KEY (CUSTOMER_ID)
  )
  RELATIONSHIPS (
    orders_to_customers AS orders (CUSTOMER_ID) REFERENCES customers (CUSTOMER_ID)
  )
  DIMENSIONS (
    orders.ORDER_DATE AS orders.ORDER_DATE,
    customers.COUNTRY   AS customers.COUNTRY
  )
  METRICS (
    orders.TOTAL_REVENUE AS SUM(orders.AMOUNT),
    orders.ORDER_COUNT   AS COUNT(orders.ORDER_ID)
  )
  COMMENT = 'Sales metrics semantic view for Cortex Analyst';
```

**Limitations:**

- All defined constraints and relationships must be named.
- All [CREATE OR ALTER SEMANTIC VIEW usage notes](/sql-reference/sql/create-semantic-view#label-create-or-alter-semantic-view-usage-notes) apply, including that tags on the semantic view or its members can’t be added or changed through the statement. Any existing tags are preserved.

### Sequence

DCM Projects supports defining sequences that generate unique numbers across sessions and statements. For more information, see
[Using Sequences](/user-guide/querying-sequences).

### Share

DCM Projects supports defining shares, which let you manage the share object and all `GRANT` statements on it declaratively,
controlling which objects are exposed to the share. All share properties supported by
[CREATE SHARE](/sql-reference/sql/create-share) are available in `DEFINE SHARE`. For more information, see
[Create and configure shares](/user-guide/data-sharing-provider).

**Limitations:**

- Consumer account assignment (`ALTER SHARE ... ADD ACCOUNTS`) must be done outside of DCM Projects, after database usage is
  granted to the share. DCM Projects creates and manages the share object and its grants, but doesn’t configure which accounts
  can access the share.

### Stages

DCM Projects supports both [external](#label-dcm-projects-object-type-external-stage) and
[internal](#label-dcm-projects-object-type-internal-stage) stages.

**Supported changes:**

- Directory table
- Comment

**Immutable attributes:**

- Encryption type

#### External stage

An external stage references data files stored in a location outside of Snowflake, such as Amazon S3, Google Cloud Storage,
or Microsoft Azure.

Warning

Don’t include sensitive information, such as API keys or credentials, in external stage definitions. DCM Projects doesn’t
currently identify and obfuscate this data, so it would be stored in plain text in your rendered DCM project files and deployment
history.

#### Internal stage

An internal stage stores data files within Snowflake.

### Stream

DCM Projects supports defining streams. All stream variants supported by
[CREATE OR ALTER STREAM](/sql-reference/sql/create-stream#create-or-alter-stream) are available in `DEFINE STREAM`,
including streams on tables, views, directory tables, and external tables.

**Limitations:**

- Streams are immutable after creation. Only the `COMMENT` can be changed. To change any other property (such as the
  source object or `APPEND_ONLY`), you must drop and recreate the stream.

### Streamlit

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

You can define one or more Streamlit apps, their infrastructure, underlying tables, and access control together in a single
DCM project folder, then deploy everything to any environment with one command.

This approach is especially useful for dashboard and data app deployments that depend on objects such as tables, views, and
dynamic tables that are also managed by DCM Projects. You can version and promote the data pipeline and the app that consumes it
together across environments.

In Public Preview, `DEFINE STREAMLIT` supports only assets referenced by an `asset://` URI in the `FROM` clause.

[![](/static/images/dcm-projects/streamlit-in-dcm-project.png)](/static/images/dcm-projects/streamlit-in-dcm-project.png)

#### Create a DCM project for Streamlit

An existing Streamlit app folder can include:

- `streamlit_app.py` or another entrypoint file
- `environment.yml` for warehouse runtime, or `requirements.txt` or `pyproject.toml` for container runtime
- Supporting Python modules, pages, or asset files

Place the app inside the DCM project root folder but outside `sources/`. Organize it in any sibling folder structure you
choose, for example, `streamlit/my_dashboard/`.

Copy code

```
my_dcm_project/
├── manifest.yml
├── sources/
│   └── definitions/
│       ├── pipeline.sql
│       ├── access.sql
│       └── dashboard.sql         ← DEFINE STREAMLIT statement
└── streamlit/
    └── my_dashboard/             ← path imported as the my_dashboard asset
        ├── streamlit_app.py
        ├── page_2.py
        ├── pyproject.toml
        └── snowflake.yml
```

Add the `DEFINE STREAMLIT` statement to your DCM Projects definitions with:

- The fully qualified name for the Streamlit object
- The `asset://` URI for the Streamlit asset
- The entrypoint filename (`MAIN_FILE`)
- The warehouse to use for query execution (`QUERY_WAREHOUSE`)
- The compute pool and runtime (`COMPUTE_POOL`, `RUNTIME_NAME`) for container-runtime apps
- An optional display title (`TITLE`)
- Any external access integrations (`EXTERNAL_ACCESS_INTEGRATIONS`) and stage imports (`IMPORTS`) that the app requires

Copy code

```
DEFINE STREAMLIT DEMO{{env_suffix}}.SERVE.MY_DASHBOARD
    FROM 'asset://my_dashboard/'
    MAIN_FILE = 'streamlit_app.py'
    QUERY_WAREHOUSE = DEMO_WH{{env_suffix}}
    COMPUTE_POOL = SYSTEM_COMPUTE_POOL_CPU
    RUNTIME_NAME = 'SYSTEM$ST_CONTAINER_RUNTIME_PY3_11'
    TITLE = 'My Dashboard'
    EXTERNAL_ACCESS_INTEGRATIONS = ()
    IMPORTS = ()
;
```

#### Import a Streamlit app as an asset

Import the Streamlit app as an asset and reference it with an `asset://` URI in the `FROM` clause. Asset files must be inside
the DCM project root folder but outside the `sources/` folder.

In `manifest.yml`, define the Streamlit folder as an asset in a top-level `assets` section. For each asset, use `path` to
specify one path or `paths` to specify a list of paths. Each asset path must be a valid glob expression or file path and must
be enclosed in single quotation marks. A directory path by itself isn’t supported. To include the contents of a directory,
append a glob pattern such as `/**/*`. Glob expressions support only `*` and `**`:

Copy code

```
targets:
  # ...

assets:
  my_dashboard:
    path: 'streamlit/my_dashboard/**/*'

  my_next_streamlit:
    paths:
      - 'streamlit_2/**/*'
      - 'streamlit/shared/library.py'

templating:
  # ...
```

If you have a pre-existing Streamlit project, you don’t need to move its files. Use the existing Streamlit project folder as
the DCM project root, and add `manifest.yml` and the `sources/` folder to that root. Then import the existing project files
with `**/*`. DCM Projects automatically excludes DCM Projects-owned files and folders from the match:

Copy code

```
assets:
  my_dashboard:
    path: '**/*'
```

Reference the asset in the `FROM` clause by using the `asset://<asset_name>/` URI. The URI references the user-defined asset
name under `assets`, not the original path or directory name:

Copy code

```
DEFINE STREAMLIT DEMO{{env_suffix}}.SERVE.MY_DASHBOARD
    FROM 'asset://my_dashboard/'
    MAIN_FILE = 'streamlit_app.py'
    QUERY_WAREHOUSE = DEMO_WH{{env_suffix}}
;
```

When DCM Projects renders the project, the imported asset files appear with the rendered definitions under
`out/rendered/assets/`. DCM Projects also includes them in the deployment artifacts.

#### Plan and deploy a DCM project with a Streamlit app

Run your regular DCM Projects `PLAN` and `DEPLOY` commands. If the `DEFINE STREAMLIT` statement, the referenced asset, or any of its
source paths or files have changed since the last successful deployment, `PLAN` and `PLAN DELTA` show the Streamlit object as
part of the changeset. `DEPLOY` replaces any modified files and creates a new version.

`PLAN` only validates that the Streamlit object can be created. It doesn’t test whether the app itself runs successfully
when started.

After the first successful deployment, the Streamlit app is immediately live. DCM Projects automatically initializes the live
version after creating the Streamlit object, so you don’t need to run `ALTER STREAMLIT` manually.

Removing the `DEFINE STREAMLIT` statement drops the Streamlit object on the next deployment.

**Limitations:**

- DCM Projects Jinja templating variables aren’t passed through to Streamlit Python files. You can use Jinja in the
  `DEFINE STREAMLIT` statement itself, for example, to set the warehouse or compute pool name, but not inside your app code.
  - To reference environment-specific objects from inside your Streamlit app at runtime, query the active context using
    `CURRENT_DATABASE()`, `CURRENT_SCHEMA()`, or similar functions to infer the environment.
- Asset paths must resolve within the DCM project. Assets can’t include files in the `sources/` folder, and you can’t
  specify a path to another repository or folder outside of the DCM project.

### Table

To define a table column with a default value and comment, specify the column name and data type, followed by the `DEFAULT` and `COMMENT`
clauses:

Copy code

```
DEFINE TABLE MY_DB.MY_SCHEMA.ORDERS (
  ORDER_ID NUMBER DEFAULT 0 COMMENT 'Unique order identifier',
  ORDER_STATUS VARCHAR DEFAULT 'PENDING' COMMENT 'Current order status'
);
```

**Limitations:**

- Reordering columns
- Changing column types to incompatible types
- Adding search optimization to a table or columns isn’t yet supported. Add it manually outside of DCM Projects using
  `ALTER TABLE ... ADD SEARCH OPTIMIZATION`.
- Adding tags and policies to a table or columns
- Virtual columns (`AS ( <expr> )` column definitions) aren’t yet supported on `DEFINE TABLE`.

### Tag

DCM Projects supports defining tags. For more information, see [Introduction to object tagging](/user-guide/object-tagging/introduction).

**Unsupported attributes:**

- Propagate

**Limitations:**

- All [CREATE OR ALTER TAG limitations](/sql-reference/sql/create-tag#create-or-alter-tag-usage-notes)
  apply to `DEFINE TAG`. They don’t apply to `ATTACH TAG`.

### Task

When definition changes are deployed for a task that is already started, Snowflake automatically suspends that task (or its root task)
temporarily, applies the change, and then resumes it again.

Newly deployed tasks are suspended by default.

**Target state:**

You can specify a target state of `STARTED` or `SUSPENDED` for each task in your definitions. Place the target state keyword
immediately before the `AS` keyword in the `DEFINE TASK` statement. If you define a task as `STARTED`, Snowflake resumes the task
after deployment. This property is independent of other changes to the task definition. If you define a task as `STARTED` and then
suspend it outside of DCM Projects, the next deployment of that same definition starts the task again.

DCM Projects handles the dependency resolution between root-task and child-task states.

Note

The target state is a DCM Projects-specific property. It won’t be visible in the DDL of the deployed task.

Copy code

```
DEFINE TASK MY_DB.MY_SCHEMA.TSK_INGEST_DAILY_ORDERS
    WAREHOUSE = 'MY_WH'
    SCHEDULE = 'USING CRON 0 5 * * * UTC'
    STARTED
AS
   SELECT 1
;
```

**Limitations:**

- All tasks in a task graph must be defined within the same DCM project, then same schema and owned by the same role.
- After you configure the [executor role and role hierarchy](#label-dcm-projects-restricted-execution), transferring ownership of a task
  graph requires multiple deployments:
  1. Define and deploy the tasks to create the task graph.
  2. Add a `GRANT OWNERSHIP` statement for every task in the graph, and deploy again to transfer ownership to the lower-level role. Ownership
     transfer removes predecessor relationships and detaches child tasks from the graph.
  3. Deploy again to restore the predecessor relationships and target states from the task definitions.
- `PLAN` only validates that the task can be created successfully. It doesn’t check whether the task will run successfully, as task
  logic is compiled at runtime.

### View

Note

To add comments to view columns, list every output column in parentheses immediately after the view name. Add `COMMENT '<comment>'` after
each column name that needs a comment. Don’t specify data types in the column list.

Copy code

```
DEFINE VIEW MY_DB.MY_SCHEMA.MY_VIEW (
  ORDER_ID COMMENT 'Unique order identifier',
  ORDER_TOTAL COMMENT 'Total order amount'
)
AS
  SELECT ORDER_ID, ORDER_TOTAL
  FROM MY_DB.MY_SCHEMA.ORDERS;
```

**Limitations:**

- Reordering columns

### Warehouse

**Immutable attributes:**

- INITIALLY\_SUSPENDED

## Project assets

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

To create or update Streamlit apps (`DEFINE STREAMLIT`) and Code Bundles (`DEFINE CODE BUNDLE`) with DCM Projects, declare their
source files as named entries in the manifest’s `assets` section. Assets let you place `manifest.yml` alongside existing code
folders and use those files in DCM Projects without moving them into `sources/`.

Each entry under the top-level `assets` section has a name and either `path` for one glob pattern or `paths` for multiple
patterns. Paths are relative to the folder that contains `manifest.yml`. For example:

```
my_dcm_project/
├── manifest.yml
├── sources/
│   └── definitions/
│       └── objects.sql
├── streamlit/
│   └── my_dashboard/
│       └── streamlit_app.py
├── code_bundles/
│   └── my_job/
│       ├── code_bundle.yml
│       └── my_job.ipynb
└── shared/
    └── helpers.py
```

Copy code

```
assets:
  my_dashboard:
    path: 'streamlit/my_dashboard/**/*'

  my_job:
    paths:
      - 'code_bundles/my_job/**/*'
      - 'shared/helpers.py'
```

Reference an entry’s name in the object’s `FROM` clause, for example, `FROM 'asset://my_dashboard'`. `DEFINE STREAMLIT` and
`DEFINE CODE BUNDLE` can’t reference the original source folder or file path directly in `FROM`. Asset names are case-sensitive
and must match `^[a-zA-Z_][a-zA-Z0-9_]*$`.

**Path constraints:**

- Paths must be relative to the folder that contains `manifest.yml` and must stay within the DCM project.
- A directory path by itself isn’t supported. Append a glob pattern, such as `/**/*`, to include the directory’s contents.
- `*` matches within one path component. `**` matches across directories. A path can also name one file.
- `?` and brace expansion aren’t supported. Brackets are literal characters. `**` must be a whole path component followed by
  another component.
- Paths can’t contain Jinja expressions. Enclose paths in single quotation marks in YAML.
- A pattern that matches no files causes the run to fail.

When you run `PLAN` or `DEPLOY` through Snowflake CLI, the CLI uploads the files that match the manifest paths. DCM Projects stores imported
files under `assets/<asset_name>/` in the deployment history artifacts. The literal directory prefix before the first wildcard
is removed:

| Pattern | Matched file | Materialized as |
| --- | --- | --- |
| `'app/**/*'` | `app/lib/util.py` | `assets/<name>/lib/util.py` |
| `'**/*'` | `app/lib/util.py` | `assets/<name>/app/lib/util.py` |
| `'app/static/**/*'` | `app/static/style.css` | `assets/<name>/style.css` |
| `'app/main.py'` | `app/main.py` | `assets/<name>/main.py` |

Expand

Show lessSee more

Entrypoints such as `MAIN_FILE` and `ENTRYPOINT` are relative to the imported root. Two files that resolve to the same
destination in one named asset cause an error. Different named assets can import the same source file.

Adding `--save-output` to `snow dcm plan` creates a local `out/` folder that contains rendered definitions under
`out/rendered/`, including imported files under `out/rendered/assets/`.

**Excluded files:**

- `sources/` is reserved for DCM Projects definitions, macros, and tests. Imported code files must be outside it. `manifest.yml` and
  `out/` are also excluded, even when explicitly named in a path.
- The CLI silently excludes dotfiles and dot-directories, including explicitly named files such as `.env`.
- Symlinks within the project are followed. Symlinks that point outside it are skipped.

**Limits:**

| Limit | Value |
| --- | --- |
| Size of a single asset file | 50 MB |
| Number of files per run | 5,000 |
| Total size of all assets | 512 MB |
| Length of an asset path | 1,024 |
| Length of an asset name | 255 |

Expand

Show lessSee more

## Grants

DCM Projects uses `GRANT` statements to assign privileges and roles within a project.

### GRANT

Just like each object can be defined only once in DCM Projects, each privilege-grantee relationship can only be defined once across all DCM Projects.

DCM Projects is only aware of grants that were defined and deployed through DCM Projects. Any grants that were added outside of DCM Projects coexist,
and DCM Projects doesn’t remove them.

Support for a `GRANT` statement that references a user or integration doesn’t mean that DCM Projects can define or manage the lifecycle of that
user or integration. Object-definition support and grant-target support are separate.

`GRANT ON ALL` and `GRANT ON FUTURE` aren’t recommended in DCM Projects. Use [inherited grants](#label-dcm-projects-inherited-grants)
instead, which apply to all current and future objects of a type within a container and offer better performance for DCM Projects executions.

Note

Support for `GRANT ON ALL` and `GRANT ON FUTURE` in DCM Projects will be deprecated in a future behavior change release in favor of inherited grants.

**Unsupported `GRANT` types:**

- CALLER grants

### OWNERSHIP grants

The DCM project owner role automatically has `OWNERSHIP` on all roles it creates inside the project. However, if one of those roles is
then granted `OWNERSHIP` of other deployed objects, the project owner role no longer has direct `OWNERSHIP` of those objects. To avoid
being locked out on future deployments, explicitly grant the role to the project owner role in the same definition files:

Copy code

```
DEFINE ROLE DATA_OWNER_ROLE;
GRANT OWNERSHIP ON TABLE MY_DB.MY_SCHEMA.MY_TABLE TO ROLE DATA_OWNER_ROLE;

-- Required: adds DATA_OWNER_ROLE to the project owner's role hierarchy so the
-- project owner inherits OWNERSHIP of MY_TABLE and can continue to manage it.
GRANT ROLE DATA_OWNER_ROLE TO ROLE DCM_PROJECT_OWNER_ROLE;
```

When removing a `GRANT OWNERSHIP` statement that was previously deployed, DCM Projects attempts to grant
ownership back to the DCM project owner, using the object’s current owner role to perform the transfer.
If the project owner role doesn’t hold the object’s current owner role, you must transfer ownership back manually outside of DCM Projects.

**Limitations:**

- The `COPY CURRENT GRANTS` and `REVOKE CURRENT GRANTS` clauses aren’t available in DCM Projects. Define all other privilege grants on the
  target object within the same DCM project as the `OWNERSHIP` grant. If the object has pre-existing grants, `PLAN` or `DEPLOY` of the
  `GRANT OWNERSHIP` statement fails.

  To work around this, do one of the following:

  - Define all desired grants on the target object in the DCM project, including any pre-existing grants.
  - Revoke the pre-existing grants manually outside of DCM Projects.

### Run procedures and tasks with restricted privileges

You can use a dedicated executor role when a DCM project deploys and manages a procedure or task, but the object should run with restricted
privileges. This pattern applies to owner’s rights procedures and tasks, which run with the privileges of their owner role.

In the same DCM project:

1. Define the procedure or task.
2. Define a dedicated executor role, such as `pipeline_runner`, or reference an existing role.
3. Grant the privileges required to run the procedure or task to the executor role.
4. Grant the executor role to the DCM project owner role. This role hierarchy prevents the project owner from losing the ability to manage
   the object after ownership is transferred.
5. Grant `OWNERSHIP` on the procedure or task to the executor role.

Keep the ownership transfer and the other privilege grants on the target object in the same DCM project. For more information, see
[OWNERSHIP grants](#label-dcm-projects-object-type-grant-ownership).

### Inherited grants

DCM Projects supports [inherited grants](/user-guide/inherited-grants-intro), which let you declaratively define a single grant on a
container (`ACCOUNT`, `DATABASE`, or `SCHEMA`) that automatically applies to every current and future object of a specified type
within that container.

**Prerequisites:**

Until the behavior change is fully rolled out, inherited grants still require a separate account-level opt-in that’s independent of DCM Projects. Before you can include them in your DCM Projects
definitions, review [inherited grants](/user-guide/inherited-grants-intro) and run:

Copy code

```
ALTER ACCOUNT SET FEATURE_RBAC_INHERITED_GRANTS = 'ENABLED';
```

The role that creates an inherited grant must have `MANAGE GRANTS` on the selected container or on a higher container. `OWNERSHIP` of the
container alone isn’t sufficient.

**Syntax:**

Use the `INHERITED` keyword in a standard `GRANT` statement inside your DCM Projects definitions:

Copy code

```
-- Grant SELECT on all current and future tables in a schema
GRANT INHERITED SELECT ON ALL TABLES
  IN SCHEMA MY_DB.MY_SCHEMA
  TO ROLE ANALYST_ROLE;

-- Grant SELECT on all current and future tables in a database
GRANT INHERITED SELECT ON ALL TABLES
  IN DATABASE MY_DB
  TO ROLE REPORTING_ROLE;
```

DCM Projects manages the lifecycle of these grants across deployments. Removing an inherited grant statement from your definitions
revokes the grant on the next deployment.

**Limitations:**

- All [inherited grant limitations](/user-guide/inherited-grants-intro#label-inherited-grants-intro-limitations) apply, including
  unsupported privilege types (for example, `OWNERSHIP`) and unsupported object types (for example, `SHARE`, `APPLICATION`,
  `INTEGRATION`).
- Inherited grants can’t be combined with `WITH GRANT OPTION`, `CASCADE`, or `RESTRICT`.
- Granting inherited privileges on imported (shared) databases or on objects owned by foreign accounts isn’t supported.
- Inherited grants on `APPLICATION` and `APPLICATION PACKAGE` objects aren’t supported.

### Container-level MANAGE GRANTS

In conjunction with inherited grants, DCM Projects also supports
[container-level `MANAGE GRANTS`](/user-guide/container-manage-grants-intro), which lets you delegate grant administration for a
specific database or schema. A role granted `MANAGE GRANTS` on a container can manage supported grants on objects inside that container
without needing account-level `SECURITYADMIN` privileges. It can’t transfer object ownership.

**Prerequisites:**

Until the behavior change is fully rolled out, container-level `MANAGE GRANTS` requires the same account-level opt-in as inherited grants. Before you can include it in your
DCM Projects definitions, run:

Copy code

```
ALTER ACCOUNT SET FEATURE_RBAC_INHERITED_GRANTS = 'ENABLED';
```

**Syntax:**

Copy code

```
-- Delegate grant administration for a schema
GRANT MANAGE GRANTS ON SCHEMA MY_DB.MY_SCHEMA
  TO ROLE ANALYTICS_ADMIN;

-- Delegate grant administration for a database
GRANT MANAGE GRANTS ON DATABASE MY_DB
  TO ROLE PROD_ACCESS_ADMIN;
```

DCM Projects manages the lifecycle of these grants across deployments. Removing a `MANAGE GRANTS` statement from your definitions
revokes the privilege on the next deployment.

**Limitations:**

- Container ownership alone doesn’t imply `MANAGE GRANTS`. The deploying role must explicitly grant this privilege to the target
  role.
- A role with container-level `MANAGE GRANTS` can’t transfer object ownership. Account-level `MANAGE GRANTS` (held by
  `SECURITYADMIN`) is still required for ownership transfers.
- `WITH GRANT OPTION` isn’t yet supported for container-level `MANAGE GRANTS` in DCM Projects definitions.
- Cascading a revocation of `MANAGE GRANTS` removes only dependent `MANAGE GRANTS` grants, not the other grants those roles
  created inside the container.

## Attachments

DCM Projects uses `ATTACH` statements to associate objects — such as data quality functions, policies, and tags — with other Snowflake objects.

**Limitations:**

- Attaching masking policies (to table or view columns) or row access policies (to tables or views) isn’t yet
  supported. You can attach either policy type manually outside of DCM Projects. DCM Projects definitions for table objects
  ignore any attached masking or row access policies and don’t revoke them on redeploy, even when the definitions
  don’t contain the policies.

### ATTACH Data Metric Function

Data metric functions (DMFs) let you define data quality expectations and attach those expectations to tables. You can select from existing
system DMFs or write your own [user-defined data metric functions (UDMFs)](#label-dcm-projects-object-type-dmf-function). You can then attach
them to tables, views, and dynamic tables with a many-to-many relationship. For more information, see [Use SQL to set up data metric functions](/user-guide/data-quality-working).

To attach data metric functions, you first need to add a `DATA_METRIC_SCHEDULE` to each table, dynamic table, or view definition. For
example: `DATA_METRIC_SCHEDULE = TRIGGER_ON_CHANGES`. The `TRIGGER_ON_CHANGES` schedule isn’t available for views.

The user-defined names of expectations must be unique per project and attachment.

Defining expectations is optional, but recommended, when attaching DMFs to table columns.
Attached DMFs without set expectations aren’t considered when running `EXECUTE DCM PROJECT <my_project> TEST ALL`.

**Supported changes:**

- Attaching system DMFs and UDMFs to tables, views, or dynamic tables inside and outside a DCM project
- Defining data expectations for table columns
- Specifying `EXECUTE AS ROLE` to run the DMF with a role other than the deploying role

**Examples:**

An example of attaching a system DMF with an expectation:

Copy code

```
ATTACH DATA METRIC FUNCTION SNOWFLAKE.CORE.MIN
  TO TABLE DCM_PROJECT_{{db}}.RAW.INVENTORY
  ON (IN_STOCK)
  EXPECTATION MIN_10_ITEMS_INVENTORY (value > 10);
```

An example of attaching a UDMF with an expectation:

Copy code

```
ATTACH DATA METRIC FUNCTION DCM_DEMO.TESTS.INVENTORY_SPREAD
  TO TABLE DCM_PROJECT_{{db}}.RAW.INVENTORY
  ON (IN_STOCK)
  EXPECTATION EVEN_ITEM_INVENTORY (VALUE < 50);
```

An example of attaching a UDMF to a table that isn’t defined within the DCM project, using `EXECUTE AS ROLE` so the DMF runs
with a role that has the required privileges on the target table:

Copy code

```
ATTACH DATA METRIC FUNCTION DCM_DEMO_3.S1.F1
  TO TABLE DCM_DEMO_3.S1.T1
  ON (A)
  EXECUTE AS ROLE INGEST_ADMIN;
```

Use `EXECUTE AS ROLE <role_name>` to attach a DMF to a table or column that another DCM project or a process outside DCM Projects
manages, such as a data quality expectation on an upstream source table that you don’t own. The deploying role only needs USAGE
on the DMF; the DMF itself runs with the specified role, which must have the required privilege on the target table. For more
information about this property, see [Required privilege on the table or view](/user-guide/data-quality-access-control#label-data-quality-access-control-object-privilege).

**Limitations:**

- Schema-level DMF attachments aren’t supported in DCM Projects.
- You can’t change the role specified by `EXECUTE AS ROLE` for an existing attachment by modifying just that property. To change
  the role, remove the `ATTACH` statement, deploy, then redefine it with the new `EXECUTE AS ROLE` value.

To see all available system DMFs, query `SHOW DATA METRIC FUNCTIONS IN DATABASE SNOWFLAKE`.

### ATTACH Tag

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Use `ATTACH TAG` to declaratively assign Snowflake object tags to the supported target types listed in this section. DCM Projects reconciles the
declared tag assignments on every deployment, replacing manual `ALTER <object> SET TAG` calls.

The tag and the target object don’t need to be defined in the same DCM project. You can reference tags and objects
anywhere in the account, as long as the deploying role has the required privileges.

**Syntax:**

You can group tag-to-target associations in different ways within a single statement. The following examples show
the supported patterns.

Single tag, single target:

Copy code

```
ATTACH TAG <tag_fqn> = '<value>'
  TO <object_keyword> <object_fqn> [ COLUMN <column_name> ];
```

Copy code

```
-- Attach a tag to a table
ATTACH TAG MY_DB.GOV.SENSITIVITY = 'PII'
  TO TABLE MY_DB.SALES.CUSTOMERS;

-- Attach a tag to a column of a table
ATTACH TAG MY_DB.GOV.SENSITIVITY = 'PII'
  TO TABLE MY_DB.SALES.CUSTOMERS COLUMN EMAIL;

-- Attach a tag to a column of a view
ATTACH TAG MY_DB.GOV.SENSITIVITY = 'PII'
  TO VIEW MY_DB.SALES.ACTIVE_CUSTOMERS COLUMN EMAIL;

-- Attach a tag to a schema
ATTACH TAG MY_DB.GOV.DATA_DOMAIN = 'marketing'
  TO SCHEMA MY_DB.MARKETING;
```

Multiple tags and multiple targets (N×M): a single `ATTACH TAG` statement can list multiple tag assignments and
multiple targets. DCM Projects expands them as a Cartesian product: every listed tag is attached to every listed target.
You can mix object-level and column-level targets in the same statement.

Copy code

```
ATTACH TAG MY_DB.GOV.TAG_PII = 'true',
           MY_DB.GOV.TAG_SENSITIVITY = 'high'
  TO TABLE MY_DB.SALES.CUSTOMERS COLUMN EMAIL,
     TABLE MY_DB.SALES.ORDERS,
     VIEW  MY_DB.SALES.ACTIVE_ACCOUNTS;
```

This single statement creates six tag-target pairs: both tags are attached to each of the three targets.

**Supported objects:**

| Object keyword | Column target supported |
| --- | --- |
| `DATABASE <db>` | No |
| `SCHEMA <db>.<schema>` | No |
| `TABLE <db>.<schema>.<name>` | Yes |
| `VIEW <db>.<schema>.<name>` | Yes |
| `DYNAMIC TABLE <db>.<schema>.<name>` | Yes |
| `FUNCTION <db>.<schema>.<name>(<arg_types>)` | No |
| `PROCEDURE <db>.<schema>.<name>(<arg_types>)` | No |
| `STAGE <db>.<schema>.<name>` | No |
| `TASK <db>.<schema>.<name>` | No |
| `ROLE <name>` | No |
| `DATABASE ROLE <db>.<name>` | No |
| `WAREHOUSE <name>` | No |

Expand

Show lessSee more

To attach a tag to a data metric function, use the `FUNCTION` keyword with `TABLE(...)` argument notation, not
`DATA METRIC FUNCTION`:

Copy code

```
ATTACH TAG MY_DB.GOV.MY_TAG = 'v1'
  TO FUNCTION MY_DB.GOV.MY_DMF(TABLE(VARCHAR));
```

**Lifecycle:**

DCM Projects tracks individual `tag-target` pairs, not whole statements. On each deployment, DCM Projects executes:

- **Attach:** Any pair that is newly declared in the definitions is attached.
- **Alter:** If the value for a pair changes, DCM Projects updates it on the next deployment.
- **Detach:** If a pair is removed from the definitions, DCM Projects detaches the tag from that target on the next
  deployment.

Tag assignments made outside DCM Projects aren’t tracked by DCM Projects and won’t be affected by a deployment, regardless of whether DCM Projects manages the
target object.

To assign a different value to the same tag on different targets, split them into separate statements:

Copy code

```
ATTACH TAG MY_DB.GOV.TAG_ENV = 'production'
  TO TABLE MY_DB.SALES.CUSTOMERS;

ATTACH TAG MY_DB.GOV.TAG_ENV = 'staging'
  TO TABLE MY_DB.SALES.ORDERS;
```

**Uniqueness constraint:**

Each `tag-target` pair must appear at most once across all files in the project. Declaring the same pair in two
different statements is an error.

You can freely reorganize how pairs are grouped across statements without affecting deployed state. DCM Projects considers
a single 2×2 statement, two 1×2 statements, and four 1×1 statements covering the same pairs to be equivalent.

**Native tagging behaviors:**

`ATTACH TAG` exercises the same engine path as `ALTER <object> SET TAG`, so all native Snowflake tagging behaviors
apply, including tag inheritance (from containers to child objects), tag propagation (from tables to columns), and
masking policy association (when a tag has a masking policy attached). See [Object tagging](/user-guide/object-tagging/introduction)
for the full description of these behaviors.

**Limitations:**

- The account-level `GRANT APPLY TAG ON ACCOUNT` privilege is enforced only when the grantee can also see the target
  object. If the grantee doesn’t hold a privilege that lets them see the target, the attachment isn’t applied.
- All native Snowflake [object tagging limitations and quotas](/user-guide/object-tagging/introduction#label-object-tagging-limitations-and-considerations)
  apply.
- Masking policies and row access policies aren’t yet supported as `ATTACH TAG` targets.
