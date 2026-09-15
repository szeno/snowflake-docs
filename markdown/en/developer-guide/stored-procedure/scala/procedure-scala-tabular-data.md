# Returning tabular with Scala in stored procedures created with SQL

You can write a procedure that returns data in tabular form. To write a procedure that returns tabular data, do the following:

- Specify `TABLE(...)` as the procedure’s return type in your [CREATE PROCEDURE](/sql-reference/sql/create-procedure) statement.

  As TABLE parameters, you can specify the returned data’s column names and [types](/sql-reference-data-types) if you know them.
  If you don’t know the returned columns when defining the procedure—such as when they’re specified at run time—you can leave out the
  TABLE parameters. When you do, the procedure’s return value columns are converted from the columns in the dataframe returned by its
  handler. Column data types are converted to SQL according to the mapping specified in [SQL-Scala Data Type Mappings](/developer-guide/udf-stored-procedure-data-type-mapping#label-sql-types-to-scala-types).
- Write the handler so that it returns the tabular result in a Snowpark dataframe.

  For more information about dataframes, see [Working with DataFrames in Snowpark Scala](/developer-guide/snowpark/scala/working-with-dataframes).

Note

A procedure generates an error at runtime if either of the following is true:

- It declares TABLE as its return type, but its handler does not return a dataframe.
- Its handler returns a dataframe, but the procedure doesn’t declare TABLE as its return type.

## Example

The examples in this section illustrate returning tabular values from a procedure that filters for rows where a column matches a string.

### Defining the data

Code in the following example creates a table of employees.

Copy code

```
CREATE OR REPLACE TABLE employees(id NUMBER, name VARCHAR, role VARCHAR);
INSERT INTO employees (id, name, role) VALUES (1, 'Alice', 'op'), (2, 'Bob', 'dev'), (3, 'Cindy', 'dev');
```

### Declaring a procedure to filter rows

Code in the following two examples create a stored procedure that takes the table name and role as arguments, returning the rows in the table
whose role column value matches the role specified as an argument.

#### Specifying return column names and types

This example specifies column names and types in the `RETURNS TABLE()` statement.

Scala 2.12Scala 2.13

Copy code

```
CREATE OR REPLACE PROCEDURE filter_by_role(table_name VARCHAR, role VARCHAR)
  RETURNS TABLE(id NUMBER, name VARCHAR, role VARCHAR)
  LANGUAGE SCALA
  RUNTIME_VERSION = 2.12
  PACKAGES = ('com.snowflake:snowpark_2.12:latest')
  HANDLER = 'Filter.filterByRole'
  AS
  $$
  import com.snowflake.snowpark.functions._
  import com.snowflake.snowpark._

  object Filter {
    def filterByRole(session: Session, tableName: String, role: String): DataFrame = {
      val table = session.table(tableName)
      val filteredRows = table.filter(col("role") === role)
      return filteredRows
    }
  }
$$;
```

Copy code

```
CREATE OR REPLACE PROCEDURE filter_by_role(table_name VARCHAR, role VARCHAR)
  RETURNS TABLE(id NUMBER, name VARCHAR, role VARCHAR)
  LANGUAGE SCALA
  RUNTIME_VERSION = 2.13
  PACKAGES = ('com.snowflake:snowpark_2.13:latest')
  HANDLER = 'Filter.filterByRole'
  AS
  $$
  import com.snowflake.snowpark.functions._
  import com.snowflake.snowpark._

  object Filter {
    def filterByRole(session: Session, tableName: String, role: String): DataFrame = {
      val table = session.table(tableName)
      val filteredRows = table.filter(col("role") === role)
      return filteredRows
    }
  }
$$;
```

Note

Currently, in the `RETURNS TABLE(...)` clause, you can’t specify GEOGRAPHY as a column type. This
applies whether you are creating a stored or anonymous procedure.

Copy code

```
CREATE OR REPLACE PROCEDURE test_return_geography_table_1()
  RETURNS TABLE(g GEOGRAPHY)
  ...
```

Copy code

```
WITH test_return_geography_table_1() AS PROCEDURE
  RETURNS TABLE(g GEOGRAPHY)
  ...
CALL test_return_geography_table_1();
```

If you attempt to specify GEOGRAPHY as a column type, calling the stored procedure results in the error:

Copy code

```
Stored procedure execution error: data type of returned table does not match expected returned table type
```

To work around this issue, you can omit the column arguments and types in `RETURNS TABLE()`.

Copy code

```
CREATE OR REPLACE PROCEDURE test_return_geography_table_1()
  RETURNS TABLE()
  ...
```

Copy code

```
WITH test_return_geography_table_1() AS PROCEDURE
  RETURNS TABLE()
  ...
CALL test_return_geography_table_1();
```

#### Omitting return column names and types

Code in the following example declares a procedure that allows return value column names and types to be extrapolated from columns in the
handler’s return value. It omits the column names and types from the `RETURNS TABLE()` statement.

Scala 2.12Scala 2.13

Copy code

```
CREATE OR REPLACE PROCEDURE filter_by_role(table_name VARCHAR, role VARCHAR)
  RETURNS TABLE()
  LANGUAGE SCALA
  RUNTIME_VERSION = 2.12
  PACKAGES = ('com.snowflake:snowpark_2.12:latest')
  HANDLER = 'Filter.filterByRole'
  AS
  $$
  import com.snowflake.snowpark.functions._
  import com.snowflake.snowpark._

  object Filter {
    def filterByRole(session: Session, tableName: String, role: String): DataFrame = {
      val table = session.table(tableName)
      val filteredRows = table.filter(col("role") === role)
      return filteredRows
    }
  }
  $$;
```

Copy code

```
CREATE OR REPLACE PROCEDURE filter_by_role(table_name VARCHAR, role VARCHAR)
  RETURNS TABLE()
  LANGUAGE SCALA
  RUNTIME_VERSION = 2.13
  PACKAGES = ('com.snowflake:snowpark_2.13:latest')
  HANDLER = 'Filter.filterByRole'
  AS
  $$
  import com.snowflake.snowpark.functions._
  import com.snowflake.snowpark._

  object Filter {
    def filterByRole(session: Session, tableName: String, role: String): DataFrame = {
      val table = session.table(tableName)
      val filteredRows = table.filter(col("role") === role)
      return filteredRows
    }
  }
  $$;
```

### Calling the procedure

The following example calls the stored procedure:

Copy code

```
CALL filter_by_role('employees', 'dev');
```

The procedure call produces the following output:

```
+----+-------+------+
| ID | NAME  | ROLE |
+----+-------+------+
| 2  | Bob   | dev  |
| 3  | Cindy | dev  |
+----+-------+------+
```
