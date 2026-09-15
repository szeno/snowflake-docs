# Executing a UDF

You can execute a user-defined function (UDF) or user-defined table function (UDTF) in the same way that you execute other functions.

## Tools for executing UDFs

Choose the tool for executing the function.

| Language | Approach |
| --- | --- |
| **SQL**  Execute a SQL command, such as by using Snowsight. | [Execute the SQL SELECT command](#label-call-udf-calling-udf) to execute a UDF. |
| **Java, Python, or Scala with Snowpark**  Write code locally in one of the supported languages, having the code execute in Snowflake. | Execute client code that uses Snowpark APIs in one of the following languages.   - [Java](/developer-guide/snowpark/java/calling-functions) - [Python](/developer-guide/snowpark/python/calling-functions) - [Scala](/developer-guide/snowpark/scala/calling-functions) |
| **Command line**  Create and manage Snowflake entities by executing commands from the command line. | Execute commands of the [Snowflake CLI](/developer-guide/snowflake-cli/index):   - [To execute SQL commands](/developer-guide/snowflake-cli/command-reference/sql-commands/sql). - [To execute Snowpark commands](/developer-guide/snowflake-cli/command-reference/snowpark-commands/execute). |
| **Python**  On the client, write code that executes management operations on Snowflake. | Execute code that uses the [Snowflake Python API](/developer-guide/snowflake-python-api/snowflake-python-managing-functions-procedures). |
| **RESTful APIs** (language-agnostic)  Make requests of RESTful endpoints to create and manage Snowflake entities. | Make a request to create a function using the [Snowflake REST API](/developer-guide/snowflake-rest-api/user-defined-function/user-defined-function-introduction) |

Expand

Show lessSee more

## Calling a UDF with SQL

In general, you call a UDF same way that you call other functions.

If a UDF has arguments, you can specify those arguments by name and by position.

For example, the following UDF accepts three arguments:

Copy code

```
CREATE OR REPLACE FUNCTION udf_concatenate_strings(
    first_arg VARCHAR,
    second_arg VARCHAR,
    third_arg VARCHAR)
  RETURNS VARCHAR
  LANGUAGE SQL
  AS
  $$
    SELECT first_arg || second_arg || third_arg
  $$;
```

When calling the UDF, you can specify the arguments by name:

Copy code

```
SELECT udf_concatenate_strings(
  first_arg => 'one',
  second_arg => 'two',
  third_arg => 'three');
```

```
+--------------------------+
| UDF_CONCATENATE_STRINGS( |
|   FIRST_ARG => 'ONE',    |
|   SECOND_ARG => 'TWO',   |
|   THIRD_ARG => 'THREE')  |
|--------------------------|
| onetwothree              |
+--------------------------+
```

If you specify the arguments by name, you don’t need to specify the arguments in any particular order:

Copy code

```
SELECT udf_concatenate_strings(
  third_arg => 'three',
  first_arg => 'one',
  second_arg => 'two');
```

```
+--------------------------+
| UDF_CONCATENATE_STRINGS( |
|   THIRD_ARG => 'THREE',  |
|   FIRST_ARG => 'ONE',    |
|   SECOND_ARG => 'TWO')   |
|--------------------------|
| onetwothree              |
+--------------------------+
```

You can also specify the arguments by position:

Copy code

```
SELECT udf_concatenate_strings(
  'one',
  'two',
  'three');
```

```
+--------------------------+
| UDF_CONCATENATE_STRINGS( |
|   'ONE',                 |
|   'TWO',                 |
|   'THREE')               |
|--------------------------|
| onetwothree              |
+--------------------------+
```

You can also specify the arguments by both position and name:

Copy code

```
SELECT udf_concatenate_strings(
  'one',
  'two',
  third_arg => 'three');
```

```
+--------------------------+
| UDF_CONCATENATE_STRINGS( |
|   'ONE',                 |
|   'TWO',                 |
|   THIRD_ARG => 'THREE')  |
|--------------------------|
| onetwothree              |
+--------------------------+
```

Note

- When you mix arguments by position and by name, all of the positional arguments must come before
  all of the named arguments.
- When you specify an argument by name, you can’t use double quotes around the argument name.

- If two functions have the same name but different argument types, you can use the argument names to specify
  which function to execute, if the argument names are different. For more information, see
  [Overloading procedures and functions](/developer-guide/udf-stored-procedure-naming-conventions#label-procedure-function-name-overloading).

### Calling a UDF that has optional arguments

If the UDF has [optional arguments](/developer-guide/udf-stored-procedure-arguments#label-procedure-function-arguments-optional), you can omit the optional arguments in
the call. Each optional argument has a default value that is used when the argument is omitted.

For example, the following UDF has one required argument and two optional arguments. Each optional argument has a default value.

Copy code

```
CREATE OR REPLACE FUNCTION build_string_udf(
    word VARCHAR,
    prefix VARCHAR DEFAULT 'pre-',
    suffix VARCHAR DEFAULT '-post'
  )
  RETURNS VARCHAR
  AS
  $$
    SELECT prefix || word || suffix
  $$
  ;
```

You can omit any of the optional arguments in the call. When you omit an argument, the default value of the argument is used.

Copy code

```
SELECT build_string_udf('hello');
```

```
+---------------------------+
| BUILD_STRING_UDF('HELLO') |
|---------------------------|
| pre-hello-post            |
+---------------------------+
```

Copy code

```
SELECT build_string_udf('hello', 'before-');
```

```
+--------------------------------------+
| BUILD_STRING_UDF('HELLO', 'BEFORE-') |
|--------------------------------------|
| before-hello-post                    |
+--------------------------------------+
```

If you need to omit an optional argument and specify another optional argument that appears after the omitted argument in the
signature, use named arguments, rather than positional arguments.

For example, suppose that you want to omit the `prefix` argument and specify the `suffix` argument. The `suffix` argument
appears after the `prefix` in the signature, so you must specify the arguments by name:

Copy code

```
SELECT build_string_udf(word => 'hello', suffix => '-after');
```

```
+-------------------------------------------------------+
| BUILD_STRING_UDF(WORD => 'HELLO', SUFFIX => '-AFTER') |
|-------------------------------------------------------|
| pre-hello-after                                       |
+-------------------------------------------------------+
```

### Calling a UDTF

You can call a UDTF the way you would call any table function. When calling a UDTF in the FROM clause of a query, specify the
UDTF’s name and arguments inside the parentheses that follow the TABLE keyword, as you would when
[calling a built-in table function](/sql-reference/functions-table#label-using-a-table-in-from-clause).

In other words, use a form such as the following for the TABLE keyword when calling a UDTF:

Copy code

```
SELECT ...
  FROM TABLE ( udtf_name (udtf_arguments) )
```

Code in the following example calls the `my_java_udtf` table function, specifying a DATE literal in the argument
`'2021-01-16'::DATE`.

Copy code

```
SELECT ...
  FROM TABLE(my_java_udtf('2021-01-16'::DATE));
```

The argument to a table function can be an expression, not just a literal. For example, a table function can be called using
a column from a table. Some examples are below, including in the [Examples section](#label-using-a-table-as-input-to-a-judtf).

As is the case with [calling UDFs](#label-call-udf-calling-udf), you can specify the arguments by name or by position.

For more information about table functions in general, see [table function](/sql-reference/functions-table).

Note

You cannot call a UDF within the DEFAULT clause of a CREATE TABLE statement.

#### Using a table or UDTF as input to a UDTF

The input to a table function can come from a table or from another UDTF, as documented in
[Using a table as input to a table function](/sql-reference/functions-table#label-using-a-table-as-input-to-a-table-function).

The example below shows how to use a table to provide input to the UDTF `split_file_into_words`:

Copy code

```
create table file_names (file_name varchar);
insert into file_names (file_name) values ('sample.txt'),
                                          ('sample_2.txt');

select f.file_name, w.word
   from file_names as f, table(split_file_into_words(f.file_name)) as w;
```

The output looks similar to the following:

Copy code

```
+-------------------+------------+
| FILE_NAME         | WORD       |
+-------------------+------------+
| sample_data.txt   | some       |
| sample_data.txt   | words      |
| sample_data_2.txt | additional |
| sample_data_2.txt | words      |
+-------------------+------------+
```

The IMPORTS clause of the UDTF must specify the name and path of each file passed to the UDTF. For example:

Copy code

```
create function split_file_into_words(inputFileName string)
    ...
    imports = ('@inline_jars/sample.txt', '@inline_jars/sample_2.txt')
    ...
```

Each file must already have been copied to a stage (in this case, the stage named `@inline_jars`) before the UDTF reads the file.

For an example of using a UDTF as an input to another UDTF, see [Extended examples using table values and other UDTFs as input](/developer-guide/udf/javascript/udf-javascript-tabular-functions#label-udf-javascript-tabular-using-table-values-as-input) in
the JavaScript UDTF documentation.

#### Table functions and partitions

Before rows are passed to table functions, the rows can be grouped into *partitions*. Partitioning has two main benefits:

- Partitioning allows Snowflake to divide up the workload to improve parallelization and thus performance.
- Partitioning allows Snowflake to process all rows with a common characteristic as a group.
  You can return results that are based on all rows in the group, not just on individual rows.

For example, you might partition stock price data into one group per stock. All stock prices for an individual company can be
analyzed together, while stock prices for each company can be analyzed independently of any other company.

Data can be partitioned explicitly or implicitly.

##### Explicit partitioning

**Explicit Partitioning into Multiple Groups**

The following statement calls the UDTF named `my_udtf` on individual partitions. Each partition contains all rows for which
the `PARTITION BY` expression evaluates to the same value (e.g. the same company or stock symbol).

Copy code

```
SELECT *
    FROM stocks_table AS st,
         TABLE(my_udtf(st.symbol, st.transaction_date, st.price) OVER (PARTITION BY st.symbol))
```

**Explicit Partitioning into a Single Group**

The following statement calls the UDTF named `my_udtf` on one partition. The `PARTITION BY <constant>` clause
(in this case `PARTITION BY 1`) puts all rows in the same partition.

Copy code

```
SELECT *
    FROM stocks_table AS st,
         TABLE(my_udtf(st.symbol, st.transaction_date, st.price) OVER (PARTITION BY 1))
```

For a more complete and realistic example, see [Examples of calling Java UDTFs in queries](/developer-guide/udf/java/udf-java-tabular-functions#label-examples-of-calling-java-udtfs-in-queries), in particular the subsection
titled [Single Partition](/developer-guide/udf/java/udf-java-tabular-functions#label-examples-of-calling-java-udtfs-in-queries-single-partition).

**Sorting Rows for Partitions**

To process each partition’s rows in a specified order, include an ORDER BY clause. This tells Snowflake to pass the rows
to the per-row handler method in the specified order.

For example, if you want to calculate the moving average of a stock price over time, then order the stock prices by timestamp (and
partition by stock symbol). The following example shows how to do this:

Copy code

```
SELECT *
     FROM stocks_table AS st,
          TABLE(my_udtf(st.symbol, st.transaction_date, st.price) OVER (PARTITION BY st.symbol ORDER BY st.transaction_date))
```

An OVER clause can contain an ORDER BY clause even without a PARTITION BY clause.

Remember that including an ORDER BY clause inside an OVER clause is not the same as putting an ORDER BY clause at the
outermost level of the query. If you want the entire query results to be ordered, you need a separate ORDER BY clause. For
example:

Copy code

```
SELECT *
    FROM stocks_table AS st,
         TABLE(my_udtf(st.symbol, st.transaction_date, st.price) OVER (PARTITION BY st.symbol ORDER BY st.transaction_date))
    ORDER BY st.symbol, st.transaction_date, st.transaction_time;
```

**Usage Notes for Explicit Partitioning**

When using a UDTF with a PARTITION BY clause, the PARTITION BY clause must use a column reference or a literal,
not a general expression. For example, the following is not allowed:

Copy code

```
SELECT * FROM udtf_table, TABLE(my_func(col1) OVER (PARTITION BY udtf_table.col2 * 2));   -- NO!
```

##### Implicit partitioning

If a table function does not explicitly partition the rows by using a PARTITION BY clause, then Snowflake typically partitions
the rows implicitly to use parallel processing to improve performance.

The number of partitions is typically based on factors such as the size of the warehouse processing the function and the
cardinality of the input relation. The rows are typically assigned to specific partitions based on factors such
as physical location of the rows (e.g. by micro-partition), so the partition grouping has no meaning.
