# Enable VPS collaboration with other organizations

VPS collaboration with private listings must be enabled through Snowflake
Support. First, however, your organization must agree to the terms and disclaimers.
After that, you can start working with support to setup participation in private listings.

## How to sign the terms and disclaimers

Before any Snowflake customer can begin to use any type of listings, their organization administrator
must accept some terms and disclaimers – this is required one time for the entire organization.
Signing waivers must be done through the Snowflake web app. For more information about Snowflake legal terms and conditions, see
[Legal requirements for providers and consumers of listings](https://other-docs.snowflake.com/en/collaboration/collaboration-listings-legal).

1. sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select your username, select **Primary Role**, and then scroll down and select **ORGADMIN**.
3. in the navigation menu, select **Admin** » **Terms**.
4. In the **Snowflake Marketplace** pane, click **View terms** for **Standard Agreement for Marketplace products**.
5. [Review and accept the Snowflake Provider and Consumer Terms](/collaboration/provider-becoming#label-accept-provider-tos-marketplace) and save a copy for your records.
6. To sign the terms, select **Review & Enable**.
7. Review the cross-region disclaimer and save a copy for your records.
8. Select **Acknowledge & Continue**.

Note

If you see an error, your user profile might be missing some contact information. If you have an administrator role, see
[Add user details to your user profile](/user-guide/ui-snowsight-profile#label-user-details-and-preferences) to update your profile using Snowsight. Otherwise, contact an
account administrator to update your user details.

## How to enable VPS collaboration

When ready to publish or obtain a private listing, both the provider and the
future consumer of the listing need to contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support) to authorize
the new connection with a specific organization.

## Privileges required

When you create a listing, you create it from the account that has the data or application package in it. The role that attaches a data
product to a listing and publishes the listing must be the same role that created, and therefore owns, the application package or share.
You cannot transfer the OWNERSHIP privilege for a share.

If you use a different role to create and manage the listing, grant the MODIFY privilege on the listing to the role
that owns the application package or share. For example:

Share or application package owner role:
:   OWNERSHIP privilege on the share or application package.
    MODIFY privilege on the listing.

Listing owner role:
:   OWNERSHIP privilege on the listing.

    Global CREATE LISTING privilege.

Within the provider account, you can use one of the following to create and manage listings:

ACCOUNTADMIN:
:   If you use the ACCOUNTADMIN role to create and manage listings, the ORGADMIN role must first
    [Delegate privileges to set up auto-fulfillment](/collaboration/provider-listings-auto-fulfillment-manage-privileges#label-delegate-laf-privileges).

Custom role:
:   If you use a custom role, the ORGADMIN role must first [Delegate privileges to set up auto-fulfillment](/collaboration/provider-listings-auto-fulfillment-manage-privileges#label-delegate-laf-privileges)
    to the ACCOUNTADMIN role, which can then be used to grant the relevant privileges to the custom role.

For more information about granting sharing privileges, see [Granting Privileges to Other Roles:](/user-guide/data-exchange-marketplace-privileges).

## How to disable VPS collaboration

If your organization no longer wants to offer or access private listings,
follow these steps:

**For consumers:**

1. [Delete all of the listings](/collaboration/provider-listings-removing#label-delete-a-listing) that you are a consumer of, consistent with the
   applicable requirements in the Provider and Consumer Terms.
2. Delete the data that you got through listings.
3. Contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support) to have collaboration disabled for your organization.

**For providers:**

1. [Delete all of the listings](/collaboration/provider-listings-removing#label-delete-a-listing) shared from your account, consistent with the applicable
   requirements in the Provider and Consumer Terms.
2. Contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support) to have collaboration disabled for your organization.

For more information, see [Removing listings as a provider](https://other-docs.snowflake.com/en/collaboration/provider-listings-removing).
