# Managing account URLs

[Preview Feature](/release-notes/preview-features) — Open

> Available to all accounts.

When an account is renamed or has its organization modified, it is assigned a new [account URL](/user-guide/organizations-connect#label-connecting-via-url) that is
used to connect to the account. Whether users can continue to use the original URL to access the account depends on how the account changed
and choices made when it changed:

Renamed account:
:   When the organization administrator renames an account, the original account URL is saved by default so users can continue to access the
    account with it. If saved, there is no limit on how long users can continue to use the original URL.

    During account renaming, the administrator can change the default to delete the original URL and prevent users from accessing the
    account with it.

    If the original URL was saved, but now you want to delete it, see [Deleting the account URL for a renamed account](#label-drop-account-access-url).

Modified organization:
:   When Snowflake Support modifies the organization of an account, they can save or delete the original account URL. If saved, the
    original URL is referred to as the “old organization URL”. This URL can be used to access the account for 90 days, at which time it is
    deleted.

    If the original URL was saved but you want to delete it before the 90 days expires, see [Deleting an organization URL](#label-drop-org-access-url).

## Deleting the account URL for a renamed account

[As the organization administrator](/user-guide/organization-administrators), you can use [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) or SQL to delete an
old account URL that was saved when the account was renamed:

Snowsight:
:   1. In the navigation menu, select **Admin** » **Accounts**.
    2. Find the active account, and select **…** » **Manage Urls**.
    3. In the **Previous Account URL** section, select **Delete URL**.
    4. Select **Delete**.

SQL:
:   Execute the [ALTER ACCOUNT … DROP OLD URL](/sql-reference/sql/alter-account) command. For example, to drop the original
    account URL for an account that was renamed, execute:

    Copy code

    ```
    ALTER ACCOUNT my_account1 DROP OLD URL;
    ```

## Deleting an organization URL

An “old organization URL” refers to the original account URL of an account whose organization has changed in one of the following ways:

- Organization was renamed.
- Organization was merged with another organization.
- Account was moved from one organization to another.

If the original account URL is saved during one of these events, users can continue to use the original URL for 90 days, at which time
it is deleted.

[As the organization administrator](/user-guide/organization-administrators), you can use Snowsight or SQL to delete the
account URL before the 90 days expire:

Snowsight:
:   1. In the navigation menu, select **Admin** » **Accounts**.
    2. Find the active account, and select **…** » **Manage Urls**.
    3. In the **Previous Organization URL** section, select **Delete URL**.
    4. Select **Delete**.

SQL:
:   Execute the [ALTER ACCOUNT … DROP OLD ORGANIZATION URL](/sql-reference/sql/alter-account) command for the account.

    For example, to drop the original account URL for an account that had its organization modified, execute:

    Copy code

    ```
    ALTER ACCOUNT my_account1 DROP OLD ORGANIZATION URL;
    ```
