Categories:
:   [Conditional expression functions](/sql-reference/expressions-conditional)

# [ NOT ] BETWEEN

Returns `TRUE` when the input expression (numeric or string) is within the specified lower and upper boundary.

## Syntax

Copy code

```
<expr> [ NOT ] BETWEEN <lower_bound> AND <upper_bound>
```

## Arguments

`expr`
:   The input expression.

`lower_bound`
:   The lower boundary.

`upper_bound`
:   The upper boundary.

## Returns

The function returns a value of type BOOLEAN.

## Usage notes

- `expr BETWEEN lower_bound AND upper_bound` is equivalent to `expr >= lower_bound AND expr <= upper_bound`.
- The data types of the argument values must be the same or [compatible](/sql-reference/data-type-conversion#label-when-coercion-occurs).

  If the function implicitly casts a value to a different data type, it might return unexpected results.

  For example, when `expr` is a TIMESTAMP value, and the `lower_bound` and `upper_bound` values
  are DATE values, the DATE values are implicitly cast to TIMESTAMP values, and the time is set to `00:00:00`. For
  the following WHERE clause, assume `timestamp_column` is a column of type TIMESTAMP in a table:

  Copy code

  ```
  WHERE timestamp_column BETWEEN '2025-04-30' AND '2025-04-31'
  ```

  When the DATE values are implicitly cast, the WHERE clause is interpreted as the following:

  Copy code

  ```
  WHERE timestamp_column BETWEEN '2025-04-30 00:00:00' AND '2025-04-31 00:00:00'
  ```

  With this WHERE clause, the function returns `FALSE` for virtually all `timestamp_column` values on 2025-04-31,
  which might not be intended. To avoid this specific issue, you can specify the next day for `upper_bound` when
  you call the function:

  Copy code

  ```
  WHERE timestamp_column BETWEEN '2025-04-30' AND '2025-05-01'
  ```

## Collation details

The expression `A BETWEEN X AND Y` is equivalent to `A >= X AND A <= Y`. The collations used for comparing
with `X` and `Y` are independent and do not need to be identical, but both need to be compatible with the
collation of `A`.

## Examples

Here are a few simple examples of using BETWEEN with numeric and string values:

Copy code

```
SELECT 'true' WHERE 1 BETWEEN 0 AND 10;
```

```
+--------+
| 'TRUE' |
|--------|
| true   |
+--------+
```

Copy code

```
SELECT 'true' WHERE 1.35 BETWEEN 1 AND 2;
```

```
+--------+
| 'TRUE' |
|--------|
| true   |
+--------+
```

Copy code

```
SELECT 'true' WHERE 'the' BETWEEN 'that' AND 'then';
```

```
+--------+
| 'TRUE' |
|--------|
| true   |
+--------+
```

The following examples use COLLATE with BETWEEN:

Copy code

```
SELECT 'm' BETWEEN COLLATE('A', 'lower') AND COLLATE('Z', 'lower');
```

```
+-------------------------------------------------------------+
| 'M' BETWEEN COLLATE('A', 'LOWER') AND COLLATE('Z', 'LOWER') |
|-------------------------------------------------------------|
| True                                                        |
+-------------------------------------------------------------+
```

Copy code

```
SELECT COLLATE('m', 'upper') BETWEEN 'A' AND 'Z';
```

```
+-------------------------------------------+
| COLLATE('M', 'UPPER') BETWEEN 'A' AND 'Z' |
|-------------------------------------------|
| True                                      |
+-------------------------------------------+
```
