# Python and Java support for serverless tasks

[Serverless tasks](/user-guide/tasks-intro#label-tasks-compute-resources-serverless) can invoke the following object types and functions: user-defined functions (UDFs) and stored procedures written in Python, Java, and Scala.

You can use Python or Java in your tasks in a few different ways. To understand the difference between these options, see
[Choosing whether to write a stored procedure or a user-defined function](/developer-guide/stored-procedures-vs-udfs).

## User-defined functions

You can create UDFs to call in your task’s AS clause. You can use UDFs to perform operations not available in SQL. For more information
about UDFs, see [User-defined functions overview](/developer-guide/udf/udf-overview).

The following examples in Python and Java create a function that adds one to the input value.

Java

Copy code

```
CREATE OR REPLACE FUNCTION add_one(i int)
  RETURNS int
  LANGUAGE java
  CALLED ON NULL INPUT
  HANDLER = 'TestFunc.addOne'
  TARGET_PATH = '@~/testfunc.jar'
  AS
    'class TestFunc {
      public static int addOne(int i) {
        return i+1;
      }
    }';
```

The following examples create `my_task2` that adds one to the return value of `my_task1`.

Java

Copy code

```
CREATE OR REPLACE TASK IF NOT EXISTS my_task2
  AFTER my_task1
  AS
    SELECT add_one(SYSTEM$GET_PREDECESSOR_RETURN_VALUE());
```

## Stored procedures

You can create stored procedures to call in your task’s AS clause. Stored procedures generally perform administrative operations by
executing SQL statements. For more information about stored procedures, see
[Stored procedures overview](/developer-guide/stored-procedure/stored-procedures-overview).

The following examples in Python and Java accept a table name and role name to return a filtered table with rows that match the specified
role.

Java

Copy code

```
CREATE OR REPLACE PROCEDURE filter_by_role(table_name VARCHAR, role VARCHAR)
  RETURNS TABLE()
  LANGUAGE JAVA
  RUNTIME_VERSION = '11'
  PACKAGES = ('com.snowflake:snowpark:latest')
  HANDLER = 'FilterClass.filterByRole'
  AS
    $$
    import com.snowflake.snowpark_java.*;

    public class FilterClass {
      public DataFrame filterByRole(Session session, String tableName, String role) {
        DataFrame table = session.table(tableName);
        DataFrame filteredRows = table.filter(Functions.col("role").equal_to(Functions.lit(role)));
        return filteredRows;
      }
    }
    $$;
```

The following examples create `task2` that calls the stored procedure with the table returned from task1 and the role of `dev`.

Java

Copy code

```
CREATE OR REPLACE TASK IF NOT EXISTS my_task2
  AFTER my_task1
  AS
    CALL filter_by_role(SYSTEM$GET_PREDECESSOR_RETURN_VALUE(), 'dev');
```

## SQL AS clause

You can also define Python or Java code directly in the AS clause of your task definition.

The following example uses Python to set the return value of `task2` to a string.

Copy code

```
CREATE OR REPLACE TASK IF NOT EXISTS task2
  SCHEDULE = '1 minute'
  AS
    $$
    print(Task completed successfully.)
    $$
  ;
```
