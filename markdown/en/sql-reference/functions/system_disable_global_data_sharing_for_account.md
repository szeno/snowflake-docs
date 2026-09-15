Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$DISABLE\_GLOBAL\_DATA\_SHARING\_FOR\_ACCOUNT

Disables Cross-Cloud Auto-Fulfillment on an account.

See also:
:   [SYSTEM$IS\_GLOBAL\_DATA\_SHARING\_ENABLED\_FOR\_ACCOUNT](/sql-reference/functions/system_is_global_data_sharing_enabled_for_account) , [SYSTEM$ENABLE\_GLOBAL\_DATA\_SHARING\_FOR\_ACCOUNT](/sql-reference/functions/system_enable_global_data_sharing_for_account), [Auto-fulfillment for listings](/collaboration/provider-listings-auto-fulfillment)

## Syntax

Copy code

```
SYSTEM$DISABLE_GLOBAL_DATA_SHARING_FOR_ACCOUNT( '<account_name>' )
```

## Arguments

`account_name`
:   Specifies the account on which to disable Cross-Cloud Auto-Fulfillment. To learn more about Snowflake account identifiers and how to locate them, see [Account identifiers](/user-guide/admin-account-identifier).

## Returns

Returns the VARCHAR value `Statement executed successfully` if the function successfully disables Cross-Cloud Auto-Fulfillment on the account.

## Access control requirements

- Only [organization administrators](/user-guide/organization-administrators) can execute this function.

## Examples

The following example disables Cross-Cloud Auto-Fulfillment on the account named `my_account`:

Copy code

```
SELECT SYSTEM$DISABLE_GLOBAL_DATA_SHARING_FOR_ACCOUNT('my_account');
```

```
+--------------------------------------------------------------------+
| SYSTEM$ENABLE_GLOBAL_DATA_SHARING_FOR_ACCOUNT('my_account') |
|--------------------------------------------------------------------|
| Statement executed successfully                                    |
+--------------------------------------------------------------------+
```
