# A Simple Example of Using Snowpark Scala

The following example prints the count and names of tables in the current database.
Replace the `<placeholders>` with values that you use to connect to Snowflake.

Copy code

```
import com.snowflake.snowpark._
import com.snowflake.snowpark.functions._

object Main {
  def main(args: Array[String]) {

    // Create a Session, specifying the properties used to
    // connect to the Snowflake database.
    val builder = Session.builder.configs(Map(
      "URL" -> "https://<account_identifier>.snowflakecomputing.com",
      "USER" -> "<username>",
      "PASSWORD" -> "<password>",
      "ROLE" -> "<role_name_with_access_to_public_schema>",
      "WAREHOUSE" -> "<warehouse_name>",
      "DB" -> "<database_name>",
      "SCHEMA" -> "<schema_name>"
    ))
    val session = builder.create

    // Get the number of tables in the PUBLIC schema.
    var dfTables = session.table("INFORMATION_SCHEMA.TABLES").filter(col("TABLE_SCHEMA") === "PUBLIC")
    var tableCount = dfTables.count()
    var currentDb = session.getCurrentDatabase.getOrElse("<no current database>")
    println(s"Number of tables in the PUBLIC schema in the $currentDb database: $tableCount")

    // Get the list of table names in the PUBLIC schema.
    var dfPublicSchemaTables = dfTables.select(col("TABLE_NAME"))
    dfPublicSchemaTables.show()
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
