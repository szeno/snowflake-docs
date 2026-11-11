# SAP® BDC Connect for Snowflake Zerocopy Connector: Private connectivity

[Business Critical Feature](/user-guide/intro-editions)

This feature requires Business Critical (or higher).

To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

When a SAP® Business Data Cloud tenant requires it, a Zerocopy Connector reaches the tenant over AWS PrivateLink instead of the
tenant’s public endpoints. This topic describes when private connectivity is used, what it requires, and how to check its status.

Private connectivity applies to the connections that Snowflake makes to SAP® Business Data Cloud: reading data products, and
publishing Snowflake data to SAP® Business Data Cloud. Snowflake connects to private endpoints that SAP® provides for your
tenant. It’s available for Snowflake accounts on AWS, when the Snowflake account and
the SAP® Business Data Cloud tenant are in the same AWS region.

## How private connectivity works

Whether a tenant requires private connectivity is set on the SAP® side by your SAP® Business Data Cloud administrator. You don’t
set it in Snowflake.

When you run `ALTER ZEROCOPY CONNECTOR ... CONNECT`, Snowflake checks whether the tenant requires private connectivity:

- If the tenant doesn’t require private connectivity, the connector connects through the tenant’s public endpoints, as it does
  without this feature. You don’t need to do anything.
- If the tenant requires private connectivity, Snowflake creates the private endpoints the connector needs, and then connects the
  connector to the tenant through them.

Snowflake creates these endpoints in your account:

Control-plane endpoint
:   Carries the connector’s requests to SAP® Business Data Cloud: sign-in and credential requests, listing data products and tables,
    and publishing data. It doesn’t carry table data. Snowflake creates one for each tenant that you connect to.

Storage endpoint
:   Carries reads of table data from cloud storage. Snowflake creates one for your account’s AWS region, shared by all of the
    account’s connectors that read through it. It might already exist if you use outbound private connectivity for external stages
    or external volumes.

## Requirements

For a connector to a tenant that requires private connectivity, your Snowflake account must meet these requirements:

- The account is hosted on AWS.
- The tenant is in the same AWS region as the account.
- The account is Business Critical Edition or higher.
- The account isn’t a trial account.
- Outbound private connectivity is available for the account. For more information, see
  [Private connectivity for outbound network traffic](/user-guide/private-connectivity-outbound).
- Additional host names are enabled for private endpoints in the account. Most tenants need this because SAP® serves sign-in
  from a different host than the connector endpoint. To enable it, contact
  [Snowflake Support](/user-guide/contacting-support).

If the account doesn’t meet one of these requirements, the connection fails before Snowflake registers the connector with the
tenant. The connector goes to `CONNECT_ERROR` state, and `DESC ZEROCOPY CONNECTOR` shows the error in the `connection_error`
column. Fix the requirement, and then run `CONNECT` again.

## Costs and limits

The endpoints that Snowflake creates for a connector are outbound private connectivity endpoints, like the ones that you create
yourself.

You pay for each private connectivity endpoint along with total data processed. For pricing of these items, see the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

You can explore the cost of these items by filtering on the following service types when querying billing views in the ACCOUNT\_USAGE and ORGANIZATION\_USAGE schemas:

- OUTBOUND\_PRIVATELINK\_ENDPOINT
- OUTBOUND\_PRIVATELINK\_DATA\_PROCESSED

For example, you can query the [USAGE\_IN\_CURRENCY\_DAILY](/sql-reference/organization-usage/usage_in_currency_daily) view and filter on these service types.

Each endpoint counts toward the limit on private endpoints for your account, including endpoints removed in the last seven days.
For details, see [Scaling considerations](/user-guide/private-connectivity-outbound#label-private-connect-external-service-limits).

A connector that uses private connectivity needs one control-plane endpoint for each tenant, plus one storage endpoint for the
account, which might already exist for external stages or external volumes. At the default limit of five endpoints, an account
can connect at most four tenants, and fewer if other endpoints already use slots.

If creating an endpoint would exceed the limit, the connection fails before Snowflake registers the connector with the tenant. A
storage endpoint that Snowflake created during that attempt remains in your account. To raise the limit, contact
[Snowflake Support](/user-guide/contacting-support).

## Check private connectivity status

To check a connector, describe it:

Copy code

```
DESC ZEROCOPY CONNECTOR my_db.my_schema.my_sap_connector;
```

The `config` column of the output includes a `private_connectivity` object:

Copy code

```
{
  "private_connectivity": {
    "required": true,
    "status": "ENABLED",
    "control_plane_endpoint": {
      "id": "<control_plane_endpoint_id>",
      "state": "CREATED"
    },
    "storage_endpoint": {
      "id": "<storage_endpoint_id>",
      "state": "CREATED"
    }
  }
}
```

The `config` column of the `SHOW ZEROCOPY CONNECTORS` output includes the same object. The object has the following fields:

| Field | Description |
| --- | --- |
| `required` | Whether the tenant required private connectivity when the connector connected. Omitted if Snowflake has no record of it and no private endpoint is in use. |
| `status` | The state of private connectivity. See [Status values](#label-sap-bdc-private-connectivity-status). |
| `reason` | Why the status is `MISCONFIGURED`. Omitted for other statuses. See [Status values](#label-sap-bdc-private-connectivity-status). |
| `control_plane_endpoint` | The endpoint for the connector’s requests to SAP® Business Data Cloud, with its `id` and `state`. The `state` is omitted if the endpoint no longer exists. The whole field is omitted if the connector has no endpoint. |
| `storage_endpoint` | The endpoint for reads of table data, with its `id` and `state`. The `id` is omitted until the endpoint is in the `CREATED` state. The whole field is omitted if the connector doesn’t need one or none exists. |

Expand

Show lessSee more

## Status values

The `status` field has one of the following values:

| Status | Description |
| --- | --- |
| `ENABLED` | The tenant requires private connectivity, and Snowflake’s records show that both endpoints are in the `CREATED` state. |
| `NOT_REQUIRED` | The tenant doesn’t require private connectivity. The connector uses the tenant’s public endpoints. |
| `MISCONFIGURED` | The tenant requires private connectivity, but an endpoint is missing or can’t carry traffic. The `reason` field says which. |
| `UNKNOWN` | Snowflake has no record of whether the tenant requires private connectivity, and no private endpoint is in use. This is the case for a connector that hasn’t connected, is disconnected, or connected before Snowflake started recording the requirement. If the connector is disconnected, no action is needed. If it’s connected and its tenant requires private connectivity, disconnect it and connect it again so that Snowflake records the requirement and creates the endpoints. Until you do, the connector continues to use the tenant’s public endpoints. |

Expand

Show lessSee more

A `MISCONFIGURED` connector has one of the following reasons. To disconnect and reconnect a connector, see
[Disconnect and reconnect](#label-sap-bdc-private-connectivity-disconnect).

| Reason | Description | How to fix |
| --- | --- | --- |
| `CONTROL_PLANE_ENDPOINT_NOT_BOUND` | The connector connected without a control-plane endpoint. | Disconnect the connector, and then run `CONNECT` again. Snowflake creates the endpoint and binds it to the connector. |
| `CONTROL_PLANE_ENDPOINT_MISSING` | The control-plane endpoint that the connector uses no longer exists. | If you removed the endpoint in the last seven days, restore it. Otherwise, disconnect the connector, and then run `CONNECT` again to create a new endpoint. |
| `CONTROL_PLANE_ENDPOINT_NOT_CREATED` | The control-plane endpoint is in a state other than `CREATED`. | Check the endpoint’s state. If it’s pending, wait for it to reach `CREATED`. If it’s pending deletion, restore it. If it’s rejected or failed, contact [Snowflake Support](/user-guide/contacting-support). |
| `STORAGE_ENDPOINT_MISSING` | The account has no storage endpoint for the connector. | If you removed the endpoint in the last seven days, restore it. Otherwise, disconnect the connector, and then run `CONNECT` again to create a new endpoint. |
| `STORAGE_ENDPOINT_NOT_CREATED` | The storage endpoint is in a state other than `CREATED`. | Check the endpoint’s state. If it’s pending, wait for it to reach `CREATED`. If it’s pending deletion, restore it. If it’s rejected or failed, contact [Snowflake Support](/user-guide/contacting-support). |

Expand

Show lessSee more

To check an endpoint’s state, see [Manage private connectivity endpoints: AWS](/user-guide/private-manage-endpoints-aws). To restore an endpoint that you removed in the
last seven days, see [SYSTEM$RESTORE\_PRIVATELINK\_ENDPOINT](/sql-reference/functions/system_restore_privatelink_endpoint). Don’t remove an endpoint that a connector
uses. If you didn’t remove an endpoint, or you can’t restore it, contact [Snowflake Support](/user-guide/contacting-support).

## Disconnect and reconnect

When you disconnect a connector, Snowflake removes the control-plane endpoint that it created for the connector, unless another
connector in the account uses the endpoint. Snowflake doesn’t remove an endpoint that existed before the connector connected, and
it doesn’t remove the storage endpoint, which other features in your account can use. Before you disconnect a connector, you must
drop the catalog-linked databases created from it and disable share-back. For details, see
[Set Up SAP® BDC Connect for Snowflake Zerocopy Connector](/user-guide/data-integration/zero-copy/sap-sql/setup).

A removed endpoint still counts toward the endpoint limit for seven days. If you reconnect to the same tenant within those seven
days, the connection fails because the endpoint is still in the removed state, and the error message includes the command to
restore it. Restore the endpoint, and then run `CONNECT` again. For the restore steps, see
[SYSTEM$RESTORE\_PRIVATELINK\_ENDPOINT](/sql-reference/functions/system_restore_privatelink_endpoint).

After you restore an endpoint, Snowflake no longer removes it when you disconnect the connector. Remove it yourself when no
connector uses it. For the steps, see [Manage private connectivity endpoints: AWS](/user-guide/private-manage-endpoints-aws).
