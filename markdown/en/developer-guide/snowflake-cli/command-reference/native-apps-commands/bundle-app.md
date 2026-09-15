# snow app bundle

Prepares a local folder with configured app artifacts.

## Syntax

Copy code

```
snow app bundle
  --package-entity-id <package_entity_id>
  --app-entity-id <app_entity_id>
  --project <project_definition>
  --env <env_overrides>
  --format <format>
  --verbose
  --debug
  --silent
  --enhanced-exit-codes
  --decimal-precision <decimal_precision>
```

## Arguments

None

## Options

`--package-entity-id TEXT`
:   The ID of the package entity on which to operate when the definition\_version is 2 or higher.

`--app-entity-id TEXT`
:   The ID of the application entity on which to operate when the definition\_version is 2 or higher.

`-p, --project TEXT`
:   Path where the Snowflake project is stored. Defaults to the current working directory.

`--env TEXT`
:   String in the format key=value. Overrides variables from the env section used for templates. Default: [].

`--format [TABLE|JSON|JSON_EXT|CSV]`
:   Specifies the output format. Default: TABLE.

`--verbose, -v`
:   Displays log entries for log levels *info* and higher. Default: False.

`--debug`
:   Displays log entries for log levels *debug* and higher; debug logs contain additional information. Default: False.

`--silent`
:   Turns off intermediate output to console. Default: False.

`--enhanced-exit-codes`
:   Differentiate exit error codes based on failure type. Default: False.

`--decimal-precision INTEGER`
:   Number of decimal places to display for decimal values. Uses Python’s default precision if not specified. [env var: SNOWFLAKE\_DECIMAL\_PRECISION].

`--help`
:   Displays the help text for this command.

## Usage notes

The `snow app bundle` command creates a temporary local directory that contains all of the Snowflake Native App artifacts. It can also automatically generate SQL scripts from your Snowpark Python code. This command is called automatically by the [snow app deploy](/developer-guide/snowflake-cli/command-reference/native-apps-commands/deploy-app), [snow app run](/developer-guide/snowflake-cli/command-reference/native-apps-commands/run-app), and [snow app version create](/developer-guide/snowflake-cli/command-reference/native-apps-commands/version/app-version-create) commands. If, however, you want to see the setup script, artifacts, and generated SQL, before uploading them to a stage, you can run this command manually. For more information about generating SQL code, see [Preparing a local folder with configured Snowflake Native App artifacts](/developer-guide/snowflake-cli/native-apps/bundle-app).

- The command uses the [project definition file](/developer-guide/snowflake-cli/native-apps/project-definitions) to determine the name of the temporary folder to create within your project directory.

  - By default, it will be `<project_directory>/output/deploy`. This directory, which is also known as the deploy root, mirrors the structure the stage will have once files are uploaded to stage in subsequent commands.
  - If you want Snowflake CLI to create a folder with a custom name instead of `output/deploy`, you can do so by providing the `deploy_root` field on the *application package* entity in the [project definition file](/developer-guide/snowflake-cli/native-apps/project-definitions).

    Note

    You must provide a relative path for the deploy root; absolute paths are rejected. The deploy root path is created inside the project directory.
  - The deploy root is a temporary directory because it gets deleted and recreated every time you run `snow app bundle` or another command invokes the `bundle` functionality.
- Because `snow app bundle` is automatically called as part of the [snow app deploy](/developer-guide/snowflake-cli/command-reference/native-apps-commands/deploy-app), [snow app run](/developer-guide/snowflake-cli/command-reference/native-apps-commands/run-app), and [snow app version create](/developer-guide/snowflake-cli/command-reference/native-apps-commands/version/app-version-create) commands, you should make changes to the source files only, outside the deploy root. If you modify files in the deploy root, the files are overwritten by the most recent state of your source files the next time you call one of these commands.
- If using a version control system such as `git`, you can choose not to track the deploy root, as it can change frequently.
- `snow app bundle` does not build or compile your artifacts for you, such as creating jar files from your Java files. It only copies the artifacts specified in the project definition file and adds them to the deploy root to mimic the stage’s directory structure.
- `snow app bundle` does not need access to your Snowflake account; it only affects your local filesystem.
- The command has the following copying and symlinking behavior for any `artifacts` of the *application package* entity in the [project definition file](/developer-guide/snowflake-cli/native-apps/project-definitions):

  - All directory names in a source path are also created in the deploy root.
  - All files in a source path are symlinked within these directories in the deploy root.
  - Some symlinked files in the deploy root can become hard links if you invoke SQL generation from those files. For more information, see [Preparing a local folder with configured Snowflake Native App artifacts](/developer-guide/snowflake-cli/native-apps/bundle-app).

  Consider the following `artifacts` list example from a project definition file:

  Copy code

  ```
  entities:
    pkg:
   type: application package
   ...
   artifacts:
     - src: dir1/dir2/*
       dest: dest_dir1/dest_dir2/
     - src: dir8/dir9/file.txt
       dest: dest_dir8/dest_file.txt
    ...
  ```

  where `dir1/dir2` in the project root could have other subdirectories, such as `dir3` and `dir4`, and some files, such as `file3.txt` and `file4.txt`.

  After running the `snow app bundle` command, your deploy root should look like the following:

  Copy code

  ```
  -- deploy_root
     -- dest_dir1
           -- dest_dir2
                 -- dir3
                     -- ... <entire directory tree of dir3>
                 -- dir4
                     -- ... <entire directory tree of dir4>
                 -- file3.txt
                 -- file4.txt
     -- dest_dir8
           -- dest_file.txt
  ```

### Snowpark annotation processing

Beginning with Snowflake CLI version 2.5.0 and [Snowpark Python API](/developer-guide/snowpark/python/index) version 1.15.0, you can leverage the Snowpark annotation processing feature with the `snow app bundle` command. This feature lets you annotate your Python code files with Snowpark Python decorators, such as `@udf`, `@sproc`, `@udaf`, and `@udtf` to let Snowflake CLI automatically generate the corresponding CREATE FUNCTION or CREATE PROCEDURE SQL statements in setup script files in the project directory. For a better understanding of these decorators, refer to the corresponding Python decorators documentation.

Snowpark annotation processing involves the following:

- It reads all Python files you marked with a `processor` field in the project definition file.
- It creates a separate temporary sandbox Python environment using the environment information provided in the processor’s `properties` sub-field.
- It executes those Python files in the sandboxed environment.
- It collects all decorated functions from those files.

Caution

The Snowpark processor executes Python files from your project directory, including subdirectories. Only use `snow app bundle`, `snow app deploy`, and `snow app diff` with projects and Python files you trust.

- With the collected information, Snowflake CLI generates the necessary SQL statements and adds them to the setup script whose location is specified in your `manifest.yaml` file.

You no longer need to repeat boilerplate SQL code for writing Snowpark extension functions for your Snowflake Native App apps.

For more information about enabling this feature in your project definition files, see [Using the Snowpark Python decorators](/developer-guide/snowflake-cli/native-apps/bundle-app#label-cli-sf-annotation-processing).

For more information about all supported artifact processors, see [More information about artifacts processors](/developer-guide/snowflake-cli/native-apps/project-definitions#label-cli-na-artifacts-processors).

## Examples

This example assumes you have made the necessary changes to your code files and added them to your `snowflake.yml` or `snowflake.local.yml` files, and also built or compiled any relevant artifacts.

Copy code

```
cd my_app_project
snow app bundle
```

The command displays information about the various steps that occur while the command runs and creates a new directory at the location specified in your project definition file (default: `my_app_project/output/deploy`).

To see a simple use case in action, you can leverage the ready-to-use templates using the following commands:

Copy code

```
snow init my_app_bundle_project --template app_basic
cd "my_app_bundle_project"
snow app bundle
ls my_app_bundle_project/output/deploy
```
