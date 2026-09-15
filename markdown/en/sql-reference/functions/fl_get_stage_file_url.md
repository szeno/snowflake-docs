Categories:
:   [File functions](/sql-reference/functions-file) (AI Functions)

# FL\_GET\_STAGE\_FILE\_URL

Returns the stage URL of a [FILE](/sql-reference/data-types-unstructured#label-data-types-file).

# Syntax

Use one of the following:

```
FL_GET_STAGE_FILE_URL( <file_expression> )

FL_GET_STAGE_FILE_URL( <variant_expression> )
```

## Arguments

`file_expression`
:   The argument must be an expression of type FILE.

`variant_expression`
:   The argument must be an OBJECT representing a FILE.

## Returns

The URL of the file as a VARCHAR.

## Examples

Example using an input FILE:

Copy code

```
CREATE TABLE file_table(f FILE);
INSERT INTO file_table SELECT TO_FILE(BUILD_STAGE_FILE_URL('@mystage', 'image.png'));

SELECT FL_GET_STAGE_FILE_URL(f) FROM file_table;
```

```
+-------------------------------------------------------------------------------------------+
| FL_GET_STAGE_FILE_URL(F)                                                                  |
|-------------------------------------------------------------------------------------------|
| https://snowflake.account.snowflakecomputing.com/api/files/TEST/PUBLIC/MYSTAGE/image.png  |
+-------------------------------------------------------------------------------------------+
```

Example using an input OBJECT:

Copy code

```
CREATE TABLE file_table(f OBJECT);
INSERT INTO file_table SELECT OBJECT_CONSTRUCT('STAGE_FILE_URL', 'https://snowflake.account.snowflakecomputing.com/api/files/TEST/PUBLIC/MYSTAGE/image.png',
  'ETAG', '<ETAG value>', 'LAST_MODIFIED', 'Wed, 11 Dec 2024 20:24:00 GMT', 'SIZE', 105859, 'CONTENT_TYPE', 'image/jpg');

SELECT FL_GET_STAGE_FILE_URL(f) FROM file_table;
```

```
+-------------------------------------------------------------------------------------------+
| FL_GET_STAGE_FILE_URL(F)                                                                  |
|-------------------------------------------------------------------------------------------|
| https://snowflake.account.snowflakecomputing.com/api/files/TEST/PUBLIC/MYSTAGE/image.png  |
+-------------------------------------------------------------------------------------------+
```
