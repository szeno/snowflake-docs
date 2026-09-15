# TABLE\_PRIVILEGES view

This Information Schema view displays a row for each table privilege that has been granted to each role in the specified (or current) database.

For more information about roles and privileges, see [Overview of Access Control](/user-guide/security-access-control-overview).

See also:
:   [APPLICABLE\_ROLES view](/sql-reference/info-schema/applicable_roles) , [ENABLED\_ROLES view](/sql-reference/info-schema/enabled_roles) , [OBJECT\_PRIVILEGES view](/sql-reference/info-schema/object_privileges)

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| GRANTOR | VARCHAR | Role who granted the table privilege |
| GRANTEE | VARCHAR | Role to whom the table privilege is granted |
| GRANTED\_TO | VARCHAR | Type of object that has been granted the privilege |
| TABLE\_CATALOG | VARCHAR | Database containing the table on which the privilege is granted |
| TABLE\_SCHEMA | VARCHAR | Schema containing the table on which the privilege is granted |
| TABLE\_NAME | VARCHAR | Name of the table on which the privilege is granted |
| PRIVILEGE\_TYPE | VARCHAR | Type of the granted privilege |
| IS\_GRANTABLE | VARCHAR | Whether the privilege was granted WITH GRANT OPTION |
| WITH\_HIERARCHY | VARCHAR | Not applicable for Snowflake. |
| CREATED | TIMESTAMP\_LTZ | Creation time of the privilege |

Expand

Show lessSee more

## Usage notes

- The view only displays objects for which the current role for the session has been granted access privileges.
- The PRIVILEGE\_TYPE column contains Snowflake privilege types. For example, the owner of a table has the OWNERSHIP privilege, rather than each of the separate privileges (e.g. SELECT, INSERT, DELETE,
  UPDATE).
