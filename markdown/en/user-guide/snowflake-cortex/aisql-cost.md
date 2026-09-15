# Cost considerations for Cortex AI Functions

Snowflake Cortex AI functions incur compute cost based on the number of tokens processed. Refer to the
[Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf) for each function’s cost in credits per million tokens.

A token is the smallest unit of text processed by Snowflake Cortex AI functions. An industry convention for text is that a token is approximately equal to four
characters, although this can vary by model, as can token equivalence for media files.

- For functions that generate new text using provided text (AI\_COMPLETE, AI\_CLASSIFY, AI\_FILTER, AI\_AGG, AI\_SUMMARIZE, SUMMARIZE (SNOWFLAKE.CORTEX), and
  AI\_TRANSLATE, and their previous versions in the SNOWFLAKE.CORTEX schema), both input and output tokens are billable.
- For Cortex Guard, only input tokens are counted. The number of input tokens is based on the number of tokens output from AI\_COMPLETE (or COMPLETE).
  Cortex Guard usage is billed in addition to the cost of the AI\_COMPLETE (or COMPLETE) function.
- For AI\_SIMILARITY, AI\_EMBED, and the SNOWFLAKE.CORTEX.EMBED\_\* functions, only input tokens are counted.
- For EXTRACT\_ANSWER, the number of billable tokens is the sum of the number of tokens in the `from_text` and
  `question` fields.
- AI\_CLASSIFY, AI\_FILTER, AI\_AGG, AI\_SENTIMENT, AI\_SUMMARIZE\_AGG, SUMMARIZE, TRANSLATE, AI\_TRANSLATE, EXTRACT\_ANSWER,
  ENTITY\_SENTIMENT, and SENTIMENT add a prompt to the input text in order to generate the response. As a result, the
  billed token count is higher than the number of tokens in the text you provide.
- AI\_CLASSIFY labels, descriptions, and examples are counted as input tokens for each record processed, not just once for each AI\_CLASSIFY call.
- For AI\_PARSE\_DOCUMENT (or SNOWFLAKE.CORTEX.PARSE\_DOCUMENT), billing is based on the number of document pages processed.
- For AI\_EXTRACT, both input and output tokens are counted. The `responseFormat` argument is counted as input tokens.
  For document formats consisting of pages, the number of pages processed is counted as input tokens. Each page in a document is counted as 970 tokens.
- For AI\_REDACT, both input and output tokens are counted.
- AI\_COUNT\_TOKENS incurs only compute cost to run the function. No additional token-based costs are incurred.

For models that support media files such as images or audio:

- Audio files are billed at 50 tokens per second of audio.
- The token equivalence of images is determined by the model used.

The cost associated with keeping a warehouse active continues to apply when executing a query that calls a Snowflake
Cortex LLM Function. For general information on compute costs, see
[Understanding compute cost](/user-guide/cost-understanding-compute).

## Warehouse sizing

Snowflake recommends using a warehouse size no larger than MEDIUM when calling Snowflake Cortex AI
Functions. Using a larger warehouse than necessary does not increase performance, but can result in unnecessary costs.
This recommendation may change in the future as we continue to evolve Cortex AI Functions.

## Track costs for AI services

To track credits used for AI Services including LLM Functions in your account, use the [METERING\_HISTORY view](/sql-reference/account-usage/metering_history):

Copy code

```
SELECT *
  FROM SNOWFLAKE.ACCOUNT_USAGE.METERING_DAILY_HISTORY
  WHERE SERVICE_TYPE='AI_SERVICES';
```

## Track credit consumption for Cortex AI Functions

To view the credit and token consumption for each AI Function call, use the [CORTEX\_FUNCTIONS\_USAGE\_HISTORY view](/sql-reference/account-usage/cortex_functions_usage_history):

Copy code

```
SELECT *
  FROM SNOWFLAKE.ACCOUNT_USAGE.CORTEX_FUNCTIONS_USAGE_HISTORY;
```

You can also view the credit and token consumption for each query within your Snowflake account. Viewing the credit and token consumption for each query helps you identify queries that are consuming the most credits and tokens.

The following example query uses the [CORTEX\_FUNCTIONS\_QUERY\_USAGE\_HISTORY view](/sql-reference/account-usage/cortex_functions_query_usage_history) to show the credit and token consumption for all of your queries within your account.

Copy code

```
SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.CORTEX_FUNCTIONS_QUERY_USAGE_HISTORY;
```

You can also use the same view to see the credit and token consumption for a specific query.

Copy code

```
SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.CORTEX_FUNCTIONS_QUERY_USAGE_HISTORY
WHERE query_id='<query-id>';
```

Note

You can’t get granular usage information for requests made with the REST API.

The query usage history is grouped by the models used in the query. For example, if you ran:

Copy code

```
SELECT AI_COMPLETE('mistral-7b', 'Is a hot dog a sandwich'), AI_COMPLETE('mistral-large', 'Is a hot dog a sandwich');
```

The query usage history would show two rows, one for `mistral-7b` and one for `mistral-large`.

## See also

For day-to-day cost governance (usage views, account-level alerts, per-user spending limits, runaway query detection),
see [Managing Cortex AI Function costs with Account Usage](/user-guide/snowflake-cortex/ai-func-cost-management).
