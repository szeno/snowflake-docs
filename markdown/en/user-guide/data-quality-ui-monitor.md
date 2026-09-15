# Monitoring data quality checks in Snowsight

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

You can use a Snowsight page to monitor the quality of data in a table or view. It provides an
interactive view of the data metric functions (DMFs) that are associated with an object, including insights about the results of those DMFs.

To gain a better understanding of data quality and DMFs, see [Introduction to data quality checks](/user-guide/data-quality-intro).

To monitor data quality health across all schemas and tables in your account from a single page, see
[Using the data quality monitoring dashboard](/user-guide/data-quality-centralized-dashboard).

## Get started

To start gaining insights into the data quality of an object, do the following:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Catalog** » **Database Explorer**, and then select the object.
3. Select the **Data Quality** tab.
4. Select **Monitoring**.
5. Do one of the following:
   - If you haven’t associated any DMFs before, select **Set up**, which opens a populated Worksheet that helps you get started with
     setting a schedule, creating custom DMFs, and associating a DMF with the object.
   - If you already have DMFs associated with the object, start exploring! You can only see a DMF if you have the appropriate
     [access control privileges](/user-guide/data-quality-access-control).

## Understanding which DMFs are running

The DMFs associated with the object are listed under **Quality Dimensions**.

DMFs are grouped as follows:

- System DMFs are grouped based on their [category](/user-guide/data-quality-system-dmfs#label-dmf-system). For example, the NULL\_COUNT and BLANK\_COUNT DMFs are grouped
  into the **Accuracy** category. When there is only one system DMF in a category (for example, the ROW\_COUNT DMF in the **Volume**
  category), the name of the DMF is omitted.
- All [custom DMFs](/user-guide/data-quality-custom-dmfs) associated with the object are grouped under **Custom**.

For each DMF, there is a row for every association between the DMF and the object. Remember that as long as the column arguments are
different, the same DMF can be associated with the same object multiple times. If there are multiple rows, select a specific column row to
see the results of running the DMF with that column as an argument.

For example, suppose the NULL\_COUNT DMF was associated with table `t1` using the following SQL statement:

Copy code

```
ALTER TABLE t1
  ADD DATA METRIC FUNCTION SNOWFLAKE.CORE.NULL_COUNT
    ON (c1);
```

The row containing the column `c1` shows the results of running this DMF.

The **Run Schedule** widget specifies how often the DMFs are running. This corresponds to the value that was set for the
DATA\_METRIC\_SCHEDULE parameter of the object. For more information, see [Adjust the schedule for DMFs](/user-guide/data-quality-working#label-data-quality-schedule).

## Investigate failed quality checks

A data quality check consists of a DMF association that has an *expectation*. An expectation lets you define criteria for whether data
passes a data quality check performed by a DMF. When the DMF returns a value, that value is compared to the expectation’s criteria to
determine whether the data passed or failed the check. For more information about using expectations to set up data quality checks,
see [Use SQL to work with expectations](/user-guide/data-quality-expectations).

You can use the following process to investigate failed quality checks.

Step 1: Were there any failed quality checks?
:   The number of failed quality checks for all DMFs associated with the object displays at the top of the **Monitoring** page.

Step 2: Which DMF category had a failed quality check?
:   Use the **Checks by dimension** widget to check the status of each group of DMFs on the **Monitoring** page. Red indicates that at
    least one DMF in the group failed a quality check.

Step 3: Which DMF association had a failed quality check?
:   If there was at least one failed quality check in the category, expand the widget for the category, and then scan the **Quality Checks**
    column to find the row where not all of the checks passed.

Step 4: What is the quality check?
:   To better understand the quality check that you’re investigating:

    1. Select the DMF association that failed the data quality check. A side panel opens.
    2. In the **Quality Checks** section, check the **Status** column to determine which quality check failed. This corresponds to the
       [expectation](/user-guide/data-quality-expectations) that was violated.
    3. For each failed quality check, use the **Expression** column to determine the value that the quality check expected the DMF to return.
       This corresponds to the [expression of the expectation](/user-guide/data-quality-expectations#label-dmf-expectation-expression).

Step 5: What assets are impacted by the quality issue?
:   With the side panel open, find the **Impacted Assets** section so you can determine what other objects might be affected by the
    quality issue. For information about interpreting the list of objects, see [\*\*Impacted Assets\*\* section](/user-guide/data-quality-ui-monitor#label-data-quality-ui-drill-impacted).

Step 6: Which records violated the quality check? ([Select system DMFs only](/user-guide/data-quality-fixing#label-data-quality-remediation-supported-dmfs))
:   1. With the side panel open, select **View failed records**.
    2. Execute the prepopulated query to see the records that failed the quality check. This query calls the SYSTEM$DATA\_METRIC\_SCAN
       function.

       For information about using the SYSTEM$DATA\_METRIC\_SCAN function to remediate the data quality issues, see
       [Using SYSTEM$DATA\_METRIC\_SCAN to fix data](/user-guide/data-quality-fixing#label-data-quality-remediate).

## Drill down into DMF results

Each row under **Quality Dimensions** shows the most current results of the DMF and a seven-day trend of results. To drill down into these
results, select a row to open a side panel. The following describes the elements of this side panel.

**View Lineage** button
:   Select a DMF to view the [lineage](/user-guide/ui-snowsight-lineage) of the object associated with that DMF.

**View failed records** button ([Select system DMFs only](/user-guide/data-quality-fixing#label-data-quality-remediation-supported-dmfs))
:   If the DMF returned a value greater than 0, you can determine which records were flagged as having quality issues. For example, if the
    NULL\_COUNT DMF returned `5`, then you can determine which five records contain a NULL value.

    Selecting **View failed records** opens a worksheet that is prepopulated with a query that calls the SYSTEM$DATA\_METRIC\_SCAN function.
    Execute this query to return the records that were included in the result of the DMF.

    For more information about using the SYSTEM$DATA\_METRIC\_SCAN function, see [Remediation of data quality issues](/user-guide/data-quality-fixing).

**Arguments** section (Multi-argument DMFs only)
:   If a custom DMF takes multiple columns as arguments, these columns are listed. You can select a column to navigate to the **Columns**
    tab of the object that contains the column.

**Quality Checks** section
:   Lists the [expectations](/user-guide/data-quality-expectations) that were added to the association between the DMF and the
    object. Each expectation implements a data quality check. This section contains the following columns:

    - **Name** — Name of the expectation.
    - **Expression** — Expression of the expectation. For more information, see [Defining what meets the expectation](/user-guide/data-quality-expectations#label-dmf-expectation-expression).
    - **Status** — Indicates whether the expectation was violated the last time the DMF ran.

**Impacted Assets** section
:   Displays the objects that are [downstream](/user-guide/ui-snowsight-lineage#label-lineage-upstream-downstream) in the lineage of the object with which the DMF is
    associated. If there is a data quality issue, you can determine what other objects are possibly affected. The contents of the section
    depend on whether the DMF accepts a single argument (like system DMFs) or whether it accepts multiple arguments.

    - If the DMF accepts one column as an argument, Snowflake checks whether the downstream object contains data from that column. For
      example, suppose the NULL\_COUNT DMF identifies NULL values in the `name` column of table `t1`. A downstream view built from `t1`
      only appears in the list of impacted assets if it contains data from the `name` column.
    - If the DMF accepts multiple columns, all downstream objects appear, even if data from the columns doesn’t exist in the downstream object.

**Run History** section
:   Graphically displays the result of the DMF over time so you can determine trends.
