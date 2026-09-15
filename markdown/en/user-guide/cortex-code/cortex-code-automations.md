# CoCo automations in CLI and Snowsight (*Preview*)

[Preview Feature](/release-notes/preview-features)  — Open

Available in all commercial regions on AWS, Azure, and Google Cloud. Not available in government,
FedRAMP, DoD, VPS, or China deployments.

## Overview

CoCo automations turn a prompt into a recurring, unattended CoCo run. Each automation runs on a
schedule in a Snowflake-managed sandbox, even when your terminal or browser is closed. Every run
creates a Cortex thread that you can open to inspect the agent’s messages, tool calls, results, and
final response.

Automations created from CoCo CLI and CoCo in Snowsight are the same Snowflake objects. You can
create an automation from one surface and monitor or manage it from the other.

Important

This page describes Snowflake-hosted automations shared by CoCo CLI and CoCo in Snowsight. CoCo
Desktop also supports local automations, but those run on your computer and have a separate
lifecycle and permission model. For more information, see [CoCo Desktop automations](/user-guide/cortex-code/cortex-code-desktop/automations).

Automations are useful for recurring work such as:

- Generating a daily performance recap.
- Checking metrics for anomalies.
- Monitoring warehouse usage and cost.
- Checking data freshness.
- Running a periodic data-quality or repository-maintenance workflow.
- Producing a scheduled digest from a connected MCP server.

## How automations work

Each automation is stored as a Snowflake `AGENT TASK` in your personal database under
`USER$.PUBLIC`. CoCo assigns the internal task name a `COCO_ROUTINE_` prefix.

When the schedule fires, Snowflake does the following:

1. Runs the saved prompt as the user who created the automation.
2. Starts CoCo in a Snowflake-managed sandbox with `/workspace` as the working directory.
3. Makes CoCo’s built-in sandbox tools available to the run.
4. Creates a Cortex thread for the run and associates it with the parent agent task.
5. Records task state, timing, query ID, and errors in task history.

An automation does not require a warehouse. The agent task is owned by the user who created it rather
than by a role, and each run executes as that user. There is no option to configure a different
executing user or role.

Important

A run does not use the role that was active in your CoCo session when you created the automation.
That role is not recorded on the agent task. Each run starts a task session whose primary role is
your user’s default role, with your user’s default secondary roles activated. For more information,
see [Run tasks with user privileges](/user-guide/tasks-intro#label-user-based-security-for-tasks).

Before you rely on an automation, confirm that your default role can reach every object the prompt
needs. A prompt that works interactively under a different role can fail or return incomplete
results when it runs on a schedule.

When you create an automation from the CoCo CLI, CoCo mounts the user’s `USER$.PUBLIC.DEFAULT$`
workspace stage at `/workspace` by default, so files written there persist across runs. Pass
`--workspace <stage_fqn>` to mount a different stage, or `--no-workspace` to skip the mount. If you
skip the mount, `/workspace` is ephemeral and its contents are discarded after each run.

## Requirements and access control

Before you use automations, the following requirements must be met:

- You must meet the standard access requirements for the CoCo surface that you use. For Snowsight
  requirements, see [Access control requirements](/user-guide/cortex-code/cortex-code-snowsight#label-cortex-code-snowsight-access-control).
- Your user must have the `EXECUTE AGENT TASK` account privilege through a role. This privilege is
  granted to the `PUBLIC` role by default, so every user in the account has it unless an
  administrator changes the grant.
- To attach an MCP server, workspace stage, or Snowflake secret, your role must also have the
  privileges required to use that object.

Because `EXECUTE AGENT TASK` is granted to `PUBLIC` by default, administrators who want to limit
automations to selected roles must first revoke the privilege from `PUBLIC`, then grant it to those
roles. For example:

Copy code

```
REVOKE EXECUTE AGENT TASK ON ACCOUNT FROM ROLE PUBLIC;
GRANT EXECUTE AGENT TASK ON ACCOUNT TO ROLE automation_user;
```

Revoking `EXECUTE AGENT TASK` prevents affected users from creating or running automations. Existing
run history remains available until it expires. Existing automations can be resumed if an
administrator restores access later.

For background on the default `PUBLIC` grant, see
[Snowflake CoWork Automations: `EXECUTE AGENT TASK` privilege granted to `PUBLIC` by default](/release-notes/bcr-bundles/un-bundled/bcr-2349).

## Cost

During public preview, user-created automations incur standard Snowflake task billing in addition to
CoCo token consumption for each run. System-initiated analysis does not incur charges.

For details about task costs, see [Monitor task costs](/user-guide/tasks-intro#label-task-monitoring-cost).
For CoCo pricing details, see the
[Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

## Create an automation in Snowsight

You can create an automation from the Automations interface or conversationally from a CoCo chat.

To create an automation from the interface:

1. Open CoCo in Snowsight, then open **Automations**. The entry point can differ by preview build.
2. Select **Create automation**. You can start from an available template or create an automation
   from scratch.
3. Enter a title and a self-contained instruction that describes what CoCo should do on every run.
4. Select the model.
5. Configure the frequency, days, time, and time zone.
6. Review the human-readable schedule, then create the automation.

You can also ask CoCo to create an automation in natural language. For example:

```
Every weekday at 9 AM Pacific time, check yesterday's pipeline failures and create a short summary.
```

CoCo gathers any missing details before creating the automation.

## Create an automation with CoCo CLI

Use the `cortex automation create` command to create an automation. The following example creates an
hourly automation:

Copy code

```
cortex automation create \
  --name pipeline_health \
  --prompt "Check pipeline failures from the last hour and summarize the likely causes." \
  --schedule "every 60 minutes"
```

For a time-of-day schedule, specify an IANA time zone:

Copy code

```
cortex automation create \
  --name daily_performance_recap \
  --prompt-file daily-performance-recap.md \
  --schedule "daily at 9am" \
  --timezone America/Los_Angeles
```

The CLI supports the following schedule forms:

- Intervals, such as `every 60 minutes`, `every 4 hours`, or `daily`.
- Daily times, such as `daily at 9am`.
- Weekly times, such as `every Tuesday at 1:15pm`.
- Multiple weekly times, such as `every Tuesday at 9am and every Friday at 2pm`.

When a natural-language schedule contains multiple weekly times, the CLI can create more than one
underlying agent task. Commands that target every matching task require the `--all` option.

You can use the following options for advanced workflows:

- `--workspace <stage_fqn>`: Mount a specific stage at `/workspace`.
- `--no-workspace`: Use an ephemeral workspace for each run.
- `--mcp <database.schema.name>`: Attach a Snowflake-managed or customer-provided MCP server. Repeat
  the option to attach more than one server.
- `--model <model_id>`: Override the default `auto` model selection.
- `--github <secret_fqn>`: Use a Snowflake secret that contains a GitHub personal access token for
  authenticated GitHub egress.
- `--pre-run-hook <command>` and `--post-run-hook <command>`: Run fixed setup or cleanup commands
  inside the sandbox around each run. See [Run setup and cleanup hooks](#label-cortex-code-automations-hooks).
- `--dry-run`: Print the generated task information and SQL without creating the automation.

Run `cortex automation --help` for the complete command reference.

### Run setup and cleanup hooks

Hooks are bash commands that the sandbox runs around each automation run, before and after the agent
loop. Because a hook is plain bash rather than an instruction, it does the same thing every run and
does not consume an agent turn. Use hooks for fixed setup and teardown, and leave work that varies
between runs in the prompt.

Hooks run only for the automation’s top-level run. They do not run again for subagents that the run
starts.

Use the following options to configure hooks:

| Option | Description |
| --- | --- |
| `--pre-run-hook <command>` | Bash to run during sandbox setup, before the agent loop starts. A nonzero exit status leaves the sandbox unavailable for the rest of the run. |
| `--post-run-hook <command>` | Bash to run after the agent produces its final response. A nonzero exit status is recorded but doesn’t fail the run. |
| `--pre-run-timeout <seconds>` | Time limit for the pre-run hook. The default is 60 seconds and the maximum is 300. |
| `--post-run-timeout <seconds>` | Time limit for the post-run hook. The default is 30 seconds and the maximum is 300. |
| `--hooks-config-path <path>` | Read hooks from a JSON file in the mounted workspace instead of the command line. The path must be relative to `/workspace`. Can’t be combined with the inline hook options. |

Expand

Show lessSee more

Warning

A failing hook does not fail the run. Task history reports the run as succeeded in both of the
following cases, so a broken hook can go unnoticed until you open the run’s thread:

- When a pre-run hook exits nonzero, the sandbox stays unavailable. The agent still starts and still
  produces a final response, but its tool calls fail, so it reports that it can’t do the work instead
  of doing it.
- When a post-run hook exits nonzero, the agent’s result is unaffected. If the post-run hook publishes
  the run’s only output, such as a `git push`, the output is lost while the run still reports success.

Inspect the thread transcript to confirm that a hook did what you expected. Do not rely on task state
alone.

Hooks run as an unprivileged user, and their working directory is not `/workspace`, so use absolute
paths or change directory explicitly.

The mounted workspace stage does not support appending to a file that already exists. You can create
and overwrite files, but a shell append such as `echo done >> /workspace/log.txt` fails with
`Operation not supported` when the target file exists, and the resulting nonzero exit status stops the
rest of the hook. Overwrite the whole file, write a new file for each run, or use a path outside the
mounted workspace.

Important

The same restriction applies to Git. Git appends to its reference log, so a repository that lives on
the mounted workspace stage accepts its first commit and then fails every later commit with
`unable to append to '.git/logs/HEAD': Operation not supported`. Clone to a path outside the mounted
workspace, such as `/tmp`, when a hook needs to commit. The clone is re-created on each run.

The following example clones a repository before the run and publishes the agent’s changes afterward.
The `--github` option gives both hooks and the agent authenticated access to GitHub:

Copy code

```
cortex automation create \
  --name repo_janitor \
  --prompt-file repo-janitor.md \
  --schedule "daily at 2am" \
  --github 'USER$YOU.PUBLIC.GITHUB_PAT' \
  --pre-run-hook "git clone --depth 1 https://github.com/my-org/my-repo /tmp/repo" \
  --post-run-hook "cd /tmp/repo && git add -A && git commit -m 'automated update' && git push"
```

The following example uses a pre-run hook as a guard. If the expected input file is missing, the hook
exits with a nonzero status, which leaves the agent unable to act on stale data:

Copy code

```
cortex automation create \
  --name metrics_digest \
  --prompt-file metrics-digest.md \
  --schedule "every 60 minutes" \
  --pre-run-hook "test -s /workspace/input/latest.csv" \
  --pre-run-timeout 15
```

To change hooks without recreating the automation, keep them in a JSON file in the mounted workspace
and reference it by its workspace-relative path. The sandbox reads the file at the start of each run,
so editing the file changes what later runs do:

Copy code

```
cortex automation create \
  --name nightly_build \
  --prompt-file nightly-build.md \
  --schedule "daily at 1am" \
  --hooks-config-path hooks/nightly.json
```

Hooks run with the same access as the rest of the automation and without an interactive approval
prompt, so treat a hook the same way you would treat any unattended script.

## Monitor and manage automations

The Automations interface in Snowsight lists your automations and their current state. Select an
automation to view its schedule, next run, last run, model, instruction, and run history.

From Snowsight, you can run an automation immediately, pause or resume its schedule, edit its
configuration, or delete it.

Use the following CLI commands to manage the same automations:

| Action | CLI command |
| --- | --- |
| List automations | `cortex automation list` |
| View configuration and state | `cortex automation describe <name>` |
| View recent runs and thread IDs | `cortex automation doctor <name>` |
| Run immediately | `cortex automation execute <name>` |
| Run immediately and wait for completion | `cortex automation execute <name> --wait` |
| Pause scheduled runs | `cortex automation suspend <name>` |
| Resume scheduled runs | `cortex automation resume <name>` |
| Delete the automation | `cortex automation drop <name>` |

Expand

Show lessSee more

In the CoCo CLI interactive interface, enter `/automation` (or `/automations`) without arguments to
open the automation list. In that list, use the arrow keys or `j` and `k` to select an automation,
press Enter to open its run history, press `r` to run the selected automation immediately, and press
Esc to exit. The same keys work in the run-history view, where Enter opens the transcript for a run.

Enter `/automation` followed by a natural-language request to create, inspect, pause, resume, or
delete an automation conversationally.

To inspect the full conversation produced by a run, first retrieve its thread ID:

Copy code

```
cortex automation doctor pipeline_health --limit 10
```

Then open the transcript:

Copy code

```
cortex conversations transcript <thread_id>
```

Task history is the authoritative source for run state and error information. A successful task can
still produce an incomplete business outcome, such as a message that was not delivered. Inspect the
thread transcript to verify the agent’s tool calls and final response.

You can also list recent automation threads directly:

Copy code

```
cortex conversations list --origin sql_function
```

## Write prompts for unattended runs

Each run starts from the saved instruction. It does not have a person available to answer follow-up
questions, approve an action, or clarify an ambiguous name.

Write prompts that:

- State that the run is unattended and must complete autonomously.
- Tell CoCo not to ask follow-up questions.
- Include the exact data objects, repositories, document IDs, channel IDs, or user IDs that the run
  should use.
- Define the expected output and destination.
- Define what the run should do when required data is missing or a tool fails.
- End with a concise success or failure status that is easy to identify in the transcript.

Before relying on a recurring schedule, trigger a run manually and inspect its transcript and side
effects.

## Security considerations

Automations use a caller’s-rights model. Each run executes as the user who created the automation
and respects Snowflake role-based access control, row access policies, and masking policies. If the
user loses access to an object, a later run can no longer access that object.

A run is scoped by the creating user’s default role and default secondary roles, not by the role that
was active when the automation was created. If the user’s default secondary roles include every role
granted to them, a run can reach any object that the user can reach through any of their roles. Take
this into account when you decide which user creates an automation.

Warning

Automation runs are unattended, so interactive tool permission prompts are disabled. Tools that are
available to the run can execute without waiting for approval. Do not schedule destructive or
irreversible actions unless the prompt, role privileges, connected tools, and target objects are
intentionally configured for that behavior.

To apply least privilege, narrow the default role and default secondary roles of the user that owns
the automation rather than switching roles before you create it. Attach only the MCP servers, stages,
and secrets required for the workflow. Avoid broad or ambiguous prompts that could act on unintended
objects.

The automation sandbox can’t access your local filesystem or locally configured MCP servers. Only
files mounted from Snowflake and MCP servers explicitly attached to the automation are available.

## Limits and preview behavior

The following limits and behaviors apply during the public preview:

- The supported minimum scheduling frequency is once per hour. The CLI schedule parser can accept
  shorter intervals, but intervals shorter than one hour are not supported for this preview.
- Automation threads and run history are retained for two months.
- Automations use fixed time-based schedules. Event-based triggers are not supported.
- Runs can take additional time to start while Snowflake provisions the managed sandbox.
- You can’t attach to a run in progress or resume a run interactively. Runs are inspected read-only
  through their task history and thread transcripts.
- The available templates, schedule controls, and interface labels can change during the preview.
- Run history can temporarily show task information without a thread link while a run is starting or
  while thread metadata is being recorded.

## Troubleshooting

### The automation command or interface is not available

Confirm that your account is in a supported deployment and that you meet the access requirements for
the CoCo surface that you use. If the feature is still unavailable, contact your Snowflake account
team.

### Creating or running an automation returns an access error

Confirm that your user has the `EXECUTE AGENT TASK` account privilege through a role. If creation
succeeds but a run reports missing access, check the privileges of your user’s default role and
default secondary roles, not the role you had active when you created the automation. The run needs
access to every referenced stage, MCP server, secret, and data object.

### A run failed

Use `cortex automation doctor <name>` to review task state, error code, error message, and query ID.
If the run produced a thread, inspect it with `cortex conversations transcript <thread_id>`.

### A run succeeded but the expected action did not happen

Open the run’s thread and inspect the tool calls and results. Task success means that the agent run
completed; it does not guarantee that every external side effect matched your intended business
outcome.

### The run can’t find a local file or MCP server

Snowflake-hosted automations can’t use resources from your local computer. Put persistent files in
a mounted Snowflake stage and attach required MCP servers when you create the automation.
