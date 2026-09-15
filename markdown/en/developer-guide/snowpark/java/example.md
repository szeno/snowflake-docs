# A Simple Example of Using Snowpark Java

The following example prints the count and names of tables in the current database.
Replace the `<placeholders>` with values that you use to connect to Snowflake.

Copy code

```
import com.snowflake.snowpark_java.*;
import java.util.HashMap;
import java.util.Map;

public class SnowparkExample {
  public static void main(String[] args) {
    // Create a Session, specifying the properties used to
    // connect to the Snowflake database.
    Map<String, String> properties = new HashMap<>();
    properties.put("URL", "https://<account_identifier>.snowflakecomputing.com");
    properties.put("USER", "<username>");
    properties.put("PASSWORD", "<password>");
    properties.put("ROLE", "<role_name_with_access_to_public_schema>");
    properties.put("WAREHOUSE", "<warehouse_name>");
    properties.put("DB", "<database_name>");
    properties.put("SCHEMA", "<schema_name>");
    Session session = Session.builder().configs(properties).create();

    // Get the number of tables in the PUBLIC schema.
    DataFrame dfTables = session.table("INFORMATION_SCHEMA.TABLES")
      .filter(Functions.col("TABLE_SCHEMA").equal_to(Functions.lit("PUBLIC")));
    long tableCount = dfTables.count();
    String currentDb = session.getCurrentDatabase().orElse("<no current database>");
    System.out.println("Number of tables in the PUBLIC schema in " + currentDb + " database: " + tableCount);

    // Get the list of table names in the PUBLIC schema.
    DataFrame dfPublicSchemaTables = dfTables.select(Functions.col("TABLE_NAME"));
    dfPublicSchemaTables.show();
  }
}
```

This prints out the number of tables and the list of tables in the schema:

Copy code

```
Number of tables in the PUBLIC schema in the "MY_DB" database: 8
...
---------------------
|"TABLE_NAME"       |
---------------------
|A_TABLE            |
...
```
