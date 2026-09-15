Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# NETWORK\_RULES view

This Account Usage view returns one row for each network rule in your account.

## Columns

| Column | Data Type | Description |
| --- | --- | --- |
| `id` | NUMBER | Internal system-generated identifier for network rule. |
| `name` | VARCHAR | Network rule name |
| `schema_id` | NUMBER | Internal system-generated identifier for the schema that contains the network rule. |
| `schema_name` | VARCHAR | Name of the schema that contains the network rule. |
| `database_id` | NUMBER | Internal system-generated identifier for the database that contains the network rule. |
| `database_name` | VARCHAR | Name of the database that contains the network rule. |
| `owner` | VARCHAR | Name of role that owns the network rule. |
| `owner_role_type` | VARCHAR | The type of role that owns the object, for example `ROLE`.   If a Snowflake Native App owns the object, the value is `APPLICATION`.   Snowflake returns NULL if you delete the object because a deleted object does not have an owner role. |
| `comment` | VARCHAR | Comment for the network rule (if any). |
| `created` | TIMESTAMP\_LTZ | Date and time that the network rule was created. |
| `last_altered` | TIMESTAMP\_LTZ | Date and time that the network rule was last altered. |
| `deleted` | TIMESTAMP\_LTZ | Date and time the network rule was dropped. |
| `mode` | VARCHAR | Mode of the network rule. For supported values, see [CREATE NETWORK RULE](/sql-reference/sql/create-network-rule). |
| `type` | VARCHAR | Type of network rule. For supported values, see [CREATE NETWORK RULE](/sql-reference/sql/create-network-rule). |
| `value_list` | VARCHAR | List of values for the network rule. For supported values, see [CREATE NETWORK RULE](/sql-reference/sql/create-network-rule). |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 120 minutes (2 hours).

- The view only displays objects for which the current role for the session has been granted access privileges.

## Example

To see your current Snowflake-managed rules, *including* IP addresses, query the [NETWORK\_RULES view](/sql-reference/account-usage/network_rules) and filter on rows where the database is SNOWFLAKE and the schema is NETWORK\_SECURITY:

Copy code

```
SELECT *
  FROM SNOWFLAKE.ACCOUNT_USAGE.NETWORK_RULES
  WHERE DATABASE = 'SNOWFLAKE' AND SCHEMA = 'NETWORK_SECURITY';
```
