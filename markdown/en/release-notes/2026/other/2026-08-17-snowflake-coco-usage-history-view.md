# Aug 17, 2026: New SNOWFLAKE\_COCO\_USAGE\_HISTORY view in Account Usage and Organization Usage (*General availability*)

The [SNOWFLAKE\_COCO\_USAGE\_HISTORY](/sql-reference/account-usage/snowflake_coco_usage_history) view is now generally available in the
ACCOUNT\_USAGE and ORGANIZATION\_USAGE schemas. It provides a unified view of usage history for
[CoCo](/user-guide/cortex-code/cortex-code) across the CLI, Desktop, and Snowsight interfaces.

The information in the view includes the number of credits consumed each time a user interacts with CoCo.
Each row in the view represents a single request and provides detail about the aggregated tokens and credits
as well as a granular breakdown by model. The view also includes an `INTERFACE` column that identifies
whether the request originated from the CLI, Desktop, or Snowsight interface.

Interface-specific usage history remains available in the
[CORTEX\_CODE\_CLI\_USAGE\_HISTORY](/sql-reference/account-usage/cortex_code_cli_usage_history),
[CORTEX\_CODE\_DESKTOP\_USAGE\_HISTORY](/sql-reference/account-usage/cortex_code_desktop_usage_history), and
[CORTEX\_CODE\_SNOWSIGHT\_USAGE\_HISTORY](/sql-reference/account-usage/cortex_code_snowsight_usage_history) views.

For more information, see [SNOWFLAKE\_COCO\_USAGE\_HISTORY view](/sql-reference/account-usage/snowflake_coco_usage_history).
