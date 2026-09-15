# GET\_AUTO\_ENABLEMENT\_STATUS

Returns the current Trust Center secure by default setting for your account.

Note

Secure by default is available only for accounts on
[Business Critical Edition](/user-guide/intro-editions) or
[Virtual Private Snowflake (VPS)](/user-guide/intro-editions) with a capacity contract.

For more information, see [Secure by default](/user-guide/trust-center/using-the-trust-center#label-trust-center-secure-by-default).

## Syntax

Copy code

```
SNOWFLAKE.TRUST_CENTER.GET_AUTO_ENABLEMENT_STATUS();
```

## Returns

Returns a table with the following columns:

| Column name | Data type | Description |
| --- | --- | --- |
| `IS_OPTED_IN` | `BOOLEAN` | `TRUE` if secure by default is enabled for the account. `FALSE` if the account turned the setting off. |
| `MODIFIED_TIMESTAMP_LTZ` | `TIMESTAMP_LTZ` | Indicates when the setting was last changed. |

Expand

Show lessSee more

## Access control requirements

Your role must have either the `SNOWFLAKE.TRUST_CENTER_ADMIN` or `SNOWFLAKE.TRUST_CENTER_VIEWER`
application role granted to it.

## Examples

Return the secure by default setting for your account:

Copy code

```
CALL SNOWFLAKE.TRUST_CENTER.GET_AUTO_ENABLEMENT_STATUS();
```
