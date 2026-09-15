# ALTER SEMANTIC VIEW

Modifies properties, materializations, or other settings for an existing [semantic view](/user-guide/views-semantic/overview).

Note

You can’t use the ALTER SEMANTIC VIEW command to change properties other than the comment. To change other properties of the
semantic view, use [CREATE OR ALTER SEMANTIC VIEW](/sql-reference/sql/create-semantic-view#label-create-or-alter-semantic-view-syntax) or replace the semantic
view. See [Replacing an existing semantic view](/user-guide/views-semantic/sql#label-semantic-views-replace).

See also:
:   [CREATE SEMANTIC VIEW](/sql-reference/sql/create-semantic-view) , [DESCRIBE SEMANTIC VIEW](/sql-reference/sql/desc-semantic-view) , [DROP SEMANTIC VIEW](/sql-reference/sql/drop-semantic-view) , [SHOW SEMANTIC VIEWS](/sql-reference/sql/show-semantic-views) , [SHOW SEMANTIC DIMENSIONS](/sql-reference/sql/show-semantic-dimensions) , [SHOW SEMANTIC DIMENSIONS FOR METRIC](/sql-reference/sql/show-semantic-dimensions-for-metric) , [SHOW SEMANTIC FACTS](/sql-reference/sql/show-semantic-facts) , [SHOW SEMANTIC METRICS](/sql-reference/sql/show-semantic-metrics)

    [CREATE OR ALTER <object>](/sql-reference/sql/create-or-alter) , [Materializing dimensions and metrics in semantic views](/user-guide/views-semantic/materializations)

## Syntax

Copy code

```
ALTER SEMANTIC VIEW [ IF EXISTS ] <name> RENAME TO <new_name>

ALTER SEMANTIC VIEW [ IF EXISTS ] <name> SET
  { COMMENT = '<string_literal>' | MAX_STALENESS = <integer> }

ALTER SEMANTIC VIEW [ IF EXISTS ] <name> UNSET
  { COMMENT | MAX_STALENESS }

ALTER SEMANTIC VIEW <name> SET TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]

ALTER SEMANTIC VIEW <name> UNSET TAG <tag_name> [ , <tag_name> ... ]

ALTER SEMANTIC VIEW <name> ADD MATERIALIZATION <materialization_name>
  WAREHOUSE = <warehouse_name>
  [ REFRESH_MODE = { AUTO | FULL | INCREMENTAL } ]
  [ IMMUTABLE WHERE ( <immutable_condition> ) ]
  AS
    DIMENSIONS <dimension_name> [ , ... ]
    METRICS <metric_name> [ , ... ]
    [ WHERE ( <filter_condition> ) ]

ALTER SEMANTIC VIEW <name> DROP MATERIALIZATION <materialization_name>

ALTER SEMANTIC VIEW <name> SUSPEND MATERIALIZATION <materialization_name>

ALTER SEMANTIC VIEW <name> RESUME MATERIALIZATION <materialization_name>

ALTER SEMANTIC VIEW <name> REFRESH MATERIALIZATION <materialization_name>
```

Note

ALTER SEMANTIC VIEW only supports setting and unsetting tags at the semantic view level. To set tags on logical tables,
dimensions, facts, or metrics within a semantic view, use the [CREATE SEMANTIC VIEW](/sql-reference/sql/create-semantic-view) command.

## Parameters

`name`
:   Specifies the identifier for the semantic view to alter.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`RENAME TO new_name`
:   Changes the name of the semantic view to `new_name`. The new identifier must be unique within the schema.

    For more details about identifiers, see [Identifier requirements](/sql-reference/identifiers-syntax).

    You can move the object to a different database and/or schema while optionally renaming the object. To do so, specify
    a qualified `new_name` value that includes the new database and/or schema name in the form
    `db_name.schema_name.object_name` or `schema_name.object_name`, respectively.

    Note

    - The destination database and/or schema must already exist. In addition, an object with the same name cannot already
      exist in the new location; otherwise, the statement returns an error.
    - Moving an object to a managed access schema is prohibited unless the object owner (that is, the role that has
      the OWNERSHIP privilege on the object) also owns the target schema.

    When an object is renamed, other objects that reference it must be updated with the new name.

`SET ...`
:   Sets one or more specified properties or parameters for the semantic view:

    `COMMENT = 'string_literal'`
    :   Adds a comment or overwrites an existing comment for the semantic view.

    `MAX_STALENESS = integer`
    :   Sets the maximum number of seconds that a [materialization](/user-guide/views-semantic/materializations) can be stale before
        Snowflake automatically suspends it. Must be set before you can add a materialization.

        Minimum value: `120` (2 minutes). You can’t unset `MAX_STALENESS` while materializations exist on the semantic view.

    `TAG tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ]`
    :   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

        The tag value is always a string, and the maximum number of characters for the tag value is 256.

        For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

`UNSET ...`
:   Unsets one or more specified properties or parameters for the semantic view, which resets the properties to their defaults:

    - `COMMENT`
    - `MAX_STALENESS` — Can only be unset when no materializations exist on the semantic view.
    - `TAG tag_name [ , tag_name ... ]`

    To unset multiple properties or parameters with a single ALTER statement, separate each property or parameter with a comma.

    When unsetting a property or parameter, specify only the property or parameter name (unless the syntax above indicates that you
    should specify the value). Specifying the value returns an error.

`ADD MATERIALIZATION materialization_name`
:   Creates or replaces a [materialization](/user-guide/views-semantic/materializations) on the semantic view that pre-aggregates the specified
    dimensions and metrics. If a materialization with the same name already exists, it is updated.

    `WAREHOUSE = warehouse_name`
    :   The warehouse used to refresh the materialization.

    `REFRESH_MODE = { AUTO | FULL | INCREMENTAL }`
    :   Controls the refresh strategy. `AUTO` (default) uses incremental refresh when possible and falls back to full refresh for
        non-additive metrics. `FULL` always recomputes all data. `INCREMENTAL` always uses incremental refresh and fails if the
        metrics don’t support it.

    `IMMUTABLE WHERE ( immutable_condition )`
    :   An optional condition that identifies rows that don’t change over time. Snowflake skips these rows during incremental
        refreshes, reducing refresh cost and time. Use unqualified column names (for example, `order_year` rather than `orders.order_year`).

    `DIMENSIONS dimension_name [ , ... ]`
    :   The dimensions to include in the materialization.

    `METRICS metric_name [ , ... ]`
    :   The metrics to pre-aggregate in the materialization.

    `WHERE ( filter_condition )`
    :   An optional filter that limits which rows the materialization stores. Queries that include a compatible WHERE clause can
        be rewritten to use the materialization. This is different from `IMMUTABLE WHERE`: `WHERE` controls which rows are stored;
        `IMMUTABLE WHERE` is a refresh optimization hint.

`DROP MATERIALIZATION materialization_name`
:   Removes a materialization from the semantic view. The semantic view itself is not affected.

`SUSPEND MATERIALIZATION materialization_name`
:   Pauses background refreshes for the materialization and stops it from being used for query rewrites.

`RESUME MATERIALIZATION materialization_name`
:   Resumes a suspended materialization, re-enabling background refreshes and query rewrites.

`REFRESH MATERIALIZATION materialization_name`
:   Triggers an immediate refresh of the materialization using the current session warehouse.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Semantic view | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |
| USAGE | Warehouse | Required to add or refresh a materialization (`ADD MATERIALIZATION`, `REFRESH MATERIALIZATION`). |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).
- `MAX_STALENESS` must be set before you can add any materialization to the semantic view.
- You can’t unset `MAX_STALENESS` while materializations exist. Drop all materializations first.
- If you change a semantic view using `CREATE OR REPLACE SEMANTIC VIEW`, all materializations are dropped. Use
  `CREATE OR ALTER SEMANTIC VIEW` to preserve materializations across semantic view changes.

## Examples

The following example renames a semantic view:

Copy code

```
ALTER SEMANTIC VIEW sv RENAME TO sv_new_name;
```

The following example sets the comment for a semantic view:

Copy code

```
ALTER SEMANTIC VIEW my_semantic_view SET COMMENT = 'my comment';
```

The following example unsets the existing comment for a semantic view:

Copy code

```
ALTER SEMANTIC VIEW my_semantic_view UNSET COMMENT;
```

The following example sets the maximum staleness for materializations to 2 hours (7200 seconds):

Copy code

```
ALTER SEMANTIC VIEW revenue_analysis SET MAX_STALENESS = 7200;
```

The following example adds a materialization:

Copy code

```
ALTER SEMANTIC VIEW revenue_analysis ADD MATERIALIZATION revenue_by_customer
  WAREHOUSE = my_wh
  IMMUTABLE WHERE (order_date < '2024-01-01')
  AS
    DIMENSIONS customers.customer_name
    METRICS orders.total_revenue;
```

The following example suspends and then resumes a materialization:

Copy code

```
ALTER SEMANTIC VIEW revenue_analysis SUSPEND MATERIALIZATION revenue_by_customer;

ALTER SEMANTIC VIEW revenue_analysis RESUME MATERIALIZATION revenue_by_customer;
```

The following example manually refreshes a materialization:

Copy code

```
ALTER SEMANTIC VIEW revenue_analysis REFRESH MATERIALIZATION revenue_by_customer;
```

The following example drops a materialization:

Copy code

```
ALTER SEMANTIC VIEW revenue_analysis DROP MATERIALIZATION revenue_by_customer;
```
