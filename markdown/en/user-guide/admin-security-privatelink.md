# AWS PrivateLink and Snowflake

[Business Critical Feature](/user-guide/intro-editions)

This feature requires Business Critical (or higher).

This topic describes how to configure AWS PrivateLink to directly connect your Snowflake account to one or more AWS Virtual Private Clouds (VPCs).

## AWS PrivateLink: Overview

[AWS PrivateLink](https://docs.aws.amazon.com/aws-technical-content/latest/aws-vpc-connectivity-options/aws-privatelink.html) is an AWS
service for creating private VPC endpoints that allow direct, secure connectivity between your AWS VPCs and the Snowflake VPC without
traversing the public internet. PrivateLink controls inbound connectivity from your network to Snowflake. To reach private data sources
from Snowflake (outbound), see [Data Connectivity Proxy](/user-guide/data-connectivity-proxy). AWS PrivateLink connectivity supports VPC endpoint services and AWS VPCs that are located in the same or in
different AWS regions. Cross-region connectivity for AWS PrivateLink allows you to use a custom endpoint service to connect a Snowflake account
in a region that is different from your AWS VPC region. Cross-region connectivity isn’t currently supported for any platform as a service (PaaS)
services, such as Amazon Simple Storage Service (Amazon S3) or key management service (KMS).

For more information, see the AWS blog page, [Introducing Cross-Region Connectivity for AWS PrivateLink](https://aws.amazon.com/blogs/networking-and-content-delivery/introducing-cross-region-connectivity-for-aws-privatelink). For information about finding the region names for your account, see [Find the cloud-provider’s name of the region for your account](#label-find-csp-region-name).

When [writing external functions](/sql-reference/external-functions), you can also use AWS PrivateLink with
[private endpoints](/sql-reference/external-functions-creating-aws-planning#label-external-functions-aws-endpoint-type).

If you have an on-premises environment, such as a non-hosted data center, you can use [AWS Direct Connect](https://aws.amazon.com/directconnect/)
with AWS PrivateLink to connect all your virtual and physical environments in a single, private network.

Note

AWS Direct Connect is a separate AWS service that must be implemented independently from AWS PrivateLink and is outside the scope of this
topic. To inquire about implementing AWS Direct Connect, please contact Amazon.

## Enable AWS PrivateLink

Note

The self-service enablement process in this section *doesn’t* currently support authorizing an AWS account identifier from a managed
cloud service or a third-party vendor.

To authorize an AWS account identifier for this use case, please retrieve the AWS account identifier from the vendor, and then contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

To enable AWS PrivateLink for your Snowflake account, complete the following steps:

1. Generate a federated token, and then save the output.

   1. To generate a token, run the [AWS CLI STS](https://docs.aws.amazon.com/cli/latest/reference/sts/get-federation-token.html) command
      on the command line.
      `get-federation-token` requires either an identity and access management user in AWS or the AWS account root
      user. For details, refer to the [AWS documentation](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_request.html#stsapi_comparison).

      Important

      The federated token expires after 12 hours. If you call any of the system functions to authorize, verify, or disable your
      Snowflake account to use AWS PrivateLink and the token has expired, regenerate the token by running the AWS CLI STS command again.

      Copy code

      ```
      aws sts get-federation-token --name sam
      ```

      In a later step, you provide the output of this command as the `federated_token` argument for the SYSTEM$AUTHORIZE\_PRIVATELINK function.
   2. From your generated token, extract the value of the `"FederatedUserId"` field.
      For example, if your token contains the following values:

      Copy code

      ```
      {
       ...
         "FederatedUser": {
           "FederatedUserId": "185...:sam",
           "Arn": "arn:aws:sts::185...:federated-user/sam"
         },
       "PackedPolicySize": 0
      }
      ```

      Extract `185...`. In the next step, you provide this 12-digit number as the `aws_id` argument for the SYSTEM$AUTHORIZE\_PRIVATELINK function.
2. Using the ACCOUNTADMIN Snowflake system role, call the
   [SYSTEM$AUTHORIZE\_PRIVATELINK](/sql-reference/functions/system_authorize_privatelink) function to *authorize* (enable) AWS PrivateLink for your
   Snowflake account:

   Copy code

   ```
   SELECT SYSTEM$AUTHORIZE_PRIVATELINK ( '<aws_id>' , '<federated_token>' );
   ```

   Where:

   - `'aws_id'`

     The 12-digit identifier that uniquely identifies your Amazon Web Services (AWS) account, as a string.
   - `'federated_token'`

     The federated token value that contains access credentials for a federated user as a string.

   For example:

   Copy code

   ```
   USE ROLE ACCOUNTADMIN;

   SELECT SYSTEM$AUTHORIZE_PRIVATELINK (
     '185...',
    '{
      "Credentials": {
        "AccessKeyId": "ASI...",
        "SecretAccessKey": "enw...",
        "SessionToken": "Fwo...",
        "Expiration": "2021-01-07T19:06:23+00:00"
      },
      "FederatedUser": {
        "FederatedUserId": "185...:sam",
        "Arn": "arn:aws:sts::185...:federated-user/sam"
      },
      "PackedPolicySize": 0
     }'
     );
   ```

   To verify your configuration, call the [SYSTEM$GET\_PRIVATELINK](/sql-reference/functions/system_get_privatelink) function in your Snowflake account on AWS.
   This function uses the same argument values for `'aws_id'` and `'federated_token'` that were used
   to authorize your Snowflake account.

   SYSTEM$GET\_PRIVATELINK returns `Account is authorized for PrivateLink.` for a successful authorization.
3. Optional: If you need to *disable* AWS PrivateLink in your Snowflake account, call the [SYSTEM$REVOKE\_PRIVATELINK](/sql-reference/functions/system_revoke_privatelink)
   function by using the same argument values for `'aws_id'` and `'federated_token'`.

To further harden your security posture, Snowflake recommends pinning private endpoints for your Snowflake account. For more information, see
[Pinning private connectivity endpoints for inbound traffic](/user-guide/pin-private-endpoints).

## Configure your AWS VPC environment

Attention

This section covers only the Snowflake-specific details for configuring your VPC environment.

Snowflake isn’t responsible for the actual configuration of the required AWS VPC endpoints, security group rules, and Domain Name
System (DNS) records. If you encounter issues with any of these configuration tasks, please contact AWS Support.

### Create and configure your AWS VPC endpoint

To create and configure a VPC endpoint in your AWS VPC environment, complete the following steps:

1. In your Snowflake account, use the ACCOUNTADMIN system role to call the
   [SYSTEM$GET\_PRIVATELINK\_CONFIG](/sql-reference/functions/system_get_privatelink_config) function, and then record the `privatelink-vpce-id` value.
2. In your AWS environment, create a VPC endpoint by using the `privatelink-vpce-id` value from the previous step.

   Note

   If the Snowflake region of your VPC endpoint is different from the region of your AWS VPC, you must make two selections that enable
   cross-region connectivity. In the AWS VPC Console, select **Enable Cross Region endpoint**, and then select the primary region of
   the service in **Service Settings** » **Service Region**.

   For complete instructions, see the step-by-step setup procedure for [configuring cross-region connectivity](https://aws.amazon.com/blogs/networking-and-content-delivery/introducing-cross-region-connectivity-for-aws-privatelink/) in the AWS documentation.

   For instructions that describe how to find the region name of your account, see [Find the cloud-provider’s name of the region for your account](#label-find-csp-region-name).
3. In your AWS environment, authorize a security group of services that connect the Snowflake outgoing connection to port `443` and
   `80` of the VPCE CIDR (Classless Inter-Domain Routing).

For more information, see the following topics in the AWS documentation:

- [Working with VPCs and subnets](https://docs.aws.amazon.com/vpc/latest/userguide/working-with-vpcs.html)
- [VPC endpoints](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-endpoints.html)
- [VPC endpoint services (AWS PrivateLink)](https://docs.aws.amazon.com/vpc/latest/userguide/endpoint-service.html)
- [Security groups for your VPC](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html)

### Find the cloud-provider’s name of the region for your account

Snowflake and the cloud provider that hosts your Snowflake account use similar, but different names for the region that hosts the Snowflake
service. You can use system functions to find region names that you use to establish connectivity across regions. To determine the cloud-provider’s
name of the region that hosts your Snowflake account, take the following steps:

1. Run the [CURRENT\_REGION](/sql-reference/functions/current_region) and [SHOW REGIONS](/sql-reference/sql/show-regions) commands.
2. In the output returned by SHOW REGIONS, find a row that shows a value in the *snowflake\_region column* that matches the output returned
   by SELECT CURRENT\_REGION().

   The value in this row’s *region* column is the cloud-provider’s name of the region that hosts your Snowflake account.

In the following example, *us-west-2* is the cloud-provider’s name of the region that hosts the Snowflake account named *AWS\_US\_WEST*.

Copy code

```
SELECT CURRENT_REGION();
```

Output:

Copy code

```
+------------------+
| CURRENT_REGION() |
|------------------|
| AWS_US_WEST_2    |
+------------------+
```

Copy code

```
SHOW REGIONS;
```

Output:

Copy code

```
+------------------+-------+-----------+-----------------+
| snowflake_region | cloud | region    | display_name    |
|------------------|-------|-----------|-----------------|
| AWS_US_WEST_2    | aws   | us-west-2 | US West (Oregon)|
+------------------+-------+-----------+-----------------+
```

### Configure your VPC network

To access Snowflake by using an AWS PrivateLink endpoint, you must create Canonical Name (CNAME) records in your DNS to resolve the appropriate
endpoint values from the [SYSTEM$GET\_PRIVATELINK\_CONFIG](/sql-reference/functions/system_get_privatelink_config) function to the DNS name of your VPC endpoint.

The values to obtain from the output of SYSTEM$GET\_PRIVATELINK\_CONFIG depend on which Snowflake features you access using private
connectivity. For a description of the possible values, see [Return values](/sql-reference/functions/system_get_privatelink_config#label-get-privatelink-config-output).

Note that the values for `regionless-snowsight-privatelink-url` and `snowsight-privatelink-url` allow access to
Snowsight and the Snowflake Marketplace using private connectivity. However, there is additional configuration if you want to enable
URL redirects. For information, see [Snowsight & Private Connectivity](/user-guide/ui-snowsight-gs#label-ui-snowsight-gs-private-connectivity).

For additional help with DNS configuration, please contact your internal AWS administrator.

Important

The structure of the Online Certificate Status Protocol (OCSP) cache server host name depends on the version of your installed clients,
as described in [Configure your Snowflake clients](#label-conf-snf-clients):

- If you use the listed version or a later version, use the format shown in [Configure your Snowflake clients](#label-conf-snf-clients), which enables better DNS
  resolution when you have multiple Snowflake accounts — for example, dev, test, and production — in the same region. When updating
  client drivers and using OCSP with PrivateLink, update the firewall rules to allow the OCSP host name.
- If you use an earlier client version, then the OCSP cache server host name takes the form `ocsp.region_id.privatelink.snowflakecomputing.com`
  without an [account identifier](/user-guide/admin-account-identifier).
- Your DNS record must resolve to private IP addresses within your VPC. If it resolves to public IP addresses, the record isn’t configured
  correctly.

### Create AWS VPC interface endpoints for Amazon S3

This step is required for Amazon S3 traffic from Snowflake clients to stay on the AWS backbone. The Snowflake clients
(such as Snowflake CLI, SnowSQL, JDBC driver, and so on) require access to Amazon S3 to perform various runtime operations.

If your AWS VPC network doesn’t allow access to the public internet, you can configure private connectivity to internal stages or more
gateway endpoints to the Amazon S3 host names required by the Snowflake clients.

There are three options to configure access to Amazon S3. The first two options avoid the public internet and the third option
uses the public internet:

- Configure an AWS VPC interface endpoint for [internal stages](/user-guide/private-internal-stages-aws) or for [Snowflake-managed storage volumes](/user-guide/private-managed-volumes-aws) if you use
  Apache Iceberg tables with Snowflake-managed storage. This option is recommended.
- Configure an Amazon S3 gateway endpoint. For more information, see the following Attention section.
- Don’t configure an interface endpoint or a gateway endpoint. This results in access that uses the public internet.

Attention

To prevent communications between an Amazon S3 bucket and an AWS VPC with Snowflake from using the public internet, you can set up an
Amazon S3 gateway endpoint in the same AWS region as the Amazon S3 bucket. This prevents communications on the public internet because
AWS PrivateLink only allows communications between VPCs, and the Amazon S3 bucket isn’t included in the VPC.

You can configure the Amazon S3 gateway endpoint to limit access to specific users, Amazon S3 resources, routes, and subnets; however,
Snowflake doesn’t require this configuration. For more information, see
[Gateway endpoints for Amazon S3](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-endpoints-s3.html).

To limit Amazon S3 gateways to use only Amazon S3 resources for Snowflake, choose one of the following options:

- Use the specific Amazon S3 host name addresses that are used by your Snowflake account in your AWS endpoint policies. For the complete list of
  host names that are used by your account, see [SYSTEM$ALLOWLIST](/sql-reference/functions/system_allowlist).
- Use an Amazon S3 host name pattern that matches the Snowflake S3 host names in your AWS endpoint policies. With this option, there are
  two possible types of connections to Snowflake: VPC-to-VPC or On-Premises-to-VPC.

  Based on your connection type, complete the following instructions:

  VPC-to-VPC:
  :   Ensure that the Amazon S3 gateway endpoint exists. Optionally modify the Amazon S3 gateway endpoint policy to match the specific host
      name patterns that are shown in the following Amazon S3 Hostnames table.

  On-Premises-to-VPC:
  :   Define a setup to include the Amazon S3 host name patterns in the firewall or proxy configuration *if* Amazon S3 traffic isn’t
      permitted on the public gateway.

If you don’t require your gateway endpoints to explicitly match your account’s Snowflake-managed S3 buckets, you can use the Amazon S3 host
name patterns shown in the following table to create gateway endpoints:

> | Amazon S3 Hostnames | Notes |
> | --- | --- |
> | **All regions** |  |
> | `sfc-*-stage.s3.amazonaws.com:443` | None. |
> | **All regions other than US East** |  |
> | `sfc-*-stage.s3-<region_id>.amazonaws.com:443` | The pattern uses a hyphen (`-`) before the region ID. |
> | `sfc-*-stage.s3.<region_id>.amazonaws.com:443` | The pattern uses a period (`.`) before the region ID. |
>
> Expand
>
> Show lessSee more

For information about creating gateway endpoints, see [Gateway VPC endpoints](https://docs.aws.amazon.com/vpc/latest/userguide/vpce-gateway.html).

## Connect to Snowflake

Before you connect to Snowflake, you can *optionally* use the Snowflake Connectivity Diagnostic tool (SnowCD) to evaluate the
network connection with Snowflake and AWS PrivateLink.

For more information, see [SnowCD](/user-guide/snowcd) and [SYSTEM$ALLOWLIST\_PRIVATELINK](/sql-reference/functions/system_allowlist_privatelink).

Otherwise, connect to Snowflake with your private connectivity account [URL](/user-guide/organizations-connect#label-connecting-via-url).

If you want to connect to Snowsight through AWS PrivateLink, follow the instructions in the
[Snowsight documentation](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).

## Block public access — *Recommended*

After you test private connectivity to Snowflake by using AWS PrivateLink, you can optionally block public access to Snowflake. This
means that users can access Snowflake only if their connection request originates from an IP address within a particular CIDR block range
specified in a Snowflake network policy.

To block public access by using a network policy:

1. Create a new network policy or edit an existing network policy.
2. Add the CIDR block range for your organization.
3. If your organization uses IPv6, create an additional network rule with `TYPE = IPV6` and add it to the network
   policy. For more information, see [Network rules](/user-guide/network-rules).
4. Activate the network policy for your account.

For more information, see [Controlling network traffic with network policies](/user-guide/network-policies).

## Configure your Snowflake clients

The following sections describe how to configure Snowflake clients for specific use cases.

### Ensure Snowflake clients support OCSP cache server

The Snowflake OCSP cache server mitigates connectivity issues between Snowflake clients and the server. To enable your installed Snowflake
clients to use the OCSP server cache, ensure that you use the following client versions:

- Snowflake CLI 3.0.0 (or higher)
- SnowSQL 1.1.57 (or higher)
- Python Connector 1.8.2 (or higher)
- JDBC Driver 3.8.3 (or higher)
- ODBC Driver 2.19.3 (or higher)

Note

The Snowflake OCSP cache server listens on port `80`, which is why you were instructed in [Create and configure your AWS VPC endpoint](#label-create-and-configure-a-vpc-endpoint-vpce)
to configure your AWS PrivateLink VPCE security group to accept both port `80` and port `443`, which is required for all other
Snowflake traffic.

### Specify a host name for Snowflake clients

Each Snowflake client requires a host name to connect to your Snowflake account.

The host name is the same as the host name that you specified in the CNAME records in [Configure your VPC network](#label-aws-pl-additional-cname-records).

This step isn’t applicable to access the Snowflake Marketplace.

For example, for an account named `xy12345`:

- If the account is in US West, the host name is `xy12345.us-west-2.privatelink.snowflakecomputing.com`.
- If the account is in EU (Frankfurt), the host name is `xy12345.eu-central-1.privatelink.snowflakecomputing.com`.

Important

The method for specifying the host name differs depending on the client:

- For the Spark connector and the ODBC and JDBC drivers, specify the entire host name.
- For all the other clients, *don’t* specify the entire host name.
  Instead, specify the [account identifier](/user-guide/admin-account-identifier) with the `privatelink` segment, which is `<account_identifier>.privatelink`. Snowflake concatenates this name with `snowflakecomputing.com` to dynamically construct the host name.

For more information about specifying the account name or host name for a Snowflake client, see the documentation for each client.

## Using SSO with AWS PrivateLink

Snowflake supports using SSO with AWS PrivateLink. For more information, see:

- [SSO with private connectivity](/user-guide/admin-security-fed-auth-overview#label-sso-private-connectivity)
- [Using Snowflake OAuth with PrivateLink and SaaS clients](/user-guide/oauth-snowflake-overview#label-oauth-private-connectivity)

## Using Client Redirect with AWS PrivateLink

Snowflake supports using Client Redirect with AWS PrivateLink.

For more information, see [Redirecting client connections](/user-guide/client-redirect).

## Using replication and Tri-Secret Secure with private connectivity

Snowflake supports replicating your data from the source account to the target account, regardless of whether you enable
Tri-Secret Secure or this feature in the target account.

## Troubleshooting

To troubleshoot problems that you might come across with PrivateLink, see the following Snowflake Community articles:

- [How to retrieve a Federation Token from AWS for PrivateLink Self-Service](https://community.snowflake.com/s/article/How-to-retrieve-a-Federation-Token-from-AWS-for-PrivateLink-Self-Service)
- [FAQ: PrivateLink Self-Service with AWS](https://community.snowflake.com/s/article/PrivateLink-Self-Service-with-AWS)
- [Troubleshooting: Snowflake self-service functions for AWS PrivateLink](https://community.snowflake.com/s/article/Troubleshooting-Snowflake-self-service-functions-for-AWS-PrivateLink)
