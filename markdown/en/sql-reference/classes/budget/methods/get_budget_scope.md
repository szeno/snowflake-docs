# <budget\_name>!GET\_BUDGET\_SCOPE

Returns the resources and tags that have been added to a [custom budget](/user-guide/budgets). Helps determine which resource
consumption is tracked by the budget.

The list does not include:

- Objects that were added automatically (for example, compute pools and warehouses created and owned by a Snowflake Native App).
- Objects that were added when a tag was added to the budget.

## Syntax

Copy code

```
<budget_name>!GET_BUDGET_SCOPE()
```

## Returns

The method returns a JSON object with the following keys:

`resource_tags`
:   The resource tags that have been added to the budget. Resources belong to the budget if they are tagged with these tags. Contains
    the following fields:

    `operator`
    :   The matching logic used for resource tags. Can be one of the following values:

        - `UNION`: A resource is included in the budget if it is tagged with *any* of the tag-value pairs in the `tags` array.
        - `INTERSECTION`: A resource must be tagged with *all* of the tag-value pairs in the `tags` array to be included in the budget.

    `tags`
    :   An array of tag objects, each with the following fields:

        `tagId`
        :   Internal identifier for the tag.

        `tagDatabase`
        :   Database that contains the tag.

        `tagSchema`
        :   Schema that contains the tag.

        `tagName`
        :   Name of the tag.

        `tagValues`
        :   Array of tag values associated with the tag.

`resources`
:   An array of resources that have been added directly to the budget. Each object contains the following fields:

    `resourceId`
    :   Internal identifier for the resource.

    `resourceName`
    :   Name of the resource.

    `resourceDomain`
    :   Domain of the resource (for example, `WAREHOUSE`, `DATABASE`, `TABLE`).

    `schemaName`
    :   Schema that contains the resource.

    `databaseName`
    :   Database that contains the resource.

## Access control requirements

The following minimum privileges and roles are required to view results for custom budgets:

- ADMIN [instance role](/user-guide/budgets#label-budgets-instance-roles) for the budget instance.
- USAGE privilege on the database and schema that contains the budget instance.

For more information, see [Budgets roles and privileges](/user-guide/budgets#label-budgets-roles-and-privileges).

## Usage notes

- This method can only be called on *custom budget* instances.
- Calling this method does not return the object. Because of this, you can’t use method chaining to call another method on the
  return value of this method. Instead, call each method in a separate SQL statement.

## Example

Get all resources and tags that have been added to the `budget_db.budget_schema.my_budget` budget:

Copy code

```
CALL budget_db.budget_schema.my_budget!GET_BUDGET_SCOPE();
```
