# Governance and availability

Cortex AI features fit into Snowflake’s broader approach to governance, availability, and cost management.
This documentation brings together the key guidance for understanding model availability, regional behavior, budgets, and access management across Snowflake AI & ML.

## Cross-region inference

Many Snowflake AI features support [cross-region inference](/user-guide/snowflake-cortex/cross-region-inference), which allows inference requests to be processed in a different region when the requested model or feature is not available in your account’s default region.
Learn when cross-region inference applies, how regional and global availability differ, and how pricing may vary depending on where inference is served.

## Model availability

[Model and feature availability](/user-guide/snowflake-cortex/aisql-regional-availability#label-cortex-llm-availability) can vary by region and georegion.
Find which models are available where, along with relevant lifecycle and status information to help plan adoption, manage change, and understand whether a feature is available natively in-region or through cross-region inference.
After a model enters the [legacy](/user-guide/snowflake-cortex/aisql-regional-availability#label-cortex-model-lifecycle)
state, only accounts that already used it can continue to call it until end-of-life.

## Cost governance and budgets

Snowflake provides usage views and budget features to help monitor AI consumption, understand spend, and respond when usage approaches configured limits.
[Track AI-related usage](/user-guide/snowflake-cortex/governance-and-availability/ai-cost-management-and-governance), connect consumption to billing, and use budgets to support internal monitoring, notifications, and spending controls across supported AI features using.

## Access controls

Across Snowflake AI & ML, most features already include access controls.
The [Cortex User role](/user-guide/snowflake-cortex/aisql), [role based access control for models](/user-guide/snowflake-cortex/aisql-privileges-and-access#label-cortex-llm-rbac), [Agent user role](/user-guide/snowflake-cortex/cortex-agents-setup#label-cortex-agents-access-control), and [Snowflake CoWork user](/user-guide/snowflake-cortex/snowflake-cowork) span part of the current feature set and show how access is managed in different product areas.
Together, these capabilities support how access is granted, managed, and restricted across features.
