# Set up profile routing in Snowflake CoWork

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

A profile routes each question to the agent best suited to answer it. This topic shows you how to
give your account a profile, starting from either of the two states an account can be in today.

- Your account has agents but no profile. Your users pick an agent themselves. Follow
  [Enable profile routing](#label-cowork-profiles-enable).
- Your account routes every question through a single agent called Main Agent. Follow
  [Migrate from Main Agent](#label-cowork-profiles-migrate).

If you are not sure which one describes your account, see
[Check which setup your account uses](#label-migrate-cowork-profiles-check).

Both paths have a CoWork Admin path and a SQL path. Use CoWork Admin unless you want to choose the
profile’s object name or schema yourself.

Read [About profiles in Snowflake CoWork](/user-guide/snowflake-cortex/snowflake-cowork/about-cowork-profiles) first. Profiles change how you
organize agents, so decide how many profiles you want before you start.

Neither path interrupts Snowflake CoWork, and your users keep working while you do it. Their
existing agents remain available, and the privileges you already granted continue to govern who
can use what.

## Check which setup your account uses

Run the following command, replacing `<si_name>` with the name of your Snowflake CoWork object:

Copy code

```
DESCRIBE SNOWFLAKE INTELLIGENCE <si_name>;
```

If `default_agent` names an agent, your account uses Main Agent. Go to
[Migrate from Main Agent](#label-cowork-profiles-migrate).

If `default_agent` is empty or absent, check whether your account already has a profile:

Copy code

```
SHOW AGENTS IN SCHEMA SNOWFLAKE_INTELLIGENCE.PROFILES;
```

- If the output lists no agent, your account has no profile and no routing. Go to
  [Enable profile routing](#label-cowork-profiles-enable).
- If the output lists an agent, your account already uses profiles. You have nothing to do.

If you do not know the name of your Snowflake CoWork object, run `SHOW SNOWFLAKE INTELLIGENCES;`.
An account can have only one.

Note

The `default_agent` column can name any agent in your account, not only an agent named
`MAIN_AGENT`. What matters is whether the column has a value, not which agent it names.

## Required privileges

CoWork Admin creates whichever of these objects your account doesn’t have yet. They are the
Snowflake CoWork object, the `SNOWFLAKE_INTELLIGENCE` database, its `AGENTS` and `PROFILES`
schemas, and the profile. Snowflake checks the privilege to create each one even when the object
already exists. So the CoWork Admin path needs every privilege marked **Yes** below, even if your
account already has all of these objects. The SQL path creates less, so it needs fewer.

| Privilege | On | Needed for | CoWork Admin | SQL path |
| --- | --- | --- | --- | --- |
| `CREATE SNOWFLAKE INTELLIGENCE` | The account | Creating the Snowflake CoWork object. Checked even when the object already exists. | Yes | No |
| `CREATE DATABASE` | The account | Creating the `SNOWFLAKE_INTELLIGENCE` database. Checked even when the database already exists. | Yes | No |
| `CREATE SCHEMA` | The `SNOWFLAKE_INTELLIGENCE` database | Creating the `AGENTS` and `PROFILES` schemas. Checked even when they already exist. Owning the database includes this privilege. | Yes | Only if `PROFILES` doesn’t exist yet |
| `CREATE AGENT` | The `SNOWFLAKE_INTELLIGENCE.PROFILES` schema | Creating `DEFAULT_PROFILE`. Already covered when CoWork Admin creates the schema for you, because your role then owns it. | Yes | Yes |
| `CREATE AGENT` | The `SNOWFLAKE_INTELLIGENCE.AGENTS` schema | Creating a default agent. CoWork Admin only does this when no agent is attached to the Snowflake CoWork object yet. | Sometimes | No |
| `MODIFY`, or ownership | The Snowflake CoWork object | Attaching the profile. The migrate path also uses this to detach the agents it replaces. | Yes | Yes |
| Ownership | The `SNOWFLAKE_INTELLIGENCE` database, its schemas, or the Snowflake CoWork object | Granting USAGE on an object you own, so your users can reach the profile. | Yes | Yes |
| `MANAGE GRANTS` | The account | Granting USAGE on the `SNOWFLAKE_INTELLIGENCE` database, its schemas, or the Snowflake CoWork object when your role doesn’t own them. | Yes | Yes |

Expand

Show lessSee more

Your primary role, or a role it inherits, needs the account-level and `CREATE` privileges above.
A secondary role doesn’t count for these, even if it’s active. `MODIFY` on the Snowflake CoWork
object counts whether it comes from your primary role or an active secondary role.

`ACCOUNTADMIN` holds the account-level privileges in this table and `MANAGE GRANTS` by default,
which makes it the simplest role to use. That’s enough as long as `ACCOUNTADMIN`, or a role in
its hierarchy, owns the `SNOWFLAKE_INTELLIGENCE` database, its schemas, and your
Snowflake CoWork object. If a different role owns one of them, `ACCOUNTADMIN` can grant itself
the privilege it’s missing, because it holds `MANAGE GRANTS`. For example:

Copy code

```
GRANT CREATE SCHEMA ON DATABASE SNOWFLAKE_INTELLIGENCE TO ROLE ACCOUNTADMIN;
```

Or grant it the owning role instead:

Copy code

```
GRANT ROLE <owner_role> TO ROLE ACCOUNTADMIN;
```

To let a custom role enable routing in CoWork Admin, run the following as `ACCOUNTADMIN`:

Copy code

```
GRANT CREATE SNOWFLAKE INTELLIGENCE ON ACCOUNT TO ROLE <role_name>;
GRANT CREATE DATABASE ON ACCOUNT TO ROLE <role_name>;
```

If the `SNOWFLAKE_INTELLIGENCE` database, its schemas, or your Snowflake CoWork object already
exist and another role owns them, also grant that role to your custom role. Ownership covers
creating schemas and agents in them, attaching the profile, and granting USAGE on them.

Copy code

```
GRANT ROLE <owner_role> TO ROLE <role_name>;
```

The manual steps under [Migrate from Main Agent](#label-cowork-profiles-migrate) need the
privileges in the **SQL path** column. Clearing `default_agent` and detaching agents use the same
`MODIFY` privilege on the Snowflake CoWork object.

These privileges set up and attach a profile. For who can use an existing Snowflake CoWork
object and its agents, see
[Grant Snowflake CoWork privileges](/user-guide/snowflake-cortex/snowflake-cowork/deploy-agents#label-snowflake-cowork-privileges).

### Create a profile in your own database and schema

CoWork Admin always uses the `SNOWFLAKE_INTELLIGENCE` database, so it needs `CREATE DATABASE` even
when the database exists. If your organization does not allow that privilege, or does not want a
`SNOWFLAKE_INTELLIGENCE` database, create the profile with SQL in a database and schema that
already exist. A profile is an agent with an `agent_router` tool that you attach to the
Snowflake CoWork object, so it can live in any schema.

This path needs these privileges. It does not need `CREATE DATABASE`, `CREATE SCHEMA`, or
`CREATE SNOWFLAKE INTELLIGENCE`, as long as your Snowflake CoWork object already exists:

- `CREATE AGENT` on your schema.
- `MODIFY` on the Snowflake CoWork object, to attach the profile.
- Ownership of the database, the schema, and the profile, or `MANAGE GRANTS` on the account, to grant
  USAGE to your users.

To let a team role create profiles, run the following as `ACCOUNTADMIN`. Replace the names with your
own:

Copy code

```
GRANT USAGE ON DATABASE MY_DB TO ROLE <team_role>;
GRANT USAGE ON SCHEMA MY_DB.MY_SCHEMA TO ROLE <team_role>;
GRANT CREATE AGENT ON SCHEMA MY_DB.MY_SCHEMA TO ROLE <team_role>;
GRANT MODIFY ON SNOWFLAKE INTELLIGENCE <si_name> TO ROLE <team_role>;
```

Then follow [Enable routing with SQL](#label-cowork-profiles-enable-sql), and replace
`SNOWFLAKE_INTELLIGENCE.PROFILES` with your database and schema. Grant USAGE on your database and
schema to every role that uses the profile. If a role cannot see your database, it cannot reach the
profile.

A few things differ from a profile in `SNOWFLAKE_INTELLIGENCE.PROFILES`:

- CoWork Admin lists the profile but cannot edit or delete it. Change it with `ALTER AGENT` and
  remove it with `DROP AGENT`.
- The `/cowork-profiles` skill in Cortex Code does not change anything until it has saved a backup.
  It saves the backup to `SNOWFLAKE_INTELLIGENCE.MIGRATION.SI_SNAPSHOTS`, and it creates the
  `MIGRATION` schema if it is missing. Without the `SNOWFLAKE_INTELLIGENCE` database and
  `CREATE SCHEMA` on it, the skill cannot start. Create and attach the profile with SQL instead, and
  record your current setup first, as in step 1 of
  [Migrate manually](#label-cowork-profiles-migrate-manual).

## Enable profile routing

Follow these steps if your account has agents attached to the Snowflake CoWork object and no
profile. The profile you create here names the agents it routes to.

CoWork Admin can do this for you, including the name your users see and the roles that get access.
Use the SQL path if you want to choose the profile’s object name or put it in a different schema.

### Enable routing in CoWork Admin

Before you start, make sure your role has the
[required privileges](#label-cowork-profiles-required-privileges).

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **AI & ML** » **CoWork Admin**.
3. On the **Introducing CoWork profiles for automatic routing** banner, select **Enable profile**.
4. Under **A profile will be created**, review the profile. To change the name your users see,
   select **Edit** next to **Profile name**. Then select **Next: Access**.
5. Under **Give roles access to this profile**, choose the roles that can use the profile. PUBLIC is
   selected by default. Then select **Enable profile**.

To change the profile’s instructions, model, or capabilities later, select the profile on the
**Agents** tab, and then select **Edit profile**.

Note

If your account shows an **Introducing: Automatic Routing** banner instead, select **Enable
routing** on the banner, and then select **Enable routing** in the **Enable automatic routing**
dialog. To set the profile’s instructions, model, or capabilities while you enable it, select
**Configure default profile** instead of **Enable routing**.

The banner appears only while your account has no profile. Once you have one, the banner does not
come back. To add further profiles, select **Create profile** below the list of profiles on the
**Agents** tab. If CoWork Admin shows a **Configuration** tab instead of an **Agents** tab, add
them from the **Configuration** tab.

If the dialog reports that you do not have the required privileges, see
[Required privileges](#label-cowork-profiles-required-privileges) for what your role needs, or ask
an account administrator to grant them and try again.

### Enable routing with SQL

Before you start, make sure your role has the
[required privileges](#label-cowork-profiles-required-privileges).

1. List the agents currently attached to your Snowflake CoWork object. These become the agents
   your profile routes to.

   Copy code

   ```
   SHOW AGENTS IN SNOWFLAKE INTELLIGENCE <si_name>;
   ```
2. Create the profile. Name each agent from step 1 in the `subagents` list. For more information, see
   [Choose which agents a profile routes to](#label-cowork-profiles-routing-scope).

   Copy code

   ```
   CREATE AGENT SNOWFLAKE_INTELLIGENCE.PROFILES.DEFAULT_PROFILE
     FROM SPECIFICATION $$
   mcp_config:
     selection: all
     types:
       - external
   models:
     orchestration: auto
   tools:
     - tool_spec:
         type: agent_router
         name: router
   tool_resources:
     router:
       subagents:
         - name: MY_DB.MY_SCHEMA.SALES_AGENT
           description: Answers questions about pipeline, quota, and closed deals.
         - name: MY_DB.MY_SCHEMA.SUPPORT_AGENT
           description: Answers questions about open tickets and escalations.
   $$;
   ```

   A profile is an agent with an `agent_router` tool that you attach to the Snowflake CoWork object,
   and it can live in any schema. This example uses the `SNOWFLAKE_INTELLIGENCE.PROFILES` schema that CoWork Admin uses. Most accounts already
   have it. If this command fails because the schema does not exist, create it with
   `CREATE SCHEMA IF NOT EXISTS SNOWFLAKE_INTELLIGENCE.PROFILES` and then run step 3. If your
   organization does not allow `CREATE DATABASE` or `CREATE SCHEMA`, see
   [Create a profile in your own database and schema](#label-cowork-profiles-custom-location).
3. Grant your users access at all three levels. Reaching an agent needs USAGE on its database, its
   schema, and the agent itself.

   Copy code

   ```
   GRANT USAGE ON DATABASE SNOWFLAKE_INTELLIGENCE TO ROLE PUBLIC;
   GRANT USAGE ON SCHEMA SNOWFLAKE_INTELLIGENCE.PROFILES TO ROLE PUBLIC;
   GRANT USAGE ON AGENT SNOWFLAKE_INTELLIGENCE.PROFILES.DEFAULT_PROFILE TO ROLE PUBLIC;
   ```

   Run all three even when the database and schema already existed. Granting the agent alone breaks
   the chain one level up, and CoWork Admin then reports that it cannot show profiles while the
   profile itself works.

   To limit the profile to a subset of users, grant USAGE to a role those users hold instead of to
   PUBLIC.
4. Attach the profile to your Snowflake CoWork object.

   Copy code

   ```
   ALTER SNOWFLAKE INTELLIGENCE <si_name>
     ADD AGENT SNOWFLAKE_INTELLIGENCE.PROFILES.DEFAULT_PROFILE;
   ```
5. Open Snowflake CoWork as one of your users and ask a question. The profile selects an agent and
   answers.

Name the agents the profile routes to in its `subagents` list. For more information, see
[Choose which agents a profile routes to](#label-cowork-profiles-routing-scope).

## Migrate from Main Agent

Follow these steps if `default_agent` names an agent. Migrating replaces that agent with a profile.

Note

Record the current value of `default_agent` before you start. Clearing the property discards it, and
rolling back requires the original agent name.

Choose one of the following paths:

- **Recommended:** [Migrate in CoWork Admin](#label-cowork-profiles-migrate-admin).
- **Alternative:** [Migrate with Cortex Code](#label-cowork-profiles-migrate-coco).
- **Fallback:** [Migrate manually](#label-cowork-profiles-migrate-manual), if you can use neither
  CoWork Admin nor Cortex Code.

Automations that call your Main Agent directly keep working on every path. A user sees the new
experience only when their role has access to at least one profile. Users without that access keep
the previous experience.

To move one role at a time instead of
[Migrate in CoWork Admin](#label-cowork-profiles-migrate-admin), see
[Roll out a profile gradually by role](#label-cowork-profiles-gradual-rollout). To build the
profile before you attach it, see
[Test a profile before you migrate](#label-cowork-profiles-test-before-migrate).

### Roll out a profile gradually by role

In Cortex Code, run `/cowork-profiles` for this rollout. Don’t do this rollout in CoWork Admin or
from the **Upgrade to CoWork Profiles** banner.
[Migrate in CoWork Admin](#label-cowork-profiles-migrate-admin) and
[Migrate with Cortex Code](#label-cowork-profiles-migrate-coco) start from that banner.

A profile is an agent, so access follows the roles you grant.

- A user with access to at least one profile sees the new experience, which has no top-level
  agent picker. A user with access to more than one profile also gets a profile picker.
- A user with access to no profile keeps the previous experience, even when a profile is attached
  to the Snowflake CoWork object. This holds only while your Main Agent isn’t attached to the
  Snowflake CoWork object. An attached Main Agent counts as a profile. See
  [Keep your Main Agent as a profile while you test](#label-cowork-profiles-keep-main-agent).

1. Grant USAGE on the profile to one role, not to PUBLIC. The role also needs USAGE on the
   `SNOWFLAKE_INTELLIGENCE` database and the `PROFILES` schema, as in step 3 of
   [Test a profile before you migrate](#label-cowork-profiles-test-before-migrate).
2. Leave your Main Agent in place. Users whose roles don’t have USAGE on the profile stay on the
   previous experience.
3. Grant USAGE on the profile to the next role when you want more people on it. Repeat for each
   role.

### Keep your Main Agent as a profile while you test

You don’t have to remove your Main Agent from your Snowflake CoWork object to adopt profiles. You
can keep it attached next to a new profile, try the profile with a few roles, and detach the Main
Agent once testing is done.

This works because Snowflake CoWork treats any attached agent that has an `agent_router` tool as a
profile, whichever schema it is in. Your Main Agent has that tool, so while it stays attached:

- Users whose roles have USAGE on the Main Agent see it as a profile.
- Users whose roles also have USAGE on the new profile see both, and switch between them with the
  profile picker.

To keep your Main Agent during the test:

1. Back up your current setup and create the profile, as in steps 1 to 3 of
   [Test a profile before you migrate](#label-cowork-profiles-test-before-migrate). Grant USAGE
   on the profile only to the roles that test it, such as `ACCOUNTADMIN` or a BI role.
2. Migrate with Cortex Code, and tell `/cowork-profiles` to keep your Main Agent attached. It
   clears `default_agent` and gives your Main Agent a fixed list of the agents it routes to before
   it detaches the other agents. Your Main Agent then keeps routing to the same agents.
3. Ask the profile the questions your users ask today, as one of the test roles.
4. When testing is done, detach your Main Agent and grant USAGE on the profile to the roles that
   should use it:

   Copy code

   ```
   ALTER SNOWFLAKE INTELLIGENCE <si_name> DROP AGENT SNOWFLAKE_INTELLIGENCE.AGENTS.MAIN_AGENT;
   ```

Note

Detach your Main Agent. Don’t drop it, and don’t revoke USAGE on it. Automations call your Main
Agent directly, and they stop working if you drop it or revoke USAGE on it. Detaching doesn’t
affect them.

Your Main Agent stays in the `AGENTS` schema during the test, so the profiles page in CoWork Admin
doesn’t list it.

### Test a profile before you migrate

You can build and test the profile while your Main Agent keeps serving everyone. Create the profile
without attaching it to your Snowflake CoWork object, test it with a small group, and then migrate.

1. Back up your current setup. In Cortex Code, run `/cowork-profiles` and ask it for a backup of
   your Snowflake CoWork object. Record the snapshot ID.
2. Create the profile from your Main Agent’s specification, as described in steps 1 to 3 of
   [Migrate manually](#label-cowork-profiles-migrate-manual). Alternatively, in Cortex Code, ask
   `/cowork-profiles` to create the profile and tell it not to attach the profile or set it as the
   default.
3. Grant access only to a role your testers hold, instead of to PUBLIC.

   Copy code

   ```
   GRANT USAGE ON DATABASE SNOWFLAKE_INTELLIGENCE TO ROLE <test_role>;
   GRANT USAGE ON SCHEMA SNOWFLAKE_INTELLIGENCE.PROFILES TO ROLE <test_role>;
   GRANT USAGE ON AGENT SNOWFLAKE_INTELLIGENCE.PROFILES.DEFAULT_PROFILE TO ROLE <test_role>;
   ```
4. Don’t attach the profile, and don’t change `default_agent`. Your users keep using your Main
   Agent and don’t see the profile.
5. Ask the profile the questions your users ask today, and check that it routes each one to the
   right agent. Because the profile isn’t attached, test it outside Snowflake CoWork. See
   [Call a Snowflake CoWork profile from the Cortex Agents API](/user-guide/snowflake-cortex/snowflake-cowork/call-cowork-profile-from-api).
6. When you are satisfied, finish the migration. Grant USAGE on the profile to PUBLIC, or to the
   roles that should use it, and then complete steps 6 to 8 of
   [Migrate manually](#label-cowork-profiles-migrate-manual). Or ask `/cowork-profiles` in Cortex
   Code to finish the migration with the profile you created.

Note

Leave the profile unattached for this test. Your users keep using your Main Agent, as in step 4.
A profile is an agent, so if you attach it, only roles with USAGE on it see it.

### Migrate in CoWork Admin

CoWork Admin creates a profile that routes to the same agents as your Main Agent, attaches it, and
stops using your Main Agent as the default.

1. Back up your current setup. In Cortex Code, run `/cowork-profiles` and ask it for a backup of
   your Snowflake CoWork object. Run it as `ACCOUNTADMIN`, so the snapshot covers every agent.
   Cortex Code saves the snapshot to `SNOWFLAKE_INTELLIGENCE.MIGRATION.SI_SNAPSHOTS`. Record the
   snapshot ID. You need it to [roll back](#label-cowork-profiles-rollback).
2. Use a role that can run the migration. `ACCOUNTADMIN` works. Another role needs `MANAGE GRANTS`
   on the account, `MODIFY` on your Main Agent and on your Snowflake CoWork object, and
   `CREATE SCHEMA` on the `SNOWFLAKE_INTELLIGENCE` database. For details, see
   [Required privileges](#label-cowork-profiles-required-privileges).
3. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
4. In the navigation menu, select **AI & ML** » **CoWork Admin**.
5. On the **Upgrade to CoWork Profiles** banner, select **Migrate automatically**.
6. Review the preview, then select **Migrate**.

When the migration finishes, CoWork Admin shows **Migrated to CoWork Profiles**. To check the
result, see [Confirm the migration worked](#label-cowork-profiles-confirm).

If a step fails, the dialog shows the failed step and its error. You then have two options:

- **Resume.** Fix the cause, such as a missing privilege, then select **Check again** and
  **Migrate**. To troubleshoot in Cortex Code instead, select **Validate with CoCo**.
- **Undo.** Restore the snapshot from step 1. See
  [Roll back the migration](#label-cowork-profiles-rollback).

### Migrate with Cortex Code

Cortex Code can do the whole migration in a conversation. Use this path if you prefer to review
each command as it runs.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **AI & ML** » **CoWork Admin**.
3. On the **Upgrade to CoWork Profiles** banner, select **Migrate with CoCo**.
4. Review the plan that Cortex Code presents. To run it, enter `CONFIRM`.

Cortex Code seeds the new profile from your Main Agent’s specification, so its instructions, model,
tools, MCP servers, and routing carry over unchanged. It records a snapshot of the state it found
before it changes anything, and it shows you every command before it runs one. Record the snapshot
ID it reports. You need it to [roll back](#label-cowork-profiles-rollback).

To keep your Main Agent in your Snowflake CoWork object, so your team can still chat with it, ask
Cortex Code to keep it attached. Before it clears `default_agent`, Cortex Code gives your Main Agent an
explicit list of the agents it routes to, as step 4 of [Migrate manually](#label-cowork-profiles-migrate-manual)
describes. Your users then see both the Main Agent and the new profile, and they can choose either.

If you can use neither CoWork Admin nor Cortex Code, migrate manually using the next section. The
manual path carries nothing over on your behalf, so plan to copy the configuration across yourself.

### Migrate manually

A profile inherits nothing from your Main Agent. Creating one does not copy the Main Agent’s
instructions, model, tools, or MCP servers, so you carry that configuration across yourself in
step 3. Skipping it gives your users a profile that routes correctly and behaves nothing like the
agent they had before.

Do these steps in order. Step 7 must come before step 8, because the `default_agent` property
determines which agents your Main Agent routes to while that property is still set.

1. Record the current state. Rolling back needs both values, and clearing `default_agent` in step 7
   discards it.

   Copy code

   ```
   DESCRIBE SNOWFLAKE INTELLIGENCE <si_name>;
   SHOW AGENTS IN SNOWFLAKE INTELLIGENCE <si_name>;
   ```

   The first command returns `default_agent`, which names your Main Agent. The second lists the
   agents attached to your Snowflake CoWork object. Those agents become the agents your new profile
   routes to.
2. Save your Main Agent’s specification.

   Copy code

   ```
   DESCRIBE AGENT SNOWFLAKE_INTELLIGENCE.AGENTS.MAIN_AGENT;
   ```

   Keep the `agent_spec` value from the output. It holds the instructions, model, tools, and MCP
   servers your users depend on today, and step 3 rebuilds the profile from it.
3. Create the profile from the specification you saved. Keep the `models`, `instructions`, `tools`,
   and `mcp_servers` blocks as they were. Add an `agent_router` tool if the specification does not
   already have one, then name one `subagents` entry for each agent from step 1.

   Copy code

   ```
   CREATE AGENT SNOWFLAKE_INTELLIGENCE.PROFILES.DEFAULT_PROFILE
     FROM SPECIFICATION $$
   models:
     orchestration: auto
   instructions:
     response: |
       Your Main Agent's response instructions, unchanged.
     orchestration: |
       Your Main Agent's orchestration instructions, unchanged.
   tools:
     - tool_spec:
         type: agent_router
         name: router
     - tool_spec:
         type: web_search
         name: web_search
   mcp_servers:
     - server_spec:
         name: MY_DB.MY_SCHEMA.MY_MCP_SERVER
   tool_resources:
     router:
       subagents:
         - name: MY_DB.MY_SCHEMA.SALES_AGENT
           description: Answers questions about pipeline, quota, and closed deals.
         - name: MY_DB.MY_SCHEMA.SUPPORT_AGENT
           description: Answers questions about open tickets and escalations.
   $$;
   ```

   The `agent_router` tool is what makes this agent a profile. The key under `tool_resources` must
   match the router tool’s `name`, which is `router` in this example. If the two do not match,
   the profile cannot read its own subagent list.

   A profile is an agent with an `agent_router` tool that you attach to the Snowflake CoWork object,
   and it can live in any schema. This example uses the `SNOWFLAKE_INTELLIGENCE.PROFILES` schema that CoWork Admin uses. Most accounts already
   have it. If this command fails because the schema does not exist, create it with
   `CREATE SCHEMA IF NOT EXISTS SNOWFLAKE_INTELLIGENCE.PROFILES` and then run step 5. If your
   organization does not allow `CREATE DATABASE` or `CREATE SCHEMA`, see
   [Create a profile in your own database and schema](#label-cowork-profiles-custom-location).

   Set each `subagents` entry’s `name` to the agent’s fully qualified name. `description` is optional.
   The profile reads it when choosing an agent, and uses it to tell users which agent they can’t
   access.
4. Optional. Keep your Main Agent in your Snowflake CoWork object, so your team can still chat with
   it. Your Main Agent has no `subagents` list, so after you clear `default_agent` in step 7 it would
   route to every agent attached to the object, including the new profile. Give it an explicit list
   first. Name the agents it routes to today, which are the agents from step 1, and leave out the new
   profile.

   Copy code

   ```
   ALTER AGENT SNOWFLAKE_INTELLIGENCE.AGENTS.MAIN_AGENT
     MODIFY LIVE VERSION SET SPECIFICATION =
     $$
   <the agent_spec from step 2, unchanged, with this block added:>
   tool_resources:
     <name of the agent_router tool in that spec>:
       subagents:
         - name: MY_DB.MY_SCHEMA.SALES_AGENT
           description: Answers questions about pipeline, quota, and closed deals.
         - name: MY_DB.MY_SCHEMA.SUPPORT_AGENT
           description: Answers questions about open tickets and escalations.
     $$;
   ```

   The new specification replaces the old one, so copy every block from step 2 into it. Without
   the list, Main Agent can also send questions to the new profile, which your users don’t get
   today. If you skip this step, don’t keep your Main Agent attached in step 8.
5. Grant your users access at all three levels. Reaching an agent needs USAGE on its database, its
   schema, and the agent itself.

   Copy code

   ```
   GRANT USAGE ON DATABASE SNOWFLAKE_INTELLIGENCE TO ROLE PUBLIC;
   GRANT USAGE ON SCHEMA SNOWFLAKE_INTELLIGENCE.PROFILES TO ROLE PUBLIC;
   GRANT USAGE ON AGENT SNOWFLAKE_INTELLIGENCE.PROFILES.DEFAULT_PROFILE TO ROLE PUBLIC;
   ```

   Run all three even when the database and schema already existed, because they are the accounts
   most likely to be missing the schema grant. Granting the agent alone breaks the chain one level
   up, and a broken chain does not read as a permission error. CoWork Admin reports that it cannot
   show profiles, while the profile itself exists, is attached, and routes correctly.

   To limit the profile to a subset of users, grant USAGE to a role those users hold instead of to
   PUBLIC. Granting to PUBLIC reaches every role in your account.
6. Attach the profile to your Snowflake CoWork object.

   Copy code

   ```
   ALTER SNOWFLAKE INTELLIGENCE <si_name>
     ADD AGENT SNOWFLAKE_INTELLIGENCE.PROFILES.DEFAULT_PROFILE;
   ```
7. Clear the `default_agent` property.

   Copy code

   ```
   ALTER SNOWFLAKE INTELLIGENCE <si_name> UNSET DEFAULT_AGENT;
   ```
8. Detach each agent you listed in step 1. Your users now reach these agents through the profile,
   so leaving them attached shows one entry per agent instead of one entry per profile.

   Copy code

   ```
   ALTER SNOWFLAKE INTELLIGENCE <si_name> DROP AGENT MY_DB.MY_SCHEMA.SALES_AGENT;
   ALTER SNOWFLAKE INTELLIGENCE <si_name> DROP AGENT MY_DB.MY_SCHEMA.SUPPORT_AGENT;
   ```

   Detach only the agents you named as subagents in step 3. If you kept your Main Agent in step 4, do
   not detach it. Detaching an agent the profile does not
   route to removes its only route, and your users can no longer reach it in Snowflake CoWork.
   Detaching leaves the agent itself in place, so keep your Main Agent for as long as you might roll
   back.

### Confirm the migration worked

1. Confirm that `default_agent` is no longer set:

   Copy code

   ```
   DESCRIBE SNOWFLAKE INTELLIGENCE <si_name>;
   ```
2. Confirm that the profile is attached and the individual agents are not:

   Copy code

   ```
   SHOW AGENTS IN SNOWFLAKE INTELLIGENCE <si_name>;
   ```

   The output lists your profile. It does not list the agents you detached in step 8.
3. Open Snowflake CoWork as one of your users and ask a question that the routed agents can
   answer. The profile selects an agent and answers.

### Roll back the migration

Rolling back returns your account to routing through Main Agent. How you roll back depends on
whether you have a snapshot.

#### Roll back from a snapshot

Use this path if you migrated in CoWork Admin or with Cortex Code and recorded a snapshot ID.

1. In Cortex Code, run `/cowork-profiles` and ask it to roll back to your snapshot ID.
2. Ask it to restore `default_agent` as well. Otherwise `default_agent` stays unset, and your users
   keep starting in the profile.
3. Review each change that Cortex Code previews, then enter `CONFIRM`.

#### Roll back with SQL

Use this path if you migrated manually or have no snapshot. Do these steps in order, using the
`default_agent` value you recorded before migrating.

Important

Setting `default_agent` back to your Main Agent fails if that agent names its own subagents. A
default agent has to route over whatever is attached to the Snowflake CoWork object, so it cannot
carry a `subagents` list of its own. Many Main Agents carry one, because that combination was
allowed before profiles existed.

Check the specification you saved in step 2 of the migration before you start. If it has a
`subagents` list under `tool_resources`, you cannot restore both the list and the default. Choose
which one to keep:

- Recreate the Main Agent with an empty `subagents` list, then set it as the default. Routing falls
  back to whatever is attached to the Snowflake CoWork object, which matches the original behavior
  as long as you re-attach every agent in step 1.
- Keep the Main Agent’s `subagents` list and leave `default_agent` unset. The specification stays
  exact, and your users reach the agent by selecting it rather than landing on it.

1. Re-attach each agent you detached.

   Copy code

   ```
   ALTER SNOWFLAKE INTELLIGENCE <si_name> ADD AGENT MY_DB.MY_SCHEMA.SALES_AGENT;
   ALTER SNOWFLAKE INTELLIGENCE <si_name> ADD AGENT MY_DB.MY_SCHEMA.SUPPORT_AGENT;
   ```
2. Set `default_agent` back to the agent that was routing before.

   Copy code

   ```
   ALTER SNOWFLAKE INTELLIGENCE <si_name>
     SET DEFAULT_AGENT = SNOWFLAKE_INTELLIGENCE.AGENTS.MAIN_AGENT;
   ```

   If this command reports that the agent has pre-configured subagents, recreate the agent with an
   empty `subagents` list and run the command again.
3. Detach the profile.

   Copy code

   ```
   ALTER SNOWFLAKE INTELLIGENCE <si_name>
     DROP AGENT SNOWFLAKE_INTELLIGENCE.PROFILES.DEFAULT_PROFILE;
   ```

The profile still exists after you detach it, so you can attach it again when you migrate. To remove
it, run `DROP AGENT SNOWFLAKE_INTELLIGENCE.PROFILES.DEFAULT_PROFILE`.

## Choose which agents a profile routes to

A profile has capability of its own. It carries a model, the MCP servers you gave it, and any skills
you added, so a profile can answer a question directly rather than route it. Naming subagents adds
routing to that.

The `subagents` list sets which agents the profile routes to. The profile routes to exactly the
agents you name, on every surface where it runs. Attaching another agent to the Snowflake CoWork
object does not add it to the profile.

Each `agent_router` tool needs a `tool_resources` entry with a `subagents` list. Set `subagents: []`
for direct answers without routing.

### Listing an agent does not grant access

Naming an agent in `subagents` gives no one access to it. A user can run a listed agent only when
their role has USAGE on the agent, its schema, and its database. You can therefore list every
production-ready agent in one profile and let role grants decide who reaches which agent.

When a user’s role lacks USAGE on a listed agent, the profile can’t route to it. By default the run
continues with the agents that user can reach, and a warning names the agent they can’t. For
more information, see
[Call a profile from the Cortex Agents API](/user-guide/snowflake-cortex/snowflake-cowork/call-cowork-profile-from-api#label-call-cowork-profile-from-api)
and [Inaccessible tool handling](/user-guide/snowflake-cortex/cortex-agents-inaccessible-tool-handling).

The profile reads each listed agent’s name and description when it chooses an agent, and a warning
can show the name of an agent the user can’t access. Treat both as visible to the profile’s users,
and write descriptions that are safe for all of them to read.

## Resolve errors

| Message | What to do |
| --- | --- |
| The agent name contains `$$`. | Rename the agent, or remove it from Snowflake CoWork, then migrate again. The specification delimiter cannot appear in a name it encloses. |
| The profile specification contains `$$`. | Remove the `$$` from the specification. It most often appears in the instructions. |
| A `subagents` entry names no agent. | Give the entry a `name`, or delete the entry. No agent was detached and your specification was not changed. |
| The specification declares no `router` tool. | Add an `agent_router` tool to the specification. Without one, the agent is not a profile and has no subagent list. |
| The `tool_resources` block is not a mapping. | Correct the indentation so that `tool_resources` contains a key matching your router tool name. |
| The profile was created but USAGE could not be granted to PUBLIC. | Grant USAGE using a role that owns the profile. Until you do, your users cannot use Snowflake CoWork. |
| The current `default_agent` cannot be read. | Confirm you have MODIFY on the Snowflake CoWork object, then migrate again. No agent was detached. |
| CoWork Admin cannot show profiles, but the profile answers questions in Snowflake CoWork. | Grant USAGE on the database and schema that hold the profile to the roles that need it. For a profile that CoWork Admin created, that is `SNOWFLAKE_INTELLIGENCE.PROFILES`. Listing profiles reads the schema, and USAGE on the agent alone does not cover it. |
| The agent has pre-configured subagents in its `agent_router` tool resources. | You are setting `default_agent` to an agent that names its own subagents. Recreate that agent with an empty `subagents` list, then set it as the default. |
| Creating a schema in `SNOWFLAKE_INTELLIGENCE` fails even though the schema already exists. | See [Required privileges](#label-cowork-profiles-required-privileges). Your role needs `CREATE SCHEMA` on the database. |
| Enabling routing reports that your role must have `CREATE SNOWFLAKE INTELLIGENCE` granted on `ACCOUNT`, even though the object already exists. | See [Required privileges](#label-cowork-profiles-required-privileges). This privilege is checked even when the Snowflake CoWork object exists. |

Expand

Show lessSee more

## What to do next

You now have one profile that serves everyone. From here you can split it by job function, so a
functional lead owns their team’s agents and routing instructions while you keep the general profile
for everyone else. For guidance on choosing a boundary between profiles, see
[About profiles in Snowflake CoWork](/user-guide/snowflake-cortex/snowflake-cowork/about-cowork-profiles).
