# APPLICATION\_SPECIFICATION view

This Information Schema view displays a row for each app specification request currently defined
in the specified or current database where the information schema is located.

For more information about app specification, see
[Use app specifications to request controlled access](/developer-guide/native-apps/requesting-app-specs).

## Columns

The following table provides definitions for the *APPLICATION\_SPECIFICATIONS* view columns.

| Column | Data type | Description |
| --- | --- | --- |
| NAME | TEXT | The name of the app specification. |
| APPLICATION\_NAME | TEXT | The name of the app that contains the app specification. |
| TYPE | TEXT | The type of app specification. Possible values are EXTERNAL\_ACCESS, SECURITY\_INTEGRATION, and LISTING. |
| SEQUENCE\_NUMBER | NUMBER | The sequence number of the app specification. |
| REQUESTED\_ON | TIMESTAMP\_LTZ | The timestamp when the app created the app specification. |
| STATUS | TEXT | The status of the app specification. Possible values are: APPROVED, PENDING, or DECLINED. |
| STATUS\_UPDATED\_ON | TIMESTAMP\_LTZ | The timestamp when the app specification was last updated, including when it was created, approved, or declined. |
| LABEL | TEXT | A label containing the name of the app specification that is displayed to consumer in Snowsight. |
| DESCRIPTION | TEXT | A description of the app specification. This description is displayed to the consumer. |
| DEFINITION | TEXT | The fields that comprise the app specification definition. |

Expand

Show lessSee more
