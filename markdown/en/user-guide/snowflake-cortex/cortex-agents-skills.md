# Agent skills

A skill is a modular, portable package of instructions, scripts, and context that gives agents
the capability to perform specific, repeatable tasks. You can reference skills stored in a named stage or a Git
repository and Cortex Agents discover them automatically for use in orchestration.

To create reusable workflows as a business user inside Snowflake CoWork, without authoring `SKILL.md` files,
see [User skills](/user-guide/snowflake-cortex/snowflake-cowork/user-skills).

## How skills work

When an agent receives a user query, it evaluates the name and description of each configured skill. If
the agent identifies a skill as relevant, it retrieves the full instructions and any supporting scripts from
the `SKILL.md` file and executes the skill. Skills follow a discovery-and-execution model. The agent doesn’t
persist a copy of the skill files, it only references the skill files in their original location and reads them
on demand during orchestration.

### SKILL.md file structure

Each skill is defined by a `SKILL.md` file that contains the following:

- A skill name
- A description of the skill
- Instructions for the agent
- Optional script references

Each skill folder must contain a `SKILL.md` file at its root. The file defines the skill’s identity, instructions,
and any associated scripts. The following example shows the structure of the skill folder:

Copy code

```
skills/
  forecaster/
    SKILL.md
    forecaster.py
  planner/
    SKILL.md
    planner.py
```

The `SKILL.md` file includes the following fields:

| Field | Required | Description |
| --- | --- | --- |
| name | Yes | Unique identifier for the skill |
| description | Yes | Brief summary used by the agent during orchestration to determine relevance |
| instructions | Yes | Detailed instructions the agent follows when executing the skill |

Expand

Show lessSee more

### Skill discovery

Cortex Agents reference the `SKILL.md` files at the root of each skill folder. The agent scans the stage contents
for `SKILL.md` files and returns the skill name, description, and file location.

### Skill orchestration

During agent invocation, the agent orchestrator uses the name and description of every skill referenced in the
agent to decide which skills are relevant to the user’s query. If a skill is selected, the agent retrieves the
full `SKILL.md` content, including detailed instructions and script paths, from the source location.

## Skill sources

You can store skills in one of the two following types of locations:

- Named stages
- Git repositories

### Named stages

The following example shows how to store skill folders in a Snowflake named stage.

Snowsight UISQL

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. Navigate to the database and schema where you want to create the stage.
3. Create a stage named `skill_stage`.
4. Upload the skill files to the stage, placing them in the `skills/forecaster/` path.

1. Create a stage for skills.

   Copy code

   ```
   CREATE STAGE IF NOT EXISTS db1.schema1.skill_stage;
   ```
2. Upload skill files to the stage.

   Copy code

   ```
   PUT file:///path/to/forecaster/SKILL.md @db1.schema1.skill_stage/skills/forecaster/;
   PUT file:///path/to/forecaster/forecaster.py @db1.schema1.skill_stage/skills/forecaster/;
   ```

### Git repositories

The following example shows how to reference skills located in a Snowflake Git repository. You can point to a
specific commit hash for stability or a tag for automatic updates:

Snowsight UISQL

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. Navigate to the Git repository integration where your skills are stored.
3. Reference the skill at a specific commit hash for stability, or use a tag for automatic updates after a FETCH.

Copy code

```
-- Reference a skill at a specific commit
@my_db.my_schema.skills_repo/commits/abc123def/skills/forecaster

-- Reference a skill at a tag (updates automatically on fetch)
@my_db.my_schema.skills_repo/tags/latest/skills/forecaster
```

Note

When you reference a Git tag, the skill updates automatically after the account admin runs a FETCH on the
repository. Commit hash references are immutable.

### Cortex Extensions

You can reference a [Cortex Extension](/user-guide/cortex-code/cortex-code-skill-plugin-sharing) by fully qualified name
(FQN) instead of listing each of its skills individually. At request time, Snowflake expands the reference into
the extension’s individual skills, so the agent orchestrator sees each member skill directly. Updates to the
extension flow to every agent that references it, and access is controlled by the `READ` privilege on the
extension object.

Set the skill source `type` to `CORTEX_EXTENSION` and `path` to the extension’s FQN. For `PLUGIN`-type extensions
(which bundle multiple skills), the outer skill `name` is optional because member skill names are derived from the
extension’s `skills/<member_name>/` subdirectories. For `SKILL`-type extensions (single-skill), `name` is required.

| Field | Required | Description |
| --- | --- | --- |
| type | Yes | Must be `CORTEX_EXTENSION`. |
| path | Yes | The extension FQN in `DATABASE.SCHEMA.EXTENSION_NAME` form. |
| version | No | Pins which committed version of the extension to expand. Accepts a concrete version name (for example, `VERSION$2`) or an alias (for example, `LAST`, `DEFAULT`). When omitted, Snowflake uses the extension’s default version and falls back to the last committed version. `LIVE` references are rejected during runtime skill resolution, not agent creation. |

Expand

Show lessSee more

At request time, each `skills/<member_name>/` subdirectory in the resolved version expands into a `STAGE` skill
whose path encodes the concrete version, for example:

```
snow://cortex_extension/MY_DB.MY_SCHEMA.MY_EXTENSION/versions/VERSION$2/skills/forecaster
```

`DESCRIBE AGENT` returns the unexpanded `CORTEX_EXTENSION` reference as stored in the specification.

#### Conflict resolution

When a skill name appears in more than one place, the following order applies:

- A skill listed explicitly in the `skills` array wins over a skill of the same name contributed by a
  `CORTEX_EXTENSION` reference. Use this to override a single member skill of a referenced extension.
- When two `CORTEX_EXTENSION` references contribute the same skill name, the later entry in the `skills` array
  wins.

## Manage skills

### List available skills

List all skills available in a named stage or git repository:

Copy code

```
LS @db1.schema1.stage1/ PATTERN='.*SKILL\.md';
```

The output shows each skill’s name, description, and file location:

| Name | Size | Checksum | Last Modified |
| --- | --- | --- | --- |
| skill\_stage/forecaster/SKILL.md | 1008 | 1232131231231 | Tue March 10 2026 02:45 GMT |
| skill\_stage/planner/SKILL.md | 2001 | 1231231231231 | Tue March 10 2026 02:45 GMT |

Expand

Show lessSee more

### List skills on an agent

View all skills configured on a specific agent:

Copy code

```
DESCRIBE AGENT db1.schema1.my_agent;
```

The output returns a JSON structure with each skill’s name and source URL.

### Add a skill to an agent

Add a skill to a Cortex Agent by updating the agent specification. You can use the Snowsight UI, SQL,
or the REST API. The description field is optional. If omitted, Snowflake reads the description from the
skill’s `SKILL.md` file.

Snowsight UISQLAPI

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. Navigate to the **Skills** tab.
3. Select **Add Skill** and choose **Stage** or **Git** as the source.
4. For a stage source, provide the name of the stage and the skill folder path.
5. For a Git source, provide the repository path to the skill.
6. Select **Add Skill**.

To add a skill from a Snowflake named stage:

Copy code

```
ALTER AGENT db1.schema1.my_agent
  MODIFY LIVE VERSION
   SET SPECIFICATION = $$
    {
     //Please include all existing non-changed fields as well
      "skills": [
        {
          "name": "forecaster",
          "source": {
            "type": "STAGE",
            "path": "@db1.schema1.stage1/skills/forecaster"
          }
        }
      ]
    }
  $$;
```

To add a skill from a Git repository:

Copy code

```
ALTER AGENT db1.schema1.my_agent
  MODIFY LIVE VERSION
   SET SPECIFICATION = $$
    {
     //Please include all existing non-changed fields as well
      "skills": [
        {
          "name": "forecaster",
          "source": {
            "type": "GIT",
            "path": "@my_db.my_schema.skills_repo/tags/latest/skills/forecaster"
          }
        }
      ]
    }
  $$;
```

To reference a Cortex Extension, so that all skills bundled in the extension are added to the
agent:

Copy code

```
ALTER AGENT db1.schema1.my_agent
  MODIFY LIVE VERSION
   SET SPECIFICATION = $$
    {
     //Please include all existing non-changed fields as well
      "skills": [
        {
          "source": {
            "type": "CORTEX_EXTENSION",
            "path": "MY_DB.MY_SCHEMA.MY_EXTENSION"
          }
        }
      ]
    }
  $$;
```

To pin the extension to a specific committed version, add a `version` field alongside `path`, for example
`"version": "VERSION$2"`.

To add a skill from a Snowflake named stage:

Copy code

```
PUT /api/v2/databases/{database}/schemas/{schema}/agents/{name}
{
    "name": "my_agent",
    "comment": "Agent with skill capabilities",
    "spec": {
        "models": {
            "orchestration": "claude-sonnet-4-6"
        },
        "instructions": {
            "response": "Provide concise forecasts and analysis."
        },
        "skills": [
            {
                "name": "forecaster",
                "source": {
                    "type": "STAGE",
                    "path": "@db1.schema1.stage1/skills/forecaster"
                }
            }
        ]
    }
}
```

To add a skill from a Git repository:

Copy code

```
PUT /api/v2/databases/{database}/schemas/{schema}/agents/{name}
{
    "name": "my_agent",
    "comment": "Agent with skill capabilities",
    "spec": {
        "models": {
            "orchestration": "claude-sonnet-4-6"
        },
        "instructions": {
            "response": "Provide concise forecasts and analysis."
        },
        "skills": [
            {
                "name": "forecaster",
                "source": {
                    "type": "GIT_INTEGRATION",
                    "path": "@my_db.my_schema.skills_repo/tags/latest/skills/forecaster"
                }
            }
        ]
    }
}
```

To reference a Cortex Extension from a persisted agent spec, so that all skills bundled in the
extension are added to the agent:

Copy code

```
PUT /api/v2/databases/{database}/schemas/{schema}/agents/{name}
{
    "name": "my_agent",
    "spec": {
        "models": {
            "orchestration": "claude-sonnet-4-6"
        },
        "skills": [
            {
                "source": {
                    "type": "CORTEX_EXTENSION",
                    "path": "MY_DB.MY_SCHEMA.MY_EXTENSION"
                }
            }
        ]
    }
}
```

You can also pass a `CORTEX_EXTENSION` reference inline to the stateless `agent:run` endpoint, without persisting
an agent. Snowflake expands the reference into the extension’s individual skills for that single request. The
`experimental` field with `ReasoningAgentToolConfig` is required to enable tool use on the stateless endpoint:

Copy code

```
POST /api/v2/cortex/agent:run
{
    "model": "claude-sonnet-4-6",
    "messages": [
        { "role": "user", "content": [{ "type": "text", "text": "Forecast Q4 revenue." }] }
    ],
    "skills": [
        {
            "name": "my-extension",
            "source": {
                "type": "CORTEX_EXTENSION",
                "path": "MY_DB.MY_SCHEMA.MY_EXTENSION",
                "version": "VERSION$2"
            }
        }
    ],
    "experimental": {
        "ReasoningAgentToolConfig": {
            "OrchestrationType": "reasoning"
        }
    }
}
```

### Update a skill

To update a skill’s content, modify the `SKILL.md` file and any associated scripts at the source location. All
agents that reference the skill automatically use the updated version on their next invocation.

To update a skill’s metadata in the agent specification (for example, the description), use the same PUT endpoint
with the updated values.

### Remove a skill from an agent

Remove a skill from an agent using the Snowsight UI, SQL, or the REST API. The remaining skills
continue to function.

Snowsight UISQLAPI

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. Navigate to the **Skills** tab.
3. Select the skill you want to remove and delete it.
4. Select **Save**.

Copy code

```
ALTER AGENT db1.schema1.my_agent
  MODIFY LIVE VERSION
   SET SPECIFICATION = $$
    {
      "skills": []
    }
  $$;
```

Update the agent specification and omit the skill from the skills array:

Copy code

```
PUT /api/v2/databases/{database}/schemas/{schema}/agents/{name}
{
    "name": "my_agent",
    "comment": "Agent with skill capabilities",
    "spec": {
        "models": {
            "orchestration": "claude-sonnet-4-6"
        },
        "instructions": {
            "response": "Provide concise forecasts and analysis."
        },
        "skills": [
        ]
    }
}
```

### Add an existing skill to another agent

You can add the same skill to multiple agents by referencing the same source path in each agent’s specification.
Because skills are referenced and not copied, updates to the skill files apply to all agents that use the skill.

### Skills with code

If your skills need to execute code, you must enable the [code execution tool](/user-guide/snowflake-cortex/cortex-agents-code-execution-tool) on the agent. All scripts referenced by a skill must be located in the same folder as the `SKILL.md` file. To attach stage-based skills to the full Cortex Code sandbox toolset (the `code_toolset_all` tool type), see [Attaching skills](/user-guide/snowflake-cortex/cortex-agents-coding-agent#attaching-skills).

### Use skills in Snowflake CoWork

The skills configured on an agent are automatically available in Snowflake CoWork. You can also explicitly
select a skill for use by selecting the **+** button and then choosing the skill from the list. That list shows the
agent’s configured skills, not the shared skills and plugins in your account. For details, see
[Use a shared skill in Snowflake CoWork](/user-guide/cortex-code/cortex-code-skill-plugin-sharing#label-cortex-code-skill-sharing-cowork).

## Access control

The following table describes the privileges required for skill operations:

| Privilege | Object | Required for |
| --- | --- | --- |
| USAGE | Stage | Reading skill files from a named stage |
| USAGE | Git Integration | Reading skill files from a Git repository |
| READ | Cortex Extension | Referencing a Cortex Extension in an agent spec |
| MODIFY | Agent | Adding, updating, or removing skills in an agent |
| OWNERSHIP | Agent | Full control over the agent configuration |
| USAGE | Agent | Invoking the agent and its skills |

Expand

Show lessSee more

## Monitoring

Skill invocations are surfaced in the thinking steps during Snowflake CoWork interactions. The monitoring
dashboard displays skill invocation details alongside other orchestration information, including which skill
was selected, the input provided, and the result returned.

## Limitations

The following limitations apply to Cortex Agent skills:

- **SKILL.md location:** The `SKILL.md` file must be at the root of the skill folder. Snowflake doesn’t search
  subdirectories.
- **Supporting files:** All scripts and supporting files must reside in the same folder as the `SKILL.md` file.
- **Git fetch requirement:** Skills referenced by Git tag don’t update automatically. The account admin must
  run a FETCH on the repository for changes to take effect.
