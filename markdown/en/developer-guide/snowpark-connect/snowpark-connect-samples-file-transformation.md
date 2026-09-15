# Samples: File transformation with Snowpark Connect for Spark

This page shows how to use a Python UDF to transform files stored on a Snowflake stage. The UDF
reads a file from the stage, applies a transformation, and writes the result to a new file. You
then copy the converted files back to the stage using `COPY FILES`.

This pattern is useful for workloads such as:

- Converting between file formats.
- Resizing images.
- Transforming files into a “golden state” in a timestamped folder.

The example assumes you’ve completed the
[local IDE setup](/developer-guide/snowpark-connect/snowpark-connect-local-ide) and have a
`~/.snowflake/connections.toml` entry configured.

## Example: Transform a staged file with a UDF

This example defines a UDF that reads a text file from a stage, appends `foo` to the end of each
line, and writes the result to a new file. The converted file is then copied back to the stage
using `SnowflakeSession` to run a `COPY FILES` command.

The UDF uses [`SnowflakeFile`](/developer-guide/udf/python/udf-python-examples#label-reading-file-from-python-udf-snowflakefile)
from the `snowflake-snowpark-python` package, which provides read and write access to files on
Snowflake stages from within UDF handlers.

Important

You must mark the UDF as nondeterministic with `.asNondeterministic()`. Calling
`SnowflakeFile.open_new_result()` requires the function to be mutable (volatile). Snowflake
only allows mutable file operations inside nondeterministic UDFs.

Copy code

```
from pyspark.sql.connect.functions import udf, lit
from pyspark.sql.types import StringType
from snowflake.snowpark_connect.snowflake_session import SnowflakeSession

qualified_stage = "<stage-name>"
file_name = "<filename-to-be-converted>"

# Add snowflake-snowpark-python to UDF dependencies for SnowflakeFile access
spark.conf.set("snowpark.connect.udf.packages", "[snowflake-snowpark-python]")

# Define the file transformation UDF
def convert_file(filename):
    from snowflake.snowpark.files import SnowflakeFile

    # Read the original file
    input_file = SnowflakeFile.open(filename, "r", require_scoped_url=False)

    # Create a new result file for the converted output
    converted_file = SnowflakeFile.open_new_result("w")

    for line in input_file.readlines():
        converted_file.write(line[:-1] + 'foo' + '\n')
    return converted_file

# Mark as nondeterministic (required for file transformation UDFs)
convert_file = udf(convert_file, StringType()).asNondeterministic()

# Create a DataFrame with the file path and run the UDF
filenames_df = spark.createDataFrame([f'@{qualified_stage}/{file_name}'], ["filename"])
result = filenames_df.select(
    convert_file('filename').alias('converted_name'),
    lit(file_name).alias("original_name")
).collect()

# Copy converted files back to the stage
snowflake_session = SnowflakeSession(spark)
values = [f"('{row[0]}','{row[1]}')" for row in result]

snowflake_session.sql(
    f"COPY FILES INTO @{qualified_stage} FROM (SELECT * FROM VALUES {','.join(values)})"
).collect()
```

### How it works

1. **Configure packages**: The `snowpark.connect.udf.packages` setting makes the
   `snowflake-snowpark-python` package available inside the UDF execution environment on Snowflake.
   This provides access to the `SnowflakeFile` class.
2. **Define the UDF**: The `convert_file` function opens the input file using `SnowflakeFile.open()`
   and creates a new output file with `SnowflakeFile.open_new_result()`. After processing, the
   function returns the result file, which produces a scoped URL pointing to the converted file.
3. **Mark as nondeterministic**: `SnowflakeFile.open_new_result()` requires the function to be
   mutable (volatile). Snowflake only allows mutable file operations inside nondeterministic
   UDFs, so you must call `.asNondeterministic()` on the UDF.
4. **Run the UDF**: A DataFrame containing the stage file path is passed through the UDF. The
   result contains the scoped URL of the converted file alongside the original filename.
5. **Copy results to stage**: `SnowflakeSession` provides access to the underlying Snowflake
   session so you can run SQL commands. The `COPY FILES` statement copies the converted files
   from their temporary location to your target stage.

Note

The scoped URL returned by the UDF is valid for 24 hours. Run the `COPY FILES` statement
within that window to persist the converted files.

## Related topics

- [File transformation with Snowpark Python UDFs](/developer-guide/snowpark/python/creating-udfs#file-transformation)
  for the equivalent pure Snowpark Python approach.
- [`SnowflakeFile` class reference](/developer-guide/udf/python/udf-python-examples#label-reading-file-from-python-udf-snowflakefile)
  for details on reading and writing files from UDF handlers.
- [User-defined functions with Snowpark Connect for Spark](/developer-guide/snowpark-connect/snowpark-connect-udfs) for
  UDF configuration options, package management, and best practices.
- [File I/O with Snowpark Connect for Spark](/developer-guide/snowpark-connect/snowpark-connect-file-io) for reading
  and writing files on stages.
