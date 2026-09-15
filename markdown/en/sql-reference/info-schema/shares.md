# SHARES view

This Information Schema view displays all outbound and inbound shares for which the current role has been granted access privileges. This view provides real time information with no latency of data.

## Columns

| Column | Data type | Description |
| --- | --- | --- |
| CREATED\_ON | TIMESTAMP\_LTZ | The timestamp when the share was created. |
| KIND | VARCHAR | The kind of the share, outbound or inbound. |
| OWNER\_ACCOUNT | VARCHAR | The owner account of the share. |
| NAME | VARCHAR | The name of the share. |
| DATABASE\_NAME | VARCHAR | The name of the primary database associated with the share. This field is empty if no database has been granted to the share. |
| TO | VARCHAR | A comma-separated list of target accounts the share is shared with (outbound). This field is empty if the share has no target accounts. |
| OWNER | VARCHAR | The name of the role that owns the share. |
| COMMENT | VARCHAR | Comment associated with the share, if any. |
| LISTING\_GLOBAL\_NAME | VARCHAR | Global unique name of the listing associated with the share, if any. |
| SECURE\_OBJECTS\_ONLY | VARCHAR | Indicates whether the share can only have secure objects granted to it. |

Expand

Show lessSee more

## Usage notes

The view doesn’t capture deleted shares.

## Examples

Retrieve all shares in the current account:

Copy code

```
SELECT * FROM <any_database>.INFORMATION_SCHEMA.SHARES;
```
