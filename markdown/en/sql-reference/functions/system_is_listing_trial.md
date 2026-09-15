Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$IS\_LISTING\_TRIAL

Preview Feature — Open

Available to all accounts

Limits the functionality of a Snowflake Native App based on whether a consumer is trialing the application as part of a [Limited trial listings](/collaboration/collaboration-listings-about#label-trial-listing) or has access to the full data product.

Returns TRUE if the consumer account is trialing the data product as part of a limited trial listing, otherwise returns FALSE.

Use this system function in a secure view, secure UDF, or Streamlit app to manage access to the functionality
of your Snowflake Native App and display certain output only to consumers with access to the full data product.

Caution

Do not use this system function to limit access to functionality for consumers trialing a paid listing.
Instead, use [SYSTEM$IS\_LISTING\_PURCHASED](/sql-reference/functions/system_is_listing_purchased).

This function infers the listing associated with the application package that contains the secure view, secure UDF, or Streamlit app,
and determines whether the account running the query is trialing the listing as part of a limited trial listing.
For more details, see [Limit functionality of your Snowflake Native App for trial consumers](/collaboration/provider-listings-preparing#label-listings-trial-limit-functionality-app).

## Syntax

Copy code

```
SYSTEM$IS_LISTING_TRIAL()
```

## Arguments

None.

## Returns

The function returns a value of type BOOLEAN.

## Examples

In this example, create a secure view that returns a subset of rows to trial consumers, but returns all rows to consumers with full access
to your data product. You can control the output of the secure view using this system function and the value of a data column to determine
which data to show to which consumers.

In this example, create a secure view `limited_functionality_view` with your data from a table named `exclusive_access_table`.
In that table, define a BOOLEAN type column, `is_trial`, where some rows of data have `is_trial` set to `TRUE` to indicate that the
data in those rows should be shown to trial consumers. Other rows have `is_trial` set to `FALSE`,
indicating that the data in those rows should be shown only to consumers with full access to your Snowflake Native App.

This example view is set up to return all rows only when it is queried by a consumer account with full access to your Snowflake Native App,
otherwise it returns only the rows where `is_trial` is set to `TRUE`.

Copy code

```
CREATE SECURE VIEW limited_functionality_view
  AS
  SELECT
    *
  FROM
    exclusive_access_table
  WHERE
    is_trial
    OR
    SYSTEM$IS_LISTING_TRIAL() = TRUE;
```

See more examples and details in [Limit functionality of your Snowflake Native App for trial consumers](/collaboration/provider-listings-preparing#label-listings-trial-limit-functionality-app).
