Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$DISABLE\_FEATURE\_GROUPS

Disables all features in a feature group for the current account.

See also:

> [SYSTEM$ENABLE\_FEATURE\_GROUPS](/sql-reference/functions/system_enable_feature_groups), [SYSTEM$DISABLE\_FEATURE\_GROUPS\_PREVIEW](/sql-reference/functions/system_disable_feature_groups_preview), [SYSTEM$DISABLE\_PREVIEW\_ACCESS](/sql-reference/functions/system_disable_preview_access)

Note

This function is available on request. To enable it for your account, [contact Snowflake Support](/user-guide/contacting-support).
Before enabling, Snowflake Support snapshots your current account-level parameter overrides
for features in the affected group, so that individual settings can be restored if you need
to revert specific per-feature settings later.

## Syntax

Copy code

```
SYSTEM$DISABLE_FEATURE_GROUPS( '<group_name>' )
```

## Arguments

`group_name`
:   Name of a feature group to disable. Case-insensitive.

    The only currently supported value is:

    | Group | Scope |
    | --- | --- |
    | `AI_FEATURES` | Cortex Search, Cortex Agent, Cortex Analyst, Cortex REST API, the AI/ML user interface in Snowsight, fine-tuning, Document AI, Snowflake Marketplace AI products, and AI SQL built-in functions such as `AI_COMPLETE`, `AI_CLASSIFY`, `AI_FILTER`, and `AI_EMBED`. |

    Expand

    Show lessSee more

    The exact set of features covered by the group can evolve over time as new AI capabilities are added.

## Returns

Returns a VARCHAR status message that the feature group has been disabled:

```
+----------------------------------------------+
| SYSTEM$DISABLE_FEATURE_GROUPS('AI_FEATURES') |
+----------------------------------------------+
| Successfully disabled groups: AI_FEATURES.   |
+----------------------------------------------+
```

## Access control requirements

- Only account administrators (users with the ACCOUNTADMIN role) can execute this function.

## Usage notes

- Group names are case-insensitive (for example, `ai_features` and `AI_FEATURES` are equivalent).
- The function operates on the current account. You can’t use it to target a different account.
- The function is idempotent. Calling it on an already-disabled group still returns a success message.
- In addition to disabling the group as a whole, the function unsets any account-level parameter
  overrides that you have set on individual features in the group, as part of the same operation.
  Snowflake Support snapshots those overrides before enabling self-service access (see the preceding note),
  which is the rollback path if you later need to restore individual per-feature settings.
- After a group is disabled, setting a parameter override for an individual feature in that group
  re-enables only that single feature, without changing the group-level status.

## Examples

Disable all AI features for the current account:

Copy code

```
USE ROLE ACCOUNTADMIN;
SELECT SYSTEM$DISABLE_FEATURE_GROUPS('AI_FEATURES');
```

Verify the current state of the group. The output shows the value of the group-level parameter
(for example, `DISABLE_ALL` after the call above), not a list of the individual features in the group:

Copy code

```
SHOW PARAMETERS LIKE 'AI_FEATURES' IN ACCOUNT;
```

Re-enable the group:

Copy code

```
SELECT SYSTEM$ENABLE_FEATURE_GROUPS('AI_FEATURES');
```
