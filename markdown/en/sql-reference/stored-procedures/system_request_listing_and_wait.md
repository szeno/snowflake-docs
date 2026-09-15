Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$REQUEST\_LISTING\_AND\_WAIT

Requests a listing and automatically polls for listing availability. To learn more about listings, see [About sharing with listings](https://other-docs.snowflake.com/en/collaboration/collaboration-listings-about).

## Syntax

Copy code

```
SYSTEM$REQUEST_LISTING_AND_WAIT( '<listing_global_name>' [ , <timeout_mins> ] )
```

## Arguments

`listing_global_name`
:   The global name of the listing being requested.

`timeout_mins`
:   The time to wait for listing request fulfillment in minutes before timing out. The default is 240 minutes or 4 hours.

## Returns

- Returns `Success: Listing <listing_global_name> is ready to be imported` when a requested listing becomes available or is already available.
- Returns `Error: Timed out waiting for the listing to be available after <timeout_mins> min(s)` when the specified timeout period is exceeded.

## Usage notes

To request a listing without waiting for listing fulfillment, enter `0` (zero) for the `timeout_mins` value. When the value is `0` and the request is successful, the message `Success: Listing <listing_global_name> requested successfully, but not waiting to confirm fulfillment` is returned.

## Examples

Copy code

```
CALL SYSTEM$REQUEST_LISTING_AND_WAIT('GZ13Z1VEWIJ', 60);
```
