Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$GET\_ALL\_REFERENCES

Iterates through all associations for a reference and returns information about the associations.

## Syntax

Copy code

```
SYSTEM$GET_ALL_REFERENCES('<reference_name>' [, <include_details> ])
```

## Arguments

**Required**

`'reference_name'`
:   The name of the reference.

**Optional**

`include_details`
:   Specifies whether to include the names of the associated objects. Accepts a `BOOLEAN` value.
    For more information, see [Returns](#label-get-all-references-returns).

    Default: `FALSE`.

## Returns

Returns a `VARCHAR` value that contains a JSON array:

- If `include_details` is `FALSE` or omitted, each element is a system-generated association alias.
- If `include_details` is `TRUE`, each element is an object with these fields:
  - `alias`: The system-generated alias of the association.
  - `database`: The parent database name of the consumer object, or `null` if the object
    doesn’t reside in a database.
  - `schema`: The parent schema name of the consumer object, or `null` if the object
    doesn’t reside in a schema.
  - `name`: The name of the consumer object. For a function or procedure, this includes
    its argument signature.

A bound single-valued reference returns one element. A multi-valued reference returns one
element for each association. If the reference has no associations, the array is empty (`[]`).

## Examples

This example assumes that the app has a multi-valued `consumer_tables` reference associated
with `consumer_db.public.orders` and `consumer_db.public.orders_archive`. See
[Examples](/sql-reference/functions/system_add_reference#examples) for an example of adding associations.

The following statements run in provider-written code executing in the installed app’s
context, such as the body of an app-owned stored procedure with owner’s rights. They aren’t
standalone statements for a consumer worksheet. The app can use the aliases to iterate
through associations and access each object with `REFERENCE('consumer_tables', '<alias>')`.

List the association aliases:

Copy code

```
SELECT SYSTEM$GET_ALL_REFERENCES('consumer_tables');
```

The returned string contains a JSON array like the following. The UUIDs are illustrative;
use the actual returned aliases in subsequent calls:

Copy code

```
[
  "6f3b7c2a-9d41-4e8f-a625-1b0c7d9e2345",
  "8a2c5e7d-3b60-4f91-b842-9d6e0a1c7358"
]
```

To include the object names, set `include_details` to `TRUE`:

Copy code

```
SELECT SYSTEM$GET_ALL_REFERENCES('consumer_tables', TRUE);
```

The returned string contains an array of objects like the following:

Copy code

```
[
  {
    "alias": "6f3b7c2a-9d41-4e8f-a625-1b0c7d9e2345",
    "database": "CONSUMER_DB",
    "schema": "PUBLIC",
    "name": "ORDERS"
  },
  {
    "alias": "8a2c5e7d-3b60-4f91-b842-9d6e0a1c7358",
    "database": "CONSUMER_DB",
    "schema": "PUBLIC",
    "name": "ORDERS_ARCHIVE"
  }
]
```

For a bound single-valued reference, the same calls return an array with one alias or one
object. After all associations are removed, either call returns `[]`.
