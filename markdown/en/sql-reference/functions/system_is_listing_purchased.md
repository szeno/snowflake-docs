Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$IS\_LISTING\_PURCHASED

Returns TRUE if the consumer account querying data has purchased the listing, otherwise returns FALSE. If an account is trialing the listing,
the function returns FALSE. Use this system function in a secure view to manage access to the data in a share and display certain data only
to paying customers.

This function infers the listing associated with the database that contains the view and determines whether the account running the query
has purchased the listing.

## Syntax

Copy code

```
SYSTEM$IS_LISTING_PURCHASED()
```

## Arguments

None.

## Returns

The function returns a value of type BOOLEAN.

## Example

Create a secure view that selects all columns in a table. The view returns rows only when queried within a consumer account that has
purchased a paid listing:

Copy code

```
CREATE SECURE VIEW paid_view
  AS
  SELECT
    *
  FROM
    paid_table
  WHERE
    SYSTEM$IS_LISTING_PURCHASED();
```

Consumers trialing the paid listing see no rows in this view.

For additional examples, see [Prepare shares for a paid listing](/collaboration/provider-listings-preparing#label-prepare-shares-paid-listings).
