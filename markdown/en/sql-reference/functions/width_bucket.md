Categories:
:   [Numeric functions](/sql-reference/functions-numeric)

# WIDTH\_BUCKET

Constructs equi-width histograms, in which the histogram range is divided into intervals of identical size, and returns the bucket number into which the value of an expression falls, after
it has been evaluated. The function returns an integer value or null (if any input is null).

## Syntax

Copy code

```
WIDTH_BUCKET( <expr> , <min_value> , <max_value> , <num_buckets> )
```

## Arguments

`expr`
:   The expression for which the histogram is created. This expression must evaluate to a numeric value or to a value that can be implicitly converted to a numeric value.

    The value must be within the range of `-(2^53 - 1)` to `2^53 - 1` (inclusive).

`min_value` and `max_value`
:   The low and high end points of the acceptable range for the expression. The end points must also evaluate to numeric values and not be equal.

    The low and high end points must be within the range of `-(2^53 - 1)` to `2^53 - 1` (inclusive). In addition, the difference
    between these points must be less than `2^53` (i.e. `abs(max_value - min_value) < 2^53`).

`num_buckets`
:   The desired number of buckets; must be a positive integer value. A value from the expression is assigned to each bucket, and the function then returns the corresponding bucket number.

    When an expression falls outside the range, the function returns:

    - `0` if the expression is less than `min_value`.
    - `num_buckets + 1` if the expression is greater than or equal to `max_value`.

## Example

Create a four-bucket histogram on the `price` column for homes sold in the price range of $200 - 600k,
ordered by sales date. The function returns the bucket number (`SALES GROUP`) for each value in the set.

> Create and fill a table:
>
> > Copy code
> >
> > ```
> > CREATE TABLE home_sales (
> >     sale_date DATE,
> >     price NUMBER(11, 2)
> >     );
> > INSERT INTO home_sales (sale_date, price) VALUES 
> >     ('2013-08-01'::DATE, 290000.00),
> >     ('2014-02-01'::DATE, 320000.00),
> >     ('2015-04-01'::DATE, 399999.99),
> >     ('2016-04-01'::DATE, 400000.00),
> >     ('2017-04-01'::DATE, 470000.00),
> >     ('2018-04-01'::DATE, 510000.00);
> > ```
>
> Query the table, calling WIDTH\_BUCKET():
>
> > Copy code
> >
> > ```
> > SELECT 
> >     sale_date, 
> >     price,
> >     WIDTH_BUCKET(price, 200000, 600000, 4) AS "SALES GROUP"
> >   FROM home_sales
> >   ORDER BY sale_date;
> > +------------+-----------+-------------+
> > | SALE_DATE  |     PRICE | SALES GROUP |
> > |------------+-----------+-------------|
> > | 2013-08-01 | 290000.00 |           1 |
> > | 2014-02-01 | 320000.00 |           2 |
> > | 2015-04-01 | 399999.99 |           2 |
> > | 2016-04-01 | 400000.00 |           3 |
> > | 2017-04-01 | 470000.00 |           3 |
> > | 2018-04-01 | 510000.00 |           4 |
> > +------------+-----------+-------------+
> > ```
