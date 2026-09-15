# Manage provider profiles

The Data Exchange has the following requirements:

- A full Snowflake account to provide or consume data sets; reader accounts are not supported.
- By default, the ACCOUNTADMIN role can perform provider functions, such as creating a listing, creating a provider profile, reviewing listing requests, etc. These tasks can be delegated to other roles. For more information, see [Grant privileges to other roles](/user-guide/data-exchange-marketplace-privileges).

## Provider profile fields

The following table describes parameters required for creating and configuring your provider profile in the Data Exchange.

| Field Name | Description | Example |
| --- | --- | --- |
| **Logo** | A high-resolution image of your logo in the JPG or PNG format. The file size cannot exceed 2MB. Square image is recommended. | image.jpg |
| **Company Name** | Company name or brand name as it appears in the data listing. This is not the name of your Snowflake account. If the provider name includes special characters, these characters are parsed out in the suggested database name. The company name is the name of the provider profile. As a provider, you can have more than one provider profile (the provider nickname must be unique for each profile). When you publish a listing, you associate it with a provider profile. | ACME |
| **Description** | A short introduction (2-3 sentences) of the provider. | Acme, recognized and documented as the most accurate source of weather forecasts and warnings in the world, has saved tens of thousands of lives, prevented hundreds of thousands of injuries and tens of billions of dollars in property damage. With global headquarters in Palo Alto, CA and other offices around the world, Acme serves more than 1.5 billion people daily to help them plan their lives. |
| **Contact Email** | Email address for potential data consumers to contact you, typically a Sales contact. | `sales@example.com` |
| **Support Link** | Email for data consumers to contact the provider with questions. This is typically a Technical Support contact. | `support@example.com` |
| **Privacy Policy Link** | A link to a privacy policy on provider’s website. The link is required only for personalized shares. | `https://www.example.com/privacy` |
| **Snowflake General Contact Email** | An email address for Snowflake to contact the provider with questions about listings. |  |
| **Snowflake Technical Contact Email** | An email address for Snowflake to contact the provider about shared data. |  |

Expand

Show lessSee more

## Create a provider profile

When you join the Data Exchange as a provider, you must set up your provider profile. A provider profile is required for publishing a data listing.

If you are assigned the Data Exchange Admin role, or you have [Provider profile level privileges](/user-guide/data-exchange-marketplace-privileges#label-provider-profile-level-privileges), you can create and manage provider profiles for a Data Exchange in the **Manage Exchanges** tab of Snowsight.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Data sharing** » **External sharing**.
3. Select **Manage Exchanges** and then select the **Provider Profiles** tab.
4. Select **Add Profile**.
5. Complete the required fields. For the description of the fields, see [Delete a provider profile](#label-configuring-metadata-for-provider-profile-data-exchange) below.
6. Save your changes.

## Edit a provider profile

You can edit a provider profile at any time. The profile updates are reflected for all listings associated with the profile.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Data sharing** » **External sharing**.
3. Select **Manage Exchanges** and select the **Provider Profiles** tab.
4. Select the profile you want to edit.
5. From the **Manage** drop-down list, select **Update Profile**.
6. Make changes to the profile.
7. Select **Next** to review the preview of the profile.
8. Save your changes.

## Delete a provider profile

You can delete a provider profile as long as it is not associated with any listings, both published or unpublished.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Data sharing** » **External sharing**.
3. Select **Manage Exchanges** and select the **Provider Profiles** tab.
4. Select the profile that you want to delete.
5. From the **Manage** drop-down list, select **Delete Profile**.

   If the **Delete Profile** option is inactive, make sure no listings are associated with the profile.
