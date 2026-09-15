# User skills in Snowflake CoWork

[Preview Feature](/release-notes/preview-features)  — Open

Available to all accounts.

Snowflake CoWork helps you answer questions in the moment. With **user skills**, you can go further: capture a
repeatable workflow once, then reuse it whenever you need that same outcome. A user skill packages the steps,
data sources, and output style you care about so Snowflake CoWork can run the workflow for you on demand.

You can create a user skill conversationally while chatting with Snowflake CoWork, from the UI
(**+** menu > **Skills** > **Create new**), or by uploading a skill folder on **Capabilities** > **Skills**.
After you create a skill, you can run it explicitly (for example by typing `/` followed by the skill name) or
implicitly, when your conversation matches how the skill was defined.

For example, an account executive can create a **Prepare for customer meeting** skill that reviews account health,
surfaces opportunities, flags risks, pulls prior conversations from Slack and email, and generates a PowerPoint
deck of talking points. Before the next customer call, they type `/prepare-for-customer-meeting Acme Corp`, or
simply ask Snowflake CoWork to help them prepare for the Acme meeting, and the skill runs that full workflow.

User skills are different from [agent skills](/user-guide/snowflake-cortex/cortex-agents-skills), which are
developer-authored `SKILL.md` packages stored on a stage or in a Git repository and attached to a Cortex Agent.
User skills are created and used by business users inside Snowflake CoWork.

## Prerequisites

Creating a skill through chat, or from **+** > **Skills** > **Create new**, requires the Cortex Agent
[code execution tool](/user-guide/snowflake-cortex/cortex-agents-code-execution-tool) (code sandbox) on the agent
you use in Snowflake CoWork. Code execution is also required to run skills that execute scripts or assemble
deliverables such as presentations.

Uploading a skill folder on **Capabilities** > **Skills** doesn’t require code execution. Skills that don’t run
scripts can also run without it.

Ask your administrator to enable the [code execution tool](/user-guide/snowflake-cortex/cortex-agents-code-execution-tool) on the agent if chat-based skill creation isn’t
available or a skill that needs scripts fails to run.

## How user skills work

A user skill stores the instructions and context that define your workflow. When you run the skill, Snowflake CoWork
follows those instructions, uses the tools and data your agent can access, and produces the outputs you defined
(for example a briefing, a risk list, or a presentation).

User skills are built on the following principles:

- **You codify the workflow once.** Capture the steps you already take so you don’t re-explain them every time.
- **Several ways to create.** Build a skill conversationally, from the **+** menu, or by uploading a skill folder.
- **Two ways to run.** Invoke a skill explicitly, or let Snowflake CoWork select it when your request matches the
  skill’s purpose.
- **You stay in control.** You can review, edit, and remove skills you own.

## Create a user skill

You can create a user skill from a conversation, from the UI, or by uploading a skill folder.

### Create from a conversation

Create a skill in the flow of a normal conversation. This path requires code execution on the agent:

1. Describe the workflow you want to reuse, for example:

   > “Create a skill that prepares me for a customer meeting. Pull account health metrics, identify opportunities and risks, summarize recent Slack and email threads, and generate a PowerPoint with talking points.”
2. Snowflake CoWork drafts the skill, including a name, description, and the steps it will follow.
3. Review the draft. Confirm it, or ask for changes, for example:

   > “Also include open support cases and the last three closed-won deals for context.”
4. Snowflake CoWork saves the skill and confirms that you can run it next time, for example:

   > “Done. Your Prepare for customer meeting skill is ready. Run it with /prepare-for-customer-meeting or ask me to prepare for a meeting.”

### Create from the UI

The **+** menu doesn’t include a form to fill out. Instead, select **Create new** to start a guided skill that
interviews you and builds the new skill from your answers. This path also requires code execution on the agent:

1. In the message bar, select the **+** menu.
2. Select **Skills**, then select **Create new**.
3. Snowflake CoWork starts the skill-creation walkthrough and asks you for a few details, for example:

   - **Name**: kebab-case, for example `weekly-metrics-report`
   - **Purpose**: what problem does it solve?
   - **Triggers**: words or phrases that should activate it
   - **Tools and integrations**: any specific data sources, APIs, or tools it should use
4. Answer each prompt. Snowflake CoWork uses your responses to draft the skill’s name, purpose, triggers, and the
   steps it will follow.
5. Review the draft, request any changes, and confirm. Snowflake CoWork saves the skill so you can run it next
   time.

### Upload a skill folder

You can also add a skill by uploading a skill folder on **Capabilities** > **Skills**. Upload doesn’t require
code execution on the agent.

1. Open **Capabilities** > **Skills**.
2. Upload the skill folder that contains the skill definition and any related files.
3. After the upload completes, the skill is available to run the same way as skills you create in chat.

## Run a user skill

After a skill exists, you can run it explicitly or implicitly.

### Run a skill explicitly

Use any of the following options when you want a specific skill:

- Type `/` in the message bar, then select or type the skill name. Add optional context after the name, for
  example:

  > “/prepare-for-customer-meeting Acme Corp”
- Select the skill from the **+** menu.
- Open **Capabilities** > **Skills**, then select the skill.

The `/` menu and **+** > **Skills** list can also include [agent skills](/user-guide/snowflake-cortex/cortex-agents-skills)
from the agent you’re using, such as profile (main-agent) and sub-agent skills. Those entries appear with agent
badges so you can tell them apart from skills you created.

### Run a skill implicitly

You can also describe what you need in natural language. Snowflake CoWork evaluates your request against the
names and descriptions of your skills. If a skill is a strong match, it runs that skill without you selecting it
from a menu. For example:

> “Help me prepare for my meeting with Acme tomorrow. I need account health, risks, and talking points.”

If more than one skill could apply, Snowflake CoWork may ask which one to use, or you can name the skill
explicitly with `/`.

## Example: Prepare for a customer meeting

The following example shows how a business user can turn a multi-step prep routine into a reusable skill.

1. Create the skill conversationally or from the UI with instructions such as:

   - Review account health metrics and recent usage trends for the named customer.
   - Identify expansion opportunities and churn or delivery risks.
   - Summarize prior conversations from Slack and email.
   - Generate a PowerPoint deck with talking points for the meeting.
2. Before the meeting, run the skill explicitly:

   > “/prepare-for-customer-meeting Acme Corp”

   Or ask in natural language:

   > “Prepare me for my Acme customer meeting tomorrow.”
3. Review the briefing, adjust the talking points in the conversation, and open the generated presentation.

## Manage your skills

You can list, edit, and delete skills from **Capabilities** > **Skills**, or conversationally. For example:

| To do this | Say something like |
| --- | --- |
| List your skills | “What skills do I have?” |
| Edit a skill | “Update my meeting prep skill to include NPS.” |
| Delete a skill | “Delete my prepare for customer meeting skill” |

Expand

Show lessSee more

## Security and access control

User skills follow a caller’s-rights model: each run executes with your own role and warehouse, without elevated
permissions. Results respect role-based access control (RBAC), row-access policies, and column-masking policies. If
you lose access to underlying data or tools the skill uses, the next run reflects your current permissions.

Skills you create are scoped to you.

## Known limitations

During this preview, the following limitations apply:

- **Code execution for chat creation and scripted skills.** Creating a skill through chat or **Create new**, and
  running skills that execute scripts or assemble files, require the Cortex Agent
  [code execution tool](/user-guide/snowflake-cortex/cortex-agents-code-execution-tool). Uploading a skill folder,
  and running skills that don’t need scripts, don’t require code execution.
- **Agent-configured tools only.** A skill can only use data sources and tools that the agent already has access
  to, such as Cortex Analyst, Cortex Search, and connected collaboration sources your administrator has enabled.
