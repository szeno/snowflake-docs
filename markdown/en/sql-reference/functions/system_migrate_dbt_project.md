Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$MIGRATE\_DBT\_PROJECT

Migrates a dbt project object to the mutable live-version model.

## Syntax

Copy code

```
SYSTEM$MIGRATE_DBT_PROJECT ( '<object_name>' )
```

## Arguments

`object_name`
:   String that specifies the fully qualified name of the dbt project object to migrate.

## Access control requirements

The role used to call this function must have the `OWNERSHIP` privilege on the dbt project object.

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- This function is available only if your account is opted in to the 2026\_06 behavior change bundle
  or a Snowflake account representative has enabled the separate single live version feature. For
  opt-in steps and the difference between creating or replacing an object and migrating an existing
  object, see [dbt Projects on Snowflake: dbt project objects migrate to a single mutable live version](/release-notes/bcr-bundles/2026_06/bcr-2362).
- The migrated object has a single mutable version named `live`.
- Migration preserves the dbt project object’s identity, grants, task references, and execution
  history.

## Examples

Migrate the dbt project object `analytics_db.dbt_projects.finance_project` to the live-version model:

Copy code

```
SELECT SYSTEM$MIGRATE_DBT_PROJECT(
  'analytics_db.dbt_projects.finance_project'
);
```
