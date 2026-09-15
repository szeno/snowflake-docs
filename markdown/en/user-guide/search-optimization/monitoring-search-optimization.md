# Monitoring search optimization using Snowsight

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

After you enable the search optimization service, you can use Snowsight to monitor statistics about how queries
use it. You can also use Snowsight to determine why a query isn’t using the search optimization service.

## Monitoring search optimization usage for a query

When a query uses the search optimization service, the [query profile](/user-guide/ui-snowsight-activity#label-snowsight-query-profile) includes
the following:

- **Search Optimization Access** node - A dedicated **Search Optimization Access** node is in the query plan.
  Select this node to access the table scan information, as well as information that is specific to search optimization.
- **Attributes** pane - This pane for the node contains the following:

  - Full table name - Identifies the table that was scanned for the query that used search optimization.
  - Search optimization usage information - This section lists the expression IDs that search optimization referenced during
    query execution. Each expression ID corresponds to a search method and column target defined for the table. Execute the
    following query to show the expression IDs and their corresponding methods and targets:

    Copy code

    ```
    DESCRIBE SEARCH OPTIMIZATION ON <table_name>;
    ```

    For more information about this command, see [DESCRIBE SEARCH OPTIMIZATION](/sql-reference/sql/desc-search-optimization).
- **Statistics** pane - This pane for the node contains the following metrics:

  - **Bytes scanned** - The total amount of data that was read during the execution of a table scan operation.
  - **Partitions scanned** - The number of micro-partitions that were actually scanned.
  - **Partitions total** - The total number of the micro-partitions for the table.
  - **Partitions pruned by search optimization** - The number of micro-partitions that search optimization effectively
    eliminated from the corresponding table scan.

The following image shows an example of the metrics on the **Statistics** pane:

![Shows the Search Optimization Access node with the search optimization statistics included.](/static/images/snowsight/search-optimization-used.png)

## Determining the reason why search optimization wasn’t used

Even when search optimization is configured for a table, it might not always be used. If search optimization wasn’t used for a query,
examine the **Table Scan** node’s **Search Optimization Usage Info** section on the **Attributes** pane. The section
shows one of the following explanations:

- When there is a predicate mismatch, the following message is shown:

  ```
  Search optimization service was not used because no
  match was found between used predicates and the
  search access paths added for the table.
  ```

  This message indicates that the predicate used in the query on this table isn’t compatible with the search methods defined for the table.
  You can review the optimization configuration for the table by executing the following command:

  Copy code

  ```
  DESCRIBE SEARCH OPTIMIZATION ON <table_name>;
  ```

  For information about the predicates and data types supported by search optimization, see [Identifying queries that can benefit from search optimization](/user-guide/search-optimization/queries-that-benefit).
- When there is a cost-based decision not to use search optimization, the following message is shown:

  ```
  The query optimizer estimated that the search optimization
  service would not be beneficial for this table scan.
  ```

  This message indicates that the predicates used in the query are compatible with the search methods defined for the table, but the query
  optimizer decided that query performance likely wouldn’t be improved by search optimization. Subsequent queries with different predicates or
  different data in the source table might use search optimization.
- When the predicate limit is exceeded, the following message is shown:

  ```
  Search optimization service was not used because the
  predicate limit was exceeded.
  ```

  This message indicates that the predicate contains too many distinct predicates. The exact count of search optimization predicates depends on
  the types of the predicates and might not match exactly the number of predicates in the query.
  [Substring queries](/user-guide/search-optimization/substring-queries) and
  [full-text search queries](/user-guide/search-optimization/text-queries) that use the wildcard syntax are more likely to reach the
  predicate limit.

The following image shows an example of a predicate mismatch message:

![Shows the Search Optimization Access node with a message about the reason for not using search optimization.](/static/images/snowsight/search-optimization-not-used.png)
