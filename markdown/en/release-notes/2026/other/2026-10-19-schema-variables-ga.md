# Oct 19, 2026: Schema variables (*General availability*)

With this release, we’re pleased to announce the general availability of schema variables.

Schema variables are named, typed, persistent scalar values scoped to a schema. Unlike session
variables, schema variables outlive sessions and are visible to all users who have the
appropriate privileges.

You can use schema variables to store shared configuration (such as a tax rate or API version),
environment tags, ETL pipeline state, parameterized view filters, and immutable constants, all
without single-row tables or UDFs.

Key capabilities include:

- Full DDL lifecycle: `CREATE VARIABLE`, `ALTER VARIABLE`, `DROP VARIABLE`, and `UNDROP VARIABLE`
  (with Time Travel support)
- Typed values with optional defaults
- Standard privilege model with separate `READ` and `WRITE` grants
- Resolution with the `$name` and `$schema.name` syntax; session variables shadow schema
  variables of the same name and can be used as per-session overrides
- Discovery via `SHOW SCHEMA VARIABLES IN SCHEMA` and `INFORMATION_SCHEMA.VARIABLES`

For more information, see the following topics:

- [Schema variables](/sql-reference/schema-variables)
- [CREATE VARIABLE](/sql-reference/sql/create-variable)
- [ALTER VARIABLE](/sql-reference/sql/alter-variable)
- [DROP VARIABLE](/sql-reference/sql/drop-variable)
- [UNDROP VARIABLE](/sql-reference/sql/undrop-variable)
- [SHOW SCHEMA VARIABLES IN SCHEMA](/sql-reference/sql/show-schema-variables)
- [DESCRIBE VARIABLE](/sql-reference/sql/desc-variable)
- [VARIABLES view](/sql-reference/info-schema/variables)
