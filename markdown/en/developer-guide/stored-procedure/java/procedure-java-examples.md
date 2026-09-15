# Java handler examples for stored procedures

## Using Snowpark APIs for asynchronous processing

In the following example, the `getResultJDBC` procedure executes an asynchronous child job that waits 10 seconds.

Copy code

```
CREATE OR REPLACE PROCEDURE getResultJDBC()
RETURNS VARCHAR
LANGUAGE JAVA
RUNTIME_VERSION = 11
PACKAGES = ('com.snowflake:snowpark:latest')
HANDLER = 'TestJavaSP.asyncBasic'
AS
$$
import java.sql.*;
import net.snowflake.client.jdbc.*;

class TestJavaSP {
  public String asyncBasic(com.snowflake.snowpark.Session session) throws Exception {
    Connection connection = session.jdbcConnection();
    SnowflakeStatement stmt = (SnowflakeStatement)connection.createStatement();
    ResultSet resultSet = stmt.executeAsyncQuery("CALL SYSTEM$WAIT(10)");
    resultSet.next();
    return resultSet.getString(1);
  }
}
$$;
```
