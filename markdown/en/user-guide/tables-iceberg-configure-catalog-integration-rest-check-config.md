# Checking your REST catalog configuration

You can use the following scenarios to check whether you’ve correctly configured authorization and access control with your Iceberg
REST catalog so that Snowflake can interact with your catalog server.

- [Check a configuration for OAuth](#label-tables-iceberg-rest-catalog-integration-verify-oauth)
- [Check a configuration for a bearer token](#label-tables-iceberg-rest-catalog-integration-verify-bearer)
- [Check a configuration for SigV4](#label-tables-iceberg-rest-catalog-integration-verify-sigv4)

## Use SYSTEM$VERIFY\_CATALOG\_INTEGRATION

You can use the [SYSTEM$VERIFY\_CATALOG\_INTEGRATION](/sql-reference/functions/system_verify_catalog_integration) function to check your catalog integration configuration.

The following example demonstrates how the system function catches and reports issues with an improperly configured catalog integration.

The following example statement creates a REST catalog integration
using an invalid OAuth client secret (this runs without error):

Copy code

```
CREATE CATALOG INTEGRATION my_rest_cat_int
  CATALOG_SOURCE = ICEBERG_REST
  TABLE_FORMAT = ICEBERG
  CATALOG_NAMESPACE = 'default'
  REST_CONFIG = (
    CATALOG_URI = 'https://abc123.us-west-2.aws.myapi.com/polaris/api/catalog'
    CATALOG_NAME = 'my_catalog_name'
  )
  REST_AUTHENTICATION = (
    TYPE = OAUTH
    OAUTH_CLIENT_ID = '123AbC ...'
    OAUTH_CLIENT_SECRET = '1365910abIncorrectSecret ...'
    OAUTH_ALLOWED_SCOPES = ('all-apis', 'sql')
  )
  ENABLED = TRUE;
```

Use the system function to verify the catalog integration, expecting failure:

Copy code

```
SELECT SYSTEM$VERIFY_CATALOG_INTEGRATION('my_rest_cat_int');
```

Output:

```
+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|                                                                                                              SYSTEM$VERIFY_CATALOG_INTEGRATION('MY_REST_CAT_INT')                                                                                                               |
+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| {                                                                                                                                                                                                                                                                               |
|  "success" : false,                                                                                                                                                                                                                                                             |                                                                                                                                                                                                                                                                    |
|   "errorCode" : "004155",                                                                                                                                                                                                                                                       |
|   "errorMessage" : "SQL Execution Error: Failed to perform OAuth client credential flow for the REST Catalog integration MY_REST_CAT_INT due to error: SQL execution error: OAuth2 Access token request failed with error 'unauthorized_client:The client is not authorized'.." |
| }                                                                                                                                                                                                                                                                               |
+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
```

Tip

To run additional diagnostic operations against your catalog integration (for example, list tables or namespaces, load the latest table metadata file, or verify connectivity), you can use the [SYSTEM$EXECUTE\_CATALOG\_OPERATION](/sql-reference/functions/system_execute_catalog_operation) function. Call the function with the `help` operation to list the operations available for your account.

## Check a configuration for OAuth

Follow these steps to check your configuration for OAuth with your remote REST catalog.

### Step 1: Retrieve an access token

Use a `curl` command to retrieve an access token from your catalog. The following example
requests an access token from Snowflake Open Catalog:

Copy code

```
curl -X POST https://xx123xx.us-west-2.aws.snowflakecomputing.com/polaris/api/catalog/v1/oauth/tokens \
    -H "Accepts: application/json" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    --data-urlencode "grant_type=client_credentials" \
    --data-urlencode "scope=PRINCIPAL_ROLE:ALL" \
    --data-urlencode "client_id=<my_client_id>" \
    --data-urlencode "client_secret=<my_client_secret>" | jq
```

Where:

- `https://xx123xx.us-west-2.aws.snowflakecomputing.com/polaris/api/catalog/v1/oauth/tokens` is the endpoint for retrieving an OAuth token
  ([getToken](https://github.com/apache/iceberg/blob/apache-iceberg-1.6.1/open-api/rest-catalog-open-api.yaml#L132)).
- `scope` is the same as the value that you specify for `OAUTH_ALLOWED_SCOPES` parameter when you create a catalog integration.
  For multiple scopes, use a space as a separator.
- `my_client_id` is the same client ID that you specify for the `OAUTH_CLIENT_ID` parameter when you create a catalog integration.
- `my_client_secret` is the same client secret that you specify for the `OAUTH_CLIENT_SECRET` parameter when you create a catalog integration.

Example return value:

```
{
  "access_token": "xxxxxxxxxxxxxxxx",
  "token_type": "bearer",
  "issued_token_type": "urn:ietf:params:oauth:token-type:access_token",
  "expires_in": 3600
}
```

### Step 2: Verify the access token permissions

Using the access token that you retrieved in the previous step,
verify that you have permission to access your catalog server.

You can use a `curl` command to list the configuration settings for your catalog:

Copy code

```
curl -X GET "https://xx123xx.us-west-2.aws.snowflakecomputing.com/polaris/api/catalog/v1/config?warehouse=<warehouse>" \
    -H "Accepts: application/json" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -H "Authorization: Bearer ${ACCESS_TOKEN}" | jq
```

Where:

- `?warehouse=warehouse` optionally specifies the warehouse name to request from your catalog (if supported). For Snowflake Open Catalog, the
  warehouse name is your catalog name.
- `ACCESS_TOKEN` is a variable that contains the `access_token` that you retrieved in the previous step.

Example return value:

```
{
  "defaults": {
    "default-base-location": "s3://my-bucket/polaris/"
  },
  "overrides": {
    "prefix": "my-catalog"
  }
}
```

### Step 3: Load a table from the catalog

You can also make a GET request to load a table. Snowflake uses the
[loadTable](https://github.com/apache/iceberg/blob/apache-iceberg-1.6.1/open-api/rest-catalog-open-api.yaml#L616)
operation to load table data from your REST catalog.

Copy code

```
curl -X GET "https://xx123xx.us-west-2.aws.snowflakecomputing.com/polaris/api/catalog/v1/<prefix>/namespaces/<namespace>/tables/<table>" \
    -H "Accepts: application/json" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -H "Authorization: Bearer ${ACCESS_TOKEN}" | jq
```

Where:

- `prefix` optionally specifies the prefix obtained from the previous `getConfig` response.
- `namespace` is the namespace of the table you want to retrieve. If the namespace is nested, use the `%1F` separator;
  for example, `parentNamespace%1FchildNamespace`.
- `table` is the table name.

## Check a configuration for a bearer token

Follow these steps to check your configuration with your remote REST catalog for using a bearer token.

### Step 1: Verify the access token permissions

Use a `curl` command to verify that you have permission to access your catalog server:

Copy code

```
curl -X GET "https://xx123xx.us-west-2.aws.snowflakecomputing.com/polaris/api/catalog/v1/config?warehouse=<warehouse>" \
    -H "Accepts: application/json" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -H "Authorization: Bearer ${BEARER_TOKEN}" | jq
```

Where:

- `https://xx123xx.us-west-2.aws.snowflakecomputing.com/polaris/api/catalog/v1/oauth/tokens` is the endpoint for retrieving an OAuth token
  ([getToken](https://github.com/apache/iceberg/blob/apache-iceberg-1.6.1/open-api/rest-catalog-open-api.yaml#L132)).
- `?warehouse=warehouse` optionally specifies the warehouse name to request from your catalog (if supported).
- `BEARER_TOKEN` is a variable that contains the `access_token` that you retrieved in the previous step.

Example return value:

```
{
  "defaults": {
    "default-base-location": "s3://my-bucket/polaris"
  },
  "overrides": {
    "prefix": "my-catalog"
  }
}
```

### Step 2: Load a table from the catalog

You can also make a GET request to load a table. Snowflake uses the
[loadTable](https://github.com/apache/iceberg/blob/apache-iceberg-1.6.1/open-api/rest-catalog-open-api.yaml#L616)
operation to load table data from your REST catalog.

Copy code

```
curl -X GET "https://xx123xx.us-west-2.aws.snowflakecomputing.com/polaris/api/catalog/v1/<prefix>/namespaces/<namespace>/tables/<table>" \
    -H "Accepts: application/json" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -H "Authorization: Bearer ${BEARER_TOKEN}" | jq
```

Where:

- `prefix` optionally specifies the prefix obtained from the previous `getConfig` response.
- `namespace` is the namespace of the table you want to retrieve. If the namespace is nested, use the `%1F` separator;
  for example, `parentNamespace%1FchildNamespace`.
- `table` is the table name.

## Check a configuration for SigV4

Follow these steps to check your configuration for SigV4 with AWS.

### Step 1: Add your user to the IAM role trust relationship

When you create a REST catalog integration for SigV4, Snowflake provisions an AWS IAM user for your Snowflake account.
You [add that Snowflake IAM user to the trust relationship](/user-guide/tables-iceberg-configure-catalog-integration-rest-api-gateway#label-tables-iceberg-rest-catalog-integration-trust-relationship-sigv4) for
an [IAM role](/user-guide/tables-iceberg-configure-catalog-integration-rest-api-gateway#label-tables-iceberg-rest-catalog-integration-configure-iam-sigv4) with permission to access your API Gateway resources.

To test your configuration, *you* can assume the role as a user in your AWS account after you add your AWS
user to the role’s trust policy document. To retrieve your current IAM user ARN, use the
[sts get-caller-identity](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/sts/get-caller-identity.html) command
for the [AWS Command Line Interface (CLI)](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html) :

Copy code

```
aws sts get-caller-identity
```

Example output:

```
{
  "UserId": "ABCDEFG1XXXXXXXXXXX",
  "Account": "123456789XXX",
  "Arn": "arn:aws:iam::123456789XXX:user/managed/my_user"
}
```

The updated trust policy document should include both the Snowflake user ARN and your user ARN as follows:

Copy code

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "AWS": [
          "<snowflake_iam_user_arn>",
          "<my_iam_user_arn>"
        ]
      },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": {
          "sts:ExternalId": "my_external_id"
        }
      }
    }
  ]
}
```

For full instructions, see [Update a role trust policy](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_update-role-trust-policy.html)
in the AWS IAM documentation.

### Step 2: Assume your IAM role to get temporary credentials

To get temporary security credentials for AWS, use the
[sts assume-role](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/sts/assume-role.html) command for the AWS CLI.

Copy code

```
aws sts assume-role \
  --role-arn <my_role_arn> \
  --role-session-name <session_name>
```

Where:

- `my_role_arn` is the Amazon Resource Name (ARN) of the IAM role that you’ve configured for Snowflake.
- `session_name` is a string identifier of your choice for the assumed role session; for example, `my_rest_session`.

Example output:

```
{
  "Credentials": {
      "AccessKeyId": "XXXXXXXXXXXXXXXXXXXXX",
      "SecretAccessKey": "XXXXXXXXXXXXXXXXXXXXX",
      "SessionToken": "XXXXXXXXXXXXXXXXXXXXX",
      "Expiration": "2024-10-09T08:13:15+00:00"
  },
  "AssumedRoleUser": {
      "AssumedRoleId": "{AccessKeyId}:my_rest_catalog_session",
      "Arn": "arn:aws:sts::123456789XXX:assumed-role/my_catalog_role/my_rest_catalog_session"
  }
}
```

Note

If the `assume-role` command fails, it means that your current AWS user isn’t included in the role’s trust policy as
an allowed principal.

Similarly, if the Snowflake IAM user ARN isn’t included in your trust policy, Snowflake won’t
be able to connect to your API Gateway resources.
For more information, see [Configure the trust relationship in IAM](/user-guide/tables-iceberg-configure-catalog-integration-rest-api-gateway#label-tables-iceberg-rest-catalog-integration-trust-relationship-sigv4).

### Step 3: Verify that your IAM role has the right permissions

Using the temporary credentials that you retrieved in the previous step,
verify that your IAM role has permission to invoke your API Gateway APIs.

You can use a `curl` command to list the configuration settings for your catalog:

Copy code

```
curl -v -X GET  "https://123xxxxxxx.execute-api.us-west-2.amazonaws.com/test_v2/v1/config?warehouse=<warehouse>" \
  --user "$AWS_ACCESS_KEY_ID":"$AWS_SECRET_ACCESS_KEY" \
  --aws-sigv4 "aws:amz:us-west-2:execute-api" \
  -H "x-amz-security-token: $AWS_SESSION_TOKEN"
```

Where:

- `123xxxxxxx.execute-api.us-west-2.amazonaws.com` is your API Gateway hostname.
- `test_v2` is the name of the stage that your API is deployed to.
- `v1/config` specifies the [getConfig](https://github.com/apache/iceberg/blob/apache-iceberg-1.6.1/open-api/rest-catalog-open-api.yaml#L65) operation from the Iceberg catalog OpenAPI definition.
- `?warehouse=warehouse` optionally specifies the warehouse name to request from your catalog (if supported).
- `$AWS_ACCESS_KEY_ID` is a variable that contains the `AccessKeyId` that you retrieved using the `sts assume-role` command.
- `$AWS_SECRET_ACCESS_KEY` is a variable that contains the `SecretAccessKey` that you retrieved using the `sts assume-role` command.
- `aws:amz:us-west-2:execute-api` is the signing name of the SigV4 protocol. For AWS Glue, use `aws:amz:us-west-2:glue` instead.
- `$AWS_SESSION_TOKEN` is a variable that contains the `SessionToken` that you retrieved using the `sts assume-role` command.

Example return value:

```
{
  "defaults": {},
  "overrides": {
    "prefix": "my-catalog"
  }
}
```

You can also make a GET request to load a table. Snowflake uses the
[loadTable](https://github.com/apache/iceberg/blob/apache-iceberg-1.6.1/open-api/rest-catalog-open-api.yaml#L616)
operation to load table data from your REST catalog.

Copy code

```
curl -v -X GET "https://123xxxxxxx.execute-api.us-west-2.amazonaws.com/test_v2/v1/<prefix>/namespaces/<namespace>/tables/<table>" \
    --user "$AWS_ACCESS_KEY_ID":"$AWS_SECRET_ACCESS_KEY" \
    --aws-sigv4 "aws:amz:us-west-2:execute-api" \
    -H "x-amz-security-token: $AWS_SESSION_TOKEN"
```

Where:

- `prefix` optionally specifies the prefix obtained from the previous `getConfig` response.
- `namespace` is the namespace of the table you want to retrieve. If the namespace is nested, use the `%1F` separator;
  for example, `parentNamespace%1FchildNamespace`.
- `table` is the table name.

**Private API**

For a private API, you can specify your VPC endpoint and private Amazon API Gateway hostname in the same `curl` commands.

For example:

Copy code

```
curl -v -X GET  "https://vpce-xxxxxxxxxxxxxxxxxxxxxxxxxx.execute-api.us-west-2.vpce.amazonaws.com/test_v2/v1/config?warehouse=<warehouse>" \
  --user "$AWS_ACCESS_KEY_ID":"$AWS_SECRET_ACCESS_KEY" \
  --aws-sigv4 "aws:amz:us-west-2:execute-api" \
  -H "x-amz-security-token: $AWS_SESSION_TOKEN"
  -H "Host: abc1defgh2.execute-api.us-west-2.amazonaws.com"
```

Where:

- `https://vpce-xxxxxxxxxxxxxxxxxxxxxxxxxx.execute-api.us-west-2.vpce.amazonaws.com/...` is the hostname of your VPC endpoint.
- `abc1defgh2.execute-api.us-west-2.amazonaws.com` is the hostname of your private API in Amazon API Gateway.
