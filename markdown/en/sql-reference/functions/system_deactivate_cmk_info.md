Categories:
:   [System functions](/sql-reference/functions-system)

# SYSTEM$DEACTIVATE\_CMK\_INFO

De-activates Tri-Secret Secure in your account.

This system function:

- Configures your account to stop using Tri-Secret Secure.
- Creates a new account master key.
- Retires the composed account master key.
- Registers your account with the rekeying background service.

See also:
:   [Understanding CMK self-registration with support activation of Tri-Secret Secure](/user-guide/security-encryption-tss#label-encryption-tss-self-register)

## Syntax

Copy code

```
SYSTEM$DEACTIVATE_CMK_INFO()
```

## Arguments

None.

## Returns

Success or error messages.

## Access control requirements

Only users granted the MODIFY privilege on the account can call this function. The MODIFY privilege on an account is typically granted only
to the ACCOUNTADMIN role.

## Usage notes

The background service generates email messages that notify the account administrator when Tri-Secret Secure is deactivated.

## Examples

Deactivate Tri-Secret Secure for your Snowflake account:

Copy code

```
SELECT SYSTEM$DEACTIVATE_CMK_INFO();
```
