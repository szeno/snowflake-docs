# SnowConvert AI - Extraction Validation

## Description

This validation step verifies if the entry code was extracted, which means the Extraction Script tool was used.

Warning

**IMPORTANT**! There is only an Extraction Script tool for [Oracle](https://github.com/Snowflake-Labs/SC.DDLExportScripts/releases/latest/download/oracle.zip), [Teradata](https://github.com/Snowflake-Labs/SC.DDLExportScripts/releases/latest/download/teradata.zip), and [SQLServer](https://github.com/Snowflake-Labs/SC.DDLExportScripts/releases/latest/download/sql-server.zip) languages. The related link will download a .zip with the extraction script and instructions.

If the entry code is not extracted, the following warning is displayed:

[![Extraction Validation Failed](/static/images/migrations/sc-assets/image(9).png "image")](/static/images/migrations/sc-assets/image(9).png)

### Exception for SQLServer

In the case of SQLServer as an input language, the extraction script does not generate the file required to validate if this tool is being used or not thus if you follow all the instructions mentioned in the extraction script guide, you could create a .***sc\_extracted*** file and locate it at the root folder of the entry code to avoid that the warning of not extraction is displayed.
