# CREATE CODE BUNDLE

Note

Notebook Project Objects have been renamed to **Code Bundles**. The `NOTEBOOK PROJECT` grammar is still supported; for that syntax, see [CREATE NOTEBOOK PROJECT](/sql-reference/sql/create-notebook-project). For background on the rename, see the [behavior change announcement](/release-notes/bcr-bundles/un-bundled/bcr-2393).

Creates a [Code Bundle](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-schedule#label-nb-in-ws-schedule-npo): a named,
schema-level object that packages your project source files (for example, `.py` scripts, `.ipynb` notebooks, and SQL files) for non-interactive
execution on Snowflake compute. When the Code Bundle is created, all files from the source are copied into the object in the specified database and
schema. The Code Bundle can then be executed using [EXECUTE CODE BUNDLE](/sql-reference/sql/execute-code-bundle).

You can create a Code Bundle from a stage or a private workspace.

Note

Creating Code Bundles from shared workspaces is not currently supported.

See also:
:   [EXECUTE CODE BUNDLE](/sql-reference/sql/execute-code-bundle), [SHOW CODE BUNDLES](/sql-reference/sql/show-code-bundles), [CREATE NOTEBOOK](/sql-reference/sql/create-notebook), [EXECUTE NOTEBOOK](/sql-reference/sql/execute-notebook)

## Syntax

**Create a Code Bundle from a private workspace:**

Copy code

```
CREATE [ OR REPLACE ] CODE BUNDLE [ IF NOT EXISTS ] <database_name>.<schema_name>.<bundle_name>
  FROM 'snow://workspace/<workspace_path>'
  [ COMMENT = '<string_literal>' ];
```

**Create a Code Bundle from a stage:**

Copy code

```
CREATE [ OR REPLACE ] CODE BUNDLE [ IF NOT EXISTS ] <database_name>.<schema_name>.<bundle_name>
  FROM '@<database_name>.<schema_name>.<stage_name>'
  [ COMMENT = '<string_literal>' ];
```

## Required parameters

`database_name.schema_name.bundle_name`
:   Fully qualified identifier for the Code Bundle.

    The bundle name must be unique within the schema.

    Identifiers must start with an alphabetic character and cannot contain spaces or special characters unless the identifier is enclosed in double
    quotes (for example, `"My Bundle"`).

    Identifiers in double quotes are case-sensitive.

`FROM { 'snow://workspace/workspace_path' | '@database_name.schema_name.stage_name' }`
:   Specifies the source that backs this Code Bundle.

    - Use a `snow://workspace/...` URL to create the Code Bundle from a workspace version in Snowsight.
    - Use a stage reference (for example, `'@my_db.my_schema.my_stage'`) to create the Code Bundle from files that you have
      deployed to an internal or temporary stage.

    When creating from a workspace, the value must be a `snow://workspace/...` URL pointing to a workspace version.

    The path typically includes:

    - USER$ or another owner.
    - Schema.
    - Workspace name.
    - Version (for example, `versions/last`).

    For example:

    - `snow://workspace/USER$.MY_SCHEMA."my_workspace"/versions/last`

To locate the workspace path, run the following command:

Copy code

```
LIST 'snow://workspace/USER$.PUBLIC.DEFAULT$/versions/last/';
```

## Optional parameters

`COMMENT = 'string_literal'`
:   Adds a comment or description to the Code Bundle.

    Use comments to describe the purpose or workflow (for example, `COMMENT = 'Code Bundle for this workflow'`).

    Comments are stored as object metadata; avoid including sensitive data in comments.

## Access control requirements

To execute `CREATE CODE BUNDLE`, a role must have sufficient privileges to create objects in the target database and schema. Required
privileges include:

- USAGE or OWNERSHIP on the database.
- USAGE or OWNERSHIP on the schema.
- CREATE CODE BUNDLE on the schema that allows creating objects within that schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- The OR REPLACE and IF NOT EXISTS clauses are mutually exclusive. They can’t both be used in the same statement.
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

- A Code Bundle points to the specified workspace version indicated in the FROM clause. Using `versions/last` always references the latest
  workspace version; using a fixed path references a static version.
- If you create the Code Bundle from a stage, you can update it by adding versions from the stage. For details,
  see [Run and schedule Notebooks in Workspaces](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-schedule).
- Use descriptive bundle names to simplify workflow orchestration.
- Replacing a Code Bundle updates the stored source path and metadata.
- To run the `CREATE CODE BUNDLE` command, you must execute it from a SQL file or SQL worksheet in Workspaces, not from within a notebook cell.

## Examples

Create a Code Bundle from a workspace:

Copy code

```
CREATE CODE BUNDLE analytics_db.workflow_schema.workflow_bundle
  FROM 'snow://workspace/USER$.workflow_schema."etl_workflow"/versions/last'
  COMMENT = 'Code Bundle for nightly ETL workflow';
```

Create a Code Bundle from a stage:

Copy code

```
CREATE CODE BUNDLE analytics_db.workflow_schema.workflow_bundle
  FROM '@CODE_BUNDLE_STAGE'
  COMMENT = 'Code Bundle created from an internal or temporary stage';
```

Create a Code Bundle from a stage using IF NOT EXISTS:

Copy code

```
CREATE CODE BUNDLE IF NOT EXISTS ML_TRAIN_BUNDLE3
  FROM '@CODE_BUNDLE_STAGE1'
  COMMENT = 'Code Bundle created from an internal or temporary stage';
```
