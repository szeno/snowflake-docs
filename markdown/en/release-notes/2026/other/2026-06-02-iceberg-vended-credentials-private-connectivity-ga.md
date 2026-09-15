# June 2, 2026: Private connectivity for catalog-vended credentials (*General availability*)

When you use catalog-vended credentials for Apache Iceberg™ tables, you can now configure outbound private connectivity so Snowflake accesses your cloud storage through a private endpoint instead of the public internet. You can enable private storage access by setting `USE_PRIVATELINK_ENDPOINT = TRUE` in the `DEFAULT_STORAGE_CONFIG` parameter of your catalog integration.

Private connectivity to storage with vended credentials is supported on AWS (using AWS PrivateLink) and Azure (using Azure Private Link).

For more information, see [Configure private connectivity to storage for catalog-vended credentials](/user-guide/tables-iceberg-vended-credentials-private-connectivity).
