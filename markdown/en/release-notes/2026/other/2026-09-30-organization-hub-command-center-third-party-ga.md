# Sep 30, 2026: Organization Command Center 3rd party access configuration (*General availability*)

3rd party access configuration in Organization Command Center is now generally available and is no longer in
[Preview](/release-notes/preview-features).

From the organization account, a user with the GLOBALORGADMIN role can open **Organization Hub** » **Command
center**, then the **3rd party access configuration** tile, to classify member accounts as internal or external, set
the default tenant type for new accounts, and maintain allowed email domains. Logins from domains that aren’t on the
allowlist can raise Trust Center security violations.

You can also configure the same tenant types and domain allowlists with SQL from the organization account (or an
ORGADMIN role-enabled account), including `CREATE ACCOUNT` with `TENANT_TYPE`, `ALTER ACCOUNT` for tenant type and
domain names, and `ALTER ORGANIZATION` for the default tenant type and organization-level domain allowlists.

This Command Center page requires an [organization account](/user-guide/organization-accounts). Access is limited to the
GLOBALORGADMIN role.

For more information, see the following topics:

- [Organization Command Center](/user-guide/organization-hub-command-center)
- [Command Center 3rd party access configuration](/user-guide/organization-hub-command-center-third-party)
- [Third party (publisher–subscriber) accounts](/user-guide/third-party-publisher-subscriber-accounts)
- [CREATE ACCOUNT](/sql-reference/sql/create-account)
- [ALTER ACCOUNT](/sql-reference/sql/alter-account)
