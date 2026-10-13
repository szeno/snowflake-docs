Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$GET\_COLUMN\_COMMENT\_PROPAGATION\_SOURCE

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Returns the column that a propagated comment was originally written on. Given a column whose comment arrived through
[column comment propagation](/user-guide/comment-propagation), the function walks the as-is column lineage upstream
and returns the fully qualified name of the column whose comment a user wrote.

Use this function to tell a comment that somebody wrote on a column from a comment that propagation copied in, and to
find the column to edit when you want to change the comment everywhere it appears.

## Syntax

Copy code

```
SYSTEM$GET_COLUMN_COMMENT_PROPAGATION_SOURCE( '<column_name>' )
```

## Arguments

`column_name`
:   Specifies the fully qualified name of the column to resolve, in the form
    `database_name.schema_name.object_name.column_name`. The
    object can be a table, view, materialized view, or dynamic table.

## Returns

Returns a VARCHAR containing the fully qualified name of the origin column, or NULL when there’s no propagation source
to report.

The function returns NULL in each of the following cases:

- The column’s comment was written by a user, rather than propagated.
- The column has no comment.
- No upstream column carrying a user-written comment is reachable through as-is lineage.
- Your role can’t resolve an object on the upstream path. The walk stops at the first object you can’t see, so the
  function doesn’t disclose the name of an object you don’t have access to.

## Usage notes

- Calling this function requires the VIEW LINEAGE privilege on the account. For more information, see
  [Access control for lineage information](/user-guide/ui-snowsight-lineage#label-lineage-privileges).
- The function reports only the origin column, not the chain of objects between that column and the one you passed in.
  To see the intervening lineage, use the **Lineage** tab in Snowsight.
- A comment that propagated and was later edited in place on the downstream column is a user comment from that point on,
  so the function returns NULL for it.

## Examples

These examples use the lineage graph from
[Examples](/user-guide/comment-propagation#label-comment-propagation-examples): a table `orders` whose column `order_id`
carries a user-written comment, a dynamic table `orders_dt` that selects it as-is, and a view `orders_v1` on that
dynamic table.

Resolve the origin of the comment on `orders_v1.order_id`:

> Copy code
>
> ```
> SELECT SYSTEM$GET_COLUMN_COMMENT_PROPAGATION_SOURCE('my_db.my_schema.orders_v1.order_id');
> ```
>
> ```
> +-----------------------------------------------------------------+
> | SYSTEM$GET_COLUMN_COMMENT_PROPAGATION_SOURCE(...)               |
> |-----------------------------------------------------------------|
> | MY_DB.MY_SCHEMA.ORDERS.ORDER_ID                                 |
> +-----------------------------------------------------------------+
> ```

Calling the function on the origin column itself returns NULL, because its comment wasn’t propagated:

> Copy code
>
> ```
> SELECT SYSTEM$GET_COLUMN_COMMENT_PROPAGATION_SOURCE('my_db.my_schema.orders.order_id');
> ```
>
> ```
> +-----------------------------------------------------------------+
> | SYSTEM$GET_COLUMN_COMMENT_PROPAGATION_SOURCE(...)               |
> |-----------------------------------------------------------------|
> | NULL                                                            |
> +-----------------------------------------------------------------+
> ```
