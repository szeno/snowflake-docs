# Overview of External OAuth in Snowflake Open Catalog

Feature — Generally Available

Not available in government regions.

This topic teaches you how to configure External OAuth servers that use OAuth 2.0 for accessing Snowflake Open Catalog.

External OAuth integrates the customer’s OAuth 2.0 server to provide a seamless SSO experience, which enables query engines access to
Open Catalog.

Open Catalog supports the following external authorization servers:

- Auth0
- Microsoft Entra ID
- Okta

## Use cases and benefits

1. Open Catalog delegates the token issuance to a dedicated authorization server to ensure that the OAuth Client and user properly
   authenticate. The result is centralized management of tokens issued to Open Catalog.
2. Clients can authenticate to Snowflake without browser access, allowing ease of integration with the External OAuth server.

## General workflow

For each of the supported identity providers, the workflow for OAuth relating to External OAuth authorization servers can be summarized as
follows. Note that the first step only occurs once and the remaining steps occur with each attempt to access Open Catalog data.

[![Diagram that shows the general workflow of External OAuth in Snowflake Open Catalog.](/static/images/user-guide/opencatalog/img/external-oauth-general-workflow.svg "General workflow of External OAuth in Snowflake Open Catalog.")](/static/images/user-guide/opencatalog/img/external-oauth-general-workflow.svg)

1. Configure your External OAuth authorization server in your environment and the security integration in Open Catalog to establish a trust.
2. A service principal attempts to access Open Catalog data through the client application, and the application attempts to verify the service
   principal.
3. On verification, the authorization server sends a JSON Web Token (i.e. OAuth token) to the query engine.
4. The Open Catalog driver passes a connection string to Open Catalog with the OAuth token.
5. Open Catalog validates the OAuth token.
6. Open Catalog performs a service principal lookup.
7. On verification, Open Catalog instantiates a session for the service principal to access data in Open Catalog based on its role.
