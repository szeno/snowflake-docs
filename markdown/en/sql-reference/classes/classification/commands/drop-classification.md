# DROP SNOWFLAKE.ML.CLASSIFICATION

Drop an instance of a classification model.

See also:
:   [CREATE SNOWFLAKE.ML.CLASSIFICATION](/sql-reference/classes/classification/commands/create-classification).

## Syntax

Copy code

```
DROP SNOWFLAKE.ML.CLASSIFICATION [ IF EXISTS ] <name>
```

## Parameters

`name`
:   Specifies the identifier for the classification model. The identifier must start with an alphabetic character and cannot contain spaces or
    special characters unless the identifier string is enclosed in double quotes (e.g. `"My object"`). Identifiers enclosed in double
    quotes are also case-sensitive.

    If the model identifier is not fully-qualified (in the form of `db_name.schema_name.model_name` or
    `schema_name.model`), the command looks for the model in the current schema for the session.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege / Role | Object | Notes |
| --- | --- | --- |
| OWNERSHIP privilege | Classification model | The role used to drop a classification model must be granted this privilege on the model. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

Dropped classification models cannot be recovered; they must be recreated.

## Examples

Drop classification model `my_model` in the current schema:

Copy code

```
DROP SNOWFLAKE.ML.CLASSIFICATION my_model;
```
