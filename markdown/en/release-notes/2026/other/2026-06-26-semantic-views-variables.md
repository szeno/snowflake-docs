# June 26, 2026: Support for variables in semantic views (*General availability*)

You can now define [variables](/user-guide/views-semantic/variables) in a
[semantic view](/user-guide/views-semantic/overview) to parameterize facts, dimensions, and metrics.
Variables let you customize calculations at query time without changing the view definition.

Define variables when you create a semantic view using the `VARIABLES` clause in the
[CREATE SEMANTIC VIEW](/sql-reference/sql/create-semantic-view) command, or by adding a `variables` key in the
[YAML specification](/user-guide/views-semantic/semantic-view-yaml-spec). Provide variable values at query time using the
`VARIABLES` clause in the [SEMANTIC\_VIEW construct](/sql-reference/constructs/semantic_view).

For more information, see [Using variables in a semantic view](/user-guide/views-semantic/variables).
