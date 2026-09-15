Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# APPLICATION\_SPECIFICATIONS view

The *APPLICATION\_SPECIFICATIONS* displays a list of all app specifications created your Snowflake account.
Each row in the view represents an app specification. Deleted app specifications are also included in the view.
Because an app specification can be deleted and recreated with the same name. To differentiate between app specifications
with the same name, use the ID column.

The retention time for deleted app specifications is 365 days. Data older than 365 days will not be available in the view.

## Columns

The following table provides definitions for the *APPLICATION\_SPECIFICATIONS* view columns.

| Column | Data type | Description |
| --- | --- | --- |
| ID | NUMBER | An internal, system-generated identifier for the app specification. |
| NAME | TEXT | The name of the app specification. |
| APPLICATION\_ID | NUMBER | An internal, system-generated identifier for the app that contains the app specification. |
| APPLICATION\_NAME | TEXT | The name of the app that contains the app specification. |
| CREATED | TIMESTAMP\_LTZ | The timestamp when the app specification was created. |
| DELETED | TIMESTAMP\_LTZ | The timestamp when the app specification was deleted. This value is NULL if the app specification has not been deleted. |
| TYPE | TEXT | The type of app specification. Possible values are EXTERNAL\_ACCESS, SECURITY\_INTEGRATION, and LISTING. |
| SEQUENCE\_NUMBER | NUMBER | The sequence number of the app specification. |
| REQUESTED\_ON | TIMESTAMP\_LTZ | The timestamp when the app created the app specification. |
| STATUS | TEXT | The status of the app specification. Possible values are: APPROVED, PENDING, or DECLINED. |
| STATUS\_UPDATED\_ON | TIMESTAMP\_LTZ | The timestamp when the app specification was last updated, including when it was created, approved, or declined. |
| LABEL | TEXT | A label containing the name of the app specification that is displayed to consumer in Snowsight. |
| DESCRIPTION | TEXT | A description of the app specification. This description is displayed to the consumer. |
| DEFINITION | TEXT | The fields that comprise the app specification definition. For more information, |

Expand

Show lessSee more
