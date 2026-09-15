# External network access examples

This topic provides examples of accessing external network locations from user-defined functions and procedures.

## Accessing PyPi to install packages in Snowpark Container

You can access the PyPi package repository by creating an external access integration.
You might do this when you want to allow Notebook users on Container Runtime to install `pip`
packages using the `pip install` command. With this kind of integration, you can also
allow Snowpark Container Services to install pip packages.

This example uses the Snowflake-managed network rule `snowflake.external_access.pypi_rule`
described in [Privileges and commands](/user-guide/network-rules#label-network-rule-managed-network-rules).

1. Create an external access integration using the `snowflake.external_access.pypi_rule` network rule.

   Copy code

   ```
   CREATE [OR REPLACE] EXTERNAL ACCESS INTEGRATION pypi_access
     ALLOWED_NETWORK_RULES = (snowflake.external_access.pypi_rule)
     ENABLED = true;
   ```
2. Create a `developer` role for users who need to use `pip install`
   in a Snowpark Container or Notebook on Container Runtime.

   Copy code

   ```
   CREATE OR REPLACE ROLE developer;
   ```
3. Grant to the `developer` role the privileges needed to use the external
   access integration you created.

   Copy code

   ```
   GRANT USAGE ON INTEGRATION pypi_access TO ROLE developer;
   ```

## Accessing the Google Translate API with OAuth

The following steps include code to create an external access integration for access to the
Google Translation API. The steps add the security integration and the permissions needed to execute the statements.

1. Create a network rule representing the external location.

   For more information about the role of a network rule in external access, including privileges required, see
   [Creating a network rule to represent the external network location](/developer-guide/external-network-access/creating-using-external-network-access#label-creating-using-external-access-integration-network-rule).

   Copy code

   ```
   CREATE OR REPLACE NETWORK RULE google_apis_network_rule
     MODE = EGRESS
     TYPE = HOST_PORT
     VALUE_LIST = ('translation.googleapis.com');
   ```
2. Create a security integration to hold the OAuth credentials required to authenticate with the external network location specified
   by the `google_apis_network_rule` network rule.

   For reference information on the command, including privileges required, see
   [CREATE SECURITY INTEGRATION (External API Authentication)](/sql-reference/sql/create-security-integration-api-auth).

   Copy code

   ```
   CREATE OR REPLACE SECURITY INTEGRATION google_translate_oauth
     TYPE = API_AUTHENTICATION
     AUTH_TYPE = OAUTH2
     OAUTH_CLIENT_ID = 'my-client-id'
     OAUTH_CLIENT_SECRET = 'my-client-secret'
     OAUTH_TOKEN_ENDPOINT = 'https://oauth2.googleapis.com/token'
     OAUTH_AUTHORIZATION_ENDPOINT = 'https://accounts.google.com/o/oauth2/auth'
     OAUTH_ALLOWED_SCOPES = ('https://www.googleapis.com/auth/cloud-platform')
     ENABLED = TRUE;
   ```
3. Create a secret to represent the credentials contained by the `google_translate_oauth` security integration.

   For more information about the role of the secret in external access, including privileges required, see
   [Creating a secret to represent credentials](/developer-guide/external-network-access/creating-using-external-network-access#label-creating-using-external-access-integration-secret).

   The secret must specify a refresh token with its OAUTH\_REFRESH\_TOKEN parameter. To obtain a refresh token from the service provider
   (in this case, from the Google Cloud Translation API service), you can use a way the provider offers or use Snowflake system functions.

   To create a secret with a refresh token, use *either* Google OAuth Playground or Snowflake system functions, as described by the
   following:

   - Snowflake system functions

     1. Execute CREATE SECRET to create a secret. You’ll update it with the refresh token in a later step.

        Copy code

        ```
        USE DATABASE my_db;
        USE SCHEMA secret_schema;

        CREATE OR REPLACE SECRET oauth_token
          TYPE = oauth2
          API_AUTHENTICATION = google_translate_oauth;
        ```
     2. Execute the [SYSTEM$START\_OAUTH\_FLOW](/sql-reference/functions/system_start_oauth_flow) function to retrieve a URL with which you can obtain a
        refresh token, specifying as its argument the name of the secret you created previously.

        Copy code

        ```
        CALL SYSTEM$START_OAUTH_FLOW( 'my_db.secret_schema.oauth_token' );
        ```

        The function generates a URL you can use to complete the OAuth consent process.
     3. In a browser, visit the generated URL and complete the OAuth2 consent process. When you’ve finished, leave the browser open to the
        last page of the process.
     4. From the browser address bar, copy all of the text after the question mark in the URL of the last page of the consent process.
     5. Execute the [SYSTEM$FINISH\_OAUTH\_FLOW](/sql-reference/functions/system_finish_oauth_flow) function, specifying as an argument the parameters you just
        copied from the browser address bar to update the secret with a refresh token.

        Be sure to execute SYSTEM$FINISH\_OAUTH\_FLOW in the same session as SYSTEM$START\_OAUTH\_FLOW. SYSTEM$FINISH\_OAUTH\_FLOW updates
        the secret you specified in SYSTEM$START\_OAUTH\_FLOW with access token and refresh token it obtained from the OAuth server.

        Copy code

        ```
        CALL SYSTEM$FINISH_OAUTH_FLOW( 'state=<remaining_url_text>' );
        ```
   - Google OAuth Playground

     1. In [Google OAuth Playground](https://developers.google.com/oauthplayground/), select and authorize the Cloud Translation API as
        specified in step 1.
     2. In Step 2, click **exchange authorization code for tokens**, then copy the **refresh token**
        token value.
     3. Execute CREATE SECRET to create a secret that specifies the refresh token value you copied.

        For more information about the role of a secret in external access, including privileges required, see
        [Creating a secret to represent credentials](/developer-guide/external-network-access/creating-using-external-network-access#label-creating-using-external-access-integration-secret).

        Copy code

        ```
        CREATE OR REPLACE SECRET oauth_token
          TYPE = oauth2
          API_AUTHENTICATION = google_translate_oauth
          OAUTH_REFRESH_TOKEN = 'my-refresh-token';
        ```
4. Create an external access integration using the network rule and secret.

   For more information about the role of an external access integration, including privileges required, see
   [Creating an external access integration](/developer-guide/external-network-access/creating-using-external-network-access#label-creating-using-external-access-integration-access-integration).

   Copy code

   ```
   CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION google_apis_access_integration
     ALLOWED_NETWORK_RULES = (google_apis_network_rule)
     ALLOWED_AUTHENTICATION_SECRETS = (oauth_token)
     ENABLED = TRUE;
   ```
5. Create a `developer` role that will be assigned to users who need to create a UDF or procedure that uses the integration.

   Copy code

   ```
   CREATE OR REPLACE ROLE developer;
   CREATE OR REPLACE ROLE user;
   ```
6. Grant to the `developer` role privileges needed to create a UDF that uses the objects for external access. This includes the
   following:

   - The READ privilege on the secret.
   - The USAGE privilege on the schema containing the secret.
   - The USAGE privilege on the integration.

     Copy code

     ```
     GRANT READ ON SECRET oauth_token TO ROLE developer;
     GRANT USAGE ON SCHEMA secret_schema TO ROLE developer;
     GRANT USAGE ON INTEGRATION google_apis_access_integration TO ROLE developer;
     ```
7. Create a UDF `google_translate_python` that translates the specified text into a phrase in the specified language. For more
   information, see [Using the external access integration in a function or procedure](/developer-guide/external-network-access/creating-using-external-network-access#label-creating-using-external-access-integration-using-udf).

   Copy code

   ```
   USE ROLE developer;

   CREATE OR REPLACE FUNCTION google_translate_python(sentence STRING, language STRING)
     RETURNS STRING
     LANGUAGE PYTHON
     RUNTIME_VERSION = 3.12
     HANDLER = 'get_translation'
     EXTERNAL_ACCESS_INTEGRATIONS = (google_apis_access_integration)
     PACKAGES = ('snowflake-snowpark-python','requests')
     SECRETS = ('cred' = oauth_token )
   AS $$
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
8. Grant the USAGE privilege on the `google_translate_python` function so that those with the `user` role can call it.

   Copy code

   ```
   GRANT USAGE ON FUNCTION google_translate_python(string, string) TO ROLE user;
   ```
9. Execute the `google_translate_python` function to translate a phrase.

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

## Accessing an external lambda function with basic authentication

The following steps include example code to create an external access integration for access to a lambda function external to Snowflake.
The example uses a placeholder for the external endpoint itself, but it could be a function available at a REST service endpoint, for example.

The external access is used in a [vectorized Python UDF](/developer-guide/udf/python/udf-python-batch) that receives a Pandas
DataFrame containing the data.

1. Create a network rule `lambda_network_rule` representing the external location `my_external_service` (here, a placeholder
   value for the location of an external endpoint).

   For more information about the role of a network rule in external access, see
   [Creating a network rule to represent the external network location](/developer-guide/external-network-access/creating-using-external-network-access#label-creating-using-external-access-integration-network-rule).

   Copy code

   ```
   CREATE OR REPLACE NETWORK RULE lambda_network_rule
     MODE = EGRESS
     TYPE = HOST_PORT
     VALUE_LIST = ('my_external_service');
   ```
2. Create a secret to represent credentials required by the external service.

   Handler code later in this example retrieves the credentials from the secret using a Snowflake API for Python.

   For more information about the role of the secret in external access, see [Creating a secret to represent credentials](/developer-guide/external-network-access/creating-using-external-network-access#label-creating-using-external-access-integration-secret).

   Copy code

   ```
   CREATE OR REPLACE SECRET secret_password
     TYPE = PASSWORD
     USERNAME = 'my_user_name'
     PASSWORD = 'my_password';
   ```
3. Create a `developer` role and grant to it READ privileges on the secret. This role will be assigned to users who need to create
   a UDF or procedure that uses the secret.

   Also, create the role that users will use to call the function.

   Copy code

   ```
   CREATE OR REPLACE ROLE developer;
   CREATE OR REPLACE ROLE user;
   ```
4. Grant to the `developer` role privileges needed to create a UDF that uses the objects for external access. This includes the
   following:

   - The READ privilege on the secret.
   - The USAGE privilege on the schema containing the secret.

   Copy code

   ```
   GRANT READ ON SECRET secret_password TO ROLE developer;
   GRANT USAGE ON SCHEMA secret_schema TO ROLE developer;
   ```
5. Create an external access integration to specify the external endpoint and credentials through the network rule and secret you created.

   For more information about the role of an external access integration, including privileges required, see
   [Creating an external access integration](/developer-guide/external-network-access/creating-using-external-network-access#label-creating-using-external-access-integration-access-integration).

   Copy code

   ```
   CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION lambda_external_access_integration
     ALLOWED_NETWORK_RULES = (lambda_network_rule)
     ALLOWED_AUTHENTICATION_SECRETS = (secret_password)
     ENABLED = TRUE;
   ```
6. Create a [vectorized Python UDF](/developer-guide/udf/python/udf-python-batch) `return_double_column`
   that accesses an external network location to process data received as a
   [Pandas DataFrame](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html).

   For more information on using external access in a UDF, see [Using the external access integration in a function or procedure](/developer-guide/external-network-access/creating-using-external-network-access#label-creating-using-external-access-integration-using-udf).

   Copy code

   ```
   CREATE OR REPLACE FUNCTION return_double_column(x int)
     RETURNS INT
     LANGUAGE PYTHON
     EXTERNAL_ACCESS_INTEGRATIONS = (lambda_external_access_integration)
     SECRETS = ('cred' = secret_password)
     RUNTIME_VERSION = 3.12
     HANDLER = 'return_first_column'
     PACKAGES = ('pandas', 'requests')
   AS $$
   import pandas
   import numpy as np
   import json
   import requests
   import base64
   import _snowflake
   from _snowflake import vectorized
   from requests.auth import HTTPBasicAuth
   from requests.adapters import HTTPAdapter
   from requests.packages.urllib3.util.retry import Retry

   session = requests.Session()
   retries = Retry(total=10, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504], allowed_methods = None)

   session.mount('https://', HTTPAdapter(max_retries=retries))

   @vectorized(input=pandas.DataFrame)
   def return_first_column(df):
     request_rows = []

     df.iloc[:,0] = df.iloc[:,0].astype(int)
     request_rows = np.column_stack([df.index, df.iloc[:,0]]).tolist()

     request_payload = {"data" : request_rows}

     username_password_object = _snowflake.get_username_password('cred');
     basic = HTTPBasicAuth(username_password_object.username, username_password_object.password)

     url = 'my_external_service'

     response = session.post(url, json=request_payload, auth=basic)

     response.raise_for_status()
     response_payload = json.loads(response.text)

     response_rows = response_payload["data"]

     return pandas.DataFrame(response_rows)[1]
   $$;
   ```
7. Grant the USAGE privilege on the `return_double_column` function so that those with the `user` role can call it.

   Copy code

   ```
   GRANT USAGE ON FUNCTION return_double_column(int) TO ROLE user;
   ```
8. Execute the `return_double_column` function, making a request to the external endpoint.

   Code in the following example creates a two-column table and inserts 100,000,000 rows containing 4-byte integers. The code
   then executes the `return_double_column` function, passing values from column `a` for processing by the external endpoint.

   Copy code

   ```
   CREATE OR REPLACE TABLE t1 (a INT, b INT);
   INSERT INTO t1 SELECT SEQ4(), SEQ4() FROM TABLE(GENERATOR(ROWCOUNT => 100000000));

   SELECT return_double_column(a) AS retval FROM t1 ORDER BY retval;
   ```

## Accessing Amazon S3 with AWS IAM

The following steps include example code to connect to an AWS S3 bucket using IAM.

For more information about AWS IAM, see [AWS IAM documentation](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_identifiers.html).

1. Create a network rule, `aws_s3_network_rule`, that represents the AWS S3 bucket at the location specified by the VALUE\_LIST
   parameter.

   For more information about the role of a network rule in external access, see
   [Creating a network rule to represent the external network location](/developer-guide/external-network-access/creating-using-external-network-access#label-creating-using-external-access-integration-network-rule).

   Copy code

   ```
   CREATE OR REPLACE NETWORK RULE aws_s3_network_rule
     MODE = EGRESS
     TYPE = PRIVATE_HOST_PORT
     VALUE_LIST = ('external-access-iam-bucket.s3.us-west-2.amazonaws.com');
   ```
2. Create a security integration to hold the AWS IAM Amazon Resource Name (ARN) credentials required to authenticate with the external
   network location specified by the `aws_s3_network_rule` network rule.

   For reference information on the command, including privileges required, see
   [CREATE SECURITY INTEGRATION (AWS IAM Authentication)](/sql-reference/sql/create-security-integration-aws-iam).

   Copy code

   ```
   CREATE OR REPLACE SECURITY INTEGRATION aws_s3_security_integration
     TYPE = API_AUTHENTICATION
     AUTH_TYPE = AWS_IAM
     ENABLED = TRUE
     AWS_ROLE_ARN = 'arn:aws:iam::736112632310:role/external-access-iam-bucket';
   ```
3. Get the ARN and ID for the IAM USER.

   1. Execute the DESC command on the security integration you created.

      Copy code

      ```
      DESC SECURITY INTEGRATION aws_s3_security_integration;
      ```
   2. From the output displayed, copy the values of the following properties to use in the next step:

      - API\_AWS\_IAM\_USER\_ARN
      - API\_AWS\_EXTERNAL\_ID
4. Grant the IAM user permissions needed to access the bucket.

   Use the ARN and ID values when configuring a trust policy as described in Step 5 of [Option 1: Configure a Snowflake storage integration to access Amazon S3](/user-guide/data-load-s3-config-storage-integration).
5. Create a [secret](/sql-reference/sql/create-secret) of type CLOUD\_PROVIDER\_TOKEN to
   represent credentials required by the external service.

   Handler code later in this example retrieves the credentials from the secret using a
   [Snowflake API](/developer-guide/external-network-access/secret-api-reference).

   For more information about the role of the secret in external access, see [Creating a secret to represent credentials](/developer-guide/external-network-access/creating-using-external-network-access#label-creating-using-external-access-integration-secret).

   Copy code

   ```
   CREATE OR REPLACE SECRET aws_s3_access_token
     TYPE = CLOUD_PROVIDER_TOKEN
     API_AUTHENTICATION = aws_s3_security_integration;
   ```
6. Create a `developer` role and grant to it READ privileges on the secret. This role will be assigned to users who need to create
   a UDF or procedure that uses the secret.

   Also, create the role that users will use to call the function.

   Copy code

   ```
   CREATE OR REPLACE ROLE developer;
   CREATE OR REPLACE ROLE user;
   ```
7. Grant to the `developer` role the privileges needed to create a UDF that uses the objects for external access. This includes the
   following:

   - The READ privilege on the secret.
   - The USAGE privilege on the schema containing the secret.

   Copy code

   ```
   GRANT READ ON SECRET aws_s3_access_token TO ROLE developer;
   GRANT USAGE ON SCHEMA secret_schema TO ROLE developer;
   ```
8. Create an [external access integration](/sql-reference/sql/create-external-access-integration)
   to specify the external endpoint and credentials through the network rule and secret you created.

   For more information about the role of an external access integration, including privileges required, see
   [Creating an external access integration](/developer-guide/external-network-access/creating-using-external-network-access#label-creating-using-external-access-integration-access-integration).

   Copy code

   ```
   CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION aws_s3_external_access_integration
     ALLOWED_NETWORK_RULES = (aws_s3_network_rule)
     ALLOWED_AUTHENTICATION_SECRETS = (aws_s3_access_token)
     ENABLED = TRUE
     COMMENT = 'Testing S3 connectivity';
   ```
9. Create a UDF that uses the external access integration to connect with the Amazon S3 bucket specified in the network rule you created.

   The handler code uses [Snowflake APIs](/developer-guide/external-network-access/secret-api-reference) to retrieve a token from
   the secret you created. From this token, you can use Snowflake APIs to retrieve values needed to create a session for connecting with
   Amazon S3, including an access key ID, secret access key, and session token.

   For more information on using external access in a UDF, see [Using the external access integration in a function or procedure](/developer-guide/external-network-access/creating-using-external-network-access#label-creating-using-external-access-integration-using-udf).

   PythonJava

   Copy code

   ```
   CREATE OR REPLACE FUNCTION aws_s3_python_function()
     RETURNS VARCHAR
     LANGUAGE PYTHON
     EXTERNAL_ACCESS_INTEGRATIONS = (aws_s3_external_access_integration)
     RUNTIME_VERSION = '3.12'
     SECRETS = ('cred' = aws_s3_access_token)
     PACKAGES = ('boto3')
     HANDLER = 'main_handler'
   AS $$
   import boto3
   import _snowflake
   from botocore.config import Config

   def main_handler():
     # Get token object
     cloud_provider_object = _snowflake.get_cloud_provider_token('cred')

     # Boto3 configuration
     config = Config(
    retries=dict(total_max_attempts=9),
    connect_timeout=30,
    read_timeout=30,
    max_pool_connections=50
     )

     # Connect to S3 using boto3
     s3 = boto3.client(
    's3',
    region_name='us-west-2',
    aws_access_key_id=cloud_provider_object.access_key_id,
    aws_secret_access_key=cloud_provider_object.secret_access_key,
    aws_session_token=cloud_provider_object.token,
    config=config
     )

     # Use S3 object to upload/download
     return 'Successfully connected with S3'
   $$;
   ```

   Copy code

   ```
   CREATE OR REPLACE FUNCTION aws_s3_java_function()
     RETURNS STRING
     LANGUAGE JAVA
     EXTERNAL_ACCESS_INTEGRATIONS = (aws_s3_external_access_integration)
     SECRETS = ('cred' = aws_s3_access_token)
     HANDLER = 'AWSTokenProvider.handle'
   AS $$
   import com.snowflake.snowpark_java.types.CloudProviderToken;
   import com.snowflake.snowpark_java.types.SnowflakeSecrets;

   public class AWSTokenProvider {
     public static String handle() {
    // Get token object
    SnowflakeSecrets sfSecret = SnowflakeSecrets.newInstance();
    CloudProviderToken cloudProviderToken = sfSecret.getCloudProviderToken("cred");

    // Create variables for AWS session credentials
    String accessKeyId = cloudProviderToken.getAccessKeyId();
    String secretAccessKey = cloudProviderToken.getSecretAccessKey();
    String token = cloudProviderToken.getToken();

    // Create S3 client using AWS APIs.

    return "Successfully connected with S3 with temp access token: " + token;
     }
   }
   $$;
   ```
10. Grant the USAGE privilege on the UDF so that those with the `user` role can call it.

Copy code

```
GRANT USAGE ON FUNCTION return_double_column(int) TO ROLE user;
```

11. Execute the function to connect to the external endpoint.

PythonJava

Copy code

```
SELECT aws_s3_python_function();
```

Copy code

```
SELECT aws_s3_java_function();
```
