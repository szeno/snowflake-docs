# Tabular SQL UDFs (UDTFs)

Snowflake supports SQL UDFs that return a set of rows, consisting of 0, 1, or multiple rows, each of which has 1 or more columns.
Such UDFs are called *tabular UDFs*, *table UDFs*, or, most frequently, *UDTFs* (user-defined table functions).

A UDTF can be accessed in the FROM clause of a query.

## Syntax

Copy code

```
CREATE OR REPLACE FUNCTION <name> ( [ <arguments> ] )
  RETURNS TABLE ( <output_col_name> <output_col_type> [, <output_col_name> <output_col_type> ... ] )
  AS '<sql_expression>'
```

For a more detailed description of the general syntax for all UDFs, including SQL UDTFs, see [CREATE FUNCTION](/sql-reference/sql/create-function).

## Arguments

`name`:
:   This should be valid database object name that follows the rules described at:
    [Identifier requirements](/sql-reference/identifiers-syntax).

`arguments`:
:   This must be an expression, for example a column name, a literal, or an
    expression that can be evaluated to a single value.
    Typically, a function takes one argument, which is a column name.
    You can pass more than one value, for example, more than one column name,
    or a column name and one or more literal values.

    It is possible to pass a constant or no value at all. However, in most cases,
    if the input is the same every time, then the output is the same every time.

`RETURNS TABLE(...)`
:   Specifies that the UDF should return a table. Inside the parentheses, specify name-and-type pairs for columns (as described below) to
    include in the returned table.

    `output_col_name`:
    :   The name of an output column to include in the returned table. There must be at least one output column.

    `output_col_type`:
    :   The data type of the output column.

`sql_expression`:
:   A valid SQL expression or statement that returns a table with zero or more rows, each of which has one or more columns.
    The outputs must match the number and data types specified in the RETURNS clause.

## Usage notes

- The main body (aka “definition”) of a SQL UDTF must be a [SELECT](/sql-reference/sql/select) expression.
- Although the delimiters around the `sql_expression` are typically single quotes, you can use
  a pair of dollar signs `$$` as the delimiter. The closing delimiter must match the opening
  delimiter. A pair of dollar signs is convenient when the `sql_expression`
  contains single quotes. An example using a pair of dollar signs is included in
  the Examples section below.

  If the delimiter is a single quote, and the body contains a single quote, you can escape the single quote in the
  body by using the backslash character `\` as the escape character. An example is included in the Examples
  section below.
- The columns defined in the UDTF can appear anywhere that a normal table column can be used.
- The return types specified in the RETURNS clause determine the names and types of the columns in the tabular results and must match the
  types of the expressions in the corresponding positions of the SELECT statement in the function body.
- When calling a UDTF, you must include the UDTF name and arguments inside parentheses following the TABLE keyword. For more, see
  [Calling a SQL UDTF](#label-udf-java-call-udtf).

Note

Tabular functions (UDTFs) have a limit of 500 input arguments and 500 output columns.

## Calling a SQL UDTF

When calling a UDTF in the FROM clause of a query, specify the UDTF’s name and arguments inside the parentheses that follow the TABLE
keyword.

In other words, use a form such as the following for the TABLE keyword when calling a UDTF:

Copy code

```
SELECT ...
  FROM TABLE ( udtf_name (udtf_arguments) )
```

## Sample SQL UDTFs

### Basic examples

This is an artificially simple example of a UDTF, which hard-codes the output. This also illustrates the
use of `$$` as a delimiter:

Copy code

```
CREATE FUNCTION t()
    RETURNS TABLE(msg VARCHAR)
    AS
    $$
        SELECT 'Hello'
        UNION
        SELECT 'World'
    $$;
```

Copy code

```
SELECT msg 
    FROM TABLE(t())
    ORDER BY msg;
+-------+
| MSG   |
|-------|
| Hello |
| World |
+-------+
```

This example is similar to the preceding example, but it uses single quotes as the delimiter, and uses the `\`
escape character to escape the single quotes in the body of the UDTF:

Copy code

```
CREATE FUNCTION t()
    RETURNS TABLE(msg VARCHAR)
    AS
    '
        SELECT \'Hello\'
        UNION
        SELECT \'World\'
    ';
```

Copy code

```
SELECT msg
    FROM TABLE(t())
    ORDER BY msg;
+-------+
| MSG   |
|-------|
| Hello |
| World |
+-------+
```

This is another basic example of a UDTF. It queries a table and returns two of the columns from that table:

Copy code

```
create or replace table orders (
    product_id varchar, 
    quantity_sold numeric(11, 2)
    );

insert into orders (product_id, quantity_sold) values 
    ('compostable bags', 2000),
    ('re-usable cups',  1000);
```

Copy code

```
create or replace function orders_for_product(PROD_ID varchar)
    returns table (Product_ID varchar, Quantity_Sold numeric(11, 2))
    as
    $$
        select product_ID, quantity_sold 
            from orders 
            where product_ID = PROD_ID
    $$
    ;
```

Copy code

```
select product_id, quantity_sold
    from table(orders_for_product('compostable bags'))
    order by product_id;
+------------------+---------------+
| PRODUCT_ID       | QUANTITY_SOLD |
|------------------+---------------|
| compostable bags |       2000.00 |
+------------------+---------------+
```

This same functionality can also be implemented using a view.

### Examples with joins

Create and use a SQL UDTF that returns country information (`COUNTRY_CODE` and `COUNTRY_NAME`) for a specified user ID:

Copy code

```
create or replace table countries (country_code char(2), country_name varchar);
insert into countries (country_code, country_name) values 
    ('FR', 'FRANCE'),
    ('US', 'UNITED STATES'),
    ('ES', 'SPAIN');

create or replace table user_addresses (user_ID integer, country_code char(2));
insert into user_addresses (user_id, country_code) values 
    (100, 'ES'),
    (123, 'FR'),
    (123, 'US');
```

Copy code

```
CREATE OR REPLACE FUNCTION get_countries_for_user ( id number )
  RETURNS TABLE (country_code char, country_name varchar)
  AS 'select distinct c.country_code, c.country_name
      from user_addresses a, countries c
      where a.user_id = id
      and c.country_code = a.country_code';
```

Copy code

```
select *
    from table(get_countries_for_user(123)) cc
    where cc.country_code in ('US','FR','CA')
    order by country_code;
+--------------+---------------+
| COUNTRY_CODE | COUNTRY_NAME  |
|--------------+---------------|
| FR           | FRANCE        |
| US           | UNITED STATES |
+--------------+---------------+
```

Create a SQL UDTF that returns the favorite color for a specified year:

Copy code

```
create or replace table favorite_years as
    select 2016 year
    UNION ALL
    select 2017
    UNION ALL
    select 2018
    UNION ALL
    select 2019;

 create or replace table colors as
    select 2017 year, 'red' color, true favorite
    UNION ALL
    select 2017 year, 'orange' color, true favorite
    UNION ALL
    select 2017 year, 'green' color, false favorite
    UNION ALL
    select 2018 year, 'blue' color, true favorite
    UNION ALL
    select 2018 year, 'violet' color, true favorite
    UNION ALL
    select 2018 year, 'brown' color, false favorite;

create or replace table fashion as
    select 2017 year, 'red' fashion_color
    UNION ALL
    select 2018 year, 'black' fashion_color
    UNION ALL
    select 2019 year, 'orange' fashion_color;
```

Copy code

```
create or replace function favorite_colors(the_year int)
    returns table(color string) as
    'select color from colors where year=the_year and favorite=true';
```

Use the UDTF in a query:

Copy code

```
select color
    from table(favorite_colors(2017))
    order by color;
+--------+
| COLOR  |
|--------|
| orange |
| red    |
+--------+
```

Use the UDTF in a join with another table; note that the join column from the table is passed as an argument to the function.

Copy code

```
select * 
    from favorite_years y join table(favorite_colors(y.year)) c
    order by year, color;
+------+--------+
| YEAR | COLOR  |
|------+--------|
| 2017 | orange |
| 2017 | red    |
| 2018 | blue   |
| 2018 | violet |
+------+--------+
```

Use a WHERE clause, rather than ON, for additional predicates:

Copy code

```
select * 
    from fashion f join table(favorite_colors(f.year)) fav
    where fav.color = f.fashion_color ;
+------+---------------+-------+
| YEAR | FASHION_COLOR | COLOR |
|------+---------------+-------|
| 2017 | red           | red   |
+------+---------------+-------+
```

Use the UDTF with a constant in a join expression; note that a WHERE clause, rather than ON, must be used for additional join conditions:

Copy code

```
select fav.color as favorite_2017, f.*
    from fashion f JOIN table(favorite_colors(2017)) fav
    where fav.color = f.fashion_color
    order by year;
+---------------+------+---------------+
| FAVORITE_2017 | YEAR | FASHION_COLOR |
|---------------+------+---------------|
| red           | 2017 | red           |
| orange        | 2019 | orange        |
+---------------+------+---------------+
```
