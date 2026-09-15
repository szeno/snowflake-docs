Categories:
:   [Aggregate functions](/sql-reference/functions-aggregation) (Semi-structured Data), [Window functions](/sql-reference/functions-window) (General), [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Array/Object)

# OBJECT\_AGG

Returns one OBJECT per group. For each (`key`, `value`) input pair, where `key`
must be a VARCHAR and `value` must be a VARIANT, the resulting OBJECT contains
a `key`:`value` field.

Aliases:
:   OBJECTAGG

## Syntax

**Aggregate function**

Copy code

```
OBJECT_AGG(<key>, <value>)
```

**Window function**

Copy code

```
OBJECT_AGG(<key>, <value>) OVER ( [ PARTITION BY <expr2> ] )
```

## Usage notes

- Input tuples with NULL `key` and/or `value` are ignored.
- Duplicate keys within a group result in a `Duplicate field key 'key'` error.
- The DISTINCT keyword is supported, but it only filters out duplicate
  rows where both `key` and `value` are equal.

- When this function is called as a window function, it does not support:
  - An ORDER BY clause within the OVER clause.
  - Explicit window frames.

## Examples

These examples build a table of key-value pairs, then use OBJECT\_AGG to collect the pairs in each
group into a single OBJECT (for example, gathering a person’s attributes into one object per person).

First, create and populate a table. The value column is typed as VARIANT because the
`value` argument of OBJECT\_AGG must be a VARIANT, so each inserted value is
cast with `::VARIANT`:

Copy code

```
CREATE OR REPLACE TABLE objectagg_example(g NUMBER, k VARCHAR(30), v VARIANT);
INSERT INTO objectagg_example SELECT 0, 'name', 'Joe'::VARIANT;
INSERT INTO objectagg_example SELECT 0, 'age', 21::VARIANT;
INSERT INTO objectagg_example SELECT 1, 'name', 'Sue'::VARIANT;
INSERT INTO objectagg_example SELECT 1, 'zip', 94401::VARIANT;

SELECT * FROM objectagg_example;
```

```
+---+------+-------+
| G |  K   |   V   |
|---+------+-------|
| 0 | name | "Joe" |
| 0 | age  | 21    |
| 1 | name | "Sue" |
| 1 | zip  | 94401 |
+---+------+-------+
```

This example uses OBJECT\_AGG as an aggregate function. Grouping by `g` produces one OBJECT per group,
where each `k` value becomes a key and its `v` value becomes the corresponding value:

Copy code

```
SELECT OBJECT_AGG(k, v) FROM objectagg_example GROUP BY g;
```

```
+-------------------+
| OBJECT_AGG(K, V)  |
|-------------------|
| {                 |
|  "name": "Sue",   |
|   "zip": 94401    |
| }                 |
| {                 |
|  "age": 21,       |
|  "name": "Joe"    |
| }                 |
+-------------------+
```

The following example is optional and shows how to expand the aggregated objects back into rows. It
passes the OBJECT produced by OBJECT\_AGG to [FLATTEN](/sql-reference/functions/flatten), which returns one
row for each key-value pair in each object:

Copy code

```
SELECT seq, key, value
  FROM (SELECT object_agg(k, v) o FROM objectagg_example GROUP BY g),
    LATERAL FLATTEN(input => o);
```

```
+-----+------+-------+
| SEQ | KEY  | VALUE |
|-----+------+-------|
|   1 | name | "Sue" |
|   1 | zip  | 94401 |
|   2 | age  | 21    |
|   2 | name | "Joe" |
+-----+------+-------+
```
