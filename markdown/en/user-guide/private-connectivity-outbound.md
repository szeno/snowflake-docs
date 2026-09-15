# Private connectivity for outbound network traffic

[Business Critical Feature](/user-guide/intro-editions)

This feature requires Business Critical (or higher).

To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Snowflake features such as external functions and external stages generate outbound network traffic from Snowflake to a cloud platform. For
increased security, you can create private endpoints in Snowflake to access the cloud platform by using the platform’s private connectivity
solution rather than traversing the public Internet. This lets you access cloud platform services privately and securely from Snowflake.

To reach private data sources on your network that aren’t accessible through a cloud-provider private endpoint (on-premises, hybrid, or
cross-cloud sources), see [Data Connectivity Proxy](/user-guide/data-connectivity-proxy).

Outbound private connectivity is available for the following Snowflake features:

- [External network locations using external access integrations](#label-private-connect-external-access)
- [External functions](#label-private-connect-external-functions)
- [External stages](#label-private-connect-external-stages)
- [External tables](#label-private-connect-external-tables)
- [Catalog integrations for Apache Iceberg™ tables](#label-private-connect-catalog-integrations)
- [External volumes for Apache Iceberg™ tables](#label-private-connect-external-volumes)
- [Apache Iceberg™ REST catalog integrations](#label-private-connect-iceberg-rest-catalogs)
- [Snowpipe automation](#label-private-connect-snowpipe)

## Outbound private connectivity costs

You pay for each private connectivity endpoint along with total data processed. For pricing of these items, see the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

You can explore the cost of these items by filtering on the following service types when querying billing views in the ACCOUNT\_USAGE and ORGANIZATION\_USAGE schemas:

- OUTBOUND\_PRIVATELINK\_ENDPOINT
- OUTBOUND\_PRIVATELINK\_DATA\_PROCESSED

For example, you can query the [USAGE\_IN\_CURRENCY\_DAILY](/sql-reference/organization-usage/usage_in_currency_daily) view and filter on these service types.

## Basic workflow

Each Snowflake feature that can use outbound private connectivity has its own prerequisites and configuration procedures. However,
there are common steps to establish outbound private connectivity.

For example, a Snowflake account administrator (user with the ACCOUNTADMIN role) or a user that has a role with the appropriate privileges
can do the following:

1. Complete any prerequisite configuration for the feature generating outbound network traffic.
2. In Snowflake, provision a private connectivity endpoint to connect to the cloud platform.
3. Authorize the private connectivity endpoint.
4. Retrieve the private connectivity endpoint URL that points to the service or resource.
5. Integrate the private connectivity endpoint URL into the Snowflake configuration of your Snowflake feature.
6. Deprovision private connectivity endpoints that are not actively being used to avoid cloud platform
   [limitations](#label-private-connect-external-service-limits).

Tip

These steps are self-service but might require collaboration with different parties to complete the setup. Consult with the
administrators that own the different services before starting.

The placement of these steps depends on the Snowflake feature. For details, refer to the configuration procedure for feature.

## Scaling considerations

Your implementation of outbound private connectivity must conform to the following limitations associated with cloud providers:

Cannot have more than five private endpoints per Snowflake account
:   Private endpoints that have been deprovisioned within the last seven days count toward this limit.

    To increase this limit, contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Cannot have more than one endpoint to the same AWS service or Azure subresource
:   For AWS, this limitation is per service. So if you have one endpoint to an S3 bucket, you cannot have a different endpoint to another S3
    bucket because the endpoint-to-S3 service combination would be duplicated.

    For Azure, if a resource has only one subresource, you can only have one endpoint. But if the resource has different subresources
    available, you can have multiple endpoints to the resource as long as they connect to different subresources.

    Note

    You can duplicate an endpoint-to-service or endpoint-to-subresource combination in a different Snowflake account.

## U.S. government regions

Support for outbound private connectivity from [U.S. SnowGov regions](/user-guide/intro-regions#label-intro-regions-snowgov-regions) is as follows:

Microsoft Azure:
:   Outbound private connectivity from regions on Microsoft Azure Government is supported. The source region with the private endpoints and
    the target Microsoft service must both be on Microsoft Azure Government.

AWS:
:   Outbound private connectivity from regions on AWS GovCloud is supported.

## External network locations using external access integrations

You can use outbound private connectivity and external access integrations to reach external network locations from Snowpark Container
Services or from UDF/UDTF and stored procedures within Snowpark.

From Snowpark
:   - [External network access and private connectivity on AWS](/developer-guide/external-network-access/creating-using-private-aws)
    - [External network access and private connectivity on Microsoft Azure](/developer-guide/external-network-access/creating-using-private-azure)

From Snowpark Container Services
:   - [Network egress using private connectivity](/developer-guide/snowpark-container-services/service-network-communications#label-working-with-services-jobs-egress-private)

## External functions

- [Private connectivity with external functions: Azure Portal](/sql-reference/external-functions-creating-azure-ui-private-connect)
- [Private connectivity with external functions: Azure ARM template](/sql-reference/external-functions-creating-azure-template-private-connect)

## External stages

- [Private connectivity to external stages for Amazon Web Services](/user-guide/data-load-aws-private)
- [Private connectivity to external stages and Snowpipe automation for Microsoft Azure](/user-guide/data-load-azure-private)
- [Private connectivity to external stages for Google Cloud](/user-guide/data-load-gcs-private)

## External tables

An [external table](/user-guide/tables-external-intro) is a Snowflake feature that allows you to query data stored in an external
stage as if the data were inside a table in Snowflake. If you configure the external stage to use private connectivity, then network traffic
to the external table uses private connectivity rather than the public internet.

## Catalog integrations for Apache Iceberg™ tables

- [Configure an Apache Iceberg™ REST catalog integration with outbound private connectivity](/user-guide/tables-iceberg-configure-catalog-integration-rest-private)

## External volumes for Apache Iceberg™ tables

- [Private connectivity to external volumes for Amazon Web Services](/user-guide/tables-iceberg-configure-external-volume-s3-private)
- [Private connectivity to external volumes for Microsoft Azure](/user-guide/tables-iceberg-configure-external-volume-azure-private)
- [Private connectivity to external volumes for Google Cloud](/user-guide/tables-iceberg-configure-external-volume-gcs-private)

## Apache Iceberg™ REST catalog integrations

- [Configure an Apache Iceberg™ REST catalog integration with outbound private connectivity](/user-guide/tables-iceberg-configure-catalog-integration-rest-private)

## Snowpipe automation

- [Private connectivity to external stages and Snowpipe automation for Microsoft Azure](/user-guide/data-load-azure-private)
