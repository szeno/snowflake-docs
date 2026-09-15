# DROP SHARE

Provider sharing not enabled for all accounts

Provider sharing is enabled by default for most, but not all accounts.

If you encounter errors when attempting to share data with consumers, the feature may not be enabled for your account. To inquire
about enabling it, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Removes the specified [share](/user-guide/data-sharing-intro) from the system and immediately revokes access for all consumers
(i.e. accounts who have created a database from the share).

See also:
:   [CREATE SHARE](/sql-reference/sql/create-share) , [ALTER SHARE](/sql-reference/sql/alter-share) , [SHOW SHARES](/sql-reference/sql/show-shares) , [DESCRIBE SHARE](/sql-reference/sql/desc-share)

## Syntax

Copy code

```
DROP SHARE <name>
```

## Parameters

`name`
:   Specifies the identifier for the share to drop. If the identifier contains spaces, special characters, or mixed-case characters, the
    entire string must be enclosed in double quotes. Identifiers enclosed in double quotes are also case-sensitive.

## Usage notes

- Only the share owner, the role with the OWNERSHIP privilege on the share, has the privileges to drop a share.
  Executing this command with any other role returns an error.
- Dropped shares cannot be recovered; they must be recreated.
- Dropping a share does not affect the database in the share (or any of the objects in the database).

Important

Before dropping a share, consider the downstream impact of performing this operation:

- Consumer accounts that have created databases from the share will no longer be able to query these databases.
- Recreating a share with the same name as a previous share does not restore the databases created (by any consumers) from the share.
  Each consumer must create a new database from the new share.
- A dropped share can not be restored. The share must be created again using the [CREATE SHARE](/sql-reference/sql/create-share) command and then
  configured using [GRANT <privilege> … TO SHARE](/sql-reference/sql/grant-privilege-share) and [ALTER SHARE](/sql-reference/sql/alter-share).

## Examples

> Copy code
>
> ```
> DROP SHARE sales_s;
>
> +-------------------------------+
> | status                        |
> |-------------------------------|
> | SALES_S successfully dropped. |
> +-------------------------------+
> ```
