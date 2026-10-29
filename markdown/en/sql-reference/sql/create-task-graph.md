# CREATE TASK GRAPH

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Creates a [Task Graph Object](/user-guide/task-graph-object) — a first-class database object that encapsulates a set of member tasks and their graph-wide settings.

This command supports the following variants:

- [CREATE OR ALTER TASK GRAPH](#label-create-or-alter-task-graph-syntax): Creates the task graph if it doesn’t exist, or alters an existing one to match the statement.
- [DEFINE TASK GRAPH](#label-define-task-graph-syntax): Declarative definition of a task graph, including its desired state, inside a DCM project.

See also:
:   [ALTER TASK GRAPH](/sql-reference/sql/alter-task-graph), [DROP TASK GRAPH](/sql-reference/sql/drop-task-graph), [EXECUTE TASK GRAPH](/sql-reference/sql/execute-task-graph), [SHOW TASK GRAPHS](/sql-reference/sql/show-task-graphs), [DESCRIBE TASK GRAPH](/sql-reference/sql/desc-task-graph)

Important

Member tasks are created and altered with the standard [CREATE TASK](/sql-reference/sql/create-task) and [ALTER TASK](/sql-reference/sql/alter-task) commands. `CREATE TASK GRAPH` only creates the graph object over an existing set of tasks connected by `AFTER` relationships.

## Syntax

Copy code

```
CREATE [ OR REPLACE ] TASK GRAPH [ IF NOT EXISTS ] <name>
  [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
  [ WITH CONTACT ( <purpose> = <contact_name> [ , <purpose> = <contact_name> ... ] ) ]
  [ SCHEDULE = { '<num> { HOURS | MINUTES | SECONDS }'
               | 'USING CRON <expr> <time_zone>' } ]
  [ ROOTS = ( <root_task_name> ) ]
  [ FINALIZER = <finalizer_task_name> ]
  [ OVERLAP_POLICY = { NO_OVERLAP | ALLOW_CHILD_OVERLAP | ALLOW_ALL_OVERLAP } ]
  [ ERROR_INTEGRATION = <integration_name> ]
  [ SUCCESS_INTEGRATION = <integration_name> ]
  [ CONFIG = <configuration_string> ]
  [ TASK_AUTO_RETRY_ATTEMPTS = <num> ]
  [ SUSPEND_TASK_AFTER_NUM_FAILURES = <num> ]
  [ COMMENT = '<string>' ]
  [ TASK_DEFAULTS ( <default_property> = <value>
                    [ , <default_property> = <value> ... ] ) ]
  [ WHEN <condition> ]
```

## Variant syntax

### CREATE OR ALTER TASK GRAPH

Creates the graph if it doesn’t exist, or updates an existing graph to match the statement. Any property the statement omits is unset or reset to its default on the existing graph: for example, omitting `FINALIZER` removes the finalizer, and omitting `TASK_DEFAULTS` removes all task defaults.

Copy code

```
CREATE OR ALTER TASK GRAPH <name>
  [ SCHEDULE = { '<num> { HOURS | MINUTES | SECONDS }'
               | 'USING CRON <expr> <time_zone>' } ]
  [ ROOTS = ( <root_task_name> ) ]
  [ FINALIZER = <finalizer_task_name> ]
  [ OVERLAP_POLICY = { NO_OVERLAP | ALLOW_CHILD_OVERLAP | ALLOW_ALL_OVERLAP } ]
  [ ERROR_INTEGRATION = <integration_name> ]
  [ SUCCESS_INTEGRATION = <integration_name> ]
  [ CONFIG = <configuration_string> ]
  [ TASK_AUTO_RETRY_ATTEMPTS = <num> ]
  [ SUSPEND_TASK_AFTER_NUM_FAILURES = <num> ]
  [ COMMENT = '<string>' ]
  [ TASK_DEFAULTS ( <default_property> = <value>
                    [ , <default_property> = <value> ... ] ) ]
  [ WHEN <condition> ]
```

Note

`CREATE OR ALTER TASK GRAPH` does not resume or suspend a graph. Use [ALTER TASK GRAPH](/sql-reference/sql/alter-task-graph) for lifecycle management.

### DEFINE TASK GRAPH

DCM Projects uses `DEFINE TASK GRAPH` statements to create and manage task graphs declaratively inside a DCM project. A `DEFINE TASK GRAPH`
statement uses the same syntax as [CREATE OR ALTER TASK GRAPH](#label-create-or-alter-task-graph-syntax), with the keyword `DEFINE` in
place of `CREATE OR ALTER`.
You can use `DEFINE TASK GRAPH` only inside DCM project definition files, not as standalone SQL.
To learn more about DCM Projects, see [Task graph](/user-guide/dcm-projects/dcm-projects-supported-entities#label-dcm-projects-object-type-task-graph).

`DEFINE TASK GRAPH` also accepts a `STARTED` or `SUSPENDED` keyword that isn’t part of `CREATE OR ALTER TASK GRAPH` syntax. The keyword
sets the desired state of the task graph as a whole. A task that is a member of a task graph can’t have its own desired state. A standalone
[DEFINE TASK](/sql-reference/sql/create-task#label-define-task-syntax) statement can set `STARTED` or `SUSPENDED` for a task that isn’t a
member of a task graph.

## Parameters

`name`
:   String that specifies the identifier for the task graph; must be unique for the schema in which it is created. For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

`SCHEDULE = ...`
:   Specifies the schedule for periodically running the graph. A schedule must be defined, or a `WHEN` condition set, for the graph to be resumable; otherwise it only runs when manually triggered with [EXECUTE TASK GRAPH](/sql-reference/sql/execute-task-graph).

`ROOTS = ( root_task_name )`
:   Specifies the root task of the graph. A task graph has exactly one root, so the list must contain exactly one task.

    You can create a graph without `ROOTS` and set it later. The graph must have a root before you can commit, resume, or execute it.

`FINALIZER = finalizer_task_name`
:   Specifies the name of a task that runs after every other task in the graph completes, used for cleanup or notifications. This replaces the per-task `FINALIZE` property that root-task-based graphs use.

`OVERLAP_POLICY = { NO_OVERLAP | ALLOW_CHILD_OVERLAP | ALLOW_ALL_OVERLAP }`
:   Specifies the overlap policy for graph runs. See [Optional parameters](/sql-reference/sql/create-task#label-create-task-optional-parameters) for the equivalent task-level semantics.

    Default: `NO_OVERLAP`

`ERROR_INTEGRATION = integration_name`
:   Specifies the name of the notification integration used to send error notifications for the graph.

`SUCCESS_INTEGRATION = integration_name`
:   Specifies the name of the notification integration used to send success notifications for the graph.

`CONFIG = configuration_string`
:   Specifies a configuration string in valid JSON format that all tasks in the graph can access.

`TASK_AUTO_RETRY_ATTEMPTS = num`
:   Specifies the number of automatic retry attempts for the graph after a failed run.

    Values: `0` - `30`. Default: `0`

`SUSPEND_TASK_AFTER_NUM_FAILURES = num`
:   Specifies the number of consecutive failed graph runs after which the graph is suspended automatically.

`COMMENT = 'string'`
:   Specifies a comment for the task graph.

`TASK_DEFAULTS ( default_property = value [ , ... ] )`
:   Specifies default settings that cascade to every member task unless the member overrides them. Only the following properties are supported: `WAREHOUSE`, `USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE`, `TARGET_COMPLETION_INTERVAL`, `SERVERLESS_TASK_MIN_STATEMENT_SIZE`, `SERVERLESS_TASK_MAX_STATEMENT_SIZE`, `USER_TASK_TIMEOUT_MS`, `EXECUTE AS USER <user_name>`, `COMMENT`, `LOG_LEVEL`, and `TRACE_LEVEL`.

`WHEN condition`
:   Specifies a Boolean SQL expression that must be true for a graph run to start. If the root task also has a `WHEN` condition, both must be true. The graph’s condition applies only to starting the run; it isn’t evaluated again for the other member tasks.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE TASK | Schema | Task graphs use the CREATE TASK privilege; there is no separate privilege for creating a task graph. |
| EXECUTE TASK | Account | Required to run the graph. |
| EXECUTE MANAGED TASK | Account | Required only if member tasks use serverless compute. |
| USAGE | Integration | Required on any integration named in `ERROR_INTEGRATION` or `SUCCESS_INTEGRATION`. |
| OWNERSHIP | Task | The tasks named in `ROOTS` and `FINALIZER` must be owned by the same role that owns the graph. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- A newly created task graph is not started. It must be committed with [ALTER TASK GRAPH … COMMIT](/sql-reference/sql/alter-task-graph#label-alter-task-graph-commit) and then resumed with [ALTER TASK GRAPH … RESUME](/sql-reference/sql/alter-task-graph#label-alter-task-graph-resume) before it runs on its schedule.
- `TASK_DEFAULTS` supplied here is the initial set. A later `SET TASK_DEFAULTS` performs a merge into the existing set, not a replace — see [ALTER TASK GRAPH](/sql-reference/sql/alter-task-graph).
- Set `SCHEDULE`, `OVERLAP_POLICY`, `ERROR_INTEGRATION`, `SUCCESS_INTEGRATION`, `TASK_AUTO_RETRY_ATTEMPTS`, `SUSPEND_TASK_AFTER_NUM_FAILURES`, and `CONFIG` on the graph. Setting them on a member task returns an error. A finalizer is also declared on the graph with `FINALIZER`, instead of on the finalizer task with `FINALIZE`.
- The tasks named in `ROOTS` and `FINALIZER` must be owned by the role that owns the graph.

## Examples

Copy code

```
-- Member tasks. Compute, log level, etc. come from the graph's TASK_DEFAULTS.
CREATE OR REPLACE TASK t_root AS SELECT 1;
CREATE OR REPLACE TASK t_a    AFTER t_root AS SELECT 2;
CREATE OR REPLACE TASK t_b    AFTER t_root AS SELECT 3;
CREATE OR REPLACE TASK t_leaf AFTER t_a, t_b AS SELECT 4;
CREATE OR REPLACE TASK t_finalizer AS SELECT 'cleanup';

-- Graph object: schedule and finalizer live here;
-- warehouse, comment, and log level cascade to members via TASK_DEFAULTS.
CREATE OR REPLACE TASK GRAPH my_pipeline
  SCHEDULE = 'USING CRON 0 * * * * UTC'
  ROOTS = ( t_root )
  FINALIZER = t_finalizer
  TASK_DEFAULTS (
    WAREHOUSE = etl_wh,
    COMMENT = 'Hourly ETL pipeline',
    LOG_LEVEL = 'INFO'
  );
```

Create the graph if it doesn’t exist, or update it in place:

Copy code

```
CREATE OR ALTER TASK GRAPH my_pipeline
  SCHEDULE = 'USING CRON 0 * * * * UTC'
  ROOTS = ( t_root )
  FINALIZER = t_finalizer
  TASK_DEFAULTS (
    WAREHOUSE = etl_wh,
    COMMENT = 'Hourly ETL pipeline (updated)',
    LOG_LEVEL = 'INFO'
  );
```
