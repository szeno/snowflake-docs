# Sep 26, 2025: AI\_COUNT\_TOKENS function (*Preview*)

The Snowflake AI\_COUNT\_TOKENS function helps you size your AI workloads by calculating the total number of input
tokens processed by large language models and task-specific functions, so you can size queries appropriately before
hitting model limits and accurately estimate costs based on input token usage.

Key features of AI\_COUNT\_TOKENS include:

- **Count tokens:** Calculate the total number of input tokens for any AI Function, including AI\_COMPLETE, AI\_EMBED, AI\_CLASSIFY, and AI\_SENTIMENT. AI\_COUNT\_TOKENS
  also takes the specific model into account for functions that can use different models.
- **Get cost optimization insights:** Get precise input token counts before running operations, helping you optimize prompts and right-size AI spending across your organization.
- **Support complex configurations:** Analyze the impact of advanced features like classification with custom labels,
  descriptions, task definitions, and examples to understand the full token impact of your AI workflows.

For more information, see [AI\_COUNT\_TOKENS](/sql-reference/functions/ai_count_tokens).
