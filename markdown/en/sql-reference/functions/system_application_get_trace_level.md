Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$APPLICATION\_GET\_TRACE\_LEVEL

Returns the trace level for the specified object. The following objects are supported:

- Functions
- Schemas
- Stored procedures
- Versioned schemas

## Syntax

Copy code

```
SYSTEM$APPLICATION_GET_TRACE_LEVEL( '<schema_name>.<object_name>' )
```

## Arguments

`'schema_name.object_name'`
:   The name of schema (or versioned schema) and object you want to determine the log
    level for.

## Usage notes

- This function can only be called by a Snowflake Native App and must be run as the APP\_PRIMARY
  role.

## Examples

Copy code

```
SELECT SYSTEM$APPLICATION_GET_TRACE_LEVEL('my_schema');
```
