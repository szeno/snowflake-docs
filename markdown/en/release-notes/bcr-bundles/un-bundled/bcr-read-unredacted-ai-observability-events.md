# Account Privilege READ UNREDACTED AI OBSERVABILITY EVENTS TABLE

Starting **April 24, 2026**, Snowflake will introduce and enforce a new **account** privilege, **READ UNREDACTED AI OBSERVABILITY EVENTS TABLE**. The privilege controls which **roles** can read **unredacted** content in Cortex Agent observability data from `SNOWFLAKE.LOCAL.AI_OBSERVABILITY_EVENTS` when they use the system table functions and related paths that read that event table. The new privilege is **off** by default for all roles. This unbundled behavior change does **not** change how data is **written** to the table; it only affects visibility of **which columns or fields** a role can see in query results and traces.

The change applies to **agent owners** and to roles with the **MONITOR** privilege on a Cortex Agent when they use observability queries that return content from the event table. The goal is to reduce exposure of potentially sensitive data to roles that are not explicitly granted the new privilege.

**System table functions:** This change applies when you call the **GET\_AI\_** [table functions](/sql-reference/functions-table) that read from `SNOWFLAKE.LOCAL.AI_OBSERVABILITY_EVENTS` (see [LOCAL schema](/sql-reference/local)), for example `GET_AI_OBSERVABILITY_EVENTS` and `GET_AI_OBSERVABILITY_LOGS`. For the full list, see [List of system-defined table functions](/sql-reference/functions-table#label-list-of-system-defined-table-functions); on the **Table functions** page, the **Cortex Agents** rows in the function table name each of these system table functions.

**Exempt from redaction** The following roles still see raw table data via direct access to the `SNOWFLAKE.LOCAL.AI_OBSERVABILITY_EVENTS` table:

> - The `ACCOUNTADMIN`
> - The `AI_OBSERVABILITY_ADMIN` application role
> - The `AI_OBSERVABILITY_READER` application role

Important

Users must **still** hold the **CORTEX\_USER** database role and, when querying a given Cortex Agent, **OWNERSHIP** or **MONITOR** on that agent, to use observability features at all. The new account privilege is **in addition** to that requirement: it only controls **whether raw content fields** (as opposed to metadata) are included in the results the role is allowed to see for data they are already allowed to access.

If **READ UNREDACTED AI OBSERVABILITY EVENTS TABLE** is not granted, roles that otherwise qualify to query observability can still see **metadata**, including:

- Tool **names** and **types**
- Token **usage** and **latency**
- **Evaluation** traces and **scores**
- **Model** name
- **Error** severity

Without an explicit **grant** of the new privilege, the same roles **do not** see the following **raw** content by default:

- **Tool** inputs and outputs
- **Conversation** history
- **Feedback** from users

To grant access to the unredacted observability content to a role, an account administrator runs:

Copy code

```
GRANT READ UNREDACTED AI OBSERVABILITY EVENTS TABLE ON ACCOUNT TO ROLE <role_name>;
```

To **restore the previous default** where every user in the account can see unredacted fields (as long as they still meet the Cortex Agent and **CORTEX\_USER** requirements above), an account administrator can grant the privilege to the **PUBLIC** role. **PUBLIC** is a [system-defined role](/user-guide/security-access-control-overview#label-access-control-overview-roles-system) documented in [Overview of Access Control](/user-guide/security-access-control-overview) ( **PUBLIC** entry). Granting to **PUBLIC** applies the privilege to all users in the account, because **PUBLIC** is automatically available to every user; use only if that matches your security policy.

Copy code

```
GRANT READ UNREDACTED AI OBSERVABILITY EVENTS TABLE ON ACCOUNT TO ROLE PUBLIC;
```

**No** action is required for teams that only need the **metadata** list above and do not need the raw input, output, conversation, or user-feedback text.

**See also**

- [Cortex Agents](/user-guide/snowflake-cortex/cortex-agents)
- [AI Observability with Snowflake Cortex](/user-guide/snowflake-cortex/ai-observability)
