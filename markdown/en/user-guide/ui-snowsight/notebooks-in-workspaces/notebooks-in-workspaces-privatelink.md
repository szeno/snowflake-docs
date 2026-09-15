# Private connectivity for Notebooks in Workspaces

Feature — Generally Available

Available to all AWS, Azure, and GCP commercial regions. PrivateLink is supported.

This topic describes how to use AWS PrivateLink, Azure Private Link, or Google Private Service Connect when accessing Notebooks in Workspaces.

## AWS PrivateLink prerequisites

To access Notebooks in Workspaces with AWS PrivateLink:

1. Set up private connectivity for your [Snowflake account](/user-guide/admin-security-privatelink).
2. Set up private connectivity for [Snowsight](/user-guide/ui-snowsight-gs#label-ui-snowsight-config-private-connectivity).

In addition, your account must already use Streamlit in Snowflake over AWS PrivateLink.

## Azure Private Link prerequisites

To access Notebooks in Workspaces with Azure Private Link:

1. Set up private connectivity for your [Snowflake account](/user-guide/privatelink-azure).
2. Set up private connectivity for [Snowsight](/user-guide/ui-snowsight-gs#label-ui-snowsight-config-private-connectivity).

In addition, your account must already use Streamlit in Snowflake over Azure Private Link.

## Google Cloud Private Service Connect prerequisites

To access Notebooks in Workspaces with Google Private Service Connect:

1. Set up private connectivity for your [Snowflake account](/user-guide/private-service-connect-google).
2. Set up private connectivity for [Snowsight](/user-guide/ui-snowsight-gs#label-ui-snowsight-config-private-connectivity).

In addition, your account must already use Streamlit in Snowflake over Google Private Service Connect.

## Configure access to Notebooks in Workspaces

To configure private connectivity for Notebooks in Workspaces, follow the steps for
[configuring private connectivity for Snowsight](/user-guide/ui-snowsight-gs#label-ui-snowsight-config-private-connectivity).

## Security considerations

Notebooks serve both HTTPS-encrypted traffic and WebSocket-encrypted traffic. The Notebooks browser client application is contained in a third-party, cross-origin
iframe within Snowsight. This enables strict cross-site browser isolation control.

Notebooks in Workspaces use a separate URL scheme for specific security requirements. Notebook URLs have their own top-level domain that does not share any elements
with Snowsight. Each notebook has a unique origin.

Note

When using AWS PrivateLink, Azure Private Link, or Google Private Service Connect, you control the DNS resolution; Snowflake does not control private connectivity DNS records.
