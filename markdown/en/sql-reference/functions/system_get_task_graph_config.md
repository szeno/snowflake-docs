Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$GET\_TASK\_GRAPH\_CONFIG

Returns information from a [task graph](/user-guide/tasks-graphs) configuration.

For information about storing configuration values in a task graph, see [CREATE TASK … CONFIG](/sql-reference/sql/create-task).

## Syntax

Copy code

```
SYSTEM$GET_TASK_GRAPH_CONFIG( [<configuration_path>] )
```

## Arguments

`configuration_path`
:   Optional path of the configuration value to return.

    Uses the same syntax as Snowflake queries for semi-structured data.
    See [GET\_PATH](/sql-reference/functions/get_path) for more information.

## Examples

The following example creates a task that defines a configuration and then uses
the SYSTEM$GET\_TASK\_GRAPH\_CONFIG function to retrieve values from the configuration.

Copy code

```
CREATE OR REPLACE TASK root_task_with_config
  WAREHOUSE = mywarehouse
  SCHEDULE = '10 m'
  CONFIG = $${"output_dir": "/temp/test_directory/", "learning_rate": 0.1}$$
  AS
  BEGIN
    LET OUTPUT_DIR STRING := SYSTEM$GET_TASK_GRAPH_CONFIG('output_dir')::string;
    LET LEARNING_RATE DECIMAL := SYSTEM$GET_TASK_GRAPH_CONFIG('learning_rate')::DECIMAL;
    ...
  END;
```

### Example: Pass configuration information to another task in a task graph

You can pass configuration information by using a JSON object
that other tasks in a task graph can read.

Use the syntax CREATE/ALTER TASK … CONFIG to set, unset,
or modify the configuration information in the root task.
Then, use the SYSTEM$GET\_TASK\_GRAPH\_CONFIG function to retrieve it.

The following example shows how you can use a JSON object to pass configuration information and
store it in a table:

Copy code

```
CREATE OR REPLACE TASK my_task_root
  SCHEDULE = '1 MINUTE'
  USER_TASK_TIMEOUT_MS = 60000
  CONFIG = $${"environment":"production", "dir":"/my_prod_directory/"}$$
  AS SELECT 1;

CREATE OR REPLACE TASK my_child_task
  USER_TASK_TIMEOUT_MS = 600000
  AFTER my_task_root
  AS
    BEGIN
      LET value := (SELECT SYSTEM$GET_TASK_GRAPH_CONFIG('dir'));
      CREATE TABLE IF NOT EXISTS my_table(name VARCHAR, value VARCHAR);
      INSERT INTO my_table VALUES('my_task_root dir',:value);
    END;
```
