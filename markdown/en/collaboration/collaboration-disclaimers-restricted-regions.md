# Collaboration disclaimers for restricted regions

## Prepare to access listings from accounts in U.S. government regions, Kingdom of Saudi Arabia (KSA), and Virtual Private Snowflake (VPS)

If your account is in a U.S. government region, KSA region, or VPS environment and you want to install data products offered privately or on the Snowflake Marketplace, or offer listings either privately or on the Snowflake Marketplace, you must review and acknowledge the following cross-region disclaimer for your organization.

Important

To get data products and share listings with Snowflake customers outside your region, Snowflake shares organization and account metadata and usage analytics with the customers you collaborate with outside of your region.

Compliance standards, such as [FedRAMP](/user-guide/cert-fedramp), and support for different regulated workloads, such as [ITAR](/user-guide/cert-itar), might be different or unavailable outside of your U.S. Government Region. Consider your compliance requirements before choosing to move or share data between Snowflake regions.

Note

You must use the ORGADMIN role or the GLOBALORGADMIN role to accept the disclaimer. You only need to accept the disclaimer once for your Snowflake account. If you do not have the ORGADMIN role, see [Enabling the ORGADMIN role in an account](/user-guide/organization-administrators#label-enabling-orgadmin-role-for-account). For organizations using a global organization account, see [Managing organizations](/user-guide/organizations).

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Admin** » **Terms**.
3. In the **Snowflake Marketplace** section, for **Sharing & Collaboration**, select **Review & Enable**.
4. Review the cross-region disclaimer and select **Acknowledge & Continue**.
5. Select **Done**.

Note

If you see an error, your user profile might be missing some contact information. If you have an administrator role, see
[Add user details to your user profile](/user-guide/ui-snowsight-profile#label-user-details-and-preferences) to update your profile using Snowsight. Otherwise, contact an
account administrator to update your user details.

## Provider guidance

Providers in all restricted regions must complete the disclaimer acceptance above before they can publish listings.

### VPS providers

1. Contact the consumer to collect the consumer’s Organization Name and Account
   Identifier. For details, see [Finding your account identifier](/user-guide/admin-account-identifier).
2. Contact Snowflake Support and ask for VPS Provider Sharing to be enabled
   between you and your new consumer. Include:
   - Your VPS deployment name and account identifier.
   - The consumer’s account identifiers.
3. Create a private listing for the consumer using Provider Studio. For the
   full workflow, see
   [About providing VPS Private Listings](/collaboration/virtual-private-snowflake/vps-collaboration-for-providers).

### U.S. government and KSA providers

For provider-specific limitations and any non-commercial-region considerations, see [Government providers](/collaboration/provider-listings-government-providers).

## Consumer guidance

Consumers in restricted regions must have the cross-region disclaimer accepted by their ORGADMIN before accessing listings. The acceptance steps above apply.

For the general consumer prerequisites — Snowflake Provider and Consumer Terms, required privileges, and paid-listing billing setup — see [Use listings as a consumer](/collaboration/consumer-becoming).

### VPS consumers

Snowflake Support must allow the provider to share with the VPS environment before the listing is accessible. Contact Snowflake Support to request that the provider be permitted to share private listings with your VPS environment. For the full consumer flow, see [About accessing and consuming listings in VPS](/collaboration/virtual-private-snowflake/vps-collaboration-for-consumers).

## Stop sharing and collaboration from a restricted region

If you no longer want to offer or access listings from your account in a restricted region (U.S. government region, KSA region, or VPS), do the following:

1. [Delete all of your listings](/collaboration/provider-listings-removing) shared from your account, consistent with the applicable requirements in the Provider and Consumer Terms.
2. Stop consuming listings by dropping the databases imported when you [accessed listings](/collaboration/consumer-listings-access).
3. [Contact Snowflake Support](/user-guide/contacting-support) to have data sharing and collaboration disabled for your organization.

Note

**VPS:** In addition to the steps above, Snowflake Support must also disable the VPS provider/consumer relationship. Contact Support to confirm that VPS collaboration has been fully removed for your organization.

The types of listings and data products that you can access from U.S. government regions are limited. See [Limitations for accessing listings from accounts in U.S. government regions](/collaboration/consumer-listings-access#label-listings-gov-consumer-limitations).
