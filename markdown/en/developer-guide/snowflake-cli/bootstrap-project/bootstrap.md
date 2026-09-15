# Bootstrapping a project from a template

To make it easier for you to instantiate projects, Snowflake CLI implements project templating. You can
[create your own project templates](#label-cli-project-templating-custom-templates) or use samples provided by Snowflake in the [Snowflake CLI templates](https://github.com/snowflakedb/snowflake-cli-templates/) public Git repository.

The [snow init](/developer-guide/snowflake-cli/command-reference/bootstrap-commands/init) command creates a project directory and populates it with file structure defined in the specified template.

- If you don’t provide the `--no-interactive` option, the command prompts for each variable specified by the template (`template.yml`) that you don’t provide with the `-D` (or `--variable`) option.
- If you do provide the `--no-interactive` option, the command uses the default values of variables (defined by the template). If the template does not define a default value for a variable and you don’t use the `-D` option to provide it, the command exits with an error.

The `snow init` command uses the following syntax:

Copy code

```
snow init PATH [--template-source SOURCE] [--template NAME] [-D key1=value1 -D key2=value2...] [--no-interactive]
```

where:

- `PATH` is a new directory where the command initializes the project. If you specify an existing directory, the command exits with an error.
- `[--template-source SOURCE]` is one of the following:

  - A local file path of the template directory.
  - A valid Git URL to the directory containing the project template. If not specified, the command defaults to the [Snowflake CLI templates](https://github.com/snowflakedb/snowflake-cli-templates/) Git repository.
- `[--template NAME]` specifies which subdirectory of `SOURCE` to use as a template (useful for remote sources). If not provided, `SOURCE` is treated as a single template.
- `[-D key1=value1 -D key2=value2...]` is a list of one or more name-value pairs, providing values for variables defined in the template (in `template.yml`). The command does not prompt for variables you provide with this option.
- `[--no-interactive]` disables prompts for user input. If you use this option, you must provide all of the required values with the `[-D key1=value1 -D key2=value2...]` options; otherwise, the command exists with an error.

For more information, see the [snow init](/developer-guide/snowflake-cli/command-reference/bootstrap-commands/init) command reference.

## Examples

- Initialize project from `example_snowpark` template from default repository:

  Copy code

  ```
  snow init my_snowpark_test_app --template example_snowpark
  ```

  The command prompts for (default values are shown in square brackets):

  ```
  Project identifier (used to determine artifacts stage path) [my_snowpark_project]:
  What stage should the procedures and functions be deployed to? [dev_deployment]: snowpark
  Initialized the new project in my_snowpark_test_app
  ```
- Initialize the project from the local template.

  Copy code

  ```
  snow init new_streamlit_project --template-source ../local_templates/example_streamlit -D query_warehouse=dev_wareshouse -D stage=testing
  ```

  In this example, `query_warehouse` and `stage` variables are specified with the `-D` option, so the command only prompts for the following:

  ```
  Name of the streamlit app [streamlit_app]:
  Initialized the new project in new_streamlit_project
  ```

## Creating custom templates

### Template layout

A project template requires a `template.yml` file that contains data that explains how the `snow init` command should render the template. If the file is not present in the template’s root directory, `snow init` finishes with an error.
For more information, see [template.yml syntax.](#label-cli-project-templating-template-yml)

### Template syntax

Template variables and expressions should be enclosed in `<! ... !>`.
Snowflake CLI also supports basic jinja2 expressions and filters, for example:

> Copy code
>
> ```
> some_file_spec:
>   filename: <! file_name !>
>   size: "<! [ max_file_size_mb, 4 ] | max !> MB"
> ```

Snowflake CLI project templates also support the following reserved variable and filter:

- `project_dir_name` variable, which automatically resolves to the root directory of the created project.

  For example, suppose your `snowflake.yml` file contains the following:

  Copy code

  ```
  definition_version: "1.1"
  snowpark:
    project_name: <! project_dir_name !>
    ...
  ```

  If you then execute the following command to initialize the project from your custom template:

  Copy code

  ```
  snow init examples/new_snowpark_project --template-source my_example_template/
  ```

  The `snow init` command renders the `snowflake.yml` file as follows:

  Copy code

  ```
  definition_version: "1.1"
  snowpark:
    project_name: new_snowpark_project
    ...
  ```
- `to_snowflake_identifier` filter, which formats user-provided strings into to correctly-formatted Snowflake identifiers.

  Snowflake strongly recommends using this filter when a variable references a Snowflake object.

  For example, suppose your `snowflake.yml` file contains the following:

  Copy code

  ```
  definition_version: "1.1"
  streamlit:
    name: <! name | to_snowflake_identifier !>
    ...
  ```

  If you then execute the following command to initialize a project from your custom template:

  Copy code

  ```
  snow init examples/streamlit --template-source my_example_template2/ -D name='My test streamlit'
  ```

  The `snow init` command renders the `snowflake.yml` file as follows:

  Copy code

  ```
  definition_version: "1.1"
  streamlit:
    name: My_test_streamlit
    ...
  ```

  If a string cannot be converted into a valid Snowflake identifier, the `snow init` command exits with an error, as shown:

  Copy code

  ```
  snow init examples/streamlit --template-source my_example_template2/ -D name=1234567890
  ```

  ```
  ╭─ Error ────────────────────────────────────────────────────────────────────────╮
  │ Value '123456789' cannot be converted to valid Snowflake identifier.         │
  │ Consider enclosing it in double quotes: ""                                   │
  ╰────────────────────────────────────────────────────────────────────────────────╯
  ```

### About the `template.yml` project template file

The `template.yml` project template file stores all of the data needed to render the project. For example:

Copy code

```
minimum_cli_version: "2.7.0"
files_to_render:
  - snowflake.yml
variables:
  - name: name
    default: streamlit_app
    prompt: "Name of the streamlit app"
    type: string
  - name: stage
    default: my_streamlit_stage
    prompt: "What stage should the app be deployed to?"
    type: string
  - name: query_warehouse
    default: my_streamlit_warehouse
    prompt: "On which warehouse SQL queries issued by the application are run"
    type: string
```

The following table lists the properties in a `template.yml` project template file.

**Template properties**

| Property | Definition |
| --- | --- |
| `minimum_cli_version`  *optional*, *string* (default:None) | Minimum Snowflake CLI version. If specified, the `snow init` command checks the version of Snowflake CLI installed and exits with an error if the installed version is lower than the specified version. |
| `files_to_render`  *optional*, *string list* (default: `[]`) | List of files to be rendered by the `snow init` command. Each path should be relative to the templates root.  Note  Template files not included in this list are added to the new project, but their content remains unchanged. |
| `variables`  *optional*, *variable list* (default: `[]`) | List of template variables. It supports customizing prompts, providing default values for optional variables and basic type checking. See the **Variables property parameters** table below for more details. Variable values are determined in order from this list.  If you omit any variable used in the `snowflake.yml` file from this list, the `snow init` command exits with the following error.  ``` ╭─ Error ─────────────────────────────────────────────────────────╮ │ Cannot determine value of variable undefined_variable         │ ╰─────────────────────────────────────────────────────────────────╯ ``` |

Expand

Show lessSee more

The following table lists the parameters of a variable property.

**Variable property parameters**

| Property | Definition |
| --- | --- |
| `name`  *required*, *string* | Name of the variable. It is used in the template files, such as `<! name !>` and in `-D` option, such as `-D name=value`. |
| `prompt`  *optional*, *string* | Prompt to display to the user to get a value. If you don’t set this parameter, the command displays the name of the parameter as the prompt text.  If you define the prompt as follows:  Copy code  ``` variables:   - name: project_id     prompt: The identifier for the project ```  `snow init` displays this prompt for the `project_id` variable.  ``` The identifier for the project: ``` |
| `default`  *optional*, *string/int/float* | Default value of the variable. If not provided, the variable is treated as required, so a user needs to provide the value after a prompt or by specifying it with the `-D` command-line option.  The following example defines two variables with default values:  Copy code  ``` variables:   - name: max_file_size_mb     default: 16   - name: file_name     default: 'default_file_name.zip' ```  When executed, the `snow init` command displays the following prompts for these two variables:  Copy code  ``` file_name [default_file_name.zip]: max_file_size_mb [16]: 5 ```  In this example, the command uses the default value (`default_file_name.zip`) for the `file_name` variable has a default value, and sets `max_file_size_mb` to the value provided by the user (5). |
| `type`  *optional*, *string* | Data type of the variable. Valid values include: `string`, `int`, and `float`. If not specified, the command assumes the value is a `string`.  The following example defines a variable as an `int` data type:  Copy code  ``` variables:   - name: max_file_size_mb     type: int ```  When executed, the snow init command displays the following errors if the user enters a value of the wrong data type:  ``` max_file_size_mb: not an int Error: 'not an int' is not a valid integer. max_file_size_mb: 14.5 Error: '14.5' is not a valid integer. max_file_size_mb: 6 Initialized the new project in example_dir ``` |

Expand

Show lessSee more
