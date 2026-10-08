# Private connectivity for Snowflake Native Apps

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

A Snowflake Native App uses the private connectivity configured on the account where the app is installed.
There is no separate private connectivity setup for the app.

This topic describes which existing configuration applies, and which limitations are specific to an app.

## Cloud platform support

AWS PrivateLink and Azure Private Link are generally available for Snowflake Native Apps with and without
containers. Google Cloud Private Service Connect is not yet supported.

For the full matrix, including Virtual Private Snowflake and government regions, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

## Ingress

Configure inbound private connectivity on the account where the app is installed:

- [AWS PrivateLink](/user-guide/admin-security-privatelink)
- [Azure Private Link](/user-guide/privatelink-azure)

For more information, see [To the Snowflake Service](/user-guide/private-connectivity-inbound#label-private-connect-snowflake-service). To open the app in
Snowsight, also configure [To Snowsight](/user-guide/private-connectivity-inbound#label-private-connect-ui).

### Streamlit

If the app includes Streamlit, also configure
[Private connectivity for Streamlit in Snowflake](/developer-guide/streamlit/object-management/privatelink) so the Streamlit URL resolves on your
private network. This includes AWS PrivateLink and Azure Private Link.

Google Cloud Private Service Connect is not supported for a Streamlit app in a Snowflake Native App. See
[Unsupported Streamlit features](/developer-guide/native-apps/adding-streamlit#label-streamlit-unsupported-features-na).

### Apps with containers

Endpoints that the app exposes use the same inbound private connectivity as Snowpark Container Services. See
[Inbound connectivity](/developer-guide/snowpark-container-services/private-connectivity#label-spcs-private-connectivity-inbound).

Open `privatelink_ingress_url` from [SHOW ENDPOINTS](/sql-reference/sql/show-endpoints), rather than the public
`ingress_url`. `SHOW ENDPOINTS` returns `privatelink_ingress_url` only for Business Critical
accounts.

## Egress

An app reaches an external endpoint over private connectivity through an external access integration.
The provider requests the endpoint with `PRIVATE_HOST_PORTS` on the app specification. See
[Request external access](/developer-guide/native-apps/requesting-app-specs-eai).

The consumer approves that app specification in the account where the app is installed. See
[Approve app specifications](/developer-guide/native-apps/ui-consumer-app-spec).

### Apps without containers

Egress from a UDF, UDTF, or stored procedure uses the same private connectivity setup as external
network access. See [External network locations using external access integrations](/user-guide/private-connectivity-outbound#label-private-connect-external-access).

### Apps with containers

Egress from the service uses the same private connectivity setup as Snowpark Container Services. See
[Network egress using private connectivity](/developer-guide/snowpark-container-services/service-network-communications#label-working-with-services-jobs-egress-private).

## Email notifications

Links in email notifications from an app do not correctly link into an account that uses private
connectivity. See [Known issue with AWS PrivateLink and Azure Private Link](/developer-guide/native-apps/limitations#label-native-apps-privatelink-email).
