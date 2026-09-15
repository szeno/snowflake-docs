Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# CORTEX\_DOCUMENT\_PROCESSING\_USAGE\_HISTORY view

This Account Usage view displays document processing function activity, including [PARSE\_DOCUMENT (SNOWFLAKE.CORTEX)](/sql-reference/functions/parse_document-snowflake-cortex),
[AI\_EXTRACT](/sql-reference/functions/ai_extract), and `<model_build_name>!PREDICT` calls. It shows pages processed and credits
used, aggregated hourly by function and model. The view includes metadata such as the following:

- Warehouse ID
- Execution timestamps
- Function names
- Model names

Decommissioned Feature

Document AI and the `model_build_name!PREDICT` method are decommissioned. For more information, see [Document AI decommission](/release-notes/bcr-bundles/un-bundled/bcr-2156).

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| QUERY\_ID | VARCHAR | A unique identifier for the SQL query |
| CREDITS\_USED | NUMBER(38,9) | The number of credits billed for Cortex Document processing functions for the specified query |
| START\_TIME | TIMESTAMP\_LTZ | Start of the hourly time range in which the query usage took place. |
| END\_TIME | TIMESTAMP\_LTZ | End of the hourly time range in which the query usage took place. |
| FUNCTION\_NAME | TEXT | The name of the Cortex Document processing function |
| MODEL\_NAME | TEXT | The name of the model |
| OPERATION\_NAME | TEXT | The name of the operation  Valid values:   - `inference` - `train` |
| PAGE\_COUNT | NUMBER | The number of pages processed |
| DOCUMENT\_COUNT | NUMBER | The number of documents processed |
| FEATURE\_COUNT | NUMBER | The number of data values defined for document processing operations that involve entry extraction |

Expand

Show lessSee more

## Usage notes

- The view provides up-to-date credit usage for an account within the last 365 days (1 year).
- Credit rate usage is based on the number of messages processed, as outlined in the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).
