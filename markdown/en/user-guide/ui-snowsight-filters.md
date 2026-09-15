# Filter query results in dashboards and worksheets

You can filter your query results in dashboards and SQL worksheets using system filters, available to all roles in Snowflake,
or with custom filters created by administrators.

## Create custom filters

Custom filters let you change the results of a query without directly editing the query.

Filters are implemented as special keywords that resolve as a subquery or list of values, which are then used in the execution of a query.
As a result, there are some limitations when using a filter in a SQL query. See [Specify a filter in a SQL query](#label-snowsight-filter-query-use).

Note

Anyone in your account can view and use a custom filter after it is created. A custom filter has an associated role,
but that role does not limit filter visibility.

### Grant permission to create custom filters

To let a user create custom filters, a user with the ACCOUNTADMIN role must grant the relevant permissions to a role granted to that user.
You can only use Snowsight to grant roles the ability to create custom filters.

To grant a role permission to create custom filters for your account, do the following:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **Dashboards** or another project tool.
3. Select [![Show or hide filter](/static/images/snowsight/snowsight-query-history-filter.png)](/static/images/snowsight/snowsight-query-history-filter.png) and, if in a worksheet, select **Manage Filters**.
4. In the dialog that appears, select **Edit Permission**.
5. In the **Filter Permissions** dialog, select the roles you want to grant the ability to create filters to.
6. Select **Save**.

### Create a custom filter

You must use Snowsight to create a filter, and you must use a role with permissions to create custom filters.

To create a custom filter, do the following:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **Dashboards** or another project tool.
3. Select [![Show or hide filter](/static/images/snowsight/snowsight-query-history-filter.png)](/static/images/snowsight/snowsight-query-history-filter.png) and, if in a worksheet, select **Manage Filters**.
4. In the **Filters** dialog that appears, select **+ Filter**.
5. To add a filter, complete the following:

   1. For **Display Name**, enter a name for the filter. This name appears on the filter when selecting the filter on a worksheet or dashboard.
   2. For **SQL Keyword**, enter a unique keyword to insert into queries. Use the format `:<string>`, without spaces.
      For example: `:page_path`.
   3. For **Description**, enter a description of the filter.
   4. For **Role**, select a role to associate with the filter and run the query used to populate filter values, if the filter is based
      on a query. Only roles with permissions to create custom filters appear in the drop-down list.
      See [Manage ownership of custom filters](#label-snowsight-filter-ownership) for more details.
   5. For **Warehouse**, select a warehouse to use to refresh filter values, if the filter is based on a query.
      The owner role for the filter must have the USAGE privilege on the warehouse you select.
      If you want to run and validate your query as part of these steps, the warehouse must be running.
   6. For **Options via**, choose whether the filter values are populated by a query or a list:
      - If you select **Query**, select **Write Query** and see [Write a query to populate a filter](#label-snowsight-filter-options-query) for guidance writing a
        filter query.
      - If you select **List**, do the following:
        1. Select **Edit List**.
        2. Optionally, for **Name**, enter a name for the list item. The name appears in the drop-down list for the filter.
           If you do not provide a name, the **Value** is used.
        3. For **Value**, enter the value of the column name to use in the filter.
        4. Continue adding name and value pairs until your list is complete, then select **Save**.
6. In the **Add Filter** dialog, for **Value Type**, choose whether the list items are **Text** or **Number** types of data.
7. If you want users to be able to select multiple items in the drop-down list of filter options,
   turn on the toggle for **Multiple values can be selected**.
8. If you want users to be able to see results for all items in the column, turn on the toggle for **Include an “All” option**, then select
   how you want the **All** option to function:

   - Select **Any value** to have the **All** in the filter mean that the column to which the filter applies can have any value in
     the results, whether or not the value exists in the filter list.
   - Select **Any value in list of options** to have **All** in the filter mean that the column to which the filter applies contains
     any item in the filter list.
9. If you want users to be able to see results for items not specified in the filter, turn on the toggle for **Include an “Other” option**.
10. Select **Save**.
11. Select **Done** to close the **Filters** dialog.

#### Write a query to populate a filter

To populate a list of filter options from a query, your query must follow certain guidelines:

- Must return the columns `name` and `value`.
- Can return the optional column `description`.
- Can return other columns, but those do not appear in the drop-down filter list.

A filter can only run one query at a time. You cannot run multiple queries to generate the list of filter options, for example by running
one query to return the `name` column and a second query to return the `value` column.

Note

The query used to populate a list of filter options is run as the user that created (or last modified) the filter.
Because anyone in your account can view and use a custom filter after it is created, make sure that the list of
filter options produced by your query do not contain protected or sensitive data.

After you write your filter query and add it in the **New filter** dialog, do the following to finish setting up your query filter:

1. Select **Done** to save your filter query and return to the **Add Filter** dialog.
2. Optionally change the default refresh option from **Refresh hourly** to **Never refresh** or **Refresh daily**. For details
   and considerations for filter refresh options, see [Manage refresh frequency for a custom filter](#label-snowsight-custom-filter-refresh).
3. Return to the steps for creating a custom filter to finish creating your filter. See [Create a custom filter](#label-snowsight-custom-filter-create).

## Review and manage custom filters in an account

To review custom filters in your account, open a worksheet or dashboard and then select [![Show or hide filter](/static/images/snowsight/snowsight-query-history-filter.png)](/static/images/snowsight/snowsight-query-history-filter.png).

To make changes to any filters, such as changing the refresh frequency for the query used to populate a custom filter list,
you must have the ACCOUNTADMIN role or a role with [permissions to manage filters](#label-snowsight-custom-filter-perms).
See [Manage refresh frequency for a custom filter](#label-snowsight-custom-filter-refresh).

### Manage ownership of custom filters

Each custom filter has an associated role. Anyone with that role can edit or delete the filter.
Users with the ACCOUNTADMIN role can view and edit every filter in the account.

If the role associated with a filter is dropped, the role dropping the filter role does not inherit ownership of the custom filter. Instead, a user with the ACCOUNTADMIN role can edit the filter and change the role associated with the filter.

### Manage refresh frequency for a custom filter

A custom filter that is populated by a SQL query also has a refresh frequency. The refresh frequency can be hourly, daily, or never.

The filter runs based on when it was saved and how long it took to run the query that refreshes the filter options.

For example, if you save a filter that has an hourly query refresh frequency at 10:07 AM, the first refresh query runs at or after 11:07 AM.
If a large number of filter refresh queries end up scheduled to run at the same time, the queries are queued to limit the number of
filter refresh queries running at the same time. The next filter refresh is based on when the last refresh completed. In this example, if
the query refresh at 11:07 AM takes 20 minutes to complete, the next refresh query would run at or after 12:27 PM.

Filter refreshes run as the user that created or last modified the filter, and are visible in **Query History** as
one of the types of **Queries executed by user tasks**.
See [Monitor query activity with Query History](/user-guide/ui-snowsight-activity) for details on using **Query History**.

To determine which filter is responsible for a filter query refresh, you must open the list of filters and open each filter to
view the details.

Note

Setting a custom filter’s refresh frequency can lead to increased consumption on your virtual warehouse. The virtual warehouse will run
the underlying query according to the configured schedule, even if no user has the filter open in their web browser. The cost incurred depends
on the query complexity and the refresh schedule that you set.

#### Troubleshoot failed filter query refreshes

Refreshes of the filter query can fail for one of the following reasons:

- The user that created or last modified the filter has been dropped or disabled in Snowflake.
- The user is inactive because they have not signed in for 3 months.

It is not possible to see which users created or last modified a given filter. If you have filters that are failing to refresh,
you might see successful authentication attempts by the WORKSHEETS\_APP\_USER user followed by failed authentication
attempts from a user in the [LOGIN\_HISTORY view](/sql-reference/account-usage/login_history) view of the ACCOUNT\_USAGE schema in the
shared SNOWFLAKE database.

For example, you can use the following query to identify login activity that uses an OAuth access token from the previous two days:

Copy code

```
SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.LOGIN_HISTORY
WHERE
    FIRST_AUTHENTICATION_FACTOR = 'OAUTH_ACCESS_TOKEN'
    AND
    REPORTED_CLIENT_TYPE = 'SNOWFLAKE_UI'
    AND
    EVENT_TIMESTAMP > DATEADD('DAY', -2, CURRENT_DATE())
ORDER BY
    EVENT_TIMESTAMP DESC;
```

Failed authentication attempts associated with a failed query refresh frequency would happen at the same time each day or each hour,
depending on the custom filter refresh frequency.

## Specify a filter in a SQL query

You can use a [system filter](#label-snowsight-filters-system-date) or a custom filter in a SQL query.
You cannot use a filter in a stored procedure or a user-defined function (UDF).

To add a filter to your SQL query, use one of the following formats:

- Specify the filter as part of a SELECT statement, like `SELECT :<filter_name>(<col_name>)`.
- Specify the filter using an equals sign as the comparator. For example:
  - `WHERE <col_name> = :<filter_name>`
  - `WHERE <:filter_name> = <col_name>`
  - `<value_a>:<value_b>::string = <:filter_name>`

You can only use an equals sign as the comparator for a filter, and as such, cannot use a filter with
[LIKE](/sql-reference/functions/like) or [CONTAINS](/sql-reference/functions/contains).

The column to which the filter applies must also match the value type expected by the filter:

- For a custom filter set to use a value type of text, the column must be a text string or cast to a text string in the query.
  See [Data types for text strings](/sql-reference/data-types-text#label-character-datatypes).
- For a custom filter set to use a value type of number, the column must be a numeric data type. See [Numeric data types](/sql-reference/data-types-numeric).
- For a system filter, the column must be a TIMESTAMP data type. See [Date & time data types](/sql-reference/data-types-datetime).

When you add a filter to your SQL query and then use the drop-down list to choose a filter option, the SQL syntax of your query is
changed. For details about how the SQL syntax is changed when different options in the list are selected, refer to the following table:

**Filter SQL reference**

| Filter option selected | SQL used |
| --- | --- |
| List item | `<col> = <list_item>` |
| Multiple list items selected | `<col> IN (<list_item>, <list_item>)` |
| All, with **Any value** specified | `true` |
| All, with **Any value in list of options** specified | `<col> IN (<list_item>, <list_item>, ... )` |
| Other | `<col> NOT IN(<list_item>, <list_item>, ... )` |

Expand

Show lessSee more

### Applying and saving filters

When you change the options selected in a filter, the option to apply your changes appears.
When you select **Apply**, the worksheet or dashboard runs and updated filtered results appear,
letting you review the changes without saving.

After you apply changes to a filter on a dashboard, the option to save your changes appears. When you select **Save**, the
changes you made to the dashboard are saved and available to other users of the dashboard.

For example, you might select **Apply** to change a filter to see results from **All Time**, but you don’t want the dashboard to run
over such a large volume of data the next time someone opens the dashboard, so you do **not** select **Save**.
After you run your dashboard over all time, you change the date range filter to **Last 7 days**, select **Apply** to run the dashboard,
and then select **Save** to save that default filter value for dashboard users.

## Snowsight system filters

The following system filters are available to all roles:

- `:daterange`

  - Filters a column by a date range, such as **Last day**, **Last 7 days**, **Last 28 days**, **Last 3 months**,
    **Last 6 months**, **Last 12 months**, **All time**, or a custom date range.

    Note

    The date range filter always uses the UTC time zone and is not affected by the [TIMESTAMP\_INPUT\_FORMAT](/sql-reference/parameters#label-timestamp-input-format) parameter.

    Defaults to **Last day**.
- `:datebucket`

  - Groups aggregate data by a period of time, such as **Second**, **Minute**, **Hour**, **Day**, **Week**,
    **Month**, **Quarter** in calendar months, or **Year**.

    Defaults to **Day**.

These filters cannot be edited or dropped.

### Example: Working with date filters

For example, given a table with order data, such as the ORDERS table in the SNOWFLAKE\_SAMPLE\_DATA database and TPCH\_SF1 schema, you
might want to query the table and group the results by a specific time bucket, such as by day or by week, and specify a specific date range
for which to retrieve results.

To do so, you can write a query as follows:

Copy code

```
SELECT
    COUNT(O_ORDERDATE) as orders,
    :datebucket(O_ORDERDATE) as bucket
FROM
    SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.ORDERS
WHERE
    O_ORDERDATE = :daterange
GROUP BY
    :datebucket(O_ORDERDATE)
ORDER BY
    bucket;
```

In this example, you:

- Count the number of orders and retrieve details about the order date from the ORDERS table.
- Filter your results by a specific date range by including the `:daterange` system filter in your WHERE clause.
- Group your results by a specific period of time by including the `:datebucket` system filter in your GROUP BY clause.
- Sort the results from earliest to latest time period by including the ORDER BY clause.

When you add filters to your query, corresponding filter buttons appear at the top of your worksheet or dashboard:

![When the filter buttons appear, they follow the show and hide filters button in the tab order.](/static/images/snowsight/snowsight-query-filter-example.png)

To manipulate the results that you see from your query, use the filters to select specific values.

For this example, set the **Group by** filter, which corresponds to the date bucket filter, to group by `Day`. Set the other
filter, which corresponds to the date range filter, to `All time`.

When you select **Apply** and apply the filter to your results, the results are grouped by day and results like the following output
appear:

```
+--------+------------+
| orders |  buckets   |
+--------+------------+
|    621 | 1992-01-01 |
|    612 | 1992-01-02 |
|    598 | 1992-01-03 |
|    670 | 1992-01-04 |
+--------+------------+
```

You can select a different date bucket to show a different grouping of data. For example, to view weekly order data, set the **Group by**
filter to `Week` and select **Apply**. Results like the following output appear:

```
+--------+------------+
| orders |  buckets   |
+--------+------------+
|   3142 | 1991-12-30 |
|   4404 | 1992-01-06 |
|   4306 | 1992-01-13 |
|   4284 | 1992-01-20 |
+--------+------------+
```
