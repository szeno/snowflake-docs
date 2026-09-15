# Create your Streamlit app

This topic describes how to deploy a Streamlit in Snowflake app from existing Streamlit app code. If you’re
new to Streamlit in Snowflake and want to try a starter app first, see
[Getting started with Streamlit in Snowflake](/developer-guide/streamlit/getting-started/overview).

Before you begin:

- Ensure that you meet the required [prerequisites](/developer-guide/streamlit/getting-started/overview#label-streamlit-prereqs).
- Choose a [runtime environment](/developer-guide/streamlit/app-development/runtime-environments) for your app (container or warehouse).
- Prepare your [dependencies](/developer-guide/streamlit/app-development/dependency-management) in a `requirements.txt`,
  `pyproject.toml`, or `environment.yml` file.
- Review the expected [file organization](/developer-guide/streamlit/app-development/file-organization) for your app’s source files.

## Deploy your app code

If you already have a Streamlit app on your local machine or on a Snowflake stage, use one
of the following methods to create a STREAMLIT object from your source files.

SnowsightSQLSnowflake CLI

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **Streamlit**.
3. Select **+ Streamlit App**.
4. Enter a name for your app.
5. In the **App location** dropdown, select the database and schema for your app.
6. Configure the runtime for your app:

   To create a container-runtime app, make the following selections:

   - Select **Run on container**.
   - If a compute pool dropdown appears, select the compute pool to run your app on.
     If no dropdown appears, the app uses the account-level
     [DEFAULT\_STREAMLIT\_COMPUTE\_POOL](/sql-reference/parameters#label-default-streamlit-compute-pool) parameter. You can change the compute
     pool after the app is created. See [Change the compute pool](/developer-guide/streamlit/app-development/managing-your-app#label-streamlit-change-compute-pool).
   - Select a query warehouse to run your app’s queries on.

   To create a warehouse-runtime app, make the following selections:

   - Select **Run on warehouse**.
   - Select a warehouse to run your app on.
7. Select **Create**.
8. In the editor, replace the starter code with your own app code. You can paste code
   directly or upload files:

   - To upload files, select **+** (Add) » **Upload file**, choose the files,
     and select **Upload**.
   - To create additional files (such as `pyproject.toml`), select **+** (Add)
     » **Create new file**.
9. Select **Run**.

1. Upload your app files to a named stage:

   Copy code

   ```
   CREATE STAGE IF NOT EXISTS my_db.my_schema.my_stage;

   PUT file:///path/to/streamlit_app.py @my_db.my_schema.my_stage/app
   AUTO_COMPRESS = FALSE OVERWRITE = TRUE;
   PUT file:///path/to/pyproject.toml @my_db.my_schema.my_stage/app
   AUTO_COMPRESS = FALSE OVERWRITE = TRUE;
   ```

   You can also upload files through Snowsight as described in
   [Staging files using Snowsight](/user-guide/data-load-local-file-system-stage-ui).
2. Create the STREAMLIT object from your staged files:

   To create a container-runtime app, run the following command:

   Copy code

   ```
   CREATE STREAMLIT my_app
   FROM '@my_db.my_schema.my_stage/app'
   MAIN_FILE = 'streamlit_app.py'
   RUNTIME_NAME = 'SYSTEM$ST_CONTAINER_RUNTIME_PY3_11'
   COMPUTE_POOL = my_compute_pool
   QUERY_WAREHOUSE = my_warehouse;
   ```

   To create a warehouse-runtime app, omit the RUNTIME\_NAME and COMPUTE\_POOL parameters:

   Copy code

   ```
   CREATE STREAMLIT my_app
   FROM '@my_db.my_schema.my_stage/app'
   MAIN_FILE = 'streamlit_app.py'
   QUERY_WAREHOUSE = my_warehouse;
   ```
3. Push your code to the live version:

   Copy code

   ```
   ALTER STREAMLIT my_app ADD LIVE VERSION FROM LAST;
   ```

   You must run this command before users with only USAGE privilege on the Streamlit
   object can view it.

For the full parameter reference, see [CREATE STREAMLIT](/sql-reference/sql/create-streamlit).

Note

[Snowflake CLI](/developer-guide/snowflake-cli/installation/installation) version 3.14.0
or later is required. Version 3.14+ uses the modern CREATE STREAMLIT syntax by default.

1. In your project directory, create a `snowflake.yml` file alongside your app code.

   To create a container-runtime app, use the following configuration:

   Copy code

   ```
   definition_version: 2
   entities:
   my_streamlit:
      type: streamlit
      identifier: my_app
      query_warehouse: my_warehouse
      compute_pool: my_compute_pool
      runtime_name: SYSTEM$ST_CONTAINER_RUNTIME_PY3_11
      main_file: streamlit_app.py
      artifacts:
      - streamlit_app.py
      - pyproject.toml
   ```

   To create a warehouse-runtime app, omit `compute_pool` and `runtime_name`:

   Copy code

   ```
   definition_version: 2
   entities:
   my_streamlit:
      type: streamlit
      identifier: my_app
      query_warehouse: my_warehouse
      main_file: streamlit_app.py
      artifacts:
      - streamlit_app.py
      - environment.yml
   ```

   List all files your app needs in the `artifacts` section.
2. Deploy the app:

   Copy code

   ```
   snow streamlit deploy --open
   ```

For more information, see the
[Creating a Streamlit app](/developer-guide/snowflake-cli/streamlit-apps/manage-apps/initialize-app) and
[Deploying a Streamlit app](/developer-guide/snowflake-cli/streamlit-apps/manage-apps/deploy-app) guides.

## View a Streamlit app

For information about the privileges required to view a Streamlit app, see
[Privileges required to view a Streamlit app](/developer-guide/streamlit/object-management/privileges#label-streamlit-access-privs-view).

SnowsightSQLSnowflake CLI

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **Streamlit**.
3. Select the Streamlit app you want to view.

If you are viewing a multipage Streamlit app, select a tab to view additional pages.

To view information about a STREAMLIT object:

Copy code

```
DESC STREAMLIT my_app;
```

To view the app in a browser, sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in), then In the navigation menu, select **Projects** » **Streamlit**,
and select the app.

To get the URL for your deployed app:

Copy code

```
snow streamlit get-url my_app
```

## Set up CI/CD with GitHub Actions

You can deploy Streamlit in Snowflake apps automatically from a Git repository using Snowflake CLI
and [GitHub Actions](https://docs.github.com/en/actions). You can use a similar
approach with other CI/CD providers.

### Prerequisites

- A GitHub repository containing your Streamlit app files and `snowflake.yml`.
- A `SNOWCLI_PW` secret configured in your GitHub repository settings.

### Example workflow

Create a `.github/workflows/deploy.yml` file in your repository:

Copy code

```
name: Deploy via Snowflake CLI

on:
  push:
    branches:
      - main

env:
  PYTHON_VERSION: '3.12'

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    environment: dev
    steps:
      - name: 'Checkout GitHub Action'
        uses: actions/checkout@v3

      - name: Install Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: 'Install Snowflake CLI'
        shell: bash
        run: |
          python -m pip install --upgrade pip
          pip install snowflake-cli

      - name: 'Create config'
        shell: bash
        env:
          SNOWFLAKE_PASSWORD: ${{ secrets.SNOWCLI_PW }}
        run: |
          mkdir -p ~/.snowflake
          cp config.toml ~/.snowflake/config.toml
          echo "password = \"$SNOWFLAKE_PASSWORD\"" >> ~/.snowflake/config.toml
          chmod 0600 ~/.snowflake/config.toml

      - name: 'Deploy the Streamlit app'
        shell: bash
        run: |
          snow streamlit deploy --replace
```

Commit and push the file to trigger the workflow.

For more information, see [GitHub Actions documentation](https://docs.github.com/en/actions).
