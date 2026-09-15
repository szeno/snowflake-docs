# Using artifact repositories

Snowflake’s default PyPI Artifact Repository lets you install PyPI packages with support for package policies in your notebooks.
The Snowflake PyPI repo is a schema-level, RBAC-governed object: `snowflake.snowpark.pypi_shared_repository`.

You can also use a [customer-hosted artifact repository](/developer-guide/udf/python/customer-hosted-python-artifact-repositories) as the package source for a notebook: for example, a Nexus, JFrog, Azure DevOps, GCP Artifact Registry, or AWS CodeArtifact repository registered as a Snowflake `ARTIFACT REPOSITORY` object.

## Privilege requirements

By default, the PUBLIC role has access to the Snowflake PyPI repo. To manage privileges, use the following commands:

Copy code

```
-- To revoke access from the PUBLIC role:
REVOKE DATABASE ROLE SNOWFLAKE.PYPI_REPOSITORY_USER FROM ROLE PUBLIC;

-- To grant access to specific roles:
GRANT DATABASE ROLE SNOWFLAKE.PYPI_REPOSITORY_USER TO ROLE <your_user_role>;
```

## Using artifact repositories in Snowsight

You can use artifact repositories in both interactive sessions and scheduled notebooks.

### Interactive sessions

1. Go to **Workspaces** > **Notebooks**.
2. Edit or create a new notebook service.
3. Choose `snowflake.snowpark.pypi_shared_repository` or a customer-hosted artifact repository from the **Artifact Repository** dropdown menu.
4. Select **Create and connect**.
5. Install packages by using a Python cell:

   Copy code

   ```
   !pip install <package_name>
   ```

### Scheduled notebooks

In the **Scheduling** dialog, choose `snowflake.snowpark.pypi_shared_repository` or a customer-hosted artifact repository from the **Artifact Repository**
dropdown menu.

Note

If you’ve selected an artifact repository in the notebook service, you can only install packages from that repository,
not through any external access integrations (EAIs).

Multi-node training APIs such as `scale_cluster` are not yet supported when using artifact repositories.

## Setting the default repository

An ACCOUNTADMIN can use a parameter to set a default artifact repository. The default repo is automatically selected
in the **Artifact Repository** dropdown, but users can still select a different repository if they have access.

This is an account-level parameter that applies to the notebook service dialogs for all users. The notebook **Artifact Repository** dropdown supports `snowflake.snowpark.pypi_shared_repository` and customer-hosted artifact repositories.

Copy code

```
-- Snowflake-managed PyPI:
ALTER ACCOUNT SET DEFAULT_PYTHON_ARTIFACT_REPOSITORY = snowflake.snowpark.pypi_shared_repository;

-- Customer-hosted repository:
ALTER ACCOUNT SET DEFAULT_PYTHON_ARTIFACT_REPOSITORY = my_db.my_schema.my_python_repo;

-- To unset the default:
ALTER ACCOUNT UNSET DEFAULT_PYTHON_ARTIFACT_REPOSITORY;
```

## Headless execution with SQL

When you use the EXECUTE NOTEBOOK PROJECT command in scheduling and production workloads, include the ARTIFACT\_REPOSITORIES
parameter as an optional argument.

Copy code

```
EXECUTE NOTEBOOK PROJECT <database_name>.<schema_name>.<project_name>
  MAIN_FILE = 'notebook.ipynb'
  COMPUTE_POOL = '<compute_pool_name>'
  QUERY_WAREHOUSE = '<warehouse_name>'
  RUNTIME = '<runtime_version>'
  [ ARGUMENTS = '<parameter_string>' ]
  [ REQUIREMENTS_FILE = '<path/to/requirements.txt>' ]
  [ EXTERNAL_ACCESS_INTEGRATIONS = ( <integration_name> ) ]
  [ ARTIFACT_REPOSITORIES = (snowflake.snowpark.pypi_shared_repository) ];
```

Note

If both EXTERNAL\_ACCESS\_INTEGRATIONS and ARTIFACT\_REPOSITORIES parameters are specified, packages are only installed from the
artifact repositories.
