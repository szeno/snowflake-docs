# ALTER TASK GRAPH

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Modifies the properties, member defaults, or lifecycle state of an existing [Task Graph Object](/user-guide/task-graph-object).

This command supports the following variants:

- [ALTER TASK GRAPH … SET / UNSET](#label-alter-task-graph-set-unset): Sets or unsets graph-wide properties, member defaults, the graph’s `WHEN` condition, tags, or contacts.
- [ALTER TASK GRAPH … COMMIT](#label-alter-task-graph-commit): Freezes staged changes into a new committed version.
- [ALTER TASK GRAPH … REVERT](#label-alter-task-graph-revert): Discards staged changes.
- [ALTER TASK GRAPH … RESUME](#label-alter-task-graph-resume): Starts running the graph on its schedule.
- [ALTER TASK GRAPH … SUSPEND](#label-alter-task-graph-suspend): Stops scheduling new runs.

See also:
:   [CREATE TASK GRAPH](/sql-reference/sql/create-task-graph), [DROP TASK GRAPH](/sql-reference/sql/drop-task-graph), [EXECUTE TASK GRAPH](/sql-reference/sql/execute-task-graph), [SHOW TASK GRAPHS](/sql-reference/sql/show-task-graphs)

## Syntax

### ALTER TASK GRAPH … SET / UNSET

Copy code

```
ALTER TASK GRAPH [ IF EXISTS ] <name> SET
  <property> = <value> [ , <property> = <value> ... ]

ALTER TASK GRAPH [ IF EXISTS ] <name> UNSET
  <property> [ , <property> ... ]

ALTER TASK GRAPH [ IF EXISTS ] <name> SET TASK_DEFAULTS (
  <default_property> = <value> [ , <default_property> = <value> ... ] )

ALTER TASK GRAPH [ IF EXISTS ] <name> UNSET TASK_DEFAULTS (
  <default_property> [ , <default_property> ... ] )

ALTER TASK GRAPH [ IF EXISTS ] <name> MODIFY WHEN <boolean_expr>

ALTER TASK GRAPH [ IF EXISTS ] <name> REMOVE WHEN

ALTER TASK GRAPH [ IF EXISTS ] <name> SET TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]

ALTER TASK GRAPH [ IF EXISTS ] <name> UNSET TAG <tag_name> [ , <tag_name> ... ]

ALTER TASK GRAPH [ IF EXISTS ] <name> SET CONTACT <purpose> = <contact_name> [ , <purpose> = <contact_name> ... ]

ALTER TASK GRAPH [ IF EXISTS ] <name> UNSET CONTACT <purpose> [ , <purpose> ... ]
```

Changes graph-wide properties, member defaults, or the graph’s `WHEN` condition. The properties are the ones listed in [CREATE TASK GRAPH](/sql-reference/sql/create-task-graph). Once the graph has a committed version, these changes are staged until you `COMMIT`, whether the graph is resumed or suspended.

Important

`SET TASK_DEFAULTS` performs a **merge**, not a replace — it changes only the properties you name, leaving the rest of the set untouched. To remove a default, use `UNSET TASK_DEFAULTS ( <property> )`. An unqualified `UNSET TASK_DEFAULTS` (with no property list) is not supported.

### ALTER TASK GRAPH … COMMIT

Copy code

```
ALTER TASK GRAPH [ IF EXISTS ] <name> COMMIT
```

Validates the graph and freezes the current shape and settings into a new committed version. The next run uses the new version. `COMMIT` does not start the schedule and has no `SCHEDULE` or `WHEN` requirement.

### ALTER TASK GRAPH … REVERT

Copy code

```
ALTER TASK GRAPH [ IF EXISTS ] <name> REVERT
```

Discards all staged (uncommitted) changes to the graph and its member tasks, restoring them to the most recently committed version. Member tasks that were newly added but never committed are disconnected from the graph rather than dropped. `REVERT` returns an error if the graph has never been committed.

### ALTER TASK GRAPH … RESUME

Copy code

```
ALTER TASK GRAPH [ IF EXISTS ] <name> RESUME
```

Starts running the graph on its schedule using the most recently committed version. The graph must have a committed version.

Important

A task graph must have a `SCHEDULE` or a `WHEN` condition set before it can be resumed. `RESUME` fails on a graph that has neither.

If you want a graph that never runs on its own and only runs when you trigger it manually with [EXECUTE TASK GRAPH](/sql-reference/sql/execute-task-graph), omit both `SCHEDULE` and `WHEN`: you can still `COMMIT` it and run it on demand. To avoid unintended scheduling, don’t call `RESUME`.

### ALTER TASK GRAPH … SUSPEND

Copy code

```
ALTER TASK GRAPH [ IF EXISTS ] <name> SUSPEND
```

Stops scheduling new runs of the graph.

## Usage notes

- A running graph executes against a **committed version**: a frozen snapshot of the graph’s shape and settings captured when you run `COMMIT`. Altering a resumed graph does not disturb runs in progress — changes are staged until the next `COMMIT`.
- Use [TASK\_GRAPH\_CHANGES](/sql-reference/functions/task_graph_changes) to see exactly what a `COMMIT` would deploy or what a `REVERT` would discard.
- `COMMIT`, `RESUME`, and `SUSPEND` require the OPERATE privilege on the task graph, or ownership of it. You don’t need OPERATE on the individual member tasks.
- `SET` and `UNSET` require ownership of the task graph.

## Examples

Change graph-wide properties and member defaults:

Copy code

```
-- Graph-wide property
ALTER TASK GRAPH my_pipeline SET SCHEDULE = '30 SECONDS';

-- Graph configuration (valid JSON). Supply the entire replacement string;
-- you can't update individual key-value pairs.
ALTER TASK GRAPH my_pipeline SET
  CONFIG = $${"output_dir": "/temp/prod_directory/", "environment": "prod"}$$;

-- Remove graph configuration
ALTER TASK GRAPH my_pipeline UNSET CONFIG;

-- Member defaults. SET TASK_DEFAULTS merges into the existing defaults —
-- it does not replace the whole set — so this changes only WAREHOUSE.
ALTER TASK GRAPH my_pipeline SET TASK_DEFAULTS ( WAREHOUSE = new_wh );

-- Remove a specific default. The property name must be specified.
ALTER TASK GRAPH my_pipeline UNSET TASK_DEFAULTS ( LOG_LEVEL );
```

Commit and resume a graph:

Copy code

```
ALTER TASK GRAPH my_pipeline COMMIT;
ALTER TASK GRAPH my_pipeline RESUME;
```

Stage changes, then discard them:

Copy code

```
-- Stage some changes...
ALTER TASK GRAPH my_pipeline SET SCHEDULE = '5 MINUTES';
ALTER TASK t_a SET WAREHOUSE = other_wh;

-- ...then discard them. Both edits are undone.
ALTER TASK GRAPH my_pipeline REVERT;
```

Add or remove a member task. Membership is defined by `AFTER` relationships reachable from the root; these are ordinary [CREATE TASK](/sql-reference/sql/create-task) / [ALTER TASK](/sql-reference/sql/alter-task) operations that become staged changes on a resumed graph:

Copy code

```
-- Add a member
CREATE OR REPLACE TASK t_extra AFTER t_a AS SELECT 'added';
ALTER TASK GRAPH my_pipeline COMMIT;   -- committed version now includes t_extra

-- Remove a member (sever, then commit, then drop)
ALTER TASK t_extra REMOVE AFTER t_a;
ALTER TASK GRAPH my_pipeline COMMIT;
DROP TASK t_extra;
```
