# May 6, 2026: Change an account Snowflake edition with ALTER ACCOUNT (*General availability*)

Organization administrators can now change the [Snowflake edition](/user-guide/intro-editions) of an account in the organization by using
`ALTER ACCOUNT <name> SET EDITION = { 'STANDARD' | 'ENTERPRISE' | 'BUSINESS_CRITICAL' }`. Run the command from an account other than the account
whose edition you’re changing.

For upgrade and downgrade requirements, regional availability, and examples, see [Working with account editions](/user-guide/organizations-manage-accounts-editions). For
full command syntax and parameters, see [ALTER ACCOUNT](/sql-reference/sql/alter-account).
