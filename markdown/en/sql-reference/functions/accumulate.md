Categories:
:   [Aggregate functions](/sql-reference/functions-aggregation) (General)

# ACCUMULATE

Returns a custom aggregate value computed by four user-defined SQL lambda functions:
initialize, accumulate, combine, and terminate. ACCUMULATE follows the
map-reduce aggregation model and integrates with GROUP BY, HAVING, and
subqueries the same way built-in aggregates do.

ACCUMULATE is especially useful for prototyping and one-off aggregations
that no built-in aggregate covers. For performance-sensitive workloads, prefer
built-in aggregates when possible, or consider whether a combination of
built-in aggregates and joins can achieve the same result. ACCUMULATE
with OBJECT, ARRAY, or VARIANT state types carries additional performance
overhead.

## Syntax

Copy code

```
ACCUMULATE(
    <input_expr>,
    <initialize_lambda>,
    <accumulate_lambda>,
    <combine_lambda>,
    <terminate_lambda>
)
```

## Arguments

`input_expr`
:   Expression evaluated once per non-NULL input row. The resulting value is
    passed to each lambda as the input value.

`initialize_lambda`
:   Lambda with signature `(value) -> <state_expr>`. Called once per non-NULL
    input row to produce the initial partial state from that row’s value.

`accumulate_lambda`
:   Lambda with signature `(state, value) -> <state_expr>`. Folds a new input
    value into an existing partial state and returns the updated state.

`combine_lambda`
:   Lambda with signature `(state1, state2) -> <state_expr>`. Merges two
    partial states produced by parallel workers. Must be associative.

`terminate_lambda`
:   Lambda with signature `(state) -> <output_expr>`. Converts the final merged
    state into the result value returned to the query.

Lambda argument names are arbitrary. Type annotations are optional; see
[Type inference](#type-inference) for details.

## Returns

Returns the value produced by `terminate_lambda`. The data type matches
the return type of `terminate_lambda`. Returns NULL if all input rows
are NULL or the input set is empty.

## Usage notes

- NULL input rows are silently skipped before any lambda is called, consistent
  with standard SQL aggregate behavior. If all input rows are NULL or the input
  set is empty, the result is NULL.
- ACCUMULATE has no persistent form. There’s no CREATE AGGREGATE FUNCTION
  or equivalent DDL. To reuse an aggregation, wrap it in a view, CTE, or stored
  procedure.
- Lambdas may only reference their declared parameters. References to columns
  from the outer query aren’t allowed. To include an outer-query value, project
  it into the input expression or precompute it in a CTE.

  The following example causes a compilation error because `column2` is not a
  lambda parameter:

  Copy code

  ```
  -- ERROR: column2 is a column reference, not a lambda parameter.
  SELECT ACCUMULATE(
   column1,
   (v INT) -> v + column2,
   ...
  ) FROM t;
  ```
- The following function classes aren’t allowed inside lambdas:

  | Function class | Examples |
  | --- | --- |
  | Aggregate functions | SUM, AVG, COUNT |
  | Window functions | ROW\_NUMBER() OVER (…) |
  | Non-deterministic functions | RANDOM(), UUID\_STRING() |

  Expand

  Show lessSee more

## Type inference

Lambda argument types are optional. When omitted, types are inferred from the
input expression and propagated through the lambda chain.

- Explicit types aren’t coerced across lambdas. If you annotate a type on any
  lambda argument, that annotation is authoritative for the state type at that
  position. If annotations across the four lambdas are inconsistent and can’t
  be reconciled (for example, `initialize` returns ARRAY but `accumulate`
  declares the state as INT), compilation fails.
- You can omit all type annotations, or annotate only some arguments; the
  compiler infers and widens types automatically. Mixing annotated and
  unannotated arguments is allowed as long as the explicit annotations are
  consistent.
- The state type (the type flowing between initialize, accumulate, and combine)
  and the output type (the return type of terminate) are tracked independently
  and may differ.
- The input expression is implicitly cast to the type expected by the
  initialize lambda’s `value` argument. For example, if the input column is
  INT and `value` is declared STRING, the cast is applied automatically.

## Examples

Compute the sum of a column, simulating the equivalent behavior of the existing `SUM(c1)` aggregate function:

Copy code

```
SELECT
    ACCUMULATE(
        c1,
        (v INT)                      -> v,
        (state INT, v INT)           -> state + v,
        (state1 INT, state2 INT)     -> state1 + state2,
        (state INT)                  -> state
    ) AS total
FROM t;
```

Compute the mean using an ARRAY to track the running sum and count:

Copy code

```
SELECT ACCUMULATE(
    c1,
    (v INT)                        -> [v, 1],
    (state ARRAY, v INT)           -> [state[0] + v, state[1] + 1],
    (state1 ARRAY, state2 ARRAY)   -> [state1[0] + state2[0], state1[1] + state2[1]],
    (state ARRAY)                  -> state[0] / state[1]
) AS mean
FROM t;
```

Compute the product of all the values in a group.

Copy code

```
SELECT
    ACCUMULATE(
        c1,
        (v INT)                      -> v,
        (state INT, v INT)           -> state * v,
        (state1 INT, state2 INT)     -> state1 * state2,
        (state INT)                  -> state
    ) AS total
FROM t;
```

A full end-to-end example of using ACCUMULATE to compute the product of a column
for calculating to annual interest rate on a variable interest rate account:

Copy code

```
CREATE OR REPLACE TEMPORARY TABLE InterestRates (
  RowId              INT           NOT NULL AUTOINCREMENT PRIMARY KEY,
  "Month"            DATE          NOT NULL,
  AnnualInterestRate DECIMAL(7,4)  NOT NULL
);

-- 12 months: mostly 5.00%, with April/October at 5.25% and July at 4.75%
INSERT INTO InterestRates ("Month", AnnualInterestRate) VALUES
  ('2025-01-01', 0.0500),
  ('2025-02-01', 0.0500),
  ('2025-03-01', 0.0500),
  ('2025-04-01', 0.0525),  -- slightly higher
  ('2025-05-01', 0.0500),
  ('2025-06-01', 0.0500),
  ('2025-07-01', 0.0475),  -- slightly lower
  ('2025-08-01', 0.0500),
  ('2025-09-01', 0.0500),
  ('2025-10-01', 0.0525),  -- slightly higher
  ('2025-11-01', 0.0500),
  ('2025-12-01', 0.0500);

SELECT
  10000.0 AS InitialBalance,
  (InitialBalance * ACCUMULATE(
      1.0 + AnnualInterestRate / 12.0,
      (val) -> val,                         -- initialize
      (state, val) -> state * val,          -- accumulate
      (state1, state2) -> state1 * state2,  -- combine
      (state) -> state                      -- terminate
  ))::NUMERIC(18,4) AS FinalBalance
FROM
  InterestRates
WHERE
  "Month" <= '2025-08-01';
```

```
+----------------+--------------+
| InitialBalance | FinalBalance |
|----------------+--------------+
| 10000          | 10338.2347   |
+----------------+--------------+
```

Compute the mean using a structured OBJECT as state:

Copy code

```
SELECT ACCUMULATE(
    c1,
    (v INT) -> {'sum': v, 'count': 1}::OBJECT(sum INT, count INT),
    (state OBJECT(sum INT, count INT), v) ->
        {'sum': state:sum + v, 'count': state:count + 1}::OBJECT(sum INT, count INT),
    (state1, state2) ->
        {'sum': state1:sum + state2:sum, 'count': state1:count + state2:count}::OBJECT(sum INT, count INT),
    (state) -> state:sum / state:count
) AS mean
FROM t;
```

Find the shortest string in a column:

Copy code

```
SELECT ACCUMULATE(
    c1,
    (v STRING) -> v,
    (state STRING, v STRING) ->
        CASE WHEN LENGTH(v) < LENGTH(state) THEN v ELSE state END,
    (state1 STRING, state2 STRING) ->
        CASE WHEN LENGTH(state1) <= LENGTH(state2) THEN state1 ELSE state2 END,
    (state STRING) -> state
) AS shortest
FROM t;
```

Use ACCUMULATE with GROUP BY:

Copy code

```
SELECT
    category,
    ACCUMULATE(
        amount,
        (v INT)                      -> v,
        (state INT, v INT)           -> state + v,
        (state1 INT, state2 INT)     -> state1 + state2,
        (state INT)                  -> state
    ) AS category_total
FROM orders
GROUP BY category;
```

Call a UDF inside a lambda:

Copy code

```
SELECT ACCUMULATE(
    c1,
    (v NUMBER)       -> v,
    (state, v)       -> my_sum_udf(state, v),
    (state1, state2) -> my_sum_udf(state1, state2),
    (state)          -> state
) AS total
FROM t;
```
