# Manage listings with SQL as a provider - examples

The following are examples of the common tasks that providers can complete programmatically with SQL commands:

- [Share data with another Snowflake account](#share-data-with-another-snowflake-account)
- [Share private listing and replicate](#share-private-listing-and-replicate)
- [Share publicly in the Marketplace](#share-publicly-in-the-marketplace)
- [Create a draft private listing ready for sharing with another account](#create-a-draft-private-listing-ready-for-sharing-with-another-account)

## Share data with another Snowflake account

Create a private listing for MySHARE and publish immediately.

| Description | Notes |
| --- | --- |
| Create a listing targeted to another account. | Submit the listing for immediate approval (`REVIEW=TRUE` default but shown for clarity).  Publish on approval (`PUBLISH=TRUE` default but shown for clarity). |

Expand

Show lessSee more

Copy code

```
CREATE EXTERNAL LISTING SHARED_WITH_ANOTHER_ACCOUNT
SHARE MySHARE AS
$$
   title: "weather data"
   description: "Listing of weather data for all zipcodes in America"
   listing_terms:
     type: "OFFLINE"
   targets:
     accounts: ["targetorg.targetaccount"]
$$ PUBLISH=TRUE REVIEW=TRUE;
```

## Share private listing and replicate

Create a private listing which is automatically replicated to other regions.

| Description | Notes |
| --- | --- |
| Create a replicated private listing. | Replicate the listing and refresh every 10 minutes.  Submit the listing for immediate approval (`REVIEW=TRUE` by default).  Publish on approval (`PUBLISH=TRUE` by default). |

Expand

Show lessSee more

Copy code

```
CREATE EXTERNAL LISTING SHARED_AND_REPLICATED
SHARE MySHARE AS
$$
   title: "weather data"
   description: "Listing containing weather data for all zipcodes in America"
   listing_terms:
     type: "OFFLINE"
   targets:
     accounts: ["targetorg.targetaccount"]
   auto_fulfillment:
     refresh_type: SUB_DATABASE
     refresh_schedule: '10 MINUTE'
$$;
```

For more information on cross-cloud auto fulfillment see [Auto-fulfillment for listings](/collaboration/provider-listings-auto-fulfillment).

## Share publicly in the Marketplace

Create a public listing in the Snowflake marketplace.

| Description | Notes |
| --- | --- |
| Create a replicated public listing in Marketplace.  Replicate the listing into multiple regions. | Replicate the listing and refresh every 10 minutes.  Submit the listing for immediate approval (`REVIEW=TRUE` by default, not shown).  Publish on approval (`PUBLISH=TRUE` by default, not shown). |

Expand

Show lessSee more

Copy code

```
CREATE EXTERNAL LISTING PUB_SHARE_AND_REPLICATE
SHARE MySHARE AS
$$
 title: "Weather Data"
 subtitle: "Weather Data on Snowflake"
 description: "This listing contains weather data for all zipcodes in America"
 terms_of_service:
   type: "STANDARD"
 targets:
   regions: ["PUBLIC.US_WEST", "PUBLIC.AWS_US_EAST_1"]
 auto_fulfillment:
   refresh_schedule: "10 MINUTE"
   refresh_type: "SUB_DATABASE"
 profile: "VERY_STARK_INDUSTRIES_PUBLIC_PROFILE"
 categories: ["BUSINESS"]
 data_dictionary:
   featured:
     database: "DATABASE_NAME"
     objects:
       - schema: "SCHEMA_NAME"
         domain: TABLE
         name: "TABLE_NAME"
 business_needs:
   - name: "Data Quality and Cleansing"
     description: "Test listing for data cleansing"
 usage_examples:
   - title: "Aggregate Weather data for a location"
     description: "Calculate the minimum and maximum temperatures over a year"
     query: "SELECT 1"
 data_attributes:
   refresh_rate: "HOURLY"
   geography:
     geo_option: "NOT_APPLICABLE"
 resources:
   documentation: "https://snowflake.com/doc"
   media: "https://www.youtube.com/watch?v=AR88dZG-hwo"
 $$;
```

## Create a draft private listing ready for sharing with another account

Create a draft listing which is automatically replicated to other regions.

This example is identical to [Share data with another Snowflake account](#share-data-with-another-snowflake-account) but creates a draft listing.
For a complete description of all combinations of the REVIEW and PUBLISH properties,
and their meanings, see [CREATE LISTING](/sql-reference/sql/create-listing).

| Description | Notes |
| --- | --- |
| Create a replicated private listing. | Replicate the listing and refresh every 10 minutes.  Do not submit the listing for approval (`REVIEW=FALSE`).  Do not publish (`PUBLISH=FALSE`). |

Expand

Show lessSee more

Copy code

```
CREATE EXTERNAL LISTING DRAFT_PRIVATE_REPLICATED
SHARE MySHARE AS
$$
   title: "weather data"
   description: "Listing containing weather data for all zipcodes in America"
   listing_terms:
     type: "OFFLINE"
   targets:
     accounts: ["targetorg.targetaccount"]
   auto_fulfillment:
     refresh_type: SUB_DATABASE
     refresh_schedule: '10 MINUTE'
$$ PUBLISH=FALSE REVIEW=FALSE;
```
