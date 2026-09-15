# Code Conversion - PostgreSQL Functional Differences

Note

For PostgreSQL, assessment and translation for TABLES and VIEWS are currently supported. Although other types of statements are recognized, they are not fully supported.

If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-PG0001

FOUND could have a different behavior in Snowflake in some scenarios.

### Severity

Low

#### Description

The FOUND property in PostgreSQL is a property based on the last executed query, it can be affected by some statements such as `INSERT`, `UPDATE`, `DELETE`, `MERGE`, `SELECT INTO`, `PERFORM`, `FETCH` and `FOR` loops. To read more details about this property, this is [PostgreSQL documentation](https://www.postgresql.org/docs/current/plpgsql-statements.html#PLPGSQL-STATEMENTS-DIAGNOSTICS).

In Snowflake there is not a direct translation for this property, for the following scenarios:

- `INSERT`
- `UPDATE`
- `DELETE`
- `MERGE`

The converted code will be `SQLFOUND` Snowflake property ([Here is the documentation](https://docs.snowflake.com/en/developer-guide/snowflake-scripting/dml-status)) since it behaves like the PostgreSQL `FOUND` property.

For the other cases such as:

- `SELECT INTO`
- `PERFORM`
- `FETCH`

The converted code will be a custom UDF (`IS_FOUND_UDF`) that behaves like the PostgreSQL `FOUND` property.

This happens because `SQLFOUND` changes its value only when at least one row is affected by the last executed query, if the last query does not change any row, it does not change.

While the `IS_FOUND_UDF` only works for statements that returns rows, if no row is returned it, it will return `FALSE`.

##### SQLFOUND Example

Copy code

```
INSERT INTO SampleTable (SampleColumn1)
VALUES ('SampleValue0.1');
```

The last query affects a table, so the `SQLFOUND` is the closest to the PostgreSQL functionality.

##### IS\_FOUND\_UDF Example

Copy code

```
SELECT SampleColumn FROM SampleTable;
```

The last query will return a row but does not change anything, so the `IS_FOUND_UDF()` is the closest to the PostgreSQL functionality.

##### IS\_FOUND\_UDF Source Code

Copy code

```
CREATE OR REPLACE FUNCTION FOUND_UDF()
RETURNS BOOLEAN
LANGUAGE SQL
IMMUTABLE
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "udf",  "convertedOn": "09/09/2024" }}'
AS
$$
SELECT (count(*) != 0) FROM TABLE(result_scan(last_query_id()))
$$;
```

#### Code Example

##### Insert Statement:

##### PostgreSQL

Copy code

```
-- Found property used with INSERT statement.
CREATE OR REPLACE PROCEDURE FoundUsingInsertProcedure()
LANGUAGE plpgsql
AS $$
BEGIN
    -- Insert into SampleTable
    INSERT INTO SampleTable (SampleColumn1)
    VALUES ('SampleValue0.1');

    SELECT FOUND;
END;
$$;
```

##### Snowflake

Copy code

```
-- Found property used with INSERT statement.
CREATE OR REPLACE PROCEDURE FoundUsingInsertProcedure ()
RETURNS VARCHAR
LANGUAGE SQL
AS $$
BEGIN
    -- Insert into SampleTable
    INSERT INTO SampleTable (SampleColumn1)
    VALUES ('SampleValue0.1');

    SELECT
        SQLFOUND /*** SSC-FDM-PG0001 - FOUND COULD HAVE A DIFFERENT BEHAVIOR IN SNOWFLAKE IN SOME SCENARIOS. ***/;
END;
$$;
```

##### Update Statement:

##### PostgreSQL

Copy code

```
 -- Found property used with UPDATE statement.
CREATE OR REPLACE PROCEDURE FoundUsingUpdateProcedure()
LANGUAGE plpgsql
AS
$$
    BEGIN
        UPDATE SampleTable
        SET SampleColumn1 = 'SampleValue0.1'
        WHERE SampleColumn1 = 'SampleValue0.1';
        SELECT FOUND;
    END;
$$;
```

##### Snowflake

Copy code

```
 -- Found property used with UPDATE statement.
CREATE OR REPLACE PROCEDURE FoundUsingUpdateProcedure ()
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
    BEGIN
        UPDATE SampleTable
        SET SampleColumn1 = 'SampleValue0.1'
        WHERE SampleColumn1 = 'SampleValue0.1';
        SELECT
        SQLFOUND /*** SSC-FDM-PG0001 - FOUND COULD HAVE A DIFFERENT BEHAVIOR IN SNOWFLAKE IN SOME SCENARIOS. ***/;
    END;
$$;
```

##### Delete Statement:

##### PostgreSQL

Copy code

```
 -- Found property used with DELETE statement.
CREATE OR REPLACE PROCEDURE FoundUsingDeleteProcedure()
LANGUAGE plpgsql
AS
$$
    BEGIN
        DELETE FROM SampleTable
        WHERE SampleColumn1 = 'SampleValue0.1';
        SELECT FOUND;
    END;
$$;
```

##### Snowflake

Copy code

```
 -- Found property used with DELETE statement.
CREATE OR REPLACE PROCEDURE FoundUsingDeleteProcedure ()
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
    BEGIN
        DELETE FROM
            SampleTable
        WHERE SampleColumn1 = 'SampleValue0.1';
        SELECT
        SQLFOUND /*** SSC-FDM-PG0001 - FOUND COULD HAVE A DIFFERENT BEHAVIOR IN SNOWFLAKE IN SOME SCENARIOS. ***/;
    END;
$$;
```

##### Merge Statement:

##### PostgreSQL

Copy code

```
 -- Found property used with MERGE statement.
CREATE OR REPLACE PROCEDURE FoundUsingMergeProcedure()
LANGUAGE plpgsql
AS
$$
    BEGIN
        MERGE INTO SampleTableB B
        USING (SELECT * FROM SampleTableA) A
        ON B.SampleColumn1 = A.SampleColumn2
        WHEN MATCHED THEN DELETE;
        SELECT FOUND;
    END;
$$;
```

##### Snowflake

Copy code

```
 -- Found property used with MERGE statement.
CREATE OR REPLACE PROCEDURE FoundUsingMergeProcedure ()
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
    BEGIN
        MERGE INTO SampleTableB B
        USING (SELECT * FROM SampleTableA) A
        ON B.SampleColumn1 = A.SampleColumn2
        WHEN MATCHED THEN DELETE !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'MergeStatement' NODE ***/!!!;
        SELECT
        SQLFOUND /*** SSC-FDM-PG0001 - FOUND COULD HAVE A DIFFERENT BEHAVIOR IN SNOWFLAKE IN SOME SCENARIOS. ***/;
    END;
$$;
```

##### Select Into Statement

##### PostgreSQL

Copy code

```
 -- Found property used with SELECT INTO statement.
CREATE OR REPLACE PROCEDURE FoundUsingSelectIntoProcedure()
LANGUAGE plpgsql
AS
$$
    DECLARE
        SampleNumber INTEGER;
    BEGIN
        SELECT 1 INTO SampleNumber;
        SELECT FOUND;
    END;
$$;
```

##### Snowflake

Copy code

```
 -- Found property used with SELECT INTO statement.
CREATE OR REPLACE PROCEDURE FoundUsingSelectIntoProcedure ()
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
    DECLARE
        SampleNumber INTEGER;
    BEGIN
        SELECT 1 INTO
        : SampleNumber;
        SELECT
        FOUND_UDF() /*** SSC-FDM-PG0001 - FOUND COULD HAVE A DIFFERENT BEHAVIOR IN SNOWFLAKE IN SOME SCENARIOS. ***/;
    END;
$$;
```

##### Perform Statement:

##### PostgreSQL

Copy code

```
 -- Found property used with PERFORM statement.
CREATE OR REPLACE PROCEDURE FoundUsingPerformProcedure()
LANGUAGE plpgsql
AS
$$
    BEGIN
        PERFORM 1;
        RETURN FOUND;
    END;
$$;
```

##### Snowflake

Copy code

```
 -- Found property used with PERFORM statement.
CREATE OR REPLACE PROCEDURE FoundUsingPerformProcedure ()
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
    BEGIN
    SELECT
        1;
    RETURN FOUND_UDF() /*** SSC-FDM-PG0001 - FOUND COULD HAVE A DIFFERENT BEHAVIOR IN SNOWFLAKE IN SOME SCENARIOS. ***/;
    END;
$$;
```

##### Fetch Statement:

##### PostgreSQL

Copy code

```
 -- Found property used with FETCH statement.
CREATE OR REPLACE PROCEDURE FoundUsingFetchProcedure ()
LANGUAGE plpgsql
AS
$$
    DECLARE
        SampleRow VARCHAR;
        SampleCursor CURSOR FOR SELECT EmptyColumn FROM EmptyTable;
    BEGIN
        OPEN SampleCursor;
        FETCH SampleCursor;
        CLOSE SampleCursor;
        SELECT FOUND;
    END;
$$;
```

##### Snowflake

Copy code

```
 -- Found property used with FETCH statement.
CREATE OR REPLACE PROCEDURE FoundUsingFetchProcedure ()
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
    DECLARE
        SampleRow VARCHAR;
        SampleCursor CURSOR FOR SELECT EmptyColumn FROM
        EmptyTable;
    BEGIN
        OPEN SampleCursor;
    !!!RESOLVE EWI!!! /*** SSC-EWI-PG0015 - FETCH CURSOR WITHOUT TARGET VARIABLES IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
        FETCH SampleCursor;
        CLOSE SampleCursor;
        SELECT
        FOUND_UDF() /*** SSC-FDM-PG0001 - FOUND COULD HAVE A DIFFERENT BEHAVIOR IN SNOWFLAKE IN SOME SCENARIOS. ***/;
    END;
$$;
```

## SSC-FDM-PG0002

Bpchar converted to varchar.

### Description

This warning is added because bpchar type (“blank-padded char”) may have some functional equivalence difference compared to the varchar data type in Snowflake. However, both data types can store the values up to the “n” length of characters and consume storage for only the amount of actual data stored. The main difference occurs when there are blanks at the end of the data, where bpchar does not store them but snowflake does.

For this reason, we can use the RTRIM function so that these blanks are not stored. But there may be cases where the functionality is not completely equivalent.

#### Code Example

##### Input Code:

##### Column Definition

Copy code

```
CREATE TABLE table1 (
    col1 BPCHAR,
    col2 BPCHAR(20)
);
```

##### Explicit Cast

Copy code

```
SELECT 'Y'::BPCHAR;
SELECT 'Y   '::BPCHAR(20);
SELECT COL1::BPCHAR(20) FROM tbl;
```

##### Generated Code:

##### Column Definition

Copy code

```
CREATE TABLE table1 (
    col1 VARCHAR /*** SSC-FDM-PG0002 - BPCHAR CONVERTED TO VARCHAR. THESE TYPES MAY HAVE SOME FUNCTIONAL DIFFERENCES. ***/,
    col2 VARCHAR(20) /*** SSC-FDM-PG0002 - BPCHAR CONVERTED TO VARCHAR. THESE TYPES MAY HAVE SOME FUNCTIONAL DIFFERENCES. ***/
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "postgresql",  "convertedOn": "09/17/2024" }}';
```

##### Explicit Cast

Copy code

```
SELECT 'Y':: VARCHAR /*** SSC-FDM-PG0002 - BPCHAR CONVERTED TO VARCHAR. THESE TYPES MAY HAVE SOME FUNCTIONAL DIFFERENCES. ***/;

SELECT
    RTRIM( 'Y   ') :: VARCHAR(20) /*** SSC-FDM-PG0002 - BPCHAR CONVERTED TO VARCHAR. THESE TYPES MAY HAVE SOME FUNCTIONAL DIFFERENCES. ***/;

SELECT
    RTRIM( COL1) :: VARCHAR(20) /*** SSC-FDM-PG0002 - BPCHAR CONVERTED TO VARCHAR. THESE TYPES MAY HAVE SOME FUNCTIONAL DIFFERENCES. ***/
FROM
    tbl;
```

#### Best Practices

- The **`rtrim`** function can resolve storage differences in case you want those blanks not to be stored. This case is handled in the [explicit cast](https://docs.snowflake.com/en/sql-reference/functions/cast.html), however, there may be other scenarios where it has to be handled manually. For more information refer to the Snowflake documentation about [RTRIM](https://docs.snowflake.com/en/sql-reference/functions/rtrim.html).

## SSC-FDM-PG0003

Bytea Converted To Binary

### Description

This warning is added because when the bytea data type is converted to binary the size limit is greatly reduced from 1GB to 8MB.

#### Code Example

##### Input Code:

Copy code

```
CREATE TABLE tbl(
    col BYTEA
);
```

##### Generated Code:

Copy code

```
CREATE TABLE tbl (
    col BINARY /*** SSC-FDM-PG0003 - BYTEA CONVERTED TO BINARY. SIZE LIMIT REDUCED FROM 1GB TO 8MB ***/
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "postgresql",  "convertedOn": "09/17/2024" }}';
```

#### Best Practices

- For more information refer to the Snowflake documentation about [Binary Data Type](https://docs.snowflake.com/en/sql-reference/data-types-text.html#binary).

## SSC-FDM-PG0004

The date output format may vary

### Description

The date output format may vary depending on the Timestamp type and the timestamp\_output\_format being used, see the [Snowflake CURRENT\_TIMESTAMP documentation](https://docs.snowflake.com/en/sql-reference/functions/current_timestamp.html).

#### Code Example

##### Input Code:

##### PostgreSQL

Copy code

```
CREATE TABLE table1 (
    dt_update timestamp without time zone DEFAULT clock_timestamp()
);
```

##### Generated Code:

##### Snowflake

Copy code

```
CREATE TABLE table1 (
    dt_update TIMESTAMP_NTZ DEFAULT CAST(
    --** SSC-FDM-PG0004 - THE DATE OUTPUT FORMAT MAY VARY DEPENDING ON THE TIMESTAMP TYPE AND THE TIMESTAMP_OUTPUT_FORMAT BEING USED. **
    CURRENT_TIMESTAMP() AS TIMESTAMP_NTZ)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "postgresql",  "convertedOn": "09/17/2024" }}';
```

### Samples

Example with CREATE TABLE.

#### Input Code:

##### PostgreSQL

Copy code

```
CREATE TABLE sample2 (
    platform_id integer NOT NULL,
    dt_update timestamp with time zone DEFAULT clock_timestamp()
);

insert into postgres.public.sample2 (platform_id) values (1);

select *, clock_timestamp() from postgres.public.sample2;
```

##### Results

| platform\_id | dt\_update | clock\_timestamp |
| --- | --- | --- |
| 1 | 2023-02-05 22:47:34.275 -0600 | 2023-02-05 23:16:15.754 -0600 |

Expand

Show lessSee more

##### Generated Code:

##### Snowflake

Copy code

```
CREATE TABLE sample2 (
    platform_id integer NOT NULL,
    dt_update TIMESTAMP_TZ DEFAULT CAST(
--** SSC-FDM-PG0004 - THE DATE OUTPUT FORMAT MAY VARY DEPENDING ON THE TIMESTAMP TYPE AND THE TIMESTAMP_OUTPUT_FORMAT BEING USED. **
CURRENT_TIMESTAMP() AS TIMESTAMP_TZ)
);

insert into postgres.public.sample2 (platform_id) values (1);
ALTER SESSION SET timestamp_output_format = 'YYYY-MM-DD HH24:MI:SS.FF';

select *,
CURRENT_TIMESTAMP(3)
from
postgres.public.sample2;
```

##### Results

| PLATFORM\_ID | DT\_UPDATE | CURRENT\_TIMESTAMP(3) |
| --- | --- | --- |
| 1 | 2023-02-05 20:52:30.082000000 | 2023-02-05 21:20:31.593 |

Expand

Show lessSee more

Example with SELECT with clock\_timestamp().

##### Input Code

##### PostgreSQL

Copy code

```
select clock_timestamp();
```

##### Results

| clock\_timestamp |
| --- |
| 2023-02-05 23:24:13.740 |

Expand

Show lessSee more

##### Generated Code

##### Snowflake

Copy code

```
ALTER SESSION SET timestamp_output_format = 'YYYY-MM-DD HH24:MI:SS.FF';
select
    CURRENT_TIMESTAMP(3);
```

##### Results

| CURRENT\_TIMESTAMP(3) |
| --- |
| 2023-02-05 21:29:24.258 |

Expand

Show lessSee more

## SSC-FDM-PG0005

UNLOGGED Table is not supported in Snowflake; data written may have different performance.

### Description

PostgreSQL’s `UNLOGGED` tables offer a significant speed advantage by skipping write-ahead logging (WAL). However, their data isn’t replicated to mirror instances. Snowflake doesn’t support this functionality, so the `UNLOGGED` clause will be commented out.

#### Code Example

##### Input Code:

##### PostgreSQL

Copy code

```
CREATE UNLOGGED TABLE TABLE1 (
   COL1 integer
);
```

##### Generated Code:

##### Snowflake

Copy code

```
CREATE
--       --** SSC-FDM-PG0005 - UNLOGGED TABLE IS NOT SUPPORTED IN SNOWFLAKE, DATA WRITTEN MAY HAVE DIFFERENT PERFORMANCE. **
--       UNLOGGED
                TABLE TABLE1 (
COL1 integer
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "greenplum",  "convertedOn": "04/21/2025",  "domain": "test" }}';
```

## SSC-FDM-PG0006

Set search path with multiple schemas.

### Description

Set search path with multiple schemas is not supported in Snowflake, see the [Snowflake USE SCHEMA documentation](https://docs.snowflake.com/en/sql-reference/sql/use-schema.html).

#### Code Example

##### Input Code:

##### PostgreSQL

Copy code

```
 SET SEARCH_PATH TO schema1, schema2, schema3;
```

##### Generated Code:

##### Snowflake

Copy code

```
 --** SSC-FDM-PG0006 - SET SEARCH PATH WITH MULTIPLE SCHEMAS IS NOT SUPPORTED IN SNOWFLAKE **
USE SCHEMA schema1 /*, schema2, schema3*/;
```

## SSC-FDM-PG0007

NULL is converted to ‘’ and may have a different behavior in Snowflake.

### Severity

Low

#### Description

In PostgreSQL the removal of a comment is handled by using the `NULL` term. However, in Snowflake, a similar method for removing a comment is to assign the value of an empty string `''` to provide the same result. This approach ensures that the comment is effectively mapped to an empty string with a similar behavior.

#### Code Example

##### Input Code:

##### PostgreSQL

Copy code

```
 COMMENT ON TABLE mytable IS NULL;
```

##### Generated Code:

##### Snowflake

Copy code

```
 COMMENT ON TABLE mytable IS '' /*** SSC-FDM-PG0007 - NULL IS CONVERTED TO '' AND MAY HAVE A DIFFERENT BEHAVIOR IN SNOWFLAKE. ***/;
```

## SSC-FDM-PG0008

Select into unlogged tables are not supported by Snowflake.

### Description

Select Into is not supported by Snowflake, this functionality was emulated with `CREATE TABLE AS`. In addition, Snowflake always uses transaction logs to protect tables and ensure data integrity and recoverability. Consequently, tables with the `UNLOGGED` option are not supported by Snowflake.

#### Code Example

##### Input Code:

##### PostgreSQL

Copy code

```
select column1
      into UNLOGGED NewTable
      from oldTable;
```

##### Generated Code:

##### Snowflake

Copy code

```
CREATE TABLE IF NOT EXISTS NewTable AS
      select column1
--      --** SSC-FDM-PG0008 - SELECT INTO UNLOGGED TABLES ARE NOT SUPPORTED BY SNOWFLAKE. **
--            into UNLOGGED NewTable
            from
            oldTable;
```

## SSC-FDM-PG0009

Sequence nextval property snowflake does not guarantee generating sequence numbers without gaps

### Description

Snowflake does not guarantee generating sequence numbers without gaps. The generated numbers consistently increase in value (or decrease in value if the step size is negative) but are not necessarily contiguous.

#### Code Example

##### Input Code:

##### PostgreSQL

Copy code

```
 SELECT nextval('seq1');
```

##### Generated Code:

##### Snowflake

Copy code

```
 SELECT seq1.nextval /*** SSC-FDM-PG0009 - THE SEQUENCE NEXTVAL PROPERTY SNOWFLAKE DOES NOT GUARANTEE GENERATING SEQUENCE NUMBERS WITHOUT GAPS. ***/;
```

## SSC-FDM-PG0010

Datatype of the left operand could not be determined. Results may vary due to the behavior of Snowflake’s bitwise function

### Description

The bitwise operators [`<<`](https://www.postgresql.org/docs/9.4/functions-bitstring.html) and [`>>`](https://www.postgresql.org/docs/9.4/functions-bitstring.html) are converted to the corresponding Snowflake functions [`BITSHIFTLEFT`](https://docs.snowflake.com/en/sql-reference/functions/bitshiftleft) and [`BITSHIFTRIGHT`](https://docs.snowflake.com/en/sql-reference/functions/bitshiftright). However, this transformation depends on knowing semantic information about the left operand, more specifically its datatype.

For shift operations involving integer left operands, the MOD function should be applied to the right operand to get equivalent results, as well as using the `INTEGER_BITSHIFTLEFT_UDF` helper for ensuring the equivalence of the shift left operation on integers. When the datatype of the left operand can not be determined, this FDM will be generated to warn about the potential functional differences.

#### Code Example

##### Input Code:

##### PostgreSQL

Copy code

```
CREATE TABLE someTable (
  intCol INTEGER,
  smallIntCol SMALLINT,
  varbyteCol VARBYTE,
  incrementValue INTEGER
)
;

SELECT
  intCol << incrementValue,
  smallIntCol >> incrementValue,
  varbyteCol << incrementValue
FROM someTable;

SELECT missingCol << incrementValue FROM missingTable;
```

##### Generated Code:

##### Snowflake

Copy code

```
CREATE TABLE someTable (
  intCol INTEGER,
  smallIntCol SMALLINT,
  varbyteCol BINARY,
  incrementValue INTEGER
)
;

SELECT
  PUBLIC.INTEGER_BITSHIFTLEFT_UDF(
  intCol, MOD(incrementValue, 32), 32),
  BITSHIFTRIGHT(
  smallIntCol, MOD(incrementValue, 16)),
  BITSHIFTLEFT(
  varbyteCol, incrementValue)
FROM
  someTable;

--** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "missingTable" **
SELECT
  --** SSC-FDM-PG0010 - DATATYPE OF THE LEFT OPERAND COULD NOT BE DETERMINED. RESULTS MAY VARY DUE TO THE BEHAVIOR OF SNOWFLAKE'S BITSHIFTLEFT BITWISE FUNCTION **
  BITSHIFTLEFT( missingCol, incrementValue) FROM
  missingTable;
```

#### Best Practices

- Ensure the source code you migrate has no missing depedencies, by providing any missing object so that the operands’ semantic information can be extracted correctly and this FDM should no longer appear

## SSC-FDM-PG0011

The use of the COLLATE column constraint has been disabled for this pattern-matching condition

### Description

This message is added when a pattern-matching condition uses arguments with COLLATE specifications, as they are not currently supported in Snowflake’s regular expression function. Consequently, the COLLATE clause must be disabled to use this function, which may result in differences in the results.

#### Code Example

##### Input Code:

##### PostgreSQL

Copy code

```
 CREATE TABLE collateTable (
col1 VARCHAR(20) COLLATE CASE_INSENSITIVE,
col2 VARCHAR(30) COLLATE CASE_SENSITIVE);

INSERT INTO collateTable values ('HELLO WORLD!', 'HELLO WORLD!');

SELECT
col1 SIMILAR TO 'Hello%' as ci,
col2 SIMILAR TO 'Hello%' as cs
FROM collateTable;
```

##### Results

| CI | CS |
| --- | --- |
| TRUE | FALSE |

Expand

Show lessSee more

**Output Code:**

##### Snowflake

Copy code

```
 CREATE TABLE collateTable (
col1 VARCHAR(20) COLLATE 'en-ci',
col2 VARCHAR(30) COLLATE 'en-cs'
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "postgresql",  "convertedOn": "01/16/2025",  "domain": "test" }}';

INSERT INTO collateTable
values ('HELLO WORLD!', 'HELLO WORLD!');

SELECT
RLIKE(COLLATE(
--** SSC-FDM-PG0011 - THE USE OF THE COLLATE COLUMN CONSTRAINT HAS BEEN DISABLED FOR THIS PATTERN-MATCHING CONDITION. **
col1, ''), 'Hello.*', 's') as ci,
RLIKE(COLLATE(
--** SSC-FDM-PG0011 - THE USE OF THE COLLATE COLUMN CONSTRAINT HAS BEEN DISABLED FOR THIS PATTERN-MATCHING CONDITION. **
col2, ''), 'Hello.*', 's') as cs
FROM
collateTable;
```

##### Results

| CI | CS |
| --- | --- |
| FALSE | FALSE |

Expand

Show lessSee more

#### Best Practices

- If you require equivalence for these scenarios, you can manually add the following parameters to the function to achieve functional equivalence:

  | Parameter | Description |
  | --- | --- |
  | `c` | Case-sensitive matching |
  | `i` | Case-insensitive matching |

  Expand

  Show lessSee more
- For more information please refer to the following [link](https://docs.snowflake.com/en/sql-reference/functions-regexp#specifying-the-parameters-for-the-regular-expression).

## SSC-FDM-PG0012

NOT NULL constraint has been removed. Assigning NULL to this variable will no longer cause a failure.

### Description

In PostgreSQL, specifying the NOT NULL constraint ensures that assigning a null value to a variable results in a runtime error. Since this clause does not exist in Snowflake, it is removed during transformation and assigning a NULL to this variable will no longer fail in execution.

#### Code Example

##### Input Code:

##### PostgreSQL

Copy code

```
 CREATE OR REPLACE PROCEDURE variable_Not_Null()
LANGUAGE plpgsql
AS $$
DECLARE
    v_notnull VARCHAR NOT NULL DEFAULT 'Test default';
BEGIN
    v_notnull := NULL;
    -- Procedure logic
END;
$$;
```

##### Result

Warning

[22004] ERROR: NULL cannot be assigned to variable “v\_notnull” declared NOT NULL

##### Generated Code:

##### Snowflake

Copy code

```
 CREATE OR REPLACE PROCEDURE variable_Not_Null ()
RETURNS VARCHAR
LANGUAGE SQL
AS $$
DECLARE
    --** SSC-FDM-PG0012 - NOT NULL CONSTRAINT HAS BEEN REMOVED. ASSIGNING NULL TO THIS VARIABLE WILL NO LONGER CAUSE A FAILURE. **
    v_notnull VARCHAR DEFAULT 'Test default';
BEGIN
    v_notnull := NULL;
    -- Procedure logic
END;
$$;
```

##### Result

Note

:class: tip
This assignment will not fail in Snowflake.

#### Best Practices

- Review the procedure logic to ensure this variable is not assigned a `NULL` value.

## SSC-FDM-PG0013

Function syntactically supported by Snowflake but may have functional differences

### Description

This functional difference message indicates that while Snowflake supports the function’s syntax (either directly or through an equivalent mapping), its behavior might be *different* from the original in some situations.

#### Code Example

##### Input Code:

##### PostgreSQL

Copy code

```
SELECT
    LISTAGG(skill) WITHIN GROUP (ORDER BY skill) OVER (PARTITION BY
    employee_name) AS employee_skills
FROM
    employees;
```

##### Generated Code:

##### Snowflake

Copy code

```
SELECT
--** SSC-FDM-PG0013 - FUNCTION SYNTACTICALLY SUPPORTED BY SNOWFLAKE BUT MAY HAVE FUNCTIONAL DIFFERENCES **
LISTAGG(skill) WITHIN GROUP (ORDER BY skill) OVER (PARTITION BY
employee_name) AS employee_skills
FROM
    employees;
```

#### Best Practices

- Carefully evaluate the functional behavior for unexpected results, as differences may only occur in specific scenarios.

## SSC-FDM-PG0014

Unknown Pseudotype transformed to Text Type

### Description

This functional difference message indicates that UNKNOWN Pseudo Type used in PostgreSQL is not supported in Snowflake and is transformed to a Text Type.

#### Code Example

##### Input Code:

##### PostgreSQL

Copy code

```
CREATE TABLE PSEUDOTYPES
(
  COL1 UNKNOWN
)
```

##### Generated Code:

##### Snowflake

Copy code

```
CREATE TABLE PSEUDOTYPES (
  COL1 TEXT /*** SSC-FDM-PG0014 -  UNKNOWN PSEUDOTYPE TRANSFORMED TO TEXT TYPE ***/
)
```

#### Best Practices

- Carefully evaluate the usages for the columns with Unknown Data Types, as differences may occur in specific scenarios.

## SSC-FDM-PG0015

PSQL command is not applicable in Snowflake

### Description

In Snowflake, **PSQL commands are not applicable.** While no longer needed for execution, the original PSQL command is retained as a comment.

#### Example Code

##### Input Code:

Copy code

```
 \set ON_ERROR_STOP TRUE
```

##### Generated Code:

Copy code

```
 ----** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE. COMMAND OPTION **
--\set ON_ERROR_STOP TRUE
```

## SSC-FDM-PG0016

Strongly typed array transformed to ARRAY without type checking.

### Description

This warning is added because PostgreSQL supports arrays of any built-in or user-defined base type, enum type, composite type, range type, or domain, whereas Snowflake does not. In Snowflake, each value in a semi-structured array is of type VARIANT.

#### Example Code

##### Input Code:

Copy code

```
CREATE TABLE sal_emp (
    name            text,
    pay_by_quarter  integer[],
    schedule        text[][]
);
```

##### Generated Code:

Copy code

```
CREATE TABLE sal_emp (
    name            text,
    pay_by_quarter ARRAY /*** SSC-FDM-PG0016 - STRONGLY TYPED ARRAY 'INTEGER[]' TRANSFORMED TO ARRAY WITHOUT TYPE CHECKING ***/,
    schedule ARRAY /*** SSC-FDM-PG0016 - STRONGLY TYPED ARRAY 'TEXT[][]' TRANSFORMED TO ARRAY WITHOUT TYPE CHECKING ***/
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "postgresql",  "convertedOn": "06/03/2025",  "domain": "no-domain-provided" }}';
```

## SSC-FDM-PG0017

User Defined function that returns a void was transformed to a Snowflake procedure.

### Description

A warning is generated for any function that returns void. This is because functions returning void typically indicate a procedure rather than a value-producing operation, which can sometimes require special handling during conversion.

#### Example Code

##### Input Code:

Copy code

```
CREATE OR REPLACE FUNCTION log_user_activity(
    user_id_param INT,
    action_param TEXT
)
RETURNS VOID AS $$
BEGIN
    INSERT INTO user_activity_log (user_id, action, activity_timestamp)
    VALUES (user_id_param, action_param, NOW());
END;
$$ LANGUAGE plpgsql;
```

##### Generated Code:

Copy code

```
--** SSC-FDM-PG0017 - USER DEFINED FUNCTION THAT RETURNS VOID WAS TRANSFORMED TO SNOWFLAKE PROCEDURE **
CREATE OR REPLACE PROCEDURE log_user_activity (
user_id_param INT,
    action_param TEXT)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "postgresql",  "convertedOn": "07/23/2025",  "domain": "no-domain-provided" }}'
AS $$
BEGIN
    INSERT INTO user_activity_log (user_id, action, activity_timestamp)
    VALUES (:user_id_param, : action_param, CURRENT_TIMESTAMP());
END;
$$;
```

## SSC-FDM-PG0018

Analyze statement is commented out, which is not applicable in Snowflake.

### Description

ANALYZE statements are flagged with a warning and commented out. While ANALYZE is used in PostgreSQL for collecting table statistics, Snowflake automatically manages this process, making the statement redundant and generally unnecessary post-conversion.

#### Example Code

##### Input Code:

Copy code

```
ANALYZE customers (first_name, last_name)
```

##### Generated Code:

Copy code

```
----** SSC-FDM-PG0018 - ANALYZE STATEMENT IS COMMENTED OUT, WHICH IS NOT APPLICABLE IN SNOWFLAKE. **
--ANALYZE customers (first_name, last_name)
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-PG0019

SnowConvert AI does not transform Python code, review the function body to ensure it is Snowflake ready

#### Description

SnowConvert AI preserves Python function bodies instead of translating their contents. The surrounding function declaration is converted for Snowflake, but the body must be reviewed for compatible runtime, handler, package, and API usage.

#### Code Example

##### Input Code:

##### PostgreSQL

Copy code

```
CREATE FUNCTION pymax (a integer, b integer)
  RETURNS integer
AS $$
  /*if a > b:
    return a
  return b*/
$$ LANGUAGE plpythonu;
```

##### Output Code:

##### Snowflake

Copy code

```
--** SSC-FDM-PG0019 - SNOWCONVERT AI DOES NOT TRANSFORM PYTHON CODE, REVIEW THE FUNCTION BODY TO ENSURE IT IS SNOWFLAKE READY **
CREATE FUNCTION pymax (a integer, b integer)
RETURNS integer
LANGUAGE PYTHON
RUNTIME_VERSION = '3.13'
HANDLER = 'main_py'
AS
  $$
  /*if a > b:
  return a
  return b*/
  $$
;
```

#### Best Practices

- Review all preserved Python code for Snowflake runtime, package, handler, and API compatibility.
- Use the arrange option when Python preprocessing is required.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)
