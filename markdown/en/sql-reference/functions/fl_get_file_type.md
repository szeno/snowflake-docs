Categories:
:   [File functions](/sql-reference/functions-file) (AI Functions)

# FL\_GET\_FILE\_TYPE

Returns the file type (modality) of a [FILE](/sql-reference/data-types-unstructured#label-data-types-file). This is a more general classification than
the content type (see [FL\_GET\_CONTENT\_TYPE](/sql-reference/functions/fl_get_content_type)).

# Syntax

Use one of the following:

```
FL_GET_FILE_TYPE( <file_expression> )

FL_GET_FILE_TYPE( <variant_expression> )
```

## Arguments

`file_expression`
:   The argument must be an expression of type FILE.

`variant_expression`
:   The argument must be an OBJECT representing a FILE.

## Returns

One of following values as a VARCHAR:

- `document`
- `video`
- `audio`
- `image`
- `compressed`
- `unknown`

Tip

To test if a file is of a particular type, use one of the `FL_IS` functions:

- [FL\_IS\_AUDIO](/sql-reference/functions/fl_is_audio)
- [FL\_IS\_COMPRESSED](/sql-reference/functions/fl_is_compressed)
- [FL\_IS\_DOCUMENT](/sql-reference/functions/fl_is_document)
- [FL\_IS\_IMAGE](/sql-reference/functions/fl_is_image)
- [FL\_IS\_VIDEO](/sql-reference/functions/fl_is_video)

## Examples

Example using an input FILE:

Copy code

```
CREATE TABLE FILE_TABLE(f FILE);
INSERT INTO file_table SELECT TO_FILE(BUILD_STAGE_FILE_URL('@mystage', 'image.png'));

SELECT FL_GET_FILE_TYPE(f) FROM file_table;
```

```
+------------------------+
| FL_GET_FILE_TYPE(F)    |
|------------------------|
| image                  |
+------------------------+
```

Example using an input OBJECT:

Copy code

```
CREATE TABLE file_table(f OBJECT);
INSERT INTO file_table SELECT OBJECT_CONSTRUCT('STAGE', 'MYSTAGE', 'RELATIVE_PATH', 'document.pdf', 'ETAG', '<ETAG value>',
  'LAST_MODIFIED', 'Wed, 11 Dec 2024 20:24:00 GMT', 'SIZE', 105859, 'FILE_TYPE', 'application/pdf');

SELECT FL_GET_FILE_TYPE(f) FROM file_table;
```

```
+------------------------+
| FL_GET_FILE_TYPE(F)    |
|------------------------|
| document               |
+------------------------+
```
