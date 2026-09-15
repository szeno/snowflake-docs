# Dropping an account

The organization administrator can drop an account to delete it from the system. A dropped account
is not deleted immediately, but rather enters a grace period during which the administrator can restore (“undrop”) the account. When the
grace period expires, Snowflake purges the dropped account from the system.

Tip

Because Snowflake does not permanently delete an account when it is initially dropped, you cannot immediately create a new account
with the same name as the one you just dropped. As a workaround,
[rename the account](/user-guide/organizations-manage-accounts-rename) before dropping it.

If the organization administrator is using the ORGADMIN role to drop an account, they cannot drop the account while they are logged in to it;
they must log in to a different ORGADMIN-enabled account before executing the DROP ACCOUNT command. This means that the organization
administrator cannot drop the last account in the organization. If your organization consists of a single account that needs to be deleted,
contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

## About the grace period

When dropping the account, the organization administrator defines a grace period during which the account can be restored. Once an account
is dropped, it is locked to prevent activity during the grace period. An organization continues to pay for the cost of account storage
during the grace period.

The minimum grace period is 3 days and the maximum grace period is 90 days, not including the current date. For example, if the
organization administrator defines the grace period as 3 days when they drop the account on Monday at 11 a.m., then the grace period
expires on Thursday at 11 a.m.

If you want to change the grace period of a dropped account, [restore the account](#label-restoring-account), then drop it
again with the new grace period.

The grace period is not the same as the data retention period of [Time Travel](/user-guide/data-time-travel).

## Dropping an account that provides listings, reader accounts, and shares

You cannot drop an account that has active listings shared to specific consumers or listings published on the Snowflake Marketplace.
Before you can drop the account, you must do the following:

1. Delete any listings provided by the account. Listings subject to a retirement policy must complete the retirement
   flow before the account can be dropped.
   See [Remove listings as a provider](/collaboration/provider-listings-removing).
2. Drop the shares associated with the listings.

If the account provides shares or reader accounts to consumers, the organization administrator of the provider account should
contact those consumers to let them know that they will lose access to the shares and reader accounts provided by the to-be-dropped account.

As soon as the account is dropped, the following happens to the shared data and data products:

- Shares stop working. Consumers lose access to data shared by the account.
- Reader accounts are dropped and then deleted at the same time as the provider account.

## Dropping an account

[As the organization administrator](/user-guide/organization-administrators), you can drop an account using [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) or
SQL.

Snowsight:
:   1. In the navigation menu, select **Admin** » **Accounts**.
    2. Find the active account, and select **…** » **Drop Account**.
    3. Enter a [grace period](#label-delete-account-grace-period) during which the account can be restored.
    4. Select **Drop Account**.

SQL:
:   Execute the [DROP ACCOUNT](/sql-reference/sql/drop-account)
    command.

    For example, to drop an account `my_account` and allow a 14-day grace period for recovering the account, enter:

    Copy code

    ```
    DROP ACCOUNT my_account GRACE_PERIOD_IN_DAYS = 14;
    ```

Note

If you want to drop a reader account, execute the [DROP MANAGED ACCOUNT](/sql-reference/sql/drop-managed-account) command.

## Viewing dropped accounts

Organization administrators have multiple options for viewing dropped accounts that are still within their grace period. Some of these
options also show dropped accounts that have been permanently deleted from the system.

Snowsight:
:   [As the organization administrator](/user-guide/organization-administrators), you can use Snowsight to view all dropped
    accounts, including those that have been permanently deleted.

    1. In the navigation menu, select **Admin** » **Accounts**.
    2. Select the **Dropped Accounts** tab.

    Dropped accounts that are still within the grace period appear with a yellow indicator and have a **Drop Date** that is in the future.

    Permanently deleted accounts have a **Drop Date** that is on or before the current date.

SQL:
:   Executing the [SHOW ACCOUNTS](/sql-reference/sql/show-accounts) command with the optional HISTORY keyword shows dropped accounts
    that are still within their grace period. Permanently deleted accounts are not included in the output.

    When the [organization administrator](/user-guide/organization-administrators) executes the following command:

    Copy code

    ```
    SHOW ACCOUNTS HISTORY;
    ```

    The output includes dropped accounts and the additional `dropped_on`, `scheduled_deletion_time`, and `restored_on`
    columns.

ACCOUNTS View:
:   Users with access to the [ORGANIZATION\_USAGE schema](/sql-reference/organization-usage) can query the
    [ACCOUNTS view](/sql-reference/organization-usage/accounts) to see all dropped accounts, including those that have been
    permanently deleted.

## Restoring an account

An organization administrator can restore, or undrop, a dropped account within the grace period, which prevents it from being purged.
Undropping an account unlocks it, allowing users to access the account as if it had never been dropped.

[As the organization administrator](/user-guide/organization-administrators), you can undrop an account using Snowsight or
SQL.

Snowsight:
:   1. In the navigation menu, select **Admin** » **Accounts**.
    2. Select the **Dropped Accounts** tab.
    3. Find the account, and select **…** » **Undrop Account**.
    4. Select **Undrop Account**.

SQL:
:   Execute the [UNDROP ACCOUNT](/sql-reference/sql/undrop-account) command to restore an account. For example, the following command
    restores the dropped account `myaccount123`, which was still within the grace period:

    Copy code

    ```
    UNDROP ACCOUNT myaccount123;
    ```
