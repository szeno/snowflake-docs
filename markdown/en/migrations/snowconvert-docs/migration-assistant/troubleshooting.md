# SnowConvert AI - Migration Assistant - Troubleshooting

Guidance on resolving issues you may encounter when using the SnowConvert AI Migration Assistant.

## **1. The Explanation or Fix suggestion is incorrect**

SnowConvert AI Migration Assistant uses Snowflake Cortex AI to generate suggestions and explanations using Large Language Models (LLMs). These models can make mistakes, so please review each output thoroughly and carefully before applying it.

## **2. Error when trying to run Cortex**

If an error occurs when executing the Snowflake Cortex, verify that your Snowflake account has access to Snowflake Cortex features, specifically, the [COMPLETE](https://docs.snowflake.com/en/sql-reference/functions/complete-snowflake-cortex) function, and the [models](model-preference#supported-models) you selected.

If one or more of your selected models are not available in your default Snowflake region, you can configure [Cross-Region Inference](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cross-region-inference) to allow Cortex calls to process in a region where they are available.

Access to these features is **necessary** to use the AI capabilities of the SnowConvert AI Migration Assistant.

## **3. No issues are listed in the SnowConvert AI Issues panel**

If no issues are listed, make sure you have selected a file with the .sql extension that contains EWIs, which are included in the .sql files that SnowConvert AI provides.

## **4. Removed issues are still on the list**

To remove EWIs you’ve resolved from the SnowConvert AI Issues list, refresh the list using the refresh button at the top of the list.
