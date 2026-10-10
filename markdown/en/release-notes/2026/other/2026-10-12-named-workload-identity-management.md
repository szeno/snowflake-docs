# Oct 12, 2026: Named workload identity management for users

You can now use SQL to register, modify, and remove named [workload identities](/user-guide/workload-identity-federation) for a service user.
Each workload identity has its own name and provider settings. A user can have up to 10 workload identities by default.

Named workload identities improve on the approach of setting the `WORKLOAD_IDENTITY` user property, which assigns a single
workload identity named `DEFAULT`. Snowflake continues to support that property.

For more information, see the following topics:

- [Workload identity federation](/user-guide/workload-identity-federation)
- [ALTER USER … ADD WORKLOAD IDENTITY](/sql-reference/sql/alter-user-add-workload-identity)
- [ALTER USER … MODIFY WORKLOAD IDENTITY](/sql-reference/sql/alter-user-modify-workload-identity)
- [ALTER USER … REMOVE WORKLOAD IDENTITY](/sql-reference/sql/alter-user-remove-workload-identity)
- [SHOW USER WORKLOAD IDENTITY AUTHENTICATION METHODS](/sql-reference/sql/show-user-workload-identity-authentication-methods)
