# Organization user and organization user group functions

The following functions help you work with [organization users and organization user groups](/user-guide/organization-users).

| Function | Description |
| --- | --- |
| [CURRENT\_ORGANIZATION\_USER](/sql-reference/functions/current_organization_user) | Indicates whether the current user in the session was imported from an organization user. |
| [IS\_ORGANIZATION\_USER](/sql-reference/functions/is_organization_user),   [IS\_USER\_IMPORTED (SYS\_CONTEXT function)](/sql-reference/functions/is_user_imported) | Tests whether a specific user was imported from an organization user. |
| [IS\_ORGANIZATION\_USER\_GROUP](/sql-reference/functions/is_organization_user_group),   [IS\_GROUP\_IMPORTED (SYS\_CONTEXT function)](/sql-reference/functions/is_group_imported) | Tests whether a specific role was imported from an organization user group. |
| [IS\_ORGANIZATION\_USER\_GROUP\_IN\_SESSION](/sql-reference/functions/is_organization_user_group_in_session),   [IS\_GROUP\_ACTIVATED (SYS\_CONTEXT function)](/sql-reference/functions/is_group_activated) | Tests whether a specific imported role is in the role hierarchy of the user’s current session. |
| [SYS\_CONTEXT (SNOWFLAKE$ORGANIZATION namespace)](/sql-reference/functions/sys_context_snowflake_organization) | Returns information about organization users and organization user groups. |
| [SYS\_CONTEXT (SNOWFLAKE$ORGANIZATION\_SESSION namespace)](/sql-reference/functions/sys_context_snowflake_organization_session) | Returns information about the current session and the current organization user in the session. |
| [SYSTEM$LINK\_ORGANIZATION\_USER](/sql-reference/functions/system_link_organization_user) | Links an organization user with an existing user object so it can be managed as an organization user going forward. |
| [SYSTEM$LINK\_ORGANIZATION\_USER\_GROUP](/sql-reference/functions/system_link_organization_user_group) | Links an organization user group with an existing access control role so it can be managed as an organization user group going forward. |
| [SYSTEM$UNLINK\_ORGANIZATION\_USER](/sql-reference/functions/system_unlink_organization_user) | Unlinks a user object from an organization user so it can be managed as a local user going forward. |
| [SYSTEM$UNLINK\_ORGANIZATION\_USER\_GROUP](/sql-reference/functions/system_unlink_organization_user_group) | Unlinks an access control role from an organization user group so it can be managed as a local role going forward. |

Expand

Show lessSee more
