# External network access and private connectivity on AWS

[Business Critical Feature](/user-guide/intro-editions)

This feature requires Business Critical (or higher).

To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

You can configure Snowflake for outbound private connectivity to an AWS external service by way of
[external network access](/developer-guide/external-network-access/external-network-access-overview).

For data sources behind a firewall that aren’t accessible by using AWS PrivateLink (for example, on-premises databases or databases in
non-AWS environments), see [Data Connectivity Proxy](/user-guide/data-connectivity-proxy).

Unlike public connectivity, with private connectivity you must do the following operations:

- Create a private connectivity endpoint. This step requires the ACCOUNTADMIN role.
- Create the network rule so the `TYPE` property is set to `PRIVATE_HOST_PORT`.

## Outbound private connectivity costs

You pay for each private connectivity endpoint along with total data processed. For pricing of these items, see the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

You can explore the cost of these items by filtering on the following service types when querying billing views in the ACCOUNT\_USAGE and ORGANIZATION\_USAGE schemas:

- OUTBOUND\_PRIVATELINK\_ENDPOINT
- OUTBOUND\_PRIVATELINK\_DATA\_PROCESSED

For example, you can query the [USAGE\_IN\_CURRENCY\_DAILY](/sql-reference/organization-usage/usage_in_currency_daily) view and filter on these service types.

## Set up private connectivity to an external Amazon S3 service

1. Call the [SYSTEM$PROVISION\_PRIVATELINK\_ENDPOINT](/sql-reference/functions/system_provision_privatelink_endpoint) system function to specify Snowflake is connecting to an
   AWS S3 service, and the hostname to use when connecting to the service:

   Copy code

   ```
   USE ROLE ACCOUNTADMIN;
   SELECT SYSTEM$PROVISION_PRIVATELINK_ENDPOINT(
     'com.amazonaws.us-west-2.s3',
     '*.s3.us-west-2.amazonaws.com'
   );
   ```

   Note

   The asterisk in `*.s3.us-west-2.amazonaws.com` specifies that you can use the endpoint to access multiple S3 buckets.
2. Execute the following SQL statement to create a network rule that allows Snowflake to send requests to an external destination, being
   sure to set the `TYPE` property to `PRIVATE_HOST_PORT`:

   Copy code

   ```
   CREATE OR REPLACE NETWORK RULE aws_s3_network_rule
     MODE = EGRESS
     TYPE = PRIVATE_HOST_PORT
     VALUE_LIST = ('external-access-iam-bucket.s3.us-west-2.amazonaws.com');
   ```
3. Execute the following SQL statement to create a security integration for external API authentication:

   Copy code

   ```
   CREATE OR REPLACE SECURITY INTEGRATION aws_s3_security_integration
     TYPE = API_AUTHENTICATION
     AUTH_TYPE = AWS_IAM
     ENABLED = TRUE
     AWS_ROLE_ARN = 'arn:aws:iam::736112632310:role/external-access-iam-bucket';
   ```
4. Execute the following SQL statement to get the `STORAGE_AWS_IAM_USER_ARN` and `STORAGE_AWS_EXTERNAL_ID` values for the IAM user:

   Copy code

   ```
   DESC SECURITY INTEGRATION aws_s3_security_integration;
   ```
5. Using the `STORAGE_AWS_IAM_USER_ARN` and `STORAGE_AWS_EXTERNAL_ID` values, follow **Step 5** in
   [Option 1: Configure a Snowflake storage integration to access Amazon S3](/user-guide/data-load-s3-config-storage-integration) to grant the IAM user access to the Amazon S3 service.
6. Execute the following SQL statement to create a token to use for authentication with the AWS S3 service:

   Copy code

   ```
   CREATE OR REPLACE SECRET aws_s3_access_token
     TYPE = CLOUD_PROVIDER_TOKEN
     API_AUTHENTICATION = aws_s3_security_integration;
   ```
7. Execute the following SQL statement to create an external access integration that uses the network rule and token created in previous
   steps:

   Copy code

   ```
   CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION aws_s3_external_access_integration
     ALLOWED_NETWORK_RULES = (aws_s3_network_rule)
     ALLOWED_AUTHENTICATION_SECRETS = (aws_s3_access_token)
     ENABLED = TRUE
     COMMENT = 'Testing S3 connectivity';
   ```
8. Execute one of the following SQL statements to create a function that can use the external access integration and the token that were
   previously created:

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
   AS
   $$
     import boto3
     import _snowflake
     from botocore.config import Config

     def main_handler():
      # Get the previously created token as an object
      cloud_provider_object = _snowflake.get_cloud_provider_token('cred')

      # Configure boto3 connection settings
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

      # Use the s3 object upload/download resources
      # ...

      return 'Successfully connected to AWS S3'
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
   AS
   $$
     import com.snowflake.snowpark_java.types.CloudProviderToken;
     import com.snowflake.snowpark_java.types.SnowflakeSecrets;

     public class AWSTokenProvider {
      public static String handle() {
          // Get the previously created token as an object
          SnowflakeSecrets sfSecret = SnowflakeSecrets.newInstance();
          CloudProviderToken cloudProviderToken = sfSecret.getCloudProviderToken("cred");

          // Create variables for the AWS session credentials
          String accessKeyId = cloudProviderToken.getAccessKeyId();
          String secretAccessKey = cloudProviderToken.getSecretAccessKey();
          String token = cloudProviderToken.getToken();

          // Use the token to create an S3 client
          // ...

          return "Successfully connected to AWS S3 with the following access token: " + token;
      }
     }
   $$;
   ```
9. Execute one of the following SQL statements to run the function you created:

   PythonJava

   Copy code

   ```
   SELECT aws_s3_python_function();
   ```

   Copy code

   ```
   SELECT aws_s3_java_function();
   ```

## Set up private connectivity to an external Amazon Bedrock service

1. Call the [SYSTEM$PROVISION\_PRIVATELINK\_ENDPOINT](/sql-reference/functions/system_provision_privatelink_endpoint) system function to specify that Snowflake is connecting to
   the AWS S3 and Amazon Bedrock services, and the hostnames to use when connecting to the services:

   Copy code

   ```
   USE ROLE ACCOUNTADMIN;
   SELECT SYSTEM$PROVISION_PRIVATELINK_ENDPOINT(
     'com.amazonaws.us-west-2.s3',
     '*.s3.us-west-2.amazonaws.com'
   );

   SELECT SYSTEM$PROVISION_PRIVATELINK_ENDPOINT(
     'com.amazonaws.us-west-2.bedrock-runtime',
     'bedrock-runtime.us-west-2.amazonaws.com'
   );
   ```
2. Execute the following SQL statement to create a network rule that allows Snowflake to send requests to an external destination, being
   sure to set the `TYPE` property to `PRIVATE_HOST_PORT`:

   Copy code

   ```
   CREATE OR REPLACE NETWORK RULE bedrock_network_rule
     MODE = EGRESS
     TYPE = PRIVATE_HOST_PORT
     VALUE_LIST = ('bedrock-runtime.us-west-2.amazonaws.com');
   ```
3. Execute the following SQL statement to create a security integration for external API authentication:

   Copy code

   ```
   CREATE OR REPLACE SECURITY INTEGRATION bedrock_security_integration
     TYPE = API_AUTHENTICATION
     AUTH_TYPE = AWS_IAM
     ENABLED = TRUE
     AWS_ROLE_ARN = 'arn:aws:iam::736112632310:role/external-access-iam-bucket';
   ```
4. Execute the following SQL statement to get the `STORAGE_AWS_IAM_USER_ARN` and `STORAGE_AWS_EXTERNAL_ID` values for the IAM user:

   Copy code

   ```
   DESC  SECURITY INTEGRATION bedrock_security_integration;
   ```
5. Using the `STORAGE_AWS_IAM_USER_ARN` and `STORAGE_AWS_EXTERNAL_ID` values, follow **Step 5** in
   [Option 1: Configure a Snowflake storage integration to access Amazon S3](/user-guide/data-load-s3-config-storage-integration) to grant the IAM user access to the Amazon Bedrock service.
6. Execute the following SQL statement to create a token to use for authentication with the AWS Bedrock service:

   Copy code

   ```
   CREATE OR REPLACE SECRET aws_bedrock_access_token
     TYPE = CLOUD_PROVIDER_TOKEN
     API_AUTHENTICATION = bedrock_security_integration;
   ```
7. Execute the following SQL statement to create an external access integration that uses the network rule and token created in previous
   steps:

   Copy code

   ```
   CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION bedrock_external_access_integration
     ALLOWED_NETWORK_RULES = (bedrock_network_rule)
     ALLOWED_AUTHENTICATION_SECRETS=(aws_bedrock_access_token)
     ENABLED=true ;
   ```
8. Execute the following SQL statement to create a function that can use the external access integration and the token that were
   previously created:

   Copy code

   ```
   CREATE OR REPLACE FUNCTION bedrock_private_connectivity_tests(
     id INT,
     instructions VARCHAR,
     user_context VARCHAR,
     model_id VARCHAR
   )
     RETURNS VARCHAR
     LANGUAGE PYTHON
     EXTERNAL_ACCESS_INTEGRATIONS = (bedrock_external_access_integration)
     RUNTIME_VERSION = '3.8'
     SECRETS = ('cred' = aws_bedrock_access_token)
     PACKAGES = ('boto3')
     HANDLER = 'bedrock_py'
   AS
   $$
     import boto3
     import json
     import _snowflake
     def bedrock_py(id, instructions, user_context, model_id):
      # Get the previously created token as an object
      cloud_provider_object = _snowflake.get_cloud_provider_token('cred')
      cloud_provider_dictionary = {
          "ACCESS_KEY_ID": cloud_provider_object.access_key_id,
          "SECRET_ACCESS_KEY": cloud_provider_object.secret_access_key,
          "TOKEN": cloud_provider_object.token
      }
      # Assign AWS credentials and choose a region
      boto3_session_args = {
          'aws_access_key_id': cloud_provider_dictionary["ACCESS_KEY_ID"],
          'aws_secret_access_key': cloud_provider_dictionary["SECRET_ACCESS_KEY"],
          'aws_session_token': cloud_provider_dictionary["TOKEN"],
          'region_name': 'us-west-2'
      }
      session = boto3.Session(**boto3_session_args)
      client = session.client('bedrock-runtime')
      # Prepare the request body for the specified model
      def prepare_request_body(model_id, instructions, user_context):
          default_max_tokens = 512
          default_temperature = 0.7
          default_top_p = 1.0
          if model_id == 'amazon.titan-text-express-v1':
              body = {
                  "inputText": f"<SYSTEM>Follow these:{instructions}<END_SYSTEM>\n<USER_CONTEXT>Use this user context in your response:{user_context}<END_USER_CONTEXT>",
                  "textGenerationConfig": {
                      "maxTokenCount": default_max_tokens,
                      "stopSequences": [],
                      "temperature": default_temperature,
                      "topP": default_top_p
                  }
              }
          elif model_id == 'ai21.j2-ultra-v1':
              body = {
                  "prompt": f"<SYSTEM>Follow these:{instructions}<END_SYSTEM>\n<USER_CONTEXT>Use this user context in your response:{user_context}<END_USER_CONTEXT>",
                  "temperature": default_temperature,
                  "topP": default_top_p,
                  "maxTokens": default_max_tokens
              }
          elif model_id == 'anthropic.claude-3-sonnet-20240229-v1:0':
              body = {
                  "max_tokens": default_max_tokens,
                  "messages": [{"role": "user", "content": f"<SYSTEM>Follow these:{instructions}<END_SYSTEM>\n<USER_CONTEXT>Use this user context in your response:{user_context}<END_USER_CONTEXT>"}],
                  "anthropic_version": "bedrock-2023-05-31"
              }
          else:
              raise ValueError("Unsupported model ID")
          return json.dumps(body)
      # Call Bedrock to get a completion
      body = prepare_request_body(model_id, instructions, user_context)
      response = client.invoke_model(modelId=model_id, body=body)
      response_body = json.loads(response.get('body').read())
      # Parse the API response based on the model
      def get_completion_from_response(response_body, model_id):
          if model_id == 'amazon.titan-text-express-v1':
              output_text = response_body.get('results')[0].get('outputText')
          elif model_id == 'ai21.j2-ultra-v1':
              output_text = response_body.get('completions')[0].get('data').get('text')
          elif model_id == 'anthropic.claude-3-sonnet-20240229-v1:0':
              output_text = response_body.get('content')[0].get('text')
          else:
              raise ValueError("Unsupported model ID")
          return output_text
      # Get the generated text from Bedrock
      output_text = get_completion_from_response(response_body, model_id)
      return output_text
     $$;
   ```
9. Execute the following SQL statement to run the function you created:

   Copy code

   ```
   SELECT bedrock_private_connectivity_tests(1, 'Summarize the main benefits of attending this university.', 'University of Waterloo', 'amazon.titan-text-express-v1');
   ```
