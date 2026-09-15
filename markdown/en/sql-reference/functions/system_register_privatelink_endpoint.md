Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$REGISTER\_PRIVATELINK\_ENDPOINT

[Business Critical Feature](/user-guide/intro-editions)

This feature requires Business Critical (or higher).

To inquire about upgrading, contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Registers a private connectivity endpoint to route your connection to the Snowflake service.

## Syntax

**AWS**

Copy code

```
SYSTEM$REGISTER_PRIVATELINK_ENDPOINT(
  '<aws_private_endpoint_vpce_id>',
  '<aws_account_id>',
  '<token>',
  [ <delay_time> ]
  )
```

**Azure**

Copy code

```
SYSTEM$REGISTER_PRIVATELINK_ENDPOINT(
  '<azure_private_endpoint_link_id>',
  '<azure_private_endpoint_resource_id>',
  '<token>',
  [ <delay_time> ]
  )
```

## Required arguments

**AWS**

`aws_private_endpoint_vpce_id`
:   Specifies the identifier for your Amazon Web Services (AWS) virtual private cloud endpoint (AWS VPCEID).

    To obtain the AWS VPCEID value, navigate through the AWS console or use the following command:

    Copy code

    ```
    aws ec2 describe-vpc-endpoints
    ```

`aws_account_id`
:   The 12-digit identifier that uniquely identifies your Amazon Web Services (AWS) account, as a string.

    To obtain the AWS account ID value, navigate through the AWS console or use the following command:

    Copy code

    ```
    aws sts get-caller-identity
    ```

**Azure**

`azure_private_endpoint_link_id`
:   Specifies the identifier for your Microsoft Azure (Azure) virtual private cloud endpoint link (Azure LinkID).

    To obtain the Azure LinkID value:

    Run the [SYSTEM$GET\_PRIVATELINK\_AUTHORIZED\_ENDPOINTS](/sql-reference/functions/system_get_privatelink_authorized_endpoints) system function.

`azure_private_endpoint_resource_id`
:   The identifier that uniquely identifies your Snowflake account in Microsoft Azure (Azure) as a string.

    To obtain the Azure private endpoint resource Id, use the following command:

    Copy code

    ```
    az network private-endpoint list --resource-group my_resource_group
    ```

`token`
:   Specifies an access token to verify ownership of the private connectivity endpoint.

    To obtain the token, you must have the corresponding read or describe privilege on the private connectivity endpoint at a minimum.
    For more information, see:

    - [AWS endpoint policies](https://docs.aws.amazon.com/vpc/latest/privatelink/vpc-endpoints-access.html)
    - [Azure private endpoint privileges](https://learn.microsoft.com/en-us/azure/private-link/rbac-permissions#private-endpoint)

    To obtain the token, use the following commands:

    - For Snowflake on AWS:

      Copy code

      ```
      aws sts get-federation-token --name snowflake --policy '{ "Version": "2012-10-17", "Statement"
      : [ { "Effect": "Allow", "Action": ["ec2:DescribeVpcEndpoints"], "Resource": ["*"] } ] }'
      ```
    - For Snowflake on Azure:

      Copy code

      ```
      az account get-access-token --subscription <subscription_id>
      ```

    For more information about limiting the scope of an access token, see:

    - For Snowflake on AWS: [Managing access token scope on Amazon Web Services](/user-guide/pin-private-endpoints#label-managing-access-token-scope-on-aws)
    - For Snowflake on Azure: [Managing access token scope on Microsoft Azure](/user-guide/pin-private-endpoints#label-managing-access-token-scope-on-azure)

## Optional arguments

`delay_time`
:   Specifies the number of minutes to wait before enforcing the private endpoint registration.

    Range: 0 to 1440 minutes (24 hours)

    0 minutes: The registration is enforced immediately.

    Default: 60 (1 hour)

    For more information about the delay time and enforcement, see [Manage enforcement with the delay time argument](/user-guide/pin-private-endpoints#label-pin-private-endpoint-delay-time).

## Returns

Returns a status message about the registration of the private connectivity endpoint.

If you specify a delay time, the function returns a message stating when the registration will be enforced, with a reminder that when you
pin multiple accounts to the same private endpoint the enforcement is based on the earliest registration.

## Usage notes

- Only account administrators (users with the ACCOUNTADMIN role) can call this function.
- You can register multiple private connectivity endpoints for your Snowflake account.

## Examples

Call the [SYSTEM$REGISTER\_PRIVATELINK\_ENDPOINT](/sql-reference/functions/system_register_privatelink_endpoint) system function to register the VPC endpoint with your
Snowflake account. The `token` arguments contain truncated values and the delay time unit is minutes:

**AWS**

Copy code

```
SELECT SYSTEM$REGISTER_PRIVATELINK_ENDPOINT(
  'vpce-0c1...',
  '123.....',
  '{
    "Credentials": {
      "AccessKeyId": "ASI...",
      "SecretAccessKey": "alD...",
      "SessionToken": "IQo...",
      "Expiration": "2024-12-10T08:20:20+00:00"
    },
    "FederatedUser": {
      "FederatedUserId": "0123...:snowflake",
      "Arn": "arn:aws:sts::174...:federated-user/snowflake"
    },
    "PackedPolicySize": 9,
    }',
  120
  );
```

**Azure**

Copy code

```
SELECT SYSTEM$REGISTER_PRIVATELINK_ENDPOINT(
  '123....',
  '/subscriptions/0cc51670-.../resourceGroups/dbsec_test_rg/providers/Microsoft.Network/
  privateEndpoints/...',
  'eyJ...',
  120
);
```
