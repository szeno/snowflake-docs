# Monitor analysis activity in collaborations

Feature — Generally Available

Currently available in [these regions](/user-guide/cleanrooms/installing-dcr#label-dcr-supported-regions).

Not available in government and VPS deployments.

Activity history gives every collaborator an audit trail of analysis activity in a collaboration. Each collaborator
sees only the activity and detail that is relevant to their [role in the collaboration](/user-guide/cleanrooms/roles); sensitive information from any partner is never
exposed across partners.

When you invoke a [template run](/user-guide/cleanrooms/collaboration-api-reference#label-dcr-collaboration-run-reference) in a collaboration, you are opting in to sharing
the activity metadata described on this page with the other collaborators whose resources were used by your run.

Note

Activity history is available in collaborations created on or after the [release of this feature](/release-notes/2026/other/2026-05-07-dcr).
Collaborations created before this date do not have access to activity history.

## What activity is visible to you

What you can see in activity history depends on your activity and the resources you contribute to the collaboration:

- **Runs your account executed:** You can always see the full detail of any analysis run your account executed in the collaboration, including template ID,
  data offerings referenced, source tables, local tables, template arguments, activation destination, duration, status, and failure
  reason.
- **Runs on your data offerings:** If your account added data offerings to the collaboration, you can see any runs that referenced
  those offerings, including the analysis runner, duration, status, and the IDs of your data offerings that were used. Source tables
  from other accounts, local tables, and template arguments are not visible to you for these runs. If a run failed, you see a redacted error message rather than the full failure detail.
- **Runs that used your template:** If your account added a template to the collaboration, you can see any runs that referenced
  that template, including the analysis runner, duration, and status. Data offering IDs, source tables, local tables, and template
  arguments are not visible to you for these runs. If a run failed, you see a redacted error message rather than the full failure detail.

If your account contributed multiple resource types, you see the union of all applicable activity.

## How to view activity history

To view activity history for a collaboration, call
[VIEW\_ACTIVITY\_HISTORY](/user-guide/cleanrooms/collaboration-api-reference#label-dcr-collaboration-view-activity-history-reference) with the collaboration name.

### Basic query

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.VIEW_ACTIVITY_HISTORY(
  $collaboration_name
);
```

### Apply additional filters

Pipe the result of the procedure call into a `SELECT` using `RESULT_SCAN` to apply additional filters in the same session.

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.VIEW_ACTIVITY_HISTORY(
  $collaboration_name
);

SELECT ACTIVITY_ID, ANALYSIS_RUNNER_ALIAS, START_TS, TOTAL_DURATION, STATUS, FAILURE_REASON
  FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()))
  WHERE START_TS >= DATEADD(day, -7, CURRENT_TIMESTAMP())
    AND STATUS = 'ERROR'
  ORDER BY START_TS DESC;
```

### Get query execution details for your account’s runs

Each activity record is tagged with its `ACTIVITY_ID` in your account’s query history. To see the full query execution details
for a run your account submitted, query [SNOWFLAKE.ACCOUNT\_USAGE.QUERY\_HISTORY](https://docs.snowflake.com/en/sql-reference/account-usage/query_history) and filter by the query tag.
Note that the view has a latency before records appear — see [QUERY\_HISTORY latency expectations](https://docs.snowflake.com/en/sql-reference/account-usage/query_history#general) for details.

Copy code

```
SELECT *
  FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
  WHERE QUERY_TAG = '{"activity_id": "<your_activity_id>"}'
  ORDER BY START_TIME DESC;
```

Replace `<your_activity_id>` with the `ACTIVITY_ID` value from `VIEW_ACTIVITY_HISTORY`.

## Result columns

`VIEW_ACTIVITY_HISTORY` returns the following columns:

| Column | Type | Description |
| --- | --- | --- |
| `ACTIVITY_ID` | VARCHAR | Unique identifier for the activity record. Also added as a Query Tag into the underlying query so you can correlate an entry with [account-level query history](https://docs.snowflake.com/en/sql-reference/account-usage/query_history). |
| `ANALYSIS_RUNNER_ALIAS` | VARCHAR | Alias of the collaborator that ran the analysis. |
| `START_TS` | TIMESTAMP\_LTZ | Timestamp when the run started. |
| `TOTAL_DURATION` | NUMBER | Total run duration, in milliseconds. |
| `STATUS` | VARCHAR | `SUCCESS` or `ERROR`. For activation template runs, `SUCCESS` reflects only that the template query executed successfully - failures during the export of activation results are not surfaced. |
| `FAILURE_REASON` | VARCHAR | Populated when `STATUS` is `ERROR`. The analysis runner who submitted the run sees the full error message. Other accounts see a redacted message. |
| `ACTIVITY_TYPE` | VARCHAR | Type of activity. Currently always `RUN`. |
| `ACTIVITY_INFO` | VARIANT | Additional details about the run. Contents are filtered based on what your account contributed to the collaboration. Possible sub-keys:   - `data_offering_ids` — IDs of the data offerings referenced by the run. Visible if your account provided data offerings. - `request_parameters.template_id` — ID of the template used. - `request_parameters.source_tables` — Tables passed to `RUN` as source tables. Visible if your account provided the   relevant data offerings. - `request_parameters.local_tables` — Tables passed to `RUN` as local tables. Visible only to the analysis runner. - `request_parameters.arguments` — Template arguments passed to `RUN`. Visible only to the analysis runner. - `request_parameters.activation_destination` — Activation destination for the run, if any. |

Expand

Show lessSee more

## Access control

You must use a role that was granted privileges by calling one of the following procedures:

- `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('VIEW ACTIVITY HISTORY', 'COLLABORATION', '{collaboration name}', '{role name}')`
- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE COLLABORATION', '{role name}')`
- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('JOIN COLLABORATION', '{role name}')`

## Limitations

- **Activation export failures are not surfaced:** For activation template runs, a `SUCCESS` status reflects only that the
  template query executed successfully. Failures that occur during the export of activation results are not reported in activity history.
- **Free-form SQL activity is not recorded:** Activity history only records template runs. Analyses run as
  [free-form SQL queries](/user-guide/cleanrooms/free-form-sql) do not appear in activity history.

## ML Jobs logs

Activity history records the overall status and duration of an ML Jobs run, the same as for any other template run.
For container-level log output (stdout/stderr from the job script), see
[Monitor the ML Job](/user-guide/cleanrooms/ml-jobs#label-dcr-ml-jobs-monitoring).

## Related topics

- [VIEW\_ACTIVITY\_HISTORY](/user-guide/cleanrooms/collaboration-api-reference#label-dcr-collaboration-view-activity-history-reference) — Stored procedure API reference.
- [Managing access to collaborations, resources, and data](/user-guide/cleanrooms/manage-access) — Granting privileges on a collaboration.
