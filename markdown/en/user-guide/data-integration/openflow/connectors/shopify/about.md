# About the Openflow Connector for Shopify

[Preview Feature](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/preview-terms-of-service/)

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

This topic describes the basic concepts, workflow, and limitations of the Openflow Connector for Shopify.

The Openflow Connector for Shopify replicates data from a Shopify store into Snowflake using the
[Shopify Admin GraphQL API](https://shopify.dev/docs/api/admin-graphql).
The connector uses [Bulk Operations](https://shopify.dev/docs/api/usage/bulk-operations/queries)
to efficiently extract large volumes of data and uses Snowpipe Streaming to load it into Snowflake.
It supports initial bulk loads, incremental updates, and delete detection.

## Use cases

Use the Openflow Connector for Shopify to replicate data from your Shopify store into Snowflake for the following:

- **E-commerce analytics:** Centralize order, product, and customer data in Snowflake for
  cross-channel reporting and business intelligence.
- **Inventory management:** Bring inventory items and locations into Snowflake for
  demand forecasting and supply chain optimization.
- **Customer insights:** Replicate customer and segment data in Snowflake for personalization,
  cohort analysis, and lifetime value modeling.
- **Operational reporting:** Track fulfillment orders, draft orders, and transactions
  in Snowflake for real-time operational dashboards.

## Supported objects

The connector ships with a built-in catalog of commonly replicated Shopify object types,
including:

- **Orders:** order data including line items, shipping and billing addresses, financial
  status, and fulfillment details.
- **Products** and **Product Variants:** product catalog data including pricing,
  inventory, and variant information.
- **Customers:** customer profiles, contact details, and marketing preferences.
- **Collections:** manual and automated product collections.
- **Inventory Items:** stock quantities and inventory tracking data.
- **Fulfillment Orders:** fulfillment assignments and shipping details.

The connector isn’t limited to these objects. You can replicate any object type supported
by the Shopify Admin GraphQL API by providing a custom definition in the **Object Definitions
Override** parameter. Custom definitions let you choose which fields to extract, use GraphQL
aliases to label or rename fields, and promote values from nested objects into dedicated
top-level Snowflake columns. For more information, see [Object definition overrides for the Openflow Connector for Shopify](/user-guide/data-integration/openflow/connectors/shopify/object-definitions).

For objects not in the built-in catalog, the connector can also auto-discover the schema
using GraphQL introspection. For more information, see [Auto-discovery](#label-auto-discovery).

## Replication lifecycle

The connector replicates data in two stages: initial bulk load and incremental synchronization.

### Initial bulk load

When the connector runs for the first time (or after a state reset), it performs a bulk
query for each configured object type using the Shopify Bulk Operations API. The connector:

1. Submits a bulk query to Shopify for each object type.
2. Polls Shopify until the bulk operation completes and a JSONL result file is available.
3. Downloads the JSONL result, flattens child connections into separate tables (with a
   `__PARENT_ID` column linking them to the parent record), and derives the Snowflake
   table schema from the GraphQL response.
4. Loads data into Snowflake using Snowpipe Streaming and merges it into the destination tables.

### Incremental synchronization

After the initial load, the connector transitions to incremental mode. It uses timestamp-based
watermarks to retrieve only records that have changed since the last sync. The connector
selects the incremental field by checking the object’s available fields against a priority
list (`updatedAt`, `createdAt`, `processedAt`) and using the first match.

The incremental frequency is user-configurable. Each incremental run retrieves changed
records and merges them into the destination tables.

## Authentication

The connector authenticates with Shopify using the OAuth2 client credentials grant. You
provide a **Shopify Client ID** and **Shopify Client Secret** from a Shopify dev app, and
the connector fetches tokens from the Shopify OAuth2 token endpoint and refreshes them as needed.

For more information, see [Set up the Openflow Connector for Shopify](/user-guide/data-integration/openflow/connectors/shopify/setup).

## Auto-discovery

The connector ships with a built-in object catalog that defines the GraphQL query
structure for a set of commonly used Shopify object types. For objects not included in the
catalog, the connector can optionally query the Shopify Admin GraphQL introspection endpoint
to discover the schema dynamically.

Auto-discovered definitions are cached in NiFi distributed state for 24 hours to
avoid repeated introspection calls. For more information, see the
[Enable Introspection](/user-guide/data-integration/openflow/connectors/shopify/setup#label-shopify-parameters)
parameter.

## How deletes are handled

For objects that support delete detection, the connector periodically queries the Shopify
[Events API](https://shopify.dev/docs/api/admin-graphql/latest/queries/events) using
`action: "destroy"` and applies soft deletes in Snowflake. Only object types that emit
destroy events in the Shopify Events API support delete detection. The connector sets a
`__SNOWFLAKE_IS_DELETED` column to TRUE and a `__SNOWFLAKE_DELETED_AT` column to the
timestamp of the deletion event. Rows are never physically removed from the destination table.

When a parent record is soft-deleted, the connector cascades the soft delete to all registered
child tables (for example, variants associated with a deleted product).

## Automatic retry and rate limiting

The connector respects Shopify’s rate limiting model, which uses a leaky bucket algorithm
with a 1,000-point capacity that refills at 50 points per second. The connector tracks
available points and automatically waits when the bucket is low to avoid throttling errors.

For throttling responses, the connector retries automatically. When Shopify returns an HTTP 429,
the connector waits for the duration specified in the `Retry-After` header before retrying.
When the API returns a `THROTTLED` GraphQL error, the connector retries with exponential backoff.
The default configuration allows up to 3 retries with an initial backoff of 1 second.

## Child record flattening

For objects with nested connections (such as order line items or returns), the connector
automatically extracts child records into separate Snowflake tables. Each child table
includes a `__PARENT_ID` column that references the parent record’s Shopify GID, enabling
joins between parent and child tables.

## Limitations

Consider the following limitations when using the connector:

- The connector requires a Shopify dev app with Admin API access.
- The [Shopify Bulk Operations API](https://shopify.dev/docs/api/usage/bulk-operations/queries) supports a maximum of 5 connections per query and 2 levels of nesting.
- The connector currently supports data extraction (ingestion) only. Writing data back to
  Shopify isn’t supported.
- Schema evolution isn’t supported in the current release. If source objects gain or lose
  fields in Shopify, you must [reset the connector state for the affected object](/user-guide/data-integration/openflow/connectors/shopify/maintain#label-reload-a-specific-object)
  to re-ingest it with the updated schema.
- Rate limits depend on your Shopify plan. The connector respects Shopify’s leaky bucket
  throttling, but very high-volume stores with many objects might require careful scheduling
  to avoid sustained throttling.
- Delete detection is only available for the object types listed in the **Objects to Track
  for Deletes** parameter. If an object type doesn’t emit destroy events in the Shopify
  Events API, delete polls for that type return zero results.
- The connector fetches up to the [`pageSize` value of each child connection](/user-guide/data-integration/openflow/connectors/shopify/object-definitions#label-child-fields)
  during incremental runs (maximum 250, the Shopify hard limit for incremental queries).
  Child records beyond this limit aren’t captured.
  The initial bulk load isn’t subject to this limit: the Shopify Bulk Operations API ignores
  the `first:` argument and returns all child records.

## Next steps

To set up the connector, see [Set up the Openflow Connector for Shopify](/user-guide/data-integration/openflow/connectors/shopify/setup).
