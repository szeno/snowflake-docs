# June 03-06, 2024 — Summit announcements

The following major features and enhancements were announced during Summit 2024.

Important

This topic does not include every feature or enhancement announced during Summit 2024. In particular, it does not include features
and enhancements that were announced, but are not yet in public preview or generally available.

## New features

### Specify appearance in Snowsight — *Preview*

With this release, we are pleased to announce the preview of specifying appearance, often referred to as dark mode, in [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
You can now specify the color scheme for Snowsight, including a scheme using darker colors with light text on a dark background
designed to reduce eye strain in low-light conditions and provide a comfortable browsing experience for users who prefer darker color palettes.

This new feature includes three settings:

- System - Use the same mode as specified by the operating system running Snowsight.
- Light - Traditional dark characters on a lighter background, typically used in normal daylight.
- Dark - Light text on a dark background to reduce eye strain in low-light conditions.

For more information and to learn how to specify appearance in Snowsight, see [Specify appearance](/user-guide/ui-snowsight-profile#label-snowsight-specify-appearance).

### Snowflake Native SDK for Connectors — *Preview*

We are pleased to announce the preview of the Snowflake Native SDK for Connectors.

The Snowflake Native SDK for Connectors is a library with templates and quickstarts in Java that you can use to quickly build your own
Snowflake Native App based Connectors to easily ingest data from an external data source into Snowflake. The sample connector in the
SDK outlines best practices to ingest data and customize application flows, along with ready-to-use code blocks for your own ingestion
logic.

For more information see [Snowflake Native SDK for Connectors](/developer-guide/native-apps/connector-sdk/about-connector-sdk).

### Snowflake Notebooks — *Preview*

We are pleased to announce the preview of Snowflake Notebooks. Snowflake Notebooks is a development interface in [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in)
that offers an interactive, cell-based programming environment for Python and SQL. In Snowflake Notebooks, you can perform exploratory
data analysis, develop machine learning models, and perform other data science and data engineering tasks all in one place.

For more information, see [About Legacy Snowflake Notebooks](/user-guide/ui-snowsight/notebooks).

### Snowpark pandas API — *Preview*

We are pleased to announce the preview of the Snowpark pandas API. The Snowpark pandas API lets you run your pandas code directly on your
data in Snowflake.

Just by changing the import statement and a few lines of code, you can get the same pandas-native experience with the scalability and
security benefits of Snowflake. With this API, you can work with much larger datasets so you can avoid rewriting your pandas pipelines to
other big data frameworks. Snowpark pandas runs workloads natively in Snowflake through transpilation to SQL, enabling it to take advantage
of parallelization and the data governance and security benefits of Snowflake.

For more information, see [pandas on Snowflake](/developer-guide/snowpark/python/pandas-on-snowflake).

### Snowflake Cortex Fine-Tuning — *Preview*

Fine-tuning allows users to adapt pre-trained models to more specialized tasks. If you don’t want the high cost of training a large model
from scratch but need better latency and results than you’re getting from prompt engineering or even retrieval augmented generation (RAG)
methods, fine-tuning an existing large model is an option. Fine-tuning allows you to use examples to adjust the behavior of the model and
improve the model’s knowledge of domain-specific tasks.

Cortex Fine-Tuning is a fully managed service that lets you fine-tune popular large language models using your data all within Snowflake.

For more information, see [Fine-tuning (Snowflake Cortex)](/user-guide/snowflake-cortex/cortex-finetuning).

### Snowflake Native Apps with Snowpark Container Services — *Preview*

We are pleased to announce the preview of Snowpark Native Apps with Snowpark Container Services.

Snowflake Native Apps with Snowpark Container Services allows you to run any containerized service supported by
Snowpark Container Services within a Snowflake Native App.
Snowflake Native Apps with Snowpark Container Services leverage all of the features of the Snowflake Native App Framework,
including provider IP protection, security and governance, data sharing, monetization, and integration with compute resources.

For more information, see [About Snowflake Native Apps with Snowpark Container Services](/developer-guide/native-apps/native-apps-about#label-native-apps-about-na-spcs).

### Apache Iceberg™ tables — *General availability*

We are pleased to announce the general availability of Apache Iceberg™ tables for Snowflake, released with Snowflake version 8.20.

Iceberg tables for Snowflake combine the performance and query semantics of regular Snowflake tables
with external cloud storage that you manage. They are ideal for maintaining a single copy of data
with interoperability across a variety of compute engines.

For more information, see [Apache Iceberg™ tables](/user-guide/tables-iceberg).

## Extensibility updates

### Snowpark Python local testing framework — *General availability*

We are pleased to announce the general availability of the Snowpark Python local testing framework, which was previously available as a
preview feature. This local testing framework is an emulator that lets you test your Python code locally when working with the Snowpark Python
library.

The Snowpark Python local testing framework allows you to create and operate on Snowpark Python DataFrames locally without connecting to a
Snowflake account. You can use the local testing framework to test your DataFrame operations on your development machine or in a
CI (continuous integration) pipeline before deploying code changes to your account. The API is the same, so you can either run your tests
locally or against a Snowflake account without making code changes.

For more information, see [Local testing framework](/developer-guide/snowpark/python/testing-locally).

## Snowsight updates

### Universal Search — *General availability*

We are pleased to announce the general availability of Universal Search in [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).

With Universal Search, you find even more objects than before, quickly and securely. Searching from the Search tab finds tables, functions,
databases, data products available to you in the Snowflake Marketplace, relevant Snowflake Documentation topics, and related articles in the
Snowflake Community Knowledge Base. With general availability, Universal Search now includes worksheets and dashboards in your search results.
Whether you enter a single word or a complete question in natural language, Universal Search can interpret your query by using your customizable
Snowflake asset metadata.

For more information, see [Search Snowflake objects and resources](/user-guide/ui-snowsight-universal-search).
