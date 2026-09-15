# Troubleshooting SQL UDFs

This topic provides troubleshooting information about SQL UDFs (user-defined functions).

## Troubleshooting

### Tips

If using a SQL UDF in a [masking policy](/sql-reference/sql/create-masking-policy), ensure the data type of the column, UDF, and
masking policy match.

### Error message: `Unsupported subquery type`

Cause:
:   If a UDF contains a query expression, then the UDF can act as a [subquery](/user-guide/querying-subqueries).
    If a subquery is passed a column name, then the subquery can act as a
    [correlated subquery](/user-guide/querying-subqueries#label-correlated-vs-uncorrelated-subqueries). If a correlated subquery violates the
    Snowflake rules for correlated subqueries, then the user gets the error message `Unsupported subquery type`.
    The example below shows an invalid correlated subquery, and how a UDF can act like a similar invalid correlated
    subquery.

    Create a pair of tables and load data into them:

    Copy code

    ```
    CREATE TABLE stores (store_ID INTEGER, city VARCHAR);
    CREATE TABLE employee_sales (employee_ID INTEGER, store_ID INTEGER, sales NUMERIC(10,2), 
        sales_date DATE);
    INSERT INTO stores (store_ID, city) VALUES 
        (1, 'Winnipeg'),
        (2, 'Toronto');
    INSERT INTO employee_sales (employee_ID, store_ID, sales, sales_date) VALUES 
        (1001, 1, 9000.00, '2020-01-27'),
        (1002, 1, 2000.00, '2020-01-27'),
        (2001, 2, 6000.00, '2020-01-27'),
        (2002, 2, 4000.00, '2020-01-27'),
        (2002, 2, 5000.00, '2020-01-28')
        ;
    ```

    The following SQL statement contains a correlated subquery that does not follow Snowflake rules. This code
    causes an `Unsupported subquery type` error:

    Copy code

    ```
    SELECT employee_ID,
           store_ID,
           (SELECT city FROM stores WHERE stores.store_ID = employee_sales.store_ID)
        FROM employee_sales;
    ```

    The code below creates and then calls a subquery-like UDF in a way that creates a correlated subquery similar to
    the one shown above:

    Copy code

    ```
    CREATE FUNCTION subquery_like_udf(X INT)
        RETURNS VARCHAR
        LANGUAGE SQL
        AS
        $$
            SELECT city FROM stores WHERE stores.store_ID = X
        $$;
    ```

    Copy code

    ```
    SELECT employee_ID, subquery_like_udf(employee_sales.store_ID)
        FROM employee_sales;
    ```

Solution #1:
:   If the UDF contains a query expression, then call the UDF only in ways consistent with the rules for
    [subqueries](/user-guide/querying-subqueries).

    For example, the following statement calls the UDF with a constant rather than with a column name, so the UDF
    does not act like a correlated subquery:

    Copy code

    ```
    SELECT subquery_like_udf(1);
    +----------------------+
    | SUBQUERY_LIKE_UDF(1) |
    |----------------------|
    | Winnipeg             |
    +----------------------+
    ```

Solution #2:
:   In some cases, you can re-write the UDF to achieve the same goal a different way. A correlated subquery is allowed
    if the subquery can be statically determined to return one row. The following UDF uses an aggregate function
    and therefore returns only one row:

    Copy code

    ```
    CREATE FUNCTION subquery_like_udf_2(X INT)
        RETURNS VARCHAR
        LANGUAGE SQL
        AS
        $$
            SELECT ANY_VALUE(city) FROM stores WHERE stores.store_ID = X
        $$;
    ```

    Copy code

    ```
    SELECT employee_ID, sales_date, subquery_like_udf_2(employee_sales.store_ID)
        FROM employee_sales
        ORDER BY employee_ID, sales_date;
    +-------------+------------+----------------------------------------------+
    | EMPLOYEE_ID | SALES_DATE | SUBQUERY_LIKE_UDF_2(EMPLOYEE_SALES.STORE_ID) |
    |-------------+------------+----------------------------------------------|
    |        1001 | 2020-01-27 | Winnipeg                                     |
    |        1002 | 2020-01-27 | Winnipeg                                     |
    |        2001 | 2020-01-27 | Toronto                                      |
    |        2002 | 2020-01-27 | Toronto                                      |
    |        2002 | 2020-01-28 | Toronto                                      |
    +-------------+------------+----------------------------------------------+
    ```
