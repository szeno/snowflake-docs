# SnowConvert AI: Power BI Repointing

This guide provides comprehensive instructions on utilizing SnowConvert AI for Power BI repointing to Snowflake. It details the process of migrating your existing Power BI reports and dashboards to leverage Snowflake as their underlying data source. You will learn how to prepare your Power BI reports, execute the SnowConvert AI tool, and validate the repointed reports to ensure seamless integration with Snowflake.

SnowConvert AI provides a new option to redefine their Power BI connections to the migrated databases in Snowflake. This redefinition of connections is called repointing. Repointing is executed inside the SnowConvert AI migration logic and uses the migration context to identify and migrate correctly embedded SQL queries.

## How To Use The Tool

Note

Notice that this feature only supports Power BI reports with the extension **.pbit**. Before starting, please save your reports to **.pbit** extension.

### Prerequisites

Before you begin, ensure you have the following:
SnowConvert AI: You need to have the tool installed. You can access it on the [SnowConvert AI page](https://www.snowflake.com/en/migrate-to-the-cloud/snowconvert-ai/).
Power BI reports: You need to download your reports and save them with the .pbit format.

#### How To Save A .Pbit Correctly

1. Open your report (.pbix) file and allow it to load.
2. Click on “File”.

[![](/static/images/migrations/sc-assets/Power_BI_Repointing/PBIClickOnFile.png "Click on File")](/static/images/migrations/sc-assets/Power_BI_Repointing/PBIClickOnFile.png)

3. Then click on “Save as”.

[![](/static/images/migrations/sc-assets/Power_BI_Repointing/PBISaveButton.png "Save As")](/static/images/migrations/sc-assets/Power_BI_Repointing/PBISaveButton.png)

4. Then click on “Browse this device”.

[![](/static/images/migrations/sc-assets/Power_BI_Repointing/PBIBrowseThisDevice.png "Browse this devise section")](/static/images/migrations/sc-assets/Power_BI_Repointing/PBIBrowseThisDevice.png)

5. Select the location to be saved and the extension as .pbit.

[![](/static/images/migrations/sc-assets/Power_BI_Repointing/PBIFileNamePbit.png "Save the template")](/static/images/migrations/sc-assets/Power_BI_Repointing/PBIFileNamePbit.png)

6. Click on “Save”.

[![](/static/images/migrations/sc-assets/Power_BI_Repointing/PBISaveButtonReport.png "Save report button")](/static/images/migrations/sc-assets/Power_BI_Repointing/PBISaveButtonReport.png)

7. Optionally, add a description and click on “Ok”.

[![](/static/images/migrations/sc-assets/Power_BI_Repointing/PBISaveTemplateDescription.png "Template report description")](/static/images/migrations/sc-assets/Power_BI_Repointing/PBISaveTemplateDescription.png)

### Migration steps

1. Locate all Power BI reports with .pbit extension in a folder.
2. In the SnowConvert AI app, add the path of the Power BI projects in the “Where is your SSIS/Power BI project(s)?” section.
3. Continue the migration steps as normally.

[![](/static/images/migrations/sc-assets/Power_BI_Repointing/PBISampleAddingPathPBIRepointing.png "Repointing Configuration")](/static/images/migrations/sc-assets/Power_BI_Repointing/PBISampleAddingPathPBIRepointing.png)

4. Reports: In the output folder, you can review the report named ETLAndBiRepointing about the repointing transformation.
5. Access: In the output folder, you can review the “repointing\_output” to access the Power BI repointing reports.
6. **Execution**: Before opening your reports, it is important to run all your migrated DDLs in your Snowflake account. Otherwise, the object will not be retrieved because they do not exist in the Snowflake account. So, follow the next steps:

   1. Run your migrated queries.
   2. Open your Power BI report.
   3. Fill in the Power BI parameters required: SF\_SERVER\_LINK, SF\_DB\_NAME, and SF\_WAREHOUSE\_NAME. For more information, please review the following [Power BI parameters documentation](https://learn.microsoft.com/en-us/power-query/power-query-query-parameters).

[![](/static/images/migrations/sc-assets/Power_BI_Repointing/PBIParameters.png "Power BI Parameters")](/static/images/migrations/sc-assets/Power_BI_Repointing/PBIParameters.png)

4. Click on load and wait until the report loads the information.
5. Provide your account credentials to the Power BI app. Additionally, if you have two-factor authentication, you may be asked to accept every connection request from Power BI. Be aware that there may be several pop-ups for authorization.
6. Review the ETLAndBiRepointing report and resolve every data entity with issues.
7. Double-check functionality.
8. Refresh the data and save your report in the format of your preference. It is now ready to be shared.

## Project structure

SnowConvert AI provides a new option to redefine their Power BI connections to the migrated databases in Snowflake. This redefinition of connections is referred to as repointing. Repointing is executed within the SnowConvert AI migration logic and utilizes the migration context to identify and migrate embedded SQL queries correctly.

Please refer to the specific source language Snowflake documentation that you are repointing:

1. [SQL Server](https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/transact/etl-bi-repointing/power-bi-transact-repointing)
2. [Oracle](https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/oracle/etl-bi-repointing/power-bi-oracle-repointing)
3. [Teradata](https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/teradata/etl-bi-repointing/power-bi-teradata-repointing)
4. [Redshift](https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/redshift/etl-bi-repointing/power-bi-redshift-repointing)
5. [Azure Synapse](https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/transact/etl-bi-repointing/power-bi-transact-repointing)
6. [PostgreSQL](https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/postgres/etl-bi-repointing/power-bi-postgres-repointing)

### Output structure overview

The output structure will resemble this and will include the repointed reports. The repointing output folder named repointing\_output will contain the repointed reports.

Additionally, a dedicated folder containing the extracted queries will be provided, named power\_bi\_sql\_queries. This folder serves a crucial purpose: to allow for a thorough double-check of all embedded SQL statements. These SQL statements will have been meticulously extracted from the applicable connectors within the Power BI environment.

Copy code

```
Output/
├── repointing_output/
│   ├── report1.pbit
│   ├── report2.pbit
│   └── reportN.pbit
└── power_bi_sql_queries/
    ├── query1.sql
    ├── query2.sql
    └── queryN.sql
```

On the other hand, in the input folder will remain the non-migrated SQL files from every single connector. If there is a need review of these.

Copy code

```
 Input/
└── power_bi_sql_queries/
    ├── query1.sql
    ├── query2.sql
    └── queryN.sql
```

## Support Capabilities

### The current version supports

1. Repointing of tables, views, and embedded SQL queries.
2. Maintain the remaining logic steps after the connection steps in the M Language (multiple lines).
3. Provides parameters inside Power BI to handle information correctly for Snowflake server link, warehouse and database name.
4. Convert queries saved as expressions (when the “Enable load” property has been disabled).
5. Renaming of columns based on related DDLs on the migration or by Power BI report references if DDLs are not provided.
6. Identification of views, if related DDLs are provided in the migration.
7. Multiple databases and schema repointing if these are using the selected platform connector in SnowConvert AI.

### Considerations

1. The schema name of the source connections is being used as the schema in the repointed connection. It is assumed that the Snowflake database objects were created under the same schema.
2. The database objects must be deployed in Snowflake before trying to open the repointed report.
3. If the column renaming step in the M Language is empty, it means that no information was found in the migration context or Power BI project references to create it.
4. Functions and procedures are not supported in connectors different from SQL Server and Azure Synapse, so these cases are not supported.
5. All found database connections related to the source language in the migration settings will be repointed, and [parameters](https://learn.microsoft.com/en-us/power-query/power-query-query-parameters) will be added.
6. Notice that other connections from other sources rather than the selected in the migration settings, are not being edited.

## Migration Reports

The ETLAndBiRepointing contains information about the repointing process. There are connectors that are not applicable for repointing, such as CSV files, JSON files, and SharePoint connections. These non-applicable connectors are unlikely to be edited, but it is recommended to double-check. It looks like the following sample:

[![](/static/images/migrations/sc-assets/Power_BI_Repointing/PBIReportSample.png "Power BI Repointing Report Sample")](/static/images/migrations/sc-assets/Power_BI_Repointing/PBIReportSample.png)

## Troubleshooting

1. If the user does not enter the requested global parameters after repointing, the load of objects is not triggered by Power BI; therefore, ensure that the parameter information is added. If
2. If the user clicks Cancel and the reports do not load, it is recommended to close and reopen the report.
3. If a visualization does not load, it may be because a column definition does not match the text case. Notice that the Snowflake connector from Power BI retrieves the entities and columns always in uppercase.
4. If you experience issues with the credential cache, you can navigate to the settings in Power BI and clear the connection to enter new credentials.
5. There may be problems with complex SQL queries after migration. These cases may require extra work to solve warning messages from the migration process (EWI - PRF - FDM).

## Limitations

1. Dynamic SQL embedded in connectors.
2. Column renaming is crucial for visualization loading. This renaming is not guaranteed to be precise due to limitations in the processed information. If no columns are found during the repointing, the default is to rename the columns based on a predefined case sensitivity. The default is uppercase because the native Snowflake connector retrieves all information in uppercase.
