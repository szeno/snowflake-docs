# Troubleshooting Python UDFs

This topic provides troubleshooting information about Python UDFs (user-defined functions).

## Troubleshooting

### Problem: A required Python library is not available through Anaconda

Third-party Python libraries, which do not have C/C++ extensions, can be imported by UDFs directly via Snowflake stages.
For more information, see [Creating a Python UDF with code uploaded from a stage](/developer-guide/udf/python/udf-python-creating#label-udf-python-stage).

To learn how to submit a request to support additional Anaconda packages, see [Using third-party packages](/developer-guide/udf/python/udf-python-packages).

### Problem: A UDF fails with the error “function available memory exhausted”

Reduce the amount of memory used by the UDF.

Check the UDF code for bugs or memory leaks.

For more information, see [Memory](/developer-guide/udf/python/udf-python-designing#label-udf-python-limitations).

### Problem: I want to extract ZIP or other archives inside a UDF

To see an example of how to upload a ZIP file to a Snowflake stage and then unzip it into the `/tmp` directory
inside the UDF, see [Unzipping a staged file](/developer-guide/udf/python/udf-python-examples#label-udf-python-unzipping-file-from-stage).

### Problem: UDF performance is slow

For information about how to improve the performance of UDFs, see [Optimizing for scale and performance](/developer-guide/udf/python/udf-python-designing#label-udf-python-scale-performance-considerations).

### Problem: The ORGADMIN role is not enabled so Anaconda packages cannot be used

When going through the steps to [get started using third-party packages from Anaconda](/developer-guide/udf/python/udf-python-packages#label-python-udfs-anaconda-terms),
the organization administrator (ORGADMIN) role is required.

To resolve this problem, follow the instructions in [Enabling the ORGADMIN role in an account](/user-guide/organization-administrators#label-enabling-orgadmin-role-for-account).

### Problem: A UDF fails with the error “UnicodeDecodeError” when reading a file

When you use the `SnowflakeFile` class to read files that contain non-text data, you must specify the input mode as binary.
Otherwise you might encounter the following error:

Copy code

```
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xf7 in position 12: invalid start byte
```

To resolve this problem, specify the input mode as binary by passing `'rb'` for the `mode` argument (the second argument). For example:

Copy code

```
with SnowflakeFile.open(file_name, 'rb') as f:
```

### Tips

Training machine learning (ML) models can sometimes be very resource intensive.
Snowpark-optimized warehouses are a type of Snowflake virtual warehouse that can be used for workloads
that require a large amount of memory and compute resources.
For information on machine learning models and Snowpark Python, see [Training Machine Learning Models with Snowpark Python](/developer-guide/snowpark/python/python-snowpark-training-ml).

If using a Python UDF in a [masking policy](/sql-reference/sql/create-masking-policy), ensure the data type of the column, UDF, and
masking policy match.

For troubleshooting information about third-party packages, see [Known issues with third-party packages](/developer-guide/udf/python/udf-python-packages#label-python-udfs-known-issues-third-party).
