# Use listings as a provider

Becoming a listing provider allows you to offer listings to consumers privately or on the Snowflake Marketplace. Being a Snowflake listing provider
makes it easier to manage sharing from your account to other Snowflake accounts.

When you share data as a provider, you can do the following:

- Monitor usage of the listings and associated data shares and products. See [Monitor listing use](/collaboration/provider-listings-monitor-studio).
- Create one or more provider profiles to manage your professional presence with consumers.
  See [Set up a provider profile](#label-creating-provider-profile-marketplace).
- Charge consumers for access to listings within Snowflake. See [Set up Stripe to get paid for listings](#label-set-up-stripe-listings).

Every private paid listing can have a price per consumer. If the trial and purchase price
for a listing differ, Snowflake recommends changing the price of the existing listing
so the consumer doesn’t need to reinstall the listing.
To learn more about listing monetization, see [Paid listings pricing models](/collaboration/provider-listings-pricing-model).

## Requirements to become a provider

To offer listings to consumers privately or on the Snowflake Marketplace, you must meet the following requirements:

- You must use a full Snowflake account. Trial accounts can share data with specified consumers, but not on the Snowflake Marketplace.
- You must not be using a Reader Account.
- You must have the ACCOUNTADMIN role or be assigned a role with provider privileges.
  See [Privileges required for working with listings](#label-permissions-required-for-working-with-listings-and-shares).
- You must meet the [Legal requirements for providers and consumers of listings](/collaboration/collaboration-listings-legal). See [Review and accept the Snowflake Provider and Consumer Terms](#label-accept-provider-tos-marketplace) for instructions.
- If your account is in a U.S. government region, you must also accept the cross-region disclaimer. See [Prepare to provide listings from accounts in U.S. government regions](/collaboration/provider-listings-government-providers#label-listings-setup-gov-provider).

To offer specific types of listings, you must also do the following:

- To offer paid listings or any listings on the Snowflake Marketplace, you must create a provider profile.
  See [Set up a provider profile](#label-creating-provider-profile-marketplace).
- To offer paid listings, you must configure your account to get paid for listings. See [Set up Stripe to get paid for listings](#label-set-up-stripe-listings) on this page.
- To list a Connected Application on the Snowflake Marketplace, complete the [Connected Application listing enablement steps](/collaboration/guidelines-reqs-for-listing-apps#label-connected-apps-pre-enablement) before you create a listing. See also [Connected Applications guidelines](/collaboration/guidelines-reqs-for-listing-apps#label-guidelines-reqs-connected-apps).

### Privileges required for working with listings

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

### Review and accept the Snowflake Provider and Consumer Terms

Before you can become a Snowflake Marketplace provider, an organization administrator (ORGADMIN) needs to
review and accept the combined Snowflake Provider and Consumer Terms.

Note

You do not need to accept the Snowflake Provider and Consumer Terms if you’re only creating free private listings and you’ve accepted the [Snowflake Customer-Controlled Data Sharing Functionality Terms](https://www.snowflake.com/legal/data-sharing-terms/).

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Admin** » **Terms**.
3. In the **Snowflake Marketplace** section, review the Snowflake Provider and Consumer Terms of service.
4. If you agree to the terms, select **Accept Terms & Conditions**.

Note

If you see an error, your user profile might be missing some contact information. If you have an administrator role, see
[Add user details to your user profile](/user-guide/ui-snowsight-profile#label-user-details-and-preferences) to update your profile using Snowsight. Otherwise, contact an
account administrator to update your user details.

See [Legal requirements for providers and consumers of listings](/collaboration/collaboration-listings-legal) for more details.

## Set up a provider profile

To offer listings to consumers privately, or on the Snowflake Marketplace, set up a provider profile in [Provider Studio](https://app.snowflake.com/#/provider-studio).
You do not need a provider profile to offer free private listings.

You only need to create a provider profile one time. You can create multiple provider profiles for one account.

Before you can create a provider profile, someone in your Snowflake account must review and accept the Snowflake Provider and Consumer Terms. Acceptance of the Snowflake Provider and Consumer Terms is not required when creating free private listings if you’ve accepted the [Snowflake Customer-Controlled Data Sharing Functionality Terms](https://www.snowflake.com/legal/data-sharing-terms/). For more information about the Snowflake Provider and Consumer Terms, see [Review and accept the Snowflake Provider and Consumer Terms](#label-accept-provider-tos-marketplace).

Note

You must use a role that has been granted the MODIFY privilege on the profile. For more information, see [Granting provider privileges to other roles in the Snowflake Marketplace or a Data Exchange](/user-guide/data-exchange-marketplace-privileges#label-granting-provider-privileges-to-other-roles).

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Provider Studio**.
3. In **Provider Studio**, select **Profiles**.
4. Select **+ Create profile** to create a profile. A dialog box appears.
5. In the **Create Profiles** dialog box, complete the fields. All fields are required. For a description
   of the fields, see [Provider profile fields](/collaboration/provider-profiles-managing#label-configuring-metadata-for-provider-profile).
6. Select **Next**, then verify that your profile details are correct.
7. Select **Submit for Approval**, or click **Save Draft** if you want to review your profile details
   before submitting it for approval.

Your provider profile must be approved before you can offer paid listings or marketplace listings. For your profile to be approved,
Snowflake verifies the following:

- You have reviewed and accepted the Snowflake Provider and Consumer Terms. Acceptance of the Snowflake Provider and Consumer Terms is not required when creating free private listings, but you must review and accept the [Snowflake Customer-Controlled Data Sharing Functionality Terms](https://www.snowflake.com/legal/data-sharing-terms/).
- Your profile abides by the Snowflake [Provider Policies](https://www.snowflake.com/provider-policies/).

See [Legal requirements for providers and consumers of listings](/collaboration/collaboration-listings-legal).

## Provide paid listings

To publish paid listings to consumers privately or on the Snowflake Marketplace, do the following:

1. Make sure that your account is eligible to provide paid listings. See [Who can provide paid listings](#label-monetization-provider-region-support).
2. Before creating a paid listing that you want to publish on the Snowflake Marketplace, contact your business development partner at Snowflake.
   If you do not have a business development partner, [submit a case with Marketplace Operations](https://snowforce.my.site.com/s/provider-onboarding-case). This step is required for listing
   approval.
3. Set up a payout method to get paid for listings. See [Set up Stripe to get paid for listings](#label-set-up-stripe-listings).

Note

If you are a commercial reseller (VAR) that wants to offer paid listings, use this form to [submit a case with Marketplace Operations](https://snowforce.my.site.com/s/provider-onboarding-case).
You only need to file one case to cover both purchasing and offering listings.

### Who can provide paid listings

As a provider, you can create paid listings if the billing address on your account is in one of the following countries:

- Australia
- Canada
- Colombia
- Finland
- France
- Germany
- Ireland
- Israel
- Italy
- Japan
- Kingdom of Saudi Arabia
- Mexico
- Netherlands
- New Zealand
- Norway
- Singapore
- Sweden
- Switzerland
- United Kingdom
- United States

See [Confirm your billing location is supported](/collaboration/consumer-listings-paying#label-monetization-consumer-region-support) for information on region availability for consumers.

### Set up Stripe to get paid for listings

Snowflake Marketplace uses Stripe to process Provider payouts. To receive payouts, Providers must create a Stripe Express
connected account as their payout method through Snowflake Marketplace. If eligible, Providers can reuse verified business information
from an existing Stripe account instead of completing verification again. To do so, the email address associated with your
Snowflake user must match your Stripe sign-in email, and you must be an Administrator or Super Administrator of the existing Stripe account.

There is no additional cost to Providers for using the Stripe connected account. As part of the setup process,
Providers must accept the [Stripe Connected Account Agreement](https://stripe.com/legal/connect-account).
This agreement is between the Provider and Stripe; Snowflake is not a party to it.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Admin** » **Billing**.
3. Click the **Marketplace billing** tab.
4. Click **Provider billing** tab.
5. Click **Activate account**.
6. In the **Provider payouts** section, click **Activate**.
7. Complete the required information to create and set up your Stripe account. You get payouts in the official currency of the country as
   specified in your Snowflake billing entity. To get payouts in USD, your Snowflake billing address must be in the United States. For
   more information, see
   [Supported accounts and settlement currencies](https://stripe.com/docs/payouts?account-country=TR#supported-accounts-and-settlement-currencies)
   in the Stripe documentation.

After you set up your Stripe account and provide a payout method, the **Provider payouts** section of the **Marketplace billing** page reports the current status of the method.
The following table describes the different statuses:

| Status | Description |
| --- | --- |
| Pending verification | Stripe is in the process of verifying your payout method. |
| Completed & verified | Your payout method has been verified by Stripe. If you have already accepted the Marketplace terms, you are ready to sell products and collect payments. |
| Manage Payout account | There is an issue with your Stripe account. The Snowsight interface provides additional details about the exact issue and how to resolve the problem. |
| Rejected | Stripe has rejected your payout method. A valid payout method must be provided. |

Expand

Show lessSee more

If you encounter issues with setting up Stripe or receiving payments, [contact Snowflake Support](/user-guide/contacting-support).

## Respond to access requests as an administrator

If you’re an account administrator or a database owner, you can provide access to requesting roles.
You receive an email about the type of request, whether it’s an installation or usage request.
For each request, you receive specific instructions on how to proceed and fulfill the access request effectively.
See [Use listings as a consumer](/collaboration/consumer-becoming) for more information.

## The Snowflake Marketplace Capacity Drawdown program

The Snowflake Marketplace Capacity Drawdown (MCD) program allows Snowflake consumers to use a percentage of their Snowflake Capacity commitment
as an additional payment method for Snowflake Marketplace [paid listings](/collaboration/consumer-listings-paying).

The MCD program is now generally available to all US-based consumers purchasing from US-based providers (excluding Florida for both
providers and consumers). The MCD program is also available as Private Preview in the United Kingdom, Switzerland, and Mexico.

Eligible providers using on-platform monetization, such as paid listings, who are not outside the US or who are using a Florida address for billing or shipping can accept MCD program payments. For more information about paid listings, see [Paid listings pricing models](/collaboration/provider-listings-pricing-model). See [Pay for Snowflake Marketplace listings](/collaboration/consumer-listings-paying) to learn more about how consumers pay for listings.

The following consumers are excluded from enrollment in the MCD Program:

- Consumers purchasing Snowflake through a reseller
- Priority Support consumers

To enroll in the MCD program, consumers can opt-in by submitting an MCD program order form at the start of a new contract, when they renew a contract, or when they amend an existing MCD program contract. To enroll in the MCD program, consumers must agree to the [Marketplace Capacity Drawdown Program Terms](https://www.snowflake.com/legal/snowflake-marketplace-capacity-drawdown-terms/) and the [Provider and Consumer Terms](https://www.snowflake.com/legal/snowflake-provider-and-consumer-terms/).

A consumer can apply an unused MCD program balance to their service consumption payment. Any invoice that *exceeds* the consumer’s MCD program balance must be paid in
full using other payment methods such as a credit card, ACH transfer, wire transfer or a SWIFT transfer. The consumer’s MCD program balance is applied first and then one of their alternate listed payment methods is used to pay any remaining balance.

Every private paid listing can have a price per consumer. If the trial and purchase price for a listing differ, Snowflake recommends that you change the price of the existing listing so that the consumer doesn’t need to reinstall the listing. For more information about listing monetization, see [Paid listings pricing models](/collaboration/provider-listings-pricing-model).
