Categories:
:   [System functions](/sql-reference/functions-system)

# SYSTEM$TAG\_VALUE\_CONTAINS\_ON\_CURRENT\_COLUMN

Returns TRUE if the specified [tag](/user-guide/object-tagging/introduction) on the column that a policy protects contains the specified
string value. Returns FALSE if that value is not assigned, or if the tag is not assigned.

Use this function in column-level protection policies, such as [masking policies](/user-guide/security-column-intro) and
[projection policies](/user-guide/projection-policies), when a tag might have more than one value.
[SYSTEM$GET\_TAG\_ON\_CURRENT\_COLUMN](/sql-reference/functions/system_get_tag_on_current_column) returns an error when multiple values exist.
For more information, see [Multi-value tags](/user-guide/object-tagging/multi-value-tags).

## Syntax

Copy code

```
SYSTEM$TAG_VALUE_CONTAINS_ON_CURRENT_COLUMN( '<tag_name>' , '<value>' )
```

## Arguments

`'tag_name'`
:   Name of the tag, as a string literal. Snowflake resolves the name when you create or alter the policy, in the schema in use
    for that statement. Use a fully qualified name for a tag in another schema.

`'value'`
:   Tag value to test for, as a string literal.

## Returns

Returns a BOOLEAN: TRUE if the value is assigned to a tag attached directly to the current column. If the column has no
directly attached tag, TRUE if the value is assigned on an inherited tag. FALSE otherwise.

## Usage notes

- Call this function from a column-level protection policy condition, such as a masking policy or a projection policy.

  Snowflake returns an error if you call it in a SELECT query, a row access policy, a view, or a user-defined function (UDF).
- Both arguments must be string literals.
- The tag must exist when you create or alter the policy. Otherwise, Snowflake returns the following error message:

  ```
  Tag '<tag_name>' does not exist or not authorized.
  ```
- The comparison is case-sensitive. On a multi-value tag, the function returns TRUE when `<value>` is one of the assigned values.
  It also returns TRUE when `<value>` equals the single value of a tag that is not multi-value.
- The function checks tags attached directly to the column. If the column has no directly attached tag, the function checks
  inherited tags.
- This function applies to table-like objects, such as views.

## Examples

Mask a column when its `sensitivity` tag contains `pii`, and leave a column visible when that value is absent:

Copy code

```
CREATE TAG sensitivity MULTI_VALUE = TRUE;

CREATE TABLE customers (email STRING, city STRING);
INSERT INTO customers VALUES ('ada@example.com', 'Boston');

CREATE MASKING POLICY mask_sensitive
  AS (v STRING) RETURNS STRING ->
    CASE
      WHEN SYSTEM$TAG_VALUE_CONTAINS_ON_CURRENT_COLUMN('sensitivity', 'pii') THEN '***MASKED***'
      ELSE v
    END;

ALTER TABLE customers MODIFY COLUMN email SET MASKING POLICY mask_sensitive;
ALTER TABLE customers MODIFY COLUMN city SET MASKING POLICY mask_sensitive;

ALTER TABLE customers MODIFY COLUMN email ADD VALUE 'pii' FOR TAG sensitivity;
ALTER TABLE customers MODIFY COLUMN city ADD VALUE 'public' FOR TAG sensitivity;
```

Every role receives `***MASKED***` for `email` and `Boston` for `city`. Dropping the `pii` value returns `ada@example.com` on the
next query.
