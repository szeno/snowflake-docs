Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# MULTI\_PARTY\_APPROVAL\_POLICIES view

[Business Critical Feature](/user-guide/intro-editions)

This feature requires Business Critical (or higher).

To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This Account Usage view provides the [Multi-party Approval](/user-guide/multi-party-approval)
policies in your account.

Each row in this view corresponds to a different Multi-party Approval policy.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| ID | NUMBER | Internal/system-generated identifier for the Multi-party Approval policy. |
| NAME | VARCHAR | Name of the Multi-party Approval policy. |
| SCHEMA\_ID | NUMBER | Internal/system-generated identifier for the schema in which the policy resides. |
| SCHEMA | VARCHAR | Schema to which the Multi-party Approval policy belongs. |
| DATABASE\_ID | NUMBER | Internal/system-generated identifier for the database in which the policy resides. |
| DATABASE | VARCHAR | Database to which the Multi-party Approval policy belongs. |
| OWNER | VARCHAR | Name of the role that owns the Multi-party Approval policy. |
| OWNER\_ROLE\_TYPE | VARCHAR | The type of role that owns the object, for example `ROLE`.   If a Snowflake Native App owns the object, the value is `APPLICATION`.   Snowflake returns NULL if you delete the object because a deleted object does not have an owner role. |
| POLICY\_DEFINITION | VARCHAR | The full YAML body of the policy, including its rules, operations, and approvers. |
| CREATED | TIMESTAMP\_LTZ | Date and time when the Multi-party Approval policy was created. |
| LAST\_ALTERED | TIMESTAMP\_LTZ | Date and time when the Multi-party Approval policy was last altered. |
| DELETED | TIMESTAMP\_LTZ | Date and time when the Multi-party Approval policy was dropped. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 120 minutes (2 hours).
