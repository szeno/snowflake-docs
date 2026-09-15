Categories:
:   [Aggregate functions](/sql-reference/functions-aggregation) (General)

# MIN\_BY

Finds the row(s) containing the minimum value for a column and returns the value of another column in that row.

For example, if a table contains the columns `employee_id` and `salary`, `MIN_BY(employee_id, salary)` returns the value
of the `employee_id` column for the row that has the lowest value in the `salary` column.

If multiple rows contain the specified minimum value, the function is non-deterministic.

To return values for multiple rows, specify the optional `maximum_number_of_values_to_return` argument. With this
additional argument:

- The function returns an [ARRAY](/sql-reference/data-types-semistructured#label-data-type-array) containing the values of a column for the rows with the lowest
  values of a specified column.
- The values in the ARRAY are sorted by their corresponding values in the column containing the minimum values.
- If multiple rows contain these lowest values, the function is non-deterministic.

For example, `MIN_BY(employee_id, salary, 5)` returns an ARRAY of values of the `employee_id` column for the five rows
containing the lowest values in the `salary` column. The IDs in the ARRAY are sorted by the corresponding values in the
`salary` column.

See also:
:   [MIN](/sql-reference/functions/min)

## Syntax

Copy code

```
MIN_BY( <col_to_return>, <col_containing_minimum> [ , <maximum_number_of_values_to_return> ] )
```

## Arguments

**Required:**

`col_to_return`
:   Column containing the value to return.

`col_containing_minimum`
:   Column containing the minimum value.

**Optional:**

`maximum_number_of_values_to_return`
:   Constant integer specifying the maximum number of values to return. You must specify a positive number. The maximum number that
    you can specify is `1000`.

## Returns

- If `maximum_number_of_values_to_return` is not specified, the function returns a value of the same type as
  `col_to_return`.
- If `maximum_number_of_values_to_return` is specified, the function returns an ARRAY containing values of the same type
  as `col_to_return`. The values in the ARRAY are sorted by their corresponding `col_containing_minimum` values.

  For example, `MIN_BY(employee_id, salary, 5)` returns the IDs of the employees with the lowest five salaries, sorted by
  `salary` (in ascending order).

## Usage notes

- The function ignores NULL values in `col_containing_minimum`.
- If all values in `col_containing_minimum` are NULL, the function returns NULL (regardless of whether the optional
  `maximum_number_of_values_to_return` argument is specified).

## Examples

The following examples demonstrate how to use the MIN\_BY function.

To run these examples, execute the following statements to set up the table and data for the examples:

Copy code

```
CREATE OR REPLACE TABLE employees(employee_id NUMBER, department_id NUMBER, salary NUMBER);

INSERT INTO employees VALUES
  (1001, 10, 10000),
  (1020, 10, 9000),
  (1030, 10, 8000),
  (900, 20, 15000),
  (2000, 20, NULL),
  (2010, 20, 15000),
  (2020, 20, 8000);
```

Execute the following statement to view the contents of this table:

Copy code

```
SELECT * FROM employees;
```

```
+-------------+---------------+--------+
| EMPLOYEE_ID | DEPARTMENT_ID | SALARY |
|-------------+---------------+--------|
|        1001 |            10 |  10000 |
|        1020 |            10 |   9000 |
|        1030 |            10 |   8000 |
|         900 |            20 |  15000 |
|        2000 |            20 |   NULL |
|        2010 |            20 |  15000 |
|        2020 |            20 |   8000 |
+-------------+---------------+--------+
```

The following example returns the ID of the employee with the lowest salary:

Copy code

```
SELECT MIN_BY(employee_id, salary) FROM employees;
```

```
+-----------------------------+
| MIN_BY(EMPLOYEE_ID, SALARY) |
|-----------------------------|
|                        1030 |
+-----------------------------+
```

Note the following:

- Because more than one row contains the minimum value for the `salary` column, the function is non-deterministic and might
  return the employee ID for a different row in subsequent executions.
- The function ignores the NULL value in the `salary` column when determining the rows with the minimum values.

The following example returns an ARRAY containing the IDs of the employees with the three lowest salaries:

Copy code

```
SELECT MIN_BY(employee_id, salary, 3) FROM employees;

+--------------------------------+
| MIN_BY(EMPLOYEE_ID, SALARY, 3) |
|--------------------------------|
| [                              |
|   1030,                        |
|   2020,                        |
|   1020                         |
| ]                              |
+--------------------------------+
```

As shown in the example, the values in the ARRAY are sorted by their corresponding values in the `salary` column. So,
MIN\_BY returns the IDs of employees sorted by their salary in ascending order.

If more than one of these rows contain the same value in the `salary` column, the order of the returned values for that salary
is non-deterministic.

See also [Using the MIN\_BY and MAX\_BY aggregate functions](/user-guide/querying-time-series-data#label-using-min-by-and-max-by).
