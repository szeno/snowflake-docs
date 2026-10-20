# UNDROP STAGE

Restores a dropped named internal or external stage.

See also:
:   [CREATE STAGE](/sql-reference/sql/create-stage) , [ALTER STAGE](/sql-reference/sql/alter-stage) , [DROP STAGE](/sql-reference/sql/drop-stage) , [SHOW STAGES](/sql-reference/sql/show-stages) , [DESCRIBE STAGE](/sql-reference/sql/desc-stage)

## Syntax

Copy code

```
UNDROP STAGE <name>
```

## Parameters

`name`
:   Specifies the identifier for the stage to restore.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE STAGE | Schema that contained the stage | Required for every stage type, including temporary stages. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- You can restore named internal stages and external stages, including temporary named stages. You can’t restore the stage associated
  with a table or a user.
- A stage is restored to the database and schema that contained it when it was dropped, even if a different database or schema is
  current for the session.
- If an active stage with the same name already exists in that schema, an error is returned.
- If no dropped stage with the specified name is available to restore, for example because its
  [retention period](#label-undrop-stage-retention) has passed, an error is returned.
- If you might need to recover a stage, make sure its effective retention period is greater than `0` days before you drop it. For
  more information, see [Retention period for dropped stages](#label-undrop-stage-retention).
- For an internal stage, the staged files are restored with the stage, and the metadata in the stage’s directory table, if any, is
  preserved.
- If the stage has a directory table with automatic refresh enabled, the pipe that refreshes the directory table resumes when the
  stage is restored.
- For an external stage, files that are added to the external location while the stage is dropped aren’t registered automatically
  when you restore the stage. Run [ALTER STAGE … REFRESH](/sql-reference/sql/alter-stage) after restoring the stage to register
  those files in the directory table.

## Retention period for dropped stages

For a named internal stage, the [STAGE\_UNDROP\_RETENTION\_TIME\_IN\_DAYS](/sql-reference/parameters#label-stage-undrop-retention-time-in-days)
parameter determines how long the stage remains available to restore after it’s dropped. You can set the parameter at the account,
database, schema, or stage level, and a stage inherits the value from the nearest level where it’s set. The default is `0` days, so
the effective retention period must be increased before you drop a stage that you might need to restore.

[MIN\_STAGE\_UNDROP\_RETENTION\_TIME\_IN\_DAYS](/sql-reference/parameters#label-min-stage-undrop-retention-time-in-days) is an
account-level minimum that also defaults to `0` days. When it’s set to a value greater than `0`, the effective retention period for
a stage is MAX(`STAGE_UNDROP_RETENTION_TIME_IN_DAYS`, `MIN_STAGE_UNDROP_RETENTION_TIME_IN_DAYS`), and setting
`STAGE_UNDROP_RETENTION_TIME_IN_DAYS` below the minimum returns an error.

Neither parameter can be set to a value greater than `1` day (Standard Edition) or `90` days (Enterprise Edition or higher).
For more information, see [Data retention period](/user-guide/data-time-travel#label-time-travel-data-retention-period).

Neither `STAGE_UNDROP_RETENTION_TIME_IN_DAYS` nor `MIN_STAGE_UNDROP_RETENTION_TIME_IN_DAYS` controls how long a dropped external
stage remains available to restore. A dropped external stage remains restorable for the data retention period that applies to it.

## Examples

### Restore the most recently dropped stage

Drop a stage and then restore it:

Copy code

```
DROP STAGE my_stage;
```

```
+--------------------------------+
| status                         |
|--------------------------------|
| MY_STAGE successfully dropped. |
+--------------------------------+
```

Copy code

```
UNDROP STAGE my_stage;
```

```
+---------------------------------------+
| status                                |
|---------------------------------------|
| Stage MY_STAGE successfully restored. |
+---------------------------------------+
```
