Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$READ\_ICEBERG\_TABLE\_PROPERTY

Returns Iceberg table properties from the metadata file of a Snowflake-managed or externally managed
[Apache Iceberg™ table](/user-guide/tables-iceberg).

## Syntax

Copy code

```
SYSTEM$READ_ICEBERG_TABLE_PROPERTY(
  '<table_name>'
  [ , '<property_name>' ]
)
```

## Arguments

`'table_name'`
:   Name of the Iceberg table. The table name is a string, so it must be enclosed in single quotes.

    - If the name is fully qualified, such as `'<db>.<schema>.<table_name>'`, enclose the entire name
      in single quotes, including the database and schema.
    - If the name is case-sensitive or includes special characters or spaces, enclose it in double
      quotes inside the single quotes, for example `'"<case_sensitive_table_name>"'`.

`'property_name'`
:   Optional Iceberg property key. Property names are case-sensitive.

    - When you specify a key, the function returns that property’s value, or NULL if the property isn’t
      present.
    - When you omit this argument, the function returns every property as a JSON object string. Pass
      the result to `PARSE_JSON` to get a VARIANT. Don’t pass NULL: omit the argument.

## Returns

A string.

- One property: the property value, or NULL when that key isn’t in the metadata file.
- All properties: a JSON object string, or `'{}'` when the table has no properties.

## Usage notes

- The function returns the table’s latest properties, including a property you just set.
- Calling this function requires privileges to access the table.

## Examples

Return every property for `my_iceberg_table`:

Copy code

```
SELECT PARSE_JSON(SYSTEM$READ_ICEBERG_TABLE_PROPERTY('my_db.my_schema.my_iceberg_table'));
```

Return one property:

Copy code

```
SELECT SYSTEM$READ_ICEBERG_TABLE_PROPERTY(
  'my_db.my_schema.my_iceberg_table',
  'write.delete.mode'
);
```
