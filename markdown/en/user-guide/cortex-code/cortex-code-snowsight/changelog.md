# Cortex Code in Snowsight changelog

This page documents notable changes to Cortex Code in Snowsight.

## September 2026

| Date | Feature | Phase |
| --- | --- | --- |
| Sep 16 | Approval modes (Default approvals / Bypass approvals) | GA |
| Sep 9 | Restrict this chat (restricted session scope) | GA |

Expand

Show lessSee more

### Approval modes

The CoCo side panel now includes an approval-mode selector next to the message
box:

- **Default approvals**: CoCo asks you to approve each tool call. You can allow
  a single call, allow the tool for this chat, or always allow that tool.
- **Bypass approvals**: CoCo runs tool calls without individual prompts. Your
  Snowflake privileges and restricted session scopes still apply.

New conversations start on **Default approvals**. If you choose **Bypass
approvals**, Snowsight remembers that choice for later conversations in the
same browser. The Home composer does not include this selector.

To hide the selector for an account, set the
`COCO__ENABLE_AUTO_APPROVE_SELECTOR` parameter to `FALSE`. This is a Snowsight
dynamic parameter, not an `ALTER ACCOUNT` session parameter. Contact your
Snowflake account team to apply it.

This setting is independent of
[COCO\_SNOWSIGHT\_ALLOW\_ALL\_PERMISSION\_OPTIONS\_DISABLED](/sql-reference/parameters#label-coco-snowsight-allow-all-permission-options-disabled),
which only hides **Allow <tool> in this chat** and **Always allow <tool>**
on individual consent prompts.

## August 2026

| Date | Feature | Phase |
| --- | --- | --- |
| Aug 27 | Subagents | GA |
| Aug 20 | Restrict this chat (restricted session scope) | Private Preview |
| Aug 14 | Automations | Private Preview |
| Aug 10 | Per-turn file changes summary | GA |
| Aug 4 | Agent-requested plan mode | GA |
| Aug 3 | Multi-image drag-and-drop upload | GA |

Expand

Show lessSee more

## July 2026

| Date | Feature | Phase |
| --- | --- | --- |
| Jul 30 | Sticky scroll for prompts | GA |
| Jul 28 | Chat pinning and archiving | GA |
| Jul 22 | Concurrent chats and fullscreen | GA |
| Jul 22 | Cloud Agents | GA |
| Jul 20 | Response copying | GA |
| Jul 20 | Account-wide default model via settings agent | GA |
| Jul 15 | Queued prompts | GA |
| Jul 13 | Infinite conversation scroll | GA |
| Jul 7 | Conversation sharing | GA |

Expand

Show lessSee more

## June 2026

| Date | Feature | Phase |
| --- | --- | --- |
| Jun 26 | Automatic context management | GA |
| Jun 18 | Chat history search | GA |

Expand

Show lessSee more

## May 2026

| Date | Feature | Phase |
| --- | --- | --- |
| May 26 | Inline mentions replacing context chips | GA |
| May 22 | MCP Connectors Integration (User and Admin) | GA |
| May 21 | Clearer CoCo tool execution | GA |
| May 1 | FedRAMP High Gov Deployments (awsusgoveast1fhplus, awsusgovwest1fhplus, azusgovvirginiafhp) | GA |

Expand

Show lessSee more

## April 2026

| Date | Feature | Phase |
| --- | --- | --- |
| Apr 30 | Favicon updates to show when Cortex Code is working or done | GA |
| Apr 29 | Permission updates for SQL execution (Allow Once, Allow all in this chat, Always Allow) | GA |
| Apr 27 | Workspace files as context via + menu or @ mention | GA |
| Apr 27 | SQL Author Skill | GA |
| Apr 27 | FedRAMP Moderate Gov Deployments (awsuseast1gov, awsuswest2gov) | GA |
| Apr 21 | Cloud Agents (UI Sandbox) | Private Preview |
| Apr 15 | Auto navigation to workspaces | GA |
| Apr 9 | Plan Mode | GA |
| Apr 3 | Snap and Ask | GA |

Expand

Show lessSee more
