Categories:
:   [System functions](/sql-reference/functions-system)

# SYSTEM$TAG\_VALUE\_CONTAINS

Returns TRUE if the specified [tag](/user-guide/object-tagging/introduction) on the specified object or column contains the specified
string value. Returns FALSE if the value is not present or the tag is not assigned to the object.

Use this function when a tag might have more than one value. [SYSTEM$GET\_TAG](/sql-reference/functions/system_get_tag)
returns an error when multiple values exist. For more information, see [Multi-value tags](/user-guide/object-tagging/multi-value-tags).

See also:
:   [SYSTEM$GET\_TAG](/sql-reference/functions/system_get_tag) , [Multi-value tags](/user-guide/object-tagging/multi-value-tags)

## Syntax

Copy code

```
SYSTEM$TAG_VALUE_CONTAINS( '<tag_name>' , '<object_name>' , '<object_domain>' , '<value>' )
```

## Arguments

`'tag_name'`
:   The name of the tag as a string (the key in the key-value pair).

`'object_name'`
:   The name of the object as a string. For a column, use `<table_name>.<column_name>`.

`'object_domain'`
:   String that identifies the object domain, in the same sense as for [SYSTEM$GET\_TAG](/sql-reference/functions/system_get_tag).
    Multi-value tags apply to tables, views, and columns, so you can typically pass one of the following values:

    - `TABLE` when the tag is on a table or view.
    - `COLUMN` when the tag is on a column (use `<table_name>.<column_name>` for `object_name` in that case).

    For every domain string the API accepts, see the `object_domain` argument on [SYSTEM$GET\_TAG](/sql-reference/functions/system_get_tag).

`'value'`
:   The tag value to check for as a string.

## Returns

Returns a BOOLEAN: TRUE if the value is assigned to the tag on the object, FALSE otherwise.

## Usage notes

- Works with both single-value and multi-value tags.
- Unlike `SYSTEM$GET_TAG`, does not error when multiple values exist.
- Value comparison is case-sensitive.
- Requires privileges to run a [DESCRIBE <object>](/sql-reference/sql/desc) operation on the object and USAGE on the database and schema where the tag exists.

## Examples

Copy code

```
SELECT SYSTEM$TAG_VALUE_CONTAINS('classification_tag', 'customers', 'TABLE', 'PII');        -- True
SELECT SYSTEM$TAG_VALUE_CONTAINS('classification_tag', 'customers', 'TABLE', 'FINANCIAL');  -- True
SELECT SYSTEM$TAG_VALUE_CONTAINS('classification_tag', 'customers', 'TABLE', 'HIPAA');      -- False
```
