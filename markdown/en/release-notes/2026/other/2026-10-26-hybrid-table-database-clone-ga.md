# Oct 26, 2026: Cloning databases that contain hybrid tables (*General availability*)

Cloning databases that contain hybrid tables is now generally available in the same Amazon Web Services,
Microsoft Azure, and Google Cloud commercial regions where hybrid tables are available.

`CREATE DATABASE ... CLONE` copies a database that contains hybrid tables, including a point-in-time
clone that uses Time Travel. Hybrid table data is physically copied, so the operation can take longer
than a metadata-only clone of standard tables and incurs compute and storage cost.

The following limits still apply:

- Hybrid tables can be cloned only with `CREATE DATABASE ... CLONE`. `CREATE SCHEMA ... CLONE`
  fails when the source schema contains hybrid tables, and cloning an individual hybrid table fails.
  Add `IGNORE HYBRID TABLES` to clone a database or schema and skip its hybrid tables.
- Point-in-time clones that include hybrid tables can use `TIMESTAMP` or `OFFSET` with `AT` or `BEFORE`.
  `STATEMENT` (a query ID) is not supported unless you add `IGNORE HYBRID TABLES`.

For more information, see [Clone databases that contain hybrid tables](/user-guide/tables-hybrid-clone).
