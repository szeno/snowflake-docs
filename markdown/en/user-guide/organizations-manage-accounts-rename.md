# Renaming an account

An organization administrator can rename an account.

When an account is renamed, Snowflake creates a new [account URL](/user-guide/organizations-connect#label-connecting-via-url) that is used to access the account.
During the renaming, the administrator can accept the default to save the original account URL so users can continue to use it, or they
can delete the original URL to force users to use the new URL. Saved URLs can be
[deleted at a later time](/user-guide/organizations-manage-accounts-urls#label-drop-account-access-url).

Note

Renaming an account has no effect on [replication and failover](/user-guide/account-replication-intro).

[As the organization administrator](/user-guide/organization-administrators), you can rename an account using [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in)
or SQL. You must use SQL to rename a reader account.

Snowsight:
:   1. In the navigation menu, select **Admin** » **Accounts**.
    2. Find the active account, and select **…** » **Edit account name**.
    3. In the **Account Name** box, enter the new account name.
    4. If you want to force users to access the account using the new account URL, clear the **Save Current URL** checkbox. Otherwise,
       accept the default to allow users to continue to use the original account URL.
    5. Select **Save**.

SQL:
:   Execute the [ALTER ACCOUNT … RENAME TO](/sql-reference/sql/alter-account) command.

    For example, the following command renames an account called `original_acctname` to `new_acctname`:

    Copy code

    ```
    ALTER ACCOUNT original_acctname RENAME TO new_acctname;
    ```

    To force users to access the account with the new account URL, set the optional SAVE\_OLD\_URL parameter to FALSE when renaming the account.

Note

Organization administrators who are using the ORGADMIN role cannot rename an account while they are logged in to it, so they must log in
to a different account before executing the renaming command. If your organization consists of a single account that needs to be renamed,
contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).
