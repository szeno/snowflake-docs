Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$IS\_GLOBAL\_DATA\_SHARING\_ENABLED\_FOR\_ACCOUNT

Specifies whether Cross-Cloud Auto-Fulfillment is enabled or disabled on an account.

See also:
:   [SYSTEM$ENABLE\_GLOBAL\_DATA\_SHARING\_FOR\_ACCOUNT](/sql-reference/functions/system_enable_global_data_sharing_for_account), [SYSTEM$DISABLE\_GLOBAL\_DATA\_SHARING\_FOR\_ACCOUNT](/sql-reference/functions/system_disable_global_data_sharing_for_account), [Auto-fulfillment for listings](/collaboration/provider-listings-auto-fulfillment)

## Syntax

Copy code

```
SYSTEM$IS_GLOBAL_DATA_SHARING_ENABLED_FOR_ACCOUNT( '<account_name>' )
```

## Arguments

`account_name`
:   The name of the account on which to determine whether Cross-Cloud Auto-Fulfillment
    is enabled. This is the account name only (for example, `my_account`), which is the
    value returned by `CURRENT_ACCOUNT_NAME()`. Do not pass the full account
    identifier used in account URLs or SQL (such as `myorg-my_account` or
    `myorg.my_account`). To learn more about Snowflake account identifiers,
    see [Account identifiers](/user-guide/admin-account-identifier).

## Returns

Returns one of the following Boolean values:

- `TRUE` (if Cross-Cloud Auto-Fulfillment is enabled for the current account)
- `FALSE` (if Cross-Cloud Auto-Fulfillment is disabled for the current account)

## Access control requirements

- Only [organization administrators](/user-guide/organization-administrators) can execute this function.

## Examples

To retrieve the account name to pass to this function, call [CURRENT\_ACCOUNT\_NAME()](/sql-reference/functions/current_account_name):

Copy code

```
SELECT CURRENT_ACCOUNT_NAME();
```

The following example determines if Cross-Cloud Auto-Fulfillment is enabled on the account named `my_account`:

Copy code

```
SELECT SYSTEM$IS_GLOBAL_DATA_SHARING_ENABLED_FOR_ACCOUNT('my_account');
```

```
+-----------------------------------------------------------------+
| SYSTEM$IS_GLOBAL_DATA_SHARING_ENABLED_FOR_ACCOUNT('my_account') |
|-----------------------------------------------------------------|
| TRUE                                                            |
+-----------------------------------------------------------------+
```
