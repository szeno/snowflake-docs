# Use data profiling to understand your data

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Data profiling helps you understand the structure, content, and quality of your data sets by automatically gathering statistics such as data
types, value distributions, counts of NULL values, and uniqueness. The data profile reveals patterns, anomalies, and potential quality
issues, which lets you assess data reliability and make informed decisions about how to clean, transform, or effectively use your data. Data
profiling simplifies the path to continuous data quality monitoring by providing insights without manual setup.

The data profile includes the following statistics:

- Number of rows in the table.
- Last time the table was updated.
- How many NULL values are in a column.
- Minimum and maximum values in a column.
- Most common values in a column.

## Get started

To view the data profile of a table or view, complete the following steps:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Catalog** » **Database Explorer**, and then select the table or view.
3. Select the **Data Quality** tab.
4. Select **Data Profile**.

## Warehouse considerations

Data profiling runs background SQL queries to display information about a table or view. Snowflake recommends using an X-Small warehouse to
run these queries; however, heavier workloads might see a performance improvement by using a larger warehouse. In general, larger warehouses
consume more credits.

By default, data profiling uses the warehouse that is set as the default for the current user. To select a different warehouse, use the
drop-down list at the top of the page.
