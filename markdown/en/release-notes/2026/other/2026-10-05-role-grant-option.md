# Oct 5, 2026: WITH GRANT OPTION for role grants

You can now grant an account role or a database role to another role with `WITH GRANT OPTION`. The
recipient role can grant that role to other roles, including with `WITH GRANT OPTION`.

Use `REVOKE GRANT OPTION FOR` to remove only the grant option. The role grant stays in place, so the
recipient still inherits the granted role’s privileges. Use `CASCADE` or `RESTRICT` to control grants
that were made from that role grant. `RESTRICT` is the default: the revoke fails when dependent grants
exist.

`WITH GRANT OPTION` applies to grants from one role to another role. A grant to a user doesn’t support
the clause.

For more information, see [GRANT ROLE](/sql-reference/sql/grant-role) and
[GRANT DATABASE ROLE](/sql-reference/sql/grant-database-role).
