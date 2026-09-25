# View collaboration activity in Snowsight

Feature — Generally Available

Currently available in [these regions](/user-guide/cleanrooms/installing-dcr#label-dcr-supported-regions).

Not available in government and VPS deployments.

The **Activity** tab gives you an audit trail of the analysis template runs in a collaboration. You can
see who ran an analysis, which template they ran, how long it took, and whether it succeeded, directly
in the UI.

The tab shows one collaboration at a time. You choose which one from a picker at the top of the tab.

What you can see depends on what your account contributed to the collaboration. You see runs that your
account submitted, runs that used a data offering you provided, and runs that used a template you shared.
The amount of detail in each record also depends on your role, and sensitive information from a partner
is never exposed to you. For a full breakdown of the fields visible to each role, see
[What activity is visible to you](/user-guide/cleanrooms/activity-history#label-dcr-collaboration-activity-history-personas).

## Open the Activity tab

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Data sharing** » **Data clean rooms**.
3. Select the **Activity** tab.

## Select a collaboration

The **Collaboration** picker lists the collaborations your account has joined, most recently updated
first. Collaborations you’ve been invited to but haven’t joined yet don’t appear, because they can’t
have activity yet. You can type in the picker to search the list.

To reload the list of collaborations, select the refresh icon next to the picker. To open the selected
collaboration’s details page in a new tab, select **View collaboration**.

## Review the activity table

Each row in the table is one analysis template run. The table shows the following columns:

| Column | Description |
| --- | --- |
| **ACTIVITY ID** | Unique identifier for the run. It’s also added as a query tag on the underlying query. |
| **RUNNER** | Alias of the collaborator that ran the analysis. |
| **TEMPLATE** | ID of the template used by the run. |
| **STARTED** | When the run began, shown as a relative time such as `2 hours ago`. |
| **DURATION** | How long the run took. |
| **STATUS** | **Success** or **Failed**. For what these mean for activation runs, see . |

Expand

Show lessSee more

The table is sorted by **STARTED**, newest first, until you change the sort order. Select any column
header except **ACTIVITY ID** to sort by that column. Sorting applies to all of the collaboration’s
activity, not just the rows currently loaded.

The table loads 50 runs at a time and loads more as you scroll. To fetch the latest activity, select the
refresh icon above the table.

## Filter and search

Use the controls above the table to narrow what’s shown. A count next to the filters tells you how many
runs match.

- **Status**: Limits the table to **All**, **Success**, or **Failed** runs.
- **Runner**: Limits the table to runs by one collaborator.
- **Template**: Limits the table to runs of one template.
- **Data offering**: Limits the table to runs that referenced one data offering.
- **Time range**: Limits the table to **Last 24 hours**, **Last 7 days**, **Last 30 days**, or
  **All time**.
- **Search runs**: Matches the activity ID, runner alias, and template ID. Matching isn’t
  case-sensitive and can occur anywhere in the value.

To reset everything at once, select **Clear all filters**.

Note

The time range defaults to **Last 30 days**. If a collaboration’s only activity is older than that, the
table reports that no activity matches your filters. Set **Time range** to **All time** to see that
activity.

## View the details of a run

Select a row to open a panel with the full record for that run. The panel header shows the activity ID, followed by the status and the elapsed time since the run started. If the
run failed, a banner at the top shows the error message.

The panel groups the record into the following sections:

- **Details**: The collaboration, analysis runner, start time, and duration. Select the collaboration
  name to open its details page in a new tab.
- **Inputs**: The template, data offerings, source tables, and local tables the run used.
- **Parameters**: The template arguments passed to the run, shown as JSON.
- **Activation**: For activation template runs, the destination collaborator and the segment that
  results were written to.
- **Query history**: How to find the run in your account’s query history, with a link to the details.
  This section appears only for runs that your own account ran.

To move through the runs in the table without closing the panel, use the previous and next arrows at
the bottom.

Note

A section or field appears only when there’s a value to show and your account is entitled to see that
value. For example, template arguments and local tables are visible only to the analysis runner who
submitted the run. A missing field can mean either that the run had no such value or that your role
can’t see it. For the fields visible to each role, see
[What activity is visible to you](/user-guide/cleanrooms/activity-history#label-dcr-collaboration-activity-history-personas).

## Access control

To view activity, you must use a role that was granted privileges by one of the following procedures:

- `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('VIEW ACTIVITY HISTORY', 'COLLABORATION', '{collaboration name}', '{role name}')`
- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE COLLABORATION', '{role name}')`
- `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('JOIN COLLABORATION', '{role name}')`

Only the collaborations that your currently selected role can access appear in the picker. To change
roles, use the role selector in your profile menu at the bottom left of Snowsight.

For more information, see [Managing access to collaborations, resources, and data](/user-guide/cleanrooms/manage-access).

## More information

See [Monitor analysis activity in collaborations](/user-guide/cleanrooms/activity-history) for more information on activity history, including:

- The fields that each role can see.
- The `VIEW_ACTIVITY_HISTORY` procedure and the columns it returns.
- How to correlate a run with your account’s query history.
- Limitations, including activation runs, free-form SQL, and older collaborations.
