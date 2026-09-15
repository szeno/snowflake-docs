# Speeding up text queries with search optimization

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Search optimization can improve the performance of queries that use the [SEARCH](/sql-reference/functions/search)
and [SEARCH\_IP](/sql-reference/functions/search_ip) functions. These queries search for character data (text) and IP
addresses in specified columns from one or more tables, including elements in VARIANT, OBJECT, and ARRAY columns.

The following sections provide more information about search optimization support for text queries:

- [Enabling search optimization for text queries](#label-search-optimization-service-text-support-setup)
- [Conditions for runtime use of FULL\_TEXT search optimization](#label-search-optimization-service-queries-text-conditions)
- [Examples of ADD (and DROP) FULL\_TEXT search optimization](#label-search-optimization-service-queries-text-examples)

## Enabling search optimization for text queries

To improve the performance of text queries on a table, use the
[ON FULL\_TEXT clause in the ALTER TABLE … ADD SEARCH OPTIMIZATION command](/sql-reference/sql/alter-table#label-alter-table-searchoptimizationaction-add)
for specific columns. Enabling search optimization at the table level doesn’t enable it for queries that use the
SEARCH or SEARCH\_IP function.

For example:

Copy code

```
ALTER TABLE lines ADD SEARCH OPTIMIZATION
  ON FULL_TEXT(play, character, line);
```

For more information, see [Enabling and disabling search optimization](/user-guide/search-optimization/enabling).

## Conditions for runtime use of FULL\_TEXT search optimization

After you have enabled FULL\_TEXT search optimization on a table that is queried with the
SEARCH function, the search access path for the optimization can be used during query planning and execution.
The following conditions must be met:

- The search optimization must be ready for use (`active` column = TRUE in the DESCRIBE SEARCH
  OPTIMIZATION output).
- The search optimization must be enabled on a superset of the columns specified in the SEARCH predicate. For example,
  if a table contains VARCHAR columns `c1,c2,c3,c4,c5`, the search optimization covers columns `c1,c2,c3`, and the function
  searches one, two, or three of those columns (but not `c4` or `c5`), the query can benefit from FULL\_TEXT search
  optimization.
- The analyzer defined for the search optimization in the ALTER TABLE command must be the same as the analyzer specified in
  the SEARCH function call.

Tip

To find out if a specific search access path was used for a query, look for a `Search Optimization Access`
node in the query profile.

## Examples of ADD (and DROP) FULL\_TEXT search optimization

The following examples show how to enable FULL\_TEXT search optimization on columns in a table to improve query performance
when the SEARCH function is used to query those columns.

### Enable FULL\_TEXT search optimization with a specific analyzer

The following example enables FULL\_TEXT search optimization on one column and specifies an analyzer.
The combination of optimization type and analyzer (`method`) is reflected in the DESCRIBE output.

Copy code

```
ALTER TABLE lines ADD SEARCH OPTIMIZATION
  ON FULL_TEXT(line, ANALYZER => 'UNICODE_ANALYZER');
```

Copy code

```
DESCRIBE SEARCH OPTIMIZATION ON lines;
```

```
+---------------+----------------------------+--------+------------------+--------+
| expression_id | method                     | target | target_data_type | active |
|---------------+----------------------------+--------+------------------+--------|
|             1 | FULL_TEXT UNICODE_ANALYZER | LINE   | VARCHAR(2000)    | true   |
+---------------+----------------------------+--------+------------------+--------+
```

If you enable FULL\_TEXT search optimization on the same column with the default analyzer, the DESCRIBE output
returns two rows and differentiates the two entries by expression ID and method.

Copy code

```
ALTER TABLE lines ADD SEARCH OPTIMIZATION
  ON FULL_TEXT(line);
```

Copy code

```
DESCRIBE SEARCH OPTIMIZATION ON lines;
```

```
+---------------+----------------------------+--------+------------------+--------+
| expression_id | method                     | target | target_data_type | active |
|---------------+----------------------------+--------+------------------+--------|
|             1 | FULL_TEXT UNICODE_ANALYZER | LINE   | VARCHAR(2000)    | true   |
|             2 | FULL_TEXT DEFAULT_ANALYZER | LINE   | VARCHAR(2000)    | false  |
+---------------+----------------------------+--------+------------------+--------+
```

### Enable FULL\_TEXT search optimization on a VARIANT column

The following command enables FULL\_TEXT search optimization on a VARIANT column.
(This `car_sales` table and its data are described under [Querying Semi-structured Data](/user-guide/querying-semistructured).)

Copy code

```
ALTER TABLE car_sales ADD SEARCH OPTIMIZATION
  ON FULL_TEXT(src);

DESCRIBE SEARCH OPTIMIZATION ON car_sales;
```

```
+---------------+----------------------------+--------+------------------+--------+
| expression_id | method                     | target | target_data_type | active |
|---------------+----------------------------+--------+------------------+--------|
|             1 | FULL_TEXT DEFAULT_ANALYZER | SRC    | VARIANT          | true   |
+---------------+----------------------------+--------+------------------+--------+
```

### Enable FULL\_TEXT search optimization on an OBJECT column

The following example enables FULL\_TEXT search optimization on an OBJECT column.

First, create a table with an OBJECT column and insert data:

Copy code

```
CREATE OR REPLACE TABLE so_object_example (object_column OBJECT);

INSERT INTO so_object_example (object_column)
  SELECT OBJECT_CONSTRUCT('a', 1::VARIANT, 'b', 2::VARIANT);
```

The following command enables FULL\_TEXT search optimization on the OBJECT column.

Copy code

```
ALTER TABLE so_object_example ADD SEARCH OPTIMIZATION
  ON FULL_TEXT(object_column);

DESCRIBE SEARCH OPTIMIZATION ON so_object_example;
```

```
+---------------+----------------------------+---------------+------------------+--------+
| expression_id | method                     | target        | target_data_type | active |
|---------------+----------------------------+---------------+------------------+--------|
|             1 | FULL_TEXT DEFAULT_ANALYZER | OBJECT_COLUMN | OBJECT           | true   |
+---------------+----------------------------+---------------+------------------+--------+
```

### Enable FULL\_TEXT search optimization on an ARRAY column

The following example enables FULL\_TEXT search optimization on an ARRAY column.

First, create a table with an ARRAY column and insert data:

Copy code

```
CREATE OR REPLACE TABLE so_array_example (array_column ARRAY);

INSERT INTO so_array_example (array_column)
  SELECT ARRAY_CONSTRUCT('a', 'b', 'c');
```

The following command enables FULL\_TEXT search optimization on the ARRAY column.

Copy code

```
ALTER TABLE so_array_example ADD SEARCH OPTIMIZATION
  ON FULL_TEXT(array_column);

DESCRIBE SEARCH OPTIMIZATION ON so_array_example;
```

```
+---------------+----------------------------+--------------+------------------+--------+
| expression_id | method                     | target       | target_data_type | active |
|---------------+----------------------------+--------------+------------------+--------|
|             1 | FULL_TEXT DEFAULT_ANALYZER | ARRAY_COLUMN | ARRAY            | true   |
+---------------+----------------------------+--------------+------------------+--------+
```

### Drop FULL\_TEXT optimization from one or more columns

You can enable FULL\_TEXT optimization on multiple columns, then later drop the optimization
from one or more of those columns. The remaining columns are still optimized.

Copy code

```
ALTER TABLE lines ADD SEARCH OPTIMIZATION
  ON FULL_TEXT(play, act_scene_line, character, line, ANALYZER => 'UNICODE_ANALYZER');

DESCRIBE SEARCH OPTIMIZATION ON lines;
```

```
+---------------+----------------------------+----------------+------------------+--------+
| expression_id | method                     | target         | target_data_type | active |
|---------------+----------------------------+----------------+------------------+--------|
|             1 | FULL_TEXT UNICODE_ANALYZER | PLAY           | VARCHAR(50)      | true   |
|             2 | FULL_TEXT UNICODE_ANALYZER | ACT_SCENE_LINE | VARCHAR(10)      | true   |
|             3 | FULL_TEXT UNICODE_ANALYZER | CHARACTER      | VARCHAR(30)      | true   |
|             4 | FULL_TEXT UNICODE_ANALYZER | LINE           | VARCHAR(2000)    | true   |
+---------------+----------------------------+----------------+------------------+--------+
```

Copy code

```
ALTER TABLE lines DROP SEARCH OPTIMIZATION ON 1, 2, 3;
```

Copy code

```
DESCRIBE SEARCH OPTIMIZATION ON lines;
```

```
+---------------+----------------------------+--------+------------------+--------+
| expression_id | method                     | target | target_data_type | active |
|---------------+----------------------------+--------+------------------+--------|
|             4 | FULL_TEXT UNICODE_ANALYZER | LINE   | VARCHAR(2000)    | true   |
+---------------+----------------------------+--------+------------------+--------+
```

### Use the wildcard (\*) to enable search optimization on all qualifying columns

The following ALTER TABLE command enables FULL\_TEXT search optimization on all four VARCHAR columns in the
`lines` table:

Copy code

```
ALTER TABLE lines ADD SEARCH OPTIMIZATION
  ON FULL_TEXT(*);
```

Copy code

```
DESCRIBE SEARCH OPTIMIZATION ON lines;
```

```
+---------------+----------------------------+----------------+------------------+--------+
| expression_id | method                     | target         | target_data_type | active |
|---------------+----------------------------+----------------+------------------+--------|
|             1 | FULL_TEXT DEFAULT_ANALYZER | PLAY           | VARCHAR(50)      | true   |
|             2 | FULL_TEXT DEFAULT_ANALYZER | ACT_SCENE_LINE | VARCHAR(10)      | true   |
|             3 | FULL_TEXT DEFAULT_ANALYZER | CHARACTER      | VARCHAR(30)      | true   |
|             4 | FULL_TEXT DEFAULT_ANALYZER | LINE           | VARCHAR(2000)    | true   |
+---------------+----------------------------+----------------+------------------+--------+
```

### Expected error when enabling FULL\_TEXT optimization

The following ALTER TABLE command fails with an expected error because one of the specified columns
is a NUMBER column:

Copy code

```
ALTER TABLE lines ADD SEARCH OPTIMIZATION
  ON FULL_TEXT(play, speech_num, act_scene_line, character, line);
```

```
001128 (42601): SQL compilation error: error line 1 at position 76
Expression FULL_TEXT(IDX_SRC_TABLE.SPEECH_NUM) cannot be used in search optimization.
```
