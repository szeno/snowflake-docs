# Staging data files from a local file system

Execute [PUT](/sql-reference/sql/put) using the [Snowflake CLI](/developer-guide/snowflake-cli/index) client, the [SnowSQL client](/user-guide/snowsql), or [Drivers](/developer-guide/drivers) to upload (stage) local data files into an internal stage.

If you want to load a few small local data files into a named internal stage, you can also use Snowsight.
Refer to [Staging files using Snowsight](/user-guide/data-load-local-file-system-stage-ui).

## Staging the data files

User Stage
:   The following example uploads a file named `data.csv` in the `/data` directory on your local machine to
    your user stage and prefixes the file with a folder named `staged`.

    Note that the `@~` character combination identifies a user stage.

    - Linux or macOS

      Copy code

      ```
      PUT file:///data/data.csv @~/staged;
      ```
    - Windows

      Copy code

      ```
      PUT file://C:\data\data.csv @~/staged;
      ```

Table Stage
:   The following example uploads a file named `data.csv` in the `/data` directory on your local machine to
    the stage for a table named `mytable`.

    Note that the `@%` character combination identifies a table stage.

    - Linux or macOS

      Copy code

      ```
      PUT file:///data/data.csv @%mytable;
      ```
    - Windows

      Copy code

      ```
      PUT file://C:\data\data.csv @%mytable;
      ```

Named Stage
:   The following example uploads a file named `data.csv` in the `/data` directory on your local machine to a
    named internal stage called `my_stage`. See [Choosing an internal stage for local files](/user-guide/data-load-local-file-system-create-stage) for information on named stages.

    In SQL, note that the `@` character by itself identifies a named stage.

    - Linux or macOS

      SQLPython

      Copy code

      ```
      PUT file:///data/data.csv @my_stage;
      ```

      Copy code

      ```
      my_stage_res = root.databases["<database>"].schemas["<schema>"].stages["my_stage"]
      my_stage_res.put("/data/data.csv", "/")
      ```
    - Windows

      SQLPython

      Copy code

      ```
      PUT file://C:\data\data.csv @my_stage;
      ```

      Copy code

      ```
      my_stage_res = root.databases["<database>"].schemas["<schema>"].stages["my_stage"]
      my_stage_res.put("C:/data/data.csv", "/")
      ```

## Listing staged data files

To see files that have been uploaded to a Snowflake stage, use the [LIST](/sql-reference/sql/list) command:

User stage:

Copy code

```
LIST @~;
```

Table stage:

Copy code

```
LIST @%mytable;
```

Named stage:

SQLPython

Copy code

```
LIST @my_stage;
```

Copy code

```
stage_files = root.databases["<database>"].schemas["<schema>"].stages["my_stage"].list_files()
for stage_file in stage_files:
  print(stage_file)
```

**Next:** [Copy data from an internal stage](/user-guide/data-load-local-file-system-copy)
