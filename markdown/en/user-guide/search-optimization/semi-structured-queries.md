# Speeding up queries of semi-structured data with search optimization

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

The search optimization service can improve the performance of point lookup and substring queries on semi-structured
data in Snowflake tables (that is, data in [VARIANT, OBJECT, and ARRAY columns](/sql-reference/data-types-semistructured)).
You can configure search optimization on columns of these types even when the structure is deeply nested and
changes frequently. You can also enable search optimization for specific elements within a semi-structured column.

The following sections provide more information about search optimization support for queries of semi-structured data:

- [Enabling search optimization for queries of semi-structured data](#label-search-optimization-service-semi-structured-support-setup)
- [Supported data types for constants and casts in predicates for semi-structured types](#label-search-optimization-service-variant-predicates-types)
- [Support for semi-structured data type values cast to VARCHAR](#label-search-optimization-service-variant-cast-text)
- [Supported predicates for point lookups on VARIANT types](#label-search-optimization-service-variant-predicates-examples)
- [Substring search in VARIANT types](#label-search-optimization-service-variant-substring)
- [Current limitations in support for semi-structured types](#label-search-optimization-service-variant-limitations)

## Enabling search optimization for queries of semi-structured data

To improve the performance for queries of semi-structured data on a table, use the
[ON clause in the ALTER TABLE … ADD SEARCH OPTIMIZATION command](/sql-reference/sql/alter-table#label-alter-table-searchoptimizationaction-add)
for specific columns or elements in columns. Queries against VARIANT, OBJECT, and ARRAY columns aren’t optimized if you
omit the ON clause. Enabling search optimization at the table level doesn’t enable it for columns with semi-structured
data types.

For example:

Copy code

```
ALTER TABLE mytable ADD SEARCH OPTIMIZATION ON EQUALITY(myvariantcol);
ALTER TABLE t1 ADD SEARCH OPTIMIZATION ON EQUALITY(c4:user.uuid);

ALTER TABLE mytable ADD SEARCH OPTIMIZATION ON SUBSTRING(myvariantcol);
ALTER TABLE t1 ADD SEARCH OPTIMIZATION ON SUBSTRING(c4:user.uuid);

ALTER TABLE mytable ADD SEARCH OPTIMIZATION ON EQUALITY(object_column);
ALTER TABLE mytable ADD SEARCH OPTIMIZATION ON SUBSTRING(object_column);

ALTER TABLE mytable ADD SEARCH OPTIMIZATION ON EQUALITY(array_column);
ALTER TABLE mytable ADD SEARCH OPTIMIZATION ON SUBSTRING(array_column);
```

For more information, see [Enabling and disabling search optimization](/user-guide/search-optimization/enabling).

## Supported data types for constants and casts in predicates for semi-structured types

The search optimization service can improve the performance of
[point lookups of semi-structured data](/user-guide/querying-semistructured) where the
following types are used for the constant and the [implicit or explicit cast](/sql-reference/data-type-conversion) for the
element:

- FIXED (including casts that specify a valid precision and scale)
- INTEGER (including synonymous types)
- VARCHAR (including synonymous types)
- DATE (including casts that specify a scale)
- TIME (including casts that specify a scale)
- TIMESTAMP, TIMESTAMP\_LTZ, TIMESTAMP\_NTZ, TIMESTAMP\_TZ (including casts that specify a scale)

The search optimization service supports the casting of types using:

- [CAST and the :: operator](/sql-reference/functions/cast)
- [TRY\_CAST](/sql-reference/functions/try_cast)

## Support for semi-structured data type values cast to VARCHAR

The search optimization service can also improve the performance of point lookups in which columns with semi-structured data types are cast
to VARCHAR and are compared to constants that are cast to VARCHAR.

For example, suppose that `src` is a VARIANT column containing BOOLEAN, DATE, and TIMESTAMP values that have been converted to VARIANT:

Copy code

```
CREATE OR REPLACE TABLE test_table
(
  id INTEGER,
  src VARIANT
);

INSERT INTO test_table SELECT 1, TO_VARIANT('true'::BOOLEAN);
INSERT INTO test_table SELECT 2, TO_VARIANT('2020-01-09'::DATE);
INSERT INTO test_table SELECT 3, TO_VARIANT('2020-01-09 01:02:03.899'::TIMESTAMP);
```

For this table, the search optimization service can improve the following queries, which cast the VARIANT column to VARCHAR and
compare the column to string constants:

Copy code

```
SELECT * FROM test_table WHERE src::VARCHAR = 'true';
SELECT * FROM test_table WHERE src::VARCHAR = '2020-01-09';
SELECT * FROM test_table WHERE src::VARCHAR = '2020-01-09 01:02:03.899';
```

## Supported predicates for point lookups on VARIANT types

The search optimization service can improve point lookup queries with the types of predicates listed below. In the examples
below, `src` is the column with a semi-structured data type, and `path_to_element` is a
[path to an element in the column with a semi-structured data type](/user-guide/querying-semistructured#label-traversing-semistructured-data).

- Equality predicates of the following form:

  `WHERE path_to_element[::target_data_type] = constant`

  In this syntax, `target_data_type` (if specified) and the data type of `constant` must be one
  of the [supported types](#label-search-optimization-service-variant-predicates-types).

  For example, the search optimization service supports:

  - Matching a VARIANT element against a NUMBER constant without explicitly casting the element.

    Copy code

    ```
    WHERE src:person.age = 42;
    ```
  - Explicitly casting a VARIANT element to NUMBER with a specified precision and scale.

    Copy code

    ```
    WHERE src:location.temperature::NUMBER(8, 6) = 23.456789;
    ```
  - Matching a VARIANT element against a VARCHAR constant without explicitly casting the element.

    Copy code

    ```
    WHERE src:sender_info.ip_address = '123.123.123.123';
    ```
  - Explicitly casting a VARIANT element to VARCHAR.

    Copy code

    ```
    WHERE src:salesperson.name::VARCHAR = 'John Appleseed';
    ```
  - Explicitly casting a VARIANT element to DATE.

    Copy code

    ```
    WHERE src:events.date::DATE = '2021-03-26';
    ```
  - Explicitly casting a VARIANT element to TIMESTAMP with a specified scale.

    Copy code

    ```
    WHERE src:event_logs.exceptions.timestamp_info(3) = '2021-03-26 15:00:00.123 -0800';
    ```
  - Matching an ARRAY element against a value of a [supported type](#label-search-optimization-service-variant-predicates-types),
    with or without explicitly casting to the type. For example:

    Copy code

    ```
    WHERE my_array_column[2] = 5;

    WHERE my_array_column[2]::NUMBER(4, 1) = 5;
    ```
  - Matching an OBJECT element against a value of a [supported type](#label-search-optimization-service-variant-predicates-types),
    with or without explicitly casting to the type. For example:

    Copy code

    ```
    WHERE object_column['mykey'] = 3;

    WHERE object_column:mykey = 3;

    WHERE object_column['mykey']::NUMBER(4, 1) = 3;

    WHERE object_column:mykey::NUMBER(4, 1) = 3;
    ```
- Predicates that use the ARRAY functions, such as:

  - `WHERE ARRAY_CONTAINS(value_expr, array)`

    In this syntax, `value_expr` must not be NULL and must evaluate to VARIANT. The data type of the value must be one of
    the [supported types](#label-search-optimization-service-variant-predicates-types).

    For example:

    Copy code

    ```
    WHERE ARRAY_CONTAINS('77.146.211.88'::VARIANT, src:logs.ip_addresses)
    ```

    In this example, the value is a constant that is implicitly cast to a VARIANT:

    Copy code

    ```
    WHERE ARRAY_CONTAINS(300, my_array_column)
    ```
  - `WHERE ARRAYS_OVERLAP(ARRAY_CONSTRUCT(constant_1, constant_2, .., constant_N), array)`

    The data type of each constant (`constant_1`, `constant_2`, and so on) must be one of the
    [supported types](#label-search-optimization-service-variant-predicates-types). The constructed ARRAY can
    include NULL constants.

    In this example, the array is in a VARIANT value:

    Copy code

    ```
    WHERE ARRAYS_OVERLAP(
      ARRAY_CONSTRUCT('122.63.45.75', '89.206.83.107'), src:senders.ip_addresses)
    ```

    In this example, the array is an ARRAY column:

    Copy code

    ```
    WHERE ARRAYS_OVERLAP(
      ARRAY_CONSTRUCT('a', 'b'), my_array_column)
    ```
- The following predicates that check for NULL values:

  - `WHERE IS_NULL_VALUE(path_to_element)`

    Note that [IS\_NULL\_VALUE](/sql-reference/functions/is_null_value) applies to JSON null values and not to SQL NULL values.
  - `WHERE path_to_element IS NOT NULL`
  - `WHERE semistructured_column IS NULL`

    where `semistructured_column` refers to the column and not a path to an element in the semi-structured data.

    For example, the search optimization service supports using the VARIANT column `src` but not the path to the element
    `src:person.age` in that VARIANT column.

## Substring search in VARIANT types

The search optimization service can optimize [wildcard or regular expression searches](/user-guide/search-optimization/substring-queries#label-search-optimization-service-queries-wildcard-regexp)
in [semi-structured columns](/sql-reference/data-types-semistructured) — that is, VARIANT, OBJECT, and ARRAY columns —
or elements in such columns.

The search optimization service can optimize predicates that use the following functions:

- [LIKE](/sql-reference/functions/like)
- [LIKE ANY](/sql-reference/functions/like_any)
- [LIKE ALL](/sql-reference/functions/like_all)
- [ILIKE](/sql-reference/functions/ilike)
- [ILIKE ANY](/sql-reference/functions/ilike_any)
- [CONTAINS](/sql-reference/functions/contains)
- [ENDSWITH](/sql-reference/functions/endswith)
- [STARTSWITH](/sql-reference/functions/startswith)
- [SPLIT\_PART](/sql-reference/functions/split_part)
- [RLIKE](/sql-reference/functions/rlike)
- [REGEXP](/sql-reference/functions/regexp)
- [REGEXP\_LIKE](/sql-reference/functions/regexp_like)

You can enable substring search optimization for a column or for multiple individual elements within a column. For
example, the following statement enables substring search optimization for a nested element in a column:

Copy code

```
ALTER TABLE test_table ADD SEARCH OPTIMIZATION ON SUBSTRING(col2:data.search);
```

After the search access path has been built, the following query can be optimized:

Copy code

```
SELECT * FROM test_table WHERE col2:data.search LIKE '%optimization%';
```

However, the following queries aren’t optimized because the WHERE clause filters don’t apply to the element
that was specified when search optimization was enabled (`col2:data.search`):

Copy code

```
SELECT * FROM test_table WHERE col2:name LIKE '%simon%parker%';
SELECT * FROM test_table WHERE col2 LIKE '%hello%world%';
```

You can specify multiple elements to be optimized. In the following example, search optimization is enabled for two specific
elements in the column `col2`:

Copy code

```
ALTER TABLE test_table ADD SEARCH OPTIMIZATION ON SUBSTRING(col2:name);
ALTER TABLE test_table ADD SEARCH OPTIMIZATION ON SUBSTRING(col2:data.search);
```

If you enable search optimization for a given element, it is enabled for any nested elements. The second ALTER TABLE statement
below is redundant because the first statement enables search optimization for the entire `data` element, including
the nested `search` element.

Copy code

```
ALTER TABLE test_table ADD SEARCH OPTIMIZATION ON SUBSTRING(col2:data);
ALTER TABLE test_table ADD SEARCH OPTIMIZATION ON SUBSTRING(col2:data.search);
```

Similarly, enabling search optimization for an entire column allows all substring searches on that column to be optimized,
including elements nested to any depth within it.

For an example that enables FULL\_TEXT search optimization on a VARIANT column in the `car_sales` table and its data,
which is described in [Querying Semi-structured Data](/user-guide/querying-semistructured), see
[Enable FULL\_TEXT search optimization on a VARIANT column](/user-guide/search-optimization/text-queries#label-search-optimization-service-queries-text-examples-variant).

### How constants are evaluated for VARIANT substring searches

When it evaluates the constant string in a query — for example, `LIKE 'constant_string'` — the search optimization service splits the
string into tokens by using the following characters as delimiters:

- Square brackets (`[` and `]`).
- Curly braces (`{` and `}`).
- Colons (`:`).
- Commas (`,`).
- Double quotes (`"`).

After it splits the string into tokens, the search optimization service considers only tokens that are at least five characters long.
The following table explains how the search optimization service handles various predicate examples:

| Example of a predicate | How the search optimization service handles the query |
| --- | --- |
| `LIKE '%TEST%'` | The search optimization service *doesn’t use* search access paths for the following predicate because the substring is shorter than five characters. |
| `LIKE '%SEARCH%IS%OPTIMIZED%'` | The search optimization service can optimize this query, by using search access paths to search for `SEARCH` and `OPTIMIZED` but not `IS`. `IS` is shorter than five characters. |
| `LIKE '%HELLO_WORLD%'` | The search optimization service can optimize this query, by using search access paths to search for `HELLO_WORLD`. |
| `LIKE '%COL:ON:S:EVE:RYWH:ERE%'` | The search optimization service splits this string into `COL`, `ON`, `S`, `EVE`, `RYWH`, `ERE`. Because all of these tokens are shorter than five characters, the search optimization service can’t optimize this query. |
| `LIKE '%{\"KEY01\":{\"KEY02\":\"value\"}%'` | The search optimization service splits this string into the tokens `KEY01`, `KEY02`, `VALUE` and uses the tokens when it optimizes the query. |
| `LIKE '%quo\"tes_and_com,mas,\"are_n\"ot\"_all,owed%'` | The search optimization service splits this string into the tokens `quo`, `tes_and_com`, `mas`, `are_n`, `ot`, `_all`, `owed`. The search optimization service can only use the tokens that are five characters or longer (`tes_and_com`, `are_n`) when it optimizes the query. |

Expand

Show lessSee more

## Current limitations in support for semi-structured types

Support for semi-structured types in the search optimization service is limited in the following ways:

- Predicates of the form `path_to_element IS NULL` aren’t supported.
- Predicates where the constants are results of scalar subqueries aren’t supported.
- Predicates that specify paths to elements that contain sub-elements aren’t supported.
- Predicates that use the [XMLGET](/sql-reference/functions/xmlget) function aren’t supported.

The [current limitations of the search optimization service](/user-guide/search-optimization/queries-that-benefit#label-search-optimization-limitations) also apply to
semi-structured types.
