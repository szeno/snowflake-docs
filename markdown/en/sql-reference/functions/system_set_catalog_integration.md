Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$SET\_CATALOG\_INTEGRATION

Replaces the catalog integration associated with an externally managed [Apache Iceberg™ table](/user-guide/tables-iceberg).

Use this function to update a table to work with an Iceberg REST catalog integration, which supports a wider range of Iceberg features, such as
[write support for externally managed Iceberg tables](/user-guide/tables-iceberg-externally-managed-writes). You might also use this function to roll back to
the original Glue catalog integration, if needed.

You can also use this function to migrate your table from one [Iceberg REST catalog integration](/user-guide/tables-iceberg-configure-catalog-integration-rest)
to another.

## Syntax

Copy code

```
SYSTEM$SET_CATALOG_INTEGRATION(
  '<table_name>' ,
  '<new_catalog_integration_name>'
)
```

## Arguments

`'table_name'`
:   Name of the Iceberg table whose catalog integration you want to replace.

`'new_catalog_integration_name'`
:   Name of the catalog integration that you want to migrate the given `table_name` to.

## Returns

The function returns a status message that the catalog integration for the table is successfully migrated. For an example, see
[Examples](#label-functions-set-catalog-integration-examples).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object |
| --- | --- |
| OWNERSHIP | Table whose catalog integration is being replaced. |
| USAGE | Current catalog integration. |
| USAGE | Target catalog integration. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- You can only replace the catalog integration for externally managed Iceberg tables in a standard Snowflake database.
  You can’t replace the catalog integration for Iceberg tables in a catalog-linked database or replace the catalog integration for any
  other type of Iceberg table.
- The type of the current catalog integration associated with the table restricts the types of catalog integrations that you can use as a
  replacement. The following table lists the supported transitions when you replace one type of catalog integration with another:

  | Current catalog integration type | New catalog integration type | Notes |
  | --- | --- | --- |
  | [AWS Glue](/sql-reference/sql/create-catalog-integration-glue) | [AWS Glue Iceberg REST](/sql-reference/sql/create-catalog-integration-rest) |  |
  | AWS Glue Iceberg REST | AWS Glue | Fall back to a catalog integration that uses an AWS Glue catalog source. |
  | [Iceberg REST](/sql-reference/sql/create-catalog-integration-rest) | Iceberg REST | Migrate the table to an alternative catalog integration. |
  | No other transition combinations are supported. |  |  |

  Expand

  Show lessSee more
- `table_name` and `new_catalog_integration_name` are string literals, so you must include the values in single quotes.
- Both the current and target catalog integrations must point to the same external catalog.
- Both the current and target catalog integrations can’t have credential vending enabled.

## Examples

Replace the AWS Glue catalog integration associated with an Iceberg table named `glue_table` with an AWS Glue
Iceberg REST catalog integration named `glue_rest_catalog_int`:

Copy code

```
SELECT SYSTEM$SET_CATALOG_INTEGRATION('glue_table', 'glue_rest_catalog_int');
```

Sample output:

Copy code

```
+------------------------------------------------------------------------------------------------------------------------------+
|                                                SYSTEM$SET_CATALOG_INTEGRATION                                                |
+------------------------------------------------------------------------------------------------------------------------------+
| Catalog integration for table GLUE_TABLE has been migrated from 'GLUE_CATALOG_INTEGRATION' to 'GLUE_REST_CATALOG_INT'        |
+------------------------------------------------------------------------------------------------------------------------------+
```

## Troubleshooting

If the function fails, it returns an error response. Common error messages include:

| Error Message | Situation and Solution |
| --- | --- |
| SYSTEM$SET\_CATALOG\_INTEGRATION does not support transitioning from catalog integration ‘[CURRENT\_CATALOG\_INTEGRATION]’ to ‘[TARGET\_CATALOG\_INTEGRATION]’ due to unsupported type combination | The current or target catalog integration provided doesn’t match the catalog integration types that are supported. For the supported types, see the [usage notes](#label-functions-set-catalog-integration-usage-notes). |
| SYSTEM$SET\_CATALOG\_INTEGRATION cannot transition from ‘[CURRENT\_CATALOG\_INTEGRATION]’ to ‘[TARGET\_CATALOG\_INTEGRATION]’ due to incompatible catalog integration configurations | The given catalog integrations are of the supported type but don’t align with one of the supported transition combinations. For the supported transition combinations, see the [usage notes](#label-functions-set-catalog-integration-usage-notes). |
| Currently doesn’t support performing transition when catalog integration ‘[CATALOG\_INTEGRATION]’ has credential vending enabled | The provided catalog integration has credential vending enabled. Provide a catalog integration with credential vending disabled and try again. |
| SYSTEM$SET\_CATALOG\_INTEGRATION can only be used on unmanaged Iceberg tables | The table provided isn’t an externally managed Iceberg table. Provide an externally managed Iceberg table and try again. |

Expand

Show lessSee more
