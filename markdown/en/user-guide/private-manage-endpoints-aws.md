# Manage private connectivity endpoints: AWS

[Business Critical Feature](/user-guide/intro-editions)

This feature requires Business Critical (or higher).

To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This topic provides information on how to manage private connectivity endpoints for use with outbound private connectivity to AWS.

## Provision private connectivity endpoints

Note

AWS doesn’t support cross-region VPC interface endpoints for the Amazon S3 service. Therefore, cross-region PrivateLink isn’t supported
for outbound connectivity to external stages and volumes that use the Amazon S3 service.

Cross-region support for AWS PrivateLink isn’t available in government regions or in the People’s Republic of China.

You can use the [SYSTEM$PROVISION\_PRIVATELINK\_ENDPOINT](/sql-reference/functions/system_provision_privatelink_endpoint) system function to create a private connectivity
endpoint by specifying the service or resource, and the host name. You must use the ACCOUNTADMIN role when you use this system function.

Note

If you use private connectivity for an external stage or external volume, you must use the wildcard character `*` when you specify
the host name. Using the wildcard doesn’t mean that all Amazon S3 buckets are accessed over a private connection. Only buckets referenced
by a Snowflake object that is enabled for private connectivity — that is, the external stage or external volume — can be accessed
through the VPC endpoint.

For example, to create a PrivateLink endpoint that connects to Amazon S3, execute the following SQL statement to configure an endpoint for
`us-west-2`:

Copy code

```
SELECT SYSTEM$PROVISION_PRIVATELINK_ENDPOINT(
  'com.amazonaws.us-west-2.s3',
  '*.s3.us-west-2.amazonaws.com'
);
```

Note

When you configure an endpoint for Amazon S3 or another platform as a service (PaaS), such as KMS, that service must be in the same region
as your Snowflake account.

The SYSTEM$PROVISION\_PRIVATELINK\_ENDPOINT function accepts a provider service name and host name as its arguments. You can obtain these
values by using the `describe-vpc-endpoint-services` subcommand from the AWS command line. As described in the
[AWS documentation](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/ec2/describe-vpc-endpoint-services.html), this AWS
subcommand returns a JSON object with a `ServiceName` field and a `PrivateDnsName` field. Use the following table to determine
which values to use for the SYSTEM$PROVISION\_PRIVATELINK\_ENDPOINT function:

| SYSTEM$PROVISION\_PRIVATELINK\_ENDPOINT argument | `describe-vpc-endpoint-services` output |
| --- | --- |
| `provider_service_name` | `ServiceName` |
| `host_name` | `PrivateDnsName`  If you use private connectivity for external stages or external volumes, you must use the value with a wildcard. |

Expand

Show lessSee more

You can create a private connectivity endpoint to a VPC endpoint service in an AWS region that is different from your Snowflake region.
If you do, ensure that the VPC endpoint service supports the Snowflake region. For information about finding the region names for your account,
see [Find the cloud-provider’s name of the region for your account](/user-guide/admin-security-privatelink#label-find-csp-region-name).

Important

*Before* you specify the `provider_service_name` as an argument for the SYSTEM$PROVISION\_PRIVATELINK\_ENDPOINT function, refer to the
Cross-Region Connectivity Pricing section on the [AWS PrivateLink pricing](https://aws.amazon.com/privatelink/pricing) page to determine
the appropriate region.

If the target service is a [VPC endpoint service](https://docs.aws.amazon.com/vpc/latest/privatelink/privatelink-share-your-services.html), the endpoint service must allow Snowflake
to connect to it. Before you create an endpoint, add the value of `privatelink-account-principal`
from the output of [SYSTEM$GET\_PRIVATELINK\_CONFIG](/sql-reference/functions/system_get_privatelink_config) as an [allowed principal](https://docs.aws.amazon.com/vpc/latest/privatelink/configure-endpoint-service.html#add-remove-permissions) of the VPC endpoint service.

The following SQL statement configures an endpoint to a VPC endpoint service:

Copy code

```
SELECT SYSTEM$PROVISION_PRIVATELINK_ENDPOINT(
  'com.amazonaws.vpce.us-west-2.vpce-svc-012345678910f1234',
  'my.onprem.storage.com'
);
```

Note

In this example, the service might be in different region from your Snowflake account.

After you create an endpoint, there is a delay before you can use the endpoint. For information about checking the status of a created
endpoint, see [SYSTEM$GET\_PRIVATELINK\_ENDPOINTS\_INFO](/sql-reference/functions/system_get_privatelink_endpoints_info).

## Set up connectivity to an endpoint that can’t be accessed directly

Not every service allows Snowflake to connect directly to specific instances through an interface endpoint. In these cases, you can
instead enable access to the service by
[setting up a proxy and exposing the service as a VPC endpoint service](#label-private-link-external-access-aws-proxy).

For a walkthrough specific to Amazon RDS, see the blog post
[Connecting To Amazon RDS Using Private Connectivity from Snowflake](https://medium.com/snowflake/connecting-to-amazon-rds-using-private-connectivity-from-snowflake-c2b538d623ed).

### Discover whether a service is available for direct access

Snowflake can usually access an AWS service directly through private connectivity if one of the following is true:

- The DNS name of the service—its `PrivateDnsName` value from the output of AWS
  [DescribeVpcEndpointServices](https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeVpcEndpointServices.html)—is
  prefixed with a wildcard.

  If the service’s DNS name starts with a wildcard character `*`, it’s likely that AWS supports directly accessing individual resources on
  that service. The DNS name is usually in this form:

  Copy code

  ```
  *.<service>.<region>.amazonaws.com
  ```
- The service is purely data-plane. [AWS Bedrock Runtime](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_Operations_Amazon_Bedrock_Runtime.html)
  is an example.

  To discover this about a given service, see the AWS documentation and blog posts.

### Access a service when direct access is not available

When a service is not available through direct access via an interface endpoint, you can enable access to the service by setting up
a proxy and exposing the service as a VPC endpoint service.

Examples of such services include the following:

- Amazon EC2 instances at `ec2.us-west-2.amazonaws.com`
- Amazon Relational Database Service (RDS) servers at `rds.us-west-2.amazonaws.com`

#### Set up AWS for access through a proxy

To expose a service instance through a proxy, you set up a virtual private cloud (VPC) and load balancer on AWS, then create a Snowflake
private link endpoint using the service name and load balancer DNS name of the AWS endpoint service.

The following describes the basic steps:

1. On AWS, create a [virtual private cloud (VPC)](https://docs.aws.amazon.com/vpc/latest/userguide/create-vpc.html) with subnets
   spanning three different availability zones.

   Choose initial availability zones (for example, az1 and az2) for your resources; Snowflake might not support newer AZs in some regions. Ensure
   that endpoints and other resources are created in the same availability zones to avoid cross-zone traffic.
2. In network settings for the service instance you want to access, ensure that the instance is in the VPC you created.
3. Create a [target group](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/create-target-group.html) that contains the
   service instance you want to access.
4. Create a [network load balancer](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/create-network-load-balancer.html)
   that forwards traffic to the target group you created.
5. Create an [endpoint service](https://docs.aws.amazon.com/vpc/latest/privatelink/configure-endpoint-service.html) with the network
   load balancer you created.

   Record the endpoint service name—`endpoint_service_name`—for use when setting up Snowflake for access to the service.
6. In Snowflake, execute the following query to retrieve the Snowflake account principal to allow the creation of endpoints:

   Copy code

   ```
   SELECT key, value FROM TABLE(FLATTEN(INPUT => PARSE_JSON(SYSTEM$GET_PRIVATELINK_CONFIG())));
   ```
7. From the results of the query, locate the `privatelink-account-principal` key and note its value.
8. On AWS, for the endpoint service you created, update the **Allow principals** section to add a principal whose ARN is the
   `privatelink-account-principal` key value from Snowflake.
9. In Snowflake, [create a private endpoint](#label-private-link-external-access-aws-create-endpoints) to the AWS endpoint service
   you created.

   When you execute the SYSTEM$PROVISION\_PRIVATELINK\_ENDPOINT function, use the following values as arguments:

   | SYSTEM$PROVISION\_PRIVATELINK\_ENDPOINT argument | Value from AWS configuration |
   | --- | --- |
   | `provider_service_name` | AWS endpoint **Service name**—the `endpoint_service_name` value—from the details section of the endpoint service. |
   | `host_name` | **DNS Name** from the network load balancer you created. |

   Expand

   Show lessSee more
10. On AWS, approve the PrivateLink connection:
11. Navigate to the endpoint connections for the endpoint service you created.
12. Select the relevant endpoint connection in a pending state.
13. Click **Accept Endpoint Connection Request**.
14. Verify the endpoint status by running the following query.

Ensure that the endpoint status changed from `pendingAcceptance` to `available`.

Copy code

```
SELECT SYSTEM$GET_PRIVATELINK_ENDPOINTS_INFO();
```

## Change the host name of a private connectivity endpoint

You can change only the host name of a previously provisioned, private connectivity endpoint without changing its network resource.
Changing the host name for an endpoint tells Snowflake that this endpoint now connects to the same service by using a different host name. To
change the host name, call the [SYSTEM$SET\_PRIVATELINK\_ENDPOINT\_HOSTNAME](/sql-reference/functions/system_set_privatelink_endpoint_hostname) system function.

## Remove a private connectivity endpoint to services

You can use the [SYSTEM$DEPROVISION\_PRIVATELINK\_ENDPOINT](/sql-reference/functions/system_deprovision_privatelink_endpoint) system function to remove a private connectivity
endpoint by specifying the service or resource.

After the endpoint is removed, the endpoint is put on a queue to be deleted after 7 days.

You need to use the ACCOUNTADMIN role when using this system function.

For example, to remove a PrivateLink with external access to Amazon S3, execute the following SQL statement:

Copy code

```
SELECT SYSTEM$DEPROVISION_PRIVATELINK_ENDPOINT('com.amazonaws.us-west-2.s3');
```

## Restore a private connectivity endpoint to services

You can use the [SYSTEM$RESTORE\_PRIVATELINK\_ENDPOINT](/sql-reference/functions/system_restore_privatelink_endpoint) system function to restore a removed private connectivity
endpoint that is still on the deletion queue by specifying the service or resource. If the endpoint is not found on the deletion queue, then
you cannot restore the endpoint.

You need to use the ACCOUNTADMIN role when using this system function.

For example, to restore a PrivateLink with external access to Amazon S3, execute the following SQL statement:

Copy code

```
SELECT SYSTEM$RESTORE_PRIVATELINK_ENDPOINT('com.amazonaws.us-west-2.s3');
```

## List all private connectivity endpoints to services

You can use the [SYSTEM$GET\_PRIVATELINK\_ENDPOINTS\_INFO](/sql-reference/functions/system_get_privatelink_endpoints_info) system function to list all private connectivity
endpoints, and information about the endpoints, in your account.

You need to use the ACCOUNTADMIN role when using this system function.

For example, to list all AWS PrivateLink endpoints with AWS services, execute the following SQL statement:

SQLReturned value

Copy code

```
SELECT SYSTEM$GET_PRIVATELINK_ENDPOINTS_INFO();
```

Copy code

```
[
  {
    "provider_service_name": "com.amazonaws.us-west-2.s3",
    "snowflake_endpoint_name": "vpce-123456789012abcdea",
    "endpoint_state": "CREATED",
    "host": "*.s3.us-west-2.amazonaws.com",
    "status": "Available"
  },
  ...
]
```

For a description of the fields of the JSON object returned by the function, see [Returns](/sql-reference/functions/system_get_privatelink_endpoints_info#label-get-private-endpoints-info-json).

Note

You can also query the [OUTBOUND\_PRIVATELINK\_ENDPOINTS](/sql-reference/account-usage/outbound_privatelink_endpoints) view in the
ACCOUNT\_USAGE schema to list the private endpoints in your account.
