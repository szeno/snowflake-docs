Categories:
:   [File functions](/sql-reference/functions-file) (AI Functions)

# TRY\_TO\_FILE

A version of [TO\_FILE](/sql-reference/functions/to_file) that returns NULL instead of raising an error.

# Syntax

Use one of the following:

```
TRY_TO_FILE( <stage_name>, <relative_path> )

TRY_TO_FILE( <file_url> )

TRY_TO_FILE( <metadata> )
```

## Arguments

Specify the file by providing:

- Both `stage_name` and `relative_path`
- `file_url`
- `metadata`

Only one of these methods can be used at a time.

`stage_name`
:   The name of the stage where the file is located, as a string, in the form `'@stage_name'`.

`relative_path`
:   The path to the file on the stage specified by `stage_name` as a string.

`file_url`
:   A valid stage or scoped file URL as a string.

`metadata`
:   An OBJECT containing the required FILE attributes. A FILE must have CONTENT\_TYPE, SIZE, ETAG, and LAST\_MODIFIED fields.
    It must also specify the file’s location in one of the following ways:

    - Both STAGE and RELATIVE\_PATH
    - STAGE\_FILE\_URL
    - SCOPED\_FILE\_URL

## Returns

A [FILE](/sql-reference/data-types-unstructured), or NULL.

## Usage notes

Returns NULL when:

- The supplied URL is not validL.
- The file is on a stage that the user lacks privileges to access.
- The supplied metadata doesn’t contain the required FILE fields.

## Examples

Unlike TO\_FILE, which raises an error on invalid arguments, TRY\_TO\_FILE returns NULL in this situation.
It otherwise works exactly like [TO\_FILE](/sql-reference/functions/to_file).

The example below illustrates the behavior of TRY\_TO\_FILE when given an invalid file path, assuming that
the file `image.png` exists on the stage but the other two files do not.

Copy code

```
SELECT
    TRY_TO_FILE('@mystage/image.png'),
    TRY_TO_FILE('@mystage/incorrect_file1.jpg'),
    TRY_TO_FILE('@mystage', 'incorrect_file2.png');
```

Result:

```
+-----------------------------------------------------+---------------------------------------------+------------------------------------------------+
| TRY_TO_FILE('@MYSTAGE/IMAGE.PNG')                   | TRY_TO_FILE('@MYSTAGE/INCORRECT_FILE1.JPG') | TRY_TO_FILE('@MYSTAGE', 'INCORRECT_FILE2.PNG') |
|-----------------------------------------------------|---------------------------------------------|------------------------------------------------|
| {                                                   | NULL                                        | NULL                                           |
|   "CONTENT_TYPE": "image/png",                      |                                             |                                                |
|   "ETAG": "2859efde6e26491810f619668280a2ce",       |                                             |                                                |
|   "LAST_MODIFIED": "Thu, 18 Sep 2025 09:02:00 GMT", |                                             |                                                |
|   "RELATIVE_PATH": "image.png",                     |                                             |                                                |
|   "SIZE": 23698,                                    |                                             |                                                |
|   "STAGE": "@MYDB.MYSCHEMA.MYSTAGE"                 |                                             |                                                |
| }                                                   |                                             |                                                |
+-----------------------------------------------------+---------------------------------------------+------------------------------------------------+
```

For more examples of creating FILE objects from valid inputs, see [TO\_FILE examples](/sql-reference/functions/to_file#label-to-file-examples).
