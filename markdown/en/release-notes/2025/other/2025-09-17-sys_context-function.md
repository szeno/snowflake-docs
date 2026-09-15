# Sep 17, 2025: New SYS\_CONTEXT function for getting context about applications, sessions, and organizations

You can call the new [SYS\_CONTEXT](/sql-reference/functions/sys_context) function to get context information about:

- [The current application](/sql-reference/functions/sys_context_snowflake_application)
- [The current environment](/sql-reference/functions/sys_context_snowflake_environment) (for example, the current account or
  region)
- [The current session](/sql-reference/functions/sys_context_snowflake_session)

For example, you can:

- Determine if an application role is activated.
- Identify the client, driver, or library that is calling the function.
- Determine if the function is being called by a person, task, or SPCS service.

You can also get context information about
[organizations](/sql-reference/functions/sys_context_snowflake_organization), including information about the
[organization information related to the session](/sql-reference/functions/sys_context_snowflake_organization_session). For
example, you can:

- Determine if an organization user or group has been imported.
- Determine if the role representing an organization user group is activated.
- Identify the name of the organization user who started the session.

Note

Getting context information about organizations is in [Preview](/release-notes/preview-features).

For more information, see [SYS\_CONTEXT](/sql-reference/functions/sys_context).
