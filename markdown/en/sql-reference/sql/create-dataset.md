# CREATE DATASET

Creates a new [machine learning dataset](/developer-guide/snowflake-ml/dataset) in the current schema or the schema that you specify.

See also:
:   [ALTER DATASET](/sql-reference/sql/alter-dataset) , [ALTER DATASET … ADD VERSION](/sql-reference/sql/alter-dataset-add-version) , [ALTER DATASET … DROP VERSION](/sql-reference/sql/alter-dataset-drop-version), [SHOW DATASETS](/sql-reference/sql/show-datasets)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] [ IF NOT EXISTS ] DATASET <name>
```

## Required parameters

`name`
:   The name of the dataset that you’re creating within the current schema or a schema that you specify.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE DATASET | Schema | Only provides the privilege to create a dataset. You must also have the USAGE privilege on the schema. |

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

## Examples

The following example creates a dataset called `my_dataset`:

Copy code

```
CREATE DATASET my_dataset;
```

The following example creates or replaces a dataset called `my_dataset`:

Copy code

```
CREATE OR REPLACE DATASET my_dataset;
```
