Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$GLOBAL\_ACCOUNT\_SET\_PARAMETER

Enables replication and failover features for a specified account in an [organization](/user-guide/organizations).

After an [organization administrator](/user-guide/organization-administrators) has called this function, the following features are enabled for the
account:

- [Replication](/user-guide/account-replication-intro)
- [Client Redirect](/user-guide/client-redirect)

Call the SQL function once for each account in your organization for which you are enabling replication and failover features. This
includes each account that you intend to contain a primary or secondary
[replication or failover group](/user-guide/account-replication-intro#label-replication-and-failover-groups), database, or
[connection](/user-guide/client-redirect#label-intro-to-client-redirect).

## Syntax

Copy code

```
SELECT SYSTEM$GLOBAL_ACCOUNT_SET_PARAMETER('<account_identifier>',
  'ENABLE_ACCOUNT_DATABASE_REPLICATION', 'true');
```

## Arguments

`<account_identifier>`
:   Identifier of an account for which you are enabling replication. The preferred format for the identifier is
    `organization_name.account_name`. Though the legacy `account_locator` format is also supported, its use is discouraged as it
    can cause unexpected results when an organization has multiple accounts with the same locator (in different regions).

    Retrieve the set of accounts in your organization using the [SHOW ACCOUNTS](/sql-reference/sql/show-accounts) command, which returns
    details about each account, including the organization name, account name, and account locator.

## Usage notes

- Only [organization administrators](/user-guide/organization-administrators) can call this SQL function.
- Multiple accounts can be enabled for replication from the same organization administrator account.
- When replication is enabled for an account using this SQL function,
  the [SHOW REPLICATION ACCOUNTS](/sql-reference/sql/show-replication-accounts) output includes the account.
- If you have more than one account with the same account locator in different regions, to enable replication, you must use
  `organization_name.account_name` as the account identifier.

## Examples

The following example enables replication for the `account1` and `account2` accounts in the `myorg` organization:

Copy code

```
SELECT SYSTEM$GLOBAL_ACCOUNT_SET_PARAMETER('myorg.account1',
  'ENABLE_ACCOUNT_DATABASE_REPLICATION', 'true');

SELECT SYSTEM$GLOBAL_ACCOUNT_SET_PARAMETER('myorg.account2',
  'ENABLE_ACCOUNT_DATABASE_REPLICATION', 'true');
```
