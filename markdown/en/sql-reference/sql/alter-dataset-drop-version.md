# ALTER DATASET … DROP VERSION

Drops a dataset version.

See also:
:   [ALTER DATASET](/sql-reference/sql/alter-dataset) , [ALTER DATASET … ADD VERSION](/sql-reference/sql/alter-dataset-add-version)

## Syntax

Copy code

```
ALTER DATASET [ IF EXISTS ] <name> DROP VERSION <version_name>
```

## Parameters

`name`
:   The name of the dataset that you’re dropping.

`DROP VERSION version_name`
:   The name of the dataset version that you’re dropping.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Dataset | Provides the privilege to both read and modify the dataset. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Examples

The following example drops version `v1` of the `my_dataset` dataset:

Copy code

```
ALTER DATASET my_dataset
DROP VERSION 'v1';
```
