# Review and join a collaboration in Snowsight

Feature — Generally Available

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

Collaborations that require review before joining appear in the **Ready to review** section of
the **Invited** tab. Reviewing prepares the collaboration in your account so that you can inspect
its full contents before committing to join: which data offerings and templates other collaborators
are sharing, and which resources are being requested from you. Joining shares any resources
requested from you, so review first if you want to see what you’re agreeing to.

To review a collaboration:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Data sharing** » **Data clean rooms**.
3. Select the **Invited** tab.
4. In the **Ready to review** section, select **Review** on the collaboration card. You can also
   select the card to open its details page and then select **Review** in the page header.
5. In the **Review Collaboration** dialog, enter a **Collaboration name**. This is the name for
   the collaboration in your own account, and it can differ from the name the owner chose.

   Important

   The collaboration name can’t be edited after this step, so pick something meaningful for your
   use case.
6. Select **Next** to submit the review request.

Preparing the collaboration usually takes a few minutes, and you can close the dialog while it
finishes. When the collaboration is ready for review, open its details page to inspect the
collaborators, templates, data offerings, and specification that the owner shared.

Note

For a cross-cloud or cross-region collaboration, you can’t start a review until the data
finishes replicating to your region. The dialog reports that replication is in progress. Select
**Refresh** to check again. For details on replication frequency and latency, see
[Managing Cross-Cloud Auto-Fulfillment in Collaboration Data Clean Rooms](/user-guide/cleanrooms/laf).

## Join a collaboration

Collaborations that are ready to join appear in the **Ready to join** section of the **Invited**
tab. Collaborations that you’ve already reviewed also appear here.

To join a collaboration:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Data sharing** » **Data clean rooms**.
3. Select the **Invited** tab.
4. Select **Join** on the collaboration card, or select the card to open its details page and
   then select **Join** in the page header.
5. Review the collaboration details, then in the **Join collaboration** dialog select
   **Confirm**.

   By selecting **Confirm**, you acknowledge that you’ve reviewed the collaboration details and
   approve your role and resources being shared with this collaboration.

Joining runs in the background and might take a few minutes. When it finishes, the collaboration
moves from your **Invited** tab to your **Joined** tab, and the full
[details page](/user-guide/cleanrooms/collab-ui-details) becomes available.

## What you can see before joining

Until you join, the **Templates** and **Data Offerings** tabs list what the collaboration
specification defines rather than live details, and you can’t act on the items they list. After you
join, the tabs show live details, and the actions to share templates and data offerings and to run
analysis become available. The **Update Requests** tab appears only after you join.

If a review or join fails, the collaboration shows a failure status and the details page explains
what went wrong. For more information, see
[Snowsight UI troubleshooting](/user-guide/cleanrooms/v2/troubleshooting#label-dcr-troubleshooting-snowsight).
