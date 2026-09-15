Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$GET\_ALL\_REFERENCES

Iterates through all associations for a reference and returns information about the associations.

## Syntax

Copy code

```
SYSTEM$GET_ALL_REFERENCES('<reference_name>', [, <include_details> = True | False ])
```

## Arguments

**Required**

`'reference_name'`
:   The name of the reference.

`{include_details = True | False }`
:   Determines the type of information returned by the function.
    For more information, see [Returns](#label-get-all-references-returns).

## Returns

- If the `include_details` parameter is set to `True`, returns a
  VARCHAR containing a JSON object that contains an array of the following name/value pairs:

  Copy code

  ```
  {
    "alias": "<value>",
    "database": "<value>",
    "schema": "<value>",
    "name": "<value>"
  }
  ```

  Where:

  - alias: The system-generated alias for the reference.
  - database: The parent database name of the consumer object, if the object resides in a
    database. Otherwise, null.
  - schema: The parent schema of the consumer object, if the object resides in a schema.
    Otherwise, null.
  - name: The name of the consumer object.
- If the `include_details` parameter is set to `False`, returns an array of
  system-generated aliases:

  - If the reference is not associated with an object, returns an empty list.
  - If the reference, is associated with an object, returns all associations for a multi-valued
    references.
  - If the reference is a single-valued reference, returns 0.
