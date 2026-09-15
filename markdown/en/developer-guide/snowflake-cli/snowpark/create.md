# Create a Snowpark project definition

The `snowflake.yml` file contains the functions and procedures declarations for a Snowpark project.

Note

Currently, the Snowpark project definition file must be named `snowflake.yml`.

The following snippet shows a sample Snowpark project definition file: with two functions and two procedures. The `hello_function` function uses external capabilities of Snowpark.

Copy code

```
definition_version: '2'

mixins:
  snowpark_shared:
    artifacts:
      - dest: my_snowpark_project
        src: app/
    stage: dev_deployment

entities:

  hello_function:
    type: function
    identifier:
      name: hello_function
    handler: functions.hello_function
    signature:
      - name: name
        type: string
    returns: string
    external_access_integrations:
      - my_external_access
    secrets:
        cred: my_cred_name
    meta:
      use_mixins:
        - snowpark_shared

  hello_procedure:
    type: procedure
    identifier:
      name: hello_procedure
    handler: procedures.hello_procedure
    signature:
      - name: name
        type: string
    returns: string
    meta:
      use_mixins:
        - snowpark_shared

  test_procedure:
    type: procedure
    identifier:
      name: test_procedure
    handler: procedures.test_procedure
    signature: ''
    returns: string
    meta:
      use_mixins:
        - snowpark_shared
```

Caution

Files inside a project directory are processed by Snowflake CLI and could be uploaded to Snowflake when executing other `snow snowpark` commands. You should use caution when putting any sensitive information inside files in a project directory.

Note

**Specifying Python dependencies in `definition_version: 2`**

Python dependencies are declared in two places, depending on where the package comes from:

- **Anaconda-channel packages** (such as `snowflake-snowpark-python`, `pandas`, or `numpy`) must be listed in a `requirements.txt` file in the project root. This file is automatically picked up by `snow snowpark deploy`.
- **PyPI packages** can go in that same `requirements.txt` file (Snowflake CLI packages them into a zip) or under the entity `packages:` field, which **requires the `artifact_repository:` field to also be set** (typically to `snowflake.snowpark.pypi_shared_repository`). Specifying `packages:` without `artifact_repository:` returns the error: *“You specified packages / artifact\_repository\_packages without setting artifact\_repository.”*

The `packages:` field is new in `definition_version: 2` and is only for artifact-repository packages. v1 projects declare dependencies in `requirements.txt` only. If you are migrating an existing v1 project, see [snow helpers v1-to-v2](/developer-guide/snowflake-cli/command-reference/helpers-commands/v1-to-v2).

## Function and procedure object properties

The following table describes the properties used by functions and procedures.

**Function and procedure object properties**

| Property | Definition |
| --- | --- |
| **identifier**  *optional*, *string* | Optional Snowflake identifier for the entity. The value can have the following forms:   - String identifier text   Copy code  ``` identifier: my-snowpark-id ```  Both unquoted and quoted identifiers are supported. To use quoted identifiers, include the surrounding quotes in the YAML value (e.g. `’”My Snowpark Function”’`).   - Object   Copy code  ``` identifier:   name: my-snowpark-id   schema: my-schema # optional   database: my-db # optional ```  Note  An error occurs if you specify a `schema` or `database` and use a fully-qualified name in the `name` property (such as `mydb.schema1.my-app`). |
| **type**  *optional*, *string* | Must be one of: `function` or `procedure`. |
| **artifact\_repository**  *optional*, *string* | Name of the artifact repository. Snowflake has a default artifact repository called `snowflake.snowpark.pypi_shared_repository` that you use to connect and install PyPI packages within Snowpark UDFs and procedures. For more information, see [Artifact Repository overview](/developer-guide/udf/python/udf-python-packages#label-python-udfs-pypi).  The `artifact_repository` and `packages` parameters let you use non-anaconda packages, similar to the following:   - In the project’s `app.py` file, you can define a function like the following:   Copy code  ``` from sklearn.datasets import load_iris from sklearn.model_selection import train_test_split from sklearn.ensemble import RandomForestClassifier  def udf():   X, y = load_iris(return_X_y=True)   X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)    model = RandomForestClassifier()   model.fit(X_train, y_train)   return model.score(X_test, y_test) ```   - In the `snowflake.yml` file, you would then define it like the following:   Copy code  ``` test_function:   type: "function"   handler: "app.udf"   identifier:     - name: "udf"   stage: "dev_deployment"   signature: ""   returns: float   artifact_repository: snowflake.snowpark.pypi_shared_repository   packages:     - "scikit-learn"   artifacts: "app.py" ```  For packages that depend on specific architectures, you can define them in the `resource_constraint` parameter as follows:  Copy code  ``` test_function:    type: "function"    handler: "app.udf"    identifier:      - name: "udf"    stage: "dev_deployment"    signature: ""    returns: float    artifact_repository: snowflake.snowpark.pypi_shared_repository    packages:      - "scikit-learn"    artifacts: "app.py" ```  For more information, see [Packages built only for x86](/developer-guide/udf/python/udf-python-packages#label-python-udfs-pypi-x86). |
| **artifact\_repository\_packages**  *optional*, *string* | Note  This property has been deprecated in favor of the `packages` property. |
| **packages**  *optional*, *string sequence* | List of PyPI packages to install from the artifact repository specified in `artifact_repository`. This field requires `artifact_repository` to be set; using `packages` alone returns an error.  You can also list PyPI packages in a project-root `requirements.txt` file. Snowflake CLI downloads packages that are not on the Anaconda channel and includes them in the application zip.  For Anaconda-channel packages (such as `snowflake-snowpark-python`, `pandas`, or `numpy`), declare them in `requirements.txt`. The `requirements.txt` file is automatically picked up by `snow snowpark deploy`.  For example:  Copy code  ``` artifact_repository: snowflake.snowpark.pypi_shared_repository packages:   - Faker   - rich   - pytest ``` |
| **artifacts**  *required*, *string sequence* | List of file source and destination pairs to add to the deploy root. You can use the following artifact properties:   - `src`: Path to the code source file or files - `dest`: Path to the directory to deploy the artifacts.   Destination paths that reference directories must end with a `/`. A glob pattern’s destination that does not end with a `/` results in an error. If omitted, `dest` defaults to the same string as `src`.  Note  Using glob patterns in Snowpark `snowflake.yml` files requires enabling the ENABLE\_SNOWPARK\_GLOB\_SUPPORT feature flag.  You can also pass in a string for each item instead of a `dict`, in which case the value is treated as both `src` and `dest`.  If `src` refers to just one file (not a glob), `dest` can refer to a target `<path>` or a `<path/name>`.  You can also pass in a string for each item instead of a `dict`, which case, the value is treated as both `src` and `dest`. |
| **handler**  *required*, *string* | Function’s or procedure’s implementation of the object inside module defined in `snowpark.src`. For example `functions.hello_function` refers to function `hello_function` from file `<src>/functions.py`. |
| **returns**  *required*, *string* | SQL type of the result. Check the list of [available types](/developer-guide/udf-stored-procedure-data-type-mapping#label-sql-python-data-type-mappings). |
| **signature**  *required*, *sequence* | The `signature` parameter describes consecutive arguments passed to the object. Each should specify its name and type, for example:  Copy code  ``` signature:   - name: "first_argument"     type: int   - name: "second_argument"     default: "default value"     type: string ```  If a function or procedure takes no arguments, set this value to an empty string (`signature: ""`).  Check the **SQL Type** column of [available types](/developer-guide/udf-stored-procedure-data-type-mapping#label-sql-python-data-type-mappings). To learn more about the syntax of named and optional arguments, see [Calling a UDF that has optional arguments](/developer-guide/udf/udf-calling-sql#label-call-udf-calling-udf-optional). |
| **runtime**  *optional*, *string* | Python version to use when executing the procedure or function. Default: “3.12”. |
| **external\_access\_integrations**  *optional*, *string sequence* | Names of [external access integrations](/sql-reference/sql/create-external-access-integration) needed for this procedure’s handler code to access external networks. See the [EXTERNAL\_ACCESS\_INTEGRATIONS parameter in CREATE PROCEDURE](/sql-reference/sql/create-procedure#label-create-procedure-python-eai) for more details. |
| **secrets**  *optional*, *dictionary* | Assigns the names of secrets to variables so that you can use the variables to reference the secrets when retrieving information from secrets in handler code. See [the SECRETS parameter in CREATE PROCEDURE](/sql-reference/sql/create-procedure#label-create-procedure-python-secrets) for more details. |
| **imports**  *optional*, *string sequence* | Stage and path to previously uploaded files you want to import. See [the IMPORT parameter in CREATE PROCEDURE](/sql-reference/sql/create-procedure#label-create-procedure-python-imports) for more details. |
| **execute\_as\_caller**  *optional*, *bool* | **Available only for procedures**. Determine whether the procedure is executed with the privileges of the owner (you) or with the privileges of the caller. Default: False (owner’s privileges). |

Expand

Show lessSee more
