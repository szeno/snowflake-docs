Categories:
:   [Query syntax](/sql-reference/constructs)

# GROUP BY GROUPING SETS

GROUPING SETS is a powerful extension of the [GROUP BY](/sql-reference/constructs/group-by) clause that computes multiple GROUP BY clauses in a single statement. A *grouping set* is a set of dimension columns.

GROUPING SETS expressions can be combined with other GROUP BY expressions, making this construct an integrated part of the GROUP BY clause rather than a separate construct. For example, you can write `GROUP BY x, GROUPING SETS(y, z)` to group by column `x` in combination with separate groupings on `y` and `z`.

A GROUPING SETS expression is equivalent to the union of two or more [GROUP BY](/sql-reference/constructs/group-by) operations in the same result set. For example:

- `GROUP BY GROUPING SETS((a))` is equivalent to the single grouping set operation `GROUP BY a`.
- `GROUP BY GROUPING SETS((a), (b))` is equivalent to `GROUP BY a UNION ALL GROUP BY b`.

Note that `GROUPING SETS(a, b)` without additional parentheses is logically equivalent to `GROUPING SETS((a), (b))` because both create two separate grouping sets, one for column `a` and one for column `b`. This expression is quite different from `GROUPING SETS((a, b))`, which creates a single grouping set that groups by both columns.

## Syntax

Copy code

```
SELECT ...
FROM ...
[ ... ]
GROUP BY [ groupItem [ , groupItem [ , ... ] ] , ] GROUPING SETS ( groupSet [ , groupSet [ , ... ] ] )
[ ... ]
```

Where:

> Copy code
>
> ```
> groupItem ::= { <column_alias> | <position> | <expr> }
>
> groupSet ::= groupItem | ( groupItem [ , groupItem [ , ... ] ] )
> ```

## Parameters

`column_alias`
:   Column alias appearing in the query block’s [SELECT](/sql-reference/sql/select) list.

`position`
:   Position of an expression in the [SELECT](/sql-reference/sql/select) list.

`expr`
:   Any expression on tables in the current scope.

## Usage notes

- Snowflake allows up to 128 grouping sets in the same query block.
- Syntax variations with parentheses:

  - `GROUPING SETS(a, b)` is shorthand for `GROUPING SETS((a), (b))`. Both create two separate grouping sets: one that groups by column `a`, and another that groups by column `b`.
  - `GROUPING SETS((a, b))` creates a single grouping set that groups by both columns `a` and `b` (similar to `GROUP BY a, b`).
- You can combine regular GROUP BY columns with GROUPING SETS: `GROUP BY x, GROUPING SETS(y, z)` groups by column `x` in combination with separate groupings on `y` and `z`.
- The output typically contains some NULL values. Because GROUP BY GROUPING SETS
  merges the results of two or more result sets, each of which was
  grouped by different criteria, some columns that have a single value
  in one result set might have many corresponding values in the
  other result set. For example, if you do a union of a set of
  employees grouped by department with a set grouped by seniority, the
  members of the set with the greatest seniority are not necessarily all
  in the same department, so the value of `department_name` is set to
  NULL. The following examples contain NULL values for this reason.

## See also

- [GROUPING](/sql-reference/functions/grouping) (Utility function to identify which grouping level produced each row)
- [GROUP BY ROLLUP](/sql-reference/constructs/group-by-rollup)
- [GROUP BY CUBE](/sql-reference/constructs/group-by-cube)

## Examples

These examples use a table of information about nurses who are trained to
assist in disasters. All of these nurses have a license as nurses (for example,
an RN has a license as a “Registered Nurse”), and an additional license (for example,
in a disaster-related specialty, such as search and rescue, radio
communications, and so on). This example simplifies and uses just two categories
of licenses:

- Nursing: RN (Registered Nurse) and LVN (Licensed Vocational Nurse).
- Amateur (“ham”) Radio: Ham radio licenses include “Technician”, “General”, and “Amateur Extra”.

The following commands create and load the table:

Copy code

```
CREATE or replace TABLE nurses (
  ID INTEGER,
  full_name VARCHAR,
  medical_license VARCHAR,   -- LVN, RN, etc.
  radio_license VARCHAR      -- Technician, General, Amateur Extra
  )
  ;

INSERT INTO nurses
    (ID, full_name, medical_license, radio_license)
  VALUES
    (201, 'Thomas Leonard Vicente', 'LVN', 'Technician'),
    (202, 'Tamara Lolita VanZant', 'LVN', 'Technician'),
    (341, 'Georgeann Linda Vente', 'LVN', 'General'),
    (471, 'Andrea Renee Nouveau', 'RN', 'Amateur Extra')
    ;
```

This query uses GROUP BY GROUPING SETS:

Copy code

```
SELECT COUNT(*), medical_license, radio_license
  FROM nurses
  GROUP BY GROUPING SETS (medical_license, radio_license)
  ORDER BY 3 DESC NULLS FIRST;
```

The first two rows show the count of RNs and LVNs (two types of nursing
licenses). The NULL values in the `radio_license` column for
those two rows are deliberate; the query grouped all of the LVNs together
(and all the RNs together) regardless of their radio license, so the
results can’t show one value in the `radio_license` column for each
row that necessarily applies to all the LVNs or RNs grouped in that row.

The next three rows show the number of nurses with each type of ham radio
license (“Technician”, “General”, and “Amateur Extra”). The NULL value
for `medical_license` in each of those three rows is deliberate because
no single medical license necessarily applies to all members of each
of those rows.

```
+----------+-----------------+---------------+
| COUNT(*) | MEDICAL_LICENSE | RADIO_LICENSE |
|----------+-----------------+---------------|
|        3 | LVN             | NULL          |
|        1 | RN              | NULL          |
|        2 | NULL            | Technician    |
|        1 | NULL            | General       |
|        1 | NULL            | Amateur Extra |
+----------+-----------------+---------------+
```

The following example demonstrates the difference between grouping by columns
separately versus grouping by columns together. The query groups by the
combination of both `medical_license` and `radio_license`:

Copy code

```
SELECT COUNT(*), medical_license, radio_license
  FROM nurses
  GROUP BY GROUPING SETS ((medical_license, radio_license))
  ORDER BY 3 DESC NULLS FIRST;
```

This query produces rows where each combination of `medical_license` and
`radio_license` appears with its count. Unlike the previous example, there
are no NULL values in the output because the query groups by both columns
together rather than creating separate groupings for each column.

```
+----------+-----------------+---------------+
| COUNT(*) | MEDICAL_LICENSE | RADIO_LICENSE |
|----------+-----------------+---------------|
|        2 | LVN             | Technician    |
|        1 | LVN             | General       |
|        1 | RN              | Amateur Extra |
+----------+-----------------+---------------+
```

The next example shows what happens when some columns contain NULL values.
Start by adding three new nurses who don’t yet have ham radio licenses.

Copy code

```
INSERT INTO nurses
    (ID, full_name, medical_license, radio_license)
  VALUES
    (101, 'Lily Vine', 'LVN', NULL),
    (102, 'Larry Vancouver', 'LVN', NULL),
    (172, 'Rhonda Nova', 'RN', NULL)
    ;
```

Then run the same query as before:

Copy code

```
SELECT COUNT(*), medical_license, radio_license
  FROM nurses
  GROUP BY GROUPING SETS (medical_license, radio_license)
  ORDER BY 3 DESC NULLS FIRST;
```

Why is there now a row that has NULL in both columns? And if all the values are
NULL, why is the COUNT(\*) result equal to 3?

The answer is that the NULL in the `radio_license` column of that row
occurs because three nurses don’t have any radio license. (The query
`SELECT DISTINCT radio_license FROM nurses` now returns four distinct
values: “Technician”, “General”, “Amateur Extra”, and “NULL”.)

The NULL value in the `medical_licenses` column occurs for the same reason that
NULL values occur in the earlier query results: the nurses counted in this
row have different medical licenses, so no one value (`RN` or `LVN`)
necessarily applies to all of the nurses counted in this row.

```
+----------+-----------------+---------------+
| COUNT(*) | MEDICAL_LICENSE | RADIO_LICENSE |
|----------+-----------------+---------------|
|        2 | RN              | NULL          |
|        5 | LVN             | NULL          |
|        3 | NULL            | NULL          |
|        2 | NULL            | Technician    |
|        1 | NULL            | General       |
|        1 | NULL            | Amateur Extra |
+----------+-----------------+---------------+
```

The following example demonstrates the combination of regular GROUP BY columns with GROUPING SETS.
This query groups by `medical_license`, and within each medical license group, creates
separate aggregations for each `radio_license` value and for all radio licenses combined:

Copy code

```
SELECT COUNT(*), medical_license, radio_license
  FROM nurses
  GROUP BY medical_license, GROUPING SETS (radio_license, ())
  ORDER BY 3 DESC NULLS FIRST;
```

For each medical license (LVN and RN), the output shows:

- Rows grouped by each specific `radio_license` value (Technician, General, Amateur Extra, or NULL for those without a radio license)
- A summary row with NULL in the `radio_license` column representing all nurses with that medical license, regardless of their radio license

```
+----------+-----------------+---------------+
| COUNT(*) | MEDICAL_LICENSE | RADIO_LICENSE |
|----------+-----------------+---------------|
|        2 | LVN             | NULL          |
|        1 | RN              | NULL          |
|        2 | RN              | NULL          |
|        5 | LVN             | NULL          |
|        2 | LVN             | Technician    |
|        1 | LVN             | General       |
|        1 | RN              | Amateur Extra |
+----------+-----------------+---------------+
```

You can compare this output to the output of a GROUP BY query without the GROUPING SETS clause:

Copy code

```
SELECT COUNT(*), medical_license, radio_license
  FROM nurses
  GROUP BY medical_license, radio_license
  ORDER BY 3 DESC NULLS FIRST;
```

```
+----------+-----------------+---------------+
| COUNT(*) | MEDICAL_LICENSE | RADIO_LICENSE |
|----------+-----------------+---------------|
|        2 | LVN             | NULL          |
|        1 | RN              | NULL          |
|        2 | LVN             | Technician    |
|        1 | LVN             | General       |
|        1 | RN              | Amateur Extra |
+----------+-----------------+---------------+
```

### Using the GROUPING function

The [GROUPING](/sql-reference/functions/grouping) utility function helps identify
which level of aggregation produced each row. This is especially useful for distinguishing
between NULL values that result from the grouping operation versus actual NULL values in
the data.

The GROUPING function returns:

- `0` for a row that is grouped on the specified column
- `1` for a row that is not grouped on the specified column (where NULL appears due to aggregation)

This example adds GROUPING functions to the query to clarify the output:

Copy code

```
SELECT
    COUNT(*),
    medical_license,
    radio_license,
    GROUPING(medical_license) AS grp_medical,
    GROUPING(radio_license) AS grp_radio
  FROM nurses
  GROUP BY GROUPING SETS (medical_license, radio_license);
```

The `grp_medical` and `grp_radio` columns show which columns were used for grouping:

- Rows 1-2: Grouped by `medical_license` (`grp_medical=0`), not by `radio_license` (`grp_radio=1`)
- Rows 3-6: Grouped by `radio_license` (`grp_radio=0`), not by `medical_license` (`grp_medical=1`)
- Row 6: The NULL value in `radio_license` is actual data (`grp_radio=0`), while the NULL in `medical_license` is from aggregation (`grp_medical=1`)

```
+----------+-----------------+---------------+-------------+-----------+
| COUNT(*) | MEDICAL_LICENSE | RADIO_LICENSE | GRP_MEDICAL | GRP_RADIO |
|----------+-----------------+---------------+-------------+-----------|
|        2 | RN              | NULL          |           0 |         1 |
|        5 | LVN             | NULL          |           0 |         1 |
|        2 | NULL            | Technician    |           1 |         0 |
|        1 | NULL            | General       |           1 |         0 |
|        3 | NULL            | NULL          |           1 |         0 |
|        1 | NULL            | Amateur Extra |           1 |         0 |
+----------+-----------------+---------------+-------------+-----------+
```
