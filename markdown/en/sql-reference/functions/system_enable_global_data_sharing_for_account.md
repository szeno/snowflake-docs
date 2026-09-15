Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$ENABLE\_GLOBAL\_DATA\_SHARING\_FOR\_ACCOUNT

Enables Cross-Cloud Auto-Fulfillment on an account. Cross-Cloud Auto-Fulfillment allows you to automatically provide the share or application package attached to your listing to other Snowflake consumer regions.

See also:
:   [SYSTEM$IS\_GLOBAL\_DATA\_SHARING\_ENABLED\_FOR\_ACCOUNT](/sql-reference/functions/system_is_global_data_sharing_enabled_for_account) , [SYSTEM$DISABLE\_GLOBAL\_DATA\_SHARING\_FOR\_ACCOUNT](/sql-reference/functions/system_disable_global_data_sharing_for_account), [Auto-fulfillment for listings](/collaboration/provider-listings-auto-fulfillment)

## Syntax

Copy code

```
SYSTEM$ENABLE_GLOBAL_DATA_SHARING_FOR_ACCOUNT( '<account_name>' )
```

## Arguments

`account_name`
:   The name of the account on which to enable Cross-Cloud Auto-Fulfillment.
    This is the account name only (for example, `my_account`), which is the
    value returned by `CURRENT_ACCOUNT_NAME()`. Do not pass the full account
    identifier used in account URLs or SQL (such as `myorg-my_account` or
    `myorg.my_account`). To learn more about Snowflake account identifiers,
    see [Account identifiers](/user-guide/admin-account-identifier).

## Returns

Returns the VARCHAR value `Statement executed successfully` if the function successfully enables Cross-Cloud Auto-Fulfillment on the account.

## Access control requirements

- Only [organization administrators](/user-guide/organization-administrators) can execute this function.

## Examples

To retrieve the account name to pass to this function, call [CURRENT\_ACCOUNT\_NAME()](/sql-reference/functions/current_account_name):

Copy code

```
SELECT CURRENT_ACCOUNT_NAME();
```

The following example enables Cross-Cloud Auto-Fulfillment on the account named `my_account`:

Copy code

```
SELECT SYSTEM$ENABLE_GLOBAL_DATA_SHARING_FOR_ACCOUNT('my_account');
```

```
+--------------------------------------------------------------------+
| SYSTEM$SYSTEM$ENABLE_GLOBAL_DATA_SHARING_FOR_ACCOUNT('my_account') |
|--------------------------------------------------------------------|
| Statement executed successfully                                    |
+--------------------------------------------------------------------+
```
