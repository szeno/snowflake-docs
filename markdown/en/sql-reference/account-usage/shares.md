Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# SHARES view

This Account Usage view returns all the shares owned by the current account, including dropped shares. The information in this view has a latency of up to 3 hours.

## Columns

The following table provides definitions for the SHARES view columns.

| Column | Data type | Description |
| --- | --- | --- |
| CREATED\_ON | TIMESTAMP\_LTZ | The timestamp when the share was created. |
| MODIFIED\_ON | TIMESTAMP\_LTZ | The timestamp when the share was last updated. |
| DELETED\_ON | TIMESTAMP\_LTZ | The timestamp when the share was deleted. This value is NULL if the share hasn’t been deleted. |
| NAME | VARCHAR | The name of the share. |
| OWNER | VARCHAR | The name of the role that owns the share. |
| COMMENT | VARCHAR | Comment associated with the share, if any. |
| DATABASE\_NAME | VARCHAR | The name of the primary database associated with the share. This field is empty if no database has been granted to the share. |
| SECURE\_OBJECTS\_ONLY | BOOLEAN | Indicates whether the share can only have secure objects granted to it. |
| TARGET\_ACCOUNTS | VARCHAR | A comma-separated list of target accounts the share is shared with (outbound). This field is empty if the share has no target accounts. |
| LISTING\_GLOBAL\_NAME | VARCHAR | Global unique name of the listing associated with the share, if any. |

Expand

Show lessSee more
