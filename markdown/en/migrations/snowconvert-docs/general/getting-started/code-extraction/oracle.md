# SnowConvert AI - Oracle

The first step for migration is getting the code that you need to migrate. There are many ways to extract the code from your database. However, we recommend using the extraction scripts provided by Snowflake.

All the source code for these scripts is open source and is available on [GitHub](https://github.com/Snowflake-Labs/SC.DDLExportScripts/).

## Prerequisites

- Access to a server with an Oracle database.
- Permission to run shell scripts with access to the server.
- Tools to connect to the Database like [`sqlplus`](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqpug/SQL-Plus-quick-start.html#GUID-BF1995BD-EF9B-4EA2-9B32-7BFACDEB79DA) or [`sqlcl`](https://www.oracle.com/database/technologies/appdev/sqlcl.html)

## Installing the scripts

Go to <https://github.com/Snowflake-Labs/SC.DDLExportScripts/>

[![image](/static/images/migrations/sc-assets/DDLExportScripts.png "image")](/static/images/migrations/sc-assets/DDLExportScripts.png)

From the Code option, select the drop-down and use the **Download ZIP** option to download the code.

Decompress the ZIP file. The code for Oracle should be under the Oracle folder

[![](/static/images/migrations/sc-assets/image(359).png)](/static/images/migrations/sc-assets/image(359).png)

When the script is done, the output folder will contain all the DDLs for the migration.

Follow the [Usage instructions](https://github.com/Snowflake-Labs/SC.DDLExportScripts/tree/main/Oracle#readme) to modify the files and run them on your system.

You can then compress this folder to use with [SnowConvert AI](../../../overview)

Copy code

```
zip -r output.zip ./output
```
