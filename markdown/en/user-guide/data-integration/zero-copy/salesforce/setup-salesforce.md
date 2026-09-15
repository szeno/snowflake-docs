# Set up Salesforce Data Cloud for Zero-Copy

This topic describes the steps a Salesforce administrator must perform in Salesforce Data Cloud to authorize the connection to Snowflake and make data products available for querying.

Complete these steps after the Snowflake administrator has created the Zerocopy Connector and provided the Enrollment ID. See [Set up the Salesforce Data Cloud Zerocopy Connector](/user-guide/data-integration/zero-copy/salesforce/setup).

## Prerequisites

Before starting, ensure:

- You have the **Data Cloud Architect** permission set in Salesforce.
- Your Salesforce org is enabled for the Snowflake V2 pilot.
- You have the **Enrollment ID** from your Snowflake administrator. This value is generated when the Zerocopy Connector is created in Snowflake and is available in Snowsight or via `SYSTEM$GET_ZEROCOPY_CONNECTOR_CONFIG`.

Note

If you have an existing data share linked to a legacy Snowflake data share target, migrate it to the Snowflake V2 data share target before proceeding. See [Migrate from the legacy Snowflake data share target](/user-guide/data-integration/zero-copy/salesforce/migrate-legacy-share) for the full procedure, including how to swap in the new database without breaking existing pipelines and dashboards.

## Create a Data Share

A Data Share defines which Salesforce Data 360 objects are made available to Snowflake. Each data share you link to the connector appears as a mountable data product on the Snowflake side.

Required permission: **Data Cloud Architect** permission set.

1. In Salesforce, navigate to **Data 360** » **Data Shares**.
2. Click **New**.
3. Enter the following details and click **Next**:

   - **Label**: Display name for the data share.
   - **Name**: API name. Auto-populated from the label; you can change it.
   - **Data Space**: Select **Default** if no other data space is provisioned in your org.
   - **Provide consent**: Check to allow admins or privileged users in the receiving Snowflake account to view and query all records of the data lake objects (DLOs) mapped to data model objects (DMOs) in the share.
   - **Description**: Optional.

Note

To comply with data policies and regulations, data sharing automatically includes the `IndividualGDPRState__dll` object, which provides consent information. Use the Individual ID to honor consent data for individuals at the share target.

4. Select the Data 360 objects to include in the data share.

Note

You can’t share an external data lake object (DLO) or a data model object (DMO) that is mapped to an external DLO.

5. Click **Save**.

## Create a Data Share Target

A Data Share Target represents the Snowflake account that receives the shared data. The Enrollment ID from Snowflake authorizes the connection.

Required permission: **Data Cloud Architect** permission set.

1. In Salesforce, navigate to **Data Cloud** » **Data Share Targets**.
2. Click **New**.
3. For the connection type, select **Snowflake V2** and click **Next**.
4. Enter the following details:

   - **Label**: Display name for the data share target.
   - **API Name**: Auto-populated from the label; you can change it.
   - **Enrollment ID**: Paste the Enrollment ID provided by your Snowflake administrator.
   - **Description**: Optional.
5. Click **Save**.

## Link the Data Share to the Data Share Target

Linking makes the data share available to the connected Snowflake account. Until a data share is linked to a target, it doesn’t appear in Snowflake.

Required permission: **Data Cloud Architect** permission set.

1. In Salesforce, navigate to **Data 360** » **Data Shares**.
2. Click the data share you want to link.
3. On the data share record, click **Link/Unlink Data Share Target**.
4. Select the Snowflake V2 data share target you created in the previous step.

   To unlink, follow the same process and deselect the target instead.
5. Click **Save**.

Important

Don’t unlink a data share from a legacy Snowflake data share target before confirming the Snowflake V2 link is working. Downstream processes in Snowflake may still reference the database created from the legacy target.

After linking, the data shares will appear in the Zerocopy Connector in Snowflake. To confirm, use `SYSTEM$ZEROCOPY_CONNECTOR_LIST_SHARES`. Linked data share targets are listed on the data share record home page.

## Next steps

Return to Snowflake to list available data products and create catalog-linked databases. See [Explore data products from Salesforce Data Cloud](/user-guide/data-integration/zero-copy/salesforce/explore-data-products).
