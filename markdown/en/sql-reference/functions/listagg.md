Categories:
:   [Aggregate functions](/sql-reference/functions-aggregation) (General) , [Window function syntax and usage](/sql-reference/functions-window-syntax) (General)

# LISTAGG

Returns the concatenated input values, separated by the `delimiter` string.

## Syntax

**Aggregate function**

Copy code

```
LISTAGG( [ DISTINCT ] <expr1> [, <delimiter> ] )
    [ WITHIN GROUP ( <orderby_clause> ) ]
```

**Window function**

Copy code

```
LISTAGG( [ DISTINCT ] <expr1> [, <delimiter> ] )
    [ WITHIN GROUP ( <orderby_clause> ) ]
    OVER ( [ PARTITION BY <expr2> ] )
```

## Required arguments

`expr1`
:   An expression (typically a column name) that determines the values to be put into the list.
    The expression must evaluate to a string, or to a data type that can be
    [cast](/sql-reference/data-type-conversion) to string.

`OVER()`
:   The OVER clause is required when the function is being used as a window function.
    For details, see [Window function syntax and usage](/sql-reference/functions-window-syntax).

## Optional arguments

`DISTINCT`
:   Removes duplicate values from the list.

`delimiter`
:   A string, or an expression that evaluates to a string. Typically, this value is
    a single-character string. The string should be surrounded by single
    quotes, as shown in the examples below.

    If no `delimiter` is specified, an empty string is used as
    the `delimiter`.

    The `delimiter` must be a constant.

`WITHIN GROUP orderby_clause`
:   One or more expressions (typically column names) that determine the order of the values for
    each group in the list.

    The WITHIN GROUP (ORDER BY) syntax supports the same parameters as the
    [ORDER BY](/sql-reference/constructs/order-by) clause in a SELECT statement.

`PARTITION BY expr2`
:   Window function sub-clause that specifies an expression (typically a column name).
    This expression defines partitions that group the input rows before the function is applied.
    For details, see [Window function syntax and usage](/sql-reference/functions-window-syntax).

## Returns

Returns a string that includes all of the non-NULL input values, separated by the `delimiter`.

This function does not return a list or an array. It returns a single string that contains all
of the non-NULL input values.

## Usage notes

- If you do not specify WITHIN GROUP (ORDER BY), the order of elements within each list is unpredictable.
  (An ORDER BY clause outside the WITHIN GROUP clause applies to the order of the output rows, not to the order
  of the list elements within a row.)
- If you specify a number for an expression in WITHIN GROUP (ORDER BY), this number is parsed as a numeric
  constant, not as the ordinal position of a column in the SELECT list. Therefore, do not specify numbers
  as WITHIN GROUP (ORDER BY) expressions.
- If you specify DISTINCT and WITHIN GROUP, both must refer to the same column. For example:

  Copy code

  ```
  SELECT LISTAGG(DISTINCT O_ORDERKEY) WITHIN GROUP (ORDER BY O_ORDERKEY) ...;
  ```

  If you specify different columns for DISTINCT and WITHIN GROUP, an error occurs:

  Copy code

  ```
  SELECT LISTAGG(DISTINCT O_ORDERKEY) WITHIN GROUP (ORDER BY O_ORDERSTATUS) ...;
  ```

  ```
  SQL compilation error: [ORDERS.O_ORDERSTATUS] is not a valid order by expression
  ```

  You must either specify the same column for DISTINCT and WITHIN GROUP or omit DISTINCT.
- Regarding NULL or empty input values:

  - If the input is empty, an empty string is returned.
  - If all input expressions evaluate to NULL, the output is an empty string.
  - If some but not all input expressions evaluate to NULL, the output contains
    all non-NULL values and excludes the NULL values.

- When this function is called as a window function, it does not support:
  - An ORDER BY clause within the OVER clause.
  - Explicit window frames.

## Collation details

- The collation of the result is the same as the collation of the input.
- Elements inside the list are ordered according to collations, if the ORDER BY sub-clause specifies an expression
  with collation.
- The `delimiter` cannot use a collation specification.
- Specifying collation inside ORDER BY does not impact the collation of the result. For example, the statement below
  contains two ORDER BY clauses, one for LISTAGG and one for the query results. Specifying collation inside
  the first one does not affect the collation of the second one. If you need to collate the output in both ORDER BY
  clauses, you must specify collation explicitly in both clauses.

  Copy code

  ```
  SELECT LISTAGG(x, ', ') WITHIN GROUP (ORDER BY last_name COLLATE 'es')
    FROM table1
    ORDER BY last_name;
  ```

## Examples

These examples use the LISTAGG function.

### Using the LISTAGG function to concatenate values in query results

The following examples use the LISTAGG function to concatenate values in the results of
queries on orders data.

Note

These examples query the [TPC-H sample data](/user-guide/sample-data-tpch). Before
running the queries, execute the following SQL statement:

Copy code

```
USE SCHEMA snowflake_sample_data.tpch_sf1;
```

This example lists the distinct `o_orderkey` values for orders with a `o_totalprice` greater than
`520000` and uses and empty string for the `delimiter`:

Copy code

```
SELECT LISTAGG(DISTINCT o_orderkey, ' ')
  FROM orders
  WHERE o_totalprice > 520000;
```

```
+-------------------------------------------------+
| LISTAGG(DISTINCT O_ORDERKEY, ' ')               |
|-------------------------------------------------|
| 2232932 1750466 3043270 4576548 4722021 3586919 |
+-------------------------------------------------+
```

This example lists the distinct `o_orderstatus` values for orders with a `o_totalprice` greater than
`520000` and uses a vertical bar for the `delimiter`:

Copy code

```
SELECT LISTAGG(DISTINCT o_orderstatus, '|')
  FROM orders
  WHERE o_totalprice > 520000;
```

```
+--------------------------------------+
| LISTAGG(DISTINCT O_ORDERSTATUS, '|') |
|--------------------------------------|
| O|F                                  |
+--------------------------------------+
```

This example lists the `o_orderstatus` and `o_clerk` values of each order with a `o_totalprice` greater than
`520000` grouped by `o_orderstatus`. The query uses a comma for the `delimiter`:

Copy code

```
SELECT o_orderstatus,
   LISTAGG(o_clerk, ', ')
     WITHIN GROUP (ORDER BY o_totalprice DESC)
  FROM orders
  WHERE o_totalprice > 520000
  GROUP BY o_orderstatus;
```

```
+---------------+---------------------------------------------------+
| O_ORDERSTATUS | LISTAGG(O_CLERK, ', ')                            |
|               |      WITHIN GROUP (ORDER BY O_TOTALPRICE DESC)    |
|---------------+---------------------------------------------------|
| O             | Clerk#000000699, Clerk#000000336, Clerk#000000245 |
| F             | Clerk#000000040, Clerk#000000230, Clerk#000000924 |
+---------------+---------------------------------------------------+
```

### Using collation with the LISTAGG function

The following examples show [collation](/sql-reference/collation) with the LISTAGG function.
The examples use the following data:

Copy code

```
CREATE OR REPLACE TABLE collation_demo (
  spanish_phrase VARCHAR COLLATE 'es');
```

Copy code

```
INSERT INTO collation_demo (spanish_phrase) VALUES
  ('piña colada'),
  ('Pinatubo (Mount)'),
  ('pint'),
  ('Pinta');
```

Note the difference in output order with the different
collation specifications. This query uses the `es` collation specification:

Copy code

```
SELECT LISTAGG(spanish_phrase, '|')
    WITHIN GROUP (ORDER BY COLLATE(spanish_phrase, 'es')) AS es_collation
  FROM collation_demo;
```

```
+-----------------------------------------+
| ES_COLLATION                            |
|-----------------------------------------|
| Pinatubo (Mount)|pint%Pinta%piña colada |
+-----------------------------------------+
```

This query uses the `utf8` collation specification:

Copy code

```
SELECT LISTAGG(spanish_phrase, '|')
    WITHIN GROUP (ORDER BY COLLATE(spanish_phrase, 'utf8')) AS utf8_collation
  FROM collation_demo;
```

```
+-----------------------------------------+
| UTF8_COLLATION                          |
|-----------------------------------------|
| Pinatubo (Mount)|Pinta%pint%piña colada |
+-----------------------------------------+
```
