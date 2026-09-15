# Manage your provider profile

This page explains the roles and privileges you need to manage a provider profile, and how to create, edit, and delete the profile that controls the company name, logo, and contact details shown on your listings.

**On this page**

1. [Required roles and privileges](#label-manage-profiles-roles-and-privileges)
2. [Create a profile](#label-create-provider-profile)
3. [Edit your provider profile](#label-edit-provider-profile)
4. [Delete your provider profile](#label-delete-provider-profile)

Tip: Common reasons provider profiles are rejected

New and updated profiles are reviewed by Snowflake before they appear on the Snowflake Marketplace. Before you submit, check for these frequent issues:

- **Low-quality logo.** The company icon is blurry, cut off, skewed, or hard to read. Use a clear, high-resolution square logo that belongs to your company.
- **Profile name doesn’t match your company.** The name should match your company name or a name you publicly do business as, so consumers can identify you.
- **Vague company description.** The description doesn’t clearly explain who you are and what you provide on the Snowflake Marketplace, or it directs consumers off-platform or to another company’s website.
- **Generic or inaccessible links.** The privacy policy or support link points to a homepage, sits behind a login, is a shortened URL, or leads to another company’s page. Link directly to the relevant page and keep it publicly accessible.

## 1. Required roles and privileges

To work with provider profiles, you need one of the following.

| Task | Required roles and privileges |
| --- | --- |
| Create a provider profile | The ACCOUNTADMIN role, or a role with the global CREATE LISTING privilege (the same privilege used to create listings) |
| Edit or delete a provider profile | The profile owner (a role with OWNERSHIP of the profile), or a role with the MODIFY privilege on the profile |
| Grant profile privileges to another role | The profile owner (a role with OWNERSHIP of the profile). See [grant privileges](/user-guide/data-exchange-marketplace-privileges#label-granting-provider-privileges-to-other-roles) |

Expand

Show lessSee more

## 2. Create a profile

You can create a profile by filling out the following information about your organization. New profiles created must be reviewed and approved by Snowflake before they become visible in the Snowflake Marketplace.

### Provider profile fields

The following table describes each field and its requirements:

| Field | Description | Example |
| --- | --- | --- |
| **Company icon** | **Required.** A high-resolution logo image in JPG or PNG format. You must include a clear and high-quality logo that belongs to your company.   - Square or circle shape, 256px by 256px recommended. - File size can’t exceed 2 MB. - Must clearly belong to your company and be easy to read. - If publishing on behalf of another entity, you may use that entity’s logo   if you have the necessary rights. - Logos that are cut off, skewed, or hard to read will not be approved. | Example company logo |
| **Company name** | **Required.** Your profile name should be the same as your company name or a name your company publicly does business as. Consumers should be able to identify your company through your profile name.   - You may only have one profile per distinct legal entity. - If two or more companies claim the same profile name, Snowflake reviews   on a first come, first served basis. - If publishing on behalf of another entity, include your entity name in   the profile name (for example, “Company B by Company A”). | *Acme Data Co.* |
| **Company description** | **Required.** A short introduction (2–3 sentences) about your company and what you offer. You must include an accurate description of your organization, highlighting its relevance to the products you offer.   - Must clearly explain who you are and what you provide. - If your profile name does not match the organization name in your product   documentation, listing terms, or privacy notice, you must clarify the   relationship here. - If your profile is managed by another company, include a “Managed by   [Company]” statement. - Free of spelling errors and major grammar issues. - Must not direct consumers off-platform or to another company’s website. | *At Acme, we provide real-time weather data to enterprises globally. Our datasets cover 195 countries and are updated daily to support demand forecasting, risk analysis, and operational planning.* |
| **Consumer contact email** | **Required.** An email address that receives notifications when a consumer requests access to your data. This email also appears under **Contact Provider** on your listing. You must include up-to-date contact information with a business domain.   - Must be a valid email, not a URL. - Use a group alias or distribution list (for example, [snowflake@company.com](mailto:snowflake@company.com)) instead of an individual’s email address, so notifications keep reaching your team if that person leaves the company. | *[sales@acme.com](mailto:sales@acme.com)* |
| **Privacy policy link** | **Required.** A URL to your public-facing privacy notice applicable to all consumer personal data collected by you or on your behalf.   - Must link directly to a privacy policy page, not a homepage or contact page. - Must be publicly accessible and not locked behind a login screen. - Must not be a shortened URL (for example, bit.ly). - Non-English privacy policy links are accepted. | *<https://www.acme.com/privacy-policy>* |
| **Support link or email** | **Required.** A link or email address for consumers to contact you for technical support. Must include a business domain.   - Can be a support email or a direct link to your support page. - Must be publicly accessible and not locked behind a login screen. - Must not be a shortened URL (for example, bit.ly). - Must not lead to another company’s page. - Recommended: use a group alias or distribution list on your company domain instead of an individual’s email address, so support requests aren’t lost if that person leaves the company. | *[support@acme.com](mailto:support@acme.com) or <https://www.acme.com/support>* |

Expand

Show lessSee more

### Snowflake contact information

The following fields are not publicly visible to consumers. Snowflake
uses these email addresses to contact providers directly regarding their
listings and account. Use a group alias or distribution list rather than an
individual’s email address, so you continue to receive these messages if that
person leaves the company.

| Field | Description | Example |
| --- | --- | --- |
| **Business contact email** | **Required.** An email address for Snowflake to contact you with questions about your listings. Must use a business domain. | *[admin@acme.com](mailto:admin@acme.com)* |
| **Technical contact email** | **Required.** An email address for Snowflake to contact you about shared data. Must use a business domain. | *[operations@acme.com](mailto:operations@acme.com)* |

Expand

Show lessSee more

Note

Providers are also notified through these emails when a listing or profile is approved or denied.

## 3. Edit your provider profile

You can edit your provider profile at any time. Most updates to your profile must be reviewed and approved by Snowflake before they become
visible in the Snowflake Marketplace.

Note

Updating the **Business Contact** and **Technical Contact** fields in your provider profile does not require approval from Snowflake.

After your updated profile is approved, the changes are visible for all listings associated with your provider profile.

To modify a provider profile, you must be the owner of the provider profile or you must use a role that has the MODIFY privilege on the
profile. For more information, see [Granting provider privileges to other roles in the Snowflake Marketplace or a Data Exchange](/user-guide/data-exchange-marketplace-privileges#label-granting-provider-privileges-to-other-roles).

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. Switch to a role that has the [MODIFY privilege on the profile](/user-guide/data-exchange-marketplace-privileges#label-modify-on-provider-profile).
3. In the navigation menu, select **Marketplace** » **Provider Studio** » **Profiles**.
4. Select the profile you want to update.
5. In the **Manage** drop-down menu, select **Update Profile**.
6. Edit the profile and then select **Submit for Approval**.

## 4. Delete your provider profile

You can delete your provider profile as long as your profile is not associated with any listings, either published or unpublished.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. Switch to a role that has the [MODIFY privilege on the profile](/user-guide/data-exchange-marketplace-privileges#label-modify-on-provider-profile).
3. In the navigation menu, select **Marketplace** » **Provider Studio** » **Profiles**.
4. Select the profile you want to delete.
5. In the **Manage** drop-down menu, select **Delete Profile**.

   Note

   If the **Delete Profile** option is inactive, make sure that no listings are associated with the profile.
6. Select **Delete**.
