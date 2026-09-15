Categories:
:   [Aggregate functions](/sql-reference/functions-aggregation) , [Window functions](/sql-reference/functions-window)

# HASH\_AGG

Returns an aggregate signed 64-bit hash value over the (unordered) set of input rows. HASH\_AGG never returns NULL, even if no input is provided. Empty input “hashes” to `0`.

One use for aggregate hash functions is to detect changes to a set of values without comparing the individual old and new values. HASH\_AGG can compute a single hash value
based on many inputs; almost any change to one of the inputs is likely to result in a change to the output of the HASH\_AGG function. Comparing two lists of values typically
requires sorting both lists, but HASH\_AGG produces the same value regardless of the order of the inputs. Because the values don’t need to be sorted for HASH\_AGG,
performance is typically much faster.

Note

HASH\_AGG is *not* a cryptographic hash function and should not be used as such.

For cryptographic purposes, use the SHA family of functions (in [String & binary functions](/sql-reference/functions-string)).

See also:
:   [HASH](/sql-reference/functions/hash)

## Syntax

**Aggregate function**

Copy code

```
HASH_AGG( [ DISTINCT ] <expr> [ , <expr2> ... ] )

HASH_AGG(*)
```

**Window function**

Copy code

```
HASH_AGG( [ DISTINCT ] <expr> [ , <expr2> ... ] ) OVER ( [ PARTITION BY <expr3> ] )

HASH_AGG(*) OVER ( [ PARTITION BY <expr3> ] )
```

## Arguments

`exprN`
:   The expression can be a general expression of any Snowflake data type, except
    [GEOGRAPHY](/sql-reference/data-types-geospatial#label-data-types-geography) and [GEOMETRY](/sql-reference/data-types-geospatial#label-data-types-geometry).

`expr2`
:   You can include additional expressions.

`expr3`
:   The column to partition on, if you want the result to be split into multiple
    windows.

`*`
:   Returns an aggregated hash value over all columns for all records, including records with
    NULL values. You can specify the wildcard for both the aggregate function and the window
    function.

    When you pass a wildcard to the function, you can qualify the wildcard with the name or alias for the table.
    For example, to pass in all of the columns from the table named `mytable`, specify the following:

    Copy code

    ```
    (mytable.*)
    ```

    You can also use the ILIKE and EXCLUDE keywords for filtering:

    - ILIKE filters for column names that match the specified pattern. Only one
      pattern is allowed. For example:

      Copy code

      ```
      (* ILIKE 'col1%')
      ```
    - EXCLUDE filters out column names that don’t match the specified column or columns. For example:

      Copy code

      ```
      (* EXCLUDE col1)

      (* EXCLUDE (col1, col2))
      ```

    Qualifiers are valid when you use these keywords. The following example uses the ILIKE keyword to
    filter for all of the columns that match the pattern `col1%` in the table `mytable`:

    Copy code

    ```
    (mytable.* ILIKE 'col1%')
    ```

    The ILIKE and EXCLUDE keywords can’t be combined in a single function call.

    For this function, the ILIKE and EXCLUDE keywords are valid only in a SELECT list or GROUP BY clause.

    For more information about the ILIKE and EXCLUDE keywords, see the “Parameters” section in [SELECT](/sql-reference/sql/select).

## Returns

Returns a signed 64-bit value as NUMBER(19,0).

HASH\_AGG never returns NULL, even for NULL inputs.

## Usage notes

- HASH\_AGG computes a “fingerprint” over an entire table, query result, or window. Any change to the input will
  influence the result of HASH\_AGG with overwhelming probability. This can be used to quickly detect changes to table
  contents or query results.

  Note that it is possible, though very unlikely, that two different input tables will produce the same result for HASH\_AGG. If you need to make sure that two tables or query results that
  produce the same HASH\_AGG result really contain the same data, you must still compare the data for equality (for example, by using the MINUS operator). For more details, see
  [Set operators](/sql-reference/operators-query).
- HASH\_AGG is *not* order-sensitive (that is, the order of rows in an input table or query result does not influence the result of HASH\_AGG). However, changing the order of input columns
  *does* change the result.
- HASH\_AGG hashes individual input rows using the [HASH](/sql-reference/functions/hash) function. The salient features of this function carry over to HASH\_AGG. In particular, HASH\_AGG is “stable” in the sense
  that any two rows that compare as equal and have compatible types are guaranteed to hash to the same value (that is, they influence the result of HASH\_AGG in the same way).

  For example, changing the scale and precision of a column that is part of some table doesn’t change the result of HASH\_AGG over that table. See [HASH](/sql-reference/functions/hash) for details.
- In contrast to most other aggregate functions, HASH\_AGG doesn’t ignore NULL inputs (that is, NULL inputs influence the result of HASH\_AGG).
- For both the aggregate function and the window function, duplicate rows, including duplicate all-NULL rows,
  influence the result. The DISTINCT keyword can be used to suppress the effect of duplicate rows.

- When this function is called as a window function, it does not support:
  - An ORDER BY clause within the OVER clause.
  - Explicit window frames.

## Collation details

- Two strings that are identical but have different collation specifications have the same hash value. In other words,
  only the string, not the collation specification, affects the hash value.
- Two strings that are different, but compare as equal according to a collation, might have a different hash value. For
  example, two strings that are identical using punctuation-insensitive collation normally have different hash
  values because only the string, not the collation specification, affects the hash value.

## Examples

This example shows that NULLs are not ignored:

Copy code

```
SELECT HASH_AGG(NULL), HASH_AGG(NULL, NULL), HASH_AGG(NULL, NULL, NULL);
```

```
+----------------------+----------------------+----------------------------+
|       HASH_AGG(NULL) | HASH_AGG(NULL, NULL) | HASH_AGG(NULL, NULL, NULL) |
|----------------------+----------------------+----------------------------|
| -5089618745711334219 |  2405106413361157177 |       -5970411136727777524 |
+----------------------+----------------------+----------------------------+
```

This example shows that empty input hashes to `0`:

Copy code

```
SELECT HASH_AGG(NULL) WHERE 0 = 1;
```

```
+----------------+
| HASH_AGG(NULL) |
|----------------|
|              0 |
+----------------+
```

Use HASH\_AGG(\*) to conveniently aggregate over all input columns:

Copy code

```
SELECT HASH_AGG(*) FROM orders;
```

```
+---------------------+
|     HASH_AGG(*)     |
|---------------------|
| 1830986524994392080 |
+---------------------+
```

This example shows that grouped aggregation is supported:

Copy code

```
SELECT YEAR(o_orderdate), HASH_AGG(*)
  FROM ORDERS GROUP BY 1 ORDER BY 1;
```

```
+-------------------+----------------------+
| YEAR(O_ORDERDATE) |     HASH_AGG(*)      |
|-------------------+----------------------|
| 1992              | 4367993187952496263  |
| 1993              | 7016955727568565995  |
| 1994              | -2863786208045652463 |
| 1995              | 1815619282444629659  |
| 1996              | -4747088155740927035 |
| 1997              | 7576942849071284554  |
| 1998              | 4299551551435117762  |
+-------------------+----------------------+
```

This example suppresses duplicate rows using DISTINCT (duplicate rows influence results of HASH\_AGG):

Copy code

```
SELECT YEAR(o_orderdate), HASH_AGG(o_custkey, o_orderdate)
  FROM orders GROUP BY 1 ORDER BY 1;
```

```
+-------------------+----------------------------------+
| YEAR(O_ORDERDATE) | HASH_AGG(O_CUSTKEY, O_ORDERDATE) |
|-------------------+----------------------------------|
| 1992              | 5686635209456450692              |
| 1993              | -6250299655507324093             |
| 1994              | 6630860688638434134              |
| 1995              | 6010861038251393829              |
| 1996              | -767358262659738284              |
| 1997              | 6531729365592695532              |
| 1998              | 2105989674377706522              |
+-------------------+----------------------------------+
```

Copy code

```
SELECT YEAR(o_orderdate), HASH_AGG(DISTINCT o_custkey, o_orderdate)
  FROM orders GROUP BY 1 ORDER BY 1;
```

```
+-------------------+-------------------------------------------+
| YEAR(O_ORDERDATE) | HASH_AGG(DISTINCT O_CUSTKEY, O_ORDERDATE) |
|-------------------+-------------------------------------------|
| 1992              | -8416988862307613925                      |
| 1993              | 3646533426281691479                       |
| 1994              | -7562910554240209297                      |
| 1995              | 6413920023502140932                       |
| 1996              | -3176203653000722750                      |
| 1997              | 4811642075915950332                       |
| 1998              | 1919999828838507836                       |
+-------------------+-------------------------------------------+
```

This example computes the number of days on which the corresponding sets of customers with orders with status not equal `'F'` and status not equal `'P'`, respectively, are identical:

Copy code

```
SELECT COUNT(DISTINCT o_orderdate) FROM orders;
```

```
+-----------------------------+
| COUNT(DISTINCT O_ORDERDATE) |
|-----------------------------|
| 2406                        |
+-----------------------------+
```

Copy code

```
SELECT COUNT(o_orderdate)
  FROM (SELECT o_orderdate, HASH_AGG(DISTINCT o_custkey)
    FROM orders
    WHERE o_orderstatus <> 'F'
    GROUP BY 1
    INTERSECT
      SELECT o_orderdate, HASH_AGG(DISTINCT o_custkey)
        FROM orders
        WHERE o_orderstatus <> 'P'
        GROUP BY 1);
```

```
+--------------------+
| COUNT(O_ORDERDATE) |
|--------------------|
| 1143               |
+--------------------+
```

The query doesn’t account for the possibility of hash collisions, so the actual number of days might be slightly lower.
