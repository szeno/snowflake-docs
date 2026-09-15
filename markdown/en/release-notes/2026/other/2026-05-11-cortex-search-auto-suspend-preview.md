# May 11, 2026: Auto-suspend and resume for Cortex Search Services (*Public Preview*)

You can now configure a Cortex Search Service to automatically suspend its serving compute after a
period of query inactivity and resume when it receives a new query. This helps reduce serving costs
on idle services without requiring manual intervention.

Set the `AUTO_SUSPEND` property to the number of seconds of inactivity before the service suspends.
The minimum value is 1800 seconds (30 minutes). Configure it when creating a service or on an
existing service:

Copy code

```
CREATE OR REPLACE CORTEX SEARCH SERVICE my_service
  ON search_column
  WAREHOUSE = my_wh
  TARGET_LAG = '1 hour'
  AUTO_SUSPEND = 1800
AS SELECT search_column FROM my_table;

ALTER CORTEX SEARCH SERVICE my_service SET AUTO_SUSPEND = 1800;
```

When an auto-suspended service receives a query, the first request pauses until the service resumes
and then completes. Resuming typically takes up to a few minutes.

For more information, see [Auto-suspend serving on inactivity](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview#label-cortex-search-auto-suspend-serving),
[CREATE CORTEX SEARCH SERVICE](/sql-reference/sql/create-cortex-search), and
[ALTER CORTEX SEARCH SERVICE](/sql-reference/sql/alter-cortex-search).
