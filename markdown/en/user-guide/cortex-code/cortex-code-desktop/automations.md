# Automations

Automations let you automate recurring work with CoCo. Each automation is a saved prompt that runs on a schedule. CoCo Desktop has two kinds of automations:

- **Local automations** run on your computer. When one fires, CoCo starts a new chat session, sends your prompt to the agent, and notifies you when it finishes. Local automations are available in all CoCo Desktop builds. They are stored locally per machine and per OS user. They are not synced across devices.
- **Cloud automations** run in Snowflake on a schedule, even while your computer is off. See [Cloud automations](#label-cortex-code-desktop-automations-cloud).

Most of this page describes local automations.

Important

Local automations only run while CoCo is open and your computer is awake. If the app is closed or the machine is asleep when an automation is due, the run is skipped. When you reopen the app, the most recent missed run for each automation is caught up automatically and shown as a “catch-up” run in history. Older missed runs are discarded.

## What automations are good for

- **Morning briefing:** Pull yesterday’s failing tests, new issues, and unmerged PRs into a single status digest at 9 am.
- **Daily code review:** Scan new commits or open pull requests on `main` since yesterday and post a short summary of what changed and anything risky.
- **Dependency and security audit:** Check `package.json`, `pyproject.toml`, or other manifests weekly for outdated or vulnerable dependencies and produce an upgrade plan.
- **Snowflake data checks:** Run a recurring query against a Snowflake table to flag row-count drops, freshness regressions, or anomalous values, and write the findings to a markdown file.

## Quick start

1. Open the **Automations** view from the activity bar.
2. Click **New**, then select **Set up manually**. If your account has Cloud automations, choose **Local**.
3. Give the automation a title and write a prompt describing what you want the agent to do.
4. Pick how often it should run (for example, **Daily at 9:00**).
5. Click **Create**. The automation starts firing on the schedule you chose.
6. Click **Run now** to fire the automation once and approve any tool permission prompts so future runs don’t stall.

The next run time is shown on the automation’s card. You can pause, edit, delete, or **Run now** at any time.

To have CoCo set up an automation for you in a chat, click **New**, then select **Create with CoCo**, and describe what the automation should do.

## Creating an automation

When you click **New** and select **Set up manually**, you’ll see a form with these fields. If your account has Cloud automations, the form first asks where the automation runs: **Cloud** or **Local**. Choose **Local** for the fields described here.

### Title

A short name to identify the automation. Shown in the automation list and used in run notifications (for example, “Daily standup summary”).

### Definition (the prompt)

The instructions sent to the agent each time the automation fires. Write this exactly as you would in a normal chat. You can:

- Reference files using `@` mentions
- Use `/` to insert a skill
- Attach files

The same prompt is sent on every run. Anchor it on stable references (skills, files in your repo, search queries) rather than on transient context.

Tip

Keep prompts self-contained. Scheduled runs don’t carry over context from previous runs: write the prompt as if the agent is seeing the request for the first time. If you find yourself copying the same multi-step instructions into multiple automations, factor them out into a skill and reference it with `/`.

### Schedule

Choose how often the automation runs:

| Option | Behavior |
| --- | --- |
| **Manual** | Never fires automatically. Use **Run now** to trigger it. |
| **Hourly** | Fires every hour at the top of the hour. |
| **Daily** | Fires once per day at the time you pick. |
| **Weekdays** | Fires Monday through Friday at the time you pick. |
| **Weekly** | Fires once per week on the day and time you pick. |
| **Custom** | Repeat every N days or weeks, optionally only on selected weekdays. |

Expand

Show lessSee more

All times are in your local timezone. CoCo adds a small randomized delay (under 2 minutes) to scheduled fire times so heavy automations don’t all queue at once; the displayed next-run time is the actual fire time.

Tip

If you have many daily automations, spread them across different times so they don’t all run at 9:00.

### Ends (optional)

Limit how long the automation keeps running:

- **Never:** runs indefinitely (default).
- **On:** stops scheduling new runs after this date.
- **After** *N* **occurrences:** stops after the automation has run successfully *N* times.

### Project

The folder the automation runs in. Pick an existing project, or choose **Playground** for automations that don’t need a workspace. If the project folder is later removed or moved, the automation auto-disables to avoid running in the wrong place; re-point it at the correct folder and re-enable.

### Model

Pick which LLM the automation uses. Leave on **Auto** to use your default model.

### Attachments (optional)

Files included as context on every run. Useful for templates, style guides, or example outputs.

## Managing automations

The Automations page lists all your automations, split into **Active** (enabled) and **Inactive** (paused).

Each row shows:

- Automation title and prompt preview
- Schedule summary (“Daily at 09:00”)
- Next run time
- Last run status

Hover a row to reveal these actions:

- **Run now:** fire the automation immediately, regardless of schedule.
- **Pause / Resume:** toggle whether the automation fires on schedule. Paused automations remain editable and can still be run manually. Pause automations before vacations so they don’t accumulate catch-up runs.
- **Edit:** change any field. Schedule changes take effect on the next computed run.
- **Delete:** permanently remove the automation and its run history.

Click an automation to open its detail view, which adds:

- **Status:** current state, last run result, next scheduled fire.
- **Previous runs:** recent run history. Click any entry to open that run’s chat session and review what the agent did.

When your account has Cloud automations, the detail view shows a sortable run history and a preview of the latest output instead.

A dot on an automation marks its newest run that you haven’t viewed yet, with failed runs taking precedence. The Agent view sidebar shows how many new runs there are. Opening the automation clears its dot.

## Run history

CoCo keeps the most recent **50 runs** per automation. Each entry records:

- When the run started and finished
- The status (`completed`, `failed`, `running`, or stalled)
- A link to the chat session it spawned
- Whether it was a catch-up run (started after the app reopened)

Older runs roll off, but the lifetime **completed run count** keeps incrementing, which is useful if you set an “After N occurrences” limit.

## Notifications

When a run completes, CoCo shows a desktop notification. Click it to jump to the chat session for that run. Notifications rely on OS-level desktop notification permission for CoCo. If you’re not seeing them, check your OS notification settings.

## Permissions

If an automation tries to use a tool that requires approval, the run pauses and waits for you to approve or deny it from the chat session. To avoid stalls on future runs, click **Run now** after creating an automation, watch the session for any tool prompts, and approve them.

To skip approval prompts entirely for an automation, use a bypass [permission mode](/user-guide/cortex-code/cortex-code-desktop/permission-modes).

## Cloud automations

Cloud automations run in Snowflake as agent tasks on a schedule, even while your computer is off or CoCo Desktop is closed. They are the same Snowflake-hosted automations that you can create and manage in CoCo CLI and CoCo in Snowsight.

Cloud automations are listed on the **Cloud** tab of the **Automations** page. The **Cloud** tab appears only in accounts where CoCo automations are enabled. To turn off Cloud automations, set the `chat.automations.cloud.enabled` setting to `false`.

You can create a cloud automation in the following ways:

- **From a template:** On the **Cloud** tab, click **Get started** on a template card, such as **CoCo Usage Report** or **Pipeline Failure Alert**. CoCo Desktop checks your access, creates the automation, and offers to run a test. Each report appears in the automation’s run history and is sent to your email address.
- **With CoCo:** Click **New**, select **Create with CoCo**, and describe the automation in the chat.
- **With a form:** Click **New**, select **Set up manually**, and choose **Cloud**. A cloud automation needs a schedule other than **Manual**, and can optionally use a **GitHub secret** for GitHub access.

Click a cloud automation to view its instruction, latest output, run history, and details. Use **Edit**, **Run now**, and **Delete** to manage it, and select its status to suspend or resume its schedule.

A cloud automation runs in a Snowflake-managed sandbox, so it can’t use files, MCP servers, or skills from your computer. For requirements, cost, security, and limits, see [CoCo automations in CLI, Snowsight, and Desktop](/user-guide/cortex-code/cortex-code-automations).
