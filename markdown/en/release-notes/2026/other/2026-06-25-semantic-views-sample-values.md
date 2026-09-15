# June 25, 2026: Support for sample values and enum indicators in semantic view DDL

When defining a [semantic view](/user-guide/views-semantic/overview), you can now specify sample values and enum indicators
in the [CREATE SEMANTIC VIEW](/sql-reference/sql/create-semantic-view) command.

- Use the `SAMPLE_VALUES` clause to provide representative values for a dimension or fact. Sample values help
  Cortex Analyst understand the range of data in a column so that it can generate more accurate SQL queries.
- Use the `IS_ENUM` keyword on a dimension to indicate that the sample values represent the complete set of possible values. When
  `IS_ENUM` is set, Cortex Analyst only chooses from those values when filtering on the column.

These features were previously available only in the [YAML specification](/user-guide/views-semantic/semantic-view-yaml-spec)
and are now supported in DDL as well.

For more information, see [Adding sample values and enum indicators](/user-guide/views-semantic/sql#label-semantic-views-sample-values).
