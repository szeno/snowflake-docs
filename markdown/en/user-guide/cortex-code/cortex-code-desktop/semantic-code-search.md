# Semantic code search

Semantic code search (**tgrep**) lets the CoCo Desktop agent find the right files in your
codebase from a plain-English description, not just an exact string match. It’s powered by
Snowflake Cortex embeddings, so the agent can locate relevant code by meaning — for example,
“where do we validate the connection before running a query” — even when the wording doesn’t
appear verbatim in the source.

## How it works

tgrep is available to the agent as a search tool that can run in **semantic**, **keyword**, or
**hybrid** mode. The first time it’s used in a workspace, CoCo bootstraps an index for that
workspace; a status-bar indicator shows indexing progress. Once indexed, searches run against
the local index and stay current as your files change.

Note

Semantic search runs on your local machine, so it isn’t available in remote or virtual
workspaces such as Remote-SSH connections or dev containers. Open the folder locally to use
it. tgrep also requires account access to the `snowflake-arctic-embed-l-v2.0` embedding
model and an active Snowflake connection.

## Consent

tgrep asks before it indexes and searches a workspace for the first time, so indexing your
code is always something you opt into per workspace. You can pause searching for a workspace
at any time — the existing index is kept and reused when you turn it back on — or reset the
choice so CoCo asks again.

## The Indexing settings page

Open **Agent Settings** and select **Indexing** to manage semantic search:

| Control | What it does |
| --- | --- |
| **Enable semantic search (tgrep)** | Global switch. When off, tgrep is never used and never indexes any workspace. |
| **Search this workspace** | Turn indexing and searching on or off for the current workspace. Off pauses it and keeps the index. |
| **Index workspace** / **Re-index** | Build or rebuild the semantic index for the current workspace now. |
| **Delete index** | Erase the stored index for a workspace and free its disk space. |
| **All Indexes** | Review every workspace that currently has an index. |

Expand

Show lessSee more

## Using it

Most of the time you don’t invoke tgrep directly — the agent reaches for it when a task calls
for finding relevant code. You can also ask explicitly, for example: “Search the codebase for
where we handle retry logic.” If semantic search is disabled or the workspace isn’t indexed,
the agent falls back to standard keyword search.
