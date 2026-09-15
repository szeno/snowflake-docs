# snow init

Creates project directory from template.

## Syntax

Copy code

```
snow init
  <path>
  --template <template>
  --template-source <template_source>
  --variable <variables>
  --no-interactive
  --format <format>
  --verbose
  --debug
  --silent
  --enhanced-exit-codes
  --decimal-precision <decimal_precision>
```

## Arguments

`path`
:   Directory to be initialized with the project. This directory must not already exist.

## Options

`--template TEXT`
:   which template (subdirectory of –template-source) should be used. If not provided, whole source will be used as the template.

`--template-source TEXT`
:   local path to template directory or URL to git repository with templates. Default: <https://github.com/snowflakedb/snowflake-cli-templates>.

`--variable, -D TEXT`
:   String in *key=value* format. Provided variables will not be prompted for.

`--no-interactive`
:   Disable prompting. Default: False.

`--format [TABLE%JSON%JSON_EXT|CSV]`
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

The `snow init` command initializes a directory specified in the `<path>` parameter with a chosen template. It renders all files mentioned in the `files_to_render` list in the `template.yml`, resolving all variables enclosed in `<! … !>`. If a `template.yml` file is not present in the template’s root directory, the command finishes with an error. For information about creating project templates, see [Bootstrapping a project from a template](/developer-guide/snowflake-cli/bootstrap-project/bootstrap).

By default, the command interactively prompts you for each parameter defined in the `template.yml` file. You can bypass the interactive prompts in the following ways:

- Use the `-D` option to specify the values for each parameter contained in the project template.
- Use the `--no-interactive` option to use default values, if defined, for each template parameter in the `template.yml` file.
- Use a combination of the `-D` and `--no-interactive` options to define values for some parameters and use the specified default values for the template.

  Note

  If you do not provide a value using the `-D` option that does not have a corresponding default value defined, the snow init command terminates with an error.

## Examples

- Bootstrap a Snowpark project that prompts for the parameters specified in the `example_snowpark` template contained in the [snowflake-cli-templates Git repository](https://github.com/snowflakedb/snowflake-cli-templates/).

  Copy code

  ```
  snow init new_snowpark_project --template example_snowpark

    Project identifier (used to determine artifacts stage path) [my_snowpark_project]:
    What stage should the procedures and functions be deployed to? [dev_deployment]: snowpark
  ```

  ```
  Initialized the new project in new_snowpark_project
  ```
- Bootstrap a Streamlit project by using the `-D` option to provide the values for some of the parameters specified in the local `../local_templates/example_streamlit` template and prompt for others.

  Copy code

  ```
  snow init new_streamlit_project --template-source ../local_templates/example_streamlit -D query_warehouse=dev_wareshouse -D stage=testing

    Name of the streamlit app [streamlit_app]: My streamlit
  ```

  ```
  Initialized the new project in new_streamlit_project
  ```
