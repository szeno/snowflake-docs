# Supported object types in DCM Projects

DCM Projects definition files support three types of statements:

- **[Entities](#label-dcm-projects-entities)** — `DEFINE` statements that create and manage Snowflake objects
- **[Grants](#label-dcm-projects-grants)** — `GRANT` statements that assign privileges and roles
- **[Attachments](#label-dcm-projects-attachments)** — `ATTACH` statements that associate objects with other objects

**Entities:**

- [Alert](#label-dcm-projects-object-type-alert)
- [Database](#label-dcm-projects-object-type-database)
- [Dynamic table](#label-dcm-projects-object-type-dynamic-table)
- [File format](#label-dcm-projects-object-type-file-format)
- [Functions](#label-dcm-projects-object-type-function)
  - [Data metric functions](#label-dcm-projects-object-type-dmf-function)
- [Network rule](#label-dcm-projects-object-type-network-rule)
- [Pipe](#label-dcm-projects-object-type-pipe)
- [Policies](#label-dcm-projects-object-type-policies)
  - [Authentication policy](#label-dcm-projects-object-type-auth-policy)
  - [Masking policy](#label-dcm-projects-object-type-masking-policy)
  - [Network policy](#label-dcm-projects-object-type-network-policy)
  - [Row access policy](#label-dcm-projects-object-type-row-access-policy)
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
- [Table](#label-dcm-projects-object-type-table)
- [Tag](#label-dcm-projects-object-type-tag)
- [Task](#label-dcm-projects-object-type-task)
- [View](#label-dcm-projects-object-type-view)
- [Warehouse](#label-dcm-projects-object-type-warehouse)

**Grants:**

- [GRANT](#label-dcm-projects-object-type-grant)
- [OWNERSHIP grants](#label-dcm-projects-object-type-grant-ownership)
- [Inherited grants](#label-dcm-projects-inherited-grants)
- [Container-level MANAGE GRANTS](#label-dcm-projects-container-manage-grants)

**Attachments:**

- [ATTACH Data Metric Function](#label-dcm-projects-object-type-dmf)
- [ATTACH TAG](#label-dcm-projects-attach-tag)

## Entities

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

- Reordering columns

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

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

DCM Projects supports defining Snowflake pipes. DCM Projects manages the pipe lifecycle (`CREATE`, `ALTER`, `DROP`) across environments using Jinja
templating. All pipe properties supported by [CREATE PIPE](/sql-reference/sql/create-pipe) are available in `DEFINE PIPE`.

**Limitations:**

- Only the pipe `COMMENT` can be changed after creation. The `COPY INTO` body and all other pipe properties are immutable.
- `AUTO_INGEST = TRUE` requires an S3/Azure/GCS event notification to be configured outside of DCM Projects. DCM Projects creates the pipe
  but doesn’t configure the cloud-side notification.

### Policies

DCM Projects supports defining the following types of policies:

#### Authentication policy

DCM Projects supports defining authentication policies. For more information, see
[CREATE AUTHENTICATION POLICY](/sql-reference/sql/create-authentication-policy).

#### Masking policy

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

DCM Projects supports defining masking policies. For more information, see [CREATE MASKING POLICY](/sql-reference/sql/create-masking-policy).

**Limitations:**

- Attaching a masking policy to a table or view column as part of a DCM project definition isn’t yet supported; see
  [Attachments](#label-dcm-projects-attachments).

#### Network policy

DCM Projects supports defining network policies, which restrict account, user, or integration access to specific IP addresses using
network rules. For more information, see [Controlling network traffic with network policies](/user-guide/network-policies).

**Limitations:**

- You can’t replace an existing network policy while it’s assigned to an account, security integration, or user. Unassign the
  policy before redeploying a replacement.
- Assigning the policy to an account, user, or integration must be done outside of DCM Projects, using `ALTER ACCOUNT`, `ALTER USER`,
  or `ALTER SECURITY INTEGRATION`.

#### Row access policy

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

DCM Projects supports defining row access policies, which filter the rows returned by a query based on the executing role. All row
access policy properties supported by [CREATE ROW ACCESS POLICY](/sql-reference/sql/create-row-access-policy) are available in
`DEFINE ROW ACCESS POLICY`. For more information, see [Understanding row access policies](/user-guide/security-row-intro).

**Limitations:**

- Attaching a row access policy to a table or view as part of a DCM project definition isn’t yet supported; see
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
    orders (CUSTOMER_ID) REFERENCES customers (CUSTOMER_ID)
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

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

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

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

DCM Projects supports defining streams. All stream variants supported by
[CREATE OR ALTER STREAM](/sql-reference/sql/create-stream#create-or-alter-stream) are available in `DEFINE STREAM`,
including streams on tables, views, directory tables, and external tables.

**Limitations:**

- Streams are immutable after creation. Only the `COMMENT` can be changed. To change any other property (such as the
  source object or `APPEND_ONLY`), you must drop and recreate the stream.

### Table

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

- All tasks in a task graph must be defined within the same DCM project.
- To transfer ownership of a task graph within DCM Projects, define a `GRANT OWNERSHIP` statement for each task in the graph. Granting
  ownership on child tasks detaches them from the graph. Deploy the project to create the graph and apply the ownership grants,
  then deploy again to restore the parent-child links from your definitions.
- `PLAN` only validates that the task can be created successfully. It doesn’t check whether the task will run successfully, as task
  logic is compiled at runtime.

### View

**Limitations:**

- Reordering columns

### Warehouse

**Immutable attributes:**

- INITIALLY\_SUSPENDED

## Grants

DCM Projects uses `GRANT` statements to assign privileges and roles within a project.

### GRANT

Just like each object can be defined only once in DCM Projects, each privilege-grantee relationship can only be defined once across all DCM Projects.

DCM Projects is only aware of grants that were defined and deployed through DCM Projects. Any grants that were added outside of DCM Projects coexist,
and DCM Projects doesn’t remove them.

Note

`GRANT ON ALL` and `GRANT ON FUTURE` aren’t recommended in DCM Projects. Use [inherited grants](#label-dcm-projects-inherited-grants)
instead, which apply to all current and future objects of a type within a container and offer better performance for DCM Projects executions.

**Unsupported `GRANT` types:**

- CALLER grants

### OWNERSHIP grants

The DCM project owner role automatically has `OWNERSHIP` on all roles it creates inside the project. However, if one of those roles is
then granted `OWNERSHIP` of other deployed entities, the project owner role no longer has direct `OWNERSHIP` of those entities. To avoid
being locked out on future deployments, explicitly grant the role to the project owner role in the same definition files:

Copy code

```
DEFINE ROLE MY_DB.MY_SCHEMA.DATA_OWNER_ROLE;
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

### Inherited grants

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

DCM Projects supports [inherited grants](/user-guide/inherited-grants-intro), which let you declaratively define a single grant on a
container (`ACCOUNT`, `DATABASE`, or `SCHEMA`) that automatically applies to every current and future object of a specified type
within that container.

**Prerequisites:**

Inherited grants require a separate account-level opt-in that’s independent of DCM Projects. Before you can include them in your DCM Projects
definitions, run:

Copy code

```
ALTER ACCOUNT SET FEATURE_RBAC_INHERITED_GRANTS = 'ENABLED';
```

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

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

In conjunction with inherited grants, DCM Projects also supports
[container-level `MANAGE GRANTS`](/user-guide/container-manage-grants-intro), which lets you delegate grant administration for a
specific database or schema. A role granted `MANAGE GRANTS` on a container can manage all grant types on objects inside that
container without needing account-level `SECURITYADMIN` privileges.

**Prerequisites:**

Container-level `MANAGE GRANTS` requires the same account-level opt-in as inherited grants. Before you can include it in your
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

- You can’t change the role specified by `EXECUTE AS ROLE` for an existing attachment by modifying just that property. To change
  the role, remove the `ATTACH` statement, deploy, then redefine it with the new `EXECUTE AS ROLE` value.

To see all available system DMFs, query `SHOW DATA METRIC FUNCTIONS IN DATABASE SNOWFLAKE`.

### ATTACH TAG

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Use `ATTACH TAG` to declaratively assign Snowflake object tags to any DCM Projects-managed entity. DCM Projects reconciles the
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
  TO <entity_keyword> <entity_fqn> [ COLUMN <column_name> ];
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
You can mix entity-level and column-level targets in the same statement.

Copy code

```
ATTACH TAG MY_DB.GOV.TAG_PII = 'true',
           MY_DB.GOV.TAG_SENSITIVITY = 'high'
  TO TABLE MY_DB.SALES.CUSTOMERS COLUMN EMAIL,
     TABLE MY_DB.SALES.ORDERS,
     VIEW  MY_DB.SALES.ACTIVE_ACCOUNTS;
```

This single statement creates six tag-target pairs: both tags are attached to each of the three targets.

**Supported entities:**

| Entity keyword | Column target supported |
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

Tags attached to objects outside of DCM Projects aren’t tracked by DCM Projects and won’t be affected by any deployment.

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
  entity. If the grantee doesn’t hold a privilege that lets them see the target, the attachment isn’t applied.
- All native Snowflake [object tagging limitations and quotas](/user-guide/object-tagging/introduction#label-object-tagging-limitations-and-considerations)
  apply.
- Masking policies and row access policies aren’t yet supported as `ATTACH TAG` targets.
