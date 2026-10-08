# Set up the Workday Data Cloud Zerocopy Connector

This topic describes how to create a Zerocopy Connector for Workday Data Cloud and connect it to your Workday tenant.

The Workday connector authenticates outbound to your Workday tenant: you supply the tenant and credential values directly in the `CONNECT` statement.

For the privileges required for each operation, see [Security and privileges](/user-guide/data-integration/zero-copy/workday-data-cloud/security).

## Prerequisites

Before creating a Zerocopy Connector:

- Your Snowflake account must be enabled for the Workday connector. If the `CREATE ZEROCOPY CONNECTOR` command isn’t recognized, contact your Snowflake account team.
- The role used to create the connector must have `CREATE ZEROCOPY CONNECTOR` on the target schema. By default, the owner role of a schema has this privilege.
- Your Workday administrator must register an API client for integrations in your Workday tenant and supply the six values in the following table.

### Connection values from Workday

| Value | Description |
| --- | --- |
| `TENANT` | Your Workday tenant name. |
| `DOMAIN` | The Workday services host, used to obtain an access token. |
| `CATALOG_ENDPOINT` | The Workday Data Cloud catalog host. |
| `CLIENT_ID` | The API client identifier. |
| `CLIENT_SECRET` | The API client secret. Snowflake stores this value encrypted and never displays it. |
| `REFRESH_TOKEN` | The long-lived refresh token issued for the API client. Snowflake stores this value encrypted and never displays it. |

Expand

Show lessSee more

Important

Don’t set an expiry on the client secret or the refresh token. If either credential expires, the connector can no longer obtain an access token and queries against the mounted catalog fail.

`CLIENT_SECRET` and `REFRESH_TOKEN` are credentials. Snowflake stores them encrypted and never displays them again: they don’t appear in `DESCRIBE ZEROCOPY CONNECTOR` output, `SHOW ZEROCOPY CONNECTORS` output, or query history. For details, see [Security and privileges](/user-guide/data-integration/zero-copy/workday-data-cloud/security).

## Create a database and schema

A Zerocopy Connector is a schema-level object. Before creating one, ensure you have a target database and schema, or create new ones. For reference, see [CREATE DATABASE](/sql-reference/sql/create-database) and [CREATE SCHEMA](/sql-reference/sql/create-schema).

Copy code

```
CREATE DATABASE IF NOT EXISTS my_db;

CREATE SCHEMA IF NOT EXISTS my_db.my_schema;
```

## Create a Zerocopy Connector

You can create the connector using the Snowsight UI or SQL.

### Using Snowsight

1. Sign in to Snowsight.
2. In the navigation menu, select **Ingestion** » **Zero-Copy**.
3. On the **Workday** card, select **Connect**.
4. Enter a **Connector name**, then select the database and schema in which to create the connector.
5. Select **Create connector**.

Snowsight then prompts you for the connection values described in [Connection values from Workday](#label-workday-connection-values). To continue in the UI, see [Connect to your Workday tenant using Snowsight](#label-workday-connect-snowsight).

### Using SQL

Always use a fully qualified name (`<db>.<schema>.<connector>`). Partially qualified and plain names resolve against the current session context, so a later change to the session database or schema can break name resolution when you create the catalog-linked database.

Copy code

```
CREATE [ OR REPLACE ] ZEROCOPY CONNECTOR [ IF NOT EXISTS ] <name>
  PARTNER = WORKDAY;
```

Copy code

```
CREATE ZEROCOPY CONNECTOR IF NOT EXISTS my_db.my_schema.my_workday_connector
  PARTNER = WORKDAY;
```

After creation, the connector is in `NEW` state and holds no credentials. No connection is attempted until you run `ALTER ... CONNECT`.

## Connect to your Workday tenant

Note

The connector must be in `NEW`, `CONNECT_ERROR`, or `DISCONNECTED` state. See [Connector states](/user-guide/data-integration/zero-copy/workday-data-cloud/security#label-workday-connector-states).

### Using SQL

Replace each placeholder with the value supplied by your Workday administrator.

Copy code

```
ALTER ZEROCOPY CONNECTOR IF EXISTS my_db.my_schema.my_workday_connector
  CONNECT WITH CONFIG = (
    TENANT           = '<tenant>',
    DOMAIN           = '<workday_url>',
    CATALOG_ENDPOINT = '<workday_catalog_url>',
    CLIENT_ID        = '<client_id>',
    CLIENT_SECRET    = '<client_secret>',
    REFRESH_TOKEN    = '<refresh_token>'
  );
```

The statement returns as soon as the credentials are stored. Snowflake then contacts Workday in the background to verify them, so the connector enters `CONNECTING` state rather than `CONNECTED`. Poll with `DESCRIBE` until the status settles:

Copy code

```
DESCRIBE ZEROCOPY CONNECTOR my_db.my_schema.my_workday_connector;
```

| `status` | Meaning |
| --- | --- |
| `CONNECTING` | Verification is in progress. Run `DESCRIBE` again. |
| `CONNECTED` | The connector is ready to use. You can now mount the catalog. |
| `CONNECT_ERROR` | Verification failed. See the `connection_error` column for the reason. |

Expand

Show lessSee more

To fix a failed connection, correct the values and reissue the same `CONNECT` statement. The connector accepts a new `CONNECT` from `CONNECT_ERROR` state, so you don’t have to drop and recreate it.

### Using Snowsight

1. In the connection panel, enter the tenant, host, and credential values described in [Connection values from Workday](#label-workday-connection-values).
2. Select **Connect**.

Snowsight redirects to the connector page, where the status is shown while Snowflake verifies the credentials. When the connector reaches `CONNECTED`, mount the catalog as described in [Explore and query Workday Data Cloud data](/user-guide/data-integration/zero-copy/workday-data-cloud/explore-data).

To review the stored configuration later, open the connector page and select the **Connector details** tab. The tab shows the non-secret options only.

## Verify connector state

Use `DESCRIBE` to check the full details of a connector:

Copy code

```
DESCRIBE ZEROCOPY CONNECTOR my_db.my_schema.my_workday_connector;
```

### Output

| Column | Description |
| --- | --- |
| `name` | Name of the Zerocopy Connector. |
| `partner` | The data partner (`WORKDAY`). |
| `config` | Configuration for the connector. For Workday, this contains the four non-secret options only: `TENANT`, `DOMAIN`, `CATALOG_ENDPOINT`, and `CLIENT_ID`. Use this column to confirm what was stored without exposing the credentials. |
| `status` | Current connector state. See [Connector states](/user-guide/data-integration/zero-copy/workday-data-cloud/security#label-workday-connector-states) for the full state machine. |
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

## Refresh intervals

The connector runs two independent background intervals, one for table metadata and one for catalog discovery. The values in the following table are the ones Snowflake recommends for Workday Data Cloud.

| Interval | Value | What it controls |
| --- | --- | --- |
| Auto refresh interval | 4 hours | How often the connector refreshes the metadata of the mounted Workday tables. Snowflake manages this interval, so there is nothing for you to set. |
| `SYNC_INTERVAL_SECONDS` | 86400 seconds (1 day) | How often Snowflake discovers structural changes in the Workday catalog, such as a new namespace or table. You set this value on the catalog-linked database when you mount the catalog. |

Expand

Show lessSee more

Neither interval affects the freshness of your query results. Snowflake contacts Workday each time you run a `SELECT` against a mounted table, so every query is served fresh data straight from your Workday tenant. Workday remains the system of record.

For how to set the sync interval, see [Sync interval](/user-guide/data-integration/zero-copy/workday-data-cloud/explore-data#label-workday-sync-interval).

## Remove the integration

Drop the objects in the following order. A connector that still has a catalog-linked database won’t disconnect, and a connected connector won’t drop.

### Disconnect the connector

Note

All catalog-linked databases created from the connector must be dropped before disconnecting. The connector must be in `CONNECTED` or `DISCONNECT_ERROR` state.

Copy code

```
-- 1. Drop the catalog-linked database first
DROP DATABASE IF EXISTS my_workday_db;

-- 2. Disconnect the connector
ALTER ZEROCOPY CONNECTOR IF EXISTS my_db.my_schema.my_workday_connector
  DISCONNECT;
```

The connector immediately enters `DISCONNECTING` state while the connection is dropped asynchronously. Poll until the status is `DISCONNECTED`:

Copy code

```
DESCRIBE ZEROCOPY CONNECTOR my_db.my_schema.my_workday_connector;
```

A disconnected connector can be reconnected. To reconnect, reissue the `CONNECT` statement with the values from your Workday administrator.

### Drop the connector

You can only drop a connector that is in `NEW`, `CONNECT_ERROR`, `DISCONNECT_ERROR`, or `DISCONNECTED` state. Zerocopy Connectors don’t support `UNDROP`.

Copy code

```
DROP ZEROCOPY CONNECTOR IF EXISTS my_db.my_schema.my_workday_connector;
```

## Next steps

When the connector is in `CONNECTED` state, mount the Workday Data Cloud catalog as a catalog-linked database and query the tables. See [Explore and query Workday Data Cloud data](/user-guide/data-integration/zero-copy/workday-data-cloud/explore-data).
