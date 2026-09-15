# Multi-value tags

## Overview

Standard tags support only a single value per tag on an object. Multi-value tags extend this capability by supporting multiple
values associated with the same tag on the same object or column. This is useful when an
object needs to be classified with multiple categories that aren’t mutually exclusive.

For example, a table might need to be tagged with multiple data sources (`DATA_SOURCE = 'CRM'` and `DATA_SOURCE = 'ERP'`)
or multiple compliance requirements (`COMPLIANCE = 'GDPR'` and `COMPLIANCE = 'PCI'`).

Key characteristics of multi-value tags:

- A tag must be explicitly configured with the MULTI\_VALUE = TRUE property to support multiple values.
- After a tag is set to multi-value, it can’t be reverted to a single-value tag.
- You use `ADD VALUE` and `DROP VALUE` operations to manage multiple values on an object.
- The default limit is 10 values per multi-value tag per object.
- Multi-value tags work with [tag propagation](/user-guide/object-tagging/propagation). The `ON_CONFLICT = MERGE` strategy is available only when `MULTI_VALUE = TRUE`.

## Multi-value tags vs single-value tags

| Topic | Single-value tags | Multi-value tags |
| --- | --- | --- |
| Cardinality | One value per tag per object or column. | Up to 10 values per tag per object by default. |
| Tag definition | Created with default behavior (`MULTI_VALUE` is false or omitted). | Tag is created or altered with `MULTI_VALUE = TRUE`. You can’t set `MULTI_VALUE` back to false. |
| Assigning values | Use `SET TAG` / `UNSET TAG` on the object or column. | Use `ADD VALUE` and `DROP VALUE` on `ALTER TABLE` to add or remove values; you can add the first value with `ADD VALUE` directly. `SET TAG` replaces the entire value set with the value you set (it doesn’t append). `UNSET TAG` removes the tag (see [ALTER TABLE ADD VALUE and DROP VALUE (multi-value tags)](#label-multi-value-tags-alter-table-add-drop)). |
| Propagation conflicts | Propagation uses your tag’s `ON_CONFLICT` behavior for a single winner value unless you adopt merge semantics separately. | `ON_CONFLICT = MERGE` is allowed only when the tag has `MULTI_VALUE = TRUE`; use it so multiple source values can accumulate on the target (for example on views). |
| `SYSTEM$GET_TAG` and policy helpers | Return the one tag value when a single value is present. | Return an error when more than one value exists. Use [SYSTEM$TAG\_VALUE\_CONTAINS](/sql-reference/functions/system_tag_value_contains) for checks, or keep policy logic on single-value tags only (see [Multi-value tags and masking policies](#label-multi-value-tags-policies)). |

Expand

Show lessSee more

## Creating a multi-value tag

To create a tag that supports multiple values, use the MULTI\_VALUE = TRUE attribute in the [CREATE TAG](/sql-reference/sql/create-tag) statement:

Copy code

```
CREATE TAG classification_tag MULTI_VALUE = TRUE;
```

You can also create a multi-value tag with propagation enabled:

Copy code

```
CREATE TAG data_source_tag
    MULTI_VALUE = TRUE
    PROPAGATE = ON_DEPENDENCY_AND_DATA_MOVEMENT
    ON_CONFLICT = MERGE;
```

To convert an existing tag to a multi-value tag, use [ALTER TAG](/sql-reference/sql/alter-tag):

Copy code

```
ALTER TAG sensitivity_tag SET MULTI_VALUE = TRUE;
```

Note

After a tag is set to multi-value, either at tag creation or by calling ALTER TAG, it can’t be reverted to a single-value tag.

## Assigning multiple values to objects

After creating a multi-value tag, use `ADD VALUE` and `DROP VALUE` on `ALTER TABLE` to add or remove values.
`SET TAG` sets the tag to exactly one string and replaces any values already present; it doesn’t append to the set.
Examples follow.

Assign multiple values to a table tag
:   To assign tag values to a table:

    Copy code

    ```
    -- Add values (ADD VALUE works for the first value too).
    ALTER TABLE customers ADD VALUE 'PII' FOR TAG classification_tag;
    ALTER TABLE customers ADD VALUE 'FINANCIAL' FOR TAG classification_tag;
    ALTER TABLE customers ADD VALUE 'GDPR' FOR TAG classification_tag;
    ```

    To remove a specific value:

    Copy code

    ```
    ALTER TABLE customers DROP VALUE 'FINANCIAL' FOR TAG classification_tag;
    ```

Assign multiple values to a column tag
:   To assign tag values to a column:

    Copy code

    ```
    -- Add values to a column.
    ALTER TABLE orders MODIFY COLUMN customer_email ADD VALUE 'email_pii' FOR TAG classification_tag;
    ALTER TABLE orders MODIFY COLUMN customer_email ADD VALUE 'contact_info' FOR TAG classification_tag;

    -- Drop a value from a column.
    ALTER TABLE orders MODIFY COLUMN customer_email DROP VALUE 'contact_info' FOR TAG classification_tag;
    ```

    You can also modify multiple columns in a single statement:

    Copy code

    ```
    ALTER TABLE orders MODIFY
        COLUMN order_id ADD VALUE 'id_field' FOR TAG classification_tag,
        COLUMN amount ADD VALUE 'financial_data' FOR TAG classification_tag;
    ```

## ALTER TABLE ADD VALUE and DROP VALUE (multi-value tags)

Adds or removes values from a multi-value tag on a table or column. This topic describes the `ADD VALUE` and `DROP VALUE` syntax for
multi-value tags. For the full `ALTER TABLE` reference, see [ALTER TABLE](/sql-reference/sql/alter-table).

### Syntax

#### Table-level operations

Copy code

```
ALTER TABLE [ IF EXISTS ] <table_name> ADD VALUE '<tag_value>' FOR TAG <tag_name>

ALTER TABLE [ IF EXISTS ] <table_name> DROP VALUE '<tag_value>' FOR TAG <tag_name>
```

#### Column-level operations

Copy code

```
ALTER TABLE [ IF EXISTS ] <table_name>
  { ALTER | MODIFY } [ COLUMN ] <col_name> ADD VALUE '<tag_value>' FOR TAG <tag_name>

ALTER TABLE [ IF EXISTS ] <table_name>
  { ALTER | MODIFY } [ COLUMN ] <col_name> DROP VALUE '<tag_value>' FOR TAG <tag_name>
```

#### Multi-column operations

You can modify multiple columns in a single statement:

Copy code

```
ALTER TABLE [ IF EXISTS ] <table_name> MODIFY
    COLUMN <col1_name> ADD VALUE '<tag_value>' FOR TAG <tag_name>,
    COLUMN <col2_name> ADD VALUE '<tag_value>' FOR TAG <tag_name>
```

### Parameters

`table_name`
:   The name of the table to modify.

`col_name`
:   The name of the column to modify (for column-level operations).

`'tag_value'`
:   The string value to add to or remove from the tag. The value must be a valid string that conforms to any `ALLOWED_VALUES`
    constraints on the tag.

`tag_name`
:   The identifier for the tag. The tag must have `MULTI_VALUE = TRUE` set.

### Usage notes for ALTER TABLE multi-value operations

- The tag must be created with `MULTI_VALUE = TRUE` (or converted using `ALTER TAG ... SET MULTI_VALUE = TRUE`) before you
  can use `ADD VALUE` or `DROP VALUE` operations. Attempting these operations on a single-value tag returns an error.
- You can use the standard `SET TAG` syntax, but it replaces the tag’s entire value set with a single string; it doesn’t append.
- Adding a duplicate value is a no-op. Dropping a value that does not exist is a no-op.
- When all values are dropped from a multi-value tag on an object, the tag association is removed from that object.
- Multi-value tags can’t be used with the `COPY TAGS` option in `CREATE TABLE ... CLONE` or `CREATE TABLE ... LIKE` statements.

Note

Views receive multi-value tags through [tag propagation](/user-guide/object-tagging/propagation) when the source tables
have multi-value tags with `ON_CONFLICT = MERGE`. Direct `ALTER VIEW ADD VALUE` syntax is not supported.

## Querying multi-value tags

The [SYSTEM$GET\_TAG](/sql-reference/functions/system_get_tag) function doesn’t support tags with multiple values.
If you call `SYSTEM$GET_TAG` on an object that has multiple values for a tag, the function returns an error.

If the tag has only one value (even if the tag is configured as multi-value), `SYSTEM$GET_TAG` returns that value without an error.

Copy code

```
-- Works: only one value assigned.
ALTER TABLE my_table ADD VALUE 'single_value' FOR TAG my_mv_tag;
SELECT SYSTEM$GET_TAG('my_mv_tag', 'my_table', 'TABLE');  -- Returns 'single_value'

-- Add another value.
ALTER TABLE my_table ADD VALUE 'second_value' FOR TAG my_mv_tag;

-- Fails: multiple values exist.
SELECT SYSTEM$GET_TAG('my_mv_tag', 'my_table', 'TABLE');  -- Error

-- Use SYSTEM$TAG_VALUE_CONTAINS instead.
SELECT SYSTEM$TAG_VALUE_CONTAINS('my_mv_tag', 'my_table', 'TABLE', 'single_value');  -- True
```

For the full reference, see [SYSTEM$TAG\_VALUE\_CONTAINS](/sql-reference/functions/system_tag_value_contains).

### SYSTEM$TAG\_VALUE\_CONTAINS

`SYSTEM$TAG_VALUE_CONTAINS` returns TRUE if the specified multi-value tag on the specified object or column contains the specified
value. It returns FALSE if the value is not present or if the tag is not assigned to the object. Use it whenever you might have more
than one value, because [SYSTEM$GET\_TAG](/sql-reference/functions/system_get_tag) raises an error when multiple values exist.

#### Examples

Copy code

```
SELECT SYSTEM$TAG_VALUE_CONTAINS('classification_tag', 'customers', 'TABLE', 'PII');        -- True
SELECT SYSTEM$TAG_VALUE_CONTAINS('classification_tag', 'customers', 'TABLE', 'FINANCIAL');  -- True
SELECT SYSTEM$TAG_VALUE_CONTAINS('classification_tag', 'customers', 'TABLE', 'HIPAA');      -- False
```

You can also use the TAG\_REFERENCES and TAG\_REFERENCES\_ALL\_COLUMNS table functions to view all tag values:

Copy code

```
SELECT *
  FROM TABLE(INFORMATION_SCHEMA.TAG_REFERENCES('customers', 'TABLE'));

SELECT *
  FROM TABLE(INFORMATION_SCHEMA.TAG_REFERENCES_ALL_COLUMNS('orders', 'TABLE'));
```

You can filter results to a specified tag:

Copy code

```
-- Show all values of the tag classification_tag in the CUSTOMERS table.
SELECT tag_name, tag_value
  FROM TABLE(INFORMATION_SCHEMA.TAG_REFERENCES('CUSTOMERS', 'TABLE'))
    WHERE tag_name = 'classification_tag';
```

## Tag propagation with multi-value tags

Multi-value tags work with [tag propagation](/user-guide/object-tagging/propagation). You can set `ON_CONFLICT = MERGE` on a tag only when `MULTI_VALUE = TRUE`; it isn’t valid for single-value tags. When you use the merge strategy, conflicting tag values from multiple source objects are combined into multiple values on the target object.

Views receive multi-value tags through propagation when all the source tables have multi-value tags with `ON_CONFLICT = MERGE`.

For example, if two source tables have different values for the same propagating tag, a view created from both tables
has both values:

Copy code

```
CREATE TAG data_source_tag
    MULTI_VALUE = TRUE
    PROPAGATE = ON_DEPENDENCY_AND_DATA_MOVEMENT
    ON_CONFLICT = MERGE;

ALTER TABLE sales_data SET TAG data_source_tag = 'sales_system';
ALTER TABLE support_data SET TAG data_source_tag = 'support_system';

-- Join view receives both values via propagation.
CREATE VIEW v_combined AS
    SELECT * FROM sales_data JOIN support_data ON sales_data.id = support_data.id;

SELECT SYSTEM$TAG_VALUE_CONTAINS('data_source_tag', 'v_combined', 'TABLE', 'sales_system');    -- True
SELECT SYSTEM$TAG_VALUE_CONTAINS('data_source_tag', 'v_combined', 'TABLE', 'support_system');  -- True
```

Changes to source table tags (adding or dropping values) automatically propagate to dependent objects.

## Multi-value tags and masking policies

The [SYSTEM$GET\_TAG\_ON\_CURRENT\_TABLE](/sql-reference/functions/system_get_tag_on_current_table) and [SYSTEM$GET\_TAG\_ON\_CURRENT\_COLUMN](/sql-reference/functions/system_get_tag_on_current_column) functions, which are used in masking policy and row access policy conditions, don’t support tags with multiple values.

If you need to use tags with masking policies, use single-value tags for the policy logic. You can use multi-value tags on
the same objects for other classification purposes, but don’t reference multi-value tags in policy conditions.

For application-level logic that needs to check multi-value tags, use `SYSTEM$TAG_VALUE_CONTAINS` in your queries:

Copy code

```
SELECT
    SYSTEM$TAG_VALUE_CONTAINS('env_tag', 'my_table', 'TABLE', 'prod') AS is_prod,
    SYSTEM$TAG_VALUE_CONTAINS('env_tag', 'my_table', 'TABLE', 'pci')  AS is_pci;
```

## Limitations

- The MULTI\_VALUE property can’t be set to FALSE. After a tag is configured as multi-value, it can’t be reverted.
- The default limit is 10 values per multi-value tag per object.
- `SYSTEM$GET_TAG`, `SYSTEM$GET_TAG_ON_CURRENT_TABLE`, and `SYSTEM$GET_TAG_ON_CURRENT_COLUMN` return an error when
  called on a tag with multiple values assigned. Use `SYSTEM$TAG_VALUE_CONTAINS` instead.
- Adding a duplicate value is a no-op (no error is raised, and the value count does not increase).
- ADD VALUE and DROP VALUE operations require the tag to have `MULTI_VALUE = TRUE`. Running these operations on a
  single-value tag returns an error.

## Supported objects

For the objects you can assign tags to, see [Supported objects](/user-guide/object-tagging/introduction#supported-objects).
