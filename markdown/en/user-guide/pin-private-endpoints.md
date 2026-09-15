# Pinning private connectivity endpoints for inbound traffic

[Business Critical Feature](/user-guide/intro-editions)

This feature requires Business Critical (or higher).

To inquire about upgrading, contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

For Snowflake accounts on Amazon Web Services (AWS) and Microsoft Azure (Azure), you can pin (specify, register, and map) private connectivity endpoints to your
account. By pinning private endpoints to your account, Snowflake ensures that the inbound traffic originating from the pinned endpoints
only goes to the account that pinned them. Snowflake recommends using pinned endpoints, network policies, and network rules to harden your
security posture by reducing the network attack surface to your Snowflake account.

Tip

Pinning allows only authorized private endpoint(s) to be used to send traffic from the customer network to a specific
Snowflake account. If you want to restrict inbound access to Snowflake accounts from specific lists of IPs and VPCE IDs/LinkIDs, use
[network policies](/user-guide/network-policies) and [network rules](/user-guide/network-rules).

Snowflake enforces a private endpoint pinning check at the point of ingress for every request received over private connectivity.
This check compares two key pieces of information:

- The endpoint ID provided in the request header.
- The account that pinned the endpoint, as recorded in Snowflake’s metadata.

If these match — in other words, if the request originates from the account that registered the endpoint — then Snowflake allows the
connection. Otherwise, Snowflake blocks the connection.

For example:

![Checking authorized access for inbound traffic through pinned private connectivity endpoints](/static/images/screens/pinning_privatelink_endpoints_inbound_diag.png)

| Pinned private endpoint | Snowflake account that pinned private endpoint | Request’s target Snowflake account | Snowflake pinning check decision |
| --- | --- | --- | --- |
| PE1 | A1 | A1 | ALLOW |
| PE1 | A1 | A2 | DENY |
| PE2 | A2 | A1 | DENY |
| PE2 | A2 | A2 | ALLOW |

Expand

Show lessSee more

## Prerequisites

Before pinning a private endpoint, you must:

- Configure a private link for your Snowflake account on AWS or Azure.
- Limit the scope of the access token you use to register an endpoint with your Snowflake account.

For more information about configuring private links, see [AWS PrivateLink](/user-guide/admin-security-privatelink) or
[Azure Private Link](/user-guide/privatelink-azure).

Important

Before you pin a private endpoint, when [Configuring private connectivity for Snowsight](/user-guide/ui-snowsight-gs#label-ui-snowsight-config-private-connectivity), ensure that the endpoint uses a *regionless*
Snowsight privatelink URL for all your accounts. A regional Snowsight privatelink URL will not connect to a pinned private endpoint.

## Manage enforcement with the delay time argument

After configuring your private links, you call the [SYSTEM$REGISTER\_PRIVATELINK\_ENDPOINT](/sql-reference/functions/system_register_privatelink_endpoint) system function to
register a private connectivity endpoint with your Snowflake account. In that function call, you can optionally specify a delay time.
The delay time is the number of minutes to wait before enforcing the private endpoint registration. The delay time value helps prevent you
from accidentally blocking yourself from accessing Snowflake when you register a new private endpoint. The maximum delay time is 1440
minutes (24 hours) and the default value is 60 minutes.

The private endpoint that you register for your Snowflake account can also be registered for other Snowflake accounts. For example, you
might have three Snowflake accounts and you want to ensure that the connection to each Snowflake account only goes through one registered
private endpoint. By setting the delay time argument to 60 minutes, you allow for sufficient time to register the private connectivity
endpoint with each Snowflake account.

However, when you register a private connectivity endpoint and specify a delay time, you must be mindful of the local timestamp of
the first account in which you call the system function. The enforcement time is based on the local timestamp of the first account
when you call the system function plus any delay time that you specify, relative to a specific private connectivity endpoint.

For example, consider pinning a single private connectivity endpoint with three accounts in the same time zone:

- If you call the system function in `account1` at 10:00 AM and specify a delay time of 60 minutes, the enforcement time is 11:00 AM.
- If you call the system function in `account2` at 10:30 AM, the enforcement time is 11:00 AM.
- If you call the system function in `account3` at 11:01 AM, the enforcement time is immediate (now).

Tip

Store the timestamp of when you register the private endpoint in the first account. Maintain a record of the accounts that are pinned
to a particular private endpoint.

If you anticipate registering multiple accounts and a delay time of 1440 minutes is not enough time, contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

## Managing access token scope on Microsoft Azure

Before pinning a private endpoint to your Snowflake account on Azure, you must limit the scope of the access token that you pass into the
[SYSTEM$REGISTER\_PRIVATELINK\_ENDPOINT](/sql-reference/functions/system_register_privatelink_endpoint) system function. Requiring the caller to scope the access token to the
private endpoint helps Snowflake authorize the caller’s access to the endpoint. This means that the token is only valid for the private
endpoint and the Snowflake account where you call the system function.

Important

Do not use the token used in the [SYSTEM$AUTHORIZE\_PRIVATELINK](/sql-reference/functions/system_authorize_privatelink) system function.
The following steps generate a token unique to [SYSTEM$REGISTER\_PRIVATELINK\_ENDPOINT](/sql-reference/functions/system_register_privatelink_endpoint).

To limit the scope of the access token for your private endpoint on Azure, do the following steps in your Microsoft Azure account:

1. [Create](https://learn.microsoft.com/en-us/cli/azure/role/definition?view=azure-cli-latest#az-role-definition-create) a subscription
   custom role definition for a role called `snowflake-pep-role`, and replace the `subscription_id` placeholder with the ID
   of your subscription.

   Copy code

   ```
   az role definition create --role-definition '{"Name":"snowflake-pep-role","Description":
   "To generate advanced proof of access token for Snowflake private endpoint pinning","Actions":
   ["Microsoft.Network/privateEndpoints/read"],"AssignableScopes":["/subscriptions/<subscription_id>"]}'
   ```

   The subscription ID must match the subscription where the private endpoint exists. You only need to create the role definition once for
   your subscription.
2. Create the role assignment and
   [assign](https://learn.microsoft.com/en-us/cli/azure/role/assignment?view=azure-cli-latest#az-role-assignment-create)
   the `snowflake-pep-role` role and private endpoint scope to a user (or a group).
   Replace the placeholders for the `user` and the `private_endpoint_resource_id`.

   Copy code

   ```
   az role assignment create --assignee <user> --role snowflake-pep-role --scope <private_endpoint_resource_id>
   ```
3. Generate the [access token](https://learn.microsoft.com/en-us/cli/azure/account?view=azure-cli-latest#az-account-get-access-token) to
   use with the [SYSTEM$REGISTER\_PRIVATELINK\_ENDPOINT](/sql-reference/functions/system_register_privatelink_endpoint) system function. Replace the `subscription_id`
   placeholder with the ID of your subscription.

   Copy code

   ```
   az account get-access-token --subscription <subscription_id>
   ```

## Managing access token scope on Amazon Web Services

Before pinning a private endpoint to your Snowflake account on AWS, you must limit the scope of the access token that you pass into the
[SYSTEM$REGISTER\_PRIVATELINK\_ENDPOINT](/sql-reference/functions/system_register_privatelink_endpoint) system function. Requiring the caller to scope the access token to the
private endpoint helps Snowflake authorize the caller’s access to the endpoint. This means that the token is only valid for the private
endpoint and the Snowflake account where you call the system function.

Important

Do not use the token used in the [SYSTEM$AUTHORIZE\_PRIVATELINK](/sql-reference/functions/system_authorize_privatelink) system function. The following steps
generate a token unique to [SYSTEM$REGISTER\_PRIVATELINK\_ENDPOINT](/sql-reference/functions/system_register_privatelink_endpoint).

To limit the scope of the access token for your private endpoint on AWS, generate a federated token, as shown in the following example:

Copy code

```
aws sts get-federation-token --name snowflake --policy
'{ "Version": "2012-10-17", "Statement":
  [ {
  "Effect": "Allow", "Action": ["ec2:DescribeVpcEndpoints"],
  "Resource": ["*"] }
  ] }'
```

## Example

As a representative example, register an endpoint to route your connection to the Snowflake service.

1. Configure [AWS PrivateLink](/user-guide/admin-security-privatelink) or
   [Azure Private Link](/user-guide/privatelink-azure) for your Snowflake account. If you already have this service configured,
   skip to the next step.
2. Log in to Snowflake by using the public internet, and use the URL that doesn’t contain a `privatelink` segment in the URL.
4. To confirm the private connectivity endpoint mapping, call the
   [SYSTEM$GET\_PRIVATELINK\_ENDPOINT\_REGISTRATIONS](/sql-reference/functions/system_get_privatelink_endpoint_registrations) system function.

You can unregister the private connectivity endpoint from your Snowflake account by calling the
[SYSTEM$UNREGISTER\_PRIVATELINK\_ENDPOINT](/sql-reference/functions/system_unregister_privatelink_endpoint) system function.

Important

If you register a VPC endpoint or private endpoint in Snowflake and delete the endpoint in your VPC or VNet, you must call the
[SYSTEM$UNREGISTER\_PRIVATELINK\_ENDPOINT](/sql-reference/functions/system_unregister_privatelink_endpoint) system function in your Snowflake account to unregister the
endpoint. Otherwise, your connection to the Snowflake Service can’t use private connectivity. It uses the public internet.
