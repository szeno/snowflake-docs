# SnowConvert AI - Migration Assistant - Billing

The SnowConvert AI Migration Assistant uses the [Snowflake Cortex REST API](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-rest-api), which incurs compute costs based on the number of tokens processed. You can view current rates in the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf), and get more information on how to monitor LLM usage and costs in your account in the [Snowflake documentation for using Large Language Models](https://docs.snowflake.com/en/user-guide/snowflake-cortex/llm-functions#cost-considerations).

It’s not possible to precisely estimate the cost of a given interaction with the Migration Assistant because each response is custom-generated based on the code object you’re working on. A reasonable estimate for a common, one-cycle interaction to resolve an EWI is 3500 tokens. At current rates of 2.55 credits per million tokens, this results in 0.0089 credits used, at a cost of ~$0.027 for [Enterprise Edition in AWS, US East (Northern Virginia)](https://www.snowflake.com/en/pricing-options/). This is only an estimate, and it is possible for interactions to use significantly more tokens than this, especially if they involve multiple rounds of conversation with the LLM.

Since SnowConvert AI Migration Assistant is using Snowflake Cortex REST API, the only way to get the required information to estimate the costs of the requests executed is by consulting the [CORTEX\_ACCOUNT\_USAGE\_HISTORY](https://docs.snowflake.com/en/sql-reference/account-usage/cortex_functions_usage_history) view by running the following query:

Copy code

```
 SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.CORTEX_FUNCTIONS_USAGE_HISTORY WHERE warehouse_id = 0 ORDER BY start_time DESC;
```

The provided query isolates requests made by the SnowConvert AI Migration Assistant by filtering for calls that did not use a virtual warehouse. This condition is effective because Cortex REST API calls are processed without a warehouse, allowing us to distinguish them from standard SQL-based queries.

Warning

**Limitation**: This query cannot distinguish between REST API calls made by the SnowConvert AI Migration Assistant and any other REST API calls executed by the same user. Consequently, if a user utilizes the Cortex REST API for other purposes, it will be impossible to isolate and attribute consumption specifically to this tool.
