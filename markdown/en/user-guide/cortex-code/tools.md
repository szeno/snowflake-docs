# CoCo CLI agent tools

CoCo has access to a comprehensive set of tools for file operations, shell commands, Web access, and more.
You don’t need to install anything extra; these tools are built into CoCo CLI and ready to use. CoCo
automatically uses appropriate tools based on your requests. You do not need to invoke them manually; just describe
what you want. For example:

```
Read the first 10 lines of the file src/main.py
Search for TODO comments in all Python files
Execute a bash command to list running processes
```

When creating custom skills, you must specify the tools the skill can use. See [Skills](/user-guide/cortex-code/extensibility#label-extensibility-skills).

The section headings on this page are display names. Wherever you name a tool in configuration, such as
a skill or subagent `tools:` list, a hook `matcher` field, or a permission rule, use the lowercase
runtime tool ID instead: `read`, `write`, `edit`, `glob`, `grep`, `bash`, and so on. These names are
case-sensitive, and a name that matches no tool is ignored without an error.

## File tools

These tools let CoCo read, write, search, and navigate files in your local filesystem. CoCo uses them
whenever your request involves understanding or modifying code, configuration, or documentation files.

### Read

Read file contents from the local filesystem. CoCo uses this tool whenever it needs to understand existing
code before making changes, inspect configuration files, or view the contents of documents you reference.

Supports:

- Text files with line numbers
- Images (PNG, JPG, etc.) displayed visually through the multimodal model
- PDFs with page-by-page text and visual extraction
- Jupyter notebooks with cells and their outputs
- Line ranges using the `@file.py$10-20` syntax for targeted reads

### Write

Create new files or overwrite existing ones. CoCo uses this tool when generating new files from scratch,
such as scaffolding a new module, creating configuration files, or writing scripts.

Supports:

- Automatic parent directory creation
- Line change tracking for session statistics
- Full file overwrite (for partial changes, CoCo uses Edit instead)

### Edit

Perform targeted search-and-replace edits within existing files. CoCo prefers this tool over Write when
modifying existing code, because it changes only the specific lines that need updating while preserving
the rest of the file.

Supports:

- Exact string matching and replacement
- Diff preview before applying changes
- `replace_all` mode for renaming variables or updating repeated patterns across a file

### Glob

Find files by name or path pattern. CoCo uses this tool to locate files before reading or editing them,
especially when you reference a file by partial name or when CoCo needs to discover related files in a
project.

Example patterns:

| Pattern | Description |
| --- | --- |
| `**/*.py` | All Python files |
| `src/**/*.ts` | TypeScript files in `src/` directory |
| `**/test_*.py` | Python test files |
| `!node_modules` | Exclude patterns |

Expand

Show lessSee more

### Grep

Search file contents using regular expressions. CoCo uses this tool to find specific code patterns,
function definitions, error messages, or configuration values across your project.

Supports:

- Recursive directory search
- Full regex pattern syntax
- Binary file detection and skipping
- Output modes: matching content lines, file paths only, or match counts

## Shell tools

These tools give CoCo access to your terminal environment for running commands, installing packages,
running tests, and interacting with developer tools like `git`, `npm`, or `docker`.

### Bash

Execute shell commands in a persistent session. CoCo uses this tool for operations that require system
access: running tests, installing dependencies, executing builds, interacting with version control,
or any task that goes beyond file manipulation.

Supports:

- Streaming output for long-running commands
- Background execution with `run_in_background` for servers and watchers
- Configurable timeout (default 2 minutes, maximum 10 minutes)
- Sandbox mode for restricted environments

### BashOutput

Retrieve output from a command that was previously launched in the background. CoCo uses this tool to
check on the status of long-running processes like development servers or test suites.

Supports:

- Regex filtering to show only relevant output lines
- Process status checking (running, completed, or failed)
- Incremental output retrieval (only new lines since last check)

### KillShell

Terminate a running background shell process. CoCo uses this tool to stop servers, cancel stuck
commands, or clean up processes that are no longer needed.

## Agent tools

These tools let CoCo delegate work to specialized subagents, ask you questions during execution,
and coordinate complex multi-step workflows.

### RunSubagent

Launch an autonomous subagent to handle a specific subtask. CoCo uses this tool when a task benefits
from parallel execution or when a specialized agent type is better suited to the work. Each subagent
runs independently and returns its results when finished.

Available subagent types:

- **general-purpose**: Full tool access, used for research and multi-step tasks
- **Explore**: Optimized for fast codebase navigation and search
- **Plan**: Focused on architecture decisions and implementation planning
- **Custom agents**: Defined in your project’s `.cortex/agents/` directory

See  for details.

### AskUserQuestion

Prompt you for input when CoCo needs clarification or a decision. CoCo uses this tool instead of
guessing when your intent is ambiguous, when multiple valid approaches exist, or when a decision
requires your judgment.

Supports:

- Multiple choice questions with descriptions
- Free-form text input with suggested defaults
- Multi-select options for non-exclusive choices

### Review

Launch a specialized review subagent to check work for quality issues. CoCo may use this tool
after completing implementation work to verify correctness.

## Web tools

These tools let CoCo search the internet and fetch web page content, providing access to current
documentation, API references, and other online resources.

### WebSearch

Search the web for current information. CoCo uses this tool when your question involves recent
events, external documentation, or information beyond its training data.

Supports:

- Multiple search engine fallbacks for reliability
- Snippet extraction from search results
- Result caching to avoid redundant searches
- 30-second timeout per search

Note

WebSearch requires enabling web search in the CoCo settings in Snowsight. See [Web search](/user-guide/cortex-code/cortex-code-snowsight#label-cortex-code-web-search).

### WebFetch

Retrieve and extract text content from a specific URL. CoCo uses this tool when you share a link,
when it needs to read documentation at a known URL, or when search results point to a relevant page.

Supports:

- Automatic HTML-to-text conversion
- Content extraction and cleaning
- Maximum 10,000 characters per fetch
- 30-second timeout

## Snowflake tools

These tools connect CoCo directly to your Snowflake account, letting it execute SQL, search for
database objects, query documentation, and work with Cortex AI features.

### SnowflakeSqlExecute

Execute SQL queries and DDL statements against your Snowflake account. CoCo uses this tool for
data exploration, schema changes, query debugging, and any task that requires interacting with
your Snowflake data.

Supports:

- Permission-level checks before execution
- Result caching to avoid re-running identical queries
- Automatic token refresh for long sessions
- Large result offloading for queries that return many rows

### SnowflakeObjectSearch

Perform semantic search across your Snowflake database objects. CoCo uses this tool to discover
tables, views, and functions that match your intent, even when you don’t know the exact object name.

| Searches | tables, views, schemas, databases, functions |
| --- | --- |
| Returns | names, columns, descriptions |

Expand

Show lessSee more

### SnowflakeProductDocs

Search the official Snowflake documentation. CoCo uses this tool to find accurate syntax references,
feature explanations, and best practices when answering questions about Snowflake capabilities.

Supported categories:

- User guide
- SQL reference
- Developer guide
- CoCo topics

### ReflectSemanticModel

Validate a Cortex Analyst semantic model YAML file. CoCo uses this tool to check your semantic model
for errors before deploying it, catching issues at each validation stage.

Validation stages:

- File existence check
- YAML syntax validation
- Schema structure validation
- Server-side semantic validation

### SnowflakeMultiCortexAnalyst

Execute natural-language queries through Cortex Analyst. CoCo uses this tool when you ask data
questions that should be answered through a semantic model rather than by writing SQL directly.

Supports:

- Natural language to SQL translation
- Semantic model context awareness
- Verified Query Retrieval for trusted answers

## Data tools

These tools support data comparison and notebook workflows, helping CoCo work with
structured data and interactive computing environments.

### DataDiff

Compare data between databases or tables to identify differences. CoCo uses this tool when you
need to verify that a migration, transformation, or replication produced consistent results.

Supports:

- Snowflake connection handling for cross-database comparison
- Account identifier derivation
- 300-second timeout for large comparisons

### NotebookExecute

Execute Jupyter notebook cells programmatically. CoCo uses this tool to run notebook code,
verify outputs, or execute data analysis workflows.

Supports:

- Configurable timeout per cell
- Kernel management (start, restart, interrupt)
- Parameter injection for parameterized notebooks
- Custom Python environment support

### NotebookEdit

Edit Jupyter notebook cells without executing them. CoCo uses this tool to modify notebook
content when you ask it to update code, add documentation cells, or restructure a notebook.

Supported modes:

- **replace**: Replace the content of an existing cell
- **insert**: Add a new cell at a specific position
- **delete**: Remove a cell from the notebook

## Plan mode tools

These tools manage CoCo’s planning workflow, which is used for complex tasks that benefit from
structured thinking before implementation.

### EnterPlanMode

Switch CoCo into plan mode for complex, multi-step tasks. In plan mode, CoCo focuses on designing
an approach rather than making immediate changes. CoCo enters plan mode automatically for tasks
with significant architectural decisions or multiple valid approaches.

### ExitPlanMode

Present a completed plan for your approval and return to implementation mode. After you review
and approve the plan, CoCo proceeds with execution.

## Memory tools

### Memory

Store and retrieve persistent information across CoCo sessions. CoCo uses this tool to remember
your preferences, project context, and decisions so that future sessions can build on past work
without starting from scratch.

Supported commands:

- **view**: Read stored memory files
- **create**: Store new information
- **str\_replace**: Update existing memory content
- **insert**: Add content at a specific location
- **delete**: Remove a memory file
- **rename**: Rename or move a memory file

Note

The Memory tool must be enabled by setting the CORTEX\_ENABLE\_MEMORY environment variable.

## Permission levels

Tools have different permission requirements based on their potential impact. CoCo’s three-tier
approval system (Auto, Confirm, Deny) determines how each tool is handled:

| Level | Tools | Behavior |
| --- | --- | --- |
| Safe | Read, Glob, Grep | Auto-approved |
| Low | Write (new files) | Usually auto-approved |
| Medium | Edit, Bash (safe) | Prompts in Confirm mode |
| High | Bash (risky), SQL write | Always prompts |
| Critical | rm -rf, sudo | Extra confirmation |

Expand

Show lessSee more

See [Security](/user-guide/cortex-code/security) for details.
