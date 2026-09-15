Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$ACTIVATE\_CMK\_INFO

Activates Tri-Secret Secure in your account, optionally with private connectivity, by using the customer-managed key (CMK) information
that you registered for your account.

This system function performs the following actions:

- Configures your account to use Tri-Secret Secure with the registered CMK.
- Creates a new composed account master key.
- Registers your account with the rekeying background service.
- Optionally, enables private connectivity on an active CMK, without rekeying.

See also:
:   [Understanding CMK self-registration with support activation of Tri-Secret Secure](/user-guide/security-encryption-tss#label-encryption-tss-self-register)

## Syntax

Copy code

```
SYSTEM$ACTIVATE_CMK_INFO( [ <option> ] )
```

## Arguments

**Required:**

None.

**Optional:**

`option`
:   You can specify one of the following values:

    `REKEY_SAME_CMK`
    :   Allows rekeying with the active CMK.

    `UPDATE_PRIVATELINK`
    :   Updates the privatelink status from the registered CMK.

## Returns

Success or error messages.

## Access control requirements

Only users that are granted the MODIFY privilege on the account can call this function.
The MODIFY privilege is typically granted only to the ACCOUNTADMIN role.

## Usage notes

The background service generates email messages that notify the account administrator about rekeying and Tri-Secret Secure activation status.

## Examples

Activate Tri-Secret Secure for your Snowflake account:

Copy code

```
SELECT SYSTEM$ACTIVATE_CMK_INFO();
```

Rekey with your current CMK:

Copy code

```
SELECT SYSTEM$ACTIVATE_CMK_INFO('REKEY_SAME_CMK');
```

Update private connectivity enablement on the CMK that is registered for use with Tri-Secret Secure and the active CMK, without rekeying.

Copy code

```
SELECT SYSTEM$ACTIVATE_CMK_INFO('UPDATE_PRIVATELINK');
```
