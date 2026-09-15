# SnowConvert AI: Extraction

SnowConvert AI provides the following options for extracting database objects:

- [Extract code](#extract-code): For SQL Server and Amazon Redshift databases, use this option if you don’t already have code for extracted database objects.
- [Load existing code](#load-existing-code): For any source database, use this option if you already have code for extracted database objects.
  You might already have code if you previously extracted the code by using SnowConvert AI or if you generated the code yourself.

## Extract code

SnowConvert AI, as part of the end-to-end migration experience, offers the option to extract database objects from your source system to prepare them for the conversion process. This extraction feature is available for SQL Server and Amazon Redshift databases, letting you connect to your source database, browse the catalog, and select specific objects for migration.

The extraction process supports different database objects depending on your source database type:

**SQL Server Objects**

- Tables
- Views
- Functions
- Stored procedures

**Amazon Redshift Objects**

- Tables
- Views
- Materialized views
- Stored procedures

To extract database objects from a source system, complete the following steps:

1. [Create the project](./project-creation), and then select **Continue**.
2. On the **Add code to your project** page,select **Extract code**.

   The **Set up code and ETL/BI projects** page appears. The following image is an example of the page
   for SQL Server:

   [![](/static/images/migrations/sc-assets/sql-standard.png "SQL Standard")](/static/images/migrations/sc-assets/sql-standard.png)
3. In **Authentication Method**, select the authentication method that you want to use to connect to the source system.
   The following authentication methods are supported:

   - **SQL Server**
     - **Standard Authentication**
     - **Windows Authentication**
   - **Amazon Redshift**
     - **Standard Authentication**
     - **IAM Provisioned Cluster**
     - **IAM Serverless**

   When you select an authentication method, the other fields on the page are refreshed based on the method.
4. To provide appropriate information for your authentication method, complete the remaining fields.
5. For SQL Server migrations, both authentication methods require verification about whether the following security settings
   are configured for your source database:

   - **Trust server certificate**: Enable if the database requires trusted certificate validation.
   - **Encrypt connection**: Enable if the database requires encrypted connections.
6. In **Where should the converted code be saved?**, select **Browse**, and then choose a location for the code.
7. In **Have ETL projects or BI/reports?**, select the options that you want to use for
   [replatforming](./etl-migration-replatform) or [repointing](./power-bi-repointing-general), and then
   select the corresponding files.
8. Select **Continue**.
9. On the **Select objects to extract** page, choose the objects that you want to migrate.

   The system retrieves the metadata and structure information for the selected objects.

   The following image shows a sample **Select objects to extract** page:

   [![](/static/images/migrations/sc-assets/sql-extraction-objects.png "SQL Extraction Objects")](/static/images/migrations/sc-assets/sql-extraction-objects.png)
10. Select **Extract objects**.
11. Review the extraction results.

    The following image shows a sample **Extraction resultst** window:

    [![](/static/images/migrations/sc-assets/sql-extraction-results.png "SQL Extraction results")](/static/images/migrations/sc-assets/sql-extraction-results.png)

When extraction is complete, move on to [Next steps](#next-steps).

## Load existing code

To load existing code for extracted database objects, complete the following steps:

1. [Create the project](./project-creation), and select **Continue**.
2. On the **Add code to your project** page, select **Already have code**.

   The **Set up code and ETL/BI projects** page appears. The following image is an example of the page
   for SQL Server:

   [![](/static/images/migrations/sc-assets/sql-standard-load-code.png "SQL Standard load code")](/static/images/migrations/sc-assets/sql-standard-load-code.png)
3. On the **Set up code and ETL/BI projects** page, specify the following information:

   - **Where is your source code?**: Select **Browse**, and then choose the location of your source code.
   - **Where should the converted code be saved?**: Select **Browse**, and then choose the location of your converted code.
4. In **Have ETL projects or BI/reports?**, select the options that you want to use for
   [replatforming](./etl-migration-replatform) or [repointing](./power-bi-repointing-general), and then
   select the corresponding files.
5. Select **Continue**.

When extraction is complete, move on to [Next steps](#next-steps).

## Next steps

Note

Only successfully extracted objects will be available for the subsequent conversion step.

After completing the extraction process, you can proceed to the [conversion process](../getting-started/running-snowconvert/conversion/README) to transform your database objects for Snowflake compatibility.
