Categories:
:   [File functions](/sql-reference/functions-file) (AI Functions)

# FL\_GET\_LAST\_MODIFIED

Returns the last modified date of a [FILE](/sql-reference/data-types-unstructured#label-data-types-file).

# Syntax

Use one of the following:

```
FL_GET_LAST_MODIFIED( <file_expression> )

FL_GET_LAST_MODIFIED( <variant_expression> )
```

## Arguments

`file_expression`
:   The argument must be an expression of type FILE.

`variant_expression`
:   The argument must be an OBJECT representing a FILE.

## Returns

A TIMESTAMP value with the date the file was last modified.

## Examples

Example using an input FILE:

Copy code

```
CREATE TABLE file_table(f FILE);
INSERT INTO file_table SELECT TO_FILE(BUILD_STAGE_FILE_URL('@mystage', 'image.png'));

SELECT FL_GET_LAST_MODIFIED(f) FROM file_table;
```

```
+-------------------------------+
| FL_GET_LAST_MODIFIED(F)       |
|-------------------------------|
| Wed, 11 Dec 2024 20:24:00 GMT |
+-------------------------------+
```

Example using an input OBJECT:

Copy code

```
CREATE TABLE file_table(f OBJECT);
INSERT INTO file_table SELECT OBJECT_CONSTRUCT('STAGE', 'MYSTAGE', 'RELATIVE_PATH', 'image.jpg', 'ETAG', '<ETAG value>',
    'LAST_MODIFIED', 'Wed, 11 Dec 2024 20:24:00 GMT', 'SIZE', 105859, 'CONTENT_TYPE', 'image/jpg');

SELECT FL_GET_LAST_MODIFIED(f) FROM file_table;
```

```
+-------------------------------+
| FL_GET_LAST_MODIFIED(F)       |
|-------------------------------|
| Wed, 11 Dec 2024 20:24:00 GMT |
+-------------------------------+
```
