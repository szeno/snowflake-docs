Schema:
:   [TRUST\_CENTER](/sql-reference/trust_center)

# EXTENSIONS view

The SNOWFLAKE.TRUST\_CENTER.EXTENSIONS view displays a row for each extension that is registered with
the Trust Center.

For more information, see [Using Trust Center extensions](/user-guide/trust-center/trust-center-extensions).

The view has the following columns:

## Columns

| Column name | Data type | Description |
| --- | --- | --- |
| NAME | VARCHAR | The name of the extension. |
| ID | NUMBER | The identifier of the extension. |
| SOURCE\_TYPE | VARCHAR | The source type of the extension:   - `APPLICATION PACKAGE` - `LISTING` |
| SOURCE | VARCHAR | If the source type is `APPLICATION PACKAGE`, the name of the application package. If the source type is `LISTING`, the identifier of the listing. |
| VERSION | VARCHAR | The version of the Snowflake Native App extension that is registered with the Trust Center. |
| PATCH | NUMBER | The patch number of the Native App extension that is registered with the Trust Center. |
| PREVIOUS\_VERSION | VARCHAR | The previous version of the Native App extension that is registered with the Trust Center. |
| PREVIOUS\_PATCH | NUMBER | The previous patch number of the Native App extension registered with the Trust Center. |
| REGISTRATION\_STATE | VARCHAR | The state of the registration of the extension with the Trust Center:   - `COMPLETED` - `IN_PROGRESS` - `FAILED` |
| REGISTRATION\_TARGET\_VERSION | VARCHAR | The version of the Native App extension that is in the process of being registered with the Trust Center. |
| REGISTRATION\_TARGET\_PATCH | NUMBER | The patch number of the Native App extension that is in the process of being registered with the Trust Center. |
| REGISTRATION\_ATTEMPTED\_ON | TIMESTAMP\_LTZ | The timestamp of the last attempted registration. |
| REGISTRATION\_FAILURE\_REASON | VARCHAR | If the last attempted registration failed, the reason for the failure. Otherwise, NULL. |
| REGISTERED\_TIMESTAMP | TIMESTAMP\_LTZ | The timestamp for when the extension was registered with the Trust Center for the first time. |

Expand

Show lessSee more
