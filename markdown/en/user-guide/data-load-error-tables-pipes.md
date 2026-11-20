# Update existing pipes for error logging and CHECK constraints

If a pipe already loads a table, you can start recording every row that the pipe rejects, and you can change the CHECK
constraints on the table, without loading any file twice or skipping any file. To turn on error logging for a table
that no pipe loads yet, see [Error logging for COPY INTO and Snowpipe](/user-guide/data-load-error-tables).

The examples on this page use the `orders` table and the `orders_pipe` pipe. For their definitions, see
[Turn on error logging and add CHECK constraints](/user-guide/data-load-error-tables#label-data-load-error-tables-turn-on) and
[Load files with ON\_ERROR = CONTINUE](/user-guide/data-load-error-tables#label-data-load-error-tables-load-files).

## Record errors from an existing pipe

A pipe that already loads the table starts recording errors within 15 minutes after you turn on error logging, without
being recreated. Rows that it rejects before then aren’t recorded. A pipe that you create after you turn on error
logging records errors from its first load.

The pipe records errors according to its `ON_ERROR` value, which you can change only by recreating the pipe:

- With the default, `SKIP_FILE`, the error table records one error for each file that the pipe skips. To record every
  rejected row, recreate the pipe with `ON_ERROR = CONTINUE`. For how this changes error notifications and other
  reports, see [Choose an ON\_ERROR value for a pipe](/user-guide/data-load-error-tables#label-data-load-error-tables-pipe-on-error).
- Error logging doesn’t support `SKIP_FILE_<num>` or `'SKIP_FILE_<num>%'`. To record errors from a pipe that uses one
  of these values, recreate the pipe with `SKIP_FILE` or `CONTINUE`.

To find the pipes that use the default, `SKIP_FILE`, list the pipes that load from a stage and whose definition doesn’t
set `ON_ERROR`. The output includes only the pipes on which your role has the `OWNERSHIP`, `MONITOR`, or `OPERATE`
privilege, unless your role has the global `MONITOR EXECUTION` privilege:

Copy code

```
SHOW PIPES IN ACCOUNT;

SELECT "database_name", "schema_name", "name"
  FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()))
  WHERE "kind" = 'STAGE'
    AND "definition" <> ''
    AND "definition" NOT ILIKE '%ON_ERROR%';
```

If you recreate several pipes, recreate one first, and check the result in step 5 before you recreate the others. To
recreate a pipe, do the following:

1. Turn on error logging for the target table, if it isn’t turned on already.
2. If you switch to `ON_ERROR = CONTINUE` and you rely on error notifications or `FAILED` events, set up another way to
   find out about errors, such as an
   [alert on the error table](/user-guide/data-load-error-tables-query#label-data-load-error-tables-alert).
3. Recreate the pipe without loading any file twice or skipping any file by following the steps in
   [Recreate a pipe safely](/user-guide/data-load-snowpipe-manage#label-snowpipe-manage-recreate-steps). In step 4 of those steps, set the
   `ON_ERROR` value that you chose in the pipe’s `COPY INTO` statement.
4. Optional: To load the rows from the files that the old pipe skipped, load the files, as described in
   [Load each skipped file](/user-guide/data-load-error-tables-reload#label-data-load-error-tables-load-skipped-files). The new pipe doesn’t
   load these files. Don’t load a file whose rows you already loaded.
5. After the new pipe loads a file that contains errors, check that the error table contains errors from the pipe
   with the `ON_ERROR` value that you chose:

   Copy code

   ```
   SELECT
       error_metadata:details:on_error::STRING AS on_error,
       COUNT(*) AS error_count
     FROM ERROR_TABLE(orders)
     WHERE error_metadata:details:pipe_name::STRING = 'MYDB.MYSCHEMA.ORDERS_PIPE'
     GROUP BY ALL;
   ```

   Replace `MYDB.MYSCHEMA` with the database and schema that contain your pipe, because the `pipe_name` value is the
   fully qualified name. The new pipe has the same name as the old pipe, so the query also counts the old pipe’s
   errors.

## Change the CHECK constraints on a table that a pipe loads

To change the CHECK constraints on a table that a pipe loads, drop each pipe that loads the table, change the
constraints, and then create the pipes again. You can’t add a CHECK constraint to a table that any pipe loads, and you
can’t drop a CHECK constraint or change it with `ALTER TABLE ... ALTER CONSTRAINT` on a table that a Snowpipe pipe
loads. Pausing the pipe doesn’t lift either restriction. If you try, the statement fails with one of the following
errors:

- `Cannot add CHECK constraint to table ... because it has active pipes`
- `Cannot drop or alter CHECK constraint on table ... because it has active pipes`

To find out which pipes block each change, see [CHECK constraints](/sql-reference/constraints-overview#label-constraints-check). To drop
and create the pipes without loading any file twice or skipping any file, follow
[Recreate a pipe safely](/user-guide/data-load-snowpipe-manage#label-snowpipe-manage-recreate-steps), with the following changes:

- If several pipes load the table, do steps 1 to 3 for each pipe before step 4, and steps 5 to 9 for each pipe after
  step 4.
- Before step 4, also suspend the tasks that run `COPY INTO` for the table, and wait for their runs in progress to
  finish. Stop the other `COPY INTO` statements and the applications that write to the table too. Rows that are
  written while a constraint is dropped aren’t checked, even after you add it again. Resume the tasks and applications
  after you create the pipes again. For the statements that suspend a task and find its runs in progress, see
  [Stop loads into the table](/user-guide/data-load-error-tables-reload#label-data-load-error-tables-stop-loads).
- In step 4, drop each pipe with `DROP PIPE`, change the constraints, and then create each pipe with `CREATE PIPE` and
  the `ON_ERROR` value that you chose, as described in
  [Choose an ON\_ERROR value for a pipe](/user-guide/data-load-error-tables#label-data-load-error-tables-pipe-on-error). Don’t use `CREATE OR REPLACE PIPE`,
  because you can’t change the constraints until every pipe that loads the table is dropped. To change the condition of
  a constraint, drop the constraint and add it again.

To add a constraint with `ALTER TABLE ... ADD CONSTRAINT`, specify `ENABLE NOVALIDATE`, which doesn’t check the rows
that the table already contains. Without it, the statement fails. For example, the following statements drop the
`orders_pipe` pipe, add a constraint that rejects orders whose ID is zero or negative, and create the pipe again from
the pipe definition that you saved:

Copy code

```
DROP PIPE orders_pipe;

ALTER TABLE orders ADD CONSTRAINT orders_id_check
  CHECK (order_id > 0) ENABLE NOVALIDATE;

CREATE PIPE orders_pipe
  AUTO_INGEST = TRUE
  AS
  COPY INTO orders
    FROM @orders_stage/json/
    FILE_FORMAT = (TYPE = JSON)
    MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
    ON_ERROR = CONTINUE;
```

To find the existing rows that violate the constraint, query the table for rows where the condition is `FALSE`:

Copy code

```
SELECT * FROM orders
  WHERE NOT (order_id > 0);
```

After you change the constraints, `COPY INTO` statements and the pipes that you create again enforce them on their next
load.
