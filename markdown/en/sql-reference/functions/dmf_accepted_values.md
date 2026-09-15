Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# ACCEPTED\_VALUES (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the number of records where the value of a column does *not* match a Boolean expression.

## Syntax

Copy code

```
SNOWFLAKE.CORE.ACCEPTED_VALUES ON ( <column>, <lambda-expression> )
```

## Arguments

`column`
:   Specifies the column that contains values that are compared to the Boolean expression in `lambda-expression`.

`lambda-expression`
:   Specifies a lambda expression consisting of the following syntax: `column -> expression`.

    The function returns the number of records where the value of `column` doesn’t match the Boolean expression. This expression can
    use the following operations and functions:

    - [Comparison operators](/sql-reference/operators-comparison)
    - [Logical operators](/sql-reference/operators-logical)
    - [[ NOT ] LIKE](/sql-reference/functions/like)
    - [[ NOT ] IN](/sql-reference/functions/in)
    - [IS [ NOT ] NULL](/sql-reference/functions/is-null)

    The `column` in the lambda expression always matches the `column` argument.

## Allowed data types

The column specified in the `column` and `lambda-expression` arguments can contain any of the following data types:

- DATE
- FLOAT
- NUMBER
- TIMESTAMP\_LTZ
- TIMESTAMP\_NTZ
- TIMESTAMP\_TZ
- VARCHAR

## Returns

The function returns a NUMBER value.

## Usage notes

- You can’t call this function directly. To learn how to associate the function with a table or view so it
  runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

  You can use the [SYSTEM$DATA\_METRIC\_SCAN](/sql-reference/functions/system_data_metric_scan) function to run the ACCEPTED\_VALUES function against a table without
  associating it.
- You cannot associate this function with the same column more than once.
- Renaming a column that is specified in the ACCEPTED\_VALUES function breaks the association between the function and the column’s table or
  view. If you rename the column, you must re-associate the function with the table or view.

## Examples

Associate the function with table `t1` so it returns the number of records where the value of the column `age` is *not* equal to five.

Copy code

```
ALTER TABLE t1
  ADD DATA METRIC FUNCTION SNOWFLAKE.CORE.ACCEPTED_VALUES ON (age, age -> age = 5);
```

Associate the function with view `order_details` so it returns the number of records where the value of column `order_status` is *not*
in the list of strings `Pending`, `Dispatched`, and `Delivered`.

Copy code

```
ALTER VIEW order_details
  ADD DATA METRIC FUNCTION SNOWFLAKE.CORE.ACCEPTED_VALUES ON (
    order_status,
    order_status -> order_status IN ('Pending', 'Dispatched', 'Delivered'));
```
