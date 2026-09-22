# SnowConvert AI - Redshift

The first step in migration is getting the code you need to migrate. There are many ways to extract the code from your database, but we recommend using the extraction scripts provided by Snowflake.

All the source code for these scripts is open source and is available on [GitHub](https://github.com/Snowflake-Labs/SC.DDLExportScripts/).

## Prerequisites

- Access to a Redshift cluster with a Redshift database.
- Access to the database preferably with a super user or database owner.
- Installation of AWS CLI.
- Access to the AWS Portal.

## Installing the scripts

Go to <https://github.com/Snowflake-Labs/SC.DDLExportScripts/>.

[![image](/static/images/migrations/sc-assets/Screenshot2025-01-28at8.37.01AM.png "image")](/static/images/migrations/sc-assets/Screenshot2025-01-28at8.37.01AM.png)

From the Code option, select the drop-down and use the **Download ZIP** option to download the code.

Decompress the ZIP file. The code for Redshift should be under the Redshift folder.

[![image](/static/images/migrations/sc-assets/Screenshot2025-01-28at8.39.54AM.png "image")](/static/images/migrations/sc-assets/Screenshot2025-01-28at8.39.54AM.png)

Follow the [Usage instructions](https://github.com/Snowflake-Labs/SC.DDLExportScripts/blob/main/Redshift/README.md) to modify the files and run them on your system.

## Package the results

When the script is done, the output folder will contain all the DDLs for the migration. You can then compress this folder to use it with [SnowConvert AI](../../../overview).

E.g. run:

Copy

Copy code

```
zip -r output.zip ./output
```
