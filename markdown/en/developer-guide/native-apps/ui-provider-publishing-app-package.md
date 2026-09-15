# Publish an app to consumers

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

After developing and testing the application package containing your app, you can
publish the app to consumers using
[listings](/collaboration/collaboration-listings-about).

As a provider, you add an application package as the data content of an listing. The consumer
installs the app in their account from the listing.

## Set up roles and privileges

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

## Prerequisites for publishing a listing for an application package

Before creating a listing for an application package, ensure that you have completed the following:

- Create and test your application package.

  Before publishing your application package, ensure that it is working correctly and that the roles and privileges
  are set properly.
- Become a Provider of Listings

  Becoming a provider of listings in Snowflake makes it easier to manage sharing apps from your account to
  other Snowflake accounts. For more information, see [Use listings as a provider](/collaboration/provider-becoming).

  Creating a provider profile is not required for private listings.

## Workflow for publishing an application package

To publish an application package:

1. Ensure that you have completed the [prerequisites](#label-nativeapps-provider-listings-prereqs) for publishing
   a listing for an application package.
2. [Set the default release directive](#label-nativeapps-provider-listings-default-rel-dir).
3. [Initiate the automated security scan](#label-nativeapps-provider-listings-set-distribution).
4. [Create a listing](#label-nativeapps-provider-listings-create).
5. (Optional) Add a pricing plan to get paid for your application.
6. [Submit your listing for approval](#label-nativeapps-provider-listings-submit-approval).

   You only need to approve listings published to the Snowflake Marketplace.
7. [Publish your listing](#label-nativeapps-provider-listings-publish).

## Set the default release directive

Before creating a listing for an application package, you must specify the default release directive that
points to the version or patch of the app you are publishing.

If you are using release channels to manage the versions of your app, you can set custom release directive for each release channel. You must set the default release directive on the default release channel.

For more information, see [Set the release directive using a release channel](/developer-guide/native-apps/release-channels#label-native-apps-relchan-release-directive)

If you are publishing your app using the legacy versioning method, you can set the default release directive on the application package. For more information, see
[Set the release directive for an app (Legacy)](/developer-guide/native-apps/update-app-release-directive)

## Initiate the automated security scan for an application package

To publish a listing for an application package to an account outside of your organization, your application package must pass an automated security scan.

The automated security scan is initiated when you set the DISTRIBUTION property of the application package to `EXTERNAL` or when you add a new version or patch to an application package that has the DISTRIBUTION property set to `EXTERNAL`. For more information, see
[Security requirements and guidelines for a Snowflake Native App](/developer-guide/native-apps/security-overview).

## Create a listing for an app

To share your app with consumers, create a listing and add the application package as the data product
of the listing.

### Create a private listing for an app

To publish your app to specific consumers, create a listing:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Provider Studio**.
3. Select **Create Listing**. The **Create Listing** window opens.
4. Enter a name for your listing.
5. In the **Who can discover the listing** section, select **Only specified consumers** to privately share the
   listing with specific accounts.
6. Click **+ Select** to select the application package to be in the listing.
7. Enter a description for your listing.
8. (Optional) If you have multiple provider profiles, select which provider profile to use to publish this listing.
9. In the **Add consumer accounts** section, add the account identifiers for the consumers with whom you want to
   share the listing.
10. If the consumer accounts are located in another region, set up auto-fulfillment:
11. Review the refresh frequency configured at the account level. If you need to use a different
    refresh frequency, see [Set the account-level refresh interval](/collaboration/provider-listings-auto-fulfillment-set-refresh-interval).
12. Optional: Select a warehouse to use to set up auto-fulfillment.
13. Select **Publish** to publish the listing to the selected consumers, or select **Save Draft**
    to save it as a draft.

To monetize your app, add a pricing plan.

### Create a listing for an app published to the Snowflake Marketplace

To publish your app on the Snowflake Marketplace, create a listing:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Provider Studio**.
3. Select **Create Listing**. The **Create Listing** window opens.
4. Enter a name for your listing.
5. In the **Who can discover the listing** section, select **Anyone on the Marketplace** to publish the listing on
   the Snowflake Marketplace.
6. In the **How will consumers access the data product?** section, select **Free** or **Paid**.
7. Select **Next**. A draft listing is created.

Before publishing your draft listing, you must configure additional required and optional capabilities.

#### Configure a Snowflake Marketplace listing for an application package

After you create a listing for the Snowflake Marketplace, you must configure additional information for your listing so that you can submit it for approval and publish it.

To configure a listing:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Provider Studio**.
3. Select the **Listings** tab, then select the draft listing you want to configure.
4. Select **Add** next to each section that appears on the page and provide the required information.

   As you provide information for each section, refer to
   [Configure listings](/collaboration/provider-listings-reference)
   for information on each field. The specific properties available to edit depend on the type of listing
   that you create.

   If you want to monetize your Snowflake Native App, add a pricing plan to get paid for your Snowflake Native App.

## Submit a listing for approval

Before you can publish a listing to the Snowflake Marketplace, you must submit the listing to Snowflake for
approval.

If you want to submit your listing for approval, but the option to **Submit for Approval** is disabled, check the
following:

- You completed the steps to configure the listing.
- You are the ACCOUNTADMIN or have the OWNERSHIP privilege for the data product attached to the listing.
- All sample SQL queries attached to the listing pass validation.

To submit a listing for approval:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Provider Studio**.
3. Select the **Listings** tab, then select the draft listing you want to submit for approval.
4. Select **Submit for Approval**.

   After the listing is reviewed by Snowflake, the state changes to **Approved** or **Denied**.

   If the listing has been denied, update the listing based on the feedback provided in comments, and resubmit it for approval.

   When a listing is approved or denied, an email notification is sent to both the Business Contact and Technical Contact email addresses
   in the provider profile associated with the listing.

## Publish a listing for an app

To publish an approved listing on the Snowflake Marketplace:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Provider Studio**.
3. Select the **Listings** tab, then select the listing you want to publish.
4. Select **Publish**.

After publishing your Snowflake Marketplace listing, you can define a
[referral link](/collaboration/provider-listings-referral-link)
to share a direct link to your listing with consumers.
