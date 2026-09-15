# Profiling Snowpark Python stored procedure handlers

You can discover how much time or memory was spent executing your handler code by using the built-in code profiler. The profiler generates
information describing how much time or memory was spent executing each line of the procedure handler.

Using the profiler, you can generate reports that focus on one of the following at a time:

- **Amount of time per line**, in which the report shows the number of times a line was executed, how long the execution took, and so on.
- **Amount of memory usage per line**, in which the report shows the amount of memory consumed per line.

The profiler saves the generated report to the Snowflake [internal user stage](/user-guide/data-load-overview#label-data-load-overview-internal-stages) you specify.
You can [read the profiler output](#label-snowpark-python-profiler-view-output) using the `StoredProcedureProfiler.get_output`
function.

Note

Profiling introduces performance overhead on Python execution and can affect the performance of the query.
It’s intended for development and testing and should not be enabled on continuous production workloads.

## Required privileges

When a stored procedure is executed after the `StoredProcedureProfiler.set_active_profiler` function is called, Snowflake checks
the following privileges for the user executing the procedure:

- You must have read write privileges on the profiling output stage.
- If the profiled stored procedure is a [caller’s rights stored procedure](/developer-guide/stored-procedure/stored-procedures-rights#label-stored-procedure-session-state-caller),
  you must use a role with USAGE privilege on the stored procedure.
- If the profiled stored procedure is an [owner’s rights stored procedure](/developer-guide/stored-procedure/stored-procedures-rights#label-stored-procedure-session-state-owners),
  you must use a role with OWNERSHIP privilege on the stored procedure.

## Limitations

- Only stored procedures are supported. UDFs support is not available yet.
- Recursive profiling is not supported. Only top-level functions of the specified modules are profiled, while functions defined inside
  functions are not.
- Profiling stored procedures created on the client-side via the `snowflake.snowpark` API is not supported.
- Python functions running in parallel through `joblib` are not profiled.
- System defined stored procedures cannot be profiled. They produce no output.
- The profiling API must be used in the same thread as the procedure was called from.

## Usage

Once you’ve set up the profiler for use, you can use it simply by calling the stored procedure to generate profiler output. After the
procedure finishes executing, the profiler’s output is written to a file on the stage you specify. You can fetch the profiler output
using a system function, as described below.

Follow these steps in your code to set up and use the profiler:

1. Acquire a profiler object from the `Session` object.
2. Specify the Snowflake stage where profile output should be written.
3. Enable the profiler and set what the profile report should focus on.
4. Call the stored procedure.
5. View profiling output.

### Acquire profiler object

In Python, create a variable of type `StoredProcedureProfiler` with which to configure and run the profiler.

Copy code

```
# Create your session
session = Session.builder.configs(CONNECTION_PARAMETERS).create()

# Acquire profiler object
profiler = session.stored_procedure_profiler
```

### Specify the Snowflake stage where profile output should be written

Before running the profiler, you must specify a stage in which to save the output. To specify the stage, call
`StoredProcedureProfiler.set_target_stage`, specifying the fully-qualified name of an internal
[Snowflake stage](/user-guide/data-load-overview#label-data-load-overview-internal-stages) to which the report should be written.

Keep in mind the following:

- The stage name must be a fully-qualified name.
- If the stage you put into this function does not exist, Snowflake creates a temporary stage with that name.
- If you want to preserve the profiler output outside of the scope of the session, create a permanent stage before executing
  `set_target_stage` and specify that permanent stage’s name in the function call.
- If you do not set a target stage with `set_target_stage`, Snowflake sets the current session’s temporary stage as the target
  stage. To discover that temporary stage, call `Session.get_session_stage`.

Code in the following example creates a temporary `profiler_output` stage to receive the profiler output.

Copy code

```
profiler.set_target_stage("mydb.myschema.profiler_output")
```

### Enable the profiler by specifying its focus

Use the `StoredProcedureProfiler.set_active_profiler` function, specifying a value indicating which kind of profile report you want
to generate.

- To have the profiler report on line use activity, set the parameter to the `LINE` value (case insensitive), as shown below:

  Copy code

  ```
  profiler.set_active_profiler("LINE")
  ```
- To have the profiler report on memory use activity, set the parameter to the `MEMORY` value (case insensitive), as shown below:

  Copy code

  ```
  profiler.set_active_profiler("MEMORY")
  ```

To disable the profiler, use the `StoredProcedureProfiler.disable` function.

### Call the stored procedure

After the profiler is enabled, [call your stored procedure](/developer-guide/snowpark/python/calling-functions#label-snowpark-python-stored-procedures).

Copy code

```
session.call("my_stored_procedure")
```

### View profiling output

At the end of execution, you can access the output using the `StoredProcedureProfiler.get_output` function.

Copy code

```
profiler.get_output()
```

## Including additional modules for profiling

When profiling, you can include modules that aren’t included by default.

By default, methods defined in the your module are profiled. These methods include the following:

- The handler method
- Methods defined in the module
- Methods imported from packages or other modules

To include additional modules for profiling, use the `StoredProcedureProfiler.register_modules` function, specifying the modules
you want to include.

Code in the following example registers modules module\_A and module\_B for profiling.

Copy code

```
profiler.register_modules(["module_A", "module_B"])
```

To unregister registered modules, use `register_modules` with no arguments, as in the following example.

Copy code

```
profiler.register_modules()
```

## Example

The following examples illustrate how to use the profiler to generate and retrieve a report of line usage.

Code in this example creates a procedure `profiler_test_proc`.

Copy code

```
CREATE OR REPLACE PROCEDURE profiler_test_proc()
RETURNS NUMBER
LANGUAGE PYTHON
RUNTIME_VERSION = 3.12
PACKAGES = ('snowflake-snowpark-python')
HANDLER = 'main'
AS
$$
from snowflake.snowpark.functions import col, udf

def main(session):
  df = session.sql("select 1")
  return df.collect()[0][0]
$$;
```

Code in the following example sets up a profiler, then profiles the `profiler_test_proc` procedure.

Copy code

```
profiler = profiler_session.stored_procedure_profiler
profiler.register_modules(["profiler_test_proc"])
profiler.set_target_stage(
  f"{db_parameters['database']}.{db_parameters['schema']}.{tmp_stage_name}"
)

profiler.set_active_profiler("LINE")

profiler_session.call("profiler_test_proc")
res = profiler.get_output()
print(res)

profiler.disable()
profiler.register_modules([])
```

The generated line profiler output looks like this:

```
Handler Name: main
Python Runtime Version: 3.12
Modules Profiled: ['main_module']
Timer Unit: 0.001 s

Total Time: 0.0619571 s
File: _udf_code.py
Function: main at line 4

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     4                                           def main(session):
     5         1          0.4      0.4      0.6      df = session.sql("select 1")
     6         1         61.6     61.6     99.4      return df.collect()[0][0]
```
