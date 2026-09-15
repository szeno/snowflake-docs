# Private connectivity for outbound network traffic in Snowflake Open Catalog

[Business Critical Feature](https://docs.snowflake.com/en/user-guide/intro-editions)

This feature requires Business Critical (or higher).

To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Feature — Generally Available

Not available in government regions.

When you work with tables in Open Catalog, you generate outbound network traffic from your Open Catalog account to your external cloud
storage. For example:

- When you select a table in Open Catalog, Open Catalog displays the schema for the table by retrieving the metadata for the table. This
  metadata is stored in your external cloud storage.
- When your query engine attempts to load data from Open Catalog, Open Catalog accesses the external cloud storage to read the metadata
  for your Iceberg table and then returns the metadata for the table to the query engine.

By default, outbound network traffic traverses the public internet. For increased security, you can enable private connectivity for outbound
network traffic to route this traffic through private endpoints instead of the public internet.

Note

Private connectivity for outbound network traffic is only supported for the following cloud storage providers:

- [Amazon S3](private-connectivity-outbound-manage-endpoints-aws)
- [Azure](private-connectivity-outbound-manage-endpoints-azure)

## Scaling considerations

Your implementation of outbound private connectivity must conform to the following limitations associated with cloud providers:

**Cannot have more than five private endpoints per Snowflake account**

> Private endpoints that have been deprovisioned within the last seven days count toward this limit.

> To increase this limit, contact Snowflake Support.

**Cannot have more than one endpoint to the same AWS service or Azure subresource**

> For AWS, this limitation is per service. So if you have one endpoint to an S3 bucket, you cannot have a different endpoint to another S3
> bucket because the endpoint-to-S3 service combination would be duplicated.

> For Azure, if a resource has only one subresource, you can only have one endpoint. But if the resource has different subresources
> available, you can have multiple endpoints to the resource as long as they connect to different subresources.

Note

You can duplicate an endpoint-to-service or endpoint-to-subresource combination in a different Snowflake account.

## Billing

Snowflake calculates costs for outbound private connectivity based on private endpoint usage. For details on pricing for outbound private
connectivity, see the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).
