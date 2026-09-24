# Using Snowpark in a clean room

End-of-life notice

The legacy Provider and Consumer Data Clean Rooms are being discontinued. See the
[end-of-life timeline](/user-guide/cleanrooms/pc-eol) for dates and migration guidance.

## Introduction

Snowflake Data Clean Rooms can work with Snowpark to provide increased computing power to your clean rooms when you need to query or
process large-scale data.

Clean rooms can use Snowpark in two ways:

- [Snowpark UDFs](#label-dcr-snowpark-udf): Use the Snowpark API in your clean room code to create Snowpark UDFs that take advantage
  of Snowpark scaling and processing power.
- [Snowpark Container Services](#label-dcr-snowpark-spcs): If you want greater control of the Snowpark environment, or want to use
  libraries not available with the Snowpark API, you can configure and host a container within a clean room. This enables you to configure
  the environment for your specific compute and storage needs, and customize the libraries available to your environment.

When you need to load data that is too big to fit in memory, use `to_pandas_batches()` and iterate over it. For example:

> Copy code
>
> ```
> df_iter = session.table(intermediary_table_name).to_pandas_batches()
> for df in df_iter:
>   ...
> ```

### General design of complex usage flows

Although you could generate your data and display it all by calling one template, in many cases it’s better to break up the data generation
steps from the result viewing steps. This way a consumer can view results multiple times without triggering a recalculation each time, or
view data from various points in the process. To break up your flow into multiple user-accessible stages, create separate templates for
triggering data generation or processing, and for viewing stored results.
[Read more about designing complex usage flows.](/user-guide/cleanrooms/multistep-flows)

## Using Snowpark UDFs in a clean room

You can use the [Snowpark API](/developer-guide/snowpark/index) in your uploaded Python code to speed up processing of large data
loads. Clean rooms support only the [Snowpark Python API](/developer-guide/snowpark/python/index). Both providers and consumers can
use the Snowpark Python API in their uploaded Python code.

### Prerequisites

- Clean rooms that run Snowpark UDFs must be run in the clean rooms API; they cannot be run in the clean rooms UI.
- You should understand the following topics:
  - [The basics of creating a clean room in code.](/user-guide/cleanrooms/tutorials/cleanroom-api-tutorial-basic)
  - [The Snowpark Python API.](/developer-guide/snowpark/python/index)
  - [How to upload Python UDFs into a clean room.](/user-guide/cleanrooms/demo-flows/custom-code)
  - [How to create custom templates.](/user-guide/cleanrooms/custom-templates)
  - Read about [designing multi-step flows](/user-guide/cleanrooms/multistep-flows) to understand internal tables.

### Using the Snowpark API in a clean room

Using the Snowpark API in your clean room Python code is the same as uploading and running any other Python UDF, except that you need to
link in the `snowflake-snowpark-python` library.

Create UDFs, UDTFs, and procedures by executing SQL using `session.sql` in the `cleanroom` schema rather than using the Snowpark
decorators. For example:

> Copy code
>
> ```
> session.sql("CREATE OR REPLACE FUNCTION cleanroom.udf(...")
> ```

### Basic steps

Here are the basic steps to use the Snowpark API through a UDF or UDTF in your clean room:

**Provider**

1. Create the clean room, set the default release directive, and link in your data in the standard way.
2. Because you probably have a very specific use case designed for your code, you probably won’t need to add join or column policies to the
   clean room, although you can do so.
3. Load your custom Snowpark handler code into the clean room by calling `provider.load_python_into_cleanroom`. The code should load the
   `snowflake-snowpark-python` package at minimum, plus any other packages that you need.
   UDFs can process and return data line by line, but Snowpark use cases typically generate an output table that is read by calling a
   separate results template.
4. Update the default release directive (because code additions generate a new patch version).
5. Create and upload a [custom template](/user-guide/cleanrooms/custom-templates) to run your Snowpark code. The only way to run a
   UDF is to trigger it from a template that calls the UDF. Some details about the UDF-calling template:

   - It should call the function using the alias and parameters that you specified in `provider.load_python_into_cleanroom`. The
     template must use the `cleanroom` namespace to call your function’s alias.
   - If the UDF writes results to a table in the clean room, and the name of the table is different for each run, your results-generating
     template should return the name of the results table, and your results template should take the table name as an argument from the
     user.
6. Upload a custom SQL template to access the results table generated by your Snowpark UDF, if you generated an intermediary results table.
   Either use the hard-coded results table name, or let the user pass in the table name generated by your code and returned by the
   results-generating template.
7. Add collaborators and publish the clean room in the standard way.

**Consumer**

The consumer installs the clean room and runs the analysis in the standard way. If the data generation and results reading are broken into
separate templates, the consumer will need to call each template in sequence.

### Example code

The following example code demonstrates how to upload and run a linear regression of “reach on impression count” to estimate the slope.

1. The consumer first runs the `prod_calculate_regression` template that runs a provider UDF to generate results. The provider UDF
   performs the following actions:

   1. **Preprocess impressions data.** Dynamic SQL is created that joins the provider’s impressions data to the consumer’s data, calculates
      the distinct count of impressions and reach by date, and stores the results in an intermediary table inside the clean room. If the
      consumer does not supply a table, the code runs against the provider’s entire impressions table.
   2. **Load the intermediary table.** The intermediary table is loaded into the Snowpark procedure as a pandas DataFrame.
   3. **Carry out regression.** The regression is calculated using the `statsmodels` library and returns results as a pandas DataFrame.
   4. **Write results to an internal clean room table.** The results are written to a results table inside the clean room, and the ID
      suffix of the table name is returned to the consumer. Since the Snowpark procedure is running inside the clean room, it has a limited
      ability to activate the data to the consumer’s account. Instead, to keep the results more secure, it is written to a table inside the
      clean room, and the consumer runs another template to read the results data.
   5. **Drop the intermediary tables.** Intermediary tables created during the calculation inside the clean room that are no longer needed
      are dropped before the Snowpark procedure finishes.
   6. **Return the name of the results table.** The name returned to the consumer must be specified when running the template to get the
      results, because results from all previous runs are retained.
2. The consumer then runs the `get_results` template, passing in the results table suffix returned by the first template to see the
   results.

To run the examples below, you need two accounts in the same web-hosting region (unless you’ve implemented
[cross-cloud auto-fulfillment](/user-guide/cleanrooms/v1/enabling-laf)): one account for the provider and another account for the
consumer.

The example code should run in a Snowflake worksheet without any additional Snowpark configuration. If you run in another environment, you
might need to install and configure the Snowpark Python API.

- [Provider worksheet example](/static/samples/clean-rooms/snowpark-udf-provider.sql)
- [Consumer worksheet example](/static/samples/clean-rooms/snowpark-udf-consumer.sql)

### More information

- [Creating User-Defined Functions (UDFs) for DataFrames in Python](/developer-guide/snowpark/python/creating-udfs).
- [Snowpark API](/developer-guide/snowpark/index)
- [Snowpark Developer Guide for Python](/developer-guide/snowpark/python/index)

## Using Snowpark Container Services in a clean room

If you want greater control over the environment that executes your Python code, you can run a Snowpark Container Service within the
clean room. This gives you fine control over the execution environment for your code, and is ideal in use cases requiring specialized
compute, storage, or other resources to maximize performance and minimize cost, or to bring in custom packages or other environment
features.

When you host a container service in your clean room, your template and any custom Python code can call functions exposed by your service.
Using Snowpark Container Services is similar to using UDFs in Snowpark, except that your UDFs are exposed as HTTP endpoints for the
template to call. You will define the service and endpoints and upload it to the clean room.

Internally-hosted endpoints are accessible only by templates within the clean room, and cannot be called directly by the clean room
collaborators.

### Prerequisites

You’ll need to understand the following topics to be able to use Snowpark Container Services in a clean room:

- [How to create a clean room in code](/user-guide/cleanrooms/tutorials/cleanroom-api-tutorial-basic).
- [The Snowpark Python API](/developer-guide/snowpark/python/index) if using that API.
- [How to create custom templates](/user-guide/cleanrooms/custom-templates).
- Read about [designing complex usage flows.](/user-guide/cleanrooms/multistep-flows) to understand how to break up processing data
  and exposing results into separate steps.

### Basic steps

**Provider**

1. Create the service spec, code, and the endpoints that handle processing requests.
2. Create an image repository and grant SAMOOHA\_APP\_ROLE access to that repository.
3. Capture the repository URL for the next step.
4. Build and upload the image to the repository URL.
5. Create the clean room, link data, add join policies, and add consumers in the standard way.
6. [Define the templates](/user-guide/cleanrooms/custom-templates) that call the service endpoints and upload them to your clean
   room. Service functions are created and called in the namespace `service_functions` (unlike UDFs, which are created and called in the
   namespace `cleanroom`).

   Copy code

   ```
   -- Template to call an SPCS function named train.
   SELECT service_functions.train(
      {{ source_table[0] }},
      {{ provider_join_col }},
      {{ my_table[0] }},
      {{ consumer_join_col }},
      {{ dimensions | sqlsafe }},
   ) AS train_result;
   ```
7. Upload your service details into the clean room by calling `provider.load_service_into_cleanroom`. This defines the image URL,
   endpoints, and other service options. The endpoint names defined here must match your service spec, and are the names that your template
   uses to call the functions.

   Copy code

   ```
   CALL samooha_by_snowflake_local_db.provider.load_service_into_cleanroom(
   $cleanroom_name,
   $$
   spec:
     containers:
     - name: lal
       image: /dcr_spcs/repos/lal_example/lal_service_image:latest
       env:
         SERVER_PORT: 8000
     endpoints:
     - name: lalendpoint
       port: 8000
       public: false
   $$,
   $$
   functions:
     - name: train
       args: PROVIDER_TABLE VARCHAR, PROVIDER_JOIN_COL VARCHAR, CONSUMER_TABLE VARCHAR, CONSUMER_JOIN_COL VARCHAR, DIMENSIONS ARRAY, FILTER VARCHAR
       returns: VARCHAR
       endpoint: lalendpoint
       path: /train
   $$);
   ```
8. Set the default release directive for your clean room. Whenever you upload or modify your service, it creates a new patch version.
9. Publish your clean room.
10. When making any changes to the image, functions, or code, you and the consumer must [update your instances](#label-dcr-spcs-update-config).

#### Consumer

1. Install the clean room and link in any data needed, in the standard way.
2. [Create a compute pool](#label-dcr-spcs-create-compute-pool) and grant access to the clean room.
3. If you will be running queries (and you almost certainly will), you must also grant USAGE privileges to the clean room on the warehouse
   being used.
4. Start the service by calling `samooha_by_snowflake_local_db.consumer.start_or_update_service`, passing in the clean room name, the
   compute pool name, and the warehouse name (if a warehouse is used).
5. Examine the available endpoints of the service by running `SHOW ENDPOINTS IN SERVICE SAMOOHA_CLEANROOM_APP_clean_room_name.services.service;`
6. When the service is up and running, you can begin to run any clean room templates that access service endpoints by calling
   `consumer.run_analysis` in the standard way.

### Creating the compute pool

Depending on who should own and configure the pool, the provider can create the compute pool inside the clean room, or the consumer
can create the compute pool outside the clean room.

If the compute pool is created outside the clean room, you must grant proper privileges to the clean room to access the pool and create the
service as shown here:

Copy code

```
-- Grant access to a warehouse to run queries. Needed only if the service queries Snowflake accounts.
USE ROLE ACCOUNTADMIN;
GRANT USAGE ON WAREHOUSE APP_WH TO APPLICATION SAMOOHA_CLEANROOM_APP_<CLEANROOM_NAME>;

-- Grant SAMOOHA_APP_ROLE privileges to create compute pools and create services
GRANT CREATE COMPUTE POOL ON ACCOUNT TO ROLE SAMOOHA_APP_ROLE WITH GRANT OPTION;
GRANT BIND SERVICE ENDPOINT ON ACCOUNT TO ROLE SAMOOHA_APP_ROLE WITH GRANT OPTION;

USE ROLE SAMOOHA_APP_ROLE;
-- Create the compute pool
CREATE COMPUTE POOL DCR_LAL_POOL
  FOR APPLICATION SAMOOHA_CLEANROOM_APP_<CLEANROOM_NAME>
  min_nodes = 1 max_nodes = 1
  instance_family = highmem_x64_l
  auto_resume = true;

-- Grant the clean room the privileges to access a pool running outside the clean room.
GRANT USAGE ON COMPUTE POOL DCR_LAL_POOL TO APPLICATION SAMOOHA_CLEANROOM_<CLEANROOM_NAME>;

-- Allow the clean room to create the service
GRANT BIND SERVICE ENDPOINT ON ACCOUNT TO APPLICATION SAMOOHA_CLEANROOM_APP_<CLEANROOM_NAME>;
```

### Updating your service code or configuration

If the provider updates the image, service spec, or endpoint names or source code, both the provider and consumer must take the following
steps.

**1. Provider:**

1. Update the image or source code as needed.
2. Call `provider.load_service_into_cleanroom`, which returns a new patch number.
3. Call `provider.set_default_release_directive` with the new patch number.

**2. Consumer:**

- Call `consumer.start_or_update_service`.

### Monitoring your service

By default, consumers can monitor their service. This behavior can be changed using the `allow_monitoring` value in the
`service_config` argument of `provider.load_service_into_cleanroom`.

If consumer monitoring is enabled, the consumer can access the monitoring logs for a given clean room service (in the format
`SAMOOHA_CLEANROOM_APP_SPCS_cleanroom_name.services.service`), service ID, and container, as shown here:

Copy code

```
SELECT VALUE AS log_line
  FROM TABLE(
    SPLIT_TO_TABLE(SYSTEM$GET_SERVICE_LOGS(
        'SAMOOHA_CLEANROOM_APP_SPCS_Lookalike_Demo.services.service', 0, 'lal'), '\n')
  );
```

The consumer can also see the state of their service by using the DESCRIBE SERVICE command as shown here:

Copy code

```
-- See the state of the service.
DESCRIBE SERVICE SAMOOHA_CLEANROOM_APP_SPCS_Lookalike_Demo.services.service;
```

You can list the service endpoints by running `SHOW ENDPOINTS IN SERVICE SAMOOHA_CLEANROOM_APP_clean_room_name.services.service;`.
For example:

Copy code

```
SHOW ENDPOINTS IN SERVICE SAMOOHA_CLEANROOM_APP_SPCS_Lookalike_Demo.services.service;
```

### Example code

The following notebooks and zip file demonstrate how to use Snowflake Container Services in a clean
room. You need two accounts with clean rooms installed: One for the provider and one for the consumer. They should be in the same cloud
hosting region. Use the zipped configuration files to define the service.

- [Provider notebook example](/static/samples/clean-rooms/spcs-provider.ipynb)
- [Consumer notebook example](/static/samples/clean-rooms/spcs-consumer.ipynb)
- [Service spec and configuration files](/static/samples/clean-rooms/spcs-spec-and-config.zip)
