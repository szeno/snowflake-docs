# About project definition files

When developing Streamlit or Snowpark applications you often work with multiple files and objects, be it python file or stored procedures. Organizing this in a clear and concise way is very important for smooth development experience. That’s the reason why Snowflake CLI is using the concept of *project definition files*.

A project definition file (usually named `snowflake.yml`) is a file containing information about the Snowflake objects you are developing. The following `snowflake.yml` example shows a project with a Snowpark UDF and a stored procedure.

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
```

## Project definition properties

The following table describes the project definition properties used by all projects.

**Common project definition properties**

| Property | Definition |
| --- | --- |
| **definition\_version**  *required*, *int* | Version of the project definition schema, which is currently 2. |
| **entities**  *optional*, *string* | List of entity definitions, such as procedures, functions, and so on. For more information, see [Specify entities](/developer-guide/snowflake-cli/project-definitions/specify-entities). |
| **env**  *optional*, *string sequence* | List of default environment specifications to be used in project templates. For more information, see [Create project definition file templates](/developer-guide/snowflake-cli/project-definitions/create-templates). |
| **mixins**  *optional*, *string sequence* | List of common values for entity properties. For more information, see [Project mixins](/developer-guide/snowflake-cli/project-definitions/specify-entities#label-cli-project-mixins). |

Expand

Show lessSee more

Each project requires specific information about what you are building. Snowflake CLI currently supports the following entity definitions from the following Snowflake domains:

- [Native App Framework](/developer-guide/snowflake-cli/native-apps/project-definitions)
- [Notebooks](/developer-guide/snowflake-cli/notebooks/use-notebooks)
- [Snowpark](/developer-guide/snowflake-cli/snowpark/create#label-snowcli-create-snowpark)
- Snowpark Container Services (SPCS)

  - [Compute pools](/developer-guide/snowflake-cli/services/manage-compute-pools#label-sfcli-pool-pdf)
  - [Image repositories](/developer-guide/snowflake-cli/services/manage-images#label-sfcli-repo-pdf)
  - [Services](/developer-guide/snowflake-cli/services/manage-services#label-sfcli-service-pdf)
- [Streamlit](/developer-guide/snowflake-cli/streamlit-apps/manage-apps/initialize-app#label-snowcli-streamlit-project-definition)
- [SQL](/developer-guide/snowflake-cli/sql/execute-sql#label-cli-sql-env-vars)

Caution

Files inside a project directory are processed by Snowflake CLI and could be uploaded to Snowflake when executing other `snow` commands. You should use caution when putting any sensitive information inside files in a project directory.
