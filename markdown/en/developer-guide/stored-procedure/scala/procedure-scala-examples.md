# Scala examples for stored procedures created with SQL

## Using Snowpark APIs for asynchronous processing

The following examples illustrate how you can use Snowpark APIs to begin asynchronous child jobs, as well as how those jobs behave under
different conditions.

In the following example, the `asyncWait` procedure executes an asynchronous child job that waits 10 seconds.

Scala 2.12Scala 2.13

Copy code

```
CREATE OR REPLACE PROCEDURE asyncWait()
  RETURNS VARCHAR
  LANGUAGE SCALA
  RUNTIME_VERSION = 2.12
  PACKAGES = ('com.snowflake:snowpark_2.12:latest')
  HANDLER = 'TestScalaSP.asyncBasic'
  AS
  $$
  import com.snowflake.snowpark._
  object TestScalaSP {
    def asyncBasic(session: com.snowflake.snowpark.Session): String = {
      val df = session.sql("select system$wait(10)")
      val asyncJob = df.async.collect()
      while(!asyncJob.isDone()) {
        Thread.sleep(1000)
      }
      "Done"
    }
  }
  $$;
```

Copy code

```
CREATE OR REPLACE PROCEDURE asyncWait()
  RETURNS VARCHAR
  LANGUAGE SCALA
  RUNTIME_VERSION = 2.13
  PACKAGES = ('com.snowflake:snowpark_2.13:latest')
  HANDLER = 'TestScalaSP.asyncBasic'
  AS
  $$
  import com.snowflake.snowpark._
  object TestScalaSP {
    def asyncBasic(session: com.snowflake.snowpark.Session): String = {
      val df = session.sql("select system$wait(10)")
      val asyncJob = df.async.collect()
      while(!asyncJob.isDone()) {
        Thread.sleep(1000)
      }
      "Done"
    }
  }
  $$;
```

Copy code

```
CALL asyncWait();
```

In the following example, the `cancelJob` procedure uses SQL to start a job that would take 10 seconds to finish. It then cancels
the child job before it finishes.

Scala 2.12Scala 2.13

Copy code

```
CREATE OR REPLACE PROCEDURE cancelJob()
  RETURNS VARCHAR
  LANGUAGE SCALA
  RUNTIME_VERSION = 2.12
  PACKAGES = ('com.snowflake:snowpark_2.12:latest')
  HANDLER = 'TestScalaSP.asyncBasic'
  AS
  $$
  import com.snowflake.snowpark._
  object TestScalaSP {
    def asyncBasic(session: com.snowflake.snowpark.Session): String = {
      val df = session.sql("select system$wait(10)")
      val asyncJob = df.async.collect()
      asyncJob.cancel()
      "Done"
    }
  }
  $$;
```

Copy code

```
CREATE OR REPLACE PROCEDURE cancelJob()
  RETURNS VARCHAR
  LANGUAGE SCALA
  RUNTIME_VERSION = 2.13
  PACKAGES = ('com.snowflake:snowpark_2.13:latest')
  HANDLER = 'TestScalaSP.asyncBasic'
  AS
  $$
  import com.snowflake.snowpark._
  object TestScalaSP {
    def asyncBasic(session: com.snowflake.snowpark.Session): String = {
      val df = session.sql("select system$wait(10)")
      val asyncJob = df.async.collect()
      asyncJob.cancel()
      "Done"
    }
  }
  $$;
```

In the following example, the `checkStatus` procedure executes an asynchronous child job that waits 10 seconds. The procedure then
checks on the status of the job before it finishes, so the check returns `False`.

Scala 2.12Scala 2.13

Copy code

```
CREATE OR REPLACE PROCEDURE checkStatus()
  RETURNS VARCHAR
  LANGUAGE SCALA
  RUNTIME_VERSION = 2.12
  PACKAGES = ('com.snowflake:snowpark_2.12:latest')
  HANDLER = 'TestScalaSP.asyncBasic'
  AS
  $$
  import java.sql.ResultSet
  import net.snowflake.client.jdbc.{SnowflakeConnectionV1, SnowflakeResultSet, SnowflakeStatement}
  object TestScalaSP {
    def asyncBasic(session: com.snowflake.snowpark.Session): String = {
      val connection = session.jdbcConnection
      val stmt = connection.createStatement()
      val rs = stmt.asInstanceOf[SnowflakeStatement].executeAsyncQuery("CALL SYSTEM$WAIT(10)")
      val status = rs.asInstanceOf[SnowflakeResultSet].getStatus.toString
      s"""status:    ${status}"""
    }
  }
  $$;
```

Copy code

```
CREATE OR REPLACE PROCEDURE checkStatus()
  RETURNS VARCHAR
  LANGUAGE SCALA
  RUNTIME_VERSION = 2.13
  PACKAGES = ('com.snowflake:snowpark_2.13:latest')
  HANDLER = 'TestScalaSP.asyncBasic'
  AS
  $$
  import java.sql.ResultSet
  import net.snowflake.client.jdbc.{SnowflakeConnectionV1, SnowflakeResultSet, SnowflakeStatement}
  object TestScalaSP {
    def asyncBasic(session: com.snowflake.snowpark.Session): String = {
      val connection = session.jdbcConnection
      val stmt = connection.createStatement()
      val rs = stmt.asInstanceOf[SnowflakeStatement].executeAsyncQuery("CALL SYSTEM$WAIT(10)")
      val status = rs.asInstanceOf[SnowflakeResultSet].getStatus.toString
      s"""status:    ${status}"""
    }
  }
  $$;
```
