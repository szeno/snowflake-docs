# May 05, 2026: Support for entity-level filters in semantic views (*General availability*)

When defining a [semantic view](/user-guide/views-semantic/overview), you can now define a fact or dimension as a filter by
specifying `LABELS = (FILTER)` in the [CREATE SEMANTIC VIEW](/sql-reference/sql/create-semantic-view) command. A filter is a fact or dimension
that resolves to a BOOLEAN value and can be used as a condition in the WHERE clause of a query.

For more information, see [Defining filters for logical tables in a semantic view](/user-guide/views-semantic/filters).
