# DROP ACCOUNT

Drops an account, which initiates the process of [deleting the account](/user-guide/organizations-manage-accounts-delete).

See also:
:   [CREATE ACCOUNT](/sql-reference/sql/create-account), [SHOW ACCOUNTS](/sql-reference/sql/show-accounts), [UNDROP ACCOUNT](/sql-reference/sql/undrop-account)

## Syntax

Copy code

```
DROP ACCOUNT [ IF EXISTS ] <name> GRACE_PERIOD_IN_DAYS = <integer>
```

## Parameters

`name`
:   Specifies the name of the account being dropped. As an example, if the full account identifier is `myorg-account123`, then specify
    `account123` as the name. If you do not know the account name, execute the [SHOW ACCOUNTS](/sql-reference/sql/show-accounts)
    command, and find the name in the `account_name` column.

    The legacy account locator cannot be used to identify the account.

`GRACE_PERIOD_IN_DAYS = integer`
:   Specifies the number of days during which the account can be restored (“undropped”). The minimum is 3 days and the maximum is 90 days.

## Usage notes

- Only [organization administrators](/user-guide/organization-administrators) can execute the command.
- The organization administrator cannot drop the account they are currently logged in to.

- When the IF EXISTS clause is specified and the target object doesn’t exist, the command completes successfully
  without returning an error.

Important

If the account contains a snapshot set that has an associated snapshot policy with a retention lock, and there are any
unexpired snapshots in the snapshot set, then you can’t delete the account containing the snapshot set.
In that case, you must wait for all the snapshots in the set to expire.
This restriction applies even to privileged roles such as ACCOUNTADMIN, and to Snowflake support.
For that reason, be careful when specifying retention lock and a long expiration
period in a snapshot policy.

## Example

To drop an account `my_account` and allow a 14-day grace period for restoring the account, enter:

> Copy code
>
> ```
> DROP ACCOUNT my_account GRACE_PERIOD_IN_DAYS = 14;
> ```
