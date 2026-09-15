# DROP MANAGED ACCOUNT

Provider sharing not enabled for all accounts

Provider sharing is enabled by default for most, but not all accounts.

If you encounter errors when attempting to share data with consumers, the feature may not be enabled for your account. To inquire
about enabling it, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Removes a managed account, including all objects created in the account, and immediately restricts access to the account. Currently
used by data providers to create reader accounts for their consumers. For more details, see [Manage reader accounts](/user-guide/data-sharing-reader-create).

See also:
:   [CREATE MANAGED ACCOUNT](/sql-reference/sql/create-managed-account) , [SHOW MANAGED ACCOUNTS](/sql-reference/sql/show-managed-accounts)

## Syntax

Copy code

```
DROP MANAGED ACCOUNT <name>
```

## Usage notes

- This command can be executed by users with the ACCOUNTADMIN role (or a role that has been granted the CREATE ACCOUNT global privilege).
- This operation can not be undone.

## Examples

Copy code

```
DROP MANAGED ACCOUNT reader_acct1;

  +------------------------------------+
  | status                             |
  |------------------------------------|
  | READER_ACCT1 successfully dropped. |
  +------------------------------------+
```
