# CoCo mode in Snowsight

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

CoCo mode is a dedicated view in Snowsight for working on a task with CoCo. The view shows your sessions, the
conversation with CoCo, and a preview of what CoCo builds. The rest of the Snowsight interface is hidden while you
work.

CoCo mode is powered by [Cloud Agents](/user-guide/cortex-code/cortex-code-snowsight/cloud-agents) and is designed
for longer data work, such as refactoring a dbt project, debugging a pipeline, or building an app. You work the way
you would on your own computer: you check out a repository, build and test changes, and review the results as you
go. The difference is that the work runs in Snowflake, in an isolated sandbox for each session, under your active
role and the governance controls that already apply to your account.

Because sessions run in Snowflake and not on your computer, you can start a long task, close your laptop, and return
later to review the results.

With CoCo mode, you can do the following:

- Run several sessions in parallel.
- Check out a GitHub repository, and then commit, push, and open pull requests.
- Build Streamlit apps, web apps, and HTML reports, with a live preview that updates as CoCo works.
- Run SQL in your Snowflake account.
- Ask CoCo for a plan before it makes changes.
- Schedule recurring work as automations.

CoCo mode and the CoCo side panel have different capabilities. To decide which one to use, see
[CoCo mode and the CoCo side panel](#label-coco-mode-side-panel).

## CoCo mode and the CoCo side panel

CoCo in Snowsight is available in two places:

- **CoCo mode:** Opens as a dedicated view for longer tasks, where sessions can work in a GitHub repository, run in
  parallel, and continue after you close your browser.
- **CoCo side panel:** Opens next to the page that you’re working on, where CoCo can read and change that page, such
  as the SQL in an open worksheet or file, or an error that you want to fix.

Use CoCo mode for larger tasks, and the CoCo side panel for work on the page in front of you:

| Task | Recommended |
| --- | --- |
| Change many files at once, such as in a dbt project or a pipeline | CoCo mode |
| Work in a GitHub repository, and then commit, push, and open a pull request | CoCo mode |
| Start a long task and return to it later, or run several tasks at the same time | CoCo mode |
| Build a Streamlit app, web app, or HTML report with a live preview | CoCo mode |
| Write, explain, or fix SQL or code in the open worksheet, file, or notebook | CoCo side panel |
| Ask about the object, query result, or error on the current page | CoCo side panel |

Expand

Show lessSee more

## Before you begin

- Your active role must have the privileges required to use CoCo in Snowsight. For more information, see
  [Access control requirements](/user-guide/cortex-code/cortex-code-snowsight#label-cortex-code-snowsight-access-control).
- To work with GitHub repositories, an administrator must
  [set up the GitHub integration](/LIMITEDACCESS/cortex-code-github-integration#label-cortex-code-github-admin-setup), and you must
  [connect your GitHub account](/LIMITEDACCESS/cortex-code-github-integration#label-cortex-code-github-user-setup).

## Switch between Snowsight and CoCo mode

The **Home** | **CoCo** toggle at the top of the navigation menu switches between Snowsight and CoCo mode:

- To open CoCo mode, in the Snowsight navigation menu, select **CoCo**. CoCo mode opens in the same browser tab, and
  the navigation menu is replaced by your sessions.
- To return to Snowsight, at the top of the CoCo mode sidebar, select **Home**. You can also open the account menu
  and select **Back to Snowsight**.

Snowsight remembers your choice. The next time that you open Snowsight, it opens the view that you used last.

## Start a task and return later

Each session runs in its own sandbox in Snowflake, not in your browser. After you start a task, you can close the
browser tab or your laptop, and the session continues to run. When you return to CoCo mode, the session list shows
the status of each session, and you can open a session to review what CoCo did.

You can run several sessions at the same time. Each session has its own conversation, files, and state, so you can
start a second task while the first one is still running.

## Find a chat

To find an earlier chat, enter part of its title in the **Search chats** box in the session list.

The session list also includes your chats from the CoCo side panel. These chats open read-only in CoCo mode. To
continue one of them, open it in the CoCo side panel.

## Work in a GitHub repository

Before you can work in a repository, an administrator must
[set up the GitHub integration](/LIMITEDACCESS/cortex-code-github-integration#label-cortex-code-github-admin-setup) for your account, and you
must [connect your GitHub account](/LIMITEDACCESS/cortex-code-github-integration#label-cortex-code-github-user-setup).

To work in a repository, select it from the project menu in the message box when you start a session. CoCo checks out
the repository in the session’s sandbox, so you and your team can work from the same repositories. You can then ask
CoCo to commit your changes, push a branch, and open a pull request.

You can’t change the repository of a session after the session starts. To work in another repository, start a new
session.

## Build apps and reports

CoCo can build Streamlit apps, web apps such as React or Flask apps, and HTML reports and dashboards in the session’s
sandbox. When CoCo starts an app, CoCo mode shows a live preview next to the conversation. CoCo mode also renders
the HTML reports and Markdown files that CoCo writes. The preview updates when CoCo changes the app or file, so you
can review the result while CoCo works.

To get started, select one of the suggested tasks on the CoCo mode home page, such as **Build an HTML report** or
**Build a query history App**, or describe what you want CoCo to build.

## Run SQL

CoCo can run SQL in your Snowflake account as part of a task, for example to explore tables, check the output of
a pipeline, or load data for a report. CoCo runs each query with your active role, so it can access only the
objects that your role can access. Depending on your approval mode, CoCo asks for your approval before it runs a
query. For more information, see [Approve tool calls](#label-coco-mode-approvals).

## Plan before CoCo makes changes

In plan mode, CoCo researches your task and proposes a plan instead of making changes. Use plan mode to review the
approach before CoCo edits files or runs commands.

To turn on plan mode, do one of the following:

- In the message box, select **+**, and then select **Plan mode**.
- Press **Cmd+Shift+P** (macOS) or **Ctrl+Shift+P** (Windows).

While plan mode is on, a **Plan** label appears in the message box. CoCo can also ask to turn on plan mode when
a task would benefit from a plan.

In plan mode, CoCo does the following:

1. Gathers context and asks clarifying questions if your request is ambiguous.
2. Saves the plan to a file, and then replies with a summary and a link to the plan.
3. Updates the plan when you reply with changes.
4. Turns off plan mode and starts work after you confirm the plan.

To turn off plan mode, select the **x** on the **Plan** label, or press the same keyboard shortcut. To start every
new session in plan mode, turn on **Default to plan mode** in [settings](#label-coco-mode-settings).

## Automate recurring work

An automation runs a CoCo prompt on a schedule, for example to check a pipeline every morning or to send a weekly
report. Automations run in Snowflake, even when your browser is closed. Automations that you create in CoCo mode are
the same Snowflake objects as automations that you create in the CoCo side panel or in CoCo CLI.

To create an automation, do one of the following:

- In the CoCo mode sidebar, select **Automations**, and then select a template or select **New**.
- On the CoCo mode home page, select **Create an automation**.
- In any session, ask CoCo to create an automation and describe what it should do and when it should run.

CoCo confirms the details with you before it creates the automation.

On the **Automations** page, you can see each automation’s status and last run. For each automation, you can run it
now, edit it, pause or resume it, or delete it. To view an automation’s instructions and the runs from the last
seven days, select the automation. To review what CoCo did in a run, select the run. The run opens as a read-only
chat.

For requirements, cost, and prompt guidance, see
[CoCo automations in CLI and Snowsight](/user-guide/cortex-code/cortex-code-automations).

## Approve tool calls

CoCo mode asks before it runs tools that can change files or data. To choose how often CoCo asks, use the approval
mode menu below the message box:

| Mode | Behavior |
| --- | --- |
| **Manual** | CoCo asks you to approve tool calls. This is the default. |
| **Auto** (*Preview*) | CoCo approves commands that it rates as safe and asks you before it runs risky ones. This mode is available only in accounts where it’s enabled. |
| **Bypass** | CoCo runs every tool call without asking. Account administrators can turn off this mode. |

Expand

Show lessSee more

To set the approval mode for new sessions, use the **Approvals** setting.

## Settings

To change your preferences for CoCo mode, open the account menu in the CoCo mode sidebar, and then select
**Settings**. The following settings apply to new sessions:

| Setting | Description |
| --- | --- |
| **Model** | The model, and the effort level where the model supports it, that new sessions use. |
| **Approvals** | Whether new sessions ask before running tools. |
| **Default to plan mode** | Starts new sessions in plan mode. |
| **Prompt history** | Lets you press the up and down arrow keys in the message box to reuse earlier prompts from the chat. |
| **cmd-Enter to submit** | Sends a message with Cmd+Enter or Ctrl+Enter instead of Enter. |
| **Ask clarifying questions** | CoCo asks its questions in a form with multiple-choice answers. When off, CoCo asks in the chat. |
| **Collapse intermediate messages** | Groups the steps of each response into one expandable section. |

Expand

Show lessSee more

The account menu also contains **MCP Connectors**, where you manage the external services that CoCo can connect to.
To manage your GitHub connection, select **Git settings** in the project menu of the message box. For more
information, see [Connect your GitHub account](/LIMITEDACCESS/cortex-code-github-integration#label-cortex-code-github-user-setup).

## Access control

CoCo mode runs with your active role and follows every grant and policy on that role. To limit what CoCo can do in
a session, for example to allow only read-only SQL, apply a
[restricted session scope](/user-guide/restricted-session-scope). For more information, see
[Restrict a chat](/user-guide/cortex-code/cortex-code-snowsight#label-cortex-code-snowsight-restricted-session-scope).

For information about how the Cloud Agents sandbox is isolated and which hosts it can reach, see
[Cloud Agents](/user-guide/cortex-code/cortex-code-snowsight/cloud-agents).

## Limitations

CoCo mode runs in its own sandbox rather than next to a Snowsight page, so some capabilities of the CoCo side panel
aren’t available:

- **No access to Snowsight pages.** CoCo mode can’t read or change the page that you were on, such as an open
  worksheet or file, selected text, a notebook cell, or a query result.
  Actions that send page context to CoCo, such as fixing an error from a worksheet, open the CoCo side panel.
- **Chats from the CoCo side panel are read-only.** To continue one of these chats, open it in the CoCo side panel.
- **Fewer interactive results.** Some interactive result features of the CoCo side panel, such as pivot tables and
  chart building, aren’t available in CoCo mode.

## Availability

- CoCo mode is available in all commercial regions on AWS, Azure, and Google Cloud.
- CoCo mode is rolling out to accounts gradually, so it might not appear in your account right away.
- CoCo mode isn’t available in government, FedRAMP, DoD, VPS, or China deployments.

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
