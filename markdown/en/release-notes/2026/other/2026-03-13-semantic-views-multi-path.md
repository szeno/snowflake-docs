# Mar 13, 2026: Support for specifying relationship paths in semantic views (*Preview*)

In some cases, multiple relationship paths might exist between two specific logical tables in a semantic view. In these cases,
you can now specify which relationship path to use when defining a metric.

Support for specifying the relationship path is in [Preview](/release-notes/preview-features).

In the METRICS clause of the [CREATE SEMANTIC VIEW](/sql-reference/sql/create-semantic-view) command, specify the name of the relationship to use
in the USING clause:

Copy code

```
METRICS (
  <table_alias>.<metric>
    [ USING ( <relationship_name> [ , ... ] )
    AS <sql_expr>
  [ , ... ]
)
```

For more information, see [Specifying the relationship for a metric when multiple relationship paths exist](/user-guide/views-semantic/sql#label-semantic-views-create-logical-tables-relations).
