Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$DEMIGRATE\_DBT\_PROJECT

Reverts a migrated dbt project object from the mutable live-version model to the previous versioned
object model.

## Syntax

Copy code

```
SYSTEM$DEMIGRATE_DBT_PROJECT ( '<object_name>' [ , '<mode>' ] )
```

## Arguments

`object_name`
:   String that specifies the fully qualified name of the dbt project object to demigrate.

`mode`
:   Optional string that specifies how to handle the live version when reverting:

    - `COMMIT` (default): Publishes the current live version as a new committed version, then reverts
      the object to the previous versioned model.
    - `ABORT`: Discards the live version and reverts to the last committed version.

    If you omit this argument, the function uses `COMMIT`.

## Access control requirements

The role used to call this function must have the `OWNERSHIP` privilege on the dbt project object.

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

This function is available only if your account is opted in to the 2026\_06 behavior change bundle or
a Snowflake account representative has enabled the separate single live version feature. This function
will no longer work after the 2026\_06 behavior change bundle is fully enabled. For details, see
[dbt Projects on Snowflake: dbt project objects migrate to a single mutable live version](/release-notes/bcr-bundles/2026_06/bcr-2362).

## Examples

Revert the dbt project object `analytics_db.dbt_projects.finance_project` to the previous versioned
object model. Because `mode` is omitted, the function uses `COMMIT` and publishes the current live
version as a new committed version:

Copy code

```
SELECT SYSTEM$DEMIGRATE_DBT_PROJECT(
  'analytics_db.dbt_projects.finance_project'
);
```

The following statement is equivalent:

Copy code

```
SELECT SYSTEM$DEMIGRATE_DBT_PROJECT(
  'analytics_db.dbt_projects.finance_project',
  'COMMIT'
);
```

Discard the live version and revert to the last committed version:

Copy code

```
SELECT SYSTEM$DEMIGRATE_DBT_PROJECT(
  'analytics_db.dbt_projects.finance_project',
  'ABORT'
);
```
