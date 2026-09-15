description:
:   The SMA-Checkpoints feature includes several settings, each with its corresponding default value.

# Snowpark Migration Accelerator: Default Settings

## Default Values

- On/Off the whole feature: Enabled.
- Collect user-defined methods returning DataFrame type: False.
- List of relevant PySpark functions to collect: (See table below).
- Sample: 100%.
- Mode: Schema.
- Enabled: Always True.

## **Default PySpark functions to collect**

| Type | PySpark Packages |
| --- | --- |
| Creation | pyspark.sql.session.SparkSession.createDataFrame<br>pyspark.sql.readwriter.DataFrameReader.csv<br>pyspark.sql.readwriter.DataFrameReader.jdbc<br>pyspark.sql.readwriter.DataFrameReader.json<br>pyspark.sql.readwriter.DataFrameReader.load<br>pyspark.sql.readwriter.DataFrameReader.orc<br>pyspark.sql.readwriter.DataFrameReader.parquet<br>pyspark.sql.readwriter.DataFrameReader.table<br>pyspark.sql.readwriter.DataFrameReader.text<br>pyspark.rdd.RDD.toDF |
| Transformation | pyspark.sql.dataframe.DataFrame.union<br>pyspark.sql.dataframe.DataFrame.intersect<br>pyspark.sql.dataframe.DataFrame.join<br>pyspark.sql.group.GroupedData.pivot |

Expand

Show lessSee more
