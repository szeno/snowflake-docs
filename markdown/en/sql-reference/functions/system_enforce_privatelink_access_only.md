Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$ENFORCE\_PRIVATELINK\_ACCESS\_ONLY

[Business Critical Feature](/user-guide/intro-editions)

This feature requires Business Critical Edition (or higher).

To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Enforces the behavior that successful connections to your Snowflake account use only your private endpoints.
Blocks connections for inbound network traffic that are routed over the public internet.

## Syntax

Copy code

```
SYSTEM$ENFORCE_PRIVATELINK_ACCESS_ONLY()
```

## Arguments

None.

## Returns

Returns a VARCHAR message that successful inbound connections now use only private endpoints.

## Access control requirements

Only account administrators — users with the ACCOUNTADMIN role — can run this function.

## Example

To enforce the behavior that successful connections to your Snowflake account use only your private endpoints:

Copy code

```
USE ROLE ACCOUNTADMIN;
SELECT SYSTEM$ENFORCE_PRIVATELINK_ACCESS_ONLY();
```
