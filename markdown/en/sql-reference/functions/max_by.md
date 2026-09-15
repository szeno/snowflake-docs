Categories:
:   [Aggregate functions](/sql-reference/functions-aggregation) (General)

# MAX\_BY

Finds the row(s) containing the maximum value for a column and returns the value of another column in that row.

For example, if a table contains the columns `employee_id` and `salary`, `MAX_BY(employee_id, salary)` returns the value
of the `employee_id` column for the row that has the highest value in the `salary` column.

If multiple rows contain the specified maximum value, the function is non-deterministic.

To return values for multiple rows, specify the optional `maximum_number_of_values_to_return` argument. With this
additional argument:

- The function returns an [ARRAY](/sql-reference/data-types-semistructured#label-data-type-array) containing the values of a column for the rows with the highest
  values of a specified column.
- The values in the ARRAY are sorted by their corresponding values in the column containing the maximum values.
- If multiple rows contain these highest values, the function is non-deterministic.

For example, `MAX_BY(employee_id, salary, 5)` returns an ARRAY of values of the `employee_id` column for the five rows
containing the highest values in the `salary` column. The IDs in the ARRAY are sorted by the corresponding values in the
`salary` column.

See also:
:   [MAX](/sql-reference/functions/max)

## Syntax

Copy code

```
MAX_BY( <col_to_return>, <col_containing_maximum> [ , <maximum_number_of_values_to_return> ] )
```

## Arguments

**Required:**

`col_to_return`
:   Column containing the value to return.

`col_containing_maximum`
:   Column containing the maximum value.

**Optional:**

`maximum_number_of_values_to_return`
:   Constant integer specifying the maximum number of values to return. You must specify a positive number. The maximum number that
    you can specify is `1000`.

## Returns

- If `maximum_number_of_values_to_return` is not specified, the function returns a value of the same type as
  `col_to_return`.
- If `maximum_number_of_values_to_return` is specified, the function returns an ARRAY containing values of the same type
  as `col_to_return`. The values in the ARRAY are sorted by their corresponding `col_containing_maximum` values.

  For example, `MAX_BY(employee_id, salary, 5)` returns the IDs of the employees with the highest five salaries, sorted by
  `salary` (in descending order).

## Usage notes

- The function ignores NULL values in `col_containing_maximum`.
- If all values in `col_containing_maximum` are NULL, the function returns NULL (regardless of whether the optional
  `maximum_number_of_values_to_return` argument is specified).

## Examples

The following examples demonstrate how to use the MAX\_BY function.

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

The following example returns the ID of the employee with the highest salary:

Copy code

```
SELECT MAX_BY(employee_id, salary) FROM employees;
```

```
+-----------------------------+
| MAX_BY(EMPLOYEE_ID, SALARY) |
|-----------------------------|
|                         900 |
+-----------------------------+
```

Note the following:

- Because more than one row contains the maximum value for the `salary` column, the function is non-deterministic and might
  return the employee ID for a different row in subsequent executions.
- The function ignores the NULL value in the `salary` column when determining the rows with the maximum values.

The following example returns an ARRAY containing the IDs of the employees with the three highest salaries:

Copy code

```
SELECT MAX_BY(employee_id, salary, 3) from employees;
```

```
+--------------------------------+
| MAX_BY(EMPLOYEE_ID, SALARY, 3) |
|--------------------------------|
| [                              |
|   900,                         |
|   2010,                        |
|   1001                         |
| ]                              |
+--------------------------------+
```

As shown in the example, the values in the ARRAY are sorted by their corresponding values in the `salary` column. So,
MAX\_BY returns the IDs of employees sorted by their salary in descending order.

If more than one of these rows contain the same value in the `salary` column, the order of the returned values for that salary
is non-deterministic.

See also [Using the MIN\_BY and MAX\_BY aggregate functions](/user-guide/querying-time-series-data#label-using-min-by-and-max-by).
