# Deploy a Snowpark project

The `snow snowpark deploy` command uploads local files to the specified stage and creates procedure and function objects defined in the project. Deploying the project alters all objects defined in it. By default, if any of the objects exist already the commands fails unless you provide the `--replace` option. All deployed objects use the same artifact, which is uploaded only once.

Copy code

```
snow snowpark deploy
```

```
+-------------------------------------------------------------+
| object                       | type      | status           |
|------------------------------+-----------+------------------|
| hello_procedure(name string) | procedure | created          |
| test_procedure()             | procedure | packages updated |
| hello_function(name string)  | function  | created          |
+-------------------------------------------------------------+
```

When you run `snow snowpark deploy`, the command does the following:

1. Snowflake CLI checks whether any of the defined objects (functions or procedures) already exists.
2. If any exist and the `--replace` flag is not provided, the command exits. The reasoning behind this approach is to be “production-safe” by avoiding unintentional changes to existing objects.
3. If all objects don’t exist or `--replace` is provided, the command:
   - If the `--prune` flag is provided, all previous contents of the stages used by defined procedure and function objects are removed.
   - Uploads the new zip artifacts.
   - Updates definitions of every procedure.
   - Updates definitions of every function.
