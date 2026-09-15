# Code Conversion - Teradata Considerations

## Numeric Data Operations

### Calculation Precision

Teradata and Snowflake handle calculations differently:

- Teradata rounds numbers after each calculation step based on the data type:

  - For decimal types, it maintains the larger precision
  - For NUMBER types, it keeps full precision
- Snowflake stores all numbers using the NUMBER data type, maintaining full precision throughout calculations. This can lead to different results compared to Teradata, especially when working with decimal, integer, or float types.

This difference in behavior is not adjusted during code conversion since it’s typically not what developers intend to change.

Teradata: SELECT (1.00/28) \_ 15.00 /\_ Returns 0.60 \*/

Snowflake will round the result of the division (1.00/28) \_ 15.00 to two decimal places:
SELECT (1.00/28) \_ 15.00 = 0.535710 = 0.54

### Integer-Integer Division

When dividing two integer values, Teradata performs truncation (floor), while Snowflake performs rounding. To maintain consistent behavior during migration, the automated code conversion automatically adds a TRUNC statement in these cases.

Teradata: SELECT (5/3) = 1 /\_ Returns 1 since integer division rounds down \_/

Snowflake: When dividing 5 by 3, the result is 1.6666666, which rounds to 2

Truncated Division in Snowflake: SELECT TRUNC(5/3) returns 1

### Banker Rounding

Teradata offers Banker’s rounding through the ROUNDHALFWAYMAGUP parameter, while Snowflake uses standard rounding methods only.

| SQL | Teradata | Snowflake |
| --- | --- | --- |
| CAST( <mark style=”background-color:blue;”>1.05</mark> AS DECIMAL(9,1)) | <mark style=”background-color:orange;”>1.0</mark> | <mark style=”background-color:orange;”>1.1</mark> |
| CAST( <mark style=”background-color:blue;”>1.15</mark> AS DECIMAL(9,1)) | 1.2 | 1.2 |
| CAST( <mark style=”background-color:blue;”>1.25</mark> AS DECIMAL(9,1)) | <mark style=”background-color:orange;”>1.2</mark> | <mark style=”background-color:orange;”>1.3</mark> |
| CAST( <mark style=”background-color:blue;”>1.35</mark> AS DECIMAL(9,1)) | 1.4 | 1.4 |
| CAST( <mark style=”background-color:blue;”>1.45</mark> AS DECIMAL(9,1)) | <mark style=”background-color:orange;”>1.4</mark> | <mark style=”background-color:orange;”>1.5</mark> |
| CAST( <mark style=”background-color:blue;”>1.55</mark> AS DECIMAL(9,1)) | 1.6 | 1.6 |
| CAST( <mark style=”background-color:blue;”>1.65</mark> AS DECIMAL(9,1)) | <mark style=”background-color:orange;”>1.6</mark> | <mark style=”background-color:orange;”>1.7</mark> |
| CAST( <mark style=”background-color:blue;”>1.75</mark> AS DECIMAL(9,1)) | 1.8 | 1.8 |
| CAST( <mark style=”background-color:blue;”>1.85</mark> AS DECIMAL(9,1)) | <mark style=”background-color:orange;”>1.8</mark> | <mark style=”background-color:orange;”>1.9</mark> |
| CAST( <mark style=”background-color:blue;”>1.95</mark> AS DECIMAL(9,1)) | 2.0 | 2.0 |

Expand

Show lessSee more

### Decimal to Integer Conversion

Teradata and Snowflake handle decimal values differently. While Teradata truncates decimal values, Snowflake rounds them to the nearest integer. To maintain consistency with Teradata’s behavior, the conversion process automatically adds a TRUNC statement.

| SQL | Teradata | Snowflake |
| --- | --- | --- |
| CAST( <mark style=”background-color:blue;”>1.0</mark> AS INTEGER) | 1 | 1 |
| CAST( <mark style=”background-color:blue;”>1.1</mark> AS INTEGER) | 1 | 1 |
| CAST( <mark style=”background-color:blue;”>1.2</mark> AS INTEGER) | 1 | 1 |
| CAST( <mark style=”background-color:blue;”>1.3</mark> AS INTEGER) | 1 | 1 |
| CAST( <mark style=”background-color:blue;”>1.4</mark> AS INTEGER) | 1 | 1 |
| CAST( <mark style=”background-color:blue;”>1.5</mark> AS INTEGER) | <mark style=”background-color:orange;”>1</mark> | <mark style=”background-color:orange;”>2</mark> |
| CAST( <mark style=”background-color:blue;”>1.6</mark> AS INTEGER) | <mark style=”background-color:orange;”>1</mark> | <mark style=”background-color:orange;”>2</mark> |
| CAST( <mark style=”background-color:blue;”>1.7</mark> AS INTEGER) | <mark style=”background-color:orange;”>1</mark> | <mark style=”background-color:orange;”>2</mark> |
| CAST( <mark style=”background-color:blue;”>1.8</mark> AS INTEGER) | <mark style=”background-color:orange;”>1</mark> | <mark style=”background-color:orange;”>2</mark> |
| CAST( <mark style=”background-color:blue;”>1.9</mark> AS INTEGER) | <mark style=”background-color:orange;”>1</mark> | <mark style=”background-color:orange;”>2</mark> |

Expand

Show lessSee more

### Number without Precision/Scale

When a Teradata NUMBER column is defined without specifying scale or precision, it can store decimal values with varying scale (from 0 to 38), as long as the total precision stays within 38 digits. However, Snowflake requires fixed scale and precision values for NUMBER columns. Here’s an example of how numbers are defined in a Teradata table with this flexible format:

Copy code

```
:force:
CREATE MULTISET TABLE DATABASEXYZ.TABLE_NUMS
     (NUM_COL1 NUMBER(*),
      NUM_COL2 NUMBER,
      NUM_COL3 NUMBER(38,*));
```

The following table shows two examples of values that exceed Snowflake’s column size limits. These values could appear in any of the previously shown Teradata columns.

Value 1: 123,345,678,901,234,567,891,012.0123456789

Value 2: 123.12345678901234567890

These numeric values would require a NUMBER(42, 20) data type, which exceeds Snowflake’s maximum precision limit of 38. Snowflake is currently working on implementing flexible precision and scale functionality.

### Truncation on INSERT for SQL DML Statements

Teradata automatically truncates string values that exceed the defined field length during insertion. While SnowConvert AI CLI maintains the same field lengths during conversion (for example, VARCHAR(20) remains VARCHAR(20)), Snowflake does not automatically truncate oversized strings. If your data ingestion process depends on automatic truncation, you will need to manually modify it by adding a LEFT() function. SnowConvert AI CLI intentionally does not add truncation automatically due to the potential impact across the entire codebase.

### Float Default Issue Example:

Copy code

```
:force:
/* <sc-table> TABLE DUMMY.EXAMPLE </sc-table> */
/**** WARNING: SET TABLE FUNCTIONALITY NOT SUPPORTED ****/
CREATE TABLE DUMMY.PUBLIC.EXAMPLE (
LOGTYPE INTEGER,
OPERSEQ INTEGER DEFAULT 0,
RUNTIME FLOAT /**** ERROR: DEFAULT CURRENT_TIME NOT VALID FOR DATA TYPE ****/
);
```

### Float Data Aggregation

Floating-point numbers are approximate representations of decimal values. Due to these approximations, different database systems may produce slightly different results when performing calculations and aggregations with float data types. This variation occurs because each database system handles floating-point arithmetic and rounding in its own way.

## Other Considerations

### Join Elimination

Snowflake executes SQL queries exactly as written, including all specified joins, regardless of whether they affect the final results. Unlike Snowflake, Teradata can automatically remove unnecessary joins by using primary and foreign key relationships defined in the table structure. This feature in Teradata primarily helps prevent poorly written queries, and it’s usually only a concern when code was specifically written to use this capability. If your existing code was designed to take advantage of Teradata’s join elimination feature, automated code conversion tools cannot address this limitation. In such cases, you may need to redesign parts of your solution.

**Using Window Functions with max() and order by**

#### Teradata behavior and defaults:

**Default**: When an ORDER BY clause is present but no ROWS or ROWS BETWEEN clause is specified, Teradata SQL window aggregate functions automatically use **ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING**.

#### Snowflake behavior and defaults:

**Default**: When you use a window aggregate function with an ORDER BY clause but without specifying ROWS or ROWS BETWEEN, Snowflake automatically applies **ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW** as the window frame.

**Example:**

Below is a sample table named TEST\_WIN that shows employee salary data across various departments.

| DEPT\_NM | DEPT\_NO | EMP\_NO | SALARY |
| --- | --- | --- | --- |
| SALES | 10 | 11 | 5000 |
| SALES | 10 | 12 | 6000 |
| HR | 20 | 21 | 1000 |
| HR | 20 | 22 | 2000 |
| PS | 30 | 31 | 7000 |
| PS | 30 | 32 | 9000 |

The following code, when executed in Teradata, calculates the highest salary among all employees, grouped by department.

Copy code

```
:force:
SELECT DEPT_NM, SALARY ,DEPT_NO,
MAX(SALARY) OVER ( ORDER BY DEPT_NO  ) AS MAX_DEPT_SALARY
FROM TEST_WIN;
```

| DEPT\_NM | SALARY | DEPT\_NO | MAX\_DEPT\_SALARY |
| --- | --- | --- | --- |
| SALES | 6000 | 10 | 9000 |
| SALES | 5000 | 10 | 9000 |
| HR | 2000 | 20 | 9000 |
| HR | 1000 | 20 | 9000 |
| PS | 7000 | 30 | 9000 |
| PS | 9000 | 30 | 9000 |

When executing the converted code using Snowflake-SnowConvert AI CLI, you may notice different results (highlighted values). These differences are expected and align with Snowflake’s default settings.

Copy code

```
:force:
SELECT DEPT_NM, SALARY ,DEPT_NO,
MAX(SALARY) OVER ( ORDER BY DEPT_NO  ) AS MAX_DEPT_SALARY
FROM TEST_WIN;
```

| DEPT\_NM | SALARY | DEPT\_NO | MAX\_DEPT\_SALARY |
| --- | --- | --- | --- |
| SALES | 5000 | 10 | 6000 |
| SALES | 6000 | 10 | 6000 |
| HR | 1000 | 20 | 6000 |
| HR | 2000 | 20 | 6000 |
| PS | 7000 | 30 | 9000 |
| PS | 9000 | 30 | 9000 |

To achieve identical results as in Teradata, you must specify the ROWS/RANGE value as shown in the code below.

Copy code

```
:force:
SELECT DEPT_NM, SALARY ,DEPT_NO,
MAX(SALARY) OVER ( ORDER BY DEPT_NO RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS MAX_DEPT_SALARY
FROM TEST WIN;
```

| DEPT\_NM | SALARY | DEPT\_NO | MAX\_DEPT\_SALARY |
| --- | --- | --- | --- |
| SALES | 5000 | 10 | 9000 |
| SALES | 6000 | 10 | 9000 |
| HR | 1000 | 20 | 9000 |
| HR | 2000 | 20 | 9000 |
| PS | 7000 | 30 | 9000 |
| PS | 9000 | 30 | 9000 |

The RANGE/ROWS clause explicitly defines how rows are ordered. You can achieve similar results by removing the ORDER BY clause completely.

## References

Snowflake: <https://docs.snowflake.com/en/sql-reference/functions-analytic.html>
Teradata: <https://docs.teradata.com/r/756LNiPSFdY~4JcCCcR5Cw/dIV_fAtkK3UeUIQ5_uucQw>
