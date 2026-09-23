# Edit a collaboration in Snowsight

Feature — Generally Available

Currently available in [these regions](/user-guide/cleanrooms/installing-dcr#label-dcr-supported-regions).

Not available in government and VPS deployments.

After you join a collaboration, you can edit it in Snowsight by sharing
templates, linking data offerings, approving template requests, and leaving or
tearing down the collaboration.

Note

Templates and data offerings must be registered in a
[registry](/user-guide/cleanrooms/registries) before they can be shared in a
collaboration. You can register them using the
[Collaboration API](/user-guide/cleanrooms/collaboration-api-reference) or
Cortex Code.

## Share a template

You can share registered templates from your account with other collaborators in
the collaboration. When you share a template, all affected collaborators
(analysis runners and data providers) must approve it before it becomes available.

To share a template:

1. Navigate to the [collaboration details page](/user-guide/cleanrooms/collab-ui-details#label-dcr-collab-ui-details).
2. Select the **Templates** tab.
3. Select **Share Template**.
4. In the dialog, select a **Template ID** from the list of registered templates in
   your account.
5. Select one or more collaborators (analysis runners) to share the template with.
6. Select **Submit Request**.

The template appears in the **Update Requests** tab with a status of **Pending**
until all required collaborators approve it.

### Share with additional collaborators

To share an existing template with additional collaborators:

1. On the **Templates** tab, select the actions menu ([![More options](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png)) on the
   template row.
2. Select **Share with collaborators**.
3. Select new collaborators to share the template with.
4. Select **Submit Request**.

### Remove collaborators from a shared template

To remove collaborators from a shared template:

1. On the **Templates** tab, select the actions menu ([![More options](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png)) on the
   template row.
2. Select **Remove collaborators**.
3. Select the collaborators to remove.
4. Select **Submit**.

## Approve or reject template requests

When a collaborator shares a new template, the request appears on the
**Update Requests** tab for all affected parties. Each collaborator who needs to
approve the template sees the request with a **Pending** status.

To approve or reject a template request:

1. Navigate to the [collaboration details page](/user-guide/cleanrooms/collab-ui-details#label-dcr-collab-ui-details).
2. Select the **Update Requests** tab.
3. Select a template request to view its details and the approval log.
4. Select **Approve** or **Reject**.
   - If you select **Reject**, provide a reason for the rejection.

After all required collaborators approve a template request, the template becomes available
for use by the designated analysis runners. If any collaborator rejects the request, the
template is not made available.

### Auto-approval

You can enable auto-approval for template requests so that your account automatically
approves new templates without manual intervention. To toggle auto-approval, use the
auto-approval setting on the [collaboration details page](/user-guide/cleanrooms/collab-ui-details#label-dcr-collab-ui-details).

## Share a data offering

If you are a data provider in the collaboration, you can share registered data offerings
from your account to make them available to analysis runners.

Note

You can share a data offering only with the role that you used to join the collaboration. If you
select a different role, the dialog tells you to switch to the role used to join.

To link a data offering:

1. Navigate to the [collaboration details page](/user-guide/cleanrooms/collab-ui-details#label-dcr-collab-ui-details).
2. Select the **Data Offerings** tab.
3. Select **Share Data Offering**.
4. In the dialog, select the **Registry** that holds the data offering. Select **Default**
   for the default account registry.
5. Select a **Data Offering ID** from the list of registered data offerings in your
   account.
6. Select the collaborators (analysis runners) who should have access to the data
   offering.
7. Select the role that you used to join the collaboration.
8. Select **Submit Request**.

The request appears on the **Update Requests** tab with a status of **Pending**. Monitor the request until its status
changes to **Completed**, which indicates that the data offering is available to the selected analysis runners.

### Unlink a data offering

To remove a data offering from the collaboration:

1. On the **Data Offerings** tab, select the actions menu ([![More options](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png)) on the
   data offering row.
2. Select **Unlink**.
3. Confirm the removal.

## Leave a collaboration

To leave a collaboration that you have joined:

1. On the [collaborations listing](/user-guide/cleanrooms/collab-ui-listing#label-dcr-collab-ui-listing), find the
   collaboration card.
2. Select the actions menu ([![More options](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png)) on the collaboration card. You can also select
   **Leave** in the header of the [collaboration details page](/user-guide/cleanrooms/collab-ui-details#label-dcr-collab-ui-details).
3. Select **Leave**.
4. In the confirmation dialog, select **Yes, leave** to confirm.

Warning

Leaving a collaboration is irreversible. You can’t rejoin a collaboration after you leave it.

While the operation runs, the collaboration shows a **Leaving** status. When it finishes, the
collaboration shows **Pending cleanup**. Select **Remove** on the collaboration card to remove it
from your account.

If your role doesn’t have permission to leave collaborations, the action is disabled and a tooltip
explains why. The action is also unavailable for some statuses, such as a collaboration that’s
already in **Leaving** status.

## Tear down a collaboration

If you’re the collaboration owner, you can tear down (delete) the collaboration.
Tearing down a collaboration removes it for all collaborators.

To tear down a collaboration:

1. On the [collaborations listing](/user-guide/cleanrooms/collab-ui-listing#label-dcr-collab-ui-listing), find the
   collaboration card.
2. Select the actions menu ([![More options](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png)) on the collaboration card. You can also select
   **Teardown** in the header of the [collaboration details page](/user-guide/cleanrooms/collab-ui-details#label-dcr-collab-ui-details).
3. Select **Teardown**.
4. In the confirmation dialog, select **Yes, teardown** to confirm.

While the operation runs, the collaboration shows **Teardown in progress**. When it finishes, the
collaboration shows **Pending cleanup**. Select **Remove** on the collaboration card to remove it
from your account.

Tearing down a collaboration doesn’t finish the cleanup in the other collaborators’ accounts. Every
other collaborator sees the collaboration change to **Pending cleanup** and must select **Remove**
to remove the clean room application and collaboration metadata from their own account.

Warning

Tearing down a collaboration is irreversible. All collaborators lose access to the
collaboration, and any data shared through the collaboration is no longer accessible.
