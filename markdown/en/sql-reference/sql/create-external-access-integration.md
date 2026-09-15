# CREATE EXTERNAL ACCESS INTEGRATION

Creates an [external access integration](/developer-guide/external-network-access/creating-using-external-network-access) for access
to external network locations from a UDF or procedure handler.

See also:
:   [ALTER EXTERNAL ACCESS INTEGRATION](/sql-reference/sql/alter-external-access-integration) , [DROP INTEGRATION](/sql-reference/sql/drop-integration) ,
    [SHOW INTEGRATIONS](/sql-reference/sql/show-integrations) , [DESCRIBE INTEGRATION](/sql-reference/sql/desc-integration)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] EXTERNAL ACCESS INTEGRATION <name>
  ALLOWED_NETWORK_RULES = ( <rule_name_1> [, <rule_name_2>, ... ] )
  [ ALLOWED_API_AUTHENTICATION_INTEGRATIONS = { ( <integration_name_1> [, <integration_name_2>, ... ] ) | none } ]
  [ ALLOWED_AUTHENTICATION_SECRETS = { ( <secret_name_1> [, <secret_name_2>, ... ] ) | all | none } ]
  ENABLED = { TRUE | FALSE }
  [ COMMENT = '<string_literal>' ]
```

## Required parameters

`name`
:   Identifier for the external access integration.

    The identifier value must start with an alphabetic character and cannot contain spaces or special characters unless the entire identifier
    string is enclosed in double quotes (e.g. `"My object"`). Identifiers enclosed in double quotes are case-sensitive.

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

`ALLOWED_NETWORK_RULES = (rule_name [ , rule_name ... ])`
:   Specifies the allowed [network rules](/sql-reference/sql/create-network-rule). Only egress rules may be specified.

`ENABLED = { TRUE | FALSE }`
:   Specifies whether this integration is enabled or disabled. If the integration is disabled, any handler code that relies
    on it will be unable to reach the external network location.

    The value is case-insensitive.

    The default is `TRUE`.

## Optional parameters

`ALLOWED_API_AUTHENTICATION_INTEGRATIONS = ( integration_name_1 [, integration_name_2, ... ] ) | none`
:   Specifies the security integrations whose OAuth authorization server issued the secret used by the UDF or procedure. The security
    integration must be [the type used for external API integration](/sql-reference/sql/create-security-integration-api-auth).

    This parameter’s value must be one of the following:

    - One or more Snowflake security integration names to allow any of the listed integrations.
    - `none` to allow no integrations.

    Security integrations specified by this parameter – as well as secrets specified by the ALLOWED\_AUTHENTICATION\_SECRETS parameter – are
    ways to allow secrets for use in a UDF or procedure that uses this external access integration. For more information, see
    [Usage notes](#label-create-external-access-integration-usage).

    For reference information about security integrations, refer to [CREATE SECURITY INTEGRATION (External API Authentication)](/sql-reference/sql/create-security-integration-api-auth).

`ALLOWED_AUTHENTICATION_SECRETS = ( secret_name [, secret_name ... ] ) | all | none`
:   Specifies the secrets that UDF or procedure handler code can use when accessing the external network locations referenced in allowed
    network rules.

    This parameter’s value must be one of the following:

    - One or more Snowflake secret names to allow any of the listed secrets.
    - `all` to allow any secret.
    - `none` to allow no secrets.

    The ALLOWED\_API\_AUTHENTICATION\_INTEGRATIONS parameter can also specify allowed secrets. For more information, see
    [Usage notes](#label-create-external-access-integration-usage).

    For reference information about secrets, refer to [CREATE SECRET](/sql-reference/sql/create-secret).

`COMMENT = 'string_literal'`
:   Specifies a comment for the external access integration.

    Default: No value

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE INTEGRATION | Account | Only the ACCOUNTADMIN role has this privilege by default. The privilege can be granted to additional roles as needed. |
| USAGE | Secret | Required for all secrets referenced by the integration. |
| USAGE | Schema | Required for all schemas containing any secrets referenced by the integration. |
| CREATE EXTERNAL ACCESS INTEGRATION | Account | Grants the ability to create external access integrations. This privilege does not grant the ability to create other types of integrations. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- You can allow secrets for use by a UDF or procedure by using two external access integration parameters, as described below.

  - With the ALLOWED\_AUTHENTICATION\_SECRETS parameter. You can specify secrets as parameter values or set the parameter’s value to
    `all`, allowing handler code to use any secret.
  - With the ALLOWED\_API\_AUTHENTICATION\_INTEGRATIONS parameter. A [secret](/sql-reference/sql/create-secret) is allowed for use when
    the secret itself specifies a security integration whose name is also specified by this parameter. The secret specifies the security
    integration with its API\_AUTHENTICATION parameter. In other words, when both the secret and the external access integration specify
    the security integration, the secret is allowed for use in functions and procedures that specify the external access integration.

  Note that these two alternatives function independently of one another. A secret is allowed if either (or both) of the parameters allows
  it, regardless of the value specified for the other parameter. For example, setting one of the parameters to `none` does not
  prevent a secret specified by the other parameter from being used in handler code.
- While you can specify network rules using a hostname, Snowflake enforces the rules at the IP level of granularity. Snowflake will not
  inspect your application’s traffic, so it is your responsibility to ensure that the external location’s host has the authentic
  service and that it is not possible to connect to other services on the same host. Whenever possible, you should use secure protocols
  such as HTTPS and TLS when communicating with internet endpoints.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

## Examples

Create an external access integration that provides access to the Google Translation API.

For a more complete example, refer to [Creating and using an external access integration](/developer-guide/external-network-access/creating-using-external-network-access).

1. Create a secret representing credentials.

   To create a secret, you must have been assigned a role with the CREATE SECRET privilege on the current schema. For other kinds of
   secret supported by this command, refer to [CREATE SECRET](/sql-reference/sql/create-secret). In this example, `google_translate_oauth`
   refers to a security integration. For more information, refer to [CREATE SECURITY INTEGRATION (External API Authentication)](/sql-reference/sql/create-security-integration-api-auth).

   Copy code

   ```
   CREATE OR REPLACE SECRET oauth_token
     TYPE = OAUTH2
     API_AUTHENTICATION = google_translate_oauth
     OAUTH_REFRESH_TOKEN = 'my-refresh-token';
   ```
2. Grant READ privileges on the secret to the `developer` role so that UDF developers can use it.

   Create the role that will be required for developers needing to use the secret.

   Copy code

   ```
   USE ROLE USERADMIN;
   CREATE OR REPLACE ROLE developer;
   ```

   Grant the READ privilege to the `developer` role.

   Copy code

   ```
   USE ROLE SECURITYADMIN;
   GRANT READ ON SECRET oauth_token TO ROLE developer;
   ```
3. Create a network rule representing the external network location. Use a role with the privileges described in
   [CREATE NETWORK RULE](/sql-reference/sql/create-network-rule).

   Copy code

   ```
   USE ROLE SYSADMIN;
   CREATE OR REPLACE NETWORK RULE google_apis_network_rule
     MODE = EGRESS
     TYPE = HOST_PORT
     VALUE_LIST = ('translation.googleapis.com');
   ```
4. Create an external access integration using the secret and network rule.

   Copy code

   ```
   USE ROLE ACCOUNTADMIN;
   CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION google_apis_access_integration
     ALLOWED_NETWORK_RULES = (google_apis_network_rule)
     ALLOWED_AUTHENTICATION_SECRETS = (oauth_token)
     ENABLED = true;
   ```
5. Grant USAGE privileges on the integration to the `developer` role so that UDF developers can use it.

   Copy code

   ```
   GRANT USAGE ON INTEGRATION google_apis_access_integration TO ROLE developer;
   ```
6. Create a UDF `google_translate_python` that translates the specified text into a phrase in the specified language. For more
   information, refer to [Using the external access integration in a function or procedure](/developer-guide/external-network-access/creating-using-external-network-access#label-creating-using-external-access-integration-using-udf).

   Copy code

   ```
   USE ROLE developer;

   CREATE OR REPLACE FUNCTION google_translate_python(sentence STRING, language STRING)
   RETURNS STRING
   LANGUAGE PYTHON
   RUNTIME_VERSION = 3.10
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
7. Grant the USAGE privilege on the `google_translate_python` function so that those with the user role can call it.

   Copy code

   ```
   GRANT USAGE ON FUNCTION google_translate_python(string, string) TO ROLE user;
   ```
8. Execute the `google_translate_python` function to translate a phrase.

   Copy code

   ```
   USE ROLE user;
   SELECT google_translate_python('Happy Thursday!', 'zh-CN');
   ```

   This generates the following output.

   ```
   -------------------------------------------------------
   | GOOGLE_TRANSLATE_PYTHON('HAPPY THURSDAY!', 'ZH-CN') |
   -------------------------------------------------------
   | 快乐星期四！                                          |
   -------------------------------------------------------
   ```
