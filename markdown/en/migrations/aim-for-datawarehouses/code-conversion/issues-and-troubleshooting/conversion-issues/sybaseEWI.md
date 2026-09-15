# Code Conversion - Sybase IQ Issues

Note

**Conversion Scope**

For Sybase IQ, assessment and translation for TABLES, VIEWS, STORED PROCEDURES, and FUNCTIONS are currently supported. Although other types of statements are recognized, they are not fully supported.

This page provides a comprehensive reference for how Sybase IQ grammar elements are translated to Snowflake equivalents. In this translation reference, you will find code examples, functional equivalence results, key differences, recommendations, known issues, and descriptions of each transformation.

## SSC-EWI-SY0001

Unsupported default value in Snowflake.

### Severity

High

#### Description

Snowflake does not support the use of the following default values.

- CURRENT REMOTE USER
- LAST USER
- CURRENT PUBLISHER

#### Code Examples

##### Input Code:

##### Sybase

Copy code

```
 create table t1
(
  col1 varchar default current remote user,
  col2 varchar default last user,
  col3 varchar default current publisher
);
```

##### Generated Code:

##### Snowflake

Copy code

```
 CREATE OR REPLACE TABLE t1 (
  col1 VARCHAR default
                       !!!RESOLVE EWI!!! /*** SSC-EWI-SY0001 - UNSUPPORTED DEFAULT VALUE CURRENT REMOTE USER IN SNOWFLAKE ***/!!!
                       current remote user,
  col2 VARCHAR default
                       !!!RESOLVE EWI!!! /*** SSC-EWI-SY0001 - UNSUPPORTED DEFAULT VALUE LAST USER IN SNOWFLAKE ***/!!!
                       last user,
  col3 VARCHAR default
                       !!!RESOLVE EWI!!! /*** SSC-EWI-SY0001 - UNSUPPORTED DEFAULT VALUE CURRENT PUBLISHER IN SNOWFLAKE ***/!!!
                       current publisher
)
;
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-SY0002

Unsupported remote table syntax in Snowflake.

### Severity

High

#### Description

Sybase IQ remote table syntax is not supported in Snowflake.

#### Code Examples

##### Input Code:

##### Sybase

Copy code

```
 CREATE TABLE remote_data(
    remote_id INT
)
AT 'remote_server;remote_db;owner;remote_object';
```

##### Generated Code:

##### Snowflake

Copy code

```
 CREATE OR REPLACE TABLE remote_data (
    remote_id INT
)
    !!!RESOLVE EWI!!! /*** SSC-EWI-SY0002 - UNSUPPORTED REMOTE TABLE SYNTAX ***/!!!
AT 'remote_server;remote_db;owner;remote_object'
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "sybase",  "convertedOn": "07/02/2025",  "domain": "no-domain-provided" }}'
;
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-SY0003

Unsupported iq unique constraint in Snowflake.

### Severity

High

#### Description

The IQ UNIQUE constraint specifies an estimate of the number of distinct values in a column. Snowflake does not contain any constraint to emulate this functionality.

#### Code Examples

##### Input Code:

##### Sybase

Copy code

```
 CREATE TABLE T1 (
  DATA VARCHAR IQ UNIQUE(10)
)
;
```

##### Generated Code:

##### Snowflake

Copy code

```
 CREATE OR REPLACE TABLE T1 (
  DATA VARCHAR
  !!!RESOLVE EWI!!! /*** SSC-EWI-SY0003 - UNSUPPORTED IQ UNIQUE CONSTRAINT ***/!!!
              IQ UNIQUE(10)
);
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-SY0004

Unsupported Syntax Table function can’t receive a query as a parameter.

### Severity

High

#### Description

Snowflake does not support passing RESULTSET as parameter in a table-value function call.

#### Code Examples

##### Input Code:

##### Sybase

Copy code

```
 SELECT
*
FROM
MyProcedure(TABLE (SELECT * FROM TABLE1));
```

##### Generated Code:

##### Snowflake

Copy code

```
 SELECT
*
FROM
TABLE(MyProcedure(
!!!RESOLVE EWI!!! /*** SSC-EWI-SY0004 - UNSUPPORTED SYNTAX TABLE FUNCTION CAN'T RECEIVE A QUERY AS PARAMETER ***/!!!
TABLE(SELECT * FROM TABLE1)));
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-SY0005

Unsupported Syntax Table function can’t be used with over expression

### Severity

High

#### Description

Snowflake does not support windows specification on a table-value function call.

#### Code Examples

##### Input Code:

##### Sybase

Copy code

```
 SELECT * FROM
MyProcedure(
TABLE (SELECT * FROM TABLE1)
OVER (PARTITION BY Col1 ORDER BY Col2 DESC));
```

##### Generated Code:

##### Snowflake

Copy code

```
         SELECT
          *
        FROM
          TABLE(MyProcedure(
          !!!RESOLVE EWI!!! /*** SSC-EWI-SY0004 - UNSUPPORTED SYNTAX TABLE FUNCTION CAN'T RECEIVE A QUERY AS PARAMETER ***/!!!
          TABLE(
            SELECT
              *
            FROM
              TABLE1
          )
          !!!RESOLVE EWI!!! /*** SSC-EWI-SY0005 - UNSUPPORTED SYNTAX TABLE FUNCTION CAN'T BE USED WITH OVER EXPRESSION ***/!!!
          OVER (
          PARTITION BY
            Col1
          ORDER BY Col2 DESC)));
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-SY0006

Open string is not supported in Snowflake.

### Severity

High

#### Description

Snowflake does not support [OPENSTRING](https://help.sap.com/docs/SAP_IQ/a898e08b84f21015969fa437e89860c8/a7749cf084f21015b73b899c1520fb06.html#parameters) functionality.

#### Code Examples

##### Input Code:

##### Sybase

Copy code

```
 SELECT * FROM
OPENSTRING (FILE '/path/to/file.txt')
WITH (Col1 INT, Col2 VARCHAR(20)) AS OS;
```

##### Generated Code:

##### Snowflake

Copy code

```
 SELECT
*
FROM
!!!RESOLVE EWI!!! /*** SSC-EWI-SY0006 - OPEN STRING IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
OPENSTRING (FILE '/path/to/file.txt')
WITH (Col1 INT, Col2 VARCHAR(20)) AS OS;
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-SY0007

DML Derived Table not supported in Snowflake.

### Severity

High

#### Description

In Sybase, during execution, the DML statement specified in the dml-derived table is executed first, and the rows affected by that DML materialize into a temporary table whose columns are described by the REFERENCING clause. The temporary table represents the result set of dml-derived-table. Snowflake does not support this behavior.

#### Code Examples

##### Input Code:

##### Sybase

Copy code

```
 SELECT * FROM (INSERT INTO TABLE1 (Col1, Col2) VALUES (1, 'test')) REFERENCING (FINAL AS F);
SELECT * FROM (DELETE FROM TABLE1) REFERENCING (FINAL AS F);
SELECT * FROM (UPDATE TABLE1 SET A = 1) REFERENCING (FINAL AS F);
```

##### Generated Code:

##### Snowflake

Copy code

```
 SELECT
  *
FROM
  !!!RESOLVE EWI!!! /*** SSC-EWI-SY0007 - DML DERIVED TABLE NOT SUPPORTED IN SNOWFLAKE ***/!!!
  (
    INSERT INTO TABLE1 (Col1, Col2) VALUES (1, 'test')
  )
  REFERENCING
  (FINAL AS F);

SELECT
  *
FROM
  !!!RESOLVE EWI!!! /*** SSC-EWI-SY0007 - DML DERIVED TABLE NOT SUPPORTED IN SNOWFLAKE ***/!!!
  (
    DELETE FROM TABLE1
  )
  REFERENCING
  (FINAL AS F);

SELECT
  *
FROM
  !!!RESOLVE EWI!!! /*** SSC-EWI-SY0007 - DML DERIVED TABLE NOT SUPPORTED IN SNOWFLAKE ***/!!!
  (
    UPDATE TABLE1
      SET
        A = 1
  )
  REFERENCING
  (FINAL AS F);
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-SY0008

Contains clause not supported in Snowflake.

### Severity

High

#### Description

In Sybase the [CONTAINS](https://help.sap.com/docs/SAP_IQ/a898e08b84f21015969fa437e89860c8/a7749cf084f21015b73b899c1520fb06.html) clause following a table name to filter the table and return only those rows matching the full text query specified with contains-query. Every matching row of the table is returned together with a score column that can be referred to using score-correlation-name. Snowflake does not support this behavior.

#### Code Examples

##### Input Code:

##### Sybase

Copy code

```
 SELECT * FROM TABLE1 CONTAINS (TextColumn, 'search term') AS Score;
```

##### Generated Code:

##### Snowflake

Copy code

```
 SELECT
  *
FROM
  TABLE1
         !!!RESOLVE EWI!!! /*** SSC-EWI-SY0008 - CONTAINS CLAUSE NOT SUPPORTED IN SNOWFLAKE ***/!!!
         CONTAINS(TextColumn,'search term') AS Score;
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-SY0009

Key Join not supported in Snowflake.

### Severity

High

#### Description

Snowflake does not support KEY JOIN. When the ON CLAUSE is specified, the KEY keyword is removed and treated as an INNER JOIN.

#### Code Examples

##### Input Code:

##### Sybase

Copy code

```
 SELECT * FROM TABLE1 KEY JOIN Table2 ON Table1.ID = Table2.ID;
SELECT * FROM TABLE1 KEY JOIN Table2;
```

##### Generated Code:

##### Snowflake

Copy code

```
   SELECT
    *
  FROM
    TABLE1
    JOIN
      Table2
      ON Table1.ID = Table2.ID;

  SELECT
    *
  FROM
    TABLE1
    !!!RESOLVE EWI!!! /*** SSC-EWI-SY0009 - KEY JOIN NOT SUPPORTED IN SNOWFLAKE ***/!!!
    KEY JOIN
      Table2;
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-EWI-SY0010

The temporary option is not supported in Snowflake.

### Severity

High

#### Description

Snowflake does not support the SET TEMPORARY OPTION statement used in Sybase IQ to configure session-level options.

#### Code Examples

##### Input Code:

##### Sybase

Copy code

```
set temporary option chained = 'OFF'
```

##### Generated Code:

##### Snowflake

Copy code

```
--        !!!RESOLVE EWI!!! /*** SSC-EWI-SY0010 - THE TEMPORARY OPTION 'chained' IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
--        set temporary option chained = 'OFF'
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)
