# Review and join a collaboration in Snowsight

[Preview Feature](/release-notes/preview-features) — Open

Currently available in [these regions](/user-guide/cleanrooms/installing-dcr#label-dcr-supported-regions).

Not available in government and VPS deployments.

When another collaborator creates a collaboration and includes your account, the
collaboration appears on your **Invited** tab in the
[collaborations listing](/user-guide/cleanrooms/collab-ui-listing#label-dcr-collab-ui-listing). From there, you can
review the collaboration details and join when ready.

Note

To join a collaboration, your role must have the JOIN COLLABORATION privilege.
To review a collaboration without joining, your role must have the REVIEW COLLABORATION
privilege. You must use the same role to join the collaboration that you used to review it.
For more information, see [Managing access to collaborations, resources, and data](/user-guide/cleanrooms/manage-access).

## Review a collaboration

Collaborations that require review before joining appear in the **Ready to Review**
section of the **Invited** tab.

To review a collaboration:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Data sharing** » **Data clean rooms**.
3. Select the **Invited** tab.
4. In the **Ready to Review** section, select **Start Review** on the collaboration card.

The review flow lets you examine the collaboration details, including:

- The collaboration name, description, and owner.
- The list of collaborators and their assigned roles.
- The templates and data offerings included in the collaboration.

After reviewing, you can choose to proceed to joining the collaboration, or close
the review dialog and return later.

## Join a collaboration

Collaborations that are ready to join appear in the **Pending Join** section of the
**Invited** tab. Collaborations that you have already reviewed also appear here.

To join a collaboration:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Data sharing** » **Data clean rooms**.
3. Select the **Invited** tab.
4. Select **Join** on the collaboration card.
5. In the join wizard, complete the following steps:

### Step 1: Basic details

Configure your local settings for the collaboration:

- **Collaboration name**: A name for the collaboration in your account. This
  can be different from the collaboration name set by the owner.
- Review the collaboration description provided by the owner.

If the join wizard detects that your current role may not have the necessary privileges,
a validation banner appears with guidance on which role to use.

Select **Next** to proceed.

### Step 2: Review and join

Review the full collaboration details before joining. The review page shows a tabbed
view of the collaboration content, including collaborators, templates, data offerings,
and the raw specification.

To use Cortex Code to get an AI-generated explanation of the collaboration, or to help
decide whether to join, select **Explain** or **Help Decide**. Cortex Code
analyzes the collaboration and provides guidance.

When you’re satisfied, select **Join** to join the collaboration. After joining,
the collaboration moves from your **Invited** tab to your **Joined** tab, and
you can access its [details page](/user-guide/cleanrooms/collab-ui-details).
