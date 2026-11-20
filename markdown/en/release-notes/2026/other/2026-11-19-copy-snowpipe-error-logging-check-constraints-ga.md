# Nov 19, 2026: Error logging and CHECK constraint enforcement for COPY INTO and Snowpipe (*General availability*)

With this release, `COPY INTO` and Snowpipe can keep invalid rows out of your tables and record the rows that they
reject, so you can find and fix bad data with SQL. Error logging and CHECK constraint enforcement for
[COPY INTO <table>](/sql-reference/sql/copy-into-table) and [Snowpipe](/user-guide/data-load-snowpipe-intro) are now generally available.

- **Keep invalid rows out of your tables:** `COPY INTO` and Snowpipe enforce
  [CHECK constraints](/sql-reference/constraints-overview#label-constraints-check) on the target table and reject the
  rows that violate them.
- **See which rows were rejected and why:** With [error logging](/user-guide/data-load-error-tables), rejected rows from
  CSV, JSON, and Parquet files go to the table’s error table, with the error and, in most cases, the source record.
- **Fix rejected rows with SQL:** Correct the rejected rows as you insert them from the error table into the target
  table, without editing the source files. For more information, see [Correct and reload rejected rows](/user-guide/data-load-error-tables-reload).

To get started, run `ALTER TABLE <name> SET ERROR_LOGGING = TRUE` and set `ON_ERROR = CONTINUE` in your `COPY INTO`
statements or pipes to record every rejected row. If a pipe already loads the table, see
[Update existing pipes for error logging and CHECK constraints](/user-guide/data-load-error-tables-pipes). Loads into tables that don’t have error logging or CHECK constraints
aren’t affected.

For more information, see [Error logging for COPY INTO and Snowpipe](/user-guide/data-load-error-tables).
