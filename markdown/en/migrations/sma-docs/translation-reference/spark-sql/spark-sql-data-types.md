description:
:   Some data type similarity between Snowflake and Snowpark

# Snowpark Migration Accelerator: Spark SQL Data Types

## Conversion Table

| Spark SQL | Snowflake | Notes |
| --- | --- | --- |
| `BIGINT` | `BIGINT` |  |
| `BOOLEAN` | `BOOLEAN` |  |
| `BYTE` | `BYTEINT` |  |
| `CHAR` | `CHAR` |  |
| `DATE` | `DATE` |  |
| `DECIMAL` | `DECIMAL` |  |
| `DOUBLE` | `DOUBLE` |  |
| `FLOAT` | `FLOAT` |  |
| `INTEGER` | `INTEGER` |  |
| `LONG` | `INT` | Check out [note](/migrations/sma-docs/translation-reference/spark-sql/spark-sql-data-types) |
| `SHORT` | `INT` | Check out [note](/migrations/sma-docs/translation-reference/spark-sql/spark-sql-data-types) |
| `STRING` | `STRING` |  |
| `TIMESTAMP` | `TIMESTAMP_TZ` |  |
| `TIMESTAMPNTZ` | `TIMESTAMP_NTZ` |  |
| `VARCHAR` | `VARCHAR` |  |

Expand

Show lessSee more

## Notes

Note

For more information, refer to the Spark SQL [data types](https://spark.apache.org/docs/latest/sql-ref-datatypes.html#data-types) documentation.

### Integer types

When converting integer data types from the source system, both `LONG` and `SHORT` are mapped to Snowflake’s `INT` data type, as `INTEGER` can accommodate the full range of values for both data types.

- SparkSQL LONG: Range from -9,223,372,036,854,775,808 to 9,223,372,036,854,775,807
- SparkSQL SHORT: Range from -32,768 to 32,767
- Snowflake INTEGER: Range from -9.9999999999999999999999999999999999999 x 10^38 to +9.9999999999999999999999999999999999999 x 10^38
