# May 28, 2024 — ML Functions Release Notes

## Simpler SQL for storing results from ML functions

You can now call the [Forecast](/user-guide/ml-functions/forecasting) and
[Detect Anomalies](/user-guide/ml-functions/anomaly-detection) ML Functions directly in the FROM clause
of a SELECT statement. You can call methods like [<model\_name>!DETECT\_ANOMALIES](/sql-reference/classes/anomaly-detection/methods/detect_anomalies),
[<model\_name>!FORECAST](/sql-reference/classes/forecast/methods/forecast), and
[<model\_name>!SHOW\_EVALUATION\_METRICS](/sql-reference/classes/forecast/methods/show_evaluation_metrics) in the FROM clause.

You can use this technique to simplify the SQL statements for saving results to a table. For example, rather than using the
[SQLID](/developer-guide/snowflake-scripting/query-id) Snowflake Scripting variable with the
[RESULT\_SCAN](/sql-reference/functions/result_scan) function to create a table containing these results:

Copy code

```
BEGIN
  CALL model!FORECAST(FORECASTING_PERIODS => 7);
  LET x := SQLID;
  CREATE TABLE my_forecasts AS SELECT * FROM TABLE(RESULT_SCAN(:x));
END;
SELECT * FROM my_forecasts;
```

you can use a query that directly selects from the results of calling the methods:

Copy code

```
CREATE TABLE my_forecasts AS
  SELECT * FROM TABLE(model!forecast(forecasting_periods => 7));
```

As shown in the example above, when calling the method, omit the [CALL](/sql-reference/sql/call) command. Instead, put the call
in parentheses, preceded by the TABLE keyword.

For details, see [Selecting columns from SQL class instance methods that return tabular data](/sql-reference/snowflake-db-classes#label-class-select-from-methods).

In addition, as [announced earlier](/release-notes/2024/other/2024-05-22-table-references) and shown in the example above,
you can use the TABLE keyword (rather than calling [SYSTEM$REFERENCE](/sql-reference/functions/system_reference)) to create a reference to
pass in to the method.
