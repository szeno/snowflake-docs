# OBJECT\_PRIVILEGES view

This Information Schema view displays a row for each access privilege granted for all objects defined in your account. It includes the privileges displayed in the [TABLE\_PRIVILEGES view](/sql-reference/info-schema/table_privileges) and
[USAGE\_PRIVILEGES view](/sql-reference/info-schema/usage_privileges).

For more information about privileges and their impact on object access, see [Overview of Access Control](/user-guide/security-access-control-overview).

See also:
:   [APPLICABLE\_ROLES view](/sql-reference/info-schema/applicable_roles) , [ENABLED\_ROLES view](/sql-reference/info-schema/enabled_roles) , [TABLE\_PRIVILEGES view](/sql-reference/info-schema/table_privileges)

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| GRANTOR | VARCHAR | Role who granted the privilege |
| GRANTEE | VARCHAR | Role to whom the privilege is granted |
| GRANTED\_TO | VARCHAR | Type of object that has been granted the privilege |
| OBJECT\_CATALOG | VARCHAR | Database containing the object on which the privilege is granted |
| OBJECT\_SCHEMA | VARCHAR | Schema containing the object on which the privilege is granted |
| OBJECT\_NAME | VARCHAR | Name of the object on which the privilege is granted |
| OBJECT\_TYPE | VARCHAR | Type of the object on which the privilege is granted |
| PRIVILEGE\_TYPE | VARCHAR | Type of the granted privilege |
| IS\_GRANTABLE | VARCHAR | Whether the privilege was granted WITH GRANT OPTION |
| CREATED | TIMESTAMP\_LTZ | Creation time of the privilege |

Expand

Show lessSee more

## Usage notes

- The view only displays objects for which the current role for the session has been granted access privileges.
