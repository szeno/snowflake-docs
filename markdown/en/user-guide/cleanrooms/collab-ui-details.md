# View collaboration details in Snowsight

Feature — Generally Available

Currently available in [these regions](/user-guide/cleanrooms/installing-dcr#label-dcr-supported-regions).

Not available in government and VPS deployments.

The collaboration details page shows comprehensive information about a single collaboration,
including collaborators, templates, data offerings, and update requests. You can access the
details page by selecting a collaboration from the
[collaborations listing](/user-guide/cleanrooms/collab-ui-listing#label-dcr-collab-ui-listing).

The details page is available for collaborations you’ve joined and for collaborations you’ve been
invited to, though an invited collaboration shows preliminary information until you review and
join it. You can’t open the details page while a collaboration is still being created. For more
information, see [What you can see before joining](/user-guide/cleanrooms/collab-ui-join#label-dcr-collab-ui-join-before).

To use Cortex Code to get an AI-generated explanation of a collaboration, select the
**Explain** button in the page header. Cortex Code opens and provides a summary of the
collaboration, including its collaborators, templates, data offerings, and status.

## Collaboration overview

The overview section at the top of the details page displays the following information:

- **Name**: The collaboration name.
- **My alias**: Your account’s alias in this collaboration.
- **Description**: The collaboration description.
- **Last updated**: The time of the last update to the collaboration, shown as a relative time
  such as `2 hours ago`.

## Page actions

The actions available in the page header depend on the collaboration’s status and on your role
in it:

- **Review**: Submit a review request for a collaboration you’ve been invited to. For more
  information, see [Review and join a collaboration in Snowsight](/user-guide/cleanrooms/collab-ui-join).
- **Join**: Join a collaboration that is ready to join.
- **Leave**: Leave a collaboration you’ve joined. You can’t rejoin a collaboration after leaving
  it.
- **Teardown**: Tear down a collaboration that you own, which removes it for all collaborators.

If your role doesn’t have the required privilege for an action, the button is disabled and a
tooltip explains why.

For more information about leaving and tearing down collaborations, see
[Edit a collaboration in Snowsight](/user-guide/cleanrooms/collab-ui-manage).

## Status banners

When a collaboration needs your attention or an operation fails, the details page shows a banner
above the tabs. For a failed operation, select the banner action to open the error details. For
more information, see
[Snowsight UI troubleshooting](/user-guide/cleanrooms/v2/troubleshooting#label-dcr-troubleshooting-snowsight).

## Collaboration tabs

Below the overview, the details page provides the following tabs:

### **Collaborators** tab

The **Collaborators** tab shows a table of all collaborators in the collaboration with
the following information:

- **Collaborator name**: The collaborator’s alias.
- **Account identifier**: The Snowflake account identifier.
- **Roles**: The roles assigned to the collaborator (Owner, Data Provider, Analysis Runner).
- **Status**: The collaborator’s current status (Joined, Invited, Reviewing, and so on).

The current collaborator (you) is marked with a **You** badge. The collaboration owner
is marked with an **Owner** badge.

A collaborator can show a **Replicating** status, which means the collaboration data is still
replicating to that collaborator’s region. This happens with cross-cloud and cross-region
collaborations. Until replication finishes, that collaborator can’t review the collaboration. For
details on replication frequency and delays, see [Managing Cross-Cloud Auto-Fulfillment in Collaboration Data Clean Rooms](/user-guide/cleanrooms/laf).

### **Templates** tab

The **Templates** tab lists the analysis templates in the collaboration that concern your account:
templates you shared with other collaborators, templates shared with you, and templates that can be
run against a data offering you provided. The templates appear in a single table, where the
**Shared by** and **Shared with** columns show each template’s relationship to your account.

For each template, you can see:

- The template ID.
- Which collaborator shared it, and which collaborators it’s shared with.
- The current approval status.

To share a new template, select **Share Template**. For more information, see
[Share a template](/user-guide/cleanrooms/collab-ui-manage#label-dcr-collab-ui-share-template).

The actions available on a row depend on your relationship to that template:

- For a template you shared, select the actions menu ([![More options](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png)) on the row to share it
  with additional collaborators or to remove collaborators from it.
- For a template shared with you, select the row to view its details, including the template SQL
  logic and its parameters. From the details you can select **Open in Workspaces** to generate a
  pre-configured run analysis SQL statement, or **Run** to use Cortex Code to generate a run
  analysis specification. For more information, see
  [Run analysis and activation in Snowsight](/user-guide/cleanrooms/collab-ui-run-analysis).

### **Data Offerings** tab

The **Data Offerings** tab lists the data offerings in the collaboration that you shared or that
are shared with you, in a single table.

For each data offering, you can see:

- The data offering ID.
- Which collaborator shared it, and which collaborators have access.

To share a new data offering, select **Share Data Offering**. For more information, see
[Share a data offering](/user-guide/cleanrooms/collab-ui-manage#label-dcr-collab-ui-link-do).

The actions available on a row depend on your relationship to that data offering:

- For a data offering shared with you, select the row to view its details, including the view name,
  join columns, and allowed columns.

### **Update Requests** tab

The **Update Requests** tab shows template update requests that require approval
from collaborators. When a collaborator shares a new template, all affected parties
(analysis runners and data providers) must approve it before it becomes available.

For each update request, you can see:

- The template ID.
- The requesting collaborator.
- The current status (Pending, Approved, Rejected).

Select a template request to view its details and the approval log, which shows the
approval status for each collaborator. To approve or reject a request, select
**Approve** or **Reject**. For more information, see
[Approve or reject template requests](/user-guide/cleanrooms/collab-ui-manage#label-dcr-collab-ui-approve-templates).

If an update request fails, hover over its status badge to see the reason. The reason also appears
in a banner when you open the request details.

The **Update Requests** tab appears only after you join the collaboration, because there’s nothing
to approve or reject until then.

### **Collaboration Spec** tab

The **Collaboration Spec** tab displays the raw YAML specification of the collaboration.
This is the same specification used by the Collaboration API and provides a complete,
machine-readable representation of the collaboration configuration.
