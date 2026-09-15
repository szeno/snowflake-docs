# APPLICABLE\_ROLES view

This Information Schema view displays one row for each role grant applied to the currently authenticated user.

For more information about roles and grants, see [Overview of Access Control](/user-guide/security-access-control-overview).

See also:
:   [ENABLED\_ROLES view](/sql-reference/info-schema/enabled_roles) , [OBJECT\_PRIVILEGES view](/sql-reference/info-schema/object_privileges) , [TABLE\_PRIVILEGES view](/sql-reference/info-schema/table_privileges) , [GRANTS\_TO\_USERS view](/sql-reference/account-usage/grants_to_users) ,
    [GRANTS\_TO\_ROLES view](/sql-reference/account-usage/grants_to_roles) , [SHOW GRANTS](/sql-reference/sql/show-grants)

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| GRANTEE | VARCHAR | Role or user to whom the privilege is granted |
| ROLE\_NAME | VARCHAR | Name of the role |
| ROLE\_OWNER | VARCHAR | Owner of the role |
| IS\_GRANTABLE | VARCHAR | Whether this role can be granted to others |

Expand

Show lessSee more

## Usage notes

The view does not display any information about [database roles](/user-guide/security-access-control-considerations#label-access-control-considerations-database-roles).
