Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$DISABLE\_PREVIEW\_ACCESS

Disables access to [open preview](/release-notes/preview-features) and private preview features.

See also:

> [SYSTEM$GET\_PREVIEW\_ACCESS\_STATUS](/sql-reference/functions/system_get_preview_access_status), [SYSTEM$ENABLE\_PREVIEW\_ACCESS](/sql-reference/functions/system_enable_preview_access), [SYSTEM$DISABLE\_FEATURE\_GROUPS\_PREVIEW](/sql-reference/functions/system_disable_feature_groups_preview)

## Syntax

Copy code

```
SYSTEM$DISABLE_PREVIEW_ACCESS()
```

## Arguments

None.

## Returns

Returns a VARCHAR status message that preview features have been disabled:

```
+----------------------------------------------------------------+
| SYSTEM$DISABLE_PREVIEW_ACCESS()                                |
+----------------------------------------------------------------+
| Preview access has been successfully disabled for this account |
+----------------------------------------------------------------+
```

## Access control requirements

- Only account administrators (users with the ACCOUNTADMIN role) can execute this function.

## Usage notes

- Applies to both private and open preview features.
- This is an all-or-nothing setting that affects all users and all previews within an account.
- Any user in the account who is using a preview feature will lose access to that feature immediately after SYSTEM$DISABLE\_PREVIEW\_ACCESS is executed.
- Snowflake Marketplace products, which are managed separately through [IMPORTED PRIVILEGES](/user-guide/data-exchange-marketplace-privileges), are not covered as part of this capability.
- Client-side libraries (such as Snowpark API) are not covered as part of this capability.

## Examples

Disable preview features:

Copy code

```
USE ROLE ACCOUNTADMIN;
SELECT SYSTEM$DISABLE_PREVIEW_ACCESS();
```

Tip

`SYSTEM$DISABLE_PREVIEW_ACCESS` disables preview access for *all* features in your account.
If you instead want to disable preview only for AI features, use
[SYSTEM$DISABLE\_FEATURE\_GROUPS\_PREVIEW](/sql-reference/functions/system_disable_feature_groups_preview), which targets the
`AI_FEATURES` feature group without affecting other previews on your account.
