# Use listings as a consumer

To access listings shared privately or on the Snowflake Marketplace, become a Snowflake consumer. You can also access data shared
as part of direct shares or data exchanges, which offer more limited data sharing capabilities.

As a consumer of listings, you can do the following:

- Access data in listings shared from other cloud platforms and Snowflake regions.
- [Access data in a private listing](/collaboration/virtual-private-snowflake/vps-collaboration-for-consumers).
- Pay for listings inside Snowflake instead of negotiating billing with each listing provider.
- Get more information about data in a listing, such as example SQL queries.

To become a consumer of listings, you must meet the following requirements:

- Your organization must agree to the legal terms. See [Accept the Snowflake Provider and Consumer Terms](#label-collaboration-consumer-terms).
- Your account must be granted the relevant privileges for working with listings. See [Set up required privileges](#set-up-required-privileges).
- To consume paid listings, you must set up payment information and be eligible to pay for listings. See [Pay for Snowflake Marketplace listings](/collaboration/consumer-listings-paying#label-set-up-billing-consumer).
- If your account is located in a U.S. government region, a KSA region, or a
  VPS environment, you must also accept the cross-region disclaimer. See
  [Collaboration disclaimers for restricted regions](/collaboration/collaboration-disclaimers-restricted-regions).

For more information, see [Pay for Snowflake Marketplace listings](/collaboration/consumer-listings-paying#label-set-up-billing-consumer).

## Accept the Snowflake Provider and Consumer Terms

The organization administrator only needs to accept the Snowflake Provider and Consumer Terms once for your organization.
After the terms have been accepted, anyone in your organization that has a role with the necessary privileges can become a consumer of listings. For details about the terms of service, see [Legal requirements for providers and consumers of listings](/collaboration/collaboration-listings-legal).

Note

You must be an organization administrator (a user granted the ORGADMIN role) to accept the terms. You do not need to accept the Snowflake Provider and Consumer Terms if your organization intends to access only free listings, or the listing terms are offline. Custom or standard listing terms must be accepted in Snowsight.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Admin** » **Terms**.
3. In the **Snowflake Marketplace** section, next to Snowflake Provider and Consumer Terms, select **Review**.
4. If you agree to the terms, select the checkbox for **I accept Snowflake Provider and Consumer Terms**.
5. You can also accept additional terms to allow users in your organization to get listings that use the [Standard Agreement for Marketplace Products](https://www.snowflake.com/marketplace/standard-agreement/):

   1. Review the [Standard Agreement for Marketplace Products](https://www.snowflake.com/marketplace/standard-agreement/)
   2. Select **I authorize my organization’s user to accept Standard Agreement for Marketplace products**.
6. Select **Save** to accept to finalize the selection or **Cancel** to cancel.

## Set up required privileges

To access a listing, you must use the ACCOUNTADMIN role or another role with the CREATE DATABASE and IMPORT SHARE privileges.
To pay for a paid listing, your role must also have the PURCHASE DATA EXCHANGE LISTING privilege.

If you don’t have a role with these privileges, you can automatically request access from the account administrator when attempting to access a listing.

To gain access, you can ask your account administrator to do one of the following:

- Grant the CREATE DATABASE and IMPORT SHARE privileges to a role on your account so that you can get access to listings.
- Get a listing for your account, then grant the IMPORTED PRIVILEGES privilege on the database created from the listing to a role on
  your account. This lets you access the data in the listing without having access to get any listing on the Snowflake Marketplace or privately.
- Install the listing for you.

See [Assigning IMPORTED PRIVILEGES to other roles](/user-guide/data-share-consumers#label-assigning-imported-privileges-other-roles) for more details about the privileges associated with listings.

## Prepare to access listings from accounts in U.S. government regions

If your account is in a [U.S. government region](/user-guide/intro-regions#label-us-gov-regions) and you want to install data products offered privately or on the Snowflake Marketplace, or
offer listings either privately or on the Snowflake Marketplace, you must review and acknowledge the following cross-region disclaimer for your
organization.

Important

To get data products and share listings with Snowflake customers outside your region, Snowflake shares organization and account metadata
and usage analytics with the customers you collaborate with outside of your region.

Compliance standards, such as [FedRAMP](/user-guide/cert-fedramp), and support for different regulated workloads, such as [ITAR](/user-guide/cert-itar), might be different or unavailable
outside of your U.S. Government Region. Consider your compliance requirements before choosing to move or share data between Snowflake regions.

Note

You must use the ORGADMIN role to accept the terms. You only need to accept terms once for your Snowflake account. If you do not have
the ORGADMIN role, see [Enabling the ORGADMIN role in an account](https:/docs.snowflake.com/en/user-guide/organization-administrators#label-enabling-orgadmin-role-for-account).

1. sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. in the navigation menu, select **Admin** » **Terms**.
3. In the **Snowflake Marketplace** section, for **Sharing & Collaboration**, select **Review & Enable**.
4. Review the cross-region disclaimer and select **Acknowledge & Continue**.
5. Select **Done**.

Note

- Providers can enable [Egress Cost Optimizer (ECO)](/collaboration/provider-listings-auto-fulfillment-eco) in a primary account in any commercial region and create listings targeted to any other region, including government regions.
- By default, ECO is unavailable to customers on a government cloud. If you’re a Gov customer, you can reach out to your Snowflake account executive for more information about ECO enablement.

You must use the ORGADMIN role and you only need to complete this step once for your organization:

1. sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. in the navigation menu, select **Admin** » **Terms**.
3. In the **Snowflake Marketplace** section, for **Sharing & Collaboration**, select **Review & Enable**.
4. Review the cross-region disclaimer and select **Acknowledge & Continue**.
5. Select **Done**.

Note

If you see an error, your user profile might be missing some contact information. If you have an administrator role, see
[Add user details to your user profile](/user-guide/ui-snowsight-profile#label-user-details-and-preferences) to update your profile using Snowsight. Otherwise, contact an
account administrator to update your user details.

# Stop sharing and collaboration from an account in a US government region

If you no longer want to offer or access listings from your account in a US government region, do the following:

1. [Delete all of your listings](/collaboration/provider-listings-removing) shared from your account, consistent with the applicable
   requirements in the Provider and Consumer Terms.
2. Stop consuming listings by dropping the databases imported when you
   [accessed listings](/collaboration/consumer-listings-access).
3. [Contact Snowflake Support](/user-guide/contacting-support) to have data sharing and collaboration disabled for your organization.

The types of listings and data products that you can access are limited. See [Limitations for accessing listings from accounts in U.S. government regions](/collaboration/consumer-listings-access#label-listings-gov-consumer-limitations).

## Prepare to access listings from accounts in the Kingdom of Saudi Arabia (KSA) region

If your account is in a [Europe and Middle East region](/user-guide/intro-regions#label-europe-regions), specifically Dammam (me-central2), and you want to install data products offered privately or on the Snowflake Marketplace, or
offer listings either privately or on the Snowflake Marketplace, you must review and acknowledge the following cross-region disclaimer for your
organization.

Important

To get data products and share listings with Snowflake customers outside your region, Snowflake shares organization and account metadata
and usage analytics with the customers you collaborate with outside of your region. Compliance standards and support for different
regulated workloads might be different or unavailable outside of your region.
Consider your compliance requirements before choosing to move or share data between Snowflake regions.

Note

You must use the ORGADMIN role to accept the terms. You only need to accept terms once for your Snowflake account. If you do not have
the ORGADMIN role, see [Enabling the ORGADMIN role in an account](https:/docs.snowflake.com/en/user-guide/organization-administrators#label-enabling-orgadmin-role-for-account).

1. sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. in the navigation menu, select **Admin** » **Terms**.
3. In the **Snowflake Marketplace** section, for **Sharing & Collaboration**, select **Review & Enable**.
4. Review the cross-region disclaimer and select **Acknowledge & Continue**.
5. Select **Done**.

Note

If you see an error, your user profile might be missing some contact information. If you have an administrator role, see
[Add user details to your user profile](/user-guide/ui-snowsight-profile#label-user-details-and-preferences) to update your profile using Snowsight. Otherwise, contact an
account administrator to update your user details.

# Stop sharing and collaboration from an account in a KSA region

If you no longer want to offer or access listings from your account in a KSA region, do the following:

1. [Delete all of your listings](/collaboration/provider-listings-removing) shared from your account, consistent with the applicable
   requirements in the Provider and Consumer Terms.
2. Stop consuming listings by dropping the databases imported when you
   [accessed listings](/collaboration/consumer-listings-access).
3. [Contact Snowflake Support](/user-guide/contacting-support) to have data sharing and collaboration disabled for your organization.
