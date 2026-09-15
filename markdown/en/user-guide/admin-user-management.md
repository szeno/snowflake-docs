# User management

User administrators can create and manage Snowflake users through SQL or the web interface:

- Using SQL, administrators can perform all user-related tasks, including changing login credentials and defaults for users.
- Snowsight supports most user-related tasks.

## Types of users

Some user objects correspond to human users while other user objects correspond to a service or application that interacts with Snowflake
programmatically without human interaction. When you create a user object, you specify the type of user to differentiate between people and
services. This distinction is important because people need to enroll in
[multi-factor authentication (MFA)](/user-guide/security-mfa), but services and applications should not because there is no one to
use a secondary method of authentication.

The `TYPE` property of a user object determines the type of user. Possible values of this `TYPE` property are as follows:

PERSON:
:   User is a human user who can interact with Snowflake.

NULL:
:   Functions the same as `PERSON`.

SERVICE:
:   User is a service or application that interacts with Snowflake without human interaction.

    To improve the security posture of non-interactive use cases, users with the `TYPE` property set to `SERVICE` have the
    following characteristics:

    - They cannot log in using a password.
    - They cannot log in using SAML SSO.
    - They cannot [enroll in MFA](/user-guide/ui-snowsight-profile#label-snowsight-set-up-mfa).
    - They are not subject to authentication policy MFA enforcement.
    - They cannot have the following properties:

      - `FIRST_NAME`
      - `MIDDLE_NAME`
      - `LAST_NAME`
      - `PASSWORD`
      - `MUST_CHANGE_PASSWORD`
      - `MINS_TO_BYPASS_MFA`
    - The following commands cannot be used:

      - ALTER USER RESET PASSWORD
      - ALTER USER SET `DISABLE_MFA = TRUE`

SERVICE\_AGENT:
:   User is an automated AI agent that interacts with its own identity and privileges.

    `SERVICE_AGENT` users share the non-interactive authentication characteristics of `SERVICE` users. Users with the `TYPE` property set to
    `SERVICE_AGENT` have the following characteristics:

    - They cannot log in using a password.
    - They cannot log in using SAML SSO.
    - They cannot [enroll in MFA](/user-guide/ui-snowsight-profile#label-snowsight-set-up-mfa).
    - They are not subject to authentication policy MFA enforcement.
    - Every session opened by a `SERVICE_AGENT` user is automatically agent-active. [IS\_AGENT\_ACTIVATED](/sql-reference/functions/is_agent_activated)
      returns `'TRUE'` for the session when you call `SYS_CONTEXT('SNOWFLAKE$CURRENT', 'IS_AGENT_ACTIVATED')`.
    - They support [workload identity federation](/user-guide/workload-identity-federation), [key-pair authentication](/user-guide/key-pair-auth),
      and [programmatic access tokens](/user-guide/programmatic-access-tokens). Unlike `SERVICE` users, `SERVICE_AGENT` users do not require a
      network policy before a programmatic access token can be created.
    - They cannot have the following properties:
      - `FIRST_NAME`
      - `MIDDLE_NAME`
      - `LAST_NAME`
      - `PASSWORD`
      - `MUST_CHANGE_PASSWORD`
      - `MINS_TO_BYPASS_MFA`
      - `MINS_TO_BYPASS_NETWORK_POLICY_REQUIREMENT`
    - The following commands cannot be used:
      - ALTER USER RESET PASSWORD
      - ALTER USER SET `DISABLE_MFA = TRUE`

    You can create and manage `SERVICE_AGENT` users using SQL ([CREATE USER](/sql-reference/sql/create-user), [ALTER USER](/sql-reference/sql/alter-user)) or the
    [SCIM API](/user-guide/scim-user-api-reference) (`type = service_agent`).

    For an overview of agent identity, including how `SERVICE_AGENT` fits with other identification
    paths, see [Agent identity](/user-guide/agent-identity). For agent-aware data governance, you can use
    `SYS_CONTEXT('SNOWFLAKE$CURRENT', 'IS_AGENT_ACTIVATED')` in masking policies. For examples, see
    [Data protection policies for agentic interactions](/user-guide/data-protection-policies-snowsight#label-data-protection-policies-agentic).

SNOWFLAKE\_SERVICE:
:   User that is created by Snowflake for [Snowpark Container Services](/developer-guide/snowpark-container-services/overview).
    Administrators cannot create users of type SNOWFLAKE\_SERVICE, nor can they change the type of an existing user to be SNOWFLAKE\_SERVICE.
    For more information about SNOWFLAKE\_SERVICE users, see [Snowpark Container Services: SQL execution](/developer-guide/snowpark-container-services/spcs-execute-sql).

LEGACY\_SERVICE:
:   A user with their `TYPE` property set to `LEGACY_SERVICE` represents a non-interactive integration. It is similar to
    `SERVICE`, but allows password and SAML authentication.

    Note

    The LEGACY\_SERVICE type is being deprecated. Use the SERVICE type for services and applications. For a timeline of the deprecation of
    LEGACY\_SERVICE, see [Planning for the deprecation of single-factor password sign-ins](/user-guide/security-mfa-rollout).

## User roles

Snowflake uses roles to control the objects (virtual warehouses, databases, tables, etc.) that users can access:

- Snowflake provides a set of predefined roles, as well as a framework for defining a hierarchy of custom roles.
- All Snowflake users are automatically assigned the predefined PUBLIC role, which enables login to Snowflake and basic object access.
- In addition to the PUBLIC role, each user can be assigned additional roles, with one of these roles designated as their *default role*. A user’s default role determines the role used in the Snowflake
  sessions initiated by the user; however, this is only a default. Users can change roles within a session at any time.
- Roles can be assigned at user creation or afterwards.

Attention

When deciding the additional roles to assign to a user, as well as designating their default role, consider the following for the predefined ACCOUNTADMIN role (required for performing account-level
administrative tasks):

- Snowflake recommends strictly controlling the assignment of ACCOUNTADMIN, but recommends assigning it to at least two users.
- ACCOUNTADMIN should never be designated as a user’s default role. Instead, designate a lower-level administrative or custom role as their default.

For more details and best practices related to the ACCOUNTADMIN role, see [Access control best practices](/user-guide/security-access-control-considerations). For more general information about roles, see
[Overview of Access Control](/user-guide/security-access-control-overview).

## Privileges required to create and modify users

The following roles or privileges are required to manage users in your account:

Create users:
:   The USERADMIN system role can create users using SQL ([CREATE USER](/sql-reference/sql/create-user)).

    If you prefer to use a custom role for this purpose, grant the CREATE USER privilege on the account to this role.

Modify users:
:   Only the role with the OWNERSHIP privilege on a user can modify most user properties using SQL
    ([ALTER USER](/sql-reference/sql/alter-user)).

## Creating users

This section describes how to create a user in a specific account.

Note

Snowsight, requires that you specify a password when you create a user. The [CREATE USER](/sql-reference/sql/create-user) command and [UserCollection.create](/developer-guide/snowflake-python-api/reference/latest/_autosummary/snowflake.core.user.UserCollection#snowflake.core.user.UserCollection.create) Python API do not.

Note

If you want to create a user who can access multiple accounts within an organization, see [Organization users](/user-guide/organization-users).

### Using Snowsight

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Governance & security** » **Users & roles**.
3. Select **+ User**.
4. In the **User Name** field, enter a unique identifier for the user. The user uses this identifier to sign in to Snowflake unless you
   specify a login name.
5. Optionally specify an email address for the user in the **Email** field.
6. In the **Password** and **Confirm Password** fields, enter the password for the user.
7. Optionally add a comment explaining why you created the user.
8. Leave the **Force user to change password on first time login** checkbox selected to force the user to change their password when they
   sign in.
9. Optionally select **Advanced User Options** to specify additional details about the user:

   - **Login Name** to use instead of the **User Name** when signing in to Snowflake.
   - **Display Name** that appears after signing in.
   - **First Name** and **Last Name** to complete the user profile.
   - **Default Role**, **Default Warehouse**, and **Default Namespace**.
10. Select **Create User**.

### Using SQL

Use the [CREATE USER](/sql-reference/sql/create-user) command to create a user.

Important

When creating a user, if you assign a default role to the user, you must then explicitly grant this role to the user. For example:

> Copy code
>
> ```
> CREATE USER janesmith PASSWORD = 'abc123' DEFAULT_ROLE = myrole MUST_CHANGE_PASSWORD = TRUE;
>
> GRANT ROLE myrole TO USER janesmith;
> ```

Note that the [GRANT ROLE](/sql-reference/sql/grant-role) command allows you to assign multiple roles to a single user. The web interface does not currently support the same capability.

### Using Python

Use the [UserCollection.create](/developer-guide/snowflake-python-api/reference/latest/_autosummary/snowflake.core.user.UserCollection#snowflake.core.user.UserCollection.create)
Python API to create a user.

Important

When creating a user, if you assign a default role to the user, you must then explicitly grant this role to the user. For example:

> Copy code
>
> ```
> from snowflake.core.user import Securable, User
>
> my_user = User(
>   name="janesmith",
>   password="abc123",
>   default_role="myrole",
>   must_change_password=True)
> root.users.create(my_user)
>
> root.users['janesmith'].grant_role(role_type="ROLE", role=Securable(name='myrole'))
> ```

## Disabling or enabling a user

Disabling a user prevents the user from logging into Snowflake. You can disable a user through the following interfaces.

### Using Snowsight

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Governance & security** » **Users & roles**.
3. Locate the user that you want to disable and select [![More options](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png) » **Disable User**.
4. In the confirmation dialog that opens, select **Disable**.

To enable a user, follow the same steps, but select **Enable User**.

### Using SQL

Use the [ALTER USER](/sql-reference/sql/alter-user) command to disable or enable a user. For example:

- Disable a user:

  Copy code

  ```
  ALTER USER janesmith SET DISABLED = TRUE;
  ```
- Enable a user:

  Copy code

  ```
  ALTER USER janesmith SET DISABLED = FALSE;
  ```

### Using Python

Use the [UserResource.create\_or\_alter](/developer-guide/snowflake-python-api/reference/latest/_autosummary/snowflake.core.user.UserResource#snowflake.core.user.UserResource.create_or_alter)
Python API to disable or enable a user. For example:

- Disable a user:

  Copy code

  ```
  user_parameters = root.users["janesmith"].fetch()
  user_parameters.disabled = True
  root.users["janesmith"].create_or_alter(user_parameters)
  ```
- Enable a user:

  Copy code

  ```
  user_parameters = root.users["janesmith"].fetch()
  user_parameters.disabled = False
  root.users["janesmith"].create_or_alter(user_parameters)
  ```

## Unlocking a user

If a user login fails after five consecutive attempts, the user is locked out of their account for a period of time (currently 15 minutes).
After the period of time elapses, the system automatically clears the lock and the user can attempt to log in again.

To unlock the user before the time has elapsed, you can reset the timer using the [ALTER USER](/sql-reference/sql/alter-user) command or the
[UserResource.create\_or\_alter](/developer-guide/snowflake-python-api/reference/latest/_autosummary/snowflake.core.user.UserResource#snowflake.core.user.UserResource.create_or_alter) Python API.

The following example resets the timer to 0, which immediately unlocks user `janesmith`:

SQLPython

Copy code

```
ALTER USER janesmith SET MINS_TO_UNLOCK = 0;
```

Copy code

```
user_parameters = root.users["janesmith"].fetch()
user_parameters.mins_to_unlock = 0
root.users["janesmith"].create_or_alter(user_parameters)
```

Tip

If a single role has the OWNERSHIP privilege on all Snowflake users, we recommend granting the role to multiple users. That way, if a member of the role is locked out, another member can unlock that user.

## Altering session parameters for a user

- To show the session parameters for a user, use the following SQL syntax:

  Copy code

  ```
  SHOW PARAMETERS [ LIKE '<pattern>' ] FOR USER <name>
  ```
- To alter the session parameters for a user, use the following syntax:

  Copy code

  ```
  ALTER USER <name> SET <session_param> = <value>
  ```

  For example, allow a user to remain connected to Snowflake indefinitely without timing out:

  Copy code

  ```
  ALTER USER janesmith SET CLIENT_SESSION_KEEP_ALIVE = TRUE;
  ```
- To reset a session parameter for a user to the default value, use the following syntax:

  Copy code

  ```
  ALTER USER <name> UNSET <session_param>
  ```

## Modifying other user properties

You can modify all other user properties using the [ALTER USER](/sql-reference/sql/alter-user) command or the
[UserResource.create\_or\_alter](/developer-guide/snowflake-python-api/reference/latest/_autosummary/snowflake.core.user.UserResource#snowflake.core.user.UserResource.create_or_alter) Python API.
You can modify many of the same user properties using Snowsight.

For example:

- Change the last name for user `janesmith` to `Jones`:

  SQL:
  :   Copy code

      ```
      ALTER USER janesmith SET LAST_NAME = 'Jones';
      ```

  Python:
  :   Copy code

      ```
      user_parameters = root.users["janesmith"].fetch()
      user_parameters.last_name = "Jones"
      root.users["janesmith"].create_or_alter(user_parameters)
      ```

  Snowsight:
  :   1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
      2. In the navigation menu, select **Governance & security** » **Users & roles**.
      3. Locate the user that you want to edit and select [![More options](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png) » **Edit**.
      4. For the **Last Name** field, enter **Jones**.
      5. Select **Save User**.
- Set or change the default warehouse, namespace, primary role, and secondary roles for user `janesmith`:

  SQL:
  :   Copy code

      ```
      ALTER USER janesmith SET DEFAULT_WAREHOUSE = mywarehouse DEFAULT_NAMESPACE = mydatabase.myschema DEFAULT_ROLE = myrole DEFAULT_SECONDARY_ROLES = ('ALL');
      ```

  Python:
  :   Copy code

      ```
      user_parameters = root.users["janesmith"].fetch()
      user_parameters.default_warehouse = "mywarehouse"
      user_parameters.default_namespace = "mydatabase.myschema"
      user_parameters.default_role = "myrole"
      user_parameters.default_secondary_roles = "ALL"
      root.users["janesmith"].create_or_alter(user_parameters)
      ```

  Snowsight:
  :   Note

      You cannot set default secondary roles for a user using Snowsight.

      1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
      2. In the navigation menu, select **Governance & security** » **Users & roles**.
      3. Locate the user that you want to edit and select [![More options](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png) » **Edit**.
      4. Open the **Advanced User Options** and enter values in the relevant fields.
      5. Select **Save User**.

## Viewing users

You can view information about users using the following interfaces.

### Using SQL

Use the [DESCRIBE USER](/sql-reference/sql/desc-user) or [SHOW USERS](/sql-reference/sql/show-users) command to view information about one or more users.

For example:

Copy code

```
DESC USER janesmith;
```

### Using Python

Use the [UserResource.fetch](/developer-guide/snowflake-python-api/reference/latest/_autosummary/snowflake.core.user.UserResource#snowflake.core.user.UserResource.fetch)
Python API to get information about a user.

For example:

Copy code

```
my_user = root.users["janesmith"].fetch()
print(my_user.to_dict())
```

Use the [UserCollection.iter](/developer-guide/snowflake-python-api/reference/latest/_autosummary/snowflake.core.user.UserCollection#snowflake.core.user.UserCollection.iter)
Python API to list users in an account.

For example:

Copy code

```
users = root.users.iter(like="jane%")
for user in users:
  print(user.name)
```

### Using Snowsight

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Governance & security** » **Users & roles**.
3. Locate the user for which you want to view more details.

   You can review the display name, status, last login time, owning role, and whether or not the user has multi-factor authentication (MFA)
   set up. If the user has a comment, you can hover over the [![Comment icon](/static/images/snowsight/snowsight-admin-user-comment.png)](/static/images/snowsight/snowsight-admin-user-comment.png).
4. Optionally select the user to see more details, such as their default settings, roles that have privileges granted on the user, and
   the roles granted to the user.

## Dropping a user

Dropping a user removes the user credentials from Snowflake.

Important

When you drop a user, the folders, worksheets, and dashboards owned by that user become inaccessible and **do not** transfer to another user
unless sharing is enabled.

Share recipients with [View, View + Run, and Edit permissions](/user-guide/ui-snowsight-worksheets#label-sharing-worksheets-and-folders)
will retain their assigned permissions and can still access the shared folders, worksheets, and dashboards. However, only users with Edit
permissions can modify or delete the shared folders, worksheets, and dashboards. If you don’t give Edit permissions to at least one other
user before you drop the owner, that owner’s folders, worksheets, and dashboards cannot be deleted.

If a dropped user’s worksheets do not have sharing enabled, an administrator can [recover up to 500 worksheets owned by the user](/user-guide/ui-snowsight-worksheets#label-snowsight-worksheets-recover).

Caution

Any worksheets in the Classic Console will be permanently deleted, and dashboards will be inaccessible if they were not previously shared
with another user.

Objects created by the user, such as tables or views, are not dropped because they are owned by the user’s active role when the objects
were created. Another user assigned the same role or a higher role in the [role hierarchy](/user-guide/security-access-control-considerations) can manage the objects or transfer ownership to another role.

### Using Snowsight

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Governance & security** » **Users & roles**.
3. Locate the user that you want to disable and select [![More options](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png) » **Drop**.
4. In the confirmation dialog that opens, select **Drop User**.

### Using SQL

Use the [DROP USER](/sql-reference/sql/drop-user) command to drop a user.

Copy code

```
DROP USER janesmith;
```

### Using Python

Use the [UserResource.drop](/developer-guide/snowflake-python-api/reference/latest/_autosummary/snowflake.core.user.UserResource#snowflake.core.user.UserResource.drop)
Python API to drop a user.

Copy code

```
root.users["janesmith"].drop()
```
