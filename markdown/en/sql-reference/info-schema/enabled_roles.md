# ENABLED\_ROLES view

This Information Schema view displays a row for each currently-enabled role in the session. A role is enabled if it is currently in use in the session or it has been granted to the role that is currently
in use.

For more information about roles, see [Overview of Access Control](/user-guide/security-access-control-overview).

See also:
:   [APPLICABLE\_ROLES view](/sql-reference/info-schema/applicable_roles) , [OBJECT\_PRIVILEGES view](/sql-reference/info-schema/object_privileges) , [TABLE\_PRIVILEGES view](/sql-reference/info-schema/table_privileges)

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| ROLE\_NAME | VARCHAR | Name of the role |
| ROLE\_OWNER | VARCHAR | Owner of the role |

Expand

Show lessSee more

## Usage notes

- The view only displays objects for which the current role for the session has been granted access privileges.
- The view always displays the PUBLIC role because it is always enabled.
- The view does not display any information about [database roles](/user-guide/security-access-control-considerations#label-access-control-considerations-database-roles).
