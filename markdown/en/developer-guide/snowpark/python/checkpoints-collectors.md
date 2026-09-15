# Snowpark Checkpoints library: Collectors

The `snowpark-checkpoints-collectors` package offers a function for extracting information from the PySpark DataFrames. You can then use that data to validate against the converted Snowpark DataFrames to ensure behavioral equivalence.

- To insert a new checkpoint collection point, use the following function:

  **Function signature:**

  Copy code

  ```
  def collect_dataframe_checkpoint(df: SparkDataFrame,
    checkpoint_name: str,
    sample: Optional[float],
    mode: Optional[CheckpointMode],
    output_path: Optional[str]) -> None:
  ```

  **Function parameters:**

  - **df:** The PySpark DataFrame
  - **checkpoint\_name:** The name of the checkpoint

    Starts with a letter (A-Z, a-z) or an underscore (\_) and contains only letters, underscores, and numbers (0-9).
  - **sample:** (Optional) The sample size

    The default value is 1.0 (entire PySpark DataFrame) in a range from 0 to 1.0.
  - **mode:** (Optional) The execution mode

    The options are `SCHEMA` (default) and `DATAFRAME`.
  - **output\_path:** (Optional) The path to the file where the checkpoint is saved

    The default value is the current working directory.

The collection process generates a JSON output file, called `checkpoint_collection_result.json`, that contains the following information about the result for each collection point:

- A timestamp for when the collection point started
- The relative path of the file where the collection point is
- The line of code of the file where the collection point is
- The name of the collection point checkpoint
- The result of the collection point (fail or pass)

## Schema inference collected data mode (Schema)

This is the default mode, which leverages Pandera schema inference to obtain the metadata and checks that will be evaluated for the specified DataFrame. This mode also collects custom data from columns of the DataFrame based on the PySpark type.

The column data and checks are collected based on the PySpark type of the column (see the following tables). For any column, no matter its type, the custom data collected includes the name of the column, the type of the column, nullable, the count of rows, the count of not null rows, and the count of null rows.

**Custom data is collected based on the PySpark type of the column**

| Column type | Custom data collected |
| --- | --- |
| Numeric (`byte`, `short`, `integer`, `long`, `float` and `double`) | Minimum value; maximum value; mean value; decimal precision (in case of integer type, the value is zero); standard deviation |
| Date | Minimum value; maximum value; date format (*%Y-%m-%d*) |
| DayTimeIntervalType and YearMonthIntervalType | Minimum value; maximum value |
| Timestamp | Minimum value; maximum value; date format (*%Y-%m-%dH:%M:%S*) |
| Timestamp ntz | Minimum value; maximum value; date format (*%Y-%m-%dT%H:%M:%S%z*) |
| String | Minimum length value; maximum length value |
| Char | PySpark handles any literal as a string type; therefore, *char* is not a valid type. |
| Varchar | PySpark handles any literal as a string type; therefore, *Varchar* is not a valid type. |
| Decimal | Minimum value; maximum value; mean value; decimal precision |
| Array | Type of the value; if allowed, null as an element; proportion of null values; maximum array size; minimum array size; mean size of arrays; whether all arrays have the same size |
| Binary | Maximum size; minimum size; mean size; whether all elements have the same size |
| Map | Type of the key; type of the value; if allowed, null as a value; proportion of null values; maximum map size; minimum map size; mean map size; whether all maps have the same size |
| Null | NullType represents None because the type data cannot be determined; therefore, it is not possible to get information from this type. |
| Struct | The metadata of the struct for each structField: `name`, `type`, `nullable`, `rows count`, `rows not null count` and `rows null count`. It is an array. |

Expand

Show lessSee more

It also defines a set of predefined validation checks for each data type detailed in the following table:

**Checks are collected based on the type of the column**

| Type | Pandera checks | Additional checks |
| --- | --- | --- |
| Boolean | Each value is True or False. | The count of True and False values |
| Numeric (`byte`, `short`, `integer`, `long`, `float` and `double`) | Each value is in the range of min value and max value. | Decimal precision; mean value; standard deviation |
| Date | N/A | Minimum and maximum values |
| Timestamp | Each value is in the range of min value and max value. | The format of the value |
| Timestamp ntz | Each value is in the range of min value and max value. | The format of the value |
| String | Each value length is in the range of min and max length. | None |
| Char | PySpark handles any literal as a string type; therefore, `char` is not a valid type. |  |
| Varchar | PySpark handles any literal as a string type; therefore, `Varchar` is not a valid type. |  |
| Decimal | N/A | N/A |
| Array | N/A | None |
| Binary | N/A | None |
| Map | N/A | None |
| Null | N/A | N/A |
| Struct | N/A | None |

Expand

Show lessSee more

This mode allows the user to define a sample of a DataFrame to collect, but it is optional. By default, the collection works with the entire DataFrame. The size of the sample must represent the population statistically.

Pandera can only infer the schema of a pandas DataFrame, which implies that the PySpark DataFrame must be converted into a pandas DataFrame, which can affect the columns’ type resolutions. In particular, pandera infers the following PySpark types as object types: `string`, `array`, `map`, `null`, `struct`, and `binary`.

The output of this mode is a JSON file for each collected DataFrame, and the name of the file is the same as the checkpoint. This file contains information related to the schema and has two sections:

- The **Pandera schema** section contains the data inferred by pandera such as name, type (pandas), whether the column allows null values, and other information for each column, and checks whether the column is based on the PySpark type. It is a `DataFrameSchema` object of pandera.
- The **custom data** section is an array of the custom data collected by each column based on the PySpark type.

Note

The collection package might have memory issues when processing large PySpark DataFrames. To work with a subset of the data instead of the entire PySpark DataFrame, you can set the sample parameter in the collection function to a value between 0.0 and 1.0.

## DataFrame collected data mode (DataFrame)

This mode collects the data of the PySpark DataFrame. In this case, the mechanism saves all data of the given DataFrame in parquet format. Using the default user Snowflake connection, it tries to upload the parquet files into the Snowflake temporal stage and create a table based on the information in the stage. The name of the file and the table are the same as the checkpoint.

The output of this mode is a parquet file result of the DataFrame saved and a table with the DataFrame data in the default Snowflake configuration connection.
