Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$DISABLE\_PRIVATELINK\_ACCESS\_ONLY

Feature — Open

Available to all accounts that are Business Critical Edition (or later).

To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

In preview, this feature is supported on AWS and Azure cloud platforms.

This feature is not available in the People’s Republic of China.

Unblocks connections for inbound network traffic that are routed over the public internet.

## Syntax

Copy code

```
SYSTEM$DISABLE_PRIVATELINK_ACCESS_ONLY()
```

## Arguments

None.

## Returns

Returns a VARCHAR message that inbound connections can use the public internet.

## Access control requirements

Only account administrators — users with the ACCOUNTADMIN role — can run this function.

## Example

Restore public access for inbound network traffic to your Snowflake account:

Copy code

```
USE ROLE ACCOUNTADMIN;
SELECT SYSTEM$DISABLE_PRIVATELINK_ACCESS_ONLY();
```
