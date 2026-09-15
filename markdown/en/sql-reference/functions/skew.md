Categories:
:   [Aggregate functions](/sql-reference/functions-aggregation) (General)

# SKEW

Returns the sample skewness of non-NULL records. If all records inside a group are NULL, the function returns NULL.

The following formula is used to compute the sample skewness:

(n^2)/((n-1) \* (n-2)) \* (m\_3/(k\_2)^(1.5))where:

- `n` denotes the number of non-null records.
- `m_3` denotes the sample third central moment.
- `k_2` denotes the symmetric unbiased estimator of the variance.

Intuitively, skew describes how asymmetric the underlying distribution is.

## Syntax

Copy code

```
SKEW( <expr> )
```

## Arguments

`expr`
:   This is an expression that evaluates to a numeric data type (INTEGER, FLOAT, DECIMAL, etc.).

## Returns

This function returns a value of type DOUBLE.

## Usage notes

- For inputs with fewer than three records, SKEW returns NULL.

## Examples

Create a table and load the data:

> Copy code
>
> ```
> create or replace table aggr(k int, v decimal(10,2), v2 decimal(10, 2));
>
> insert into aggr values
>     (1, 10, null),
>     (2, 10, null),
>     (2, 20, 22),
>     (2, 25, null),
>     (2, 30, 35);
> ```

Display the data:

> Copy code
>
> ```
> select *
>     from aggr
>     order by k, v;
> +---+-------+-------+
> | K |     V |    V2 |
> |---+-------+-------|
> | 1 | 10.00 |  NULL |
> | 2 | 10.00 |  NULL |
> | 2 | 20.00 | 22.00 |
> | 2 | 25.00 |  NULL |
> | 2 | 30.00 | 35.00 |
> +---+-------+-------+
> ```

Query the data:

> Copy code
>
> ```
> select SKEW(K), SKEW(V), SKEW(V2)
>     from aggr;
> +--------------+---------------+----------+
> |      SKEW(K) |       SKEW(V) | SKEW(V2) |
> |--------------+---------------+----------|
> | -2.236069766 | 0.05240788515 |     NULL |
> +--------------+---------------+----------+
> ```
