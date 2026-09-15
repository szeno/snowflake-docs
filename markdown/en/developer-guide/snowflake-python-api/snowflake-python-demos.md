# Snowflake Python Demos API

The Snowflake Python Demos library (`snowflake.demos`) helps you rapidly scaffold demos for
[Snowflake Notebooks](/user-guide/ui-snowsight/notebooks) by automating environment setup tasks — such as configuring the database,
schema, role, permissions, and dataset access — to streamline getting started with Snowflake Notebooks.

With this library, you can perform these tasks:

- Load and set up Snowflake Notebooks demos in your Snowflake environment.
- Explore interactive notebooks step by step to get hands-on experience.
- Tear down resources easily when you’re done.

## Prerequisites

Before you get started with the Snowflake Demos API, complete the following steps:

1. Verify that you have installed one of the supported Python versions:

   - 3.9
   - 3.10
   - 3.11
   - 3.12
2. [Install the Snowflake Demos library](#label-snowflake-python-demos-install).
3. [Set up a default Snowflake connection](#label-snowflake-python-demos-connection).
4. [Import](#label-snowflake-python-demos-import).

### Install the Snowflake Demos library

You can install the Snowflake Demos library for use with conda or a virtual environment. To set up the library, follow these steps:

1. [Activate a Python environment](/developer-guide/snowflake-python-api/snowflake-python-installing#label-snowflake-python-activate-environment).
2. To install the library, run the following `pip install` command:

   Copy code

   ```
   pip install snowflake.demos
   ```

### Set up a default Snowflake connection

The Snowflake Demos API uses the default connection for the [Snowflake Python Connector](/developer-guide/python-connector/python-connector).
To configure this connection, follow the instructions in [Setting a default connection](/developer-guide/python-connector/python-connector-connect#label-python-default-connection).

For example, to specify a named connection as the default connection in your Snowflake `config.toml` file, you add your default
connection name to the `config.toml` file as follows:

Copy code

```
default_connection_name = '<connection_name>'
```

For information about specifying connection definitions in a TOML configuration file, see [Connecting using the `connections.toml` file](/developer-guide/python-connector/python-connector-connect#label-python-connection-toml).

### Import `snowflake.demos`

To use the library in your terminal, you can open an interactive shell such as the standard Python REPL.

1. Run the following command (which might vary depending on your Python environment):

   Copy code

   ```
   python3
   ```
2. In the REPL session, to import the library and the relevant functions, run the following code:

   Copy code

   ```
   from snowflake.demos import help, load_demo, teardown
   ```

## Listing available demos

After importing the library, you can use the `help()` function to see the list of available demos that you can load and start
exploring. This function returns a table with the following columns:

- `demo_name`: A dash-delimited string that represents the demo name.
- `title`: The human-readable demo name title.
- `num_steps`: The number of steps in the demo.

### Current list of available demos

Note

The following content is not supported by Snowflake. All code is provided “AS IS” and without warranty.

The Snowflake Demos API currently works with the following list of demos:

| demo\_name | title | num\_steps |
| --- | --- | --- |
| `analysis-churn-notebooks` | Data analysis and churn prediction using Snowflake Notebooks | 2 |
| `analytics-cortex` | Customer reviews analytics using Snowflake Cortex | 1 |
| `anthropic-cortex` | Getting started with Anthropic on Snowflake Cortex | 1 |
| `external-access-nb` | Access external endpoints | 1 |
| `get-started-partitioned-models` | Getting started with partitioned models and Snowflake Model Registry | 1 |
| `get-started-snowapi-nb` | Creating Snowflake objects using Python API | 1 |
| `get-started-snowpark-ws-nb` | Getting started with Snowpark in Snowflake Notebooks and Python Worksheets | 1 |
| `get-started-snowflake-ml` | Getting started with Snowflake ML | 4 |
| `ingest-json-data` | Ingest public JSON | 1 |
| `intro-snowpark-pandas` | Introduction to Snowpark pandas | 1 |
| `intro-to-feature-store-nb` | Introduction to Feature Store using Snowflake Notebooks | 1 |
| `intro-to-snowflake-nb` | My first Notebook project | 1 |
| `load-csv-to-stage` | Load CSV from S3 | 1 |
| `ref-cells-and-vars` | Reference cells and variables | 1 |
| `visual-data-stories` | Visual data stories with Snowflake Notebooks | 1 |
| `working-with-files` | Working with files | 1 |

Expand

Show lessSee more

## Working with demos

After completing the [prerequisites](#label-snowflake-python-demos-prerequisites), you can start using the Snowflake Demos API to work
with demos as described in the following sections.

### Load and explore a demo

- To load a specific demo and set up its associated resources in Snowflake, call `load_demo()` with an argument that specifies the
  `demo_name` of any available demo, as found in the `help()` output.

  For example:

  Copy code

  ```
  load_demo('get-started-snowflake-ml')
  ```

Tip

- To store a reference to the demo as an object, assign the result of `load_demo()` to a variable:

  Copy code

  ```
  demo = load_demo('get-started-snowflake-ml')
  ```

Assigning the result to a variable is required if you’re working with a multi-step demo (`num_steps` > 1). You will need this
reference to call `show_next()` or `show(step=<number>)` to move to the next notebook in the demo.

You can also use this reference to quickly tear down the demo later.

This function does the following:

- Creates a connection to Snowflake if it’s the first time you’re loading a demo.
- Creates the necessary notebooks.
- Displays the notebook URL for the first step of the demo (step 1), if you are not assigning `load_demo()` to a variable.
  - If you assign `load_demo()` to a variable, you need to call `demo.show()` to get the first notebook URL.

The output should look similar to the following:

```
Connecting to Snowflake...✅
Using ACCOUNTADMIN role...✅
Creating Database SNOWFLAKE_DEMO_DB...✅
Creating Schema SNOWFLAKE_DEMO_SCHEMA...✅
Creating Warehouse SNOWFLAKE_DEMO_WH...✅
Creating Stage SNOWFLAKE_DEMO_STAGE...✅
Uploading files to stage SNOWFLAKE_DEMO_STAGE/get-started-snowflake-ml and creating notebooks...
Creating notebook get_started_snowflake_ml_start_here...✅
Creating notebook get_started_snowflake_ml_sf_nb_snowflake_ml_feature_transformations...✅
Creating notebook get_started_snowflake_ml_sf_nb_snowflake_ml_model_training_inference...✅
Creating notebook get_started_snowflake_ml_sf_nb_snowpark_ml_adv_mlops...✅
Running setup for this demo...✅
```

Note

A known issue exists with the printed notebook URLs. If the URL doesn’t open directly, you can copy and paste it into a new browser tab
or access the notebook manually in Snowsight under the **Notebooks** tab.

### View the demo URL

You can use the `show()` function to view the URL to a specific step in the demo.

- To view the URL for the current step, first assign the result of `load_demo()` to a variable, such as `demo`, and then call
  `show()` with no arguments:

  Copy code

  ```
  demo.show()
  ```

  The output should look similar to this:

  ```
  Showing step 1.
  Please copy and paste this url in your web browser to open the notebook:
  https://app.snowflake.com/myorg/myaccount/#/notebooks/SNOWFLAKE_DEMO_DB.SNOWFLAKE_DEMO_SCHEMA.GET_STARTED_SNOWFLAKE_ML_START_HERE
  ```
- To get the notebook URL for a specific step in the demo, pass the `step` argument with a specified step number to `show()`:

  Copy code

  ```
  demo.show(step=1)
  ```
- To get the notebook URL for the next step in a multi-step demo, use the `show_next()` function:

  Copy code

  ```
  demo.show_next()
  ```

### Delete a demo and its resources

When you’re done exploring the demos that you set up, you might want to clean up all created resources, datasets, and notebooks that were
created.

- To delete a single demo and its associated resources, first assign the result of `load_demo()` to a variable such as `demo`, and
  then call `teardown()` on it:

  Copy code

  ```
  demo.teardown()
  ```
- To delete all demos and any associated resources that have been set up, call `teardown()` as a top-level function:

  Copy code

  ```
  teardown()
  ```
