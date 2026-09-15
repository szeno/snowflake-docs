Categories:
:   [System functions](/sql-reference/functions-system) (Information)

# SYSTEM$SHOW\_BUDGETS\_FOR\_RESOURCE

Returns a string containing a list of the [budgets](/user-guide/budgets) that track a specified resource (for example,
a table or a schema).

See also:
:   [<budget\_name>!GET\_LINKED\_RESOURCES](/sql-reference/classes/budget/methods/get_linked_resources)

## Syntax

Copy code

```
SYSTEM$SHOW_BUDGETS_FOR_RESOURCE( '<resource_domain>' , '<resource_name>' )
```

## Arguments

`'resource_domain'`
:   Domain of the resource. You can specify one of the following values:

- `compute_pool`
- `database`
- `materialized_view`
- `pipe`
- `schema`
- `table`
- `task`
- `warehouse`

`'resource_name'`
:   Name of the resource (for example, the name of the table).

## Returns

Returns a VARCHAR value containing the comma-delimited list of the fully qualified names of the budgets for the resource.
The list is surrounded by square brackets.

If there are no budgets tracking the specified resource, the function returns a string containing an empty pair of square brackets
(`[]`).

## Usage notes

The output of this function includes budgets that include the resource because of any of the following reasons:

- The resource was added directly to the budget.
- The resource has the tag/value combination that was added to the budget.
- The resource belongs to an object (for example, a database) that was added to the budget.

## Examples

The following example returns the list of budgets that track the schema named `my_db.my_schema`:

Copy code

```
SELECT SYSTEM$SHOW_BUDGETS_FOR_RESOURCE('SCHEMA', 'my_db.my_schema');
```

```
+---------------------------------------------------------------+
| SYSTEM$SHOW_BUDGETS_FOR_RESOURCE('SCHEMA', 'MY_DB.MY_SCHEMA') |
|---------------------------------------------------------------|
| [BUDGETS_DB.BUDGETS_SCHEMA.MY_BUDGET]                         |
+---------------------------------------------------------------+
```

The following example returns the list of budgets that track the table named `my_db.my_schema.my_table`. In this example, the
table is not tracked by any budget, so the function returns an empty list.

Copy code

```
SELECT SYSTEM$SHOW_BUDGETS_FOR_RESOURCE('TABLE', 'my_db.my_schema.my_table');
```

```
+-----------------------------------------------------------------------+
| SYSTEM$SHOW_BUDGETS_FOR_RESOURCE('TABLE', 'MY_DB.MY_SCHEMA.MY_TABLE') |
|-----------------------------------------------------------------------|
| []                                                                    |
+-----------------------------------------------------------------------+
```
