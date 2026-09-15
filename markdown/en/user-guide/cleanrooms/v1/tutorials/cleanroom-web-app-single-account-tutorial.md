# Tutorial: Create and run a clean room using the clean rooms UI and a single account

## Introduction

End-of-life notice

The legacy Provider and Consumer Data Clean Rooms are being discontinued. Migrate to the
[Collaboration API](/user-guide/cleanrooms/overview) using the
[migration tool](/user-guide/cleanrooms/migration-tool) before the dates below.

- **2026-10-01:** New legacy clean rooms may not be created via the
  [web application user interface](/user-guide/cleanrooms/v1/web-app-introduction).
- **2027-02-01:** The [web application user interface](/user-guide/cleanrooms/v1/web-app-introduction)
  will no longer be accessible, and new legacy clean rooms may not be created via the
  [Provider and Consumer API](/user-guide/cleanrooms/getting-started).
- **2027-06-01:** Legacy [Provider and Consumer clean rooms](/user-guide/cleanrooms/getting-started)
  will no longer be accessible. Use the [Collaboration API](/user-guide/cleanrooms/overview)
  to create and manage clean rooms.

This tutorial leads you through the basic steps to create and use a clean room using the clean rooms UI. Clean rooms enable users to
share data with a collaborator while maintaining the privacy of the data by tightly controlling what can be done with it.

### What you’ll learn

In this tutorial, you will learn how to use the clean rooms UI by doing the following actions:

- Add a collaborator to your clean room environment. In this tutorial, you will add yourself as a collaborator.
- Create a clean room, including how to add data, specify join policies, define which type of analysis a collaborator can run on the data,
  and share the clean room with a collaborator.
- Install a clean room, add data, and define how this data is joined with the collaborator’s data.
- Run an analysis.
- Activate the results of the analysis.

### About clean room collaborators

Clean room collaborators are either providers or consumers:

- A *provider* is the account that creates and configures the clean room. In a typical clean room, the provider adds all the SQL templates
  that the consumer can run in the clean room. The provider adds data, sets usage restrictions on it, and invites consumers, who can
  join the clean room to run the templates.
- A *consumer* is the account invited to participate in the clean room. The consumer adds their own data and runs the templates on the
  clean room data, according to the limitations set by the provider.

In this tutorial, you act as both the provider and the consumer in the clean room. In a real world clean room, the provider and consumer
would use separate accounts.

### Prerequisites

- You must have access to a Snowflake environment with the Snowflake Data Clean Rooms UI installed. You must either
  [install the environments yourself](/user-guide/cleanrooms/installing-dcr), or ask an administrator to
  [grant you access to the clean rooms UI in a Snowflake account](/user-guide/cleanrooms/manage-dcr-users#label-cleanrooms-get-started-add-users).
- This tutorial uses a sample table named CUSTOMERS\_2. Either search Snowsight for the table
  SAMOOHA\_SAMPLE\_DATABASE.DEMO.CUSTOMERS\_2, or run the following SQL command in your Snowflake account to confirm that you have this
  table installed:

  Copy code

  ```
  SHOW TABLES LIKE 'CUSTOMERS_2' IN SCHEMA SAMOOHA_SAMPLE_DATABASE.DEMO;
  ```

  If the response has no rows, then you, or someone with ACCOUNTADMIN role, must run the following command to install the sample table:

  Copy code

  ```
  USE ROLE ACCOUNTADMIN;
  EXECUTE IMMEDIATE FROM @SAMOOHA_BY_SNOWFLAKE.APP_SCHEMA.MOUNT_CODE_STAGE/dcr_loader.sql;
  ```

Note

This tutorial uses a single account for both the provider and consumer in the clean room. This type of clean room,
an *internal testing clean room*, is for testing purposes only, and can’t later be used in production or shared with other accounts.
Internal testing clean rooms support [most, but not all clean room features](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-self-share-for-developers). If you would
like to try using clean rooms two separate Snowflake accounts, try the [two-account tutorial](/user-guide/cleanrooms/v1/tutorials/cleanroom-web-app-tutorial).

## Sign in to the clean rooms UI

End-of-life notice

The legacy Provider and Consumer Data Clean Rooms are being discontinued. Migrate to the
[Collaboration API](/user-guide/cleanrooms/overview) using the
[migration tool](/user-guide/cleanrooms/migration-tool) before the dates below.

- **2026-10-01:** New legacy clean rooms may not be created via the
  [web application user interface](/user-guide/cleanrooms/v1/web-app-introduction).
- **2027-02-01:** The [web application user interface](/user-guide/cleanrooms/v1/web-app-introduction)
  will no longer be accessible, and new legacy clean rooms may not be created via the
  [Provider and Consumer API](/user-guide/cleanrooms/getting-started).
- **2027-06-01:** Legacy [Provider and Consumer clean rooms](/user-guide/cleanrooms/getting-started)
  will no longer be accessible. Use the [Collaboration API](/user-guide/cleanrooms/overview)
  to create and manage clean rooms.

[Sign in to the clean rooms UI.](/user-guide/cleanrooms/web-app-introduction#label-cleanroom-web-app-sign-in) Provide your Snowflake account credentials for an account where you
can act as a clean rooms provider. A provider has permission to create a clean room.

## Provider: Create and share a clean room

End-of-life notice

The legacy Provider and Consumer Data Clean Rooms are being discontinued. Migrate to the
[Collaboration API](/user-guide/cleanrooms/overview) using the
[migration tool](/user-guide/cleanrooms/migration-tool) before the dates below.

- **2026-10-01:** New legacy clean rooms may not be created via the
  [web application user interface](/user-guide/cleanrooms/v1/web-app-introduction).
- **2027-02-01:** The [web application user interface](/user-guide/cleanrooms/v1/web-app-introduction)
  will no longer be accessible, and new legacy clean rooms may not be created via the
  [Provider and Consumer API](/user-guide/cleanrooms/getting-started).
- **2027-06-01:** Legacy [Provider and Consumer clean rooms](/user-guide/cleanrooms/getting-started)
  will no longer be accessible. Use the [Collaboration API](/user-guide/cleanrooms/overview)
  to create and manage clean rooms.

In this section, you will do the following actions as a provider:

- Create a clean room.
- Add data to the clean room that is being shared with collaborators.
- Define a join policy, which controls which columns a collaborator can join their own data with.
- Define which types of analyses a collaborator can run in the clean room.
- Share the clean room with the consumer.

### Start the creation process

To begin the process of creating a clean room:

1. In the left navigation, select **Clean Rooms**.
2. On the **Clean Rooms** page, select **+ Clean Room**.
3. Name your clean room `Tutorial`.

   You will allow collaborators to run an audience overlap analysis in the clean room.

### Add data to your clean room

To add data to your clean room:

1. In the **Datasource** section, select `Snowflake`.
2. From the **Tables** drop-down list, select the SAMOOHA\_SAMPLE\_DATABASE.DEMO.CUSTOMERS table.
3. Select **Next**.

Note

If a table added here is deleted, renamed, moved, or has restrictive permissions added, the table will no longer be usable in the clean
room unless you restore the old table with the same location, name, and permissions.

### Specify a join policy

A *join policy* specifies which columns of your data a collaborator can join on.

To specify a join policy:

1. From the **Join Columns** drop-down list, select the following columns:

   - `HASHED_EMAIL`
   - `HASHED_FIRST_NAME`
   - `HASHED_LAST_NAME`
   - `HASHED_PHONE`

   A collaborator can join their data with these columns only.
2. Select **Next**.

### Configure an analysis template

*Analysis templates* control how a collaborator can access the shared data in a clean room. Collaborators can only run analyses and queries
that conform to the template.

Select and configure an analysis template for clean room collaborators:

1. Select the `Audience Overlap & Segmentation` template.

   Collaborators are limited to running only the analyses that you select.
2. From the **Tables** drop-down list, select DEMO.CUSTOMERS.

   Collaborators can only analyze data in the DEMO.CUSTOMERS table.
3. From the **Segmentation & Attribute Columns** drop-down list, select the following columns:

   - `AGE_BAND`
   - `DEVICE_TYPE`
   - `EDUCATION_LEVEL`
   - `STATUS`

   A consumer can filter and create segments using these columns.
4. Enable **Allow categorical value previews during filtering**.
5. Select **Next**.

### Share and publish the clean room

Now that you have created and configured the clean room, you can share it with a collaborator so they can use it to run analyses.

To share the clean room with yourself:

1. Enable the **Enable Internal Test Clean Room** setting.
2. Select **Finish**.
3. In the dialog that opens, read the notes, then select **Proceed** to create the clean room.

Note

If you were sharing this clean room with another account, you would take the following steps:

1. In the **Select Collaborator** drop-down list, select the consumer’s account name.
2. Select **Finish**.

### Monitor the status of the clean room

It takes a few minutes for the clean room to be created. During this time a **Processing** label is shown on the clean room tile in
the **Created** tab.

To check for status changes:

- Every few minutes, select **Refresh**

  When the tile label changes from **Processing** to an **Edit** button, you can continue to the consumer steps.

## Consumer: Install and configure the clean room

End-of-life notice

The legacy Provider and Consumer Data Clean Rooms are being discontinued. Migrate to the
[Collaboration API](/user-guide/cleanrooms/overview) using the
[migration tool](/user-guide/cleanrooms/migration-tool) before the dates below.

- **2026-10-01:** New legacy clean rooms may not be created via the
  [web application user interface](/user-guide/cleanrooms/v1/web-app-introduction).
- **2027-02-01:** The [web application user interface](/user-guide/cleanrooms/v1/web-app-introduction)
  will no longer be accessible, and new legacy clean rooms may not be created via the
  [Provider and Consumer API](/user-guide/cleanrooms/getting-started).
- **2027-06-01:** Legacy [Provider and Consumer clean rooms](/user-guide/cleanrooms/getting-started)
  will no longer be accessible. Use the [Collaboration API](/user-guide/cleanrooms/overview)
  to create and manage clean rooms.

In this step, you switch from acting as the provider, who creates and shares a clean room, to acting as the consumer, who installs and
runs the clean room. Because this is an internal testing clean room, you will use the same Snowflake account for the provider and consumer.

As a consumer, you will do the following actions:

- Install the clean room that was shared with you by the provider.
- Add data to the clean room so that it can be joined with the provider’s data.
- Add a join policy to define how the consumer’s data and the provider’s data are related.
- Define the columns that analysts can use to create segments, filter results, and enrich activation data.

### Install the clean room as a consumer

Installation in the UI involves joining, configuring, and then installing the clean room.

To configure the clean room:

1. In the left navigation, select **Clean Rooms**.
2. Select the **Invited** tab.
3. Find the `Tutorial` tile, and select **Join**.

   If the clean room isn’t in your **Invited** tab, select **Refresh**. If it’s still not there, confirm that the clean room has an
   **Edit** button in the **Created** tab. If there is no edit button, you didn’t create the clean room as a provider.

### Add consumer data to the clean room

To add data to the clean room:

1. In the **Datasource** section, select `Snowflake`.
2. From the **Tables** drop-down list, select and then save SAMOOHA\_SAMPLE\_DATABASE.DEMO.CUSTOMERS\_2.

   - If this table is not in your list, see the Prerequisites section in the tutorial introduction to learn how to install it.
3. Select **Next**.

Note

If a table added here is deleted, renamed, moved, or has restrictive permissions added, the table will no longer be usable in the clean
room unless you restore the old table with the same location, name, and permissions.

### Define a join policy

Next, specify which consumer columns are joinable in an analysis or query in this clean room:

1. In the **Specify Join Policies** pane, in the **Join Policies** section, choose columns from your data (labeled **My Columns**)
   and equivalent columns from the provider’s table (labeled **Collaborator Columns**).
2. Ensure that the columns from the consumer’s table (**My Columns**) and the columns from the provider’s table
   (**Collaborator Columns**) match in content (the column names don’t need to match).

   For example, the consumer’s `HASHED_EMAIL` column should be joined with the provider’s
   `HASHED_EMAIL` column. All joined columns must match in the analysis that you select.
3. Select **Next** to navigate to the **Configure Analysis & Query** pane.

### Define the segmentation and activation columns

When you select segmentation and activation columns during the clean room installation process, you define which columns are available to
users running an analysis in the clean room. Analysts can create segments based only on these columns. When you send activation data back
to the provider, analysts can’t enrich the results of the analysis with data unless the data comes from one of these columns.

To define the segmentation and activation columns:

1. Select and then save the DEMO.CUSTOMERS\_2 table from the **Tables** drop-down list.
2. From the **Segmentation & Attribute Columns** drop-down list, select and then save the following columns:

   - `INCOME_BRACKET`
   - `REGION_CODE`
   - `STATUS`
3. Select **Finish** to install the clean room.

   Installation takes a few minutes to complete.
4. Select **Refresh** every few minutes to check for changes.

   When the tile label changes from **Processing** to a **Run** button, the clean room is installed and you can run an analysis.

## Consumer: Run an analysis

End-of-life notice

The legacy Provider and Consumer Data Clean Rooms are being discontinued. Migrate to the
[Collaboration API](/user-guide/cleanrooms/overview) using the
[migration tool](/user-guide/cleanrooms/migration-tool) before the dates below.

- **2026-10-01:** New legacy clean rooms may not be created via the
  [web application user interface](/user-guide/cleanrooms/v1/web-app-introduction).
- **2027-02-01:** The [web application user interface](/user-guide/cleanrooms/v1/web-app-introduction)
  will no longer be accessible, and new legacy clean rooms may not be created via the
  [Provider and Consumer API](/user-guide/cleanrooms/getting-started).
- **2027-06-01:** Legacy [Provider and Consumer clean rooms](/user-guide/cleanrooms/getting-started)
  will no longer be accessible. Use the [Collaboration API](/user-guide/cleanrooms/overview)
  to create and manage clean rooms.

In this step, you run an audience overlap and segmentation analysis in the clean room. You must first select the data to use in the
analysis.

To configure and run an analysis:

1. In the **Joined** tab, find the clean room tile and then select **Run**.
2. Select **Audience Overlap & Segmentation** » **Proceed**.
3. In **My Tables**, select CUSTOMERS.
4. In **Collaborator’s Tables**, select CUSTOMERS.
5. In **Required Parameters** » **My Join Columns**, define the following joins:

   1. From the drop-down list, select and then save `HASHED_EMAIL`.
   2. Select **+ Join Column**, then select `HASHED_FIRST_NAME` and `HASHED_LAST_NAME`.
   3. Select **+ Join Column**, then select `HASHED_PHONE`.

   When you run an analysis in the clean room, results include records where any of the following items are true:

   - The consumer’s `HASHED_EMAIL` matches the provider’s `HASHED_EMAIL`.
   - The consumer’s `HASHED_FIRST_NAME` matches the provider’s `HASHED_FIRST_NAME` and the consumer’s `HASHED_LAST_NAME`
     matches the provider’s `HASHED_LAST_NAME`.
   - The consumer’s `HASHED_PHONE` matches the provider’s `HASHED_PHONE`.
6. In the **User Segmentation** section, perform the following steps:

   1. From the **My Columns** drop-down list, select `INCOME_BRACKET`.
   2. From the **Collaborator Columns** drop-down list, select `AGE_BAND`.

   The results of the analysis are grouped into these segments.
7. In the **Filters** section, use the drop-down lists to specify `CUSTOMERS.STATUS = GOLD`.

   This limits analysis results to results where `STATUS = GOLD`.
8. Select **Run**.

   You can optionally choose a different warehouse size to run the analysis by changing the **Warehouse**
   drop-down selection.
9. In the **Analyses & Queries** page, when the status of your analysis is **Completed**:

   1. Select the analysis to see your results.
   2. Scroll to the **Results** section of the page. You can toggle the results to see either overlap or non-overlap rates.
   3. To see the segmentation groups of your analysis, select **Download**, and then open the comma-delimited file.
10. Continue to the next step to activate (send) enriched results to the consumer’s Snowflake account.

## Consumer: Activate the results to the consumer account

End-of-life notice

The legacy Provider and Consumer Data Clean Rooms are being discontinued. Migrate to the
[Collaboration API](/user-guide/cleanrooms/overview) using the
[migration tool](/user-guide/cleanrooms/migration-tool) before the dates below.

- **2026-10-01:** New legacy clean rooms may not be created via the
  [web application user interface](/user-guide/cleanrooms/v1/web-app-introduction).
- **2027-02-01:** The [web application user interface](/user-guide/cleanrooms/v1/web-app-introduction)
  will no longer be accessible, and new legacy clean rooms may not be created via the
  [Provider and Consumer API](/user-guide/cleanrooms/getting-started).
- **2027-06-01:** Legacy [Provider and Consumer clean rooms](/user-guide/cleanrooms/getting-started)
  will no longer be accessible. Use the [Collaboration API](/user-guide/cleanrooms/overview)
  to create and manage clean rooms.

In this step, you activate the results of your analysis by pushing them to the consumer’s Snowflake account. These results are
enriched with data from the consumer and provider tables.

To activate the results of the analysis:

1. In the **Results** section for the analysis, select **Activate**.
2. In the **Activation Hub** section, select the name of your account.

   This section lists accounts and services where you can activate
   data to. The list can include [third-party activation connectors](/user-guide/cleanrooms/connector-activation) that send data
   to services outside of Snowflake.
3. In the **Segment Name** field, enter `My test segment`, or another unique name for this result set.

   Copy and save the segment name that you provide here.
4. From the **ID Columns** drop-down list, select `HASHED_EMAIL`.
5. From the **Attribute Columns** drop-down list, select **Select All**.

   When you look at the results of the analysis, the matched records will be enriched with data from both consumer and provider tables.

   The available columns are the same as the segmentation and activation columns that you selected as the consumer when you installed the
   clean room.
6. Select **Push Data**.

Congratulations! You have now installed and configured a clean room in a consumer account, run an analysis, and pushed the results to
the consumer account for activation.

## View the activated data

End-of-life notice

The legacy Provider and Consumer Data Clean Rooms are being discontinued. Migrate to the
[Collaboration API](/user-guide/cleanrooms/overview) using the
[migration tool](/user-guide/cleanrooms/migration-tool) before the dates below.

- **2026-10-01:** New legacy clean rooms may not be created via the
  [web application user interface](/user-guide/cleanrooms/v1/web-app-introduction).
- **2027-02-01:** The [web application user interface](/user-guide/cleanrooms/v1/web-app-introduction)
  will no longer be accessible, and new legacy clean rooms may not be created via the
  [Provider and Consumer API](/user-guide/cleanrooms/getting-started).
- **2027-06-01:** Legacy [Provider and Consumer clean rooms](/user-guide/cleanrooms/getting-started)
  will no longer be accessible. Use the [Collaboration API](/user-guide/cleanrooms/overview)
  to create and manage clean rooms.

In the previous step you activated to the consumer’s Snowsight account. Here is how to view the activated data by using either the
Snowflake web application or code:

SnowsightSQL

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) with the same account where you ran the clean room. Use the Snowflake UI, not the clean
   rooms UI.
2. In the navigation menu, select **Catalog** » **Database Explorer**.
3. Search for `SAMOOHA_BY_SNOWFLAKE_LOCAL_DB`.
4. Navigate to **PUBLIC** » **Tables** » **CONSUMER\_DIRECT\_ACTIVATION\_SUMMARY**.
5. Select **Data Preview** to view the activation data.
   - If you don’t see data there, confirm that you are using the same Snowflake account that you used to activate your data.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) with the same account where you ran the clean room. Use the Snowflake UI, not the clean
   rooms UI.
2. In the navigation menu, select **Projects** » **Worksheets**.
3. Select **+ SQL Worksheet**.
4. to list the activation data that was pushed to the consumer’s clean room environment, paste and run the following statement
   into the new worksheet. Substitute the segment name that you entered when you ran the activation in the clean rooms UI.

   Copy code

   ```
   SELECT *
   FROM SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.PUBLIC.CONSUMER_DIRECT_ACTIVATION_SUMMARY
   WHERE segment = '<your segment name>';
   ```

   If you don’t see data, confirm that you are using the same Snowflake account that you used to activate your data, and that you
   are using the segment name that you specified when you activated the results.

## Clean up

End-of-life notice

The legacy Provider and Consumer Data Clean Rooms are being discontinued. Migrate to the
[Collaboration API](/user-guide/cleanrooms/overview) using the
[migration tool](/user-guide/cleanrooms/migration-tool) before the dates below.

- **2026-10-01:** New legacy clean rooms may not be created via the
  [web application user interface](/user-guide/cleanrooms/v1/web-app-introduction).
- **2027-02-01:** The [web application user interface](/user-guide/cleanrooms/v1/web-app-introduction)
  will no longer be accessible, and new legacy clean rooms may not be created via the
  [Provider and Consumer API](/user-guide/cleanrooms/getting-started).
- **2027-06-01:** Legacy [Provider and Consumer clean rooms](/user-guide/cleanrooms/getting-started)
  will no longer be accessible. Use the [Collaboration API](/user-guide/cleanrooms/overview)
  to create and manage clean rooms.

You can delete the clean room and activation data that you created for this tutorial to clean up your production environment.

### Delete the activation data

To delete the activation data from the provider’s Snowflake account:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) for the provider account. Sign in to the **Snowflake UI**, not the clean rooms UI.
2. In the navigation menu, select **Projects** » **Worksheets**.
3. Select **+ SQL Worksheet**.
4. In the new worksheet, paste and run the following statement to delete the activation data created for this tutorial.
   Substitute your custom segment name in the location indicated:

   Copy code

   ```
   DELETE FROM SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.PUBLIC.CONSUMER_DIRECT_ACTIVATION_SUMMARY
   WHERE segment = '<your segment name>';
   ```

### Delete the clean room

Deleting a clean room in the provider account removes it from both the provider account and the consumer account.

To delete a clean room:

1. In the clean rooms UI, in the left navigation, select **Clean Rooms**.
2. In the **Created** tab, find the clean room tile.
3. Select [![Three vertical dots indicating more options](/static/images/icons/vertical-more-icon.png)](/static/images/icons/vertical-more-icon.png) » **Delete** » **Proceed**.

## Learn more

End-of-life notice

The legacy Provider and Consumer Data Clean Rooms are being discontinued. Migrate to the
[Collaboration API](/user-guide/cleanrooms/overview) using the
[migration tool](/user-guide/cleanrooms/migration-tool) before the dates below.

- **2026-10-01:** New legacy clean rooms may not be created via the
  [web application user interface](/user-guide/cleanrooms/v1/web-app-introduction).
- **2027-02-01:** The [web application user interface](/user-guide/cleanrooms/v1/web-app-introduction)
  will no longer be accessible, and new legacy clean rooms may not be created via the
  [Provider and Consumer API](/user-guide/cleanrooms/getting-started).
- **2027-06-01:** Legacy [Provider and Consumer clean rooms](/user-guide/cleanrooms/getting-started)
  will no longer be accessible. Use the [Collaboration API](/user-guide/cleanrooms/overview)
  to create and manage clean rooms.

Congratulations! You have now used the clean rooms UI to create and share a clean room as a provider. You have also acted as a consumer
who is using the clean room to analyze data within a privacy-preserving environment.

For more information about Snowflake Data Clean Rooms, see the following resources:

- For general information, see [Overview of Provider and Consumer Clean Rooms](/user-guide/cleanrooms/getting-started).
- For more information about the clean rooms UI, see [Legacy Clean Rooms UI overview](/user-guide/cleanrooms/v1/web-app-introduction).
- For information about using the developer APIs to work with a Snowflake Data Clean Room programmatically, see
  [Snowflake Data Clean Rooms developer’s guide](/user-guide/cleanrooms/v1/developer-introduction).
