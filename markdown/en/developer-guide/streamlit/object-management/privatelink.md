# Private connectivity for Streamlit in Snowflake

This topic describes using private connectivity when accessing Streamlit in Snowflake.

## Configuring access to Snowflake

1. Set up private connectivity for your Snowflake account for a supported service:

   - [AWS PrivateLink](/user-guide/admin-security-privatelink)
   - [Azure Private Link](/user-guide/privatelink-azure)
   - [Google Cloud Private Service Connect](/user-guide/private-service-connect-google)
2. Set up private connectivity for [Snowsight](/user-guide/ui-snowsight-gs#label-ui-snowsight-config-private-connectivity).

## Configuring access to Streamlit in Snowflake

To determine the hostname, call [SYSTEM$GET\_PRIVATELINK\_CONFIG](/sql-reference/functions/system_get_privatelink_config) in your Snowflake account.
The Streamlit hostname is displayed under the `app-service-privatelink-url` key, which is the wildcard URL required for
routing Streamlit application traffic through a private connectivity service, such as AWS PrivateLink.

Note

You can set up a new VPC endpoint for Streamlit or create a DNS record to the same VPC endpoint of your Snowflake account, as shown in the following example:

- Record name: `*.<identifier>.privatelink.snowflake.app`
- Type: CNAME
- Route traffic to: same VPC as your Snowflake traffic.

You can enable per-account hostname routing by setting the
[ENABLE\_PER\_ACCOUNT\_APP\_SERVICE\_PRIVATELINK\_URL](/sql-reference/parameters#label-enable-per-account-app-service-privatelink-url)
account parameter to `TRUE`. When enabled, the `app-service-privatelink-url` key returned by the
[SYSTEM$GET\_PRIVATELINK\_CONFIG](/sql-reference/functions/system_get_privatelink_config) function returns a
per-account wildcard hostname. Prior to enablement, the `app-service-privatelink-url-next` key will
return this value.

- Record name: `*.orgname-account-name.region.cloud.privatelink.snowflake.app`
- Type: CNAME
- Route traffic to: same VPC as your Snowflake traffic.

This per-account CNAME replaces the deployment-scoped wildcard and can be used for all app services
in your account. Update your private DNS entries and firewall rules to use the new URL format before
enabling the parameter.

## Security considerations

Streamlit in Snowflake apps serve both HTTPS-encrypted traffic and WebSocket-encrypted traffic. The Streamlit browser client application is mounted in a third-party, cross-origin
iframe within Snowsight. This enables strict cross-site browser isolation control.

Streamlit in Snowflake uses a separate URL scheme for specific security requirements. Streamlit URLs have their own top-level domain with no shared elements
with Snowsight. Each Streamlit app has a unique origin.

Note

When using AWS PrivateLink or Azure Private Link, you control the DNS resolution; there are no PrivateLink DNS records controlled by Snowflake.
