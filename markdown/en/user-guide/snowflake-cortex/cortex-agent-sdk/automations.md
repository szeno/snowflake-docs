# Schedule automations with the Cortex Agent SDK

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

An automation runs an agent on a schedule, with no one in the loop. Use `client.automations` to create and manage
automations from your own application. The SDK supports two kinds of automation:

- A saved Cortex Agent that answers the same prompt on each run, such as a daily sales summary.
- An unattended Cortex Code (CoCo) session that runs in a Snowflake-managed sandbox, such as a nightly check of failed
  tasks.

Automations are also available in Snowflake CoWork and CoCo, where users create them without writing code. See
[Automations in Snowflake CoWork](/user-guide/snowflake-cortex/snowflake-cowork/automations) and
[CoCo automations](/user-guide/cortex-code/cortex-code-automations). As in Snowflake CoWork and CoCo, each automation
is an agent task. The SDK creates it in your personal database under `USER$.PUBLIC`, by using the Snowflake SQL API with
the client’s existing authentication. You don’t need a separate connector. The agent task itself doesn’t need a
warehouse, but a saved agent’s tools still use the warehouses configured for them.

Boolean and null values in this topic use TypeScript spelling. In Python, use `True`, `False`, and `None`.

## Before you begin

- Your user needs the `EXECUTE AGENT TASK` account privilege through a role. Snowflake grants this privilege to
  `PUBLIC` by default, and administrators can revoke it. See
  [Enable or disable automations](/user-guide/snowflake-cortex/snowflake-cowork/automations#label-automations-enable-disable).
- Each run uses your user’s default role and default secondary roles, not the role that was active when you created
  the automation. Confirm that your default role can reach every object the prompt needs. See
  [Run tasks with user privileges](/user-guide/tasks-intro#label-user-based-security-for-tasks).
- To schedule a saved agent, your default role or default secondary roles need `USAGE` on the agent and on the
  database and schema that contain it, plus `USAGE` on any warehouses that the agent’s tools use. See
  [Access control and authentication](/user-guide/snowflake-cortex/cortex-agents-setup).

## Choose an automation type

Set `type` when you create an automation. If you omit `type`, the SDK creates a saved-agent automation. The two types
are:

| Type | What runs | Use it when |
| --- | --- | --- |
| `agent` (default) | A saved Cortex Agent, with your prompt as the user message. | You’ve already built an agent that answers the question, and you want the answer on a schedule. |
| `coding` | A CoCo session in a Snowflake-managed sandbox, with your prompt as the task. | The work needs to run commands, read files, or write files. |

Expand

Show lessSee more

## Set a schedule

Pass a Snowflake task schedule: an interval of `60 MINUTES` or longer, or a `USING CRON` expression with a time zone,
such as `USING CRON 0 9 * * * UTC`. Automations can run at most once per hour. Snowflake validates the schedule
when it creates the task. For the schedule syntax, see [CREATE TASK](/sql-reference/sql/create-task).

## Create a saved-agent automation

Pass the task name, the saved agent, a prompt, and a schedule.

TypeScriptPython

Copy code

```
import { CortexAgentClient } from "@snowflake/cortex-agent-sdk";

const client: CortexAgentClient = new CortexAgentClient({
  account: process.env.SNOWFLAKE_ACCOUNT!,
  auth: process.env.SNOWFLAKE_PAT!,
});

await client.automations.create({
  name: "DAILY_SALES",
  agent: { database: "ANALYTICS", schema: "PUBLIC", name: "SALES_AGENT" },
  prompt: "Summarize yesterday's sales.",
  schedule: "USING CRON 0 9 * * * UTC",
  enabled: true,
});
```

Copy code

```
from snowflake.cortex.agents import CortexAgentClient

client: CortexAgentClient = CortexAgentClient(account="my_account", auth="<token>")

client.automations.create(
    "DAILY_SALES",
    agent={"database": "ANALYTICS", "schema": "PUBLIC", "name": "SALES_AGENT"},
    prompt="Summarize yesterday's sales.",
    schedule="USING CRON 0 9 * * * UTC",
    enabled=True,
)
```

## Create a CoCo automation

Set `type` to `coding` to schedule an unattended CoCo session instead of a saved agent.

TypeScriptPython

Copy code

```
await client.automations.create({
  type: "coding",
  name: "DAILY_CHECK",
  prompt: "Check yesterday's failed tasks and summarize the likely causes.",
  schedule: "USING CRON 0 9 * * * UTC",
  model: "auto",
  enabled: true,
});
```

Copy code

```
client.automations.create(
    "DAILY_CHECK",
    type="coding",
    prompt="Check yesterday's failed tasks and summarize the likely causes.",
    schedule="USING CRON 0 9 * * * UTC",
    model="auto",
    enabled=True,
)
```

In addition to `name`, `prompt`, `schedule`, `enabled`, and `resumeThread`, CoCo automations accept these options:

| Option (TypeScript / Python) | Default | Description |
| --- | --- | --- |
| `model` / `model` | `auto` | The model that CoCo uses for the run. |
| `workspaceStage` / `workspace_stage` | `USER$.PUBLIC.DEFAULT$` | The workspace stage that Snowflake mounts at `/workspace`. Files written there persist across runs. Pass the fully qualified name of another workspace stage, or pass `null` to run without a mount. Without a mount, `/workspace` is ephemeral, and its contents are discarded after each run. |
| `disableEmail` / `disable_email` | `false` | Stops Snowflake from emailing you a report after each run. |

Expand

Show lessSee more

By default, a CoCo automation that you create with the SDK uses a read-only Snowflake session scope, in addition to
your default role and default secondary roles. The effective scope depends on the account’s automation configuration,
and the SDK has no option to change it. The scope applies only to Snowflake, so the run can still create, change, and
delete files in the sandbox.

Warning

A CoCo automation runs with no one available to approve tool calls, so the SDK turns off permission prompts for tools
and the sandbox. Tools available to the run can act without approval. Write prompts that are safe to run unattended,
and don’t schedule destructive or irreversible actions. See
[Write prompts for unattended runs](/user-guide/cortex-code/cortex-code-automations#label-cortex-code-automations-prompts).

The SDK doesn’t set up Git repositories, network integrations, secrets, MCP servers, or setup and cleanup hooks for a
CoCo automation. To use any of these, create the automation with the CoCo CLI. See
[Create an automation with CoCo CLI](/user-guide/cortex-code/cortex-code-automations#label-cortex-code-automations-create-cli).

## How the SDK creates automations

These rules apply to both kinds of automation:

- **Names are exact.** Task names and each part of the agent name are case-sensitive. Pass them without SQL quotes,
  and the SDK quotes them for you. For example, an agent created with the unquoted name `sales_agent` is stored as
  `SALES_AGENT`, so pass `SALES_AGENT`.
- **Existing tasks aren’t replaced.** Creation fails if a task with the same name already exists.
- **New automations are suspended.** Set `enabled` to `true` to start the schedule when you create the automation, or
  call `resume` later. Starting the schedule doesn’t run the automation right away. To run it once now, call
  `execute`.
- **Creation and enabling are separate steps.** If the automation is created but can’t be enabled, the call fails with
  that error, and the SDK doesn’t delete the automation. Check its state with `describe` or `list`, and then call
  `resume`.
- **Each run starts a new conversation.** To continue the previous run’s conversation instead, set `resumeThread`
  (TypeScript) or `resume_thread` (Python) to `true`.

## Manage automations

Use these methods for both kinds of automation. Each method except `list` takes the task name. The SDK doesn’t have a
method that changes an existing automation. To change an automation’s prompt, schedule, or options, call `delete`, and
then call `create` again with the new values.

| Method | What it does |
| --- | --- |
| `list()` | Lists every agent task in `USER$.PUBLIC`, including tasks created outside the SDK. |
| `describe(name)` | Returns the task’s definition, schedule, and state. |
| `execute(name)` | Starts one run now. The method returns when Snowflake accepts the run, not when the run finishes. |
| `suspend(name)` | Pauses the schedule. |
| `resume(name)` | Starts the schedule. |
| `delete(name)` | Deletes the task. |

Expand

Show lessSee more

TypeScriptPython

Copy code

```
await client.automations.execute("DAILY_SALES");
await client.automations.suspend("DAILY_SALES");

const tasks = await client.automations.list();
for (const row of tasks.rows) {
  console.log(row.name, row.state, row.schedule);
}
```

Copy code

```
client.automations.execute("DAILY_SALES")
client.automations.suspend("DAILY_SALES")

for row in client.automations.list().rows:
    print(row["name"], row["state"], row["schedule"])
```

## Read the results of a run

Each run saves its conversation in a thread. A run’s thread appears only after the run starts, so a run that you just
started with `execute` might not have a thread yet.

To read an automation’s results, get the task ID from `list()`, list the threads for that task, and then read the
assistant’s messages in each thread. Reading threads uses the direct API client, a separate class from the client in
the earlier examples. For more about the direct API client, see
[Use the direct Cortex Agent API](/user-guide/snowflake-cortex/cortex-agent-sdk/running-agents).

TypeScriptPython

Copy code

```
import {
  CortexAgentClient as ApiCortexAgentClient,
  ThreadMessageView,
} from "@snowflake/cortex-agent-sdk/api";

const api: ApiCortexAgentClient = new ApiCortexAgentClient({
  account: process.env.SNOWFLAKE_ACCOUNT!,
  auth: process.env.SNOWFLAKE_PAT!,
});

const tasks = await client.automations.list();
const task = tasks.rows.find((row) => row.name === "DAILY_SALES");

const listed = await api.threads.list({ task_id: task!.id! });
for await (const thread of listed.page) {
  const detail = await api.threads.describe(String(thread.thread_id));
  for (const raw of detail.responseBody.messages ?? []) {
    const message: ThreadMessageView = new ThreadMessageView(raw);
    if (message.role === "assistant") {
      console.log(thread.thread_name, message.text);
    }
  }
}
```

Copy code

```
from snowflake.cortex.agents.api import CortexAgentClient as ApiCortexAgentClient
from snowflake.cortex.agents.api import ThreadMessageView

api: ApiCortexAgentClient = ApiCortexAgentClient(account="my_account", auth="<token>")

task = next(row for row in client.automations.list().rows if row["name"] == "DAILY_SALES")

for thread in api.threads.list(task_id=task["id"]):
    detail = api.threads.describe(str(thread["thread_id"]))
    for raw in detail.get("messages", []):
        message = ThreadMessageView(raw)
        if message.role == "assistant":
            print(thread["thread_name"], message.text)
```

For other thread methods, see “Manage threads directly” in [Use the direct Cortex Agent API](/user-guide/snowflake-cortex/cortex-agent-sdk/running-agents).

## Handle method results and timeouts

Each method returns an `AutomationResult`:

- `rows`: the result rows, keyed by column name. Values keep their SQL API format, usually strings or `null`.
- `statementHandle` (TypeScript) or `statement_handle` (Python): the ID of the SQL statement.
- `response`: the original HTTP response for the statement, including headers and the request ID.

If a statement is still running when Snowflake first responds, the SDK waits and checks again. By default, it waits up
to 60 seconds for each statement. To change the limit, pass `waitTimeoutMs` in the options argument (TypeScript), or
pass the `wait_timeout` keyword argument in seconds (Python). If the limit is reached, the SDK raises
`AutomationWaitTimeoutError`, which includes the statement handle.

Stopping the wait doesn’t stop the statement or the run on Snowflake. Check the automation’s state before you try
again. To cancel the wait, pass an abort `signal` in the options argument (TypeScript), pass
`options={"cancel": event}` where `event` is a `threading.Event` (Python), or cancel the task that awaits the call
(asynchronous Python).

`AsyncCortexAgentClient` has the same methods. Await each call. See
[Use the asynchronous Python client](/user-guide/snowflake-cortex/cortex-agent-sdk/async-python).

## Cost

Each run incurs standard Snowflake task billing, plus the usage of the agent or CoCo session that it runs. See
[Monitor task costs](/user-guide/tasks-intro#label-task-monitoring-cost) and
[CoCo automations cost](/user-guide/cortex-code/cortex-code-automations#label-cortex-code-automations-cost).

## Legal notices

Where your configuration of Cortex Code uses a model provided on the
[Model and Service Pass-Through Terms](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/ai-features/model-pass-through-terms/),
your use of that model is further subject to the terms for that model on that page.

The data classification of inputs and outputs are as set forth in the following table.

| Input data classification | Output data classification | Designation |
| --- | --- | --- |
| Usage Data | Customer Data | Covered AI Features [[1]](#footnote-1) |

Expand

Show lessSee more

[1]
Represents the defined term used in the AI Terms and Acceptable Use Policy.

For additional information, refer to [Snowflake AI and ML](/guides-overview-ai-features).
