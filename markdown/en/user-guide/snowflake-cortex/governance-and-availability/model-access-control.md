# Model access control

Snowflake Cortex provides two mechanisms to enforce access to models:

- [Role-based access control (RBAC)](#label-cortex-llm-rbac) (recommended, fine-grained control)
- [Account-level allowlist parameter](#label-cortex-llm-allowlist) (legacy, planned for deprecation)

Use the account-level allowlist for account-wide defaults and RBAC for per-role control. You can also [use both mechanisms together](#label-cortex-llm-rbac-with-account-allowlist): access is granted if either mechanism permits it. Snowflake recommends migrating to RBAC exclusively.

This page covers model access only. To control which roles can call Cortex AI Functions, see [Cortex LLM privileges](/user-guide/snowflake-cortex/aisql-privileges-and-access#label-cortex-llm-privileges).

Note

The ACCOUNTADMIN role always has access to all models on the account, regardless of the CORTEX\_MODELS\_ALLOWLIST parameter or model RBAC grants. Because access granted through a secondary role is also honored, a user who has ACCOUNTADMIN as a secondary role can access all models as well. To verify that the allowlist and RBAC restrictions work as expected, test them with a role other than ACCOUNTADMIN and disable secondary roles with `USE SECONDARY ROLES NONE`.

## Account-level allowlist parameter

Warning

`CORTEX_MODELS_ALLOWLIST` is being deprecated. Starting in August 2026, you can no longer change this parameter to a new value. The only permitted change will be to set it to `'None'`. Later in 2026, the parameter will be removed entirely. Snowflake recommends [migrating to role-based access control (RBAC)](#label-cortex-llm-migrate-to-rbac) now, which provides finer-grained, per-role control and is the go-forward model access mechanism.

You can control model access across your entire account using the CORTEX\_MODELS\_ALLOWLIST parameter. [Supported features](#label-cortex-llm-model-access-supported-features) respect this parameter and block allowlist access to models that are not listed, unless the calling role has RBAC access to the model. For how the two mechanisms interact, see [How RBAC and the allowlist interact](#label-cortex-llm-rbac-with-account-allowlist).

The CORTEX\_MODELS\_ALLOWLIST parameter can be set to `'All'`, `'None'`, or to a comma-separated list
of model names. Model names are case-sensitive and must be specified in lowercase (for example, `'mistral-large2'`
rather than `'MISTRAL-LARGE2'`). This parameter can only be set at the account level, not at the user or session
levels. Only the ACCOUNTADMIN role can set the parameter using the [ALTER ACCOUNT](/sql-reference/sql/alter-account) command.

Examples:

- To allow access to all models:

  Copy code

  ```
  ALTER ACCOUNT SET CORTEX_MODELS_ALLOWLIST = 'All';
  ```
- To allow access to the `mistral-large2` and `llama3.1-70b` models:

  Copy code

  ```
  ALTER ACCOUNT SET CORTEX_MODELS_ALLOWLIST = 'mistral-large2,llama3.1-70b';
  ```
- To block allowlist access to all models (roles with RBAC grants can still use those models):

  Copy code

  ```
  ALTER ACCOUNT SET CORTEX_MODELS_ALLOWLIST = 'None';
  ```

Snowflake recommends migrating to RBAC instead, as described in the following section.

## Role-based access control (RBAC)

Although Cortex models are not themselves Snowflake objects, Snowflake lets you create model objects in the SNOWFLAKE.MODELS schema that *represent* the Cortex models. By applying RBAC to these objects, you can control access to models the same way you would any other Snowflake object. [Supported features](#label-cortex-llm-model-access-supported-features) accept the identifiers of objects in SNOWFLAKE.MODELS wherever a model can be specified.

Tip

To use RBAC exclusively, set CORTEX\_MODELS\_ALLOWLIST to `'None'`.

### Refresh model objects and application roles

The `SNOWFLAKE.MODELS` schema is refreshed daily to include objects for all currently available Cortex models. The refresh also creates the corresponding application roles and `CORTEX-MODEL-ROLE-ALL`, a role that covers all models.

Snowflake runs the daily refresh with a Snowflake-managed task, `SNOWFLAKE.MODELS.CORTEX_BASE_MODELS_REFRESH_TASK`, which you can’t change or schedule. If you need a newly available model before the next daily run, an ACCOUNTADMIN can call the stored procedure on demand. To refresh more often, create your own task that calls the procedure on the schedule you want. Your own task uses compute in your account.

Copy code

```
CALL SNOWFLAKE.MODELS.CORTEX_BASE_MODELS_REFRESH();
```

You can call the procedure at any time. It doesn’t create duplicate objects or roles.

The managed task can show intermittent `FAILED` runs in [TASK\_HISTORY](/sql-reference/functions/task_history). These failures don’t remove model objects, and the next daily run typically succeeds, so you can ignore them.

### Grant application roles to user roles

You can grant model application roles to specific user roles in your account.

- To grant a role access to a specific model:

  Copy code

  ```
  GRANT APPLICATION ROLE SNOWFLAKE."CORTEX-MODEL-ROLE-LLAMA3.1-70B" TO ROLE MY_ROLE;
  ```
- To grant a role access to all current and future models:

  Copy code

  ```
  GRANT APPLICATION ROLE SNOWFLAKE."CORTEX-MODEL-ROLE-ALL" TO ROLE MY_ROLE;
  ```

### Default bootstrap of CORTEX-MODEL-ROLE-ALL

As part of the
[CORTEX\_MODELS\_ALLOWLIST deprecation](/release-notes/bcr-bundles/un-bundled/bcr-2378)
behavior change, Snowflake grants the `CORTEX-MODEL-ROLE-ALL` application role to the
`SNOWFLAKE.PUBLIC` application role. `SNOWFLAKE.PUBLIC` is granted to the account-level PUBLIC
role, so users inherit access to all current and future Cortex models by default (subject to
[Cortex LLM privileges](/user-guide/snowflake-cortex/aisql-privileges-and-access#label-cortex-llm-privileges)). Accounts that have
`CORTEX_MODELS_ALLOWLIST` set to `'All'` (including new accounts, which default to `'All'`)
receive this bootstrap grant.

This bootstrap path is separate from grants you make yourself with
`GRANT APPLICATION ROLE ... TO ROLE PUBLIC`. Use the stored procedures in this section to manage
the bootstrap grant. Use ordinary `GRANT` and `REVOKE APPLICATION ROLE` statements only for grants
you manage yourself.

#### Investigate whether the bootstrap grant is present

To confirm that `CORTEX-MODEL-ROLE-ALL` is granted through `SNOWFLAKE.PUBLIC`, run the following as
ACCOUNTADMIN and look for `CORTEX-MODEL-ROLE-ALL` in the result:

Copy code

```
SHOW GRANTS TO APPLICATION ROLE SNOWFLAKE.PUBLIC;
```

You can also list model application roles and see which account roles inherit `SNOWFLAKE.PUBLIC`:

Copy code

```
SHOW APPLICATION ROLES LIKE 'CORTEX-MODEL%' IN APPLICATION SNOWFLAKE;
SHOW GRANTS OF APPLICATION ROLE SNOWFLAKE.PUBLIC;
```

Tip

`SNOWFLAKE.PUBLIC` is an application role on the SNOWFLAKE database. It is not the same object as
the account-level PUBLIC role. Use `SHOW GRANTS TO APPLICATION ROLE SNOWFLAKE.PUBLIC` to audit the
bootstrap grant. `SHOW GRANTS TO ROLE PUBLIC` shows account-level PUBLIC grants and might not
reflect the bootstrap path.

#### Revoke or restore the bootstrap grant

To remove default access to all models through the bootstrap grant, call
[SNOWFLAKE.LOCAL.REVOKE\_FROM\_PUBLIC\_APPLICATION\_ROLE](/sql-reference/stored-procedures/snowflake_local_revoke_from_public_application_role) with a role that has the `SNOWFLAKE.SNOWFLAKE_PUBLIC_GRANT_ADMIN` application role, such as
ACCOUNTADMIN:

Copy code

```
CALL SNOWFLAKE.LOCAL.REVOKE_FROM_PUBLIC_APPLICATION_ROLE(
  'APP_ROLE',
  'CORTEX-MODEL-ROLE-ALL'
);
```

After the revoke, re-run `SHOW GRANTS TO APPLICATION ROLE SNOWFLAKE.PUBLIC` and confirm that
`CORTEX-MODEL-ROLE-ALL` is no longer listed. Then grant specific model application roles to the
roles that need them.

To restore the bootstrap grant after you’ve revoked it, call
[SNOWFLAKE.LOCAL.GRANT\_TO\_PUBLIC\_APPLICATION\_ROLE](/sql-reference/stored-procedures/snowflake_local_grant_to_public_application_role):

Copy code

```
CALL SNOWFLAKE.LOCAL.GRANT_TO_PUBLIC_APPLICATION_ROLE(
  'APP_ROLE',
  'CORTEX-MODEL-ROLE-ALL'
);
```

Important

A raw `REVOKE APPLICATION ROLE SNOWFLAKE."CORTEX-MODEL-ROLE-ALL" FROM ROLE PUBLIC` statement does
**not** remove the bootstrap grant from `SNOWFLAKE.PUBLIC`, and it doesn’t persist that intent
across Snowflake upgrades. Always use
[SNOWFLAKE.LOCAL.REVOKE\_FROM\_PUBLIC\_APPLICATION\_ROLE](/sql-reference/stored-procedures/snowflake_local_revoke_from_public_application_role) to revoke the bootstrap grant.

If you previously ran `GRANT APPLICATION ROLE SNOWFLAKE."CORTEX-MODEL-ROLE-ALL" TO ROLE PUBLIC`
yourself, you can still revoke that customer-managed grant with
`REVOKE APPLICATION ROLE SNOWFLAKE."CORTEX-MODEL-ROLE-ALL" FROM ROLE PUBLIC`. That revoke doesn’t
replace the stored-procedure revoke for the `SNOWFLAKE.PUBLIC` bootstrap path.

### Use model objects with supported features

To use model objects with supported Cortex features, specify the identifier of the model object in SNOWFLAKE.MODELS as the model argument.
You can use a fully-qualified identifier, a partial identifier, or a simple model name that will be automatically resolved to SNOWFLAKE.MODELS.

- Using a fully-qualified identifier:

  Copy code

  ```
  SELECT AI_COMPLETE('SNOWFLAKE.MODELS."LLAMA3.1-70B"', 'Hello');
  ```
- Using a partial identifier:

  Copy code

  ```
  USE DATABASE SNOWFLAKE;
  USE SCHEMA MODELS;
  SELECT AI_COMPLETE('LLAMA3.1-70B', 'Hello');
  ```
- Using automatic lookup with a simple model name:

  Copy code

  ```
  -- Automatically resolves to SNOWFLAKE.MODELS."LLAMA3.1-70B"
  SELECT AI_COMPLETE('llama3.1-70b', 'Hello');
  ```

### How RBAC and the allowlist interact

A number of Cortex features accept a model name as a string argument, for example `AI_COMPLETE('model', 'prompt')`. When you provide a model name:

1. Cortex first attempts to locate a matching model object in `SNOWFLAKE.MODELS`. If you provide an unqualified name like `'x'`, it automatically looks for `SNOWFLAKE.MODELS."X"`.
2. Access is granted if **either** of the following is true:
   - The calling role has USAGE on the model object (via an application role granted through RBAC), **or**
   - The model name matches an entry in `CORTEX_MODELS_ALLOWLIST` (or the allowlist is set to `'All'`).
3. Access is denied only if **both** checks fail.

The following example shows that either mechanism can grant access. The allowlist allows `mistral-large2`; the role has RBAC access to `LLAMA3.1-70B` but not to `claude-sonnet-4-6`. The last query fails because neither mechanism permits that model.

Copy code

```
-- set up access
USE SECONDARY ROLES NONE;
USE ROLE ACCOUNTADMIN;
ALTER ACCOUNT SET CORTEX_MODELS_ALLOWLIST = 'MISTRAL-LARGE2';
CALL SNOWFLAKE.MODELS.CORTEX_BASE_MODELS_REFRESH();
GRANT APPLICATION ROLE SNOWFLAKE."CORTEX-MODEL-ROLE-LLAMA3.1-70B" TO ROLE PUBLIC;

-- test access
USE ROLE PUBLIC;

-- this succeeds because mistral-large2 is in the allowlist
SELECT AI_COMPLETE('MISTRAL-LARGE2', 'Hello');

-- this succeeds because the role has access to the model object
SELECT AI_COMPLETE('SNOWFLAKE.MODELS."LLAMA3.1-70B"', 'Hello');

-- this fails because the first argument is
-- neither an identifier for an accessible model object
-- nor is it a model name in the allowlist
SELECT AI_COMPLETE('claude-sonnet-4-6', 'Hello');
```

## Common pitfalls

- Access to a model (whether by allowlist or RBAC) does not always mean that it can be used. It may still be subject to
  cross-region, [legacy or end-of-life](/user-guide/snowflake-cortex/aisql-regional-availability#label-cortex-model-lifecycle), or other availability constraints. These restrictions can result in error messages that
  seem similar to model access errors. To check which Cortex Base Models are currently available in your account and
  their lifecycle status, use [SHOW CORTEX BASE MODELS](/sql-reference/sql/show-cortex-base-models).
- Model access controls only govern the use of a model and not the use of a feature itself. A feature can have its own access
  controls. For example, access to `AI_COMPLETE` is governed by the `CORTEX_USER` or `AI_FUNCTIONS_USER` database role and the USE AI FUNCTIONS account-level privilege. For more information, see
  [Cortex LLM privileges](/user-guide/snowflake-cortex/aisql-privileges-and-access#label-cortex-llm-privileges).
- Not all features support model access controls. For more information about what a feature supports, see the [supported features](#label-cortex-llm-model-access-supported-features) table.
- After you grant or revoke a model application role, requests through [Cortex AI Gateway](/user-guide/snowflake-cortex/cortex-ai-gateway#label-cortex-ai-gateway-access-control)
  and the [Cortex REST API](/user-guide/snowflake-cortex/cortex-rest-api) can take up to 5 minutes to reflect the change.
  Cortex AI Functions reflect these changes sooner.
- Secondary roles can obscure permissions. For example, if a user has ACCOUNTADMIN as a secondary role, all model objects may appear
  accessible. Disable secondary roles temporarily when verifying permissions.
- Revoking `CORTEX-MODEL-ROLE-ALL` from the account-level PUBLIC role does not remove the
  [bootstrap grant](#label-cortex-model-role-all-bootstrap) on `SNOWFLAKE.PUBLIC`. Use
  `SHOW GRANTS TO APPLICATION ROLE SNOWFLAKE.PUBLIC` to check, and
  [SNOWFLAKE.LOCAL.REVOKE\_FROM\_PUBLIC\_APPLICATION\_ROLE](/sql-reference/stored-procedures/snowflake_local_revoke_from_public_application_role) to revoke.
- Qualified model object identifiers are quoted and therefore case-sensitive. For more information, see
  [QUOTED\_IDENTIFIERS\_IGNORE\_CASE](/sql-reference/parameters#label-quoted-identifiers-ignore-case).

## Migrate from the allowlist to RBAC

Because `CORTEX_MODELS_ALLOWLIST` is planned for deprecation, Snowflake recommends migrating to model RBAC. The following steps walk through a complete migration.

### Step 1: Check your current allowlist

As ACCOUNTADMIN, check what models are currently allowlisted:

Copy code

```
SHOW PARAMETERS LIKE 'CORTEX_MODELS_ALLOWLIST' IN ACCOUNT;
```

Note the value. For example:

- `'All'`: all models are accessible. Rely on the
  [CORTEX-MODEL-ROLE-ALL bootstrap](#label-cortex-model-role-all-bootstrap), or grant
  `CORTEX-MODEL-ROLE-ALL` yourself to replace this.
- `'model-a,model-b'`: only specific models are accessible. Grant per-model roles to replace this.
- `'None'`: no models are accessible. You can set RBAC grants selectively.

### Step 2: Grant equivalent model application roles

Because `CORTEX_MODELS_ALLOWLIST` applies account-wide, the direct RBAC equivalent is granting model application roles to the PUBLIC role. Snowflake grants PUBLIC to every user and every role in the account, so every role inherits those grants. Start by replicating the allowlist behavior exactly, then tighten access to specific roles as needed.

Warning

A grant to PUBLIC covers ordinary user sessions. It doesn’t cover code that runs inside a native app. Native app code uses the app’s own role hierarchy, not the consumer account’s PUBLIC role. If the app calls a Cortex AI function, grant the model application role to the application, or to the role in use inside the app.

For restricted caller’s rights (RCR) stored procedures, granting model application roles to PUBLIC is sufficient. Model RBAC doesn’t evaluate RCR caller grants in RCR contexts.

Test all your workloads, including stored procedures and native apps, before you disable the allowlist.

The `SNOWFLAKE.MODELS` schema is refreshed daily and already contains objects for all available models. To see which model roles are available:

Copy code

```
SHOW APPLICATION ROLES LIKE 'CORTEX-MODEL%' IN APPLICATION SNOWFLAKE;
```

To replicate an allowlist that includes specific models (equivalent to `CORTEX_MODELS_ALLOWLIST = 'model-a,model-b'`), grant those roles to PUBLIC:

Copy code

```
USE ROLE ACCOUNTADMIN;

GRANT APPLICATION ROLE SNOWFLAKE."CORTEX-MODEL-ROLE-MODEL-A" TO ROLE PUBLIC;
GRANT APPLICATION ROLE SNOWFLAKE."CORTEX-MODEL-ROLE-MODEL-B" TO ROLE PUBLIC;
```

To replicate an allowlist that allows all models (equivalent to `CORTEX_MODELS_ALLOWLIST = 'All'`),
either rely on the automatic
[CORTEX-MODEL-ROLE-ALL bootstrap](#label-cortex-model-role-all-bootstrap) through `SNOWFLAKE.PUBLIC`,
or grant the role yourself to PUBLIC:

Copy code

```
USE ROLE ACCOUNTADMIN;

GRANT APPLICATION ROLE SNOWFLAKE."CORTEX-MODEL-ROLE-ALL" TO ROLE PUBLIC;
```

Once the allowlist is disabled, you can take advantage of RBAC’s finer-grained control by
removing broad all-models access and granting specific model roles only to the roles that need
them. If all-models access came from the `SNOWFLAKE.PUBLIC` bootstrap, revoke it with the stored
procedure. If you granted `CORTEX-MODEL-ROLE-ALL` to PUBLIC yourself, use
`REVOKE APPLICATION ROLE`:

Copy code

```
USE ROLE ACCOUNTADMIN;

-- If the bootstrap grant is present (preferred check: SHOW GRANTS TO APPLICATION ROLE SNOWFLAKE.PUBLIC)
CALL SNOWFLAKE.LOCAL.REVOKE_FROM_PUBLIC_APPLICATION_ROLE(
  'APP_ROLE',
  'CORTEX-MODEL-ROLE-ALL'
);

-- Only if you previously granted CORTEX-MODEL-ROLE-ALL to PUBLIC yourself
REVOKE APPLICATION ROLE SNOWFLAKE."CORTEX-MODEL-ROLE-ALL" FROM ROLE PUBLIC;

-- Grant specific models only to the roles that need them
GRANT APPLICATION ROLE SNOWFLAKE."CORTEX-MODEL-ROLE-MODEL-A" TO ROLE analyst_role;
GRANT APPLICATION ROLE SNOWFLAKE."CORTEX-MODEL-ROLE-MODEL-B" TO ROLE data_science_role;
```

If you want to restrict model access to a specific group of users rather than all users in the account, grant the model role to a custom role and make sure broad all-models access isn’t still available through PUBLIC or the bootstrap path:

Copy code

```
USE ROLE ACCOUNTADMIN;

-- Create a role for users who need model access
CREATE ROLE IF NOT EXISTS cortex_ai_role;

-- Grant the desired model roles to that custom role
GRANT APPLICATION ROLE SNOWFLAKE."CORTEX-MODEL-ROLE-MODEL-A" TO ROLE cortex_ai_role;
GRANT APPLICATION ROLE SNOWFLAKE."CORTEX-MODEL-ROLE-MODEL-B" TO ROLE cortex_ai_role;

-- Remove bootstrap all-models access if present
CALL SNOWFLAKE.LOCAL.REVOKE_FROM_PUBLIC_APPLICATION_ROLE(
  'APP_ROLE',
  'CORTEX-MODEL-ROLE-ALL'
);

-- Only if you previously granted CORTEX-MODEL-ROLE-ALL to PUBLIC yourself
REVOKE APPLICATION ROLE SNOWFLAKE."CORTEX-MODEL-ROLE-ALL" FROM ROLE PUBLIC;

-- Assign the custom role to the users who need access
GRANT ROLE cortex_ai_role TO USER alice;
GRANT ROLE cortex_ai_role TO USER bob;
```

### Step 3: Verify access with RBAC

Before disabling the allowlist, verify that the RBAC grants work as expected. Switch to a non-ACCOUNTADMIN role that has the model role grant and run a test call:

Copy code

```
USE ROLE PUBLIC;

-- Should succeed if CORTEX-MODEL-ROLE-MODEL-A was granted to PUBLIC
SELECT AI_COMPLETE('SNOWFLAKE.MODELS."MODEL-A"', 'Hello');
```

To see which models the current role has access to:

Copy code

```
SHOW CORTEX BASE MODELS IN SCHEMA SNOWFLAKE.MODELS;
```

### Step 4: Disable the allowlist

Once you’ve confirmed that RBAC grants are working, disable the allowlist so that RBAC is the only access mechanism:

Copy code

```
USE ROLE ACCOUNTADMIN;

ALTER ACCOUNT SET CORTEX_MODELS_ALLOWLIST = 'None';
```

Setting the allowlist to `'None'` disables the allowlist fallback entirely, so only RBAC grants determine access.

## Supported features

Model access controls follow the model. The same restriction applies in every feature that uses that model, including [Cortex Agents](/user-guide/snowflake-cortex/cortex-agents) and [Snowflake CoWork](/user-guide/snowflake-cortex/snowflake-cowork).

Model access controls are supported by the following features:

| Feature | Account-level allowlist | Role-based access control | Notes |
| --- | --- | --- | --- |
| [AI\_COMPLETE](/sql-reference/functions/ai_complete) | ✔ | ✔ |  |
| [AI\_CLASSIFY](/sql-reference/functions/ai_classify) | ✔ | ✔ | If the model powering this function is not allowed, the error message contains information about how to modify the allowlist or model RBAC grants. |
| [AI\_FILTER](/sql-reference/functions/ai_filter) | ✔ | ✔ | If the model powering this function is not allowed, the error message contains information about how to modify the allowlist or model RBAC grants. |
| [AI\_AGG](/sql-reference/functions/ai_agg) | ✔ | ✔ | If the model powering this function is not allowed, the error message contains information about how to modify the allowlist or model RBAC grants. |
| [AI\_SUMMARIZE\_AGG](/sql-reference/functions/ai_summarize_agg) | ✔ | ✔ | If the model powering this function is not allowed, the error message contains information about how to modify the allowlist or model RBAC grants. |
| [AI\_TRANSCRIBE](/sql-reference/functions/ai_transcribe) | ✔ | ✔ |  |
| [AI\_EXTRACT](/sql-reference/functions/ai_extract) | ✔ | ✔ |  |
| [AI\_SENTIMENT](/sql-reference/functions/ai_sentiment) | ✔ | ✔ |  |
| [AI\_TRANSLATE](/sql-reference/functions/ai_translate) | ✔ | ✔ |  |
| [AI\_PARSE\_DOCUMENT](/sql-reference/functions/ai_parse_document) | ✔ | ✔ |  |
| [AI\_REDACT](/sql-reference/functions/ai_redact) | ✔ | ✔ |  |
| [Cortex REST API](/user-guide/snowflake-cortex/cortex-rest-api) | ✔ | ✔ | Grants and revokes can take up to 5 minutes to take effect. |
| [Cortex AI Gateway](/user-guide/snowflake-cortex/cortex-ai-gateway) | ✔ | ✔ | Grants and revokes can take up to 5 minutes to take effect. |
| [Cortex Playground](/user-guide/snowflake-cortex/cortex-playground) | ✔ | ✔ |  |
| [Snowflake CoCo](/user-guide/cortex-code/cortex-code) | ✔ | ✔ | Applies to CoCo in Snowsight, CoCo Desktop, and CoCo CLI. The model picker shows only the models the current role can access. |
| [Cortex Agents](/user-guide/snowflake-cortex/cortex-agents) | ✔ | ✔ | Applies to the orchestration model selected for the agent in Snowsight, SQL, or the REST API. |
| [Snowflake CoWork](/user-guide/snowflake-cortex/snowflake-cowork) | ✔ | ✔ | Applies to the orchestration model of the agents that Snowflake CoWork runs. |

Expand

Show lessSee more
