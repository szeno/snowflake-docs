# SnowConvert AI: Project Creation

SnowConvert AI manages migrations by using SnowConvert AI projects. A SnowConvert AI project contains metadata about migrating a data set into Snowflake, such as the source database platform, input files, and output location. You can save and reuse these settings for multiple conversion runs.

To create a new project, complete the following steps:

1. Open SnowConvert AI, and then select **New Project**.

   The **New Project** page appears:

   [![](/static/images/migrations/sc-assets/snowconvert-create-project.png "Create Project")](/static/images/migrations/sc-assets/snowconvert-create-project.png)
2. Enter the following information:

   - **Project name**: The name of the project.
   - **Select source**: The type of the source database system; for example, SQL Server, Oracle, and so on.
3. To use Snowflake Cortex to help verify and fix migration objects, turn on **AI features**.

   If you don’t want to use Snowflake Cortex for the migration, turn off **AI features**.

   For more information about Snowflake Cortex, see [Snowflake AI and ML](https://docs.snowflake.com/en/guides-overview-ai-features).
4. For **Snowflake connection**, optionally enter the information required to connect to your Snowflake account.
5. Select **Save Project**.

After creating a project, you can proceed to the [extraction process](./extraction) to extract database objects from your source system to prepare them for the conversion process.
