# Configure a catalog integration for Amazon API Gateway

The following diagram shows how Snowflake interacts with your REST catalog server using API Gateway and SigV4 authentication.

![Diagram showing how an Iceberg REST catalog works with Amazon API Gateway, IAM, and S3.](/static/images/iceberg/getting-started-tutorial/tables-iceberg-rest-catalog-integration-sigv4-flow.svg)

Follow the steps in this topic to use a REST API in
[Amazon API Gateway](https://docs.aws.amazon.com/apigateway/latest/developerguide/welcome.html)
and [Signature Version 4 (SigV4)](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-signing.html) authentication
to securely connect Snowflake to an Iceberg REST catalog that isn’t publicly accessible.

1. [Create a REST API in Amazon API Gateway](#label-tables-iceberg-rest-catalog-integration-configure-api-sigv4)
2. [Create an IAM policy and attach it to a role](#label-tables-iceberg-rest-catalog-integration-configure-iam-sigv4)
3. [Attach an API Gateway resource policy (private APIs only)](#label-tables-iceberg-rest-catalog-integration-configure-resource-policy-sigv4)
4. [Select IAM-based authorization for your API](#label-tables-iceberg-rest-catalog-integration-select-iam-auth-sigv4)
5. [Retrieve the endpoint URL](#label-tables-iceberg-rest-catalog-integration-retrieve-url-sigv4)
6. [Create a catalog integration for SigV4](#label-tables-iceberg-rest-catalog-integration-create-sigv4)
7. [Configure the trust relationship in IAM](#label-tables-iceberg-rest-catalog-integration-trust-relationship-sigv4)

## Create a REST API in Amazon API Gateway

To connect Snowflake to your Iceberg REST catalog, you need a
[REST API resource](https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-rest-api.html)
in Amazon API Gateway.

If you don’t already have a REST API resource in Amazon API Gateway for your Iceberg catalog,
you can create a simple REST API by modifying and importing an Iceberg catalog OpenAPI definition file or manually adding endpoints.

Note

To import the Iceberg catalog OpenAPI definition, you must modify the YAML file. Amazon API Gateway does not support all components
of the OpenAPI 2.0 or 3.0 specifications. For more information, see
[Amazon API Gateway important notes for REST APIs](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-known-issues.html#api-gateway-known-issues-rest-apis).

1. In the AWS Management Console, search for and select **API Gateway**.
2. Select **Create API**.
3. Select **Build** under **REST API**. To create a *private* REST API, select **Build** under **REST API Private**.
4. Select one of the following options:

   - To create an API by manually adding endpoints, select **New API**.
   - To create an API using an OpenAPI definition file, select **Import API**, then upload the file or paste
     the definition in the code editor.
5. Enter an **API name** and optional **Description**.

   Note

   You don’t need to enter a VPC endpoint ID when you create a private REST API.
6. Select **Create API**.

For more information about creating and developing a REST API in API Gateway, see
the [Amazon API Gateway Developer Guide](https://docs.aws.amazon.com/apigateway/latest/developerguide/rest-api-develop.html).

## Create an IAM policy and attach it to a role

In this step, you create an AWS IAM role that Snowflake can use to connect to API Gateway.
You attach a policy to the role that grants permission to call your API.

1. In the AWS Management Console, search for and select **IAM**.
2. From the left-hand navigation pane, select **Policies**.
3. Select **Create policy** and then select **JSON** for the **Policy editor**.
4. Replace the empty policy with a policy that has permission to invoke your API methods.
   For example, the following general policy allows the invoke action for all API Gateway resources in an AWS account.

   Copy code

   ```
   {
     "Version": "2012-10-17",
     "Statement": [
    {
        "Effect": "Allow",
        "Action": [
            "execute-api:Invoke"
        ],
        "Resource": "arn:aws:execute-api:*:<aws_account_id>:*"
    }
     ]
   }
   ```

   Important

   As a best practice, use a policy that grants the minimum required privileges for your use case. For additional guidance and example policies,
   see [Control access to an API with IAM permissions](https://docs.aws.amazon.com/apigateway/latest/developerguide/permissions.html).
5. Select **Next**.
6. Enter a **Policy name** (for example, `snowflake_access`) and an optional **Description**.
7. Select **Create policy**.
8. From the left-hand navigation pane in the IAM dashboard, select **Roles**.
9. Select a role to attach the policy to. When you create a catalog integration, you specify this role. If you don’t have a role, [create a new role](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-user.html).
10. On the role **Summary** page in the **Permissions** tab, select **Add permissions** » **Attach policies**.
11. Search for and check the box next to the policy that you created for API Gateway, then select **Add permissions**.
12. On the role **Summary** page, copy the role **ARN**. You specify this ARN when you create a catalog integration.

## Attach an API Gateway resource policy (private APIs only)

If your REST API is private, you must attach an Amazon API Gateway resource policy to your API. The resource
policy allows Snowflake to call your API from the Amazon Virtual Private Cloud (VPC) in which your Snowflake account is located.

1. In Snowflake, call the [SYSTEM$GET\_SNOWFLAKE\_PLATFORM\_INFO](/sql-reference/functions/system_get_snowflake_platform_info)
   function to retrieve the IDs for the VPC in which your Snowflake account is located.
   From the function output, for each property identified with “purpose”: “generic”, record the corresponding VPC ID(s).

   Copy code

   ```
   SELECT SYSTEM$GET_SNOWFLAKE_PLATFORM_INFO();
   ```

   Output:

   ```
   {
     "snowflake-vpc-id": ["vpc-c1c234a5"],
     "snowflake-egress-vpc-ids": [
    ...
    {
      "id": "vpc-c1c234a5",
      "expires": "2025-03-01T00:00:00",
      "purpose": "generic"
    },
    ...
     ]
   }
   ```
2. Follow the instructions in [Attaching API Gateway resource policies](https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-resource-policies-create-attach.html#apigateway-resource-policies-create-attach-console)
   to attach a resource policy to your REST API.

   Paste and modify the following example policy.

   Copy code

   ```
   {
     "Version": "2012-10-17",
     "Statement": [
    {
      "Effect": "Deny",
      "Principal": "*",
      "Action": "execute-api:Invoke",
      "Resource": "<api_gateway_arn>",
      "Condition": {
        "StringNotEquals": {
          "aws:sourceVpc": "<snowflake_vpc_id>"
        }
      }
    },
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:sts::123456789XXX:assumed-role/<my_api_permissions_role_name>/snowflake"
      },
      "Action": "execute-api:Invoke",
      "Resource": "<api_gateway_arn>/*/*/*",
      "Condition": {
        "StringEquals": {
          "aws:sourceVpc": "<snowflake_vpc_id>"
        }
      }
    }
     ]
   }
   ```

The first statement in the policy denies all requests that don’t originate from the Snowflake VPC. The second statement allows the invoke
action (for all methods) from requests originating from the Snowflake VPC that use the
[assumed-role session principal](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_principal.html#principal-role-session).

To learn more about API Gateway resource policies, see:

- [Controlling access to an API with API Gateway resource policies](https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-resource-policies.html)
- [API Gateway resource policy examples](https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-resource-policies-examples.html)

## Select IAM-based authorization for your API

Select IAM-based authorization for each method that you want to provide access to in your REST API.
With IAM-based authorization, Snowflake can use the IAM role that you configured to make
calls to the API.

1. In the Amazon API Gateway console, select your REST API.
2. For each method:

   1. Under **Resources**, select a method from the list.
   2. Under **Method request settings**, select **Edit**.
   3. For **Authorization**, select **AWS IAM**.
   4. Select **Save**.
3. To apply the authorization changes, select **Deploy API**. For more information, see
   [Deploying a REST API from the API Gateway console](https://docs.aws.amazon.com/apigateway/latest/developerguide/how-to-deploy-api-with-console.html).

## Retrieve the endpoint URL

Retrieve your REST API endpoint URL (or *invoke* URL). Your API must be deployed to a stage before you can
retrieve the endpoint URL.

1. In the Amazon API Gateway console, select your REST API.
2. In the left-hand navigation pane, select **Stages**.
3. Under **Stage details**, copy the **Invoke URL**.

You specify the endpoint URL when you create a catalog integration.

## Create a catalog integration for SigV4

After you have a REST API in Amazon API Gateway and have completed the initial steps to
control access to your API using IAM permissions, you can create a catalog integration
in Snowflake.

To view the command syntax and parameter descriptions,
see [CREATE CATALOG INTEGRATION (Apache Iceberg™ REST)](/sql-reference/sql/create-catalog-integration-rest).

**Public REST API**

To create a catalog integration for a public REST API, specify `ICEBERG_REST`
as the `CATALOG_SOURCE` and use `SIGV4` authentication.

Include details such as your API endpoint URL and IAM role ARN.

Copy code

```
CREATE OR REPLACE CATALOG INTEGRATION my_rest_catalog_integration
  CATALOG_SOURCE = ICEBERG_REST
  TABLE_FORMAT = ICEBERG
  CATALOG_NAMESPACE = 'my_namespace'
  REST_CONFIG = (
    CATALOG_URI = 'https://asdlkfjwoalk-execute-api.us-west-2-amazonaws.com/MyApiStage'
    CATALOG_API_TYPE = AWS_API_GATEWAY
  )
  REST_AUTHENTICATION = (
    TYPE = SIGV4
    SIGV4_IAM_ROLE = 'arn:aws:iam::123456789XXX:role/my_api_permissions_role'
    SIGV4_EXTERNAL_ID = 'my_iceberg_external_id'
  )
  ENABLED = TRUE;
```

**Private REST API**

To create a catalog integration for a private REST API, you must set the `CATALOG_API_TYPE`
parameter to `AWS_PRIVATE_API_GATEWAY`.

Copy code

```
CREATE OR REPLACE CATALOG INTEGRATION my_rest_catalog_integration
  CATALOG_SOURCE = ICEBERG_REST
  TABLE_FORMAT = ICEBERG
  CATALOG_NAMESPACE = 'my_namespace'
  REST_CONFIG = (
    CATALOG_URI = 'https://asdlkfjwoalk-execute-api.us-west-2-amazonaws.com/MyApiStage'
    CATALOG_API_TYPE = AWS_PRIVATE_API_GATEWAY
  )
  REST_AUTHENTICATION = (
    TYPE = SIGV4
    SIGV4_IAM_ROLE = 'arn:aws:iam::123456789XXX:role/my_api_permissions_role'
    SIGV4_EXTERNAL_ID = 'my_iceberg_external_id'
  )
  ENABLED = TRUE;
```

Note

Both examples specify an
[external ID](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-user_externalid.html)
(`SIGV4_EXTERNAL_ID = 'my_iceberg_external_id'`) that you can use in the trust relationship for your IAM role (in the next step).

Specifying an external ID lets you use the same IAM role across multiple catalog integrations without updating the
IAM role trust policy. Doing so is particularly useful in testing scenarios if you need to create or replace a catalog integration many times.

## Configure the trust relationship in IAM

Retrieve information about the AWS IAM user that was created for your
Snowflake account when you created the catalog integration, and configure the trust
relationship for your IAM role.

1. In Snowflake, call the [DESCRIBE CATALOG INTEGRATION](/sql-reference/sql/desc-catalog-integration) command:

   Copy code

   ```
   DESCRIBE CATALOG INTEGRATION my_rest_catalog_integration;
   ```

   Record the following values:

   > | Value | Description |
   > | --- | --- |
   > | `API_AWS_IAM_USER_ARN` | The AWS IAM user created for your Snowflake account, for example, `arn:aws:iam::123456789001:user/abc1-b-self1234`. Snowflake provisions a single IAM user for your entire Snowflake account. |
   > | `API_AWS_EXTERNAL_ID` | The external ID that’s needed to establish a trust relationship. If you didn’t specify an external ID (`SIGV4_EXTERNAL_ID`) when you created the catalog integration, Snowflake generates an ID for you to use. Record the value so that you can update your IAM role trust policy with the generated external ID. |
   >
   > Expand
   >
   > Show lessSee more
2. In the AWS Management Console, search for and select **IAM**.
3. From the left-hand navigation pane, select **Roles**.
4. Select the IAM role that you created for your catalog integration.
5. Select the **Trust relationships** tab.
6. Select **Edit trust policy**.
7. Modify the policy document with the values that you recorded.

   Copy code

   ```
   {
     "Version": "2012-10-17",
     "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "AWS": "<api_aws_iam_user_arn>"
      },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": {
          "sts:ExternalId": "<api_aws_external_id>"
        }
      }
    }
     ]
   }
   ```
8. Select **Update policy** to save your changes.
