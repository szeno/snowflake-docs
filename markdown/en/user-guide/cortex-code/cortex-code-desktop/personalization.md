# Personalization

The **Personalization** page in Agent Settings is where you customize how the CoCo Desktop
agent behaves and what it is allowed to do. From here you can give the agent standing
instructions, turn built-in tools on or off, and manage the agent’s memory.

## Open the Personalization page

Open **Agent Settings** and select **Personalization** from the sidebar. The page has three
sections: **Custom instructions**, **Tools**, and **Memory**.

## Custom instructions

Custom instructions are standing guidance that CoCo applies to every conversation — tone,
preferred output format, conventions, or domain knowledge you don’t want to repeat each time.

Type your instructions into the editor and click **Save**. Your text is stored in the
user-scope instruction file `~/.snowflake/cortex/AGENTS.md`, so it applies across every
workspace. Because it is the same file, edits you make here and edits you make directly in
`AGENTS.md` stay in sync. For how instruction files are discovered and combined, see
[Instruction files](/user-guide/cortex-code/cortex-code-desktop/instruction-files).

Note

Custom instructions are capped at 512 KB. Keep them focused: broad, always-on instructions
are added to every prompt, so concise guidance works best.

## Tools

The **Tools** section controls which built-in agent tools are available. Each toggle takes
effect immediately.

| Tool | What it allows |
| --- | --- |
| **Web Search Tool** | Allow the agent to search the web for relevant information. |
| **Web Fetch Tool** | Allow the agent to fetch content from URLs. |
| **Notebook Tools** | Allow the agent to read, edit, and execute cells in Jupyter notebooks, including managing kernels and inspecting data. |

Expand

Show lessSee more

Note

The **Web Search** tool depends on account-level access to web search. If it is locked, ask
your administrator to enable the `ENABLE_CORTEX_WEBSEARCH` parameter for your account.

## Memory

The **Memory** section controls whether the agent remembers context across conversations.
Turn **Enable memories** on to let CoCo generate memories from your chats and bring them into
new chats, use **Browse memories** to open the folder where they are stored, and use **Reset
memories** to delete them all.

For how memory works, what gets stored, and how it is applied, see
[Memory](/user-guide/cortex-code/cortex-code-desktop/memory).
