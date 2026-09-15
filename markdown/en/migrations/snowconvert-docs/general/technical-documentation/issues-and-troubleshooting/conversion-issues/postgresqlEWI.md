# Code Conversion - PostgreSQL Issues

Note

**Conversion Scope**

For PostgreSQL, the assessment and translation capabilities primarily focus on TABLES and VIEWS.
While other types of ANSI-standard statements are recognized, they are not yet fully supported for conversion. The tool may identify them, but will not perform a complete translation for these unsupported code units.

## SSC-EWI-PG0001

Age is not supported on Snowflake

### Severity

Medium

#### Description

This error is added because the `age()` functionality is not supported.

#### Code Example

##### Input Code:

##### PostgreSQL

Copy code

```
 SELECT
   age(date1::date, date2::date)
FROM
   Table1;
```

##### Generated Code:

##### Snowflake

Copy code

```
 --** SSC-FDM-0007 - MISSING DEPENDENT OBJECTS "age", "Table1" **
SELECT
   !!!RESOLVE EWI!!! /*** SSC-EWI-PG0001 - AGE IS NOT SUPPORTED ON SNOWFLAKE. ***/!!!
   AGE(date1::date, date2::date)
FROM
   Table1;
```

#### Best Practices

- The `Datediff` time function can solve some cases where the objective of the query is to obtain a specific range of values but this has to be handled manually for each scenario. For more information please refer to the Snowflake documentation about [Datediff](https://docs.snowflake.com/en/sql-reference/functions/datediff.html).
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-PG0002

Constraint index parameter not supported

### Severity

Low

#### Description

The use of the following index parameters in constraints are not supported by Snowflake.

- INCLUDE
- WITH
- USING INDEX TABLESPACE

#### Code Example

##### Input Code:

##### PostgreSQL

Copy code

```
 CREATE TABLE Table1 (
    code        char(5),
    date_prod   date,
    CONSTRAINT production UNIQUE(date_prod) INCLUDE(code)
);

CREATE TABLE Table2 (
    name    varchar(40),
    UNIQUE(name) WITH (fillfactor=70)
);

CREATE TABLE Table3 (
    name    varchar(40),
    PRIMARY KEY(name) USING INDEX TABLESPACE tablespace_name
);
```

##### Generated Code:

##### Snowflake

Copy code

```
 CREATE TABLE Table1 (
    code        char(5),
    date_prod   date,
    CONSTRAINT production UNIQUE(date_prod)
                                            !!!RESOLVE EWI!!! /*** SSC-EWI-PG0002 - INCLUDE PARAMETER NOT APPLICABLE. CONSTRAINT INDEX PARAMETERS ARE NOT SUPPORTED IN SNOWFLAKE. ***/!!! INCLUDE(code)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "postgresql",  "convertedOn": "09/17/2024" }}';

CREATE TABLE Table2 (
    name    varchar(40),
    UNIQUE(name)
                 !!!RESOLVE EWI!!! /*** SSC-EWI-PG0002 - WITH PARAMETER NOT APPLICABLE. CONSTRAINT INDEX PARAMETERS ARE NOT SUPPORTED IN SNOWFLAKE. ***/!!! WITH (fillfactor=70)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "postgresql",  "convertedOn": "09/17/2024" }}';

CREATE TABLE Table3 (
    name    varchar(40),
    PRIMARY KEY(name)
                      !!!RESOLVE EWI!!! /*** SSC-EWI-PG0002 - USING PARAMETER NOT APPLICABLE. CONSTRAINT INDEX PARAMETERS ARE NOT SUPPORTED IN SNOWFLAKE. ***/!!! USING INDEX TABLESPACE tablespace_name
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "postgresql",  "convertedOn": "09/17/2024" }}';
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-PG0003

Inheritance not supported

### Severity

Low

#### Description

Inheritance between tables is allowed in PostgreSQL, but Snowflake does not support it. For more information about inheritance in PostgreSQL click [here](https://www.postgresql.org/docs/current/ddl-inherit.html).

#### Code Example

##### Input Code:

##### PostgreSQL

Copy code

```
 ALTER TABLE Table1
ADD CONSTRAINT const3 UNIQUE (zip);
```

##### Generated Code:

##### Snowflake

Copy code

```
 !!!RESOLVE EWI!!! /*** SSC-EWI-PG0003 - TABLE INHERITANCE IS NOT SUPPORTED IN SNOWFLAKE. ***/!!!
ALTER TABLE Table1
ADD CONSTRAINT const3 UNIQUE (zip);
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-PG0004

Exclude constraint not supported

### Severity

Medium

#### Description

The exclude constraint used in PostgreSQL is not supported by Snowflake.

#### Code Example

##### Input Code:

##### PostgreSQL

Copy code

```
 CREATE TABLE Table1 (
    id      int,
    EXCLUDE USING gist (id WITH &&)
);
```

##### Generated Code:

##### Snowflake

Copy code

```
 CREATE TABLE Table1 (
    id      int,
    !!!RESOLVE EWI!!! /*** SSC-EWI-PG0004 - EXCLUDE CONSTRAINT IS NOT SUPPORTED IN SNOWFLAKE. ***/!!!
    EXCLUDE USING gist (id WITH &&)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "postgresql",  "convertedOn": "09/17/2024" }}';
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-PG0006

Reference to a variable using the Label is not supported by Snowflake.

### Severity

Medium

#### Description

This error is added when a FOR loop’s body references a variable using the label. Snowflake does not support referencing a variable using the qualified name.

#### Code Example

##### Input Code:

##### PostgreSQL

Copy code

```
 CREATE OR REPLACE PROCEDURE procedure1(out result VARCHAR(100))
LANGUAGE plpgsql
AS $$
BEGIN
result := '<';
<<outer_loop>>
for i in 1..3 loop
  <<inner_loop>>
  for i in 4..6 loop
  result := result || '(' || outer_loop.i || ', ' || i || ')';
  end loop inner_loop;
end loop outer_loop;
result := result || '>';
END;
$$;
```

##### Generated Code:

##### Snowflake

Copy code

```
 CREATE OR REPLACE PROCEDURE procedure1 (result OUT VARCHAR(100))
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "postgresql",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
AS $$
BEGIN
result := '<';
for i in 1 TO 3
                --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
                loop
  for i in 4 TO 6
                  --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
                  loop
  result := result || '(' ||
                             !!!RESOLVE EWI!!! /*** SSC-EWI-PG0006 - REFERENCE TO A VARIABLE USING THE LABEL IS NOT SUPPORTED BY SNOWFLAKE. ***/!!! outer_loop.i || ', ' || i || ')';
  end loop inner_loop;
end loop outer_loop;
result := result || '>';
END;
$$;
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-PG0007

Into clause in Dynamic SQL is not support in Snowflake

### Severity

Low

#### Description

PostgreSQL Dynamic SQL allows the `INTO` clause to store query results in variables. Snowflake does not support this functionality. Therefore, the `INTO` clause will be flagged with an EWI’.

#### Code Example

##### Input Code:

##### PostgreSQL

Copy code

```
 CREATE OR REPLACE PROCEDURE get_max_id(table_name VARCHAR, OUT max_id INTEGER)
AS $$
DECLARE
    sql_statement VARCHAR;
BEGIN
    sql_statement := 'SELECT MAX(id) FROM ' || table_name || ';';
    EXECUTE sql_statement INTO max_id;
END;
$$ LANGUAGE plpgsql;
```

##### Generated Code:

##### Snowflake

Copy code

```
 CREATE OR REPLACE PROCEDURE get_max_id (table_name VARCHAR, max_id OUT INTEGER)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "postgresql",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
AS $$
DECLARE
    sql_statement VARCHAR;
BEGIN
    sql_statement := 'SELECT MAX(id) FROM ' || table_name || ';';
    EXECUTE IMMEDIATE sql_statement
                                    !!!RESOLVE EWI!!! /*** SSC-EWI-PG0007 - INTO CLAUSE IN DYNAMIC SQL IS NOT SUPPORTED IN SNOWFLAKE. ***/!!! INTO max_id;
END;
$$;
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-PG0008

The use of interval within a to\_char function is not compatible with Snowflake.

### Severity

High

#### Description

The use of `interval` within the `to_char` to convert date/times data types into text is not supported in Snowflake.

#### Code Example

##### Input Code:

##### PostgreSQL

Copy code

```
 SELECT to_char(interval '15h 2m 12s', 'HH24:MI:SS');
```

##### Generated Code:

##### Snowflake

Copy code

```
 SELECT to_char(INTERVAL '15h, 2m, 12s', 'HH24:MI:SS') !!!RESOLVE EWI!!! /*** SSC-EWI-PG0008 - THE USE OF INTERVAL WITHIN TO_CHAR IS NOT SUPPORTED BY SNOWFLAKE. ***/!!!;
```

For more information please refer to

- PostgreSQL [to\_char](https://www.postgresql.org/docs/15/functions-formatting.html).
- Snowflake [to\_char](https://docs.snowflake.com/en/sql-reference/functions/to_char).

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-PG0009

Comment on ‘Type’ is not supported by Snowflake.

### Severity

Low

#### Description

In the original code, there are various objects that can receive comments. However, in Snowflake, several of these objects do not exist, and thus, comments cannot be assigned to them. The code for handling these scenarios is commented out to prevent any potential errors.

#### Code Example

##### Input Code:

##### PostgreSQL

Copy code

```
 COMMENT ON RULE rule_name on TABLE_NAME IS 'this is a comment';
```

##### Generated Code:

##### Snowflake

Copy code

```
 !!!RESOLVE EWI!!! /*** SSC-EWI-PG0009 - COMMENT ON 'RULE' IS NOT SUPPORTED BY SNOWFLAKE. ***/!!!
COMMENT ON RULE rule_name on TABLE_NAME IS 'this is a comment';
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-PG0010

Create temporary sequence is not supported by Snowflake

### Severity

Low

#### Description

When a temporary sequence is created in PostgreSQL, it is only created for the active session and is automatically deleted when you log out of the session. However, this functionality is not available in Snowflake, so it is generated as a normal sequence. When executed, a similar sequence name may already exist, which will cause an error for an existing object.

#### Code Example

##### Input code:

##### PostgreSQL

Copy code

```
 CREATE TEMPORARY SEQUENCE sequence1;
CREATE TEMP SEQUENCE sequence2;
```

##### Generated Code:

##### Snowflake

Copy code

```
 --** SSC-FDM-PG0009 - THE SEQUENCE NEXTVAL PROPERTY SNOWFLAKE DOES NOT GUARANTEE GENERATING SEQUENCE NUMBERS WITHOUT GAPS. **
CREATE TEMPORARY !!!RESOLVE EWI!!! /*** SSC-EWI-PG0010 - CREATE TEMPORARY SEQUENCE IS NOT SUPPORTED BY SNOWFLAKE. ***/!!! SEQUENCE sequence1;

--** SSC-FDM-PG0009 - THE SEQUENCE NEXTVAL PROPERTY SNOWFLAKE DOES NOT GUARANTEE GENERATING SEQUENCE NUMBERS WITHOUT GAPS. **
 CREATE TEMP !!!RESOLVE EWI!!! /*** SSC-EWI-PG0010 - CREATE TEMPORARY SEQUENCE IS NOT SUPPORTED BY SNOWFLAKE. ***/!!! SEQUENCE sequence2;
```

### Best Practices

- If you have a creation problem, you can try to rename the sequence to avoid collisions.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-PG0011

The sequence option ‘option\_name’ is not supported by Snowflake.

### Severity

Low

#### Description

Some options available in PostgreSQL for the sequence statement are not supported by Snowflake.

The unsupported options are:

- Unlogged.
- AS &lt;data\_type>.
- MinValue.
- MaxValue.
- No MinValue.
- No MaxValue.
- Cache.
- Cycle.
- Owner By.

#### Code Example

##### Input code:

##### PostgreSQL

Copy code

```
 CREATE UNLOGGED SEQUENCE sequence_name;
```

##### Generated Code:

##### Snowflake

Copy code

```
 --** SSC-FDM-PG0009 - THE SEQUENCE NEXTVAL PROPERTY SNOWFLAKE DOES NOT GUARANTEE GENERATING SEQUENCE NUMBERS WITHOUT GAPS. **
CREATE UNLOGGED !!!RESOLVE EWI!!! /*** SSC-EWI-PG0011 - 'UNLOGGED' IS NOT SUPPORTED BY SNOWFLAKE. ***/!!! SEQUENCE sequence_name;
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-PG0012

NOT VALID constraint option is not supported by Snowflake.

### Description

The [`NOT VALID`](https://www.postgresql.org/docs/current/sql-altertable.html#SQL-ALTERTABLE-DESC-ADD-TABLE-CONSTRAINT) constraint option is used in the context of adding or altering a constraint to indicate that the constraint should be added or modified without checking the existing data for compliance with the constraint. This clause is not supported by Snowflake.

#### Code Example

##### Input Code:

##### PostgreSQL

Copy code

```
 ALTER TABLE Table1 *
ADD CONSTRAINT const UNIQUE (zip) NOT VALID;
```

##### Generated Code:

##### Snowflake

Copy code

```
 ALTER TABLE Table1
ADD CONSTRAINT const UNIQUE (zip)
                                  !!!RESOLVE EWI!!! /*** SSC-EWI-PG0012 - NOT VALID CONSTRAINT OPTION IS NOT SUPPORTED BY SNOWFLAKE. ***/!!! NOT VALID;
```

#### Best Practices

- No additional user actions are required.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-PG0014

Snowflake scripting cursors do not support fetch orientation

### Severity

Medium

#### Description

In Snowflake, the [FETCH cursor](https://docs.snowflake.com/en/sql-reference/snowflake-scripting/fetch) statement always fetches the next row in the cursor. When transforming the code, cursor orientations that are equivalent to a FETCH NEXT will be transformed as they are functionally equivalent in Snowflake, namely:

- `FETCH NEXT`
- `FETCH FORWARD`
- `FETCH RELATIVE 1`
- `FETCH` (no orientation specified)

Any other orientation is unsupported and the FETCH statement will be marked with this EWI to reflect that.

#### Code Example

##### Input Code:

##### PostgreSQL

Copy code

```
 CREATE OR REPLACE PROCEDURE cursor_test()
AS $$
BEGIN
   FETCH FORWARD FROM cursor1 INTO my_var;
   FETCH FIRST FROM cursor1 INTO my_var;
   FETCH LAST FROM cursor1 INTO my_var;
END;
$$;
```

##### Generated Code:

##### Snowflake

Copy code

```
 CREATE OR REPLACE PROCEDURE cursor_test ()
RETURNS VARCHAR
AS $$
BEGIN
   FETCH
   	cursor1 INTO my_var;
   !!!RESOLVE EWI!!! /*** SSC-EWI-PG0014 - SNOWFLAKE SCRIPTING CURSORS DO NOT SUPPORT FETCH ORIENTATION. ***/!!!
   FETCH FIRST FROM cursor1 INTO my_var;
   !!!RESOLVE EWI!!! /*** SSC-EWI-PG0014 - SNOWFLAKE SCRIPTING CURSORS DO NOT SUPPORT FETCH ORIENTATION. ***/!!!
   FETCH LAST FROM cursor1 INTO my_var;
END;
$$;
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-PG0015

Fetch cursor without target variables is not supported in Snowflake

### Severity

Medium

#### Description

In PostgreSQL, it is possible to use a [FETCH statement](https://www.postgresql.org/docs/current/sql-fetch.html) without INTO to print on the console the values of fetched rows. However, Snowflake requires the [FETCH statement](https://docs.snowflake.com/en/sql-reference/snowflake-scripting/fetch) to specify the INTO clause with the variables where the fetched row values are going to be stored.

Whenever a FETCH with no INTO is found in the code, this EWI will be generated to notify the user that this type of FETCH is not supported.

#### Code Example

##### Input Code:

##### PostgreSQL

Copy code

```
 FETCH PRIOR FROM cursor1;
```

##### Generated Code:

##### Snowflake

Copy code

```
 !!!RESOLVE EWI!!! /*** SSC-EWI-PG0015 - FETCH CURSOR WITHOUT TARGET VARIABLES IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
FETCH PRIOR FROM cursor1;
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-PG0016

Bit String Type converted to Varchar Type

### Severity

Low

#### Description

When migrating from PostgreSQL, be aware that its BIT String Types and related functions are not natively supported in Snowflake. These data types will be converted to Snowflake’s VARCHAR. This conversion means that any PostgreSQL queries or application logic that depend on bitwise operations on these columns will require significant modification to achieve the same functionality in Snowflake.

#### Code Example

##### Input Code:

##### PostgreSQL

Copy code

```
 CREATE TABLE table1 (
   col1 bit(10)
);
```

##### Generated Code:

##### Snowflake

Copy code

```
 CREATE TABLE table1 (
   col1 CHARACTER(10) !!!RESOLVE EWI!!! /*** SSC-EWI-PG0016 - BIT DATA TYPE CONVERTED TO CHARACTER ***/!!!
);
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-PG0017

Transformation for routine body literal is not supported.

### Severity

Low

#### Description

Transformation for quoted literal routine body is not supported. Use the arrange option - prompt the Snowflake AIM Agent for Data Warehouses to arrange the code before its translation to modify it to dollar routine body.

#### Code Example

##### Input Code:

##### PostgreSQL

Copy code

```
CREATE OR REPLACE PROCEDURE proc1 (x varchar default 'pigs')
LANGUAGE plpgsql
AS
'
begin
    --test
   insert into tabletest2 values (`Dianne''s pigs`);
   x = ''Diannes pigs'';
end;
';
```

##### Generated Code:

##### Snowflake

Copy code

```
CREATE OR REPLACE PROCEDURE proc1 (x varchar default 'pigs' !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'ParameterDefaultExpr' NODE ***/!!!)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "postgresql",  "convertedOn": "01/13/2026",  "domain": "no-domain-provided",  "migrationid": "m7mbAfEK5XyHKQR4pRek1g==" }}'
EXECUTE AS CALLER
AS
   !!!RESOLVE EWI!!! /*** SSC-EWI-PG0017 - TRANSFORMATION FOR ROUTINE BODY LITERAL IS NOT SUPPORTED. USE ARRANGE OPTION. ***/!!!
'
begin
    --test
   insert into tabletest2 values (`Dianne''s pigs`);
   x = ''Diannes pigs'';
end;
';
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-PG0018

Python code is not transformed, review the function body to ensure it is Snowflake ready

Note

This EWI is deprecated; please refer to [SSC-FDM-PG0019](../functional-difference/postgresqlFDM#ssc-fdm-pg0019) for the latest version of this issue.

### Severity

Medium

#### Description

Python code in function bodies is not transformed. The Python code is passed through unchanged. Review the function body to ensure it is Snowflake-ready before deployment.

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

##### Generated Code:

##### Snowflake

Copy code

```
 !!!RESOLVE EWI!!! /*** SSC-EWI-PG0018 - SNOWCONVERT AI DOES NOT TRANSFORM PYTHON CODE, REVIEW THE FUNCTION BODY TO ENSURE IT IS SNOWFLAKE READY ***/!!!
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

- Review all Python code in function bodies for Snowflake compatibility.
- If the function uses Python syntax that requires preprocessing, use the arrange option - prompt the Snowflake AIM Agent for Data Warehouses to arrange the code before its translation to modify it to dollar routine body
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-PG0019

Python code parsing is not supported, use the arrange option to enable Python code preprocessing

### Severity

Low

#### Description

Parsing Python code in function bodies is not supported. When the arrange option is not activated, Python syntax may not be recognized, and the code may be commented out or left unprocessed. Use the arrange option to enable Python code preprocessing before conversion.

#### Code Example

##### Input Code:

##### PostgreSQL

Copy code

```
 CREATE FUNCTION pymax (a integer, b integer)
  RETURNS integer
AS $$
  if a > b:
    return a
  return b
$$ LANGUAGE plpythonu;
```

##### Generated Code:

##### Snowflake

Copy code

```
 !!!RESOLVE EWI!!! /*** SSC-EWI-PG0019 - SNOWCONVERT AI DOES NOT SUPPORT PYTHON CODE PARSING, USE THE ARRANGE OPTION TO ENABLE PYTHON CODE PREPROCESSING ***/!!!
CREATE FUNCTION pymax (a integer, b integer)
RETURNS integer
LANGUAGE PYTHON
RUNTIME_VERSION = '3.13'
HANDLER = 'main_py'
AS
  $$
-- ** SSC-EWI-0001 - UNRECOGNIZED TOKEN ON SOME LINE OF THE SOURCE CODE. LAST MATCHING TOKEN WAS 'if' ON LINE '4' COLUMN '3'. **
--  if a > b:
--    return a
--  return b
  $$
;
```

#### Best Practices

- Enable the arrange option before conversion to preprocess Python code.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-PG0020

ROWID pseudo-column is not supported in Snowflake

### Severity

Medium

#### Description

PostgreSQL-compatible sources can expose `ROWID` as a physical row-location pseudo-column. Snowflake has no equivalent pseudo-column, so SnowConvert AI preserves each reference and adds this EWI for replacement with a stable primary key or other logical identifier.

#### Code Example

##### Input Code:

##### PostgreSQL

Copy code

```
SELECT rowid FROM flat_smsn_optn_late_actv;
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT
  !!!RESOLVE EWI!!! /*** SSC-EWI-PG0020 - ROWID PSEUDOCOLUMN IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
  rowid
FROM
  flat_smsn_optn_late_actv;
```

#### Best Practices

- Replace `ROWID` references with a stable primary key or another logical row identifier.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)
