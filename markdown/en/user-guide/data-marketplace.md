# About listings

With listings, you can provide data and other information to other Snowflake users, and you can access data and other information shared by Snowflake providers.

You can explore, access, and provide listings to consumers privately and on the Snowflake Marketplace. To learn more about the Snowflake Marketplace, see [About Snowflake Marketplace](/collaboration/collaboration-marketplace-about).

## What is a listing?

A listing is an enhanced method of [Secure Data Sharing](/user-guide/data-sharing-intro) and uses the same
[provider and consumer model](/user-guide/data-sharing-intro#label-overview-data-providers-consumers).

As a provider, you can share a Snowflake Native App or data in your Snowflake account by creating and publishing a listing to specific Snowflake
accounts or on the Snowflake Marketplace. To get started, see [Use listings as a provider](/collaboration/provider-becoming).

As a consumer, you can access a Snowflake Native App or data shared by other Snowflake accounts on the Snowflake Marketplace or privately with your
account using a listing. To get started, see [Use listings as a consumer](/collaboration/consumer-becoming).

Listings add capabilities to Secure Data Sharing such as the following:

- Offer a share publicly on the Snowflake Marketplace.
- Charge consumers for access to the data in the share.
- Monitor interest in your listing and usage of the data in the share.
- Provide metadata about the share, such as a title, description, sample SQL queries, and information about the data provider.

For more details about listings compared with other types of sharing at Snowflake, see
[Overview of Data Sharing at Snowflake](/guides-overview-sharing).

You can explore listings and providers on the Snowflake Marketplace through [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in). See [About Snowflake Marketplace](/collaboration/collaboration-marketplace-about).

Note

To use listings and the Snowflake Marketplace, you need to agree to additional terms. See [Legal requirements for providers and consumers of listings](/collaboration/collaboration-listings-legal).

When you offer data and apps to consumers, you choose how to make your data product available to consumers and how consumers can access your data product. A data product is the share or the app attached to your listing.

## Listing availability options

When you offer a listing, you choose how to make your data product available to consumers:

- **Privately**, available only to specific consumers. Private listings let you take advantage of the capabilities of
  listings to share data and other information directly with other Snowflake accounts in any Snowflake region.
- **Publicly**, visible on the Snowflake Marketplace. You can offer listings on the Snowflake Marketplace to market
  your data product across the Snowflake Data Cloud. Offering a listing on the Snowflake Marketplace lets you share curated data offerings with
  many consumers simultaneously, rather than maintaining sharing relationships with each individual consumer.

  See [About Snowflake Marketplace](/collaboration/collaboration-marketplace-about) for more about publishing on the Snowflake Marketplace.

## Listing access options

When you offer a listing, you choose how consumers can access your data product:

- [Free access to your full data product](#label-free-listing), with no payment required.
- [Limited trial access to your data product](#label-trial-listing), with unlimited access to the full data product available upon request.
- [Paid access to your data product](#label-paid-listing), using the pricing models offered by Snowflake.

### Free listings

A free listing is available privately to specific consumers, or publicly on the Snowflake Marketplace, and provides instant access to a
full published dataset.

When published on the Snowflake Marketplace, this type of listing is best for providing generic, aggregated, or non-customer-specific data. When
shared privately with specific consumers, you can use this type of listing to provide data products to existing business partners at no
cost or according to negotiated payment terms.

For more information about creating free listings, see [Create and publish a listing](/collaboration/provider-listings-creating-publishing).

### Limited trial listings

A limited trial listing is available on the Snowflake Marketplace and provides instant limited access to a data product.

A provider can choose whether to offer a subset of data as part of the trial data product, or make the full product available for a short
period of time, or something else. Providers can set the availability period for limited trial listings from 1 to 90 days.

Consumers can trial the data product attached to the limited trial listing and request unlimited access to your data product.
A provider can then choose who to offer the full data product to and whether (or how much) to charge for the data product.
For example, in response to a request you might offer:

- A free private listing to a consumer with whom you have an existing business relationship or with whom you have negotiated payment terms.
- A paid private listing to a consumer, using one of the [pricing models](/collaboration/provider-listings-pricing-model) offered
  by Snowflake.

Limited trial listings let providers make a data product visible to and free to try by anyone on the Snowflake Marketplace, but fully available
only to consumers that they choose to do business with. This type of listing is best for providing customer-specific data, or for cases
when you want to allow only certain consumers to purchase your data product due to licensing agreements, regulatory requirements, or other
commercial reasons.

For guidance preparing to offer your data product as a limited trial, see [Prepare to offer a limited trial listing](/collaboration/provider-listings-preparing#label-prepare-limited-trial-listing).

### Paid listings

A paid listing is available privately or on the Snowflake Marketplace. As a provider, you can create paid listings to charge consumers to access
or use your listing.

Paid listings are only available to consumers in specific regions, and from providers in specific regions.

- For more information about becoming a provider of paid listings, see [Provide paid listings](/collaboration/provider-becoming#label-monetization-provider-onboarding).
- For more information about paying for listings as a consumer, see [Pay for Snowflake Marketplace listings](/collaboration/consumer-listings-paying).
- For more information about the pricing models you can use as a provider, see [Paid listings pricing models](/collaboration/provider-listings-pricing-model).

Paid listings are best for data products that offer proprietary or industry-specific data, or insights and analytics performed on
freely available data. This type of listing also offers consumers the ability to try and buy a data product with unified procurement
through Snowflake.

## Pricing plans and offers

### Pricing plans

Pricing plans allow providers to offer multiple stock keeping units (SKUs) for a single paid listing. With pricing plans, providers don’t have to create a listing for every SKU that they offer to consumers. Instead, after creating a pricing plan, providers create offers that are extended to consumers.

Pricing plans and offers simplify listing monetization and management. An offer provides consumers with individualized billing, payment terms, payment schedules, and contract start and end dates. Consumers can review an offer before committing, and an offer can be quickly accepted or rejected.

Note

Pricing plans and offers are not available for organizational listings. Organizational listings focus on secure data sharing within an organization, allowing teams to access and utilize internal data products without the complexities of pricing models or offers.

### Offers

Offers define the purchase terms for a listing. Offers are specific to each consumer and provide individualized billing, payment terms, payment schedules, and contract start and end dates. After a consumer receives an offer from a listing provider, the consumer can review the terms and then accept or reject the offer.

Consumers can review offers in Snowsight on the **Data sharing** » **External sharing** page.

### Limitations for listings that include pricing plans and offers

- Providers can’t convert a listing to a new type (for example, from a limited trial listing to a paid listing).
- Consumers can’t convert a Snowflake Native App from one listing type to another (for example, from a private listing to a paid listing).

## V1 vs. V2 listings

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

When working with listings in Snowflake, it’s important to understand the distinctions between Version 1 (V1) and Version 2 (V2) listings. These versions differ significantly in their manifest formats, targeting capabilities, feature sets, and compatibility requirements.

### V1 listings

V1 listings are the original format for listings in Snowflake and are compatible with all Snowflake accounts that support listings. They support basic listing functionalities, including private and public sharing, but lack advanced features such as pricing plans and offers. In the [listing manifest](/progaccess/listing-manifest-reference), V1 listings use a `targets` field, and the listing targets are specified by individual account names. For example:

Copy code

```
...
targets:
  accounts: ["Org1.Account1", "Org2.Account2"]
...
```

### V2 listings

V2 listings introduce a new manifest format that provides enhanced targeting capabilities, allowing providers to specify a wider range of targeting options, including organizations, accounts with specific roles, locations, and organization-level groups.

In the [listing manifest](/progaccess/listing-manifest-reference), V2 listings allow users to specify `external_targets` and `locations`. For example:

Copy code

```
...
external_targets:
  access:
    - organization: OrgName2
      accounts: [acc1, acc2]
    - account: acc2
      roles: [role1, role2]
locations:
  access_regions:
    - name: "PUBLIC.AWS_US_WEST_2"
...
```
