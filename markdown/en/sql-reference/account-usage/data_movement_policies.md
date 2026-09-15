Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# DATA\_MOVEMENT\_POLICIES view

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This Account Usage view displays a row for each data movement policy defined in your account.

## Columns

| Column name | Data type | Description |
| --- | --- | --- |
| `ID` | NUMBER | Internal/system-generated identifier for the data movement policy. |
| `NAME` | VARCHAR | Name of the data movement policy. |
| `SCHEMA_ID` | NUMBER | Internal/system-generated identifier for the schema of the policy. |
| `SCHEMA` | VARCHAR | Schema of the data movement policy. |
| `DATABASE_ID` | NUMBER | Internal/system-generated identifier for the database of the policy. |
| `DATABASE` | VARCHAR | Database of the data movement policy. |
| `OWNER` | VARCHAR | Name of the role that owns the data movement policy. |
| `COMMENT` | VARCHAR | Comment for the data movement policy. |
| `CREATED` | TIMESTAMP\_LTZ | Date and time when the data movement policy was created. |
| `LAST_ALTERED` | TIMESTAMP\_LTZ | Date and time when the data movement policy was last altered. |
| `DELETED` | TIMESTAMP\_LTZ | Date and time when the data movement policy was dropped. |
| `OWNER_ROLE_TYPE` | VARCHAR | Type of the role that owns the object, for example `ROLE` or `DATABASE_ROLE`. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 120 minutes (2 hours).
- The view only displays objects for which the current role for the session has been granted access privileges.

These views are also available in the ORGANIZATION\_USAGE schema. Organization usage must be enabled for the account.
