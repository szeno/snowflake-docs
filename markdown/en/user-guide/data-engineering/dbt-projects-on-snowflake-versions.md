# Numbered versions for dbt project objects and files

Warning

The numbered-version functionality described on this page is available only until the 2026\_06 behavior change bundle is fully enabled. After
the change, dbt project objects use a single mutable `live` version, and any remaining versioned objects are automatically migrated. For
details, see [dbt Projects on Snowflake: dbt project objects migrate to a single mutable live version](/release-notes/bcr-bundles/2026_06/bcr-2362).

Snowflake maintains immutable versions of dbt project objects and their source files. This versioning lets you track and manage changes
throughout the development lifecycle.

Note

dbt project object versions are distinct from the dbt Core or dbt Fusion version used for execution. For more information, see [Supported dbt versions for dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-dbt-core-versions).

Snowflake identifies dbt project object versions in the dbt project stage, as shown in the following example.

`snow://dbt/my_db.my_schema.my_dbt_project_object/versions/<version_id>`

`<version_id>` can be any of the following identifiers:

| Identifier | Description |
| --- | --- |
| `VERSION$<num>` | Specifies a version identifier in the form `VERSION$<num>`, where `<num>` is a positive integer. For example, `VERSION$1`.  The version number begins at `1` when you create a dbt project object and increments by one with each new version of the dbt project object.  Snowflake increments the version identifier when you perform the following tasks:   - **Redeploy dbt project** from a workspace (runs the ALTER command with the ADD VERSION option). - Update the project by using the [ALTER DBT PROJECT](/sql-reference/sql/alter-dbt-project) command. - Run the Snow CLI `snow dbt deploy` command.   Snowflake resets the version identifier to `1` and removes all version aliases when you run the CREATE DBT PROJECT command with the `OR REPLACE` option.  Warning  Don’t use `snow dbt deploy --force` to create a new version. `--force` runs `CREATE OR REPLACE DBT PROJECT`, which removes all existing versions and run history. |
| `LAST` | Indicates the most recent version of the dbt project object. |
| `FIRST` | Indicates the oldest version of the dbt project object. |
| `<version_name_alias>` | Indicates a custom version name alias that you have created for a specific version of the dbt project object using the [ALTER DBT PROJECT](/sql-reference/sql/alter-dbt-project) command with the ADD VERSION option. A version name alias always maps to a specific version identifier, such as `VERSION$3`. |

Expand

Show lessSee more

Project files stored in the dbt project stage are organized by version, with each version having its own subdirectory. For example, a dbt
project object named `my_dbt_project_object` with a version identifier of `VERSION$3` and a dbt project file named `dbt_project.yml`
can be referenced as `snow://dbt/my_db.my_schema.my_dbt_project_object/versions/VERSION$3/dbt_project.yml`.
