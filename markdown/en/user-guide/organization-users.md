# Organization users

[Enterprise Edition Feature](/user-guide/intro-editions)

Organization users and organization user groups require Enterprise Edition. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Organizations with multiple accounts often need to have the same person be a user in more than one of those accounts. The same is true of a
service or application that runs in more than one account. To avoid the repetition of creating a user object in each account separately,
the organization administrator can create an *organization user* in the [organization account](/user-guide/organization-accounts). Each
organization user acts as a global user entity that can be imported into regular accounts by account administrators, simplifying the
process of having the same person or service have a user object in multiple accounts.

Account administrators don’t add organization users directly to their regular account. Rather, they add *organization user groups*, which
are logical groupings of organization users. When the account administrator imports the organization user group, its organization users are
added to the account.

Note

If you want to create organization users for people or services that already have a user object in one or more regular accounts, you’ll
need to link the organization user with the existing user object after importing the organization user group. For more information, see
[Resolve conflicts after importing users](#label-org-users-conflicts).

## Get started

The basic workflow of getting organization users into one or more accounts is as follows:

1. As a global organization administrator in the organization account:

   1. [Create an organization user](#label-org-users) for each person or service that
      you want to be a user in multiple regular accounts.
   2. [Create an organization user group](#label-org-users-groups-create) that is a logical grouping of the users.
   3. [Add the organization users to the organization user group](#label-org-users-groups-add).
   4. [Make the organization user group available](#label-org-users-groups-visibility) to the account administrators in regular accounts.
2. As an administrator in a regular account:

   1. [Import the organization user group](#label-org-users-add) into the account.
   2. [Check for and resolve any conflicts](#label-org-users-conflicts).

For an end-to-end example of this workflow, see [Extended example](#label-org-users-example).

## Create an organization user

The organization administrator creates an organization user with the basic properties of a user object such as the login name and email.
Only an email is required, but these basic properties can’t be set in a regular account after the user is imported. For a list of these
basic properties, see [CREATE ORGANIZATION USER](/sql-reference/sql/create-organization-user).

As an example, the following command creates an organization user:

Copy code

```
USE ROLE GLOBALORGADMIN;

CREATE ORGANIZATION USER asmith
   EMAIL = 'asmith@example.com'
   LOGIN_NAME = 'asmith@example.com';
```

The USERADMIN role can also create an organization user.

## Organization user types

An organization user is either a `PERSON` user, which represents a person, or a `SERVICE` user, which represents a service or application
that interacts with Snowflake without human interaction. Specify the `TYPE` property to choose between them. If you don’t specify a type, the
organization user is a `PERSON` user. For the characteristics of each type, including the authentication methods that a service user can
use, see [Types of users](/user-guide/admin-user-management#label-user-management-types).

For example, the following command creates an organization user for a service that loads data in several accounts:

Copy code

```
USE ROLE GLOBALORGADMIN;

CREATE ORGANIZATION USER etl_pipeline
   EMAIL = 'data-platform@example.com'
   TYPE = SERVICE;
```

The type of an organization user determines the following:

- The type of the user objects that Snowflake creates when an account administrator imports an organization user group. Importing a group
  that contains `etl_pipeline` creates a `SERVICE` user named `etl_pipeline` in the regular account.
- The existing users that the organization user is eligible to link to, when an account administrator resolves a conflict. For more
  information, see [Resolve conflicts after importing users](#label-org-users-conflicts).

`PERSON` and `SERVICE` are the only types available to an organization user. Other user types, such as `SERVICE_AGENT` and
`LEGACY_SERVICE`, are only available to users in a regular account. You also can’t change the type after you create the organization user,
so create the organization user with the type that the corresponding users in your accounts need.

## Organization user groups

*Organization user groups* are logical groupings of organization users. The organization administrator creates these organization
user groups, then adds the organization users that should belong in each group. When the account administrator imports an organization user
group into an account, all the organization users in the group become user objects in the regular account. An organization user can be a
member of multiple organization user groups.

When the account administrator imports an organization user group into a regular account, Snowflake creates an access control
[role](/user-guide/security-access-control-overview#label-access-control-overview-roles) of the same name. For example, if the organization user group is named `data_stewards`,
then importing the group to the regular account creates a role named `data_stewards`. Each user imported from the organization user group is
granted this role.

Administrators in the regular account can fine-tune access control by granting and revoking privileges to the role that has
been granted to each of the users that were imported from the organization user group. You can also grant account-specific roles to the new
role or grant the new role to account-specific roles.

You can import the same organization user group into multiple regular accounts to implement consistent roles across the organization. Each
regular account can assign account-specific privileges to the role, but the naming will be consistent. Alternatively, you could create a
separate organization user group for each account, then add the organization users that are needed in a particular account to the
appropriate organization user group.

If the administrator imports multiple organization user groups that contain the same organization user, only one local user is created, and
this user is granted the roles from all of the organization user groups.

The organization administrator task of preparing an organization user group for the account administrator of regular accounts is a
three-step process:

1. [Create the organization user group](#label-org-users-groups-create).
2. [Add organization users to the group](#label-org-users-groups-add).
3. [Set the visibility of the group](#label-org-users-groups-visibility) to specify which regular accounts can access it.

### Create an organization user group

The organization administrator executes the [CREATE ORGANIZATION USER GROUP](/sql-reference/sql/create-organization-user-group) command to create a new organization
user group in the organization account.

As an example, the following command creates an organization user group that represents a logical grouping of data engineers.

Copy code

```
USE ROLE GLOBALORGADMIN;

CREATE ORGANIZATION USER GROUP data_engineers_group
 IS_GRANTABLE = TRUE;
```

Because the administrator set `IS_GRANTABLE=TRUE`, the account administrator will be able to grant the role created from the
organization user group to a local, account-specific role. Without that parameter, the account administrator can’t grant the role imported
from the organization user group to another role in the regular account.

The USERADMIN role can also create an organization user group.

### Add organization users to an organization user group

After the organization administrator creates an organization user group, they can execute the
[ALTER ORGANIZATION USER GROUP](/sql-reference/sql/alter-organization-user-group) command to add organization users to the group as a comma-delimited list. For
example, to add two existing organization users to the organization user group `data_engineers_group`, execute:

Copy code

```
ALTER ORGANIZATION USER GROUP data_engineers_group
   ADD ORGANIZATION USERS asmith, sjohnson;
```

### Make organization user groups available to regular accounts

After you have created an organization group, you need to specify which regular accounts can view and import the group. Account administrators
cannot use the organization user group to import users until you use the [ALTER ORGANIZATION USER GROUP](/sql-reference/sql/alter-organization-user-group) command
to set the visibility of the group. You can specify that all regular accounts can import the organization user group or you can restrict access
to specific accounts.

The following command only allows the account `qa_env` to add the organization user group:

Copy code

```
ALTER ORGANIZATION USER GROUP data_engineers_group
   SET VISIBILITY = ACCOUNTS qa_env;
```

Note

An organization administrator cannot unilaterally hide an organization user group from an
account that previously had visibility. An administrator in the regular account must run the ALTER ACCOUNT REMOVE ORGANIZATION USER GROUP
command to remove the organization user group from the account before the organization administrator can change the visibility.

## Import users in a regular account

After the organization administrator has created an organization user group, administrators in regular accounts can
import the organization users by executing the ALTER ACCOUNT command to add the organization user group. These administrators can
only import an organization user group if the organization administrator has
[set the visibility of the group](#label-org-users-groups-visibility) so the regular account can access it.

By default, only users with the ACCOUNTADMIN role can import organization user groups into the regular account. To allow other users to import an
organization group, grant them the IMPORT ORGANIZATION USER GROUPS privilege.

The syntax to import an organization user group to a regular account is as follows:

Copy code

```
ALTER ACCOUNT ADD ORGANIZATION USER GROUP <group_name>
```

For an example of importing an organization user group to add users, see [Extended example](#label-org-users-example).

## Resolve conflicts after importing users

The account administrator who imports organization users in their regular account must manually check for conflicts. These conflicts can
arise between the properties of users or the name of the organization user group.

### Conflict between organization user group and existing role

A conflict occurs when the name of the organization user group matches the name of an existing
[role](/user-guide/security-access-control-overview#label-access-control-overview-roles) in the regular account. The users in the group are not imported until you resolve the
conflict.

To check whether there is a conflict after importing an organization user group, do the following:

1. Execute the [SHOW ORGANIZATION USER GROUPS](/sql-reference/sql/show-organization-user-groups) command.
2. In the `is_imported` column, check if the value is TRUE. If the value is FALSE, the organization user group was not successfully
   imported, which might indicate that there is a conflict.

You can resolve the conflict between a role and an organization user group by linking the role with the group. Linking a role allows it to
be managed as an organization user group going forward. After you link the conflicting role, the organization user group is added to the
account without further action. Call the [SYSTEM$LINK\_ORGANIZATION\_USER\_GROUP](/sql-reference/functions/system_link_organization_user_group) function to link a role with
an organization user group.

For example, suppose the role `marketing_team` existed in your account before importing the organization user group `marketing_team` to the
account. To link the role to the organization user group and complete the process of importing the group, execute the following:

Copy code

```
SELECT SYSTEM$LINK_ORGANIZATION_USER_GROUP('marketing_team');
```

### Conflict between organization user and existing user

A conflict occurs when any of the following is true:

- The `name` property of an organization user matches the `name` of an existing user in the regular account.
- The `login_name` property of an organization user matches the `login_name` of an existing user in the regular account.

To check whether there is a user conflict after importing an organization user group, do the following:

1. Execute the [SHOW ORGANIZATION USERS IN ORGANIZATION USER GROUP](/sql-reference/sql/show-organization-users) command.
2. In the `is_imported` column, find rows where the value is FALSE. At least one property of the user in that row conflicts with the
   properties of an existing user.

Tip

You can use the [pipe operator](/sql-reference/operators-flow) (`->>`) to post-process the output of SHOW ORGANIZATION USERS and filter on
the `is_imported` column. For example, to search for organization users that were not successfully imported from the
`marketing_team` organization user group, run the following query:

Copy code

```
SHOW ORGANIZATION USERS IN ORGANIZATION USER GROUP marketing_team
  ->> SELECT * FROM $1 WHERE "is_imported" = 'false';
```

Use one of the following strategies to resolve a conflict between an organization user and an existing user:

- **Link the existing user**: If an existing user object corresponds to the same person or service as an organization user, and you want to
  manage the user as an organization user going forward, you can link the existing user with the organization user to resolve the conflict.
  Call the [SYSTEM$LINK\_ORGANIZATION\_USER](/sql-reference/functions/system_link_organization_user) function to link an existing user with an organization user. For
  example, to link the existing user `jloeb` with the organization user `jloebsmith`, call the function as follows:

  Copy code

  ```
  SELECT SYSTEM$LINK_ORGANIZATION_USER('jloeb', 'jloebsmith');
  ```

  The two users must have compatible types. A `SERVICE` organization user can only be linked to a `SERVICE` local user. A `PERSON`
  organization user can only be linked to a local user that is a `PERSON` user or whose `TYPE` property is `NULL`. If the types aren’t
  compatible, the function returns an error and the local user isn’t linked. Because you can’t change the type of an organization user, use
  [ALTER USER](/sql-reference/sql/alter-user) to change the type of the local user, then link it. For example, to link a service user that predates
  the organization user to the `SERVICE` organization user `etl_pipeline`:

  Copy code

  ```
  ALTER USER legacy_loader SET TYPE = SERVICE;

  SELECT SYSTEM$LINK_ORGANIZATION_USER('legacy_loader', 'etl_pipeline');
  ```
- **Drop the existing user**: If you want the organization user to completely replace the local user, run a
  [DROP USER](/sql-reference/sql/drop-user) command to delete the local user. After the local object is dropped, Snowflake automatically adds the
  new user object that corresponds to the organization user.
- **Rename the existing user or its properties**: If you don’t want to link the existing local user with an organization user, but you
  want to preserve the existing user instead of dropping it, you can rename the user object or its properties in the
  regular account to resolve the conflict. After the local object is renamed, Snowflake automatically adds the new user object that
  corresponds to the organization user. For example, if the pre-existing user and the organization user both have the login name
  `JOE_LOGIN`, you could execute the following in the regular account to avoid the conflict:

  Copy code

  ```
  USE ROLE ACCOUNTADMIN;
  ALTER USER joe SET LOGIN_NAME = joe_login_renamed;
  ```

## Modifying imported users

Administrators in a regular account can use the [ALTER USER](/sql-reference/sql/alter-user) command to modify a subset of the properties of a user
object after it has been imported. The administrator can modify all properties *except* the properties that can be set on the
organization user in the organization account. For a list of the properties that can only be set in the organization account, see
[CREATE ORGANIZATION USER](/sql-reference/sql/create-organization-user).

## Testing whether users and roles were imported

Administrators in a regular account can use the [SYS\_CONTEXT](/sql-reference/functions/sys_context) function to determine whether local users and
roles were created when an organization user group was imported into the account.

To determine whether local user `joe` is linked to an organization user, run the following command:

Copy code

```
SELECT SYS_CONTEXT('SNOWFLAKE$ORGANIZATION', 'IS_USER_IMPORTED', 'joe');
```

To determine whether the role `analysts` corresponds to an organization user group that was imported, run the following command:

Copy code

```
SELECT SYS_CONTEXT('SNOWFLAKE$ORGANIZATION', 'IS_GROUP_IMPORTED', 'analysts');
```

## Removing organization users and groups

Organization users and organization user groups can be [removed from a single account](#label-org-users-remove-account) or removed from
all accounts by [dropping them in the organization account](#label-org-users-remove-org).

### Removing users from a single regular account

An account administrator can execute an ALTER ACCOUNT command to remove an organization user group from the account. Removing the
organization user group drops all of the users that were imported and removes the role that was created when the organization user group
was imported. This command does not affect the organization users and organization user groups in other regular accounts, nor in the
organization account.

Note

An organization user can be a member of multiple organization user groups. If a user was imported from more than one organization
group, removing one of the groups from the regular account does not remove the user. The user isn’t removed until all of the organization
user groups are removed.

For example, the following command drops all of the users imported from the `data_stewards` group and deletes the `data_stewards`
role:

Copy code

```
ALTER ACCOUNT REMOVE ORGANIZATION USER GROUP data_stewards;
```

### Removing users from all regular accounts

When an organization user is dropped in the organization account, the corresponding user object is dropped from every regular account that
imported the user. To drop an organization user, execute the [DROP ORGANIZATION USER](/sql-reference/sql/drop-organization-user) command in the organization
account.

When an organization user group is dropped in the organization account, the effect on organization users depends on whether the users in the
regular account belong to other organization user groups that were also imported into the account. If an organization user belongs to a different
organization user group that was imported, the user is not removed from the account. Otherwise, dropping the organization user group removes
all of the users imported from the group.

Dropping an organization user group also removes the role that was created when the group was imported.

To drop an organization user group, execute the [DROP ORGANIZATION USER GROUP](/sql-reference/sql/drop-organization-user-group) command in the organization account.

## Unlinking organization users and organization user groups

When organization users are successfully imported into a regular account, the local user object is linked to the organization user. If you
decide you want to keep the user object in an account, but no longer want it associated with the organization user, you can use the
[SYSTEM$UNLINK\_ORGANIZATION\_USER](/sql-reference/functions/system_unlink_organization_user) function to unlink the local user from the organization user. All of the
properties of the user are preserved and it can be managed as a local user going forward.

Similarly, you can use the [SYSTEM$UNLINK\_ORGANIZATION\_USER\_GROUP](/sql-reference/functions/system_unlink_organization_user_group) function to unlink a role that was created
by adding an organization user group. This keeps everything about the role the same, but unlinks it from the organization user group. Local
user objects that were added when the organization user group was imported are also unlinked, and are managed as local users going forward.

## Extended example

Organization administrator workflow
:   1. As the organization administrator, sign in to the organization account.
    2. Create organization users for two people who are data stewards:

       Copy code

       ```
       USE ROLE GLOBALORGADMIN;

       CREATE ORGANIZATION USER joe_kelley
       EMAIL = 'jkelley@example.com'
       LOGIN_NAME = 'jkelley@example.com';

       CREATE ORGANIZATION USER grace_vivian
       EMAIL = 'gvivian@example.com'
       LOGIN_NAME = 'gvivian@example.com';
       ```
    3. Create an organization user group that represents a logical grouping of data stewards.

       Copy code

       ```
       CREATE ORGANIZATION USER GROUP data_stewards_group;
       ```
    4. Add the organization users to the new organization user group.

       Copy code

       ```
       ALTER ORGANIZATION USER GROUP data_stewards_group
       ADD ORGANIZATION USERS joe_kelley, grace_vivian;
       ```
    5. Allow all regular accounts to import the organization user group.

       Copy code

       ```
       ALTER ORGANIZATION USER GROUP data_stewards_group
       SET VISIBILITY = ALL;
       ```

Account administrator workflow
:   1. As the account administrator, sign in to the regular account where you want to import the organization users.
    2. List the organization user groups that can be imported into the account.

       Copy code

       ```
       USE ROLE ACCOUNTADMIN;

       SHOW ORGANIZATION USER GROUPS;
       ```
    3. Import the organization user group into the account.

       Copy code

       ```
       ALTER ACCOUNT
         ADD ORGANIZATION USER GROUP data_stewards_group;
       ```
    4. Check for conflicts between the organization user group and an existing role:

       Copy code

       ```
       SHOW ORGANIZATION USER GROUPS;
       ```

       Make sure the value of the `is_imported` column is TRUE, which indicates there was no conflict.
    5. List the users that have been added to the account and check for conflicts:

       Copy code

       ```
       SHOW ORGANIZATION USERS IN ORGANIZATION USER GROUP data_stewards_group;
       ```

       Make sure the value of the `is_imported` column is TRUE for all of the organization users, which indicates there were no
       conflicts.

## Related functions

For a list of functions that help you work with organization users and organization user groups, see
[Organization user and organization user group functions](/sql-reference/functions-organization-users).

## Limitations and considerations

After an organization user is added to a regular account, you’ll set up the user’s authentication methods the same as any other user.
You can’t set up authentication at the organization level.
