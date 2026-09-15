description:
:   The destination is Snowflake and the source is…

# Snowpark Migration Accelerator: Supported Platforms

## Supported Platforms

The Snowpark Migration Accelerator (SMA) currently supports the following programming languages as source code:

- Python
- Scala
- SQL

The SMA analyzes both code files and notebook files to identify any usage of Spark API and other third-party APIs. For a complete list of file types that SMA can analyze, please refer to [Supported Filetypes](/migrations/sma-docs/user-guide/before-using-the-sma/supported-filetypes).

### SQL Dialects

The Snowpark Migration Accelerator (SMA) can analyze code files to identify SQL elements. Currently, SMA can detect SQL code written in the following formats:

- Spark SQL
- Hive QL
- Databricks SQL

### SQL Assessment and Conversion Guidelines

While Spark SQL and Snowflake SQL are highly compatible, some SQL code may not convert perfectly.

SQL analysis is only possible when the SQL is received in the following ways:

- A SQL cell within a supported notebook file
- A .sql or .hql file
- A complete string passed to a `spark.sql` statement.

  Some variable substitutions are not supported. Here are a few examples:

  - Parsed:

    Copy code

    ```
    spark.sql("select * from TableA")
    ```

    New SMA scenarios supported include the following:

    Copy code

    ```
    # explicit concatenation
    spark.sql("select * from TableA" + ' where col1 = 1')

    # implicit concatenation (juxtaposition)
    spark.sql("select * from TableA" ' where col1 = 1')

    # var initialized with sql in previous lines before execution on same scope
    sql = "select * from TableA"
    spark.sql(sql)

    # f-string interpolation:
    spark.sql(f"select * from {varTableA}")

    # format kindof interpolation
    spark.sql("select * from {}".format(varTableA))

    # mix var with concat and f-string interpolation
    sql = f"select * from {varTableA} " + f'where {varCol1} = 1'
    spark.sql(sql)
    ```
  - Not Parsed:

    Copy code

    ```
    some_variable = "TableA"
    spark.sql("select * from" + some_variable)
    ```

  SQL elements are accounted for in the object inventories, and a readiness score is generated specifically for SQL.
