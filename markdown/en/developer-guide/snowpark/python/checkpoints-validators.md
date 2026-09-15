# Snowpark Checkpoints library: Validators

The Snowpark Checkpoints package offers a set of validations that can be applied to the Snowpark code to ensure behavioral equivalence against the PySpark code.

## Functions provided by the framework

- check\_with\_spark: A decorator that will convert any Snowpark DataFrame arguments to a function or sample and then to PySpark DataFrames. The check will then execute a provided spark function that mirrors the functionality of the new Snowpark function and compares the outputs between the two implementations. Assuming the spark function and Snowpark functions are semantically identical, this decorator verifies those functions on real, sampled data.

  Parameters:
  :   - `job_context` (SnowparkJobContext): The job context that contains configuration and details for the validation
      - `spark_function` (fn): The equivalent PySpark function to compare against the Snowpark implementation
      - `checkpoint_name` (str): A name for the checkpoint; defaults to None
      - `sample_number` (Optional[int], optional): The number of rows for validation; defaults to 100
      - `sampling_strategy` (Optional[SamplingStrategy], optional): The strategy used for sampling data; defaults to `SamplingStrategy.RANDOM_SAMPLE`
      - `output_path` (Optional[str], optional): The path to the file where the validation results are stored; defaults to None

  Example:

  Copy code

  ```
  def original_spark_code_I_dont_understand(df):
    from pyspark.sql.functions import col, when

    ret = df.withColumn(
        "life_stage",
        when(col("byte") < 4, "child")
        .when(col("byte").between(4, 10), "teenager")
        .otherwise("adult"),
    )
    return ret

  @check_with_spark(
    job_context=job_context, spark_function=original_spark_code_I_dont_understand
  )
  def new_snowpark_code_I_do_understand(df):
    from snowflake.snowpark.functions import col, lit, when

    ref = df.with_column(
        "life_stage",
        when(col("byte") < 4, lit("child"))
        .when(col("byte").between(4, 10), lit("teenager"))
        .otherwise(lit("adult")),
    )
    return ref

  df1 = new_snowpark_code_I_do_understand(df)
  ```
- validate\_dataframe\_checkpoint: This function validates a Snowpark DataFrame against a specific checkpoint schema file or imported DataFrame according to the argument mode. It ensures that the information collected for that DataFrame and the DataFrame that is passed to the function are equivalent.

  Parameters:
  :   - `df` (SnowparkDataFrame): The DataFrame to validate
      - `checkpoint_name` (str): The name of the checkpoint to validate against
      - `job_context` (SnowparkJobContext, optional): The job context for the validation; required for DATAFRAME mode
      - `mode` (CheckpointMode): The mode of validation (for example, SCHEMA or DATAFRAME); defaults to SCHEMA
      - `custom_checks` (Optional[dict[Any, Any]], optional): Custom checks to apply during validation
      - `skip_checks` (Optional[dict[Any, Any]], optional): Checks to skip during validation
      - `sample_frac` (Optional[float], optional): Fraction of the DataFrame to sample for validation; defaults to 0.1
      - `sample_number` (Optional[int], optional): Number of rows to sample for validation
      - `sampling_strategy` (Optional[SamplingStrategy], optional): Strategy to use for sampling
      - `output_path` (Optional[str], optional): The path to the file where the validation results are stored

  Example:

  Copy code

  ```
  # Check a schema/stats here!
  validate_dataframe_checkpoint(
   df1,
   "demo_add_a_column_dataframe",
   job_context=job_context,
   mode=CheckpointMode.DATAFRAME, # CheckpointMode.Schema)
  )
  ```

  Depending on the mode selected, the validation will use either the collected schema file or a DataFrame loaded in Snowflake to verify the equivalence against the PySpark version.
- check\_output\_schema: This decorator validates the schema of a Snowpark function’s output and ensures that the output DataFrame conforms to a specified Pandera schema. It is particularly useful for enforcing data integrity and consistency in Snowpark pipelines. This decorator takes several parameters, including the Pandera schema to validate against, the checkpoint name, sampling parameters, and an optional job context. It wraps the Snowpark function and performs schema validation on the output DataFrame before returning the result.

  Example:

  Copy code

  ```
  from pandas import DataFrame as PandasDataFrame
  from pandera import DataFrameSchema, Column, Check
  from snowflake.snowpark import Session
  from snowflake.snowpark import DataFrame as SnowparkDataFrame
  from snowflake.snowpark_checkpoints.checkpoint import check_output_schema
  from numpy import int8

  # Define the Pandera schema
  out_schema = DataFrameSchema(
  {
   "COLUMN1": Column(int8, Check.between(0, 10, include_max=True, include_min=True)),
   "COLUMN2": Column(float, Check.less_than_or_equal_to(-1.2)),
   "COLUMN3": Column(float, Check.less_than(10)),
  }
  )

  # Define the Snowpark function and apply the decorator
  @check_output_schema(out_schema, "output_schema_checkpoint")
  def preprocessor(dataframe: SnowparkDataFrame):
   return dataframe.with_column(
   "COLUMN3", dataframe["COLUMN1"] + dataframe["COLUMN2"]
  )

  # Create a Snowpark session and DataFrame
  session = Session.builder.getOrCreate()
  df = PandasDataFrame(
  {
   "COLUMN1": [1, 4, 0, 10, 9],
   "COLUMN2": [-1.3, -1.4, -2.9, -10.1, -20.4],
  }
  )

  sp_dataframe = session.create_dataframe(df)

  # Apply the preprocessor function
  preprocessed_dataframe = preprocessor(sp_dataframe)
  ```
- check\_input\_schema: This decorator validates the schema of a Snowpark function’s input arguments. This decorator ensures that the input DataFrame conforms to a specified Pandera schema before the function is executed. It is particularly useful for enforcing data integrity and consistency in Snowpark pipelines. This decorator takes several parameters, including the Pandera schema to validate against, the checkpoint name, sampling parameters, and an optional job context. It wraps the Snowpark function and performs schema validation on the input DataFrame before executing the function.

  Example:

  Copy code

  ```
  from pandas import DataFrame as PandasDataFrame
  from pandera import DataFrameSchema, Column, Check
  from snowflake.snowpark import Session
  from snowflake.snowpark import DataFrame as SnowparkDataFrame
  from snowflake.snowpark_checkpoints.checkpoint import check_input_schema
  from numpy import int8

  # Define the Pandera schema
  input_schema = DataFrameSchema(
  {
   "COLUMN1": Column(int8, Check.between(0, 10, include_max=True, include_min=True)),
   "COLUMN2": Column(float, Check.less_than_or_equal_to(-1.2)),
  }
  )

  # Define the Snowpark function and apply the decorator
  @check_input_schema(input_schema, "input_schema_checkpoint")
  def process_dataframe(dataframe: SnowparkDataFrame):
    return dataframe.with_column(
        "COLUMN3", dataframe["COLUMN1"] + dataframe["COLUMN2"]
    )

  # Create a Snowpark session and DataFrame
  session = Session.builder.getOrCreate()
  df = PandasDataFrame(
  {
   "COLUMN1": [1, 4, 0, 10, 9],
   "COLUMN2": [-1.3, -1.4, -2.9, -10.1, -20.4],
  }
  )
  sp_dataframe = session.create_dataframe(df)

  # Apply the process_dataframe function
  processed_dataframe = process_dataframe(sp_dataframe)
  ```

## Statistics checks

Statistics validations are applied to the specific column type by default when the validation is run in `SCHEMA` mode; these checks can be skipped with `skip_checks`.

| Column type | Default check |
| --- | --- |
| Numeric: `byte`, `short`, `integer`, `long`, `float`, and `double` | between: Validate whether the value is between the min or the max, including the min and max.  decimal\_precision: If the value is decimal, this will check the decimal precision.  mean: Validate whether the mean of the columns falls within a specific range. |
| Boolean | isin: Validate whether the value is True or False.  True\_proportion: Validate whether the proportion of the True values falls within a specific range.  False\_proportion: Validate whether the proportion of the False values falls within a specific range. |
| Date: `date`, `timestamp`, and `timestamp_ntz` | between: Validate whether the value is between the min or the max, including the min and max. |
| Nullable: All supported types | Null\_proportion: Validate the null proportion accordingly. |

Expand

Show lessSee more

## Skip checks

With this granular control for checks, you can skip column validation or specific checks for a column. With the parameter `skip_checks`, you can specify the particular column and which validation type you want to skip. The name of the check used to skip is the one associated with the check.

- `str_contains`
- `str_endswith`
- `str_length`
- `str_matches`
- `str_startswith`
- `in_range`
- `equal_to`
- `greater_than_or_equal_to`
- `greater_than`
- `less_than_or_equal_to`
- `less_than`
- `not_equal_to`
- `notin`
- `isin`

Example:

Copy code

```
df = pd.DataFrame(
{
      "COLUMN1": [1, 4, 0, 10, 9],
      "COLUMN2": [-1.3, -1.4, -2.9, -10.1, -20.4],
}
)

schema = DataFrameSchema(
{
      "COLUMN1": Column(int8, Check.between(0, 10, element_wise=True)),
      "COLUMN2": Column(
          float,
          [
              Check.greater_than(-20.5),
              Check.less_than(-1.0),
              Check(lambda x: x < -1.2),
          ],
      ),
}
)

session = Session.builder.getOrCreate()
sp_df = session.create_dataframe(df)
check_dataframe_schema(
  sp_df,
  schema,
  skip_checks={"COLUMN1": [SKIP_ALL], "COLUMN2": ["greater_than", "less_than"]},
)
```

## Custom checks

You can add additional checks to the schema generated from the JSON file with the `custom_checks` property. This adds the check to the pandera schema.

Example:

Copy code

```
df = pd.DataFrame(
  {
        "COLUMN1": [1, 4, 0, 10, 9],
        "COLUMN2": [-1.3, -1.4, -2.9, -10.1, -20.4],
  }
)

session = Session.builder.getOrCreate()
sp_df = session.create_dataframe(df)

# Those check will be added to the schema generate from the JSON file
result = validate_dataframe_checkpoint(
  sp_df,
  "checkpoint-name",
  custom_checks={
        "COLUMN1": [
            Check(lambda x: x.shape[0] == 5),
            Check(lambda x: x.shape[1] == 2),
    ],
    "COLUMN2": [Check(lambda x: x.shape[0] == 5)],
  },
)
```

## Sampling strategies

The provided code’s sampling process is designed to efficiently validate large DataFrames by taking a representative sample of the data. This approach helps perform schema validation without the need to process the entire dataset, which can be computationally expensive and time-consuming.

Parameters:
:   - `sample_frac`: This parameter specifies the fraction of the DataFrame to sample. For example, if `sample_frac` is set to 0.1, then 10 percent of the DataFrame rows will be sampled. This is useful when you want to validate a subset of the data to save on computational resources.
    - `sample_number`: This parameter specifies the exact number of rows to sample from the DataFrame. For example, if `sample_number` is set to 100, then 100 rows will be sampled from the DataFrame. This is useful when you want to validate a fixed number of rows regardless of the DataFrame size.

## Validation result

After any type of validation is executed, the result, whether it passes or fails, is saved into `checkpoint_validation_results.json`. This file is primarily used for the functionalities of the VSCode extension. It contains information about the status of the validation, timestamp, checkpoint name, number of the line where the execution of the function occurs, and the file.

It also logs the result into the default Snowflake account in a table called *SNOWPARK\_CHECKPOINTS\_REPORT*, which contains information about the validation result.

- `DATE`: Execute timestamp of the validation
- `JOB`: Name of the SnowparkJobContext
- `STATUS`: Status of the validation
- `CHECKPOINT`: Name of the checkpoint validated
- `MESSAGE`: Error message
- `DATA`: Data from the validation execution
- `EXECUTION_MODE`: Validation mode executed
