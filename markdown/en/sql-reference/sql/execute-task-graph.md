# EXECUTE TASK GRAPH

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Triggers one immediate run of a [Task Graph Object](/user-guide/task-graph-object)’s committed version, regardless of its schedule.

See also:
:   [CREATE TASK GRAPH](/sql-reference/sql/create-task-graph), [ALTER TASK GRAPH](/sql-reference/sql/alter-task-graph), [SHOW TASK GRAPHS](/sql-reference/sql/show-task-graphs)

## Syntax

Copy code

```
EXECUTE TASK GRAPH <name>
  [ USING CONFIG = <configuration_string> ]

EXECUTE TASK GRAPH <name> RETRY LAST

EXECUTE TASK GRAPH <name> RETRY GRAPH RUN GROUP '<graph_run_group_id>'
```

## Parameters

`name`
:   String that specifies the identifier of the task graph to run.

`USING CONFIG = configuration_string`
:   Specifies a JSON configuration string for this run only. It’s merged with the graph’s `CONFIG`: fields you specify override the graph’s values, and the rest come from the graph. The graph definition isn’t changed.

`RETRY LAST`
:   Retries the most recent failed run, starting from the tasks that failed or were canceled rather than re-running the entire graph. The retry is a new run in the same graph run group. The last run must be in state FAILED or CANCELED, and its first attempt must have started within the last 14 days.

`RETRY GRAPH RUN GROUP 'graph_run_group_id'`
:   Retries a specific earlier run, identified by its `GRAPH_RUN_GROUP_ID`, starting from the tasks that failed or were canceled. The run’s first attempt must have started within the last 14 days. To find the ID, query [COMPLETE\_TASK\_GRAPHS](/sql-reference/functions/complete_task_graphs) with `GRAPH_NAME`.

## Usage notes

- `EXECUTE TASK GRAPH` runs the **committed version** of the graph. Staged (uncommitted) changes aren’t included: if you’ve edited the graph or its member tasks and want those edits in the run, run [ALTER TASK GRAPH … COMMIT](/sql-reference/sql/alter-task-graph#label-alter-task-graph-commit) first, then `EXECUTE TASK GRAPH`.
- If the graph has never been committed, `EXECUTE TASK GRAPH` commits it once and then runs that first committed version.
- The graph doesn’t need to be resumed, and it doesn’t need a `SCHEDULE` or `WHEN`, so you can use this command to run a graph that runs only on demand.
- Requires the OPERATE privilege on the task graph, or ownership of it.

## Examples

Commit staged changes so they’re included in the run, then execute:

Copy code

```
ALTER TASK GRAPH my_pipeline COMMIT;
EXECUTE TASK GRAPH my_pipeline;
```

Run once with a configuration override:

Copy code

```
EXECUTE TASK GRAPH my_pipeline
  USING CONFIG = $${"environment": "testing"}$$;
```

Retry the most recent failed run:

Copy code

```
EXECUTE TASK GRAPH my_pipeline RETRY LAST;
```
