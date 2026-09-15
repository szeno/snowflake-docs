# Managing Snowflake stages

The `snow stage` commands let you perform additional stage-specific tasks:

- [Create a named stage if it does not already exist](#label-snowcli-stage-create).
- [Copy all files from source to target directory](#label-snowcli-stage-copy).
- [List the contents of a stage](#label-snowcli-stage-list).
- [Execute SQL files from a stage](#label-snowcli-stage-execute).
- [Remove a file from a stage](#label-snowcli-stage-remove).

## Create a named stage

The `snow stage create` command creates a named stage if it does not already exist.

Copy code

```
snow stage create <stage_name>
```

For example, to create a stage called `new_stage`, enter the following command:

Copy code

```
snow stage create new_stage
```

```
+-----------------------------------------------------+
| key    | value                                      |
|--------+--------------------------------------------|
| status | Stage area NEW_STAGE successfully created. |
+-----------------------------------------------------+
```

The following example shows what happens if you try to create a stage, `packages`, that already exists.

Copy code

```
# stage that already exists
snow stage create packages
```

```
+--------------------------------------------------------+
| key    | value                                         |
|--------+-----------------------------------------------|
| status | PACKAGES already exists, statement succeeded. |
+--------------------------------------------------------+
```

If you want to specify the type of encryption to use for all files stored on the stage, add the `--encryption` option to specify whether you want to full encryption (`SNOWFLAKE_FULL`) or only server-side encryption (`SNOWFLAKE_SSE`).

Copy code

```
snow stage create new_stage --encryption SNOWFLAKE_FULL
```

```
+-----------------------------------------------------+
| key    | value                                      |
|--------+--------------------------------------------|
| status | Stage area NEW_STAGE successfully created. |
+-----------------------------------------------------+
```

## Copy files to and from a stage

The `snow stage copy` command copies a file from the local machine to a stage, from a stage to a local machine, or between named stages.

Copy code

```
snow stage copy <source_path> <destination_path>
```

Note the following guidelines:

- The stage path must start with `@`, as shown in the following examples.
- When you copy a single file, `<destination_path>` must identify a directory, not a file. If the specified directory does not exist, the command creates it.
- By default, when you copy a local directory to a stage, the local directory must contain only files. You can use the `--recursive` option to upload sub-directories in the local directory. You can use glob patterns with the `--recursive` option.
- When you copy a directory from a stage to a local filesystem, the command currently flattens its internal tree structure. To illustrate, assume your local directory contains the following:

  ```
  test_case.py
  tests/abc.py
  tests/test1/x1.txt
  tests/test1/x2.txt
  ```

  After copying the directory from the stage, the local filesystem directory contains the following:

  ```
  test_case.py
  abc.py
  x1.txt
  x2.txt
  ```

  Note

  If you want to maintain the file structure from the source directory, you can include the `--recursive` option.

### Copy files to a stage

- To copy files from the local machine to a stage, enter a command similar to the following:

  Copy code

  ```
  snow stage copy local_example_app @example_app_stage/app
  ```

  ```
  put file:///.../local_example_app/* @example_app_stage/app4 auto_compress=false parallel=4 overwrite=False
  +--------------------------------------------------------------------------------------
  | source           | target           | source_size | target_size | source_compression...
  |------------------+------------------+-------------+-------------+--------------------
  | environment.yml  | environment.yml  | 62          | 0           | NONE             ...
  | snowflake.yml    | snowflake.yml    | 252         | 0           | NONE             ...
  | streamlit_app.py | streamlit_app.py | 109         | 0           | NONE             ...
  +--------------------------------------------------------------------------------------
  ```

You can use the `snow stage list-files` command to verify the command copied the files successfully:

Copy code

```
snow stage list-files example_app_stage
```

```
ls @example_app_stage
​+------------------------------------------------------------------------------------
| name                                   | size | md5                              | ...
|----------------------------------------+------+----------------------------------+-
| example_app_stage/app/environment.yml  | 64   | 45409c8da098125440bfb7ffbcd900f5 | ...
| example_app_stage/app/snowflake.yml    | 256  | a510b1d59fa04f451b679d43c703b6d4 | ...
| example_app_stage/app/streamlit_app.py | 112  | e6c2a89c5a164e34a0faf60b086bbdfc | ...
+------------------------------------------------------------------------------------
```

### Copy files from a stage

- To copy files from a stage to a directory on the local machine, enter a command similar to the following:

  Copy code

  ```
  mkdir local_app_backup
  snow stage copy @example_app_stage/app local_app_backup
  ```

  ```
  get @example_app_stage/app file:///.../local_app_backup/ parallel=4
  +------------------------------------------------+
  | file             | size | status     | message |
  |------------------+------+------------+---------|
  | environment.yml  | 62   | DOWNLOADED |         |
  | snowflake.yml    | 252  | DOWNLOADED |         |
  | streamlit_app.py | 109  | DOWNLOADED |         |
  +------------------------------------------------+
  ```

You can list the directory contents to verify the command copied the files correctly:

Copy code

```
ls local_app_backup
```

```
environment.yml  snowflake.yml    streamlit_app.py
```

Note that the local directory must exist.

You can copy from a user stage (`@~`):

> Copy code
>
> ```
> snow stage copy "@~" . --recursive
> ```
>
> ```
> +------------------------------------------------+
> | file             | size | status     | message |
> |------------------+------+------------+---------|
> | environment.yml  | 62   | DOWNLOADED |         |
> | snowflake.yml    | 252  | DOWNLOADED |         |
> | streamlit_app.py | 109  | DOWNLOADED |         |
> +------------------------------------------------+
> ```

### Copy files between stages

You can copy files directly between two named stages without downloading them to your local machine first. This can be useful for organizing files across different stages or creating backups.

- To copy files from one stage to another, use the following syntax:

  Copy code

  ```
  snow stage copy @source_stage @destination_stage
  ```

The following example copies all files from the `production_stage` to the `backup_stage`:

Copy code

```
snow stage copy @production_stage @backup_stage
```

```
+------------------------------------------------------------+
| file                                                       |
|------------------------------------------------------------|
| __init__.py                                                |
| main.py                                                    |
| procedure.py                                               |
+------------------------------------------------------------+
```

Note

When you copy between stages, the destination cannot be a user stage (`@~`). You must specify named stages for both source and destination.

### Use glob patterns to specify files

You can specify multiple files matching a regular expression by using a glob pattern for the `source_path` argument. You must enclose the glob pattern in single or double quotes.

The following example copies all `.txt` files in a directory to a stage.

Copy code

```
snow stage copy "testdir/*.txt" @TEST_STAGE_3
```

```
put file:///.../testdir/*.txt @TEST_STAGE_3 auto_compress=false parallel=4 overwrite=False
+------------------------------------------------------------------------------------------------------------+
| source | target | source_size | target_size | source_compression | target_compression | status   | message |
|--------+--------+-------------+-------------+--------------------+--------------------+----------+---------|
| b1.txt | b1.txt | 3           | 16          | NONE               | NONE               | UPLOADED |         |
| b2.txt | b2.txt | 3           | 16          | NONE               | NONE               | UPLOADED |         |
+------------------------------------------------------------------------------------------------------------+
```

## List the contents of a stage

The `snow stage list-files` command lists the stage contents.

Copy code

```
snow stage list-files <stage_path>
```

For example, to list the packages in a stage, enter the following command:

Copy code

```
snow stage list-files packages
```

```
ls @packages
+-------------------------------------------------------------------------------------
| name                 | size     | md5                              | last_modified
|----------------------+----------+----------------------------------+----------------
| packages/plp.Ada.zip | 824736   | 90639175a0ac7735e67525118b81047c | Tue, 16 Jan ...
| packages/samrand.zip | 13721024 | 648f0bae2f65fd4c9f178b17c23de7e5 | Tue, 16 Jan ...
+-------------------------------------------------------------------------------------
```

## Execute files from a stage

Note

Snowflake CLI does not support executing Python files for Python versions 3.12 and above.

The `snow stage execute` command executes SQL or Python files from a stage.

Copy code

```
snow stage execute <stage_path>
```

- For `.sql` files, the it performs an [EXECUTE IMMEDIATE FROM](/sql-reference/sql/execute-immediate-from) command on `.sql` files from a stage.
- For `.py` files, it executes a session-scoped [Snowpark Python procedure](/developer-guide/snowpark/python/creating-sprocs).

  Snowflake CLI executes the procedure in Snowflake to guarantee a consistent execution environment. If your Python scripts require additional requirements, you should specify them in a `requirements.txt` file that resides in the same directory as the files on the stage. The `snow stage execute` command only supports packages from the Snowflake Anaconda channel.

  By default, the command looks for the `requirements.txt` file in the following precedence:

  - Stage path specified in the command’s `stage_path` parameter.
  - Parent directories of the specified stage path hierarchy, until it reaches the stage.
  - If you don’t specify a `requirements.txt` file, the command assumes no additional packages are necessary.

  For example, if you run `snow stage execute @my_stage/ml/app1/scripts`, the command looks for the file as follows:

  - `my_stage/ml/app1/scripts/requirements.txt`
  - `my_stage/ml/app1/requirements.txt`
  - `my_stage/ml/requirements.txt`
  - `my_stage/ml/requirements.txt`

The following examples illustrate ways to execute different sets of `.sql` files from a stage:

- Specify only a stage name to execute all `.sql` files in the stage:

  Copy code

  ```
  snow stage execute "@scripts"
  ```

  ```
  SUCCESS - scripts/script1.sql
  SUCCESS - scripts/script2.sql
  SUCCESS - scripts/dir/script.sql
  +------------------------------------------+
  | File                   | Status  | Error |
  |------------------------+---------+-------|
  | scripts/script1.sql    | SUCCESS | None  |
  | scripts/script2.sql    | SUCCESS | None  |
  | scripts/dir/script.sql | SUCCESS | None  |
  +------------------------------------------+
  ```
- Specify a user stage (`@~`) to execute the `script.sql` files in the user stage:

  Copy code

  ```
  snow stage execute "@~/script1.sql"
  ```

  ```
  SUCCESS - scripts/script1.sql
  +------------------------------------------+
  | File                   | Status  | Error |
  |------------------------+---------+-------|
  | @~/script.sql          | SUCCESS | None  |
  +------------------------------------------+
  ```

### Use glob patterns to select subsets of files

- Specify a glob-like pattern to execute all `.sql` files in the `dir` directory:

  Copy code

  ```
  snow stage execute "@scripts/dir/*"
  ```

  ```
  SUCCESS - scripts/dir/script.sql
  +------------------------------------------+
  | File                   | Status  | Error |
  |------------------------+---------+-------|
  | scripts/dir/script.sql | SUCCESS | None  |
  +------------------------------------------+
  ```
- Specify a glob-like pattern to execute only `.sql` files in the `dir` directory that begin with “script”, followed by one character:

  Copy code

  ```
  snow stage execute "@scripts/script?.sql"
  ```

  ```
  SUCCESS - scripts/script1.sql
  SUCCESS - scripts/script2.sql
  +---------------------------------------+
  | File                | Status  | Error |
  |---------------------+---------+-------|
  | scripts/script1.sql | SUCCESS | None  |
  | scripts/script2.sql | SUCCESS | None  |
  +---------------------------------------+
  ```
- Specify a direct file path with the `--silent` option:

  Copy code

  ```
  snow stage execute "@scripts/script1.sql" --silent
  ```

  ```
  +---------------------------------------+
  | File                | Status  | Error |
  |---------------------+---------+-------|
  | scripts/script1.sql | SUCCESS | None  |
  +---------------------------------------+
  ```

## Remove a file from a stage

The `snow stage remove` command removes a file from a stage.

Copy code

```
snow stage remove <stage_name> <file_name>
```

For example, to remove a file from a stage, enter a command similar to the following:

Copy code

```
snow stage remove example_app_stage app/pages/my_page.py
```

```
+-------------------------------------------------+
| key    | value                                  |
|--------+----------------------------------------|
| name   | example_app_stage/app/pages/my_page.py |
| result | removed                                |
+-------------------------------------------------+
```
