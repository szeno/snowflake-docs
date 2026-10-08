# Workday Data Cloud Zerocopy Connector: Security and privileges

This topic describes the privileges required to create and manage a Zerocopy Connector for Workday Data Cloud, how Snowflake protects the Workday credentials, and the states a connector moves through.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| `CREATE ZEROCOPY CONNECTOR` | Schema | Required to create a Zerocopy Connector. By default, the schema owner has this privilege. |
| `OPERATE` | Zerocopy Connector | Required to connect the connector to a Workday tenant (`ALTER ... CONNECT`) and to disconnect it (`ALTER ... DISCONNECT`). |
| `USAGE` | Zerocopy Connector | Required to create a catalog-linked database from the connector (also requires `CREATE DATABASE` on the account). |
| `MODIFY` | Zerocopy Connector | Required to set or unset properties such as `COMMENT`. |
| `MONITOR` | Zerocopy Connector | Any privilege on the connector (for example, `MONITOR`) is sufficient to describe the connector or show connectors. |
| `OWNERSHIP` | Zerocopy Connector | Required to rename or drop the connector. |
| `CREATE DATABASE` | Account | Required to create a catalog-linked database from a Zerocopy Connector (also requires `USAGE` on the connector). |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Credential handling

The `CONNECT` statement takes six values from your Workday tenant. Snowflake treats two of them as credentials:

- `CLIENT_SECRET`
- `REFRESH_TOKEN`

Snowflake stores both encrypted and never displays them again. They don’t appear in the `config` column of `DESCRIBE ZEROCOPY CONNECTOR`, in `SHOW ZEROCOPY CONNECTORS` output, or in query history. The `config` column returns the four non-secret options only (`TENANT`, `DOMAIN`, `CATALOG_ENDPOINT`, and `CLIENT_ID`), which is how you confirm what was stored without exposing the credentials.

Because the credentials can’t be read back, there is no way to recover them from Snowflake. Keep them in your own secret store if you need them again, or have your Workday administrator reissue them.

Important

Don’t set an expiry on the client secret or the refresh token. Snowflake uses the refresh token to obtain access tokens for the lifetime of the connection. If either credential expires, the connector can no longer authenticate and queries against the mounted catalog fail until you reissue the `CONNECT` statement with new values.

## Read-only access

Catalog-linked databases created from a Workday connector are read-only. `INSERT`, `UPDATE`, `DELETE`, and DDL statements against the mounted tables are rejected. Workday remains the system of record, so all writes happen in Workday.

## Connector states

A Zerocopy Connector transitions through the following states. Understanding the state is important because some operations are only permitted in specific states.

| State | Description |
| --- | --- |
| `NEW` | Initial state after the connector is created. The connector holds no credentials and no connection has been attempted. |
| `CONNECTING` | The credentials are stored and Snowflake is verifying them against the Workday tenant in the background. The connector enters this state as soon as `ALTER ... CONNECT` returns. |
| `CONNECTED` | The credentials were verified and the connection is established. Catalog-linked databases can only be created when the connector is in this state. |
| `CONNECT_ERROR` | Verification failed. The error message is persisted in the `connection_error` column. You can retry by reissuing `ALTER ... CONNECT` with corrected values from this state. |
| `DISCONNECTING` | A disconnection is in progress. The connector enters this state immediately after `ALTER ... DISCONNECT` is issued. |
| `DISCONNECTED` | The connection has been dropped. You can reconnect from this state. |
| `DISCONNECT_ERROR` | The disconnection attempt failed. The error message is persisted in the `connection_error` column. |
| `DELETED` | The connector has been dropped. This state is permanent: Zerocopy Connectors don’t support `UNDROP`. |

Expand

Show lessSee more

### State transition rules

- `ALTER ... CONNECT` is permitted when the connector is in `NEW`, `CONNECT_ERROR`, or `DISCONNECTED` state.
- The connector transitions to `CONNECTING` as soon as the credentials are stored, not when Workday confirms them. Poll with `DESCRIBE ZEROCOPY CONNECTOR` until the status settles on `CONNECTED` or `CONNECT_ERROR`.
- `ALTER ... DISCONNECT` is permitted when the connector is in `CONNECTED` or `DISCONNECT_ERROR` state.
- All catalog-linked databases created from the connector must be dropped before disconnecting.
- `DROP ZEROCOPY CONNECTOR` is permitted when the connector is in `NEW`, `CONNECT_ERROR`, `DISCONNECT_ERROR`, or `DISCONNECTED` state.
- Catalog-linked databases don’t support `UNDROP`.
