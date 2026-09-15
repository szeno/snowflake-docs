# Determining the benefits of search optimization

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

After you configure search optimization for your tables, you can assess the benefits of search optimization by querying the
SEARCH\_OPTIMIZATION\_BENEFITS view.

This view provides information about the number of partitions pruned due to search optimization. To determine the efficacy of
pruning, you can compare the number of partitions pruned in the `partitions_pruned_additional` column against the total number
of partitions pruned (the sum of the values in the `partitions_pruned_default` column and the `partitions_pruned_additional`
column).

For more information, see [SEARCH\_OPTIMIZATION\_BENEFITS view](/sql-reference/account-usage/search_optimization_benefits).
