Categories:
:   [File functions](/sql-reference/functions-file) (AI Functions)

# FL\_IS\_VIDEO

Checks if the input is a video [FILE](/sql-reference/data-types-unstructured#label-data-types-file).

# Syntax

Use one of the following:

```
FL_IS_VIDEO( <file_expression> )

FL_IS_VIDEO( <variant_expression> )
```

## Arguments

`file_expression`
:   The argument must be an expression of type FILE.

`variant_expression`
:   The argument must be an OBJECT representing a FILE.

## Returns

A BOOLEAN indicating whether the file is a video.

## Examples

Example using an input FILE:

Copy code

```
CREATE TABLE file_table(f FILE);
INSERT INTO file_table SELECT TO_FILE(BUILD_STAGE_FILE_URL('@mystage', 'image.png'));

SELECT FL_IS_VIDEO(f) FROM file_table;
```

```
+-------------------+
| FL_IS_VIDEO(F)    |
|-------------------|
| False             |
+-------------------+
```

Example using an input OBJECT:

Copy code

```
CREATE TABLE file_table(f OBJECT);
INSERT INTO file_table SELECT OBJECT_CONSTRUCT('STAGE', 'MYSTAGE', 'RELATIVE_PATH', 'movie.mp4', 'ETAG', '<ETAG value>',
  'LAST_MODIFIED', 'Wed, 11 Dec 2024 20:24:00 GMT', 'SIZE', 105859, 'FILE_TYPE', 'video/mp4');

SELECT FL_IS_VIDEO(f) FROM file_table;
```

```
+-------------------+
| FL_IS_VIDEO(F)    |
|-------------------|
| True              |
+-------------------+
```
