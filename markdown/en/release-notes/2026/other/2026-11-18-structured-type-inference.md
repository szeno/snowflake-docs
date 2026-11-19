# Nov 18, 2026: Schema detection and evolution for structured types (*General availability*)

With this release, Snowflake can create structured `OBJECT`, `ARRAY`, and `MAP` columns from the nested data in your Parquet, JSON,
Avro, and ORC files. When you load these files with `COPY INTO` or Snowpipe, schema evolution adds new structured columns and
fields as your data evolves.

Key use cases include:

- **Create tables with structured columns from your files:** [INFER\_SCHEMA](/sql-reference/functions/infer_schema) infers the structured
  column definitions, so you don’t write them by hand.
- **Add new nested columns and fields as they appear:** Schema evolution adds new nested columns as structured columns and adds
  new fields to existing structured columns.
- **Evolve nested columns in Snowflake-managed Apache Iceberg™ tables:** Like standard tables, these tables now gain new nested columns
  and fields.

To get started, set `INFER_NESTED_TYPES` to `TRUE` in
[INFER\_SCHEMA](/sql-reference/functions/infer_schema#label-infer-schema-infer-nested-types) and in your
[COPY INTO](/sql-reference/sql/copy-into-table#label-copy-option-infer-nested-types) statements or pipes. `INFER_NESTED_TYPES` is
`FALSE` by default, so existing loads aren’t affected.

For more information, see [Detect and evolve structured columns](/user-guide/data-load-schema-evolution#label-schema-evolution-structured-types).
