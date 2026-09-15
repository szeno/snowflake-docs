# Oracle - Joins

> A join is a query that combines rows from two or more tables, views, or materialized views. Oracle Database performs a join whenever multiple tables appear in the `FROM` clause of the query. ([Oracle SQL Language Reference JOINS](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/Joins.html#GUID-568EC26F-199A-4339-BFD9-C4A0B9588937))

## Antijoin

Note

Some parts in the output code are omitted for clarity reasons.

### Description

> An antijoin returns rows from the left side of the predicate for which there are no corresponding rows on the right side of the predicate. It returns rows that fail to match (NOT IN) the subquery on the right side. Antijoin transformation cannot be done if the subquery is on an `OR` branch of the `WHERE` clause. ([Oracle SQL Language Reference Anti Join](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/Joins.html#GUID-D688F2E3-7F1E-4339-894F-01A73E62328C)).

No special transformation is performed for this kind of *Join* since Snowflake supports the same syntax.

### Sample Source Patterns

Note

*Order by clause* added because the result order may vary between Oracle and Snowflake.

Note

Since the result set is too large, *Row Limiting Clause* was added. You can remove it to retrieve the entire result set.

Note

Check this [section](../sample-data) to set up the sample database.

#### Where Not In

##### Oracle

Copy code

```
SELECT e.employee_id, e.first_name, e.last_name FROM hr.employees e
WHERE e.department_id NOT IN

    (SELECT h.department_id FROM hr.departments h WHERE location_id = 1700)

ORDER BY e.last_name
FETCH FIRST 10 ROWS ONLY;
```

##### Result

| EMPLOYEE\_ID | FIRST\_NAME | LAST\_NAME |
| --- | --- | --- |
| 174 | Ellen | Abel |
| 166 | Sundar | Ande |
| 130 | Mozhe | Atkinson |
| 105 | David | Austin |
| 204 | Hermann | Baer |
| 167 | Amit | Banda |
| 172 | Elizabeth | Bates |
| 192 | Sarah | Bell |
| 151 | David | Bernstein |
| 129 | Laura | Bissot |

Expand

Show lessSee more

##### Snowflake

Copy code

```
SELECT e.employee_id, e.first_name, e.last_name FROM
    hr.employees e
WHERE e.department_id NOT IN
        !!!RESOLVE EWI!!! /*** SSC-EWI-0108 - THE FOLLOWING SUBQUERY MATCHES AT LEAST ONE OF THE PATTERNS CONSIDERED INVALID AND MAY PRODUCE COMPILATION ERRORS ***/!!!
    (SELECT h.department_id FROM
            hr.departments h WHERE location_id = 1700)

ORDER BY e.last_name
    FETCH FIRST 10 ROWS ONLY;
```

##### Result

| EMPLOYEE\_ID | FIRST\_NAME | LAST\_NAME |
| --- | --- | --- |
| 174 | Ellen | Abel |
| 166 | Sundar | Ande |
| 130 | Mozhe | Atkinson |
| 105 | David | Austin |
| 204 | Hermann | Baer |
| 167 | Amit | Banda |
| 172 | Elizabeth | Bates |
| 192 | Sarah | Bell |
| 151 | David | Bernstein |
| 129 | Laura | Bissot |

Expand

Show lessSee more

#### Where Not Exists

##### Oracle

Copy code

```
SELECT   d.department_id, d.department_name
FROM     hr.departments d
WHERE    NOT EXISTS

         (SELECT 1 FROM hr.employees E WHERE
         e.department_id = d.department_id)

ORDER BY d.department_id
FETCH FIRST 10 ROWS ONLY;
```

##### Result

| DEPARTMENT\_ID | DEPARTMENT\_NAME |
| --- | --- |
| 120 | Treasury |
| 130 | Corporate Tax |
| 140 | Control And Credit |
| 150 | Shareholder Services |
| 160 | Benefits |
| 170 | Manufacturing |
| 180 | Construction |
| 190 | Contracting |
| 200 | Operations |
| 210 | IT Support |

Expand

Show lessSee more

##### Snowflake

Copy code

```
SELECT   d.department_id, d.department_name
FROM
         hr.departments d
WHERE    NOT EXISTS
                  !!!RESOLVE EWI!!! /*** SSC-EWI-0108 - THE FOLLOWING SUBQUERY MATCHES AT LEAST ONE OF THE PATTERNS CONSIDERED INVALID AND MAY PRODUCE COMPILATION ERRORS ***/!!!
         (SELECT 1 FROM
                           hr.employees E WHERE
         e.department_id = d.department_id)

ORDER BY d.department_id
         FETCH FIRST 10 ROWS ONLY;
```

##### Result

| DEPARTMENT\_ID | DEPARTMENT\_NAME |
| --- | --- |
| 120 | Treasury |
| 130 | Corporate Tax |
| 140 | Control And Credit |
| 150 | Shareholder Services |
| 160 | Benefits |
| 170 | Manufacturing |
| 180 | Construction |
| 190 | Contracting |
| 200 | Operations |
| 210 | IT Support |

Expand

Show lessSee more

### Known issues

#### 1. Results ordering mismatch between languages

The result of the query will have the same content in both database engines but the order might be different if no *Order By* clause is defined in the query.

### Related EWIs

1. [SSC-EWI-0108](../../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0108): This subquery matches a pattern considered invalid and may cause compilation errors.

## Band Join

Note

Some parts in the output code are omitted for clarity reasons.

### Description

> A **band join** is a special type of nonequijoin in which key values in one data set must fall within the specified range (“band”) of the second data set. The same table can serve as both the first and second data sets. ([Oracle SQL Language Reference BandJoin](https://docs.oracle.com/en/database/oracle/oracle-database/21/tgsql/joins.html#GUID-24F34188-110F-4245-9DE7-43954092AFE0))

In this section, we will see how a band join is executed in Snowflake and the execution plan is very similar to the improved version of Oracle.

### Sample Source Patterns

Note

*Order by* clause added because the result order may vary between Oracle and Snowflake.

Note

Since the result set is too large, *Row Limiting Clause* was added. You can remove it to retrieve the entire result set.

Note

Check this [section](../sample-data) to set up the sample database.

Warning

If you migrate this code without the create tables, the converter won’t be able to load semantic information of the columns and a warning will appear on the arithmetic operations.

#### Basic Band Join case

##### Oracle

Copy code

```
SELECT  e1.last_name ||
        ' has salary between 100 less and 100 more than ' ||
        e2.last_name AS "SALARY COMPARISON"
FROM    employees e1,
        employees e2
WHERE   e1.salary
BETWEEN e2.salary - 100
AND     e2.salary + 100
ORDER BY "SALARY COMPARISON"
FETCH FIRST 10 ROWS ONLY
```

##### Result

| SALARY COMPARISON |
| --- |
| Abel has salary between 100 less and 100 more than Abel |
| Abel has salary between 100 less and 100 more than Cambrault |
| Abel has salary between 100 less and 100 more than Raphaely |
| Ande has salary between 100 less and 100 more than Ande |
| Ande has salary between 100 less and 100 more than Mavris |
| Ande has salary between 100 less and 100 more than Vollman |
| Atkinson has salary between 100 less and 100 more than Atkinson |
| Atkinson has salary between 100 less and 100 more than Baida |
| Atkinson has salary between 100 less and 100 more than Gates |
| Atkinson has salary between 100 less and 100 more than Geoni |

Expand

Show lessSee more

##### Snowflake

Copy code

```
SELECT
                NVL(  e1.last_name :: STRING, '') ||
                ' has salary between 100 less and 100 more than ' || NVL(
                e2.last_name :: STRING, '') AS "SALARY COMPARISON"
FROM
                employees e1,
                employees e2
WHERE   e1.salary
BETWEEN
        !!!RESOLVE EWI!!! /*** SSC-EWI-OR0036 - TYPES RESOLUTION ISSUES, ARITHMETIC OPERATION '-' MAY NOT BEHAVE CORRECTLY BETWEEN unknown AND Number ***/!!! e2.salary - 100
AND
        !!!RESOLVE EWI!!! /*** SSC-EWI-OR0036 - TYPES RESOLUTION ISSUES, ARITHMETIC OPERATION '+' MAY NOT BEHAVE CORRECTLY BETWEEN unknown AND Number ***/!!!     e2.salary + 100
ORDER BY "SALARY COMPARISON"
FETCH FIRST 10 ROWS ONLY;
```

##### Result

| SALARY COMPARISON |
| --- |
| Abel has salary between 100 less and 100 more than Abel |
| Abel has salary between 100 less and 100 more than Cambrault |
| Abel has salary between 100 less and 100 more than Raphaely |
| Ande has salary between 100 less and 100 more than Ande |
| Ande has salary between 100 less and 100 more than Mavris |
| Ande has salary between 100 less and 100 more than Vollman |
| Atkinson has salary between 100 less and 100 more than Atkinson |
| Atkinson has salary between 100 less and 100 more than Baida |
| Atkinson has salary between 100 less and 100 more than Gates |
| Atkinson has salary between 100 less and 100 more than Geoni |

Expand

Show lessSee more

Warning

Migrating some `SELECT` statements without the corresponding tables could generate the [SSC-EWI-OR0036](../../../issues-and-troubleshooting/conversion-issues/oracleEWI#ssc-ewi-or0036): Types resolution issues. To avoid this warning, include the `CREATE TABLE` inside the file.

The results are the same making the BAND JOIN functional equivalent.

#### Execution plan

As extra information, the special thing about the band joins is the execution plan.

The following image shows the [enhanced execution plan](https://docs.oracle.com/en/database/oracle/oracle-database/21/tgsql/joins.html#GUID-24F34188-110F-4245-9DE7-43954092AFE0) (implemented since Oracle 12c) for the test query:

[![](/static/images/migrations/sc-assets/image(125)(1).png)](/static/images/migrations/sc-assets/image(125)(1).png)

And in the following image, we will see the execution plan in Snowflake:

[![](/static/images/migrations/sc-assets/image(67)(1).png)](/static/images/migrations/sc-assets/image(67)(1).png)

Note

The execution plan in Snowflake is very similar to Oracle’s optimized version. The final duration and performance of the query will be affected by many other factors and are completely dependent on each DBMS internal functionality.

### Known Issues

#### 1. Results ordering mismatch between languages

The query result will have the same content in both database engines but the order might be different if no *Order By* clause is defined in the query.

### Related EWIs

- [SSC-EWI-OR0036](../../../issues-and-troubleshooting/conversion-issues/oracleEWI#ssc-ewi-or0036)[:](../../../issues-and-troubleshooting/conversion-issues/oracleEWI#ssc-ewi-or0036) Types resolution issues, the arithmetic operation may not behave correctly between string and date.

## Cartesian Products

Note

Some parts in the output code are omitted for clarity reasons.

> If two tables in a join query have no join condition, then Oracle Database returns their Cartesian product. Oracle combines each row of one table with each row of the other. ([Oracle SQL Reference Cartesian Products Subsection](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/Joins.html#GUID-70DD48FA-BF46-4479-9C3F-146C5616E440))

Oracle and Snowflake are also compatible with the ANSI Cross Join syntax that has the same behavior of a cartesian product.

No special transformation is performed for this kind of *Join* since Snowflake supports the same syntax.

### Sample Source Patterns

Note

*Order by clause* was added because the result order may vary between Oracle and Snowflake.

Note

Since the result set is too large, *Row Limiting Clause* was added. You can remove it to retrieve the entire result set.

Note

Check this [section](../sample-data) to set up the sample database.

#### Implicit Syntax

##### Oracle

Copy code

```
-- Resulting rows
SELECT * FROM hr.employees, hr.departments
ORDER BY first_name
FETCH FIRST 5 ROWS ONLY;

-- Resulting total rows
SELECT COUNT(*) FROM hr.employees, hr.departments;
```

##### Result 1

| EMPLOYEE\_ID | FIRST\_NAME | LAST\_NAME | EMAIL | PHONE\_NUMBER | HIRE\_DATE | JOB\_ID | SALARY | COMMISSION\_PCT | MANAGER\_ID | DEPARTMENT\_ID | DEPARTMENT\_ID | DEPARTMENT\_NAME | MANAGER\_ID | LOCATION\_ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 121 | Adam | Fripp | AFRIPP | 650.123.2234 | 2005-04-10 00:00:00.000 | ST\_MAN | 8200 |  | 100 | 50 | 10 | Administration | 200 | 1700 |
| 121 | Adam | Fripp | AFRIPP | 650.123.2234 | 2005-04-10 00:00:00.000 | ST\_MAN | 8200 |  | 100 | 50 | 50 | Shipping | 121 | 1500 |
| 121 | Adam | Fripp | AFRIPP | 650.123.2234 | 2005-04-10 00:00:00.000 | ST\_MAN | 8200 |  | 100 | 50 | 40 | Human Resources | 203 | 2400 |
| 121 | Adam | Fripp | AFRIPP | 650.123.2234 | 2005-04-10 00:00:00.000 | ST\_MAN | 8200 |  | 100 | 50 | 30 | Purchasing | 114 | 1700 |
| 121 | Adam | Fripp | AFRIPP | 650.123.2234 | 2005-04-10 00:00:00.000 | ST\_MAN | 8200 |  | 100 | 50 | 20 | Marketing | 201 | 1800 |

Expand

Show lessSee more

##### Result 2

| COUNT(\*) |
| --- |
| 2889 |

Expand

Show lessSee more

##### Snowflake

Copy code

```
-- Resulting rows
SELECT * FROM
hr.employees,
hr.departments
ORDER BY first_name
FETCH FIRST 5 ROWS ONLY;

-- Resulting total rows
SELECT COUNT(*) FROM
hr.employees,
hr.departments;
```

##### Result 1

| EMPLOYEE\_ID | FIRST\_NAME | LAST\_NAME | EMAIL | PHONE\_NUMBER | HIRE\_DATE | JOB\_ID | SALARY | COMMISSION\_PCT | MANAGER\_ID | DEPARTMENT\_ID | DEPARTMENT\_ID | DEPARTMENT\_NAME | MANAGER\_ID | LOCATION\_ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 121 | Adam | Fripp | AFRIPP | 650.123.2234 | 2005-04-10 | ST\_MAN | 8200.00 |  | 100 | 50 | 40 | Human Resources | 203 | 2400 |
| 121 | Adam | Fripp | AFRIPP | 650.123.2234 | 2005-04-10 | ST\_MAN | 8200.00 |  | 100 | 50 | 20 | Marketing | 201 | 1800 |
| 121 | Adam | Fripp | AFRIPP | 650.123.2234 | 2005-04-10 | ST\_MAN | 8200.00 |  | 100 | 50 | 10 | Administration | 200 | 1700 |
| 121 | Adam | Fripp | AFRIPP | 650.123.2234 | 2005-04-10 | ST\_MAN | 8200.00 |  | 100 | 50 | 50 | Shipping | 121 | 1500 |
| 121 | Adam | Fripp | AFRIPP | 650.123.2234 | 2005-04-10 | ST\_MAN | 8200.00 |  | 100 | 50 | 30 | Purchasing | 114 | 1700 |

Expand

Show lessSee more

##### Result 2

| COUNT(\*) |
| --- |
| 2889 |

Expand

Show lessSee more

#### Cross Join Syntax

##### Oracle

Copy code

```
-- Resulting rows
SELECT * FROM hr.employees CROSS join hr.departments
ORDER BY first_name
FETCH FIRST 5 ROWS ONLY;

-- Resulting total rows
SELECT COUNT(*) FROM hr.employees CROSS join hr.departments;
```

##### Result 1

| EMPLOYEE\_ID | FIRST\_NAME | LAST\_NAME | EMAIL | PHONE\_NUMBER | HIRE\_DATE | JOB\_ID | SALARY | COMMISSION\_PCT | MANAGER\_ID | DEPARTMENT\_ID | DEPARTMENT\_ID | DEPARTMENT\_NAME | MANAGER\_ID | LOCATION\_ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 121 | Adam | Fripp | AFRIPP | 650.123.2234 | 2005-04-10 00:00:00.000 | ST\_MAN | 8200 |  | 100 | 50 | 10 | Administration | 200 | 1700 |
| 121 | Adam | Fripp | AFRIPP | 650.123.2234 | 2005-04-10 00:00:00.000 | ST\_MAN | 8200 |  | 100 | 50 | 50 | Shipping | 121 | 1500 |
| 121 | Adam | Fripp | AFRIPP | 650.123.2234 | 2005-04-10 00:00:00.000 | ST\_MAN | 8200 |  | 100 | 50 | 40 | Human Resources | 203 | 2400 |
| 121 | Adam | Fripp | AFRIPP | 650.123.2234 | 2005-04-10 00:00:00.000 | ST\_MAN | 8200 |  | 100 | 50 | 30 | Purchasing | 114 | 1700 |
| 121 | Adam | Fripp | AFRIPP | 650.123.2234 | 2005-04-10 00:00:00.000 | ST\_MAN | 8200 |  | 100 | 50 | 20 | Marketing | 201 | 1800 |

Expand

Show lessSee more

##### Result 2

| COUNT(\*) |
| --- |
| 2889 |

Expand

Show lessSee more

##### Snowflake

Copy code

```
:force:
-- Resulting rows
SELECT * FROM
hr.employees
CROSS join hr.departments
ORDER BY first_name
FETCH FIRST 5 ROWS ONLY;

-- Resulting total rows
SELECT COUNT(*) FROM
hr.employees
CROSS join hr.departments;
```

### Known issues

#### 1. Results ordering mismatch between languages

The result of the query will have the same content in both database engines but the order might be different if no *Order By* clause is defined in the query.

### Related EWIs

No related EWIs.

## Equijoin

Note

Some parts in the output code are omitted for clarity reasons.

### Description

An equijoin is an implicit form of the join with a join condition containing an equality operator. For more information, see the [Oracle Equijoin documentation](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/Joins.html#GUID-3AA5EB23-2D84-4E19-BD7E-E66A3C59D888).

No special transformation is performed for this kind of *Join* since Snowflake supports the same syntax.

### Sample Source Patterns

Note

*Order by clause* added because the result order may vary between Oracle and Snowflake.

Note

Since the result set is too large, the *Row Limiting Clause* was added. You can remove it to retrieve the entire result set.

Note

Check this [section](../sample-data) to set up the sample database.

#### Basic Equijoin case

##### Oracle

Copy code

```
 SELECT last_name, job_id, hr.departments.department_id, department_name
FROM hr.employees, hr.departments
WHERE hr.employees.department_id = hr.departments.department_id
ORDER BY last_name
FETCH FIRST 5 ROWS ONLY;
```

##### Result

| LAST\_NAME | JOB\_ID | DEPARTMENT\_ID | DEPARTMENT\_NAME |
| --- | --- | --- | --- |
| Abel | SA\_REP | 80 | Sales |
| Ande | SA\_REP | 80 | Sales |
| Atkinson | ST\_CLERK | 50 | Shipping |
| Austin | IT\_PROG | 60 | IT |
| Baer | PR\_REP | 70 | Public Relations |

Expand

Show lessSee more

##### Snowflake

Copy code

```
 SELECT last_name, job_id, hr.departments.department_id, department_name
FROM
hr.employees,
hr.departments
WHERE hr.employees.department_id = hr.departments.department_id
ORDER BY last_name
FETCH FIRST 5 ROWS ONLY;
```

##### Result

| LAST\_NAME | JOB\_ID | DEPARTMENT\_ID | DEPARTMENT\_NAME |
| --- | --- | --- | --- |
| Abel | SA\_REP | 80 | Sales |
| Ande | SA\_REP | 80 | Sales |
| Atkinson | ST\_CLERK | 50 | Shipping |
| Austin | IT\_PROG | 60 | IT |
| Baer | PR\_REP | 70 | Public Relations |

Expand

Show lessSee more

### Known issues

#### 1. Results ordering mismatch between languages

The result of the query will have the same content in both database engines but the order might be different if no *Order By* clause is defined in the query.

### Related EWIs

No related EWIs.

## Inner Join

Note

Some parts in the output code are omitted for clarity reasons.

### Description

> An inner join (sometimes called a simple join) is a join of two or more tables that returns only those rows that satisfy the join condition. ([Oracle SQL Reference Inner Join Subsection](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/Joins.html#GUID-794F7DD5-FB18-4ADC-9E46-ADDA8C30C3C6)).

Copy code

```
{ [ INNER ] JOIN table_reference
 { ON condition
 | USING (column [, column ]...)
 }
| { CROSS
 | NATURAL [ INNER ]
 }
 JOIN table_reference
}
```

### Sample Source Patterns

Note

*Order by* clause added because the result order may vary between Oracle and Snowflake.

Note

Since the result set is too large, *Row Limiting Clause* was added. You can remove this clause to retrieve the entire result set.

Note

Check this [section](../sample-data) to set up the sample database.

#### Basic Inner Join

In the Inner Join clause “INNER” is an optional keyword, the following queries have two selects that retrieve the same data set.

##### Oracle

Copy code

```
 SELECT
    *
FROM
    hr.employees
INNER JOIN hr.departments ON
    hr.departments.department_id = hr.employees.department_id
ORDER BY employee_id
FETCH NEXT 10 ROWS ONLY;

SELECT
    *
FROM
    hr.employees
JOIN hr.departments ON
    hr.departments.department_id = hr.employees.department_id
ORDER BY employee_id
FETCH NEXT 10 ROWS ONLY;
```

##### Result

| EMPLOYEE\_ID | FIRST\_NAME | LAST\_NAME | EMAIL | PHONE\_NUMBER | HIRE\_DATE | JOB\_ID | SALARY | COMMISSION\_PCT | MANAGER\_ID | DEPARTMENT\_ID | DEPARTMENT\_ID | DEPARTMENT\_NAME | MANAGER\_ID | LOCATION\_ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 100 | Steven | King | SKING | 515.123.4567 | 2003-06-17 00:00:00.000 | AD\_PRES | 24000 |  |  | 90 | 90 | Executive | 100 | 1700 |
| 101 | Neena | Kochhar | NKOCHHAR | 515.123.4568 | 2005-09-21 00:00:00.000 | AD\_VP | 17000 |  | 100 | 90 | 90 | Executive | 100 | 1700 |
| 102 | Lex | De Haan | LDEHAAN | 515.123.4569 | 2001-01-13 00:00:00.000 | AD\_VP | 17000 |  | 100 | 90 | 90 | Executive | 100 | 1700 |
| 103 | Alexander | Hunold | AHUNOLD | 590.423.4567 | 2006-01-03 00:00:00.000 | IT\_PROG | 9000 |  | 102 | 60 | 60 | IT | 103 | 1400 |
| 104 | Bruce | Ernst | BERNST | 590.423.4568 | 2007-05-21 00:00:00.000 | IT\_PROG | 6000 |  | 103 | 60 | 60 | IT | 103 | 1400 |
| 105 | David | Austin | DAUSTIN | 590.423.4569 | 2005-06-25 00:00:00.000 | IT\_PROG | 4800 |  | 103 | 60 | 60 | IT | 103 | 1400 |
| 106 | Valli | Pataballa | VPATABAL | 590.423.4560 | 2006-02-05 00:00:00.000 | IT\_PROG | 4800 |  | 103 | 60 | 60 | IT | 103 | 1400 |
| 107 | Diana | Lorentz | DLORENTZ | 590.423.5567 | 2007-02-07 00:00:00.000 | IT\_PROG | 4200 |  | 103 | 60 | 60 | IT | 103 | 1400 |
| 108 | Nancy | Greenberg | NGREENBE | 515.124.4569 | 2002-08-17 00:00:00.000 | FI\_MGR | 12008 |  | 101 | 100 | 100 | Finance | 108 | 1700 |
| 109 | Daniel | Faviet | DFAVIET | 515.124.4169 | 2002-08-16 00:00:00.000 | FI\_ACCOUNT | 9000 |  | 108 | 100 | 100 | Finance | 108 | 1700 |

Expand

Show lessSee more

##### Snowflake

Copy code

```
 SELECT
    *
FROM
hr.employees
INNER JOIN
    hr.departments
    ON
    hr.departments.department_id = hr.employees.department_id
ORDER BY employee_id
FETCH NEXT 10 ROWS ONLY;

SELECT
    *
FROM
    hr.employees
JOIN
    hr.departments
    ON
    hr.departments.department_id = hr.employees.department_id
ORDER BY employee_id
FETCH NEXT 10 ROWS ONLY;
```

##### Result

| EMPLOYEE\_ID | FIRST\_NAME | LAST\_NAME | EMAIL | PHONE\_NUMBER | HIRE\_DATE | JOB\_ID | SALARY | COMMISSION\_PCT | MANAGER\_ID | DEPARTMENT\_ID | DEPARTMENT\_ID | DEPARTMENT\_NAME | MANAGER\_ID | LOCATION\_ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 100 | Steven | King | SKING | 515.123.4567 | 2003-06-17 | AD\_PRES | 24000.00 |  |  | 90 | 90 | Executive | 100 | 1700 |
| 101 | Neena | Kochhar | NKOCHHAR | 515.123.4568 | 2005-09-21 | AD\_VP | 17000.00 |  | 100 | 90 | 90 | Executive | 100 | 1700 |
| 102 | Lex | De Haan | LDEHAAN | 515.123.4569 | 2001-01-13 | AD\_VP | 17000.00 |  | 100 | 90 | 90 | Executive | 100 | 1700 |
| 103 | Alexander | Hunold | AHUNOLD | 590.423.4567 | 2006-01-03 | IT\_PROG | 9000.00 |  | 102 | 60 | 60 | IT | 103 | 1400 |
| 104 | Bruce | Ernst | BERNST | 590.423.4568 | 2007-05-21 | IT\_PROG | 6000.00 |  | 103 | 60 | 60 | IT | 103 | 1400 |
| 105 | David | Austin | DAUSTIN | 590.423.4569 | 2005-06-25 | IT\_PROG | 4800.00 |  | 103 | 60 | 60 | IT | 103 | 1400 |
| 106 | Valli | Pataballa | VPATABAL | 590.423.4560 | 2006-02-05 | IT\_PROG | 4800.00 |  | 103 | 60 | 60 | IT | 103 | 1400 |
| 107 | Diana | Lorentz | DLORENTZ | 590.423.5567 | 2007-02-07 | IT\_PROG | 4200.00 |  | 103 | 60 | 60 | IT | 103 | 1400 |
| 108 | Nancy | Greenberg | NGREENBE | 515.124.4569 | 2002-08-17 | FI\_MGR | 12008.00 |  | 101 | 100 | 100 | Finance | 108 | 1700 |
| 109 | Daniel | Faviet | DFAVIET | 515.124.4169 | 2002-08-16 | FI\_ACCOUNT | 9000.00 |  | 108 | 100 | 100 | Finance | 108 | 1700 |

Expand

Show lessSee more

#### Inner Join with using clause

##### Oracle

Copy code

```
SELECT
    *
FROM
    hr.employees
INNER JOIN hr.departments
    USING(department_id)
ORDER BY employee_id
FETCH NEXT 10 ROWS ONLY;
```

##### Result

| DEPARTMENT\_ID | EMPLOYEE\_ID | FIRST\_NAME | LAST\_NAME | EMAIL | PHONE\_NUMBER | HIRE\_DATE | JOB\_ID | SALARY | COMMISSION\_PCT | MANAGER\_ID | DEPARTMENT\_NAME | MANAGER\_ID | LOCATION\_ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 90 | 100 | Steven | King | SKING | 515.123.4567 | 2003-06-17 00:00:00.000 | AD\_PRES | 24000 |  |  | Executive | 100 | 1700 |
| 90 | 101 | Neena | Kochhar | NKOCHHAR | 515.123.4568 | 2005-09-21 00:00:00.000 | AD\_VP | 17000 |  | 100 | Executive | 100 | 1700 |
| 90 | 102 | Lex | De Haan | LDEHAAN | 515.123.4569 | 2001-01-13 00:00:00.000 | AD\_VP | 17000 |  | 100 | Executive | 100 | 1700 |
| 60 | 103 | Alexander | Hunold | AHUNOLD | 590.423.4567 | 2006-01-03 00:00:00.000 | IT\_PROG | 9000 |  | 102 | IT | 103 | 1400 |
| 60 | 104 | Bruce | Ernst | BERNST | 590.423.4568 | 2007-05-21 00:00:00.000 | IT\_PROG | 6000 |  | 103 | IT | 103 | 1400 |
| 60 | 105 | David | Austin | DAUSTIN | 590.423.4569 | 2005-06-25 00:00:00.000 | IT\_PROG | 4800 |  | 103 | IT | 103 | 1400 |
| 60 | 106 | Valli | Pataballa | VPATABAL | 590.423.4560 | 2006-02-05 00:00:00.000 | IT\_PROG | 4800 |  | 103 | IT | 103 | 1400 |
| 60 | 107 | Diana | Lorentz | DLORENTZ | 590.423.5567 | 2007-02-07 00:00:00.000 | IT\_PROG | 4200 |  | 103 | IT | 103 | 1400 |
| 100 | 108 | Nancy | Greenberg | NGREENBE | 515.124.4569 | 2002-08-17 00:00:00.000 | FI\_MGR | 12008 |  | 101 | Finance | 108 | 1700 |
| 100 | 109 | Daniel | Faviet | DFAVIET | 515.124.4169 | 2002-08-16 00:00:00.000 | FI\_ACCOUNT | 9000 |  | 108 | Finance | 108 | 1700 |

Expand

Show lessSee more

##### Snowflake

Copy code

```
SELECT
    *
FROM
hr.employees
INNER JOIN
    hr.departments
    USING(department_id)
ORDER BY employee_id
FETCH NEXT 10 ROWS ONLY;
```

##### Result

| DEPARTMENT\_ID | EMPLOYEE\_ID | FIRST\_NAME | LAST\_NAME | EMAIL | PHONE\_NUMBER | HIRE\_DATE | JOB\_ID | SALARY | COMMISSION\_PCT | MANAGER\_ID | DEPARTMENT\_NAME | MANAGER\_ID | LOCATION\_ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 90 | 100 | Steven | King | SKING | 515.123.4567 | 2003-06-17 | AD\_PRES | 24000.00 |  |  | Executive | 100 | 1700 |
| 90 | 101 | Neena | Kochhar | NKOCHHAR | 515.123.4568 | 2005-09-21 | AD\_VP | 17000.00 |  | 100 | Executive | 100 | 1700 |
| 90 | 102 | Lex | De Haan | LDEHAAN | 515.123.4569 | 2001-01-13 | AD\_VP | 17000.00 |  | 100 | Executive | 100 | 1700 |
| 60 | 103 | Alexander | Hunold | AHUNOLD | 590.423.4567 | 2006-01-03 | IT\_PROG | 9000.00 |  | 102 | IT | 103 | 1400 |
| 60 | 104 | Bruce | Ernst | BERNST | 590.423.4568 | 2007-05-21 | IT\_PROG | 6000.00 |  | 103 | IT | 103 | 1400 |
| 60 | 105 | David | Austin | DAUSTIN | 590.423.4569 | 2005-06-25 | IT\_PROG | 4800.00 |  | 103 | IT | 103 | 1400 |
| 60 | 106 | Valli | Pataballa | VPATABAL | 590.423.4560 | 2006-02-05 | IT\_PROG | 4800.00 |  | 103 | IT | 103 | 1400 |
| 60 | 107 | Diana | Lorentz | DLORENTZ | 590.423.5567 | 2007-02-07 | IT\_PROG | 4200.00 |  | 103 | IT | 103 | 1400 |
| 100 | 108 | Nancy | Greenberg | NGREENBE | 515.124.4569 | 2002-08-17 | FI\_MGR | 12008.00 |  | 101 | Finance | 108 | 1700 |
| 100 | 109 | Daniel | Faviet | DFAVIET | 515.124.4169 | 2002-08-16 | FI\_ACCOUNT | 9000.00 |  | 108 | Finance | 108 | 1700 |

Expand

Show lessSee more

#### Cross Inner Join

##### Oracle

Copy code

```
SELECT
    *
FROM
    hr.employees
CROSS JOIN hr.departments
ORDER BY department_name, employee_id
FETCH NEXT 10 ROWS ONLY;
```

##### Result

| EMPLOYEE\_ID | FIRST\_NAME | LAST\_NAME | EMAIL | PHONE\_NUMBER | HIRE\_DATE | JOB\_ID | SALARY | COMMISSION\_PCT | MANAGER\_ID | DEPARTMENT\_ID | DEPARTMENT\_ID | DEPARTMENT\_NAME | MANAGER\_ID | LOCATION\_ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 100 | Steven | King | SKING | 515.123.4567 | 2003-06-17 00:00:00.000 | AD\_PRES | 24000 |  |  | 90 | 110 | Accounting | 205 | 1700 |
| 101 | Neena | Kochhar | NKOCHHAR | 515.123.4568 | 2005-09-21 00:00:00.000 | AD\_VP | 17000 |  | 100 | 90 | 110 | Accounting | 205 | 1700 |
| 102 | Lex | De Haan | LDEHAAN | 515.123.4569 | 2001-01-13 00:00:00.000 | AD\_VP | 17000 |  | 100 | 90 | 110 | Accounting | 205 | 1700 |
| 103 | Alexander | Hunold | AHUNOLD | 590.423.4567 | 2006-01-03 00:00:00.000 | IT\_PROG | 9000 |  | 102 | 60 | 110 | Accounting | 205 | 1700 |
| 104 | Bruce | Ernst | BERNST | 590.423.4568 | 2007-05-21 00:00:00.000 | IT\_PROG | 6000 |  | 103 | 60 | 110 | Accounting | 205 | 1700 |
| 105 | David | Austin | DAUSTIN | 590.423.4569 | 2005-06-25 00:00:00.000 | IT\_PROG | 4800 |  | 103 | 60 | 110 | Accounting | 205 | 1700 |
| 106 | Valli | Pataballa | VPATABAL | 590.423.4560 | 2006-02-05 00:00:00.000 | IT\_PROG | 4800 |  | 103 | 60 | 110 | Accounting | 205 | 1700 |
| 107 | Diana | Lorentz | DLORENTZ | 590.423.5567 | 2007-02-07 00:00:00.000 | IT\_PROG | 4200 |  | 103 | 60 | 110 | Accounting | 205 | 1700 |
| 108 | Nancy | Greenberg | NGREENBE | 515.124.4569 | 2002-08-17 00:00:00.000 | FI\_MGR | 12008 |  | 101 | 100 | 110 | Accounting | 205 | 1700 |
| 109 | Daniel | Faviet | DFAVIET | 515.124.4169 | 2002-08-16 00:00:00.000 | FI\_ACCOUNT | 9000 |  | 108 | 100 | 110 | Accounting | 205 | 1700 |

Expand

Show lessSee more

##### Snowflake

Copy code

```
 SELECT
    *
FROM
hr.employees
CROSS JOIN hr.departments
ORDER BY department_name, employee_id
FETCH NEXT 10 ROWS ONLY;
```

##### Result

| EMPLOYEE\_ID | FIRST\_NAME | LAST\_NAME | EMAIL | PHONE\_NUMBER | HIRE\_DATE | JOB\_ID | SALARY | COMMISSION\_PCT | MANAGER\_ID | DEPARTMENT\_ID | DEPARTMENT\_ID | DEPARTMENT\_NAME | MANAGER\_ID | LOCATION\_ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 100 | Steven | King | SKING | 515.123.4567 | 2003-06-17 | AD\_PRES | 24000.00 |  |  | 90 | 110 | Accounting | 205 | 1700 |
| 101 | Neena | Kochhar | NKOCHHAR | 515.123.4568 | 2005-09-21 | AD\_VP | 17000.00 |  | 100 | 90 | 110 | Accounting | 205 | 1700 |
| 102 | Lex | De Haan | LDEHAAN | 515.123.4569 | 2001-01-13 | AD\_VP | 17000.00 |  | 100 | 90 | 110 | Accounting | 205 | 1700 |
| 103 | Alexander | Hunold | AHUNOLD | 590.423.4567 | 2006-01-03 | IT\_PROG | 9000.00 |  | 102 | 60 | 110 | Accounting | 205 | 1700 |
| 104 | Bruce | Ernst | BERNST | 590.423.4568 | 2007-05-21 | IT\_PROG | 6000.00 |  | 103 | 60 | 110 | Accounting | 205 | 1700 |
| 105 | David | Austin | DAUSTIN | 590.423.4569 | 2005-06-25 | IT\_PROG | 4800.00 |  | 103 | 60 | 110 | Accounting | 205 | 1700 |
| 106 | Valli | Pataballa | VPATABAL | 590.423.4560 | 2006-02-05 | IT\_PROG | 4800.00 |  | 103 | 60 | 110 | Accounting | 205 | 1700 |
| 107 | Diana | Lorentz | DLORENTZ | 590.423.5567 | 2007-02-07 | IT\_PROG | 4200.00 |  | 103 | 60 | 110 | Accounting | 205 | 1700 |
| 108 | Nancy | Greenberg | NGREENBE | 515.124.4569 | 2002-08-17 | FI\_MGR | 12008.00 |  | 101 | 100 | 110 | Accounting | 205 | 1700 |
| 109 | Daniel | Faviet | DFAVIET | 515.124.4169 | 2002-08-16 | FI\_ACCOUNT | 9000.00 |  | 108 | 100 | 110 | Accounting | 205 | 1700 |

Expand

Show lessSee more

#### Natural Inner Join

##### Oracle

Copy code

```
SELECT
    *
FROM
    hr.employees
NATURAL JOIN hr.departments
ORDER BY employee_id
FETCH NEXT 10 ROWS ONLY;
```

##### Result

| MANAGER\_ID | DEPARTMENT\_ID | EMPLOYEE\_ID | FIRST\_NAME | LAST\_NAME | EMAIL | PHONE\_NUMBER | HIRE\_DATE | JOB\_ID | SALARY | COMMISSION\_PCT | DEPARTMENT\_NAME | LOCATION\_ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 100 | 90 | 101 | Neena | Kochhar | NKOCHHAR | 515.123.4568 | 2005-09-21 00:00:00.000 | AD\_VP | 17000 |  | Executive | 1700 |
| 100 | 90 | 102 | Lex | De Haan | LDEHAAN | 515.123.4569 | 2001-01-13 00:00:00.000 | AD\_VP | 17000 |  | Executive | 1700 |
| 103 | 60 | 104 | Bruce | Ernst | BERNST | 590.423.4568 | 2007-05-21 00:00:00.000 | IT\_PROG | 6000 |  | IT | 1400 |
| 103 | 60 | 105 | David | Austin | DAUSTIN | 590.423.4569 | 2005-06-25 00:00:00.000 | IT\_PROG | 4800 |  | IT | 1400 |
| 103 | 60 | 106 | Valli | Pataballa | VPATABAL | 590.423.4560 | 2006-02-05 00:00:00.000 | IT\_PROG | 4800 |  | IT | 1400 |
| 103 | 60 | 107 | Diana | Lorentz | DLORENTZ | 590.423.5567 | 2007-02-07 00:00:00.000 | IT\_PROG | 4200 |  | IT | 1400 |
| 108 | 100 | 109 | Daniel | Faviet | DFAVIET | 515.124.4169 | 2002-08-16 00:00:00.000 | FI\_ACCOUNT | 9000 |  | Finance | 1700 |
| 108 | 100 | 110 | John | Chen | JCHEN | 515.124.4269 | 2005-09-28 00:00:00.000 | FI\_ACCOUNT | 8200 |  | Finance | 1700 |
| 108 | 100 | 111 | Ismael | Sciarra | ISCIARRA | 515.124.4369 | 2005-09-30 00:00:00.000 | FI\_ACCOUNT | 7700 |  | Finance | 1700 |
| 108 | 100 | 112 | Jose Manuel | Urman | JMURMAN | 515.124.4469 | 2006-03-07 00:00:00.000 | FI\_ACCOUNT | 7800 |  | Finance | 1700 |

Expand

Show lessSee more

##### Snowflake

Copy code

```
SELECT
    *
FROM
hr.employees
NATURAL JOIN
    hr.departments
ORDER BY employee_id
FETCH NEXT 10 ROWS ONLY;
```

##### Result

| MANAGER\_ID | DEPARTMENT\_ID | EMPLOYEE\_ID | FIRST\_NAME | LAST\_NAME | EMAIL | PHONE\_NUMBER | HIRE\_DATE | JOB\_ID | SALARY | COMMISSION\_PCT | DEPARTMENT\_NAME | LOCATION\_ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 100 | 90 | 101 | Neena | Kochhar | NKOCHHAR | 515.123.4568 | 2005-09-21 | AD\_VP | 17000.00 |  | Executive | 1700 |
| 100 | 90 | 102 | Lex | De Haan | LDEHAAN | 515.123.4569 | 2001-01-13 | AD\_VP | 17000.00 |  | Executive | 1700 |
| 103 | 60 | 104 | Bruce | Ernst | BERNST | 590.423.4568 | 2007-05-21 | IT\_PROG | 6000.00 |  | IT | 1400 |
| 103 | 60 | 105 | David | Austin | DAUSTIN | 590.423.4569 | 2005-06-25 | IT\_PROG | 4800.00 |  | IT | 1400 |
| 103 | 60 | 106 | Valli | Pataballa | VPATABAL | 590.423.4560 | 2006-02-05 | IT\_PROG | 4800.00 |  | IT | 1400 |
| 103 | 60 | 107 | Diana | Lorentz | DLORENTZ | 590.423.5567 | 2007-02-07 | IT\_PROG | 4200.00 |  | IT | 1400 |
| 108 | 100 | 109 | Daniel | Faviet | DFAVIET | 515.124.4169 | 2002-08-16 | FI\_ACCOUNT | 9000.00 |  | Finance | 1700 |
| 108 | 100 | 110 | John | Chen | JCHEN | 515.124.4269 | 2005-09-28 | FI\_ACCOUNT | 8200.00 |  | Finance | 1700 |
| 108 | 100 | 111 | Ismael | Sciarra | ISCIARRA | 515.124.4369 | 2005-09-30 | FI\_ACCOUNT | 7700.00 |  | Finance | 1700 |
| 108 | 100 | 112 | Jose Manuel | Urman | JMURMAN | 515.124.4469 | 2006-03-07 | FI\_ACCOUNT | 7800.00 |  | Finance | 1700 |

Expand

Show lessSee more

#### Cross Natural Join

##### Oracle

Copy code

```
SELECT
    *
FROM
    hr.employees
CROSS NATURAL JOIN hr.departments
ORDER BY employee_id
FETCH NEXT 10 ROWS ONLY;
```

##### Result

| MANAGER\_ID | DEPARTMENT\_ID | EMPLOYEE\_ID | FIRST\_NAME | LAST\_NAME | EMAIL | PHONE\_NUMBER | HIRE\_DATE | JOB\_ID | SALARY | COMMISSION\_PCT | DEPARTMENT\_NAME | LOCATION\_ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 100 | 90 | 101 | Neena | Kochhar | NKOCHHAR | 515.123.4568 | 2005-09-21 00:00:00.000 | AD\_VP | 17000 |  | Executive | 1700 |
| 100 | 90 | 102 | Lex | De Haan | LDEHAAN | 515.123.4569 | 2001-01-13 00:00:00.000 | AD\_VP | 17000 |  | Executive | 1700 |
| 103 | 60 | 104 | Bruce | Ernst | BERNST | 590.423.4568 | 2007-05-21 00:00:00.000 | IT\_PROG | 6000 |  | IT | 1400 |
| 103 | 60 | 105 | David | Austin | DAUSTIN | 590.423.4569 | 2005-06-25 00:00:00.000 | IT\_PROG | 4800 |  | IT | 1400 |
| 103 | 60 | 106 | Valli | Pataballa | VPATABAL | 590.423.4560 | 2006-02-05 00:00:00.000 | IT\_PROG | 4800 |  | IT | 1400 |
| 103 | 60 | 107 | Diana | Lorentz | DLORENTZ | 590.423.5567 | 2007-02-07 00:00:00.000 | IT\_PROG | 4200 |  | IT | 1400 |
| 108 | 100 | 109 | Daniel | Faviet | DFAVIET | 515.124.4169 | 2002-08-16 00:00:00.000 | FI\_ACCOUNT | 9000 |  | Finance | 1700 |
| 108 | 100 | 110 | John | Chen | JCHEN | 515.124.4269 | 2005-09-28 00:00:00.000 | FI\_ACCOUNT | 8200 |  | Finance | 1700 |
| 108 | 100 | 111 | Ismael | Sciarra | ISCIARRA | 515.124.4369 | 2005-09-30 00:00:00.000 | FI\_ACCOUNT | 7700 |  | Finance | 1700 |
| 108 | 100 | 112 | Jose Manuel | Urman | JMURMAN | 515.124.4469 | 2006-03-07 00:00:00.000 | FI\_ACCOUNT | 7800 |  | Finance | 1700 |

Expand

Show lessSee more

##### Snowflake

Copy code

```
SELECT
    *
FROM
    hr.employees
    NATURAL JOIN
        hr.departments
ORDER BY employee_id
FETCH NEXT 10 ROWS ONLY;
```

##### Result

| MANAGER\_ID | DEPARTMENT\_ID | EMPLOYEE\_ID | FIRST\_NAME | LAST\_NAME | EMAIL | PHONE\_NUMBER | HIRE\_DATE | JOB\_ID | SALARY | COMMISSION\_PCT | DEPARTMENT\_NAME | LOCATION\_ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 100 | 90 | 101 | Neena | Kochhar | NKOCHHAR | 515.123.4568 | 2005-09-21 | AD\_VP | 17000.00 |  | Executive | 1700 |
| 100 | 90 | 102 | Lex | De Haan | LDEHAAN | 515.123.4569 | 2001-01-13 | AD\_VP | 17000.00 |  | Executive | 1700 |
| 103 | 60 | 104 | Bruce | Ernst | BERNST | 590.423.4568 | 2007-05-21 | IT\_PROG | 6000.00 |  | IT | 1400 |
| 103 | 60 | 105 | David | Austin | DAUSTIN | 590.423.4569 | 2005-06-25 | IT\_PROG | 4800.00 |  | IT | 1400 |
| 103 | 60 | 106 | Valli | Pataballa | VPATABAL | 590.423.4560 | 2006-02-05 | IT\_PROG | 4800.00 |  | IT | 1400 |
| 103 | 60 | 107 | Diana | Lorentz | DLORENTZ | 590.423.5567 | 2007-02-07 | IT\_PROG | 4200.00 |  | IT | 1400 |
| 108 | 100 | 109 | Daniel | Faviet | DFAVIET | 515.124.4169 | 2002-08-16 | FI\_ACCOUNT | 9000.00 |  | Finance | 1700 |
| 108 | 100 | 110 | John | Chen | JCHEN | 515.124.4269 | 2005-09-28 | FI\_ACCOUNT | 8200.00 |  | Finance | 1700 |
| 108 | 100 | 111 | Ismael | Sciarra | ISCIARRA | 515.124.4369 | 2005-09-30 | FI\_ACCOUNT | 7700.00 |  | Finance | 1700 |
| 108 | 100 | 112 | Jose Manuel | Urman | JMURMAN | 515.124.4469 | 2006-03-07 | FI\_ACCOUNT | 7800.00 |  | Finance | 1700 |

Expand

Show lessSee more

#### Natural Cross Join

##### Oracle

Copy code

```
SELECT
    *
FROM
    hr.employees
NATURAL CROSS JOIN hr.departments
ORDER BY employee_id
FETCH NEXT 10 ROWS ONLY;
```

##### Result

| EMPLOYEE\_ID | FIRST\_NAME | LAST\_NAME | EMAIL | PHONE\_NUMBER | HIRE\_DATE | JOB\_ID | SALARY | COMMISSION\_PCT | MANAGER\_ID | DEPARTMENT\_ID | DEPARTMENT\_ID | DEPARTMENT\_NAME | MANAGER\_ID | LOCATION\_ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 100 | Steven | King | SKING | 515.123.4567 | 2003-06-17 00:00:00.000 | AD\_PRES | 24000 |  |  | 90 | 10 | Administration | 200 | 1700 |
| 100 | Steven | King | SKING | 515.123.4567 | 2003-06-17 00:00:00.000 | AD\_PRES | 24000 |  |  | 90 | 100 | Finance | 108 | 1700 |
| 100 | Steven | King | SKING | 515.123.4567 | 2003-06-17 00:00:00.000 | AD\_PRES | 24000 |  |  | 90 | 90 | Executive | 100 | 1700 |
| 100 | Steven | King | SKING | 515.123.4567 | 2003-06-17 00:00:00.000 | AD\_PRES | 24000 |  |  | 90 | 80 | Sales | 145 | 2500 |
| 100 | Steven | King | SKING | 515.123.4567 | 2003-06-17 00:00:00.000 | AD\_PRES | 24000 |  |  | 90 | 70 | Public Relations | 204 | 2700 |
| 100 | Steven | King | SKING | 515.123.4567 | 2003-06-17 00:00:00.000 | AD\_PRES | 24000 |  |  | 90 | 60 | IT | 103 | 1400 |
| 100 | Steven | King | SKING | 515.123.4567 | 2003-06-17 00:00:00.000 | AD\_PRES | 24000 |  |  | 90 | 50 | Shipping | 121 | 1500 |
| 100 | Steven | King | SKING | 515.123.4567 | 2003-06-17 00:00:00.000 | AD\_PRES | 24000 |  |  | 90 | 40 | Human Resources | 203 | 2400 |
| 100 | Steven | King | SKING | 515.123.4567 | 2003-06-17 00:00:00.000 | AD\_PRES | 24000 |  |  | 90 | 30 | Purchasing | 114 | 1700 |
| 100 | Steven | King | SKING | 515.123.4567 | 2003-06-17 00:00:00.000 | AD\_PRES | 24000 |  |  | 90 | 20 | Marketing | 201 | 1800 |

Expand

Show lessSee more

##### Snowflake

Copy code

```
SELECT
    *
FROM
    hr.employees
    CROSS JOIN hr.departments
ORDER BY employee_id
FETCH NEXT 10 ROWS ONLY;
```

##### Result

| EMPLOYEE\_ID | FIRST\_NAME | LAST\_NAME | EMAIL | PHONE\_NUMBER | HIRE\_DATE | JOB\_ID | SALARY | COMMISSION\_PCT | MANAGER\_ID | DEPARTMENT\_ID | DEPARTMENT\_ID | DEPARTMENT\_NAME | MANAGER\_ID | LOCATION\_ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 100 | Steven | King | SKING | 515.123.4567 | 2003-06-17 | AD\_PRES | 24000.00 |  |  | 90 | 80 | Sales | 145 | 2500 |
| 100 | Steven | King | SKING | 515.123.4567 | 2003-06-17 | AD\_PRES | 24000.00 |  |  | 90 | 20 | Marketing | 201 | 1800 |
| 100 | Steven | King | SKING | 515.123.4567 | 2003-06-17 | AD\_PRES | 24000.00 |  |  | 90 | 60 | IT | 103 | 1400 |
| 100 | Steven | King | SKING | 515.123.4567 | 2003-06-17 | AD\_PRES | 24000.00 |  |  | 90 | 70 | Public Relations | 204 | 2700 |
| 100 | Steven | King | SKING | 515.123.4567 | 2003-06-17 | AD\_PRES | 24000.00 |  |  | 90 | 90 | Executive | 100 | 1700 |
| 100 | Steven | King | SKING | 515.123.4567 | 2003-06-17 | AD\_PRES | 24000.00 |  |  | 90 | 30 | Purchasing | 114 | 1700 |
| 100 | Steven | King | SKING | 515.123.4567 | 2003-06-17 | AD\_PRES | 24000.00 |  |  | 90 | 10 | Administration | 200 | 1700 |
| 100 | Steven | King | SKING | 515.123.4567 | 2003-06-17 | AD\_PRES | 24000.00 |  |  | 90 | 100 | Finance | 108 | 1700 |
| 100 | Steven | King | SKING | 515.123.4567 | 2003-06-17 | AD\_PRES | 24000.00 |  |  | 90 | 50 | Shipping | 121 | 1500 |
| 100 | Steven | King | SKING | 515.123.4567 | 2003-06-17 | AD\_PRES | 24000.00 |  |  | 90 | 40 | Human Resources | 203 | 2400 |

Expand

Show lessSee more

### Known issues

#### 1. Results ordering mismatch between languages

The result of the query will have the same content in both database engines but the order might be different if no *Order By* clause is defined in the query.

### Related EWIs

No related EWIs.

## Outer Join

Note

Some parts in the output code are omitted for clarity reasons.

### Description

> An outer join extends the result of a simple join. An outer join returns all rows that satisfy the join condition and returns some or all those rows from one table for which no rows from the other satisfy the join condition. ([Oracle SQL Language Reference Outer Joins Subsection](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/Joins.html#GUID-29A4584C-0741-4E6A-A89B-DCFAA222994A)).

#### Oracle ANSI syntax

Copy code

```
[ query_partition_clause ] [ NATURAL ]
outer_join_type JOIN table_reference
 [ query_partition_clause ]
 [ ON condition
 | USING ( column [, column ]...)
 ]
```

Copy code

```
outer_join_type
{ FULL | LEFT | RIGHT } [ OUTER ]
```

Oracle also supports the (+) operator that can be used to do outer joins. This operator is added to a column expression in the WHERE clause.

Copy code

```
column_expression (+)
```

#### Snowflake ANSI syntax

Snowflake also supports the ANSI syntax for OUTER JOINS, just like Oracle. However, the behavior when using the (+) operator might be different depending on the usage. For more information, see the [Snowflake JOIN documentation](https://docs.snowflake.com/en/sql-reference/constructs/join.html).

The Snowflake grammar is one of the following:

Copy code

```
SELECT ...
FROM <object_ref1> [
                     {
                       INNER
                       | { LEFT | RIGHT | FULL } [ OUTER ]
                     }
                   ]
                   JOIN <object_ref2>
  [ ON <condition> ]
[ ... ]
```

Copy code

```
SELECT *
FROM <object_ref1> [
                     {
                       INNER
                       | { LEFT | RIGHT | FULL } [ OUTER ]
                     }
                   ]
                   JOIN <object_ref2>
  [ USING( <column_list> ) ]
[ ... ]
```

Copy code

```
SELECT ...
FROM <object_ref1> [
                     {
                       | NATURAL [ { LEFT | RIGHT | FULL } [ OUTER ] ]
                       | CROSS
                     }
                   ]
                   JOIN <object_ref2>
[ ... ]
```

### Sample Source Patterns

Note

*Order by* clause added because the result order may vary between Oracle and Snowflake.

Note

Since the result set is too large, *Row Limiting Clause* was added. You can remove it to retrieve the entire result set.

Note

Check this [section](../sample-data) to set up the sample database.

Note

For the following examples, these inserts and alter statements were executed to distinguish better the result for each kind of JOIN:

Copy code

```
INSERT INTO hr.regions VALUES (5, 'Oceania');
ALTER TABLE hr.countries DROP CONSTRAINT countr_reg_fk;
INSERT INTO hr.countries VALUES ('--', 'Unknown Country', 0);
```

#### 1. ANSI syntax

Snowflake fully supports the ANSI syntax for SQL JOINS. The behavior is the same for both database engines.

#### Left Outer Join On

##### Oracle

Copy code

```
SELECT * FROM
hr.countries c
LEFT OUTER JOIN hr.regions r ON c.region_id = r.region_id
ORDER BY country_id
FETCH FIRST 10 ROWS ONLY;
```

##### Result

| COUNTRY\_ID | COUNTRY\_NAME | REGION\_ID | REGION\_ID | REGION\_NAME |
| --- | --- | --- | --- | --- |
| – | Unknown Country | 0 |  |  |
| AR | Argentina | 2 | 2 | Americas |
| AU | Australia | 3 | 3 | Asia |
| BE | Belgium | 1 | 1 | Europe |
| BR | Brazil | 2 | 2 | Americas |
| CA | Canada | 2 | 2 | Americas |
| CH | Switzerland | 1 | 1 | Europe |
| CN | China | 3 | 3 | Asia |
| DE | Germany | 1 | 1 | Europe |
| DK | Denmark | 1 | 1 | Europe |

Expand

Show lessSee more

##### Snowflake

Copy code

```
SELECT * FROM
hr.countries c
LEFT OUTER JOIN
hr.regions r ON c.region_id = r.region_id
ORDER BY country_id
FETCH FIRST 10 ROWS ONLY;
```

##### Result

| COUNTRY\_ID | COUNTRY\_NAME | REGION\_ID | REGION\_ID | REGION\_NAME |
| --- | --- | --- | --- | --- |
| – | Unknown Country | 0.0000000000000000000 |  |  |
| AR | Argentina | 2.0000000000000000000 | 2.0000000000000000000 | Americas |
| AU | Australia | 3.0000000000000000000 | 3.0000000000000000000 | Asia |
| BE | Belgium | 1.0000000000000000000 | 1.0000000000000000000 | Europe |
| BR | Brazil | 2.0000000000000000000 | 2.0000000000000000000 | Americas |
| CA | Canada | 2.0000000000000000000 | 2.0000000000000000000 | Americas |
| CH | Switzerland | 1.0000000000000000000 | 1.0000000000000000000 | Europe |
| CN | China | 3.0000000000000000000 | 3.0000000000000000000 | Asia |
| DE | Germany | 1.0000000000000000000 | 1.0000000000000000000 | Europe |
| DK | Denmark | 1.0000000000000000000 | 1.0000000000000000000 | Europe |

Expand

Show lessSee more

#### Right Outer Join On

##### Oracle

Copy code

```
SELECT * FROM
hr.countries c
RIGHT OUTER JOIN hr.regions r ON c.region_id = r.region_id
ORDER BY country_id DESC
FETCH FIRST 10 ROWS ONLY;
```

##### Result

| COUNTRY\_ID | COUNTRY\_NAME | REGION\_ID | REGION\_ID | REGION\_NAME |
| --- | --- | --- | --- | --- |
| – |  |  | 5 | Oceania |
| ZW | Zimbabwe | 4 | 4 | Middle East and Africa |
| ZM | Zambia | 4 | 4 | Middle East and Africa |
| US | United States of America | 2 | 2 | Americas |
| UK | United Kingdom | 1 | 1 | Europe |
| SG | Singapore | 3 | 3 | Asia |
| NL | Netherlands | 1 | 1 | Europe |
| NG | Nigeria | 4 | 4 | Middle East and Africa |
| MX | Mexico | 2 | 2 | Americas |
| ML | Malaysia | 3 | 3 | Asia |

Expand

Show lessSee more

##### Snowflake

Copy code

```
SELECT * FROM
hr.countries c
RIGHT OUTER JOIN
hr.regions r ON c.region_id = r.region_id
ORDER BY country_id DESC
FETCH FIRST 10 ROWS ONLY;
```

##### Result

| COUNTRY\_ID | COUNTRY\_NAME | REGION\_ID | REGION\_ID | REGION\_NAME |
| --- | --- | --- | --- | --- |
| – |  | 5.0000000000000000000 | Oceania |  |
| ZW | Zimbabwe | 4.0000000000000000000 | 4.0000000000000000000 | Middle East and Africa |
| ZM | Zambia | 4.0000000000000000000 | 4.0000000000000000000 | Middle East and Africa |
| US | United States of America | 2.0000000000000000000 | 2.0000000000000000000 | Americas |
| UK | United Kingdom | 1.0000000000000000000 | 1.0000000000000000000 | Europe |
| SG | Singapore | 3.0000000000000000000 | 3.0000000000000000000 | Asia |
| NL | Netherlands | 1.0000000000000000000 | 1.0000000000000000000 | Europe |
| NG | Nigeria | 4.0000000000000000000 | 4.0000000000000000000 | Middle East and Africa |
| MX | Mexico | 2.0000000000000000000 | 2.0000000000000000000 | Americas |
| ML | Malaysia | 3.0000000000000000000 | 3.0000000000000000000 | Asia |

Expand

Show lessSee more

#### Full Outer Join On

##### Oracle

Copy code

```
SELECT * FROM
hr.countries c
FULL OUTER JOIN hr.regions r ON c.region_id = r.region_id
ORDER BY r.region_name DESC, c.country_id
FETCH FIRST 10 ROWS ONLY;
```

##### Result

| COUNTRY\_ID | COUNTRY\_NAME | REGION\_ID | REGION\_ID | REGION\_NAME |
| --- | --- | --- | --- | --- |
| – | Unknown Country | 0 |  |  |
| – |  |  | 5 | Oceania |
| EG | Egypt | 4 | 4 | Middle East and Africa |
| IL | Israel | 4 | 4 | Middle East and Africa |
| KW | Kuwait | 4 | 4 | Middle East and Africa |
| NG | Nigeria | 4 | 4 | Middle East and Africa |
| ZM | Zambia | 4 | 4 | Middle East and Africa |
| ZW | Zimbabwe | 4 | 4 | Middle East and Africa |
| BE | Belgium | 1 | 1 | Europe |
| CH | Switzerland | 1 | 1 | Europe |

Expand

Show lessSee more

##### Snowflake

Copy code

```
SELECT * FROM
hr.countries c
FULL OUTER JOIN
hr.regions r ON c.region_id = r.region_id
ORDER BY r.region_name DESC, c.country_id
FETCH FIRST 10 ROWS ONLY;
```

##### Result

| COUNTRY\_ID | COUNTRY\_NAME | REGION\_ID | REGION\_ID | REGION\_NAME |
| --- | --- | --- | --- | --- |
| – | Unknown Country | 0.0000000000000000000 |  |  |
| – |  |  | 5.0000000000000000000 | Oceania |
| EG | Egypt | 4.0000000000000000000 | 4.0000000000000000000 | Middle East and Africa |
| IL | Israel | 4.0000000000000000000 | 4.0000000000000000000 | Middle East and Africa |
| KW | Kuwait | 4.0000000000000000000 | 4.0000000000000000000 | Middle East and Africa |
| NG | Nigeria | 4.0000000000000000000 | 4.0000000000000000000 | Middle East and Africa |
| ZM | Zambia | 4.0000000000000000000 | 4.0000000000000000000 | Middle East and Africa |
| ZW | Zimbabwe | 4.0000000000000000000 | 4.0000000000000000000 | Middle East and Africa |
| BE | Belgium | 1.0000000000000000000 | 1.0000000000000000000 | Europe |
| CH | Switzerland | 1.0000000000000000000 | 1.0000000000000000000 | Europe |

Expand

Show lessSee more

#### 2. Natural Outer Join

Both Oracle and Snowflake support the Natural Outer Join and they behave the same.

> A NATURAL JOIN is identical to an explicit JOIN on the common columns of the two tables, except that the common columns are included only once in the output. (A natural join assumes that columns with the same name, but in different tables, contain corresponding data.)([Snowflake SQL Language Reference JOIN](https://docs.snowflake.com/en/sql-reference/constructs/join.html))

#### Natural Left Outer Join

##### Oracle

Copy code

```
SELECT * FROM
hr.countries c
NATURAL LEFT OUTER JOIN hr.regions r
ORDER BY country_id
FETCH FIRST 10 ROWS ONLY;
```

##### Result

| REGION\_ID | COUNTRY\_ID | COUNTRY\_NAME | REGION\_NAME |
| --- | --- | --- | --- |
| 0 | – | Unknown Country |  |
| 2 | AR | Argentina | Americas |
| 3 | AU | Australia | Asia |
| 1 | BE | Belgium | Europe |
| 2 | BR | Brazil | Americas |
| 2 | CA | Canada | Americas |
| 1 | CH | Switzerland | Europe |
| 3 | CN | China | Asia |
| 1 | DE | Germany | Europe |
| 1 | DK | Denmark | Europe |

Expand

Show lessSee more

##### Snowflake

Copy code

```
SELECT * FROM
hr.countries c
NATURAL LEFT OUTER JOIN
hr.regions r
ORDER BY country_id
FETCH FIRST 10 ROWS ONLY;
```

##### Result

| REGION\_ID | COUNTRY\_ID | COUNTRY\_NAME | REGION\_NAME |
| --- | --- | --- | --- |
| 0.0000000000000000000 | – | Unknown Country |  |
| 2.0000000000000000000 | AR | Argentina | Americas |
| 3.0000000000000000000 | AU | Australia | Asia |
| 1.0000000000000000000 | BE | Belgium | Europe |
| 2.0000000000000000000 | BR | Brazil | Americas |
| 2.0000000000000000000 | CA | Canada | Americas |
| 1.0000000000000000000 | CH | Switzerland | Europe |
| 3.0000000000000000000 | CN | China | Asia |
| 1.0000000000000000000 | DE | Germany | Europe |
| 1.0000000000000000000 | DK | Denmark | Europe |

Expand

Show lessSee more

#### Natural Right Outer Join

##### Oracle

Copy code

```
SELECT * FROM
hr.countries c
NATURAL RIGHT OUTER JOIN hr.regions r
ORDER BY country_id DESC
FETCH FIRST 10 ROWS ONLY;
```

##### Result

| REGION\_ID | COUNTRY\_ID | COUNTRY\_NAME | REGION\_NAME |
| --- | --- | --- | --- |
| 5 |  |  | Oceania |
| 4 | ZW | Zimbabwe | Middle East and Africa |
| 4 | ZM | Zambia | Middle East and Africa |
| 2 | US | United States of America | Americas |
| 1 | UK | United Kingdom | Europe |
| 3 | SG | Singapore | Asia |
| 1 | NL | Netherlands | Europe |
| 4 | NG | Nigeria | Middle East and Africa |
| 2 | MX | Mexico | Americas |
| 3 | ML | Malaysia | Asia |

Expand

Show lessSee more

##### Snowflake

Copy code

```
SELECT * FROM
hr.countries c
NATURAL RIGHT OUTER JOIN
hr.regions r
ORDER BY country_id DESC
FETCH FIRST 10 ROWS ONLY;
```

##### Result

| REGION\_ID | COUNTRY\_ID | COUNTRY\_NAME | REGION\_NAME |
| --- | --- | --- | --- |
| 5.0000000000000000000 |  |  | Oceania |
| 4.0000000000000000000 | ZW | Zimbabwe | Middle East and Africa |
| 4.0000000000000000000 | ZM | Zambia | Middle East and Africa |
| 2.0000000000000000000 | US | United States of America | Americas |
| 1.0000000000000000000 | UK | United Kingdom | Europe |
| 3.0000000000000000000 | SG | Singapore | Asia |
| 1.0000000000000000000 | NL | Netherlands | Europe |
| 4.0000000000000000000 | NG | Nigeria | Middle East and Africa |
| 2.0000000000000000000 | MX | Mexico | Americas |
| 3.0000000000000000000 | ML | Malaysia | Asia |

Expand

Show lessSee more

#### 3. Basic Outer Join with USING

Table columns can be joined using the USING keyword. The results will be the same as a basic OUTER JOIN with the ON keyword.

#### Left Outer Join Using

##### Oracle

Copy code

```
SELECT * FROM
hr.countries c
LEFT OUTER JOIN hr.regions r USING (region_id)
ORDER BY country_id
FETCH FIRST 10 ROWS ONLY;
```

##### Result

| REGION\_ID | COUNTRY\_ID | COUNTRY\_NAME | REGION\_NAME |
| --- | --- | --- | --- |
| 0 | – | Unknown Country |  |
| 2 | AR | Argentina | Americas |
| 3 | AU | Australia | Asia |
| 1 | BE | Belgium | Europe |
| 2 | BR | Brazil | Americas |
| 2 | CA | Canada | Americas |
| 1 | CH | Switzerland | Europe |
| 3 | CN | China | Asia |
| 1 | DE | Germany | Europe |
| 1 | DK | Denmark | Europe |

Expand

Show lessSee more

##### Snowflake

Copy code

```
SELECT * FROM
hr.countries c
LEFT OUTER JOIN
hr.regions r USING (region_id)
ORDER BY country_id
FETCH FIRST 10 ROWS ONLY;
```

##### Result

| REGION\_ID | COUNTRY\_ID | COUNTRY\_NAME | REGION\_NAME |
| --- | --- | --- | --- |
| 0.0000000000000000000 | – | Unknown Country |  |
| 2.0000000000000000000 | AR | Argentina | Americas |
| 3.0000000000000000000 | AU | Australia | Asia |
| 1.0000000000000000000 | BE | Belgium | Europe |
| 2.0000000000000000000 | BR | Brazil | Americas |
| 2.0000000000000000000 | CA | Canada | Americas |
| 1.0000000000000000000 | CH | Switzerland | Europe |
| 3.0000000000000000000 | CN | China | Asia |
| 1.0000000000000000000 | DE | Germany | Europe |
| 1.0000000000000000000 | DK | Denmark | Europe |

Expand

Show lessSee more

#### 4. (+) Operator

Oracle and Snowflake have a (+) operator that can be used for outer joins too. In some cases, Snowflake may not work properly when using this operator.

For more information regarding this operator in Snowflake, check [this](https://docs.snowflake.com/en/sql-reference/constructs/where.html#joins-in-the-where-clause).

#### Left Outer Join with (+) operator

##### Oracle

Copy code

```
SELECT * FROM hr.countries c, hr.regions r
WHERE c.region_id = r.region_id(+)
ORDER BY country_id
FETCH FIRST 10 ROWS ONLY;
```

##### Result

| COUNTRY\_ID | COUNTRY\_NAME | REGION\_ID | REGION\_ID | REGION\_NAME |
| --- | --- | --- | --- | --- |
| – | Unknown Country | 0 |  |  |
| AR | Argentina | 2 | 2 | Americas |
| AU | Australia | 3 | 3 | Asia |
| BE | Belgium | 1 | 1 | Europe |
| BR | Brazil | 2 | 2 | Americas |
| CA | Canada | 2 | 2 | Americas |
| CH | Switzerland | 1 | 1 | Europe |
| CN | China | 3 | 3 | Asia |
| DE | Germany | 1 | 1 | Europe |
| DK | Denmark | 1 | 1 | Europe |

Expand

Show lessSee more

##### Snowflake

Copy code

```
SELECT * FROM
hr.countries c,
hr.regions r
WHERE c.region_id = r.region_id(+)
ORDER BY country_id
FETCH FIRST 10 ROWS ONLY;
```

##### Result

| COUNTRY\_ID | COUNTRY\_NAME | REGION\_ID | REGION\_ID | REGION\_NAME |
| --- | --- | --- | --- | --- |
| – | Unknown Country | 0.0000000000000000000 |  |  |
| AR | Argentina | 2.0000000000000000000 | 2.0000000000000000000 | Americas |
| AU | Australia | 3.0000000000000000000 | 3.0000000000000000000 | Asia |
| BE | Belgium | 1.0000000000000000000 | 1.0000000000000000000 | Europe |
| BR | Brazil | 2.0000000000000000000 | 2.0000000000000000000 | Americas |
| CA | Canada | 2.0000000000000000000 | 2.0000000000000000000 | Americas |
| CH | Switzerland | 1.0000000000000000000 | 1.0000000000000000000 | Europe |
| CN | China | 3.0000000000000000000 | 3.0000000000000000000 | Asia |
| DE | Germany | 1.0000000000000000000 | 1.0000000000000000000 | Europe |
| DK | Denmark | 1.0000000000000000000 | 1.0000000000000000000 | Europe |

Expand

Show lessSee more

#### Right Outer Join with (+) operator

##### Oracle

Copy code

```
SELECT * FROM hr.countries c, hr.regions r
WHERE c.region_id (+) = r.region_id
ORDER BY country_id DESC
FETCH FIRST 10 ROWS ONLY;
```

##### Result

| COUNTRY\_ID | COUNTRY\_NAME | REGION\_ID | REGION\_ID | REGION\_NAME |
| --- | --- | --- | --- | --- |
| – |  |  | 5 | Oceania |
| ZW | Zimbabwe | 4 | 4 | Middle East and Africa |
| ZM | Zambia | 4 | 4 | Middle East and Africa |
| US | United States of America | 2 | 2 | Americas |
| UK | United Kingdom | 1 | 1 | Europe |
| SG | Singapore | 3 | 3 | Asia |
| NL | Netherlands | 1 | 1 | Europe |
| NG | Nigeria | 4 | 4 | Middle East and Africa |
| MX | Mexico | 2 | 2 | Americas |
| ML | Malaysia | 3 | 3 | Asia |

Expand

Show lessSee more

##### Snowflake

Copy code

```
SELECT * FROM
hr.countries c,
hr.regions r
WHERE c.region_id (+) = r.region_id
ORDER BY country_id DESC
FETCH FIRST 10 ROWS ONLY;
```

##### Result

| COUNTRY\_ID | COUNTRY\_NAME | REGION\_ID | REGION\_ID | REGION\_NAME |
| --- | --- | --- | --- | --- |
| – |  |  | 5.0000000000000000000 | Oceania |
| ZW | Zimbabwe | 4.0000000000000000000 | 4.0000000000000000000 | Middle East and Africa |
| ZM | Zambia | 4.0000000000000000000 | 4.0000000000000000000 | Middle East and Africa |
| US | United States of America | 2.0000000000000000000 | 2.0000000000000000000 | Americas |
| UK | United Kingdom | 1.0000000000000000000 | 1.0000000000000000000 | Europe |
| SG | Singapore | 3.0000000000000000000 | 3.0000000000000000000 | Asia |
| NL | Netherlands | 1.0000000000000000000 | 1.0000000000000000000 | Europe |
| NG | Nigeria | 4.0000000000000000000 | 4.0000000000000000000 | Middle East and Africa |
| MX | Mexico | 2.0000000000000000000 | 2.0000000000000000000 | Americas |
| ML | Malaysia | 3.0000000000000000000 | 3.0000000000000000000 | Asia |

Expand

Show lessSee more

#### Single table joined with multiple tables with (+)

In Oracle, you can join a single table with multiple tables using the (+) operator, however, Snowflake does not support this. Queries with this kind of Outer Joins will be changed to ANSI syntax.

##### Oracle

Copy code

```
SELECT
c.country_id,
c.country_name,
r.region_id,
r.region_name,
l.location_id,
l.street_address,
l.postal_code,
l.city
FROM
hr.countries c, hr.regions r,  hr.locations l
WHERE
c.region_id(+) = r.region_id AND
l.country_id = c.country_id(+)
ORDER BY r.region_id, l.city
FETCH FIRST 10 ROWS ONLY;
```

##### Result

| COUNTRY\_ID | COUNTRY\_NAME | REGION\_ID | REGION\_NAME | LOCATION\_ID | STREET\_ADDRESS | POSTAL\_CODE | CITY |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  | 1 | Europe | 2000 | 40-5-12 Laogianggen | 190518 | Beijing |
| CH | Switzerland | 1 | Europe | 3000 | Murtenstrasse 921 | 3095 | Bern |
|  |  | 1 | Europe | 2100 | 1298 Vileparle (E) | 490231 | Bombay |
| CH | Switzerland | 1 | Europe | 2900 | 20 Rue des Corps-Saints | 1730 | Geneva |
|  |  | 1 | Europe | 1300 | 9450 Kamiya-cho | 6823 | Hiroshima |
| UK | United Kingdom | 1 | Europe | 2400 | 8204 Arthur St |  | London |
|  |  | 1 | Europe | 3200 | Mariano Escobedo 9991 | 11932 | Mexico City |
| DE | Germany | 1 | Europe | 2700 | Schwanthalerstr. 7031 | 80925 | Munich |
| UK | United Kingdom | 1 | Europe | 2500 | Magdalen Centre, The Oxford Science Park | OX9 9ZB | Oxford |
| IT | Italy | 1 | Europe | 1000 | 1297 Via Cola di Rie | 00989 | Roma |

Expand

Show lessSee more

##### Snowflake

Copy code

```
SELECT
c.country_id,
c.country_name,
r.region_id,
r.region_name,
l.location_id,
l.street_address,
l.postal_code,
l.city
FROM
hr.regions r
CROSS JOIN hr.locations l
LEFT OUTER JOIN
hr.countries c
ON
c.region_id = r.region_id
AND
l.country_id = c.country_id
ORDER BY r.region_id, l.city
FETCH FIRST 10 ROWS ONLY;
```

##### Result

| COUNTRY\_ID | COUNTRY\_NAME | REGION\_ID | REGION\_NAME | LOCATION\_ID | STREET\_ADDRESS | POSTAL\_CODE | CITY |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  | 1.0000000000000000000 | Europe | 2000 | 40-5-12 Laogianggen | 190518 | Beijing |
| CH | Switzerland | 1.0000000000000000000 | Europe | 3000 | Murtenstrasse 921 | 3095 | Bern |
|  |  | 1.0000000000000000000 | Europe | 2100 | 1298 Vileparle (E) | 490231 | Bombay |
| CH | Switzerland | 1.0000000000000000000 | Europe | 2900 | 20 Rue des Corps-Saints | 1730 | Geneva |
|  |  | 1.0000000000000000000 | Europe | 1300 | 9450 Kamiya-cho | 6823 | Hiroshima |
| UK | United Kingdom | 1.0000000000000000000 | Europe | 2400 | 8204 Arthur St |  | London |
|  |  | 1.0000000000000000000 | Europe | 3200 | Mariano Escobedo 9991 | 11932 | Mexico City |
| DE | Germany | 1.0000000000000000000 | Europe | 2700 | Schwanthalerstr. 7031 | 80925 | Munich |
| UK | United Kingdom | 1.0000000000000000000 | Europe | 2500 | Magdalen Centre, The Oxford Science Park | OX9 9ZB | Oxford |
| IT | Italy | 1.0000000000000000000 | Europe | 1000 | 1297 Via Cola di Rie | 00989 | Roma |

Expand

Show lessSee more

#### Using (+) operator with a column from a not-joined table and a non-column value

In Oracle, you can use the (+) operator with a Column and join it with a value that is not a column from another table. Snowflake can also do this but it will fail if the table of the column was not joined with another table. To solve this issue, the (+) operator is removed from the query when this scenario happens and the result will be the same as in Oracle.

##### Oracle

Copy code

```
SELECT * FROM hr.regions r
WHERE
r.region_name (+) LIKE 'A%'
ORDER BY region_id;
```

##### Result

| REGION\_ID | REGION\_NAME |
| --- | --- |
| 2 | Americas |
| 3 | Asia |

Expand

Show lessSee more

##### Snowflake

Copy code

```
SELECT * FROM
hr.regions r
WHERE
r.region_name LIKE 'A%'
ORDER BY region_id;
```

##### Result

| REGION\_ID | REGION\_NAME |
| --- | --- |
| 2.0000000000000000000 | Americas |
| 3.0000000000000000000 | Asia |

Expand

Show lessSee more

### Known issues

For all the unsupported cases, please check the related EWIs to obtain recommendations and possible workarounds.

#### 1. Converted Outer Joins to ANSI syntax might reorder the columns

When a query with a non-ANSI Outer Join is converted to an ANSI Outer Join, it may change the order of the columns in the converted query. To fix this issue, try to select the columns in the specific order required.

##### Oracle

Copy code

```
SELECT
*
FROM
hr.countries c, hr.regions r,  hr.locations l
WHERE
c.region_id(+) = r.region_id AND
l.country_id = c.country_id(+)
ORDER BY r.region_id, l.city
FETCH FIRST 10 ROWS ONLY;
```

##### Result

| COUNTRY\_ID | COUNTRY\_NAME | REGION\_ID | REGION\_ID | REGION\_NAME | LOCATION\_ID | STREET\_ADDRESS | POSTAL\_CODE | CITY | STATE\_PROVINCE | COUNTRY\_ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  | 1 | Europe | 2000 | 40-5-12 Laogianggen | 190518 | Beijing |  | CN |
| CH | Switzerland | 1 | 1 | Europe | 3000 | Murtenstrasse 921 | 3095 | Bern | BE | CH |
|  |  |  | 1 | Europe | 2100 | 1298 Vileparle (E) | 490231 | Bombay | Maharashtra | IN |
| CH | Switzerland | 1 | 1 | Europe | 2900 | 20 Rue des Corps-Saints | 1730 | Geneva | Geneve | CH |
|  |  |  | 1 | Europe | 1300 | 9450 Kamiya-cho | 6823 | Hiroshima |  | JP |
| UK | United Kingdom | 1 | 1 | Europe | 2400 | 8204 Arthur St |  | London |  | UK |
|  |  |  | 1 | Europe | 3200 | Mariano Escobedo 9991 | 11932 | Mexico City | Distrito Federal, | MX |
| DE | Germany | 1 | 1 | Europe | 2700 | Schwanthalerstr. 7031 | 80925 | Munich | Bavaria | DE |
| UK | United Kingdom | 1 | 1 | Europe | 2500 | Magdalen Centre, The Oxford Science Park | OX9 9ZB | Oxford | Oxford | UK |
| IT | Italy | 1 | 1 | Europe | 1000 | 1297 Via Cola di Rie | 00989 | Roma |  | IT |

Expand

Show lessSee more

##### Snowflake

Copy code

```
SELECT
*
FROM
hr.regions r
CROSS JOIN hr.locations l
LEFT OUTER JOIN
hr.countries c
ON
c.region_id = r.region_id
AND
l.country_id = c.country_id
ORDER BY r.region_id, l.city
FETCH FIRST 10 ROWS ONLY;
```

##### Result

| REGION\_ID | REGION\_NAME | LOCATION\_ID | STREET\_ADDRESS | POSTAL\_CODE | CITY | STATE\_PROVINCE | COUNTRY\_ID | COUNTRY\_ID | COUNTRY\_NAME | REGION\_ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1.0000000000000000000 | Europe | 2000 | 40-5-12 Laogianggen | 190518 | Beijing |  | CN |  |  |  |
| 1.0000000000000000000 | Europe | 3000 | Murtenstrasse 921 | 3095 | Bern | BE | CH | CH | Switzerland | 1.0000000000000000000 |
| 1.0000000000000000000 | Europe | 2100 | 1298 Vileparle (E) | 490231 | Bombay | Maharashtra | IN |  |  |  |
| 1.0000000000000000000 | Europe | 2900 | 20 Rue des Corps-Saints | 1730 | Geneva | Geneve | CH | CH | Switzerland | 1.0000000000000000000 |
| 1.0000000000000000000 | Europe | 1300 | 9450 Kamiya-cho | 6823 | Hiroshima |  | JP |  |  |  |
| 1.0000000000000000000 | Europe | 2400 | 8204 Arthur St |  | London |  | UK | UK | United Kingdom | 1.0000000000000000000 |
| 1.0000000000000000000 | Europe | 3200 | Mariano Escobedo 9991 | 11932 | Mexico City | Distrito Federal, | MX |  |  |  |
| 1.0000000000000000000 | Europe | 2700 | Schwanthalerstr. 7031 | 80925 | Munich | Bavaria | DE | DE | Germany | 1.0000000000000000000 |
| 1.0000000000000000000 | Europe | 2500 | Magdalen Centre, The Oxford Science Park | OX9 9ZB | Oxford | Oxford | UK | UK | United Kingdom | 1.0000000000000000000 |
| 1.0000000000000000000 | Europe | 1000 | 1297 Via Cola di Rie | 00989 | Roma |  | IT | IT | Italy | 1.0000000000000000000 |

Expand

Show lessSee more

##### 2. Outer joined between predicate with an interval with multiple tables

Between predicates can be used for non-ANSI OUTER JOINS. In Oracle, columns inside the interval can be outer joined, even if they come from different tables, however, Snowflake does not support this. For these cases, the between predicate will be commented out.

##### Oracle

Copy code

```
SELECT
*
FROM
hr.countries c, hr.regions r,  hr.locations l WHERE
l.location_id  BETWEEN r.region_id(+) AND c.region_id(+)
ORDER BY r.region_id, l.city
FETCH FIRST 10 ROWS ONLY;
```

##### Result

| COUNTRY\_ID | COUNTRY\_NAME | REGION\_ID | REGION\_ID | REGION\_NAME | LOCATION\_ID | STREET\_ADDRESS | POSTAL\_CODE | CITY | STATE\_PROVINCE | COUNTRY\_ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  | 1 | Europe | 2000 | 40-5-12 Laogianggen | 190518 | Beijing |  | CN |
|  |  |  | 1 | Europe | 3000 | Murtenstrasse 921 | 3095 | Bern | BE | CH |
|  |  |  | 1 | Europe | 2100 | 1298 Vileparle (E) | 490231 | Bombay | Maharashtra | IN |
|  |  |  | 1 | Europe | 2900 | 20 Rue des Corps-Saints | 1730 | Geneva | Geneve | CH |
|  |  |  | 1 | Europe | 1300 | 9450 Kamiya-cho | 6823 | Hiroshima |  | JP |
|  |  |  | 1 | Europe | 2400 | 8204 Arthur St |  | London |  | UK |
|  |  |  | 1 | Europe | 3200 | Mariano Escobedo 9991 | 11932 | Mexico City | Distrito Federal, | MX |
|  |  |  | 1 | Europe | 2700 | Schwanthalerstr. 7031 | 80925 | Munich | Bavaria | DE |
|  |  |  | 1 | Europe | 2500 | Magdalen Centre, The Oxford Science Park | OX9 9ZB | Oxford | Oxford | UK |
|  |  |  | 1 | Europe | 1000 | 1297 Via Cola di Rie | 00989 | Roma |  | IT |

Expand

Show lessSee more

##### Snowflake

Copy code

```
SELECT
*
FROM
hr.countries c,
hr.regions r,
hr.locations l WHERE
!!!RESOLVE EWI!!! /*** SSC-EWI-OR0090 - INVALID NON-ANSI OUTER JOIN BETWEEN PREDICATE CASE FOR SNOWFLAKE. ***/!!!
l.location_id  BETWEEN r.region_id(+) AND c.region_id(+)
ORDER BY r.region_id, l.city
FETCH FIRST 10 ROWS ONLY;
```

### Related EWIs

1. [SSC-EWI-OR0090](../../../issues-and-troubleshooting/conversion-issues/oracleEWI#ssc-ewi-or0090): Non-Ansi Outer Join has an invalid Between predicate.

## Self Join

Note

Some parts in the output codes are omitted for clarity reasons.

### Description

> A self join is a join of a table to itself. This table appears twice in the `FROM` clause and is followed by table aliases that qualify column names in the join condition. ([Oracle SQL Language Reference Self Join Subsection](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/Joins.html#GUID-B0F5C614-CBDD-45F6-966D-00BAD6463440))

### Sample Source Patterns

Note

*Order by* clause added because the result order may vary between Oracle and Snowflake.

Note

Check this [section](../sample-data) to set up the sample database.

#### Basic Self Join case

##### Oracle

Copy code

```
SELECT e1.last_name||' works for '||e2.last_name
   "Employees and Their Managers"
   FROM hr.employees e1, hr.employees e2
   WHERE e1.manager_id = e2.employee_id
      AND e1.last_name LIKE 'R%'
   ORDER BY e1.last_name;
```

##### Result

| Employees and Their Managers |
| --- |
| Rajs works for Mourgos |
| Raphaely works for King |
| Rogers works for Kaufling |
| Russell works for King |

Expand

Show lessSee more

##### Snowflake

Copy code

```
SELECT
   NVL( e1.last_name :: STRING, '') || ' works for ' || NVL(e2.last_name :: STRING, '') "Employees and Their Managers"
FROM
   hr.employees e1,
   hr.employees e2
   WHERE e1.manager_id = e2.employee_id
      AND e1.last_name LIKE 'R%'
   ORDER BY e1.last_name;
```

##### Result

| Employees and Their Managers |
| --- |
| Rajs works for Mourgos |
| Raphaely works for King |
| Rogers works for Kaufling |
| Russell works for King |

Expand

Show lessSee more

Note

As proved previously the **self join** in Oracle is functionally equivalent to Snowflake.

### Known Issues

No issues were found.

### Related EWIs

No related EWIs.

## Semijoin

Note

Some parts in the output code are omitted for clarity reasons.

### Description

> A semijoin returns rows that match an `EXISTS` subquery without duplicating rows from the left side of the predicate when multiple rows on the right side satisfy the criteria of the subquery. Semijoin transformation cannot be done if the subquery is on an `OR` branch of the `WHERE` clause. ([Oracle SQL Language Reference Semijoin Subsection](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/Joins.html#GUID-E98C180E-8A17-469D-8E68-56245E28104B))

### Sample Source Patterns

Note

*Order by* clause added because the result order may vary between Oracle and Snowflake.

Note

Check this [section](../sample-data) to set up the sample database.

#### Basic Semijoin case

##### Oracle

Copy code

```
SELECT * FROM hr.departments
   WHERE EXISTS
   (SELECT * FROM hr.employees
       WHERE departments.department_id = employees.department_id
       AND employees.salary > 2500)
   ORDER BY department_name;
```

##### Result

| DEPARTMENT\_ID | DEPARTMENT\_NAME | MANAGER\_ID | LOCATION\_ID |
| --- | --- | --- | --- |
| 110 | Accounting | 205 | 1700 |
| 10 | Administration | 200 | 1700 |
| 90 | Executive | 100 | 1700 |
| 100 | Finance | 108 | 1700 |
| 40 | Human Resources | 203 | 2400 |
| 60 | IT | 103 | 1400 |
| 20 | Marketing | 201 | 1800 |
| 70 | Public Relations | 204 | 2700 |
| 30 | Purchasing | 114 | 1700 |
| 80 | Sales | 145 | 2500 |
| 50 | Shipping | 121 | 1500 |

Expand

Show lessSee more

##### Snowflake

Copy code

```
SELECT * FROM
   hr.departments
   WHERE EXISTS
   (SELECT * FROM
         hr.employees
       WHERE departments.department_id = employees.department_id
       AND employees.salary > 2500)
   ORDER BY department_name;
```

##### Result

| DEPARTMENT\_ID | DEPARTMENT\_NAME | MANAGER\_ID | LOCATION\_ID |
| --- | --- | --- | --- |
| 110 | Accounting | 205 | 1700 |
| 10 | Administration | 200 | 1700 |
| 90 | Executive | 100 | 1700 |
| 100 | Finance | 108 | 1700 |
| 40 | Human Resources | 203 | 2400 |
| 60 | IT | 103 | 1400 |
| 20 | Marketing | 201 | 1800 |
| 70 | Public Relations | 204 | 2700 |
| 30 | Purchasing | 114 | 1700 |
| 80 | Sales | 145 | 2500 |
| 50 | Shipping | 121 | 1500 |

Expand

Show lessSee more

Note

As proved previously the **semijoin** in Oracle is functionally equivalent to Snowflake.

### Known Issues

No issues were found.

### Related EWIs

No related EWIs.
