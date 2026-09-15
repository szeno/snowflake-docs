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
:   Specifies the account on which you want to determine if Cross-Cloud Auto-Fulfillment is enabled or disabled. To learn more about Snowflake account identifiers and how to locate them, see [Account identifiers](/user-guide/admin-account-identifier).

## Returns

Returns one of the following Boolean values:

- `TRUE` (if Cross-Cloud Auto-Fulfillment is enabled for the current account)
- `FALSE` (if Cross-Cloud Auto-Fulfillment is disabled for the current account)

## Access control requirements

- Only [organization administrators](/user-guide/organization-administrators) can execute this function.

## Examples

The following example determines if Cross-Cloud Auto-Fulfillment is enabled on the account named `my_account`:

Copy code

```
SELECT SYSTEM$IS_GLOBAL_DATA_SHARING_ENABLED_FOR_ACCOUNT('my_account');
```

```
+------------------------------------------------------------------------+
| SYSTEM$SYSTEM$IS_GLOBAL_DATA_SHARING_ENABLED_FOR_ACCOUNT('my_account') |
|------------------------------------------------------------------------|
| TRUE                                                                   |
+------------------------------------------------------------------------+
```
