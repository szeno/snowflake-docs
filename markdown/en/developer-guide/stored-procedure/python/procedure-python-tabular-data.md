# Returning tabular data from a Python stored procedure

You can write a procedure that returns data in tabular form. To write a procedure that returns tabular data, do the following:

- Specify `TABLE(...)` as the procedure’s return type in your [CREATE PROCEDURE](/sql-reference/sql/create-procedure) statement.

  As TABLE parameters, you can specify the returned data’s column names and [types](/sql-reference-data-types) if you know them.
  If you don’t know the returned columns when defining the procedure — such as when they’re specified at run time — you can leave out the
  TABLE parameters. When you do, the procedure’s return value columns will be converted from the columns in the `DataFrame` returned by its
  handler. Column data types will be converted to SQL according to the mapping specified in [SQL-Python Data Type Mappings](/developer-guide/udf-stored-procedure-data-type-mapping#label-sql-python-data-type-mappings).
- Write the handler so that it returns the tabular result in a Snowpark DataFrame.

  For more information about dataframes, see [Working with DataFrames in Snowpark Python](/developer-guide/snowpark/python/working-with-dataframes).

## Examples

The examples in this section illustrate returning tabular values from a procedure that filters for rows where a column matches a string.

### Defining the data

Code in the following example creates a table of employees.

Copy code

```
CREATE OR REPLACE TABLE employees(id NUMBER, name VARCHAR, role VARCHAR);
INSERT INTO employees (id, name, role) VALUES (1, 'Alice', 'op'), (2, 'Bob', 'dev'), (3, 'Cindy', 'dev');
```

### Specifying return column names and types

This example specifies column names and types in the `RETURNS TABLE()` statement.

Copy code

```
CREATE OR REPLACE PROCEDURE filterByRole(tableName VARCHAR, role VARCHAR)
RETURNS TABLE(id NUMBER, name VARCHAR, role VARCHAR)
LANGUAGE PYTHON
RUNTIME_VERSION = '3.9'
PACKAGES = ('snowflake-snowpark-python')
HANDLER = 'filter_by_role'
AS
$$
from snowflake.snowpark.functions import col

def filter_by_role(session, table_name, role):
   df = session.table(table_name)
   return df.filter(col("role") == role)
$$;
```

### Omitting return column names and types

Code in the following example declares a procedure that allows return value column names and types to be extrapolated from columns in the
handler’s return value. It omits the column names and types from the `RETURNS TABLE()` statement.

Copy code

```
CREATE OR REPLACE PROCEDURE filterByRole(tableName VARCHAR, role VARCHAR)
RETURNS TABLE()
LANGUAGE PYTHON
RUNTIME_VERSION = '3.9'
PACKAGES = ('snowflake-snowpark-python')
HANDLER = 'filter_by_role'
AS
$$
from snowflake.snowpark.functions import col

def filter_by_role(session, table_name, role):
  df = session.table(table_name)
  return df.filter(col("role") == role)
$$;
```

### Calling the procedure

The following example calls the stored procedure:

Copy code

```
CALL filterByRole('employees', 'dev');
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
