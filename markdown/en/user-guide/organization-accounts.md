# Organization accounts

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

The *organization account* is a special type of account that organization administrators use to perform tasks that affect the entire
organization. For example, administrators use the organization account to do the following:

- View organization-level data collected from all accounts in the organization, including the query history from each account.
- Manage organization-level objects (for example, organization users) for all accounts, or a subset of accounts, in an organization.
- Enable Snowflake Marketplace terms for the entire organization.
- Manage the lifecycle of accounts in an organization, including creating and deleting accounts.
- Enable replication for an account.

There is only one organization account for an organization.

## Features available in the organization account

This section describes features that are available from the organization account.

See the following sections for more information about each feature:

- [Premium views](#label-organization-accounts-premium-views)
- [Organization users and user groups](#label-organization-users-and-user-groups)

### Premium views

The ORGANIZATION\_USAGE schema in the organization account contains views that are not available in the ORGANIZATION\_USAGE schema of a
regular account. These additional views are called *premium views*, which are available by default when you create the organization account.
These premium views provide organization-level data that isn’t otherwise available in a single view. For example, you can query the
TAG\_REFERENCES premium view to learn how tags are used throughout the organization, not just in a specific account.

For more information, including costs associated with premium views, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

### Organization users and user groups

Organizations with more than one account sometimes need someone to manage a user or role in multiple accounts. If you don’t want to create
a separate user or role in each account, then you can create an organization user and organization user group in the organization account.

For more information, see [Organization users](/user-guide/organization-users).

## Compliance considerations for hybrid organizations

An organization can have accounts in both regulated regions and non-regulated regions. For example, an organization can have one account in
a [U.S. SnowGov Region](/user-guide/intro-regions#label-intro-regions-snowgov-regions) and another in a [commercial region](/user-guide/intro-regions#label-na-general-regions).
These organizations are called *hybrid organizations*.

Features associated with an organization account might result in [metadata](/sql-reference/metadata) moving from one region to another.
For example, [premium views](/user-guide/organization-accounts-premium-views) might move associated metadata from a regular account’s
region to the region of the organization account. Metadata associated with an organization-level object — for example, an
[organization user](/user-guide/organization-users) — might move from the region of the organization account to the region of an
account that imports the object. For hybrid organizations, this means that metadata might move between a regulated region and a non-regulated
region.

If you have a hybrid organization, Snowflake recommends the following actions:

- Create your organization account in the regulated region.
- Don’t define an organization-level object with sensitive or regulated data.

Compliance standards, such as [FedRAMP](/user-guide/cert-fedramp), and support for different regulated workloads, such as
[ITAR](/user-guide/cert-itar), might be different or unavailable outside of your U.S. SnowGov Region. Consider your compliance
requirements before choosing to move or share data between Snowflake regions.

## About administrator roles and assignable privileges

Organization administrators use the GLOBALORGADMIN role in the organization account to perform all organization-level tasks, including
administration of the organization account itself.

Note

Before the introduction of the organization account, organization administrators used the ORGADMIN role in an ORGADMIN-enabled account to
perform organization-level tasks. Using the ORGADMIN role in an ORGADMIN-enabled account is being phased out. Use the GLOBALORGADMIN role
in the organization account to perform organization-level tasks.

Snowflake will send a notification email to customers at least three months prior to phasing out the ORGADMIN role.

The GLOBALORGADMIN role can assign privileges to other roles to let other users perform organization-level tasks. In the organization
account, the GLOBALORGADMIN role can assign the following privileges:

- APPLY TAG
- MANAGE ACCOUNTS
- MANAGE LISTING AUTO FULFILLMENT
- MANAGE ORGANIZATION CONTACTS
- MANAGE ORGANIZATION TERMS
- PURCHASE DATA EXCHANGE LISTING

These privileges are set on the account level. For example, to assign the MANAGE ACCOUNTS privilege to the role `custom_role`, execute the
following:

Copy code

```
USE ROLE GLOBALORGADMIN;

GRANT MANAGE ACCOUNTS ON ACCOUNT TO ROLE custom_role;
```

For more information about these privileges, see [Access control privileges](/user-guide/security-access-control-privileges).

## Create the organization account

Before creating the organization account, consider the following details:

- If your organization includes an account in a [U.S. SnowGov Region](/user-guide/intro-regions#label-intro-regions-snowgov-regions), Snowflake recommends
  creating the organization account in this regulated region. For more information about the implication of having an organization with
  both regulated and non-regulated accounts, see [Compliance considerations for hybrid organizations](#label-orgs-hybrid-considerations).
- Creating the organization account results in the ORGANIZATION\_USAGE schema being populated with data, which
  [incurs additional costs](/user-guide/organization-accounts-premium-views#label-org-account-views-cost) for your organization.
- You can’t convert an existing ORGADMIN-enabled account to be the organization account.

To create the organization account:

1. Choose an existing account from which you will create the organization account. This existing account must have the
   [ORGADMIN role enabled](/user-guide/organization-administrators#label-enabling-orgadmin-role-for-account).
2. Sign in to the account you are using to create the organization account.
3. Switch to the ORGADMIN role. For example:

   Copy code

   ```
   USE ROLE ORGADMIN;
   ```
4. Execute the [CREATE ORGANIZATION ACCOUNT](/sql-reference/sql/create-organization-account) command. For example:

   Copy code

   ```
   CREATE ORGANIZATION ACCOUNT myorgaccount
    ADMIN_NAME = admin
    ADMIN_PASSWORD = 'TestPassword1'
    EMAIL = 'myemail@myorg.org'
    MUST_CHANGE_PASSWORD = true
    EDITION = enterprise;
   ```

Note

Snowflake does not support custom account locators for organization accounts. For alternatives, contact your Snowflake representative.

## Delete the organization account

If you want to drop the organization account in your multi-account organization, then contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Note

New functionality in Snowflake that includes organization-level administrative tasks will require an organization account. If you are
concerned about the costs associated with [premium views](/user-guide/organization-accounts-premium-views), contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support) to request that they be disabled instead of deleting the account.

## Move the organization account to a different region

You can move an organization account between regions as long as those regions are in either the PUBLIC region group or a VPS region group.

Snowflake uses replication groups to move objects from the organization account in the source region to the organization account in the new
region. As a result, only objects that can be replicated are moved with the organization account and there are replication costs associated
with the move. For a list of objects that can be moved with the organization account, see [Replicated objects](/user-guide/account-replication-intro#label-replicated-objects).

Note

[Organization profiles](/user-guide/collaboration/organization-profiles/org-profiles-create-manage) move with the organization
account to the new region.

Moving the organization account to a different region is a two-step process:

1. Call the [SYSTEM$INITIATE\_MOVE\_ORGANIZATION\_ACCOUNT](/sql-reference/functions/system_initiate_move_organization_account) function from the organization account to start
   the process of moving it. Snowflake begins replicating objects to the new region.

   The function accepts a temporary account name, the new region, and a list of objects to move as its arguments. For example:

   Copy code

   ```
   CALL SYSTEM$INITIATE_MOVE_ORGANIZATION_ACCOUNT(
     'MY_TEMP_NAME',
     'aws_us_west_2',
     'ALL');
   ```
2. When you have verified that the data in the organization account has been successfully replicated in the new region, call the
   [SYSTEM$COMMIT\_MOVE\_ORGANIZATION\_ACCOUNT](/sql-reference/functions/system_commit_move_organization_account) function to finalize the move, specifying a grace period
   after which the original organization account is deleted.

   For example, the following call finalizes the move, and specifies that the original organization account in the source region will
   be deleted after 14 days.

   Copy code

   ```
   CALL SYSTEM$COMMIT_MOVE_ORGANIZATION_ACCOUNT(14);
   ```

At any point, you can view the status of an attempt to move an organization account by calling the
[SYSTEM$SHOW\_MOVE\_ORGANIZATION\_ACCOUNT\_STATUS](/sql-reference/functions/system_show_move_organization_account_status) function.

Note

When an organization account is moved, the views in the ORGANIZATION\_USAGE schema must be repopulated with data, a process that can take up
to one week.

## Limitations

Replication isn’t fully supported for the organization account; some objects can’t be replicated to or from the organization account.
