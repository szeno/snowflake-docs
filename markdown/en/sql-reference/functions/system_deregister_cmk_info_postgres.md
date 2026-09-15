Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$DEREGISTER\_CMK\_INFO\_POSTGRES

Cancels registration of your currently-registered customer-managed key (CMK) for use with Snowflake Postgres Tri-Secret Secure.

## Syntax

Copy code

```
SYSTEM$DEREGISTER_CMK_INFO_POSTGRES();
```

## Arguments

None.

## Returns

Returns a status message to system administrators stating that registration of your current CMK is cancelled.

## Arguments

None.

## Access control requirements

Only account administrators (users with the ACCOUNTADMIN role) can call this function.

## Examples

De-register your CMK for your Snowflake account:

Copy code

```
SELECT SYSTEM$DEREGISTER_CMK_INFO_POSTGRES();
```
