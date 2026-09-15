# Cortex Playground

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

The Cortex Playground lets you compare text completions across the multiple large language models available in
Cortex AI. You can test language model responses across prompts and model settings, and perform side-by-side comparisons
of model outputs. With a few clicks, you can also connect the model to a Snowflake table to experiment directly on your
data. The Cortex Playground is purpose-built to help you easily test how different language models perform for your
use case before you decide which model to deploy into production.

The Cortex Playground supports all of the models available for the COMPLETE function that are available in your
account’s region. For the complete list of models, see [Model availability](/user-guide/snowflake-cortex/aisql-regional-availability#label-cortex-llm-availability).

## Required privileges

The Cortex Playground requires the CORTEX\_USER database role that includes the privileges to call Snowflake Cortex LLM functions.
For more information, see [Cortex LLM privileges](/user-guide/snowflake-cortex/aisql-privileges-and-access#label-cortex-llm-privileges).

## Get started with the Cortex Playground

The Cortex Playground is accessible from the Snowflake AI & ML Studio. You can access the studio from Snowsight as follows:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **AI & ML** » **AI Studio**. The Cortex Playground appears among other the other Studio functions.

   ![Cortex playground box.](/static/images/cortex-llm/cortex-playground-studio.png)
3. To open the playground, select **Try**.

## Test your prompt with a language model

Use the Cortex Playground to test prompts across different language models.

1. Select a warehouse. This warehouse is used to run the SQL command that calls the COMPLETE function.
2. Select a model from the dropdown menu at the top. The drop down menu includes only the models that are available in the region
   of the account being used.

   ![Cortex playground model list.](/static/images/cortex-llm/cortex-playground-models.png)
3. Enter your prompt in the prompt box and select `Enter`.
4. The model output appears above the prompt box. You can select **View Code** to see and copy the SQL command used to process your prompt.

To try a different prompt or model, choose the desired model and enter a new prompt in the prompt box, then select `Enter`.

## Compare model outputs

To compare the output of your prompts between two different models or two different settings of the same model, use the **Compare**
feature.

### Compare two models

1. Select **Compare** in the top right corner.
2. Select different models for the two panels using the dropdown menu on each side.
3. Open the settings panel by selecting **Change settings** [![Open settings button.](/static/images/snowsight/icons/settings-menu-icon.png)](/static/images/snowsight/icons/settings-menu-icon.png) next to **Compare**.
4. Select the **Sync** toggle to use the same settings for the two models.
5. Enter your prompt and select `Enter`. The output from the models you selected appears on each side.

### Compare settings for one model

1. Select **Compare** in the top right corner.
2. Select the same model for the two panels.
3. Open the settings panel by selecting **Change settings** [![Open settings button.](/static/images/snowsight/icons/settings-menu-icon.png)](/static/images/snowsight/icons/settings-menu-icon.png) next to **Compare**.
4. Choose different settings for **temperature**, **top\_p** or **max\_tokens** for each tab to compare how the language model response
   changes with different model settings. For more details on these parameters, see
   [AI\_COMPLETE](/sql-reference/functions/ai_complete).
5. You can also check **Enable Cortex Guard** to implement safeguards that filter out potentially inappropriate or unsafe large
   language model (LLM) responses. For more details on Cortex Guard, see [Cortex Guard](/sql-reference/functions/ai_complete-single-string#label-cortex-llm-complete-cortex-guard).
6. Enter your prompt and select `Enter`. The output from the model for each set of settings appears on each side.

## Connect to Snowflake tables

You can connect the model to a Snowflake table with textual data that you want to test with text completion.

Note

You can select only one column. The Cortex Playground returns at most 100 rows.

1. Select the **+ Connect your data** button in the prompt box.
2. Select your Snowflake data source from the drop down menu.
3. Select the column with the textual data you want to test.
4. Select a column to use as a filter. You can use this column to select a record from your data source.
5. Select **Done**.
6. Select a record from your data source using the **Select <filter column>** field in the prompt box. You can select a record by
   scrolling or by searching for a term in the text data. To search, enter a term in the search box. The following example shows
   a filter column named **ID**. In this example, you could search for a particular ID number or enter a string to match the text data.

   ![Cortex playground connect data.](/static/images/cortex-llm/cortex-playground-connect-data.png)
7. Enter a **System Prompt** and select `Enter` to see the model response. A system prompt provides instructions to the model on how
   to process the input text. For example, you might want the model to summarize the selected text or pull out keywords from it.

## Controlling settings

You can adjust model settings to compare how the language model response changes when provided with different **temperature**,
**top\_p**, and **max\_tokens** settings. To implement safeguards that filter out potentially inappropriate or unsafe
responses, select **Enable Cortex Guard** in the settings panel.

You can read more about how these settings potentially impact language model responses in the
[AI\_COMPLETE (Prompt object)](/sql-reference/functions/ai_complete-prompt-object#label-cortex-complete-temperature-tokens) page.

1. Select **Change settings** [![Open settings button.](/static/images/snowsight/icons/settings-menu-icon.png)](/static/images/snowsight/icons/settings-menu-icon.png) to open the settings menu on the top right corner.
2. Check the box for the setting to adjust its value.

   ![Cortex playground model settings.](/static/images/cortex-llm/cortex-playground-settings.png)
3. Try out prompts with different settings.

## Exporting a SQL query

To get a SQL query that includes the settings, such as temperature, that you’ve defined in the Cortex Playground,
select **View Code** after any model response. The displayed code can be executed from a
[worksheet](/user-guide/ui-snowsight-worksheets-gs) or [notebook](/user-guide/ui-snowsight/notebooks), or
automated for continuous execution using [streams and tasks](/user-guide/data-pipelines-intro).
You can also use this code with a [dynamic table](/user-guide/dynamic-tables/overview).

Note

Dynamic tables do not support incremental refresh with COMPLETE.

The following images show examples of the **View SQL** dialog.

![Exporting SQL with data connected](/static/images/cortex-llm/cortex-playground-export-code-connected.png)

Example 1: Exporting code when you connect the model to a Snowflake table

![Exporting code without data connected](/static/images/cortex-llm/cortex-playground-export-code.png)

Example 2: Exporting code when you do not connect the model to a Snowflake table
