Categories:
:   [System functions](/sql-reference/functions-system)

# SYSTEM$TAG\_VALUE\_CONTAINS\_ON\_CURRENT\_TABLE

Returns TRUE if the specified [tag](/user-guide/object-tagging/introduction) on the table that a policy protects contains the specified
string value. Returns FALSE if that value is not assigned, or if the tag is not assigned.

Use this function in [data protection policies](/user-guide/data-protection-policies-snowsight)
when a tag might have more than one value. [SYSTEM$GET\_TAG\_ON\_CURRENT\_TABLE](/sql-reference/functions/system_get_tag_on_current_table)
returns an error when multiple values exist. For more information, see [Multi-value tags](/user-guide/object-tagging/multi-value-tags).

## Syntax

Copy code

```
SYSTEM$TAG_VALUE_CONTAINS_ON_CURRENT_TABLE( '<tag_name>' , '<value>' )
```

## Arguments

`'tag_name'`
:   Name of the tag, as a string literal. Snowflake resolves the name when you create or alter the policy, in the schema in use
    for that statement. Use a fully qualified name for a tag in another schema.

`'value'`
:   Tag value to test for, as a string literal.

## Returns

Returns a BOOLEAN: TRUE if the value is assigned to the tag on the current table, including a value inherited from a parent
object. FALSE otherwise.

## Usage notes

- Call this function from a [data protection policy](/user-guide/data-protection-policies-snowsight) condition.

  Snowflake returns an error if you call it in a SELECT query, a view, a materialized view, or a user-defined function (UDF).
- Both arguments must be string literals.
- The tag must exist when you create or alter the policy. Otherwise, Snowflake returns the following error message:

  ```
  Tag '<tag_name>' does not exist or not authorized.
  ```
- The comparison is case-sensitive. On a multi-value tag, the function returns TRUE when `<value>` is one of the assigned values.
  It also returns TRUE when `<value>` equals the single value of a tag that is not multi-value.
- The function checks the tag on the table, including a tag the table inherits from a parent object.
- This function applies to table-like objects, such as views.

## Examples

Mask a column when the table’s `sensitivity` tag contains `confidential`:

Copy code

```
CREATE TAG sensitivity MULTI_VALUE = TRUE;

CREATE TABLE orders (id NUMBER, note STRING);
INSERT INTO orders VALUES (1, 'invoice 42');

CREATE MASKING POLICY mask_by_table
  AS (v STRING) RETURNS STRING ->
    CASE
      WHEN SYSTEM$TAG_VALUE_CONTAINS_ON_CURRENT_TABLE('sensitivity', 'confidential') THEN '***MASKED***'
      ELSE v
    END;

ALTER TABLE orders MODIFY COLUMN note SET MASKING POLICY mask_by_table;
ALTER TABLE orders ADD VALUE 'confidential' FOR TAG sensitivity;
```

Every role receives `***MASKED***` for `note`.

Hide every row when the table’s tag contains `restricted`:

Copy code

```
CREATE TAG access_tag MULTI_VALUE = TRUE;

CREATE TABLE tickets (id NUMBER, body STRING);
INSERT INTO tickets VALUES (1, 'visible');

CREATE ROW ACCESS POLICY hide_restricted
  AS (id_val NUMBER) RETURNS BOOLEAN ->
    CASE
      WHEN SYSTEM$TAG_VALUE_CONTAINS_ON_CURRENT_TABLE('access_tag', 'restricted') THEN false
      ELSE true
    END;

ALTER TABLE tickets ADD ROW ACCESS POLICY hide_restricted ON (id);
ALTER TABLE tickets ADD VALUE 'restricted' FOR TAG access_tag;
```

Every role, including the policy owner, receives no rows from `tickets`. Dropping the `restricted` value returns the inserted row on
the next query.
