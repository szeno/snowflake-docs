Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# ACCEPTED\_VALUES\_PERCENT (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the percentage of records where the value of a column does *not* match a Boolean expression. To get the number of those
records instead, use [ACCEPTED\_VALUES (system data metric function)](/sql-reference/functions/dmf_accepted_values).

## Syntax

Copy code

```
SNOWFLAKE.CORE.ACCEPTED_VALUES_PERCENT ON ( <column>, <lambda-expression> )
```

## Arguments

`column`
:   Specifies the column that contains values that are compared to the Boolean expression in `lambda-expression`.

`lambda-expression`
:   Specifies a lambda expression consisting of the following syntax: `column -> expression`.

    The function returns the percentage of records where the value of `column` doesn’t match the Boolean expression. This expression can
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

The function returns a FLOAT value between 0 and 100: the percentage of records in scope where the value of the column doesn’t
match the Boolean expression. A value of 0 means that no record in scope fails the Boolean expression.

The records in scope are all records in the table or view. If you associate the function with a [FILTER](/user-guide/data-quality-filter)
clause, they are the records that satisfy the filter. If you associate the function with a
[WITHIN GROUP](/user-guide/data-quality-group-by) clause, they are the records in each group.

The function returns NULL if no records are in scope.

## Usage notes

- You can’t call this function directly. To learn how to associate the function with a table or view so it
  runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

  You can use the [SYSTEM$DATA\_METRIC\_SCAN](/sql-reference/functions/system_data_metric_scan) function to run the ACCEPTED\_VALUES\_PERCENT function against a table without
  associating it.

  When you use SYSTEM$DATA\_METRIC\_SCAN with this function, you must specify the ARGUMENT\_EXPRESSION argument, as you do for
  ACCEPTED\_VALUES.
- A record is counted as not matching only when the Boolean expression evaluates to FALSE. If the expression evaluates to NULL, for
  example because a comparison involves a NULL value, the record isn’t counted as not matching. All records are included in the total
  number of records.

  To count NULL values as not matching, include the NULL check in the expression, for example
  `column IS NOT NULL AND column IN ('A', 'B')`.
- Renaming a column that is specified in the ACCEPTED\_VALUES\_PERCENT function breaks the association between the function and the
  column’s table or view. If you rename the column, you must re-associate the function with the table or view.
- You must specify the lambda expression when you associate the function. You can omit it when you drop the association.
- You can’t associate this function with the same column more than once. You can associate both ACCEPTED\_VALUES\_PERCENT and
  [ACCEPTED\_VALUES (system data metric function)](/sql-reference/functions/dmf_accepted_values) with the same column.

## Examples

Associate the function with table `orders` so it returns the percentage of records where the value of the column `status` is *not*
`ACTIVE` or `PENDING`. The expectation is violated when more than 5 percent of the records don’t match:

Copy code

```
ALTER TABLE orders
  ADD DATA METRIC FUNCTION SNOWFLAKE.CORE.ACCEPTED_VALUES_PERCENT
    ON (status, status -> status IN ('ACTIVE', 'PENDING'))
    EXPECTATION at_most_5_pct (VALUE <= 5);
```

Associate the function with view `order_details` so it returns the percentage of records where the value of column `order_status`
is *not* in the list of strings `Pending`, `Dispatched`, and `Delivered`:

Copy code

```
ALTER VIEW order_details
  ADD DATA METRIC FUNCTION SNOWFLAKE.CORE.ACCEPTED_VALUES_PERCENT ON (
    order_status,
    order_status -> order_status IN ('Pending', 'Dispatched', 'Delivered'));
```
