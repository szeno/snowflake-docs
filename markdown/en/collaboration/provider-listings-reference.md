# Configure listings

This page describes the fields you use to configure a listing, including visibility, basic information, product type, accessibility, and metadata, along with the roles and privileges you need to set them. The required fields depend on whether you’re publishing a public listing on the Snowflake Marketplace or a private listing shared directly with specific accounts.

**On this page**

1. [Required roles and privileges](#label-configure-listings-roles-and-privileges)
2. [Listing visibility](#label-listing-visibility)
3. [Basic information](#label-configuring-metadata-for-data-listing)
4. [Product type](#label-listings-data-product)
5. [Listing accessibility](#label-listing-accessibility)
6. [Listing metadata](#label-listing-metadata)
7. [Additional public listing fields](#label-additional-public-listing-fields)
8. [Additional private listing fields](#label-additional-private-listing-fields)

Tip: Common reasons public listings are rejected

Before you submit a public listing for approval, check for these frequent issues:

- **Short or incomplete description.** Your description should clearly explain what the product is and why it’s valuable. Avoid 1–2 sentence summaries that only describe the contents. For datasets, include the scope, scale and the value for consumers. For apps, explain what the application does, the problem it solves, and the benefits to users.
- **Generic documentation link.** Your documentation link should point directly to documentation for the specific data product you’re listing. Do not link to your company’s homepage, a general documentation portal, or a landing page that requires users to search for the product.
- **Incorrect or restricted category.** Choose the [category](#label-listings-additional-fields) that best represents your product so consumers can find it easily on the Marketplace. If you select a [restricted category](/collaboration/provider-listings-reference#label-restricted-categories), make sure you’ve included the required object or metadata before submitting the listing.
- **Inconsistent product attributes.** Verify that your [attributes](/collaboration/provider-listings-reference#label-listings-data-product-attributes)—such as update frequency, geographic coverage, time range, refresh schedule, or supported regions—accurately describe your product and are consistent with the title, description, documentation, and the underlying data or application.

## 1. Required roles and privileges

To configure the fields on this page, you need one of the following.

| Task | Required roles and privileges |
| --- | --- |
| Configure any field on a listing | The ACCOUNTADMIN role, or a role with the OWNERSHIP or MODIFY privilege on the listing |
| Add a trial to a paid listing | The ACCOUNTADMIN role, or the listing owner (a role with the OWNERSHIP privilege on the listing) |

Expand

Show lessSee more

The listing must already exist before you can configure these fields.

For the full set of roles and privileges required to create, modify, and publish listings, see [Required roles and privileges](/collaboration/provider-listings-creating-publishing#label-required-roles-and-privileges).

## 2. Listing visibility

When you create a listing, you first select the listing visibility. This
determines which fields are required and how consumers can access your data product.

| Option | Description | Example |
| --- | --- | --- |
| **Public Listing** | Available to all consumers on the Snowflake Marketplace. Requires Snowflake approval before publishing. Consumers can discover and install your listing directly from the Snowflake Marketplace. | Snowflake Marketplace listing visibility option in Provider Studio |
| **Private Listing** | Shared directly with specific Snowflake accounts that you designate. Does not require Snowflake approval. Not visible on the Snowflake Marketplace. | Specified Consumers listing visibility option in Provider Studio |

Expand

Show lessSee more

## 3. Basic information

Complete the following descriptive fields for your listing:

Note

If you are creating a private listing, only the following fields are
required: Title, Profile, Description, and Terms of Service.

| Field | Description | Example |
| --- | --- | --- |
| **Title** | **Required.** The title of your listing as it appears to consumers.   - Max 110 characters. - Use title case format. - Use a high-level, non-generic title. - Must be unique across your provider profile. | *Global Macroeconomic Data, Consumer Price Index (CPI): USA* |
| **Subtitle** | **Required for public listings.** A short tagline displayed below the listing name.   - Max 100 characters. - Use sentence case. - Do not repeat the title. | *Real-time weather forecasts for 190 countries* |
| **Profile** | **Required.** The provider profile to associate with this listing. Controls which company name and logo appear on the listing. See [Manage your provider profile](/collaboration/provider-profiles-managing). | Select the profile you want the listing to be listed under. |
| **Description** | **Required.** The most important field on your listing (250–6000 characters).  The description must include:   - An introduction to your product. - Details about the nature of the product:   - **For data products:** Details on the product’s tables and fields.   - **For Native App products:** Details about the product’s functionality.   - **For listings that include AI objects:** Include the following for each AI object:     - A description of the AI object and its purpose.     - 2–3 representative example inputs or prompts demonstrating expected behavior.     - Any known conditions, limitations, or data requirements for successful use. - Use cases for the product. - Use rich text formatting where applicable. - Use consistent punctuation and check spelling and grammar. - Do not include PII or misleading information. | **What is this listing about:**  A central source of US housing and real estate data, including valuation, financing, migration, addresses, points of interest (POI), and income statistics.  **Scope, scale:**  Nationwide coverage across the United States, with datasets suitable for national, regional, and local market analysis.  **Value for consumers:**  Helps teams analyze market trends, benchmark property values, and plan investments without assembling disparate housing data sources. |
| **Link to Documentation** | **Required for public listings.** A link to additional information about your product. This can be a product page, data dictionary, self-service learning tools, or other related information about the specific product you are listing.   - Preferably hosted on your company website. - Must be publicly accessible on the internet. - Link can’t be locked behind a login screen. | *<https://data-docs.snowflake.com/solutions/asset-wealth-management>* |
| **Business Needs** | **Required for public listings.** At least 1 business need is required. Select up to 6 business needs that your data product addresses.   - Use pre-defined categories where possible. Custom business needs   are not discoverable in the Snowflake Marketplace search. - If creating a custom business need, use 2–4 words maximum. - Each example must be specific to the selected category and describe   a use case of your data product. - Business need examples should not repeat the value already stated   in the Description field. - You can edit business needs at any time without resubmitting for approval. | **Pre-defined:** *Location Geocoding*  Use these addresses to convert geocoding addresses to coordinates, and vice versa reverse geocoding coordinates to readable addresses. This information can be paired against other datasets to determine geographic hierarchies (for example, mapping to census data to determine wealthiest zip codes, or mapping to company sales data to see zip codes/areas with the highest revenue).  **Custom:** *Property investment analysis*  Compare housing valuation, migration, and income statistics across US markets to identify regions with strong appreciation potential and target acquisition opportunities. |
| **Terms of Service** | **Required.** The service agreement that consumers must accept before accessing your listing. Select one of the following:   - **Standard Agreement for Marketplace Products**: Snowflake’s   standard listing terms available at   <https://www.snowflake.com/marketplace/standard-agreement/>.   By selecting this, you confirm you have reviewed it and the   [Disclaimer](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/snowflake-marketplace/standard-agreement-for-marketplace-products/)   with your legal counsel. - **Custom**: Provide a URL to your own listing terms. Must be   publicly accessible and not require authentication to access. - **Listing terms will be provided offline**: Available for   private listings only. This option lets you provide listing terms   to your consumers that isn’t available at a URL. | *<https://www.snowflake.com/marketplace/standard-agreement/>* |

Expand

Show lessSee more

## 4. Product type

Configure the data product for your listing. This can be a secure share, a Snowflake Native App, or a Connected App.

You can select objects and have Snowflake create a secure share, or add a share that you already created.
See [Prepare the shares for your listing](/collaboration/provider-listings-preparing#label-marketplace-preparing-shares) for guidance creating shares for paid listings.

Select the type of data product you want to share with consumers:

| Data product type | Description | Example |
| --- | --- | --- |
| **Secure Share** | Provide live, secure access to data and other objects in your account. | Secure Share data product type option in Provider Studio |
| **Native App** | Application runs directly and securely in the consumer’s account. | Native App data product type option in Provider Studio |
| **Connected App** | Application connects to the consumer’s account to process data. | Connected App data product type option in Provider Studio |

Expand

Show lessSee more

When adding a data product to your listing, consider the following:

- Secure shares can only be attached to one listing.
- Application packages can be attached to multiple listings.
- After the listing is published, you can’t attach a different share.
- You can only see shares that your current role owns.
- The data product must be legally shareable (that is, you must own the data or have the right to share it).
- Until a listing is published, it can only be associated with a share in the local/primary account. After the
  listing is published, it can be associated with a share in additional regions that you have selected.

### Connection string identifiers (Connected Apps only)

For Connected Apps, add one or more valid connection string identifiers (CSIDs).
Submit the same CSIDs that you submitted when you registered on the Snowflake
Partner Network portal. See [Connected App requirements](/collaboration/guidelines-reqs-for-listing-apps#connected-apps)
for more details.

## 5. Listing accessibility

Listing access controls how consumers can access your data product. You can select the following
listing accessibility types and modify if it is still in draft.

For listings that are published, you can’t change the listing accessibility. See
[Listing access options](/collaboration/collaboration-listings-about#label-listing-access-types) for more details.

| Accessibility type | Public listing | Private listing |
| --- | --- | --- |
| **Free** | Available | Available |
| **Limited trial** | Available | Not available |
| **Paid listing** | Available (only for providers who meet the [paid listing requirements](/collaboration/provider-becoming#label-monetization-provider-onboarding)) | Available (only for providers who meet the [paid listing requirements](/collaboration/provider-becoming#label-monetization-provider-onboarding)) |

Expand

Show lessSee more

## 6. Listing metadata

Complete the following additional and optional fields for your listing.

### Additional fields

After completing the basic information, the following fields become available
for your listing:

Note

Additional fields are required for public listings only. Private listings
can skip this section.

| Field | Description | Example |
| --- | --- | --- |
| **Category** | **Required for public listings.** Categories help consumers find your listing on the Snowflake Marketplace. The category must reflect the product listed.   - Select up to 3 categories from the available drop-down list. - Not available for private listings.   The following categories are restricted and require a specific product or AI object:   - **Cortex AI Ready**: May only be selected if the listing includes   at least one attached AI object, such as a Cortex Agent, Semantic View, or CKE. - **Integrated SaaS Applications**: May only be selected for Connected Application listings. - **Cortex Knowledge Extensions**: Requires an attached CKE.   Listings that select a restricted category without the required object will not be approved. | *Financial Services, Economics, Banking* |
| **Attributes** | **Required for public listings.** Define additional attributes that describe the characteristics of your data product. Ensure these fields are consistent with what is stated in your listing title, description, and other fields.  **Update Frequency**: How often your data product is updated. If updated at different frequencies, choose the highest frequency. Must match the update cadence described elsewhere in your listing.  **Geographic Coverage**: Select the geographic regions your data product covers. Should reflect what is actually included in the data product.  **Geographic Granularity**: If you specify global or multiple states or countries as the geographic coverage of your dataset, select a granularity for the data product. You can only choose one option, so select the most granular option available in your data product.  **Time Range**: The time period your data product covers. Choose from pre-defined time ranges or specify a custom date range (for example, 2020-01-01 to 2024-12-31).  **Additional Attributes** *(optional)*: Any additional information you want to communicate to consumers. Up to 4 attributes, 2–5 words each, max 80 characters per attribute. | **Update Frequency:** Monthly  **Geographic Coverage:** United States  **Geographic Granularity:** Zip code  **Time Range:** 2015-01-01 to 2024-12-31  **Additional Attributes:** Includes points of interest (POI) data |
| **Quick Start Examples** | **Required for public listings with a Secure Share data product.** Not required for Native App or Connected App listings. Select **Add** to add one SQL query. Snowflake recommends including 3–4 sample queries.  **Title**: A descriptive title for the query to help consumers understand how they can use the data product.  **Description** *(optional)*: Description that ties the title to a specific use case. Use *schema*.*table* format when referencing tables and views. Do not include the database name.  **SQL Query**: The SQL query code. Snowflake automatically validates your queries. If a query fails validation, the listing can’t be published.  The query must meet the following requirements:   - Must return at least one row. - Must reference objects that are explicitly in the share. - Objects must be qualified using `<SCHEMA>.<OBJECT>` format.   Do not include the database name. For example, `EXAMPLE_SCHEMA.TABLE_A`. | **Title:** Find zip codes with top adjusted gross income per capita  **Description:** Show the top 5 zip codes by gross income that have a population of at least 10k people  Copy code  ``` SELECT   geo.zip_code,   ROUND(     income.agi / NULLIF(pop.count, 0),     0   )   AS per_capita_income FROM <INCOME_SCHEMA>.<INCOME_TABLE> income JOIN <POP_SCHEMA>.<POP_TABLE> pop   ON income.geo_id = pop.geo_id JOIN <GEO_SCHEMA>.<GEO_TABLE> geo   ON income.geo_id = geo.geo_id WHERE pop.count > 10000 ORDER BY per_capita_income DESC LIMIT 5; ``` |

Expand

Show lessSee more

### Pricing

**Required for paid listings.** Pricing applies to paid listings, whether public or private. Prices are in US dollars only.

To set up pricing, go to the **Pricing** section and configure the following:

- **Pricing plan.** The pricing model that determines how consumers are charged, such as a usage-based plan (for example, a monthly access fee plus per-query charges) or a flat fee. A pricing plan is required for **Self-serve** offers, where consumers see the price and purchase directly, but optional for **Sales-led** offers, where consumers contact you to complete the purchase.
- **Standard offer (required).** The offer that publishes your listing for purchase. It ties the pricing plan to the purchase terms, including the purchase type (**Self-serve** so consumers see the price and buy directly, or **Sales-led** so they contact you first), the contract type and duration, payment options, and the price and description consumers see.

For the available pricing models and the detailed steps to create a pricing plan and offer, see [Paid listings pricing models](/collaboration/provider-listings-pricing-model) and [Create and publish a listing](/collaboration/provider-listings-creating-publishing).

### Optional fields

Depending on your listing’s access type, you can also configure the following optional fields. For details, see the section for each field.

| Optional field | Description |
| --- | --- |
| **Trial** | Offer consumers a free trial of your data product. The available trial options depend on your listing’s access type. See [Trial](#label-listings-trial). |
| **Data dictionary** | Give consumers insight into the contents and structure of your listing before they install the data product into their account. See [Data dictionary](#label-listings-data-dictionaries). |
| **Compliance certifications** | Add compliance certification badges to your listing to build trust with consumers. See [Compliance certifications](#label-listings-compliance-certifications). |

Expand

Show lessSee more

#### Trial

You can offer the following trial types:

- **Limited time**: Consumers can trial your data product for a limited period of time. Choose this if you offer your entire data product for a short period.
- **Unlimited time**: Consumers can trial your data product indefinitely. Choose this if you offer a sample of your full data product.
- **Limited functionality**: Consumers have access to limited functionality of your data product.
- **Limited functionality and time**: Consumers have access to limited functionality for a limited time.

The trial types you can offer depend on your listing’s access type and data product type:

| Listing type | Limited time | Unlimited time | Limited functionality | Limited functionality and time |
| --- | --- | --- | --- | --- |
| **Limited trial** (dataset) | Yes | Yes | — | — |
| **Limited trial** (Native App) | Yes | Yes | Yes | Yes |
| **Paid listing** | Yes | — | Yes | Yes |

Expand

Show lessSee more

Warning

You must limit functionality to your app by using the
[SYSTEM$IS\_LISTING\_TRIAL](/sql-reference/functions/system_is_listing_trial) system function.
If your app is not set up to limit functionality, trial customers will
receive full access.

**For paid listings**

Trials are optional for all paid listings, including public and private listings.

Note

Only account administrators (users with the ACCOUNTADMIN role) or the
listing owner (a role with OWNERSHIP privilege on the listing) can
add a trial to a paid listing.

To add a trial:

1. Go to the Trial section.
2. Select Add Trial.
3. Select the trial terms:

   - Limited time: free trial for 1, 7, 30, 60, or 90 days; access ends when trial ends.
   - Limited functionality: free trial with limited functionality; doesn’t expire until consumer upgrades.
   - Limited functionality and time: limited functionality for 1, 7, 30, 60, or 90 days.
4. Add a trial description (optional).

Tip

To restrict data to paying customers, use the
[SYSTEM$IS\_LISTING\_PURCHASED](/sql-reference/functions/system_is_listing_purchased) system function
in a secure view. It returns TRUE only for consumers who have purchased the listing, so consumers
who are trialing the listing don’t see the restricted data.

#### Data dictionary

After adding a data product to your listing, you can add a data dictionary. A data dictionary provides consumers insight into the contents
and structure of your listing before installing the data product into their account.

A data dictionary is optional, and the accompanying data preview is also optional.

The following sections explain what a data dictionary is, how to set one up, how to mask sensitive data in previews, and how previews are
refreshed.

##### About data dictionaries

You can use a data dictionary to make the contents of your listing visible to consumers. A data dictionary is generated for tables and
views within a listing. Listings can also include a preview of data, referred to as a Data Dictionary Data Preview.

Your data is visible in two ways:

| Visibility type | Description |
| --- | --- |
| **Featured objects** | Allow the consumer to quickly view the contents of the object. You can select up to five of the most important database objects within the listing. |
| **All objects** | Allows the consumer to view all of the objects within a listing. It is auto-generated when you publish a listing. |

Expand

Show lessSee more

Data dictionary Data Preview allow both providers and consumers to preview data for tables and views associated with listings.

Previews provide a representative sample of the data, allowing:

- Providers to see exactly what data will be available in a preview.
- Consumers to determine if a listing contains the data they are looking for.

Note

Data in a listing is automatically made available for preview.
Providers needn’t do anything special to enable preview.

##### Set up a data dictionary for your listing

Before you can add a data dictionary, you must add a data product to the listing.

To set up a data dictionary, do the following:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Provider Studio** » **Listings**.
3. Find and select the listing where you want to add a data dictionary.
4. Select **Save and Create Data Dictionary**.

   Note

   By saving this share, you agree that Snowflake is permitted to create a data dictionary and associated preview for the share and
   display it to consumers when the listing is published.

   Note that Data Dictionary data previews are automatically updated when underlying data changes.

   If your data product contains PII or other personal data, mask those columns as such.
   For more information, including instructions on how to mask PII and other personal data see [Mask PII and other data in data previews](#label-listings-data-product-data-preview).

   After you save the listing, the data dictionary displays, listing all of the tables, views, and functions within the listing.
5. Search for or select an object that you want to include as a featured object, then select **Add to featured**.

   Optionally, repeat this step to add additional featured objects. You can have up to five featured objects in a listing.
6. Select **Save**.

You can edit column descriptions for tables in the Provider Studio, or you can use SQL.
Use the COMMENT parameter in the [CREATE <object>](/sql-reference/sql/create) and [ALTER <object>](/sql-reference/sql/alter) commands or the [COMMENT](/sql-reference/sql/comment)
command to add a comment describing an object or [individual table columns](/sql-reference/sql/alter-table-column).

##### Mask PII and other data in data previews

Snowflake periodically runs [Data Classification](/user-guide/classify-intro) on Data Previews to identify and mask any column with a high likelihood of containing PII
(Personally identifiable information) or other personal data. Personal data includes information relating to an identified or identifiable
person, such as:

- Name, age, email, or mailing address
- Educational or employment information
- Location data or device activity
- Customer records, or account information

Once Snowflake identifies and masks a PII column, an email is sent to the technical contact listed in the provider profile to review the
details. At any time, you can manually select or deselect PII columns in the Data Preview.

To view or modify PII classification results, do the following:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Provider Studio**.
3. Select **Listings** from the top navigation. To create a listing, see [Create and publish a listing](/collaboration/provider-listings-creating-publishing).
4. Select the listing to review.
5. Under Data Dictionary, select **Edit**.
6. Select the table or view to review.
7. Review the classification results.
   Columns containing PII or any other personal data are classified as “Contains PII”.
8. Select the **Data Preview** tab to preview the object’s content, which may include masked data.
9. If a column is not identified correctly:

   - If a column is mistakenly identified as containing PII, deselect the checkbox to the left of the **Name** column to ensure that the
     data in that column is unmasked in the Data Preview.
   - If a column contains PII but has not been identified as such, select the checkbox to the left of the **Name** column to ensure that
     the data in that column is masked in the Data Preview.
10. Select **Save**.
11. If you agree with the Data Classification, select **Save**.

Note

Data Preview content is generated when a data dictionary is enabled for a listing. Preview data for individual tables and views may not
be immediately available while data is generated.

It can take up to 3 to 4 hours for columns selected as PII in Provider Studio to display as masked on the consumer-facing listing.

##### Data preview refresh

If you add or remove objects in your listing, or change the schema of an object, the associated data preview will be refreshed, if enabled.
Updating the object data will not result in a data preview refresh.

Note

Data Previews are refreshed automatically approximately every few hours. You may not see the refreshed preview immediately after adding
or removing objects, or updating schemas. If the data within the existing objects (for example, rows in a table) is updated, but there
are no schema changes or new objects added, the data preview will not be refreshed immediately. In this case, the data preview will only
be updated during the next biweekly refresh.

#### Compliance certifications

If you’re a provider who has completed compliance certification by a third-party auditor, you can configure your listings to include this certification. You can add, edit, and remove compliance certifications directly in Provider Studio or through the listing manifest. When you provide the supporting compliance reports, Snowflake’s compliance team will review your submission. Upon approval, marketplace consumers can see your certifications in the Snowflake Marketplace, helping you build trust and transparency with potential consumers.

Consumers can filter Snowflake Marketplace listings by compliance certification, so adding certifications to your listings can increase their visibility to potential buyers.

Snowflake supports the following compliance certifications:

- FedRAMP
- GDPR
- HIPAA
- ISO 27001
- PCI DSS
- SOC 2

Note

Certifications are tied to listings and not to providers. Providers that have undergone compliance certification must submit proof of compliance for each of their listings.

##### Add compliance certifications by using Snowsight

To add compliance certifications when creating or configuring a listing by using Snowsight, follow these steps:

1. Sign in to Snowsight.
2. In the navigation menu, select **Marketplace –> Provider Studio**.
3. Select the **Listings** tab, then create a new listing or select an existing draft.
4. Set the profile and choose a product and access type.
5. In the optional **Certifications** section, add the certification for your listing. You can upload the supporting compliance documentation and set the expiration date for each certification.
6. Submit your listing for approval.

##### Add compliance certifications by using SQL

To create a listing that includes compliance badges by using SQL, follow these steps:

1. Using an approved [profile](/collaboration/provider-listings-preparing#label-set-up-access-listings), create your [listing manifest.yml](/progaccess/listing-manifest-reference).
2. In the manifest file, add the `compliance_badges` field and include a line for each certification type; for example:

   Copy code

   ```
   title: "My listing title"
   subtitle: "My listing subtitle"
   description: "My listing description"
   profile: "MyProfile"
   …
   compliance_badges:
   - type: SOC2
     expiry: 12-25-2026
     files:
    - soc2_compliance_verification.pdf
   - type: HIPAA
     expiry: 06-07-2026
     files:
    - hipaa_compliance_verification.pdf
   ```
3. Install and configure [SnowSQL](/user-guide/snowsql).
4. To connect to SnowSQL, run the following command:

   Copy code

   ```
   snowsql -c my_example_connection
   ```
5. To create a database, schema, and stage, run the following commands:

   Copy code

   ```
   CREATE DATABASE <db name>;
   CREATE SCHEMA <schema name>;
   CREATE STAGE <stage_name>;
   ```
6. To upload your listing manifest file from local to stage, run the following command:

   Copy code

   ```
   PUT file:///<local_path>/manifest.yml @<stage_name>/<prefix>
     SOURCE_COMPRESSION=None
     AUTO_COMPRESSION=False
     OVERWRITE=True;
   ```

   Note

   To use Snowsight to upload files to a stage, follow the steps in [Staging files using Snowsight](/user-guide/data-load-local-file-system-stage-ui).
7. To upload the compliance documents that are listed in manifest to stage, run the following commands:

   Copy code

   ```
   PUT file:///<local_path>/soc2_compliance_verification.pdf @<stage_name>/<prefix>
   PUT file:///<local_path>/hipaa_compliance_verification.pdf @<stage_name>/<prefix>
   PUT file:///<local_path>/sample.pdf @<stage_name>/<prefix>
     SOURCE_COMPRESSION=None
     AUTO_COMPRESSION=False
     OVERWRITE=True;
   ```
8. To verify that the files uploaded successfully and with the correct names, run the following command:

   Copy code

   ```
   LIST @<stage_name>/<prefix>;
   ```
9. To create a listing by using the manifest file you uploaded to the stage, use [CREATE LISTING](/sql-reference/sql/create-listing); for example:

   Copy code

   ```
   CREATE EXTERNAL LISTING <listing_name>
     APPLICATION PACKAGE <app package name>
     FROM @<staging_name>/<prefix>
     REVIEW = True
     PUBLISH = True;
   ```

##### Confirm that the compliance badge was added to the listing (SQL)

After you add a certification to a listing by using SQL, you can verify that it was added correctly:

1. Run the following command:

   Copy code

   ```
   DESCRIBE LISTING <listing_name> REVISION = DRAFT;
   ```
2. In the output, check the manifest.yml column for the `compliance_badges` section.

## 7. Additional public listing fields

Note

Region availability applies to public listings on the Snowflake Marketplace only.

### Region availability

Select the regions where your listing is available and how your data product
is fulfilled to consumers in those regions.

| Field | Description |
| --- | --- |
| **Region Availability** | By default, your listing is available in **All regions**. Choosing all regions ensures the availability of your listing in any future regions added by Snowflake. For paid listings, selecting this option makes the listing available in supported regions and any future supported regions added by Snowflake.  If your listing has specific regional limitations, select **All regions** to change the region availability to **Custom regions** and select the regions in which you want to offer your data product. When you choose custom regions, your listing is still visible in all Snowflake Marketplace regions, but consumers can only get your data product in the regions you specify. |
| **Fulfillment Method** | **Automatic** fulfillment is selected by default. With Cross-Cloud Auto-fulfillment, your data product is automatically fulfilled to a region and you incur costs only when there is consumer demand in that region. These costs cover transferring and storing your data product in other Snowflake regions. For a breakdown of these charges, see [Auto-fulfillment costs](/collaboration/provider-understand-cost-auto-fulfillment).  When you use auto-fulfillment, you must also select a refresh frequency at which to update the data product shared with consumers. You must select a refresh frequency of a maximum of 8 days. If your data product is a Snowflake Native App, you can only set a refresh frequency on the account level.  For more details on auto-fulfillment, see [Auto-fulfillment for listings](/collaboration/provider-listings-auto-fulfillment).  If you can’t use auto-fulfillment, select **Manual** to manually replicate your data product. To fulfill requests, you must set up accounts in regions with consumer demand, manually replicate the product to each account, create secure shares in each account, and attach those shares to this listing. See [Manually replicate data to fulfill a listing request](/collaboration/provider-listings-managing#label-manually-replicate-listing). |

Expand

Show lessSee more

## 8. Additional private listing fields

Note

The following sections apply to private listings shared directly with
specific consumers.

### Consumer accounts

To publish a listing to specific consumers, you must specify the account
identifiers for the accounts that you want to share with.

**Consumer Accounts**: Specifies the Snowflake accounts that you want to
share your private listing with. You can use Snowflake account identifiers
or URLs. See [Finding the organization and account name for an account](/user-guide/admin-account-identifier#label-account-name-find) for details.

**Example:** *ORGABC.ACCOUNT123*,
*https://<organization\_name>-<account\_name>.snowflakecomputing.com*

If you’re sharing with a consumer account in a different region, you must
also set up auto-fulfillment. See
[Auto-fulfillment for listings](/collaboration/provider-listings-auto-fulfillment) for more information.
