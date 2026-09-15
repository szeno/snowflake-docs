# Introduction to organizations

An *organization* is a first-class Snowflake object that links the accounts owned by your business entity. Organizations simplify account
management and billing, [Replication and Failover/Failback](/user-guide/replication-intro), Snowflake Secure Data Sharing, and other
account administration tasks.

This feature allows organization administrators to view, create, and manage all of your accounts across different regions and cloud platforms.

## Types of accounts

An organization can consist of the following types of accounts:

- Organization account: Special account used by organization administrators to manage multi-account organizations and to access usage data
  from premium views in the ORGANIZATION\_USAGE schema. For more information, see [Organization accounts](/user-guide/organization-accounts).
- Regular Snowflake account, including [trial accounts](/user-guide/admin-trial-account).
- Snowflake Open Catalog account: Special account used by service admins and catalog admins to manage catalogs defined in Snowflake Open
  Catalog. For more information, see [Snowflake Open Catalog overview](https://other-docs.snowflake.com/en/opencatalog/overview).

## Benefits

- A central view of all accounts within your organization. For more information, refer to [Viewing accounts in your organization](/user-guide/organizations-manage-accounts-view).
- Self-service account creation. For more information, refer to [Creating an account](/user-guide/organizations-manage-accounts-create).
- Data availability and durability by leveraging data replication and failover. For more information, see [Introduction to replication and failover across multiple accounts](/user-guide/account-replication-intro).
- Seamless data sharing with Snowflake consumers across regions. For more information, see [Share data securely across regions and cloud platforms](/user-guide/secure-data-sharing-across-regions-platforms).
- Ability to monitor and understand usage across all accounts in the organization. For more information, see [Organization Usage](/sql-reference/organization-usage) views.

## Organization creation

Snowflake customers never directly create an organization. For users who sign-up for a Snowflake account using the self-service option,
an organization is automatically created with a system-generated name when the account is created. For entities who work directly with
Snowflake personnel to set up accounts, Snowflake creates the organization to which the accounts belong using a custom name. In either
case, users can create additional accounts that belong to the organization after it is created with the initial account.

## Viewing the name of your organization and its accounts

If you are the [organization administrator](/user-guide/organization-administrators), you can view the name of your organization and
its accounts through the web interface or using SQL:

> SQL:
> :   Execute a [SHOW ACCOUNTS](/sql-reference/sql/show-accounts) command.
>
> [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in):
> :   In the navigation menu, select **Admin** » **Accounts**. The organization name is listed above the account names.

Users with any role can execute the [CURRENT\_ORGANIZATION\_NAME](/sql-reference/functions/current_organization_name)
function to return the organization of the current account.

Users with any role can also find the organization name and account name for a specific account that they have previously signed in to.
See [Finding the organization and account name for an account](/user-guide/admin-account-identifier#label-account-name-find).

## Changing the name of your organization

If you want to change the name of an organization, for example to change a system-generated name to a more user-friendly one,
contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

When you contact Snowflake Support, you must decide whether users can temporarily access accounts in the
organization using the original [account URL](/user-guide/organizations-connect#label-connecting-via-url). If you keep the original account URL, it is automatically dropped
after 90 days, at which time users must use the new account URL to access the account. If you want to drop the account URL before the 90 days
expire, see [Deleting an organization URL](/user-guide/organizations-manage-accounts-urls#label-drop-org-access-url).

## Deleting an organization

To delete your Snowflake organization:

1. [Delete all accounts in the organization](/user-guide/organizations-manage-accounts-delete), except the account being used for the
   deletion.
2. Contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support) to delete the last account and the organization.
