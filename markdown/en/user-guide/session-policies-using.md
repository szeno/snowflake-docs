# Using session policies

This topic provides examples on how to use session policies.

## Standard session policy

The following steps are a representative guide to creating a session policy and setting the session policy on an account or user.

These steps assume a centralized management approach in which a custom role named `policy_admin` owns the session policy (i.e. has the
OWNERSHIP privilege on the session policy) and is responsible for setting the session policy on an account or user (i.e. has the APPLY
SESSION POLICY on ACCOUNT privilege or the APPLY SESSION POLICY ON USER privilege).

Note

To set a policy on an account, the `policy_admin` custom role must have the following permissions:

- USAGE on the database and schema that contain the session policy.
- CREATE SESSION POLICY on the schema that contains the session policy.

Follow these steps to implement a session policy.

1. Create a custom role that allows users to create and manage session policies. Throughout this example custom role is `policy_admin`,
   although the role could have any appropriate name.

   If the custom role already exists, continue to the next step.

   Otherwise, create the `policy_admin` custom role:

   Copy code

   ```
   USE ROLE USERADMIN;

   CREATE ROLE policy_admin;
   ```
2. Grant privileges to the custom role.

   If the `policy_admin` custom role does not already have the following privileges, grant these privileges as shown below:

   - USAGE on the database and schema that will contain the session policy.
   - CREATE SESSION POLICY on the schema that will contain the session policy.
   - APPLY SESSION POLICY on the account.
   - APPLY SESSION POLICY on each user, if you plan to set session policies at the user level.

   Copy code

   ```
   USE ROLE SECURITYADMIN;

   GRANT USAGE ON DATABASE mydb TO ROLE policy_admin;

   GRANT USAGE, CREATE SESSION POLICY ON SCHEMA mydb.policies TO ROLE policy_admin;

   GRANT APPLY SESSION POLICY ON ACCOUNT TO ROLE policy_admin;
   ```

   If associating a session policy with an individual user:

   Copy code

   ```
   GRANT APPLY SESSION POLICY ON USER jsmith TO ROLE policy_admin;
   ```

   For more information, see [Summary of commands, operations, and privileges](/user-guide/session-policies-managing#label-session-policy-privilege-ddl-summary).
3. Create a new session policy.

   Copy code

   ```
   USE ROLE policy_admin;

   CREATE SESSION POLICY mydb.policies.session_policy_prod_1
     SESSION_IDLE_TIMEOUT_MINS = 30
     SESSION_UI_IDLE_TIMEOUT_MINS = 30
     SESSION_MAX_LIFESPAN_MINS = 480
     SESSION_UI_MAX_LIFESPAN_MINS = 480
     COMMENT = 'Session policy for the prod_1 environment';
   ```

   For more information, see [CREATE SESSION POLICY](/sql-reference/sql/create-session-policy).
4. Set the session policy on the account with the [ALTER ACCOUNT](/sql-reference/sql/alter-account) command, or a user with the
   [ALTER USER](/sql-reference/sql/alter-user) command.

   Copy code

   ```
   USE ROLE policy_admin;

   ALTER ACCOUNT SET SESSION POLICY mydb.policies.session_policy_prod_1;

   ALTER USER jsmith SET SESSION POLICY my_database.my_schema.session_policy_prod_1;
   ```

   Important

   To replace a session policy that is already set for an account or user, unset the session policy first and then set the new session
   policy for the account or user. For example:

   Copy code

   ```
   ALTER ACCOUNT UNSET session policy;

   ALTER ACCOUNT SET SESSION POLICY mydb.policies.session_policy_prod_2;
   ```

## Specifying secondary roles in a session policy

The following sections detail how to specify secondary roles in a session policy:

- [Set the property in a session policy](#label-session-policy-secondary-roles-set)
- [Unset the property in a session policy](#label-session-policy-secondary-roles-unset)
- [Disallow secondary roles for all users in the account](#label-session-policy-no-sec-roles-all-users)
- [Disallow secondary roles for a specific user](#label-session-policies-no-sec-roles-user)
- [Allow a user to use specific secondary roles](#label-session-policies-specify-sec-roles-user)

For more information about secondary roles in a session policy, see [Secondary roles in a session policy](/user-guide/session-policies#label-session-policy-secondary-roles-concepts)

### Set the property in a session policy

The security administrator can create a new session policy or modify an existing session policy to set the
`ALLOWED_SECONDARY_ROLES` property. For example:

- Create a new session policy to allow all secondary roles:

  Copy code

  ```
  CREATE OR REPLACE SESSION POLICY prod_env_session_policy
    SESSION_IDLE_TIMEOUT_MINS = 30
    SESSION_UI_IDLE_TIMEOUT_MINS = 30
    SESSION_MAX_LIFESPAN_MINS = 480
    SESSION_UI_MAX_LIFESPAN_MINS = 480
    ALLOWED_SECONDARY_ROLES = ('ALL')
    COMMENT = 'session policy for use in the prod_1 environment';
  ```
- Modify an existing session policy to disallow secondary roles:

  Copy code

  ```
  ALTER SESSION POLICY prod_env_session_policy
    SET ALLOWED_SECONDARY_ROLES = ();
  ```

  The [ALTER SESSION POLICY](/sql-reference/sql/alter-session-policy) command can modify the property value if the property is already set.

For details about the syntax, see the [Managing session policies](/user-guide/session-policies-managing).

You can use the [DESCRIBE SESSION POLICY](/sql-reference/sql/desc-session-policy) command or call the [GET\_DDL](/sql-reference/functions/get_ddl) function to view
the value of the `ALLOWED_SECONDARY_ROLES` property.

### Unset the property in a session policy

You can use an ALTER SESSION POLICY command to unset secondary roles in the session policy:

Copy code

```
ALTER SESSION POLICY prod_env_session_policy
  UNSET ALLOWED_SECONDARY_ROLES;
```

### Disallow secondary roles for all users in the account

To prevent all users in an account from using secondary roles, set a session policy on the account that disallows secondary roles for the
session. For example:

1. Modify a session policy to disallow secondary roles:

   Copy code

   ```
   ALTER SESSION POLICY prod_env_session_policy SET ALLOWED_SECONDARY_ROLES = ();
   ```
2. Assign the session policy to the account:

   Copy code

   ```
   ALTER ACCOUNT SET SESSION POLICY prod_env_session_policy;
   ```

If a user tries to activate secondary roles with a USE SECONDARY ROLES command, such as `USE SECONDARY ROLES analyst;`, the following
error message occurs:

```
SQL execution error: USE SECONDARY ROLES '[ANALYST]' not allowed as per session policy.
```

### Disallow secondary roles for a specific user

To disallow a specific user from using secondary roles, set a session policy on the user that disallows secondary roles for the session.
For example, if that session policy already exists:

Copy code

```
ALTER USER jsmith SET SESSION POLICY prod_env_session_policy;
```

If there is a session policy that is set on the account, the session policy assigned to the user overrides the session policy on the
account.

If the user runs a USE SECONDARY ROLES command to activate secondary roles, such as `USE SECONDARY ROLES (ANALYST, DATA_SCIENTIST);`
they will see the following error message:

```
SQL execution error: USE SECONDARY ROLES '[ANALYST, DATA_SCIENTIST]' not allowed as per session policy.
```

### Allow a user to use specific secondary roles

To enable a user to use specific secondary roles, do the following:

1. Create a session policy that specifies the secondary roles a user can use:

   Copy code

   ```
   CREATE OR REPLACE SESSION POLICY prod_env_session_policy
     SESSION_IDLE_TIMEOUT_MINS = 30
     SESSION_UI_IDLE_TIMEOUT_MINS = 30
     SESSION_MAX_LIFESPAN_MINS = 480
     SESSION_UI_MAX_LIFESPAN_MINS = 480
     ALLOWED_SECONDARY_ROLES = (DATA_SCIENTIST, ANALYST)
     COMMENT = 'session policy for user secondary roles data_scientist and analyst';
   ```
2. Set the session policy on the user:

   Copy code

   ```
   ALTER USER bsmith SET SESSION POLICY prod_env_session_policy;
   ```

The user can activate the secondary roles as needed with a USE SECONDARY ROLES command. For example:

- Activate all secondary roles:

  Copy code

  ```
  USE SECONDARY ROLES ALL;
  ```
- Activate `DATA_SCIENTIST` as a secondary role:

  Copy code

  ```
  USE SECONDARY ROLES DATA_SCIENTIST;
  ```

For details about the syntax, see [USE SECONDARY ROLES](/sql-reference/sql/use-secondary-roles).

## Replicate the session policy to a target account

You can replicate a session policy and its references, which are the assignments to a user or the account, from the source account to the
target account using database replication and account replication. For details, see:

- [Account replication](/user-guide/account-replication-considerations#label-account-replication-considerations-security-policies).
- [Database replication](/user-guide/database-replication-considerations#label-database-replication-considerations-masking-row-policies).

For details about replicating a session policy that specifies secondary roles, see
[replicate session policies with secondary roles](/user-guide/account-replication-considerations#label-account-replication-session-policy-secondary-roles).
