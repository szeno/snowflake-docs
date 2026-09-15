# Snowflake Open Catalog release notes

Overview of the most recent releases of Snowflake Open Catalog.

## September 29, 2025

### Support for External OAuth and key pair authentication

You can now connect to Snowflake Open Catalog with External OAuth or key pair authentication. For more
information, see:

- [Overview of External OAuth in Open Catalog](external-oauth-overview)
- [Overview of key pair authentication in Open Catalog](key-pair-auth-overview)

## May 27, 2025

### Access the Open Catalog UI with private connectivity

You can now access the Open Catalog UI through private connectivity instead of over the public internet. For more information, see:

- [Configure private connectivity for the Open Catalog UI](private-connectivity-ui-configure)
- [Sign in to Open Catalog using private connectivity](signin-snowflake-customer#using-private-connectivity)

## May 5, 2025

### Support for private connectivity

Snowflake supports using private connectivity with Snowflake Open Catalog. Use private connectivity
to route your connection to Snowflake Open Catalog through private endpoints or private IP addresses instead of the public internet.
For more information, see:

- [Private connectivity for inbound network traffic in Snowflake Open Catalog](private-connectivity-inbound-configure-aws)
- [Private connectivity for outbound network traffic in Snowflake Open Catalog](private-connectivity-outbound)

## March 31, 2025

### Support for SAML-based SSO

With this release, we are pleased to announce support for using SAML-based single sign-on (SSO) with Snowflake Open Catalog.

SSO for Open Catalog lets you integrate Open Catalog with a third-party identity provider. Users can now sign in
to the Open Catalog web interface by using existing credentials managed by an identity provider (IdP). You don’t have to manage separate
usernames and passwords in Open Catalog. To learn more, see [Overview of SSO in Snowflake Open Catalog](sso-overview).

## November 7, 2024

### Credential vending for external catalogs is now disabled by default

With this release, credential vending for external catalogs is now disabled by default. External catalogs aren’t managed by Snowflake Open
Catalog, so Open Catalog can’t enforce certain directory structure hierarchies. For more information about directory structure hierarchies,
see [Organize catalog content](https://other-docs.snowflake.com/en/opencatalog/organize-catalog-content). Therefore, credential vending for
external catalogs is disabled by default when you create the catalog. In addition, it’s also now disabled for existing external catalogs.
However, you have the option to enable credential vending for an external catalog. For details, see
[Enable credential vending for an external catalog](./enable-credential-vending-external-catalog).

## October 18, 2024

### Snowflake Open Catalog: General Availability

With this release, we are pleased to announce the general availability of Snowflake Open Catalog, which was previously named Polaris Catalog
and was available as a preview feature. With general availability, we’ve made the following updates:

- A service admin can now create additional users for the Open Catalog account. These users can manage the account through the Open Catalog
  web interface. For details, see [Manage users](./manage-users).
- A catalog admin can now secure individual namespaces or tables within a catalog. You can also continue to secure a catalog at the catalog
  level. For details, see [Secure catalogs](./secure-catalogs).
- When viewing the schema for a table in Snowflake Open Catalog, you can now view the nested schema for a column. For details, see
  [View the schema for a table](./view-table-schema).
- We’ve added billing support for Open Catalog, but you can use Open Catalog for free until April 30, 2025. For more information, see
  [Billing](./overview#billing).

## August 8, 2024

With this release, we are pleased to announce the availability of the following new enhancements in Open Catalog.

### Snowflake now supports queries on tables with nested namespaces

Previously, we listed a limitation where Snowflake couldn’t read tables registered in Open Catalog that were located under a nested
namespace. Snowflake now supports querying tables located under a nested namespace. For example, if you create a nested namespace
`namespace1.namespace1a.namespace1ab`, Snowflake can read tables grouped under the namespace `namespace1ab`. For more information, see
[Create a namespace](organize-catalog-content#create-a-namespace).

## July 30, 2024

With this release, we are pleased to announce the initial public preview release of Open Catalog hosted on Snowflake with the following features:

### Apache Iceberg™ Rest API

Open Catalog provides an Apache Iceberg Rest Catalog API, which enables support for any query engine that supports the Apache Iceberg™ Rest catalog specification.

### Authentication

Users can create service connections that provide a Client ID and Client Secret service credentials. These credentials are used for authentication by using OAuth 2.0.

### Open Catalog user interface

Open Catalog is provided with a web application to simplify the management of the catalog. Within the UI, users can manage catalogs, service principals, and the privileges for service principals.

### Role-based security model

A role-based access control (RBAC) security model is included, so customers can manage the level of access each user or user group is allowed on the catalog. For more information, see [Access control](access-control).

### Credential vending

Access to the storage objects where the data resides is managed by Open Catalog. When a user requests access to a table, whether for read or write, a temporary scoped storage credential is generated and passed back to the calling engine, which provides the appropriate access permissions to the folder in which the data resides within the storage.

### Snowflake warehouse catalog integration for Open Catalog

A new catalog integration for Open Catalog is available within Snowflake. This catalog integration allows users to create externally managed Apache Iceberg™ tables that point to tables that reside in Open Catalog for querying.

## Considerations and limitations

The following considerations and limitations apply to Open Catalog, and are subject to change:

**Signup**

- Customers who haven’t previously created a Snowflake Open Catalog account can’t sign up for their first Open Catalog account. New
  customers should use [Snowflake Horizon Catalog](/user-guide/tables-iceberg-access-using-external-query-engine-snowflake-horizon) for
  Apache Iceberg™ tables and multi-engine interoperability with Iceberg. Existing Snowflake Open Catalog customers can continue to use
  Open Catalog and can create additional Open Catalog accounts if necessary.

**Catalogs**

- Open Catalog currently supports Apache Iceberg™ tables that use either:
  - Open Catalog as the Iceberg catalog
  - Snowflake as the Iceberg catalog. External Iceberg catalogs other than Snowflake aren’t currently supported. If you want to add Iceberg tables from other external catalogs, you must migrate them.
- You can’t import existing Iceberg tables from vendors such as Glue or Tabular into an internal catalog in Open Catalog, but they can be added to external catalogs.
- Snowflake can query but can’t write to tables managed by Open Catalog.
- Snowflake Iceberg tables, which are available in external catalogs, are read only in Open Catalog.
- For internal catalogs, you can’t rename a table across namespaces. For example, you can’t rename a table from `/mytables/ns1/table1` to `/mytables/ns2/table1`.
- When creating an internal or external catalog, you can’t specify a default base location or allowed location that overlaps with the directory hierarchy for a different catalog. For example, if the default base location for catalog1 is `s3://mytables/db1/schema1/table1`, you can’t specify the default base location for your new catalog as `s3://mytables/db1/`.

**Access control**

- The scoped access policy for a table is limited to the `<table_base>/metadata/` and `<table_base>/data/` directories.

**Iceberg**

- When calling the registerTable API, you can’t register a table in a location that is outside of the parent namespace directory. For example, if the folder hierarchy for a catalog is `s3://teambucket/iceberg/namespace1/namespace1a/`, you can’t create `mytbl3` with a base location `s3://teambucket/iceberg/namespace1`. You can create it, for example, with a base location `s3://teambucket/iceberg/namespace1/mytbl3`.
- If you call the `dropTable` API and request to purge the table’s data and metadata by setting the `purgeRequested` parameter to `true`, Open Catalog
  makes a best effort to delete the following items:

  - All data and metadata files associated with the table
  - The storage directory for the table

  However, some of these items might not be deleted. If so, navigate to your external cloud storage to identify and delete
  the orphaned files or storage directory yourself.
