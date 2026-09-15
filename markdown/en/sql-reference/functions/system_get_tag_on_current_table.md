Categories:
:   [System functions](/sql-reference/functions-system)

# SYSTEM$GET\_TAG\_ON\_CURRENT\_TABLE

Returns the tag string value assigned to the table based upon the specified tag or NULL if a tag is not assigned to the specified table.

Use this function in the [masking policy](/user-guide/security-column-intro) conditions or the
[row access policy](/user-guide/security-row-intro) conditions.

## Syntax

Copy code

```
SYSTEM$GET_TAG_ON_CURRENT_TABLE( '<tag_name>' )
```

## Arguments

`'tag_name'`
:   Identifier for the tag as a string.

    For example, if the tag is named `cost_center` use `'cost_center'` as the argument.

## Usage notes

- Currently, this function can only be used in a masking policy or row access policy condition to dynamically evaluate the tag string value
  set on a table.

  Snowflake returns an error while using the function in a SELECT query, view, materialized view, or a user-defined function (UDF).
- Note that this function applies to all table-like objects (e.g. views).
- If the tag is a [multi-value tag](/user-guide/object-tagging/multi-value-tags) and more than one value is assigned, this function
  returns an error. Don’t reference multi-value tags in policy conditions.
- The tag must exist when calling this system function; otherwise, Snowflake returns the following error message:

  Copy code

  ```
  Tag '<tag_name>' does not exist or not authorized.
  ```

## Examples

For a contextual example on how to use this function, see [Example 3: Protect a table based on the table tag string value](/user-guide/tag-based-masking-policies#label-tag-masking-policy-table-string-value).
