# Speeding up queries of structured data with search optimization

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

The search optimization service can improve the performance of point-lookup and substring queries on
structured data in Snowflake tables; that is, data in
[structured ARRAY, OBJECT, and MAP columns](/sql-reference/data-types-structured). You can configure
search optimization on columns of these types even when the structure is deeply nested and changes frequently.
You can also enable search optimization for specific elements within a structured column.

The following sections provide more information about search optimization support for queries of structured data:

- [Enabling search optimization for queries of structured data](#label-search-optimization-service-structured-support-setup)
- [Supported predicates for point lookups on structured types](#label-search-optimization-service-structured-predicates)
- [Substring search in structured types](#label-search-optimization-service-structured-substring)
- [Schema evolution support](#label-search-optimization-service-structured-schema-evolution)
- [Current limitations in support for structured types](#label-search-optimization-service-structured-limitations)

## Enabling search optimization for queries of structured data

To improve the performance for queries of structured data types on a table, use the
[ON clause in the ALTER TABLE … ADD SEARCH OPTIMIZATION command](/sql-reference/sql/alter-table#label-alter-table-searchoptimizationaction-add)
for specific columns or elements in columns. Queries against structured ARRAY, OBJECT, and MAP columns aren’t
optimized if you omit the ON clause. Enabling search optimization at the table level doesn’t enable it for columns
with structured data types.

For example:

Copy code

```
ALTER TABLE mytable ADD SEARCH OPTIMIZATION ON SUBSTRING(array_column);
ALTER TABLE mytable ADD SEARCH OPTIMIZATION ON EQUALITY(array_column[1]);

ALTER TABLE mytable ADD SEARCH OPTIMIZATION ON EQUALITY(object_column);
ALTER TABLE mytable ADD SEARCH OPTIMIZATION ON SUBSTRING(object_column:key);

ALTER TABLE mytable ADD SEARCH OPTIMIZATION ON EQUALITY(map_column);
ALTER TABLE mytable ADD SEARCH OPTIMIZATION ON EQUALITY(map_column:user.uuid);
```

The following rules apply to the keywords you use in these ALTER TABLE … ADD SEARCH OPTIMIZATION commands:

- You can use the EQUALITY keyword with any inner element or the column itself.
- You can use the SUBSTRING keyword only with inner elements that have
  [text string](/sql-reference/data-types-text#label-character-datatypes) data types.

For more information, see [Enabling and disabling search optimization](/user-guide/search-optimization/enabling).

## Supported data types for constants and casts in predicates for structured types

The search optimization service can improve the performance of point lookups of structured data where the
following types are used for the constant and the [implicit or explicit cast](/sql-reference/data-type-conversion)
for the element:

- FIXED (including casts that specify a valid precision and scale)
- INTEGER (including synonymous types)
- VARCHAR (including synonymous types)
- DATE (including casts that specify a scale)
- TIME (including casts that specify a scale)
- TIMESTAMP, TIMESTAMP\_LTZ, TIMESTAMP\_NTZ, TIMESTAMP\_TZ (including casts that specify a scale)

The search optimization service supports the casting of types by using the following conversion functions:

- [CAST and the :: operator](/sql-reference/functions/cast)
- [TRY\_CAST](/sql-reference/functions/try_cast)

## Supported predicates for point lookups on structured types

The search optimization service can improve point-lookup queries with the types of predicates shown in the following
list. In the examples, `src` is the column with a structured data type, and `path_to_element` is a
path to an element in the column with a structured data type:

- Equality predicates of the following form:

  `WHERE path_to_element[::target_data_type] = constant`

  In this syntax, `target_data_type` (if specified) and the data type of `constant` must be one
  of the [supported types](#label-search-optimization-service-structured-predicates-types).

  For example, the search optimization service supports the following predicates:

  - Matching an OBJECT or MAP element against a NUMBER constant without explicitly casting the element:

    Copy code

    ```
    WHERE src:person.age = 42;
    ```
  - Explicitly casting an OBJECT or MAP element to NUMBER with a specified precision and scale:

    Copy code

    ```
    WHERE src:location.temperature::NUMBER(8, 6) = 23.456789;
    ```
  - Matching an OBJECT or MAP element against a VARCHAR constant without explicitly casting the element:

    Copy code

    ```
    WHERE src:sender_info.ip_address = '123.123.123.123';
    ```
  - Explicitly casting an OBJECT or MAP element to VARCHAR:

    Copy code

    ```
    WHERE src:salesperson.name::VARCHAR = 'John Appleseed';
    ```
  - Explicitly casting an OBJECT or MAP element to DATE:

    Copy code

    ```
    WHERE src:events.date::DATE = '2021-03-26';
    ```
  - Explicitly casting an OBJECT or MAP element to TIMESTAMP with a specified scale:

    Copy code

    ```
    WHERE src:event_logs.exceptions.timestamp_info(3) = '2021-03-26 15:00:00.123 -0800';
    ```
  - Matching an ARRAY element against a value of a [supported type](/user-guide/search-optimization/semi-structured-queries#label-search-optimization-service-variant-predicates-types),
    with or without an explicit cast:

    Copy code

    ```
    WHERE my_array_column[2] = 5;

    WHERE my_array_column[2]::NUMBER(4, 1) = 5;
    ```
  - Matching an OBJECT or MAP element against a value of a [supported type](/user-guide/search-optimization/semi-structured-queries#label-search-optimization-service-variant-predicates-types),
    with or without an explicit cast:

    Copy code

    ```
    WHERE object_column['mykey'] = 3;

    WHERE object_column:mykey = 3;

    WHERE object_column['mykey']::NUMBER(4, 1) = 3;

    WHERE object_column:mykey::NUMBER(4, 1) = 3;
    ```
- Predicates that use the ARRAY functions, such as the following predicates:

  - `WHERE ARRAY_CONTAINS(value_expr, array)`

    In this syntax, `value_expr` must not be NULL and must evaluate to VARIANT. The data type of the
    value must be one of the [supported types](/user-guide/search-optimization/semi-structured-queries#label-search-optimization-service-variant-predicates-types):

    Copy code

    ```
    WHERE ARRAY_CONTAINS('77.146.211.88'::VARIANT, src:logs.ip_addresses)
    ```

    In this example, the value is a constant that is implicitly cast to an OBJECT:

    Copy code

    ```
    WHERE ARRAY_CONTAINS(300, my_array_column)
    ```
  - `WHERE ARRAYS_OVERLAP(ARRAY_CONSTRUCT(constant_1, constant_2, .., constant_N), array)`

    The data type of each constant — `constant_1`, `constant_2`, and so on — must be one of the
    [supported types](/user-guide/search-optimization/semi-structured-queries#label-search-optimization-service-variant-predicates-types). The constructed ARRAY can
    include NULL constants.

    In this example, the array is in an OBJECT value:

    Copy code

    ```
    WHERE ARRAYS_OVERLAP(
      ARRAY_CONSTRUCT('122.63.45.75', '89.206.83.107'), src:senders.ip_addresses)
    ```

    In this example, the array is in an ARRAY column:

    Copy code

    ```
    WHERE ARRAYS_OVERLAP(
      ARRAY_CONSTRUCT('a', 'b'), my_array_column)
    ```
- The following predicates check for NULL values:

  - `WHERE IS_NULL_VALUE(path_to_element)`

    Note

    [IS\_NULL\_VALUE](/sql-reference/functions/is_null_value) applies to JSON null values and not to SQL NULL values.
  - `WHERE path_to_element IS NOT NULL`
  - `WHERE structured_column IS NULL`

    where `structured_column` refers to the column and not a path to an element in the structured data.

    For example, the search optimization service supports using the OBJECT column `src` but not the path to the element
    `src:person.age` in that OBJECT column.

## Substring search in structured types

You can enable substring search only if the target structured element is a
[text string](/sql-reference/data-types-text#label-character-datatypes) data type.

For example, consider the following table:

Copy code

```
CREATE TABLE t(
  col OBJECT(
    a INTEGER,
    b STRING,
    c MAP(INTEGER, STRING),
    d ARRAY(STRING)
  )
);
```

For this table, search optimization for SUBSTRING search *can* be added on the following target structured elements:

- `col:b` because its type is STRING.
- `col:c[value]` — for example, `col:c[0]`, `col:c[100]` — if the values are text string types.

For this table, search optimization for SUBSTRING search *can’t* be added on the following target structured elements:

- `col` because its type is structured OBJECT.
- `col:a` because its type is INTEGER.
- `col:c` because its type is MAP.
- `col:d` because its type is ARRAY.

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

If you enable search optimization for a given element, it is enabled for any unnested elements of a text string type.
Search optimization isn’t enabled for nested elements or elements of non-text string types.

### How constants are evaluated for structured substring searches

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

## Schema evolution support

The schema of structured columns can evolve over time. For more information about schema evolution, see
[ALTER ICEBERG TABLE … ALTER COLUMN … SET DATA TYPE (structured types)](/sql-reference/sql/alter-iceberg-table-alter-column-set-data-type).

As part of a single schema-evolution operation, the following modifications can occur:

- Type widening
- Reordering elements
- Adding elements
- Removing elements
- Renaming elements

The search optimization service isn’t invalidated as part of the schema-evolution operation. Instead,
the search optimization service handles operations in the following ways:

Type widening (for example, INT to NUMBER)
:   Search optimization access paths aren’t affected.

Adding elements
:   The newly added elements are automatically reflected in the existing search optimization access paths.

Removing elements
:   When elements are removed from a structured column, the search optimization service automatically
    drops access paths that are prefixed by the removed element.

    For example, create a table with a column of OBJECT type, and then insert data:

    Copy code

    ```
    CREATE OR REPLACE TABLE test_struct (
      a OBJECT(
        b INTEGER,
        c OBJECT(
          d STRING,
          e VARIANT
          )
      )
    );

    INSERT INTO test_struct (a) SELECT
      {
        'b': 100,
        'c': {
            'd': 'value1',
            'e': 'value2'
      }
      }::OBJECT(
        b INTEGER,
        c OBJECT(
            d STRING,
            e VARIANT
        )
    );
    ```

    To view the data, query the table:

    Copy code

    ```
    SELECT * FROM test_struct;
    ```

    ```
    +--------------------+
    | A                  |
    |--------------------|
    | {                  |
    |   "b": 100,        |
    |   "c": {           |
    |     "d": "value1", |
    |     "e": "value2"  |
    |   }                |
    | }                  |
    +--------------------+
    ```

    The following statement removes element `c` from the object:

    Copy code

    ```
    ALTER TABLE test_struct ALTER COLUMN a
      SET DATA TYPE OBJECT(
        b INTEGER);
    ```

    When this statement runs, the access paths at `a`, `a:c`, `a:c:d`
    and `a:c:e` are dropped.

Renaming elements
:   When an element is renamed, the search optimization service automatically drops access paths prefixed
    by the renamed element and adds them back with the newly named path. This operation incurs an additional
    maintenance cost to process the newly added path in the search optimization service.

    For example, create a table with a column of OBJECT type, and then insert data:

    Copy code

    ```
    CREATE OR REPLACE TABLE test_struct (
      a OBJECT(
        b INTEGER,
        c OBJECT(
          d STRING,
          e VARIANT
          )
      )
    );

    INSERT INTO test_struct (a) SELECT
      {
        'b': 100,
        'c': {
            'd': 'value1',
            'e': 'value2'
      }
      }::OBJECT(
        b INTEGER,
        c OBJECT(
            d STRING,
            e VARIANT
        )
    );
    ```

    To view the data, query the table:

    Copy code

    ```
    SELECT * FROM test_struct;
    ```

    ```
    +--------------------+
    | A                  |
    |--------------------|
    | {                  |
    |   "b": 100,        |
    |   "c": {           |
    |     "d": "value1", |
    |     "e": "value2"  |
    |   }                |
    | }                  |
    +--------------------+
    ```

    The following statement renames element `c` to `c_new` in the object:

    Copy code

    ```
    ALTER TABLE test_struct ALTER COLUMN a
      SET DATA TYPE OBJECT(
        b INTEGER,
        c_new OBJECT(
          d STRING,
          e VARIANT
        )
      ) RENAME FIELDS;
    ```

    The access paths at `a`, `a:c`, `a:c:d`, `a:c:e` are dropped and re-added as `a`, `a:c_new`,
    `a:c_new:d`, `a:c_new:e`.

Reordering elements
:   Search optimization access paths aren’t affected.

## Current limitations in support for structured types

Support for structured types in the search optimization service is limited in the following ways:

- Predicates of the form `path_to_element IS NULL` aren’t supported.
- Predicates where the constants are results of scalar subqueries aren’t supported.
- Predicates that specify paths to elements that contain sub-elements aren’t supported.
- Predicates that use the [XMLGET](/sql-reference/functions/xmlget) function aren’t supported.

- Predicates that use the [MAP\_CONTAINS\_KEY](/sql-reference/functions/map_contains_key) function aren’t supported.

The [current limitations of the search optimization service](/user-guide/search-optimization/queries-that-benefit#label-search-optimization-limitations) also apply to
structured types.
