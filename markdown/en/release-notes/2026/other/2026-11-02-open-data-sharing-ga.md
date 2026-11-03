# Nov 02, 2026: Open Data Sharing (*General availability*)

Open Data Sharing is now generally available and is no longer in [Preview](/release-notes/preview-features).

With Open Data Sharing, you can share live, read-only data in Snowflake-managed Iceberg tables with consumers outside Snowflake by using standard Iceberg REST
Catalog APIs, without data movement or ETL pipelines.

This release adds the following capabilities:

- **Cross-region sharing**: You can make listing data available to external consumers in Snowflake commercial regions on AWS and
  Azure. Each external consumer is bound to the single region that you set when you create it, and Snowflake auto-fulfills the
  listing to that region. The region determines where the data is served from, not where the consumer’s client connects from.
  Cross-region external consumers are supported in AWS and Azure commercial regions.
- **Workload identity federation**: In addition to programmatic access tokens (PATs), external consumers can authenticate by using
  [workload identity federation (WIF)](/user-guide/open-data-sharing-workload-identity) with AWS, Microsoft Azure, Google Cloud, or
  OpenID Connect (OIDC) identity providers. For instructions to connect, see [Connect to an open-sharing catalog](/user-guide/open-data-sharing-connect).
- **Open-client access for existing listings**: You can add external consumers to an existing listing, so the same listing serves
  Snowflake consumers and open clients. For more information, see
  [Make listings available to open clients](/collaboration/collaboration-listings-about#label-listing-availability-open-clients).

For more information, see [Share data with non-Snowflake consumers](/user-guide/open-data-sharing).
