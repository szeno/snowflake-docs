# Code Bundles: EXECUTE CODE BUNDLE and EXECUTE NOTEBOOK PROJECT return RETURN\_VALUE instead of status or result

[EXECUTE CODE BUNDLE](/sql-reference/sql/execute-code-bundle) and [EXECUTE NOTEBOOK PROJECT](/sql-reference/sql/execute-notebook-project)
no longer return a success message in a column named `status` or `result`. A successful run returns one row with one nullable `VARCHAR`
column named `RETURN_VALUE`, which holds the value that the run returned, or NULL if it returned nothing. The `status` and `result` columns
are removed for every bundle type and compute type. The Code Bundles REST API and Python API change in the same way.

This change affects anything that reads the output of these commands, including:

- SQL scripts, stored procedures, and tasks that read the output with `RESULT_SCAN`, `$1`, or a column name.
- Applications that use a Snowflake driver or connector, such as JDBC, ODBC, or the Python connector, and read the result set.
- Orchestrators, CI/CD pipelines, and other third-party tools that run these commands and inspect the `status` or `result` column or the
  success message to decide whether a run succeeded.
- Clients of the Code Bundles REST API and the Snowflake Python API.

The following table summarizes the change:

| Surface | Before the change | After the change |
| --- | --- | --- |
| SQL result set | One column, `status` or `result`, that contains a success message. | One nullable `VARCHAR` column, `RETURN_VALUE`, that contains the run’s return value or NULL. |
| REST API response body | `{"status": "..."}` or `{"result": "..."}` | `{"return_value": "..."}`, or `{"return_value": null}` when the run returns nothing. |
| Python API (`CodeBundleResource.execute()`) | Returns a `SuccessResponse` whose `status` holds the success message. | Returns an `ExecuteCodeBundleResponse`. Its `return_value` attribute holds the run’s return value (`str` or `None`). It isn’t a `SuccessResponse`, and its `status` is `None`. |
| Failed run | The statement raises an error and returns no row. | Unchanged: the statement raises an error and returns no row. |

Expand

Show lessSee more

Before the change:
:   A successful run returns one row with one column that contains a success message. The column name and the message depend on how the run
    executes:

    | How the run executes | Column | Value of a successful run |
    | --- | --- | --- |
    | Notebook projects, and `custom` Code Bundles on a compute pool | `status` | `Statement executed successfully.` |
    | `ml` Code Bundles | `status` | `Statement executed successfully.` |
    | `custom` Python Code Bundles on a warehouse | `result` | `Project <name> executed successfully` |
    | `custom` Java or Scala Code Bundles on a warehouse | `result` | An empty string |
    | `spark` Code Bundles | `status` or `result`, depending on the Spark runtime | `Spark Application completed successfully.` or an empty string |

    Expand

    Show lessSee more

    For example:

    Copy code

    ```
    EXECUTE CODE BUNDLE my_db.my_schema.my_bundle
      ENTRYPOINT = 'main.py';
    ```

    ```
    +----------------------------------+
    | status                           |
    |----------------------------------|
    | Statement executed successfully. |
    +----------------------------------+
    ```

After the change:
:   A successful run returns one row with one nullable `VARCHAR` column named `RETURN_VALUE`, for every bundle type and compute type. The column
    contains the value that the run returned:

    | Entrypoint | `RETURN_VALUE` |
    | --- | --- |
    | A notebook (`.ipynb`) on a compute pool that calls `notebook.exit(value)` | The value passed to `notebook.exit()`. |
    | A Python method entrypoint in the form `file.py:method` | The value that the method returns. |
    | Any other run, including a Python script entrypoint such as `main.py` and Java or Scala Code Bundles | NULL |

    Expand

    Show lessSee more

    A Python `str` is returned as is. Any other value is returned as JSON text, as produced by `json.dumps()` with its default settings, so
    `{"rows_loaded": 42}` keeps the space after the colon and non-ASCII characters are escaped. A value that can’t be encoded as JSON fails the
    run with a `ReturnValueError`. On a compute pool, including notebook runs, the encoded value can be at most 16 MiB; a larger value fails the
    run with a `ReturnValueError`. On a warehouse, the size limits for stored procedure return values apply.

    On a compute pool, including notebook runs, returning a value requires [Container Runtime 3.0](/developer-guide/container-runtime/version-3) or later. Container Runtime 2.x
    versions don’t support return values.

    For example, if `main.py` defines a `run` method that returns `{"rows_loaded": 42}`:

    Copy code

    ```
    EXECUTE CODE BUNDLE my_db.my_schema.my_bundle
      ENTRYPOINT = 'main.py:run';
    ```

    ```
    +---------------------+
    | RETURN_VALUE        |
    |---------------------|
    | {"rows_loaded": 42} |
    +---------------------+
    ```

    A run that returns nothing produces one row in which `RETURN_VALUE` is NULL:

    Copy code

    ```
    EXECUTE CODE BUNDLE my_db.my_schema.my_bundle
      ENTRYPOINT = 'main.py';
    ```

    ```
    +--------------+
    | RETURN_VALUE |
    |--------------|
    | NULL         |
    +--------------+
    ```

    You can read the column as `$1`, `RETURN_VALUE`, or `"RETURN_VALUE"`. In [Snowflake Scripting](/developer-guide/snowflake-scripting/index),
    use `INTO` to assign the value to a variable:

    Copy code

    ```
    DECLARE
      run_output VARCHAR;
    BEGIN
      EXECUTE CODE BUNDLE my_db.my_schema.my_bundle
        ENTRYPOINT = 'main.py:run'
        INTO :run_output;
      RETURN run_output;
    END;
    ```

## Impact on existing code

- **Code that reads the column by name fails.** A query or client that references the `status` or `result` column fails with an invalid
  identifier error, or gets no value from a driver’s column lookup.
- **Code that reads the column by position keeps running, but gets a different value.** Code that uses `$1`, `fetchone()[0]`, `rows[0][0]`,
  or a similar positional read now receives the run’s return value or NULL instead of the success message.
- **Code that compares the output to a success message stops matching.** For example, a check such as
  `status = 'Statement executed successfully.'` is never true after the change. A tool that treats a missing or different success message as
  a failure reports successful runs as failed.
- **REST API responses change.** `POST /api/v2/databases/{database}/schemas/{schema}/code-bundles/{name}:execute` and
  `POST /api/v2/code-bundle-executions` return the result row as JSON with lowercase column names. The body changes from `{"status": ...}`
  or `{"result": ...}` to `{"return_value": ...}`.
- **Python API checks change.** Code that checks `isinstance(response, SuccessResponse)` or reads `response.status` after
  `CodeBundleResource.execute()` no longer detects success.
- **`EXECUTE NOTEBOOK PROJECT` changes in the same way.** Existing schedules and tasks that use the `NOTEBOOK PROJECT` grammar keep running.
  Only code that reads their output is affected.

## Actions required

Decide whether a run succeeded from whether the statement or request succeeded, not from its output. This approach works both before and
after the change.

- **SQL and Snowflake Scripting:** A run that completes without raising an error succeeded. Catch the error to handle a failure:

  Copy code

  ```
  BEGIN
    EXECUTE CODE BUNDLE my_db.my_schema.my_bundle
      ENTRYPOINT = 'main.py';
    RETURN 'succeeded';
  EXCEPTION
    WHEN OTHER THEN
      RETURN 'failed: ' || SQLERRM;
  END;
  ```
- **Drivers and connectors:** Treat a statement that completes without an exception as a successful run. Don’t compare the first column to a
  success message. Read `RETURN_VALUE` only if your entrypoint returns a value:

  Copy code

  ```
  cur = conn.cursor()
  # A failed run raises an exception here.
  cur.execute("EXECUTE CODE BUNDLE my_db.my_schema.my_bundle ENTRYPOINT = 'main.py:run'")
  return_value = cur.fetchone()[0]  # The run's return value, or None.
  ```
- **REST API:** Use the HTTP status code to decide whether a run succeeded. Read `return_value` from the response body only if your
  entrypoint returns a value.
- **Python API:** Treat `CodeBundleResource.execute()` returning without raising an exception as a successful run. Remove checks for
  `SuccessResponse` and `response.status`, and read `response.return_value` if your entrypoint returns a value.
- **Third-party tools and orchestrators:** If a tool checks for a `status` or `result` column or a success message, update its configuration,
  or upgrade it to a version that decides success from whether the statement succeeds.
- **Review past runs:** To check the status of a run after it finishes, query the
  [CODE\_BUNDLE\_HISTORY](/sql-reference/functions/code_bundle_history) table function by the run’s query ID:

  Copy code

  ```
  SELECT STATUS, ERROR_MESSAGE
    FROM TABLE(SNOWFLAKE.INFORMATION_SCHEMA.CODE_BUNDLE_HISTORY(
      QUERY_ID => '<query_id>'));
  ```

## When RETURN\_VALUE is NULL after a successful run

In addition to runs that don’t return a value, `RETURN_VALUE` is NULL in the following cases, even when the notebook calls
`notebook.exit(value)` or the method returns a value:

- The statement returns before the run finishes, such as when the run is executed asynchronously.
- The stages that Snowflake uses to cache notebook results in your account aren’t encrypted with `SNOWFLAKE_FULL` encryption.

## Additional notes

- If you have questions or concerns about this change, contact [Snowflake Support](/user-guide/contacting-support).
- For the complete output reference, see [EXECUTE CODE BUNDLE](/sql-reference/sql/execute-code-bundle#label-execute-code-bundle-output).
- For how to return a value from a notebook or a Python method, see
  [Return a value from a run](/developer-guide/code-bundles/code-bundles#return-values).

Ref: n/a
