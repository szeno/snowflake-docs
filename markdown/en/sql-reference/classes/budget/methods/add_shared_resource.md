# <budget\_name>!ADD\_SHARED\_RESOURCE

Adds a shared resource to a [custom budget](/user-guide/budgets). When you add a shared resource, consumption is tracked only if the
resource is used by certain users. These users are tagged with a tag-value pair that was added to the budget using the
[SET\_USER\_TAGS](/sql-reference/classes/budget/methods/set_user_tags) method.

For more information, see [Using budgets for AI features (shared resources)](/user-guide/budgets/budget-shared-resources).

## Syntax

Copy code

```
<budget_name>!ADD_SHARED_RESOURCE( '<domain>' [ , '<instance>' ] )
```

## Arguments

`'domain'`
:   The type of resource being added to the budget. Valid values:

    - `AI FUNCTION`
    - `CORTEX CODE`
    - `CORTEX AGENT`
    - `SNOWFLAKE INTELLIGENCE`

    Unless you specify a second argument, the budget tracks consumption for all resources within the specified domain.

`'instance'`
:   Optional. Specifies a specific resource within the selected `domain` to add to the budget.

    For domains that support instance-level selection (such as `AI FUNCTION` and `CORTEX CODE`), this argument allows you to track a specific function or interface.

    For object-backed domains (`CORTEX AGENT` and `SNOWFLAKE INTELLIGENCE`), pass an [object reference](/sql-reference/references) for the instance value: use the serialized string returned by [SYSTEM$REFERENCE](/sql-reference/functions/system_reference), or a subquery such as `(SELECT SYSTEM$REFERENCE(...))`.

    If you don’t specify a second argument, the budget tracks all instances within the domain.

    Examples:

    - AI Functions: `AI_CLASSIFY`, `AI_COMPLETE`
    - Cortex Code: `CORTEX_CODE_CLI`, `CORTEX_CODE_SNOWSIGHT`

## Returns

Returns a VARCHAR value that indicates whether or not the resource was successfully added to the budget.

If the resource could not be added to the budget, the function returns an error message.

## Access control requirements

The following privileges and roles are required to call this method for a custom budget:

- ADMIN [instance role](/user-guide/budgets#label-budgets-instance-roles) for the budget instance.
- USAGE privilege on the database and schema that contain the budget instance.
- USAGE privilege on the database and schema that contain the resource being added (for schema objects).

For more information, see [Budgets roles and privileges](/user-guide/budgets#label-budgets-roles-and-privileges).

## Usage notes

- You can only add shared resources to *custom budgets*.
- To verify the results of the method, call the [GET\_BUDGET\_SCOPE](/sql-reference/classes/budget/methods/get_budget_scope) method.
- When all objects of the specified entity type are added (for example, all AI Functions), you can’t add individual resources of that type.
- Calling this method does not return the object. Because of this, you can’t use method chaining to call another method on the
  return value of this method. Instead, call each method in a separate SQL statement.

## Examples

Add all AI Functions to the budget:

Copy code

```
CALL finance_budget!ADD_SHARED_RESOURCE('AI FUNCTION');
```

Add a specific AI function to the budget:

Copy code

```
CALL finance_budget!ADD_SHARED_RESOURCE('AI FUNCTION', 'AI_CLASSIFY');
```

Add all Cortex Code workloads to the budget:

Copy code

```
CALL finance_budget!ADD_SHARED_RESOURCE('CORTEX CODE');
```

Add the Cortex Code CLI workload to the budget:

Copy code

```
CALL finance_budget!ADD_SHARED_RESOURCE('CORTEX CODE', 'CORTEX_CODE_CLI');
```

Add the Cortex Code Snowsight workload to the budget:

Copy code

```
CALL finance_budget!ADD_SHARED_RESOURCE('CORTEX CODE', 'CORTEX_CODE_SNOWSIGHT');
```

Add all Cortex Agent workloads to the budget:

Copy code

```
CALL finance_budget!ADD_SHARED_RESOURCE('CORTEX AGENT');
```

Add a specific Cortex Agent workload to the budget:

Copy code

```
CALL finance_budget!ADD_SHARED_RESOURCE(
  'CORTEX AGENT',
  (SELECT SYSTEM$REFERENCE('CORTEX AGENT', 'myagent'))
);
```

Add all Snowflake CoWork workloads to the budget:

Copy code

```
CALL finance_budget!ADD_SHARED_RESOURCE('SNOWFLAKE INTELLIGENCE');
```

Add a specific Snowflake CoWork workload to the budget:

Copy code

```
CALL finance_budget!ADD_SHARED_RESOURCE(
  'SNOWFLAKE INTELLIGENCE',
  (SELECT SYSTEM$REFERENCE('SNOWFLAKE INTELLIGENCE', 'my_si'))
);
```
