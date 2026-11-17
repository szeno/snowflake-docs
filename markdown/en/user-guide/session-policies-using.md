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

   To replace a session policy that is already set for an account or user, specify `FORCE` in the statement that sets the new session
   policy. The existing policy stays in place until the new one replaces it, so the account or user is never without a policy during the
   transition. For example:

   Copy code

   ```
   ALTER ACCOUNT SET SESSION POLICY mydb.policies.session_policy_prod_2 FORCE;
   ```

   Alternatively, unset the session policy first and then set the new session policy for the account or user. No policy is set between
   the two statements. For example:

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

## Example journeys

The following journeys show how common goals combine the facts documented elsewhere. They are examples, not the only supported paths. You
can combine the same settings in other ways, using the linked pages for the details. The SQL uses placeholders such as `<minutes>` for
values, so look up the valid range and defaults in the linked pages before you choose one.

### Log human users out of Snowsight after a period of inactivity

**Goal:** Require human users to authenticate again to Snowsight after they have been idle for a different period of time than the default.

**Check first:**

- Confirm that your role has the privileges to create and apply a session policy. See [Session policy privileges](/user-guide/session-policies-managing#session-policy-privileges).
- Find out whether a session policy is already applied at the level you plan to use, and which policy takes precedence for a user. See
  [Precedence](/user-guide/session-policies-managing#precedence) and [Auditing session policies](/user-guide/session-policies-managing#auditing-session-policies).
- Choose the idle timeout. The setting for Snowsight is described in [Session policies](/user-guide/session-policies#label-session-policy-policies).

**Steps:**

1. Create a policy that sets only the Snowsight idle timeout:

   Copy code

   ```
   CREATE SESSION POLICY mydb.policies.snowsight_idle_policy
     SESSION_UI_IDLE_TIMEOUT_MINS = <minutes>
     COMMENT = 'Snowsight idle timeout for human users';
   ```
2. Apply it to all human users. For which users this covers, see [Applying a session policy](/user-guide/session-policies-managing#label-session-policy-applying).

   Copy code

   ```
   ALTER ACCOUNT SET SESSION POLICY mydb.policies.snowsight_idle_policy FOR ALL PERSON USERS;
   ```

   If a policy is already set at this level, see [Replacing an applied policy](/user-guide/session-policies-managing#replacing-an-applied-policy).

**Verify:**

Copy code

```
DESC SESSION POLICY mydb.policies.snowsight_idle_policy;

SELECT *
FROM TABLE(
  mydb.INFORMATION_SCHEMA.POLICY_REFERENCES(
    POLICY_NAME => 'mydb.policies.snowsight_idle_policy'
  ));
```

For when a change takes effect for open sessions, see [Secondary roles in a session policy](/user-guide/session-policies#label-session-policy-secondary-roles-concepts). For
what happens when a Snowsight session expires, see
[Snowsight session expiration and logout behavior](/user-guide/session-policies#snowsight-session-expiration-and-logout-behavior).

**Undo:**

Copy code

```
ALTER ACCOUNT UNSET SESSION POLICY FOR ALL PERSON USERS;
```

### Set session limits for drivers, the CLI, and service users

**Goal:** Limit the idle time and total lifespan of sessions opened through drivers, the CLI, and service users.

**Check first:**

- Which interfaces the session timeouts cover. See [Snowflake sessions](/user-guide/session-policies#snowflake-sessions).
- Which settings apply to service users. See [Session policies](/user-guide/session-policies#label-session-policy-policies).
- Whether a service user already has a policy of its own, which takes precedence over the account-level policy for its type. See
  [Precedence](/user-guide/session-policies-managing#precedence).

**Steps:**

1. Create a policy with the programmatic idle timeout and maximum lifespan:

   Copy code

   ```
   CREATE SESSION POLICY mydb.policies.programmatic_limits_policy
     SESSION_IDLE_TIMEOUT_MINS = <minutes>
     SESSION_MAX_LIFESPAN_MINS = <minutes>
     COMMENT = 'Session limits for programmatic clients';
   ```
2. Apply it to all service users, or use `FOR ALL PERSON USERS` for human users who connect through drivers and the CLI:

   Copy code

   ```
   ALTER ACCOUNT SET SESSION POLICY mydb.policies.programmatic_limits_policy FOR ALL SERVICE USERS;
   ```

Warning

A maximum lifespan ends the session when it is reached, regardless of activity, even when a client keeps the session alive. When a
session closes, its running queries and jobs are terminated. Before you set `SESSION_MAX_LIFESPAN_MINS`, check that your longest
running jobs finish within it. See [Session policy considerations](/user-guide/session-policies#considerations) and
[Snowsight session expiration and logout behavior](/user-guide/session-policies#snowsight-session-expiration-and-logout-behavior).

**Verify:**

Copy code

```
DESC SESSION POLICY mydb.policies.programmatic_limits_policy;
```

**Undo:**

Copy code

```
ALTER ACCOUNT UNSET SESSION POLICY FOR ALL SERVICE USERS;
```

### Limit what an AI agent can do with a restricted session scope

**Goal:** Set a ceiling on what an agent can do in a session. Choose a predefined scope, or an RSS object.

**Check first:**

- What the predefined scopes allow and don’t allow. See [Predefined scopes](/user-guide/restricted-session-scope#predefined-scopes).
- If you need a custom scope, the privileges required to create an RSS object and its structure. See
  [RSS YAML structure](/user-guide/restricted-session-scope#label-agent-rss-yaml-structure) and
  [Create an RSS object and reference it](/user-guide/restricted-session-scope#label-agent-rss-create-object).

**Steps:**

1. Create a session policy that references the scope.

   Use a predefined scope:

   Copy code

   ```
   CREATE SESSION POLICY mydb.governance.agent_policy
     AGENT_RESTRICTED_SESSION_SCOPE = '<predefined_scope>';
   ```

   Or create an RSS object as described in [Create an RSS object and reference it](/user-guide/restricted-session-scope#label-agent-rss-create-object), and reference it by
   fully qualified name:

   Copy code

   ```
   CREATE SESSION POLICY mydb.governance.agent_policy
     AGENT_RESTRICTED_SESSION_SCOPE = '<rss_object_name>';
   ```
2. Apply the policy to the account or to a user. See [Attach the session policy to the account or a user](/user-guide/restricted-session-scope#attach-the-session-policy-to-the-account-or-a-user).

**Verify:** From a session where an agent is active, check the active scope:

Copy code

```
SELECT SYS_CONTEXT('SNOWFLAKE$SESSION', 'ACTIVE_RESTRICTED_SESSION_SCOPES');
```

For when the scope applies, see [Restricted Session Scope for agents](/user-guide/session-policies#restricted-session-scope-for-agents). For when a change to an RSS object takes
effect, see [RSS YAML structure](/user-guide/restricted-session-scope#label-agent-rss-yaml-structure).

**Undo:**

Copy code

```
ALTER ACCOUNT UNSET SESSION POLICY;
```

### Change a policy that is already applied

**Goal:** Change settings on a session policy that users already have.

**Check first:**

- Who the policy reaches. See [Auditing session policies](/user-guide/session-policies-managing#auditing-session-policies).
- That your role owns the policy. See [Session policy privileges](/user-guide/session-policies-managing#session-policy-privileges).
- When a change takes effect for sessions that are already open. See [Secondary roles in a session policy](/user-guide/session-policies#label-session-policy-secondary-roles-concepts).

**Steps:**

1. Find out who the policy reaches:

   Copy code

   ```
   SELECT *
   FROM TABLE(
     mydb.INFORMATION_SCHEMA.POLICY_REFERENCES(
       POLICY_NAME => 'mydb.policies.session_policy_prod_1'
     ));
   ```
2. Alter only the settings you mean to change. For the settings you can set, see [ALTER SESSION POLICY](/sql-reference/sql/alter-session-policy):

   Copy code

   ```
   ALTER SESSION POLICY mydb.policies.session_policy_prod_1
     SET SESSION_IDLE_TIMEOUT_MINS = <minutes>;
   ```

**Verify:** Describe the policy and compare it with what you recorded before the change:

Copy code

```
DESC SESSION POLICY mydb.policies.session_policy_prod_1;
```

**Undo:** Set the changed setting back to the value you recorded before the change.

### Apply a policy to a policy scope, or replace the policy already there

**Goal:** Apply a policy to the account, to all users of one type, or to one user. If a policy is already set at that level, replace it.

**Check first:**

- The three levels, and which clause selects each. See [Applying a session policy](/user-guide/session-policies-managing#label-session-policy-applying).
- Which policy takes precedence when more than one applies. See [Precedence](/user-guide/session-policies-managing#precedence).
- Which policy is already set. See [Auditing session policies](/user-guide/session-policies-managing#auditing-session-policies).

**Steps:**

1. Apply the policy at the level you chose, here to all service users:

   Copy code

   ```
   ALTER ACCOUNT SET SESSION POLICY mydb.policies.programmatic_limits_policy FOR ALL SERVICE USERS;
   ```
2. If a policy is already set at that level, use `FORCE` to replace it. The existing policy stays in place until the new one replaces it, so
   the level is never without a policy. What `FORCE` replaces is described in
   [Replacing an applied policy](/user-guide/session-policies-managing#replacing-an-applied-policy). Alternatively, unset the existing policy
   at that level first and then set the new one. No policy is set at that level between the two statements.

   Copy code

   ```
   ALTER ACCOUNT SET SESSION POLICY mydb.policies.programmatic_limits_policy FOR ALL SERVICE USERS FORCE;
   ```

**Verify:** List the users the policy reaches, as in [Auditing session policies](/user-guide/session-policies-managing#auditing-session-policies).

**Undo:** Unset the policy at that level, and set the previous policy again if you replaced one:

Copy code

```
ALTER ACCOUNT UNSET SESSION POLICY FOR ALL SERVICE USERS;
```
