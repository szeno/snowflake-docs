# Nov 13, 2026: Many-to-many relationships in semantic views (*Preview*)

Many-to-many relationships are now in preview for semantic views. You can model a many-to-many relationship
between two logical tables in either of the following ways:

- **Through a bridge table**: Define two many-to-one relationships from a bridge (junction) table to each of the
  two entity tables.
- **Directly**: Define a relationship that references columns that aren’t a primary key or unique key in the
  other logical table. You don’t need a bridge table or a special keyword.

In both cases, Snowflake infers the many-to-many path from the relationship graph and handles deduplication
automatically, so metric values aren’t double-counted when a query fans out across the relationship.

For example, the following relationship is a direct many-to-many relationship because the `promotions` logical
table doesn’t define a primary key, and the same promotion code can appear in several rows:

Copy code

```
RELATIONSHIPS (
  orders_to_promotions AS orders(promo_code) REFERENCES promotions(promo_code)
)
```

You can define many-to-many relationships with [CREATE SEMANTIC VIEW](/sql-reference/sql/create-semantic-view) or in the
`relationships` key of the [YAML specification](/user-guide/views-semantic/semantic-view-yaml-spec).

Queries that traverse many-to-many relationships can’t use level of detail (LOD) metrics or multi-path metrics
that use the `USING` clause.

For more information, see the following topics:

- [Modeling many-to-many relationships](/user-guide/views-semantic/sql#label-semantic-views-many-to-many)
- [Many-to-many relationship queries](/user-guide/views-semantic/querying#label-semantic-views-querying-many-to-many)
