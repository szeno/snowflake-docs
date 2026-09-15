# Resharing listings

With resharing, providers can allow consumers to share their incoming listings with other Snowflake accounts, either within the same region
or across regions. Resharing extends the reach of your data products without requiring you to manage individual sharing relationships with
every downstream consumer.

There are three roles involved in resharing, each representing a different Snowflake account:

- **Provider**: The account that owns the original data and publishes the listing. The provider can turn on or off resharing on their
  listings to control downstream resharing of their data.
- **Resharer**: A consumer of the provider’s listing who creates new views from the incoming listing and shares them with other accounts.
- **Consumer**: The account that accesses the reshared listing from the resharer.

Note

Multi-hop resharing is possible, so a resharer may reshare data that itself has been reshared with them.

Resharing supports several scenarios, including:

- **Resharing external listings within an organization**: A company might acquire weather data on the Snowflake Marketplace or privately
  from an external vendor. The central data team might then want to reshare the incoming listing after applying some entitlements to the
  rest of the organization on the internal marketplace or as private listings.
- **Resharing internal listings within an organization or externally**: Within an internal marketplace, a marketing team creates a
  reshareable listing and provides that listing to the sales team. The sales team accesses that data and uses parts of it, such as a view,
  and incorporates that into their own data product. The sales team then shares that transformed data product with the finance team. The
  sales team might also take some elements of this incoming dataset, apply policies, and share externally with their partners.
- **Resharing cross-region**: A company has Snowflake accounts throughout the world, with a central company-wide warehouse in Germany. An
  account in Malaysia shares data with a Snowflake account in Germany. That data can then be reshared to a second account in the same
  region without creating any copies. For cross-region resharing, Snowflake automatically replicates the data to the target region.

## Key features

- **Expand reach**: Providers can share data publicly or privately and enable that data to be reshared, making their data products more
  valuable to their customers.
- **Low operational and storage costs**: Consumers don’t have to create and maintain physical copies of data.
- **Ability to transform on reshare**: Consumers can optionally manage or transform the data product and then reshare it within their
  internal marketplace with colleagues, or privately share it with business partners.
- **Value-added reseller bundling**: Bundle incoming listings from other vendors as part of your Native App or data products.
- **Cross-region auto-fulfillment**: When a resharer shares listing data to another region, listing auto-fulfillment replicates the data to
  the target region. The provider doesn’t incur additional costs for this replication. Replication costs are attributed to the resharer.

## Resharing listings workflow

A typical workflow for resharing includes a minimum of three parties.

1. The provider who owns the original data product shares their data product publicly or privately with a consumer (Consumer A).
2. Consumer A creates a view that references the shared data and then shares these *outgoing* views publicly or privately with a
   second-level account (Consumer B).
3. Consumer B retrieves and uses the reshared data product.

## Resharing access control requirements

The roles and privileges for resharing a listing are the same as those for [Creating a listing](/user-guide/collaboration/listings/organizational/org-listing-create#label-organizational-listing-privileges).

For provider-specific information, see [Using resharing as a provider](/collaboration/resharing-as-provider).

For resharer-specific information, see [Reshare incoming data as a resharer](/collaboration/resharing-as-resharer).

## Monitoring resharing activity

Snowflake provides a usage view to help providers monitor resharing activity for their listings:

- [RESHARED\_LISTING\_CONSUMPTION\_DAILY](/sql-reference/data-sharing-usage/reshared-listing-consumption-daily): Returns a daily record
  for each resharer account that has active reshares of your listing. Use this view to identify which accounts are resharing your listings,
  monitor the number of active reshares over time, and understand the geographic distribution of resharing activity.
