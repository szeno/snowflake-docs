# CLASS\_INSTANCE\_FUNCTIONS view

This Information Schema view displays a row for each function in a
[class](/sql-reference/snowflake-db-classes) instance.

See also:
:   [CLASS\_INSTANCES view](/sql-reference/info-schema/class_instances),
    [CLASS\_INSTANCE\_PROCEDURES view](/sql-reference/info-schema/class_instance_procedures),
    [SHOW FUNCTIONS](/sql-reference/sql/show-functions)

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| FUNCTION\_NAME | VARCHAR | Name of the function. |
| FUNCTION\_INSTANCE\_NAME | VARCHAR | Name of the class instance to which the function belongs. |
| FUNCTION\_INSTANCE\_SCHEMA | VARCHAR | Name of the schema to which the class instance belongs. |
| FUNCTION\_INSTANCE\_DATABASE | VARCHAR | Name of the database to which the class instance belongs. |
| FUNCTION\_OWNER | VARCHAR | Name of the role that owns the function. |
| ARGUMENT\_SIGNATURE | VARCHAR | Type signature of the function’s arguments. |
| DATA\_TYPE | VARCHAR | Data type of the return value. |
| CHARACTER\_MAXIMUM\_LENGTH | NUMBER | Maximum length in characters of string type return value. |
| CHARACTER\_OCTET\_LENGTH | NUMBER | Maximum length in bytes of string type return value. |
| NUMERIC\_PRECISION | NUMBER | Numeric precision of numeric type return value. |
| NUMERIC\_PRECISION\_RADIX | NUMBER | Radix of precision of numeric type return value. |
| NUMERIC\_SCALE | NUMBER | Scale of numeric type return value. |
| FUNCTION\_LANGUAGE | VARCHAR | Language of the function. |
| FUNCTION\_DEFINITION | VARCHAR | Function definition. |
| VOLATILITY | VARCHAR | Whether the function is volatile or immutable. |
| IS\_NULL\_CALL | VARCHAR | ‘YES’ if the function is called on null input. |
| IS\_SECURE | VARCHAR | ‘YES’ if the function is [secure](/developer-guide/secure-udf-procedure). |
| CREATED | TIMESTAMP\_LTZ | Date and time when the function was created. |
| LAST\_ALTERED | TIMESTAMP\_LTZ | Date and time the object was last altered by a DML, DDL, or background metadata operation. See [Usage Notes](#usage-notes). |
| COMMENT | VARCHAR | Comment for this function. |
| IS\_EXTERNAL [[1]](#footnote-1) | VARCHAR | ‘YES’ if the function is an [external function](/sql-reference/external-functions). |
| API\_INTEGRATION [[1]](#footnote-1) | VARCHAR | Name of the API integration object to authenticate the call to the proxy service. |
| CONTEXT\_HEADERS [[1]](#footnote-1) | VARCHAR | Context header information for the external function. |
| MAX\_BATCH\_ROWS [[1]](#footnote-1) | NUMBER | Maximum number of rows in each batch sent to the proxy service. |
| COMPRESSION [[1]](#footnote-1) | VARCHAR | Type of compression. |
| PACKAGES | VARCHAR | Packages requested by the function. |
| RUNTIME\_VERSION | VARCHAR | Runtime version of the language used by the function. NULL if the function is SQL or JavaScript. |
| INSTALLED\_PACKAGES | VARCHAR | All packages installed by the function. Output for Python functions only. |
| IS\_MEMOIZABLE | VARCHAR | ‘YES’ if the function is memoizable, ‘NO’ otherwise. |

Expand

Show lessSee more

[1]
These fields apply only to [Writing external functions](/sql-reference/external-functions).

## Usage notes

- The view only displays objects for which the current role for the session has been granted
  an instance role with access privileges.
- The LAST\_ALTERED column is updated when the following operations are performed on an object:

  - DDL operations.
  - DML operations (for tables only). This column is updated even when no rows are affected by the DML statement.
  - Background maintenance operations on metadata performed by Snowflake.

## Examples

Retrieve the functions for class instances in the `mydatabase` database:

Copy code

```
SELECT function_name,
       function_instance_name AS instance_name,
       argument_signature,
       data_type AS return_value_data_type
    FROM mydatabase.INFORMATION_SCHEMA.CLASS_INSTANCE_FUNCTIONS;
```
