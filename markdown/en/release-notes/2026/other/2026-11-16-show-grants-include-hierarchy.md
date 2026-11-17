# Nov 16, 2026: SHOW GRANTS TO … INCLUDE HIERARCHY (*General availability*)

With this release, you can add `INCLUDE HIERARCHY` to `SHOW GRANTS TO` statements to list the grants held by every role in a
grantee’s [role hierarchy](/user-guide/security-access-control-overview#label-role-hierarchy-and-privilege-inheritance), not only
the grants made directly to that role or user.

When you specify `INCLUDE HIERARCHY`, Snowflake expands the roles granted to the specified role or user, including account roles,
database roles, and application roles granted recursively, and the account-level PUBLIC role. Grants held by instance roles,
service roles, or class roles are omitted. Each output row keeps the `grantee_name` of the role that holds the grant, so you
can see which role in the hierarchy provides a privilege.

You can use `INCLUDE HIERARCHY` with the following statements:

- `SHOW GRANTS TO ROLE`
- `SHOW GRANTS TO DATABASE ROLE`
- `SHOW GRANTS TO USER`
- `SHOW FUTURE GRANTS TO ROLE`
- `SHOW FUTURE GRANTS TO DATABASE ROLE`
- `SHOW CALLER GRANTS TO ROLE`
- `SHOW CALLER GRANTS TO DATABASE ROLE`

For more information, see [SHOW GRANTS](/sql-reference/sql/show-grants) and [SHOW CALLER GRANTS](/sql-reference/sql/show-caller-grants).
