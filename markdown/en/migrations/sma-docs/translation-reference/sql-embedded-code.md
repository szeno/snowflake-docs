description:
:   Transform the SQL Code embedded in your Scala / Python Code

# Snowpark Migration Accelerator: SQL Embedded code

Note

Currently, SMA only supports the [*pyspark.sql*](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.SparkSession.sql.html) function.

SMA can transform SQL code that is embedded within Python or Scala files. It processes embedded SQL code in the following file extensions:

- Python source code files (with .py extension)
- Scala source code files (with .scala extension)
- Jupyter Notebook files (with .ipynb extension)
- Databricks source files (with .python or .scala extensions)
- Databricks Notebook archive files (with .dbc extension)

## Embedded SQL Code transformation Samples

### Supported Case

- Using the [*spark.sql*](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.SparkSession.sql.html) function in Python to execute SQL queries:

Copy code

```
# Original in Spark
spark.sql("""MERGE INTO people_target pt
USING people_source ps
ON (pt.person_id1 = ps.person_id2)
WHEN NOT MATCHED BY SOURCE THEN DELETE""")
```

Copy code

```
# SMA transformation
spark.sql("""MERGE INTO people_target pt
USING (
   SELECT
      pt.person_id1
   FROM
      people_target pt
      LEFT JOIN
         people_source ps
         ON pt.person_id1 = ps.person_id2
   WHERE
      ps.person_id2 IS NULL
) s_src
ON pt.person_id1 = s_src.person_id1
WHEN MATCHED THEN
   DELETE;""")
```

## Unsupported Cases

When SMA encounters code that it cannot convert, it generates an Error, Warning, and Issue (EWI) message in the output code. For more details about these messages, see [EWI](/migrations/sma-docs/translation-reference/sql-embedded-code).

The following scenarios are not currently supported:

- When working with SQL code, you can incorporate string variables in the following way:

Copy code

```
query = "SELECT COUNT(COUNTRIES) FROM SALES"
dfSales = spark.sql(query)
```

Copy code

```
query = "SELECT COUNT(COUNTRIES) FROM SALES"
#EWI: SPRKPY1077 => SQL embedded code cannot be processed.
dfSales = spark.sql(query)
```

- Combining strings to build SQL code using simple concatenation:

Copy code

```
base = "SELECT "
criteria_1 = " COUNT(*) "
criteria_2 = " * "
fromClause = " FROM COUNTRIES"

df1 = spark.sql(bas + criteria_1 + fromClause)
df2 = spark.sql(bas + criteria_2 + fromClause)
```

Copy code

```
base = "SELECT "
criteria_1 = " COUNT(*) "
criteria_2 = " * "
fromClause = " FROM COUNTRIES"
#EWI: SPRKPY1077 => SQL embedded code cannot be processed.

df1 = spark.sql(bas + criteria_1 + fromClause)
#EWI: SPRKPY1077 => SQL embedded code cannot be processed.
df2 = spark.sql(bas + criteria_2 + fromClause)
```

- Using string interpolation to dynamically generate SQL statements:

Copy code

```
# Old Style interpolation
UStbl = "SALES_US"
salesUS = spark.sql("SELECT * FROM %s" % (UStbl))

# Using format function
COLtbl = "COL_SALES WHERE YEAR(saleDate) > 2023"
salesCol = spark.sql("SELECT * FROM {}".format(COLtbl))

# New Style
UKTbl = " UK_SALES_JUN_18"
salesUk = spark.sql(f"SELECT * FROM {UKTbl}")
```

Copy code

```
# Old Style interpolation
UStbl = "SALES_US"
#EWI: SPRKPY1077 => SQL embedded code cannot be processed.
salesUS = spark.sql("SELECT * FROM %s" % (UStbl))

# Using format function
COLtbl = "COL_SALES WHERE YEAR(saleDate) > 2023"
#EWI: SPRKPY1077 => SQL embedded code cannot be processed.
salesCol = spark.sql("SELECT * FROM {}".format(COLtbl))

# New Style
UKTbl = " UK_SALES_JUN_18"
#EWI: SPRKPY1077 => SQL embedded code cannot be processed.
salesUk = spark.sql(f"SELECT * FROM {UKTbl}")
```

- Using functions that generate SQL queries dynamically:

Copy code

```
def ByMonth(month):
    query = f"SELECT * LOGS WHERE MONTH(access_date) = {month}"
    return spark.sql(query)
```

Copy code

```
def ByMonth(month):
query = f"SELECT * LOGS WHERE MONTH(access_date) = {month}"
    #EWI: SPRKPY1077 => SQL embedded code cannot be processed.
    return spark.sql(query)
```

## Unsupported Cases and EWI messages

- When analyzing Scala code, the error code SPRKSCL1173 indicates unsupported embedded SQL statements.

Copy code

```
/*Scala*/
 class SparkSqlExample {
    def main(spark: SparkSession) : Unit = {
    /*EWI: SPRKSCL1173 => SQL embedded code cannot be processed.*/
    spark.sql("CREATE VIEW IF EXISTS My View AS Select * From my Table WHERE date < current_date() ")
    }
```

- When Python code contains unsupported embedded SQL statements, the error code SPRKPY1077 will be displayed.

Copy code

```
# Python Output
#EWI: SPRKPY1077 => SQL embedded code cannot be processed.
b = spark.sql("CREATE VIEW IF EXISTS My View AS Select * From my Table WHERE date < current_date() ")
```
