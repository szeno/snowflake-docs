# UNDROP ACCOUNT

Restores a [dropped account](/user-guide/organizations-manage-accounts-delete) that has not yet been permanently deleted
(a dropped account that is within its grace period).

To obtain a list of dropped accounts that can be restored, refer to [Viewing dropped accounts](/user-guide/organizations-manage-accounts-delete#label-viewing-dropped-deleted-accounts).

See also:
:   [CREATE ACCOUNT](/sql-reference/sql/create-account), [DROP ACCOUNT](/sql-reference/sql/drop-account), [SHOW ACCOUNTS](/sql-reference/sql/show-accounts)

## Syntax

Copy code

```
UNDROP ACCOUNT <name>
```

## Parameters

`name`
:   Specifies the name of the account being restored. As an example, if the full account identifier is `myorg-account123`, then
    specify `account123` as the name.

    The legacy account locator cannot be used to identify the account.

## Usage notes

- Only [organization administrators](/user-guide/organization-administrators) can execute the command.

- UNDROP relies on the Snowflake [Time Travel](/user-guide/data-time-travel) feature. An object can be restored only if
  the object was deleted within the [Data retention period](/user-guide/data-time-travel#label-time-travel-data-retention-period). The default value is 24 hours.

## Example

To restore the dropped account `myaccount123`, which was still within the grace period, enter:

Copy code

```
UNDROP ACCOUNT myaccount123;
```
