# View collaboration details in Snowsight

[Preview Feature](/release-notes/preview-features) — Open

Currently available in [these regions](/user-guide/cleanrooms/installing-dcr#label-dcr-supported-regions).

Not available in government and VPS deployments.

The collaboration details page shows comprehensive information about a single collaboration,
including collaborators, templates, data offerings, and update requests. You can access the
details page by selecting a collaboration from the
[collaborations listing](/user-guide/cleanrooms/collab-ui-listing#label-dcr-collab-ui-listing).

To use Cortex Code to get an AI-generated explanation of a collaboration, select the
**Explain** button in the page header. Cortex Code opens and provides a summary of the
collaboration, including its collaborators, templates, data offerings, and status.

## Collaboration overview

The overview section at the top of the details page displays the following information:

- **Name**: The collaboration name.
- **My alias**: Your account’s alias in this collaboration.
- **Description**: The collaboration description.
- **Last updated**: The timestamp of the last update to the collaboration.

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

### **Shared by you** tab

The **Shared by you** tab shows the templates and data offerings that you have shared
into this collaboration. This tab has two sections:

**Templates you shared**

A table of templates that your account has shared with other collaborators. For each
template, you can see:

- The template ID.
- Which collaborators the template is shared with.
- The current approval status.

To share a new template, select **Share Template**. For more information, see
[Share a template](/user-guide/cleanrooms/collab-ui-manage#label-dcr-collab-ui-share-template).

To share an existing template with additional collaborators, or to remove collaborators from
a shared template, select the actions menu ([![More options](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png)) on the template row.

**Data offerings you shared**

A table of data offerings that your account has linked to this collaboration. For each
data offering, you can see:

- The data offering ID.
- Which collaborators have access.

To share a new data offering, select **Share Data Offering**. For more information, see
[Share a data offering](/user-guide/cleanrooms/collab-ui-manage#label-dcr-collab-ui-link-do).

### **Shared with you** tab

The **Shared with you** tab shows templates and data offerings available for you to
use in analysis. This tab has two sections:

**Available Templates to Run**

A list of analysis templates available to you, organized by analysis runner. Select a
template to view its details, including:

- The template SQL logic.
- Template parameters and their descriptions.
- Which collaborators provided the template.

From the template details, you can:

- Select **Open in Workspaces** to generate a pre-configured run analysis SQL statement
  and open it in a Snowflake workspace.
- Select **Run** to use Cortex Code to generate a run analysis specification
  tailored to the template and collaboration context.

For more information, see [Run analysis and activation in Snowsight](/user-guide/cleanrooms/collab-ui-run-analysis).

**Available data offerings**

A list of data offerings available for use in your analysis templates, including:

- The data offering ID.
- Which collaborator provided the data offering.

Select a data offering to view its details, including the view name, join columns, and
allowed columns.

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

### **Collaboration Spec** tab

The **Collaboration Spec** tab displays the raw YAML specification of the collaboration.
This is the same specification used by the Collaboration API and provides a complete,
machine-readable representation of the collaboration configuration.
