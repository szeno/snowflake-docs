# PERIOD data type

The PERIOD data type stores an anchored temporal range as a single value: a beginning bound and an
ending bound of the same element type. Unlike [interval data types](/sql-reference/data-types-datetime#label-datatypes-interval-variations),
which represent a duration without a fixed location in time, a PERIOD value identifies a specific
range on the timeline (for example, an employment window or a version validity interval).

PERIOD values use half-open interval semantics `[begin, end)`: the beginning bound is inclusive and
the ending bound is exclusive. The range starts at the beginning bound and extends up to but not
including the ending bound. Empty periods aren’t allowed; the constructor and casts require
`begin < end`.

Note

This topic documents the PERIOD *data type* (a first-class column type). It doesn’t document the
SQL:2011 `PERIOD FOR` table-level clause that binds two existing scalar columns into a logical
period for temporal versioning. That clause isn’t supported.

## Specify a PERIOD data type

To specify a PERIOD type, use the following syntax:

Copy code

```
PERIOD( <element_type> )
```

Where `element_type` is one of the following:

- DATE
- TIME [ `(<scale>)` ]
- TIMESTAMP\_NTZ [ `(<scale>)` ]
- TIMESTAMP\_LTZ [ `(<scale>)` ]
- TIMESTAMP\_TZ [ `(<scale>)` ]

For TIME and TIMESTAMP element types, you can specify a scale from `0` to `9`. If you omit the
scale, Snowflake uses the default scale for that temporal type.

You must specify an element type. Bare `PERIOD` (without an element type) isn’t a valid column or
expression type.

Examples of valid type definitions:

Copy code

```
PERIOD(DATE)
PERIOD(TIME(0))
PERIOD(TIMESTAMP_NTZ(9))
PERIOD(TIMESTAMP_LTZ)
PERIOD(TIMESTAMP_TZ(6))
```

## Bound semantics

Every PERIOD value is a half-open range `[begin, end)`:

- Instant `begin` is included in the period.
- Instant `end` is excluded from the period.
- Adjacent periods such as `[a, b)` and `[b, c)` don’t overlap and meet at `b`.

Both bounds must be finite. PERIOD doesn’t support unbounded ranges, infinity literals, or
NULL-as-unbounded semantics. To represent an open-ended range (for example, “still active”), use a
convention such as a far-future ending bound:

Copy code

```
PERIOD_CONSTRUCT(hire_date, DATE '9999-12-31')
```

Snowflake doesn’t expose PostgreSQL-style configurable bracket inclusivity (`[]`, `()`, `(]`).
Half-open `[begin, end)` is the only stored form.

## Construct PERIOD values

You can create PERIOD values in the following ways:

### PERIOD\_CONSTRUCT

[PERIOD\_CONSTRUCT](/sql-reference/functions/period_construct) builds a PERIOD from two temporal
expressions of the same element type:

Copy code

```
SELECT PERIOD_CONSTRUCT(DATE '2024-01-01', DATE '2024-12-31');
```

If `begin >= end`, Snowflake raises an error.

### Typed literal

Use the parameterized ANSI literal form:

Copy code

```
SELECT PERIOD(DATE) '[2024-01-01, 2024-12-31)';
```

Bounds are parsed according to the session input formats for the element type (for example,
DATE\_INPUT\_FORMAT for DATE bounds).

### Explicit cast from text

Cast a string in canonical `[begin, end)` form to a PERIOD type:

Copy code

```
SELECT '[2024-01-01, 2024-12-31)'::PERIOD(DATE);

SELECT TRY_CAST('[2024-01-01, 2024-12-31)' AS PERIOD(DATE));
```

`TRY_CAST` returns NULL for malformed strings or invalid bounds (`begin >= end`) instead of
raising an error.

There is no implicit coercion from TEXT to PERIOD outside DML contexts that allow a text
representation of the column type.

## Access PERIOD bounds

Use the accessor functions to extract typed begin and end values:

Copy code

```
SELECT
    PERIOD_BEGIN(active_period) AS begin_bound,
    PERIOD_END(active_period) AS end_bound
  FROM employment_windows;
```

The result type matches the PERIOD element type (DATE, TIME, or the corresponding TIMESTAMP
variant). For a full worked example, see [Create a table and query PERIOD values](#label-period-example-create-query).

## Ordering and comparison

PERIOD values are orderable and hashable. Ordering is begin-first, then end:

- `p1 < p2` if `PERIOD_BEGIN(p1) < PERIOD_BEGIN(p2)`, or the beginning bounds are equal and
  `PERIOD_END(p1) < PERIOD_END(p2)`.

You can use PERIOD columns in `ORDER BY`, `GROUP BY`, and `SELECT DISTINCT`, and count them with
`COUNT`. Aggregate functions such as `MIN`, `MAX`, `SUM`, and `AVG` aren’t supported on PERIOD.

Equality of two PERIOD values compares both bounds. For predicate helpers such as overlaps and
contains, see [Period functions](/sql-reference/functions-period).

## Conversion

### Convert to a PERIOD value

You can explicitly cast to PERIOD from:

- TEXT / VARCHAR (canonical `[begin, end)` string)
- NULL (standard null handling)

Cross-element PERIOD casts (for example, PERIOD(DATE) to PERIOD(TIMESTAMP\_NTZ)) require an
explicit cast. There is no implicit coercion between different PERIOD element types.

### Convert from a PERIOD value

You can explicitly cast a PERIOD value to TEXT / VARCHAR. The result is the canonical string form
`[begin, end)`, using the session output formats for the element type:

Copy code

```
SELECT TO_CHAR(PERIOD(DATE) '[2024-01-01, 2024-12-31)') AS period_text;
```

```
+--------------------------+
| PERIOD_TEXT              |
|--------------------------|
| [2024-01-01, 2024-12-31) |
+--------------------------+
```

Drivers currently receive PERIOD values as text in that canonical form.

## Load and unload PERIOD data

When you load or unload PERIOD columns as text (for example, CSV or JSON string fields), use the
canonical form:

- JSON: a quoted string such as `"[2024-01-01, 2024-12-31)"`
- CSV: an unquoted or quoted string such as `[2024-01-01, 2024-12-31)`

PERIOD isn’t a native Parquet or Iceberg type. Creating a PERIOD column on a managed Iceberg table
isn’t supported.

## Data governance

A [masking policy](/user-guide/security-column-intro) or
[row access policy](/user-guide/security-row-intro) protects a PERIOD column the same way it protects
a column of any other type. The following behavior is specific to PERIOD.

### Masking policy element type must match

A masking policy signature must match the column data type. For a PERIOD column, this match includes
the element type: define the policy with the same PERIOD element type as the column, and use that
type for both the input argument and the return value.

For example, the following masking policy applies to a `PERIOD(DATE)` column:

Copy code

```
CREATE MASKING POLICY period_date_mask AS (val PERIOD(DATE))
  RETURNS PERIOD(DATE) ->
    CASE
      WHEN CURRENT_ROLE() = 'ANALYST' THEN val
      ELSE PERIOD(DATE) '[1970-01-01, 1970-01-02)'
    END;
```

When you attach a masking policy directly to a column with
[ALTER TABLE … ALTER COLUMN](/sql-reference/sql/alter-table-column) (`SET MASKING POLICY`),
Snowflake rejects a policy whose element type doesn’t match the column. For example, attaching the
`PERIOD(DATE)` policy to a `PERIOD(TIME)` column returns an error:

```
COLUMN data type PERIOD(TIME(9)) does not match with masking policy data type PERIOD.
```

With [tag-based masking](/user-guide/tag-based-masking-policies), a tag can carry one masking policy
per PERIOD element type. For example, you can assign both a `PERIOD(DATE)` policy and a
`PERIOD(TIME)` policy to the same tag; each tagged column is then protected by the policy that
matches its element type. As with all data types, a tag’s policy protects a column only when their
types match: if a tagged column’s element type doesn’t match any masking policy on the tag, that
column isn’t masked.

## Current limitations

The following limitations apply to the PERIOD data type:

- Bare `PERIOD` without an element type isn’t supported as a column or expression type.
- Unbounded periods and Teradata-style `UNTIL_CLOSED` / `UNTIL_CHANGED` sentinels aren’t
  supported.
- The SQL:2011 `PERIOD FOR` table declaration isn’t supported.
- PERIOD columns aren’t supported on Iceberg tables.
- Client drivers serialize PERIOD as text; structured begin/end client types aren’t available yet.
- Support in non-SQL UDFs, stored procedures in languages other than SQL, and Snowpark is limited
  or deferred. Prefer SQL for PERIOD expressions.
- Interval arithmetic that shifts a PERIOD by an INTERVAL duration isn’t supported yet.
- Storing PERIOD values inside VARIANT (and related semi-structured embedding) is deferred.

## PERIOD functions

Snowflake provides constructor, accessor, predicate, and set-operation functions for PERIOD values.
For the full list, see [Period functions](/sql-reference/functions-period).

## Examples for the PERIOD data type

The following examples show how to store, construct, compare, and combine PERIOD values:

- [Create a table and query PERIOD values](#label-period-example-create-query)
- [Construct PERIOD values safely](#label-period-example-construction)
- [Work with half-open bound semantics](#label-period-example-half-open)
- [Test relationships with predicates](#label-period-example-predicates)
- [Combine periods with set operations](#label-period-example-set-operations)
- [Order PERIOD values](#label-period-example-ordering)
- [Use a TIMESTAMP element type](#label-period-example-timestamp)

### Create a table and query PERIOD values

1. Create a table with a PERIOD(DATE) column:

   Copy code

   ```
   CREATE OR REPLACE TABLE employment_windows (
     employee_id INTEGER,
     active_period PERIOD(DATE)
   );
   ```
2. Insert rows using three construction styles: a typed literal, a cast from text, and
   [PERIOD\_CONSTRUCT](/sql-reference/functions/period_construct):

   Copy code

   ```
   INSERT INTO employment_windows VALUES
     (1, PERIOD(DATE) '[2020-01-15, 2023-06-30)'),
     (2, '[2021-03-01, 9999-12-31)'::PERIOD(DATE)),
     (3, PERIOD_CONSTRUCT(DATE '2022-09-01', DATE '2024-01-01'));
   ```
3. Query the typed bounds with the accessor functions, and display the canonical text form with
   `TO_CHAR`:

   Copy code

   ```
   SELECT
       employee_id,
       PERIOD_BEGIN(active_period) AS start_date,
       PERIOD_END(active_period) AS end_date,
       TO_CHAR(active_period) AS period_text
     FROM employment_windows
     ORDER BY employee_id;
   ```

   ```
   +-------------+------------+------------+--------------------------+
   | EMPLOYEE_ID | START_DATE | END_DATE   | PERIOD_TEXT              |
   |-------------+------------+------------+--------------------------|
   |           1 | 2020-01-15 | 2023-06-30 | [2020-01-15, 2023-06-30) |
   |           2 | 2021-03-01 | 9999-12-31 | [2021-03-01, 9999-12-31) |
   |           3 | 2022-09-01 | 2024-01-01 | [2022-09-01, 2024-01-01) |
   +-------------+------------+------------+--------------------------+
   ```
4. You can also display the whole column in canonical form by casting it to VARCHAR:

   Copy code

   ```
   SELECT employee_id, active_period::VARCHAR AS period_varchar
     FROM employment_windows
     ORDER BY employee_id;
   ```

   ```
   +-------------+--------------------------+
   | EMPLOYEE_ID | PERIOD_VARCHAR           |
   |-------------+--------------------------|
   |           1 | [2020-01-15, 2023-06-30) |
   |           2 | [2021-03-01, 9999-12-31) |
   |           3 | [2022-09-01, 2024-01-01) |
   +-------------+--------------------------+
   ```

### Construct PERIOD values safely

You can build the same PERIOD value from a typed literal, a cast from text, or
[PERIOD\_CONSTRUCT](/sql-reference/functions/period_construct), as shown in the previous example. When
you parse untrusted text, use `TRY_CAST` so that malformed strings or invalid bounds (`begin >= end`)
return NULL instead of raising an error:

Copy code

```
SELECT
    TRY_CAST('[2024-01-01, 2024-12-31)' AS PERIOD(DATE)) AS valid_bounds,
    TRY_CAST('[2024-12-31, 2024-01-01)' AS PERIOD(DATE)) AS invalid_bounds;
```

```
+--------------------------+----------------+
| VALID_BOUNDS             | INVALID_BOUNDS |
|--------------------------+----------------|
| [2024-01-01, 2024-12-31) | NULL           |
+--------------------------+----------------+
```

### Work with half-open bound semantics

Because a PERIOD is half-open `[begin, end)`, the beginning bound is contained in the period but the
ending bound isn’t:

Copy code

```
SELECT
    PERIOD_CONTAINS(PERIOD(DATE) '[2024-01-01, 2024-04-01)', DATE '2024-01-01') AS begin_inclusive,
    PERIOD_CONTAINS(PERIOD(DATE) '[2024-01-01, 2024-04-01)', DATE '2024-04-01') AS end_exclusive;
```

```
+-----------------+---------------+
| BEGIN_INCLUSIVE | END_EXCLUSIVE |
|-----------------+---------------|
| True            | False         |
+-----------------+---------------+
```

### Test relationships with predicates

The predicate functions test how two periods relate. This example checks overlap, adjacency, and
containment for three periods:

Copy code

```
WITH periods AS (
  SELECT
    PERIOD(DATE) '[2024-01-01, 2024-04-01)' AS p1,
    PERIOD(DATE) '[2024-03-01, 2024-06-01)' AS p2,
    PERIOD(DATE) '[2024-04-01, 2024-07-01)' AS p3
)
SELECT
    PERIOD_OVERLAPS(p1, p2) AS p1_overlaps_p2,
    PERIOD_OVERLAPS(p1, p3) AS p1_overlaps_p3,
    PERIOD_MEETS(p1, p3) AS p1_meets_p3,
    PERIOD_CONTAINS(p1, DATE '2024-01-01') AS contains_begin,
    PERIOD_CONTAINS(p1, DATE '2024-04-01') AS contains_end
  FROM periods;
```

```
+----------------+----------------+-------------+----------------+--------------+
| P1_OVERLAPS_P2 | P1_OVERLAPS_P3 | P1_MEETS_P3 | CONTAINS_BEGIN | CONTAINS_END |
|----------------+----------------+-------------+----------------+--------------|
| True           | False          | True        | True           | False        |
+----------------+----------------+-------------+----------------+--------------+
```

Adjacent periods that meet at a shared boundary don’t overlap, because the shared instant is the
exclusive ending bound of the earlier period and the inclusive beginning bound of the later period.

### Combine periods with set operations

Use [PERIOD\_INTERSECT](/sql-reference/functions/period_intersect) to return the overlapping sub-range
of two periods:

Copy code

```
SELECT PERIOD_INTERSECT(
    PERIOD(DATE) '[2024-01-01, 2024-07-01)',
    PERIOD(DATE) '[2024-04-01, 2024-10-01)'
  ) AS overlap;
```

```
+--------------------------+
| OVERLAP                  |
|--------------------------|
| [2024-04-01, 2024-07-01) |
+--------------------------+
```

When the arguments are disjoint, `PERIOD_INTERSECT` returns NULL.

Use [PERIOD\_LDIFF](/sql-reference/functions/period_ldiff) and
[PERIOD\_RDIFF](/sql-reference/functions/period_rdiff) to return the part of the first period that
lies before or after a second period:

Copy code

```
SELECT
    PERIOD_LDIFF(
      PERIOD(DATE) '[2024-01-01, 2024-07-01)',
      PERIOD(DATE) '[2024-04-01, 2024-10-01)'
    ) AS left_remainder,
    PERIOD_RDIFF(
      PERIOD(DATE) '[2024-01-01, 2024-07-01)',
      PERIOD(DATE) '[2024-01-01, 2024-04-01)'
    ) AS right_remainder;
```

```
+--------------------------+--------------------------+
| LEFT_REMAINDER           | RIGHT_REMAINDER          |
|--------------------------+--------------------------|
| [2024-01-01, 2024-04-01) | [2024-04-01, 2024-07-01) |
+--------------------------+--------------------------+
```

When the second period doesn’t cut the corresponding side of the first, these functions return NULL.

### Order PERIOD values

PERIOD values sort begin-first, then end. The following query orders three periods that share a
beginning bound or a beginning month:

Copy code

```
SELECT p::VARCHAR AS p
  FROM (
    SELECT PERIOD(DATE) '[2024-01-01, 2024-06-01)' AS p
    UNION ALL SELECT PERIOD(DATE) '[2024-02-01, 2024-03-01)'
    UNION ALL SELECT PERIOD(DATE) '[2024-01-01, 2024-12-31)'
  )
  ORDER BY p;
```

```
+--------------------------+
| P                        |
|--------------------------|
| [2024-01-01, 2024-06-01) |
| [2024-01-01, 2024-12-31) |
| [2024-02-01, 2024-03-01) |
+--------------------------+
```

The two periods that begin on `2024-01-01` sort by their ending bound, and the period that begins on
`2024-02-01` sorts last.

### Use a TIMESTAMP element type

PERIOD isn’t limited to dates. This example builds a work shift as a `PERIOD(TIMESTAMP_NTZ)` value:

Copy code

```
SELECT PERIOD(TIMESTAMP_NTZ) '[2024-01-01 09:00:00, 2024-01-01 17:00:00)' AS shift;
```

```
+----------------------------------------------------------------+
| SHIFT                                                          |
|----------------------------------------------------------------|
| [2024-01-01 09:00:00.000000000, 2024-01-01 17:00:00.000000000) |
+----------------------------------------------------------------+
```
