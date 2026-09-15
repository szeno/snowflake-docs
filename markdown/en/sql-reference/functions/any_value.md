Categories:
:   [Aggregate functions](/sql-reference/functions-aggregation) (General) , [Window functions](/sql-reference/functions-window) (General)

# ANY\_VALUE

Returns some value of the expression from the group. The result is non-deterministic.

## Syntax

**Aggregate function**

Copy code

```
ANY_VALUE( [ DISTINCT ] <expr1> )
```

**Window function**

Copy code

```
ANY_VALUE( [ DISTINCT ] <expr1> ) OVER ( [ PARTITION BY <expr2> ] )
```

## Arguments

`expr1`
:   The input expression.

`expr2`
:   The column to partition on, if you want the result to be split into multiple
    partitions.

## Returns

This function can return a value of any data type.

If the input expression is NULL, the function returns NULL.

## Usage notes

- The DISTINCT keyword can be specified for this function, but it does not have any effect.
- The function doesn’t exclude NULL values. If the expression contains NULL values, the function can
  return a NULL value.

- When this function is called as a window function, it does not support:
  - An ORDER BY clause within the OVER clause.
  - Explicit window frames.

## Using ANY\_VALUE with GROUP BY statements

ANY\_VALUE can simplify and optimize the performance of [GROUP BY](/sql-reference/constructs/group-by) statements. A common problem for many queries is that the result of a query with a GROUP BY
clause can only contain expressions used in the GROUP BY clause itself, or results of aggregate functions. For example:

Copy code

```
SELECT customer.id , customer.name , SUM(orders.value)
  FROM customer
  JOIN orders ON customer.id = orders.customer_id
  GROUP BY customer.id , customer.name;
```

In this query, the `customer.name` attribute needs to be in the GROUP BY to be included in the result. This is unnecessary
(for example, when `customer.id` is known to be unique) and makes the computation
possibly more complex and slower. Another option is to use an aggregate function. For example:

Copy code

```
SELECT customer.id , MIN(customer.name) , SUM(orders.value)
  FROM customer
  JOIN orders ON customer.id = orders.customer_id
  GROUP BY customer.id;
```

This simplifies the GROUP BY clause, but still requires computing the [MIN](/sql-reference/functions/min) function, which incurs an extra cost.

With ANY\_VALUE, you can execute the following query:

Copy code

```
SELECT customer.id , ANY_VALUE(customer.name) , SUM(orders.value)
  FROM customer
  JOIN orders ON customer.id = orders.customer_id
  GROUP BY customer.id;
```
