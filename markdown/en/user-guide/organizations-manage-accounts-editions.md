Feature — Generally Available

Currently available in [these regions](/user-guide/intro-regions).

Not available in DoD and China deployments.

# Working with account editions

Each account in an organization has a specific [Snowflake edition](/user-guide/intro-editions) that determines its available features
and level of service.

[As the organization administrator](/user-guide/organization-administrators), you can check the account edition in
[Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) or using SQL:

> Snowsight:
> :   In the navigation menu, select **Admin** » **Accounts**.
>
> SQL:
> :   Execute the [SHOW ACCOUNTS](/sql-reference/sql/show-accounts) command.

Tip

If you are not an organization administrator but want to view the edition of an account, do the following:

1. Open Snowsight, and then select your name to open the user menu.
2. Locate the account and select **View Account Details**.
3. View the edition and other details.

## Change the account edition

An [organization administrator](/user-guide/organization-administrators) can change the [Snowflake edition](/user-guide/intro-editions)
of an account by using SQL. For example, you can upgrade from Standard Edition to Enterprise Edition if you want to
use features that are only available in the Enterprise Edition.

Note

Managed accounts (sometimes referred to as parent accounts), including reader accounts created by a provider account, cannot be altered with `ALTER ACCOUNT ... SET EDITION`.
To change the edition on a managed account, contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

If you are downgrading from a higher edition to a lower edition, you must first stop using all features that are unique to the higher
edition. For example, if you have existing masking policies in the account, you cannot downgrade to the Standard Edition because masking
policies are only available in Enterprise Edition or higher. In this case, you need to delete all masking policies before changing
the edition.

After you change the edition of an account, you cannot downgrade the account within the same day.

Note

You cannot upgrade an account to the VPS Edition without contacting Snowflake Support.

The organization administrator executes the [ALTER ACCOUNT](/sql-reference/sql/alter-account) command to change the edition of an account. The
syntax of the command is:

Copy code

```
ALTER ACCOUNT <name> SET EDITION =
  { 'STANDARD' | 'ENTERPRISE' | 'BUSINESS_CRITICAL' }
```

### Example

The following steps change the edition of the `acct_1` account to the Enterprise Edition:

1. [As the organization administrator](/user-guide/organization-administrators), open a Worksheet and execute the following command:

   Copy code

   ```
   ALTER ACCOUNT acct_1 SET EDITION = 'ENTERPRISE';
   ```
