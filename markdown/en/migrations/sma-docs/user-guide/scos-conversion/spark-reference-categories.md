description:
:   Categories of references to the Spark API

# Snowpark Migration Accelerator: Spark Reference Categories

SnowConvert for Spark categorizes Spark elements based on how they can be mapped to Snowpark. The following categories describe how each Spark reference is translated, including:

- Whether SnowConvert can automatically convert it
- Whether it’s possible to implement in Snowpark

Also it provides

- Examples of the translation
- Description of the mapping process

The sections below explain each status type and provide examples.

## Direct

Direct translation means the function works exactly the same way in both PySpark and Snowpark, requiring no modifications to the code.

- Snowpark Support: Available
- Tool Support: Available
- Spark Example:

Copy code

```
col("col1")
```

- Snowpark Example:

Copy code

```
col("col1")
```

## Rename

The PySpark function has an equivalent in Snowpark, but you need to use a different function name.

- Snowpark Support: Available
- Tool Support: Available
- Spark Example:

Copy code

```
orderBy("date")
```

- Snowpark Example:

Copy code

```
sort("date")
```

## Helper

Note

Starting from Spark Conversion Core V2.40.0, the Python extensions library is no longer supported. Python Spark elements will not be classified as extensions from this version onward. However, helper classes in the Snowpark extensions library will continue to be available for Spark Scala.

To address the difference between Spark and Snowpark functionality, you can create a helper function in an extension file. This helper function will have the same signature as the original Spark function and can be called from any file where needed. The extension library will contain this function to resolve the compatibility issue.

For more information about the Snowpark extensions library, visit our GitHub repository at <https://github.com/Snowflake-Labs/snowpark-extensions>.

Examples include fixed additional parameters and changes to parameter order.

- Snowpark Support: Available
- Tool Support: Available
- Spark Example:

Copy code

```
instr(str, substr)
```

- Snowpark Example:

Copy code

```
# creating a helper function named instr with an
# identical signature as the pyspark function, like:

def instr(source: str, substr: str) -> str:
    """
    Returns the position of a substring within a source string.
    Similar to the CHARINDEX function in SQL.

    Args:
        source: The string to search in
        substr: The string to search for

    Returns:
        The position where the substring is found, or 0 if not found
    """
    return charindex(substr, str)
```

## Transformation

The function is rebuilt in Snowpark to achieve the same results as the original, though it may look different. The new version might use multiple functions or additional code lines to accomplish the same task.

- Snowpark Support: Yes
- Tool Support: Yes
- Spark Example:

Copy code

```
col1 = col("col1")
col2 = col("col2")
col1.contains(col2)
```

- Snowpark Example:

Copy code

```
col1 = col("col1")
col2 = col("col2")
from snowflake.snowpark.functions as f
f.contains(col1, col2)
```

## WorkAround

This category applies when SMA cannot automatically convert a PySpark element, but there is a documented manual solution available in the tool’s documentation to help you complete the conversion.

- Snowpark Support: Available
- Tool Support: Not Available
- Spark Example:

Copy code

```
instr(str, substr)
```

- Snowpark Example:

Copy code

```
#EWI: SPRKPY#### => pyspark function has a workaround, see documentation for more info
charindex(substr, str)
```

## NotSupported

This category applies when a PySpark element cannot be converted because there is no matching equivalent in Snowflake.

- Snowpark Support: Not Available
- Tool Support: Not Available
- Spark Example:

Copy code

```
df:DataFrame = spark.createDataFrame(rowData, columns)
df.alias("d")
```

- Snowpark Example:

Copy code

```
df:DataFrame = spark.createDataFrame(rowData, columns)
# EWI: SPRKPY11XX => DataFrame.alias is not supported
# df.alias("d")
```

## NotDefined

This error occurs when the tool identifies a PySpark element but cannot convert it because the element is not included in the tool’s supported conversion database.

- Snowpark Support: Not Available
- Tool Support: Not Available
- Spark Example: Not Applicable
- Snowpark Example: Not Applicable

The assessment results will classify all detected Spark API references into the following categories.
