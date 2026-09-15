# Manage the request approval workflow

The request approval workflow allows consumers to request access to Internal Marketplace organizational listings. This workflow reduces the time providers need to spend managing organizational listing access, and it provides consumers with quicker access to critical organizational listings.

When setting up the request approval workflow, providers can choose to manage organizational listing access requests within Snowsight, or they can provide an email or a URL that consumers can use to request access to an organizational listing. Allowing consumers to manage their organizational listing access requests within Snowsight simplifies the request process and makes sure organizational listing access requests are processed quickly.

All request approval workflow tasks are completed in Snowsight. As the functionality matures, programmatic options for managing the request approval workflow will become available.

The request approval workflow cannot be used to grant access to roles and users.

## Create a new organizational listing with a request approval workflow

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Data sharing** » **Internal sharing**.
3. Select **+ Create Listing**.
4. Select a data product such as a table, view, or other data product to add to the listing.

   1. Review the generated share identifier, then select **Generate listing**.
5. Select **+ Access control**.
6. Complete the **Grant access** section:

   > | Field | Description |
   > | --- | --- |
   > | **Who can access this data product?** | Select one of the following:  - **Entire organization**: Anyone in the organization can access the listing. If **Entire organization** is selected and [cross-cloud auto-fulfillment](http://other-docs.snowflake.com/en/collaboration/provider-listings-auto-fulfillment) is enabled on your account, then you’ll be prompted to review the auto-fulfillment refresh settings for the listing.  - **Selected accounts and roles**: Only selected accounts and roles can access. - **No accounts or roles are pre-approved**: (Default) Data product will only be available by request. |
   > | **Accounts** | If **Selected accounts and roles** is selected, select one or more accounts.  Optional. Select **+ Add another account** to add second and subsequent accounts.  By default, all roles in the selected accounts can access the listing. Select **Selected roles** to grant access only to specific roles each selected account. |
   >
   > Expand
   >
   > Show lessSee more
7. Complete the **Allow discovery** section:

   > | Field | Description |
   > | --- | --- |
   > | **Who else can discover the listing and request access?** | Select one of the following:  - **Entire organization**: (Default) Anyone in the organization can discover the listing and request access. - **Selected accounts and roles**: Only selected accounts and roles can discover the listing and request access. - **Not discoverable by users without access**: Only users with access can discover the listing. |
   > | **Accounts** | If **Selected accounts and roles** is selected, select one or more accounts.  Optional. Select **+ Add another account** to add additional accounts. |
   > | **Selected user roles** | If **Selected roles** is selected, enter one or more roles to grant access. |
   >
   > Expand
   >
   > Show lessSee more
8. Select **Set up request approval flow** and then select one of the following options in the **How should the request approval happen** list:

   - **Manage requests in Snowflake**: Consumers submit, review, and manage organizational listing access in Snowsight. Go to step 10.
   - **Manage requests outside of Snowflake**: Consumers request organizational listing access using the email address or URL you provide. Go to step 11.
9. If you selected **Manage requests in Snowflake**:

   1. In the **Approver email for notifications** field, enter the email address for organizational listing access submissions.
   2. Optional. To add additional organizational listing approvers, select **Add Role** and then select a role.
   3. Select **Done**.
10. If you selected **Manage requests outside of Snowflake**:
11. In the **Approver contact** field, enter the email address or a URL for organizational listing access submissions.
12. Select **Done**.
13. Select **Save**.
14. Add an organizational listing title:
15. Select **Untitled listing**.
16. In the **Listing title** field, enter a descriptive title for your organizational listing.
17. Select **Save**.
18. Optional. Add supporting documentation, terms and conditions, and attributes.
19. Select **Publish** to make the listing available in the **Internal Marketplace**.

If you exit without publishing, the listing is saved as a draft.

## Set up the request approval workflow in an existing organizational listing

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Data sharing** » **Internal sharing**.
3. On the **Listings** tab, select the listing you want to edit.
4. Select **Edit** in the **Approver Contact** area.
5. Select one of the following options in the **How should the request approval happen** list:

   - **Manage requests in Snowflake**: Consumers submit, review, and manage organizational listing access in Snowsight. Go to step 7.
   - **Manage requests outside of Snowflake**: Consumers request organizational listing access using the email address or URL you provide. Go to step 8.
6. If you selected **Manage requests in Snowflake**:

   1. In the **Approver email for notifications** field, enter the email address for organizational listing access submissions.
   2. Optional. Select **Add Role** to add additional organizational listing approvers.
   3. Select **Done**.
7. If you selected **Manage requests outside of Snowflake**:

   1. In the **Approver contact** field, enter the email address or a URL for organizational listing access submissions.
   2. Select **Done**.

## Respond to an organizational listing access request

As a provider, requests for organizational listing access are sent to the email address you specified when you set up the request approval workflow for an organizational listing.

Note

To approve an organizational listing access request, you need access to the Snowflake account the request originated from, and a role that owns or can modify the organizational listing. If you don’t meet these requirements, the **Review Request** control within the request email is inoperative.

1. Open your email application, then locate and open the organizational listing access request.
2. Review the request details.
3. Select **Review Request**.

   The Internal Requests page in Snowsight opens.
4. Select the organizational listing request that matches the organizational listing the consumer requested in their email.
5. Review the details of the organizational listing access request.
6. Optional. To grant organizational listing access to a role different from what the consumer specified, select **Give access to a different role from requested**, and then select or enter a new role name in the **Change requested role to** field.

   The options available for the **Change requested role to** field are determined by the consumer account where the request originated.

   If the consumer’s organizational listing request and the organizational listing originate from the same account as the provider, a list of autopopulated roles is available. If the consumer’s organizational listing request and the organizational listing originate from a different account than the provider, the role name must be entered manually.

   Manually entered role names must be an exact match to the roles defined in Snowsight. Only a single role can be entered.

   Only roles with OWNERSHIP or MODIFY privileges on the organizational listing can approve organizational listing access requests. To increase the number of organizational listing access approvers, grant them the MODIFY privilege on the organizational listing.
7. Optional. Enter comments explaining your reasoning for granting or denying the organizational listing access request.
8. Select one of the following options:

   - Select **Deny request** to deny the organizational listing access request. An email is sent to the consumer indicating organizational listing access was denied.
   - Select **Grant request** to grant the organizational listing access request. An email is sent to the consumer indicating organizational listing access was granted.

## View the Snowsight Internal Requests page

As a provider, you can use the **Internal Request** page in Snowsight to grant, deny, and review previous organizational listing access requests.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Provider Studio**.
3. Select the **Requests** tab.
4. Optional. Select the **Needs review** tab, select an organizational listing access request, and then grant or deny the request.
5. Optional. Select the **Resolved requests** tab, select a previous organizational listing access request, and then review the request details. You can use the **Status** list to filter previous organizational listing requests by their status.

## Request access to an organizational listing

As a consumer, you can quickly request access to an organizational listing that you want to access in the Internal Marketplace.

Note

To request access to an organizational listing, your Snowsight user profile must be complete and include a valid email address. See [Manage your user settings in Snowsight](/user-guide/ui-snowsight-profile).

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Catalog** » **Internal Marketplace**.
3. Search for an organizational listing and then select it.
4. Select **Request access**.
5. Select the role you are using to access the organizational listing.
6. Enter the reason why you’re requesting access to the organizational listing in the **Reason for access** field.
7. Select **Submit request**.
8. Select **Submit request** to close the **Request sent** dialog.

## View the status of an organizational listing access request

As a consumer, you can check the status of an active organizational listing access request at any time. You can also review when and why a previous organizational listing access request was denied.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Catalog** » **Internal Marketplace**.
3. Search for the organizational listing you’re waiting to access and then select it.
4. Select **View request** or **View previous request** if previous access was denied.
5. Review the details of your organizational listing access request.
6. Select **Close**.

## Access an approved organizational listing

As a consumer, a notification that your organizational listing access request was approved or denied is sent to the email address specified in your Snowsight user profile.

1. Open your email application and then locate and open the organizational listing access request.
2. Review the request details.
3. Select **Review Request**.

   The landing page for the organizational listing opens in Snowsight.
4. Select **Query in worksheet** to access the organizational listing.
5. Optional. To request access to an approved organizational listing for a different role, select a different role, and then select **Request access**.

## Withdraw an organizational listing access request

As a consumer, you can cancel an organizational listing access when it’s no longer required, or you need to update the access request information.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Catalog** » **Internal Marketplace**.
3. Search for the organizational listing access request you want to cancel and then select it.
4. Select **Withdraw request**.
5. Select **Confirm**.

## Specify the request approval type programmatically

You can specify the request approval type programmatically using the `request_approval_type` parameter.

`request_approval_type` (Optional)
:   You must specify one of the following with `request_approval_type` to define whether the request and approval will happen inside or outside of Snowflake:

    - `REQUEST_AND_APPROVE_IN_SNOWFLAKE`: Consumers submit, review, and manage organizational listing access in Snowsight.
    - `REQUEST_AND_APPROVE_OUTSIDE_SNOWFLAKE`: Consumers request organizational listing access using the email address or URL you provide.

    The following is an example of the format:

    Copy code

    ```
    . . .
    request_approval_type: "REQUEST_AND_APPROVE_IN_SNOWFLAKE"
    . . .
    ```
