# Manage data listings

## Considerations for creating a listing

Note

These considerations also apply for creating a listing in a remote region.

- Since the data is shared between different accounts, data consumers should be able to use shared data objects without using double-quoted identifiers (see [Identifier requirements](/sql-reference/identifiers-syntax)). As a result, object identifiers for tables, columns, and share names must be upper case and use only alphanumeric characters.
- To ensure that your sensitive data in a shared database is not exposed to users in consumer accounts, see [Use secure objects to control data access](/user-guide/data-sharing-secure-views).
- Shares that are currently shared with a consumer account (i.e. via a direct share) can be added to a listing. Consumers must accept the listing terms in a Data Exchange web interface before they can create a database from the share.
- Only the role that created the share can attach the share to a listing.
- A share can only be attached to one listing. If a share has already been attached to a listing, it cannot be attached to another listing, even if the listing has been deleted.
- Before a new or modified free listing can be published, all sample queries are auto-validated to ensure that referenced objects are added to the share and the queries can be run successfully.
- The data must be legally shareable (i.e. the provider must own the data or have the right to share it).

  > Note
  >
  > To the extent any data in your data listing or data set is governed by any laws or contractual obligations, you must ensure that you have the legal and contractual rights to share such data. For example, you can only share protected health information (PHI) through a personalized data share and, to do so, you must: (1) have signed a business associate agreement (BAA) with Snowflake and the Consumer receiving the PHI, and; (2) ensure that the Consumer has also signed a BAA with Snowflake. Also, while you can share personal data through a data share, to do so you must have the applicable legal and contractual rights if the data is not publicly available.

## Considerations for creating a listing in a remote region and replicating data

- When you publish a listing, consumers will see your listing in all selected regions.
- While listings are automatically replicated, the data is not.
- For free listings, you must replicate data to each of the selected regions before publishing the listing.
- For personalized listings, you can replicate data upon consumer’s request.
- Make sure to allocate time to set up replication and understand costs involved.
- To share data in a region, you must have an account in that region in order to replicate data. If you have more than one account, all accounts must belong to the same organization.
- When you publish a listing in a remote region, you can either allow all accounts in your organization to fulfill listing requests or explicitly add individual accounts as providers. Only the listing owner can specify who can fulfill listing requests.
- Cross region data sharing utilizes Snowflake data replication functionality, for more information, see [Share data securely across regions and cloud platforms](/user-guide/secure-data-sharing-across-regions-platforms).
- You do not need to replicate the data to each region until a consumer requests it.
- For free listings, you have an option to pre-associate a share with the listing in a remote region. This will allow consumers to get the share instantly without submitting a request.
- To see a list of shares attached to a listing in a remote region, you must log in to the remote account from which you attached the share to the listing.

## Data listing fields

The following table describes parameters required for creating and configuring a data listing in the Data Exchange.

| Section | Field Name | Description | Example |
| --- | --- | --- | --- |
| **Basic Information** | **Listing Type** | See [Types of Listings](/collaboration/collaboration-listings-about#label-listing-access-types). | Available Values: Free, Personalized |
|  | **Profile** | The name of the provider profile that owns the share. You must create a provider profile before you can publish a listing. |  |
|  | **Title** | Title of the data listing. The title cannot exceed 110 characters. | Historical Weather by Postcode. |
|  | **Subtitle** | Subtitle of the data listing. The subtitle cannot exceed 110 characters. Title and subtitle should not be redundant. | Historical Weather Data by Location. |
|  | **Data Update Frequency** | How often the data is updated. | Available values: Near real-time, Daily, Weekly, Monthly, Quarterly, Annually, Never (Static Data). |
|  | **Category** | Data listings are categorized for easy discovery. |  |
|  | **Terms of Service** | A link to the listing terms hosted on the provider’s website. Consumers accept the terms before they can access the data. Listing terms are required for free listings, and are optional for personalized listings. | `https://www.example.com/en/legal` |
| **Details** | **Description** | Description of the shared dataset. The description must include:   (a) Scale of data   (b) Description of tables/views   (c) Whether the dataset is a sample   (d) Where to find data dictionaries. | ACME is the number one supplier of customized, pinpoint weather warnings to large enterprises, as well as a vital information source for worldwide weather forecasts, data and meteorological consulting services. This data is historical weather data for US zip codes that can be used to further enhance your existing data to provide deeper analytics. |
|  | **Link to Documentation** | A link to a page on provider’s website with more detailed documentation. Documentation must be clear and reference the right schema objects present in the Snowflake share. It cannot be just standard documentation. | `https://developer.example.com` |
| **Data** | **Database Objects or Secure Share** | Select data you wish to share. This section is only available for free data listings. |  |
| **Business Needs** | **Business Need** | Data listings are grouped by business needs for easy discovery.   - You can select up to six business needs for your listing. If you do not see a relevant business need in the drop-down list, you can create a custom one.   - Consumers can easily discover listings based on business needs available in the drop-down list. However, custom business needs you add are not included, and are only visible in your listing details. |  |
|  | **Description** | Description of how your data or data service addresses the business need. |  |
| **Sample SQL Query** | **Title** | Descriptive title for the query to help consumers understand the data. You can add more than one example. |  |
|  | **Description (Optional)** | Description of the example with additional instructions, e.g. name of the schema, sample tables, fields, use cases. |  |
|  | **SQL Query** | Test sample queries against the database you use to create the share. Snowflake auto-validates the queries to ensure that all referenced objects are added to the share and the queries run successfully. If the validation fails, an error message with a reason is displayed. You can see an exclamation sign next to each query that failed. |  |
| **Region Availability** | **All available regions** or **Specific Regions** | Regions where your listing will be visible. You will need to replicate the data to these regions. You can edit the list of available regions at any time without resubmitting it for administrator’s approval. If you remove a region that was previously available, consumers in that region will no longer be able to see the listing. |  |

Expand

Show lessSee more

## Create and publish a data listing

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Data sharing** » **External sharing**.
3. Select the **Share Data** drop-down list and select a data exchange.
4. In the **New Listing** dialog box, enter the listing title as it appears to the consumers and select the listing type. For more information about listing type, see [Types of Listings](/collaboration/collaboration-listings-about#label-listing-access-types).
5. Complete each of the sections for the new listing. You can save the draft at any time to finish it later. For a description of each section and related fields, see [Configure listings](/collaboration/provider-listings-reference).

   For a free listing, to associate a share with the listing, when editing the **Data** section:

   > Note
   >
   > Until a listing is published, it can only be associated with a share in the local/primary account. After the listing is published, it can be associated with a share in additional regions that you have selected.

   1. Select **Select Data**.
   2. If a secure share exists, navigate to the share and select it. If a share does not exist, navigate to the desired database and select the database objects you wish to add to the share.

      Note

      If you do not see a share, it is either already attached to another listing, or has been previously shared with consumers.
   3. Select **Done**.
   4. (Optional) You can change the default name for the secure share.
   5. Select **Save**.
6. Once you complete all of the sections, select **Publish** to publish the listing to the selected regions.

   The **Publish** button is not activated if:

   - Any of the provided sample SQL queries fail validation. For more information, see [Data listing fields](#label-configuring-metadata-for-data-listing-data-exchange).
   - You are not the share owner.

## View personalized listing requests

> Note
>
> Email notifications are sent to providers to notify them of data requests. You can change the request notification email for a specific listing in the **Settings** tab.

1. In the navigation menu, select **Data sharing** » **External sharing**.
2. Select the **Requests** tab. Use the filtering drop down list to view requests by status.

## Approve consumer requests for data listings in a remote region

Note

- For **personalized** listings, data is not automatically available in remote regions. The provider is responsible for replicating their data to each of these regions.
- For **free** listings, you have an option to pre-associate a share with the listing in a remote region. This allows consumers to get the share instantly without submitting a request. You can also replicate data and attach a share to a listing after receiving a request from the first consumer in a region. Once the listing is attached to the share, all consumers in that region can access the share instantly.
- You can specify whether a listing can be fulfilled by a select provider account(s) or by any account in the organization.
- If the consumer is in a different region, before attaching a share, you must set up replication of data to the account in each remote region. For more information, see [Share data securely across regions and cloud platforms](/user-guide/secure-data-sharing-across-regions-platforms).

1. In the navigation menu, select **Data sharing** » **External sharing**.
2. Select the **Requests** tab.
3. Select **Review** next to the listing name.
4. In the **Associate Secure Share** section, select an account where you wish to create the share.
5. Select the role that owns the share and the shared database objects (or has the necessary privileges on the database objects to be able to add them to a share).
6. select **Select Data**.
7. If a secure share exists, navigate to the share and select it. If a share does not exist, navigate to the desired database and select the database objects you wish to add to the share.

   Note

   If you do not see a share, it is either already attached to another listing, or has been previously shared with consumers.
8. Select **Done**.
9. (Optional) Change the default name for the secure share.
10. Select **Fulfill Request**.

> Tip
>
> If you receive an error when fulfilling a request for a remote region, consider the following:
>
> - Has the remote account been added to the Marketplace as a provider?
> - Is the remote account part of the same organization as the account you published the listing from?
> - Did you create a new share using the ACCOUNTADMIN role?
> - Have you added other consumers to the share you are trying to attach?

## View fulfilled listing requests

Providers who fulfill free or personalized listing requests using [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) can view records of consumers added to the
share. To view the records, in the navigation menu, select **Data sharing** » **Internal sharing**, and select the **Shared by your account** tab.

These records are also available in the [QUERY\_HISTORY view](/sql-reference/account-usage/query_history).

## Edit a data listing

When you publish a new version of the listing, it overwrites the previously published listing. If you remove a region that was previously available, consumers in that region will no longer have access to the shared dataset.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) as an ACCOUNTADMIN.
2. In the navigation menu, select **Data sharing** » **External sharing** » **Shared by your account**.
3. Click the name of the listing you wish to update.
4. Next to the listing title, click **New Draft**.
5. Click **Edit** for the section you wish to update.
6. Click **Publish**.

## Unpublish a data listing

When you unpublish a data listing, existing consumers can still access the data share unless you remove them from the share. New consumers cannot see it.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) as an ACCOUNTADMIN.
2. In the navigation menu, select **Data sharing** » **External sharing** » **Shared by your account**.
3. Select the name of the listing you wish to unpublish.
4. In the top-right corner, from the **Live** drop-down list, select **Unpublish**.

## Republish a data listing

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) as an ACCOUNTADMIN.
2. In the navigation menu, select **Data sharing** » **External sharing** » **Shared by your account**.
3. Select the name of the listing you wish to republish.
4. In the top-right corner, from the drop-down list select **Re-publish**.
5. Select **Re-publish** to republish the listing.

## Remove a data listing

See [Removing listings as a provider](https://other-docs.snowflake.com/en/collaboration/provider-listings-removing).

## Update a data share

You can update a data share using Snowsight.
Keep in mind that each time you modify a data listing, you must notify the consumers to ensure that you do not break their processes.
Examples of breaking changes include:

- Adding/removing a column.
- Renaming objects.
- Removing objects.
