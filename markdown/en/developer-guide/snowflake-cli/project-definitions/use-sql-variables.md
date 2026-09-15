# Use variables in SQL

Note

Support for variables requires project definition version 1.1.

You can also use project files to define variables that other commands, such as `snow sql`, can use. The `env` section in the project definition file(typically, `snowflake.yml`) lets you define variables as shown:

Copy code

```
definition_version: 2
env:
  database: "dev"
  role: "eng_rl"
```

After adding the `env` section to the project definition file, you can pass the variables to the `snow sql` command instead of specifying the variable and value on the command line.

Instead specifying the database and role on the command line with the `--variable` option, as shown:

Copy code

```
snow sql \
-q "grant usage on database <% database %> to <% role %>" \
-D "database=dev" \
-D "role=eng_rl"
```

you can specify the variables defined in the `env` section as shown:

Copy code

```
snow sql -q "grant usage on database <% ctx.env.database %> to <% ctx.env.role %>"
```

You can include the `env` section in addition to any other sections you include in the project definition file.

Copy code

```
definition_version: 2
entities:
  test_function:
    type: "function"
    stage: "dev_deployment"
    artifacts: ["app/"]
    handler: "functions.hello_function"
    signature: ""
    returns: string

  hello_procedure:
    type: "procedure"
    stage: "dev_deployment"
    artifacts: ["app/"]
    handler: "procedures.hello_procedure"
    signature:
      - name: "name"
        type: "string"
    returns: string

env:
  database: "dev"
  role: "eng_rl"
```

Note

If your current project definition file uses `definition_version: 1`, you must update it to `definition_version: 1.1` if you want to take advantage of the variables feature. If you do not change the value, Snowflake CLI ignores the `env` section, but the other types of projects (`snowpark`, in this example) still work as expected.

You can override any variable defined the in `snowflake.yml` project definition file by setting a shell environment variable by the same name (case-sensitive). For example, to override the `database` value defined in the example, you can execute the following shell command:

Copy code

```
export database="other"
```

For more information about using `env` variables, see [Storing variables in the `snowflake.yml` project definition file](/developer-guide/snowflake-cli/sql/execute-sql#label-cli-sql-env-vars).
