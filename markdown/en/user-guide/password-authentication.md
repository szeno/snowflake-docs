# Working with passwords

This topic describes how an administrator can configure password requirements and reset user passwords.

## Password policies

A password policy specifies the requirements that must be met to create and reset a password to authenticate to Snowflake.

Snowflake provides two options for password policies:

- A built-in password policy to facilitate the initial user provisioning process.
- A schema-level password policy object that can be set at the level of the Snowflake account, an individual user, or both depending on
  the use cases and needs of the user administrator.

### Best practices for password policies and passwords

Snowflake recommends the following best practices regarding passwords and password policies:

Create and enforce the custom password policy
:   The password policy object is enforced once the password policy is set on an account or user.

    Set these properties to values that meet your internal security needs. For details, see [Step 4: Create a password policy](#label-password-policy-create)
    (in this topic):

    - `PASSWORD_HISTORY` to ensure users cannot reuse passwords too frequently and to help prevent brute force attacks to determine the
      password for a user.
    - `PASSWORD_MIN_AGE_DAYS` to require the user to use the new password. A value of 0 is not recommended because the user can change the
      password to exhaust the password history and reuse the original password value too soon.

    To require the user to change their password to meet the password policy on their initial or next login to Snowflake, set the
    `MUST_CHANGE_PASSWORD` property on the user to `TRUE` using an [ALTER USER](/sql-reference/sql/alter-user) command.

    For details, see [Step 6: Require a password change](#label-password-policy-require-change) (in this topic).

Require strong passwords
:   Define an account-level password policy to require strong passwords.

    A strong password has at least 14 characters and includes a combination of uppercase and lowercase letters, special characters
    (for example, `!` and `*`), and numbers.

MFA
:   Use [multi-factor authentication (MFA)](/user-guide/security-mfa) for additional security.

Using SCIM
:   You can set a password for the user to access Snowflake in a SCIM API request. SCIM administrators and user administrators should choose
    to manage the user password to access Snowflake in either your identity provider or using a password policy in Snowflake.

    Currently, users provisioned to Snowflake with SCIM are required to have their password meet the
    [default Snowflake password policy](#label-snowflake-password-policy). This requirement can be bypassed if you choose to use this
    password policy feature.

    To bypass the default password policy requirement, follow the instructions in the [Using Password Policies](#using-password-policies) section (in this topic).

Monitoring passwords
:   To monitor passwords:

    - Query the Snowflake Account Usage [USERS](/sql-reference/account-usage/users) view to determine whether the `HAS_PASSWORD`
      column value returns `TRUE` for a given user.
    - Query the Snowflake Account Usage [LOGIN\_HISTORY](/sql-reference/account-usage/login_history) view and evaluate the
      `FIRST_AUTHENTICATION_FACTOR` column. If a user does not require a password to access Snowflake, execute an
      [ALTER USER](/sql-reference/sql/alter-user) command to set the `password` property to NULL.

### Setting an initial password for new users

During the initial user creation, it is possible to set a weak password for the user that does not meet the minimum requirements
of the password policy that is in effect. This gives administrators the option to use generic passwords for the user during the
creation process. If this pathway is chosen, Snowflake strongly recommends setting the `MUST_CHANGE_PASSWORD` property to
`TRUE` to require users to change their password on their next login, including the initial login. When a user resets
their password, they must choose one that conforms to the password policy in effect, whether it is a Snowflake-provided policy or a custom
one.

Additionally, Snowflake allows creating users without an initial password to support business processes in which new users are not allowed
to log into the system. If this occurs, the user’s `PASSWORD` property value will be `NULL`. However, as a general rule,
Snowflake expects that users are created with initial passwords.

### Snowflake-provided password policy

A password can be any case-sensitive string up to 256 characters, including blank spaces and special (that is, non-alphanumeric) characters,
such as exclamation points (`!`), percent signs (`%`), and asterisks (`*`).

In the context of resetting an existing password (for example, change `'test12345'` to `'q@-*DaC2yjZoq3Re4JYX'`), Snowflake
enforces the following password policy as a minimum requirement while using the [ALTER USER](/sql-reference/sql/alter-user) command and the
web interface:

- Must be at least 14 characters long.
- Must contain at least 1 digit.
- Must contain at least 1 uppercase letter and 1 lowercase letter.

Snowflake strongly recommends the following guidelines for creating the strongest passwords possible:

- Create a unique password for Snowflake (that is, do not reuse passwords from other systems or accounts).
- Include multiple, random mixed-case letters, numbers, and special characters, including blank spaces.
- Do not use easily-guessed common passwords, names, numbers, or dates.

### Custom password policy for the account and users

The custom password policy is a schema-level object that specifies the requirements that must be met to create and reset a password to
authenticate to Snowflake, including the number of attempts to enter the password successfully and the number of minutes before a password
can be retried (that is, the “lockout” time).

The password policy requirements for a password include upper or lowercase letters, special characters, numbers, and password length to
meet security requirements for users and clients to authenticate to Snowflake. Password policies that require strong passwords help to meet
security guidelines and regulations.

Snowflake supports setting a password policy for your Snowflake account and for individual users. Only one password policy
can be set at any given time for your Snowflake account or a user. If a password policy exists for the Snowflake account and another
password policy is set for a user in the same Snowflake account, the user-level password policy takes precedence over the account-level
password policy.

The password policy applies to new passwords that are set in your Snowflake account. To ensure that users with existing passwords meet the
password policy requirements, require users to change their password during their next login to Snowflake as shown in
[Step 6: Require a password change](#label-password-policy-require-change) (in this topic).

Note

Most password policy property changes take effect the next time a user changes their password. For example, if you change the
`PASSWORD_MAX_LENGTH` property from `10` to `16` to require the user to use a longer password then the user must
comply with the password policy change whenever they change their password. You can set the user property `MUST_CHANGE_PASSWORD`
to `TRUE` with an [ALTER USER](/sql-reference/sql/alter-user) statement to require the user to change their password on their next login
to Snowflake.

However, some password policy property changes take effect during the next login because Snowflake does not force the user to change
their password in their current session:

- `PASSWORD_MAX_AGE_DAYS = integer`
- `PASSWORD_MAX_RETRIES = integer`
- `PASSWORD_LOCKOUT_TIME_MINS = integer`

Any changes to these properties do not affect the current session. For example, a change to the value of the
`PASSWORD_MAX_AGE_DAYS` property does not cause the user’s current password to expire. However, during the next login to
Snowflake, the user must change their password.

#### Considerations

- [Future grants](/sql-reference/sql/grant-privilege#label-grant-privilege-schema-future-grants) of privileges on password policies are not supported.

  As a workaround, grant the APPLY PASSWORD POLICY privilege to a custom role to allow that role to apply password policies on the user or
  the Snowflake account.
- The password policy can be managed with SQL using [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql) or a
  supported [driver or connector](/guides-overview-connecting), or using Snowsight.
- When you reset or change a password, Snowflake evaluates the password policy to ensure that the newly created password matches the
  password policy requirements.
- Tracking password policy usage:

  - Query the Account Usage [PASSWORD\_POLICIES](/sql-reference/account-usage/password_policies) view to return a row for each
    password policy in your Snowflake account.
  - Use the Information Schema table function [POLICY\_REFERENCES](/sql-reference/functions/policy_references) to return a row for each user that is
    assigned to the specified password policy and a row for the password policy assigned to the Snowflake account.

    Currently, only the following syntax is supported for password policies:

    Copy code

    ```
    POLICY_REFERENCES( POLICY_NAME => '<password_policy_name>' )
    ```

    Where `password_policy_name` is the fully qualified name of the password policy.

    For example, execute the following query to return a row for each user that is assigned the password policy named
    `password_policy_prod_1`, which is stored in the database named `my_db` and the schema named `my_schema`:

    Copy code

    ```
    SELECT *
    FROM TABLE(
        my_db.information_schema.policy_references(
    POLICY_NAME => 'my_db.my_schema.password_policy_prod_1'
      )
    );
    ```

### Access control for password policies

The following access control privileges allow users to work with password policies:

| Privilege | Object type | Usage |
| --- | --- | --- |
| CREATE PASSWORD POLICY | Schema | Enables creating a new password policy. |
| APPLY PASSWORD POLICY | Account, User | Enables applying a password policy at the account or user level. |
| OWNERSHIP | Password policy | Grants full control over the password policy. Required to alter most properties of a password policy. |

Expand

Show lessSee more

The following table summarizes the relationship between password policy DDL operations and their necessary privileges.

| Operation | Privilege required |
| --- | --- |
| Create password policy | A role with the CREATE PASSWORD POLICY privilege on the schema to store the password policy. |
| Alter password policy | A role with the OWNERSHIP privilege on the password policy. |
| Drop password policy | A role with the OWNERSHIP privilege on the password policy. |
| Describe password policy | A role with the OWNERSHIP privilege on the password policy or   the APPLY PASSWORD POLICY privilege on the account. |
| Show password policies | A role with the OWNERSHIP privilege on the password policy or   the APPLY PASSWORD POLICY privilege on the account. |
| Set & unset password policy | A role with the APPLY PASSWORD POLICY privilege on the account or the user. |

Expand

Show lessSee more

Note

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

### DDL commands

Snowflake provides the following DDL commands to manage password policy objects:

- [CREATE PASSWORD POLICY](/sql-reference/sql/create-password-policy)
- [ALTER PASSWORD POLICY](/sql-reference/sql/alter-password-policy)
- [DROP PASSWORD POLICY](/sql-reference/sql/drop-password-policy)
- [SHOW PASSWORD POLICIES](/sql-reference/sql/show-password-policies)
- [DESCRIBE PASSWORD POLICY](/sql-reference/sql/desc-password-policy)

### Using password policies

The following steps are a representative guide to define and set a password policy in Snowflake.

These steps assume a centralized management approach in which a custom role named `policy_admin` owns the password policy (that is, has the
OWNERSHIP privilege on the password policy) and is responsible for setting the password policy on an account or user
(that is, has the global APPLY PASSWORD POLICY privilege, as shown in [step 2](#label-pwd-policy-grant-privileges)).

Note

To set a policy on an account, the `policy_admin` custom role must also have the USAGE privilege on the database and schema that
contain the password policy.

For more information, see: [Access control privileges](/user-guide/security-access-control-privileges)

#### Step 1: Create the custom role

Create a custom role that allows creating and managing password policies. Throughout this topic, the example custom role is named
`policy_admin`, although the role could have any appropriate name.

If the custom role already exists, continue to the next step.

Otherwise, create the `policy_admin` custom role.

> Copy code
>
> ```
> USE ROLE USERADMIN;
>
> CREATE ROLE policy_admin;
> ```

#### Step 2: Grant privileges to the custom role

If the `policy_admin` custom role does not already have the following privileges, grant these privileges as shown below:

- USAGE on the database and schema that will contain the password policy.
- CREATE PASSWORD POLICY on the schema that will store the password policy.
- APPLY PASSWORD POLICY on the account.

Copy code

```
USE ROLE SECURITYADMIN;

GRANT USAGE ON DATABASE security TO ROLE policy_admin;

GRANT USAGE ON SCHEMA security.policies TO ROLE policy_admin;

GRANT CREATE PASSWORD POLICY ON SCHEMA security.policies TO ROLE policy_admin;

GRANT APPLY PASSWORD POLICY ON ACCOUNT TO ROLE policy_admin;
```

If you decide to set a password policy on a user, grant the APPLY PASSWORD POLICY privilege on the user. For example, if the username is
`JSMITH`, execute the following command.

> Copy code
>
> ```
> GRANT APPLY PASSWORD POLICY ON USER jsmith TO ROLE policy_admin;
> ```

For more information, see [Access control for password policies](#label-password-policy-privilege-ddl-summary).

#### Step 3: Grant the custom role to a user

Grant the `policy_admin` custom role to the users responsible for managing password policies.

Copy code

```
USE ROLE SECURITYADMIN;
GRANT ROLE policy_admin TO USER jsmith;
```

For more information, see [Configuring access control](/user-guide/security-access-control-configure)

#### Step 4: Create a password policy

Using the `policy_admin` custom role, create a password policy named `password_policy_prod_1`. For more information, see
[CREATE PASSWORD POLICY](/sql-reference/sql/create-password-policy).

> Copy code
>
> ```
> USE ROLE policy_admin;
>
> USE SCHEMA security.policies;
>
> CREATE PASSWORD POLICY PASSWORD_POLICY_PROD_1
>     PASSWORD_MIN_LENGTH = 14
>     PASSWORD_MAX_LENGTH = 24
>     PASSWORD_MIN_UPPER_CASE_CHARS = 2
>     PASSWORD_MIN_LOWER_CASE_CHARS = 2
>     PASSWORD_MIN_NUMERIC_CHARS = 2
>     PASSWORD_MIN_SPECIAL_CHARS = 2
>     PASSWORD_MIN_AGE_DAYS = 1
>     PASSWORD_MAX_AGE_DAYS = 999
>     PASSWORD_MAX_RETRIES = 3
>     PASSWORD_LOCKOUT_TIME_MINS = 30
>     PASSWORD_HISTORY = 5
>     COMMENT = 'production account password policy';
> ```
>
> Note
>
> The property `PASSWORD_MAX_AGE_DAYS` is set to the largest value, 999. Choose a value that aligns with your internal
> guidelines. For details, see [CREATE PASSWORD POLICY](/sql-reference/sql/create-password-policy).

#### Step 5: Set the password policy on the account or an individual user

Set the policy on an account with the [ALTER ACCOUNT](/sql-reference/sql/alter-account) command:

> Copy code
>
> ```
> ALTER ACCOUNT SET PASSWORD POLICY security.policies.password_policy_prod_1;
> ```

If you decide to create an additional password policy for one or more users, set the user-level password policy on a user with an
[ALTER USER](/sql-reference/sql/alter-user) command:

> Copy code
>
> ```
> ALTER USER jsmith SET PASSWORD POLICY security.policies.password_policy_user;
> ```

Important

To replace a password policy that is already set for an account or user, unset the password policy first and then set the new password
policy for the account or user. For example:

> Copy code
>
> ```
> ALTER ACCOUNT UNSET PASSWORD POLICY;
>
> ALTER ACCOUNT SET PASSWORD POLICY security.policies.password_policy_prod_2;
> ```

#### Step 6: Require a password change

Set the `MUST_CHANGE_PASSWORD` property to `TRUE` for individual users using an [ALTER USER](/sql-reference/sql/alter-user) statement to
require the users to change their password to meet the password policy on their next login to Snowflake.

> Copy code
>
> ```
> ALTER USER JSMITH SET MUST_CHANGE_PASSWORD = true;
> ```

## Resetting the password for a user

Administrators can change a user’s password through the following interfaces.

### Snowsight

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Governance & security** » **Users & roles**.
3. Locate the user whose password you want to change and select [![More options](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png) » **Reset Password**.
4. Enter a new password for the user and confirm the password.
5. Select **Update**.

### Using SQL

Use the [ALTER USER](/sql-reference/sql/alter-user) command to input a user’s password. For example:

> Copy code
>
> ```
> ALTER USER janesmith SET PASSWORD = 'H8MZRqa8gEe/kvHzvJ+Giq94DuCYoQXmfbb$Xnt' MUST_CHANGE_PASSWORD = TRUE;
> ```

Alternatively, use the ALTER USER … RESET PASSWORD syntax to generate a URL to share with the user. The URL opens a web page on which the user can enter the new password. For example:

> Copy code
>
> ```
> ALTER USER janesmith RESET PASSWORD;
> ```
>
> Note
>
> - The generated URL is valid for one use only and expires after 12 hours.
> - Executing the ALTER USER … RESET PASSWORD statement does not invalidate the current password. The user can continue to use the old password until the new password is set.

### Using Python

The [UserResource.create\_or\_alter](/developer-guide/snowflake-python-api/reference/latest/_autosummary/snowflake.core.user.UserResource#snowflake.core.user.UserResource.create_or_alter)
method in the Snowflake Python APIs currently does not support changing the `password` for an existing user. You can only set the password
using this method when creating a new user.

## Resetting the password for an administrator

An account administrator (that is, a user with the ACCOUNTADMIN role) can reset their own password using the procedure described in
[Resetting the Password for a User](#resetting-the-password-for-a-user).

If an account administrator is locked out of their account, a different user with the ACCOUNTADMIN role
can reset the password for the locked-out administrator. In the event that the administrator is locked out and there is no other
administrator to change the password, contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support) to reset the password.
