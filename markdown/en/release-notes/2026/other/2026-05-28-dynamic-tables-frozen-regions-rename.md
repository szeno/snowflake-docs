# May 28, 2026: Dynamic tables immutability constraints renamed to frozen regions

The dynamic tables feature formerly known as the immutability constraint is now called the
frozen region of a dynamic table. As part of this rename, the `IMMUTABLE WHERE` clause is
also renamed to `FROZEN WHERE`.

The terminology changes are as follows:

| Old | New |
| --- | --- |
| Immutability constraint (feature name) | Frozen region of a dynamic table |
| `IMMUTABLE WHERE` (SQL keyword) | `FROZEN WHERE` |
| Immutable region | Frozen region |
| Mutable region | Active region |
| `METADATA$IS_IMMUTABLE` (metadata column) | `METADATA$IS_FROZEN` |

Expand

Show lessSee more

The rename is backward compatible. The `IMMUTABLE WHERE` keyword still works in `CREATE DYNAMIC TABLE`
and `ALTER DYNAMIC TABLE`, the `METADATA$IS_IMMUTABLE` metadata column still works, and existing
dynamic tables don’t need any changes.

For more information, see [Frozen regions and backfill](/user-guide/dynamic-tables/frozen-regions),
[CREATE DYNAMIC TABLE](/sql-reference/sql/create-dynamic-table), and [ALTER DYNAMIC TABLE](/sql-reference/sql/alter-dynamic-table).
