# Listing manifest reference

Creating Snowflake listings programmatically requires a manifest, written in YAML
(<https://yaml.org/spec/>). Use the information provided here to learn about the manifest format and its individual
sections.

See also:
:   [CREATE LISTING](/sql-reference/sql/create-listing), [ALTER LISTING](/sql-reference/sql/alter-listing), [DESCRIBE LISTING](/sql-reference/sql/desc-listing), [SHOW LISTINGS](/sql-reference/sql/show-listings), [DROP LISTING](/sql-reference/sql/drop-listing)

Note

Fields can be any of:

- Optional - Optional for either marketplace listings or private listings.
- Required - Required for either marketplace listings or private listings.
- Qualified - requirements differ for marketplace listings or private listings and optional vs required is qualified by listing type.
  For example optional for private listings, but required for marketplace listings.

The general format of a listing manifest is:

Copy code

```
#
# Listing prefix
#
title: <listing title>
subtitle: <Optional listing subtitle>
description: <listing description>
profile : <Optional name of the provider profile>

listing_terms:
  - # Required listing terms that the consumer must sign.
targets:
  - # Required <List> Consumer accounts to target with this private listing.
auto_fulfillment:
  - # Required when the target accounts are outside the provider's region, otherwise optional.
resharing:
  # Optional; Controls whether the listing can be reshared by consumers.
business_needs:
  - # Optional <List> BusinessNeed elements; maximum 6.
categories:
  - # Optional <List> The category or area the listing belongs to, maximum 1.
cke_content_protection:
  - # Optional <List> CKE content protection elements; maximum 1.
compliance_badges:
  - # Optional <List> Compliance badges; maximum 6.
data_attributes:
  - # Optional <Name Value pairs> DataAttributes elements; maximum 1.
data_dictionary:
  - # Required for public listings and optional for all other listing types.
data_preview:
  - # Required for public listings and optional for all other listing types.
draft_access_type:
  - # Required <String> for "by request" listings.
locations:
  - # Optional list of regions to share into.
monetization_display_order:
  - # Optional <List> MonetizationDisplayOrder elements.
offers:
  - # Optional <List> Offer elements; maximum 100.
pricing_plans:
  - # Optional <List> PricingPlan elements; maximum 100.
resources:
  - # Optional for private listings; required for marketplace listings, <Name Value pairs> Resources elements such as documentation and media.
trial_details:
  - # Optional <Name Value pairs> Provides details about a trial listing.
usage_examples:
  - # Optional <List> UsageExample elements; maximum 10.
share_restrictions:
  # Optional <Boolean> Enable share restrictions for this listing.
```

The following sections detail each listing manifest field and child field and provide associated examples.

## Listing prefix

Each listing manifest starts with the following fields:

- `title` (String, required, maximum length 110): Listing title.
- `subtitle` (String, optional for private, required for marketplace listings, maximum length 110): Listing subtitle.
- `description` (String, required, maximum length 7500): Listing description. Markdown syntax is supported.
- `custom_contact` (String, optional): Email. Must be a valid, well formed email address.
- `profile` (String, optional for private listings, required for marketplace listings): Name of an approved provider profile.

For more information, refer to: [Provider basic information](https://other-docs.snowflake.com/collaboration/provider-listings-reference#label-configuring-metadata-for-data-listing).

Note

Values for `profile` can be found by executing `show profiles in data exchange SNOWFLAKE_DATA_MARKETPLACE;`.

### Listing prefix example

Copy code

```
title: Weather information
subtitle: Historical weather by postcode.
description: This listing includes historical weather data by post code.
profile: My provider profile
```

## `listing_terms`

The **required** `listing_terms` (required) field contains the following name value pairs:

- `listing_terms.type` (enum, required): must be one of:

  - `STANDARD` - Refers to the Standard Agreement for Marketplace Products.
  - `OFFLINE` - Indicates that terms are negotiated offline by the parties.
  - `CUSTOM` - When specified, must specify a value for `listing_terms.link`.
- `listing_terms.link` (required when type is CUSTOM): A fully qualified link to the provider’s listing terms, must start with `http` or `https`.

For more information, refer to **Terms of Service** in the table in [Basic information](https://other-docs.snowflake.com/collaboration/provider-listings-reference#label-configuring-metadata-for-data-listing).

Note

Consumers can accept listing terms programmatically. For more information contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

### `listing_terms` example

Copy code

```
. . .
listing_terms:
  type: "CUSTOM"
  link: "http://example.com/my/listing/terms"
. . .
```

## `targets`

Note

This field can only be used with [V1 listings](/collaboration/collaboration-listings-about#label-v1-vs-v2-listings).

The `targets` field is required for marketplace and private listings.

Contains a list, maximum of 100 elements:

- `targets.accounts` (Required if `targets.region` not present): List of accounts with which to share the listing.

  Each target account must be in `<OrgName>.<AccountName>` format, where:

  - `OrgName` can be obtained using [SELECT CURRENT\_ORGANIZATION\_NAME();](/sql-reference/functions/current_organization_name).
  - `AccountName` can be obtained from account\_name using [SHOW ACCOUNTS](/sql-reference/sql/show-accounts) or using Snowsight.

or

- `targets.regions` (Required if `targets.accounts` not present):

  List of regions with which to share the listing.

  Each target region must be of the form “region\_groups\_type.snowflake\_region”.
  In addition, “ALL” is supported for including all regions.

  For example “PUBLIC.AWS\_US\_EAST\_1”.

  For a complete list of region group types and Snowflake regions execute:

  Copy code

  ```
  SHOW REGIONS IN DATA EXCHANGE SNOWFLAKE_DATA_MARKETPLACE;
  ```

For more information, see [Required for public listings. At least 1 business need is required.](/collaboration/provider-listings-reference#label-listing-provider-business-need).

### `targets` examples

Define a set of target accounts for this listing.

Copy code

```
. . .
targets:
   accounts: ["Org1.Account1", "Org2.Account2"]
. . .
```

Define a set of target regions for this listing.

Copy code

```
. . .
targets:
   regions: ["PUBLIC.AWS_US_EAST_1", "PUBLIC.AZURE_WESTUS2"]
. . .
```

## `auto_fulfillment`

Cross-Cloud Auto-fulfillment allows the data product associated with a listing
to be automatically fulfilled to other Snowflake regions.
The `auto_fulfillment` field defines how that auto-fulfillment takes place.

For more information on Cross-Cloud Auto-fulfillment, see [Auto-fulfillment for listings](/collaboration/provider-listings-auto-fulfillment).

Auto-fulfillment is only required if you’re sharing data to multiple regions.
Do not enable it if you are sharing to accounts in the same region.

If you share data across multiple regions, the `auto_fulfillment` is:

- Required if your data product is an application package.
- Required if your data product is shared through a private listing.
- Recommended if your data product is shared through a public listing.

Contains the following name value pairs:

- `auto_fulfillment.refresh_schedule`
  - `<num> MINUTE` - Number of minutes. Minimum 10 minutes, maximum 8 days, or 11520 minutes.

    If `refresh_type` is specified as `SUB_DATABASE_WITH_REFERENCE_USAGE`, do not include this setting.
    The refresh schedule for application packages must be defined at the account level and cannot specified at the listing level.

    For more information see [Set the account-level refresh interval](/collaboration/provider-listings-auto-fulfillment-set-refresh-interval).

- `USING CRON <expression>` - Defines the data product auto-fulfillment refresh schedule.
  The syntax for `USING CRON` and `REPLICATION SCHEDULE` are the same. See [Parameters](/sql-reference/sql/create-replication-group#label-create-replication-group-parameters).
- `auto_fulfillment.refresh_type` (required when using `auto_fulfillment`): Must be one of -

  - `SUB_DATABASE` - database replication (object level) - recommended.
  - `SUB_DATABASE_WITH_REFERENCE_USAGE` - application package.
  - `FULL_DATABASE` - database replication (for the entire database). (Deprecated.)
- `auto_fulfillment.refresh_schedule_override` (optional): Overrides the defined update refresh frequency for all listings that use the same database. When this value is `FALSE`, listing updates fail when multiple listings sharing the same database have different refresh frequencies.

  - `TRUE` - enables the refresh frequency override.
  - `FALSE` - (default) disables the refresh frequency override.
- `auto_fulfillment.warehouse` (optional): The name of the warehouse used to create and refresh hidden dynamic tables for
  cross-region resharing. This warehouse is used only for resharing maintenance operations. Required when the listing is a reshared
  listing. Can be omitted for non-reshared listings.

See also [Auto-fulfillment for listings](/collaboration/provider-listings-auto-fulfillment).

### `auto_fulfillment.refresh_schedule` examples

The following example refreshes the data product associated with a listing every 10 minutes:

Copy code

```
. . .
listing_terms: . . .
. . .
auto_fulfillment:
  refresh_schedule: 10 MINUTE
  refresh_type: SUB_DATABASE
. . .
```

The following example refreshes the data product associated with a listing on specific days and times in specific regions:

Copy code

```
. . .
listing_terms: . . .
. . .
auto_fulfillment:
  refresh_schedule: USING CRON  0 17 * * MON-FRI Europe/London
  refresh_type: SUB_DATABASE
. . .
```

The following example enables the refresh frequency override for listings that share the same database but have different refresh frequencies:

Copy code

```
. . .
listing_terms: . . .
. . .
auto_fulfillment:
  refresh_schedule: 10 MINUTE
  refresh_type: SUB_DATABASE
  refresh_schedule_override: TRUE
. . .
```

### Snowflake Native App `auto_fulfillment` example

`SUB_DATABASE_WITH_REFERENCE_USAGE` can only be used with application packages
and cannot be combined with `auto_fulfillment.refresh_schedule`.

Copy code

```
. . .
listing_terms: . . .
. . .
auto_fulfillment:
  refresh_type: SUB_DATABASE_WITH_REFERENCE_USAGE
. . .
```

### Object level `auto_fulfillment` example

Copy code

```
. . .
listing_terms: . . .
. . .
auto_fulfillment:
  refresh_type: SUB_DATABASE
. . .
```

## `resharing`

The `resharing` field controls whether consumers of the listing can reshare the data product with other accounts.

For more information on resharing, see [Resharing listings](/collaboration/reshare-listings).

Contains the following name value pairs:

- `resharing.enabled` (optional): Enables or disables resharing for the listing.

  - `true` - (default) allows consumers to reshare the listing data.
  - `false` - prevents consumers from resharing the listing data.
- `resharing.only_within_organization` (optional): Specifies whether consumers can reshare the listing only within their own organization,
  or also with other organizations.

  - `true` - consumers can reshare the listing only within their own organization.
  - `false` - consumers can reshare the listing outside of their own organization.

  For organizational listings, the default behavior restricts resharing to within the same organization. For other listings, consumers
  can reshare to any account unless this restriction is added.

  For more information, see [To require that any consumer who reshares your listing can only reshare it to…](/collaboration/resharing-as-provider#label-resharing-restrict-org).

### `resharing` example

The following example enables resharing on a listing:

Copy code

```
. . .
listing_terms: . . .
. . .
resharing:
  enabled: true
. . .
```

The following example enables resharing on a listing to only within consumer organization:

Copy code

```
. . .
listing_terms: . . .
. . .
resharing:
  enabled: true
  only_within_organization: true
. . .
```

## `business_needs`

Listings are grouped by business needs for easy discovery.
Business need is a describes how a specific listing meets a given business need.
For more information, see [Required for public listings. At least 1 business need is required.](/collaboration/provider-listings-reference#label-listing-provider-business-need).

### STANDARD business needs

- `business_needs.name` (required when using `business_needs`):

  Valid values include:

  - “360-Degree Customer View”
  - “Supply Chain”
  - “Personalize Customer Experiences”
  - “Inventory Management”
  - “Accelerating Advertising Revenue”
  - “Attribution Analysis”
  - “Contact Data Enrichment”
  - “Foot Traffic Analytics”
  - “Audience Segmentation”
  - “Sentiment Analysis”
  - “ESG Investment Analysis”
  - “Fundamental Analysis”
  - “Quantitative Analysis”
  - “Risk Analysis”
  - “Fraud Remediation”
  - “Customer Onboarding”
  - “Identity Resolution”
  - “Asset Valuation”
  - “Economic Impact Analysis”
  - “Demand Forecasting”
  - “Population Health Management”
  - “Real World Data (RWD)”
  - “Location Planning”
  - “Regulatory Reporting”
  - “Subscriber Acquisition and Retention”
  - “Life Sciences Commercialization”
  - “Patient 360”
  - “Blockchain Analysis”
  - “Customer Acquisition”
  - “Data Quality and Cleansing”
  - “Location Data Enrichment”
  - “Location Geocoding”
  - “Machine Learning”
  - “Market Analysis”
  - “Pricing Analysis”
  - “Audience Activation”

`business_needs[].description` (required when using `business_needs`): Description of associated business\_needs.name, maximum length 1000.

`business_needs[].type`: STANDARD (optional).

### CUSTOM business needs

Custom business needs include a user defined `name`, `description`, and required `type` field with value CUSTOM.

`business_needs.name` (required when using `business_needs`): User defined name.

`business_needs[].description` (required when using `business_needs`): Description of associated business\_needs.name, maximum length 1000.

`business_needs[].type`: CUSTOM (required when defining custom business needs).

### `business_needs` examples

Standard without optional `type`

Copy code

```
. . .
business_needs:
 - name: "Real World Data (RWD)"
   description: "Global weather data"
. . .
```

Standard with optional `type`

Copy code

```
. . .
business_needs:
 - name: "Real World Data (RWD)"
   description: "Global weather data"
   type: STANDARD
. . .
```

Custom with required `type`

Copy code

```
. . .
business_needs:
 - name: "Machinery Maintenance"
   description: "Repair and maintenance data for machinery"
   type: CUSTOM
. . .
```

## `categories`

The `categories` field specifies the category or area the listing belongs to.
Categories are optional for private listings but required for marketplace listings.

Categories are used in Snowflake Marketplace to browse listings by area and help consumers find your data.

The `categories` field is a list, but can only contain a single entry, from the set below:

- BUSINESS
- CONNECTORS
- DEMOGRAPHICS
- ECONOMY
- ENERGY
- ENVIRONMENT
- FINANCIAL
- GOVERNMENT
- HEALTH
- IDENTITY
- LEGAL
- LOCAL
- LOOKUP\_TABLES
- MARKETING
- MEDIA
- SECURITY
- SPORTS
- TRANSPORTATION
- TRAVEL
- WEATHER

### `categories` example

Copy code

```
. . .
categories:
 - ECONOMY
. . .
```

## `cke_content_protection`

The `cke_content_protection` field is used to protect the content of a Cortex Knowledge Extension (CKE). Using this field, providers can restrict the amount of content a consumer can access. The threshold limits the percentage of the indexed corpus that a consumer can retrieve within a rolling 24-hour period. When a consumer exceeds the configured threshold, subsequent queries to the CKE are blocked until the window resets, and the consumer receives an error indicating that they’ve reached the content protection threshold.

The `cke_content_protection` field contains the following entries:

- `enable`: Indicates whether content protection is enabled.

  - `TRUE` - Content protection is enabled.
  - `FALSE` - Content protection is disabled.
- `threshold`: The threshold for content protection when content protection is enabled. This indicates the percentage of the indexed corpus that any one consumer can retrieve within a rolling 24-hour period. This can be a value between 0 and 1.

### `cke_content_protection` example

Copy code

```
. . .
cke_content_protection:
  enable: TRUE
  threshold: 0.2
. . .
```

## `compliance_badges`

The `compliances_badges` field is used to indicate that a listing was reviewed by a third-party auditor and was certified as compliant with a specific standard or regulation.

When you configure a compliance badge, you can specify up to six types. Include the expiration date for each badge and the accompanying third-party certification documentation.

The following fields are used to configure a compliance badge:

- `compliance_badges`: Used to declare and configure a compliance badge for a listing. Providers can declare multiple compliance certifications within the `compliance_badges` property.
  - `type`: The compliance certification being requested. The following list shows the possible values:

    - `SOC2`
    - `FEDRAMP`
    - `GDPR`
    - `HIPAA`
    - `ISO27001`
    - `PCIDSS`
  - `expiry`: The date when the compliance certification expires.
  - `files`: The list of files that are used to verify the compliance certification.

For more information, see [Compliance certifications](/collaboration/provider-listings-reference#label-listings-compliance-certifications).

### `compliance_badges` example

Copy code

```
. . .
compliance_badges:
  - type: SOC2
    expiry: 12-25-2026
    files:
      - soc2_compliance_verification.pdf
  - type: HIPAA
    expiry: 06-07-2026
    files:
      - hipaa_compliance_verification.pdf
  - type: FEDRAMP
    expiry: 03-15-2027
    files:
      - fedramp_compliance_verification.pdf
. . .
```

## `data_attributes`

Data attributes provide consumers insight into information about the listing such as refresh rate and other characteristics.

The `data_attributes` field is optional for private listings but required for marketplace listings.

For additional information on data product attributes, see [Required for public listings. Define additional attributes that](/collaboration/provider-listings-reference#label-listings-data-product-attributes).

Contains the following name value pairs:

- `data_attributes.refresh_rate` (required for data listings; optional for app listings)

  Specifies how often your data product is updated in Snowflake.

  One of:

  - CONTINUOUSLY
  - HOURLY
  - DAILY
  - WEEKLY
  - MONTHLY
  - QUARTERLY
  - ANNUALLY
  - STATIC
- `data_attributes.geography` (required), containing:

  Specifies the geographic regions for which your data product has coverage.

  - `granularity` (string, required)

    Geographic coverage of your dataset.

    One of:

    - LATITUDE\_LONGITUDE
    - ADDRESS
    - POSTAL\_CODE
    - CITY
    - COUNTY
    - STATE
    - COUNTRY
    - REGION\_CONTINENT
  - `geo_option` (string, required)

    One of:

    - NOT\_APPLICABLE
    - GLOBAL
    - COUNTRIES
  - `coverage` (required based on selection of `geo_option`), containing either :

    - `states` (list of states) containing any list of valid U.S. state names.

    Or

    - `continents` (list of continents):

      Any of:

      - ASIA
      - EUROPE
      - AFRICA
      - NORTH AMERICA
      - SOUTH AMERICA
      - OCEANIA
      - ANTARCTICA
  - `time` (required) containing:

    Specifies the time period that your data product covers.

    - `granularity` (required)

    One of:

    - EVENT\_BASED
    - HOURLY
    - DAILY
    - WEEKLY
    - MONTHLY
    - YEARLY
    - `time_range` (required) containing the following name/value pairs:
      - `time_frame` (required)

        One of:

        - NEXT
        - LAST
        - BETWEEN
      - `unit` (required)
        One of:

        - DAYS
        - WEEKS
        - MONTHS
        - YEARS
      - `value` (required when `time_frame` is NEXT/LAST, integer), range 1-100.
      - `start_time` (required when `time_frame` is BETWEEN, String date), format MM-DD-YYYY.
      - `end_time` (required when `time_frame` is BETWEEN, String date), format MM-DD-YYYY.

### `data_attributes` example

Copy code

```
. . .
data_attributes:
  refresh_rate: DAILY
  geography:
    granularity:
      - REGION_CONTINENT
    geo_option: COUNTRIES
    coverage:
      continents:
        ASIA:
          - INDIA
          - CHINA
        NORTH AMERICA:
          - UNITED STATES
          - CANADA
        EUROPE:
          - UNITED KINGDOM
    time:
      granularity: MONTHLY
      time_range:
        time_frame: LAST
        unit: MONTHS
        value: 6
```

## `data_dictionary`

The `data_dictionary` field provides consumers insight into the contents and structure of a listing before they install it into their account.
Required for public listings, optional for all other listing types.

The `data_dictionary` field contains a list of up to five data dictionary entries:

- `data_dictionary.featured` (required when using `data_dictionary`): must be ‘featured’.
- `data_dictionary.featured.database` (required when using `data_dictionary`): database name.
- `data_dictionary.featured.objects` (required when using `data_dictionary`): list of name value pairs -
  - `name` (string, required): object name
  - `schema` (string, required): schema
  - `domain` (required):

    One of:

    - DATABASE
    - SCHEMA
    - TABLE
    - VIEW
    - EXTERNAL\_TABLE
    - MATERIALIZED\_VIEW
    - DIRECTORY\_TABLE
    - FUNCTION
    - COLUMN

See also [Data product - data dictionary](https://other-docs.snowflake.com/collaboration/provider-listings-reference#label-listings-data-dictionaries).

### `data_dictionary` example

Copy code

```
. . .
data_dictionary:
 featured:
    database: "WEATHERDATA"
    objects:
       - name: "GLOBAL_WEATHER"
         schema: "PUBLIC"
         domain: "TABLE"
       - name: "GLOBAL_WEATHER_REPORT"
         schema: "PUBLIC"
         domain: "TABLE"
. . .
```

## `data_preview`

The `data_preview` field allows providers to identify and hide Personally identifiable information (PII) in the data preview samples generated from listing data. PII data is data that could directly or indirectly reveal an individual’s identity. Required for public listings, and optional for all other listing types.

The `data_preview` field includes the following entries:

- `data_preview.has_pii` (required when using `data_preview`): indicates whether PII is included in the listing data.

  - `TRUE` - PII is included in the listing data.
  - `FALSE` - PII is not included in the listing data.
- `data_preview.metadata_overrides` (recommended when `data_preview.has_pii` is `TRUE` ): identifies the location of the PII listing data and the objects within that dataset containing PII to hide or expose.

  - `database` (string, required): Database name.
  - `objects` (list, required): The objects to hide or expose columns from in the data preview samples:
    - `schema` (string, required): Schema name.
    - `domain` (string, required): Domain name.
    - `name` (string, required): Object name
    - `pii_columns` (list, optional): The columns containing PII.
    - `overridden_pii_columns` (list, optional): The columns Snowflake classification identified as containing PII, but should be available in the data preview samples shared with consumers.

      Periodically, Snowflake runs classifications on generated data previews. Any columns containing PII are defined in `classified_pii_columns` when `SHOW` commands are run.

      Columns identified by Snowflake as containing PII are hidden from consumers of the listing only in the data preview samples. If a provider of a listing determines the columns are erroneously identified as containing PII, they can specify the specific columns they want included in the data preview samples using `overridden_pii_columns`.

### `data_preview` example

Copy code

```
. . .
data_preview:
 has_pii: TRUE
 metadata_overrides:
    database: WEATHERDATA
    objects:
       - schema: PUBLIC
         domain: TABLE
         name: GLOBAL_WEATHER
         pii_columns: [ADDRESS, PHONE]
         overridden_pii_columns: [FIRST_NAME, LAST_NAME]
. . .
```

## `draft_access_type`

Specifies how access to a draft listing is controlled.

This field determines the access model for the listing while it’s in draft status. This is especially relevant for [compliance badging](/collaboration/provider-listings-reference#label-listings-compliance-certifications), as providers await approval of a listing’s badge or badges by the Snowflake compliance team.

The allowed values for `draft_access_type` are:

- UNKNOWN
- FREE
- PAID
- LIMITED\_TRIAL

### `draft_access_type` examples

> Copy code
>
> ```
> . . .
> draft_access_type: "PAID"
> . . .
> ```

## `external_targets`

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

The `external_targets` field is used to share public or private V2 listings.

Note

This field can only be used with [V2 listings](/collaboration/collaboration-listings-about#label-v1-vs-v2-listings).

The `access` field is **required** when `external_targets` is specified, and it must include one of the following sub-fields:

- `organization`: When creating a private listing, specify the organization name and accounts that can access the listing.
- `account`: When creating a private listing, specify the organization name and accounts that can access the listing.
- `all_organizations`: When creating a public listing, set this to `true`.

### `external_targets` examples

The follow example shows how to use `external_targets` to share private listings.

> Copy code
>
> ```
> . . .
> external_targets:
>   access:
>     - organization: OrgName2
>       accounts: [acc1, acc2]
> . . .
> ```

The follow example shows how to use `external_targets` to share public listings.

> Copy code
>
> ```
> . . .
> external_targets:
>   access:
>     - all_organizations: true
> . . .
> ```

## `locations`

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Specifies the **optional** `locations` that can discover or access the listing.

Note

This field can only be used with [V2 listings](/collaboration/collaboration-listings-about#label-v1-vs-v2-listings).

The `access_regions` field is **required** when `locations` is specified, and it must include one of the following sub-fields:

- `ALL`: All regions can discover or access the listing.
- `name`: An array of regions of the form “region\_groups\_type.snowflake\_region” that can discover or access the listing; for example, *access\_regions: - name: PUBLIC.AWS\_US\_WEST\_2*.

Available region groupings for VPS deployments include the following:

- AWS\_US\_EAST\_1 (“US East (N. Virginia)”)
- AWS\_US\_EAST\_2 (“US East (Ohio)”)
- AWS\_US\_WEST\_2 (“US West (Oregon)”)
- AWS\_EU\_WEST\_1 (“EU (Ireland)”)
- AWS\_EU\_WEST\_2 (“EU (London)”)
- AZURE\_EASTUS2 (“East US 2 (Virginia)”)
- AZURE\_CENTRALUS (“Central US (Iowa)”)

### `locations` example

> Copy code
>
> ```
> . . .
> locations:
>   access_regions:
>     - name: "PUBLIC.AWS_US_WEST_2"
> . . .
> ```

For a complete list of regions, see [SHOW REGIONS](/sql-reference/sql/show-regions).

## `monetization_display_order`

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

The optional `monetization_display_order` field specifies the order in which pricing plans are displayed to consumers in Snowflake Marketplace.

Note

This field can only be used with [V2 listings](/collaboration/collaboration-listings-about#label-v1-vs-v2-listings).

### `monetization_display_order` example

Copy code

```
. . .
monetization_display_order:
  - offer_id_1
  - offer_id_2
  - offer_id_3
. . .
```

## `offers`

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Note

This field can only be used with [V2 listings](/collaboration/collaboration-listings-about#label-v1-vs-v2-listings).

The optional `offers` field includes a list of up to eight offers that are associated with the listing. The `offers` field includes the following name value pairs:

- `name` (String, required ): The user-defined name of the offer. The name must be formatted as all uppercase.
- `type` (String, required): Must be one of the following types:

  - `FILE`: Indicates that the offer is defined in a local YAML file.
  - `URL`: Indicates that the offer is defined in a remote URL.
- `path` (String, required): The path to the local or remote [offers YAML](/user-guide/collaboration/listings/pricing-plans-offers/offer-manifest-reference).

### `offers` example

Copy code

```
. . .
offers:
  - name: PRICING_PLAN_1_DEFAULT_OFFER
    type: FILE
    path: offers/PRICING_PLAN_1_DEFAULT_OFFER.yaml
. . .
```

## `pricing_plans`

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Note

This field can only be used with [V2 listings](/collaboration/collaboration-listings-about#label-v1-vs-v2-listings).

The optional `pricing_plans` field includes a list of pricing plans that are associated with the listing. The `pricing_plans` field includes the following name value pairs:

- `name` (String, required): The user-defined name of the pricing plan. The name must be formatted as all uppercase.
- `type` (String, required): Must be one of the following types:

  - `FILE`: Indicates that the offer is defined in a local YAML file.
  - `URL`: Indicates that the offer is defined in a remote URL.
- `path` (String, required): The path to the local or remote [pricing plan YAML](/user-guide/collaboration/listings/pricing-plans-offers/pricing-plan-manifest-reference).

### `pricing_plans` example

Copy code

```
. . .
pricing_plans:
  - name: PRICING_PLAN_1
    type: FILE
    path: pricingPlans/PRICING_PLAN_1.yaml
. . .
```

## `resources`

Resources contain information about the listing, including links to documentation and a video.

The `resources` field is optional for private listing but required for marketplace listings.

Contains the following name value pairs:

- `resources.documentation` (String, required ): A fully qualified link to a page on your website with more detailed documentation for the listing.
  Must start with `http` or `https`.
- `resources.media` (String, optional): A fully qualified link to an unlisted or public YouTube video for the listing.

For more information see [Additional fields](/collaboration/provider-listings-reference#label-configuring-metadata-for-data-listing-details).

### `resources` example

Copy code

```
. . .
resources:
  documentation: https://www.example.com/documentation/
  media: https://www.youtube.com/watch?v=MEFlT3dc3uc
. . .
```

## `trial_details`

The optional `trial_details` field captures trial details associated with the listing and includes the following name value pairs:

- `trial_type` (String, required ): Specifies the type of the trial. Must be one of the following types:

  - `TIME`
  - `USAGE`
  - `LIMITED`
  - `LIMITED_TIME`
- `trial_time_limit` (Integer, optional): Specifies the number of days that the listing will be allowed as a trial, after which the consumer would need to request the full product. A null value indicates that the listing is an unlimited time trial. Either `trial_time_limit` or `trial_usage_limit` must be specified.
- `trial_usage_limit` (Integer, optional): Specifies the number of allowed free uses with this listing, after which the consumer would need to upgrade. Either `trial_time_limit` or `trial_usage_limit` must be specified.
- `trial_usage_unit` (Long, optional): Specifies the unit (such as queries or rows) for the trial usage. Depending on this usage unit, the usage count is incremented accordingly. This field can only be used with `trial-usage_limit`.
- `description` (String, optional): A string describing the trial details. The maximum length is 4,096 characters.

### `trial_details` example

Copy code

```
. . .
trial_details:
  trial_type: TIME
  trial_time_limit: 30
  description: "This is a 30-day free trial"
. . .
```

## `usage_examples`

The `usage_examples` field is optional for private listings but required for marketplace listings.

Contains a list of the following name value pairs:

- `usage.title` (String, required): Usage example title; maximum length 110 characters.
- `usage.description` (String, optional): Associated description; maximum length 300 characters.
- `usage.query` (String, required): Query associated with the usage example; maximum length 30,000 characters.

For more information, see [Required for public listings with a Secure Share data product.](/collaboration/provider-listings-reference#label-provider-listing-reference-sample-sql-queries).

### `usage_examples` example

Copy code

```
. . .
usage_examples:
  - title: "Return all weather for the US"
    description: "Example of how to select weather information for the United States"
    query: "select * from weather where country_code='USA'";
. . .
```

## `share_restrictions`

The `share_restrictions` field controls whether edition and HIPAA share restrictions are enforced for this listing.
When set to `TRUE`, Snowflake prevents consumer accounts in lower editions from accessing a listing from a
Business Critical (or higher) provider, and prevents non-HIPAA consumer accounts from accessing a listing from a
HIPAA provider.

This field is only supported for private external listings. It can’t be used for public listings, organizational
listings, or private listings that target the entire organization.

If this field isn’t provided during a listing update, the existing value is preserved. To disable share restrictions
for a listing, explicitly set the field to `FALSE`.

You can also enable share restrictions at the account level for all listings. For more information, see
[Listing share restrictions](/collaboration/listing-share-restrictions).

### `share_restrictions` example

Copy code

```
. . .
share_restrictions: TRUE
. . .
```

## Complete YAML example for a V1 data share listing

[V1 listings](/collaboration/collaboration-listings-about#label-v1-vs-v2-listings) use `targets` to define the accounts that can access the listing.

Copy code

```
title: "Covid data listing"
subtitle: "Listing about covid"
description: "Example covid manifest"
profile: "MyProfile"
listing_terms:
  type: "STANDARD"
targets:
  accounts: ["Org1.Account1", "Org2.Account2"]
auto_fulfillment:
  refresh_schedule: "120 MINUTE"
  refresh_type: "SUB_DATABASE"
business_needs:
  - name: "Life Sciences Commercialization"
    description: "COVID-19 Epidemiological Data"
usage_examples:
  - title: "Get total case count by country"
    description: "Calculates the total number of cases by country, aggregated over time."
    query: "SELECT  COUNTRY_REGION, SUM(CASES) AS Cases FROM ECDC_GLOBAL GROUP BY COUNTRY_REGION;"
data_attributes:
  refresh_rate: HOURLY
  geography:
    granularity:
      - ADDRESS
    geo_option: COUNTRIES
    coverage:
      continents:
        ASIA:
          - INDIA
          - CHINA
        NORTH AMERICA:
          - UNITED STATES
          - CANADA
        EUROPE:
          - UNITED KINGDOM
    time:
      granularity: MONTHLY
      time_range:
      time_frame: BETWEEN
      start_date: 12-24-2020
      end_date: 12-25-2021
data_preview:
  has_pii: TRUE
  metadata_overrides:
    database: WEATHERDATA
    objects:
      schema: PUBLIC
      domain: TABLE
      name: GLOBAL_WEATHER
      pii_columns: [ADDRESS, PHONE]
      overridden_pii_columns: [FIRST_NAME, LAST_NAME]
resources:
  documentation: https://www.example.com/documentation/
  media: https://www.youtube.com/watch?v=MEFlT3dc3uc
categories:
  - HEALTH
compliance_badges:
  - type: SOC2
    expiry: 12-25-2026
    files:
      - soc2_compliance_verification.pdf
  - type: HIPAA
    expiry: 06-07-2026
    files:
      - hipaa_compliance_verification.pdf
  - type: FEDRAMP
    expiry: 03-15-2027
    files:
      - fedramp_compliance_verification.pdf
cke_content_protection:
  enable: TRUE
  threshold: 0.2
trial_details:
  trial_type: TIME
  trial_time_limit: 30
  description: "This is a 30-day free trial"
```

## Complete YAML example for a V2 data share listing

[V2 listings](/collaboration/collaboration-listings-about#label-v1-vs-v2-listings) use `external_targets` to define the organizations and roles that can access the listing. V2 listings also allow users to define pricing plans and offers.

Copy code

```
title: "Covid data listing"
subtitle: "Listing about covid"
description: "Example covid manifest"
profile: "MyProfile"
listing_terms:
  type: "STANDARD"
external_targets:
  access:
    - organization: OrgName2
      accounts: [acc1, acc2]
    - account: acc2
      roles: [role1, role2]
auto_fulfillment:
  refresh_schedule: "120 MINUTE"
  refresh_type: "SUB_DATABASE"
business_needs:
  - name: "Life Sciences Commercialization"
    description: "COVID-19 Epidemiological Data"
usage_examples:
  - title: "Get total case count by country"
    description: "Calculates the total number of cases by country, aggregated over time."
    query: "SELECT  COUNTRY_REGION, SUM(CASES) AS Cases FROM ECDC_GLOBAL GROUP BY COUNTRY_REGION;"
data_attributes:
  refresh_rate: HOURLY
  geography:
    granularity:
      - ADDRESS
    geo_option: COUNTRIES
    coverage:
      continents:
        ASIA:
          - INDIA
          - CHINA
        NORTH AMERICA:
          - UNITED STATES
          - CANADA
        EUROPE:
          - UNITED KINGDOM
    time:
      granularity: MONTHLY
      time_range:
      time_frame: BETWEEN
      start_date: 12-24-2020
      end_date: 12-25-2021
data_preview:
  has_pii: TRUE
  metadata_overrides:
    database: WEATHERDATA
    objects:
      schema: PUBLIC
      domain: TABLE
      name: GLOBAL_WEATHER
      pii_columns: [ADDRESS, PHONE]
      overridden_pii_columns: [FIRST_NAME, LAST_NAME]
locations:
  access_regions:
    - name: "PUBLIC.AWS_US_WEST_2"
monetization_display_order:
  - offer_id_1
pricing_plans:
  - name: PRICING_PLAN_1
    type: FILE
    path: pricingPlans/PRICING_PLAN_1.yaml
offers:
  - name: PRICING_PLAN_1_DEFAULT_OFFER
    type: FILE
    path: offers/PRICING_PLAN_1_DEFAULT_OFFER.yaml
resources:
  documentation: https://www.example.com/documentation/
  media: https://www.youtube.com/watch?v=MEFlT3dc3uc
categories:
  - HEALTH
compliance_badges:
  - type: SOC2
    expiry: 12-25-2026
    files:
      - soc2_compliance_verification.pdf
  - type: HIPAA
    expiry: 06-07-2026
    files:
      - hipaa_compliance_verification.pdf
  - type: FEDRAMP
    expiry: 03-15-2027
    files:
      - fedramp_compliance_verification.pdf
draft_access_type: "LIMITED_TRIAL"
cke_content_protection:
  enable: TRUE
  threshold: 0.2
trial_details:
  trial_type: TIME
  trial_time_limit: 30
  description: "This is a 30-day free trial"
```
