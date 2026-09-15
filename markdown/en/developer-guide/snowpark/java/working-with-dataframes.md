# Working with DataFrames in Snowpark Java

In Snowpark, the main way in which you query and process data is through a DataFrame. This topic explains how to work with
DataFrames.

To retrieve and manipulate data, you use the [DataFrame](../reference/scala/com/snowflake/snowpark/DataFrame.html) class. A DataFrame represents a relational dataset that is evaluated
lazily: it only executes when a specific action is triggered. In a sense, a DataFrame is like a query that needs to be evaluated
in order to retrieve data.

To retrieve data into a DataFrame:

1. [Construct a DataFrame, specifying the source of the data for the dataset](#label-snowpark-java-dataframe-construct).

   For example, you can create a DataFrame to hold data from a table, an external CSV file, or the execution of a SQL statement.
2. [Specify how the dataset in the DataFrame should be transformed](#label-snowpark-java-dataframe-transform).

   For example, you can specify which columns should be selected, how the rows should be filtered, how the results should be
   sorted and grouped, etc.
3. [Execute the statement to retrieve the data into the DataFrame](#label-snowpark-java-dataframe-action-method).

   In order to retrieve the data into the DataFrame, you must invoke a method that performs an action (for example, the
   `collect()` method).

The next sections explain these steps in more detail.

## Setting up the Examples for this Section

Some of the examples of this section use a DataFrame to query a table named `sample_product_data`. If you want to run these
examples, you can create this table and fill the table with some data by executing the following SQL statements:

Copy code

```
CREATE OR REPLACE TABLE sample_product_data (id INT, parent_id INT, category_id INT, name VARCHAR, serial_number VARCHAR, key INT, "3rd" INT, amount NUMBER(12, 2), quantity INT, product_date DATE);
INSERT INTO sample_product_data VALUES
    (1, 0, 5, 'Product 1', 'prod-1', 1, 10, 1.00, 15, TO_DATE('2021.01.01', 'YYYY.MM.DD')),
    (2, 1, 5, 'Product 1A', 'prod-1-A', 1, 20, 2.00, 30, TO_DATE('2021.02.01', 'YYYY.MM.DD')),
    (3, 1, 5, 'Product 1B', 'prod-1-B', 1, 30, 3.00, 45, TO_DATE('2021.03.01', 'YYYY.MM.DD')),
    (4, 0, 10, 'Product 2', 'prod-2', 2, 40, 4.00, 60, TO_DATE('2021.04.01', 'YYYY.MM.DD')),
    (5, 4, 10, 'Product 2A', 'prod-2-A', 2, 50, 5.00, 75, TO_DATE('2021.05.01', 'YYYY.MM.DD')),
    (6, 4, 10, 'Product 2B', 'prod-2-B', 2, 60, 6.00, 90, TO_DATE('2021.06.01', 'YYYY.MM.DD')),
    (7, 0, 20, 'Product 3', 'prod-3', 3, 70, 7.00, 105, TO_DATE('2021.07.01', 'YYYY.MM.DD')),
    (8, 7, 20, 'Product 3A', 'prod-3-A', 3, 80, 7.25, 120, TO_DATE('2021.08.01', 'YYYY.MM.DD')),
    (9, 7, 20, 'Product 3B', 'prod-3-B', 3, 90, 7.50, 135, TO_DATE('2021.09.01', 'YYYY.MM.DD')),
    (10, 0, 50, 'Product 4', 'prod-4', 4, 100, 7.75, 150, TO_DATE('2021.10.01', 'YYYY.MM.DD')),
    (11, 10, 50, 'Product 4A', 'prod-4-A', 4, 100, 8.00, 165, TO_DATE('2021.11.01', 'YYYY.MM.DD')),
    (12, 10, 50, 'Product 4B', 'prod-4-B', 4, 100, 8.50, 180, TO_DATE('2021.12.01', 'YYYY.MM.DD'));
```

To verify that the table was created, run:

Copy code

```
SELECT * FROM sample_product_data;
```

## Constructing a DataFrame

To construct a DataFrame, you can use methods in the `Session` class. Each of the following methods constructs a DataFrame
from a different type of data source:

- To create a DataFrame from data in a table, view, or stream, call the `table` method:

  Copy code

  ```
  // Create a DataFrame from the data in the "sample_product_data" table.
  DataFrame dfTable = session.table("sample_product_data");

  // Print out the first 10 rows.
  dfTable.show();
  ```

  Note

  The `table` method returns an `Updatable` object. `Updatable` extends `DataFrame` and provides
  additional methods for working with data in the table (e.g. methods for updating and deleting data). See
  [Updating, Deleting, and Merging Rows in a Table](#label-snowpark-java-dataframe-updatable).
- To create a DataFrame from specified values:

  1. Construct an array of `Row` objects that contain the values.
  2. Construct a `StructType` object that describes the data types of those values.
  3. Call the `createDataFrame` method, passing in the array and `StructType` object.

  Copy code

  ```
   // Import name from the types package, which contains StructType and StructField.
  import com.snowflake.snowpark_java.types.*;
  ...

   // Create a DataFrame containing specified values.
   Row[] data = {Row.create(1, "a"), Row.create(2, "b")};
   StructType schema =
  StructType.create(
    new StructField("num", DataTypes.IntegerType),
    new StructField("str", DataTypes.StringType));
   DataFrame df = session.createDataFrame(data, schema);

   // Print the contents of the DataFrame.
   df.show();
  ```

  Note

  Words reserved by Snowflake are not valid as column names when constructing a DataFrame. For a list of reserved words, refer to
  [Reserved & limited keywords](/sql-reference/reserved-keywords).
- To create a DataFrame containing a range of values, call the `range` method:

  Copy code

  ```
  // Create a DataFrame from a range
  DataFrame dfRange = session.range(1, 10, 2);

  // Print the contents of the DataFrame.
  dfRange.show();
  ```
- To [create a DataFrame for a file in a stage](#label-snowpark-java-dataframe-stages-query), call `read` to get a
  `DataFrameReader` object. In the `DataFrameReader` object, call the method corresponding to the format of the data
  in the file:

  Copy code

  ```
  // Create a DataFrame from data in a stage.
  DataFrame dfJson = session.read().json("@mystage2/data1.json");

  // Print the contents of the DataFrame.
  dfJson.show();
  ```
- To create a DataFrame to hold the results of a SQL query, call the `sql` method:

  Copy code

  ```
  // Create a DataFrame from a SQL query
  DataFrame dfSql = session.sql("SELECT name from sample_product_data");

  // Print the contents of the DataFrame.
  dfSql.show();
  ```

  Note: Although you can use this method to execute SELECT statements that retrieve data from tables and staged files, you should
  use the `table` and `read` methods instead. Methods like `table` and `read` can provide better syntax
  highlighting, error highlighting, and intelligent code completion in development tools.

## Specifying How the Dataset Should Be Transformed

To specify which columns should be selected and how the results should be filtered, sorted, grouped, etc., call the DataFrame
methods that transform the dataset. To identify columns in these methods, use the `Functions.col` static method or an
expression that evaluates to a column. (See [Specifying Columns and Expressions](#label-snowpark-java-dataframe-cols-and-expressions).)

For example:

- To specify which rows should be returned, call the `filter` method:

  Copy code

  ```
  // Create a DataFrame for the rows with the ID 1
  // in the "sample_product_data" table.
  DataFrame df = session.table("sample_product_data").filter(
    Functions.col("id").equal_to(Functions.lit(1)));
  df.show();
  ```
- To specify the columns that should be selected, call the `select` method:

  Copy code

  ```
  // Create a DataFrame that contains the id, name, and serial_number
  // columns in the "sample_product_data" table.
  DataFrame df = session.table("sample_product_data").select(
    Functions.col("id"), Functions.col("name"), Functions.col("serial_number"));
  df.show();
  ```

Each method returns a new DataFrame object that has been transformed. (The method does not affect the original DataFrame object.)
This means that if you want to apply multiple transformations, you can
[chain method calls](#label-snowpark-java-dataframe-chaining-method-calls), calling each subsequent transformation method
on the new DataFrame object returned by the previous method call.

Note that these transformation methods do not retrieve data from the Snowflake database. (The action methods described in
[Performing an Action to Evaluate a DataFrame](#label-snowpark-java-dataframe-action-method) perform the data retrieval.) The transformation methods simply specify how
the SQL statement should be constructed.

### Specifying Columns and Expressions

When calling these transformation methods, you might need to specify columns or expressions that use columns. For example, when
calling the `select` method, you need to specify the columns that should be selected.

To refer to a column, create a [Column](../reference/scala/com/snowflake/snowpark/Column.html) object by calling the [Functions.col](../reference/java/com/snowflake/snowpark_java/Functions.html#col(java.lang.String)) static method.

Copy code

```
DataFrame dfProductInfo = session.table("sample_product_data").select(Functions.col("id"), Functions.col("name"));
dfProductInfo.show();
```

Note

To create a `Column` object for a literal, see [Using Literals as Column Objects](#label-snowpark-java-dataframe-cols-lit).

When specifying a filter, projection, join condition, etc., you can use `Column` objects in an expression. For example:

- You can use `Column` objects with the `filter` method to specify a filter condition:

  Copy code

  ```
  // Specify the equivalent of "WHERE id = 12"
  // in an SQL SELECT statement.
  DataFrame df = session.table("sample_product_data");
  df.filter(Functions.col("id").equal_to(Functions.lit(12))).show();
  ```

  Copy code

  ```
  // Specify the equivalent of "WHERE key + category_id < 10"
  // in an SQL SELECT statement.
  DataFrame df2 = session.table("sample_product_data");
  df2.filter(Functions.col("key").plus(Functions.col("category_id")).lt(Functions.lit(10))).show();
  ```
- You can use `Column` objects with the `select` method to define an alias:

  Copy code

  ```
  // Specify the equivalent of "SELECT key * 10 AS c"
  // in an SQL SELECT statement.
  DataFrame df3 = session.table("sample_product_data");
  df3.select(Functions.col("key").multiply(Functions.lit(10)).as("c")).show();
  ```
- You can use `Column` objects with the `join` method to define a join condition:

  Copy code

  ```
  // Specify the equivalent of "sample_a JOIN sample_b on sample_a.id_a = sample_b.id_a"
  // in an SQL SELECT statement.
  DataFrame dfLhs = session.table("sample_a");
  DataFrame dfRhs = session.table("sample_b");
  DataFrame dfJoined = dfLhs.join(dfRhs, dfLhs.col("id_a").equal_to(dfRhs.col("id_a")));
  dfJoined.show();
  ```

#### Referring to Columns in Different DataFrames

When referring to columns in two different DataFrame objects that have the same name (for example, joining the DataFrames on that
column), you can use the `col` method in each DataFrame object to refer to a column in that object (for example,
`df1.col("name")` and `df2.col("name")`).

The following example demonstrates how to use the `col` method to refer to a column in a specific DataFrame. The example
joins two DataFrame objects that both have a column named `value`. The example uses the `as` method of the `Column`
object to change the names of the columns in the newly created DataFrame.

Copy code

```
// Create a DataFrame that joins two other DataFrames (dfLhs and dfRhs).
// Use the DataFrame.col method to refer to the columns used in the join.
DataFrame dfLhs = session.table("sample_a");
DataFrame dfRhs = session.table("sample_b");
DataFrame dfJoined = dfLhs.join(dfRhs, dfLhs.col("id_a").equal_to(dfRhs.col("id_a"))).select(dfLhs.col("value").as("L"), dfRhs.col("value").as("R"));
dfJoined.show();
```

### Using Double Quotes Around Object Identifiers (Table Names, Column Names, etc.)

The names of databases, schemas, tables, and stages that you specify must conform to the
[Snowflake identifier requirements](/sql-reference/identifiers-syntax). When you specify a name, Snowflake considers the
name to be in upper case. For example, the following calls are equivalent:

Copy code

```
// The following calls are equivalent:
df.select(Functions.col("id123"));
df.select(Functions.col("ID123"));
```

If the name does not conform to the identifier requirements, you must use double quotes (`"`) around the name. Use a backslash
(`\`) to escape the double quote character within a Java string literal. For example, the following table name does not start
with a letter or an underscore, so you must use double quotes around the name:

Copy code

```
DataFrame df = session.table("\"10tablename\"");
```

Note that when specifying the name of a column, you don’t need to use double quotes around the name. The Snowpark library
automatically encloses the column name in double quotes for you if the name does not comply with the identifier requirements:

Copy code

```
// The following calls are equivalent:
df.select(Functions.col("3rdID"));
df.select(Functions.col("\"3rdID\""));

// The following calls are equivalent:
df.select(Functions.col("id with space"));
df.select(Functions.col("\"id with space\""));
```

If you have already added double quotes around a column name, the library does not insert additional double quotes around the
name.

In some cases, the column name might contain double quote characters:

Copy code

```
describe table quoted;
+------------------------+ ...
| name                   | ...
|------------------------+ ...
| name_with_"air"_quotes | ...
| "column_name_quoted"   | ...
+------------------------+ ...
```

As explained in [Identifier requirements](/sql-reference/identifiers-syntax), for each double quote character within a double-quoted identifier, you
must use two double quote characters (e.g. `"name_with_""air""_quotes"` and `"""column_name_quoted"""`):

Copy code

```
DataFrame dfTable = session.table("quoted");
dfTable.select("\"name_with_\"\"air\"\"_quotes\"");
dfTable.select("\"\"\"column_name_quoted\"\"\"");
```

Keep in mind that when an identifier is enclosed in double quotes (whether you explicitly added the quotes or the library added
the quotes for you), [Snowflake treats the identifier as case-sensitive](/sql-reference/identifiers-syntax):

Copy code

```
// The following calls are NOT equivalent!
// The Snowpark library adds double quotes around the column name,
// which makes Snowflake treat the column name as case-sensitive.
df.select(Functions.col("id with space"));
df.select(Functions.col("ID WITH SPACE"));
```

### Using Literals as Column Objects

To use a literal in a method that passes in a `Column` object, create a `Column` object for the literal by passing
the literal to the `lit` static method in the `Functions` class. For example:

Copy code

```
// Show the first 10 rows in which category_id is greater than 5.
// Use `Functions.lit(5)` to create a Column object for the literal 5.
DataFrame df = session.table("sample_product_data");
df.filter(Functions.col("category_id").gt(Functions.lit(5))).show();
```

If the literal is a floating point or double value in Java (e.g. `0.05` is treated as a Double by default), the Snowpark library
generates SQL that implicitly casts the value to the corresponding Snowpark data type (e.g. `0.05::DOUBLE`). This can produce
an approximate value that differs from the exact number specified.

For example, the following code displays no matching rows, even though the filter (that matches values greater than or equal to
`0.05`) should match the rows in the DataFrame:

Copy code

```
// Create a DataFrame that contains the value 0.05.
DataFrame df = session.sql("select 0.05 :: Numeric(5, 2) as a");

// Applying this filter results in no matching rows in the DataFrame.
df.filter(Functions.col("a").leq(Functions.lit(0.06).minus(Functions.lit(0.01)))).show();
```

The problem is that `Functions.lit(0.06)` and `Functions.lit(0.01)` produce approximate values for `0.06` and `0.01`,
not the exact values.

To avoid this problem, [cast the literal to the Snowpark type](#label-snowpark-java-dataframe-cols-cast) that you want to
use. For example, to use a [NUMBER](/sql-reference/data-types-numeric#label-data-type-number) with a precision of 5 and a scale of 2:

Copy code

```
import com.snowflake.snowpark_java.types.*;
...

df.filter(Functions.col("a").leq(Functions.lit(0.06).cast(DataTypes.createDecimalType(5, 2)).minus(Functions.lit(0.01).cast(DataTypes.createDecimalType(5, 2))))).show();
```

### Casting a Column Object to a Specific Type

To cast a `Column` object to a specific type, call the [cast](../reference/java/com/snowflake/snowpark_java/Column.html#cast(com.snowflake.snowpark_java.types.DataType)) method, and pass in a type object from the
[com.snowflake.snowpark\_java.types package](../reference/java/com/snowflake/snowpark_java/types/package-summary.html). For example, to cast a literal as a [NUMBER](/sql-reference/data-types-numeric#label-data-type-number) with a precision
of 5 and a scale of 2:

Copy code

```
// Import for the DecimalType class..
import com.snowflake.snowpark_java.types.*;

Column decimalValue = Functions.lit(0.05).cast(DataTypes.createDecimalType(5,2));
```

### Chaining Method Calls

Because each [method that transforms a DataFrame object](#label-snowpark-java-dataframe-transform) returns a new DataFrame
object that has the transformation applied, you can [chain method calls](https://en.wikipedia.org/wiki/Method_chaining) to
produce a new DataFrame that is transformed in additional ways.

The following example returns a DataFrame that is configured to:

- Query the `sample_product_data` table.
- Return the row with `id = 1`.
- Select the `name` and `serial_number` columns.

Copy code

```
DataFrame dfProductInfo = session.table("sample_product_data").filter(Functions.col("id").equal_to(Functions.lit(1))).select(Functions.col("name"), Functions.col("serial_number"));
dfProductInfo.show();
```

In this example:

- `session.table("sample_product_data")` returns a DataFrame for the `sample_product_data` table.

  Although the DataFrame does not yet contain the data from the table, the object does contain the definitions of the columns in
  the table.
- `filter(Functions.col("id").equal_to(Functions.lit(1)))` returns a DataFrame for the `sample_product_data` table that is
  set up to return the row with `id = 1`.

  Note again that the DataFrame does not yet contain the matching row from the table. The matching row is not retrieved until you
  [call an action method](#label-snowpark-java-dataframe-action-method).
- `select(Functions.col("name"), Functions.col("serial_number"))` returns a DataFrame that contains the `name` and
  `serial_number` columns for the row in the `sample_product_data` table that has `id = 1`.

When you chain method calls, keep in mind that the order of calls is important. Each method call returns a DataFrame that has been
transformed. Make sure that subsequent calls work with the transformed DataFrame.

For example, in the code below, the `select` method returns a DataFrame that just contains two columns: `name` and
`serial_number`. The `filter` method call on this DataFrame fails because it uses the `id` column, which is not in the
transformed DataFrame.

Copy code

```
// This fails with the error "invalid identifier 'ID'."
DataFrame dfProductInfo = session.table("sample_product_data").select(Functions.col("name"), Functions.col("serial_number")).filter(Functions.col("id").equal_to(Functions.lit(1)));
dfProductInfo.show();
```

In contrast, the following code executes successfully because the `filter()` method is called on a DataFrame that contains
all of the columns in the `sample_product_data` table (including the `id` column):

Copy code

```
// This succeeds because the DataFrame returned by the table() method
// includes the "id" column.
DataFrame dfProductInfo = session.table("sample_product_data").filter(Functions.col("id").equal_to(Functions.lit(1))).select(Functions.col("name"), Functions.col("serial_number"));
dfProductInfo.show();
```

Keep in mind that you might need to make the `select` and `filter` method calls in a different order than you would
use the equivalent keywords (SELECT and WHERE) in a SQL statement.

### Limiting the Number of Rows in a DataFrame

To limit the number of rows in a DataFrame, you can use the [limit](../reference/java/com/snowflake/snowpark_java/DataFrame.html#limit(int)) transformation method.

The Snowpark API also provides action methods for retrieving and printing out a limited number of rows:

- the [first](../reference/java/com/snowflake/snowpark_java/DataFrame.html#first(int)) action method (to execute the query and return the first `n` rows)
- the [show](../reference/java/com/snowflake/snowpark_java/DataFrame.html#show(int)) action method (to execute the query and print the first `n` rows)

These methods effectively add a [LIMIT](/sql-reference/constructs/limit) clause to the SQL statement that is executed.

As explained in the [usage notes for LIMIT](/sql-reference/constructs/limit#label-limit-cmd-usage-notes), the results are non-deterministic unless you
specify a sort order (ORDER BY) in conjunction with LIMIT.

To keep the ORDER BY clause with the LIMIT clause (e.g. so that ORDER BY is not in a separate subquery), you must call the method
that limits results on the DataFrame returned by the `sort` method.

For example, if you are [chaining method calls](#label-snowpark-java-dataframe-chaining-method-calls):

Copy code

```
DataFrame df = session.table("sample_product_data");

// Limit the number of rows to 5, sorted by parent_id.
DataFrame dfSubset = df.sort(Functions.col("parent_id")).limit(5);

// Return the first 5 rows, sorted by parent_id.
Row[] arrayOfRows = df.sort(Functions.col("parent_id")).first(5);

// Print the first 5 rows, sorted by parent_id.
df.sort(Functions.col("parent_id")).show(5);
```

### Retrieving Column Definitions

To retrieve the definition of the columns in the dataset for the DataFrame, call the `schema` method. This method returns
a `StructType` object that contains an `Array` of `StructField` objects. Each `StructField` object
contains the definition of a column.

Copy code

```
import com.snowflake.snowpark_java.types.*;
...

// Get the StructType object that describes the columns in the
// underlying rowset.
StructType tableSchema = session.table("sample_product_data").schema();
System.out.println("Schema for sample_product_data: " + tableSchema);
```

In the returned `StructType` object, the column names are always normalized. Unquoted identifiers are returned in uppercase,
and quoted identifiers are returned in the exact case in which they were defined.

The following example creates a DataFrame containing the columns named `ID` and `3rd`. For the column name `3rd`, the
Snowpark library automatically encloses the name in double quotes (`"3rd"`) because
[the name does not comply with the requirements for an identifier](#label-snowpark-java-dataframe-cols-identifiers).

The example calls the `schema` method and then calls the `names` method on the returned `StructType` object to
get an array of column names. The names are normalized in the `StructType` returned by the `schema` method.

Copy code

```
import java.util.Arrays;
...

// Create a DataFrame containing the "id" and "3rd" columns.
DataFrame dfSelectedColumns = session.table("sample_product_data").select(Functions.col("id"), Functions.col("3rd"));
// Print out the names of the columns in the schema.
System.out.println(Arrays.toString(dfSelectedColumns.schema().names()));
```

### Joining DataFrames

To join DataFrame objects, call the [join](../reference/java/com/snowflake/snowpark_java/DataFrame.html#join(com.snowflake.snowpark_java.DataFrame,com.snowflake.snowpark_java.Column,java.lang.String)) method.

The following sections explain how to use DataFrames to perform a join:

- [Setting up the Sample Data for the Joins](#label-snowpark-java-dataframe-join-sample-data)
- [Specifying the Columns for the Join](#label-snowpark-java-dataframe-join-columns)
- [Performing a Natural Join](#label-snowpark-java-dataframe-join-natural)
- [Specifying the Type of Join](#label-snowpark-java-dataframe-join-type)
- [Joining Multiple Tables](#label-snowpark-java-dataframe-multiple-joins)
- [Performing a Self-Join](#label-snowpark-java-dataframe-self-join)

#### Setting up the Sample Data for the Joins

The examples in the next sections use sample data that you can set up by executing the following SQL statements:

Copy code

```
CREATE OR REPLACE TABLE sample_a (
  id_a INTEGER,
  name_a VARCHAR,
  value INTEGER
);
INSERT INTO sample_a (id_a, name_a, value) VALUES
  (10, 'A1', 5),
  (40, 'A2', 10),
  (80, 'A3', 15),
  (90, 'A4', 20)
;
CREATE OR REPLACE TABLE sample_b (
  id_b INTEGER,
  name_b VARCHAR,
  id_a INTEGER,
  value INTEGER
);
INSERT INTO sample_b (id_b, name_b, id_a, value) VALUES
  (4000, 'B1', 40, 10),
  (4001, 'B2', 10, 5),
  (9000, 'B3', 80, 15),
  (9099, 'B4', NULL, 200)
;
CREATE OR REPLACE TABLE sample_c (
  id_c INTEGER,
  name_c VARCHAR,
  id_a INTEGER,
  id_b INTEGER
);
INSERT INTO sample_c (id_c, name_c, id_a, id_b) VALUES
  (1012, 'C1', 10, NULL),
  (1040, 'C2', 40, 4000),
  (1041, 'C3', 40, 4001)
;
```

#### Specifying the Columns for the Join

With the `DataFrame.join` method, you can specify the columns to use in one of the following ways:

- Specify a Column expression that describes the join condition.
- Specify one or more columns that should be used as the common columns in the join.

The following example performs an inner join on the column named `id_a`:

Copy code

```
// Create a DataFrame that joins the DataFrames for the tables
// "sample_a" and "sample_b" on the column named "id_a".
DataFrame dfLhs = session.table("sample_a");
DataFrame dfRhs = session.table("sample_b");
DataFrame dfJoined = dfLhs.join(dfRhs, dfLhs.col("id_a").equal_to(dfRhs.col("id_a")));
dfJoined.show();
```

Note that the example uses the `DataFrame.col` method to specify the condition to use for the join. See
[Specifying Columns and Expressions](#label-snowpark-java-dataframe-cols-and-expressions) for more about this method.

This prints the following output:

Copy code

```
----------------------------------------------------------------------
|"ID_A"  |"NAME_A"  |"VALUE"  |"ID_B"  |"NAME_B"  |"ID_A"  |"VALUE"  |
----------------------------------------------------------------------
|10      |A1        |5        |4001    |B2        |10      |5        |
|40      |A2        |10       |4000    |B1        |40      |10       |
|80      |A3        |15       |9000    |B3        |80      |15       |
----------------------------------------------------------------------
```

##### Identical Column Names Duplicated in the Join Result

In the DataFrame resulting from a join, the Snowpark library uses the column names found in the tables that were joined even when the
column names are identical across tables. When this happens, these column names are duplicated in the DataFrame resulting from the join.
To access a duplicated column by name, call the `col` method on the DataFrame representing the column’s original table. (For more
information about specifying columns, see [Referring to Columns in Different DataFrames](#label-snowpark-java-multiple-dataframes-cols).)

Code in the following example joins two DataFrames, then calls the `select` method on the joined DataFrame. It specifies the columns
to select by calling the `col` method from the variable representing the respective DataFrame objects: `dfRhs` and
`dfLhs`. It uses the `as` method to give the columns new names in the DataFrame that the `select` method creates.

Copy code

```
DataFrame dfLhs = session.table("sample_a");
DataFrame dfRhs = session.table("sample_b");
DataFrame dfJoined = dfLhs.join(dfRhs, dfLhs.col("id_a").equal_to(dfRhs.col("id_a")));
DataFrame dfSelected = dfJoined.select(dfLhs.col("value").as("LeftValue"), dfRhs.col("value").as("RightValue"));
dfSelected.show();
```

This prints the following output:

Copy code

```
------------------------------
|"LEFTVALUE"  |"RIGHTVALUE"  |
------------------------------
|5            |5             |
|10           |10            |
|15           |15            |
------------------------------
```

##### Deduplicate Columns Before Saving or Caching

Note that when a DataFrame resulting from a join includes duplicate column names, you must deduplicate or rename columns to remove
duplication in the DataFrame before you save the result to a table or cache the DataFrame. For duplicate column names in a DataFrame that
you save to a table or cache, the Snowpark library will replace duplicate column names with aliases so that they’re no longer duplicated.

The following example illustrates how the output of a cached DataFrame might appear if column names `ID_A` and `VALUE` were
duplicated in a join from two tables, then not deduplicated or renamed prior to caching the result.

Copy code

```
--------------------------------------------------------------------------------------------------
|"l_ZSz7_ID_A"  |"NAME_A"  |"l_ZSz7_VALUE"  |"ID_B"  |"NAME_B"  |"r_heec_ID_A"  |"r_heec_VALUE"  |
--------------------------------------------------------------------------------------------------
|10             |A1        |5               |4001    |B2        |10             |5               |
|40             |A2        |10              |4000    |B1        |40             |10              |
|80             |A3        |15              |9000    |B3        |80             |15              |
--------------------------------------------------------------------------------------------------
```

#### Performing a Natural Join

To perform a [natural join](/user-guide/querying-joins#label-querying-join-natural) (where DataFrames are joined on columns that have the same name),
call the [naturalJoin](../reference/java/com/snowflake/snowpark_java/DataFrame.html#naturalJoin(com.snowflake.snowpark_java.DataFrame)) method.

The following example joins the DataFrames for the tables `sample_a` and `sample_b` on their common columns (the column
`id_a`):

Copy code

```
DataFrame dfLhs = session.table("sample_a");
DataFrame dfRhs = session.table("sample_b");
DataFrame dfJoined = dfLhs.naturalJoin(dfRhs);
dfJoined.show();
```

This prints the following output:

Copy code

```
---------------------------------------------------
|"ID_A"  |"VALUE"  |"NAME_A"  |"ID_B"  |"NAME_B"  |
---------------------------------------------------
|10      |5        |A1        |4001    |B2        |
|40      |10       |A2        |4000    |B1        |
|80      |15       |A3        |9000    |B3        |
---------------------------------------------------
```

#### Specifying the Type of Join

By default, the `DataFrame.join` method creates an inner join. To specify a different type of join, set the
`joinType` argument to one of the following values:

| Type of Join | `joinType` |
| --- | --- |
| Inner join | `inner` (default) |
| Cross join | `cross` |
| Full outer join | `full` |
| Left outer join | `left` |
| Left anti join | `leftanti` |
| Left semi join | `leftsemi` |
| Right outer join | `right` |

Expand

Show lessSee more

For example:

Copy code

```
// Create a DataFrame that performs a left outer join on
// "sample_a" and "sample_b" on the column named "id_a".
DataFrame dfLhs = session.table("sample_a");
DataFrame dfRhs = session.table("sample_b");
DataFrame dfLeftOuterJoin = dfLhs.join(dfRhs, dfLhs.col("id_a").equal_to(dfRhs.col("id_a")), "left");
dfLeftOuterJoin.show();
```

This prints the following output:

Copy code

```
----------------------------------------------------------------------
|"ID_A"  |"NAME_A"  |"VALUE"  |"ID_B"  |"NAME_B"  |"ID_A"  |"VALUE"  |
----------------------------------------------------------------------
|40      |A2        |10       |4000    |B1        |40      |10       |
|10      |A1        |5        |4001    |B2        |10      |5        |
|80      |A3        |15       |9000    |B3        |80      |15       |
|90      |A4        |20       |NULL    |NULL      |NULL    |NULL     |
----------------------------------------------------------------------
```

#### Joining Multiple Tables

To join multiple tables:

1. Create a DataFrame for each table.
2. Call the `DataFrame.join` method on the first DataFrame, passing in the second DataFrame.
3. Using the DataFrame returned by the `join` method, call the `join` method, passing in the third DataFrame.

You can [chain](#label-snowpark-java-dataframe-chaining-method-calls) the `join` calls as shown below:

Copy code

```
DataFrame dfFirst = session.table("sample_a");
DataFrame dfSecond  = session.table("sample_b");
DataFrame dfThird = session.table("sample_c");
DataFrame dfJoinThreeTables = dfFirst.join(dfSecond, dfFirst.col("id_a").equal_to(dfSecond.col("id_a"))).join(dfThird, dfFirst.col("id_a").equal_to(dfThird.col("id_a")));
dfJoinThreeTables.show();
```

This prints the following output:

Copy code

```
------------------------------------------------------------------------------------------------------------
|"ID_A"  |"NAME_A"  |"VALUE"  |"ID_B"  |"NAME_B"  |"ID_A"  |"VALUE"  |"ID_C"  |"NAME_C"  |"ID_A"  |"ID_B"  |
------------------------------------------------------------------------------------------------------------
|10      |A1        |5        |4001    |B2        |10      |5        |1012    |C1        |10      |NULL    |
|40      |A2        |10       |4000    |B1        |40      |10       |1040    |C2        |40      |4000    |
|40      |A2        |10       |4000    |B1        |40      |10       |1041    |C3        |40      |4001    |
------------------------------------------------------------------------------------------------------------
```

#### Performing a Self-Join

If you need to join a table with itself on different columns, you can’t perform the self-join with a single DataFrame. The
following examples that use a single DataFrame to perform a self-join fail because the column expressions for `"id"` are
present in the left and right sides of the join:

Copy code

```
// This fails because columns named "id" and "parent_id"
// are in the left and right DataFrames in the join.
DataFrame df = session.table("sample_product_data");
DataFrame dfJoined = df.join(df, Functions.col("id").equal_to(Functions.col("parent_id")));
```

Copy code

```
// This fails because columns named "id" and "parent_id"
// are in the left and right DataFrames in the join.
DataFrame df = session.table("sample_product_data");
DataFrame dfJoined = df.join(df, df.col("id").equal_to(df.col("parent_id")));
```

Both of these examples fail with the following exception:

Copy code

```
Exception in thread "main" com.snowflake.snowpark_java.SnowparkClientException:
  Joining a DataFrame to itself can lead to incorrect results due to ambiguity of column references.
  Instead, join this DataFrame to a clone() of itself.
```

Instead, use the [clone](../reference/java/com/snowflake/snowpark_java/DataFrame.html#clone()) method to create a clone of the DataFrame object, and use the two DataFrame objects to perform the join:

Copy code

```
// Create a DataFrame object for the "sample_product_data" table for the left-hand side of the join.
DataFrame dfLhs = session.table("sample_product_data");
// Clone the DataFrame object to use as the right-hand side of the join.
DataFrame dfRhs = dfLhs.clone();

// Create a DataFrame that joins the two DataFrames
// for the "sample_product_data" table on the
// "id" and "parent_id" columns.
DataFrame dfJoined = dfLhs.join(dfRhs, dfLhs.col("id").equal_to(dfRhs.col("parent_id")));
dfJoined.show();
```

If you want to perform a self-join on the same column, call the `join` method that passes in the name of the column (or an
array of column names) for the `USING` clause:

Copy code

```
// Create a DataFrame that performs a self-join on a DataFrame
// using the column named "key".
DataFrame df = session.table("sample_product_data");
DataFrame dfJoined = df.join(df, "key");
```

## Performing an Action to Evaluate a DataFrame

As mentioned earlier, the DataFrame is lazily evaluated, which means the SQL statement isn’t sent to the server for execution
until you perform an action. An action causes the DataFrame to be evaluated and sends the corresponding SQL statement to the
server for execution.

The following sections explain how to perform an action synchronously and asynchronously on a DataFrame:

- [Performing an Action Synchronously](#label-snowpark-java-dataframe-action-method-sync)
- [Performing an Action Asynchronously](#label-snowpark-java-dataframe-action-method-async)

### Performing an Action Synchronously

To perform an action synchronously, call one of the following action methods:

| Method to Perform an Action Synchronously | Description |
| --- | --- |
| `DataFrame.collect()` | Evaluates the DataFrame and returns the resulting dataset as an `Array` of [Row](../reference/scala/com/snowflake/snowpark/Row.html) objects. See [Returning All Rows](#label-snowpark-java-dataframe-return-all-rows). |
| `DataFrame.toLocalIterator()` | Evaluates the DataFrame and returns an `Iterator` of [Row](../reference/scala/com/snowflake/snowpark/Row.html) objects. If the result set is large, use this method to avoid loading all the results into memory at once. See [Returning an Iterator for the Rows](#label-snowpark-java-dataframe-return-iterator). |
| `DataFrame.count()` | Evaluates the DataFrame and returns the number of rows. |
| `DataFrame.show()` | Evaluates the DataFrame and prints the rows to the console. Note that this method limits the number of rows to 10 (by default). See [Printing the Rows in a DataFrame](#label-snowpark-java-dataframe-print-results). |
| `DataFrame.cacheResult()` | Executes the query, creates a temporary table, and puts the results into the table. The method returns a `HasCachedResult` object that you can use to access the data in this temporary table. See [Caching a DataFrame](#label-snowpark-java-dataframe-caching). |
| `DataFrame.write().saveAsTable()` | Saves the data in the DataFrame to the specified table. See [Saving Data to a Table](#label-snowpark-java-dataframe-save-table). |
| `DataFrame.read().fileformat().copyInto('tableName')` | Copies the data in the DataFrame to the specified table. See [Copying Data from Files into a Table](#label-snowpark-java-dataframe-stages-copy-into-table). |
| `Session.table('tableName').delete()` | Deletes rows in the specified table. See [Updating, Deleting, and Merging Rows in a Table](#label-snowpark-java-dataframe-updatable). |
| `Session.table('tableName').update()`, `Session.table('tableName').updateColumn()` | Updates rows in the specified table. See [Updating, Deleting, and Merging Rows in a Table](#label-snowpark-java-dataframe-updatable). |
| `Session.table('tableName').merge().methods.collect()` | Merges rows into the specified table. See [Updating, Deleting, and Merging Rows in a Table](#label-snowpark-java-dataframe-updatable). |

Expand

Show lessSee more

For example, to execute the query and return the number of results, call the `count` method:

Copy code

```
// Create a DataFrame for the "sample_product_data" table.
DataFrame dfProducts = session.table("sample_product_data");

// Send the query to the server for execution and
// print the count of rows in the table.
System.out.println("Rows returned: " + dfProducts.count());
```

You can also call action methods to:

- [Execute a query against a table and return the results](#label-snowpark-java-dataframe-return-all-rows).
- [Execute a query and print the results to the console](#label-snowpark-java-dataframe-print-results).

Note: If you are calling the `schema` method to get the definitions of the columns in the DataFrame, you do not need to
call an action method.

### Performing an Action Asynchronously

Note

This feature was introduced in Snowpark 0.11.0.

To perform an action asynchronously, call the `async` method to return an “async actor” object (e.g.
`DataFrameAsyncActor`), and call an asynchronous action method in that object.

These action methods of an async actor object return a `TypedAsyncJob` object, which you can use to check
the status of the asynchronous action and retrieve the results of the action.

The next sections explain how to perform actions asynchronously and check the results.

- [Understanding the Basic Flow of Asynchronous Actions](#label-snowpark-java-dataframe-action-method-async-basic)
- [Specifying the Maximum Number of Seconds to Wait](#label-snowpark-java-dataframe-action-method-async-timeout)
- [Accessing an Asynchronous Query by ID](#label-snowpark-java-dataframe-action-method-async-query-id)

#### Understanding the Basic Flow of Asynchronous Actions

You can use the following methods to perform an action asynchronously:

| Method to Perform an Action Asynchronously | Description |
| --- | --- |
| `DataFrame.async().collect()` | Asynchronously evaluates the DataFrame to retrieve the resulting dataset as an `Array` of [Row](../reference/scala/com/snowflake/snowpark/Row.html) objects. See [Returning All Rows](#label-snowpark-java-dataframe-return-all-rows). |
| `DataFrame.async.toLocalIterator` | Asynchronously evaluates the DataFrame to retrieve an `Iterator` of [Row](../reference/scala/com/snowflake/snowpark/Row.html) objects. If the result set is large, use this method to avoid loading all the results into memory at once. See [Returning an Iterator for the Rows](#label-snowpark-java-dataframe-return-iterator). |
| `DataFrame.async().count()` | Asynchronously evaluates the DataFrame to retrieve the number of rows. |
| `DataFrame.write().async().saveAsTable()` | Asynchronously saves the data in the DataFrame to the specified table. See [Saving Data to a Table](#label-snowpark-java-dataframe-save-table). |
| `DataFrame.read().fileformat().async().copyInto('tableName')` | Asynchronously copies the data in the DataFrame to the specified table. See [Copying Data from Files into a Table](#label-snowpark-java-dataframe-stages-copy-into-table). |
| `Session.table('tableName').async().delete()` | Asynchronously deletes rows in the specified table. See [Updating, Deleting, and Merging Rows in a Table](#label-snowpark-java-dataframe-updatable). |
| `Session.table('tableName').async().update()` and `Session.table('tableName').async().updateColumn()` | Asynchronously updates rows in the specified table. See [Updating, Deleting, and Merging Rows in a Table](#label-snowpark-java-dataframe-updatable). |

Expand

Show lessSee more

From the returned [TypedAsyncJob](../reference/scala/com/snowflake/snowpark/TypedAsyncJob.html) object, you can do the following:

- To determine if the action has completed, call the `isDone` method.
- To get the query ID that corresponds to the action, call the `getQueryId` method.
- To return the results of the action (e.g. the `Array` of `Row` objects for the `collect` method or the count
  of rows for the `count` method), call the `getResult` method.

  Note that `getResult` is a blocking call.
- To cancel the action, call the `cancel` method.

For example, to execute a query asynchronously and retrieve the results as an `Array` of `Row` objects, call
`async().collect()`:

Copy code

```
import java.util.Arrays;

// Create a DataFrame with the "id" and "name" columns from the "sample_product_data" table.
// This does not execute the query.
DataFrame df = session.table("sample_product_data").select(Functions.col("id"), Functions.col("name"));

// Execute the query asynchronously.
// This call does not block.
TypedAsyncJob<Row[]> asyncJob = df.async().collect();
// Check if the query has completed execution.
System.out.println("Is query " + asyncJob.getQueryId() + " done? " + asyncJob.isDone());
// Get an Array of Rows containing the results, and print the results.
// Note that getResult is a blocking call.
Row[] results = asyncJob.getResult();
System.out.println(Arrays.toString(results));
```

To execute the query asynchronously and retrieve the number of results, call `async().count()`:

Copy code

```
// Create a DataFrame for the "sample_product_data" table.
DataFrame dfProducts = session.table("sample_product_data");

// Execute the query asynchronously.
// This call does not block.
TypedAsyncJob<Long> asyncJob = dfProducts.async().count();
// Check if the query has completed execution.
System.out.println("Is query " + asyncJob.getQueryId() + " done? " + asyncJob.isDone());
// Print the count of rows in the table.
// Note that getResult is a blocking call.
System.out.println("Rows returned: " + asyncJob.getResult());
```

#### Specifying the Maximum Number of Seconds to Wait

When calling the `getResult` method, you can use the `maxWaitTimeInSeconds` argument to specify the maximum number of
seconds to wait for the query to complete before attempting to retrieve the results. For example:

Copy code

```
// Wait a maximum of 10 seconds for the query to complete before retrieving the results.
Row[] results = asyncJob.getResult(10);
```

If you omit this argument, the method waits for the maximum number of seconds specified by the
[snowpark\_request\_timeout\_in\_seconds](/developer-guide/snowpark/java/creating-session#label-snowpark-java-request-timeout-in-seconds) configuration property. (This is a
property that you can set when [creating the Session object](/developer-guide/snowpark/java/creating-session#label-snowpark-java-creating-session).)

#### Accessing an Asynchronous Query by ID

If you have the query ID of an asynchronous query that you submitted earlier, you can call `Session.createAsyncJob` method
to create an [AsyncJob](../reference/scala/com/snowflake/snowpark/AsyncJob.html) object that you can use to check the status of the query, retrieve the query results, or cancel the
query.

Note that unlike `TypedAsyncJob`, `AsyncJob` does not provide a `getResult` method for retrieving the results.
If you need to retrieve the results, call the `getRows` or `getIterator` method instead.

For example:

Copy code

```
import java.util.Arrays;
...

AsyncJob asyncJob = session.createAsyncJob(myQueryId);
// Check if the query has completed execution.
System.out.println("Is query " + asyncJob.getQueryId() + " done? " + asyncJob.isDone());
// If you need to retrieve the results, call getRows to return an Array of Rows containing the results.
// Note that getRows is a blocking call.
Row[] rows = asyncJob.getRows();
System.out.println(Arrays.toString(rows));
```

## Retrieving Rows into a DataFrame

After you [specify how the DataFrame should be transformed](#label-snowpark-java-dataframe-transform), you can
[call an action method](#label-snowpark-java-dataframe-action-method) to execute a query and return the results. You can
return all of the rows in an `Array`, or you can return an `Iterator` that allows you to iterate over the results,
row by row. In the latter case, if the amount of data is large, the rows are loaded into memory by chunk to avoid loading a large
amount of data into memory.

- [Returning All Rows](#label-snowpark-java-dataframe-return-all-rows)
- [Returning an Iterator for the Rows](#label-snowpark-java-dataframe-return-iterator)
- [Returning the First <code className=”samp”><em>n</em></code> Rows](#label-snowpark-java-dataframe-return-first-n-rows)

### Returning All Rows

To return all rows at once, call the [collect](../reference/java/com/snowflake/snowpark_java/DataFrame.html#collect()) method. This method returns an Array of [Row](../reference/scala/com/snowflake/snowpark/Row.html) objects. To retrieve the values
from the row, call the `getType` method (e.g. `getString`, `getInt`, etc.).

For example:

Copy code

```
Row[] rows = session.table("sample_product_data").select(Functions.col("name"), Functions.col("category_id")).sort(Functions.col("name")).collect();
for (Row row : rows) {
  System.out.println("Name: " + row.getString(0) + "; Category ID: " + row.getInt(1));
}
```

### Returning an Iterator for the Rows

If you want to use an `Iterator` to iterate over the [Row](../reference/scala/com/snowflake/snowpark/Row.html) objects in the results, call [toLocalIterator](../reference/java/com/snowflake/snowpark_java/DataFrame.html#toLocalIterator()). If the amount
of data in the results is large, the method loads the rows by chunk to avoid loading all rows into memory at once.

For example:

Copy code

```
import java.util.Iterator;

Iterator<Row> rowIterator = session.table("sample_product_data").select(Functions.col("name"), Functions.col("category_id")).sort(Functions.col("name")).toLocalIterator();
while (rowIterator.hasNext()) {
  Row row = rowIterator.next();
  System.out.println("Name: " + row.getString(0) + "; Category ID: " + row.getInt(1));
}
```

### Returning the First <code className=”samp”><em>n</em></code> Rows

To return the first `n` rows, call the [first](../reference/java/com/snowflake/snowpark_java/DataFrame.html#first(int)) method, passing in the number of rows to return.

As explained in [Limiting the Number of Rows in a DataFrame](#label-snowpark-java-dataframe-limit), the results are non-deterministic. If you want the results to be
deterministic, call this method on a sorted DataFrame (`df.sort().first()`).

For example:

Copy code

```
import java.util.Arrays;
...

DataFrame df = session.table("sample_product_data");
Row[] rows = df.sort(Functions.col("name")).first(5);
System.out.println(Arrays.toString(rows));
```

## Printing the Rows in a DataFrame

To print the first 10 rows in the DataFrame to the console, call the [show](../reference/java/com/snowflake/snowpark_java/DataFrame.html#show(int)) method. To print out a different number of rows, pass
in the number of rows to print.

As explained in [Limiting the Number of Rows in a DataFrame](#label-snowpark-java-dataframe-limit), the results are non-deterministic. If you want the results to be
deterministic, call this method on a sorted DataFrame (`df.sort().show()`).

For example:

Copy code

```
DataFrame df = session.table("sample_product_data");
df.sort(Functions.col("name")).show();
```

## Updating, Deleting, and Merging Rows in a Table

Note

This feature was introduced in Snowpark 0.7.0.

When you call `Session.table` to create a `DataFrame` object for a table, the method returns an `Updatable`
object, which extends `DataFrame` with additional methods for updating and deleting data in the table. (See [Updatable](../reference/scala/com/snowflake/snowpark/Updatable.html).)

If you need to update or delete rows in a table, you can use the following methods of the `Updatable` class:

- Call `update` or `updateColumn` to update existing rows in the table. See
  [Updating Rows in a Table](#label-snowpark-java-dataframe-update-table-rows).
- Call `delete` to delete rows from a table. See [Deleting Rows in a Table](#label-snowpark-java-dataframe-delete-table-rows).
- Call `merge` to insert, update, and delete rows in one table, based on data in a second table or subquery. (This is the
  equivalent of the [MERGE](/sql-reference/sql/merge) command in SQL.) See [Merging Rows into a Table](#label-snowpark-java-dataframe-merge-table-rows).

### Updating Rows in a Table

To update the rows in a table, call the `update` or `updateColumn` method, passing in a `Map` that associates
the columns to update and the corresponding values to assign to those columns:

- To specify the column names as strings in the `Map`, call `updateColumn`.
- To specify `Column` objects in the `Map`, call `update`.

Both methods return an `UpdateResult` object, which contains the number of rows that were updated. (See [UpdateResult](../reference/scala/com/snowflake/snowpark/UpdateResult.html).)

Note

Both methods are [action methods](#label-snowpark-java-dataframe-action-method), which means that calling the method
sends SQL statements to the server for execution.

For example, to replace the values in the column named `count` with the value `1`, and you want to use a `Map` that
associates the column name (a `String`) with the corresponding value, call `updateColumn`:

Copy code

```
import java.util.HashMap;
import java.util.Map;
...

Map<String, Column> assignments = new HashMap<>();
assignments.put("3rd", Functions.lit(1));
Updatable updatableDf = session.table("sample_product_data");
UpdateResult updateResult = updatableDf.updateColumn(assignments);
System.out.println("Number of rows updated: " + updateResult.getRowsUpdated());
```

If you want to use a `Column` object in the `Map` to identify the column to update, call `update`:

Copy code

```
import java.util.HashMap;
import java.util.Map;
...

Map<Column, Column> assignments = new HashMap<>();
assignments.put(Functions.col("3rd"), Functions.lit(1));
Updatable updatableDf = session.table("sample_product_data");
UpdateResult updateResult = updatableDf.update(assignments);
System.out.println("Number of rows updated: " + updateResult.getRowsUpdated());
```

If the update should be made only when a condition is met, you can specify that condition as an argument. For example, to replace
the values in the column named `count` with `2` for rows in which the `category_id` column has the value `20`:

Copy code

```
import java.util.HashMap;
import java.util.Map;
...
Map<Column, Column> assignments = new HashMap<>();
assignments.put(Functions.col("3rd"), Functions.lit(2));
Updatable updatableDf = session.table("sample_product_data");
UpdateResult updateResult = updatableDf.update(assignments, Functions.col("category_id").equal_to(Functions.lit(20)));
System.out.println("Number of rows updated: " + updateResult.getRowsUpdated());
```

If you need to base the condition on a join with a different `DataFrame` object, you can pass that `DataFrame` in as
an argument and use that `DataFrame` in the condition. For example, to replace the values in the column named `count` with
`3` for rows in which the `category_id` column matches the `category_id` in the `DataFrame` `dfParts`:

Copy code

```
import java.util.HashMap;
import java.util.Map;
...
Map<Column, Column> assignments = new HashMap<>();
assignments.put(Functions.col("3rd"), Functions.lit(3));
Updatable updatableDf = session.table("sample_product_data");
DataFrame dfParts = session.table("parts");
UpdateResult updateResult = updatableDf.update(assignments, updatableDf.col("category_id").equal_to(dfParts.col("category_id")), dfParts);
System.out.println("Number of rows updated: " + updateResult.getRowsUpdated());
```

### Deleting Rows in a Table

For the `delete` method, you can specify a condition that identifies the rows to delete, and you can base that condition on
a join with another DataFrame. `delete` returns a `DeleteResult` object, which contains the
number of rows that were deleted. (See [DeleteResult](../reference/scala/com/snowflake/snowpark/DeleteResult.html).)

Note

`delete` is an [action method](#label-snowpark-java-dataframe-action-method), which means that calling the method sends
SQL statements to the server for execution.

For example, to delete the rows that have the value `1` in the `category_id` column:

Copy code

```
Updatable updatableDf = session.table("sample_product_data");
DeleteResult deleteResult = updatableDf.delete(updatableDf.col("category_id").equal_to(Functions.lit(1)));
System.out.println("Number of rows deleted: " + deleteResult.getRowsDeleted());
```

If the condition refers to columns in a different DataFrame, pass that DataFrame in as the second argument. For example, to delete
the rows in which the `category_id` column matches the `category_id` in the `DataFrame` `dfParts`, pass in `dfParts`
as the second argument:

Copy code

```
Updatable updatableDf = session.table("sample_product_data");
DeleteResult deleteResult = updatableDf.delete(updatableDf.col("category_id").equal_to(dfParts.col("category_id")), dfParts);
System.out.println("Number of rows deleted: " + deleteResult.getRowsDeleted());
```

### Merging Rows into a Table

To insert, update, and delete rows in one table based on values in a second table or a subquery (the equivalent of the
[MERGE](/sql-reference/sql/merge) command in SQL), do the following:

1. In the `Updatable` object for the table where you want the data merged in, call the `merge` method, passing in
   the `DataFrame` object for the other table and the column expression for the join condition.

   This returns a `MergeBuilder` object that you can use to specify the actions to take (e.g. insert, update, or delete) on
   the rows that match and the rows that don’t match. (See [MergeBuilder](../reference/scala/com/snowflake/snowpark/MergeBuilder.html).)
2. Using the `MergeBuilder` object:

   - To specify the update or deletion that should be performed on matching rows, call the `whenMatched` method.

     If you need to specify an additional condition when rows should be updated or deleted, you can pass in a column expression for
     that condition.

     This method returns a `MatchedClauseBuilder` object that you can use to specify the action to perform. (See
     [MatchedClauseBuilder](../reference/scala/com/snowflake/snowpark/MatchedClauseBuilder.html).)

     Call the `update` or `delete` method in the `MatchedClauseBuilder` object to specify the update or delete
     action that should be performed on matching rows. These methods return a `MergeBuilder` object that you can use to
     specify additional clauses.
   - To specify the insert that should be performed when rows do not match, call the `whenNotMatched` method.

     If you need to specify an additional condition when rows should be inserted, you can pass in a column expression for that
     condition.

     This method returns a `NotMatchedClauseBuilder` object that you can use to specify the action to perform. (See
     [NotMatchedClauseBuilder](../reference/scala/com/snowflake/snowpark/NotMatchedClauseBuilder.html).)

     Call the `insert` method in the `NotMatchedClauseBuilder` object to specify the insert action that should be
     performed when rows do not match. These methods return a `MergeBuilder` object that you can use to specify additional
     clauses.
3. When you are done specifying the inserts, updates, and deletions that should be performed, call the `collect` method of
   the `MergeBuilder` object to perform the specified inserts, updates, and deletions on the table.

   `collect` returns a `MergeResult` object, which contains the number of rows that were inserted, updated, and
   deleted. (See [MergeResult](../reference/scala/com/snowflake/snowpark/MergeResult.html).)

The following example inserts a row with the `id` and `value` columns from the `source` table into the `target` table if
the `target` table does not contain a row with a matching ID:

Copy code

```
MergeResult mergeResult = target.merge(source, target.col("id").equal_to(source.col("id")))
                    .whenNotMatched().insert(new Column[]{source.col("id"), source.col("value")})
                    .collect();
```

The following example updates a row in the `target` table with the value of the `value` column from the row in the `source`
table that has the same ID:

Copy code

```
import java.util.HashMap;
import java.util.Map;
...
Map<String, Column> assignments = new HashMap<>();
assignments.put("value", source.col("value"));
MergeResult mergeResult = target.merge(source, target.col("id").equal_to(source.col("id")))
                    .whenMatched().update(assignments)
                    .collect();
```

## Saving Data to a Table

You can save the contents of a DataFrame to a new or existing table. In order to do this, you must have the following privileges:

- CREATE TABLE privileges on the schema, if the table does not exist.
- INSERT privileges on the table.

To save the contents of a DataFrame to a table:

1. Call the [write](../reference/java/com/snowflake/snowpark_java/DataFrame.html#write()) method of the DataFrame to get a [DataFrameWriter](../reference/scala/com/snowflake/snowpark/DataFrameWriter.html) object.
2. Call the [mode](../reference/java/com/snowflake/snowpark_java/DataFrameWriter.html#mode(com.snowflake.snowpark_java.SaveMode)) method of the `DataFrameWriter` object, passing in a [SaveMode](../reference/scala/com/snowflake/snowpark/SaveMode$.html) object that specifies your preferences
   for writing to the table:

   - To insert rows, pass in `SaveMode.Append`.
   - To overwrite the existing table, pass in `SaveMode.Overwrite`.

   This method returns the same `DataFrameWriter` object configured with the specified mode.
3. If you are inserting rows into an existing table (`SaveMode.Append`) and the column names in the DataFrame match the
   column names in the table, call the [DataFrameWriter.option](../reference/scala/com/snowflake/snowpark/DataFrameWriter.html#option(key:String,value:Any):com.snowflake.snowpark.DataFrameWriter), passing in `"columnOrder"` and `"name"` as
   arguments.

   Note

   This method was introduced in Snowpark 1.4.0.

   By default, the `columnOrder` option is set to `"index"`, which means that the `DataFrameWriter` inserts the
   values in the order that the columns appear. For example, the `DataFrameWriter` inserts the value from the first column
   from the DataFrame in the first column in the table, the second column from the DataFrame in the second column in the table,
   etc.

   This method returns the same `DataFrameWriter` object configured with the specified option.
4. Call the [saveAsTable](../reference/java/com/snowflake/snowpark_java/DataFrameWriter.html#saveAsTable(java.lang.String)) method of the `DataFrameWriter` object to save the contents of the DataFrame to a specified
   table.

   You do not need to call a separate method (e.g. `collect`) to execute the SQL statement that saves the data to the table.
   `saveAsTable` is an [action method](#label-snowpark-java-dataframe-action-method) that executes the SQL statement.

The following example overwrites an existing table (identified by the `tableName` variable) with the contents of the DataFrame
`df`:

Copy code

```
df.write().mode(SaveMode.Overwrite).saveAsTable(tableName);
```

The following example inserts rows from the DataFrame `df` into an existing table (identified by the `tableName` variable).
In this example, the table and the DataFrame both contain the columns `c1` and `c2`.

The example demonstrates the difference between setting the `columnOrder` option to `"name"` (which inserts values
into the table columns with the same names as the DataFrame columns) and using the default `columnOrder` option (which
inserts values into the table columns based on the order of the columns in the DataFrame).

Copy code

```
DataFrame df = session.sql("SELECT 1 AS c2, 2 as c1");
// With the columnOrder option set to "name", the DataFrameWriter uses the column names
// and inserts a row with the values (2, 1).
df.write().mode(SaveMode.Append).option("columnOrder", "name").saveAsTable(tableName);
// With the default value of the columnOrder option ("index"), the DataFrameWriter uses the column positions
// and inserts a row with the values (1, 2).
df.write().mode(SaveMode.Append).saveAsTable(tableName);
```

## Creating a View From a DataFrame

To create a view from a DataFrame, call the [createOrReplaceView](../reference/java/com/snowflake/snowpark_java/DataFrame.html#createOrReplaceView(java.lang.String)) method:

Copy code

```
df.createOrReplaceView("db.schema.viewName");
```

Note that calling `createOrReplaceView` immediately creates the new view. More importantly, it does not
cause the DataFrame to be evaluated. (The DataFrame itself is not evaluated until you
[perform an action](#label-snowpark-java-dataframe-action-method).)

Views that you create by calling `createOrReplaceView` are persistent. If you no longer need that view, you can
[drop the view manually](/sql-reference/sql/drop-view).

If you need to create a temporary view just for the session, call the [createOrReplaceTempView](../reference/java/com/snowflake/snowpark_java/DataFrame.html#createOrReplaceTempView(java.lang.String)) method instead:

Copy code

```
df.createOrReplaceTempView("db.schema.viewName");
```

## Caching a DataFrame

In some cases, you may need to perform a complex query and keep the results for use in subsequent operations (rather than
executing the same query again). In these cases, you can cache the contents of a DataFrame by calling the [cacheResult](../reference/java/com/snowflake/snowpark_java/DataFrame.html#cacheResult()) method.

This method:

- Runs the query.

  You do not need to [call a separate action method to retrieve the results](#label-snowpark-java-dataframe-retrieve-results)
  before calling `cacheResult`. `cacheResult` is an action method that executes the query.
- Saves the results in a temporary table

  Because `cacheResult` creates a temporary table, you must have the CREATE TABLE privilege on the schema that is in use.
- Returns a [HasCachedResult](../reference/scala/com/snowflake/snowpark/HasCachedResult.html) object, which provides access to the results in the temporary table.

  Because `HasCachedResult` extends `DataFrame`, you can perform some of the same operations on this cached data as
  you can perform on a DataFrame.

Note

Because `cacheResult` executes the query and saves the results to a table, the method can result in increased compute and
storage costs.

For example:

Copy code

```
// Set up a DataFrame to query a table.
DataFrame df = session.table("sample_product_data").filter(Functions.col("category_id").gt(Functions.lit(10)));
// Retrieve the results and cache the data.
HasCachedResult cachedDf = df.cacheResult();
// Create a DataFrame containing a subset of the cached data.
DataFrame dfSubset = cachedDf.filter(Functions.col("category_id").equal_to(Functions.lit(20))).select(Functions.col("name"), Functions.col("category_id"));
dfSubset.show();
```

Note that the original DataFrame is not affected when you call this method. For example, suppose that `dfTable` is a DataFrame
for the table `sample_product_data`:

Copy code

```
HasCachedResult dfTempTable = dfTable.cacheResult();
```

After you call `cacheResult`, `dfTable` still points to the `sample_product_data` table, and you can continue to use
`dfTable` to query and update that table.

To use the cached data in the temporary table, you use `dfTempTable` (the `HasCachedResult` object returned by
`cacheResult`).

## Working With Files in a Stage

The Snowpark library provides classes and methods that you can use to [load data into Snowflake](/guides-overview-loading-data) and
[unload data from Snowflake](/user-guide/data-unload-overview) by using files in stages.

Note

In order to use these classes and methods on a stage, you must have the required
[privileges for working with the stage](/user-guide/security-access-control-privileges#label-access-control-privileges-stage).

The next sections explain how to use these classes and methods:

- [Uploading and Downloading Files in a Stage](#label-snowpark-java-dataframe-stages-file-operation)
- [Using Input Streams to Upload and Download Data in a Stage](#label-snowpark-java-dataframe-stages-file-operation-streams)
- [Setting Up a DataFrame for Files in a Stage](#label-snowpark-java-dataframe-stages-query)
- [Loading Data from Files into a DataFrame](#label-snowpark-java-dataframe-stages-collect)
- [Copying Data from Files into a Table](#label-snowpark-java-dataframe-stages-copy-into-table)
- [Saving a DataFrame to Files on a Stage](#label-snowpark-java-dataframe-stages-copy-into-location)

### Uploading and Downloading Files in a Stage

To upload and download files in a stage, use the `put` and `get` methods of the [FileOperation](../reference/scala/com/snowflake/snowpark/FileOperation.html) object:

- [Uploading Files to a Stage](#label-snowpark-java-dataframe-stages-file-put)
- [Downloading Files from a Stage](#label-snowpark-java-dataframe-stages-file-get)

#### Uploading Files to a Stage

To upload files to a stage:

1. Verify that you have the [privileges to upload files to the stage](/user-guide/security-access-control-privileges#label-access-control-privileges-stage).
2. Use the [file](../reference/java/com/snowflake/snowpark_java/Session.html#file()) method of the `Session` object to access the [FileOperation](../reference/scala/com/snowflake/snowpark/FileOperation.html) object for the session.
3. Call the [put](../reference/java/com/snowflake/snowpark_java/FileOperation.html#put(java.lang.String,java.lang.String,java.util.Map)) method of the `FileOperation` object to upload the files to a stage.

   This method executes a SQL [PUT](/sql-reference/sql/put) command.

   - To specify any [optional parameters](/sql-reference/sql/put#label-put-optional-parameters) for the PUT command, create a `Map` of the
     parameters and values, and pass in the `Map` as the `options` argument. For example:

     Copy code

     ```
     import java.util.HashMap;
     import java.util.Map;
     ...
     // Upload a file to a stage without compressing the file.
     Map<String, String> putOptions = new HashMap<>();
     putOptions.put("AUTO_COMPRESS", "FALSE");
     PutResult[] putResults = session.file().put("file:///tmp/myfile.csv", "@myStage", putOptions);
     ```
   - In the `localFileName` argument, you can use wildcards (`*` and `?`) to identify a set of files to upload. For
     example:

     Copy code

     ```
     // Upload the CSV files in /tmp with names that start with "file".
     // You can use the wildcard characters "*" and "?" to match multiple files.
     PutResult[] putResults = session.file().put("file:///tmp/file*.csv", "@myStage/prefix2");
     ```
4. Check the `Array` of [PutResult](../reference/scala/com/snowflake/snowpark/PutResult.html) objects returned by the `put` method to determine if the files were successfully
   uploaded. For example, to print the filename and the status of the PUT operation for that file:

   Copy code

   ```
   // Print the filename and the status of the PUT operation.
   for (PutResult result : putResults) {
     System.out.println(result.getSourceFileName() + ": " + result.getStatus());
   }
   ```

#### Downloading Files from a Stage

To download files from a stage:

1. Verify that you have the [privileges to download files from the stage](/user-guide/security-access-control-privileges#label-access-control-privileges-stage).
2. Use the [file](../reference/java/com/snowflake/snowpark_java/Session.html#file()) method of the `Session` object to access the [FileOperation](../reference/scala/com/snowflake/snowpark/FileOperation.html) object for the session.
3. Call the [get](../reference/scala/com/snowflake/snowpark/functions$.html#get(col1:com.snowflake.snowpark.Column,col2:com.snowflake.snowpark.Column):com.snowflake.snowpark.Column) method of the `FileOperation` object to download the files from a stage.

   This method executes a SQL [GET](/sql-reference/sql/get) command.

   To specify any [optional parameters](/sql-reference/sql/get#label-get-optional-parameters) for the GET command, create a `Map` of the
   parameters and values, and pass in the `Map` as the `options` argument. For example:

   Copy code

   ```
   import java.util.HashMap;
   import java.util.Map;
   ...
   // Upload a file to a stage without compressing the file.
   // Download files with names that match a regular expression pattern.
   Map<String, String> getOptions = new HashMap<>();
   getOptions.put("PATTERN", "'.*file_.*.csv.gz'");
   GetResult[] getResults = session.file().get("@myStage", "file:///tmp", getOptions);
   ```
4. Check the `Array` of [GetResult](https://docs.snowflake.com/en/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/GetResult.html) objects returned by the `get` method to determine if the files were successfully
   downloaded. For example, to print the filename and the status of the GET operation for that file:

   Copy code

   ```
   // Print the filename and the status of the GET operation.
   for (GetResult result : getResults) {
     System.out.println(result.getFileName() + ": " + result.getStatus());
   }
   ```

### Using Input Streams to Upload and Download Data in a Stage

Note

This feature was introduced in Snowpark 1.4.0.

To use input streams to upload data to a file on a stage and download data from a file on a stage, use the `uploadStream`
and `downloadStream` methods of the [FileOperation](../reference/scala/com/snowflake/snowpark/FileOperation.html) object:

- [Using an Input Stream to Upload Data to a File on a Stage](#label-snowpark-java-dataframe-stages-file-streams-upload)
- [Using an Input Stream to Download Data from a File on a Stage](#label-snowpark-java-dataframe-stages-file-streams-download)

#### Using an Input Stream to Upload Data to a File on a Stage

To upload the data from a [java.io.InputStream](https://docs.oracle.com/en/java/javase/11/docs/api/java.base/java/io/InputStream.html) object to a file on a stage:

1. Verify that you have the [privileges to upload files to the stage](/user-guide/security-access-control-privileges#label-access-control-privileges-stage).
2. Use the [file](../reference/java/com/snowflake/snowpark_java/Session.html#file()) method of the `Session` object to access the [FileOperation](../reference/scala/com/snowflake/snowpark/FileOperation.html) object for the session.
3. Call the [uploadStream](../reference/java/com/snowflake/snowpark_java/FileOperation.html#uploadStream(java.lang.String,java.io.InputStream,boolean)) method of the `FileOperation` object.

   Pass in the complete path to the file on the stage where the data should be written and the `InputStream` object. In
   addition, use the `compress` argument to specify whether or not the data should be compressed before it is uploaded.

For example:

Copy code

```
import java.io.InputStream;
...
boolean compressData = true;
String pathToFileOnStage = "@myStage/path/file";
session.file().uploadStream(pathToFileOnStage, new ByteArrayInputStream(fileContent.getBytes()), compressData);
```

#### Using an Input Stream to Download Data from a File on a Stage

To download data from a file on a stage to a [java.io.InputStream](https://docs.oracle.com/en/java/javase/11/docs/api/java.base/java/io/InputStream.html) object:

1. Verify that you have the [privileges to download files from the stage](/user-guide/security-access-control-privileges#label-access-control-privileges-stage).
2. Use the [file](../reference/java/com/snowflake/snowpark_java/Session.html#file()) method of the `Session` object to access the [FileOperation](../reference/scala/com/snowflake/snowpark/FileOperation.html) object for the session.
3. Call the [downloadStream](../reference/java/com/snowflake/snowpark_java/FileOperation.html#downloadStream(java.lang.String,boolean)) method of the `FileOperation` object.

   Pass in the complete path to the file on the stage containing the data to download. Use the `decompress` argument to
   specify whether or not the data in the file is compressed.

For example:

Copy code

```
import java.io.InputStream;
...
boolean isDataCompressed = true;
String pathToFileOnStage = "@myStage/path/file";
InputStream is = session.file().downloadStream(pathToFileOnStage, isDataCompressed);
```

### Setting Up a DataFrame for Files in a Stage

This section explains how to set up a DataFrame for files in a Snowflake stage. Once you create this DataFrame, you can use the
DataFrame to:

- [retrieve data from the files](#label-snowpark-java-dataframe-stages-collect)
- [copy data from the files into a table](#label-snowpark-java-dataframe-stages-copy-into-table)

To set up a DataFrame for files in a Snowflake stage, use the `DataFrameReader` class:

1. Verify that you have the following privileges:

   - [Privileges to access files in the stage](/user-guide/security-access-control-privileges#label-access-control-privileges-stage).
   - One of the following:
     - CREATE TABLE privileges on the schema, if you plan to specify
       [copy options](/developer-guide/snowpark/java/working-with-dataframes#label-snowpark-java-dataframe-stages-copy-options) that determine how data is copied from the staged files.
     - CREATE FILE FORMAT privileges on the schema, otherwise.
2. Call the `read` method in the `Session` class to access a `DataFrameReader` object.
3. If the files are in CSV format, describe the fields in the file. To do this:

   1. Create a [StructType](../reference/scala/com/snowflake/snowpark/types/StructType$.html) object that consists of an array of [StructField](../reference/scala/com/snowflake/snowpark/types/StructField$.html) objects that describe the fields in the file.
   2. For each `StructField` object, specify the following:

      - The name of the field.
      - The data type of the field (specified as an object in the `com.snowflake.snowpark_java.types` package).
      - Whether or not the field is nullable.

      For example:

      Copy code

      ```
      import com.snowflake.snowpark_java.types.*;
      ...

      StructType schemaForDataFile = StructType.create(
        new StructField("id", DataTypes.StringType, true),
        new StructField("name", DataTypes.StringType, true));
      ```
   3. Call the `schema` method in the `DataFrameReader` object, passing in the `StructType` object.

      For example:

      Copy code

      ```
      DataFrameReader dfReader = session.read().schema(schemaForDataFile);
      ```

      The `schema` method returns a `DataFrameReader` object that is configured to read files containing the specified
      fields.

      Note that you do not need to do this for files in other formats (such as JSON). For those files, the
      `DataFrameReader` treats the data as a single field of the VARIANT type with the field name `$1`.
4. If you need to specify additional information about how the data should be read (for example, that the data is compressed or
   that a CSV file uses a semicolon instead of a comma to delimit fields), call the [DataFrameReader.option](../reference/scala/com/snowflake/snowpark/DataFrameReader.html#option(key:String,value:Any):com.snowflake.snowpark.DataFrameReader) method or the
   [DataFrameReader.options](../reference/scala/com/snowflake/snowpark/DataFrameReader.html#options(configs:Map%5BString,Any%5D):com.snowflake.snowpark.DataFrameReader) method.

   Pass in the name and value of the option that you want to set. You can set the following types of options:

   - The [file format options](/sql-reference/sql/create-file-format#label-create-file-format-formattypeoptions) described in the
     [documentation on CREATE FILE FORMAT](/sql-reference/sql/create-file-format).
   - The [copy options](/sql-reference/sql/copy-into-table#label-copy-into-table-copyoptions) described in the
     [COPY INTO TABLE documentation](/sql-reference/sql/copy-into-table).

     Note that setting copy options can result in a more expensive execution strategy when you
     [retrieve the data into the DataFrame](#label-snowpark-java-dataframe-action-method).

   The following example sets up the `DataFrameReader` object to query data in a CSV file that is not compressed and that
   uses a semicolon for the field delimiter.

   Copy code

   ```
   dfReader = dfReader.option("field_delimiter", ";").option("COMPRESSION", "NONE");
   ```

   The `option` method returns a `DataFrameReader` object that is configured with the specified options.

   To set multiple options, you can either
   [chain calls](#label-snowpark-java-dataframe-chaining-method-calls) to the `option` method (as shown in the example
   above) or call the [DataFrameReader.options](../reference/scala/com/snowflake/snowpark/DataFrameReader.html#options(configs:Map%5BString,Any%5D):com.snowflake.snowpark.DataFrameReader) method, passing in a `Map` of the names and values of the options.
5. Call the method corresponding to the format of the files. You can call one of the following methods:

   - [DataFrameReader.avro](../reference/scala/com/snowflake/snowpark/DataFrameReader.html#avro(path:String):com.snowflake.snowpark.CopyableDataFrame)
   - [DataFrameReader.csv](../reference/scala/com/snowflake/snowpark/DataFrameReader.html#csv(path:String):com.snowflake.snowpark.CopyableDataFrame)
   - [DataFrameReader.json](../reference/scala/com/snowflake/snowpark/DataFrameReader.html#json(path:String):com.snowflake.snowpark.CopyableDataFrame)
   - [DataFrameReader.orc](../reference/scala/com/snowflake/snowpark/DataFrameReader.html#orc(path:String):com.snowflake.snowpark.CopyableDataFrame)
   - [DataFrameReader.parquet](../reference/scala/com/snowflake/snowpark/DataFrameReader.html#parquet(path:String):com.snowflake.snowpark.CopyableDataFrame)
   - [DataFrameReader.xml](../reference/scala/com/snowflake/snowpark/DataFrameReader.html#parquet(path:String):com.snowflake.snowpark.CopyableDataFrame)

   When calling these methods, pass in the stage location of the files to be read. For example:

   Copy code

   ```
   DataFrame df = dfReader.csv("@mystage/myfile.csv");
   ```

   To specify multiple files that start with the same prefix, specify the prefix after the stage name. For example, to load files
   that have the prefix `csv_` from the stage `@mystage`:

   Copy code

   ```
   DataFrame df = dfReader.csv("@mystage/csv_");
   ```

   The methods corresponding to the format of a file return a [CopyableDataFrame](../reference/scala/com/snowflake/snowpark/CopyableDataFrame.html) object for that file. `CopyableDataFrame`
   extends `DataFrame` and provides additional methods for working the data in staged files.
6. Call an action method to:

   - [retrieve data from the files](#label-snowpark-java-dataframe-stages-collect), or
   - [copy data from the files into a table](#label-snowpark-java-dataframe-stages-copy-into-table)

   As is the case with DataFrames for tables, the data is not retrieved into the DataFrame until you call
   [an action method](#label-snowpark-java-dataframe-action-method).

### Loading Data from Files into a DataFrame

After you [set up a DataFrame for files in a stage](#label-snowpark-java-dataframe-stages-query), you can load data from the
files into the DataFrame:

1. Use the DataFrame object methods to [perform any transformations](#label-snowpark-java-dataframe-transform) needed on the
   dataset (for example, selecting specific fields, filtering rows, etc.).

   For example, to extract the `color` element from a JSON file named `data.json` in the stage named `mystage`:

   Copy code

   ```
   DataFrame df = session.read().json("@mystage/data.json").select(Functions.col("$1").subField("color"));
   ```

   As explained earlier, for files in formats other than CSV (e.g. JSON), the `DataFrameReader` treats the data in the file
   as a single VARIANT column with the name `$1`.
2. Call the `DataFrame.collect` method to load the data. For example:

   Copy code

   ```
   Row[] results = df.collect();
   ```

### Copying Data from Files into a Table

After you [set up a DataFrame for files in a stage](#label-snowpark-java-dataframe-stages-query), you can call the
[copyInto](../reference/java/com/snowflake/snowpark_java/CopyableDataFrame.html#copyInto(java.lang.String)) method to copy the data into a table. This method executes the [COPY INTO <table>](/sql-reference/sql/copy-into-table) command.

Note

You do not need to call the `collect` method before calling `copyInto`. The data from the files does not need to
be in the DataFrame before you call `copyInto`.

For example, the following code loads data from the CSV file specified by `myFileStage` into the table `mytable`. Because the
data is in a CSV file, the code must also [describe the fields in the file](/developer-guide/snowpark/java/working-with-dataframes#label-snowpark-java-dataframe-stages-csv-schema). The example does this by calling the [schema](../reference/java/com/snowflake/snowpark_java/DataFrameReader.html#schema(com.snowflake.snowpark_java.types.StructType)) method of the
`DataFrameReader` object and passing in a [StructType](../reference/scala/com/snowflake/snowpark/types/StructType$.html) object (`schemaForDataFile`) containing an array of
[StructField](../reference/scala/com/snowflake/snowpark/types/StructField$.html) objects that describe the fields.

Copy code

```
CopyableDataFrame copyableDf = session.read().schema(schemaForDataFile).csv("@mystage/myfile.csv");
copyableDf.copyInto("mytable");
```

### Saving a DataFrame to Files on a Stage

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Note

This feature was introduced in Snowpark 1.5.0.

If you need to save a DataFrame to files on a stage, you can call the [DataFrameWriter](../reference/scala/com/snowflake/snowpark/DataFrameWriter.html) method corresponding to the format of
the file (e.g. the `csv` method to write to a CSV file), passing in the stage location where the files should be saved.
These `DataFrameWriter` methods execute the [COPY INTO <location>](/sql-reference/sql/copy-into-location) command.

Note

You do not need to call the `collect` method before calling these `DataFrameWriter` methods. The data from the file
does not need to be in the DataFrame before you call these methods.

To save the contents of a DataFrame to files on a stage:

1. Call the [write](../reference/java/com/snowflake/snowpark_java/DataFrame.html#write()) method of the DataFrame object to get a [DataFrameWriter](../reference/scala/com/snowflake/snowpark/DataFrameWriter.html) object. For example, to get the
   `DataFrameWriter` object for a DataFrame that represents the table named `sample_product_data`:

   Copy code

   ```
   DataFrameWriter dfWriter = session.table("sample_product_data").write();
   ```
2. If you want to overwrite the contents of the file (if the file exists), call the [mode](../reference/java/com/snowflake/snowpark_java/DataFrameWriter.html#mode(com.snowflake.snowpark_java.SaveMode)) method of the `DataFrameWriter`
   object, passing in `SaveMode.Overwrite`.

   Otherwise, by default, the `DataFrameWriter` reports an error if the specified file on the stage already exists.

   The `mode` method returns the same `DataFrameWriter` object configured with the specified mode.

   For example, to specify that the `DataFrameWriter` should overwrite the file on the stage:

   Copy code

   ```
   dfWriter = dfWriter.mode(SaveMode.Overwrite);
   ```
3. If you need to specify additional information about how the data should be saved (for example, that the data should be
   compressed or that you want to use a semicolon to delimit fields in a CSV file), call the [DataFrameWriter.option](../reference/scala/com/snowflake/snowpark/DataFrameWriter.html#option(key:String,value:Any):com.snowflake.snowpark.DataFrameWriter) method
   or the [DataFrameWriter.options](../reference/scala/com/snowflake/snowpark/DataFrameWriter.html#options(configs:Map%5BString,Any%5D):com.snowflake.snowpark.DataFrameWriter) method.

   Pass in the name and value of the option that you want to set. You can set the following types of options:

   - The [file format options](/sql-reference/sql/copy-into-location#label-copy-into-location-formattypeoptions) described in the
     [documentation on COPY INTO <location>](/sql-reference/sql/copy-into-location).
   - The [copy options](/sql-reference/sql/copy-into-location#label-copy-into-location-copyoptions) described in the
     documentation on COPY INTO <location>.
   - [PARTITION BY or HEADER](/sql-reference/sql/copy-into-location#label-copy-into-location-optional-parameters).

   Note that you can’t use the `option` method to set the following options:

   - The TYPE format type option.
   - The OVERWRITE copy option. To set this option, call the `mode` method instead (as mentioned in the previous step).

   The following example sets up the `DataFrameWriter` object to save data to a CSV file in uncompressed form, using a
   semicolon (rather than a comma) as the field delimiter.

   Copy code

   ```
   dfWriter = dfWriter.option("field_delimiter", ";").option("COMPRESSION", "NONE");
   ```

   The `option` method returns a `DataFrameWriter` object that is configured with the specified option.

   To set multiple options, you can
   [chain calls](#label-snowpark-java-dataframe-chaining-method-calls) to the `option` method (as shown in the example
   above) or call the [DataFrameWriter.options](../reference/scala/com/snowflake/snowpark/DataFrameWriter.html#options(configs:Map%5BString,Any%5D):com.snowflake.snowpark.DataFrameWriter) method, passing in a `Map` of the names and values of the options.
4. To return details about each file that was saved, set the `DETAILED_OUTPUT`
   [copy option](/sql-reference/sql/copy-into-location#label-copy-into-location-copyoptions) to `TRUE`.

   By default, `DETAILED_OUTPUT` is `FALSE`, which means that the method returns a single row of output containing the
   fields `"rows_unloaded"`, `"input_bytes"`, and `"output_bytes"`.

   When you set `DETAILED_OUTPUT` to `TRUE`, the method returns a row of output for each file saved. Each row contains
   the fields `FILE_NAME`, `FILE_SIZE`, and `ROW_COUNT`.
5. Call the method corresponding to the format of the file to save the data to the file. You can call one of the following
   methods:

   - [DataFrameWriter.csv](../reference/scala/com/snowflake/snowpark/DataFrameWriter.html#csv(path:String):com.snowflake.snowpark.WriteFileResult)
   - [DataFrameWriter.json](../reference/scala/com/snowflake/snowpark/DataFrameWriter.html#json(path:String):com.snowflake.snowpark.WriteFileResult)
   - [DataFrameWriter.parquet](../reference/scala/com/snowflake/snowpark/DataFrameWriter.html#parquet(path:String):com.snowflake.snowpark.WriteFileResult)

   When calling these methods, pass in the stage location of the file where the data should be written (e.g. `@mystage`).

   By default, the method saves the data to filenames with the prefix `data_` (e.g. `@mystage/data_0_0_0.csv`). If you want
   the files to be named with a different prefix, specify the prefix after the stage name. For example:

   Copy code

   ```
   WriteFileResult writeFileResult = dfWriter.csv("@mystage/saved_data");
   ```

   This example saves the contents of the DataFrame to files that begin with the prefix `saved_data` (e.g.
   `@mystage/saved_data_0_0_0.csv`).
6. Check the [WriteFileResult](../reference/scala/com/snowflake/snowpark/WriteFileResult.html) object returned for information about the amount of data written to the file.

   From the `WriteFileResult` object, you can access the output produced by the COPY INTO <location> command:

   - To access the rows of output as an array of [Row](../reference/scala/com/snowflake/snowpark/Row.html) objects, call the `getRows` method.
   - To determine which fields are present in the rows, call the `getSchema` method, which returns a [StructType](../reference/scala/com/snowflake/snowpark/types/StructType$.html) that
     describes the fields in the row.

   For example, to print out the names of the fields and values in the output rows:

   Copy code

   ```
   WriteFileResult writeFileResult = dfWriter.csv("@mystage/saved_data");
   Row[] rows = writeFileResult.getRows();
   StructType schema = writeFileResult.getSchema();
   for (int i = 0 ; i < rows.length ; i++) {
     System.out.println("Row:" + i);
     Row row = rows[i];
     for (int j = 0; j < schema.size(); j++) {
    System.out.println(schema.get(j).name() + ": " + row.get(j));
     }
   }
   ```

The following example uses a DataFrame to save the contents of the table named `car_sales` to JSON files with the prefix
`saved_data` on the stage `@mystage` (e.g. `@mystage/saved_data_0_0_0.json`). The sample code:

- Overwrites the file, if the file already exists on the stage.
- Returns detailed output about the save operation.
- Saves the data uncompressed.

Finally, the sample code prints out each field and value in the output rows returned:

Copy code

```
DataFrame df = session.table("car_sales");
WriteFileResult writeFileResult = df.write().mode(SaveMode.Overwrite).option("DETAILED_OUTPUT", "TRUE").option("compression", "none").json("@mystage/saved_data");
Row[] rows = writeFileResult.getRows();
StructType schema = writeFileResult.getSchema();
for (int i = 0 ; i < rows.length ; i++) {
  System.out.println("Row:" + i);
  Row row = rows[i];
  for (int j = 0; j < schema.size(); j++) {
    System.out.println(schema.get(j).name() + ": " + row.get(j));
  }
}
```

## Working with Semi-Structured Data

Using a DataFrame, you can query and access [semi-structured data](/user-guide/semistructured-intro) (e.g JSON data). The
next sections explain how to work with semi-structured data in a DataFrame.

- [Traversing Semi-Structured Data](#label-snowpark-java-dataframe-semistructured-traverse)
- [Explicitly Casting Values in Semi-Structured Data](#label-snowpark-java-dataframe-semistructured-cast)
- [Flattening an Array of Objects into Rows](#label-snowpark-java-dataframe-semistructured-flatten)

Note

The examples in these sections use the sample data in [Sample Data Used in Examples](/user-guide/querying-semistructured#label-sample-data-semistructured-data).

### Traversing Semi-Structured Data

To refer to a specific field or element in semi-structured data, use the following methods of the [Column](../reference/scala/com/snowflake/snowpark/Column.html) object:

- Use [subField(“<field\_name>”)](../reference/java/com/snowflake/snowpark_java/Column.html#subField(java.lang.String)) to return a `Column` object for a field in an OBJECT (or a VARIANT that contains an
  OBJECT).
- Use [subField(<index>)](../reference/java/com/snowflake/snowpark_java/Column.html#subField(int)) to return a `Column` object for an element in an ARRAY (or a VARIANT that contains an ARRAY).

Note

If the field name or elements in the path are irregular and make it difficult to use the `Column.apply` methods, you can
use [Functions.get](../reference/java/com/snowflake/snowpark_java/Functions.html#get(com.snowflake.snowpark_java.Column,com.snowflake.snowpark_java.Column)), [Functions.get\_ignore\_case](../reference/java/com/snowflake/snowpark_java/Functions.html#get_ignore_case(com.snowflake.snowpark_java.Column,com.snowflake.snowpark_java.Column)), or [Functions.get\_path](../reference/java/com/snowflake/snowpark_java/Functions.html#get_path(com.snowflake.snowpark_java.Column,com.snowflake.snowpark_java.Column)) as an alternative.

For example, the following code selects the `dealership` field in objects in the `src` column of the
[sample data](/user-guide/querying-semistructured#label-sample-data-semistructured-data):

Copy code

```
DataFrame df = session.table("car_sales");
df.select(Functions.col("src").subField("dealership")).show();
```

The code prints the following output:

Copy code

```
----------------------------
|"""SRC""['DEALERSHIP']"   |
----------------------------
|"Valley View Auto Sales"  |
|"Tindel Toyota"           |
----------------------------
```

Note

The values in the DataFrame are surrounded by double quotes because these values are returned as string literals. To cast these
values to a specific type, see [Explicitly Casting Values in Semi-Structured Data](#label-snowpark-java-dataframe-semistructured-cast).

You can also [chain method calls](#label-snowpark-java-dataframe-chaining-method-calls) to traverse a path to a specific
field or element.

For example, the following code selects the `name` field in the `salesperson` object:

Copy code

```
DataFrame df = session.table("car_sales");
df.select(Functions.col("src").subField("salesperson").subField("name")).show();
```

The code prints the following output:

Copy code

```
------------------------------------
|"""SRC""['SALESPERSON']['NAME']"  |
------------------------------------
|"Frank Beasley"                   |
|"Greg Northrup"                   |
------------------------------------
```

As another example, the following code selects the first element of `vehicle` field, which holds an array of vehicles. The
example also selects the `price` field from the first element.

Copy code

```
DataFrame df = session.table("car_sales");
df.select(Functions.col("src").subField("vehicle").subField(0)).show();
df.select(Functions.col("src").subField("vehicle").subField(0).subField("price")).show();
```

The code prints the following output:

Copy code

```
---------------------------
|"""SRC""['VEHICLE'][0]"  |
---------------------------
|{                        |
|  "extras": [            |
|    "ext warranty",      |
|    "paint protection"   |
|  ],                     |
|  "make": "Honda",       |
|  "model": "Civic",      |
|  "price": "20275",      |
|  "year": "2017"         |
|}                        |
|{                        |
|  "extras": [            |
|    "ext warranty",      |
|    "rust proofing",     |
|    "fabric protection"  |
|  ],                     |
|  "make": "Toyota",      |
|  "model": "Camry",      |
|  "price": "23500",      |
|  "year": "2017"         |
|}                        |
---------------------------

------------------------------------
|"""SRC""['VEHICLE'][0]['PRICE']"  |
------------------------------------
|"20275"                           |
|"23500"                           |
------------------------------------
```

As an alternative to the `apply` method, you can use [Functions.get](../reference/java/com/snowflake/snowpark_java/Functions.html#get(com.snowflake.snowpark_java.Column,com.snowflake.snowpark_java.Column)), [Functions.get\_ignore\_case](../reference/java/com/snowflake/snowpark_java/Functions.html#get_ignore_case(com.snowflake.snowpark_java.Column,com.snowflake.snowpark_java.Column)), or
[Functions.get\_path](../reference/java/com/snowflake/snowpark_java/Functions.html#get_path(com.snowflake.snowpark_java.Column,com.snowflake.snowpark_java.Column)) functions if the field name or elements in the path are irregular and make it difficult to use the
`Column.subField` methods.

For example, the following lines of code both print the value of a specified field in an object:

Copy code

```
df.select(Functions.get(Functions.col("src"), Functions.lit("dealership"))).show();
df.select(Functions.col("src").subField("dealership")).show();
```

Similarly, the following lines of code both print the value of a field at a specified path in an object:

Copy code

```
df.select(Functions.get_path(Functions.col("src"), Functions.lit("vehicle[0].make"))).show();
df.select(Functions.col("src").subField("vehicle").subField(0).subField("make")).show();
```

### Explicitly Casting Values in Semi-Structured Data

By default, the values of fields and elements are returned as string literals (including the double quotes), as shown in the
examples above.

To avoid unexpected results, call the [cast](#label-snowpark-java-dataframe-cols-cast) method to cast the value to a specific
type. For example, the following code prints out the values without and with casting:

Copy code

```
// Import the objects for the data types, including StringType.
import com.snowflake.snowpark_java.types.*;
...
DataFrame df = session.table("car_sales");
df.select(Functions.col("src").subField("salesperson").subField("id")).show();
df.select(Functions.col("src").subField("salesperson").subField("id").cast(DataTypes.StringType)).show();
```

The code prints the following output:

Copy code

```
----------------------------------
|"""SRC""['SALESPERSON']['ID']"  |
----------------------------------
|"55"                            |
|"274"                           |
----------------------------------

---------------------------------------------------
|"CAST (""SRC""['SALESPERSON']['ID'] AS STRING)"  |
---------------------------------------------------
|55                                               |
|274                                              |
---------------------------------------------------
```

### Flattening an Array of Objects into Rows

If you need to “flatten” semi-structured data into a DataFrame (e.g. producing a row for every object in an array), call the
[flatten](../reference/java/com/snowflake/snowpark_java/DataFrame.html#flatten(com.snowflake.snowpark_java.Column)) method. This method is equivalent to the [FLATTEN](/sql-reference/functions/flatten) SQL function. If you pass in
a path to an object or array, the method returns a DataFrame that contains a row for each field or element in the object or array.

For example, in the [sample data](/user-guide/querying-semistructured#label-sample-data-semistructured-data), `src:customer` is an array of objects that
contain information about a customer. Each object contains a `name` and `address` field.

If you pass this path to the `flatten` function:

Copy code

```
DataFrame df = session.table("car_sales");
df.flatten(Functions.col("src").subField("customer")).show();
```

the method returns a DataFrame:

Copy code

```
----------------------------------------------------------------------------------------------------------------------------------------------------------
|"SRC"                                      |"SEQ"  |"KEY"  |"PATH"  |"INDEX"  |"VALUE"                            |"THIS"                               |
----------------------------------------------------------------------------------------------------------------------------------------------------------
|{                                          |1      |NULL   |[0]     |0        |{                                  |[                                    |
|  "customer": [                            |       |       |        |         |  "address": "San Francisco, CA",  |  {                                  |
|    {                                      |       |       |        |         |  "name": "Joyce Ridgely",         |    "address": "San Francisco, CA",  |
|      "address": "San Francisco, CA",      |       |       |        |         |  "phone": "16504378889"           |    "name": "Joyce Ridgely",         |
|      "name": "Joyce Ridgely",             |       |       |        |         |}                                  |    "phone": "16504378889"           |
|      "phone": "16504378889"               |       |       |        |         |                                   |  }                                  |
|    }                                      |       |       |        |         |                                   |]                                    |
|  ],                                       |       |       |        |         |                                   |                                     |
|  "date": "2017-04-28",                    |       |       |        |         |                                   |                                     |
|  "dealership": "Valley View Auto Sales",  |       |       |        |         |                                   |                                     |
|  "salesperson": {                         |       |       |        |         |                                   |                                     |
|    "id": "55",                            |       |       |        |         |                                   |                                     |
|    "name": "Frank Beasley"                |       |       |        |         |                                   |                                     |
|  },                                       |       |       |        |         |                                   |                                     |
|  "vehicle": [                             |       |       |        |         |                                   |                                     |
|    {                                      |       |       |        |         |                                   |                                     |
|      "extras": [                          |       |       |        |         |                                   |                                     |
|        "ext warranty",                    |       |       |        |         |                                   |                                     |
|        "paint protection"                 |       |       |        |         |                                   |                                     |
|      ],                                   |       |       |        |         |                                   |                                     |
|      "make": "Honda",                     |       |       |        |         |                                   |                                     |
|      "model": "Civic",                    |       |       |        |         |                                   |                                     |
|      "price": "20275",                    |       |       |        |         |                                   |                                     |
|      "year": "2017"                       |       |       |        |         |                                   |                                     |
|    }                                      |       |       |        |         |                                   |                                     |
|  ]                                        |       |       |        |         |                                   |                                     |
|}                                          |       |       |        |         |                                   |                                     |
|{                                          |2      |NULL   |[0]     |0        |{                                  |[                                    |
|  "customer": [                            |       |       |        |         |  "address": "New York, NY",       |  {                                  |
|    {                                      |       |       |        |         |  "name": "Bradley Greenbloom",    |    "address": "New York, NY",       |
|      "address": "New York, NY",           |       |       |        |         |  "phone": "12127593751"           |    "name": "Bradley Greenbloom",    |
|      "name": "Bradley Greenbloom",        |       |       |        |         |}                                  |    "phone": "12127593751"           |
|      "phone": "12127593751"               |       |       |        |         |                                   |  }                                  |
|    }                                      |       |       |        |         |                                   |]                                    |
|  ],                                       |       |       |        |         |                                   |                                     |
|  "date": "2017-04-28",                    |       |       |        |         |                                   |                                     |
|  "dealership": "Tindel Toyota",           |       |       |        |         |                                   |                                     |
|  "salesperson": {                         |       |       |        |         |                                   |                                     |
|    "id": "274",                           |       |       |        |         |                                   |                                     |
|    "name": "Greg Northrup"                |       |       |        |         |                                   |                                     |
|  },                                       |       |       |        |         |                                   |                                     |
|  "vehicle": [                             |       |       |        |         |                                   |                                     |
|    {                                      |       |       |        |         |                                   |                                     |
|      "extras": [                          |       |       |        |         |                                   |                                     |
|        "ext warranty",                    |       |       |        |         |                                   |                                     |
|        "rust proofing",                   |       |       |        |         |                                   |                                     |
|        "fabric protection"                |       |       |        |         |                                   |                                     |
|      ],                                   |       |       |        |         |                                   |                                     |
|      "make": "Toyota",                    |       |       |        |         |                                   |                                     |
|      "model": "Camry",                    |       |       |        |         |                                   |                                     |
|      "price": "23500",                    |       |       |        |         |                                   |                                     |
|      "year": "2017"                       |       |       |        |         |                                   |                                     |
|    }                                      |       |       |        |         |                                   |                                     |
|  ]                                        |       |       |        |         |                                   |                                     |
|}                                          |       |       |        |         |                                   |                                     |
----------------------------------------------------------------------------------------------------------------------------------------------------------
```

From this DataFrame, you can select the `name` and `address` fields from each object in the `VALUE` field:

Copy code

```
df.flatten(Functions.col("src").subField("customer")).select(Functions.col("value").subField("name"), Functions.col("value").subField("address")).show();
```

Copy code

```
-------------------------------------------------
|"""VALUE""['NAME']"   |"""VALUE""['ADDRESS']"  |
-------------------------------------------------
|"Joyce Ridgely"       |"San Francisco, CA"     |
|"Bradley Greenbloom"  |"New York, NY"          |
-------------------------------------------------
```

The following code adds to the previous example by
[casting the values to a specific type](#label-snowpark-java-dataframe-semistructured-cast) and changing the names of the columns:

Copy code

```
df.flatten(Functions.col("src").subField("customer")).select(Functions.col("value").subField("name").cast(DataTypes.StringType).as("Customer Name"), Functions.col("value").subField("address").cast(DataTypes.StringType).as("Customer Address")).show();
```

Copy code

```
-------------------------------------------
|"Customer Name"     |"Customer Address"  |
-------------------------------------------
|Joyce Ridgely       |San Francisco, CA   |
|Bradley Greenbloom  |New York, NY        |
-------------------------------------------
```

## Executing SQL Statements

To execute a SQL statement that you specify, call the `sql` method in the `Session` class, and pass in the statement
to be executed. The method returns a DataFrame.

Note that the SQL statement won’t be executed until you [call an action method](#label-snowpark-java-dataframe-action-method).

Copy code

```
import java.util.Arrays;

// Get the list of the files in a stage.
// The collect() method causes this SQL statement to be executed.
DataFrame dfStageFiles  = session.sql("ls @myStage");
Row[] files = dfStageFiles.collect();
System.out.println(Arrays.toString(files));

// Resume the operation of a warehouse.
// Note that you must call the collect method in order to execute
// the SQL statement.
session.sql("alter warehouse if exists myWarehouse resume if suspended").collect();

DataFrame tableDf = session.table("sample_product_data").select(Functions.col("id"), Functions.col("name"));
// Get the count of rows from the table.
long numRows = tableDf.count();
System.out.println("Count: " + numRows);
```

If you want to [call methods to transform the DataFrame](#label-snowpark-java-dataframe-transform) (e.g. filter, select,
etc.), note that these methods work only if the underlying SQL statement is a SELECT statement. The transformation methods are not
supported for other kinds of SQL statements.

Copy code

```
import java.util.Arrays;

DataFrame df = session.sql("select id, category_id, name from sample_product_data where id > 10");
// Because the underlying SQL statement for the DataFrame is a SELECT statement,
// you can call the filter method to transform this DataFrame.
Row[] results = df.filter(Functions.col("category_id").lt(Functions.lit(10))).select(Functions.col("id")).collect();
System.out.println(Arrays.toString(results));

// In this example, the underlying SQL statement is not a SELECT statement.
DataFrame dfStageFiles = session.sql("ls @myStage");
// Calling the filter method results in an error.
dfStageFiles.filter(...);
```
