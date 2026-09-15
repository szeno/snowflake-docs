# Querying data using worksheets

After you [create or open a worksheet](/user-guide/ui-snowsight-worksheets-gs), you can
[manage the worksheet](/user-guide/ui-snowsight-worksheets), write and execute queries, explore query results and history,
and set up filters using Snowsight.

## Writing queries in worksheets

After you open a worksheet, you can write SQL queries and statements.

Note

Multiple SQL statements in a single API call are not supported. Ensure that each SQL query in the worksheet ends with a single
semicolon (;).

### Set worksheet context

When you set a database and optionally, a database schema, as the worksheet context, you can reference objects in the schema
without fully qualifying the object names in your query.

### Write queries with autocomplete

As you enter your script in the query editor, the autocomplete feature suggests:

- Query syntax keywords such as SQL functions or aliases.
- Values that match table or column names within a schema.

Select a function to view its syntax and a brief description.

Snowflake tracks table aliases and suggests them as autocomplete options. For example, if you execute a query using `posts as p` or
`posts p` as an alias, the next time you type `p`, the autocomplete feature suggests the alias as an option.

### Use Snowflake Copilot to write queries

Snowflake Copilot is an LLM-powered assistant that simplifies data analysis. You can use natural language requests to explore a new dataset,
generate queries or refine existing queries.

See [Using Snowflake Copilot](/user-guide/snowflake-copilot) to learn more about Snowflake Copilot and for example prompts to get you started.

### Append a SQL script to an existing worksheet

If you have a SQL script in a file, you can append it to an existing worksheet by doing the following:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **Worksheets**.
3. Open a worksheet.
4. Hover over the tab for the worksheet and select [![More actions for worksheet](/static/images/snowsight/snowsight-worksheet-vertical-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-vertical-ellipsis.png), then choose **Import SQL from File**.
5. Browse to the SQL file on your computer.

   The file contents are appended to your worksheet.

### Refer to database object names in worksheets

While you write queries in your worksheet, refer to the database objects relevant to the queries in the **Databases** explorer. You can
drill down to specific database objects, or use search to locate a database, schema, or object that you have access to.

Using the **Databases** explorer, you can pin databases and database objects for quick reference. When you hover over a database object,
select the **Pin** icon to pin them. Pinned objects appear at the top of the **Databases** explorer in the **Pinned** section.
You might need to expand the section to view all your pinned objects.

After you locate a database object, you can place the name of the object in the worksheet that you’re editing:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **Worksheets**.
3. Open a worksheet.
4. Locate the database object in the **Databases** explorer.
5. Hover over the object name and select **…** more menu » **Place Name in Editor**.

   The fully qualified object name appears after your cursor location in the worksheet.

For database tables and views, you can also add the column names to the worksheet that you’re editing:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **Worksheets**.
3. Open a worksheet.
4. Locate the database object in the **Databases** explorer.
5. Hover over the object name and select **…** more menu » **Add Columns in Editor**.

   The comma-separated column names appear after your cursor location in the worksheet.

### Format your queries

When a worksheet is open, you can select the name of the worksheet to format the queries in your worksheet, and view the keyboard shortcuts.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **Worksheets**.
3. Open a worksheet.
4. Hover over the tab for the worksheet and select [![More actions for worksheet](/static/images/snowsight/snowsight-worksheet-vertical-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-vertical-ellipsis.png).
5. In the drop-down list, select **Format query** to format the query text for readability.

### Load data to a table

If you’re using a worksheet and want to add some data to work with, you can load data into a table without leaving your worksheet:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **Worksheets**.
3. Open a worksheet.
4. Select **Objects** to view the object explorer.
5. Locate a specific table using search or browsing.
6. Hover over a specific table name and select [![More options](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png) » **Load Data**.
7. Follow the prompts to upload one or more structured or unstructured files of 50MB or less.

Refer to [Load data using Snowsight](/user-guide/data-load-web-ui) for more details.

## Executing and running queries

You can run a single query or multiple queries sequentially in the same worksheet.

- To run a single query, in the query editor, place your cursor in the query, and then select the **Run** button.
- To run the entire worksheet, from the **More options** dropdown menu next to the **Run** button, select **Run All**.

### Running worksheets in folders

Folders no longer have a role assigned to them. An owner or editor of a worksheet in a folder can change the worksheet to run as any role.
You can also add [USE ROLE](/sql-reference/sql/use-role) to a worksheet in a folder to run different statements in the worksheet as different roles.

When you create a worksheet inside a folder, the worksheet is created with the role of your current session.

Note

To run a worksheet in a folder that was shared with you, even if you have **View and Run** or **Edit** permissions on the folder,
you must use the same role as the worksheet. If you do not have the same role, duplicate the worksheet and run it as one of your own roles.

## Exploring the worksheet results

Note

Available to most accounts. Accounts in U.S. government regions, accounts using Virtual Private Snowflake (VPS), and accounts
that use Private Connectivity to access Snowflake continue to see query results limited to 10,000 rows.

When you run one query or all queries in a worksheet, you see the query results.

The query results display as a table. You can navigate the query results with the arrow keys on your keyboard, as you would with a
spreadsheet. You can select columns, cells, rows, or ranges in the results table. You can copy and paste any selection.

For up to 1 million rows of results, you can review generated statistics that display contextual information for any selection,
as well as overall statistics. See [Automatic contextual statistics](#label-snowsight-contextual-stats) for more details.

If you want to view your results as a chart, select **Chart**. For more details about charts, see
[Visualizing worksheet data](/user-guide/ui-snowsight-visualizations).

Query results are cached. For more details, see [Stored results for past worksheet versions](/user-guide/ui-snowsight-worksheets#label-snowsight-worksheets-results-cache) and
[Manage worksheet history and versions](/user-guide/ui-snowsight-worksheets#label-snowsight-worksheet-history).

### Cost considerations for transforming query results

Note

Available to most accounts. Accounts in U.S. government regions, accounts using Virtual Private Snowflake (VPS), and accounts
that use Private Connectivity to access Snowflake are not charged when transforming query results.

Note that some column transformation activities performed on the query results of Snowsight worksheets incur
compute cost. The compute cost is billed against the same warehouse used to run the query.

For example, when you sort a column by ascending or descending order using the column options, the changes affect all of your results,
instead of just the first 10,000 rows returned, and you incur compute cost.

![When you select a column, arrows display that you can use to sort a column ascending or descending.](/static/images/snowsight/snowsight-column-sort.png)

To identify the interactions that incur compute cost, filter the **Query History** page to view only SQL statements that contain the
**SQL Text**: `snowsight_transform_cte`.

The following transformations do not incur cost:

- Showing a thousands separator for numeric columns.
- Displaying a column as a percentage.
- Increasing or decreasing decimal precision.
- Formatting date and timestamp columns.

In addition, transformations performed by the recipient of a shared worksheet operating on a limited set of results do not incur cost.
For more details about shared worksheet results, see [Viewing results for past runs of a worksheet](/user-guide/ui-snowsight-worksheets#label-snowsight-worksheets-viewing-results).

For more details about compute cost, see [Exploring compute cost](/user-guide/cost-exploring-compute).

### Automatic contextual statistics

Select columns, cells, rows, or ranges in the results table to view relevant information about the selected data in the inspector pane (to
the right of the results table). Contextual statistics are automatically generated for all column types. The statistics are intended to help
you make sense of your data at a glance.

The column overview displays a preview of the statistics for each column. Select a column from the inspector or the column header to view
detailed column statistics.

The statistics pane generates different metrics for different types of columns. You can interact with and filter using the items in the
statistics pane.

Filled/empty meters
:   All columns show how many rows are filled and empty. Columns displaying some data types, such as email and JSON, also indicate the
    number of invalid rows.

Histograms
:   Displayed for all date, time, and numeric columns.

    The histogram indicates the rows that fall into a particular range. Click a bar or drag over the histogram to select a range. You can
    fine tune your selection by clicking the value labels above the histogram to input specific values.

Frequency distributions
:   Displayed for all categorical columns. Categorical columns are text columns where the same values are used more than once.

Email domain distributions
:   Displayed for email columns. The email domain distribution shows the frequency distribution of domain name occurrences.

Key distributions
:   Displayed for JSON columns. The key distribution shows the frequency of the top keys present in the result set if all the rows contain
    JSON objects. If the column includes JSON arrays, the key distribution shows the relative types of JSON values in the column.

### View query details

The **Query Details** includes information about the execution of the query, including:

- The duration of the query execution.
- The number of rows in the results.
- When the execution completed.
- The quantity of data scanned by the query.
- The role used to execute the query.
- The warehouse used to execute the query.

Some query details are available for only 14 days.

### View the query profile

To access a detailed profile of your query, on the **Query Details** pane select the **…** more menu » **View Query Profile**.

The query profile opens in a new browser tab.

For information on reviewing the query profile, see [Review Query Profile](/user-guide/ui-snowsight-activity#label-snowsight-query-profile).

### Download your query results

To download your query results as a CSV-formatted or TSV-formatted file, select **Download results**.

The size of your file depends on the amount of data returned by your query. Snowflake does not limit the size of files
exported for query results.

### View query history

After you run SQL in a worksheet, you can review the history of queries run in the worksheet, for example to compare results of different
query runs. You must use the same role as the worksheet to view the query history for the worksheet.

When the **Results** pane is visible, select [![Query history](/static/images/snowsight/snowsight-query-history-clock.png)](/static/images/snowsight/snowsight-query-history-clock.png) (**Query history**) to review the queries that have been
run in the worksheet, as well as the results for those queries.
The history includes up to 25 queries run in that worksheet during your current session and previous sessions over the last 14 days.

You can review the following information:

- The status of a query that is in progress.
- What time the query was run.
- How long the query took to run, in milliseconds or seconds.
- Which query was run.
- The query ID.

Select a row to see the results for that query execution in the **Results** pane. If you do not have the primary role used to run a query
that you view in **Query history**, you cannot view the results for that query. Subqueries spawned by stored procedures or Python
worksheets do not display.

To filter the query history for the worksheet by status, warehouse, or other aspects:

- Filter the query executions by status. For example, review queries that are still in the **Running** or **Queued** status
  and do not yet display results.
- Select [![Show or hide filter](/static/images/snowsight/snowsight-query-history-filter.png)](/static/images/snowsight/snowsight-query-history-filter.png) to filter by warehouse, SQL text in the query, a specific query ID, or a duration greater
  than a specific time period.

Hover over a query execution row to see a full preview of the SQL statement that was run, copy the query ID, and optionally open the
query details for the query execution. See [Review Query History in Snowsight](/user-guide/ui-snowsight-activity#label-snowsight-activity-query-history) for more information about query details.

### Query history data redacted from a Snowflake Native App

For queries related to a Snowflake Native App, the `query_text` and `error_message` fields are redacted
from the [query history](/user-guide/ui-snowsight-activity) in the following contexts:

- Queries run when the app is installed or upgraded.
- Queries that originate from a child job of a stored procedure owned by the app.

In each of these situations, the cell of the query history in Snowsight appears blank.
