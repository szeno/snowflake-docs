# SHOW VERSIONS IN DATASET

Displays information about the datasets in your account at either the schema or database level.

See also:
:   [SHOW DATASETS](/sql-reference/sql/show-datasets) , [ALTER DATASET](/sql-reference/sql/alter-dataset), [CREATE DATASET](/sql-reference/sql/create-dataset)

## Syntax

Copy code

```
SHOW VERSIONS [ LIKE '<pattern>' ] IN DATASET <dataset_name>
  [ LIMIT <rows>]
```

## Parameters

`IN DATASET dataset_name`
:   Name of dataset for which versions are displayed.

`LIKE pattern`
:   Restricts the list of returned datasets to those matching the specified pattern. Matching is case-insensitive.

`LIMIT num`
:   Limits the maximum number of rows returned.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP or USAGE | Dataset | Provides the privilege to show the dataset versions within the account. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).
