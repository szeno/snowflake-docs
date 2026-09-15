# Cortex Agent versioning

Cortex Agent versioning enables a lifecycle management model that lets you develop, test, and deploy agents
through distinct versions. Each agent has a **live version** — a mutable working copy you use for development —
and can have any number of **named versions** — immutable snapshots you use for stable deployments. By committing
the live version, you create a named version that captures the agent’s configuration at a point in time. You can
then route API requests to any version by name, alias, or shortcut.

This model separates the development workflow from the production workflow. You iterate on the live version,
commit it when ready, assign an alias like `production` to the committed version, and route traffic to that
alias. If you need to roll back, you point the alias to a previous named version.

## How agent versioning works

An agent’s version lifecycle follows a commit-based model:

1. When you create an agent, it automatically creates a committed `VERSION$1` and a `LIVE` version with the
   same spec.
2. You create or modify the agent’s live version during development.
3. When the agent is ready for deployment, you commit the live version. Snowflake creates a named version with a
   system-assigned identifier in the format `VERSION$N` (for example, `VERSION$2`, `VERSION$3`).
4. You assign an alias or set the named version as the default.
5. Interaction requests target the named version — either by name, alias, or shortcut — for stable, repeatable
   behavior.

After a commit, the live version isn’t automatically recreated. You explicitly create a new live version when
you’re ready to resume development.

You can also create named versions directly from a stage or Git repository without going through the live
version. This supports workflows where changes are merged offline and then imported as a new version.

## Live versions

The live version is the mutable, editable state of an agent. You use it during development to iterate on the
agent’s configuration, instructions, tools, and skills. Each agent can have at most one live version at a time.
In the API, SQL, and version identifiers, that version is `LIVE`. In Snowsight, the same version is
displayed as `DRAFT`.

You create a live version in one of the following ways:

- **From agent creation**: When you create a new agent, a live version is automatically created.
- **From the last committed version**: Restore the live version from the most recent named version to continue
  development from a known state.
- **From the Snowsight UI**: The UI can issue the creation of a new live version.

Copy code

```
-- Create a live version from the last committed version
ALTER AGENT my_agent ADD LIVE VERSION FROM LAST
  COMMENT = 'Resuming development from v3';
```

You can optionally assign an alias to the live version at creation time:

Copy code

```
-- Create a live version with an alias
ALTER AGENT my_agent ADD LIVE VERSION dev FROM LAST;
```

The live version is designed for interactive development. Snowflake recommends committing the live version before
using it in production to ensure you have an immutable reference point.

## Named versions

A named version is an immutable snapshot of the agent’s configuration at the time of the commit. Once created,
a named version can’t be modified — you can only update its metadata (comment or alias) or drop it entirely.
This immutability makes named versions the foundation for stable, reproducible deployments.

Snowflake assigns each named version a system identifier in the format `VERSION$N`, where `N` increments
with each commit:

Copy code

```
-- Commit the live version to create a named version
ALTER AGENT my_agent COMMIT
  COMMENT = 'Production release for Q1';
```

This creates `VERSION$2` (or the next available number). You can also create named versions directly from a
stage or Git repository:

Copy code

```
-- Create a named version from a stage
ALTER AGENT my_agent ADD VERSION FROM @my_stage/agents/my_agent
  COMMENT = 'Imported from feature branch';
```

To view all versions on an agent:

Copy code

```
SHOW VERSIONS IN AGENT my_agent;
```

To remove a named version you no longer need:

Copy code

```
ALTER AGENT my_agent DROP VERSION VERSION$1;
```

Note

You can only drop named versions. You can’t drop the live version.

## Aliases

An alias is a human-readable label that you assign to a version. Aliases make it easier to reference versions
in API calls and stage operations without knowing the system-assigned version number. Common alias patterns
include `production`, `staging`, `canary`, and `rollback`.

You assign an alias to a named version or the live version:

Copy code

```
-- Assign an alias to a named version
ALTER AGENT my_agent
  MODIFY VERSION VERSION$3 SET ALIAS = production;

-- Assign an alias to the live version
ALTER AGENT my_agent
  MODIFY LIVE VERSION SET ALIAS = dev;
```

Once assigned, you can use the alias anywhere a version identifier is accepted — in API calls, stage URIs, and
SQL commands.

Alias behavior:

- Each alias must be unique within an agent.
- Aliases are case-sensitive if created with double-quoted identifiers; otherwise they are stored in uppercase.
- You can reassign an alias from one version to another to redirect traffic without changing the calling code.

For example, to promote a new version to production, reassign the `production` alias:

Copy code

```
-- Point the production alias to the latest version
ALTER AGENT my_agent
  MODIFY VERSION VERSION$4 SET ALIAS = production;
```

All API calls that target the `production` alias now route to `VERSION$4` without any change to the calling
application.

## Version shortcuts

Snowflake provides built-in shortcuts for referencing versions without knowing the exact version name or alias.
You can use these shortcuts in the API endpoint and in stage URIs:

| Shortcut | Description |
| --- | --- |
| `LIVE` | The current live version (displayed as `DRAFT` in the UI) |
| `FIRST` | The first committed named version |
| `LAST` | The most recently committed named version |
| `DEFAULT` | The version set as the default for the agent |

Expand

Show lessSee more

Shortcuts are useful for automation scripts and CI/CD pipelines where the exact version number isn’t known ahead
of time. For example, you can always run the latest committed version with the `LAST` shortcut, or target the
version that the agent owner designated as the default.

## Default version

Unless you set it explicitly, the `DEFAULT` version is the latest committed version. You can also designate
one version as the default for the agent. The default version is the version that the agent uses when no version
is specified in an API call:

Copy code

```
-- Set the default version
ALTER AGENT my_agent
  SET DEFAULT_VERSION = 'VERSION$3';
```

You can also set the default to a system shortcut such as `FIRST` or `LAST`:

Copy code

```
ALTER AGENT my_agent
  SET DEFAULT_VERSION = LAST;
```

Setting a default version allows you to control which version serves traffic without requiring callers to
specify a version in every request. When you promote a new version, update the default to redirect all
unversioned API calls.

## Versioning and CI/CD

Agent versioning integrates with CI/CD workflows by supporting version creation from external sources — stages
and Git repositories — and providing aliases and shortcuts for environment routing.

A typical CI/CD workflow for agents follows this pattern:

1. **Develop**: Edit the agent’s live version in the Snowsight UI or through SQL. Test interactively.
2. **Commit**: When the agent is ready, commit the live version to create an immutable named version.
3. **Test**: Route test traffic to the new named version using its system ID or a `staging` alias.
4. **Promote**: Reassign the `production` alias to the new version once testing passes.
5. **Roll back**: If issues arise, reassign the `production` alias to the previous named version.

For teams that manage agent configurations in Git, the workflow shifts to an import model:

1. **Develop**: Edit agent configuration files in a Git repository.
2. **Merge**: Review and merge changes through your standard pull request process.
3. **Import**: Create a named version from the Git-connected stage, bypassing the live version entirely.
4. **Deploy**: Assign the `production` alias to the imported version.

Copy code

```
-- Import a version from a Git-connected stage after a merge
ALTER AGENT my_agent ADD VERSION FROM @my_repo/tags/v2.1/agents/my_agent
  COMMENT = 'Automated deploy from CI pipeline';
```

You can also create a new agent directly from a stage as part of an infrastructure-as-code workflow:

Copy code

```
CREATE AGENT my_agent
  COMMENT = 'Deployed by CI pipeline'
  FROM @my_stage/agents/my_agent;
```

## Stage operations

Each agent version has an internal versioned stage path that you can access through the `snow://agent/` URI
scheme. This lets you inspect the files that make up a version — including the agent specification, skill
definitions, and supporting scripts.

The URI format is:

Copy code

```
snow://agent/<agent_name>/versions/<version>/[<file_name>]
```

The `<version>` segment accepts a system version ID (`VERSION$N`), a user-defined alias, or the keyword
`live`.

Copy code

```
-- List all files in the production version
LIST snow://agent/my_agent/versions/production/;

-- Download the agent spec from a specific version
GET snow://agent/my_agent/versions/VERSION$2/agent.yaml file:///tmp/;
```

Stage operations are read-only and useful for auditing, debugging, and comparing versions.

## Run a specific version

You can target a specific version of an agent using either the REST API or the SQL function.

### REST API

Send a request to the versioned API endpoint:

Copy code

```
POST /api/v2/databases/{database}/schemas/{schema}/agents/{name}/versions/{version}:run
```

The `{version}` path parameter accepts any of the following:

| Identifier type | Example |
| --- | --- |
| System version name | `VERSION$2` |
| User-defined alias | `production` |
| Shortcut | `FIRST`, `LAST`, `DEFAULT`, `LIVE` |

Expand

Show lessSee more

By default, the API streams responses as server-sent events (SSE). To receive a single JSON response, set
`stream` to `false` in the request body.

### SQL function

Append `!<version>` to the agent name in the [DATA\_AGENT\_RUN](/sql-reference/functions/data_agent_run-snowflake-cortex) function:

Copy code

```
-- Run a specific committed version
SELECT SNOWFLAKE.CORTEX.DATA_AGENT_RUN(
  'MY_DB.MY_SCHEMA.MY_AGENT!VERSION$2',
  $${"messages": [{"role": "user", "content": [{"type": "text", "text": "Hello"}]}]}$$
);

-- Run the LIVE version (displayed as DRAFT in the UI)
SELECT SNOWFLAKE.CORTEX.DATA_AGENT_RUN(
  'MY_DB.MY_SCHEMA.MY_AGENT!LIVE',
  $${"messages": [{"role": "user", "content": [{"type": "text", "text": "Hello"}]}]}$$
);

-- Run the DEFAULT version (same as omitting the suffix)
SELECT SNOWFLAKE.CORTEX.DATA_AGENT_RUN(
  'MY_DB.MY_SCHEMA.MY_AGENT!DEFAULT',
  $${"messages": [{"role": "user", "content": [{"type": "text", "text": "Hello"}]}]}$$
);
```

The version suffix supports the same identifiers as the REST API: system version names (`VERSION$N`),
aliases, and shortcuts (`LIVE`, `DEFAULT`, `LAST`, `FIRST`). If no version suffix is specified, the
agent’s DEFAULT version is used.

If the agent name contains a `!` character, enclose that part of the name in double quotes so it is not
treated as a version separator. For example, `'db.schema."my!agent"!LIVE'` targets the LIVE version of
an agent named `my!agent`.

## Limitations

The following limitations apply to Cortex Agent versioning:

- **One live version**: Each agent can have at most one live version at a time.
- **Live version not auto-created**: After you commit the live version, a new live version isn’t automatically
  created. You must create one explicitly.
- **Named versions are immutable**: You can’t modify the configuration of a named version. You can only update
  metadata (comment, alias) or drop it.
- **Drop named only**: You can drop named versions but not the live version.
- **Alias uniqueness**: Each alias must be unique within an agent. Assigning an alias that already exists on
  another version results in an error.
- **Case sensitivity**: Aliases are case-sensitive when created with double-quoted identifiers; otherwise they
  are stored in uppercase.
