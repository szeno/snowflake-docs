# Publish data from Snowflake to SAP® BDC Connect for Snowflake

Note

The [`manage-zerocopy-sapbdc`](/user-guide/cortex-code/bundled-skills#label-bundled-skill-manage-zerocopy-sapbdc) skill manages the end-to-end lifecycle of the SAP and Snowflake Zero-Copy Integration and connector: creating connectors, consuming data products from SAP® BDC, publishing Snowflake data to SAP® BDC, analyzing shared data, and troubleshooting issues, all through a conversational, step-by-step workflow. This skill is now bundled with Cortex Code (CoCo), and you can use it to automate the steps in this topic.

This topic describes how to publish Snowflake data back to SAP® BDC Connect for Snowflake by
creating a share, granting access to databases, schemas, and tables, and
associating the share with a Zerocopy Connector.

The connector must be in `CONNECTED` state and have `SHARE_BACK` enabled
before associating a share. See [Set Up SAP® BDC Connect for Snowflake Zerocopy Connector](/user-guide/data-integration/zero-copy/sap-sql/setup) for details.

## Enable share back

Before publishing data to SAP® BDC Connect for Snowflake, enable share back on the connector:

Copy code

```
ALTER ZEROCOPY CONNECTOR IF EXISTS my_db.my_schema.my_sap_connector
  SET SHARE_BACK = TRUE;
```

Note

The role used to create the share must have the `CREATE SHARE` privilege
on the account. For the full list of required privileges, see
[SAP® BDC Connect for Snowflake Zerocopy Connector — Security and Privileges](/user-guide/data-integration/zero-copy/sap-sql/security).

## Grant access to Snowflake objects

To publish Snowflake data to SAP® BDC Connect for Snowflake, you first create a Snowflake share and
grant access to the databases, schemas, and tables you want to publish. For
more information about creating and managing shares, see
[CREATE SHARE](/sql-reference/sql/create-share).

Note

- The tables must be Iceberg V3 tables. When you create a table, set
  `ICEBERG_VERSION = 3`, or set `ICEBERG_VERSION_DEFAULT = 3` at the database
  or schema level. For more information, see [ICEBERG\_VERSION](/sql-reference/parameters#label-iceberg-version) and
  [ICEBERG\_VERSION\_DEFAULT](/sql-reference/parameters#label-iceberg-version-default).
- The tables must use Snowflake as the Iceberg catalog
  ([Snowflake-managed Iceberg tables](/user-guide/tables-iceberg#label-tables-iceberg-snowflake-as-catalog)).
  When you create a table, set `CATALOG = 'SNOWFLAKE'`. For more information,
  see [CREATE ICEBERG TABLE (Snowflake as the Iceberg catalog)](/sql-reference/sql/create-iceberg-table-snowflake).
- The tables must use Snowflake storage, which is the default when you use
  Snowflake as the catalog. For more information, see
  [Snowflake storage for Apache Iceberg™ tables](/user-guide/tables-iceberg-internal-storage).
- The tables must have copy-on-write enabled. When you create a table, set
  `ICEBERG_MERGE_ON_READ_BEHAVIOR = 'DISABLED'`. For more information, see
  [Use row-level deletes](/user-guide/tables-iceberg-manage#label-tables-iceberg-row-level-deletes).
- The tables must use a compatible storage serialization policy so that
  SAP® BDC Connect for Snowflake can consume the published data. When you create a table, set
  `STORAGE_SERIALIZATION_POLICY = 'COMPATIBLE'`. For more information, see
  [STORAGE\_SERIALIZATION\_POLICY](/sql-reference/parameters#label-storage-serialization-policy).
- Each shared data product should map to a single dedicated database. For
  more information about direct shares, see [About Secure Data Sharing](/user-guide/data-sharing-intro).

Alternatively, you can set these properties at the database or schema level so
that all tables automatically inherit them.

Snowflake recommends setting the required Iceberg configuration at the
database level so that all tables in the database automatically inherit the
correct settings. Use [CREATE DATABASE](/sql-reference/sql/create-database) for a new database or
[ALTER DATABASE](/sql-reference/sql/alter-database) to update an existing one:

Copy code

```
-- New database
CREATE DATABASE my_publish_db
  ICEBERG_VERSION_DEFAULT = 3
  CATALOG = 'SNOWFLAKE'
  ICEBERG_MERGE_ON_READ_BEHAVIOR = 'DISABLED'
  STORAGE_SERIALIZATION_POLICY = 'COMPATIBLE';

-- Existing database
ALTER DATABASE my_publish_db SET
  ICEBERG_VERSION_DEFAULT = 3
  CATALOG = 'SNOWFLAKE'
  ICEBERG_MERGE_ON_READ_BEHAVIOR = 'DISABLED'
  STORAGE_SERIALIZATION_POLICY = 'COMPATIBLE';
```

If you prefer to set these properties at the table level instead, specify
them explicitly when creating each table:

Copy code

```
CREATE ICEBERG TABLE my_publish_db.my_schema.my_table (
  id STRING PRIMARY KEY,
  name STRING,
  value NUMBER(38,0)
)
  ICEBERG_VERSION = 3
  CATALOG = 'SNOWFLAKE'
  ICEBERG_MERGE_ON_READ_BEHAVIOR = 'DISABLED'
  STORAGE_SERIALIZATION_POLICY = 'COMPATIBLE';
```

Note

You must define a primary key on each Iceberg table that you publish to SAP® BDC Connect for Snowflake. In the preceding example, `id` is the primary key. Mark the same column as the key (`"key": true`) in the CSN document when you publish the data product.

### Create a share

To create a share, the role must have the `CREATE SHARE` privilege on the
account. For the full list of required privileges, see [SAP® BDC Connect for Snowflake Zerocopy Connector — Security and Privileges](/user-guide/data-integration/zero-copy/sap-sql/security).

Create a share using [CREATE SHARE](/sql-reference/sql/create-share):

Copy code

```
CREATE SHARE IF NOT EXISTS my_share;
```

### Grant access to the share

Grant `USAGE` on the database:

Copy code

```
GRANT USAGE ON DATABASE my_publish_db TO SHARE my_share;
```

Grant `USAGE` on the schema:

Copy code

```
GRANT USAGE ON SCHEMA my_publish_db.my_schema TO SHARE my_share;
```

Grant `SELECT` on a specific table:

Copy code

```
GRANT SELECT ON TABLE my_publish_db.my_schema.my_table TO SHARE my_share;
```

### Associate the share with the connector

After granting access, associate the share with the Zerocopy Connector:

Copy code

```
ALTER ZEROCOPY CONNECTOR my_db.my_schema.my_sap_connector
  ADD SHARE my_share;
```

To view the shares associated with a Zerocopy Connector, use
`DESC ZEROCOPY CONNECTOR`:

Copy code

```
DESC ZEROCOPY CONNECTOR my_db.my_schema.my_sap_connector;
```

## Revoke access

To disassociate a share from the Zerocopy Connector:

Copy code

```
ALTER ZEROCOPY CONNECTOR my_db.my_schema.my_sap_connector
  REMOVE SHARE my_share;
```

To revoke access to a previously granted object from the share:

Copy code

```
REVOKE USAGE ON DATABASE my_publish_db FROM SHARE my_share;

REVOKE USAGE ON SCHEMA my_publish_db.my_schema FROM SHARE my_share;

REVOKE SELECT ON TABLE my_publish_db.my_schema.my_table FROM SHARE my_share;
```

## Publish a data product to SAP® BDC Connect for Snowflake

After granting access to Snowflake objects, publish the data product to
SAP® BDC by calling the `SYSTEM$SAP_PUBLISH_DATA_PRODUCT` function. This
makes the data product discoverable and accessible from the SAP® BDC side.

Note

The `OPERATE` privilege on the connector is required to call
`SYSTEM$SAP_PUBLISH_DATA_PRODUCT`.

Copy code

```
SELECT SYSTEM$SAP_PUBLISH_DATA_PRODUCT(
  '<connector_name>',
  '<snowflake_share_name>',
  '<open_resource_discovery_metadata>',
  '<csn_document_json>'
);
```

For example:

Copy code

```
SELECT SYSTEM$SAP_PUBLISH_DATA_PRODUCT(
  'my_db.my_schema.my_sap_connector',
  'my_share',
  '{
    "title": "Airline Data Product",
    "shortDescription": "Airline dimension data from Snowflake.",
    "description": "Contains airline identifiers and attributes published from Snowflake to SAP BDC."
  }',
  '{
    "csnInteropEffective": "1.0",
    "$version": "2.0",
    "i18n": {},
    "meta": {
      "creator": "Snowflake CSN Interop Generator - Minimal",
      "flavor": "inferred"
    },
    "definitions": {
      "MY_SCHEMA": { "kind": "context" },
      "MY_SCHEMA.MY_TABLE": {
        "kind": "entity",
        "elements": {
          "ID": {
            "type": "cds.String",
            "key": true,
            "notNull": true
          },
          "NAME": {
            "type": "cds.String"
          },
          "VALUE": {
            "type": "cds.Decimal",
            "precision": 38,
            "scale": 0
          }
        }
      }
    }
  }'
);
```

| Parameter | Description |
| --- | --- |
| `connector_name` | Fully qualified name of the Zerocopy Connector (for example, `my_db.my_schema.my_sap_connector`). |
| `snowflake_share_name` | Name of the Snowflake share, also the name of the share on the SAP® BDC side. |
| `open_resource_discovery_metadata` | A JSON object describing the data product in SAP® BDC. Contains the following fields:   - `title`: Display name of the data product. - `shortDescription`: Brief summary of the data product. - `description`: Full description of the data product. |
| `csn_document_json` | The SAP® Core Schema Notation (CSN) JSON payload describing the structure of the data product. Provided by the caller. |

Expand

Show lessSee more

Note

If the function fails to resolve `connector_name` or
`snowflake_share_name`, verify that the names use the correct case.
Snowflake identifiers are case-sensitive when quoted. For more information,
see [Identifier requirements](/sql-reference/identifiers-syntax).
