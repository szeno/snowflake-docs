Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$DEREGISTER\_CMK\_INFO

Cancels registration of your currently-registered customer-managed key (CMK) for use with Tri-Secret Secure.

See also:
:   [Understanding CMK self-registration with support activation of Tri-Secret Secure](/user-guide/security-encryption-tss#label-encryption-tss-self-register)

## Syntax

Copy code

```
SYSTEM$DEREGISTER_CMK_INFO();
```

## Arguments

None.

## Returns

Returns a status message to system administrators stating that registration of your current CMK is cancelled.

## Access control requirements

Only account administrators (users with the ACCOUNTADMIN role) can call this function.

## Examples

De-register your CMK for your Snowflake account:

Copy code

```
SELECT SYSTEM$DEREGISTER_CMK_INFO();
```
