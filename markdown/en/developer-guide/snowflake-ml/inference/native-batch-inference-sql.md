# Snowflake Native Batch Inference (SQL)

Use the Snowflake Model Registry to execute batch inference calls to your models. You can integrate these batch inference calls into your Snowflake workflows. With Snowflake Native Batch Inference, you can do the following:

- Integrate into your Snowflake SQL, Snowpark Python, Streaming, and Dynamic Tables workflows.
- Use third party tools such as dbt with the results of your inference calls

## Where to run a model?

### Selecting a Runtime Environment

You can either host a model on a Virtual Warehouse or a SPCS compute pool. Use the following information to determine where you’re hosting your model.

| Runtime | Best For… | Avoid When… |
| --- | --- | --- |
| Virtual Warehouse | • In-Database Batch Inference: Executing models as native SQL functions. • Zero-Ops Experience: Leveraging existing warehouses without managing compute pools. • Small Models: CPU-runnable models (e.g., scikit-learn, XGBoost). | • Hardware Constraints: The model requires a GPU for execution. • Memory Limits: Model size exceeds 15GB. (this limit is lower for smaller warehouse sizes). |
| Snowpark Container Services (SPCS) | • Large Models: Optimized for LLMs, deep learning models requiring high memory, or models requiring GPUs. • Custom Environments: For specific pip packages or a custom OS-level environment not found in standard warehouses. | • Organizational Policy: SPCS is not yet approved or enabled in your account. • Sufficient warehouse compute: If your warehouse can process your batch inference requests, you don’t need the additional compute from SPCS. • Government Regions: SPCS-based inference is not available in government regions. |

Expand

Show lessSee more

### To run model on warehouse

To host your model on a warehouse, specify WAREHOUSE in the target\_platforms argument to log your model. For more information, see working with dependencies and target platforms.

For information about whether an existing model is runnable in a warehouse, run SHOW VERSIONS IN MODEL. If the runnable\_in column has WAREHOUSE as a value, you can run it.

### To run model on SPCS

To use your model in SPCS, you must deploy the model as a service. For more information about deploying a model to SPCS, see deploying the model for online inference. Make sure auto-suspend is active.

Note

Model owners or users with the READ privilege on the model can deploy the model to a service.
By default, only the service owner can invoke service functions. To let another role call the
service (for SQL calls using `service_name!method_name(...)` syntax), grant the service role
`INFERENCE_SERVICE_FUNCTION_USAGE` using
[GRANT SERVICE ROLE](/sql-reference/sql/grant-service-role).

Note

If your service is suspended, it automatically resumes when there’s an inference request. However, if service fails to resume within a specified timeframe, the query might fail. Queries might fail to resume if there are a lack of available nodes in the compute pool. To mitigate this risk, you can explicitly resume the service and wait for its availability.

Use an XSMALL or SMALL warehouse to route your inference requests to the SPCS compute pool. A warehouse can run multiple threads per node and send a large number of inference requests with each request. Consequently, the service operating within SPCS can be easily overwhelmed. Therefore, the recommendation is to utilize an XSMALL or SMALL warehouse when the model is deployed to SPCS.

## Inference from Python

If you’re using the Snowflake Python API to make inference requests, you must have the snowflake-ml-python package.

### Connect to Model Registry

Retrieve the model that you’re using for inference requests from the model registry. Use the following code to retrieve the model:

Copy code

```
from snowflake.ml.registry import Registry

registry = Registry(session=session, database_name=DATABASE, schema_name=REGISTRY_SCHEMA)
mv = registry.get_model('my_model').version('my_version')  # returns ModelVersion
```

### Run batch inference job

Use the run method of your model version object to run a batch inference job. Using the run method, you can:

- Run an inference job on either a warehouse or an SPCS compute pool.
- Provide a Snowpark or pandas dataframe with the inference data.

The run method returns a dataframe that matches the type of the dataframe that you’ve specified. For example, if you specify a pandas dataframe as the input, you get a pandas dataframe as the output.

Note

Snowpark DataFrames undergo lazy evaluation. The execution only happens upon the DataFrame’s collect, show, or to\_pandas method.

The following example runs a batch inference job on a warehouse:

Copy code

```
# Run inference on a warehouse
# mv: snowflake.ml.model.ModelVersion
remote_prediction = mv.run(input_features, function_name="predict")
remote_prediction.show()
```

To run inference on SPCS instead of a warehouse, add the `service_name` argument to the `run` call:

Copy code

```
# Run inference on SPCS
# mv: snowflake.ml.model.ModelVersion
remote_prediction = mv.run(input_features, function_name="predict", service_name="example_spcs_service")
remote_prediction.show()
```

To see the methods that you can call from a model, run mv.show\_functions. The return value of this method is a list of ModelFunctionInfo objects. Each of these objects includes the following attributes:

- name: The name of the function that can be called from Python or SQL.
- target\_method: The name of the Python method in the original logged model.

Copy code

```
# Get signature of the inference function in Python
# mv: snowflake.ml.model.ModelVersion
mv.show_functions()
```

### Passing parameters during inference

If the model’s signature includes parameters defined in the
[ParamSpec](https://docs.snowflake.com/developer-guide/snowpark-ml/reference/latest/api/model/snowflake.ml.model.model_signature.ParamSpec) object, you can pass parameter values at inference time using the `params` argument. Any parameter that isn’t included in the dictionary uses its default value from
the signature. The `params` argument works the same way whether you are running inference on a warehouse or on SPCS.

Copy code

```
# Pass parameters to override default values
# mv: snowflake.ml.model.ModelVersion
remote_prediction = mv.run(
    input_features,
    function_name="predict",
    params={"temperature": 0.9, "max_tokens": 512}
)
```

## Inference from SQL

Use the following command to understand the functions available and the signature for a model version:

Copy code

```
SHOW FUNCTION IN MODEL mymodel VERSION myversion;
```

### To run model on warehouse

Use the `MODEL(model_name)!method_name(...)` syntax to call or invoke methods of a model. The methods available on a model are determined by the underlying Python model class. For example, many types of models use a method named predict for inference.

To call a method of the default model, use the following syntax. Include any method arguments within the parentheses and specify the table containing the inference data in the FROM clause.

Copy code

```
SELECT MODEL(<model_name>)!<method_name>(...) FROM <table_name>;
```

To invoke a method from a specific version of a model, create an alias to the specific version of the model and call the method through the alias.

Use the following syntax to call a method from a specific version of a model.

Copy code

```
SELECT MODEL(<model_name>,<version_or_alias_name>)!<method_name>(...) FROM <table_name>;
```

The following example uses the LAST alias to call the latest version of a model.

Copy code

```
SELECT MODEL(my_model,LAST)!predict(...) FROM my_table;
```

### Passing parameters in SQL

If the model’s signature includes parameters defined with
[ParamSpec](/developer-guide/snowflake-ml/model-registry/model-signature), you can pass parameter values as
additional arguments after the input columns. Parameters can be specified by position or by name.

When using positional arguments, parameters can be omitted from the right-hand side, and the defaults from the
signature are used:

Copy code

```
-- Pass all parameters positionally (temperature, then max_tokens)
SELECT MODEL(my_model, v1)!predict(input_text, 0.9, 512) FROM my_table;

-- Omit max_tokens from the right; its default value from the signature is used
SELECT MODEL(my_model, v1)!predict(input_text, 0.9) FROM my_table;
```

When using named arguments, all arguments (including input columns) must be specified by name. This lets you pass
only specific parameters regardless of their position:

Copy code

```
SELECT MODEL(my_model, v1)!predict(
    input_text => input_text,
    max_tokens => 512
) FROM my_table;
```

Note

You must specify all arguments by name or all by position. You cannot mix positional and named arguments in the
same call.

### To run model on SPCS

Unlike running in a warehouse, functions can be called from a service by calling `service_name!method_name(...)`.

Copy code

```
SELECT <mservice_name>!<method_name>(...) FROM <table_name>;
```

Parameters are passed the same way as with warehouse functions, either all positionally or all by name:

Copy code

```
-- Positional
SELECT my_service!predict(input_text, 0.9, 512) FROM my_table;

-- Named arguments (all arguments must be named)
SELECT my_service!predict(input_text => input_text, max_tokens => 512) FROM my_table;
```

## Continuous Model Inference with Dynamic Tables

Snowflake’s dynamic tables establish a continuous transformation layer atop streaming data. By defining a dynamic table that applies the predictions of a machine learning model to incoming data, one can sustain an automated, continuously operating model inference pipeline on the data without the requirement for manual orchestration.

Consider, for instance, a stream of login events populating a table (LOGINS\_RAW), which includes columns such as USER\_ID, LOCATION, and a timestamp. This table is subsequently updated with the model’s predictions regarding the login risk for newly-arrived events. Crucially, only new rows are processed with the model’s predictions.

### SQL

Dynamic Tables offer a robust capability for Snowflake users to perform incremental inference on incoming data. Use SQL to define a dynamic table that references the model and applies it to new incoming rows in LOGINS\_RAW:

Copy code

```
CREATE OR REPLACE DYNAMIC TABLE logins_with_predictions
    WAREHOUSE = my_wh
    TARGET_LAG = '20 minutes'
    REFRESH_MODE = INCREMENTAL
    INITIALIZE = on_create
    COMMENT = 'Dynamic table with continuously updated model predictions'
AS
SELECT
    login_id,
    user_id,
    location,
    event_time,
    MODEL(ml.registry.mymodel)!predict(l.user_id, l.location) AS prediction_result
FROM logins_raw;
```

### Snowpark Python

The Snowpark Python API allows you to access the model registry programmatically and run inference directly on DataFrames. This approach can be more flexible and maintainable, especially in code-driven environments.

Copy code

```
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col
from snowflake.ml.registry import Registry

# Initialize the registry
reg = Registry(session=sp_session, database_name="ML", schema_name="REGISTRY")

# Retrieve the default model version from the registry
model = reg.get_model("MYMODEL")

# Load the source data
df_raw = sp_session.table("LOGINS_RAW")

# Run inference on the necessary features
predictions_df = model.run(df_raw.select("USER_ID", "LOCATION"))

# Join predictions back to the source data
joined_df = df_raw.join(predictions_df, on=["USER_ID", "LOCATION"])

# Create or replace a dynamic table from the joined DataFrame
joined_df.create_or_replace_dynamic_table(
    name="LOGINS_WITH_PREDICTIONS",
    warehouse="MY_WH",
    lag='20 minutes',
    refresh_mode='INCREMENTAL',
    initialize="ON_CREATE",
    comment="Dynamic table continuously updated with model predictions"
)
```

The code sample above will run inference using MYMODEL on new data in LOGINS\_RAW every 20 minutes automatically.

### Immutable vs volatile

This incrementality is essential and necessitates that all functions invoked within the Dynamic Table definition be designated as IMMUTABLE. While functions within a standard model are typically IMMUTABLE, Custom models default to VOLATILE. If the underlying model is known to be immutable, it is crucial to ensure that the corresponding model function is explicitly marked as immutable when the model is logged.
