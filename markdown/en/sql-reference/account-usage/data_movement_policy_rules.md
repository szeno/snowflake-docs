Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# DATA\_MOVEMENT\_POLICY\_RULES view

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This Account Usage view displays a row for each data movement rule defined in your account.

## Columns

| Column name | Data type | Description |
| --- | --- | --- |
| `ID` | NUMBER | Internal/system-generated identifier for the data movement rule. |
| `NAME` | VARCHAR | Name of the data movement rule. |
| `SCHEMA_ID` | NUMBER | Internal/system-generated identifier for the schema of the rule. |
| `SCHEMA` | VARCHAR | Schema of the data movement rule. |
| `DATABASE_ID` | NUMBER | Internal/system-generated identifier for the database of the rule. |
| `DATABASE` | VARCHAR | Database of the data movement rule. |
| `OWNER` | VARCHAR | Name of the role that owns the data movement rule. |
| `OWNER_ROLE_TYPE` | VARCHAR | Type of the role that owns the object, for example `ROLE` or `DATABASE_ROLE`. |
| `COMMENT` | VARCHAR | Comment for the data movement rule. |
| `MOVEMENT_TYPE` | VARCHAR | Type of movement the rule applies to: `COPY_INTO_EXTERNAL_STAGE`, `COPY_INTO_INTERNAL_STAGE`, `AGENT_ACCESS`, `SNOWSIGHT_UI`, `UI_DOWNLOAD`, `PROGRAMMATIC_FETCH`, or `UNKNOWN`. |
| `FUNCTION_SIGNATURE` | VARCHAR | Parameter signature for the rule function. |
| `FUNCTION_BODY` | VARCHAR | SQL expression body of the rule. |
| `FUNCTION_RETURN_TYPE` | VARCHAR | Return data type of the rule function. |
| `CREATED` | TIMESTAMP\_LTZ | Date and time when the data movement rule was created. |
| `LAST_ALTERED` | TIMESTAMP\_LTZ | Date and time when the data movement rule was last altered. |
| `DELETED` | TIMESTAMP\_LTZ | Date and time when the data movement rule was dropped. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 2 hours.
- The view only displays objects for which the current role for the session has been granted access privileges.

These views are also available in the ORGANIZATION\_USAGE schema. Organization usage must be enabled for the account.
