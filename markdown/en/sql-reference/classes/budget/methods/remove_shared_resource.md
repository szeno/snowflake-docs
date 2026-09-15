# <budget\_name>!REMOVE\_SHARED\_RESOURCE

Removes a shared resource from a [custom budget](/user-guide/budgets). Shared resources are added to the budget using the
[ADD\_SHARED\_RESOURCE](/sql-reference/classes/budget/methods/add_shared_resource) method.

## Syntax

Copy code

```
<budget_name>!REMOVE_SHARED_RESOURCE( '<domain>' [ , '<instance>' ] )
```

## Arguments

`'domain'`
:   The type of resource being removed from the budget. Valid values:

    - `AI FUNCTION`
    - `CORTEX CODE`
    - `CORTEX AGENT`
    - `SNOWFLAKE INTELLIGENCE`

    Unless you specify a second argument, the budget stops tracking consumption for all resources within the specified domain.

`'instance'`
:   Optional. Specifies a specific resource within the selected `domain` to remove from the budget.

    For domains that support instance-level selection (such as `AI FUNCTION` and `CORTEX CODE`), this argument identifies a specific function or interface to remove.

    For object-backed domains (`CORTEX AGENT` and `SNOWFLAKE INTELLIGENCE`), pass an [object reference](/sql-reference/references) for the instance value: use the serialized string returned by [SYSTEM$REFERENCE](/sql-reference/functions/system_reference), or a subquery such as `(SELECT SYSTEM$REFERENCE(...))`.

    Examples:

    - AI Functions: `AI_CLASSIFY`, `AI_COMPLETE`
    - Cortex Code: `CORTEX_CODE_CLI`, `CORTEX_CODE_SNOWSIGHT`

## Returns

Returns a VARCHAR value that indicates whether or not the resource was successfully removed from the budget.

If the resource could not be removed from the budget, the function returns an error message.

## Access control requirements

The following minimum privileges and roles are required to call this method on a *custom budget*:

- ADMIN [instance role](/user-guide/budgets#label-budgets-instance-roles) for the budget instance.
- USAGE privilege on the database and schema that contains the budget instance.
- USAGE privilege on the database and schema that contain the resource (for schema objects).

For more information, see [Budgets roles and privileges](/user-guide/budgets#label-budgets-roles-and-privileges).

## Usage notes

- This method can only be called on *custom budget* instances.
- Calling this method does not return the object. Because of this, you can’t use method chaining to call another method on the
  return value of this method. Instead, call each method in a separate SQL statement.

## Examples

Remove all AI Functions from the budget:

Copy code

```
CALL finance_budget!REMOVE_SHARED_RESOURCE('AI FUNCTION');
```

Remove a specific AI function from the budget:

Copy code

```
CALL finance_budget!REMOVE_SHARED_RESOURCE('AI FUNCTION', 'AI_CLASSIFY');
```

Remove all Cortex Code workloads from the budget:

Copy code

```
CALL finance_budget!REMOVE_SHARED_RESOURCE('CORTEX CODE');
```

Remove the Cortex Code CLI workload from the budget:

Copy code

```
CALL finance_budget!REMOVE_SHARED_RESOURCE('CORTEX CODE', 'CORTEX_CODE_CLI');
```

Remove the Cortex Code Snowsight workload from the budget:

Copy code

```
CALL finance_budget!REMOVE_SHARED_RESOURCE('CORTEX CODE', 'CORTEX_CODE_SNOWSIGHT');
```

Remove all Cortex Agent workloads from the budget:

Copy code

```
CALL finance_budget!REMOVE_SHARED_RESOURCE('CORTEX AGENT');
```

Remove a specific Cortex Agent workload from the budget:

Copy code

```
CALL finance_budget!REMOVE_SHARED_RESOURCE(
  'CORTEX AGENT',
  (SELECT SYSTEM$REFERENCE('CORTEX AGENT', 'myagent'))
);
```

Remove all Snowflake CoWork workloads from the budget:

Copy code

```
CALL finance_budget!REMOVE_SHARED_RESOURCE('SNOWFLAKE INTELLIGENCE');
```

Remove a specific Snowflake CoWork workload from the budget:

Copy code

```
CALL finance_budget!REMOVE_SHARED_RESOURCE(
  'SNOWFLAKE INTELLIGENCE',
  (SELECT SYSTEM$REFERENCE('SNOWFLAKE INTELLIGENCE', 'my_si'))
);
```
