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

Model access is separate from the AI function privileges on this page. Use role-based access control (RBAC) on the model objects in the `SNOWFLAKE.MODELS` schema, or the legacy `CORTEX_MODELS_ALLOWLIST` parameter, to control which roles can use each model. For details, see [Model access control](/user-guide/snowflake-cortex/governance-and-availability/model-access-control).
