# Enabling and disabling search optimization

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

To enable search optimization, use a role that has the necessary privileges, then enable it for an entire table or
specific columns using the [ALTER TABLE](/sql-reference/sql/alter-table) …
[ADD SEARCH OPTIMIZATION](/sql-reference/sql/alter-table#label-alter-table-searchoptimizationaction-add) command.

## Required access control privileges

To add, configure, or remove search optimization for a table, you must:

- Have OWNERSHIP privilege on the table.
- Have ADD SEARCH OPTIMIZATION privilege on the schema that contains the table. To grant this privilege:

  Copy code

  ```
  GRANT ADD SEARCH OPTIMIZATION ON SCHEMA <schema_name> TO ROLE <role>
  ```

To use the search optimization service for a query, you just need the SELECT privilege on the table.

You don’t need any additional privileges. Because SEARCH OPTIMIZATION is a table property, it is automatically
detected and used (if appropriate) when querying a table.

## Configuring search optimization

Note

Adding search optimization to a large table (a table containing terabytes (TB) or more of data) might result in an immediate
increase in credit consumption over a short period of time.

When you add search optimization to a table, the maintenance service immediately starts building the search access paths for the
table in the background. If the table is large, the maintenance service might massively parallelize this work, which can result
in increased costs over a short period of time.

Before you add search optimization to a large table,
[get an estimate of these costs](/user-guide/search-optimization/cost-estimation#label-search-optimization-estimate-costs) so that you know what to expect.

When you enable search optimization, you have a choice of enabling it for a whole table or for specific columns in the
table.

- Enabling search optimization for a whole table enables it for point-lookup queries on all eligible columns.

  To enable search optimization for a whole table, use the [ALTER TABLE](/sql-reference/sql/alter-table) …
  [ADD SEARCH OPTIMIZATION](/sql-reference/sql/alter-table#label-alter-table-searchoptimizationaction-add) command *without* the ON clause.
- Enabling search optimization for specific columns avoids spending credits on creating search access paths for columns
  that you don’t often use in queries, and also allows you to select additional types of queries to be optimized for
  each column, potentially further increasing performance.

  To enable search optimization for specific columns, specifying the types of queries to be optimized, use the
  [ON clause in the ALTER TABLE … ADD SEARCH OPTIMIZATION command](#label-search-optimization-service-configuration-adding).
  In the ON clause in ADD SEARCH OPTIMIZATION, you specify which columns should be enabled for search optimization. When enabling
  search optimization for a given column, you can also specify a search method (for example, EQUALITY for equality and IN searches,
  GEO for GEOGRAPHY searches, or SUBSTRING for substring searches). You can enable more than one search method on the same column.
- You can enable search optimization for a whole Apache Iceberg™ table or for specific columns in the table by using the
  [ALTER ICEBERG TABLE](/sql-reference/sql/alter-iceberg-table) …
  [ADD SEARCH OPTIMIZATION](/sql-reference/sql/alter-iceberg-table#label-alter-iceberg-table-searchoptimizationaction) command.

In general, enabling search optimization only for specific columns is the best practice.

The following sections explain how to configure search optimization for a table:

- [Enabling search optimization for specific columns](#label-search-optimization-service-configuration-adding)
- [Enabling search optimization for an entire table](#label-search-optimization-service-configuration-entire-table)

After you have configured search optimization, you can inspect your configuration to make sure it is correct.

- [Verifying that a table is configured for search optimization](#label-search-optimization-service-configuration-verify)

You can remove search optimization from specific columns or whole tables when you have discovered that search
optimization does not provide enough benefit.

- [Removing search optimization from specific columns or the entire table](#label-search-optimization-service-configuration-removing)

## Enabling search optimization for specific columns

To configure search optimization for a specific column, use the
[ALTER TABLE](/sql-reference/sql/alter-table) …
[ADD SEARCH OPTIMIZATION](/sql-reference/sql/alter-table#label-alter-table-searchoptimizationaction-add) command with the ON clause.

Note

When running this command, use a role that has
[the privileges to add search optimization to the table](/user-guide/search-optimization/enabling#label-access-control-privileges-for-search-optimization).

The ON clause specifies that you want to configure search optimization for specific columns. For details on the syntax, see
[the section on ALTER TABLE … ADD SEARCH OPTIMIZATION](/sql-reference/sql/alter-table#label-alter-table-searchoptimizationaction-add).

Note

If you just want to apply search optimization for equality and IN predicates to all applicable columns in the table, see
[Enabling search optimization for an entire table](#label-search-optimization-service-configuration-entire-table).

After running this command, you can
[verify that the columns have been configured for search optimization](#label-search-optimization-service-configuration-verify).

The next sections contain examples that demonstrate how to specify the configuration for search optimization:

- [Example: Full-text search optimization on specific columns](#label-enable-full-text-search)
- [Example: Supporting equality and IN predicates for specific columns](#label-search-optimization-service-configuration-example-basic)
- [Example: Supporting equality and IN predicates for all applicable columns](#label-search-optimization-service-configuration-example-wildcard)
- [Example: Supporting different types of predicates](#label-search-optimization-service-configuration-example-different-methods)
- [Example: Supporting different predicates on the same column](#label-search-optimization-service-configuration-example-same-col)
- [Example: Supporting equality and IN predicates for an element in a VARIANT](#label-search-optimization-service-configuration-example-variant)
- [Example: Supporting geospatial functions](#label-search-optimization-service-configuration-example-geo)

### Example: Full-text search optimization on specific columns

You can perform text searches by using the [SEARCH](/sql-reference/functions/search) and [SEARCH\_IP](/sql-reference/functions/search_ip)
functions. To improve query execution performance when these functions are used, enable FULL\_TEXT search optimization. You can
enable FULL\_TEXT search optimization on a table by using different subsets of the columns in the table and different text
analyzers. For information about the behavior of different analyzers, see [How search terms are tokenized](/sql-reference/functions/search#label-how-search-terms-tokenized).

Enable FULL\_TEXT search optimization on a set of columns in a table by using the following syntax.

Copy code

```
ALTER TABLE <name> ADD SEARCH OPTIMIZATION
  ON FULL_TEXT( { * | <col1> [ , <col2>, ... ] } [ , ANALYZER => '<analyzer_name>' ]);
```

The columns you specify must be VARCHAR, VARIANT, ARRAY, or OBJECT columns. Columns with other data types aren’t supported.
In addition, you can specify individual [paths](/user-guide/querying-semistructured#label-traversing-semistructured-data) to columns of type VARIANT,
ARRAY, or OBJECT.

You can specify the wildcard asterisk character (`*`) instead of a list of columns. In this case, the optimization is
automatically enabled on all the columns of supported types.

If specified, the [ANALYZER =&gt; ‘analyzer\_name’](/sql-reference/functions/search#label-search-analyzer) argument must be one of the choices that is documented for the
SEARCH function. If you don’t specify an analyzer, the DEFAULT\_ANALYZER is used.

Note

For query execution with the SEARCH function to be optimized, the analyzer specified for the search optimization
in the ALTER TABLE command must be the same as the analyzer specified in the SEARCH function call. If the analyzers don’t
match, the search access path won’t be selected.

This example enables FULL\_TEXT search optimization on three VARCHAR columns that might be the targets of a
SEARCH query.

Copy code

```
ALTER TABLE lines ADD SEARCH OPTIMIZATION
  ON FULL_TEXT(play, character, line);
```

To describe the search optimization configuration for this table, run the following command:

Copy code

```
DESCRIBE SEARCH OPTIMIZATION ON lines;
```

```
+---------------+----------------------------+-----------+------------------+--------+
| expression_id | method                     | target    | target_data_type | active |
|---------------+----------------------------+-----------+------------------+--------|
|             1 | FULL_TEXT DEFAULT_ANALYZER | PLAY      | VARCHAR(50)      | true   |
|             2 | FULL_TEXT DEFAULT_ANALYZER | CHARACTER | VARCHAR(30)      | true   |
|             3 | FULL_TEXT DEFAULT_ANALYZER | LINE      | VARCHAR(2000)    | true   |
+---------------+----------------------------+-----------+------------------+--------+
```

For more information, see [Displaying the search optimization configuration for a table](#label-search-optimization-service-configuration-displaying).

This example enables FULL\_TEXT search optimization on a VARCHAR column that might be the target of a
SEARCH\_IP query.

Copy code

```
ALTER TABLE ipt ADD SEARCH OPTIMIZATION ON FULL_TEXT(ip1, ANALYZER => 'ENTITY_ANALYZER');
```

To remove the search optimization configuration, run one of the following commands:

Copy code

```
ALTER TABLE lines DROP SEARCH OPTIMIZATION
  ON FULL_TEXT(play, character, line);
```

Copy code

```
ALTER TABLE lines DROP SEARCH OPTIMIZATION
  ON play, character, line;
```

Copy code

```
ALTER TABLE lines DROP SEARCH OPTIMIZATION
  ON 1, 2, 3;
```

In the third ALTER TABLE … DROP SEARCH OPTIMIZATION command, `1, 2, 3` refers to the expression IDs
returned by the DESCRIBE command.

You can also modify a FULL\_TEXT search optimization configuration by dropping a subset of the columns (by name or
expression ID). For more information, see [Removing search optimization from specific columns or the entire table](#label-search-optimization-service-configuration-removing).

For more examples that enable and drop FULL\_TEXT search optimization, see
[Examples of ADD (and DROP) FULL\_TEXT search optimization](/user-guide/search-optimization/text-queries#label-search-optimization-service-queries-text-examples).

### Example: Supporting equality and IN predicates for specific columns

To optimize searches with equality predicates for the columns `c1`, `c2`, and `c3` in the table `t1`, execute the
following statement:

Copy code

```
ALTER TABLE t1 ADD SEARCH OPTIMIZATION ON EQUALITY(c1, c2, c3);
```

You can also specify the same search method more than once in the ON clause:

Copy code

```
-- This statement is equivalent to the previous statement.
ALTER TABLE t1 ADD SEARCH OPTIMIZATION ON EQUALITY(c1), EQUALITY(c2, c3);
```

### Example: Supporting equality and IN predicates for all applicable columns

To optimize searches with equality predicates for all applicable columns in the table, execute the following statement:

Copy code

```
ALTER TABLE t1 ADD SEARCH OPTIMIZATION ON EQUALITY(*);
```

Note the following:

- As explained in the
  [description of the syntax for the search method and target](/sql-reference/sql/alter-table#label-alter-table-searchoptimizationaction-search-method-target),
  for a given method, you cannot specify both an asterisk and specific columns.
- Although omitting the ON clause also configures search optimization for equality and IN predicates on all applicable
  columns in the table, there are differences between specifying and omitting the ON clause. See
  [Enabling search optimization for an entire table](#label-search-optimization-service-configuration-entire-table).

### Example: Supporting different types of predicates

To optimize searches with equality predicates for the column `c1` and `c2` and substring searches for the column `c3`,
execute the following statement:

Copy code

```
ALTER TABLE t1 ADD SEARCH OPTIMIZATION ON EQUALITY(c1, c2), SUBSTRING(c3);
```

### Example: Supporting different predicates on the same column

To optimize searches for both equality predicates and substring predicates on the same column, `c1`, execute the following statement:

Copy code

```
ALTER TABLE t1 ADD SEARCH OPTIMIZATION ON EQUALITY(c1), SUBSTRING(c1);
```

### Example: Supporting equality and IN predicates for an element in a VARIANT

To optimize searches with equality predicates on the VARIANT element `uuid` nested in the element `user` in the VARIANT column
`c4`, execute the following statement:

Copy code

```
ALTER TABLE t1 ADD SEARCH OPTIMIZATION ON EQUALITY(c4:user.uuid);
```

### Example: Supporting geospatial functions

To optimize searches with predicates that use geospatial functions with GEOGRAPHY objects in the `c1` column, execute the following
statement:

Copy code

```
ALTER TABLE t1 ADD SEARCH OPTIMIZATION ON GEO(c1);
```

## Enabling search optimization for an entire table

To specify EQUALITY for all columns of the supported data types (except for
[semi-structured](/sql-reference/data-types-semistructured) and [GEOGRAPHY](/sql-reference/data-types-geospatial#label-data-types-geography)),
use the [ALTER TABLE](/sql-reference/sql/alter-table) …
[ADD SEARCH OPTIMIZATION](/sql-reference/sql/alter-table#label-alter-table-searchoptimizationaction-add) command without the ON clause.

Note

When running this command, use a role that has
[the privileges to add search optimization to the table](/user-guide/search-optimization/enabling#label-access-control-privileges-for-search-optimization).

For example:

Copy code

```
ALTER TABLE test_table ADD SEARCH OPTIMIZATION;
```

For more information on the syntax, see
[the section on search optimization in ALTER TABLE](/sql-reference/sql/alter-table#label-alter-table-searchoptimizationaction).

After running this command, you can
[verify that the columns have been configured for search optimization](#label-search-optimization-service-configuration-verify).

### Effect on subsequently added columns

After you run ALTER TABLE … ADD SEARCH OPTIMIZATION command without the ON clause, any columns that are subsequently added to the table
will also be configured for optimization on EQUALITY.

However, if you execute ALTER TABLE … { ADD | DROP } SEARCH OPTIMIZATION with the ON clause on the same table, any
columns that are subsequently added to the table won’t be configured for EQUALITY automatically. You must execute
ALTER TABLE … ADD SEARCH OPTIMIZATION ON … to configure these newly added columns for EQUALITY.

## Verifying that a table is configured for search optimization

To verify that the table and its columns have been configured for search optimization:

1. [Display the search optimization configuration](#label-search-optimization-service-configuration-displaying) for the
   table and its columns.
2. Run the [SHOW TABLES](/sql-reference/sql/show-tables) command to verify that search optimization has been added and to determine how
   much of the table has been optimized.

   For example:

   Copy code

   ```
   SHOW TABLES LIKE '%test_table%';
   ```

   In the output from this command:

   - Verify that SEARCH\_OPTIMIZATION is `ON`, which indicates that search optimization has been added.
   - Check the value of SEARCH\_OPTIMIZATION\_PROGRESS. This specifies the percentage of the table that has been optimized so far.

     When search optimization is first added to a table, the performance benefits don’t appear immediately.
     The search optimization service starts populating data in the background. The benefits appear increasingly as
     the maintenance catches up to the current state of the table.

     Before you run a query to verify that search optimization is working, wait until this shows that the table has been fully
     optimized.
3. Run a query to verify that search optimization is working.

   Note that the Snowflake optimizer automatically chooses when to use the search optimization service for a particular query.
   Users cannot control which queries search optimization is used for.

   Choose a query that the search optimization service is designed to optimize.
   See [Identifying queries that can benefit from search optimization](/user-guide/search-optimization/queries-that-benefit#label-search-optimization-service-when-should-you-use-search-paths).
4. In the web UI, view the query plan for this query, and verify that the query node “Search Optimization Access” is part of the
   query plan.

## Displaying the search optimization configuration for a table

To display the search optimization configuration for a table, use the [DESCRIBE SEARCH OPTIMIZATION](/sql-reference/sql/desc-search-optimization) command.

For example, suppose that you execute the following statement to configure search optimization for a column:

Copy code

```
ALTER TABLE t1 ADD SEARCH OPTIMIZATION ON EQUALITY(c1);
```

Executing DESCRIBE SEARCH OPTIMIZATION produces the following output:

Copy code

```
DESCRIBE SEARCH OPTIMIZATION ON t1;
```

```
+---------------+----------+--------+------------------+--------+
| expression_id |  method  | target | target_data_type | active |
+---------------+----------+--------+------------------+--------+
| 1             | EQUALITY | C1     | NUMBER(38,0)     | true   |
+---------------+----------+--------+------------------+--------+
```

## Removing search optimization from specific columns or the entire table

You can remove the search optimization configuration for specific columns, or you can remove the SEARCH OPTIMIZATION property
from the entire table.

- [Dropping search optimization for specific columns](#label-search-optimization-service-configuration-dropping)
- [Removing search optimization from the table](#label-search-optimization-service-configuration-dropping-all)

### Dropping search optimization for specific columns

To drop the search optimization configuration for specific columns, use the following command:
[ALTER TABLE](/sql-reference/sql/alter-table) …
[DROP SEARCH OPTIMIZATION](/sql-reference/sql/alter-table#label-alter-table-searchoptimizationaction-drop) command with the ON clause.

For example, suppose that executing the DESCRIBE SEARCH OPTIMIZATION command prints the following expressions:

Copy code

```
DESCRIBE SEARCH OPTIMIZATION ON t1;
```

```
+---------------+-----------+-----------+-------------------+--------+
| expression_id |  method   | target    | target_data_type  | active |
+---------------+-----------+-----------+-------------------+--------+
|             1 | EQUALITY  | C1        | NUMBER(38,0)      | true   |
|             2 | EQUALITY  | C2        | VARCHAR(16777216) | true   |
|             3 | EQUALITY  | C4        | NUMBER(38,0)      | true   |
|             4 | EQUALITY  | C5        | VARCHAR(16777216) | true   |
|             5 | EQUALITY  | V1        | VARIANT           | true   |
|             6 | SUBSTRING | C2        | VARCHAR(16777216) | true   |
|             7 | SUBSTRING | C5        | VARCHAR(16777216) | true   |
|             8 | GEO       | G1        | GEOGRAPHY         | true   |
|             9 | EQUALITY  | V1:"key1" | VARIANT           | true   |
|            10 | EQUALITY  | V1:"key2" | VARIANT           | true   |
+---------------+-----------+-----------+-------------------+--------+
```

To drop search optimization for substrings on the column `c2`, execute the following statement:

Copy code

```
ALTER TABLE t1 DROP SEARCH OPTIMIZATION ON SUBSTRING(c2);
```

To drop search optimization for all methods on the column `c5`, execute the following statement:

Copy code

```
ALTER TABLE t1 DROP SEARCH OPTIMIZATION ON c5;
```

Because the column `c5` is configured to optimize equality and substring searches, the statement above drops the configuration
for equality and substring searches for `c5`.

To drop search optimization for equality on the column `c1` and to drop the configuration specified by the expression IDs `6`
and `8`, execute the following statement:

Copy code

```
ALTER TABLE t1 DROP SEARCH OPTIMIZATION ON EQUALITY(c1), 6, 8;
```

For more information on the syntax, see
[the section on ALTER TABLE … DROP SEARCH OPTIMIZATION](/sql-reference/sql/alter-table#label-alter-table-searchoptimizationaction-drop).

### Removing search optimization from the table

To remove the SEARCH OPTIMIZATION property from a table:

1. Switch to a role that has [the privileges to remove search optimization from the table](/user-guide/search-optimization/enabling#label-access-control-privileges-for-search-optimization).
2. Run the [ALTER TABLE](/sql-reference/sql/alter-table) …
   [DROP SEARCH OPTIMIZATION](/sql-reference/sql/alter-table#label-alter-table-searchoptimizationaction-drop) command without the ON clause:

   Copy code

   ```
   ALTER TABLE [IF EXISTS] <table_name> DROP SEARCH OPTIMIZATION;
   ```

   For example:

   Copy code

   ```
   ALTER TABLE test_table DROP SEARCH OPTIMIZATION;
   ```

For more information, see
[the section on ALTER TABLE … DROP SEARCH OPTIMIZATION](/sql-reference/sql/alter-table#label-alter-table-searchoptimizationaction-drop).
