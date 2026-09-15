# Prepare data for a listing

This topic contains guidance for preparing to create a listing, including how to prepare a data product for different types of listings.

## Prepare to create a listing

Before you create a listing, do the following:

1. Decide how to offer your data product. See [Listing availability options](/collaboration/collaboration-listings-about#label-listing-availability) and [Listing access options](/collaboration/collaboration-listings-about#label-listing-access-types).
2. Set up roles and privileges to simplify creating listings. See [Set up roles and privileges for listings](#label-set-up-access-listings).
3. Identify the objects that you want to share. See [Decide what to put in a listing](#label-decide-listing-contents).
4. Prepare the objects to be shared with others. See [Prepare the shares for your listing](#label-prepare-listing-shares).
5. Determine how you want to manage access to your data product:

   - Provide access for free, with no restrictions.
   - Charge for your listing by creating a paid listing. See [Prepare to offer a paid listing](#label-prepare-offer-paid-listings).
   - Offer limited access to your data product as a free trial, then offer unlimited access to your data product by request.
     See [Prepare to offer a limited trial listing](#label-prepare-limited-trial-listing).
6. Choose which cloud region(s) you want to offer your listing in. See [Prepare your listing to be shared in other regions](#label-considerations-for-creating-a-new-listing-different-region).

If you plan to list a Connected Application on the Snowflake Marketplace, complete the [Connected Application listing enablement steps](/collaboration/guidelines-reqs-for-listing-apps#label-connected-apps-pre-enablement) before you create a listing. See also [Connected Applications guidelines](/collaboration/guidelines-reqs-for-listing-apps#label-guidelines-reqs-connected-apps).

The listing and data share must be in compliance with the Snowflake [Provider Policies](https://www.snowflake.com/provider-policies/).

## Set up roles and privileges for listings

When you create a listing, you create it from the account that has the data or application package in it. The role that attaches a data
product to a listing and publishes the listing must be the same role that created, and therefore owns, the application package or share.
You cannot transfer the OWNERSHIP privilege for a share.

If you use a different role to create and manage the listing, grant the MODIFY privilege on the listing to the role
that owns the application package or share. For example:

Share or application package owner role:
:   OWNERSHIP privilege on the share or application package.
    MODIFY privilege on the listing.

Listing owner role:
:   OWNERSHIP privilege on the listing.

    Global CREATE LISTING privilege.

Within the provider account, you can use one of the following to create and manage listings:

ACCOUNTADMIN:
:   If you use the ACCOUNTADMIN role to create and manage listings, the ORGADMIN role must first
    [Delegate privileges to set up auto-fulfillment](/collaboration/provider-listings-auto-fulfillment-manage-privileges#label-delegate-laf-privileges).

Custom role:
:   If you use a custom role, the ORGADMIN role must first [Delegate privileges to set up auto-fulfillment](/collaboration/provider-listings-auto-fulfillment-manage-privileges#label-delegate-laf-privileges)
    to the ACCOUNTADMIN role, which can then be used to grant the relevant privileges to the custom role.

For more information about granting sharing privileges, see [Granting Privileges to Other Roles:](/user-guide/data-exchange-marketplace-privileges).

## Decide what to put in a listing

As you prepare to share data from your account with a listing, decide what to put in the listing.

First, make sure that the data you want to share is in Snowflake, and that you have the legal and contractual rights to share the data.
If needed, load the data that you want to share into Snowflake. See [Overview of data loading](/user-guide/data-load-overview).

Note

To the extent any data in your listing or data set is governed by any laws or contractual obligations, you must ensure that you have the
legal and contractual rights to share such data. For example, you can only share protected health information (PHI) through a personalized
listing and, to do so, you must: (1) have signed a business associate agreement (BAA) with Snowflake and the Consumer receiving the PHI,
and; (2) ensure that the Consumer has also signed a BAA with Snowflake. Also, while you can share personal data through both a free or
personalized listing, to do so you must have the applicable legal and contractual rights if the data is not publicly available.

Next, decide how to offer the data that you have as a listing. If you plan to offer listings on the Snowflake Marketplace or only as
private listings directly with specific customers, you might make different decisions about what to place inside the listing.

- Consider the availability of your data.
- Consider the consumers that you expect to access your listings.
- Consider the formats of the data that you select for the share, such as a table, view, secure view, or other database object.

For example, if you want to provide listings about dog grooming, you might make decisions like the following:

- Offer a publicly available free listing on the Snowflake Marketplace with information about dog breeds and fur length.
- Offer a limited trial listing on the Snowflake Marketplace with a sample data product that contains data about the time it takes to
  groom a standard poodle, with the option for consumers to request a full data product about grooming insights for more dog breeds.
- Offer a limited trial listing on the Snowflake Marketplace with a data product that contains data about the time it takes to groom any
  breed of dog, with the option for consumers to request unlimited access to your data product.
- Offer a private listing to a partner organization with insights about the length of time it takes to groom various dogs, and the
  typical frequency of grooming appointments for different dog breeds.

In this example, you offer valuable data on the Snowflake Marketplace, but offer more specific insights to an organization that you already
have a trusted business relationship with.

## Prepare the shares for your listing

You can create a share before creating a listing, or select the database, tables, and views to comprise your data product when you create
the listing. See [Create and configure shares](/user-guide/data-sharing-provider).

If you plan to offer many listings, create shares separately from listings so that you can more easily manage your data product. You cannot
provide multiple listings from the same share.

### Consider how to keep shares updated

Consider the maintenance of the data in your share. Over time, you might need to make changes to your data shares as the information that
you want to provide in listings changes.

You also need to consider how to keep the data in shares updated, and make sure that the contents of the share are useful to consumers.

If objects in a share are dropped and later recreated, you need to add the recreated objects to the share so that they remain available to
consumers. For example, if you refresh some data in the share by dropping and recreating a table in the database, you need to update the
share to include the recreated table.

### Prepare the data to be shared

Prepare the data that you want to share in your listing to be shared with others.

- Use unquoted object identifiers for tables, columns, and share names. Use only upper case and alphanumeric characters for object names to
  let listing consumers use the shared data objects without having to double-quote identifiers. See [Identifier requirements](/sql-reference/identifiers-syntax).
- Protect sensitive data in shared databases. Create secure views and use secure objects to control access to data. See
  [Use secure objects to control data access](/user-guide/data-sharing-secure-views)
- You can add shares that are already shared with a consumer account, such as with a direct share, to a listing.
- A share can only be attached to one listing. If a share has already been attached to a listing, you cannot attach it to another listing,
  even if the listing has been deleted.
- Do not use account-level roles to protect data, such as with a policy or a secure view definition. Auto-fulfillment does
  not replicate account-level roles. For more information about this restriction, see [Auto-fulfillment for objects that depend on account roles](/collaboration/provider-understand-auto-fulfillment-objects#label-listings-auto-fulfill-account-roles).
  Instead, use database roles and the [IS\_DATABASE\_ROLE\_IN\_SESSION](/sql-reference/functions/is_database_role_in_session) system function.
  For more information, see [Share data protected by a policy](/user-guide/data-sharing-policy-protected-data).

## Prepare to offer a limited trial listing

A limited trial listing lets you offer either a sample of your data product as a free trial, giving consumers insight into what might be
available from a full data product or limited time access to your full data product. Providers can set the availability period for limited trial listings from 1 to 90 days. For more information about limited trial listings, see [Limited trial listings](/collaboration/collaboration-listings-about#label-trial-listing).

If you choose to offer a sample of your full data product, the sample data product ideally provides a subset of the real data
included in your full data product and is representative of the full data product in the following ways:

- Contains the same columns.
- Contains the same or similar ranges and distributions of values in the data.

Limited trial listings include a data dictionary, so the general shape of the data in the full data product should be clear from the sample data product that you offer.

For example, if you are a dog training and grooming company, you might consider offering one of the following sample data products with a
limited trial listing:

| Sample data product recommendation | Sample data product example | Full data product example |
| --- | --- | --- |
| Contains a complete dataset for a specific complete attribute of the data. | Contains up-to-date grooming insights for a Standard Poodle. | Contains up-to-date grooming insights for all dog breeds. |
| Contains the full dataset for a specific, outdated time period. | Contains grooming insights and prices for all dog breeds from May, 2021. | Contains up-to-date grooming insights and prices for all dog breeds. |
| Contains synthetic data that is representative of the full data product. | Contains up-to-date insights and prices about training the fictional Acadian Hound dog breed. | Contains up-to-date insights and prices about training all dog breeds. |

Expand

Show lessSee more

Offering a relevant and complete subset of your full data product as the sample data product for your limited trial listing helps consumers
understand the value of your full data product and makes them more likely to request the full data product.

### Limit functionality of your Snowflake Native App for trial consumers

If you offer your Snowflake Native App on the Snowflake Marketplace as a limited trial listing and want to limit the functionality available to trial
consumers, use the [SYSTEM$IS\_LISTING\_TRIAL](/sql-reference/functions/system_is_listing_trial) system function when creating secure views, secure UDFs, or
Streamlit apps included in your Snowflake Native App.

Using the system function to control the visibility of data and UDF output means that you don’t have to maintain a separate
application package to limit functionality to trial consumers.

You can limit the functionality of the following:

- Secure view
- Secure user-defined function (UDF)
- Application logic, such as the setup script or a Streamlit app.

For more details about adding data content or UDFs to your application package, see:

- [Share data content in a Snowflake Native App](/developer-guide/native-apps/preparing-data-content).
- [Add application logic to an application package](/developer-guide/native-apps/adding-application-logic).

#### Example 1: Return different data in a view to consumers in a trial

To define a secure view that returns data only to consumers with access to the full version of your Snowflake Native App, you could use the
following example code:

Copy code

```
CREATE OR REPLACE SECURE VIEW limited_functionality_view
  AS
  SELECT *
    FROM db_name.schema_name.table_name
    WHERE SYSTEM$IS_LISTING_TRIAL() = false;
```

If a consumer that is trialing your Snowflake Native App attempts to query the view, they see no results.

#### Example 2: Show the output of a secure SQL UDF only to non-trial consumers

To define a secure SQL UDF `shared_function()` that returns results only to consumers with access to the full version of your Snowflake Native App,
you could use the following example code:

Copy code

```
CREATE OR REPLACE SECURE FUNCTION schema_name.shared_function()
  RETURNS VARCHAR
  AS
  $$
    CASE
      WHEN SYSTEM$IS_LISTING_TRIAL() = FALSE
        THEN 'full product'
      ELSE 'trial'
    END
  $$;
```

In this example, if a consumer is trialing your Snowflake Native App, when they call the secure UDF they see the output `trial`.

#### Example 3: Show a different Streamlit UI to trial consumers

You can also call the system function inside of a Streamlit app to limit the functionality of your Streamlit app in a Snowflake Native App.
For example, you can display one title in the UI to consumers that trial your Snowflake Native App, and another title to consumers with
full access to your Snowflake Native App.

Copy code

```
# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session

session = get_active_session()
# Here we assign result of our function to a variable
result = session.sql("SELECT SYSTEM$IS_LISTING__TRIAL()")

# Write directly to the app
if result:
  st.title("Enjoy your limited trial of this application!")
else:
  st.title("Welcome to the full version of this application!")
```

## Prepare to offer a paid listing

If you want to charge for your listing, you must do the following:

1. Determine if you can offer paid listings. See [Who can provide paid listings](/collaboration/provider-becoming#label-monetization-provider-region-support).
2. Prepare the data to offer a trial of the data. See [Prepare shares for a paid listing](#label-prepare-shares-paid-listings).
3. Decide on the pricing plan that best fits your listing. See [Paid listings pricing models](/collaboration/provider-listings-pricing-model) to review the available pricing plans.

### Where you can publish paid listings

Only providers in certain regions can publish paid listings. See [Who can provide paid listings](/collaboration/provider-becoming#label-monetization-provider-region-support).

In addition, paid listings can only be published to certain regions. See [Confirm your billing location is supported](/collaboration/consumer-listings-paying#label-monetization-consumer-region-support) to see to which
regions you can publish paid listings.

### Prepare shares for a paid listing

When you offer a paid listing on the Snowflake Marketplace, you must offer consumers the ability to trial the listing before they purchase it.
Trials are optional for paid private listings. As part of the trial, you can limit consumers to specific data and functionality, a specific
time period, or a combination.

If you choose to limit trial consumers to specific data and functionality, create a single share for your paid listing and use secure views and
a system function provided by Snowflake, [SYSTEM$IS\_LISTING\_PURCHASED](/sql-reference/functions/system_is_listing_purchased), to control which data is visible to
trial consumers and which data is available only to paying consumers.

Note

If your listing includes a secure user-defined function (UDF), you cannot limit visibility of the UDF. Both paying customers and trial
customers of your listing can view the secure UDF.

Refer to the following examples to create your own secure views to display different data to paying consumers and trial consumers.

If you want to allow trial consumers to use all data in your listing for a limited period of time, do not use the SYSTEM$IS\_LISTING\_PURCHASED
function in your view definitions for your share.

#### Example 1: Return data based on the purchase status of the account

Create a secure view that selects all columns in a table. The view returns rows only when queried within a consumer account that has
purchased your paid listing.

Copy code

```
CREATE SECURE VIEW paid_v
  AS
  SELECT
    *
  FROM
    paid_t
  WHERE
    SYSTEM$IS_LISTING_PURCHASED() = TRUE;
```

#### Example 2: Return a subset of rows based on the purchase status of the account

Create a secure view that returns a subset of rows based on the boolean value of a specific column in the data. In this example, the
underlying table contains a column named `is_free` that is used to determine which data to show to which consumers.

Some rows have `is_free` set to `TRUE`, indicating that the data in those rows can be shown to trial consumers. Other rows have
`is_free` set to `FALSE`, indicating that the data in those rows should be shown only to paying consumers.

This example view is set up to return all rows only when it is queried by a consumer account that has purchased the paid listing, otherwise
it returns only the rows where `is_free` is set to `TRUE`.

Copy code

```
CREATE SECURE VIEW paid_v
  AS
  SELECT
    *
  FROM
    paid_t
  WHERE
    is_free
    OR
    SYSTEM$IS_LISTING_PURCHASED() = TRUE;
```

#### Example 3: Return only the most recent rows based on the purchase status of the account

Create a secure view that returns only rows from the previous 7 days to a consumer account that is trialing, but has not yet purchased,
your paid listing.

This example uses a column with a timestamp data type to filter the data, but you can use other column data types in your secure view
definition.

Copy code

```
CREATE SECURE VIEW paid_v
  AS
  SELECT *
  FROM
    paid_t
  WHERE
    (timestamp > current_timestamp() - interval '7 days')
    OR
    SYSTEM$IS_LISTING_PURCHASED() = TRUE;
```

#### Validate secure views for paid and trial data

After you prepare your secure views, validate that you set them up correctly by simulating the experiences of paid and trial consumer
accounts. Run queries against the secure views to confirm that each type of consumer has access to the expected data.

Important

This method does not validate whether consumers can securely access your data. This method only validates whether the share works as
expected for your consumers.

To validate your shares, execute a query against a secure view using `SHARE_CONTEXT(SYSTEM$IS_LISTING_PURCHASED)`:

Copy code

```
EXECUTE USING SHARE_CONTEXT(SYSTEM$IS_LISTING_PURCHASED=>{ 'TRUE' | 'FALSE' })
  AS <query>
```

Where:

- `SYSTEM$IS_LISTING_PURCHASED` specifies whether you want to validate as a paid consumer, or as a trial or unpaid consumer. The valid
  values are:

  - `TRUE`, to validate the share as a paid consumer.
  - `FALSE`, to validate the share as a trial or unpaid consumer.
- `<query>` is the SQL query that you want to run against the secure view.

When you use the command to run your query, the query is executed against the share as though you are a consumer.

For example, suppose you have a share that you want to validate. Your share includes a secure view named `PURCHASED_VIEW`, which
protects all data from a table named `SHARE_TABLE`. You want to validate that the data can be accessed only by a consumer that
purchased the listing.

To confirm that trial consumers cannot access any data in the secure view, run the following query:

Copy code

```
EXECUTE USING share_context(system$is_listing_purchased=>'FALSE')
  AS
    SELECT
      *
    FROM
      example_database.example_schema.PURCHASED_VIEW
```

If the secure view works as expected and no data is accessible to trial consumers, your query returns the following response:

Copy code

```
Query produced no results
```

To confirm that your paid consumers have access to the data, run the following query:

Copy code

```
EXECUTE USING share_context(system$is_listing_purchased=>'TRUE')
  AS
    SELECT
      *
    FROM
      example_database.example_schema.PURCHASED_VIEW
```

If the secure view works as expected, your query returns all of the columns and rows in `SHARE_TABLE`, the desired outcome for paid
consumers.

## Prepare your listing to be shared in other regions

When you configure your listing, you can choose to offer it in different regions. Offering listings in other regions requires replicating data.

Consider the time it takes to replicate data and the costs involved in replication.

- For a listing in the Snowflake Marketplace, you can choose which regions to make your listing available in. When you do, you can manually
  replicate the data or use auto-fulfillment to make your product available to consumers that get your listing. See
  [Manually replicate data to fulfill a listing request](/collaboration/provider-listings-managing#label-manually-replicate-listing) or [Auto-fulfillment for listings](/collaboration/provider-listings-auto-fulfillment) for more details.
- For a private listing, you need to share your listing to the regions where your consumer’s accounts are. You use auto-fulfillment to
  replicate the product to the consumers that get your listing. See [Auto-fulfillment for listings](/collaboration/provider-listings-auto-fulfillment) for more details.

All cross-region data sharing at Snowflake uses Snowflake’s data replication functionality.
See [Share data securely across regions and cloud platforms](/user-guide/secure-data-sharing-across-regions-platforms).
