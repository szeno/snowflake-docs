# API Reference for Access to Secrets

You can use Java, Python, or Scala to retrieve credentials contained in a secret you created with the [CREATE SECRET](/sql-reference/sql/create-secret)
statement. This topic lists the methods for getting information from a secret. These are available with APIs included in Snowflake.

## Java API for Secret Access

For code in Java, use the `com.snowflake.snowpark_java.types.SnowflakeSecrets` class.

Note

You can also use the Java API in Scala code.

The following table lists methods for accessing data in a secret.

| Method | Description |
| --- | --- |
| `public String getGenericSecretString(String genericStringSecretName)` | Gets the generic token string held by the secret specified by `genericStringSecretName`. Returns a valid token string. |
| `public String getOAuthAccessToken(String oauthSecretName)` | Gets the OAuth2 access token held by the secret specified by `oauthSecretName`. Returns an OAuth2 token string. |
| `public String getSecretType(String secretName)` | Gets the type of the secret specified by `secretName`. Returns the TYPE parameter value set for this secret when it was created with the [CREATE SECRET](/sql-reference/sql/create-secret) statement. |
| `public UsernamePassword getUsernamePassword(String usernamePasswordSecretName)` | Gets the username and password from the secret specified by `usernamePasswordSecretName`. Returns a `com.snowflake.snowpark_java.types.UsernamePassword` with username and password. |
| `public CloudProviderToken getCloudProviderToken(String cloudProviderSecretName)` | Gets a cloud provider token containing values you can use to create a session with the cloud provider, such as AWS. Returns a `com.snowflake.snowpark_java.types.CloudProviderToken` with the following methods:   - `String getAccessKeyId` - `String getSecretAccessKey` - `String getToken` |
| `public String getWifToken(String secretName, String audience)` | Gets a signed JWT for the Workload Identity Federation (WIF) secret. The first argument `secretName` is the secret binding name declared in the `SECRETS` clause of the function. The `audience` parameter sets the `aud` claim in the JWT. Returns a signed JWT string. The secret must be of type `WORKLOAD_IDENTITY_FEDERATION`. |

Expand

Show lessSee more

To use the `SnowflakeSecrets` class:

1. Make the Snowpark library available to your handler code using the PACKAGES clause as described in
   [CREATE FUNCTION](/sql-reference/sql/create-function).
2. In your handler code, import `com.snowflake.snowpark_java.types.SnowflakeSecrets`.
3. Construct a `SnowflakeSecrets` object, and call one of the methods listed above to access the secret.

Code in the following example retrieves the value set for the TYPE clause when the secret was created with CREATE SECRET. Here,
the `oauth_token` secret is of type OAUTH2.

Copy code

```
CREATE OR REPLACE FUNCTION get_secret_type()
  RETURNS STRING
  LANGUAGE JAVA
  HANDLER = 'SecretTest.getSecretType'
  EXTERNAL_ACCESS_INTEGRATIONS = (external_access_integration)
  PACKAGES = ('com.snowflake:snowpark:latest')
  SECRETS = ('cred' = oauth_token )
  AS
  $$
  import com.snowflake.snowpark_java.types.SnowflakeSecrets;

  public class SecretTest {
    public static String getSecretType() {
      SnowflakeSecrets sfSecrets = SnowflakeSecrets.newInstance();

      String secretType = sfSecrets.getSecretType("cred");

      return secretType;
    }
  }
  $$;
```

## Python API for Secret Access

For code in Python, use the `_snowflake` module exposed to Python UDFs that execute within Snowflake. The following table lists
`_snowflake` functions for accessing data in a secret.

| Function | Description |
| --- | --- |
| `get_generic_secret_string(generic_string_secret_name)` | Gets the generic token string held by the secret specified by `generic_string_secret_name`. Returns a valid token string. |
| `get_oauth_access_token(oauth_secret_name)` | Gets the OAuth2 access token held by the secret specified by `oauth_secret_name`. Returns an OAuth2 token string. |
| `get_secret_type(secret_name)` | Gets the type of the secret specified by `secret_name`. Returns the TYPE parameter value set for this secret when it was created with the [CREATE SECRET](/sql-reference/sql/create-secret) statement. |
| `get_username_password(username_password_secret_name)` | Gets the username and password from the secret specified by `username_password_secret_name`. Returns an object with `username` and `password` attributes. |
| `get_cloud_provider_token(cloud_provider_secret_name)` | Gets a cloud provider object containing values you can use to create a session with the cloud provider, such as AWS. Returns a type with the following attributes:   - `access_key_id` - `secret_access_key` - `token` |
| `get_wif_token(secret_name, audience)` | Gets a signed JWT for the Workload Identity Federation (WIF) secret. The first argument `secret_name` is the secret binding name declared in the `SECRETS` clause of the function. The `audience` parameter sets the `aud` claim in the JWT. Returns a signed JWT string. The secret must be of type `WORKLOAD_IDENTITY_FEDERATION`. |

Expand

Show lessSee more

To use the `_snowflake` module in your handler code, import it as you would another module.

Code in the following example retrieves the value set for the TYPE clause when the secret was created with CREATE SECRET. Here,
the `oauth_token` secret is of type OAUTH2.

Copy code

```
CREATE OR REPLACE FUNCTION get_secret_type()
  RETURNS STRING
  LANGUAGE PYTHON
  RUNTIME_VERSION = 3.12
  HANDLER = 'get_secret'
  EXTERNAL_ACCESS_INTEGRATIONS = (external_access_integration)
  SECRETS = ('cred' = oauth_token )
  AS
$$
import _snowflake

def get_secret():
  secret_type = _snowflake.get_secret_type('cred')
  return secret_type
$$;
```

Code in the following example retrieves the username and password held by the secret.

Copy code

```
CREATE OR REPLACE FUNCTION get_secret_username_password()
  RETURNS STRING
  LANGUAGE PYTHON
  RUNTIME_VERSION = 3.12
  HANDLER = 'get_secret_username_password'
  EXTERNAL_ACCESS_INTEGRATIONS = (external_access_integration)
  SECRETS = ('cred' = credentials_secret )
  AS
$$
import _snowflake

def get_secret_username_password():
  username_password_object = _snowflake.get_username_password('cred');

  username_password_dictionary = {}
  username_password_dictionary["Username"] = username_password_object.username
  username_password_dictionary["Password"] = username_password_object.password

  return username_password_dictionary
$$;
```
