# UPDATE\_AUTO\_ENABLEMENT\_STATUS

Updates whether your account has Trust Center secure by default enabled or disabled.

Note

Secure by default is available only for accounts on
[Business Critical Edition](/user-guide/intro-editions) or
[Virtual Private Snowflake (VPS)](/user-guide/intro-editions) with a capacity contract.

For more information, see [Secure by default](/user-guide/trust-center/using-the-trust-center#label-trust-center-secure-by-default).

## Syntax

Copy code

```
SNOWFLAKE.TRUST_CENTER.UPDATE_AUTO_ENABLEMENT_STATUS(
  <is_enabled>
  [ , '<comment>' ] );
```

## Arguments

**Required:**

`is_enabled`
:   `BOOLEAN` value that specifies whether secure by default is enabled for the account. Set to `TRUE`
    to enable secure by default, or `FALSE` to disable it.

**Required when you disable secure by default:**

`'comment'`
:   `VARCHAR` value that describes why you’re changing the setting. Must not exceed 1000 characters.

## Returns

Returns a `VARCHAR` status message.

## Access control requirements

Your role must have the `SNOWFLAKE.TRUST_CENTER_ADMIN` application role granted to it.

## Examples

Disable secure by default:

Copy code

```
CALL SNOWFLAKE.TRUST_CENTER.UPDATE_AUTO_ENABLEMENT_STATUS(
  FALSE,
  'We manage scanner package enablement manually');
```

Enable secure by default:

Copy code

```
CALL SNOWFLAKE.TRUST_CENTER.UPDATE_AUTO_ENABLEMENT_STATUS(TRUE);
```
