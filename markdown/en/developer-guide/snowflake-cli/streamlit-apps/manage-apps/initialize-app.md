# Creating a Streamlit app

## Prerequisites

Before creating a Streamlit app with Snowflake CLI, you should meet the following prerequisites:

- Ensure that your account has the correct privileges as described in [Privileges required to create and use a Streamlit app](/developer-guide/streamlit/object-management/privileges).
- Ensure that you can create or have access to a named stage where you can upload your Streamlit app files.

## Bootstrap a Streamlit app

The `snow init` command creates a local directory with a sample set of files that help you get started creating a Streamlit app. When you execute this command, Snowflake CLI creates the following directory structure:

```
example_streamlit/            - project name (default: example_streamlit)
  snowflake.yml               - configuration for snow streamlit commands
  environment.yml             - additional config for Streamlit, for example installing packages
  streamlit_app.py            - entrypoint file of the app
  pages/                      - directory name for Streamlit pages (default pages)
  common/                     - example “shared library”
```

To initialize a Streamlit app, enter the following command:

Copy code

```
snow init new_streamlit_project --template example_streamlit -D query_warehouse=dev_warehouse -D stage=testing
```

Caution

Files inside a project directory are processed by Snowflake CLI and could be uploaded to Snowflake when executing other `snow streamlit` commands. You should use caution when putting any sensitive information inside files in a project directory.

For more information about the file structure, see [Organize your Streamlit app files](/developer-guide/streamlit/app-development/file-organization).

## Create the project definition for a Streamlit app

Each Streamlit app in Snowflake must include a `snowflake.yml` project definition file. Streamlit is limited to one application per project definition file.

The following shows a sample `snowflake.yml` project definition file:

Copy code

```
definition_version: 2
entities:
  my_streamlit:
    type: streamlit
    identifier: streamlit_app
    stage: my_streamlit_stage
    query_warehouse: my_streamlit_warehouse
    main_file: streamlit_app.py
    pages_dir: pages/
    external_access_integrations:
      - test_egress
    secrets:
      dummy_secret: "db.schema.dummy_secret"
    imports:
      - "@my_stage/foo.py"
    artifacts:
      - common/hello.py
      - environment.yml
    grants:
      - privilege: USAGE
        role: streamlit_role
```

The following table describes the properties of a Streamlit project definition.

**Streamlit project definition properties**

| Property | Definition |
| --- | --- |
| **identifier**  *optional*, *string* | Optional Snowflake identifier for the entity. The value can have the following forms:   - String identifier text   Copy code  ``` identifier: my-streamlit-id ```  Both unquoted and quoted identifiers are supported. To use quoted identifiers, include the surrounding quotes in the YAML value (e.g. `’”My Streamlit Application”’`).   - Object   Copy code  ``` identifier:   name: my-streamlit-id   schema: my-schema # optional   database: my-db # optional ```  Note  An error occurs if you specify a `schema` or `database` and use a fully-qualified name in the `name` property (such as `mydb.schema1.my-app`). |
| **type**  *optional*, *string* | Must be `streamlit`. |
| **comment**  *optional*, *string* | Comment for the Streamlit dashboard. |
| **title**  *optional*, *string* | Human-readable title for the Streamlit dashboard. |
| **tags**  *optional*, *object sequence* | Tags to apply to the Streamlit app when you deploy it with `snow streamlit deploy`. Each entry has a `name` (a valid Snowflake identifier) and a `value`. Default: None. |
| **stage**  *optional*, *string* | Stage in which the app’s artifacts will be stored. Default: None. |
| **query\_warehouse**  *required*, *string* | Snowflake warehouse to host the app. |
| **main\_file**  *optional*, *string* | [Entrypoint file](https://docs.streamlit.io/get-started/tutorials/create-an-app) of the streamlit app. Default: “streamlit\_app.py”. |
| **pages\_dir**  *optional*, *string* | Streamlit [pages](https://docs.streamlit.io/get-started/tutorials/create-a-multipage-app). Default: “pages”. |
| **external\_access\_integrations**  *optional*, *string sequence* | Names of [external access integrations](/sql-reference/sql/create-external-access-integration) needed for this Streamlit application code to access external networks. See [the optional parameters for CREATE STREAMLIT](/sql-reference/sql/create-streamlit#label-create-streamlit-optional-parameters) for more details. |
| **secrets**  *optional*, *dictionary* | Assigns the names of secrets to variables so that you can use the variables to reference the secrets when retrieving information from secrets in application code. |
| **imports**  *optional*, *string sequence* | Stage and path to previously uploaded files you want to import. See [the optional parameters for CREATE STREAMLIT](/sql-reference/sql/create-streamlit#label-create-streamlit-optional-parameters) for more details. |
| **artifacts**  *required*, *string sequence* | List of file source and destination pairs to add to the deploy root. You can use the following artifact properties:   - `src`: Path to the code source file or files. - `dest`: Path to the directory to deploy the artifacts.   Destination paths that reference directories must end with a `/`. A glob pattern’s destination that does not end with a `/` results in an error. If omitted, `dest` defaults to the same string as `src`.  You can also pass in a string for each item instead of a `dict`, in which case the value is treated as both `src` and `dest`.  If `src` refers to just one file (not a glob), `dest` can refer to a target `<path>` or a `<path/name>`.  You can also pass in a string for each item instead of a `dict`; in that case, the value is treated as both `src` and `dest`. |
| **grants**  *optional*, *grant sequence* | Grants that should be given for the Streamlit app. Each grant must specify the privilege and exactly one of `role:` or `user:`. You can also set `with_grant_option: true` so the grantee can share the app onward. A `sharing:` list is the older spelling of USAGE grants and is treated the same as `grants:` entries whose privilege is USAGE. For more details, see [the optional parameters for CREATE STREAMLIT](/sql-reference/sql/create-streamlit#label-create-streamlit-optional-parameters). |

Expand

Show lessSee more
