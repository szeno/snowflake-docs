# Developer tools

Feature — Generally Available

Available to all AWS, Azure, and GCP commercial regions. PrivateLink is supported.

Developer tools include the **Variables Explorer**, the **Terminal**, the **Scratchpad**, and the **Dependency graph**.
These tools allow you to explore and interact with your data and the notebook environment.

To access the developer tools, in the control bar at the top of the notebook, select <icon>:ui:*Tools*.

[![Notebook tools icon](/static/images/snowsight/workspaces/notebook-tools-icon.png)](/static/images/snowsight/workspaces/notebook-tools-icon.png)

You must be connected to a notebook service to use the developer tools. Switching to a different service will restart
the tools.

## Using the Variables Explorer

The Variables Explorer is a visual tool that lets you inspect the variables currently loaded in your session while you
are working interactively. It shows the **Name**, **Type**, **Shape**, and **Preview** for each variable. Variables are
updated when a cell finishes running.

## Using the Terminal

The Terminal lets you run any shell command in the notebook’s container environment:

- Install dependencies: `pip install`, `pip list`, or check installed packages.
- Manage files: `ls`, `pwd`, navigate directories, and view files.
- Run parallel jobs
- Monitor compute resource usage

Example for installing and running `htop` for monitoring compute resource usage in real time:

Copy code

```
# If installation fails, run `apt update` first
apt install htop
htop
```

## Using the Scratchpad

The Scratchpad is an exploratory space for you to quickly experiment with code, ideas, calculations, or notes without
worrying about structure or polish. Commands that you execute in the Scratchpad don’t change the notebook file.

You can do the following in the Scratchpad:

- Quick ad-hoc queries: Test SQL without adding cells to your notebook.
- Data exploration: Verify table contents, schemas, or run exploratory queries.
- Debugging: Verify data or test query fragments before adding them to notebook cells.
- One-off operations: Run commands that don’t need to be saved (such as SHOW GRANTS or DESCRIBE TABLE).

Results stay visible while you work but aren’t saved with the notebook.

## Using the Dependency graph

Each Python and SQL cell is visualized as a tile. The arrows linking an upstream cell and the downstream cell (or cells)
indicate variable referencing relationships. When you hover over the arrow, it shows all the variables from the upstream
cell being referenced in a particular downstream cell. Any cell can have none, one, or multiple downstream cells.

The Dependency graph provides the same **Run current cell + all descendant cells** option as in the main notebook editor.

For example:

- `cell_1`: you have a simple `!pip install` command. `cell_1` doesn’t have any downstream cells.
- `cell_2`: you have `var = 10`. `var` is then used in `cell_3`, `cell_5`, and `cell_10`. There will be one arrow
  pointing from `cell_2` to each of those three downstream cells.
- Later, if you update `cell_2` to `var = 100`, you can use **Run current cell + all descendant cells** to update
  `cell_3`, `cell_5`, and `cell_10`.
