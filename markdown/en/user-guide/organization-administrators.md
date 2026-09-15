# Organization administrators

Organization administrators perform organization-level tasks such as managing accounts and viewing organization-level usage information.
Currently, there are two ways to perform organization-level tasks:

- Use the GLOBALORGADMIN role in the organization account
- Use the ORGADMIN role

## Using the GLOBALORGADMIN role

Multi-account organizations should use the GLOBALORGADMIN role in the [organization account](/user-guide/organization-accounts) to perform
organization-level tasks. A user with the GLOBALORGADMIN role is also known as the global organization administrator.

To perform tasks as the global organization administrator, do the following:

1. Sign in to the organization account.
2. Do one of the following:
   - If you are performing tasks in a SQL worksheet, execute the following command:

     Copy code

     ```
     USE ROLE GLOBALORGADMIN;
     ```
   - If you are performing other tasks in Snowsight, [switch your active role](/user-guide/ui-snowsight-gs#label-switching-your-active-role) to
     GLOBALORGADMIN.

## Using the ORGADMIN role

Important

Using the ORGADMIN role in an ORGADMIN-enabled account is being phased out for multi-account organizations. Strongly consider using the
[GLOBALORGADMIN role in the organization account](#label-org-admins-globalorgadmin) to perform organization-level tasks.

Snowflake will send a notification email to customers at least three months prior to phasing out the ORGADMIN role.

To perform tasks with the ORGADMIN role, do the following:

1. Sign in to an ORGADMIN-enabled account.
2. Do one of the following:
   - If you are performing tasks in a SQL worksheet, execute the following command:

     Copy code

     ```
     USE ROLE ORGADMIN;
     ```
   - If you are performing other tasks in Snowsight, [switch your active role](/user-guide/ui-snowsight-gs#label-switching-your-active-role) to ORGADMIN.

## Enabling the ORGADMIN role in an account

The first account in an organization has the ORGADMIN role enabled. You can use this account to enable the role in other accounts. For example, to
enable the ORGADMIN role for an account `my_account1`, the organization administrator can execute the following
command from an account that already has the ORGADMIN role enabled:

Copy code

```
USE ROLE ORGADMIN;

ALTER ACCOUNT my_account1 SET IS_ORG_ADMIN = TRUE;
```

Keep the following in mind when enabling the ORGADMIN role:

- The ALTER ACCOUNT syntax only accepts the [account name format](/user-guide/admin-account-identifier#label-account-name) of the account identifier. You cannot use the
  account locator to specify the account.
- By default, the ORGADMIN role can be enabled in a maximum of eight accounts. If your organization requires more accounts with the ORGADMIN
  role, contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).
- The ORGADMIN role cannot be enabled for a [reader account](/user-guide/data-sharing-reader-create).

## Disable the ORGADMIN role

You can prevent regular, ORGADMIN-enabled accounts from being used to perform organization-level tasks.
To accomplish this, execute the ALTER ACCOUNT command to remove the ORGADMIN role from the account. For example, if you want to stop using
the `account_123` account to perform organization-level tasks, do the following:

1. Sign in to a **different** ORGADMIN-enabled account.
2. Assume the ORGADMIN role:

   Copy code

   ```
   USE ROLE ORGADMIN;
   ```
3. Execute the following command:

   Copy code

   ```
   ALTER ACCOUNT account_123 SET IS_ORG_ADMIN = FALSE;
   ```

The ALTER ACCOUNT syntax only accepts the [account name format](/user-guide/admin-account-identifier#label-account-name) of the account identifier. You cannot use the
account locator to specify the account.

Note

Currently, you cannot disable the ORGADMIN role if it is the last account that has the role enabled. Contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).
