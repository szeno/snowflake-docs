# Automations in Snowflake CoWork

Snowflake CoWork can deliver insights on a schedule instead of waiting for you to ask. With **automations**, you can schedule recurring reports that run automatically on a cadence you define, delivering AI-generated summaries, key metrics, and insights directly to your inbox. Each run re-executes your question against the latest data.

You can set up an automation in two ways: conversationally while chatting with Snowflake CoWork, or manually from the **Automations** tab. For example, a demand planner can set up a Monday morning performance report once and have it arrive by email each week, with a summary, key metrics, and a link to open the full report in Snowflake CoWork for follow-up questions.

## How automations work

An automation subscribes you to a question. Each time the automation runs, Snowflake CoWork re-executes the original question against current data and delivers the result to your email. Because the question runs fresh each time, the report always reflects the latest data.

Automations are built on the following principles:

- **You have the final say.** Snowflake CoWork suggests smart defaults, such as a delivery day and time, but you can change or cancel any automation at any time.
- **You only pay for what you set up.** An automation uses your own compute when it runs. See [Cost and limits](#label-automations-cost-and-limits).
- **Two ways to set up.** Create and manage automations conversationally with Snowflake CoWork or from the **Automations** tab, whichever fits your flow.

## Create an automation

You can create an automation from a conversation or from the **Automations** tab.

### Create from a conversation

Create an automation in the flow of a normal conversation:

1. Ask Snowflake CoWork a question, such as:

   > “Show me last week’s demand forecast performance by product line”
2. Snowflake CoWork returns the analysis, including any charts.
3. Snowflake CoWork suggests turning the report into an automation, for example:

   > “This looks like a report you might want regularly. Want me to send it to you every Monday at 9 AM?”
4. Confirm or adjust the suggestion in your reply. You can accept the defaults, decline, or change the timing, for example:

   > “Send it every Monday at 8 AM instead”
5. Snowflake CoWork confirms the schedule and the first delivery date, for example:

   > “Done. I’ll email you this report every Monday at 8 AM PT. First delivery: February 24.”

You can also ask for an automation directly without waiting for a suggestion, for example:

> “Send me this report every Monday”

### Create from the Automations tab

To configure an automation yourself:

1. In the left navigation, select the **Automations** tab.
2. On the Automations page, select **Create automation**.
3. Choose how to define the automation:
   - **From a conversation**: opens Snowflake CoWork chat, where you can ask a question and turn the result into an automation. See [Create from a conversation](#label-automations-create-conversation).
   - **Manually**: configure the automation yourself.
4. Enter the automation details:
   - **Name**: a label to identify the automation.
   - **Instructions**: the question or report you want Snowflake CoWork to run.
   - **Frequency**: how often the automation runs (hourly, daily, weekly, or monthly).
5. Select **Create**.

## Email delivery

Snowflake CoWork delivers automations by email. Each email includes:

- A summary of the report with the key metrics.
- A link that opens the full report in Snowflake CoWork, pre-loaded so you can continue the conversation and ask follow-up questions.

Email works with corporate email systems. Reports are generated at the scheduled time and cached, so the full report opens quickly when you select the link.

If your email isn’t set up, you can still create automations and review each run from the **Automations** tab, but Snowflake CoWork can’t deliver reports by email until your email is ready:

- **No email on file:** Contact your account administrator to add an email address to your account.
- **Unverified email:** Send yourself a verification email from Snowflake CoWork. Once you verify it, delivery resumes with the next scheduled run.

## Manage your automations

You can list, edit, reschedule, pause, resume, and delete automations in two ways:

- **From the Automations tab:** select the **Automations** tab in the left navigation. The Automations page lists each report’s schedule, delivery channel, and status, and lets you edit, pause, resume, or delete them.
- **Conversationally:** just ask. For example, ask “What automations do I have?” and Snowflake CoWork responds with the same details.

The following table shows common conversational management requests:

| To do this | Say something like |
| --- | --- |
| List your automations | “What automations do I have?” |
| Change a schedule | “Change my Monday report to 7 AM instead” |
| Pause an automation | “Pause the quarterly review report” |
| Resume a paused automation | “Resume the quarterly review report” |
| Delete an automation | “Delete my weekly demand forecast report” |

Expand

Show lessSee more

A paused automation stops sending until you resume it. A deleted automation is removed.

## Where reports appear

Each time an automation runs, it creates a new conversation thread. When you select the link in an email, Snowflake CoWork opens that thread with the report pre-loaded, and you can continue the conversation from there.

You can also see your reports from the **Automations** tab, which lists each automation and its runs. You can view previous runs from the last two months.

## Security and access control

Automations follow a caller’s-rights model: each run executes with your own role and warehouse, without elevated permissions. As a result, every report respects role-based access control (RBAC), row-access policies, and column-masking policies. If you lose access to the underlying data, the report reflects your current permissions the next time it runs.

Links in automation emails use time-limited tokens, results are encrypted at rest, and operations are logged.

## Enable or disable automations

The Automations feature is on by default for all users. It works by granting the EXECUTE AGENT TASK privilege to the PUBLIC role, which allows Snowflake CoWork to schedule and run tasks on your behalf. Agent tasks are Snowflake tasks that run on a user’s behalf to re-execute a question and deliver the result on a schedule.

Administrators can opt out at any time by running the SQL command shown below, and can disable or restrict automations by revoking this privilege.

To disable Automations for all users:

Copy code

```
REVOKE EXECUTE AGENT TASK ON ACCOUNT FROM ROLE PUBLIC;
```

To enable Automations for specific roles only, revoke from PUBLIC first, then grant to the roles you choose:

Copy code

```
REVOKE EXECUTE AGENT TASK ON ACCOUNT FROM ROLE PUBLIC;
GRANT EXECUTE AGENT TASK ON ACCOUNT TO ROLE <role_name>;
```

When access is disabled:

- The **Automations** tab remains visible, but surfaces a message explaining that access is disabled.
- Prior run history is still viewable until its TTL (time to live) expires.
- If an administrator later re-enables access, existing automations can be resumed.

## Cost and limits

An automation uses your own compute each time it runs, billed through standard Snowflake task billing.

The following limits apply:

- Scheduling frequency is capped at once per hour.

## Known limitations

The following limitations apply:

- **Email delivery only.** Automations are delivered by email.
- **A verified email address is required for delivery.** You can create automations without a verified email, but Snowflake CoWork can’t email reports until you have a linked, verified email address. See [Email delivery](#label-automations-email-delivery). Alternatively, an account administrator can verify an email domain with a DNS TXT record to grant verified-email status to every user in that domain across the organization. For more information, see [Domain verification](/user-guide/admin-domain-verification).
- **Scheduled reports only.** Automations run on a fixed hourly, daily, weekly, or monthly schedule.
