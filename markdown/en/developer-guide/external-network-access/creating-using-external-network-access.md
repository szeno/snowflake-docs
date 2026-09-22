# Creating and using an external access integration

To enable access to specific external network locations, you create an external access integration that specifies a list of network rules
that specify external locations and a list of secrets you are allowed to use. By using the EXTERNAL\_ACCESS\_INTEGRATIONS clause to refer to
this integration when creating the UDF or procedure with CREATE FUNCTION or CREATE PROCEDURE, you allow the handler code to use the secret
to authenticate with the external location.

An administrator can monitor requests made to external network locations by using the
[EXTERNAL\_ACCESS\_HISTORY](/sql-reference/account-usage/external_access_history) view.

For an end-to-end sequence of code examples you might use to set up and use external access, refer to
[External network access examples](/developer-guide/external-network-access/external-network-access-examples).

Use the following steps to set up access to an external network location from a UDF or procedure.

1. Choose whether to connect to the external network location using the
   [public internet or private connectivity](#label-creating-using-external-access-integration-connectivity).
2. [Create a network rule](#label-creating-using-external-access-integration-network-rule) to represent the external network location.
3. [Create a secret](#label-creating-using-external-access-integration-secret) to hold credentials.
4. [Create an external access integration](#label-creating-using-external-access-integration-access-integration),
   aggregating the secret and network rule so that they may be used by the handler when accessing the external location.
5. [Create the UDF](#label-creating-using-external-access-integration-using-udf) or procedure with the EXTERNAL\_ACCESS\_INTEGRATIONS
   parameter set to the integration’s name as a value. This gives the function or procedure permission to access the external network
   locations and use the credentials specified by network rules and secrets in the integration.

   You separately set the SECRET parameter to the name of a secret included in the integration so that you have access to the
   secret’s contents from handler code.

   In function or procedure handler code, access the external network location specified in a network rule included in the integration.
   An attempt to access a network location that is not specified by an allowed network rule will be denied.

## Choosing the public internet or private connectivity

When you connect to an external network location, the connectivity from Snowflake to the external network location can go through the
public internet or use private connectivity through [Azure Private Link](https://learn.microsoft.com/en-us/azure/private-link/private-link-overview)
(Microsoft documentation), [AWS PrivateLink](https://docs.aws.amazon.com/vpc/latest/privatelink/what-is-privatelink.html) (AWS documentation), or
[Google Cloud Private Service Connect](https://cloud.google.com/vpc/docs/private-service-connect) (Google Cloud documentation).
You might use private connectivity based on the security requirements of your connection to the external network location.
Using private connectivity can help you meet your security requirements.

If you use the public internet, follow the instructions in the following sections in this topic.

If you use private connectivity, the person configuring the interaction must have been assigned the ACCOUNTADMIN role. In addition,
your Snowflake account must be [Business Critical Edition](/user-guide/intro-editions#label-snowflake-editions-business-critical) (or higher). Using
[Azure Private Link](/developer-guide/external-network-access/creating-using-private-azure#label-external-access-private-billing), [AWS PrivateLink](/developer-guide/external-network-access/creating-using-private-aws#label-external-access-private-billing-aws), or
[Google Cloud Private Service Connect](/developer-guide/external-network-access/creating-using-private-gcp#label-external-access-private-billing-gcp) incurs an additional billing charge. Review these
topics for more information:

- [Private connectivity for outbound network traffic](/user-guide/private-connectivity-outbound)
- [Manage private connectivity endpoints: Azure](/user-guide/private-manage-endpoints-azure)
- [Manage private connectivity endpoints: AWS](/user-guide/private-manage-endpoints-aws)
- [Manage private connectivity endpoints: Google Cloud](/user-guide/private-manage-endpoints-gcp)

Next, configure the access to the external network location to use private connectivity as shown in one of the following topics:

- [External network access and private connectivity on Microsoft Azure](/developer-guide/external-network-access/creating-using-private-azure).
- [External network access and private connectivity on AWS](/developer-guide/external-network-access/creating-using-private-aws).
- [External network access and private connectivity on Google Cloud](/developer-guide/external-network-access/creating-using-private-gcp).

## Creating a network rule to represent the external network location

You can use the [CREATE NETWORK RULE](/sql-reference/sql/create-network-rule) command to create a network rule that represents the external network’s
location and restrictions for access. For example, a network rule specifies network identifiers such as a hostname and the direction of
communication with the network (ingress or egress).

To support access to an external network, an administrator will include the rule when creating an
[external access integration](#label-creating-using-external-access-integration-access-integration). Each rule included in the
integration specifies an external network location that the function or procedure is allowed to access.

When creating a network rule for use in an external access integration, you specify the following:

- EGRESS as the MODE parameter value.
- A TYPE parameter value that indicates the type of network, such as HOST\_PORT or PRIVATE\_HOST\_PORT.
- The external location’s endpoint in the VALUE\_LIST parameter.
- (Optional) A port number with the external location’s endpoint name. If you omit a port number, Snowflake will use the default port number for
  external access, 443.

  For example, if the endpoint requires port 80, the VALUE\_LIST parameter might be as follows:

  Copy code

  ```
  VALUE_LIST = ('example.com:80')
  ```

### Access control

For security, Snowflake requires that when creating a network rule, you must use a role that has the following:

- The CREATE NETWORK RULE privilege on the schema that will hold the rule.

### Example

Code in the following example creates a network rule called `google_apis_network_rule` for outbound requests to the Google
Translation API.

For more examples, see [External network access examples](/developer-guide/external-network-access/external-network-access-examples).

Copy code

```
CREATE OR REPLACE NETWORK RULE google_apis_network_rule
  MODE = EGRESS
  TYPE = HOST_PORT
  VALUE_LIST = ('translation.googleapis.com');
```

## Creating a secret to represent credentials

You can use [CREATE SECRET](/sql-reference/sql/create-secret) to create a secret that represents credentials required to authenticate with the
external network location. For example, the secret can contain credentials such as a username and password or a
[security integration](/sql-reference/sql/create-security-integration).

For access to an external network location that supports OAuth, a best practice is to have your secret contain a reference to a
[security integration](/sql-reference/sql/create-security-integration) that contains values needed for OAuth flow such as a client ID,
client secret, token endpoint, and so on.

The secret will be used in the following ways:

- By an administrator when creating the [external access integration](#label-creating-using-external-access-integration-access-integration).

  When creating the integration, the administrator will specify the secrets that developers may use in handler code when creating a
  function or procedure that uses the integration.
- By a developer when creating a UDF or procedure handler.

  The developer will specify the allowed secret that contains the credentials that handler code can use to authenticate when making a request
  to the external location. When writing a handler, a developer can use a Snowflake API to retrieve credentials contained by the secret
  rather than including the credentials as literal values in handler code.

Note

For an OAuth secret that requires a refresh token, you can obtain the token in multiple ways, including through system functions available
in Snowflake. For an example, see [Accessing the Google Translate API with OAuth](/developer-guide/external-network-access/external-network-access-examples#label-creating-using-external-access-integration-accessing-translate-api).

### Access control

For security, Snowflake requires that when creating a secret, you must use a role that has the following:

- The CREATE SECRET privilege on the schema that will hold the secret.

### Example

Code in the following example creates a secret called `oauth_token` that specifies a security integration (represented by
`google_translate_oauth`) containing values needed to authenticate using OAuth.

For a more complete example, including the code for creating the security integration, refer to
[External network access examples](/developer-guide/external-network-access/external-network-access-examples).

Copy code

```
CREATE OR REPLACE SECRET oauth_token
  TYPE = OAUTH2
  API_AUTHENTICATION = google_translate_oauth
  OAUTH_REFRESH_TOKEN = 'my-refresh-token';
```

Tip

In this preview, you can specify the `TYPE` as `GENERIC_STRING` when you want to use an API key only as credentials.

Copy code

```
CREATE OR REPLACE SECRET bp_maps_api
  TYPE = GENERIC_STRING
  SECRET_STRING = 'replace-with-your-api-key';
```

## Creating an external access integration

You can use the [CREATE EXTERNAL ACCESS INTEGRATION](/sql-reference/sql/create-external-access-integration) command to create an external access integration that aggregates allowed network
rules (representing external network locations) and allowed secrets (representing credentials for authenticating) for use with UDFs
and procedures.

In particular, the external access integration specifies those network rules and secrets that UDFs and procedures referencing the
integration may use.

The external access integration will be used by an administrator to manage access to external network locations from UDFs and procedures.
The integration specifies only those locations and credentials allowed for use by UDFs and procedures that reference the integration.
An administrator can also enable or disable the integration to manage access to external locations.

To route traffic to a private data source through Data Connectivity Proxy, include a network rule with
`MODE = DATA_CONNECTIVITY_PROXY_EGRESS` in the integration, then associate the integration with the DCP object by using
`EXTERNAL_ACCESS_INTEGRATIONS` on `CREATE DATA CONNECTIVITY PROXY` or `ALTER DATA CONNECTIVITY PROXY`. For the setup
procedure, see [Set up Data Connectivity Proxy](/user-guide/data-connectivity-proxy-setup).

### Access control

For security, Snowflake requires that when creating an external access integration, you must use a role that has the following:

- The CREATE INTEGRATION privilege on the account.
- The USAGE privilege on any secret the integration uses, as well as the USAGE privilege on the secret’s schema.

### Example

Code in the following example creates an external access integration called `google_apis_access_integration`. The integration specifies
the `google_apis_network_rule` network rule (representing the network location) and the `oauth_token` secret
(representing credentials).

For more information about this rule and secret, refer to [Creating a network rule to represent the external network location](#label-creating-using-external-access-integration-network-rule) and
[Creating a secret to represent credentials](#label-creating-using-external-access-integration-secret).

Copy code

```
CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION google_apis_access_integration
  ALLOWED_NETWORK_RULES = (google_apis_network_rule)
  ALLOWED_AUTHENTICATION_SECRETS = (oauth_token)
  ENABLED = true;
```

## Using the external access integration in a function or procedure

When using the [CREATE FUNCTION](/sql-reference/sql/create-function) or [CREATE PROCEDURE](/sql-reference/sql/create-procedure) command to create a UDF or
procedure, you can enable access to external network locations as follows:

- Include the EXTERNAL\_ACCESS\_INTEGRATIONS parameter, setting its value to one or more integrations.

  Each integration you specify allows access to the external network locations and secrets the integration specifies.
- Include the SECRETS parameter, setting its value to one or more secrets and the names you’ll use to access them from handler code.

  The secrets you specify as values must also be specified in the external access integration.
- In handler code, access the secret to retrieve credentials for authenticating with the external network location.

Note

Always use a Snowflake secret to represent credentials rather than including the credentials as literal values in code. In addition to
protecting credentials, using a secret makes it possible to audit and manage use of the credentials because only those granted the
READ privilege on the secret may use an integration containing it in a UDF or procedure.

Snowflake limits the total number of connections that can be made from a particular UDF. To avoid running into resource exhaustion issues,
reuse connections as much as possible. You can achieve this by creating the TCP client or session once during the UDF initialization,
then using it in the UDF handler for the rest of the query.

### Access control

For security, Snowflake requires that when creating a UDF or procedure, you must use a role that has the following:

- The READ privilege on any secret it references, as well as the USAGE privilege on the secret’s schema.
- The USAGE privilege on any integration it references.

Requiring these privileges enables an administrator to manage the set of users who can enable external access. For more information, refer
to [GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege) and [Access control privileges](/user-guide/security-access-control-privileges).

### Example

Code in the following example creates a UDF called `google_translate_python`, specifying an external access integration called
`google_apis_access_integration` (refer to [Creating an external access integration](#label-creating-using-external-access-integration-access-integration) for details).
The integration specifies a network rule (representing an external network location) and secret (representing credentials) that a UDF
referencing the integration is allowed to use. For more information about this rule and secret, refer to
[Creating a network rule to represent the external network location](#label-creating-using-external-access-integration-network-rule) and [Creating a secret to represent credentials](#label-creating-using-external-access-integration-secret).

The Python handler code uses the `_snowflake.get_oauth_access_token` function to retrieve the OAuth token from the secret, then uses
the token to authenticate with the external location. The handler code may make a request to the specified URL because that URL’s host is
listed in the network rule specified by the integration.

Copy code

```
CREATE OR REPLACE FUNCTION google_translate_python(sentence STRING, language STRING)
RETURNS STRING
LANGUAGE PYTHON
RUNTIME_VERSION = 3.12
HANDLER = 'get_translation'
EXTERNAL_ACCESS_INTEGRATIONS = (google_apis_access_integration)
PACKAGES = ('snowflake-snowpark-python','requests')
SECRETS = ('cred' = oauth_token )
AS
$$
import _snowflake
import requests
import json
session = requests.Session()
def get_translation(sentence, language):
  token = _snowflake.get_oauth_access_token('cred')
  url = "https://translation.googleapis.com/language/translate/v2"
  data = {'q': sentence,'target': language}
  response = session.post(url, json = data, headers = {"Authorization": "Bearer " + token})
  return response.json()['data']['translations'][0]['translatedText']
$$;
```
