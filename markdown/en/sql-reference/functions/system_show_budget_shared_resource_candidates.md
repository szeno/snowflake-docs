Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$SHOW\_BUDGET\_SHARED\_RESOURCE\_CANDIDATES

Returns the list of resources that can be added as shared resources to a [budget](/user-guide/budgets).

For more information about configuring a budget to track consumption by shared resources, see [Using budgets for AI features (shared resources)](/user-guide/budgets/budget-shared-resources).

## Syntax

Copy code

```
SYSTEM$SHOW_BUDGET_SHARED_RESOURCE_CANDIDATES( '<domain>' )
```

## Arguments

`'domain'`
:   Specifies a type of resource. The function returns all resources of the specified type that can be added to a budget as shared resources.

    Currently, the only supported value is `'AI_FUNCTION'`, which lists all AI functions that can be added as shared resources to a budget.

## Returns

The function returns an array of objects. Each object contains the following keys:

| Key | Data type | Description |
| --- | --- | --- |
| `id` | NUMBER | Internal identifier for the resource. |
| `name` | VARCHAR | Name of the resource (for example, the AI function name). |
| `domain` | VARCHAR | Type of resource (for example, `AI_FUNCTION`). |

Expand

Show lessSee more

## Examples

List the AI functions that can be added as shared resources to a budget:

Copy code

```
CALL SYSTEM$SHOW_BUDGET_SHARED_RESOURCE_CANDIDATES('AI_FUNCTION');
```
