# CREATE NOTEBOOK

Creates a new [Snowflake notebook](/user-guide/ui-snowsight/notebooks) or replaces an existing notebook.

## Syntax

Copy code

```
CREATE [ OR REPLACE ] NOTEBOOK [ IF NOT EXISTS ] <name>
  [ FROM '<source_location>' ]
  [ MAIN_FILE = '<main_file_name>' ]
  [ COMMENT = '<string_literal>' ]
  [ QUERY_WAREHOUSE = <warehouse_to_run_nb_and_sql_queries_in> ]
  [ IDLE_AUTO_SHUTDOWN_TIME_SECONDS = <number_of_seconds> ]
  [ RUNTIME_NAME = '<runtime_name>' ]
  [ COMPUTE_POOL = '<compute_pool_name>' ]
  [ WAREHOUSE = <warehouse_to_run_notebook_python_runtime> ]
```

## Required parameters

`name`
:   String that specifies the identifier (i.e. name) for the notebook; must be unique for the schema in which the notebook is created.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the
    entire identifier string is enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in double quotes are also
    case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Optional parameters

`FROM 'source_location'`
:   Specifies that the notebook should be created from an `.ipynb` file in the specified stage location. To create the notebook from a file
    on a stage, set `source_location` to the stage location of the file, and set the MAIN\_FILE parameter to the name of the file.

    If this parameter is not specified, the notebook object is created from a template notebook.

`MAIN_FILE = 'main_file_name'`
:   User-specified identifier for the notebook file name. This is separate from the notebook object name, which is specified in the
    `name` parameter. This file must be an `ipynb` file.

`QUERY_WAREHOUSE = warehouse_name`
:   Specifies the warehouse where SQL queries in the notebook are run.
    This parameter is optional. However, it is required to run the EXECUTE NOTEBOOK command.

`IDLE_AUTO_SHUTDOWN_TIME_SECONDS = number_of_seconds`
:   Number of seconds of idle time before the notebook is shut down automatically. This parameter is only available for notebooks running
    on the Container Runtime. The value must be an integer between 60 and 259200 (72 hours).

    Default: 3600 seconds

`RUNTIME_NAME = runtime_name`
:   - *‘SYSTEM$WAREHOUSE\_RUNTIME’* (default): Runs the notebook in a Snowflake warehouse (Warehouse Runtime only).
    - *‘SYSTEM$BASIC\_RUNTIME’*: Runs the notebook in a Snowpark Container Services (SPCS) container using a CPU runtime (Container Runtime only).
    - *‘SYSTEM$GPU\_RUNTIME’*: Runs the notebook in a Snowpark Container Services (SPCS) container using a GPU runtime (Container Runtime only).

    When specifying a Container Runtime (*SYSTEM$BASIC\_RUNTIME\_ or \_SYSTEM$GPU\_RUNTIME*), you must also include the *COMPUTE\_POOL* parameter. *SYSTEM$WAREHOUSE\_RUNTIME* is for Warehouse Runtime only.

`COMPUTE_POOL = compute_pool_name`
:   (Container Runtime only) Specifies the compute pool that hosts the notebook when using a Container Runtime. This parameter is required when *RUNTIME\_NAME* is set
    to *SYSTEM$BASIC\_RUNTIME\_ or \_SYSTEM$GPU\_RUNTIME*.

    For more information about compute pools, see [Snowpark Container Services: Working with compute pools](/developer-guide/snowpark-container-services/working-with-compute-pool).

`WAREHOUSE = warehouse_name`
:   The warehouse is used to run:

    > - For Warehouse Runtime: Both the notebook kernel and SQL queries (including Snowpark pushdown compute).
    > - For Container Runtime: Only SQL queries (including Snowpark pushdown compute). The notebook kernel runs on the compute pool.

    If you don’t specify a warehouse when you create a notebook, Snowflake uses the default warehouse defined by the schema lineage
    parameter *DEFAULT\_STREAMLIT\_NOTEBOOK\_WAREHOUSE*. You can set this parameter at the schema, database, or account lineage level to define a
    preferred warehouse.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object |
| --- | --- |
| USAGE | Database |
| USAGE or OWNERSHIP | Schema |
| CREATE NOTEBOOK | Schema |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- When creating a notebook that uses a Container Runtime, the notebook runs inside a Snowpark Container Services environment. Container runtime notebooks must
  specify both the *RUNTIME\_NAME* and *COMPUTE\_POOL* parameters.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

- The OR REPLACE and IF NOT EXISTS clauses are mutually exclusive. They can’t both be used in the same statement.
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

## Examples

The following creates a notebook named `mynotebook`:

Copy code

```
CREATE NOTEBOOK mynotebook;
```

Although the QUERY\_WAREHOUSE parameter is optional, specifying it is recommended when creating a new notebook so
that EXECUTE NOTEBOOK can be run on the warehouse.

Copy code

```
CREATE NOTEBOOK mynotebook
 QUERY_WAREHOUSE = my_warehouse;
```

The following example creates a notebook from an `ipynb` file on a stage:

Copy code

```
CREATE NOTEBOOK mynotebook
 FROM '@my_db.my_schema.my_stage'
 MAIN_FILE = 'my_notebook_file.ipynb'
 QUERY_WAREHOUSE = my_warehouse;
```

The following example creates a notebook using Container Runtime (CPU):

Copy code

```
CREATE NOTEBOOK my_cpu_notebook
  RUNTIME_NAME = 'SYSTEM$BASIC_RUNTIME'
  COMPUTE_POOL = 'my_compute_pool';
```

The following example creates a notebook using Container Runtime (GPU):

Copy code

```
CREATE NOTEBOOK my_gpu_notebook
  RUNTIME_NAME = 'SYSTEM$GPU_RUNTIME'
  COMPUTE_POOL = 'gpu_pool_1';
```
