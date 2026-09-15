# AWS VPC interface endpoints for internal stages

[Business Critical Feature](/user-guide/intro-editions)

This feature requires Business Critical (or higher).

To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This topic provides concepts as well as detailed instructions for connecting to Snowflake internal stages through AWS VPC Interface
Endpoints.

## Overview

AWS [VPC interface endpoints](https://docs.aws.amazon.com/vpc/latest/privatelink/endpoint-services-overview.html) and
[AWS PrivateLink for Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/privatelink-interface-endpoints.html) can be
combined to provide secure connectivity to Snowflake internal stages. This setup ensures that data loading and data unloading operations to
Snowflake internal stages use the AWS internal network and do not take place over the public Internet.

Prior to AWS supporting VPC interface endpoints for internal stage access, it was necessary to create a proxy farm within the AWS VPC to
facilitate secure access to Snowflake internal stages. With the added support of VPC interface endpoints for Snowflake internal stages,
users and client applications can now access Snowflake internal stages over the private AWS network. The following diagram summarizes this
new support:

![Connect to internal stage using AWS PrivateLink for S3](/static/images/internal-stage-private-connect-aws.png)

Note the following regarding the numbers in the BEFORE diagram:

- Users have two options to connect to a Snowflake internal stage:

  - Option A allows an on-premises connection directly to the internal stage as shown by the number 1.
  - Option B allows a connection to the internal stage through a proxy farm as shown by the numbers 2 and 3.
- If using the proxy farm, users can also connect to Snowflake directly as denoted by the number 4.

Note the following regarding the numbers in the AFTER diagram:

- The updates in this feature remove the need to connect to Snowflake or a Snowflake internal stage through a proxy farm.
- An on-premises user can connect to Snowflake directly as shown in number 5.
- To connect to a Snowflake internal stage, on-premises users connect to an interface endpoint, number 6, and then use AWS PrivateLink
  for Amazon S3 to connect to the Snowflake internal stage as shown in number 7.

There is a single Amazon S3 bucket per internal stage deployment. A
[prefix](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-prefixes.html) in the internal stage Amazon S3 bucket is used to
organize the data in each Snowflake account. The Amazon S3 bucket endpoint URLs are different depending on whether the connection to the
bucket uses private connectivity (i.e. AWS PrivateLink for S3).

Public Amazon S3 Global Endpoint URL:
:   `<bucket_name>.s3.region.amazonaws.com/prefix`

Private Amazon S3 Endpoint URL:
:   `<bucket_name>.<vpceID>.s3.<region>.vpce.amazonaws.com/prefix`

### Benefits

Implementing VPC interface endpoints to access Snowflake internal stages provides the following advantages:

- Internal stage data does not traverse the public Internet.
- Client and SaaS applications, such as Microsoft PowerBI, that run outside of the AWS VPC can connect to Snowflake securely.
- Administrators are not required to modify firewall settings to access internal stage data.
- Administrators can implement consistent security and monitoring regarding how users connect to storage accounts.

### Limitations

AWS doesn’t support cross-region VPC interface endpoints for the Amazon S3 service. Therefore, your VPC interface endpoint must be located in the same region as your Snowflake account to provide inbound connectivity to your Snowflake account’s internal stage.

Cross-region support for AWS PrivateLink isn’t available in government regions or in the People’s Republic of China.

Customers that use a SnowGov region for Federal Information Processing Standard (FIPS) compliance should be aware that AWS Privatelink for
Amazon S3 doesn’t support FIPS endpoints.

For more information about the AWS regions in which FIPS is enforced, see [Supported cloud regions](/user-guide/intro-regions).

For information about finding the region names for your account, see [Find the cloud-provider’s name of the region for your account](/user-guide/admin-security-privatelink#label-find-csp-region-name).

For more information about limitations of AWS PrivateLink, see the
[AWS documentation](https://docs.aws.amazon.com/AmazonS3/latest/userguide/privatelink-interface-endpoints.html#privatelink-limitations).

## Getting started

Before configuring AWS and Snowflake to allow requests to access a Snowflake internal stage via AWS PrivateLink, you must:

- [Meet the prerequisites](#label-aws-privatelink-internal-stage-prerequisites).
- [Choose the implementation strategy](#label-aws-privatelink-internal-stage-choose-strategy) that fits your environment.

### Prerequisites

- Set the [ENABLE\_INTERNAL\_STAGES\_PRIVATELINK](/sql-reference/parameters#label-enable-internal-stages-privatelink) parameter to enable support for connecting to an internal stage over AWS
  PrivateLink. For both implementation strategies discussed in this topic, the account administrator must execute:

  Copy code

  ```
  USE ROLE ACCOUNTADMIN;
  ALTER ACCOUNT SET ENABLE_INTERNAL_STAGES_PRIVATELINK = true;
  ```
- [AWS PrivateLink for S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/privatelink-interface-endpoints.html).

  > Important
  >
  > AWS PrivateLink for S3 is an AWS service that must be enabled in your cloud environment.
  >
  > For help with configuring and implementing this service, contact your internal AWS administrator.
- Update the firewall allow-listing as follows:

  - If using an outbound firewall, ensure that it allows all the URLs required by Snowflake. For details, see [SnowCD (Connectivity Diagnostic Tool)](/user-guide/snowcd).
- For `us-east-1` customers only: If using one of the following Snowflake clients to connect to Snowflake, please upgrade to the
  client version as follows:

  - JDBC driver: 3.13.3 (or higher)
  - ODBC driver: 2.23.2 (or higher)
  - Python Connector for Snowflake: 2.5.1 (or higher)
  - SnowSQL: 1.2.17 (or higher)
    - Upgrade SnowSQL before using this feature. For more information, see [Installing SnowSQL](/user-guide/snowsql-install-config).
    - Starting with version 1.3.0, SnowSQL disables automatic upgrades by default to avoid potential issues that can affect production environments when an automatic upgrade occurs. To upgrade, you should download and install new versions manually, preferably in a non-production environment. Snowflake recommends you leave this setting disabled, but you can manually enable the auto-upgrade behavior by configuring the SnowSQL `noup` [option](/user-guide/snowsql-install-config#label-snowsql-enable-auto-upgrade) option.

### Choosing an implementation strategy

Choosing the right implementation strategy depends on whether your organization is using AWS PrivateLink to access a single internal stage
or multiple internal stages.

- If your organization is accessing the internal stage of a single account, see [Accessing an internal stage with an interface endpoint](#label-aws-privatelink-internal-stage-procedure).
- If your organization is accessing the internal stages of multiple accounts, see
  [Accessing Internal stages with dedicated interface endpoints](#label-aws-privatelink-internal-stage-network-isolation). This strategy uses multiple interface endpoints to connect, one for each
  internal stage.

## Accessing an internal stage with an interface endpoint

Snowflake recommends the following implementation strategy when your organization accesses the internal stage of a *single account*. If you
plan to access multiple internal stages from your VPC, see [Accessing Internal stages with dedicated interface endpoints](#label-aws-privatelink-internal-stage-network-isolation).

To configure a VPC interface endpoint to access a Snowflake internal stage, it is necessary to have support from the following three roles in
your organization:

1. The Snowflake account administrator (that is, a user with the Snowflake ACCOUNTADMIN system role).
2. The AWS administrator.
3. The network administrator.

Depending on the organization, it might be necessary to coordinate the configuration efforts with more than one person or team to implement
the following configuration steps.

### Procedure

Complete the following steps to configure and implement secure access to a Snowflake internal stage through a VPC endpoint:

1. As a Snowflake account administrator, execute the following statements in your Snowflake account and record the value defined by the
   `privatelink_internal_stage` key. Note that the Amazon S3 bucket name is defined in the first segment of the URL when read from left
   to right. For more information, see [ENABLE\_INTERNAL\_STAGES\_PRIVATELINK](/sql-reference/parameters#label-enable-internal-stages-privatelink) and
   [SYSTEM$GET\_PRIVATELINK\_CONFIG](/sql-reference/functions/system_get_privatelink_config).

   Copy code

   ```
   USE ROLE ACCOUNTADMIN;
   ALTER ACCOUNT SET ENABLE_INTERNAL_STAGES_PRIVATELINK = true;
   select key, value from table(flatten(input=>parse_json(system$get_privatelink_config())));
   ```
2. As the AWS administrator, create a VPC endpoint for AWS PrivateLink for S3 using the AWS Console. Record the VPCE DNS Name for use in
   the next step; do not record any VPCE DNS zonal names.

   The VPCE DNS Name can be found by
   [describing an interface endpoint](https://docs.aws.amazon.com/vpc/latest/privatelink/vpce-interface.html#describe-interface-endpoint)
   once the endpoint is created.

   In this example, a wildcard (i.e. `*`) is listed as the leading character in the VPCE DNS Name. Replace the leading wildcard with the
   Amazon S3 bucket name from the previous step. For example:

   Replace:
   :   `*.vpce-000000000000a12-abc00ef0.s3.us-west-2.vpce.amazonaws.com`

   With:
   :   `<bucket_name>.vpce-000000000000a12-abc00ef0.s3.us-west-2.vpce.amazonaws.com`
3. As the network administrator, update the DNS settings to resolve the following URL:

   `<bucket_name>.s3.<region>.amazonaws.com` to the VPCE DNS name after the leading wildcard is replaced with the Amazon S3 bucket name.

   In this example, resolve `<bucket_name>.s3.<region>.amazonaws.com` to
   `<bucket_name>.vpce-000000000000a12-abc00ef0.s3.us-west-2.vpce.amazonaws.com`.

   Tip

   - Do not use wildcard characters (i.e. `*`) with DNS mapping because of the possible impact of accessing other Amazon S3 buckets outside
     of Snowflake.
   - Use a separate Snowflake account for testing, and configure a private hosted DNS zone in a test VPC to test the feature so that the
     testing is isolated and does not impact your other workloads.
   - If using a separate Snowflake account is not possible, use a test user to access Snowflake from a test VPC where the DNS changes are
     made.
   - To test from on-premises applications, use DNS forwarding to forward requests to the AWS private hosted zone in the VPC where the DNS
     settings are made. If there are client applications in both the VPC and on-premises, use AWS Transit Gateway.
   - Execute the following command from the client machine to verify that the IP address returned is the private IP
     address for the storage account:

     Copy code

     ```
     dig <bucket_name>.s3.<region>.amazonaws.com
     ```
4. For Snowflake accounts in `us-east-1`, verify your Snowflake clients are on their latest versions.

## Accessing Internal stages with dedicated interface endpoints

Snowflake recommends the following implementation strategy when your organization accesses the internal stages of *multiple accounts*.

The [S3\_STAGE\_VPCE\_DNS\_NAME](/sql-reference/parameters#label-s3-stage-vpce-dns-name) parameter allows users to associate a Snowflake account with the DNS name
of an Amazon S3 interface endpoint. This allows organizations with multiple Snowflake accounts in an AWS deployment to associate each
internal stage with a different interface endpoint. When each internal stage has its own interface endpoint, network traffic to a specific
internal stage is isolated from network traffic to other internal stages.

Before continuing, make sure you have [met the prerequisites](#label-aws-privatelink-internal-stage-prerequisites).

### Benefits

The strategy in which an internal stage within an AWS deployment has a dedicated Amazon S3 interface endpoint has the following benefits:

Security:
:   Each account can have a different security strategy because individual interface endpoints can have different security
    configurations.

Chargeback models:
:   Companies can isolate network traffic based on the type of account (for example, production vs. development), and attribute
    costs associated with data flowing through an endpoint to the correct account.

DNS Management:
:   The DNS name of an Amazon S3 interface endpoint is a globally unique name that locates the specific endpoint within a specific
    region. AWS automatically registers this DNS name in its public DNS service, meaning it is publicly resolvable. For these reasons, an
    administrator does not need to do any additional DNS configuration to route traffic through an Amazon S3 interface endpoint to an internal
    stage. For example, the administrator does not need to set up a private hosted zone (PHZ) when configuring the Amazon Route 53
    DNS service or register a DNS name to point to an endpoint.

### Configuration

The network isolation strategy consists of the following:

1. In AWS, an administrator creates a new Amazon S3 interface endpoint for every Snowflake account in the organization. For example, if an
   organization has two accounts in the Snowflake deployment, the administrator creates two interface endpoints.
2. In Snowflake, an administrator uses the S3\_STAGE\_VPCE\_DNS\_NAME parameter to associate each Snowflake account with the DNS name of its
   dedicated interface endpoint. All traffic to the account’s internal stage goes through this interface endpoint.

#### AWS configuration

In your VPC as an AWS administrator:

1. [Create a separate Amazon S3 interface endpoint](https://docs.aws.amazon.com/vpc/latest/privatelink/create-interface-endpoint.html#create-interface-endpoint-aws)
   for each of your Snowflake accounts.
2. For each of these endpoints, use the AWS VPC Management Console to:
   1. Open the endpoint to view its **Details**.
   2. Find the **DNS Names** field, and copy the region-scoped DNS name. The Snowflake S3\_STAGE\_VPCE\_DNS\_NAME parameter will be set to
      this value.

      The format of the region-scoped DNS name looks like `*.vpce-sd98fs0d9f8g.s3.us-west-2.vpce.amazonaws.com`. Though AWS also provides
      an availability zone DNS name, Snowflake recommends the region-scoped DNS name because it provides high availability with failover
      capabilities.

#### Snowflake configuration

After the AWS administrator creates the interface endpoint for a Snowflake account’s internal stage, the Snowflake administrator can
use the S3\_STAGE\_VPCE\_DNS\_NAME parameter to associate the DNS name of that endpoint with the account.

The S3\_STAGE\_VPCE\_DNS\_NAME parameter should be set to the region-scoped DNS Name of the interface endpoint associated with a specific
internal stage. The standard format begins with an asterisk (`*`) and ends with `vpce.amazonaws.com`
(for example, `*.vpce-sd98fs0d9f8g.s3.us-west-2.vpce.amazonaws.com`).

As an example, the account administrator can execute the following to associate an endpoint with the current account:

Copy code

```
ALTER ACCOUNT SET S3_STAGE_VPCE_DNS_NAME = '*.vpce-sd98fs0d9f8g.s3.us-west2.vpce.amazonaws.com';
```

#### User overrides of interface endpoints

Snowflake supports user-level overrides within accounts that use [gateway endpoints for Amazon S3](https://docs.aws.amazon.com/vpc/latest/privatelink/vpc-endpoints-s3.html).
If your organization has applications (typically, users with the `TYPE` property set to `SERVICE`) running in the cloud that use S3
gateway endpoints to access internal stages, you can preserve DNS isolation (use S3 interface endpoints) at the account level, while allowing
specific service users in the same account to use S3 gateway endpoints. After [setting dedicated interface endpoints](#label-aws-privatelink-internal-stage-network-isolation)
for each account, set an override for each user that you want to use the default S3 gateway endpoint.

For example, to associate a service user session with an internal stage that is being accessed through an Amazon S3 gateway endpoint, run the
following ALTER USER command:

Copy code

```
ALTER USER service1 SET S3_STAGE_VPCE_DNS_NAME = 's3-gateway-vpce-default';
```

`s3-gateway-vpce-default` is a reserved token used by the runtime to override the internal stage access and route session traffic through
the S3 gateway endpoint.

### Final DNS value

The final DNS name associated with an account has the form: `<bucketname>.bucket.vpce-<vpceid>.s3.<region>.vpce.amazonaws.com`

Where:

- `<bucketname>` is the name of the internal stage’s Amazon S3 bucket.
- `<vpceid>` is the unique identifier of the Amazon S3 interface endpoint associated with the account.
- `<region>` is the [cloud region](/user-guide/intro-regions) that hosts your Snowflake account.

The final DNS name appears in logs for each driver that connects to the internal stage.
