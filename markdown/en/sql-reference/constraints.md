# Constraints

Constraints define integrity and consistency rules for data stored in tables.
Snowflake provides support for constraints as defined in the ANSI SQL standard,
as well as some extensions for compatibility with other databases, such as Oracle.

Important

- For standard tables, Snowflake supports defining and maintaining constraints, but
  doesn’t enforce them, except for NOT NULL and CHECK constraints, which are always enforced.

  Violations of constraints might cause unexpected downstream effects. If you decide to create a
  constraint that must be relied upon, ensure that your downstream processes can maintain data
  integrity. For more information, see [Constraint properties](/sql-reference/sql/create-table-constraint#label-extended-constraint-properties).

  Constraints on standard tables are provided primarily for data modeling purposes and compatibility
  with other databases, as well as to support client tools that utilize constraints. For example,
  Tableau supports using constraints to perform join culling (join elimination), which can improve the
  performance of generated queries and cube refresh.
- For [hybrid tables](/user-guide/tables-hybrid), Snowflake both supports and enforces
  constraints. Primary key constraints are required and enforced on all hybrid tables, and other
  constraints are enforced when used.

**Next Topics:**

- [Overview of constraints](/sql-reference/constraints-overview)
- [Creating constraints](/sql-reference/constraints-create)
- [Modifying constraints](/sql-reference/constraints-alter)
- [Dropping constraints](/sql-reference/constraints-drop)
