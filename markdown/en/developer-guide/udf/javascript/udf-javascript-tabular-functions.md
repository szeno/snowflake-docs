# Tabular JavaScript UDFs (UDTFs)

You can write the handler for a user-defined [table function](/sql-reference/functions-table) (UDTF) in JavaScript.

Your handler code processes rows received in the UDTF call and returns a tabular result. The received rows are partitioned,
either implicitly by Snowflake or explicitly in the syntax of the function call. You use callback functions you write to
process individual rows as well as the partitions into which they’re grouped.

The JavaScript code must meet the following requirements for the UDTF to be valid:

- The code must define a single literal JavaScript object.
- The defined object must include a callback function named `processRow()`. For more information, see
  [Object callback functions](#label-udf-javascript-object-callback-functions).

Important

If the JavaScript code does not meet these requirements, the UDTF will still be created; however, it will fail when called in a query.

Note

Tabular functions (UDTFs) have a limit of 500 input arguments and 500 output columns.

## Object callback functions

Through the JavaScript code, Snowflake interacts with the UDTF by invoking callback functions during the execution of the query. The
following skeleton outlines all available callback functions and their expected signatures:

Copy code

```
{
   processRow: function (row, rowWriter, context) {/*...*/},
   finalize: function (rowWriter, context) {/*...*/},
   initialize: function (argumentInfo, context) {/*...*/},
}
```

Note that only `processRow()` is required; the other functions are optional.

### `processRow()`

This callback function is invoked once for each row in the input relation. The arguments to `processRow()` are passed in
the `row` object. For each of the arguments defined in the [CREATE FUNCTION](/sql-reference/sql/create-function) statement used to
create the UDTF, there is a property on the `row` object with the same name in all uppercase. The value of this property
is the value of the argument for the current row. (The value is converted to a JavaScript value.)

The `rowWriter` argument is used by the user-supplied code to produce output rows. The `rowWriter` object defines a
single function, `writeRow()`. The `writeRow()` function takes one argument,
the *row object*, which is a single row in the output table represented as a JavaScript object. For each column defined in the RETURNS
clause of the [CREATE FUNCTION](/sql-reference/sql/create-function) command, a corresponding property can be defined on the row object. The value
of that property on the row object becomes the value for the corresponding column in the output relation. Any output columns without
a corresponding property on the row object will have the value NULL in the result table.

### `finalize()`

The `finalize()` callback function is invoked once, after all rows have been passed to `processRow()`. (If the data is
grouped into [partitions](#label-udf-javascript-partitions), then `finalize()` is invoked once for each partition,
after all rows in that partition have been passed to `processRow()`.)

This callback function can be used to output any state that might have been aggregated in `processRow()` using the same row
`rowWriter` as is passed to `processRow()`.

Note

While Snowflake supports large partitions with timeouts tuned to process them successfully, especially large partitions can cause
processing to time out (such as when `finalize` takes too long to complete). Please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support) if you need the
timeout threshold adjusted for specific usage scenarios.

### `initialize()`

This callback function is invoked once for each partition prior to any invocations of `processRow()`.

Use `initialize()` to set up any state needed during the result computation.

The `initialize()` function’s `argumentInfo` parameter contains metadata about the arguments to the user-defined
function. For example, if the UDF is defined as:

Copy code

```
CREATE FUNCTION f(argument_1 INTEGER, argument_2 VARCHAR) ...
```

then `argumentInfo` contains information about `argument_1` and `argument_2`.

`argumentInfo` has a property for each of those arguments. Each property is an object with the following values:

- `type`: String. The type of this argument.
- `isConst`: Boolean. If true, the value of this argument is constant (i.e. is the same for every row).
- `constValue`: If `isConst` (as defined above) is true, this entry contains the constant value of the argument; otherwise,
  this field is `undefined`.

The `initialize()` function cannot produce output rows.

### General usage notes for callback functions

- All three callback functions take a `context` object; this is reserved for future use and currently is empty.

  Caution

  Modifying the `context` object can yield undefined behavior.
- Additional functions and properties can be defined, as needed, on the object for use in the UDTF.
- The arguments to the callback functions are positional and can be named anything; however, for the purposes of this topic, the above
  names are used for the remaining discussion and examples.

## Partitions

In many situations, you might want to group rows into *partitions*. Partitioning has two main benefits:

- It allows you to group rows based on a common characteristic. This allows you to process all rows within the group together,
  and process each group independently.
- It allows Snowflake to divide up the workload to improve parallelization and thus performance.

For example, you might partition stock price data into one group per stock. All stock prices for an individual company can be
processed together, and the groups for different companies are processed independently.

The following statement calls the UDTF named `js_udtf()` on individual partitions. Each partition contains all rows for which
the `PARTITION BY` expression evaluates to the same value (e.g. the same stock symbol).

Copy code

```
SELECT * FROM tab1, TABLE(js_udtf(tab1.c1, tab1.c2) OVER (PARTITION BY <expression>)) ...;
```

When you specify a partition expression to use with a UDTF, Snowflake calls:

- `initialize()` once for each partition.
- `processRow()` once for each individual row in that partition.
- `finalize()` once for each partition (after processing the last row in that partition).

You might also want to process each partition’s rows in a specified order. For example, if you want to calculate the moving average
of a stock price over time, then order the stock prices by timestamp (as well as partitioning by stock or company). The following
example shows how to do this:

Copy code

```
SELECT * FROM tab1, TABLE(js_udtf(tab1.c1, tab1.c2) OVER (PARTITION BY <expression> ORDER BY <expression>)) ...;
```

When you specify an `ORDER BY` clause, the rows are processed in the order defined by the `ORDER BY` expression. Specifically,
the rows are passed to `processRow()` in the order defined by the `ORDER BY` expression.

In most cases, partitioning data almost automatically improves opportunities for parallelization and thus higher performance.
Snowflake usually executes several UDTF *instances* in parallel. (For this discussion, an instance of a JavaScript UDTF is defined
as one instance of the JavaScript object used to represent the function in Snowflake.) Each partition of rows is passed to a single
instance of the UDTF.

Note, however, that there is not necessarily a one-to-one relationship between partitions and UDTF instances. Although each
partition is processed by only one UDTF instance, the converse is not necessarily true — a single UDTF instance can process
multiple partitions. It is therefore important to use `initialize()` and `finalize()` to specifically set up and tear
down each partition, for example, to avoid “carrying over” accumulated values from the processing of one partition to the
processing of another partition.

### Result columns

When a table is joined to a table function, as in the partitioning examples above, the result set can contain the following, depending
on what is selected:

- The columns defined in the RETURNS clause of the [CREATE FUNCTION](/sql-reference/sql/create-function) command.
- The columns from the table, including both columns used to partition the data and other columns, whether or not they are used as input
  parameters to the UDTF.

Note that rows produced in the `processRow` callback and rows produced by `finalize` differ in the following ways:

- When a row is produced in `processRow`, Snowflake can correlate it to an input row, namely the one passed into the function
  as the `row` argument. Note that if a given `processRow` invocation produces more than one row, the input attributes are
  correlated with each output row.

  For rows produced in `processRow`, all input columns can be joined to the output relation.

In the `finalize` callback, Snowflake is unable to correlate it to any single row because there is no current row to correlate to.

- For rows produced in the `finalize` callback, only the columns used in the PARTITION BY clause are available (as these are the
  same for any row in the current partition); all other attributes are NULL. If no PARTITION BY clause is specified, all those attributes
  are NULL.

## Calling JavaScript UDTFs in queries

When calling a UDTF in the FROM clause of a query, specify the UDTF’s name and arguments inside the parentheses that follow the TABLE
keyword.

In other words, use a form such as the following for the TABLE keyword when calling a UDTF:

Copy code

```
SELECT ...
  FROM TABLE ( udtf_name (udtf_arguments) )
```

Note

For more about calling UDFs and UDTFs, see [Executing a UDF](/developer-guide/udf/udf-calling-sql).

### No partitioning

This simple example shows how to call a UDTF. This example passes literal values.
The UDTF merely returns the parameters in the reverse of the order in which they were passed.
This example does not use partitioning.

Copy code

```
SELECT * FROM TABLE(js_udtf(10.0::FLOAT, 20.0::FLOAT));
+----+----+
|  Y |  X |
|----+----|
| 20 | 10 |
+----+----+
```

This example calls a UDTF and passes it values from another table. In this example, the
UDTF named `js_udtf` is called once for each row in the table named `tab1`. Each time that the function is called,
it is passed values from columns `c1` and `c2` of the current row.
As above, the UDTF is called without a `PARTITION BY` clause.

Copy code

```
SELECT * FROM tab1, TABLE(js_udtf(tab1.c1, tab1.c2)) ;
```

When no partitioning is used, the Snowflake execution engine partitions the input itself according to multiple factors, such as the
size of the warehouse processing the function and the cardinality of the input relation. When running in this mode, the user code
can make no assumptions about partitions. This is most useful when the function only needs to look at rows in isolation to produce
its output and no state is aggregated across rows.

### Explicit partitioning

JavaScript UDTFs can also be called using a partition. For example:

Copy code

```
SELECT * FROM tab1, TABLE(js_udtf(tab1.c1, tab1.c2) OVER (PARTITION BY tab1.c3 ORDER BY tab1.c1));
```

### Explicit partitioning with an empty `OVER` clause

Copy code

```
SELECT * FROM tab1, TABLE(js_udtf(tab1.c1, tab1.c2) OVER ());
```

An empty `OVER` clause means that every row belongs to the same partition (i.e. the entire input relation is one partition).

Note

You should exercise caution when calling a JavaScript UDTF with an empty `OVER` clause because this limits Snowflake to
creating one instance of the function and, therefore, Snowflake is unable to parallelize the computation.

## Sample JavaScript UDTFs

This section contains several sample JavaScript UDTFs.

### Basic `Hello World` examples

The following JavaScript UDTF takes no parameters and always returns the same values. It is provided primarily for illustration purposes:

Copy code

```
CREATE OR REPLACE FUNCTION HelloWorld0()
    RETURNS TABLE (OUTPUT_COL VARCHAR)
    LANGUAGE JAVASCRIPT
    AS '{
        processRow: function f(row, rowWriter, context){
           rowWriter.writeRow({OUTPUT_COL: "Hello"});
           rowWriter.writeRow({OUTPUT_COL: "World"});
           }
        }';

SELECT output_col FROM TABLE(HelloWorld0());
```

Output:

Copy code

```
+------------+
| OUTPUT_COL |
+============+
| Hello      |
+------------+
| World      |
+------------+
```

The following JavaScript UDTF is also for illustration purposes, but uses an input parameter. Note that JavaScript is case-sensitive,
but SQL forces identifiers to uppercase, so when the JavaScript code references a SQL parameter name, the JavaScript code must use
uppercase.

Note also that function parameters are accessed through the parameter named `row` in the `get_params()` function:

Copy code

```
CREATE OR REPLACE FUNCTION HelloHuman(First_Name VARCHAR, Last_Name VARCHAR)
    RETURNS TABLE (V VARCHAR)
    LANGUAGE JAVASCRIPT
    AS '{
        processRow: function get_params(row, rowWriter, context){
           rowWriter.writeRow({V: "Hello"});
           rowWriter.writeRow({V: row.FIRST_NAME});  // Note the capitalization and the use of "row."!
           rowWriter.writeRow({V: row.LAST_NAME});   // Note the capitalization and the use of "row."!
           }
        }';

SELECT V AS Greeting FROM TABLE(HelloHuman('James', 'Kirk'));
```

Output:

Copy code

```
+------------+
|  GREETING  |
+============+
| Hello      |
+------------+
| James      |
+------------+
| Kirk       |
+------------+
```

### Basic examples illustrating the callback functions

The following JavaScript UDTF illustrates all the API callback functions and various output columns. It simply returns all rows as-is
and provides a count of the number of characters seen in each partition. It also illustrates how to share state across a partition
using a `THIS` reference. Note that the example uses an `initialize()` callback to initialize the counter to zero; this
is needed because a given function instance can be used to process multiple partitions:

Copy code

```
-- set up for the sample
CREATE TABLE parts (p FLOAT, s STRING);

INSERT INTO parts VALUES (1, 'michael'), (1, 'kelly'), (1, 'brian');
INSERT INTO parts VALUES (2, 'clara'), (2, 'maggie'), (2, 'reagan');

-- creation of the UDTF
CREATE OR REPLACE FUNCTION "CHAR_SUM"(INS STRING)
    RETURNS TABLE (NUM FLOAT)
    LANGUAGE JAVASCRIPT
    AS '{
    processRow: function (row, rowWriter, context) {
      this.ccount = this.ccount + 1;
      this.csum = this.csum + row.INS.length;
      rowWriter.writeRow({NUM: row.INS.length});
    },
    finalize: function (rowWriter, context) {
     rowWriter.writeRow({NUM: this.csum});
    },
    initialize: function(argumentInfo, context) {
     this.ccount = 0;
     this.csum = 0;
    }}';
```

The following query illustrates calling the `CHAR_SUM` UDTF on the `parts` table with no partitioning:

Copy code

```
SELECT * FROM parts, TABLE(char_sum(s));
```

Output:

Copy code

```
+--------+---------+-----+
| P      | S       | NUM |
+--------+---------+-----+
| 1      | michael | 7   |
| 1      | kelly   | 5   |
| 1      | brian   | 5   |
| 2      | clara   | 5   |
| 2      | maggie  | 6   |
| 2      | reagan  | 6   |
| [NULL] | [NULL]  | 34  |
+--------+---------+-----+
```

When no partitioning is specified, Snowflake automatically defines partitions. In this example, due to the small number of rows,
only one partition is created (i.e. only one invocation of `finalize()` is executed). Note that the final row has NULL values
in the input columns.

Same query, but with explicit partitioning:

Copy code

```
SELECT * FROM parts, TABLE(char_sum(s) OVER (PARTITION BY p));
```

Output:

Copy code

```
+--------+---------+-----+
| P      | S       | NUM |
+--------+---------+-----+
| 1      | michael | 7   |
| 1      | kelly   | 5   |
| 1      | brian   | 5   |
| 1      | [NULL]  | 17  |
| 2      | clara   | 5   |
| 2      | maggie  | 6   |
| 2      | reagan  | 6   |
| 2      | [NULL]  | 17  |
+--------+---------+-----+
```

This example partitions over the `p` column, yielding two partitions. For each partition, a single row is returned in the
`finalize()` callback, yielding a total of two rows, distinguished by the NULL value in the `s` column. Because
`p` is the PARTITION BY column, the rows created in `finalize()` have the value of `p` that defines the current partition.

### Extended examples using table values and other UDTFs as input

This basic UDTF converts a “range” of IP addresses to a complete list of IP addresses. The input consists of the first 3 segments
of the IP address (e.g. `'192.168.1'`) and then the start and end of the range used to generate the last segment (e.g. `42` and
`45`):

Copy code

```
CREATE OR REPLACE FUNCTION range_to_values(PREFIX VARCHAR, RANGE_START FLOAT, RANGE_END FLOAT)
    RETURNS TABLE (IP_ADDRESS VARCHAR)
    LANGUAGE JAVASCRIPT
    AS $$
      {
        processRow: function f(row, rowWriter, context)  {
          var suffix = row.RANGE_START;
          while (suffix <= row.RANGE_END)  {
            rowWriter.writeRow( {IP_ADDRESS: row.PREFIX + "." + suffix} );
            suffix = suffix + 1;
            }
          }
      }
      $$;

SELECT * FROM TABLE(range_to_values('192.168.1', 42::FLOAT, 45::FLOAT));
```

Output:

Copy code

```
+--------------+
| IP_ADDRESS   |
+==============+
| 192.168.1.42 |
+--------------+
| 192.168.1.43 |
+--------------+
| 192.168.1.44 |
+--------------+
| 192.168.1.45 |
+--------------+
```

Building on the previous example, you might want to calculate individual IP addresses for more than one range. This next statement
creates a table of ranges that can be used to expand to individual IP addresses. The query then inputs the rows from the table into
the `range_to_values()` UDTF to return the individual IP addresses:

Copy code

```
CREATE TABLE ip_address_ranges(prefix VARCHAR, range_start INTEGER, range_end INTEGER);
INSERT INTO ip_address_ranges (prefix, range_start, range_end) VALUES
    ('192.168.1', 42, 44),
    ('192.168.2', 10, 12),
    ('192.168.2', 40, 40)
    ;

SELECT rtv.ip_address
  FROM ip_address_ranges AS r, TABLE(range_to_values(r.prefix, r.range_start::FLOAT, r.range_end::FLOAT)) AS rtv;
```

Output:

Copy code

```
+--------------+
| IP_ADDRESS   |
+==============+
| 192.168.1.42 |
+--------------+
| 192.168.1.43 |
+--------------+
| 192.168.1.44 |
+--------------+
| 192.168.2.10 |
+--------------+
| 192.168.2.11 |
+--------------+
| 192.168.2.12 |
+--------------+
| 192.168.2.40 |
+--------------+
```

Attention

In this example, the syntax used in the FROM clause is identical to the syntax of an inner join (i.e. `FROM t1, t2`); however,
the operation performed is not a true inner join. The actual behavior is the `range_to_values()` function is called with the values
from each row in the `ip_address changes` table. In other words, it would be equivalent to writing:

> Copy code
>
> ```
> for input_row in ip_address_ranges:
>   output_row = range_to_values(input_row.prefix, input_row.range_start, input_row.range_end)
> ```

The concept of passing values to a UDTF can be extended to multiple UDTFs. The next example creates a UDTF named `fake_ipv4_to_ipv6()`
that “converts” IPV4 address to IPV6 addresses. The query then calls the function as part of a more complex statement involving another UDTF:

Copy code

```
-- Example UDTF that "converts" an IPV4 address to a range of IPV6 addresses.
-- (for illustration purposes only and is not intended for actual use)
CREATE OR REPLACE FUNCTION fake_ipv4_to_ipv6(ipv4 VARCHAR)
    RETURNS TABLE (IPV6 VARCHAR)
    LANGUAGE JAVASCRIPT
    AS $$
      {
        processRow: function f(row, rowWriter, context)  {
          rowWriter.writeRow( {IPV6: row.IPV4 + "." + "000.000.000.000"} );
          rowWriter.writeRow( {IPV6: row.IPV4 + "." + "..."} );
          rowWriter.writeRow( {IPV6: row.IPV4 + "." + "FFF.FFF.FFF.FFF"} );
          }
      }
      $$;

SELECT ipv6 FROM TABLE(fake_ipv4_to_ipv6('192.168.3.100'));
```

Output:

Copy code

```
+-------------------------------+
| IPV6                          |
+===============================+
| 192.168.3.100.000.000.000.000 |
+-------------------------------+
| 192.168.3.100....             |
+-------------------------------+
| 192.168.3.100.FFF.FFF.FFF.FFF |
+-------------------------------+
```

The following query uses the `fake_ipv4_to_ipv6` and `range_to_values()` UDTFs created earlier, with input from the
`ip_address changes` table. In other words, it starts with a set of IP address ranges, converts them to individual IPV4 addresses, and
then takes each IPV4 address and “converts” it to a range of IPV6 addresses:

Copy code

```
SELECT rtv6.ipv6
  FROM ip_address_ranges AS r,
       TABLE(range_to_values(r.prefix, r.range_start::FLOAT, r.range_end::FLOAT)) AS rtv,
       TABLE(fake_ipv4_to_ipv6(rtv.ip_address)) AS rtv6
  WHERE r.prefix = '192.168.2'  -- limits the output for this example
  ;
```

Output:

Copy code

```
+------------------------------+
| IPV6                         |
+==============================+
| 192.168.2.10.000.000.000.000 |
+------------------------------+
| 192.168.2.10....             |
+------------------------------+
| 192.168.2.10.FFF.FFF.FFF.FFF |
+------------------------------+
| 192.168.2.11.000.000.000.000 |
+------------------------------+
| 192.168.2.11....             |
+------------------------------+
| 192.168.2.11.FFF.FFF.FFF.FFF |
+------------------------------+
| 192.168.2.12.000.000.000.000 |
+------------------------------+
| 192.168.2.12....             |
+------------------------------+
| 192.168.2.12.FFF.FFF.FFF.FFF |
+------------------------------+
| 192.168.2.40.000.000.000.000 |
+------------------------------+
| 192.168.2.40....             |
+------------------------------+
| 192.168.2.40.FFF.FFF.FFF.FFF |
+------------------------------+
```

Note that this example used join syntax twice, but neither of the operations was a true join; both were calls to a UDTF using the
output of a table or another UDTF as input.

A true inner join is order-insensitive. For example, the following statements are identical:

`table1 INNER JOIN table2 ON ...`
`table2 INNER JOIN table1 ON ...`

Inputting values to a UDTF is not a true join, and the operations are not order-insensitive. For example, the
following query is identical to the previous example, except it reverses the order of the UDTFs in the FROM clause:

Copy code

```
SELECT rtv6.ipv6
  FROM ip_address_ranges AS r,
       TABLE(fake_ipv4_to_ipv6(rtv.ip_address)) AS rtv6,
       TABLE(range_to_values(r.prefix, r.range_start::FLOAT, r.range_end::FLOAT)) AS rtv
 WHERE r.prefix = '192.168.2'  -- limits the output for this example
  ;
```

The query fails with the following error message:

`SQL compilation error: error line 3 at position 35 invalid identifier 'RTV.IP_ADDRESS'`

The `rtv.ip_address` identifier is invalid because it was not defined before it was used. In a true join, this wouldn’t happen, but
when processing UDTFs using join syntax, this error might occur.

Next, try a statement that mixes inputting to a UDTF with a true join; however, remember that inputting to a UDTF and doing an inner join
both use the same syntax, which might be confusing:

Copy code

```
-- First, create a small table of IP address owners.
-- This table uses only IPv4 addresses for simplicity.
DROP TABLE ip_address_owners;
CREATE TABLE ip_address_owners (ip_address VARCHAR, owner_name VARCHAR);
INSERT INTO ip_address_owners (ip_address, owner_name) VALUES
  ('192.168.2.10', 'Barbara Hart'),
  ('192.168.2.11', 'David Saugus'),
  ('192.168.2.12', 'Diego King'),
  ('192.168.2.40', 'Victoria Valencia')
  ;

-- Now join the IP address owner table to the IPv4 addresses.
SELECT rtv.ip_address, ipo.owner_name
  FROM ip_address_ranges AS r,
       TABLE(range_to_values(r.prefix, r.range_start::FLOAT, r.range_end::FLOAT)) AS rtv,
       ip_address_owners AS ipo
 WHERE ipo.ip_address = rtv.ip_address AND
      r.prefix = '192.168.2'   -- limits the output for this example
  ;
```

Output:

Copy code

```
+--------------+-------------------+
| IP_ADDRESS   | OWNER_NAME        |
+==============+===================+
| 192.168.2.10 | Barbara Hart      |
+--------------+-------------------+
| 192.168.2.11 | David Saugus      |
+--------------+-------------------+
| 192.168.2.12 | Diego King        |
+--------------+-------------------+
| 192.168.2.40 | Victoria Valencia |
+--------------+-------------------+
```

Attention

The preceding example works as described; however, you should take care when combining UDTFs with true joins because this might result in non-deterministic and/or unexpected behavior.

Also, note that this behavior might change in the future.
