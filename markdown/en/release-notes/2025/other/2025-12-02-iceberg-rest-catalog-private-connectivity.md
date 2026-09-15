# Dec 02, 2025: Private connectivity for Apache Iceberg™ REST catalog integrations (*General availability*)

You can now set up an Apache Iceberg™ REST catalog integration to use outbound private connectivity.
This feature lets you connect to external Iceberg REST catalogs, such as generic Iceberg REST, Amazon Web Services (AWS) Glue Data Catalog,
and Databricks Unity Catalog, through private endpoints instead of the public internet.
This enhances security by keeping your network traffic within your cloud provider’s private network.

Private connectivity is only supported for catalog integrations on AWS that use AWS PrivateLink and
Microsoft Azure that use Azure Private Link.

For more information, see [Configure an Apache Iceberg™ REST catalog integration with outbound private connectivity](/user-guide/tables-iceberg-configure-catalog-integration-rest-private).
