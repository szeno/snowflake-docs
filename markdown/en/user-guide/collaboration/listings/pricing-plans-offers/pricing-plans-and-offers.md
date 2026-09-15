# Pricing plans and offers

## Understand pricing plans

A pricing plan lets providers specify a [pricing model](/collaboration/provider-listings-pricing-model) (flat-fee versus usage-based), a base price, a billing frequency, and more for their listings. These listings can be public (available on the Snowflake Marketplace) or private (shared directly with a consumer).

- Providers can create public listings on the Snowflake Marketplace that include multiple pricing plans.
- For both public and private listings, providers can optionally specify to show the price and pricing information on the listing page, allowing consumers to review this information before they purchase.
- For private listings, where providers opt to not show pricing information on the pricing plan, providers can still reference the listing when extending offers to consumers.

### Self-serve pricing plans

Self-serve pricing plans allow consumers to purchase products directly from listings without provider interaction. This type of pricing plan includes a price, pricing model, and billing frequency on the provider’s listing page.

Providers can configure multiple pricing plans for a listing, such as “Good-Better-Best” pricing. This allows consumers to select the pricing option that works best for them. And when a consumer selects a pricing plan, they can immediately complete a purchase.

## Understand offers

Providers can create offers that define purchase terms for a listing and then extend those offers to consumers. Offers provide individualized billing, payment terms, payment schedules, and contract start and end dates. Before accepting or rejecting an offer, consumers can review the terms and request changes.

When consumers purchase an offer on the Snowflake Marketplace, all existing billing methods are supported, including the [Marketplace Capacity Drawdown (MCD) program](/collaboration/marketplace-capacity-drawdown).

Providers can extend offers to consumers in Snowsight or programmatically.

### Understand offer types

Providers can create two types of offers: standard and private.

- Standard offers are public on the Snowflake Marketplace and are tied to pricing plans. When a consumer views a listing with a standard offer, they can see pricing details and accept the offer directly from the listing page.
- Private offers are individualized offers that providers can extend directly to specific consumers. Private offers aren’t visible on the Snowflake Marketplace. They also don’t have to be tied to a pricing plan. For private offers that are tied to pricing plans, providers can apply negotiated pricing that includes discounts and custom terms. For private offers that aren’t tied to a pricing plan, providers can create a [one-time pricing offer](/user-guide/collaboration/listings/pricing-plans-offers/providers-create-manage-offers#label-create-one-time-pricing-offer) for the listing.

## FAQs

**Can I add offers to my existing paid listings?**

No, existing paid listings are v1 listings. Offers are only available on v2 paid listings.

**How can I convert my existing v1 paid listing to a v2 paid listing?**

A migration feature that will allow converting a v1 paid listing to a v2 paid listing will be available to partners at a future date.

**If my consumer is on a free trial and they accept an offer, what happens?**

After a consumer accepts an offer, the offer will govern access to and metering of the product. Specifically, the offer’s access start date determines when the consumer can start using the product. To ensure a seamless experience for your consumers, set the access start date to **When offer accepted**. This way, the consumer can start using the product immediately after accepting the offer, even if they are still on a free trial.

**How can I give free access for a period of time on a paid offer?**

You can set the access start time to **When offer accepted** and set the **First invoice date** to the date when you want to start charging the consumer.
