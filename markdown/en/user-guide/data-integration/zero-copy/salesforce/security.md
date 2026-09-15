# Salesforce Data Cloud Zerocopy Connector: Security and privileges

This topic describes the privileges required to create and manage a Zerocopy
Connector and the catalog-linked databases created from it.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| `CREATE ZEROCOPY CONNECTOR` | Schema | Required to create a Zerocopy Connector. By default, the schema owner has this privilege. |
| `OPERATE` | Zerocopy Connector | Required to retrieve the connector configuration using `SYSTEM$GET_ZEROCOPY_CONNECTOR_CONFIG` and to disconnect the connector (`ALTER ... DISCONNECT`). |
| `USAGE` | Zerocopy Connector | Required to create a catalog-linked database from the connector (also requires `CREATE DATABASE` on the account). |
| `MODIFY` | Zerocopy Connector | Required to set or unset properties such as `COMMENT`. |
| `MONITOR` | Zerocopy Connector | Any privilege on the connector (for example, `MONITOR`) is sufficient to describe the connector, show connectors, or list shares. |
| `OWNERSHIP` | Zerocopy Connector | Required to rename or drop the connector. |
| `CREATE DATABASE` | Account | Required to create a catalog-linked database from a Zerocopy Connector (also requires `USAGE` on the connector). |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Connector states

A Zerocopy Connector transitions through the following states. Understanding
the state is important because some operations are only permitted in specific
states.

| State | Description |
| --- | --- |
| `NEW` | Initial state after the connector is created. No connection has been attempted yet. |
| `CONNECTING` | A connection attempt is in progress. The connector enters this state after a Snowflake V2 Data Share Target is created in Salesforce Data Cloud. |
| `CONNECTED` | The connection is established. Catalog-linked databases can only be created when the connector is in this state. |
| `CONNECT_ERROR` | The connection attempt failed. The error message is persisted on the connector. You can retry the connection from this state. |
| `DISCONNECTING` | A disconnection is in progress. The connector enters this state immediately after `ALTER ... DISCONNECT` is issued. |
| `DISCONNECTED` | The connection has been dropped. You can reconnect from this state. |
| `DISCONNECT_ERROR` | The disconnection attempt failed. The error message is persisted on the connector. |
| `DELETED` | The connector has been dropped. This state is permanent — Zerocopy Connectors do not support `UNDROP`. |

Expand

Show lessSee more

### State transition rules

- The connector transitions to `CONNECTING` automatically when a Snowflake V2 Data Share Target is created in Salesforce Data Cloud.
- `ALTER ... DISCONNECT` is permitted when the connector is in `CONNECTED`
  or `DISCONNECT_ERROR` state.
- All catalog-linked databases created from the connector must be dropped before disconnecting.
- `DROP ZEROCOPY CONNECTOR` is permitted when the connector is in `NEW`,
  `CONNECT_ERROR`, `DISCONNECT_ERROR`, or `DISCONNECTED` state.
- Catalog-linked databases do not support `UNDROP`.
