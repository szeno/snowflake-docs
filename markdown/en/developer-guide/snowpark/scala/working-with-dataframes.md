# Working with DataFrames in Snowpark Scala

In Snowpark, the main way in which you query and process data is through a DataFrame. This topic explains how to work with
DataFrames.

To retrieve and manipulate data, you use the [DataFrame](../reference/scala/com/snowflake/snowpark/DataFrame.html) class. A DataFrame represents a relational dataset that is evaluated
lazily: it only executes when a specific action is triggered. In a sense, a DataFrame is like a query that needs to be evaluated
in order to retrieve data.

To retrieve data into a DataFrame:

1. [Construct a DataFrame, specifying the source of the data for the dataset](#label-snowpark-dataframe-construct).

   For example, you can create a DataFrame to hold data from a table, an external CSV file, or the execution of a SQL statement.
2. [Specify how the dataset in the DataFrame should be transformed](#label-snowpark-dataframe-transform).

   For example, you can specify which columns should be selected, how the rows should be filtered, how the results should be
   sorted and grouped, etc.
3. [Execute the statement to retrieve the data into the DataFrame](#label-snowpark-dataframe-action-method).

   In order to retrieve the data into the DataFrame, you must invoke a method that performs an action (for example, the
   `collect()` method).

The next sections explain these steps in more detail.

## Setting up the Examples for this Section

Some of the examples of this section use a DataFrame to query a table named `sample_product_data`. If you want to run these
examples, you can create this table and fill the table with some data by executing the following SQL statements:

Copy code

```
CREATE OR REPLACE TABLE sample_product_data (id INT, parent_id INT, category_id INT, name VARCHAR, serial_number VARCHAR, key INT, "3rd" INT);
INSERT INTO sample_product_data VALUES
    (1, 0, 5, 'Product 1', 'prod-1', 1, 10),
    (2, 1, 5, 'Product 1A', 'prod-1-A', 1, 20),
    (3, 1, 5, 'Product 1B', 'prod-1-B', 1, 30),
    (4, 0, 10, 'Product 2', 'prod-2', 2, 40),
    (5, 4, 10, 'Product 2A', 'prod-2-A', 2, 50),
    (6, 4, 10, 'Product 2B', 'prod-2-B', 2, 60),
    (7, 0, 20, 'Product 3', 'prod-3', 3, 70),
    (8, 7, 20, 'Product 3A', 'prod-3-A', 3, 80),
    (9, 7, 20, 'Product 3B', 'prod-3-B', 3, 90),
    (10, 0, 50, 'Product 4', 'prod-4', 4, 100),
    (11, 10, 50, 'Product 4A', 'prod-4-A', 4, 100),
    (12, 10, 50, 'Product 4B', 'prod-4-B', 4, 100);
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
  val dfTable = session.table("sample_product_data")

  // To print out the first 10 rows, call:
  //   dfTable.show()
  ```

  Note

  The `session.table` method returns an `Updatable` object. `Updatable` extends `DataFrame` and provides
  additional methods for working with data in the table (e.g. methods for updating and deleting data). See
  [Updating, Deleting, and Merging Rows in a Table](#label-snowpark-dataframe-updatable).
- To create a DataFrame from a sequence of values, call the `createDataFrame` method:

  Copy code

  ```
  // Create a DataFrame containing a sequence of values.
  // In the DataFrame, name the columns "i" and "s".
  val dfSeq = session.createDataFrame(Seq((1, "one"), (2, "two"))).toDF("i", "s")
  ```

  Note

  Words reserved by Snowflake are not valid as column names when constructing a DataFrame. For a list of reserved words, refer to
  [Reserved & limited keywords](/sql-reference/reserved-keywords).
- To create a DataFrame containing a range of values, call the `range` method:

  Copy code

  ```
  // Create a DataFrame from a range
  val dfRange = session.range(1, 10, 2)
  ```
- To [create a DataFrame for a file in a stage](#label-snowpark-dataframe-stages-query), call `read` to get a
  `DataFrameReader` object. In the `DataFrameReader` object, call the method corresponding to the format of the data
  in the file:

  Copy code

  ```
  // Create a DataFrame from data in a stage.
  val dfJson = session.read.json("@mystage2/data1.json")
  ```
- To create a DataFrame to hold the results of a SQL query, call the `sql` method:

  Copy code

  ```
  // Create a DataFrame from a SQL query
  val dfSql = session.sql("SELECT name from products")
  ```

  Note: Although you can use this method to execute SELECT statements that retrieve data from tables and staged files, you should
  use the `table` and `read` methods instead. Methods like `table` and `read` can provide better syntax
  highlighting, error highlighting, and intelligent code completion in development tools.

## Specifying How the Dataset Should Be Transformed

To specify which columns should be selected and how the results should be filtered, sorted, grouped, etc., call the DataFrame
methods that transform the dataset. To identify columns in these methods, use the `col` function or an expression that
evaluates to a column. (See [Specifying Columns and Expressions](#label-snowpark-dataframe-cols-and-expressions).)

For example:

- To specify which rows should be returned, call the `filter` method:

  Copy code

  ```
  // Import the col function from the functions object.
  import com.snowflake.snowpark.functions._

  // Create a DataFrame for the rows with the ID 1
  // in the "sample_product_data" table.
  //
  // This example uses the === operator of the Column object to perform an
  // equality check.
  val df = session.table("sample_product_data").filter(col("id") === 1)
  df.show()
  ```
- To specify the columns that should be selected, call the `select` method:

  Copy code

  ```
  // Import the col function from the functions object.
  import com.snowflake.snowpark.functions._

  // Create a DataFrame that contains the id, name, and serial_number
  // columns in the "sample_product_data" table.
  val df = session.table("sample_product_data").select(col("id"), col("name"), col("serial_number"))
  df.show()
  ```

Each method returns a new DataFrame object that has been transformed. (The method does not affect the original DataFrame object.)
This means that if you want to apply multiple transformations, you can
[chain method calls](#label-snowpark-dataframe-chaining-method-calls), calling each subsequent transformation method on the
new DataFrame object returned by the previous method call.

Note that these transformation methods do not retrieve data from the Snowflake database. (The action methods described in
[Performing an Action to Evaluate a DataFrame](#label-snowpark-dataframe-action-method) perform the data retrieval.) The transformation methods simply specify how the SQL
statement should be constructed.

### Specifying Columns and Expressions

When calling these transformation methods, you might need to specify columns or expressions that use columns. For example, when
calling the `select` method, you need to specify the columns that should be selected.

To refer to a column, create a [Column](../reference/scala/com/snowflake/snowpark/Column.html) object by calling the [col](../reference/scala/com/snowflake/snowpark/functions$.html#col(colName:String):com.snowflake.snowpark.Column) function in the `com.snowflake.snowpark.functions`
object.

Copy code

```
// Import the col function from the functions object.
import com.snowflake.snowpark.functions._

val dfProductInfo = session.table("sample_product_data").select(col("id"), col("name"))
dfProductInfo.show()
```

Note

To create a `Column` object for a literal, see [Using Literals as Column Objects](#label-snowpark-dataframe-cols-lit).

When specifying a filter, projection, join condition, etc., you can use `Column` objects in an expression. For example:

- You can use `Column` objects with the `filter` method to specify a filter condition:

  Copy code

  ```
  // Specify the equivalent of "WHERE id = 20"
  // in an SQL SELECT statement.
  df.filter(col("id") === 20)
  ```

  Copy code

  ```
  // Specify the equivalent of "WHERE a + b < 10"
  // in an SQL SELECT statement.
  df.filter((col("a") + col("b")) < 10)
  ```
- You can use `Column` objects with the `select` method to define an alias:

  Copy code

  ```
  // Specify the equivalent of "SELECT b * 10 AS c"
  // in an SQL SELECT statement.
  df.select((col("b") * 10) as "c")
  ```
- You can use `Column` objects with the `join` method to define a join condition:

  Copy code

  ```
  // Specify the equivalent of "X JOIN Y on X.a_in_X = Y.b_in_Y"
  // in an SQL SELECT statement.
  dfX.join(dfY, col("a_in_X") === col("b_in_Y"))
  ```

#### Referring to Columns in Different DataFrames

When referring to columns in two different DataFrame objects that have the same name (for example, joining the DataFrames on that
column), you can use the `DataFrame.col` method in one DataFrame object to refer to a column in that object (for example,
`df1.col("name")` and `df2.col("name")`).

The following example demonstrates how to use the `DataFrame.col` method to refer to a column in a specific DataFrame. The
example joins two DataFrame objects that both have a column named `key`. The example uses the `Column.as` method to change
the names of the columns in the newly created DataFrame.

Copy code

```
// Create a DataFrame that joins two other DataFrames (dfLhs and dfRhs).
// Use the DataFrame.col method to refer to the columns used in the join.
val dfJoined = dfLhs.join(dfRhs, dfLhs.col("key") === dfRhs.col("key")).select(dfLhs.col("value").as("L"), dfRhs.col("value").as("R"))
```

#### Using the `apply` Method to Refer to a Column

As an alternative to the `DataFrame.col` method, you can use the `DataFrame.apply` method to refer to a column in a
specific DataFrame. Like the `DataFrame.col` method, the `DataFrame.apply` method accepts a column name as input and
returns a `Column` object.

Note that when an object has an `apply` method in Scala, you can call the `apply` method by calling the object as if
it were a function. For example, to call `df.apply("column_name")`, you can simply write `df("column_name")`. The
following calls are equivalent:

- `df.col("<column_name>")`
- `df.apply("<column_name>")`
- `df("<column_name>")`

The following example is the same as the previous example but uses the `DataFrame.apply` method to refer to the columns in
a join operation:

Copy code

```
// Create a DataFrame that joins two other DataFrames (dfLhs and dfRhs).
// Use the DataFrame.apply method to refer to the columns used in the join.
// Note that dfLhs("key") is shorthand for dfLhs.apply("key").
val dfJoined = dfLhs.join(dfRhs, dfLhs("key") === dfRhs("key")).select(dfLhs("value").as("L"), dfRhs("value").as("R"))
```

### Using Shorthand For a Column Object

As an alternative to using the `col` function, you can refer to a column in one of these ways:

- Use a dollar sign in front of the quoted column name (`$"column_name"`).
- Use an apostrophe (a single quote) in front of the unquoted column name (`'column_name`).

To do this, import the names from the `implicits` object after you create a `Session` object:

Copy code

```
val session = Session.builder.configFile("/path/to/properties").create

// Import this after you create the session.
import session.implicits._

// Use the $ (dollar sign) shorthand.
val df = session.table("T").filter($"id" === 10).filter(($"a" + $"b") < 10)

// Use ' (apostrophe) shorthand.
val df = session.table("T").filter('id === 10).filter(('a + 'b) < 10).select('b * 10)
```

### Using Double Quotes Around Object Identifiers (Table Names, Column Names, etc.)

The names of databases, schemas, tables, and stages that you specify must conform to the
[Snowflake identifier requirements](/sql-reference/identifiers-syntax). When you specify a name, Snowflake considers the
name to be in upper case. For example, the following calls are equivalent:

Copy code

```
// The following calls are equivalent:
df.select(col("id123"))
df.select(col("ID123"))
```

If the name does not conform to the identifier requirements, you must use double quotes (`"`) around the name. Use a backslash
(`\`) to escape the double quote character within a Scala string literal. For example, the following table name does not start
with a letter or an underscore, so you must use double quotes around the name:

Copy code

```
val df = session.table("\"10tablename\"")
```

Note that when specifying the name of a column, you don’t need to use double quotes around the name. The Snowpark library
automatically encloses the column name in double quotes for you if the name does not comply with the identifier requirements:

Copy code

```
// The following calls are equivalent:
df.select(col("3rdID"))
df.select(col("\"3rdID\""))

// The following calls are equivalent:
df.select(col("id with space"))
df.select(col("\"id with space\""))
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
val dfTable = session.table("quoted")
dfTable.select("\"name_with_\"\"air\"\"_quotes\"").show()
dfTable.select("\"\"\"column_name_quoted\"\"\"").show()
```

Keep in mind that when an identifier is enclosed in double quotes (whether you explicitly added the quotes or the library added
the quotes for you), [Snowflake treats the identifier as case-sensitive](/sql-reference/identifiers-syntax):

Copy code

```
// The following calls are NOT equivalent!
// The Snowpark library adds double quotes around the column name,
// which makes Snowflake treat the column name as case-sensitive.
df.select(col("id with space"))
df.select(col("ID WITH SPACE"))
```

### Using Literals as Column Objects

To use a literal in a method that passes in a `Column` object, create a `Column` object for the literal by passing
the literal to the `lit` function in the `com.snowflake.snowpark.functions` object. For example:

Copy code

```
// Import for the lit and col functions.
import com.snowflake.snowpark.functions._

// Show the first 10 rows in which num_items is greater than 5.
// Use `lit(5)` to create a Column object for the literal 5.
df.filter(col("num_items").gt(lit(5))).show()
```

If the literal is a floating point or double value in Scala (e.g. `0.05` is
[treated as a Double by default](https://docs.scala-lang.org/overviews/scala-book/built-in-types.html)), the Snowpark library
generates SQL that implicitly casts the value to the corresponding Snowpark data type (e.g. `0.05::DOUBLE`). This can produce
an approximate value that differs from the exact number specified.

For example, the following code displays no matching rows, even though the filter (that matches values greater than or equal to
`0.05`) should match the rows in the DataFrame:

Copy code

```
// Create a DataFrame that contains the value 0.05.
val df = session.sql("select 0.05 :: Numeric(5, 2) as a")

// Applying this filter results in no matching rows in the DataFrame.
df.filter(col("a") <= lit(0.06) - lit(0.01)).show()
```

The problem is that `lit(0.06)` and `lit(0.01)` produce approximate values for `0.06` and `0.01`, not the exact values.

To avoid this problem, you can use one of the following approaches:

- Option 1: [Cast the literal to the Snowpark type](#label-snowpark-dataframe-cols-cast) that you want to use. For example,
  to use a [NUMBER](/sql-reference/data-types-numeric#label-data-type-number) with a precision of 5 and a scale of 2:

  Copy code

  ```
  df.filter(col("a") <= lit(0.06).cast(new DecimalType(5, 2)) - lit(0.01).cast(new DecimalType(5, 2))).show()
  ```
- Option 2: Cast the value to the type that you want to use before passing the value to the `lit` function. For example,
  if you want to use the
  [BigDecimal type](https://docs.scala-lang.org/overviews/scala-book/built-in-types.html#bigint-and-bigdecimal):

  Copy code

  ```
  df.filter(col("a") <= lit(BigDecimal(0.06)) - lit(BigDecimal(0.01))).show()
  ```

### Casting a Column Object to a Specific Type

To cast a `Column` object to a specific type, call the [Column.cast](../reference/scala/com/snowflake/snowpark/Column.html#cast(to:com.snowflake.snowpark.types.DataType):com.snowflake.snowpark.Column) method, and pass in a type object from the
[com.snowflake.snowpark.types package](../reference/scala/com/snowflake/snowpark/types/index.html). For example, to cast a literal as a [NUMBER](/sql-reference/data-types-numeric#label-data-type-number) with a precision of 5
and a scale of 2:

Copy code

```
// Import for the lit function.
import com.snowflake.snowpark.functions._
// Import for the DecimalType class..
import com.snowflake.snowpark.types._

val decimalValue = lit(0.05).cast(new DecimalType(5,2))
```

### Chaining Method Calls

Because each [method that transforms a DataFrame object](#label-snowpark-dataframe-transform) returns a new DataFrame object
that has the transformation applied, you can [chain method calls](https://en.wikipedia.org/wiki/Method_chaining) to produce a
new DataFrame that is transformed in additional ways.

The following example returns a DataFrame that is configured to:

- Query the `sample_product_data` table.
- Return the row with `id = 1`.
- Select the `name` and `serial_number` columns.

Copy code

```
val dfProductInfo = session.table("sample_product_data").filter(col("id") === 1).select(col("name"), col("serial_number"))
dfProductInfo.show()
```

In this example:

- `session.table("sample_product_data")` returns a DataFrame for the `sample_product_data` table.

  Although the DataFrame does not yet contain the data from the table, the object does contain the definitions of the columns in
  the table.
- `filter(col("id") === 1)` returns a DataFrame for the `sample_product_data` table that is set up to return the row with
  `id = 1`.

  Note again that the DataFrame does not yet contain the matching row from the table. The matching row is not retrieved until you
  [call an action method](#label-snowpark-dataframe-action-method).
- `select(col("name"), col("serial_number"))` returns a DataFrame that contains the `name` and `serial_number` columns
  for the row in the `sample_product_data` table that has `id = 1`.

When you chain method calls, keep in mind that the order of calls is important. Each method call returns a DataFrame that has been
transformed. Make sure that subsequent calls work with the transformed DataFrame.

For example, in the code below, the `select` method returns a DataFrame that just contains two columns: `name` and
`serial_number`. The `filter` method call on this DataFrame fails because it uses the `id` column, which is not in the
transformed DataFrame.

Copy code

```
// This fails with the error "invalid identifier 'ID'."
val dfProductInfo = session.table("sample_product_data").select(col("name"), col("serial_number")).filter(col("id") === 1)
```

In contrast, the following code executes successfully because the `filter()` method is called on a DataFrame that contains
all of the columns in the `sample_product_data` table (including the `id` column):

Copy code

```
// This succeeds because the DataFrame returned by the table() method
// includes the "id" column.
val dfProductInfo = session.table("sample_product_data").filter(col("id") === 1).select(col("name"), col("serial_number"))
dfProductInfo.show()
```

Keep in mind that you might need to make the `select` and `filter` method calls in a different order than you would
use the equivalent keywords (SELECT and WHERE) in a SQL statement.

### Limiting the Number of Rows in a DataFrame

To limit the number of rows in a DataFrame, you can use the [DataFrame.limit](../reference/scala/com/snowflake/snowpark/DataFrame.html#limit(n:Int):com.snowflake.snowpark.DataFrame) transformation method.

The Snowpark API also provides action methods for retrieving and printing out a limited number of rows:

- the [DataFrame.first](../reference/scala/com/snowflake/snowpark/DataFrame.html#first(n:Int):Array%5Bcom.snowflake.snowpark.Row%5D) action method (to execute the query and return the first `n` rows)
- the [DataFrame.show](../reference/scala/com/snowflake/snowpark/DataFrame.html#show(n:Int):Unit) action method (to execute the query and print the first `n` rows)

These methods effectively add a [LIMIT](/sql-reference/constructs/limit) clause to the SQL statement that is executed.

As explained in the [usage notes for LIMIT](/sql-reference/constructs/limit#label-limit-cmd-usage-notes), the results are non-deterministic unless you
specify a sort order (ORDER BY) in conjunction with LIMIT.

To keep the ORDER BY clause with the LIMIT clause (e.g. so that ORDER BY is not in a separate subquery), you must call the method
that limits results on the DataFrame returned by the `sort` method.

For example, if you are [chaining method calls](#label-snowpark-dataframe-chaining-method-calls):

Copy code

```
// Limit the number of rows to 5, sorted by parent_id.
var dfSubset = df.sort(col("parent_id")).limit(5);

// Return the first 5 rows, sorted by parent_id.
var arrayOfRows = df.sort(col("parent_id")).first(5)

// Print the first 5 rows, sorted by parent_id.
df.sort(col("parent_id")).show(5)
```

### Retrieving Column Definitions

To retrieve the definition of the columns in the dataset for the DataFrame, call the `schema` method. This method returns
a `StructType` object that contains an `Array` of `StructField` objects. Each `StructField` object
contains the definition of a column.

Copy code

```
// Get the StructType object that describes the columns in the
// underlying rowset.
val tableSchema = session.table("sample_product_data").schema
println("Schema for sample_product_data: " + tableSchema);
```

In the returned `StructType` object, the column names are always normalized. Unquoted identifiers are returned in uppercase,
and quoted identifiers are returned in the exact case in which they were defined.

The following example creates a DataFrame containing the columns named `ID` and `3rd`. For the column name `3rd`, the
Snowpark library automatically encloses the name in double quotes (`"3rd"`) because
[the name does not comply with the requirements for an identifier](#label-snowpark-dataframe-cols-identifiers).

The example calls the `schema` method and then calls the `names` method on the returned `StructType` object to
get an `ArraySeq` of column names. The names are normalized in the `StructType` returned by the `schema` method.

Copy code

```
// Create a DataFrame containing the "id" and "3rd" columns.
val dfSelectedColumns = session.table("sample_product_data").select(col("id"), col("3rd"))
// Print out the names of the columns in the schema. This prints out:
//   ArraySeq(ID, "3rd")
println(dfSelectedColumns.schema.names.toSeq)
```

### Joining DataFrames

To join DataFrame objects, call the [DataFrame.join](../reference/scala/com/snowflake/snowpark/DataFrame.html#join(right:com.snowflake.snowpark.DataFrame,joinExprs:com.snowflake.snowpark.Column,joinType:String):com.snowflake.snowpark.DataFrame) method.

The following sections explain how to use DataFrames to perform a join:

- [Setting up the Sample Data for the Joins](#label-snowpark-dataframe-join-sample-data)
- [Specifying the Columns for the Join](#label-snowpark-dataframe-join-columns)
- [Performing a Natural Join](#label-snowpark-dataframe-join-natural)
- [Specifying the Type of Join](#label-snowpark-dataframe-join-type)
- [Joining Multiple Tables](#label-snowpark-dataframe-multiple-joins)
- [Performing a Self-Join](#label-snowpark-dataframe-self-join)

#### Setting up the Sample Data for the Joins

The examples in the next sections use sample data that you can set up by executing the following SQL statements:

Copy code

```
create or replace table sample_a (
  id_a integer,
  name_a varchar,
  value integer
);
insert into sample_a (id_a, name_a, value) values
  (10, 'A1', 5),
  (40, 'A2', 10),
  (80, 'A3', 15),
  (90, 'A4', 20)
;
create or replace table sample_b (
  id_b integer,
  name_b varchar,
  id_a integer,
  value integer
);
insert into sample_b (id_b, name_b, id_a, value) values
  (4000, 'B1', 40, 10),
  (4001, 'B2', 10, 5),
  (9000, 'B3', 80, 15),
  (9099, 'B4', null, 200)
;
create or replace table sample_c (
  id_c integer,
  name_c varchar,
  id_a integer,
  id_b integer
);
insert into sample_c (id_c, name_c, id_a, id_b) values
  (1012, 'C1', 10, null),
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
val dfLhs = session.table("sample_a")
val dfRhs = session.table("sample_b")
val dfJoined = dfLhs.join(dfRhs, dfLhs.col("id_a") === dfRhs.col("id_a"))
dfJoined.show()
```

Note that the example uses the `DataFrame.col` method to specify the condition to use for the join. See
[Specifying Columns and Expressions](#label-snowpark-dataframe-cols-and-expressions) for more about this method.

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
information about specifying columns, see [Referring to Columns in Different DataFrames](#label-snowpark-multiple-dataframes-cols).)

Code in the following example joins two DataFrames, then calls the `select` method on the joined DataFrame. It specifies the columns
to select by calling the `col` method from the variable representing the respective DataFrame objects: `dfRhs` and
`dfLhs`. It uses the `as` method to give the columns new names in the DataFrame that the `select` method creates.

Copy code

```
val dfLhs = session.table("sample_a")
val dfRhs = session.table("sample_b")
val dfJoined = dfLhs.join(dfRhs, dfLhs.col("id_a") === dfRhs.col("id_a"))
val dfSelected = dfJoined.select(dfLhs.col("value").as("LeftValue"), dfRhs.col("value").as("RightValue"))
dfSelected.show()
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
call the [DataFrame.naturalJoin](../reference/scala/com/snowflake/snowpark/DataFrame.html#naturalJoin(right:com.snowflake.snowpark.DataFrame):com.snowflake.snowpark.DataFrame) method.

The following example joins the DataFrames for the tables `sample_a` and `sample_b` on their common columns (the column
`id_a`):

Copy code

```
val dfLhs = session.table("sample_a")
val dfRhs = session.table("sample_b")
val dfJoined = dfLhs.naturalJoin(dfRhs)
dfJoined.show()
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
val dfLhs = session.table("sample_a")
val dfRhs = session.table("sample_b")
val dfLeftOuterJoin = dfLhs.join(dfRhs, dfLhs.col("id_a") === dfRhs.col("id_a"), "left")
dfLeftOuterJoin.show()
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

You can [chain](#label-snowpark-dataframe-chaining-method-calls) the `join` calls as shown below:

Copy code

```
val dfFirst = session.table("sample_a")
val dfSecond  = session.table("sample_b")
val dfThird = session.table("sample_c")
val dfJoinThreeTables = dfFirst.join(dfSecond, dfFirst.col("id_a") === dfSecond.col("id_a")).join(dfThird, dfFirst.col("id_a") === dfThird.col("id_a"))
dfJoinThreeTables.show()
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

If you need to join a table with itself on different columns, you cannot perform the self-join with a single DataFrame. The
following examples that use a single DataFrame to perform a self-join fail because the column expressions for `"id"` are
present in the left and right sides of the join:

Copy code

```
// This fails because columns named "id" and "parent_id"
// are in the left and right DataFrames in the join.
val df = session.table("sample_product_data");
val dfJoined = df.join(df, col("id") === col("parent_id"))
```

Copy code

```
// This fails because columns named "id" and "parent_id"
// are in the left and right DataFrames in the join.
val df = session.table("sample_product_data");
val dfJoined = df.join(df, df("id") === df("parent_id"))
```

Both of these examples fail with the following exception:

Copy code

```
Exception in thread "main" com.snowflake.snowpark.SnowparkClientException:
  Joining a DataFrame to itself can lead to incorrect results due to ambiguity of column references.
  Instead, join this DataFrame to a clone() of itself.
```

Instead, use the [DataFrame.clone](../reference/scala/com/snowflake/snowpark/DataFrame.html#clone():com.snowflake.snowpark.DataFrame) method to create a clone of the DataFrame object, and use the two DataFrame objects to
perform the join:

Copy code

```
// Create a DataFrame object for the "sample_product_data" table for the left-hand side of the join.
val dfLhs = session.table("sample_product_data")
// Clone the DataFrame object to use as the right-hand side of the join.
val dfRhs = dfLhs.clone()

// Create a DataFrame that joins the two DataFrames
// for the "sample_product_data" table on the
// "id" and "parent_id" columns.
val dfJoined = dfLhs.join(dfRhs, dfLhs.col("id") === dfRhs.col("parent_id"))
dfJoined.show()
```

If you want to perform a self-join on the same column, call the `join` method that passes in a `Seq` of column
expressions for the `USING` clause:

Copy code

```
// Create a DataFrame that performs a self-join on a DataFrame
// using the column named "key".
val df = session.table("sample_product_data");
val dfJoined = df.join(df, Seq("key"))
```

## Performing an Action to Evaluate a DataFrame

As mentioned earlier, the DataFrame is lazily evaluated, which means the SQL statement isn’t sent to the server for execution
until you perform an action. An action causes the DataFrame to be evaluated and sends the corresponding SQL statement to the
server for execution.

The following sections explain how to perform an action synchronously and asynchronously on a DataFrame:

- [Performing an Action Synchronously](#label-snowpark-dataframe-action-method-sync)
- [Performing an Action Asynchronously](#label-snowpark-dataframe-action-method-async)

### Performing an Action Synchronously

To perform an action synchronously, call one of the following action methods:

| Method to Perform an Action Synchronously | Description |
| --- | --- |
| `DataFrame.collect` | Evaluates the DataFrame and returns the resulting dataset as an `Array` of [Row](../reference/scala/com/snowflake/snowpark/Row.html) objects. See [Returning All Rows](#label-snowpark-dataframe-return-all-rows). |
| `DataFrame.toLocalIterator` | Evaluates the DataFrame and returns an [Iterator](https://docs.scala-lang.org/overviews/collections/iterators.html) of [Row](../reference/scala/com/snowflake/snowpark/Row.html) objects. If the result set is large, use this method to avoid loading all the results into memory at once. See [Returning an Iterator for the Rows](#label-snowpark-dataframe-return-iterator). |
| `DataFrame.count` | Evaluates the DataFrame and returns the number of rows. |
| `DataFrame.show` | Evaluates the DataFrame and prints the rows to the console. Note that this method limits the number of rows to 10 (by default). See [Printing the Rows in a DataFrame](#label-snowpark-dataframe-print-results). |
| `DataFrame.cacheResult` | Executes the query, creates a temporary table, and puts the results into the table. The method returns a `HasCachedResult` object that you can use to access the data in this temporary table. See [Caching a DataFrame](#label-snowpark-dataframe-caching). |
| `DataFrame.write.saveAsTable` | Saves the data in the DataFrame to the specified table. See [Saving Data to a Table](#label-snowpark-dataframe-save-table). |
| `DataFrame.write.(csv%json%parquet)` | Saves a DataFrame to a specified file on a stage. See [Saving a DataFrame to Files on a Stage](#label-snowpark-dataframe-stages-copy-into-location). |
| `DataFrame.read.fileformat.copyInto('tableName')` | Copies the data in the DataFrame to the specified table. See [Copying Data from Files into a Table](#label-snowpark-dataframe-stages-copy-into-table). |
| `Session.table('tableName').delete` | Deletes rows in the specified table. See [Updating, Deleting, and Merging Rows in a Table](#label-snowpark-dataframe-updatable). |
| `Session.table('tableName').update` | Updates rows in the specified table. See [Updating, Deleting, and Merging Rows in a Table](#label-snowpark-dataframe-updatable). |
| `Session.table('tableName').merge.methods.collect` | Merges rows into the specified table. See [Updating, Deleting, and Merging Rows in a Table](#label-snowpark-dataframe-updatable). |

Expand

Show lessSee more

To execute the query and return the number of results, call the `count` method:

Copy code

```
// Create a DataFrame for the "sample_product_data" table.
val dfProducts = session.table("sample_product_data")

// Send the query to the server for execution and
// print the count of rows in the table.
println("Rows returned: " + dfProducts.count())
```

You can also call action methods to:

- [Execute a query against a table and return the results](#label-snowpark-dataframe-return-all-rows).
- [Execute a query and print the results to the console](#label-snowpark-dataframe-print-results).

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

- [Understanding the Basic Flow of Asynchronous Actions](#label-snowpark-dataframe-action-method-async-basic)
- [Specifying the Maximum Number of Seconds to Wait](#label-snowpark-dataframe-action-method-async-timeout)
- [Accessing an Asynchronous Query by ID](#label-snowpark-dataframe-action-method-async-query-id)

#### Understanding the Basic Flow of Asynchronous Actions

You can use the following methods to perform an action asynchronously:

| Method to Perform an Action Asynchronously | Description |
| --- | --- |
| `DataFrame.async.collect` | Asynchronously evaluates the DataFrame to retrieve the resulting dataset as an `Array` of [Row](../reference/scala/com/snowflake/snowpark/Row.html) objects. See [Returning All Rows](#label-snowpark-dataframe-return-all-rows). |
| `DataFrame.async.toLocalIterator` | Asynchronously evaluates the DataFrame to retrieve an [Iterator](https://docs.scala-lang.org/overviews/collections/iterators.html) of [Row](../reference/scala/com/snowflake/snowpark/Row.html) objects. If the result set is large, use this method to avoid loading all the results into memory at once. See [Returning an Iterator for the Rows](#label-snowpark-dataframe-return-iterator). |
| `DataFrame.async.count` | Asynchronously evaluates the DataFrame to retrieve the number of rows. |
| `DataFrame.write.async.saveAsTable` | Asynchronously saves the data in the DataFrame to the specified table. See [Saving Data to a Table](#label-snowpark-dataframe-save-table). |
| `DataFrame.write.async.(csv%json%parquet)` | Saves a DataFrame to a specified file on a stage. See [Saving a DataFrame to Files on a Stage](#label-snowpark-dataframe-stages-copy-into-location). |
| `DataFrame.read.fileformat.async.copyInto('tableName')` | Asynchronously copies the data in the DataFrame to the specified table. See [Copying Data from Files into a Table](#label-snowpark-dataframe-stages-copy-into-table). |
| `Session.table('tableName').async.delete` | Asynchronously deletes rows in the specified table. See [Updating, Deleting, and Merging Rows in a Table](#label-snowpark-dataframe-updatable). |
| `Session.table('tableName').async.update` | Asynchronously updates rows in the specified table. See [Updating, Deleting, and Merging Rows in a Table](#label-snowpark-dataframe-updatable). |
| `Session.table('tableName').merge.methods.async.collect` | Asynchronously merges rows into the specified table. Supported in version 1.3.0 or later. See [Updating, Deleting, and Merging Rows in a Table](#label-snowpark-dataframe-updatable). |

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
`DataFrame.async.collect`:

Copy code

```
// Create a DataFrame with the "id" and "name" columns from the "sample_product_data" table.
// This does not execute the query.
val df = session.table("sample_product_data").select(col("id"), col("name"))

// Execute the query asynchronously.
// This call does not block.
val asyncJob = df.async.collect()
// Check if the query has completed execution.
println(s"Is query ${asyncJob.getQueryId()} done? ${asyncJob.isDone()}")
// Get an Array of Rows containing the results, and print the results.
// Note that getResult is a blocking call.
val results = asyncJob.getResult()
results.foreach(println)
```

To execute the query asynchronously and retrieve the number of results, call `DataFrame.async.count`:

Copy code

```
// Create a DataFrame for the "sample_product_data" table.
val dfProducts = session.table("sample_product_data")

// Execute the query asynchronously.
// This call does not block.
val asyncJob = df.async.count()
// Check if the query has completed execution.
println(s"Is query ${asyncJob.getQueryId()} done? ${asyncJob.isDone()}")
// Print the count of rows in the table.
// Note that getResult is a blocking call.
println("Rows returned: " + asyncJob.getResult())
```

#### Specifying the Maximum Number of Seconds to Wait

When calling the `getResult` method, you can use the `maxWaitTimeInSeconds` argument to specify the maximum number of
seconds to wait for the query to complete before attempting to retrieve the results. For example:

Copy code

```
// Wait a maximum of 10 seconds for the query to complete before retrieving the results.
val results = asyncJob.getResult(10)
```

If you omit this argument, the method waits for the maximum number of seconds specified by the
[snowpark\_request\_timeout\_in\_seconds](/developer-guide/snowpark/scala/creating-session#label-snowpark-request-timeout-in-seconds) configuration property. (This is a property
that you can set when [creating the Session object](/developer-guide/snowpark/scala/creating-session#label-snowpark-creating-session).)

#### Accessing an Asynchronous Query by ID

If you have the query ID of an asynchronous query that you submitted earlier, you can call `Session.createAsyncJob` method
to create an [AsyncJob](../reference/scala/com/snowflake/snowpark/AsyncJob.html) object that you can use to check the status of the query, retrieve the query results, or cancel the
query.

Note that unlike `TypedAsyncJob`, `AsyncJob` does not provide a `getResult` method for retrieving the results.
If you need to retrieve the results, call the `getRows` or `getIterator` method instead.

For example:

Copy code

```
val asyncJob = session.createAsyncJob(myQueryId)
// Check if the query has completed execution.
println(s"Is query ${asyncJob.getQueryId()} done? ${asyncJob.isDone()}")
// If you need to retrieve the results, call getRows to return an Array of Rows containing the results.
// Note that getRows is a blocking call.
val rows = asyncJob.getRows()
rows.foreach(println)
```

## Retrieving Rows into a DataFrame

After you [specify how the DataFrame should be transformed](#label-snowpark-dataframe-transform), you can
[call an action method](#label-snowpark-dataframe-action-method) to execute a query and return the results. You can return
all of the rows in an `Array`, or you can return an [Iterator](https://docs.scala-lang.org/overviews/collections/iterators.html) that allows you to iterate over the results, row by row. In
the latter case, if the amount of data is large, the rows are loaded into memory by chunk to avoid loading a large amount of data
into memory.

- [Returning All Rows](#label-snowpark-dataframe-return-all-rows)
- [Returning an Iterator for the Rows](#label-snowpark-dataframe-return-iterator)
- [Returning the First <code className=”samp”><em>n</em></code> Rows](#label-snowpark-dataframe-return-first-n-rows)

### Returning All Rows

To return all rows at once, call the [DataFrame.collect](../reference/scala/com/snowflake/snowpark/DataFrame.html#collect():Array%5Bcom.snowflake.snowpark.Row%5D) method. This method returns an Array of [Row](../reference/scala/com/snowflake/snowpark/Row.html) objects. To retrieve the
values from the row, call the `getType` method (e.g. `getString`, `getInt`, etc.).

For example:

Copy code

```
import com.snowflake.snowpark.functions._

val rows = session.table("sample_product_data").select(col("name"), col("category_id")).sort(col("name")).collect()
for (row <- rows) {
  println(s"Name: ${row.getString(0)}; Category ID: ${row.getInt(1)}")
}
```

### Returning an Iterator for the Rows

If you want to use an [Iterator](https://docs.scala-lang.org/overviews/collections/iterators.html) to iterate over the [Row](../reference/scala/com/snowflake/snowpark/Row.html) objects in the results, call [DataFrame.toLocalIterator](../reference/scala/com/snowflake/snowpark/DataFrame.html#toLocalIterator:Iterator%5Bcom.snowflake.snowpark.Row%5D). If the
amount of data in the results is large, the method loads the rows by chunk to avoid loading all rows into memory at once.

For example:

Copy code

```
import com.snowflake.snowpark.functions._

while (rowIterator.hasNext) {
  val row = rowIterator.next()
  println(s"Name: ${row.getString(0)}; Category ID: ${row.getInt(1)}")
}
```

### Returning the First <code className=”samp”><em>n</em></code> Rows

To return the first `n` rows, call the [DataFrame.first](../reference/scala/com/snowflake/snowpark/DataFrame.html#first(n:Int):Array%5Bcom.snowflake.snowpark.Row%5D) method, passing in the number of rows to return.

As explained in [Limiting the Number of Rows in a DataFrame](#label-snowpark-dataframe-limit), the results are non-deterministic. If you want the results to be
deterministic, call this method on a sorted DataFrame (`df.sort().first()`).

For example:

Copy code

```
import com.snowflake.snowpark.functions._

val df = session.table("sample_product_data")
val rows = df.sort(col("name")).first(5)
rows.foreach(println)
```

## Printing the Rows in a DataFrame

To print the first 10 rows in the DataFrame to the console, call the [DataFrame.show](../reference/scala/com/snowflake/snowpark/DataFrame.html#show(n:Int):Unit) method. To print out a different number of
rows, pass in the number of rows to print.

As explained in [Limiting the Number of Rows in a DataFrame](#label-snowpark-dataframe-limit), the results are non-deterministic. If you want the results to be
deterministic, call this method on a sorted DataFrame (`df.sort().show()`).

For example:

Copy code

```
import com.snowflake.snowpark.functions._

val df = session.table("sample_product_data")
df.sort(col("name")).show()
```

## Updating, Deleting, and Merging Rows in a Table

Note

This feature was introduced in Snowpark 0.7.0.

When you call `Session.table` to create a `DataFrame` object for a table, the method returns an `Updatable`
object, which extends `DataFrame` with additional methods for updating and deleting data in the table. (See [Updatable](../reference/scala/com/snowflake/snowpark/Updatable.html).)

If you need to update or delete rows in a table, you can use the following methods of the `Updatable` class:

- Call `update` to update existing rows in the table. See [Updating Rows in a Table](#label-snowpark-dataframe-update-table-rows).
- Call `delete` to delete rows from a table. See [Deleting Rows in a Table](#label-snowpark-dataframe-delete-table-rows).
- Call `merge` to insert, update, and delete rows in one table, based on data in a second table or subquery. (This is the
  equivalent of the [MERGE](/sql-reference/sql/merge) command in SQL.) See [Merging Rows into a Table](#label-snowpark-dataframe-merge-table-rows).

### Updating Rows in a Table

For the `update` method, pass in a `Map` that associates the columns to update and the corresponding values to assign
to those columns. `update` returns an `UpdateResult` object, which contains the number of rows that were updated. (See
[UpdateResult](../reference/scala/com/snowflake/snowpark/UpdateResult.html).)

Note

`update` is an [action method](#label-snowpark-dataframe-action-method), which means that calling the method sends
SQL statements to the server for execution.

For example, to replace the values in the column named `count` with the value `1`:

Copy code

```
val updatableDf = session.table("sample_product_data")
val updateResult = updatableDf.update(Map("count" -> lit(1)))
println(s"Number of rows updated: ${updateResult.rowsUpdated}")
```

The example above uses the name of the column to identify the column. You can also use a column expression:

Copy code

```
val updateResult = updatableDf.update(Map(col("count") -> lit(1)))
```

If the update should be made only when a condition is met, you can specify that condition as an argument. For example, to replace
the values in the column named `count` for rows in which the `category_id` column has the value `20`:

Copy code

```
val updateResult = updatableDf.update(Map(col("count") -> lit(1)), col("category_id") === 20)
```

If you need to base the condition on a join with a different `DataFrame` object, you can pass that `DataFrame` in as
an argument and use that `DataFrame` in the condition. For example, to replace the values in the column named `count` for
rows in which the `category_id` column matches the `category_id` in the `DataFrame` `dfParts`:

Copy code

```
val updatableDf = session.table("sample_product_data")
val dfParts = session.table("parts")
val updateResult = updatableDf.update(Map(col("count") -> lit(1)), updatableDf("category_id") === dfParts("category_id"), dfParts)
```

### Deleting Rows in a Table

For the `delete` method, you can specify a condition that identifies the rows to delete, and you can base that condition on
a join with another DataFrame. `delete` returns a `DeleteResult` object, which contains the
number of rows that were deleted. (See [DeleteResult](../reference/scala/com/snowflake/snowpark/DeleteResult.html).)

Note

`delete` is an [action method](#label-snowpark-dataframe-action-method), which means that calling the method sends
SQL statements to the server for execution.

For example, to delete the rows that have the value `1` in the `category_id` column:

Copy code

```
val updatableDf = session.table("sample_product_data")
val deleteResult = updatableDf.delete(updatableDf("category_id") === 1)
println(s"Number of rows deleted: ${deleteResult.rowsDeleted}")
```

If the condition refers to columns in a different DataFrame, pass that DataFrame in as the second argument. For example, to delete
the rows in which the `category_id` column matches the `category_id` in the `DataFrame` `dfParts`, pass in `dfParts`
as the second argument:

Copy code

```
val updatableDf = session.table("sample_product_data")
val deleteResult = updatableDf.delete(updatableDf("category_id") === dfParts("category_id"), dfParts)
println(s"Number of rows deleted: ${deleteResult.rowsDeleted}")
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
val mergeResult = target.merge(source, target("id") === source("id"))
                      .whenNotMatched.insert(Seq(source("id"), source("value")))
                      .collect()
```

The following example updates a row in the `target` table with the value of the `value` column from the row in the `source`
table that has the same ID:

Copy code

```
val mergeResult = target.merge(source, target("id") === source("id"))
                      .whenMatched.update(Map("value" -> source("value")))
                      .collect()
```

## Saving Data to a Table

You can save the contents of a DataFrame to a new or existing table. In order to do this, you must have the following privileges:

- CREATE TABLE privileges on the schema, if the table does not exist.
- INSERT privileges on the table.

To save the contents of a DataFrame to a table:

1. Call the [DataFrame.write](../reference/scala/com/snowflake/snowpark/DataFrame.html#write:com.snowflake.snowpark.DataFrameWriter) method to get a [DataFrameWriter](../reference/scala/com/snowflake/snowpark/DataFrameWriter.html) object.
2. Call the [DataFrameWriter.mode](../reference/scala/com/snowflake/snowpark/DataFrameWriter.html#mode(saveMode:com.snowflake.snowpark.SaveMode):com.snowflake.snowpark.DataFrameWriter) method, passing in a [SaveMode](../reference/scala/com/snowflake/snowpark/SaveMode$.html) object that specifies your preferences for writing to the
   table:

   - To insert rows, pass in `SaveMode.Append`.
   - To overwrite the existing table, pass in `SaveMode.Overwrite`.

   This method returns the same `DataFrameWriter` object configured with the specified mode.
3. If you are inserting rows into an existing table (`SaveMode.Append`) and the column names in the DataFrame match the
   column names in the table, call the [DataFrameWriter.option](../reference/scala/com/snowflake/snowpark/DataFrameWriter.html#option(key:String,value:Any):com.snowflake.snowpark.DataFrameWriter) method, passing in `"columnOrder"` and `"name"` as
   arguments.

   Note

   This method was introduced in Snowpark 1.4.0.

   By default, the `columnOrder` option is set to `"index"`, which means that the `DataFrameWriter` inserts the
   values in the order that the columns appear. For example, the `DataFrameWriter` inserts the value from the first column
   from the DataFrame in the first column in the table, the second column from the DataFrame in the second column in the table,
   etc.

   This method returns the same `DataFrameWriter` object configured with the specified option.
4. Call the [DataFrameWriter.saveAsTable](../reference/scala/com/snowflake/snowpark/DataFrameWriter.html#saveAsTable(tableName:String):Unit) to save the contents of the DataFrame to a specified table.

   You do not need to call a separate method (e.g. `collect`) to execute the SQL statement that saves the data to the table.
   `saveAsTable` is an [action method](#label-snowpark-dataframe-action-method) that executes the SQL statement.

The following example overwrites an existing table (identified by the `tableName` variable) with the contents of the DataFrame
`df`:

Copy code

```
df.write.mode(SaveMode.Overwrite).saveAsTable(tableName)
```

The following example inserts rows from the DataFrame `df` into an existing table (identified by the `tableName` variable).
In this example, the table and the DataFrame both contain the columns `c1` and `c2`.

The example demonstrates the difference between setting the `columnOrder` option to `"name"` (which inserts values
into the table columns with the same names as the DataFrame columns) and using the default `columnOrder` option (which
inserts values into the table columns based on the order of the columns in the DataFrame).

Copy code

```
val df = session.sql("SELECT 1 AS c2, 2 as c1")
// With the columnOrder option set to "name", the DataFrameWriter uses the column names
// and inserts a row with the values (2, 1).
df.write.mode(SaveMode.Append).option("columnOrder", "name").saveAsTable(tableName)
// With the default value of the columnOrder option ("index"), the DataFrameWriter uses column positions
// and inserts a row with the values (1, 2).
df.write.mode(SaveMode.Append).saveAsTable(tableName)
```

## Creating a View From a DataFrame

To create a view from a DataFrame, call the [DataFrame.createOrReplaceView](../reference/scala/com/snowflake/snowpark/DataFrame.html#createOrReplaceView(viewName:String):Unit) method:

Copy code

```
df.createOrReplaceView("db.schema.viewName")
```

Note that calling `createOrReplaceView` immediately creates the new view. More importantly, it does not
cause the DataFrame to be evaluated. (The DataFrame itself is not evaluated until you
[perform an action](#label-snowpark-dataframe-action-method).)

Views that you create by calling `createOrReplaceView` are persistent. If you no longer need that view, you can
[drop the view manually](/sql-reference/sql/drop-view).

If you need to create a temporary view just for the session, call the [DataFrame.createOrReplaceTempView](../reference/scala/com/snowflake/snowpark/DataFrame.html#createOrReplaceTempView(viewName:String):Unit) method instead:

Copy code

```
df.createOrReplaceTempView("db.schema.viewName")
```

## Caching a DataFrame

In some cases, you may need to perform a complex query and keep the results for use in subsequent operations (rather than
executing the same query again). In these cases, you can cache the contents of a DataFrame by calling the
[DataFrame.cacheResult](../reference/scala/com/snowflake/snowpark/DataFrame.html#cacheResult():com.snowflake.snowpark.HasCachedResult) method.

This method:

- Runs the query.

  You do not need to [call a separate action method to retrieve the results](#label-snowpark-dataframe-retrieve-results)
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
import com.snowflake.snowpark.functions._

// Set up a DataFrame to query a table.
val df = session.table("sample_product_data").filter(col("category_id") > 10)
// Retrieve the results and cache the data.
val cachedDf = df.cacheResult()
// Create a DataFrame containing a subset of the cached data.
val dfSubset = cachedDf.filter(col("category_id") === lit(20)).select(col("name"), col("category_id"))
dfSubset.show()
```

Note that the original DataFrame is not affected when you call this method. For example, suppose that `dfTable` is a DataFrame
for the table `sample_product_data`:

Copy code

```
val dfTempTable = dfTable.cacheResult()
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

- [Uploading and Downloading Files in a Stage](#label-snowpark-dataframe-stages-file-operation)
- [Using Input Streams to Upload and Download Data in a Stage](#label-snowpark-dataframe-stages-file-operation-streams)
- [Setting Up a DataFrame for Files in a Stage](#label-snowpark-dataframe-stages-query)
- [Loading Data from Files into a DataFrame](#label-snowpark-dataframe-stages-collect)
- [Copying Data from Files into a Table](#label-snowpark-dataframe-stages-copy-into-table)
- [Saving a DataFrame to Files on a Stage](#label-snowpark-dataframe-stages-copy-into-location)

### Uploading and Downloading Files in a Stage

To upload and download files in a stage, use the [FileOperation](../reference/scala/com/snowflake/snowpark/FileOperation.html) object:

- [Uploading Files to a Stage](#label-snowpark-dataframe-stages-file-put)
- [Downloading Files from a Stage](#label-snowpark-dataframe-stages-file-get)

#### Uploading Files to a Stage

To upload files to a stage:

1. Verify that you have the [privileges to upload files to the stage](/user-guide/security-access-control-privileges#label-access-control-privileges-stage).
2. Use [Session.file](../reference/scala/com/snowflake/snowpark/Session.html#file:com.snowflake.snowpark.FileOperation) to access the [FileOperation](../reference/scala/com/snowflake/snowpark/FileOperation.html) object for the session.
3. Call the [FileOperation.put](../reference/scala/com/snowflake/snowpark/FileOperation.html#put(localFileName:String,stageLocation:String,options:Map%5BString,String%5D):Array%5Bcom.snowflake.snowpark.PutResult%5D) method to upload the files to a stage.

   This method executes a SQL [PUT](/sql-reference/sql/put) command.

   - To specify any [optional parameters](/sql-reference/sql/put#label-put-optional-parameters) for the PUT command, create a `Map` of the
     parameters and values, and pass in the `Map` as the `options` argument. For example:

     Copy code

     ```
     // Upload a file to a stage without compressing the file.
     val putOptions = Map("AUTO_COMPRESS" -> "FALSE")
     val putResults = session.file.put("file:///tmp/myfile.csv", "@myStage", putOptions)
     ```
   - In the `localFilePath` argument, you can use wildcards (`*` and `?`) to identify a set of files to upload. For
     example:

     Copy code

     ```
     // Upload the CSV files in /tmp with names that start with "file".
     // You can use the wildcard characters "*" and "?" to match multiple files.
     val putResults = session.file.put("file:///tmp/file*.csv", "@myStage/prefix2")
     ```
4. Check the `Array` of [PutResult](../reference/scala/com/snowflake/snowpark/PutResult.html) objects returned by the `put` method to determine if the files were successfully
   uploaded. For example, to print the filename and the status of the PUT operation for that file:

   Copy code

   ```
   // Print the filename and the status of the PUT operation.
   putResults.foreach(r => println(s"  ${r.sourceFileName}: ${r.status}"))
   ```

#### Downloading Files from a Stage

To download files from a stage:

1. Verify that you have the [privileges to download files from the stage](/user-guide/security-access-control-privileges#label-access-control-privileges-stage).
2. Use [Session.file](../reference/scala/com/snowflake/snowpark/Session.html#file:com.snowflake.snowpark.FileOperation) to access the [FileOperation](../reference/scala/com/snowflake/snowpark/FileOperation.html) object for the session.
3. Call the [FileOperation.get](../reference/scala/com/snowflake/snowpark/FileOperation.html#get(stageLocation:String,targetDirectory:String,options:Map%5BString,String%5D):Array%5Bcom.snowflake.snowpark.GetResult%5D) method to download the files from a stage.

   This method executes a SQL [GET](/sql-reference/sql/get) command.

   To specify any [optional parameters](/sql-reference/sql/get#label-get-optional-parameters) for the GET command, create a `Map` of the
   parameters and values, and pass in the `Map` as the `options` argument. For example:

   Copy code

   ```
   // Download files with names that match a regular expression pattern.
   val getOptions = Map("PATTERN" -> s"'.*file_.*.csv.gz'")
   val getResults = session.file.get("@myStage", "file:///tmp", getOptions)
   ```
4. Check the `Array` of [GetResult](https://docs.snowflake.com/en/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/GetResult.html) objects returned by the `get` method to determine if the files were successfully
   downloaded. For example, to print the filename and the status of the GET operation for that file:

   Copy code

   ```
   // Print the filename and the status of the GET operation.
   getResults.foreach(r => println(s"  ${r.fileName}: ${r.status}"))
   ```

### Using Input Streams to Upload and Download Data in a Stage

Note

This feature was introduced in Snowpark 1.4.0.

To use input streams to upload data to a file on a stage and download data from a file on a stage, use the `uploadStream`
and `downloadStream` methods of the [FileOperation](../reference/scala/com/snowflake/snowpark/FileOperation.html) object:

- [Using an Input Stream to Upload Data to a File on a Stage](#label-snowpark-dataframe-stages-file-streams-upload)
- [Using an Input Stream to Download Data from a File on a Stage](#label-snowpark-dataframe-stages-file-streams-download)

#### Using an Input Stream to Upload Data to a File on a Stage

To upload the data from a [java.io.InputStream](https://docs.oracle.com/en/java/javase/11/docs/api/java.base/java/io/InputStream.html) object to a file on a stage:

1. Verify that you have the [privileges to upload files to the stage](/user-guide/security-access-control-privileges#label-access-control-privileges-stage).
2. Use [Session.file](../reference/scala/com/snowflake/snowpark/Session.html#file:com.snowflake.snowpark.FileOperation) to access the [FileOperation](../reference/scala/com/snowflake/snowpark/FileOperation.html) object for the session.
3. Call the [FileOperation.uploadStream](../reference/scala/com/snowflake/snowpark/FileOperation.html#uploadStream(stageLocation:String,inputStream:java.io.InputStream,compress:Boolean):Unit) method.

   Pass in the complete path to the file on the stage where the data should be written and the `InputStream` object. In
   addition, use the `compress` argument to specify whether or not the data should be compressed before it is uploaded.

For example:

Copy code

```
import java.io.InputStream
...
val compressData = true
val pathToFileOnStage = "@myStage/path/file"
session.file.uploadStream(pathToFileOnStage, new ByteArrayInputStream(fileContent.getBytes()), compressData)
```

#### Using an Input Stream to Download Data from a File on a Stage

To download data from a file on a stage to a [java.io.InputStream](https://docs.oracle.com/en/java/javase/11/docs/api/java.base/java/io/InputStream.html) object:

1. Verify that you have the [privileges to download files from the stage](/user-guide/security-access-control-privileges#label-access-control-privileges-stage).
2. Use [Session.file](../reference/scala/com/snowflake/snowpark/Session.html#file:com.snowflake.snowpark.FileOperation) to access the [FileOperation](../reference/scala/com/snowflake/snowpark/FileOperation.html) object for the session.
3. Call the [FileOperation.downloadStream](../reference/scala/com/snowflake/snowpark/FileOperation.html#downloadStream(stageLocation:String,decompress:Boolean):java.io.InputStream) method.

   Pass in the complete path to the file on the stage containing the data to download. Use the `decompress` argument to
   specify whether or not the data in the file is compressed.

For example:

Copy code

```
import java.io.InputStream
...
val isDataCompressed = true
val pathToFileOnStage = "@myStage/path/file"
val is = session.file.downloadStream(pathToFileOnStage, isDataCompressed)
```

### Setting Up a DataFrame for Files in a Stage

This section explains how to set up a DataFrame for files in a Snowflake stage. Once you create this DataFrame, you can use the
DataFrame to:

- [retrieve data from the files](#label-snowpark-dataframe-stages-collect)
- [copy data from the files into a table](#label-snowpark-dataframe-stages-copy-into-table)

To set up a DataFrame for files in a Snowflake stage, use the `DataFrameReader` class:

1. Verify that you have the following privileges:

   - [Privileges to access files in the stage](/user-guide/security-access-control-privileges#label-access-control-privileges-stage).
   - One of the following:
     - CREATE TABLE privileges on the schema, if you plan to specify
       [copy options](/developer-guide/snowpark/scala/working-with-dataframes#label-snowpark-dataframe-stages-copy-options) that determine how data is copied from the staged files.
     - CREATE FILE FORMAT privileges on the schema, otherwise.
2. Call the `read` method in the `Session` class to access a `DataFrameReader` object.
3. If the files are in CSV format, describe the fields in the file. To do this:

   1. Create a [StructType](../reference/scala/com/snowflake/snowpark/types/StructType$.html) object that consists of a sequence of [StructField](../reference/scala/com/snowflake/snowpark/types/StructField$.html) objects that describe the fields in the file.
   2. For each `StructField` object, specify the following:

      - The name of the field.
      - The data type of the field (specified as an object in the `com.snowflake.snowpark.types` package).
      - Whether or not the field is nullable.

      For example:

      Copy code

      ```
      import com.snowflake.snowpark.types._

      val schemaForDataFile = StructType(
          Seq(
        StructField("id", StringType, true),
        StructField("name", StringType, true)))
      ```
   3. Call the `schema` method in the `DataFrameReader` object, passing in the `StructType` object.

      For example:

      Copy code

      ```
      var dfReader = session.read.schema(schemaForDataFile)
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
     [retrieve the data into the DataFrame](#label-snowpark-dataframe-action-method).

   The following example sets up the `DataFrameReader` object to query data in a CSV file that is not compressed and that
   uses a semicolon for the field delimiter.

   Copy code

   ```
   dfReader = dfReader.option("field_delimiter", ";").option("COMPRESSION", "NONE")
   ```

   The `option` method returns a `DataFrameReader` object that is configured with the specified option.

   To set multiple options, you can either
   [chain calls](#label-snowpark-dataframe-chaining-method-calls) to the `option` method (as shown in the example
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
   val df = dfReader.csv("@s3_ts_stage/emails/data_0_0_0.csv")
   ```

   To specify multiple files that start with the same prefix, specify the prefix after the stage name. For example, to load files
   that have the prefix `csv_` from the stage `@mystage`:

   Copy code

   ```
   val df = dfReader.csv("@mystage/csv_")
   ```

   The methods corresponding to the format of a file return a [CopyableDataFrame](../reference/scala/com/snowflake/snowpark/CopyableDataFrame.html) object for that file. `CopyableDataFrame`
   extends `DataFrame` and provides additional methods for working the data in staged files.
6. Call an action method to:

   - [retrieve data from the files](#label-snowpark-dataframe-stages-collect), or
   - [copy data from the files into a table](#label-snowpark-dataframe-stages-copy-into-table)

   As is the case with DataFrames for tables, the data is not retrieved into the DataFrame until you call
   [an action method](#label-snowpark-dataframe-action-method).

### Loading Data from Files into a DataFrame

After you [set up a DataFrame for files in a stage](#label-snowpark-dataframe-stages-query), you can load data from the files
into the DataFrame:

1. Use the DataFrame object methods to [perform any transformations](#label-snowpark-dataframe-transform) needed on the
   dataset (for example, selecting specific fields, filtering rows, etc.).

   For example, to extract the `color` element from a JSON file named `data.json` in the stage named `mystage`:

   Copy code

   ```
   val df = session.read.json("@mystage/data.json").select(col("$1")("color"))
   ```

   As explained earlier, for files in formats other than CSV (e.g. JSON), the `DataFrameReader` treats the data in the file
   as a single VARIANT column with the name `$1`.
2. Call the `DataFrame.collect` method to load the data. For example:

   Copy code

   ```
   val results = df.collect()
   ```

### Copying Data from Files into a Table

After you [set up a DataFrame for files in a stage](#label-snowpark-dataframe-stages-query), you can call the
[CopyableDataFrame.copyInto](../reference/scala/com/snowflake/snowpark/CopyableDataFrame.html#copyInto(tableName:String):Unit) method to copy the data into a table. This method executes the
[COPY INTO <table>](/sql-reference/sql/copy-into-table) command.

Note

You do not need to call the `collect` method before calling `copyInto`. The data from the files does not need to
be in the DataFrame before you call `copyInto`.

For example, the following code loads data from the CSV file specified by `myFileStage` into the table `mytable`. Because the
data is in a CSV file, the code must also [describe the fields in the file](/developer-guide/snowpark/scala/working-with-dataframes#label-snowpark-dataframe-stages-csv-schema). The
example does this by calling the [DataFrameReader.schema](../reference/scala/com/snowflake/snowpark/DataFrameReader.html#schema(schema:com.snowflake.snowpark.types.StructType):com.snowflake.snowpark.DataFrameReader) method and passing in a [StructType](../reference/scala/com/snowflake/snowpark/types/StructType$.html) object (`csvFileSchema`)
containing a sequence of [StructField](../reference/scala/com/snowflake/snowpark/types/StructField$.html) objects that describe the fields.

Copy code

```
val df = session.read.schema(csvFileSchema).csv(myFileStage)
df.copyInto("mytable")
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

1. Call the [DataFrame.write](../reference/scala/com/snowflake/snowpark/DataFrame.html#write:com.snowflake.snowpark.DataFrameWriter) method to get a [DataFrameWriter](../reference/scala/com/snowflake/snowpark/DataFrameWriter.html) object. For example, to get the `DataFrameWriter` object
   for a DataFrame that represents the table named `sample_product_data`:

   Copy code

   ```
   dfWriter = session.table("sample_product_data").write
   ```
2. If you want to overwrite the contents of the file (if the file exists), call the [DataFrameWriter.mode](../reference/scala/com/snowflake/snowpark/DataFrameWriter.html#mode(saveMode:com.snowflake.snowpark.SaveMode):com.snowflake.snowpark.DataFrameWriter) method, passing in
   `SaveMode.Overwrite`.

   Otherwise, by default, the `DataFrameWriter` reports an error if the specified file on the stage already exists.

   The `mode` method returns the same `DataFrameWriter` object configured with the specified mode.

   For example, to specify that the `DataFrameWriter` should overwrite the file on the stage:

   Copy code

   ```
   dfWriter = dfWriter.mode(SaveMode.Overwrite)
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

   Note that you cannot use the `option` method to set the following options:

   - The TYPE format type option.
   - The OVERWRITE copy option. To set this option, call the `mode` method instead (as mentioned in the previous step).

   The following example sets up the `DataFrameWriter` object to save data to a CSV file in uncompressed form, using a
   semicolon (rather than a comma) as the field delimiter.

   Copy code

   ```
   dfWriter = dfWriter.option("field_delimiter", ";").option("COMPRESSION", "NONE")
   ```

   The `option` method returns a `DataFrameWriter` object that is configured with the specified option.

   To set multiple options, you can
   [chain calls](#label-snowpark-dataframe-chaining-method-calls) to the `option` method (as shown in the example
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
   val writeFileResult = dfWriter.csv("@mystage/saved_data")
   ```

   This example saves the contents of the DataFrame to files that begin with the prefix `saved_data` (e.g.
   `@mystage/saved_data_0_0_0.csv`).
6. Check the [WriteFileResult](../reference/scala/com/snowflake/snowpark/WriteFileResult.html) object returned for information about the amount of data written to the file.

   From the `WriteFileResult` object, you can access the output produced by the COPY INTO <location> command:

   - To access the rows of output as an array of [Row](../reference/scala/com/snowflake/snowpark/Row.html) objects, use the `rows` value member.
   - To determine which fields are present in the rows, use the `schema` value member, which is a [StructType](../reference/scala/com/snowflake/snowpark/types/StructType$.html) that
     describes the fields in the row.

   For example, to print out the names of the fields and values in the output rows:

   Copy code

   ```
   val writeFileResult = dfWriter.csv("@mystage/saved_data")
   for ((row, index) <- writeFileResult.rows.zipWithIndex) {
     (writeFileResult.schema.fields, writeFileResult.rows(index).toSeq).zipped.foreach {
    (structField, element) => println(s"${structField.name}: $element")
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
val df = session.table("car_sales")
val writeFileResult = df.write.mode(SaveMode.Overwrite).option("DETAILED_OUTPUT", "TRUE").option("compression", "none").json("@mystage/saved_data")
for ((row, index) <- writeFileResult.rows.zipWithIndex) {
  println(s"Row: $index")
  (writeFileResult.schema.fields, writeFileResult.rows(index).toSeq).zipped.foreach {
    (structField, element) => println(s"${structField.name}: $element")
  }
}
```

## Working with Semi-Structured Data

Using a DataFrame, you can query and access [semi-structured data](/user-guide/semistructured-intro) (for example, JSON data).
The next sections explain how to work with semi-structured data in a DataFrame.

- [Traversing Semi-Structured Data](#label-snowpark-dataframe-semistructured-traverse)
- [Explicitly Casting Values in Semi-Structured Data](#label-snowpark-dataframe-semistructured-cast)
- [Flattening an Array of Objects into Rows](#label-snowpark-dataframe-semistructured-flatten)

Note

The examples in these sections use the sample data in [Sample Data Used in Examples](/user-guide/querying-semistructured#label-sample-data-semistructured-data).

### Traversing Semi-Structured Data

To refer to a specific field or element in semi-structured data, use the following methods of the [Column](../reference/scala/com/snowflake/snowpark/Column.html) object:

- Use [Column.apply(“<field\_name>”)](../reference/scala/com/snowflake/snowpark/Column.html#apply(field:String):com.snowflake.snowpark.Column) to return a `Column` object for a field in an OBJECT (or a VARIANT that contains an
  OBJECT).
- Use [Column.apply(<index>)](../reference/scala/com/snowflake/snowpark/Column.html#apply(idx:Int):com.snowflake.snowpark.Column) to return a `Column` object for an element in an ARRAY (or a VARIANT that contains an ARRAY).

Note

If the field name or elements in the path are irregular and make it difficult to use the `Column.apply` methods, you can
use the [get](../reference/scala/com/snowflake/snowpark/functions$.html#get(col1:com.snowflake.snowpark.Column,col2:com.snowflake.snowpark.Column):com.snowflake.snowpark.Column), [get\_ignore\_case](../reference/scala/com/snowflake/snowpark/functions$.html#get_ignore_case(obj:com.snowflake.snowpark.Column,field:com.snowflake.snowpark.Column):com.snowflake.snowpark.Column), or [get\_path](../reference/scala/com/snowflake/snowpark/functions$.html#get_path(col:com.snowflake.snowpark.Column,path:com.snowflake.snowpark.Column):com.snowflake.snowpark.Column) functions as an alternative.

As mentioned in [Using the Method to Refer to a Column](#label-snowpark-dataframe-apply-method), you can omit the method name `apply`:

Copy code

```
col("column_name")("field_name")
col("column_name")(index)
```

For example, the following code selects the `dealership` field in objects in the `src` column of the
[sample data](/user-guide/querying-semistructured#label-sample-data-semistructured-data):

Copy code

```
val df = session.table("car_sales")
df.select(col("src")("dealership")).show()
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
values to a specific type, see [Explicitly Casting Values in Semi-Structured Data](#label-snowpark-dataframe-semistructured-cast).

You can also [chain method calls](#label-snowpark-dataframe-chaining-method-calls) to traverse a path to a specific field or
element.

For example, the following code selects the `name` field in the `salesperson` object:

Copy code

```
val df = session.table("car_sales")
df.select(col("src")("salesperson")("name")).show()
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
val df = session.table("car_sales")
df.select(col("src")("vehicle")(0)).show()
df.select(col("src")("vehicle")(0)("price")).show()
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

As an alternative to the `apply` method, you can use the [get](../reference/scala/com/snowflake/snowpark/functions$.html#get(col1:com.snowflake.snowpark.Column,col2:com.snowflake.snowpark.Column):com.snowflake.snowpark.Column), [get\_ignore\_case](../reference/scala/com/snowflake/snowpark/functions$.html#get_ignore_case(obj:com.snowflake.snowpark.Column,field:com.snowflake.snowpark.Column):com.snowflake.snowpark.Column), or [get\_path](../reference/scala/com/snowflake/snowpark/functions$.html#get_path(col:com.snowflake.snowpark.Column,path:com.snowflake.snowpark.Column):com.snowflake.snowpark.Column) functions if the field
name or elements in the path are irregular and make it difficult to use the `Column.apply` methods.

For example, the following lines of code both print the value of a specified field in an object:

Copy code

```
df.select(get(col("src"), lit("dealership"))).show()
df.select(col("src")("dealership")).show()
```

Similarly, the following lines of code both print the value of a field at a specified path in an object:

Copy code

```
df.select(get_path(col("src"), lit("vehicle[0].make"))).show()
df.select(col("src")("vehicle")(0)("make")).show()
```

### Explicitly Casting Values in Semi-Structured Data

By default, the values of fields and elements are returned as string literals (including the double quotes), as shown in the
examples above.

To avoid unexpected results, call the [cast](#label-snowpark-dataframe-cols-cast) method to cast the value to a specific
type. For example, the following code prints out the values without and with casting:

Copy code

```
// Import the objects for the data types, including StringType.
import com.snowflake.snowpark.types._
...
val df = session.table("car_sales")
df.select(col("src")("salesperson")("id")).show()
df.select(col("src")("salesperson")("id").cast(StringType)).show()
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
[DataFrame.flatten](../reference/scala/com/snowflake/snowpark/DataFrame.html#flatten(input:com.snowflake.snowpark.Column):com.snowflake.snowpark.DataFrame) method. This method is equivalent to the [FLATTEN](/sql-reference/functions/flatten) SQL function. If you pass in
a path to an object or array, the method returns a DataFrame that contains a row for each field or element in the object or array.

For example, in the [sample data](/user-guide/querying-semistructured#label-sample-data-semistructured-data), `src:customer` is an array of objects that
contain information about a customer. Each object contains a `name` and `address` field.

If you pass this path to the `flatten` function:

Copy code

```
val df = session.table("car_sales")
df.flatten(col("src")("customer")).show()
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
df.flatten(col("src")("customer")).select(col("value")("name"), col("value")("address")).show()
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
[casting the values to a specific type](#label-snowpark-dataframe-semistructured-cast) and changing the names of the columns:

Copy code

```
df.flatten(col("src")("customer")).select(col("value")("name").cast(StringType).as("Customer Name"), col("value")("address").cast(StringType).as("Customer Address")).show()
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

Note that the SQL statement won’t be executed until you [call an action method](#label-snowpark-dataframe-action-method).

Copy code

```
// Get the list of the files in a stage.
// The collect() method causes this SQL statement to be executed.
val dfStageFiles = session.sql("ls @myStage")
val files = dfStageFiles.collect()
files.foreach(println)

// Resume the operation of a warehouse.
// Note that you must call the collect method in order to execute
// the SQL statement.
session.sql("alter warehouse if exists myWarehouse resume if suspended").collect()

val tableDf = session.table("table").select(col("a"), col("b"))
// Get the count of rows from the table.
val numRows = tableDf.count()
println("Count: " + numRows);
```

If you want to [call methods to transform the DataFrame](#label-snowpark-dataframe-transform) (e.g. filter, select, etc.),
note that these methods work only if the underlying SQL statement is a SELECT statement. The transformation methods are not
supported for other kinds of SQL statements.

Copy code

```
val df = session.sql("select id, category_id, name from sample_product_data where id > 10")
// Because the underlying SQL statement for the DataFrame is a SELECT statement,
// you can call the filter method to transform this DataFrame.
val results = df.filter(col("category_id") < 10).select(col("id")).collect()
results.foreach(println)

// In this example, the underlying SQL statement is not a SELECT statement.
val dfStageFiles = session.sql("ls @myStage")
// Calling the filter method results in an error.
dfStageFiles.filter(...)
```
