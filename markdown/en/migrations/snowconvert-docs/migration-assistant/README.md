# SnowConvert AI - Migration Assistant

Visual Studio Code Extension

The SnowConvert AI Migration Assistant is an AI-powered tool designed to streamline the resolution of errors, warnings, and issues ([EWIs](../general/technical-documentation/issues-and-troubleshooting/conversion-issues/README)) encountered after converting SQL code using SnowConvert.

Integrated within the Snowflake Visual Studio Code extension, the Migration Assistant offers an interactive workflow for navigating, understanding, and fixing EWIs, accelerating your migration to Snowflake.

The assistant leverages the [Snowflake REST API](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-rest-api) to provide explanations and actionable suggestions for EWIs that SnowConvert AI cannot automatically resolve.

Warning

- The SnowConvert AI Migration Assistant uses **Snowflake Cortex AI** to provide helpful suggestions. Large language models can make mistakes, so it’s essential to review and validate all explanations and fixes before implementation.
- Using this tool requires signing in to your Snowflake account and having access to **SNOWFLAKE.CORTEX.COMPLETE** and at least one of the [supported models](model-preference#supported-models) by the Assistant.
- You can use [cross-region inference](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cross-region-inference) if your preferred models are not available in your default region.

## Key Features

- AI-driven analysis of EWIs using the Snowflake REST API.
- Explanations of EWI root causes.
- Chat interaction about SQL-related topics
- Actionable solutions and recommendations.
- Seamless integration with the Snowflake Visual Studio Code extension.

## Supported sources

SnowConvert AI Migration Assistant has been optimized for migrations with Microsoft SQL Server as a source database, and we recommend using it for migrations from this source.

The assistant is designed to work with all supported SnowConvert AI source databases, and in **future releases**, we will optimize results for a wider set of source databases.

## Learn More

- [Getting Started](getting-started/)
- [Troubleshooting](troubleshooting/)
- [Legal Notices](legal-notices/)
