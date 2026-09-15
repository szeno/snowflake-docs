# Memory

Memory lets the CoCo Desktop agent carry context from one conversation to the next. When
memory is enabled, CoCo records durable facts — your preferences, project context, and
guidance you’ve given it — and brings the relevant ones back into new conversations
automatically, so you don’t have to re-explain them each time.

## How memory works

CoCo stores memories as Markdown files under `~/.snowflake/cortex/memory/`. Memory is
organized into two scopes:

- **Global memory** applies everywhere. It is indexed by a top-level `MEMORY.md` file plus
  topic files it points to.
- **Project memory** is scoped to a single workspace, so context about one project doesn’t
  leak into another. Each workspace has its own memory index and topic files.

At the start of each conversation, CoCo automatically loads the global and project-level
`MEMORY.md` index so it knows what it already remembers. It reads the linked topic files on
demand as they become relevant, and writes new entries as it learns things worth keeping.
When CoCo reads or updates memory, you’ll see a **Reading memory**, **Updating memory**, or
**Browsing memories** indicator in the transcript.

Note

Memory is for durable context, not the current task. CoCo saves things like your role and
preferences, standing project decisions, and feedback you’ve given it — not transient,
in-conversation state.

## Manage memory

Memory is managed from the **Memory** section of the **Personalization** page in Agent
Settings. See [Personalization](/user-guide/cortex-code/cortex-code-desktop/personalization).

| Control | What it does |
| --- | --- |
| **Enable memories** | Turn memory on or off. When off, CoCo neither generates new memories nor applies existing ones. |
| **Browse memories** | Open `~/.snowflake/cortex/memory/` so you can read, edit, or back up the memory files directly. |
| **Reset memories** | Permanently delete all stored memory files. This action cannot be undone. |

Expand

Show lessSee more

Tip

Because memories are plain Markdown files on disk, you can review exactly what CoCo has
remembered at any time with **Browse memories**, and edit or remove individual entries
by hand.
