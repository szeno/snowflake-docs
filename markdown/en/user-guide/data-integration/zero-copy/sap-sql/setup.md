# Set up SAP® BDC Connect for Snowflake Zerocopy Connector

Note

The [`manage-zerocopy-sapbdc`](/user-guide/cortex-code/bundled-skills#label-bundled-skill-manage-zerocopy-sapbdc) skill manages the end-to-end lifecycle of the SAP and Snowflake Zero-Copy Integration and connector — creating connectors, consuming data products from SAP® BDC, publishing Snowflake data to SAP® BDC, analyzing shared data, and troubleshooting issues, all through a conversational, step-by-step workflow. This skill is now bundled with Cortex Code (CoCo), and you can use it to automate the steps in this topic.

Note

The Zerocopy Connector is subject to the [SAP® BDC Connect for Snowflake Terms](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/sap-bdc-connect-snowflake/).

The steps to share Data Products from SAP® BDC to SAP® Snowflake accounts and existing Snowflake
accounts that use the SAP® BDC Connect for Snowflake are exactly the same.

This topic describes how to create and manage a Zerocopy Connector for
SAP® BDC Connect for Snowflake on the Snowflake side. For the SAP® side setup, see
[SAP® Snowflake](/user-guide/data-integration/zero-copy/sap-sql/setup-sap-snowflake) or
[SAP® BDC Connect for Snowflake](/user-guide/data-integration/zero-copy/sap-sql/setup-sap-bdc).

For the privileges required for each operation, see [SAP® BDC Connect for Snowflake Zerocopy Connector — Security and Privileges](/user-guide/data-integration/zero-copy/sap-sql/security).

## Prerequisites

Before creating a Zerocopy Connector:

- An `ORGADMIN` must accept the SAP® BDC Connect for Snowflake Terms.
  This only needs to be done once per Snowflake organization. Terms of Service
  cannot be self-revoked — contact Snowflake support and legal to revoke them.

  To accept the SAP® BDC Connect for Snowflake Terms in Snowsight:

  1. Sign in to Snowflake as a user with the `ORGADMIN` role.
  2. In the navigation menu, select **Admin** » **Terms**.
  3. In the **Snowflake Marketplace** section, next to
     **SAP® BDC Connect for Snowflake Terms**, select **Review**.
  4. Select **Acknowledge & Continue**.
- Complete the SAP® side setup described in
  [SAP® Snowflake](/user-guide/data-integration/zero-copy/sap-sql/setup-sap-snowflake) or
  [SAP® BDC Connect for Snowflake](/user-guide/data-integration/zero-copy/sap-sql/setup-sap-bdc).
- The role used to create the connector must have `CREATE ZEROCOPY CONNECTOR`
  on the target schema. By default, the owner role of a schema has this privilege.

## Create a database and schema

A Zerocopy Connector is a schema-level object. Before creating one, ensure
you have a target database and schema, or create new ones. For reference, see
[CREATE DATABASE](/sql-reference/sql/create-database) and
[CREATE SCHEMA](/sql-reference/sql/create-schema).

Copy code

```
CREATE DATABASE IF NOT EXISTS my_db;

CREATE SCHEMA IF NOT EXISTS my_db.my_schema;
```

## Create a Zerocopy Connector

A Zerocopy Connector is a schema-level object. You can specify a fully qualified
name (`<db>.<schema>.<connector>`), a partially qualified name, or a plain
name when the database and schema are set in the current session context.

Copy code

```
CREATE [ OR REPLACE ] ZEROCOPY CONNECTOR [ IF NOT EXISTS ] <name>
  PARTNER = SAP_BDC;
```

Copy code

```
CREATE ZEROCOPY CONNECTOR IF NOT EXISTS my_db.my_schema.my_sap_connector
  PARTNER = SAP_BDC;
```

After creation, the connector is in `NEW` state. No connection is established
until you run `ALTER ... CONNECT`.

## Enroll with SAP® BDC

Note

The connector must be in `NEW`, `CONNECT_ERROR`, or `DISCONNECTED`
state. See  for details.

Copy code

```
ALTER ZEROCOPY CONNECTOR IF EXISTS my_db.my_schema.my_sap_connector
  CONNECT WITH CONFIG = (
    INVITATION_LINK = '<Invitation Link from SAP BDC>'
  );
```

The connector immediately enters `CONNECTING` state while the connection is
established asynchronously. Use `DESC ZEROCOPY CONNECTOR` to check the
current state.

### Verify connector state

Use `DESCRIBE` to check the current state of a connector:

Copy code

```
DESC ZEROCOPY CONNECTOR my_db.my_schema.my_sap_connector;
```

#### Output

| Column | Description |
| --- | --- |
| `name` | Name of the Zerocopy Connector. |
| `partner` | The data partner (for example, `SAP_BDC`). |
| `config` | The configuration of the data partner. For SAP® BDC, this contains the SAP® BDC Connector Endpoint. |
| `status` | Current connector state. See . |
| `connection_error` | Error message if the connector is in `CONNECT_ERROR` or `DISCONNECT_ERROR` state; otherwise empty. |
| `catalog_linked_databases` | Mounted catalog-linked databases that are visible to the current role. |
| `share_back` | Whether sharing data from Snowflake to SAP® BDC is enabled for this connector. |
| `shares` | Snowflake data shares that are associated with this connector. |
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
-- Set a comment
ALTER ZEROCOPY CONNECTOR IF EXISTS my_db.my_schema.my_sap_connector
  SET COMMENT = 'SAP BDC connector for sales data products';

-- Enabling share back allows publishing data from Snowflake to SAP BDC
ALTER ZEROCOPY CONNECTOR IF EXISTS my_db.my_schema.my_sap_connector
  SET SHARE_BACK = TRUE;
```

To unset a property and restore its default value:

Copy code

```
ALTER ZEROCOPY CONNECTOR IF EXISTS my_db.my_schema.my_sap_connector
  UNSET COMMENT;

ALTER ZEROCOPY CONNECTOR IF EXISTS my_db.my_schema.my_sap_connector
  UNSET SHARE_BACK;
```

## Disconnect the connector

Note

All catalog-linked databases created from the connector must be
dropped before disconnecting. Share-back must be disabled before
disconnecting. The connector must be in `CONNECTED` or
`DISCONNECT_ERROR` state.

Copy code

```
ALTER ZEROCOPY CONNECTOR IF EXISTS my_db.my_schema.my_sap_connector
  DISCONNECT;
```

The connector immediately enters `DISCONNECTING` state while the connection
is dropped asynchronously. When successful, it transitions to `DISCONNECTED`.

## Drop the connector

You can only drop a connector that is in `NEW`, `CONNECT_ERROR`,
`DISCONNECT_ERROR`, or `DISCONNECTED` state. Zerocopy Connectors do not support `UNDROP`.

Copy code

```
DROP ZEROCOPY CONNECTOR IF EXISTS my_db.my_schema.my_sap_connector;
```

## Next steps

Once the connector is in `CONNECTED` state, you can:

- List available SAP® data products and create catalog-linked databases.
  See [Explore Data Products from SAP® BDC Connect for Snowflake](/user-guide/data-integration/zero-copy/sap-sql/explore-data-products).
- Publish Snowflake data back to SAP® BDC. See [Publish Data from Snowflake to SAP® BDC Connect for Snowflake](/user-guide/data-integration/zero-copy/sap-sql/publish-data).
