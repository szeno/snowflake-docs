# Save analysis results in collaborations

Feature — Generally Available

Currently available in [these regions](/user-guide/cleanrooms/installing-dcr#label-dcr-supported-regions).

Not available in government and VPS deployments.

By default, the results of a `COLLABORATION.RUN` call are returned to the caller and aren’t stored. If you want to revisit results later,
compare runs, or track how results change over time (for example, a weekly audience overlap trend), you can save the results of a run to
a durable table in the clean room. You can then query the saved table directly instead of rerunning the analysis.

To save results, add the `save_mode` and `name` fields to your [analysis specification](/user-guide/cleanrooms/spec-analysis). The run
still returns the analysis rows inline, exactly as it does without saving, so existing callers aren’t affected.

Saving results is supported for SQL analysis templates (`sql_analysis`). Activation templates don’t support `save_mode`.

## How saving works

When you run an analysis with `save_mode`, the clean room writes the results to a table named after the `name` field in the
`SAVED_RESULTS` schema of the clean room application installed in your account:

```
SFDCR_<COLLABORATION_NAME>.SAVED_RESULTS.<name>
```

Replace `<COLLABORATION_NAME>` with your collaboration name, and keep the `SFDCR_` prefix.

The `SAVED_RESULTS` schema isn’t versioned, so saved results persist across clean room upgrades.

Each saved table contains every column that the template returns, plus two metadata columns that Snowflake adds to each row:

`SFDCR$RUN_TIMESTAMP`
:   The time (`TIMESTAMP_NTZ`) when the row was written. All rows written by the same run share the same value, so you can group by this
    column to compare runs.

`SFDCR$ACTIVITY_ID`
:   The activity ID of the `COLLABORATION.RUN` call that wrote the row. Use this column to join saved results to the
    [analysis activity history](/user-guide/cleanrooms/activity-history).

These metadata columns are excluded from the results that `COLLABORATION.RUN` returns inline. The inline results contain only the rows
written by that call, even when the saved table holds rows from earlier runs.

Snowflake also records each saved result in the `SAVED_RESULTS.SFDCR$SUMMARY` table, which has the following columns:

| Column | Description |
| --- | --- |
| `RESULT_NAME` | The `name` of the saved result. |
| `TEMPLATE_NAME` | The template that produced the result. |
| `ANALYSIS_SPEC` | The analysis specification used to create the result. |

Expand

Show lessSee more

Saved results are stored in your account, in the clean room application installed for the collaboration. Other collaborators can’t
see them. In your account, roles that can run analyses in the collaboration have `SELECT` access to the saved tables and to
`SFDCR$SUMMARY`, but can’t modify or drop them.

## Save modes

Set `save_mode` to one of the following values. If you omit `save_mode`, the results aren’t saved.

`create`
:   Creates a new saved result table and saves the results of the current run into it. If a saved result with the same `name` already
    exists, the run fails before the analysis query runs, so no compute is spent.

`insert`
:   Appends the results of the current run to an existing saved result table. Use `insert` for every run after the first one. The run
    fails before the analysis query runs if no saved result with that `name` exists yet.

    The analysis specification for an insert must match the specification that created the table. Only `save_mode` can differ. Argument
    values must match exactly, and the order of list entries such as `source_tables` must match too. The order of keys doesn’t matter.
    Adding or changing optional fields such as `version` or `description` also causes a mismatch. If the specification doesn’t match, the
    run fails before the analysis query runs.

    The output columns must also match the saved table, in the same order. If the source table adds, removes, or reorders a column, insert
    fails and lists the columns that differ. Use `replace` or save under a new name.

`replace`
:   Replaces the saved result table with a new table that contains only the results of the current run. Because the whole table is
    replaced, all rows from previous runs saved under this `name`, including rows appended by `insert` runs, are permanently removed. If no
    saved result with that `name` exists, `replace` creates one. The specification recorded in `SFDCR$SUMMARY` is updated to the new
    specification.

The `save_mode` value isn’t case-sensitive.

## Considerations

Consider the following before you save results:

- **Saved results can’t be deleted.** After you save a result, you can’t drop its table or delete rows from it. The only way to remove
  saved rows is a `replace` run, which discards all of them. Choose result names carefully.
- **`replace` overwrites all history for the result name.** A `replace` run discards every row previously saved under that `name`,
  including rows appended by earlier `insert` runs, and keeps only the rows from the current run. There’s no confirmation or safeguard.
  To keep history, use `insert` instead.
- **Create first, then insert.** Like a database table, use `create` for the first run and `insert` for every later run.
- **To change the analysis, use a new name.** Because `insert` requires the same specification, a run with different arguments or
  view mappings can’t be appended to an existing result. Save it under a new `name` with `create`, or use `replace` if you’re willing to
  lose the existing history.
- **Output columns must stay the same.** An `insert` fails if the analysis output columns differ from the saved table, even when the
  specification is unchanged. This happens when a source table adds, removes, or reorders a column. The error lists the columns that
  differ. Use `replace` or save under a new name.
- **A valid result name is required.** When `save_mode` is set, use up to 75 letters, digits, or underscores for `name`, and don’t
  start with a digit. Names aren’t case-sensitive and must be unique within the collaboration’s saved results, so `weekly_overlap` and
  `WEEKLY_OVERLAP` refer to the same saved result.
- **Template output can’t use reserved column names.** If a template’s output already contains a column named `SFDCR$RUN_TIMESTAMP` or `SFDCR$ACTIVITY_ID`, the save
  fails. Alias the column in the template.

## Example

The following example saves the results of an audience overlap analysis on the first run, and then appends the results of later runs.

1. Run the analysis with `save_mode: create` to create the saved result table and save the first run’s results:

   Copy code

   ```
   CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.RUN(
     'my_collaboration',
     $$
   api_version: 2.0.0
   spec_type: analysis
   name: weekly_audience_overlap
   save_mode: create
   template: standard_audience_overlap_v0
   template_configuration:
     view_mappings:
       source_tables:
         - Provider1.provider1_offering_v1.CUSTOMERS
     local_view_mappings:
       my_tables:
         - Analyst1.analyst1_offering_v1.CUSTOMERS
     arguments:
       join_clauses:
         - "p1.hashed_email = c1.hashed_email"
       count_column:
         - hashed_email
   $$
   );
   ```
2. For each later run, use the same specification with `save_mode: insert` to append that run’s results:

   Copy code

   ```
   CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.RUN(
     'my_collaboration',
     $$
   api_version: 2.0.0
   spec_type: analysis
   name: weekly_audience_overlap
   save_mode: insert
   template: standard_audience_overlap_v0
   template_configuration:
     view_mappings:
       source_tables:
         - Provider1.provider1_offering_v1.CUSTOMERS
     local_view_mappings:
       my_tables:
         - Analyst1.analyst1_offering_v1.CUSTOMERS
     arguments:
       join_clauses:
         - "p1.hashed_email = c1.hashed_email"
       count_column:
         - hashed_email
   $$
   );
   ```
3. Query the saved result. Group by `SFDCR$RUN_TIMESTAMP` to compare runs:

   Copy code

   ```
   SELECT "SFDCR$RUN_TIMESTAMP", COUNT(*) AS row_count
     FROM SFDCR_MY_COLLABORATION.SAVED_RESULTS.WEEKLY_AUDIENCE_OVERLAP
     GROUP BY "SFDCR$RUN_TIMESTAMP"
     ORDER BY "SFDCR$RUN_TIMESTAMP";
   ```

## List saved results

To list the saved results in a collaboration, along with the template that produced each one, join `INFORMATION_SCHEMA.TABLES` to
`SFDCR$SUMMARY`:

Copy code

```
SELECT t.TABLE_NAME, t.CREATED, t.LAST_ALTERED, t.ROW_COUNT, s.TEMPLATE_NAME
  FROM SFDCR_MY_COLLABORATION.INFORMATION_SCHEMA.TABLES t
  JOIN SFDCR_MY_COLLABORATION.SAVED_RESULTS."SFDCR$SUMMARY" s
    ON UPPER(t.TABLE_NAME) = UPPER(s.RESULT_NAME)
  WHERE t.TABLE_SCHEMA = 'SAVED_RESULTS';
```
