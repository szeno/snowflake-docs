# CoCo CLI cloud sandbox

Feature — Generally Available

Generally available in all commercial regions on AWS, Azure, and Google Cloud. Requires [Cross-region inference](/user-guide/snowflake-cortex/cross-region-inference) to be enabled.

Start CoCo CLI with the `--cloud` option to run the agent’s tools inside a Snowflake-managed
container instead of on your local machine. Your terminal remains the interface, but file
reads and edits, shell commands, and other tool calls all execute server-side against a
[workspace](/user-guide/ui-snowsight/workspaces) mounted into the container.

This is the CLI equivalent of [Cloud Agents](/user-guide/cortex-code/cortex-code-snowsight/cloud-agents)
in Snowsight, and it is distinct from the local
[CoCo CLI sandbox](/user-guide/cortex-code/sandbox), which isolates commands using your
operating system’s built-in controls but still runs them on your machine.

Important

In cloud mode, the agent operates on the mounted workspace — not on your local working
directory. Files on your machine are not uploaded and are not visible to the agent. To work
on a local project, use CoCo CLI without `--cloud`.

## When to use cloud mode

| Use cloud mode when | Use local mode when |
| --- | --- |
| You want the agent’s commands to run entirely off your machine. | You are working on files in a local Git checkout. |
| Your project already lives in a workspace, optionally connected to a Git repository. | You depend on local tooling, credentials, or MCP servers. |
| You want the session to be continuable from Snowsight. | You need `--sql-read-only` or restricted session scope. |
| You want a clean, reproducible environment for each session. | You need to attach more than five images to a message. |

Expand

Show lessSee more

## Starting a cloud session

Start CoCo CLI with `--cloud`:

Copy code

```
cortex --cloud
```

Your personal default workspace (`USER$<your_user>.PUBLIC.DEFAULT$`) is mounted at
`/workspace` in the container, and the agent works there.

To mount a specific workspace, pass its fully-qualified name as the value of `--cloud`:

Copy code

```
cortex --cloud MY_DB.PUBLIC.MY_WORKSPACE
```

To skip the mount entirely and use an ephemeral `/workspace` that is discarded when the
session ends, add `--no-workspace`:

Copy code

```
cortex --cloud --no-workspace
```

Note

`--cloud <name>` and `--no-workspace` are mutually exclusive: one mounts a workspace, the
other skips the mount.

## Workspaces

The mounted workspace is the agent’s filesystem. Changes the agent makes under `/workspace`
are written back to the workspace, so they persist after the session ends and are visible in
Snowsight. Anything the agent writes outside `/workspace` (for example, `/tmp`) is
discarded when the container stops.

Because workspaces can be [connected to a Git repository](/user-guide/ui-snowsight/workspaces-git),
you can point a cloud session at a repository you have already connected in
Snowsight, and review or commit the agent’s changes from there.

The workspace name must be fully qualified as `DATABASE.SCHEMA.NAME`. Names are matched
case-sensitively, so a workspace created with a lowercase name must be passed exactly as it
was created.

### Browsing and switching workspaces

Run `/workspace` during a cloud session to list the workspaces you can access — both those
you own and those shared with you — and select one:

```
/workspace
```

Note

The container is bound to the conversation it was created for, so selecting a different
workspace takes effect on the next conversation. Run `/clear` after selecting, or restart
CoCo CLI, for the new workspace to be mounted.

You can also list workspaces with SQL:

Copy code

```
SHOW WORKSPACES IN ACCOUNT;
```

See [SHOW WORKSPACES](/sql-reference/sql/show-workspaces).

## Where tools run

In cloud mode, the container provides the agent’s tools, so almost everything runs
server-side:

| Capability | Runs |
| --- | --- |
| File reads and edits, search, shell commands, Python | In the container |
| Skills, subagents, and background tasks | In the container |
| Prompts that ask you to choose or confirm something | In your terminal |
| MCP servers you configured locally | On your machine |

Expand

Show lessSee more

Locally configured MCP servers remain available because CoCo CLI hosts them: the container
cannot reach them, so the client continues to run those tools and pass results back. Skills
and plugins installed only on your machine are not available in cloud mode; the container
supplies its own set.

## Accessing GitHub from a cloud session

By default, the container has no credentials for GitHub. To let the agent run `git` and `gh`
against repositories you have access to, store a GitHub personal access token (PAT) in a
Snowflake secret and name that secret with `--github`:

Copy code

```
CREATE SECRET MY_DB.PUBLIC.GITHUB_PAT
  TYPE = PASSWORD
  USERNAME = 'git'
  PASSWORD = '<your_github_pat>';
```

Copy code

```
cortex --cloud --github MY_DB.PUBLIC.GITHUB_PAT
```

Passing `--github` implies `--cloud`, so you can omit `--cloud` when using it.

The value you pass is the secret’s fully-qualified name, not the token itself. Snowflake
fetches the token server-side using your session, and injects it only on outbound requests
to GitHub. The token never enters the container’s environment in plaintext, never appears in
the conversation transcript, and is never written to your machine. You can only reference a
secret you are already authorized to read.

Tip

Grant the PAT the narrowest scopes the task requires, set an expiration, and rotate it
regularly. See [Security best practices for CoCo CLI](/user-guide/cortex-code/security).

## Network access

Outbound network access from the container is restricted rather than disabled. HTTPS egress
is limited to Snowflake and to platform-configured package registries and build tooling (for
example PyPI, npm and Yarn, RubyGems, crates.io, the Go module proxy, Maven and Gradle, and
similar hosts), so the agent can install dependencies. GitHub is reachable only when you
pass `--github`.

Access to other hosts requires [external access integrations](/developer-guide/external-network-access/external-network-access-overview)
that your Snowflake administrator configures. These use the same primitives as UDFs and
stored procedures, and credentials are managed as Snowflake secrets.

Account administrators can block all non-Snowflake egress from CoCo sandboxes across the
account by setting the [COCO\_CLOUD\_AGENTS\_NON\_SNOWFLAKE\_EGRESS\_DISABLED](/sql-reference/parameters#label-coco-cloud-agents-non-snowflake-egress-disabled)
account parameter to `TRUE`:

Copy code

```
ALTER ACCOUNT SET COCO_CLOUD_AGENTS_NON_SNOWFLAKE_EGRESS_DISABLED = TRUE;
```

Only `ACCOUNTADMIN` can change this parameter, and the default is `FALSE`. When it is `TRUE`,
the container cannot reach hosts outside Snowflake, including package registries and GitHub.

## Security and isolation

- **No change to existing grants.** Cloud mode does not modify your Snowflake RBAC settings
  or grant additional SQL access. The agent acts as you.
- **Isolated execution.** Each session runs in its own container, managed by Snowflake.
- **Your machine is not exposed.** The agent cannot read your local files, environment
  variables, or credentials, and cannot run commands on your machine.
- **Scoped persistence.** Only the mounted workspace persists. The rest of the container
  filesystem is discarded when the session ends.

For general guidance, see [Security best practices for CoCo CLI](/user-guide/cortex-code/security).

## Non-interactive use

`--cloud` works with non-interactive runs, which makes it a good fit for CI/CD pipelines
where you do not want an agent touching the build machine:

Copy code

```
cortex exec --cloud "summarize the changes in this workspace" --allowed "Read"
```

Prompts that would require your approval are automatically rejected in `cortex exec`. See
[CoCo CLI reference](/user-guide/cortex-code/cli-reference).

## Limitations

- **Local files are not available.** The agent sees the mounted workspace, not your working
  directory.
- **`--sql-read-only` and restricted session scope are not supported.** Both apply to a
  local SQL connection and have no effect server-side, so CoCo CLI exits with an error
  rather than appear to apply a guard it cannot enforce.
- **Locally installed skills and plugins are not available.** The container supplies its own.
- **At most five images per message.** Attach fewer images, or send them across several
  messages.
- **Switching workspaces requires a new conversation.** Run `/clear` after `/workspace`.

## Availability

- Generally available in all commercial regions on AWS, Azure, and Google Cloud.
- Not available in government, FedRAMP, DoD, VPS, or China deployments.
