# Privileges and model access for Cortex AI Functions

## Cortex LLM privileges

Access to Snowflake Cortex AI Functions is gated by an account-level privilege and one of several database roles.
Use the following sections to grant or revoke access at the account, role, or per-function level.

### USE AI FUNCTIONS on the account privilege

Important

Your users need both the USE AI FUNCTIONS account-level privilege (or a per-function `USE AI FUNCTION <name>`
privilege) and one of the CORTEX\_USER or
[AI\_FUNCTIONS\_USER](#label-cortex-ai-functions-user-role) database roles to use Snowflake Cortex AI Functions.

The USE AI FUNCTIONS account-level privilege includes the privileges that allow your users to call Snowflake Cortex AI functions. By default, the USE AI FUNCTIONS privilege is granted to the PUBLIC role. The PUBLIC role is automatically granted to all users and roles, allowing all users in your account to use the Snowflake Cortex AI functions. If you don’t want all your users to have this privilege, you can revoke access to the PUBLIC role and grant access to other roles.

If you need finer-grained control over which AI functions individual roles can call, see
[USE AI FUNCTION <name> — per-function privileges](#label-cortex-ai-function-per-function-privileges).

To control which roles have the USE AI FUNCTIONS privilege:

- Revoke it from the PUBLIC role.
- Grant it to specific roles.

Important

You must use the ACCOUNTADMIN role to manage the USE AI FUNCTIONS account-level privilege.

To revoke the USE AI FUNCTIONS account-level privilege from the PUBLIC role, run the following command:

Copy code

```
REVOKE USE AI FUNCTIONS ON ACCOUNT
FROM ROLE PUBLIC;
```

Note

Revoking the USE AI FUNCTIONS account-level privilege prevents your users from accessing most Snowflake Cortex AI Functions.
Your users need **both** the USE AI FUNCTIONS account-level privilege and one of the CORTEX\_USER or
[AI\_FUNCTIONS\_USER](#label-cortex-ai-functions-user-role) database roles to use Snowflake Cortex AI Functions. If a user has the USE AI FUNCTIONS account-level privilege but doesn’t have the CORTEX\_USER role, they can still use the AI\_AGG and AI\_SUMMARIZE\_AGG functions.

After you’ve revoked the USE AI FUNCTIONS privilege from the PUBLIC role, you can use the ACCOUNTADMIN role to grant it to other roles in your Snowflake account.

The following example:

1. Grants the USE AI FUNCTIONS privilege to `cortex_user_role`.
2. Grants the `cortex_user_role` to `example_user`.

Copy code

```
USE ROLE ACCOUNTADMIN;

CREATE ROLE cortex_user_role;

GRANT USE AI FUNCTIONS ON ACCOUNT TO ROLE cortex_user_role;

GRANT ROLE cortex_user_role TO USER example_user;
```

You can grant access to Snowflake Cortex AI Functions through roles that are commonly used by specific groups of users. For example, if you’ve created an `analyst` role that is used as a default role by analysts in your organization, you can grant these users access to Snowflake Cortex AI Functions with a single [GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege) statement. For more information about granting privileges to commonly used roles, see [User roles](/user-guide/admin-user-management#label-user-management-user-roles).

Copy code

```
GRANT USE AI FUNCTIONS ON ACCOUNT TO ROLE analyst;
```

Important

Currently, USE AI FUNCTIONS does not apply to AI Function queries that are run inside Snowflake native applications. A query with AI Function calls runs successfully regardless of whether the role has USE AI FUNCTIONS privilege.

### USE AI FUNCTION <name> — per-function privileges

In addition to the blanket USE AI FUNCTIONS privilege, you can grant per-function privileges using
`USE AI FUNCTION <name>`. This allows ACCOUNTADMIN to control access at the individual function level
instead of granting access to all AI functions at once.

The per-function privilege and the blanket USE AI FUNCTIONS privilege have an **OR** relationship:

- If a role has USE AI FUNCTIONS, it can call **all** Cortex AI functions, regardless of any per-function grants or revocations.
- If a role has only `USE AI FUNCTION AI_COMPLETE`, it can call only the AI\_COMPLETE function.
- If a role has both USE AI FUNCTIONS and a per-function grant, revoking the per-function grant does **not** affect access because the blanket privilege still applies.

Important

Per-function privileges require the same CORTEX\_USER (or AI\_FUNCTIONS\_USER) database role as the blanket
USE AI FUNCTIONS privilege.

#### Supported per-function privileges

The following table lists each Cortex AI function and its corresponding per-function privilege name for use
with `GRANT USE AI FUNCTION <name> ON ACCOUNT TO ROLE <role_name>`.

| Function | Per-function privilege name |
| --- | --- |
| [AI\_COMPLETE](/sql-reference/functions/ai_complete) | AI\_COMPLETE |
| [AI\_CLASSIFY](/sql-reference/functions/ai_classify) | AI\_CLASSIFY |
| [AI\_FILTER](/sql-reference/functions/ai_filter) | AI\_FILTER |
| [AI\_AGG](/sql-reference/functions/ai_agg) | AI\_AGG |
| [AI\_EMBED](/sql-reference/functions/ai_embed) | AI\_EMBED |
| [AI\_EXTRACT](/sql-reference/functions/ai_extract) | AI\_EXTRACT |
| [AI\_SENTIMENT](/sql-reference/functions/ai_sentiment) | AI\_SENTIMENT |
| [AI\_SUMMARIZE\_AGG](/sql-reference/functions/ai_summarize_agg) | AI\_SUMMARIZE\_AGG |
| [AI\_SIMILARITY](/sql-reference/functions/ai_similarity) | AI\_SIMILARITY |
| [AI\_TRANSCRIBE](/sql-reference/functions/ai_transcribe) | AI\_TRANSCRIBE |
| [AI\_PARSE\_DOCUMENT](/sql-reference/functions/ai_parse_document) | AI\_PARSE\_DOCUMENT |
| [AI\_REDACT](/sql-reference/functions/ai_redact) | AI\_REDACT |
| [AI\_TRANSLATE](/sql-reference/functions/ai_translate) | AI\_TRANSLATE |
| [AI\_COUNT\_TOKENS](/sql-reference/functions/ai_count_tokens) | AI\_COUNT\_TOKENS |
| [SNOWFLAKE.CORTEX.COMPLETE](/sql-reference/functions/complete-snowflake-cortex) | COMPLETE |
| [SNOWFLAKE.CORTEX.CLASSIFY\_TEXT](/sql-reference/functions/classify_text-snowflake-cortex) | CLASSIFY\_TEXT |
| [SNOWFLAKE.CORTEX.COUNT\_TOKENS](/sql-reference/functions/count_tokens-snowflake-cortex) | COUNT\_TOKENS |
| [SNOWFLAKE.CORTEX.EMBED\_TEXT](/sql-reference/functions/embed_text_1024-snowflake-cortex) | EMBED\_TEXT |
| [SNOWFLAKE.CORTEX.ENTITY\_SENTIMENT](/sql-reference/functions/entity_sentiment-snowflake-cortex) | ENTITY\_SENTIMENT |
| [SNOWFLAKE.CORTEX.EXTRACT\_ANSWER](/sql-reference/functions/extract_answer-snowflake-cortex) | EXTRACT\_ANSWER |
| [SNOWFLAKE.CORTEX.PARSE\_DOCUMENT](/sql-reference/functions/parse_document-snowflake-cortex) | PARSE\_DOCUMENT |
| [SNOWFLAKE.CORTEX.SENTIMENT](/sql-reference/functions/sentiment-snowflake-cortex) | SENTIMENT |
| [SNOWFLAKE.CORTEX.SUMMARIZE](/sql-reference/functions/ai_summarize) | SUMMARIZE |
| [SNOWFLAKE.CORTEX.SUMMARIZE\_AGG](/sql-reference/functions/summarize_agg-snowflake-cortex) | SUMMARIZE\_AGG |
| [SNOWFLAKE.CORTEX.TRANSLATE](/sql-reference/functions/translate-snowflake-cortex) | TRANSLATE |
| [SNOWFLAKE.CORTEX.TRY\_COMPLETE](/sql-reference/functions/try_complete-snowflake-cortex) | TRY\_COMPLETE |

Expand

Show lessSee more

#### Granting per-function privileges

Use the ACCOUNTADMIN role to grant a per-function privilege. The syntax is:

Copy code

```
GRANT USE AI FUNCTION <function_name> ON ACCOUNT TO ROLE <role_name>;
```

The following example revokes the blanket privilege from PUBLIC, then grants only AI\_COMPLETE access to a
specific role:

Copy code

```
USE ROLE ACCOUNTADMIN;

-- Remove blanket access from PUBLIC
REVOKE USE AI FUNCTIONS ON ACCOUNT FROM ROLE PUBLIC;

-- Create a role with access to only AI_COMPLETE
CREATE ROLE ai_complete_user_role;
GRANT USE AI FUNCTION AI_COMPLETE ON ACCOUNT TO ROLE ai_complete_user_role;
GRANT DATABASE ROLE SNOWFLAKE.CORTEX_USER TO ROLE ai_complete_user_role;

GRANT ROLE ai_complete_user_role TO USER example_user;
```

You can grant multiple per-function privileges to the same role to build a custom set of allowed functions:

Copy code

```
USE ROLE ACCOUNTADMIN;

CREATE ROLE ai_analyst_role;

GRANT USE AI FUNCTION AI_COMPLETE ON ACCOUNT TO ROLE ai_analyst_role;
GRANT USE AI FUNCTION AI_CLASSIFY ON ACCOUNT TO ROLE ai_analyst_role;
GRANT USE AI FUNCTION AI_EXTRACT ON ACCOUNT TO ROLE ai_analyst_role;
GRANT USE AI FUNCTION AI_TRANSLATE ON ACCOUNT TO ROLE ai_analyst_role;

GRANT DATABASE ROLE SNOWFLAKE.CORTEX_USER TO ROLE ai_analyst_role;
GRANT ROLE ai_analyst_role TO USER analyst_user;
```

#### Revoking per-function privileges

To revoke a per-function privilege:

Copy code

```
REVOKE USE AI FUNCTION <function_name> ON ACCOUNT FROM ROLE <role_name>;
```

For example:

Copy code

```
USE ROLE ACCOUNTADMIN;

REVOKE USE AI FUNCTION AI_COMPLETE ON ACCOUNT FROM ROLE ai_analyst_role;
```

After revocation, the role can no longer call AI\_COMPLETE unless it also has the blanket USE AI FUNCTIONS
privilege.

#### Viewing per-function grants

You can view per-function privilege grants using SHOW GRANTS:

Copy code

```
-- View all grants to a specific role
SHOW GRANTS TO ROLE ai_analyst_role;

-- View all grants on the account
SHOW GRANTS ON ACCOUNT;
```

Per-function grants appear with the privilege name `USE AI FUNCTION <function_name>` (for example,
`USE AI FUNCTION AI_COMPLETE`).

### Using AI Functions with Restricted Caller’s Rights

To use AI Functions with Restricted Caller’s Rights, you must grant the USE AI FUNCTIONS privilege (or the appropriate `USE AI FUNCTION <name>` per-function privilege) to both the session role and the service or application owner role.

For example, to use AI Functions inside a Snowpark Container Services (SPCS) service that runs with Restricted Caller’s Rights:

1. Grant the USE AI FUNCTIONS privilege to the role used in the SPCS session (for example, `CHATBOT_USER_ROLE`):

   Copy code

   ```
   GRANT USE AI FUNCTIONS ON ACCOUNT TO ROLE CHATBOT_USER_ROLE;
   ```
2. Grant the caller version of the privilege to the service owner role:

   Copy code

   ```
   GRANT CALLER USE AI FUNCTIONS ON ACCOUNT TO ROLE <service_owner_role>;
   ```

### CORTEX\_USER database role

The CORTEX\_USER database role in the SNOWFLAKE database includes the privileges that allow users to call Snowflake
Cortex AI Functions. By default, the CORTEX\_USER role is granted to the PUBLIC role. The PUBLIC role is automatically granted
to all users and roles, so this allows all users in your account to use the Snowflake Cortex AI functions.

If you don’t want all users to have this privilege, you can revoke access to the PUBLIC role and grant access to other roles.
The SNOWFLAKE.CORTEX\_USER database role cannot be granted directly to a user. For more information, see
[Using SNOWFLAKE database roles](/sql-reference/snowflake-db-roles#label-using-snowflake-db-roles).

To revoke the CORTEX\_USER database role from the PUBLIC role, run the following commands using the ACCOUNTADMIN role:

Copy code

```
REVOKE DATABASE ROLE SNOWFLAKE.CORTEX_USER
  FROM ROLE PUBLIC;

REVOKE IMPORTED PRIVILEGES ON DATABASE SNOWFLAKE
  FROM ROLE PUBLIC;
```

You can then selectively provide access to specific roles. A user with the ACCOUNTADMIN role can grant this role to a custom role in
order to allow users to access Cortex AI functions. In the following example, use the ACCOUNTADMIN role and grant the user `some_user`
the CORTEX\_USER database role via the account role `cortex_user_role`, which you create for this purpose.

Copy code

```
USE ROLE ACCOUNTADMIN;

CREATE ROLE cortex_user_role;
GRANT DATABASE ROLE SNOWFLAKE.CORTEX_USER TO ROLE cortex_user_role;

GRANT ROLE cortex_user_role TO USER some_user;
```

You can also grant access to Snowflake Cortex AI functions through existing roles commonly used by specific groups of
users. (See [User roles](/user-guide/admin-user-management#label-user-management-user-roles).) For example, if you have created an `analyst` role that is used
as a default role by analysts in your organization, you can easily grant these users access to Snowflake Cortex AI
Functions with a single GRANT statement.

Copy code

```
GRANT DATABASE ROLE SNOWFLAKE.CORTEX_USER TO ROLE analyst;
```

### AI\_FUNCTIONS\_USER database role

The AI\_FUNCTIONS\_USER database role in the SNOWFLAKE database allows users to call Snowflake Cortex
[scalar AI functions](/user-guide/snowflake-cortex/aisql#label-cortex-llm-ai-function) (all Cortex AI functions except the aggregate functions
AI\_AGG and AI\_SUMMARIZE\_AGG) without granting access to Cortex services such as Cortex Agent, Cortex Analyst,
Cortex Fine-tuning, or Cortex Search.

Important

Your users need both the USE AI FUNCTIONS account-level privilege (or a per-function `USE AI FUNCTION <name>`
privilege) plus one of CORTEX\_USER and AI\_FUNCTIONS\_USER database roles to call Snowflake Cortex AI functions.

AI\_FUNCTIONS\_USER role is not granted to the PUBLIC role by default. ACCOUNTADMIN must
explicitly grant this role to roles that require access to AI functions. The AI\_FUNCTIONS\_USER database role
cannot be granted directly to users but must be granted to roles that users can assume. For more information, see
[Using SNOWFLAKE database roles](/sql-reference/snowflake-db-roles#label-using-snowflake-db-roles).

The following example creates a custom role, grants the AI\_FUNCTIONS\_USER database role to it, and assigns the role
to a user.

Copy code

```
USE ROLE ACCOUNTADMIN;

CREATE ROLE analyst_rl;
GRANT DATABASE ROLE SNOWFLAKE.AI_FUNCTIONS_USER TO ROLE analyst_rl;

GRANT ROLE analyst_rl TO USER some_user;
```

Alternatively, to give all users access to scalar AI function capabilities, grant the AI\_FUNCTIONS\_USER role to the
PUBLIC role.

Copy code

```
USE ROLE ACCOUNTADMIN;

GRANT DATABASE ROLE SNOWFLAKE.AI_FUNCTIONS_USER TO ROLE PUBLIC;
```

### CORTEX\_EMBED\_USER database role

The CORTEX\_EMBED\_USER database role in the SNOWFLAKE database includes the privileges that allow users to call the text
embedding functions AI\_EMBED, EMBED\_TEXT\_768, and EMBED\_TEXT\_1024 and to create Cortex Search Services with managed
vector embeddings. CORTEX\_EMBED\_USER allows you to grant embedding privileges separately from other Cortex AI capabilities.

Note

You can create Cortex Search Services with user-provided embeddings without the CORTEX\_EMBED\_USER role. In that
case, you must generate the embeddings yourself, outside of Snowflake, and load them into a table.

Unlike the CORTEX\_USER role, the CORTEX\_EMBED\_USER role is not granted to the PUBLIC role by default. You must
explicitly grant this role to roles that require embedding capabilities if you have revoked the CORTEX\_USER role. The
CORTEX\_EMBED\_USER database role cannot be granted directly to users but must be granted to roles that users can assume.
The following example illustrates this process.

Copy code

```
USE ROLE ACCOUNTADMIN;

CREATE ROLE cortex_embed_user_role;
GRANT DATABASE ROLE SNOWFLAKE.CORTEX_EMBED_USER TO ROLE cortex_embed_user_role;

GRANT ROLE cortex_embed_user_role TO USER some_user;
```

Alternatively, to give all users access to embedding capabilities, grant the CORTEX\_EMBED\_USER role to the PUBLIC role as follows.

Copy code

```
USE ROLE ACCOUNTADMIN;

GRANT DATABASE ROLE SNOWFLAKE.CORTEX_EMBED_USER TO ROLE PUBLIC;
```

### Using AI Functions in stored procedures with EXECUTE AS RESTRICTED CALLER

To use AI Functions inside stored procedures with `EXECUTE AS RESTRICTED CALLER`, grant the following privileges to the role that created the stored procedure:

Copy code

```
GRANT INHERITED CALLER USAGE ON ALL SCHEMAS IN DATABASE snowflake TO ROLE <role_that_created_the_stored_procedure>;
GRANT INHERITED CALLER USAGE ON ALL FUNCTIONS IN DATABASE snowflake TO ROLE <role_that_created_the_stored_procedure>;
GRANT CALLER USAGE ON DATABASE snowflake TO ROLE <role_that_created_the_stored_procedure>;
```

## Control model access

Snowflake Cortex provides two mechanisms to enforce access to models:

- [Role-based access control (RBAC)](#label-cortex-llm-rbac) (recommended, fine-grained control)
- [Account-level allowlist parameter](#label-cortex-llm-allowlist) (legacy, planned for deprecation)

Use the account-level allowlist for account-wide defaults and RBAC for per-role control. You can also [use both mechanisms together](#label-cortex-llm-rbac-with-account-allowlist): access is granted if either mechanism permits it. Snowflake recommends migrating to RBAC exclusively.

Note

The ACCOUNTADMIN role always has access to all models on the account, regardless of the CORTEX\_MODELS\_ALLOWLIST parameter or model RBAC grants. Because access granted through a secondary role is also honored, a user who has ACCOUNTADMIN as a secondary role can access all models as well. To verify that the allowlist and RBAC restrictions work as expected, test them with a role other than ACCOUNTADMIN and disable secondary roles with `USE SECONDARY ROLES NONE`.

### Account-level allowlist parameter

Warning

`CORTEX_MODELS_ALLOWLIST` is being deprecated. Starting in August 2026, you can no longer change this parameter to a new value — the only permitted change will be to set it to `'None'`. Later in 2026, the parameter will be removed entirely. Snowflake recommends [migrating to role-based access control (RBAC)](#label-cortex-llm-migrate-to-rbac) now, which provides finer-grained, per-role control and is the go-forward model access mechanism.

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

### Role-based access control (RBAC)

Although Cortex models are not themselves Snowflake objects, Snowflake lets you create model objects in the SNOWFLAKE.MODELS schema that *represent* the Cortex models. By applying RBAC to these objects, you can control access to models the same way you would any other Snowflake object. [Supported features](#label-cortex-llm-model-access-supported-features) accept the identifiers of objects in SNOWFLAKE.MODELS wherever a model can be specified.

Tip

To use RBAC exclusively, set CORTEX\_MODELS\_ALLOWLIST to `'None'`.

#### Refresh model objects and application roles

The `SNOWFLAKE.MODELS` schema is automatically populated with objects representing all currently available Cortex
models and is refreshed daily. The refresh also creates corresponding application roles and
`CORTEX-MODEL-ROLE-ALL`, a role that covers all models.

Snowflake runs that daily refresh with a Snowflake-managed task,
`SNOWFLAKE.MODELS.CORTEX_BASE_MODELS_REFRESH_TASK`. The task calls the
`SNOWFLAKE.MODELS.CORTEX_BASE_MODELS_REFRESH` stored procedure. You don’t create, own, or schedule the task, and it
doesn’t incur compute charges in your account.

The task can appear in [TASK\_HISTORY](/sql-reference/functions/task_history) and in task-failure notifications. An
intermittent `FAILED` status for this task is expected and doesn’t mean that model objects were removed. You can ignore
those failures; the next scheduled daily run typically succeeds, and you can’t change the task’s SQL or retry settings.
If you monitor task failures, exclude this Snowflake-managed task (or tasks in the `SNOWFLAKE` database) so it doesn’t
raise alerts that need no action.

If you need newly available models before the next daily run, an `ACCOUNTADMIN` can call the stored procedure on demand:

Copy code

```
CALL SNOWFLAKE.MODELS.CORTEX_BASE_MODELS_REFRESH();
```

Tip

You can safely call `CORTEX_BASE_MODELS_REFRESH` at any time; it won’t create duplicate objects or roles.

After refreshing the model objects, you can verify that the models appear in the SNOWFLAKE.MODELS schema as follows:

Copy code

```
SHOW MODELS IN SNOWFLAKE.MODELS;
```

The returned list of models resembles the following:

| created\_on | name | model\_type | database\_name | schema\_name | owner |
| --- | --- | --- | --- | --- | --- |
| 2025-04-22 09:35:38.558 -0700 | CLAUDE-4-5-SONNET | CORTEX\_BASE | SNOWFLAKE | MODELS | SNOWFLAKE |
| 2025-04-22 09:36:16.793 -0700 | LLAMA3.1-405B | CORTEX\_BASE | SNOWFLAKE | MODELS | SNOWFLAKE |
| 2025-04-22 09:37:18.692 -0700 | OPENAI-GPT-5.2 | CORTEX\_BASE | SNOWFLAKE | MODELS | SNOWFLAKE |

Expand

Show lessSee more

To verify that you can see the application roles associated with these models, use the SHOW APPLICATION ROLES command, as in the following example:

Copy code

```
SHOW APPLICATION ROLES LIKE 'CORTEX-MODEL%' IN APPLICATION SNOWFLAKE;
```

The list of application roles resembles the following:

| created\_on | name | owner | comment | owner\_role\_type |
| --- | --- | --- | --- | --- |
| 2025-04-22 09:35:38.558 -0700 | CORTEX-MODEL-ROLE-ALL | SNOWFLAKE | MODELS | APPLICATION |
| 2025-04-22 09:36:16.793 -0700 | CORTEX-MODEL-ROLE-LLAMA3.1-405B | SNOWFLAKE | MODELS | APPLICATION |

Expand

Show lessSee more

#### Grant application roles to user roles

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

#### Default bootstrap of CORTEX-MODEL-ROLE-ALL

As part of the
[CORTEX\_MODELS\_ALLOWLIST deprecation](/release-notes/bcr-bundles/un-bundled/bcr-2378)
behavior change, Snowflake grants the `CORTEX-MODEL-ROLE-ALL` application role to the
`SNOWFLAKE.PUBLIC` application role. `SNOWFLAKE.PUBLIC` is granted to the account-level PUBLIC
role, so users inherit access to all current and future Cortex models by default (subject to
[Cortex LLM privileges](#label-cortex-llm-privileges)). Accounts that have
`CORTEX_MODELS_ALLOWLIST` set to `'All'` (including new accounts, which default to `'All'`)
receive this bootstrap grant.

This bootstrap path is separate from grants you make yourself with
`GRANT APPLICATION ROLE ... TO ROLE PUBLIC`. Use the stored procedures in this section to manage
the bootstrap grant. Use ordinary `GRANT` and `REVOKE APPLICATION ROLE` statements only for grants
you manage yourself.

##### Investigate whether the bootstrap grant is present

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

##### Revoke or restore the bootstrap grant

To remove default access to all models through the bootstrap grant, call the following procedure
as ACCOUNTADMIN:

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

To restore the bootstrap grant after you’ve revoked it:

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
`SNOWFLAKE.LOCAL.REVOKE_FROM_PUBLIC_APPLICATION_ROLE` to revoke the bootstrap grant.

If you previously ran `GRANT APPLICATION ROLE SNOWFLAKE."CORTEX-MODEL-ROLE-ALL" TO ROLE PUBLIC`
yourself, you can still revoke that customer-managed grant with
`REVOKE APPLICATION ROLE SNOWFLAKE."CORTEX-MODEL-ROLE-ALL" FROM ROLE PUBLIC`. That revoke doesn’t
replace the stored-procedure revoke for the `SNOWFLAKE.PUBLIC` bootstrap path.

#### Use model objects with supported features

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

#### How RBAC and the allowlist interact

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

### Common pitfalls

- Access to a model (whether by allowlist or RBAC) does not always mean that it can be used. It may still be subject to
  cross-region, [legacy or end-of-life](/user-guide/snowflake-cortex/aisql-regional-availability#label-cortex-model-lifecycle), or other availability constraints. These restrictions can result in error messages that
  seem similar to model access errors. To check which Cortex Base Models are currently available in your account and
  their lifecycle status, use [SHOW CORTEX BASE MODELS](/sql-reference/sql/show-cortex-base-models).
- Model access controls only govern the use of a model and not the use of a feature itself. A feature can have its own access
  controls. For example, access to `AI_COMPLETE` is governed by the `CORTEX_USER` or `AI_FUNCTIONS_USER` database role and the USE AI FUNCTIONS account-level privilege. For more information, see
  [Cortex LLM privileges](#label-cortex-llm-privileges).
- Not all features support model access controls. For more information about what a feature supports, see the [supported features](#label-cortex-llm-model-access-supported-features) table.
- Secondary roles can obscure permissions. For example, if a user has ACCOUNTADMIN as a secondary role, all model objects may appear
  accessible. Disable secondary roles temporarily when verifying permissions.
- Revoking `CORTEX-MODEL-ROLE-ALL` from the account-level PUBLIC role does not remove the
  [bootstrap grant](#label-cortex-model-role-all-bootstrap) on `SNOWFLAKE.PUBLIC`. Use
  `SHOW GRANTS TO APPLICATION ROLE SNOWFLAKE.PUBLIC` to check, and
  `SNOWFLAKE.LOCAL.REVOKE_FROM_PUBLIC_APPLICATION_ROLE` to revoke.
- Qualified model object identifiers are quoted and therefore case-sensitive. For more information, see
  [QUOTED\_IDENTIFIERS\_IGNORE\_CASE](/sql-reference/parameters#label-quoted-identifiers-ignore-case).

### Migrate from the allowlist to RBAC

Because `CORTEX_MODELS_ALLOWLIST` is planned for deprecation, Snowflake recommends migrating to model RBAC. The following steps walk through a complete migration.

#### Step 1: Check your current allowlist

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

#### Step 2: Grant equivalent model application roles

Because `CORTEX_MODELS_ALLOWLIST` applies account-wide, the direct RBAC equivalent is granting model application roles to the PUBLIC role, which is automatically granted to all users. Start by replicating the allowlist behavior exactly, then tighten access to specific roles as needed.

Warning

Granting to PUBLIC is not sufficient in all execution contexts. In the following scenarios, PUBLIC’s grants may not be active, and you must grant model application roles directly to the specific role in use:

- **Secondary roles disabled**: When a session runs `USE SECONDARY ROLES NONE`, only the active primary role’s grants apply. If the active role doesn’t inherit PUBLIC’s model grants through its own role chain, the call will fail.
- **Native Apps**: Native app execution contexts use the app’s own role hierarchy. Account-level PUBLIC grants don’t automatically carry through.

Restricted caller’s rights (RCR) stored procedures are an exception. Model RBAC doesn’t evaluate RCR caller grants in RCR contexts, so granting model application roles to PUBLIC is sufficient for RCR workloads.

Test all your workloads — including stored procedures, native apps, and any session that sets secondary roles — before disabling the allowlist.

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

#### Step 3: Verify access with RBAC

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

#### Step 4: Disable the allowlist

Once you’ve confirmed that RBAC grants are working, disable the allowlist so that RBAC is the only access mechanism:

Copy code

```
USE ROLE ACCOUNTADMIN;

ALTER ACCOUNT SET CORTEX_MODELS_ALLOWLIST = 'None';
```

Setting the allowlist to `'None'` disables the allowlist fallback entirely, so only RBAC grants determine access.

### Supported features

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
| [Cortex REST API](/user-guide/snowflake-cortex/cortex-rest-api) | ✔ | ✔ |  |
| [Cortex Playground](/user-guide/snowflake-cortex/cortex-playground) | ✔ | ✔ |  |
| [Snowflake CoCo](/user-guide/cortex-code/cortex-code) | ✔ | ✔ | Applies to CoCo in Snowsight, CoCo Desktop, and CoCo CLI. The model picker shows only the models the current role can access. |

Expand

Show lessSee more
