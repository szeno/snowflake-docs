# Code Conversion - IBM DB2 Functional Differences

## SSC-FDM-DB0001

FUNCTIONALITY MIGHT BE DIFFERENT DEPENDING ON THE DB2 DATABASE.

### Severity

Low

### Description

This message is shown whenever a SQL element behaves differently depending on the DB2 database version ([DB2 for i](https://www.ibm.com/docs/en/i/7.4?topic=database), [DB2 for z/OS](https://www.ibm.com/docs/en/db2-for-zos/12?topic=db2-sql), or [DB2 for Linux, Unix, and Windows](https://www.ibm.com/docs/en/db2/11.5?topic=database-fundamentals)). All DB2 versions are treated as one and therefore, the translation for the element might have functionality differences when compared to the original platform.

### Cases

Listed below are all the SQL elements so far identified, that behave differently depending on the DB2 database version.

#### CURRENT MEMBER

DB2 for z/OS: [CURRENT MEMBER](https://www.ibm.com/docs/en/db2-for-zos/11?topic=registers-current-member) specifies the member name of a current Db2 data sharing member on which a statement is executing. The value of CURRENT MEMBER is a character string.

Db2 for LUW: The [CURRENT MEMBER](https://www.ibm.com/docs/en/db2/11.5?topic=registers-current-member) special register specifies an INTEGER value that identifies the coordinator member for the statement.

##### Code example

##### Input code:

Copy code

```
 CREATE TABLE T1
(
  COL1 INT,
  COL2 CHAR(8) WITH DEFAULT CURRENT MEMBER
);
```

##### Output code:

Copy code

```
 CREATE TABLE T1
 (
  COL1 INT,
  COL2 CHAR(8) DEFAULT
  --** SSC-FDM-DB0001 - FUNCTIONALITY FOR CURRENT_ROLE MIGHT BE DIFFERENT DEPENDING ON THE DB2 DATABASE. **
  CURRENT_ROLE()
)
 COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/02/2025",  "domain": "no-domain-provided" }}';
```

### Recommendations

- Review your code and keep in mind that the result transformation can behave differently according to the Db2 version that is being used.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-DB0002

DECFLOAT TYPE CHANGED TO NUMBER BECAUSE IT IS ONLY SUPPORTED IN TABLE COLUMNS AND CAST EXPRESSIONS IN SNOWFLAKE.

### Severity

Low

### Description

This message is shown when a `DECFLOAT` data type is used in a context not supported by Snowflake. In Snowflake, `DECFLOAT` is only permitted in:

- Table column definitions (`CREATE TABLE`)
- `CAST` expressions (`CAST(value AS DECFLOAT)`)

When `DECFLOAT` is used in other contexts such as procedure parameters, function parameters, or local variable declarations, it is transformed to `NUMBER(38, 37)` and this FDM is added to indicate the functional difference.

### Code Example

#### DB2

Copy code

```
CREATE PROCEDURE TestProc (param1 DECFLOAT)
BEGIN
  DECLARE local_var DECFLOAT;
  SET local_var = param1;
END;
```

#### Snowflake

Copy code

```
CREATE OR REPLACE PROCEDURE TestProc (param1 NUMBER(38, 37) --** SSC-FDM-DB0002 - DECFLOAT TYPE CHANGED TO NUMBER BECAUSE IT IS ONLY SUPPORTED IN TABLE COLUMNS AND CAST EXPRESSIONS IN SNOWFLAKE. **
)
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
BEGIN
  LET local_var NUMBER(38, 37) --** SSC-FDM-DB0002 - DECFLOAT TYPE CHANGED TO NUMBER BECAUSE IT IS ONLY SUPPORTED IN TABLE COLUMNS AND CAST EXPRESSIONS IN SNOWFLAKE. **
  := NULL;
  local_var := param1;
END;
$$;
```

### Recommendations

- Review the converted code to ensure that using `NUMBER(38, 37)` instead of `DECFLOAT` does not affect your application logic.
- If precise decimal floating-point arithmetic is critical for these parameters or variables, consider refactoring your code to use table columns or `CAST` expressions where `DECFLOAT` is supported.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)
