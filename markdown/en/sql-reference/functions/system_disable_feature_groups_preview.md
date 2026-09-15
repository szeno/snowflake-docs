Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$DISABLE\_FEATURE\_GROUPS\_PREVIEW

Disables only the preview features in a feature group for the current account. Generally available
features in the group remain enabled.

See also:

> [SYSTEM$DISABLE\_FEATURE\_GROUPS](/sql-reference/functions/system_disable_feature_groups), [SYSTEM$ENABLE\_FEATURE\_GROUPS](/sql-reference/functions/system_enable_feature_groups), [SYSTEM$DISABLE\_PREVIEW\_ACCESS](/sql-reference/functions/system_disable_preview_access)

Note

This function is available on request. To enable it for your account, [contact Snowflake Support](/user-guide/contacting-support).
Before enabling, Snowflake Support snapshots your current account-level parameter overrides
for features in the affected group, so that individual settings can be restored if you need
to revert specific per-feature settings later.

## Syntax

Copy code

```
SYSTEM$DISABLE_FEATURE_GROUPS_PREVIEW( '<group_name>' )
```

## Arguments

`group_name`
:   Name of a feature group whose preview features you want to disable. Case-insensitive.

    The only currently supported value is:

    | Group | Scope |
    | --- | --- |
    | `AI_FEATURES` | Cortex Search, Cortex Agent, Cortex Analyst, Cortex REST API, the AI/ML user interface in Snowsight, fine-tuning, Document AI, Snowflake Marketplace AI products, and AI SQL built-in functions such as `AI_COMPLETE`, `AI_CLASSIFY`, `AI_FILTER`, and `AI_EMBED`. |

    Expand

    Show lessSee more

    The exact set of features covered by the group can evolve over time as new AI capabilities are added.

## Returns

Returns a VARCHAR status message that the preview features in the group have been disabled:

```
+----------------------------------------------------------------+
| SYSTEM$DISABLE_FEATURE_GROUPS_PREVIEW('AI_FEATURES')           |
+----------------------------------------------------------------+
| Successfully disabled preview features in groups: AI_FEATURES. |
+----------------------------------------------------------------+
```

## Access control requirements

- Only account administrators (users with the ACCOUNTADMIN role) can execute this function.

## Usage notes

- Group names are case-insensitive (for example, `ai_features` and `AI_FEATURES` are equivalent).
- The function operates on the current account. You can’t use it to target a different account.
- The function is idempotent. Calling it on a group whose preview is already disabled still returns
  a success message.
- Only features in the group that are currently set to a preview value (private preview or open
  preview) are affected. Generally available features in the group remain enabled.
- If you want to disable preview access for *all* features in your account (not just AI features),
  use [SYSTEM$DISABLE\_PREVIEW\_ACCESS](/sql-reference/functions/system_disable_preview_access) instead.
- After preview is disabled for a group, setting a parameter override for an individual feature
  in that group re-enables only that single feature, without changing the group-level status.

## Examples

Disable preview features in the `AI_FEATURES` group for the current account:

Copy code

```
USE ROLE ACCOUNTADMIN;
SELECT SYSTEM$DISABLE_FEATURE_GROUPS_PREVIEW('AI_FEATURES');
```

Re-enable the group:

Copy code

```
SELECT SYSTEM$ENABLE_FEATURE_GROUPS('AI_FEATURES');
```
