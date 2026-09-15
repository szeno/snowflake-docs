# Snowflake AI pricing

Snowflake AI features use **AI Credit pricing**, a flat, simplified pricing model for AI services.
AI Credits are separate from Platform Credits and provide consistent pricing regardless of your
Snowflake edition. AI costs scale with your usage. Each service is charged per the relevant table in the Consumption table. There are no per-seat fees. Automatic AI Credit discounts apply based on your annual contract value (ACV).

## AI Credits compared to Platform Credits

Snowflake compute costs are quoted in credits. There are two types:

- **AI Credits**: Apply to AI features listed in Table 6 of [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf). AI Credits
  provide a flat pricing model regardless of edition (Standard, Enterprise, Business Critical, or VPS)
  or region. AI Credits have the same price regardless of customer edition.
- **Platform Credits**: The default credit price for all other Snowflake usage. Any pricing not specifically identified as AI Credit pricing uses
  Platform Credits. Platform Credit prices may vary by edition and region.

## AI Credit price

| Routing type | Price per AI Credit | When it applies |
| --- | --- | --- |
| Global routing | $2.00 | `CORTEX_ENABLED_CROSS_REGION` is set to `ANY_REGION`, `AWS_GLOBAL`, `GCP_GLOBAL`, or `AZURE_GLOBAL`. Requests can be routed across broader Snowflake-supported capacity, providing the lowest AI Credit price and broader model availability. |
| Regional routing | $2.20 | `CORTEX_ENABLED_CROSS_REGION` is set to `DISABLED` or a specific regional setting such as `AWS_US`, `AWS_EU`, `AZURE_US`, or `AZURE_EU`. Requests are restricted to the account’s home region or selected geographies, typically for data residency or compliance requirements. |

Expand

Show lessSee more

For more information about the cross-region routing parameter, see [CORTEX\_ENABLED\_CROSS\_REGION](/sql-reference/parameters#cortex-enabled-cross-region).

## Features that use AI Credit pricing

The following features use AI Credit pricing. For complete details, see Table 6 of
[Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

| Feature | Pricing type |
| --- | --- |
| Cortex Code | AI Credit |
| Cortex Agents | AI Credit |
| Snowflake CoWork | AI Credit |
| Cortex REST API | AI Credit |
| AI Functions | AI Credit |
| Cortex Search | AI Credit |
| Cortex Batch Search | AI Credit |
| AI Parse Doc | AI Credit |
| Cortex Fine-tuning | Platform Credit (legacy) |
| Cortex Analyst API | Platform Credit (legacy) |

Expand

Show lessSee more

## Feature pricing details

### Snowflake CoWork

Snowflake CoWork is billed in AI Credits based on token consumption. Snowflake CoWork uses agents to orchestrate multi-step workflows. Costs are additive across the underlying services the agent invokes (such as Cortex Analyst and Cortex Search). The specific rate depends on the model selected for orchestration. You can monitor per-agent usage through the [SNOWFLAKE\_COWORK\_USAGE\_HISTORY](/sql-reference/account-usage/snowflake_cowork_usage_history_view) view.

### Cortex Agents

Cortex Agents are billed in AI Credits per million tokens processed. Because agents orchestrate multi-step workflows, costs are additive across the underlying services the agent invokes (such as Cortex Analyst and Cortex Search). The specific rate depends on the model selected for orchestration. You can monitor per-agent usage through the [CORTEX\_AGENT\_USAGE\_HISTORY](/sql-reference/account-usage/cortex_agent_usage_history) view.

### Cortex Analyst

Snowflake recommends invoking Cortex Analyst through Cortex Agents, in which case the pricing is the same token-based AI Credit model as Cortex Agents. If you invoke Cortex Analyst directly through the standalone Analyst API, it’s billed per 1,000 messages. In both cases, executing the generated SQL incurs standard virtual warehouse compute charges.

### Cortex Search

Cortex Search is billed based on two components: serving compute and embedding compute. Serving compute is charged Credits per GB per month of indexed data (including vector embeddings) and runs continuously while the service is resumed. Embedding compute is charged per token when data is inserted or updated. For more details, see [Understanding cost for Cortex Search Services](/user-guide/snowflake-cortex/cortex-search/cortex-search-costs).

### Cortex Batch Search

Cortex Batch Search is billed Credits per GB per hour of indexed data for the duration of the batch job. Unlike interactive Cortex Search, serving compute only runs while the batch job is active rather than continuously. Additional costs include query embedding tokens and virtual warehouse compute for orchestration.

### AI Functions

AI Functions (such as AI\_COMPLETE, AI\_EMBED, AI\_CLASSIFY, and AI\_EXTRACT) are billed in AI Credits per million tokens processed. The rate varies by model. Both input and output tokens count toward consumption, and you can track usage through the CORTEX\_FUNCTIONS\_QUERY\_USAGE\_HISTORY view.

### Cortex REST API

The Cortex REST API is billed in AI Credits per million tokens. Prompt caching is supported, with cache reads billed at a reduced rate compared to standard input tokens. The specific per-token rate depends on the model you select.

### AI Parse Doc

AI Parse Doc is billed in AI Credits per 1,000 pages processed. The rate depends on the parsing mode.

## Additional details

AI Credit pricing only applies to the AI features listed above. Non-AI services such as warehouses,
storage, and data transfer continue to use Platform Credit pricing. Your existing capacity balance
and contract terms are unchanged, and no contract amendments are required.

No action is required to receive the ACV based discounts. Note that capacity discounts don’t apply to AI Credits.

## Example

Assume a customer has an Enterprise Edition account, where Platform Credits are $3.00 per credit and AI Credits are $2.00 per credit for global routing. If the customer uses 100 Platform Credits and 100 AI Credits, their spend would be:

- Platform usage: 100 credits × $3.00 = $300
- AI usage: 100 credits × $2.00 = $200
- Total spend: $500
