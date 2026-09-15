# EXECUTE DCM PROJECT

Executes one of the following actions on a [DCM project](/user-guide/dcm-projects/dcm-projects-overview):

- `EXECUTE DCM PROJECT <name> PLAN` performs a dry run of the DCM project to analyze the changes that would be applied to the target
  during a deployment, but doesn’t apply any changes.
- `EXECUTE DCM PROJECT <name> PLAN DELTA` performs a faster dry run that only evaluates definitions that changed since the last
  deployment, and any downstream definitions that depend on them.
- `EXECUTE DCM PROJECT <name> DEPLOY` deploys the changes defined in the project’s definition files to the account.
- `EXECUTE DCM PROJECT <name> TEST ALL` tests all expectations from attached data metric functions managed by the DCM project.
- `EXECUTE DCM PROJECT <name> PREVIEW` returns a data sample of the current definitions specified in the source path for
  the specified table, view, or dynamic table.
- `EXECUTE DCM PROJECT <name> PURGE` drops all entities, revokes all grants, and removes all attachments currently managed
  by the DCM project.

See also:
:   [CREATE DCM PROJECT](/sql-reference/sql/create-dcm-project), [ALTER DCM PROJECT](/sql-reference/sql/alter-dcm-project), [DESCRIBE DCM PROJECT](/sql-reference/sql/desc-dcm-project), [DROP DCM PROJECT](/sql-reference/sql/drop-dcm-project), [SHOW DCM PROJECTS](/sql-reference/sql/show-dcm-projects), [SHOW DEPLOYMENTS IN DCM PROJECT](/sql-reference/sql/show-deployments-in-dcm-project)

## Syntax

Copy code

```
EXECUTE DCM PROJECT <name>
  PLAN [ DELTA ]
  [ USING [ CONFIGURATION <config_name> ] [ (<expr>, [, <expr>, ...]) ] ]
  FROM '<source-files_path>'
  [ OUTPUT_PATH '<output_path>' ]

EXECUTE DCM PROJECT <name>
  DEPLOY [ AS "<deployment_name_alias>" ]
  [ USING [ CONFIGURATION <name> ] [ (<expr>, [, <expr>, ...]) ] ]
  FROM '<source-files_path>'

EXECUTE DCM PROJECT <name>
  TEST ALL

EXECUTE DCM PROJECT <name>
  PREVIEW <fully_qualified_table_object_name>
  USING CONFIGURATION <config_name>
  FROM '<source_files_path>'

EXECUTE DCM PROJECT <name>
  PURGE [ AS "<deployment_name_alias>" ]
```

## Required parameters

`name`
:   Specifies the identifier for the DCM project to execute.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`PLAN`
:   Instructs Snowflake to perform a dry run of the DCM project. For a dry run, Snowflake analyzes the changes that
    would be applied to the target during a deployment, but doesn’t apply any changes.

`PLAN DELTA`
:   Instructs Snowflake to perform a faster dry run that only evaluates the definitions that changed since the last
    deployment, and any downstream definitions in the project that depend on them. Unlike a full `PLAN`, `PLAN DELTA`
    doesn’t compare unchanged definitions against the current account state.

    Use `PLAN DELTA` during active development to get faster feedback on incremental changes. Because it skips unchanged
    definitions, it doesn’t detect changes that happened outside of DCM Projects on your account since the last deployment (for
    example, a view dropped or altered by another user). Always run a full `PLAN` before deploying to ensure no external
    changes will cause a deployment failure.

`DEPLOY [ AS "deployment_name_alias" ]`
:   Deploys the changes defined in the project’s definition files to the account; optionally specifies an alias for the deployment.

`FROM 'source_files_path'`
:   Specifies the directory that contains the source files for the DCM project. The directory must contain a manifest file and at least one
    definition file in `/sources/definitions/`. The manifest file provides the templating values in case a configuration was specified.

`TEST ALL`
:   [![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open

    Available to all accounts.

    Tests all data quality expectations attached to tables, dynamic tables, or views which are currently managed by the DCM project.

`PREVIEW fully_qualified_table_object_name`
:   [![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open

    Available to all accounts.

    Returns a data sample of the current definitions specified in the source path for the specified table, view, or dynamic table -
    independent of any deployed state.

`PURGE [ AS "deployment_name_alias" ]`
:   Drops all entities, revokes all grants, and removes all attachments currently managed by the DCM project, by running a
    deployment with no definitions. Optionally, specify an alias for the deployment.

    Warning

    PURGE is destructive by design. Use it with caution and only for non-production projects, such as development sandboxes
    or demos.

    PURGE doesn’t drop the DCM project itself. To remove the project object after purging, run [DROP DCM PROJECT](/sql-reference/sql/drop-dcm-project). The purge
    execution appears in the deployment history of the DCM project, where you can confirm that the command ran successfully.

## Optional parameters

`USING CONFIGURATION config_name`
:   Specifies the configuration to use. This lets you customize deployments for different environments, such as development, staging, or
    production, without using different project definition files.

    If the configuration name is not in all uppercase, enclose it in double quotes.

`USING ( expr [, expr , ... ] )`
:   Optionally specifies template variable values. Using this option overrides any default or configuration values for this specific variable.
    The single expression must have the following form: `<variable_name> => <variable_value>`. For lists, use the following form:
    `<variable_name> => [<value1>, <value2>, ...]`. For example: `wh_size => 'MEDIUM'` or `teams => ['TEAM_A', 'TEAM_B']`.

    This lets you customize deployments for different environments, such as development, staging, or production, without using different
    project definition files.

`OUTPUT_PATH 'output_path'`
:   Specifies a directory where Snowflake writes the rendered project definitions and the raw changeset from a `PLAN` execution. If
    the directory doesn’t exist, Snowflake creates it. Each `PLAN` execution that specifies `OUTPUT_PATH` overwrites any previously
    rendered output in that directory.

    See [The /out/ subfolder](/user-guide/dcm-projects/dcm-projects-overview#label-dcm-projects-out-folder) for details on the contents of
    this directory.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | DCM project | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Output

After the DCM project executes, this command returns the following output depending on the variation:

- PLAN, DEPLOY, and PURGE: A single row containing a JSON object with the change log. Because PURGE runs as an empty
  deployment, its output is identical to DEPLOY, with all managed entities reported as `DROP`.
- PREVIEW: A result set.
- TEST ALL: A single row containing a JSON object that contains the full response.

### PLAN and DEPLOY output

Note

For object types still in preview, the exact output format can be subject to change.

The standard plan output contains the following information about the plan execution in JSON format:

```
{
  "version": 2,
  "metadata": {
    "timestamp": <timestamp>,
    "query_id": <query_id>,
    "project_name": <project_name>,
    "user": <user>,
    "role_name": <role_name>,
    "command": <command>
  },
  "changeset": [
    {
      "type": <type>,
      "object_id": {
        "domain": <domain>,
        "name": <name>,
        "fqn": <fqn>,
        "database": <database>,
        "schema": <schema>
      },
      "changes": [
        {
          "kind": <kind>,
          "attribute_name": <attribute_name>,
          "value": <value>,
          "changes": [
            {
              "kind": <kind>,
              "attribute_name": <attribute_name>,
              "value": <value>
            }
          ]
        }
      ]
    }
  ]
}
```

| Property | Description |
| --- | --- |
| `version` | Schema version of the output format. Version 2 is the latest and only supported version. |
| `metadata` | Contextual information about the execution. |
| `metadata.timestamp` | ISO 8601 timestamp of when the command was executed. |
| `metadata.query_id` | Unique identifier for the query that produced this plan. |
| `metadata.project_name` | Fully qualified name of the DCM Project object. |
| `metadata.user` | Name of the user who executed the command. |
| `metadata.role_name` | Active role used to execute the command. |
| `metadata.command` | The command that was executed. `PLAN` or `DEPLOY`. |
| `changeset` | An array of change entries. Each entry represents one object that would be or was created, altered, or dropped. An empty array indicates the project definitions are already in sync with the account. |
| `changeset[].type` | The planned action for the object. Possible values: `CREATE`, `ALTER`, `DROP`. |
| `changeset[].object_id` | Identifies the target object. |
| `changeset[].object_id.domain` | The Snowflake object type. |
| `changeset[].object_id.name` | Name of the object. |
| `changeset[].object_id.fqn` | Fully qualified name of the object. |
| `changeset[].object_id.database` | Database containing the object. Omitted for account-level objects. |
| `changeset[].object_id.schema` | Schema containing the object. Omitted for database-level and account-level objects. |
| `changeset[].changes` | An array of change descriptors detailing the specific attribute modifications. |
| `changeset[].changes[].kind` | The type of change. Possible values: `set`, `changed`, `unset`, `nested`, `collection`. The value of `kind` determines the remaining keys in the object. |
| `changeset[].changes[].attribute_name` | Name of the attribute being set or changed. Present when `kind` is `set`, `changed`, or `unset`. |
| `changeset[].changes[].value` | The new value for the attribute. Present when `kind` is `set` or `changed`. |
| `changeset[].changes[].prev_value` | The previous value of the attribute before the change. Present only when `kind` is `changed`. |
| `changeset[].changes[].collection_name` | Name of the collection being modified (for example, `columns`, `constraints`, `privileges`, `expectations`). Present only when `kind` is `collection`. |
| `changeset[].changes[].id_label` | Label used to identify items within the collection (for example, `name`). Present only on certain collections. |
| `changeset[].changes[].changes` | A nested array of collection item descriptors. Present only when `kind` is `collection`. |
| `changeset[].changes[].changes[].kind` | The type of change to the collection item. Possible values: `added`, `removed`, `modified`. |
| `changeset[].changes[].changes[].item_id` | Identifies the item within the collection. Can be a string or an object, depending on the collection type. |
| `changeset[].changes[].changes[].changes` | An array of further change descriptors for this item. Present for `added` and `modified` items. Always absent for `removed` items. |

Expand

Show lessSee more

An example of a plan output:

```
{
  "version": 2,
  "metadata": {
    "timestamp": <timestamp>,
    "query_id": <query_id>,
    "project_name": <project_name>,
    "user": <user>,
    "role_name": <role_name>,
    "command": <command>
  },
  "changeset": [
    {
      "type": "CREATE",
      "object_id": {
        "domain": "TABLE",
        "name": "CUSTOMER_SUMMARY",
        "fqn": "MY_DB.ANALYTICS.CUSTOMER_SUMMARY",
        "database": "MY_DB",
        "schema": "ANALYTICS"
      },
      "changes": [
        {
          "kind": "set",
          "attribute_name": "warehouse_size",
          "value": "XSMALL"
        },
        {
          "kind": "set",
          "attribute_name": "query",
          "value": "SELECT customer_id, SUM(amount) AS total FROM orders GROUP BY customer_id"
        }
      ]
    },
    {
      "type": "ALTER",
      "object_id": {
        "domain": "DYNAMIC_TABLE",
        "name": "ORDER_DETAILS",
        "fqn": "MY_DB.ANALYTICS.ORDER_DETAILS",
        "database": "MY_DB",
        "schema": "ANALYTICS"
      },
      "changes": [
        {
          "kind": "changed",
          "attribute_name": "warehouse_size",
          "value": "SMALL",
          "prev_value": "XSMALL"
        },
        {
          "kind": "collection",
          "collection_name": "columns",
          "id_label": "name",
          "changes": [
            {
              "kind": "added",
              "item_id": "DISCOUNT_AMOUNT",
              "changes": [
                {
                  "kind": "set",
                  "attribute_name": "data_type",
                  "value": "NUMBER(10,2)"
                }
              ]
            },
            {
              "kind": "modified",
              "item_id": "ORDER_STATUS",
              "changes": [
                {
                  "kind": "changed",
                  "attribute_name": "data_type",
                  "value": "VARCHAR(50)",
                  "prev_value": "VARCHAR(20)"
                }
              ]
            },
            {
              "kind": "removed",
              "item_id": "LEGACY_FLAG"
            }
          ]
        }
      ]
    },
    {
      "type": "DROP",
      "object_id": {
        "domain": "VIEW",
        "name": "OLD_REPORT_VIEW",
        "fqn": "MY_DB.ANALYTICS.OLD_REPORT_VIEW",
        "database": "MY_DB",
        "schema": "ANALYTICS"
      },
      "changes": []
    }
  ]
}
```

### TEST ALL output

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

The TEST output contains the overall status and expectations with their values in the following format:

Note

During the preview phase, the exact output format can be subject to change.

```
{
  "status": <status>,
  "expectations": [
    {
      "table_name": <table_name>,
      "metric_database": <metric_database>,
      "metric_schema": <metric_schema>,
      "metric_name": <metric_name>,
      "expectation_name": <expectation_name>,
      "expectation_expression": <expectation_expression>,
      "value": <value>,
      "expectation_violated": <expectation_violated>,
      "column_names": <column_names>
    }
  ]
}
```

| Property | Description |
| --- | --- |
| `status` | Overall result of the test run. Possible values: `SUCCESSFUL` (all expectations met), `FAILED` (one or more expectations violated). |
| `expectations[]` | An array of expectation results, one for each data quality expectation evaluated. |
| `table_name` | Fully qualified name of the table or view on which the expectation was evaluated. |
| `metric_database` | Database that contains the data metric function. |
| `metric_schema` | Schema that contains the data metric function. |
| `metric_name` | Name of the data metric function (for example, `NULL_COUNT`, `MIN`, `UNIQUE_COUNT`). |
| `expectation_name` | Name of the expectation as defined in the project. |
| `expectation_expression` | Boolean expression that the metric value is evaluated against (for example, `value = 0`, `value >= 0`). |
| `value` | The result of the data metric function evaluation. Present only when `expectation_violated` is `false`. |
| `expectation_violated` | Whether the expectation was violated. `true` if the metric value did not satisfy the expectation expression; `false` otherwise. |
| `column_names` | An array of column names on which the data metric function was evaluated. |

Expand

Show lessSee more

An example of the JSON output for a data quality test:

```
{
  "status": "FAILED",
  "expectations": [
    {
      "table_name": "db.schema.my_table",
      "metric_database": "SNOWFLAKE",
      "metric_schema": "CORE",
      "metric_name": "NULL_COUNT",
      "expectation_name": "no_nulls_in_id",
      "expectation_expression": "value = 0",
      "value": 0,
      "expectation_violated": false,
      "column_names": ["ID"]
    },
    {
      "table_name": "db.schema.my_table",
      "metric_database": "SNOWFLAKE",
      "metric_schema": "CORE",
      "metric_name": "UNIQUE_COUNT",
      "expectation_name": "unique_id_check",
      "expectation_expression": "value >= 100",
      "value": null,
      "expectation_violated": true,
      "column_names": ["ID"]
    }
  ]
}
```

## Usage notes

When executing a DCM project with EXECUTE DCM PROJECT PLAN, the output of the command is the same as for the actual deployment. The
difference is that no changes to the affected account are applied. This feature allows you to verify whether the rendered definition files
have a valid syntax, what changes would be applied to the account, and whether the project owner role has the required privileges to apply
these changes.

Because PLAN closely mirrors DEPLOY, it requires the same OWNERSHIP privilege on the DCM project as DEPLOY, even though no changes
are applied. This way, a dry run surfaces privilege errors before deployment.

To avoid unintended changes and catch errors, always run EXECUTE DCM PROJECT PLAN before you deploy a DCM project.

### Support for template variables

Template variables let you dynamically choose the content of the parameterized definitions files during the DCM project execution. You can
use template variables in the following ways:

See the [Template variable examples](#label-dcm-projects-template-variable-execute-examples) section for examples.

## Examples

### Basic examples

Execute a DCM project in PLAN mode to validate changes to a project without applying them:

Copy code

```
EXECUTE DCM PROJECT my_project
  PLAN
  FROM '@my_database.my_schema.my_stage/my_project';
```

Execute a DCM project in PLAN DELTA mode to quickly validate only the definitions that changed since the last
deployment:

Copy code

```
EXECUTE DCM PROJECT my_project
  PLAN DELTA
  FROM '@my_database.my_schema.my_stage/my_project';
```

Execute a DCM project in DEPLOY mode (to apply changes) to specify a deployment alias and
a configuration named PROD:

Copy code

```
EXECUTE DCM PROJECT my_project
  DEPLOY AS "my_update"
  USING CONFIGURATION PROD
  FROM '@my_database.my_schema.my_stage/my_project';
```

Purge a non-production DCM project to drop all entities, revoke all grants, and remove all attachments it currently manages,
with an alias to label the entry in the deployment history:

Copy code

```
EXECUTE DCM PROJECT my_project PURGE AS "sandbox cleanup";
```

### Template variable examples

The following examples demonstrate how you can specify the value
for template variables in an EXECUTE DCM PROJECT statement.

**Override the template variable defined in the DCM project’s manifest file**

1. Define a template variable named `desc` in the manifest file:

   Copy code

   ```
   manifest_version: 2
   type: DCM_PROJECT
   default_target: DCM_DEV
   targets:
     DCM_DEV:
    desc: "created by hello world project"
   ```
2. Create a definition file that uses the template variable:

   Copy code

   ```
   DEFINE DATABASE NEW_DB;
   DEFINE TABLE NEW_DB.PUBLIC.TBL (ID INT) COMMENT = '{{desc}}';
   ```
3. Call the EXECUTE DCM PROJECT command in DEPLOY mode,
   and specify a value for the `desc` variable to override its default value in the manifest:

   Copy code

   ```
   EXECUTE DCM PROJECT MY_PROJECT DEPLOY
     USING CONFIGURATION FIRST_CONFIG (desc => 'This object is mine')
     FROM '/my/project/source';
   ```

**Provide a value for a template variable not defined in the manifest file**

1. Create a definition file with the desired commands:

   Copy code

   ```
   DEFINE DATABASE NEW_DB;
   DEFINE TABLE NEW_DB.PUBLIC.TBL (ID INT) COMMENT = '{{desc_new}}';
   ```
2. Call the EXECUTE DCM PROJECT command, and specify a value for the `desc_new` variable:

   Copy code

   ```
   EXECUTE DCM PROJECT MY_PROJECT (desc_new => 'This object is mine');
   ```
