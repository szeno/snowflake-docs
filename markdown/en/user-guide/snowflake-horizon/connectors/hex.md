# Hex

Horizon Catalog collects metadata, cells, and column-level lineage from Hex using a Hex workspace
API key. Complete the following steps to connect Hex to Horizon Catalog:

1. [Create an API key in Hex](#1-create-an-api-key-in-hex).
2. [Create the Hex connection](#2-create-the-hex-connection).
3. [Set up metadata access](#3-set-up-metadata-access).

Note

Horizon Catalog links Snowflake columns to the Hex cell that queried them, based on your Snowflake
query history or directly from cell SQL. Table-level lineage is always attributed to the Hex
project as a whole, not to individual cells.

## 1. Create an API key in Hex

1. Sign in to Hex and open **Settings** (bottom-left).
2. Under **Account**, select **API keys**.
3. Create a new **Workspace token**:
   - Enter a meaningful description.
   - Set the expiration (Snowflake recommends **No Expiry** so metadata sync doesn’t break when
     the token expires).
   - Under **API Scopes**, enable **Projects** > **Read access**.
   - Under **API Scopes**, enable **Cells** > **Read access**. Horizon Catalog uses this to ingest
     the individual cells in each project for column-level lineage.
   - Optional: under **API Scopes**, enable **Data connections** > **Read access**. Horizon
     Catalog uses this to detect which Snowflake connection your Hex cells query, so it can also
     derive lineage directly from cell SQL, covering cells that haven’t been run yet, which query
     history alone can’t see. Without this scope, lineage still works, but only for cells that have
     already been queried.
   - Optional: under **API Scopes**, enable **Users** > **Read access**. Horizon Catalog uses this
     to show the real name of each project’s owner and creator. Without this scope, Horizon
     Catalog shows their email address instead.
4. Select **Generate token** and copy the token. You’ll paste it into Horizon Catalog.

## 2. Create the Hex connection

In Snowflake, open **Catalog > Connections**, select **Hex**, and fill in the **Define
connection** step:

| Field | Value |
| --- | --- |
| **Display Name** | A name for the connection |
| **API Key** | The workspace token from Step 1 |
| **Hex URL** | Your Hex instance URL, made up of the base URL and your site ID (for example, `https://app.hex.tech/<site>`) |
| **Snowflake Database** | The Snowflake database where Horizon Catalog stores the connector metadata (default: `CONNECTORS`) |
| **Snowflake Schema** | The Snowflake schema where Horizon Catalog stores the connector metadata (default: `METADATA`) |

Expand

Show lessSee more

Metadata starts loading automatically for every collection in your Hex workspace. Initial
discovery can take up to 24 hours. When the sync completes, Hex projects, their cells, and lineage
appear in Horizon Catalog.

## Select collections to sync

Note

Horizon Catalog syncs every collection the first time it connects to your Hex workspace, because
the list of collections isn’t known until after that first sync.

To limit which collections Horizon Catalog keeps syncing, reconfigure the data source and open
**Select collections**. Deselecting a collection removes its projects from Horizon Catalog on the
next sync.

## 3. Set up metadata access

Other roles can’t see the metadata and lineage that this connector collects until you grant them
access. Grant `USAGE` on the connector, and on the database and schema that contain it, to each role
that needs to view the connector’s metadata and lineage:

Copy code

```
GRANT USAGE ON DATABASE CONNECTORS TO ROLE <role_name>;
GRANT USAGE ON SCHEMA CONNECTORS.METADATA TO ROLE <role_name>;
GRANT USAGE ON METADATA CONNECTOR CONNECTORS.METADATA.<connector_name> TO ROLE <role_name>;
```

If you stored the connector in a different database or schema, replace `CONNECTORS` and `METADATA`
with the actual database and schema names.

For more information about metadata access, see
[Metadata access control](/user-guide/snowflake-horizon/connectors/access-control).

## Connection security

All communication between Horizon Catalog and Hex uses HTTPS (TLS 1.2 or higher), and the Hex API
key is stored as an encrypted secret.

For more details, see [Security and data protection](/user-guide/snowflake-horizon/connectors/security).
