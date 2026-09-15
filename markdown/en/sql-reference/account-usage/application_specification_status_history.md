Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# APPLICATION\_SPECIFICATION\_STATUS\_HISTORY view

The *APPLICATION\_SPECIFICATION\_STATUS\_HISTORY* view provides a history of the status changes for app specifications in your Snowflake account. Each row in the view represents a change in the status of an app specification, including when it was approved or declined or when the app creates a new request

The retention time for this view is 365 days, meaning that data older than 365 days will not be available in the view.

## Columns

The following table provides definitions for the *APPLICATION\_SPECIFICATION\_STATUS\_HISTORY* view columns.

| Column | Data type | Description |
| --- | --- | --- |
| ID | NUMBER | An internal, system-generated identifier for the app specification. |
| NAME | TEXT | The name of the app specification. |
| APPLICATION\_ID | NUMBER | An internal, system-generated identifier for the app that contains the app specification. |
| APPLICATION\_NAME | TEXT | The name of the app that contains the app specification. |
| TYPE | TEXT | The type of app specification. Possible values are EXTERNAL\_ACCESS, SECURITY\_INTEGRATION, and LISTING. |
| SEQUENCE\_NUMBER | NUMBER | The sequence number of the app specification. |
| USER\_NAME | TEXT | The name of the user that updated the app specification status. This field is empty if the app specification is a new pending request created by the app. |
| STATUS | TEXT | The status of the app specification. Possible values are: APPROVED, PENDING, DECLINED. |
| STATUS\_UPDATED\_ON | TIMESTAMP\_LTZ | The timestamp when the app specification was last updated, including when it was created, approved, or declined. |
| LABEL | TEXT | A label containing the name of the app specification that is displayed to consumer in Snowsight. |
| DESCRIPTION | TEXT | A description on the app specification that is displayed to the consumer. |
| DEFINITION | TEXT | The fields that comprise the app specification definition. For more information, see [Use app specifications to request controlled access](/developer-guide/native-apps/requesting-app-specs). |

Expand

Show lessSee more
