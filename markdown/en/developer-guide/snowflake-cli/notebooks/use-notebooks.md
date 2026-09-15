# Using Snowflake Notebooks

Snowflake CLI includes the following `snow notebook` commands that let you create and execute [Snowflake notebooks](/user-guide/ui-snowsight/notebooks) from the command line:

- [snow notebook create](/developer-guide/snowflake-cli/command-reference/notebook-commands/create)
- [snow notebook deploy](/developer-guide/snowflake-cli/command-reference/notebook-commands/deploy)
- [snow notebook execute](/developer-guide/snowflake-cli/command-reference/notebook-commands/execute)
- [snow notebook get-url](/developer-guide/snowflake-cli/command-reference/notebook-commands/get-url)
- [snow notebook open](/developer-guide/snowflake-cli/command-reference/notebook-commands/open)
- [Snowflake notebooks](/user-guide/ui-snowsight/notebooks)

## Create a notebook

Note

Beginning with version 3.4.0, Snowflake CLI added the `snow notebook deploy` command to replace the `snow notebook create` command. To support backward compatibility, you can still create a notebook using the `snow notebook create` command, but Snowflake recommends that you begin using the new [Deploy and create a notebook](#label-cli-deploy-notebook) procedure.

The `snow notebook create` command creates a notebook from an existing notebook on stage. The command returns a link to the new
notebook. The following example creates the MY\_NOTEBOOK notebook from the specified staged notebook:

Copy code

```
snow notebook create MY_NOTEBOOK -f @MY_STAGE/path/to/notebook.ipynb
```

The command creates the notebook in the default warehouse defined for the connection. You can use the `--warehouse` option to specify an
alternative warehouse or to specify one if the connection doesn’t define a default warehouse.

## Deploy and create a notebook

The `snow notebook deploy` command uploads local files to a stage and creates a new Notebook object inside your chosen database and schema. Your project definition file should specify the main notebook file and query warehouse. The `--replace` option replaces the specified Notebook object if it already exists.

Each notebook in Snowflake must include a `snowflake.yml` project definition file.

The following example shows a sample `snowflake.yml` notebook project definition file:

Copy code

```
definition_version: 2
entities:
  my_notebook:
    type: notebook
    query_warehouse: xsmall
    notebook_file: notebook.ipynb
    runtime_environment_version: "WH-RUNTIME-2.0" # optional; omit to use the default warehouse runtime
    artifacts:
    - notebook.ipynb
    - data.csv
```

Valid warehouse runtime values are `WH-RUNTIME-1.0` (Python 3.9, the default) and `WH-RUNTIME-2.0` (Python 3.10). For more information, see [Create a notebook](/user-guide/ui-snowsight/notebooks-create).

The following table describes the properties of a notebook [project definition](/developer-guide/snowflake-cli/project-definitions/about):

**Notebook project definition properties**

| Property | Definition |
| --- | --- |
| **type**  *required*, *string* | Must be `notebook`. |
| **query\_warehouse**  *required*, *string* | Snowflake warehouse to host the notebook. |
| **notebook\_file**  *required*, *string* | Path to the notebook file. |
| **artifacts**  *required*, *string sequence* | List of files uploaded to the stage. Notebook file should be included in this list. |
| **stage\_path**  *optional*, *string* | Path to the stage where the artifacts will be stored. Default: `notebooks/<notebook_id>`. |
| **compute\_pool**  *optional*, *string* | Compute pool for a [containerized notebook](/developer-guide/snowflake-ml/notebooks-on-spcs) to use.  Note  Containerized notebooks are currently in PuPr. |
| **runtime\_name**  *optional*, *string* | Name of the Container Runtime for a [containerized notebook](/developer-guide/snowflake-ml/notebooks-on-spcs) to use. The following values are valid:   - `SYSTEM$BASIC_RUNTIME` for CPU runtime - `SYSTEM$GPU_RUNTIME` for GPU runtime   Note  Containerized notebooks are currently in PuPr. |
| **runtime\_environment\_version**  *optional*, *string* | Runtime environment version for a notebook entity in your project definition file. This field is optional; if omitted, the notebook uses the default warehouse runtime (`WH-RUNTIME-1.0`, Python 3.9). Allowed values are `WH-RUNTIME-1.0` and `WH-RUNTIME-2.0` (Python 3.10). For more information, see [Create a notebook](/user-guide/ui-snowsight/notebooks-create).  Notebook entity deployments will be rejected if both `compute_pool` and `runtime_environment_version` are specified in the configuration, leading to a validation failure.  Note  This field currently applies only to notebooks running on standard Snowflake warehouses, not those using compute pools (containerized notebooks). |
| **identifier**  *optional*, *string* | Optional Snowflake identifier for the entity. The value can have the following forms:   - String identifier text   Copy code  ``` identifier: my_notebook_id ```  Both unquoted and quoted identifiers are supported. To use quoted identifiers, include the surrounding quotes in the YAML value (e.g., `’”My Notebook”’`).   - Object   Copy code  ``` identifier:   name: my_notebook_id   schema: my_schema # optional   database: my_db # optional ```  Note  An error occurs if you specify a `schema` or `database` and use a fully qualified name in the `name` property (such as `mydb.schema1.my_notebook`). |

Expand

Show lessSee more

The following example uploads the files specified in your project definition file and creates a new notebook named `my_notebook`:

Copy code

```
snow notebook deploy my_notebook
```

```
Uploading artifacts to @notebooks/my_notebook
  Creating stage notebooks if not exists
  Uploading artifacts
Creating notebook my_notebook
Notebook successfully deployed and available under https://snowflake.com/provider-deduced-from-connection/#/notebooks/DB.SCHEMA.MY_NOTEBOOK
```

## Execute a notebook

The snow notebook execute command executes a notebook in headless mode. Currently, the command only returns a message indicating whether
the notebook executed successfully.

Copy code

```
snow notebook execute MY_NOTEBOOK
```

```
Notebook MY_NOTEBOOK executed.
```
