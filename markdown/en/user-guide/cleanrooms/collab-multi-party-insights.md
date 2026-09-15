# Multi-party insights

Feature — Generally Available

Currently available in [these regions](/user-guide/cleanrooms/installing-dcr#label-dcr-supported-regions).

Not available in government and VPS deployments.

## About the template

This template demonstrates a three-party data clean room use case built on Snowflake Collaboration Data Clean Rooms. It brings together three distinct
datasets representing different parties in an advertising and measurement workflow:

- **Publisher (Exposures):** Ad exposure data including hashed email, IP address, impression date, ad group, and campaign ID,
  representing audience impressions on an ad platform.
- **Advertiser (Purchases):** Purchase transaction data including hashed email, purchase date, platform, location, and purchase amount,
  representing customer buying behavior across mobile, desktop, and CTV.
- **Identity Partner (Customer Spine):** Identity resolution data including hashed email, state, and filing type, serving as a third-party
  spine that enriches the collaboration with geolocation and demographic attributes.

The template joins all three datasets using standardized join keys (hashed email SHA-256) to surface aggregated insights on purchase
behavior broken out by geolocation. Specifically, the analysis computes the total number of purchases and average spend amount per state
and ad group across the three parties.

This three-party join is a key capability of Snowflake Collaboration Data Clean Rooms, going beyond the one-to-one provider-consumer clean room
models. The collaboration specification controls which parties can run which templates and access which data offerings, enabling flexible
permissioning. For example, the identity provider can contribute data without having access to run any analysis templates.

Two SQL templates are included:

- **Audience Overlap:** A simple overlap query that returns distinct hashed emails found across the joined datasets, useful for audience
  activation.
- **State Spend Analysis:** An insights query that joins all three tables to compute total purchases and average spend per state and ad
  group, delivering actionable campaign performance insights.

## Collaboration roles

| Collaborator | Roles | Actions |
| --- | --- | --- |
| Publisher | Owner, data provider | Registers a data offering (ad exposure data) and two analysis templates (audience overlap and state spend analysis). Creates the collaboration. |
| Advertiser | Analysis runner, data provider | Registers a data offering (purchase transaction data). Joins the collaboration, links their data, and runs the analysis templates. |
| Identity Partner | Data provider | Registers a data offering (customer spine with geolocation and demographic attributes). Joins the collaboration and links their data. Doesn’t run any analysis templates. |

Expand

Show lessSee more

## Key use cases

- **Identity resolution:** Securely match customer records across publisher, advertiser, and third-party identity providers using hashed
  join keys, enabling a unified view of audiences without exposing raw PII.
- **Audience overlap analysis:** Identify shared audiences between a publisher, advertiser, and identity data provider to evaluate match
  rates, refine targeting strategies, and activate matched segments for campaigns.
- **Purchase attribution by geography:** Attribute purchase behavior to specific ad groups and geographic regions by joining advertiser
  transaction data with publisher exposure data and a third-party identity spine.
- **Campaign performance optimization:** Aggregate total purchases and average spend by state and ad group to understand which campaigns
  and regions are driving the most value, enabling data-driven budget allocation.

## Get the worksheets and template

You can run this example in two ways:

- **Single account:** Run the entire example in one Snowflake account, where one account plays all three roles.
- **Three accounts:** Run the example across three separate Snowflake accounts in the same organization and the same cloud hosting
  environment, with each account playing a different role (publisher, advertiser, identity partner).

[See instructions to upload a SQL worksheet into your Snowflake account](/user-guide/cleanrooms/tutorials-and-samples#label-dcr-list-of-sample-notebooks-and-worksheets).

### Single-account method

Download and run the following worksheets in order in a single Snowflake account. The first worksheet generates sample data and registers
all three data offerings and both templates. The second worksheet creates the collaboration, joins, and runs both analysis templates.

1. [Download the data registration worksheet](/static/samples/clean-rooms/multi-party-insights-owner-registration.sql).
   Run this first to generate sample data and register data offerings and templates.
2. [Download the single-account worksheet](/static/samples/clean-rooms/multi-party-insights-single-account.sql).
   Run this to create the collaboration, join, and run both analysis templates.

### Three-account method

Download and run the following worksheets across three separate Snowflake accounts. The publisher registers data and templates, creates the
collaboration, and runs analyses. The advertiser and identity partner each register their own data, review, and join the collaboration.

**Publisher account (Account 1):**

1. [Download the owner registration worksheet](/static/samples/clean-rooms/multi-party-insights-owner-registration.sql).
   Run this first to generate sample data and register data offerings and templates.
2. [Download the publisher worksheet](/static/samples/clean-rooms/multi-party-insights-publisher.sql).
   Run this to create the three-party collaboration, join, and run analyses.

**Advertiser account (Account 2):**

- [Download the advertiser worksheet](/static/samples/clean-rooms/multi-party-insights-advertiser.sql).
  Run this to generate purchase data, register a data offering, review and join the collaboration, and run the analysis.

**Identity partner account (Account 3):**

- [Download the identity partner worksheet](/static/samples/clean-rooms/multi-party-insights-identity-partner.sql).
  Run this to generate customer spine data, register a data offering, and review and join the collaboration.
