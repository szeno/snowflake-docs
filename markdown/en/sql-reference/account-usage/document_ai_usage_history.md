Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# DOCUMENT\_AI\_USAGE\_HISTORY view

Decommissioned Feature

Document AI and the `model_build_name!PREDICT` method are decommissioned. For more information, see [Document AI decommission](/release-notes/bcr-bundles/un-bundled/bcr-2156).

The DOCUMENT\_AI\_USAGE\_HISTORY view can be used to query the job history for Document AI.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| START\_TIME | TIMESTAMP\_LTZ | Start of the hourly time range in which the query usage took place. |
| END\_TIME | TIMESTAMP\_LTZ | End of the hourly time range in which the query usage took place. |
| CREDITS\_USED | NUMBER(38,9) | Number of credits used for Document AI compute between START\_TIME and END\_TIME. |
| QUERY\_ID | VARCHAR | A unique identifier for the SQL query. |
| OPERATION\_NAME | TEXT | Name of the Document AI operation: `Inference` (entity extraction) or `Inference-Table-Extraction` (table extraction). |
| PAGE\_COUNT | NUMBER | Number of pages processed. |
| DOCUMENT\_COUNT | NUMBER | Number of documents processed. |
| FEATURE\_COUNT | NUMBER | Number of data values defined to be extracted. |

Expand

Show lessSee more
