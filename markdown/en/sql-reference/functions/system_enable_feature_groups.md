Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$ENABLE\_FEATURE\_GROUPS

Re-enables a feature group for the current account that was previously disabled with
[SYSTEM$DISABLE\_FEATURE\_GROUPS](/sql-reference/functions/system_disable_feature_groups) or [SYSTEM$DISABLE\_FEATURE\_GROUPS\_PREVIEW](/sql-reference/functions/system_disable_feature_groups_preview).

See also:

> [SYSTEM$DISABLE\_FEATURE\_GROUPS](/sql-reference/functions/system_disable_feature_groups), [SYSTEM$DISABLE\_FEATURE\_GROUPS\_PREVIEW](/sql-reference/functions/system_disable_feature_groups_preview), [SYSTEM$DISABLE\_PREVIEW\_ACCESS](/sql-reference/functions/system_disable_preview_access)

Note

This function is available on request. To enable it for your account, [contact Snowflake Support](/user-guide/contacting-support).
Before enabling, Snowflake Support snapshots your current account-level parameter overrides
for features in the affected group, so that individual settings can be restored if you need
to revert specific per-feature settings later.

## Syntax

Copy code

```
SYSTEM$ENABLE_FEATURE_GROUPS( '<group_name>' )
```

## Arguments

`group_name`
:   Name of a feature group to re-enable. Case-insensitive.

    The only currently supported value is:

    | Group | Scope |
    | --- | --- |
    | `AI_FEATURES` | Cortex Search, Cortex Agent, Cortex Analyst, Cortex REST API, the AI/ML user interface in Snowsight, fine-tuning, Document AI, Snowflake Marketplace AI products, and AI SQL built-in functions such as `AI_COMPLETE`, `AI_CLASSIFY`, `AI_FILTER`, and `AI_EMBED`. |

    Expand

    Show lessSee more

    The exact set of features covered by the group can evolve over time as new AI capabilities are added.

## Returns

Returns a VARCHAR status message that the feature group has been re-enabled:

```
+---------------------------------------------+
| SYSTEM$ENABLE_FEATURE_GROUPS('AI_FEATURES') |
+---------------------------------------------+
| Successfully enabled groups: AI_FEATURES.   |
+---------------------------------------------+
```

## Access control requirements

- Only account administrators (users with the ACCOUNTADMIN role) can execute this function.

## Usage notes

- Group names are case-insensitive (for example, `ai_features` and `AI_FEATURES` are equivalent).
- The function operates on the current account. You can’t use it to target a different account.
- The function is idempotent. Calling it on an already-enabled group still returns a success message.
- **This function restores only the group-level setting to its default. It does not restore
  the individual account-level parameter overrides that** [SYSTEM$DISABLE\_FEATURE\_GROUPS](/sql-reference/functions/system_disable_feature_groups)
  **(or** [SYSTEM$DISABLE\_FEATURE\_GROUPS\_PREVIEW](/sql-reference/functions/system_disable_feature_groups_preview) **) unset when the group was disabled.**
  To roll back specific per-feature settings, [contact Snowflake Support](/user-guide/contacting-support)
  to restore them from the pre-change snapshot.

## Examples

Re-enable AI features for the current account:

Copy code

```
USE ROLE ACCOUNTADMIN;
SELECT SYSTEM$ENABLE_FEATURE_GROUPS('AI_FEATURES');
```
