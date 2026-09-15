# Private connectivity for Notebooks

This topic describes using AWS PrivateLink, Azure Private Link, or Google Private Service Connect when accessing Snowflake Notebooks. This feature
is available in both [Warehouse and Container Runtimes](/user-guide/ui-snowsight/notebooks#label-notebook-runtime-descriptions) for AWS and Azure, and in Warehouse Runtime for Google.

## AWS PrivateLink prerequisites

To access Snowflake Notebooks with AWS PrivateLink:

1. Set up private connectivity for your [Snowflake account](/user-guide/admin-security-privatelink).
2. Set up private connectivity for [Snowsight](/user-guide/ui-snowsight-gs#label-ui-snowsight-config-private-connectivity).

In addition, your account must already use Streamlit in Snowflake over AWS PrivateLink. Notebooks uses the Streamlit engine and widgets to execute and render
notebook cell outputs.

## Azure Private Link prerequisites

To access Snowflake Notebooks with Azure Private Link:

1. Set up private connectivity for your [Snowflake account](/user-guide/privatelink-azure).
2. Set up private connectivity for [Snowsight](/user-guide/ui-snowsight-gs#label-ui-snowsight-config-private-connectivity).

In addition, your account must already use Streamlit in Snowflake over Azure Private Link. Notebooks relies on the Streamlit engine for execution and uses
Streamlit widgets to render cell outputs.

## Google Cloud Private Service Connect prerequisites

To access Snowflake Notebooks with Google Private Service Connect:

1. Set up private connectivity for your [Snowflake account](/user-guide/private-service-connect-google).
2. Set up private connectivity for [Snowsight](/user-guide/ui-snowsight-gs#label-ui-snowsight-config-private-connectivity).

In addition, your account must already use Streamlit in Snowflake over Google Private Service Connect. Notebooks relies on the Streamlit engine for execution
and uses Streamlit widgets to render cell outputs.

## Configure access to Snowflake Notebooks

To determine the hostname:

- Call [SYSTEM$GET\_PRIVATELINK\_CONFIG](/sql-reference/functions/system_get_privatelink_config) in your Snowflake account. Use the value returned for the `app-service-privatelink-url` key.
  This URL is used to route traffic to Snowflake-hosted app services, including Snowflake Notebooks, over AWS PrivateLink, Azure Private Link, or Google Private Service Connect.

Note

You can set up a new VPC endpoint for Notebooks or create a DNS record to the same VPC endpoint of your Snowflake account, as shown in the following example:

- Record name: `*.abcd.privatelink.snowflake.app`
- Type: CNAME
- Route traffic to: same VPC as your Snowflake traffic.

You can enable per-account hostname routing by setting the
[ENABLE\_PER\_ACCOUNT\_APP\_SERVICE\_PRIVATELINK\_URL](/sql-reference/parameters#label-enable-per-account-app-service-privatelink-url)
account parameter to `TRUE`. When enabled, the
[SYSTEM$GET\_PRIVATELINK\_CONFIG](/sql-reference/functions/system_get_privatelink_config) function will contain the per-account wildcard hostname
in the `app-service-privatelink-url` key. When disabled, the `app-service-privatelink-url-key` will contain
the per-account hostname.

- Record name: `*.orgname-account-name.region.cloud.privatelink.snowflake.app`
- Type: CNAME
- Route traffic to: same VPC as your Snowflake traffic.

This per-account CNAME replaces the deployment-scoped wildcard and can be used for all app services
in your account. Update your private DNS entries and firewall rules to use the new URL format prior
to changing the parameter.

## Security considerations

Notebooks serve both HTTPS-encrypted traffic and WebSocket-encrypted traffic. The Notebooks browser client application is mounted in a third-party, cross-origin
iframe within Snowsight. This enables strict cross-site browser isolation control.

Snowflake Notebooks use a separate URL scheme for specific security requirements. Notebook URLs have their own top-level domain that does not share any elements
with Snowsight. Each notebook has a unique origin.

Note

When using AWS PrivateLink, Azure Private Link, or Google Private Service Connect, you control the DNS resolution; no private connectivity
DNS records are controlled by Snowflake.
