# Summit announcements: June 02-05, 2025

The following major features and enhancements were announced during Summit 2025.

Important

This topic does not include every feature or enhancement announced during Summit 2025. In particular, it does not include features
and enhancements that were announced, but are not yet in public preview or generally available.

## SQL updates

### Defining semantic views (*General availability*)

The ability to define [semantic views](/user-guide/views-semantic/overview) (which are schema-level objects that correspond
to semantic models) is now generally available.

To create and manage semantic views, you can use SQL commands (such as [CREATE SEMANTIC VIEW](/sql-reference/sql/create-semantic-view)) and the
[Cortex Analyst Semantic View Generator](/user-guide/views-semantic/ui), which is a wizard in Snowsight that guides you
through the process of creating a semantic view.

Once you create a semantic view, Cortex Analyst can leverage the information in the semantic view definition and generate the
SQL against the physical tables directly. Semantic views can improve the accuracy of responses by combining LLM reasoning with
rule-based definitions.

For more information, see [Overview of semantic views](/user-guide/views-semantic/overview).

### Querying semantic views (*Preview*)

The ability to query semantic views is now available as a preview feature. You can now use a SELECT statement to query a
semantic view by specifying the [SEMANTIC\_VIEW](/sql-reference/constructs/semantic_view) clause. In this clause, you specify the
dimensions and metrics that you want to retrieve. You can also filter the results based on dimensions.

For information, see [Querying semantic views](/user-guide/views-semantic/querying).

## Data loading / unloading updates

### Snowpipe Streaming with high-performance architecture (*Preview*)

With this release, we’re pleased to announce the preview of Snowpipe Streaming’s new high-performance architecture. This
next-generation implementation delivers significantly enhanced throughput and optimized streaming performance with a predictable,
throughput-based pricing model (credits per uncompressed GB). It utilizes the new Snowpipe Streaming SDK and introduces a PIPE
object for managing data flow, enabling lightweight transformations during ingestion and server-side schema validation. We
recommend evaluating this advanced architecture for new streaming projects due to its performance, scalability, and cost
predictability.

For more information, see [Snowpipe Streaming key concepts](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-overview).

## Snowflake Native App Framework

With this release, the Snowflake Native App Framework supports the following features:

### Restricted caller’s rights (*Preview*)

Snowflake Native App Framework supports using restricted caller’s rights in stored procedures and Snowpark Container Services service in an app.
Restricted caller’s rights allow a stored procedure or service to run with caller’s rights, but restricts which of the caller’s privileges they run with.

See [Restricted Caller’s Rights](/developer-guide/restricted-callers-rights) and
[Use owner’s rights and restricted caller’s rights in an app](https://other-docs.snowflake.com/en/native-apps/consumer-restricted-callers-rights) for more information.

### Feature policies (*Preview*)

In this release, the Snowflake Native App Framework introduces feature policies.
Feature policies allow consumers to restrict the types of objects an app can create.
For example, consumers can create a feature policy to prohibit an app from creating a warehouse.
If an app attempts to create a warehouse during installation, the installation fails.
See [Use feature policies to limit the objects an app can create](https://other-docs.snowflake.com/en/native-apps/consumer-feature-policies) for more information.

### Support for Snowflake ML in Snowflake Native Apps (*Preview*)

The Snowflake Native App Framework supports models created using [Snowflake ML](/developer-guide/snowflake-ml/overview).
Providers can include access to pre-trained models in an app or train a model after the app is installed. The app can train models on data in the provider or consumer accounts.

See [Use Snowflake machine learning models in a Snowflake Native App](/developer-guide/native-apps/snowflake-ml-na-about) for more information.
