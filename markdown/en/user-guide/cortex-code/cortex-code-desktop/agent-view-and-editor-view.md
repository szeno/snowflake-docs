# Agent view and Editor view

CoCo Desktop runs in two top-level workspace views: **Agent view** for running and reviewing many agents across workspaces in one window, and **Editor view** for the full VS Code-style IDE scoped to a single workspace.

Tip

The simplest way to switch is the **view toggle button in the title bar**. You can also run *Toggle Agent or Editor view* from the command palette. Your active conversation follows you across the toggle.

## Views at a glance

| View | Main pane | Layout | Best for |
| --- | --- | --- | --- |
| **Agent view** | Chat | Workspace + conversation sidebar; a side rail of inspectors (Changes, terminal, and more) for the active conversation. Lists every workspace you’ve added in one window. | Driving and reviewing one or many agents, especially across multiple repos; monitoring long-running tasks or automations. |
| **Editor view** | Code editor | Standard IDE: file explorer, source control, run & debug, terminal, extensions, plus chat in a side view. One workspace per window. | Hand-editing code, debugging, using extensions, with the agent on the side. |

Expand

Show lessSee more

## Agent view

Agent view replaces the editor area with an agent-first surface. The conventional editor parts (activity bar, primary side bar, editor groups, panel) are hidden so the chat and its surrounding context get the full window. Agent view is designed around three capabilities:

### 1. Parallelism across workspaces, in one window

Editor view is one workspace per window. Agent view lets you drive agents in many workspaces side-by-side without juggling windows.

- The sidebar lists **all** workspaces you’ve added, each with its own conversation history.
- Switching workspaces is a single click, with no *Open Folder* and no window reload.
- Each conversation runs in its own workspace context: file pickers, terminals, search, and tool calls all scope to that conversation’s folder.
- A built-in **Playground** workspace is always available for one-off chats that don’t belong to any project.

### 2. Built-in review of agent changes

Each conversation tracks the files an agent has modified. Agent view surfaces these changes directly, so reviewing and acting on them does not require opening separate source-control or diff views.

- A *Changes* panel in the side rail lists every file the active conversation has touched, with a unified diff, a changed-files tree, a scope selector, and per-file accept and reject actions.
- Pending changes, approval prompts, and diff stats are scoped to each conversation and persist as you switch between them.
- Bulk actions (accept all, reject all, open file) are available without leaving the Agent view surface.
- Every turn that edits files also ends with an **N files changed** summary card in the chat, showing added and removed line totals and per-file badges. Click a row to jump to the diff.

### 3. Background execution and notifications

Conversations continue running when not in focus. Agent view’s sidebar acts as a status dashboard for everything in flight at once. Editor view’s chat panel shows only the active session.

- The sidebar shows per-conversation state for every workspace at once: in progress, awaiting approval, unread.
- Approval prompts and notifications attach to the conversation that needs attention, so you can triage many in-flight agents without switching focus.
- Automations appear in the same list, with the same indicators.

### Surfaces at a glance

- **Sidebar** lists your workspaces and their conversations, with search and a button to start a new agent.
- **Conversation pane** shows the active chat, including tool calls, approvals, and inline diffs.
- **Right-hand rail** holds *Changes*, terminal, and other inspectors for the active conversation.

## Editor view

Editor view is the familiar IDE: file explorer, editors, source control, run & debug, terminal, and extensions are all front-and-center. Chat lives in a side view rather than as the main pane, so you can edit code and talk to the agent simultaneously.

- All editor-area features (multi-cursor editing, find/replace across files, language tooling, debugging, tasks) are available exactly as in upstream VS Code.
- Extensions, keybindings, and settings carry over. Editor view is not a stripped-down view; it is the full workbench.
- The chat side view shares the same conversation list as Agent view, so you can pick up where you left off.

## Workspace scoping

Conversations, skills, and plugins are all scoped per workspace. Agent view and Editor view are different views over the same underlying state, not separate stores.

- **Conversations** belong to the workspace they were started in and persist in that workspace’s storage. Editor view shows the current workspace’s conversations; Agent view shows conversations across every workspace you’ve added, grouped by workspace.
- **Skills and plugins** resolve from a global set (shared across all workspaces) plus the active conversation’s workspace-local set. An agent running in one workspace only sees that workspace’s project-defined skills and plugins, never another workspace’s.
- **Tool calls** (file picker, terminal, search) always run in the active conversation’s workspace context, regardless of which view you’re using.
- Starting, continuing, archiving, or deleting a conversation in one view is reflected in the other.

When you toggle, your active conversation follows you only if it belongs to the workspace Editor view is open on. Conversations from other workspaces remain accessible in Agent view’s sidebar.

## Choosing a view

**Rule of thumb:** if *you* are writing the code, use Editor view. If *agents* are writing the code and your job is to dispatch them, watch them, and review their output, especially across more than one workspace, use Agent view.

- **Hand-editing, debugging, using extensions**: Editor view. Keep the agent in the loop via the chat side view.
- **Driving one or more agents on real work**: Agent view. Chat gets the main pane and the side rail surfaces the agent’s changes, terminal, and other context as the work progresses.
- **Running agents across multiple repos or workspaces in parallel**: Agent view. One window covers all of them.
- **Long-running tasks or automations**: Agent view. Unread indicators and notifications are designed for stepping away and coming back.
