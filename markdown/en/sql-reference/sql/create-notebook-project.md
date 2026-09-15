# CREATE NOTEBOOK PROJECT

Creates a notebook project object. A [notebook project object (NPO)](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-schedule#label-nb-in-ws-schedule-npo) links a Snowsight workspace
to a database and schema. When the NPO is created, all files from the workspace are copied into the project in the specified database and schema.
The notebook project can then be executed using [EXECUTE NOTEBOOK PROJECT](/sql-reference/sql/execute-notebook-project).
You can create a notebook project object from a stage or a private workspace.

Note

Creating notebook project objects from shared workspaces is not currently supported.

See also:
:   [EXECUTE NOTEBOOK PROJECT](/sql-reference/sql/execute-notebook-project), [SHOW NOTEBOOK PROJECTS](/sql-reference/sql/show-notebook-projects), [CREATE NOTEBOOK](/sql-reference/sql/create-notebook), [EXECUTE NOTEBOOK](/sql-reference/sql/execute-notebook)

## Syntax

**Create a notebook project object from a private workspace:**

Copy code

```
CREATE NOTEBOOK PROJECT <database_name>.<schema_name>.<project_name>
  FROM 'snow://workspace/<workspace_path>'
  [ COMMENT = '<string_literal>' ];
```

**Create a notebook project object from a stage:**

Copy code

```
CREATE NOTEBOOK PROJECT [ IF NOT EXISTS ] <database_name>.<schema_name>.<project_name>
  FROM '@<database_name>.<schema_name>.<stage_name>'
  [ COMMENT = '<string_literal>' ];
```

## Required parameters

`database_name.schema_name.project_name`
:   Fully qualified identifier for the notebook project.

    The project name must be unique within the schema.

    Identifiers must start with an alphabetic character and cannot contain spaces or special characters unless the identifier is enclosed in double
    quotes (for example, `"My Project"`).

    Identifiers in double quotes are case-sensitive.

`FROM { 'snow://workspace/workspace_path' | '@database_name.schema_name.stage_name' }`
:   Specifies the source that backs this notebook project.

    - Use a `snow://workspace/...` URL to create the notebook project from a workspace version in Snowsight.
    - Use a stage reference (for example, `'@my_db.my_schema.my_stage'`) to create the notebook project from notebook files that you have
      deployed to an internal or temporary stage.

    When creating from a workspace, the value must be a `snow://workspace/...` URL pointing to a workspace version.

    The path typically includes:

    - USER$ or another owner.
    - Schema.
    - Workspace name.
    - Version (for example, `versions/last`).

    For example:

    - `snow://workspace/USER$.MY_SCHEMA."my_notebook_workspace"/versions/last`

To locate the workspace path, run the following command:

Copy code

```
LIST 'snow://workspace/USER$.PUBLIC.DEFAULT$/versions/last/';
```

## Optional parameters

`COMMENT = 'string_literal'`
:   Adds a comment or description to the notebook project object.

    Use comments to describe the purpose or workflow (for example, `COMMENT = 'Notebook project for this workflow'`).

    Comments are stored as object metadata; avoid including sensitive data in comments.

## Access control requirements

To execute `CREATE NOTEBOOK PROJECT`, a role must have sufficient privileges to create objects in the target database and schema. Required
privileges include:

- USAGE or OWNERSHIP on the database.
- USAGE or OWNERSHIP on the schema.
- CREATE NOTEBOOK PROJECT on the schema that allows creating objects within that schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- The OR REPLACE and IF NOT EXISTS clauses are mutually exclusive. They can’t both be used in the same statement.
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

- A notebook project points to the specified workspace version indicated in the FROM clause. Using `versions/last` always references the latest
  workspace version; using a fixed path references a static version.
- If you create the notebook project from a stage, you can update it by adding versions from the stage. For details,
  see [Run and schedule Notebooks in Workspaces](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-schedule).
- Use descriptive project names to simplify workflow orchestration.
- Replacing a project updates the stored workspace path and metadata.
- To run the `CREATE NOTEBOOK PROJECT` command, you must execute it from a SQL file or SQL worksheet in Workspaces, not from within a notebook cell.

## Examples

Create a notebook project for a workspace:

Copy code

```
CREATE NOTEBOOK PROJECT analytics_db.workflow_schema.workflow_proj
  FROM 'snow://workspace/USER$.workflow_schema."etl_workflow"/versions/last'
  COMMENT = 'Notebook project for nightly ETL workflow';
```

Create a notebook project from a stage:

Copy code

```
CREATE NOTEBOOK PROJECT analytics_db.workflow_schema.workflow_proj
  FROM '@NOTEBOOK_PROJECT_STAGE'
  COMMENT = 'Notebook project created from an internal or temporary stage';
```

Create a notebook project from a stage using IF NOT EXISTS:

Copy code

```
CREATE NOTEBOOK PROJECT IF NOT EXISTS ML_TRAIN_NOTEBOOK3
  FROM '@NOTEBOOK_PROJECT_STAGE1'
  COMMENT = 'Notebook project created from an internal or temporary stage';
```
