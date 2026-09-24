# Tutorial: Create and run a clean room using the clean rooms UI and two accounts

## Introduction

End-of-life notice

The legacy Provider and Consumer Data Clean Rooms are being discontinued. See the
[end-of-life timeline](/user-guide/cleanrooms/pc-eol) for dates and migration guidance.

Clean rooms enable users to share data with a collaborator while maintaining the privacy of the data by tightly controlling what can be
done with it. This tutorial leads you through the basic flow of using the clean rooms UI to work with a Snowflake Data Clean Room with two test
accounts, which enable the full functionality of clean rooms. If have access to only a single Snowflake account with clean rooms installed,
you can try the [single-account tutorial](/user-guide/cleanrooms/v1/tutorials/cleanroom-web-app-single-account-tutorial) instead.

### What you will learn

In this tutorial, you will learn how to use the clean rooms UI by doing the following tasks:

- Add a collaborator to your clean rooms environment.
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

### Prerequisites

- You must have access to two Snowflake environment with the Snowflake Data Clean Rooms UI installed: one to use as a provider, and the
  other to use as a consumer. You must either [install the environments yourself](/user-guide/cleanrooms/installing-dcr), or ask an
  administrator to [grant you access to the clean rooms UI in a Snowflake account](/user-guide/cleanrooms/manage-dcr-users#label-cleanrooms-get-started-add-users).
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

## Provider: Sign in to the clean rooms UI

End-of-life notice

The legacy Provider and Consumer Data Clean Rooms are being discontinued. See the
[end-of-life timeline](/user-guide/cleanrooms/pc-eol) for dates and migration guidance.

Sign in to the clean room where you will create, configure, and share a clean room as a provider.

[Sign in to the clean rooms UI.](/user-guide/cleanrooms/web-app-introduction#label-cleanroom-web-app-sign-in) Provide your Snowflake account credentials for the account that
will act as the provider.

## Provider: Add the consumer as a collaborator

End-of-life notice

The legacy Provider and Consumer Data Clean Rooms are being discontinued. See the
[end-of-life timeline](/user-guide/cleanrooms/pc-eol) for dates and migration guidance.

In this section you will add the consumer account that you are using for this tutorial as a collaborator. Administrators must define
someone as a collaborator *before* other users can share a clean room with that collaborator.

To add the consumer as a collaborator:

1. In the left navigation, select **Collaborators**.
2. Select the **Snowflake Partners** tab.
3. Select **+ Snowflake Partner**.
4. In the **Company Name** field, enter `Tutorial Consumer`.
5. In the **Email Address** field, enter the email associated with your clean room user.
6. In the **Account Locator** field, enter the
   [account locator](/user-guide/admin-account-identifier#label-account-locator) of the Snowflake account that you are using as a consumer.
7. Select the cloud and region of the account that hosts your consumer account.
8. Select **Add**.

## Provider: Create and share a clean room

End-of-life notice

The legacy Provider and Consumer Data Clean Rooms are being discontinued. See the
[end-of-life timeline](/user-guide/cleanrooms/pc-eol) for dates and migration guidance.

In this section, you will do the following:

- Create a clean room.
- Add data to the clean room that is shared with collaborators.
- Define a join policy, which controls which columns a collaborator can join with their own data.
- Define which types of analysis a collaborator can run in the clean room.
- Share the clean room with the consumer.

### Start the creation process

To begin the process of creating a clean room:

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
room unless you restore the old table at the same location, name, and permissions.

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

To share a clean room:

1. Use the **Select Collaborator** drop-down list to select `Tutorial Consumer`.
2. Select **Finish**.
3. Wait until the clean room is created before continuing with this tutorial. Periodically select **Refresh** until the
   `Tutorial` tile changes from **Processing** to **Edit**.

Congratulations! You have created and shared a Snowflake Data Clean Room.

Next, you will switch to act as the consumer who joins the clean room and uses it to analyze data.

## Consumer: Sign in to the clean rooms UI

End-of-life notice

The legacy Provider and Consumer Data Clean Rooms are being discontinued. See the
[end-of-life timeline](/user-guide/cleanrooms/pc-eol) for dates and migration guidance.

In this section, you switch from being the provider who created and shared the clean room to acting as the consumer to install and run the
clean room.

- [Sign in to the clean rooms UI.](/user-guide/cleanrooms/web-app-introduction#label-cleanroom-web-app-sign-in) Provide the Snowflake account credentials for the account that
  acts as the consumer.

## Consumer: Install and configure the clean room

End-of-life notice

The legacy Provider and Consumer Data Clean Rooms are being discontinued. See the
[end-of-life timeline](/user-guide/cleanrooms/pc-eol) for dates and migration guidance.

In this section you will do the following actions:

- Install the clean room that was shared with you from the provider account.
- Add data to the clean room so it can be joined with the provider’s data.
- Add a join policy to define how the consumer data and the provider data are related.
- Define the columns that analysts can use to create segments, filter results, and enrich activation data.

### Start the installation process

To start installing a clean room that has been shared by the provider account:

1. In the left navigation, select **Clean Rooms**.
2. Select the **Invited** tab.
3. Find the `Tutorial` tile, and select **Join**.

### Add consumer data to the clean room

To add data to the clean room:

1. In the **Datasource** section, select `Snowflake`.
2. From the **Tables** drop-down list, select and then save SAMOOHA\_SAMPLE\_DATABASE.DEMO.CUSTOMERS\_2.

   - If this table is not in your list, see the Prerequisites section in the tutorial introduction to learn how to install it.
3. Select **Next**.

Note

If a table added here is deleted, renamed, moved, or has restrictive permissions added, the table will no longer be usable in the clean
room unless you restore the old table at the same location, name, and permissions.

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

When you select segmentation and activation columns during the clean room installation process, you define which columns are
available to users running an analysis in the clean room. Analysts can create segments based on only these columns. When you send
activation data back to the provider, analysts cannot enrich the results of the analysis with data unless it comes from one of these
columns.

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

The legacy Provider and Consumer Data Clean Rooms are being discontinued. See the
[end-of-life timeline](/user-guide/cleanrooms/pc-eol) for dates and migration guidance.

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

## Consumer: Activate the results

End-of-life notice

The legacy Provider and Consumer Data Clean Rooms are being discontinued. See the
[end-of-life timeline](/user-guide/cleanrooms/pc-eol) for dates and migration guidance.

In this step you will activate the results of your analysis to the provider’s Snowflake account. These results are enriched with data from
the consumer and provider tables.

To activate the results of the analysis:

1. In the **Results** section, select **Activate**.
2. Select the name of the provider account you used to share the clean room.
3. In the **Segment Name** field, specify `My test segment`, or another unique name for this result set.
4. From the **ID Columns** drop-down list, select `HASHED_EMAIL`.
5. From the **Attribute Columns** drop-down list, select **Select All**.

   When the provider looks at the results of the analysis, the matched records will be enriched with the additional data found in these
   columns.

   The available columns are the same as the segmentation and activation columns that you selected as the consumer when you installed the
   clean room.
6. Select **Push Data**.

Congratulations! You have now installed and configured a clean room in a consumer account, run an analysis, and pushed the results back to
the provider account for activation.

## Provider: View the activated data

End-of-life notice

The legacy Provider and Consumer Data Clean Rooms are being discontinued. See the
[end-of-life timeline](/user-guide/cleanrooms/pc-eol) for dates and migration guidance.

In the previous step you activated to the provider’s Snowsight account. Provider activation
data is stored in the SAMOOHA\_BY\_SNOWFLAKE\_LOCAL\_DB.PUBLIC.PROVIDER\_ACTIVATION\_SUMMARY table of the provider’s Snowflake account.

**Prerequisite**

The first time a consumer activates data to a provider’s account, the provider must sign in to the clean rooms UI for about 30 minutes
*after* the consumer has activated data. This is needed only once per clean room per consumer account. Later activations by the same
consumer in the same clean room do not need this step. To activate data to the provider’s account you must create a pipeline between the
consumer account and the provider account.

After this prerequisite step, you can view the activated data in your provider account using either Snowsight or SQL:

SnowsightSQL

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) for the provider account. (Use the **Snowflake UI**, not the clean room UI.)
   environment.
2. In the navigation menu, select **Catalog** » **Explorer**.
3. Navigate to `SAMOOHA_BY_SNOWFLAKE_LOCAL_DB` » `PUBLIC` » `Tables` » `PROVIDER_ACTIVATION_SUMMARY`.
4. Select **Data Preview** to view the activation data.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) for the provider account. You are signing in to the Snowflake account, not the clean room
   environment.
2. In the navigation menu, select **Projects** » **Worksheets**.
3. Select **+ SQL Worksheet**.
4. In the new worksheet, paste and run the following statement to list the activation data that was pushed from the consumer’s
   clean room environment. Substitute the segment name that you entered when you ran the activation in the clean rooms UI.

   Copy code

   ```
   SELECT *
   FROM SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.PUBLIC.PROVIDER_ACTIVATION_SUMMARY
   WHERE segment = '<your segment name>';
   ```

## Clean up

End-of-life notice

The legacy Provider and Consumer Data Clean Rooms are being discontinued. See the
[end-of-life timeline](/user-guide/cleanrooms/pc-eol) for dates and migration guidance.

You can delete the clean room and activation data that you created for this tutorial to clean up your production environment.

### Delete the activation data

To delete the activation data from the provider’s Snowflake account:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) for the provider account. You are signing in to the Snowflake account, not the clean room environment.
2. In the navigation menu, select **Projects** » **Worksheets**.
3. Select **+ SQL Worksheet**.
4. In the new worksheet, paste and run the following statement to delete the activation data created for this tutorial.
   Substitute your custom segment name in the location indicated:

   Copy code

   ```
   DELETE FROM SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.PUBLIC.PROVIDER_ACTIVATION_SUMMARY
   WHERE segment = '<your segment name>';
   ```

### Delete the clean room

Deleting a clean room in the provider account removes it from both the provider account and the consumer account.

To delete a clean room:

1. [Sign in to the clean rooms UI.](/user-guide/cleanrooms/web-app-introduction#label-cleanroom-web-app-sign-in)
2. In the left navigation, select **Clean Rooms**.
3. On the **Created** tab, find the `Tutorial` tile and select the More icon ([![Three vertical dots indicating more options](/static/images/icons/vertical-more-icon.png)](/static/images/icons/vertical-more-icon.png)).
4. Select **Delete**.
5. Select **Proceed**.

## Learn more

End-of-life notice

The legacy Provider and Consumer Data Clean Rooms are being discontinued. See the
[end-of-life timeline](/user-guide/cleanrooms/pc-eol) for dates and migration guidance.

Congratulations! You have now used the clean rooms UI to create and share a clean room as a provider. You have also acted as the consumer
who is using the clean room to analyze data within a privacy-preserving environment.

You can use the following resources to learn more:

- For general information, see [Overview of Snowflake Data Clean Rooms](/user-guide/cleanrooms/overview).
- For more information about the clean rooms UI, see [Legacy Clean Rooms UI overview](/user-guide/cleanrooms/v1/web-app-introduction).
- For information about using the developer APIs to work with a Snowflake Data Clean Room programmatically, see
  [Snowflake Data Clean Rooms developer’s guide](/user-guide/cleanrooms/v1/developer-introduction).
