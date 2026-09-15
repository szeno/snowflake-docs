# Set up the Salesforce Data Cloud Zerocopy Connector

This topic describes how to create the Zerocopy Connector for Salesforce Data Cloud on the Snowflake side and retrieve the Enrollment ID needed to authorize the connection.

Complete these steps first. Once you have the Enrollment ID, provide it to your Salesforce administrator to complete the Salesforce-side setup. See [Set up Salesforce Data Cloud for Zero-Copy](/user-guide/data-integration/zero-copy/salesforce/setup-salesforce).

For the privileges required for each operation, see [Security and privileges](/user-guide/data-integration/zero-copy/salesforce/security).

## Prerequisites

The role used to create the connector must have `CREATE ZEROCOPY CONNECTOR` on the target schema. By default, the owner role of a schema has this privilege.

## Create a database and schema

A Zerocopy Connector is a schema-level object. Before creating one, ensure
you have a target database and schema, or create new ones. For reference, see
[CREATE DATABASE](/sql-reference/sql/create-database) and [CREATE SCHEMA](/sql-reference/sql/create-schema).

Copy code

```
CREATE DATABASE IF NOT EXISTS my_db;

CREATE SCHEMA IF NOT EXISTS my_db.my_schema;
```

## Create a Zerocopy Connector

You can create the connector using the Snowsight UI or SQL.

### Using Snowsight

1. In Snowsight, navigate to **Ingestion** » **Zero-Copy**.
2. Select the **Overview** tab.
3. On the **Salesforce Data 360 Connect for Snowflake** card, click **Connect**.
4. In the **Connection details** panel:
   - **Connector name**: Enter a name, or use the auto-generated name (for example, `SALESFORCE_CONNECT_1785545041895`).
   - **Connector location**: Select the schema where the connector will be installed.
5. Click **Create connector**.

After creation, Snowsight displays an **Enrollment ID** in the **Establish connection to Salesforce** panel. Copy this value — you will provide it to your Salesforce administrator in the next step.

### Using SQL

Copy code

```
CREATE ZEROCOPY CONNECTOR IF NOT EXISTS my_db.my_schema.my_sfdc_connector
  PARTNER = SALESFORCE;
```

After creation, the connector is in `NEW` state. Retrieve the Enrollment ID using:

Copy code

```
SELECT SYSTEM$GET_ZEROCOPY_CONNECTOR_CONFIG('my_db.my_schema.my_sfdc_connector');
```

The output includes an `enrollment_code` value. Copy it and provide it to your Salesforce administrator.

## Provide the Enrollment ID to Salesforce

Share the Enrollment ID with your Salesforce administrator. They use it to create a **Data Share Target** in Salesforce Data Cloud, which establishes the authorized connection back to your Snowflake account. See [Set up Salesforce Data Cloud for Zero-Copy](/user-guide/data-integration/zero-copy/salesforce/setup-salesforce) for the Salesforce-side steps.

After the Salesforce administrator creates the Data Share Target using the Enrollment ID, the connector transitions from `NEW` to `CONNECTING` and then to `CONNECTED` automatically. No additional action is required on the Snowflake side to establish the connection.

Use `DESC ZEROCOPY CONNECTOR` to monitor progress while waiting:

Copy code

```
DESC ZEROCOPY CONNECTOR my_db.my_schema.my_sfdc_connector; -- check state
```

The connector is ready when `status` shows `CONNECTED`.

## Verify connector state

Use `DESCRIBE` to check the full details of a connector:

Copy code

```
DESC ZEROCOPY CONNECTOR my_db.my_schema.my_sfdc_connector;
```

### Output

| Column | Description |
| --- | --- |
| `name` | Name of the Zerocopy Connector. |
| `partner` | The data partner (`SALESFORCE`). |
| `config` | Configuration for the connector, including the Salesforce tenant endpoint and tenant ID. |
| `status` | Current connector state. See [Salesforce Data Cloud Zerocopy Connector: Security and privileges](/user-guide/data-integration/zero-copy/salesforce/security) for the full state machine. |
| `connection_error` | Error message if the connector is in `CONNECT_ERROR` or `DISCONNECT_ERROR` state; otherwise empty. |
| `catalog_linked_databases` | Mounted catalog-linked databases visible to the current role. |
| `database_name` | Database in which the connector resides. |
| `schema_name` | Schema in which the connector resides. |
| `owner` | Role that owns the connector. |
| `owner_role_type` | Type of the owner role. |
| `comment` | Optional comment set on the connector. |
| `created_on` | Timestamp when the connector was created. |
| `updated_on` | Timestamp when the connector was last updated. |

Expand

Show lessSee more

To list all connectors visible to the current role:

Copy code

```
SHOW ZEROCOPY CONNECTORS IN SCHEMA my_db.my_schema;

SHOW ZEROCOPY CONNECTORS IN DATABASE my_db;

SHOW ZEROCOPY CONNECTORS IN ACCOUNT;
```

## Set properties

You can set optional properties on a connector using `ALTER ... SET`:

Copy code

```
ALTER ZEROCOPY CONNECTOR IF EXISTS my_db.my_schema.my_sfdc_connector
  SET COMMENT = 'Salesforce Data Cloud connector for CRM data products';
```

To unset a property and restore its default value:

Copy code

```
ALTER ZEROCOPY CONNECTOR IF EXISTS my_db.my_schema.my_sfdc_connector
  UNSET COMMENT;
```

## Disconnect the connector

Note

All catalog-linked databases created from the connector must be
dropped before disconnecting. The connector must be in `CONNECTED` or
`DISCONNECT_ERROR` state.

Copy code

```
ALTER ZEROCOPY CONNECTOR IF EXISTS my_db.my_schema.my_sfdc_connector
  DISCONNECT;
```

The connector immediately enters `DISCONNECTING` state while the connection
is dropped asynchronously. When successful, it transitions to `DISCONNECTED`.

## Drop the connector

You can only drop a connector that is in `NEW`, `CONNECT_ERROR`,
`DISCONNECT_ERROR`, or `DISCONNECTED` state. Zerocopy Connectors do not support `UNDROP`.

Copy code

```
DROP ZEROCOPY CONNECTOR IF EXISTS my_db.my_schema.my_sfdc_connector;
```

## Next steps

Once the connector is in `CONNECTED` state, your Salesforce administrator can share data products. See [Set up Salesforce Data Cloud for Zero-Copy](/user-guide/data-integration/zero-copy/salesforce/setup-salesforce) to complete the Salesforce-side setup, then [Explore data products from Salesforce Data Cloud](/user-guide/data-integration/zero-copy/salesforce/explore-data-products) to list and query the shared data.
