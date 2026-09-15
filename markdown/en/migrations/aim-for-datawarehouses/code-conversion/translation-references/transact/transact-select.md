# SQL Server-Azure Synapse - SELECT

## SELECT

Translation reference for SELECT statement inside procedures in Transact-SQL.

Applies to

- SQL Server
- Azure Synapse Analytics

Note

Multiple result sets are returned in temporary tables

### Description

Snowflake SQL supports returning tables as a return type for Stored Procedures, but unlike Transact-SQL, Snowflake does not support returning multiple resultsets in the same procedure. For this scenario, all the query IDs are stored in a temporary table and returned as an array.

### Sample Source Patterns

The following example details the transformation when there is only one SELECT statement in the procedure.

#### Transact-SQL

##### Single Resultset

Copy code

```
CREATE PROCEDURE SOMEPROC()
AS
BEGIN
        SELECT * from AdventureWorks.HumanResources.Department;
END
```

##### Output

| DepartmentID | Name | GroupName |
| --- | --- | --- |
| 1 | Engineering | Research and Development |
| 2 | Tool Design | Research and Development |
| 3 | Sales | Sales and Marketing |
| 4 | Marketing | Sales and Marketing |
| 5 | Purchasing | Inventory Management |
| 6 | Research and Development | Research and Development |
| 7 | Production | Manufacturing |
| 8 | Production Control | Manufacturing |
| 9 | Human Resources | Executive General and Administration |
| 10 | Finance | Executive General and Administration |
| 11 | Information Services | Executive General and Administration |
| 12 | Document Control | Quality Assurance |
| 13 | Quality Assurance | Quality Assurance |
| 14 | Facilities and Maintenance | Executive General and Administration |
| 15 | Shipping and Receiving | Inventory Management |
| 16 | Executive | Executive General and Administration |

Expand

Show lessSee more

##### Snowflake SQL

##### Single Resultset

Copy code

```
CREATE OR REPLACE PROCEDURE SOMEPROC ()
RETURNS TABLE()
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
        DECLARE
                ProcedureResultSet RESULTSET;
        BEGIN
                ProcedureResultSet := (
                SELECT
                        *
                from
                        AdventureWorks.HumanResources.Department);
                RETURN TABLE(ProcedureResultSet);
        END;
$$;
```

##### Output

| DepartmentID | Name | GroupName |
| --- | --- | --- |
| 1 | Engineering | Research and Development |
| 2 | Tool Design | Research and Development |
| 3 | Sales | Sales and Marketing |
| 4 | Marketing | Sales and Marketing |
| 5 | Purchasing | Inventory Management |
| 6 | Research and Development | Research and Development |
| 7 | Production | Manufacturing |
| 8 | Production Control | Manufacturing |
| 9 | Human Resources | Executive General and Administration |
| 10 | Finance | Executive General and Administration |
| 11 | Information Services | Executive General and Administration |
| 12 | Document Control | Quality Assurance |
| 13 | Quality Assurance | Quality Assurance |
| 14 | Facilities and Maintenance | Executive General and Administration |
| 15 | Shipping and Receiving | Inventory Management |
| 16 | Executive | Executive General and Administration |

Expand

Show lessSee more

The following example details the transformation when there are many SELECT statements in the procedure.

##### Transact-SQL

##### Multiple Resultset

Copy code

```
 CREATE PROCEDURE SOMEPROC()
AS
BEGIN
        SELECT * from AdventureWorks.HumanResources.Department;
        SELECT * from AdventureWorks.HumanResources.Shift;
END
```

##### Output

| DepartmentID | Name | GroupName |
| --- | --- | --- |
| 1 | Engineering | Research and Development |
| 2 | Tool Design | Research and Development |
| 3 | Sales | Sales and Marketing |
| 4 | Marketing | Sales and Marketing |
| 5 | Purchasing | Inventory Management |
| 6 | Research and Development | Research and Development |
| 7 | Production | Manufacturing |
| 8 | Production Control | Manufacturing |
| 9 | Human Resources | Executive General and Administration |
| 10 | Finance | Executive General and Administration |
| 11 | Information Services | Executive General and Administration |
| 12 | Document Control | Quality Assurance |
| 13 | Quality Assurance | Quality Assurance |
| 14 | Facilities and Maintenance | Executive General and Administration |
| 15 | Shipping and Receiving | Inventory Management |
| 16 | Executive | Executive General and Administration |

Expand

Show lessSee more

| ShiftID | Name | StartTime | EndTime | ModifiedDate |
| --- | --- | --- | --- | --- |
| 1 | Day | 07:00:00 | 15:00:00 | 2008-04-30 00:00:00.000 |
| 2 | Evening | 15:00:00 | 23:00:00 | 2008-04-30 00:00:00.000 |
| 3 | Night | 23:00:00 | 07:00:00 | 2008-04-30 00:00:00.000 |

Expand

Show lessSee more

##### Snowflake SQL

##### Single Resultset

Copy code

```
CREATE OR REPLACE PROCEDURE SOMEPROC ()
RETURNS ARRAY
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
        DECLARE
                ProcedureResultSet1 VARCHAR;
                ProcedureResultSet2 VARCHAR;
                return_arr ARRAY := array_construct();
        BEGIN
                ProcedureResultSet1 := 'RESULTSET_' || REPLACE(UPPER(UUID_STRING()), '-', '_');
                CREATE OR REPLACE TEMPORARY TABLE IDENTIFIER(:ProcedureResultSet1) AS
                        SELECT
                                *
                        from
                                AdventureWorks.HumanResources.Department;
                return_arr := array_append(return_arr, :ProcedureResultSet1);
                ProcedureResultSet2 := 'RESULTSET_' || REPLACE(UPPER(UUID_STRING()), '-', '_');
                CREATE OR REPLACE TEMPORARY TABLE IDENTIFIER(:ProcedureResultSet2) AS
                        SELECT
                                *
                        from
                                AdventureWorks.HumanResources.Shift;
                return_arr := array_append(return_arr, :ProcedureResultSet2);
                --** SSC-FDM-0020 - MULTIPLE RESULT SETS ARE RETURNED IN TEMPORARY TABLES **
                RETURN return_arr;
        END;
$$;
```

##### Output

| DepartmentID | Name | GroupName |
| --- | --- | --- |
| 1 | Engineering | Research and Development |
| 2 | Tool Design | Research and Development |
| 3 | Sales | Sales and Marketing |
| 4 | Marketing | Sales and Marketing |
| 5 | Purchasing | Inventory Management |
| 6 | Research and Development | Research and Development |
| 7 | Production | Manufacturing |
| 8 | Production Control | Manufacturing |
| 9 | Human Resources | Executive General and Administration |
| 10 | Finance | Executive General and Administration |
| 11 | Information Services | Executive General and Administration |
| 12 | Document Control | Quality Assurance |
| 13 | Quality Assurance | Quality Assurance |
| 14 | Facilities and Maintenance | Executive General and Administration |
| 15 | Shipping and Receiving | Inventory Management |
| 16 | Executive | Executive General and Administration |

Expand

Show lessSee more

| ShiftID | Name | StartTime | EndTime | ModifiedDate |
| --- | --- | --- | --- | --- |
| 1 | Day | 07:00:00 | 15:00:00 | 2008-04-30 00:00:00.000 |
| 2 | Evening | 15:00:00 | 23:00:00 | 2008-04-30 00:00:00.000 |
| 3 | Night | 23:00:00 | 07:00:00 | 2008-04-30 00:00:00.000 |

Expand

Show lessSee more

### Known Issues

1. The query results should be accessed by using the IDs returned by the Stored Procedure

### Related EWIs

1. [SSC-FDM-0020](../../issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0020): Multiple result sets are returned in temporary tables.

## TOP

Applies to

- SQL Server
- Azure Synapse Analytics

### Description

Note

Some parts in the output code are omitted for clarity reasons.

Limits the rows returned in a query result set to a specified number of rows or percentage of rows. When you use `TOP` with the `ORDER BY` clause, the result set is limited to the first *N* number of ordered rows. Otherwise, `TOP` returns the first ***N*** number of rows in an undefined order. Use this clause to specify the number of rows returned from a `SELECT` statement. Or, use `TOP` to specify the rows affected by an `INSERT`, `UPDATE`, `MERGE`, or `DELETE` statement. ([Transact-SQL TOP documentation](https://learn.microsoft.com/en-us/sql/t-sql/queries/top-transact-sql?view=sql-server-ver16))

#### Syntax in Transact-SQL

Copy code

```
 TOP (expression) [PERCENT] [ WITH TIES ]
```

Note

To get more information about the **`TOP`** arguments please check the [Transact-SQL TOP documentation](https://learn.microsoft.com/en-us/sql/t-sql/queries/top-transact-sql?view=sql-server-ver16#arguments).

##### Syntax in Snowflake

Copy code

```
 TOP <n>
```

Note

To get more information about **`TOP`** arguments please check the [Snowflake TOP documentation](https://docs.snowflake.com/en/sql-reference/constructs/top_n#parameters).

### Sample Source Patterns

To execute correctly the following samples it is required run the next `CREATE TABLE` statement:

#### Transact-SQL

Copy code

```
 CREATE TABLE Cars(
    Model VARCHAR(15),
    Price MONEY,
    Color VARCHAR(10)
);

INSERT Cars VALUES ('sedan', 10000, 'red'),
('convertible', 15000, 'blue'),
('coupe', 20000, 'red'),
('van', 8000, 'blue'),
('sub', 8000, 'green');
```

##### Snowflake

Copy code

```
 CREATE OR REPLACE TABLE Cars (
    Model VARCHAR(15),
    Price NUMBER(38, 4),
    Color VARCHAR(10)
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
;

INSERT INTO Cars VALUES ('sedan', 10000, 'red'),
('convertible', 15000, 'blue'),
('coupe', 20000, 'red'),
('van', 8000, 'blue'),
('sub', 8000, 'green');
```

#### Common Case

##### Transact-SQL

##### Query

Copy code

```
 SELECT TOP(1) Model, Color, Price
FROM Cars
WHERE Color = 'red'
```

##### Result

| Model | Color | Price |
| --- | --- | --- |
| sedan | red | 10000.0000 |

Expand

Show lessSee more

##### Snowflake

##### Query

Copy code

```
 SELECT
TOP 1
Model,
Color,
Price
FROM
Cars
WHERE
Color = 'red';
```

##### Result

| MODEL | COLOR | PRICE |
| --- | --- | --- |
| sedan | red | 10,000 |

Expand

Show lessSee more

#### TOP using PERCENT

##### Transact-SQL

##### Query

Copy code

```
 SELECT TOP(50)PERCENT Model, Color, Price FROM Cars
```

##### Result

| Model | Color | Prices |
| --- | --- | --- |
| sedan | red | 10000.0000 |
| convertible | blue | 15000.0000 |
| coupe | green | 20000.0000 |

Expand

Show lessSee more

##### Snowflake

##### Query

Copy code

```
SELECT
TOP 50 !!!RESOLVE EWI!!! /*** SSC-EWI-0040 - THE 'TOP PERCENT' CLAUSE IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
Model,
Color,
Price
FROM
Cars;
```

##### Result

| MODEL | COLOR | PRICE |
| --- | --- | --- |
| sedan | red | 10,000 |
| convertible | blue | 15,000 |
| coupe | red | 20,000 |
| van | blue | 8,000 |
| sub | green | 8,000 |

Expand

Show lessSee more

Warning

Since `PERCENT` argument is not supported by Snowflake it is being removed from the `TOP` clause, that’s why the result of executing the query in Snowflake is not equivalent to Transact-SQL.

#### TOP WITH TIES

##### Transact-SQL

##### Query

Copy code

```
 SELECT TOP(50)PERCENT WITH TIES Model, Color, Price FROM Cars ORDER BY Price;
```

##### Result

| Model | Color | Price |
| --- | --- | --- |
| van | blue | 8000.0000 |
| sub | green | 8000.0000 |
| sedan | red | 10000.0000 |

Expand

Show lessSee more

##### Snowflake

##### Query

Copy code

```
 SELECT
 TOP 50 !!!RESOLVE EWI!!! /*** SSC-EWI-0040 - THE 'TOP PERCENT AND WITH TIES' CLAUSE IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
  Model,
  Color,
  Price
 FROM
  Cars
 ORDER BY Price;
```

##### Result

| MODEL | COLOR | PRICE |
| --- | --- | --- |
| sub | green | 8,000 |
| van | blue | 8,000 |
| sedan | red | 10,000 |
| convertible | blue | 15,000 |
| coupe | red | 20,000 |

Expand

Show lessSee more

Warning

Since `WITH TIES` argument is not supported by Snowflake it is being removed from the `TOP` clause, that’s why the result of executing the query in Snowflake is not equivalent to Transact-SQL.

### Known Issues

#### 1. PERCENT argument is not supported by Snowflake

Since the `PERCENT` argument is not supported by Snowflake it is being removed from the `TOP` clause and a warning is being added. Functional equivalence mismatches in the results could happen.

##### 2. WITH TIES argument is not supported by Snowflake

Since the `WITH TIES` argument is not supported by Snowflake it is being removed from the `TOP` clause and a warning is being added. Functional equivalence mismatches in the results could happen.

### Related EWIs

1. [SSC-EWI-0040](../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0040): Statement Not Supported.
