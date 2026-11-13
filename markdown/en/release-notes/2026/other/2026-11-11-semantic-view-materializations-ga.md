# Nov 11, 2026: Semantic view materializations (*General availability*)

Semantic view materializations are now generally available and are no longer in [Preview](/release-notes/preview-features).
With materializations, you can pre-aggregate frequently queried dimensions and metrics in a semantic view to improve query
performance.

With this release, you can also do the following:

- **Get recommendations from CoCo:** Use the bundled `suggest-sv-materializations` skill in CoCo to analyze slow semantic
  view queries or a Snowflake dashboard and get recommended materializations.
- **Check whether a query can use a materialization:** Call SYSTEM$CHECK\_SEMANTIC\_VIEW\_MATERIALIZATION\_REWRITE to check an
  existing materialization, or SYSTEM$CHECK\_HYPOTHETICAL\_SEMANTIC\_VIEW\_MATERIALIZATION\_REWRITE to check a materialization
  before you create it.
- **Materialize semi-additive metrics:** You can now include
  [semi-additive metrics](/user-guide/views-semantic/sql#label-semantic-views-metrics-semi-additive) in materializations.

For more information, see the following topics:

- [Materializing dimensions and metrics in semantic views](/user-guide/views-semantic/materializations)
- [Getting materialization recommendations with CoCo](/user-guide/views-semantic/materializations#label-semantic-views-materializing-coco)
- [Checking whether a query can use a materialization](/user-guide/views-semantic/materializations#label-semantic-views-materializing-check-rewrite)
