# AWS VPC interface endpoints for Snowflake-managed storage volumes

This topic provides concepts and detailed instructions for connecting to Snowflake-managed storage volumes through AWS VPC
interface endpoints.

## Overview

When you use an external query engine such as Apache Spark to read from or write to an iceberg table that uses
Snowflake-managed storage, the query engine communicates directly with the native iceberg volume hosted on Amazon S3. By default,
this traffic can traverse the public internet.

For information about using Snowflake-managed storage volumes with Apache Iceberg™ tables, see
[Snowflake storage for Apache Iceberg™ tables](/user-guide/tables-iceberg-internal-storage).

[AWS PrivateLink for Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/privatelink-interface-endpoints.html) can
be combined with VPC interface endpoints to provide secure connectivity to the managed storage volume. This setup ensures that
read and write operations from your external query engine to the native iceberg volume use the AWS internal network instead of the
public internet.

### Benefits

Implementing VPC interface endpoints to access Snowflake-managed storage volumes provides the following advantages:

- Data doesn’t traverse the public internet when external query engines read from or write to the Snowflake-managed Iceberg volume.
- Client and SaaS applications, such as Microsoft Power BI, that run outside of the AWS VPC can connect to Snowflake securely.
- Administrators aren’t required to modify firewall settings to access volume data.
- Administrators can implement consistent security and monitoring for how query engines connect to storage.

### Limitations

AWS doesn’t support cross-region VPC interface endpoints for the Amazon S3 service. Therefore, your VPC interface endpoint must be
located in the same region as your Snowflake account to provide inbound connectivity to your Snowflake-managed
storage volume.

Cross-region support for AWS PrivateLink isn’t available in government regions or in the People’s Republic of China.

Customers that use a SnowGov region for Federal Information Processing Standard (FIPS) compliance should be aware that AWS PrivateLink for
Amazon S3 doesn’t support FIPS endpoints.

For more information about the AWS regions in which FIPS is enforced, see [Supported cloud regions](/user-guide/intro-regions).

For information about finding the region names for your account, see [Find the cloud-provider’s name of the region for your account](/user-guide/admin-security-privatelink#label-find-csp-region-name).

For more information about limitations of AWS PrivateLink, see the
[AWS documentation](https://docs.aws.amazon.com/AmazonS3/latest/userguide/privatelink-interface-endpoints.html#privatelink-limitations).

## Getting started

Before configuring AWS and Snowflake to allow requests to access a Snowflake-managed storage volume through AWS PrivateLink, you
must meet the prerequisites.

### Prerequisites

- [AWS PrivateLink for S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/privatelink-interface-endpoints.html).

  > Important
  >
  > AWS PrivateLink for S3 is an AWS service that must be enabled in your cloud environment.
  >
  > For help with configuring and implementing this service, contact your internal AWS administrator.
- Update the firewall allow-listing as follows:

  - If using an outbound firewall, ensure that it allows all the URLs required by Snowflake. For details, see [SnowCD (Connectivity Diagnostic Tool)](/user-guide/snowcd).
- For `us-east-1` customers only: If using one of the following Snowflake clients to connect to Snowflake, upgrade to the
  client version as follows:

  - JDBC driver: 3.13.3 (or higher)
  - ODBC driver: 2.23.2 (or higher)
  - Python Connector for Snowflake: 2.5.1 (or higher)
  - SnowSQL: 1.2.17 (or higher)
    - Upgrade SnowSQL before using this feature. For more information, see [Installing SnowSQL](/user-guide/snowsql-install-config).
    - Starting with version 1.3.0, SnowSQL disables automatic upgrades by default to avoid potential issues that can affect production environments when an automatic upgrade occurs. To upgrade, you should download and install new versions manually, preferably in a non-production environment. Snowflake recommends you leave this setting disabled, but you can manually enable the auto-upgrade behavior by configuring the SnowSQL `noup` [option](/user-guide/snowsql-install-config#label-snowsql-enable-auto-upgrade).

## Accessing a Snowflake-managed storage volume with an interface endpoint

To configure a VPC interface endpoint to access a Snowflake-managed storage volume, the following roles in your organization must
coordinate:

1. The Snowflake account administrator (that is, a user with the Snowflake ACCOUNTADMIN system role).
2. The AWS administrator.
3. The network administrator.

Depending on the organization, it might be necessary to coordinate the configuration efforts with more than one person or team to implement the following configuration steps.

### Procedure

Complete the following steps to configure and implement secure access to a Snowflake-managed storage volume through a VPC endpoint:

1. As the AWS administrator, create a VPC endpoint to S3 using the AWS Console. Record the VPCE DNS Name for
   use in the next step; do not record any VPCE DNS zonal names.

   The VPCE DNS Name can be found by
   [describing an interface endpoint](https://docs.aws.amazon.com/vpc/latest/privatelink/vpce-interface.html#describe-interface-endpoint)
   once the endpoint is created.

   Example VPCE DNS Name: `*.vpce-000000000000a12-abc00ef0.s3.us-west-2.vpce.amazonaws.com`
2. Configure your external query engine to use the VPCE DNS name directly. Replace the \*\*\* in the VPCE DNS name with *bucket*. For example, in Apache Spark:

   ```
   .config("spark.sql.catalog.<catalog_name>.s3.endpoint",
        "bucket.vpce-000000000000a12-abc00ef0.s3.us-west-2.vpce.amazonaws.com")
   ```

   Tip

   Use a separate Snowflake account for testing, and configure a private hosted DNS zone in a test VPC to test the feature so
   that the testing is isolated and doesn’t impact your other workloads.

## Blocking public access

After you configure VPC interface endpoints to access the managed storage volume through AWS PrivateLink, you can optionally
restrict access to the volume by using network rules and network policies. For more information about using network policies
to protect Snowflake-managed storage volumes, see
[Protecting Snowflake-managed storage volumes on AWS](/user-guide/network-policies#label-network-policies-rules-managed-volumes).

### Prerequisites

To use network rules to restrict access to a Snowflake-managed storage volume, the account administrator must enable the
[ENFORCE\_NETWORK\_RULES\_FOR\_SNOWFLAKE\_MANAGED\_STORAGE\_VOLUME](/sql-reference/parameters#label-enforce-network-rules-for-snowflake-managed-storage-volume) parameter:

Copy code

```
USE ROLE ACCOUNTADMIN;
ALTER ACCOUNT SET ENFORCE_NETWORK_RULES_FOR_SNOWFLAKE_MANAGED_STORAGE_VOLUME = true;
```

### Creating a network rule

Create a network rule with `MODE = SNOWFLAKE_MANAGED_STORAGE_VOLUME` and `TYPE = AWSVPCEID` to restrict access to the managed
storage volume based on VPC endpoint identifiers:

Copy code

```
CREATE NETWORK RULE managed_volume_rule
  TYPE = AWSVPCEID
  VALUE_LIST = ('vpce-123abc3420c1931')
  MODE = SNOWFLAKE_MANAGED_STORAGE_VOLUME
  COMMENT = 'Allow access from Horizon and S3 VPC endpoints';
```

### Applying a network policy

Create a network policy that uses the network rule and apply it to the account:

Copy code

```
CREATE NETWORK POLICY managed_volume_policy
  ALLOWED_NETWORK_RULE_LIST = ('managed_volume_rule')
  COMMENT = 'Restrict Snowflake-managed storage volume access to specific VPC endpoints';

ALTER ACCOUNT SET NETWORK_POLICY = managed_volume_policy;
```
