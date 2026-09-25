# Running notebooks with parameters

Feature — Generally Available

Available to all AWS, Azure, and GCP commercial regions. PrivateLink is supported.

Parameters passed in the `ARGUMENTS` list are placed into the `sys.argv` list, with one entry per argument.

The examples on this page use [EXECUTE CODE BUNDLE](/sql-reference/sql/execute-code-bundle), which takes a list of
argument strings. The older [EXECUTE NOTEBOOK PROJECT](/sql-reference/sql/execute-notebook-project) command takes a single
string instead. To pass a value that’s computed at runtime, such as a task configuration value, see
[Pass arguments computed at runtime](/sql-reference/sql/execute-code-bundle#label-execute-code-bundle-dynamic-arguments).

## Example: Execute a Code Bundle with parameters

The following example passes two arguments (`env` and `prod`) using `ARGUMENTS = ('env', 'prod')`.

The first element (`sys.argv[0]`) is the notebook filename, followed by each argument in the list.

Copy code

```
EXECUTE CODE BUNDLE "<database_name>"."<schema_name>"."<bundle_name>"
  ENTRYPOINT = 'path/to/notebook.ipynb' -- Notebook file to run
  ARGUMENTS = ('env', 'prod'); -- Each element is passed as a separate argument. Point to the environment configuration.
```

The compute pool, runtime, query warehouse, and dependencies are defined in the Code Bundle’s `code_bundle.yml` specification.

## View all arguments

To inspect the full list of parameters passed to the session, use the `sys` module.

Copy code

```
import sys
print(sys.argv)
```

Output example:

```
['exampletestSCOS.ipynb', 'env', 'prod']
```

## Print each argument

To process or log each parameter individually, loop through the `sys.argv` list.

Copy code

```
import sys
for arg in sys.argv:
    print(arg)
```

Output example:

```
exampletestSCOS.ipynb
env
prod
```

## Access a specific argument

Parameters are accessed by their index in the list. Because `sys.argv[0]` is the notebook name, the first user parameter starts at `index[1]`.

Copy code

```
import sys

# Access the first user parameter
first_param = sys.argv[1]
print(first_param)
```

Output example:

```
env
```

For full syntax and parameter details, see [EXECUTE CODE BUNDLE](/sql-reference/sql/execute-code-bundle).
