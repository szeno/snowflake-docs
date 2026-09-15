# Tag inheritance

A tag is inherited based on the Snowflake securable object hierarchy. A descendant of an object in the hierarchy inherits tags from its
ancestors. For example, a schema in an account inherits tags set on the account. Similarly, if a tag is applied to a table, the tag gets
applied to the columns in that table.

The following diagram shows the Snowflake securable object hierarchy:

> ![Child objects in the Snowflake securable object hierarchy inherit tags](/static/images/securable-object-hierarchy-org-to-column.png)

Note

Tag inheritance does not include propagation to nested objects. In the following example, `materialized_view_1` does not inherit
tags from `table_1` or `view_1`.

`table_1` » `view_1` » `materialized_view_1`

If you want tags from `view_1` to get automatically assigned to `materialized_view_1`, see
[Automatic tag propagation with user-defined tags](/user-guide/object-tagging/propagation).

## Overriding tag inheritance

It’s possible to override the value of an inherited tag on a given object by [manually setting](/user-guide/object-tagging/work#label-object-tagging-set) the tag on
the object. For example, if a table column inherits the tag named `cost_center` with a tag string value called `sales`, the tag can be
updated with a more specific tag string value such as `sales_na`, to specify the North America sales cost center.

The value of an inherited tag is overwritten when the tag is applied to the object as a result of
[automatic propagation](/user-guide/object-tagging/propagation).

The value of an inherited tag is overwritten by [sensitive data classification](/user-guide/classify-intro).
