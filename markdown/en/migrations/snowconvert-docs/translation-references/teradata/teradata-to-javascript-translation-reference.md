# Teradata - SQL to JavaScript (Procedures)

## GET DIAGNOSTICS EXCEPTION

Translation reference to convert Teradata GET DIAGNOSTICS EXCEPTION statement to Snowflake Scripting

### Description

> GET DIAGNOSTICS retrieves information about successful, exception, or completion conditions from the Diagnostics Area.

For more information, see the [Teradata GET DIAGNOSTICS documentation](https://docs.teradata.com/r/Teradata-VantageTM-SQL-Stored-Procedures-and-Embedded-SQL/March-2019/Condition-Handling/GET-DIAGNOSTICS).

Copy code

```
 GET DIAGNOSTICS
{
  [ EXCEPTION < condition_number >
    [ < parameter_name | variable_name > = < information_item > ]...
  ]
  |
  [ < parameter_name | variable_name > = < information_item > ]...
}
```

Note

Some parts of the output code are omitted for clarity reasons.

### Sample Source Patterns

#### Teradata

##### Query

Copy code

```
 -- Additional Params: -t JavaScript
CREATE PROCEDURE getDiagnosticsSample ()
BEGIN
    DECLARE V_MESSAGE, V_CODE VARCHAR(200);
    DECLARE V_Result INTEGER;
    SELECT c1 INTO V_Result FROM tab1;
    GET DIAGNOSTICS EXCEPTION 1 V_MESSAGE = MESSAGE_TEXT;
END;
```

##### Snowflake

##### Javascript

Copy code

```
 CREATE OR REPLACE PROCEDURE getDiagnosticsSample ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
EXECUTE AS CALLER
AS
$$
    // SnowConvert AI Helpers Code section is omitted.

    var V_MESSAGE;
    var V_CODE;
    var V_RESULT;
    EXEC(`SELECT c1 FROM tab1`,[]);
    [V_RESULT] = INTO();
    V_MESSAGE = MESSAGE_TEXT;
$$;
```

### Known Issues

1. **Unsupported condition attributes statements**
   1. CLASS\_ORIGIN
   2. CONDITION\_IDENTIFIER
   3. CONDITION\_NUMBER
   4. MESSAGE\_LENGTH
   5. RETURNED\_SQLSTATE
   6. SUBCLASS\_ORIGIN

### Related EWIs

No related EWIs.

## **If**

The transformation for the [IF statement](https://docs.teradata.com/reader/I5Vi6UNnylkj3PsoHlLHVQ/GOzyPogDqU7DWoFvg6YMCw) is:

**Teradata**

Copy code

```
 IF value = 2 THEN
```

**Snowflake**

Copy code

```
if (value == 2) {
}
```

## **Case**

The transformation for the [Case statement](https://docs.teradata.com/reader/I5Vi6UNnylkj3PsoHlLHVQ/nuR4riyH6QmcdmMu01TQEw) is:

**Teradata**

Copy code

```
 case value
when 0 then
  select * from table1
else
  update table1 set name = "SpecificValue" where id = value;
end case
```

**Snowflake**

Copy code

```
switch (value) {
  case 0:
    EXEC(`SELECT * FROM PUBLIC.table1`, []);
    break;
  default:
    EXEC(
      `UPDATE PUBLIC.table1 set name = "SpecificValue" where id = value`,
      [],
    );
    break;
}
```

## **Cursor Declare, OPEN, FETCH and CLOSE**

The transformation for [cursor statements](https://docs.teradata.com/reader/I5Vi6UNnylkj3PsoHlLHVQ/vLlfGRxfadgP4k0a~0jpkA) is:

**Teradata**

### Cursor

Copy code

```
 -- Additional Params: -t JavaScript
CREATE PROCEDURE procedure1()
DYNAMIC RESULT SETS 2
BEGIN

    -------- Local variables --------
    DECLARE sql_cmd VARCHAR(20000) DEFAULT ' ';
    DECLARE num_cols INTEGER;

    ------- Declare cursor with return only-------
    DECLARE resultset CURSOR WITH RETURN ONLY FOR firststatement;

    ------- Declare cursor -------
    DECLARE cur2 CURSOR FOR SELECT COUNT(columnname) FROM table1;

    -------- Set --------
    SET sql_cmd='sel * from table1';

    -------- Prepare cursor --------
    PREPARE firststatement FROM sql_cmd;

    -------- Open cursors --------
    OPEN resultset;
    OPEN cur1;

    -------- Fetch -------------
    FETCH cur1 INTO val1, val2;

    -------- Close cursor --------
    CLOSE cur1;
END;
```

**Snowflake**

#### JavaScript Cursor

Copy code

```
 CREATE OR REPLACE PROCEDURE procedure1 ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
EXECUTE AS CALLER
AS
$$
    // SnowConvert AI Helpers Code section is omitted.

    //------ Local variables --------
    var SQL_CMD = ` `;
    var NUM_COLS;
    var RESULTSET = new CURSOR(() => FIRSTSTATEMENT,[],true);
    //----- Declare cursor -------
    var CUR2 = new CURSOR(`SELECT COUNT(columnname) FROM table1`,[],false);
    //------ Set --------
    SQL_CMD = `SELECT * from table1`;
    //------ Prepare cursor --------
    var FIRSTSTATEMENT = SQL_CMD;
    //------ Open cursors --------
    RESULTSET.OPEN();
    CUR1.OPEN();
    //------ Fetch -------------
    CUR1.FETCH() && ([val1,val2] = CUR1.INTO());
    //------ Close cursor --------
    CUR1.CLOSE();
    return PROCRESULTS();
$$;
```

## **While**

The transformation for [while statement](https://docs.teradata.com/reader/I5Vi6UNnylkj3PsoHlLHVQ/fTCuW3l9hT6vtPc7V3QpcA) is:

**Teradata**

### While

Copy code

```
 while (counter < 10) do
    set counter = counter + 1;
```

### Snowflake

#### While

Copy code

```
 while ( counter < 10) {
    counter = counter + 1;
}
```

## **Security**

The transformation for [security statements](https://docs.teradata.com/reader/zzfV8dn~lAaKSORpulwFMg/knEJa8MckUZrAYquDblFAA) is:

| Teradata | Snowflake |
| --- | --- |
| SQL SECURITY CREATOR | EXECUTE AS OWNER |
| SQL SECURITY INVOKER | EXECUTE AS CALLER |
| SQL SECURITY DEFINER | EXECUTE AS OWNER |

Expand

Show lessSee more

## **FOR-CURSOR-FOR loop**

The transformation for [FOR-CURSOR-FOR loop](https://docs.teradata.com/reader/scPHvjfglIlB8F70YliLAw/YyY70D3vVqnHSAIE30t78g) is:

**Teradata**

### For-Cursor-For-Loop

Copy code

```
:force:
-- Additional Params: -t JavaScript
REPLACE PROCEDURE Database1.Proc1()
BEGIN
    DECLARE lNumber INTEGER DEFAULT 1;
    FOR class1 AS class2 CURSOR FOR
      SELECT COL0,
      TRIM(COL1) AS COL1ALIAS,
      TRIM(COL2),
      COL3
      FROM someDb.prefixCol
    DO
      INSERT INTO TempDB.Table1 (:lgNumber, :lNumber, (',' || :class1.ClassCD || '_Ind CHAR(1) NOT NULL'));
      SET lNumber = lNumber + 1;
    END FOR;
END;
```

**Snowflake**

#### JavaScript For-Cursor-For-Loop

Copy code

```
 CREATE OR REPLACE PROCEDURE Database1.Proc1 ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
EXECUTE AS CALLER
AS
$$
    // SnowConvert AI Helpers Code section is omitted.

    var LNUMBER = 1;
    /*** SSC-EWI-0023 - PERFORMANCE REVIEW - THIS LOOP CONTAINS AN INSERT, DELETE OR UPDATE STATEMENT ***/
    for(var CLASS2 = new CURSOR(`SELECT
   COL0,
   TRIM(COL1) AS COL1ALIAS,
   TRIM(COL2),
   COL3
FROM
   someDb.prefixCol`,[],false).OPEN();CLASS2.NEXT();) {
        let CLASS1 = CLASS2.CURRENT;
        EXEC(`INSERT INTO TempDB.Table1
VALUES (:lgNumber, :1, (',' || :
!!!RESOLVE EWI!!! /*** SSC-EWI-0026 - THE  VARIABLE class1.ClassCD MAY REQUIRE A CAST TO DATE, TIME OR TIMESTAMP ***/!!!
:2 || '_Ind CHAR(1) NOT NULL'))`,[LNUMBER,CLASS1.CLASSCD]);
        LNUMBER = LNUMBER + 1;
    }
    CLASS2.CLOSE();
$$;
```

*Note: The FOR loop present in the Teradata procedure is transformed to a FOR block in javascript that emulates its functionality.*

## **Procedure parameters and variables referenced inside statements**

The transformation for the procedure parameters and variables that are referenced inside the statements of the procedure is:

**Teradata**

### Parameters and variables

Copy code

```
 -- Additional Params: -t JavaScript
REPLACE PROCEDURE PROC1 (param1 INTEGER, param2 VARCHAR(30))
BEGIN
    DECLARE var1          VARCHAR(1024);
    DECLARE var2          SMALLINT;
    DECLARE weekstart date;
    set weekstart= '2019-03-03';
    set var1 = 'something';
    set var2 = 123;

    SELECT * FROM TABLE1 WHERE SOMETHING = :param1;
    SELECT * FROM TABLE1 WHERE var1 = var1 AND date1 = weekstart AND param2 = :param2;
    INSERT INTO TABLE2 (col1, col2, col3, col4, col5) VALUES (:param1, :param2, var1, var2, weekstart);
END;
```

**Snowflake**

#### JavaScript prameters and variables

Copy code

```
 CREATE OR REPLACE PROCEDURE PROC1 (PARAM1 FLOAT, PARAM2 STRING)
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
EXECUTE AS CALLER
AS
$$
    // SnowConvert AI Helpers Code section is omitted.

    var VAR1;
    var VAR2;
    var WEEKSTART;
    WEEKSTART = `2019-03-03`;
    VAR1 = `something`;
    VAR2 = 123;
    // ** SSC-EWI-0022 - ONE OR MORE IDENTIFIERS IN THIS STATEMENT WERE CONSIDERED PARAMETERS BY DEFAULT. REFERENCED TABLE NOT FOUND. **
    EXEC(`SELECT * FROM TABLE1 WHERE SOMETHING = :1`,[PARAM1]);
    // ** SSC-EWI-0022 - ONE OR MORE IDENTIFIERS IN THIS STATEMENT WERE CONSIDERED PARAMETERS BY DEFAULT. REFERENCED TABLE NOT FOUND. **
    EXEC(`SELECT * FROM TABLE1 WHERE :1 = :1 AND date1 = :2 AND param2 = :3`,[VAR1,WEEKSTART,PARAM2]);
    // ** SSC-EWI-0022 - ONE OR MORE IDENTIFIERS IN THIS STATEMENT WERE CONSIDERED PARAMETERS BY DEFAULT. REFERENCED TABLE NOT FOUND. **
    EXEC(`INSERT INTO TABLE2 (col1, col2, col3, col4, col5) VALUES (:1, :2, :3, :4, :5)`,[PARAM1,PARAM2,VAR1,VAR2,WEEKSTART]);
$$;
```

*Note: Whenever a procedure parameter or a variable declared inside the procedure is referenced inside a Teradata statement that has to be converted,* *this reference is escaped from the resulting text to preserve the original reference’s functionality.*

## **Leave**

In Javascript, it’s possible to use `break` with an additional parameter, thus emulating the behavior of a Teradata `LEAVE` jump.

Labels can also be emulated by using Javascript Labeled Statements.

The transformation for [LEAVE statement](https://docs.teradata.com/reader/I5Vi6UNnylkj3PsoHlLHVQ/60WkuZd8ir9NgHlhlJcxIA) is:

**Teradata**

### Leave

Copy code

```
:force:
-- Additional Params: -t JavaScript
REPLACE PROCEDURE  PROC1 ()
BEGIN
  DECLARE v_propval            VARCHAR(1024);

 DECLARE Cur1 cursor for
   Select
      propID
   from viewName.viewCol
   where propval is not null;

LABEL_WHILE:
  WHILE (SQLCODE = 0)
  DO
      IF (SQLSTATE = '02000' )
       THEN LEAVE LABEL_WHILE;
      END IF;
      LABEL_INNER_WHILE:
      WHILE (SQLCODE = 0)
      DO
        IF (SQLSTATE = '02000' )
          THEN LEAVE LABEL_INNER_WHILE;
        END IF;
      END WHILE LABEL_INNER_WHILE;
      SELECT * FROM TABLE1;
  END WHILE L1;
END;
```

**Snowflake**

#### JavaScript Leave

Copy code

```
 CREATE OR REPLACE PROCEDURE PROC1 ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
EXECUTE AS CALLER
AS
$$
 // SnowConvert AI Helpers Code section is omitted.

 var V_PROPVAL;
 var CUR1 = new CURSOR(`SELECT propID from viewName.viewCol
  where
  propval is not null`,[],false);
  LABEL_WHILE: {
  while ( SQLCODE == 0 ) {
   if (SQLSTATE == `02000`) {
    break LABEL_WHILE;
   }
   LABEL_INNER_WHILE: {
    while ( SQLCODE == 0 ) {
     if (SQLSTATE == `02000`) {
      break LABEL_INNER_WHILE;
     }
    }
   }
   EXEC(`SELECT * FROM TABLE1`,[]);
  }
 }
$$;
```

## Getting Results from Procedures

### Description of the translation

In Teradata, there are two ways to return data from a procedure. The first is through output parameters and the second through *Dynamic Result Sets* and *Cursors.* Both are shown in the following example. Each important point is explained below.

### Example of returning data from a Stored Procedure

**Teradata**

#### Out parameter

Copy code

```
:force:
-- Additional Params: -t JavaScript
REPLACE PROCEDURE Procedure1(OUT P1 INTEGER)
    DYNAMIC RESULT SETS 2
    BEGIN
        DECLARE SQL_CMD,SQL_CMD_1  VARCHAR(20000) DEFAULT ' ';
        DECLARE RESULTSET CURSOR WITH RETURN ONLY FOR FIRSTSTATEMENT;
        SET SQL_CMD = 'SEL * FROM EMPLOYEE';
        PREPARE FIRSTSTATEMENT FROM SQL_CMD;
        OPEN RESULTSET;
        SET P1 = (SEL CAST(AVG(AGE) AS INTEGER) FROM EMPLOYEE);
    END;
```

**Snowflake**

##### JavaScript out parameter

Copy code

```
 CREATE OR REPLACE PROCEDURE Procedure1 (P1 FLOAT)
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
EXECUTE AS CALLER
AS
$$
    // SnowConvert AI Helpers Code section is omitted.

    var SQL_CMD = ` `;
    var SQL_CMD_1 = ` `;
    var RESULTSET = new CURSOR(() => FIRSTSTATEMENT,[],true);
    SQL_CMD = `SELECT * FROM EMPLOYEE`;
    var FIRSTSTATEMENT = SQL_CMD;
    RESULTSET.OPEN();
    EXEC(`(
   SELECT
      CAST(AVG(AGE) AS INTEGER)
   FROM
      EMPLOYEE
)`,[]);
    var subQueryVariable0;
    [subQueryVariable0] = INTO();
    P1 = subQueryVariable0;
    return PROCRESULTS(P1);
$$;
```

In this converted SQL, there are several conversions that take place:

- The `DYNAMIC RESULT SETS 2` definition is converted to a `DYNAMIC_RESULTS` variable.

Copy code

```
var DYNAMIC_RESULTS = 2;
```

- When a cursor with an `WITH RETURN`attribute is opened (and therefore a query is executed), its query ID is stored in the`_OUTQUERIES`collection to be later returned. The query id is obtained by the`getQueryId()`function provided in the [JavaScript API for Snowflake stored procedures](https://docs.snowflake.com/en/sql-reference/stored-procedures-api.html#getQueryId).
- Only the first k-query-IDs are stored in the collection, where k is the value of the`DYNAMIC_RESULTS`variable. This is done to emulate Teradata’s behavior, which only returns the first k-opened-cursors, even if more are opened in the stored procedure.
- The combination of `DECLARE CURSOR WITH RETURN` with `PREPARE` is translated to:

Copy code

```
var RESULTSET = new CURSOR(() => FIRSTSTATEMENT, [], true);
```

- The output parameters are supported through the return statement of the procedure. An array is created containing the value of each output parameter and the`_OUTQUERIES`collection. The`PROCRESULTS`function deals with the creation and filling of this array. See [PROCRESULTS() helper](./helpers-for-procedures#procresults) for more information.

Copy code

```
return PROCRESULTS(P1);
```

### Example of getting data from a Stored Procedure

If the output parameters and the query IDs are returned from a procedure, a second one could call the first one to get these values, as shown below:

**Teradata**

#### Call procedure

Copy code

```
 -- Additional Params: -t JavaScript
CREATE PROCEDURE Procedure2()
BEGIN
    DECLARE x INTEGER;
    CALL Procedure1(x);
END;
```

**Snowflake**

##### JavaScript Call procedure

Copy code

```
 CREATE OR REPLACE PROCEDURE Procedure2 ()
RETURNS STRING
LANGUAGE JAVASCRIPT
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
EXECUTE AS CALLER
AS
$$
    // SnowConvert AI Helpers Code section is omitted.

    var X;
    EXEC(`CALL Procedure1(:1)`,[X]);
$$;
```

- The value of the`P1`argument from`Procedure1`is returned and stored in the`X`variable.
- The`_OUTQUERIES`returned from`Procedure1`are stored in the`resultset`variable.

Note

This behavior also applies to the INOUT parameters.

### Known Issues

No issues were found.

### Related EWIs

1. [SSC-EWI-0022](../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0022): One or more identifiers in this statement were considered parameters by default.
2. [SSC-EWI-0023](../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0023): Performance Review - A loop contains an insert, delete, or update statement.
3. [SSC-EWI-0026](../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0026): The variable may require a cast to date, time, or timestamp.
4. [SSC-FDM-TD0001](../../issues-and-troubleshooting/functional-difference/teradataFDM#ssc-fdm-td0001): This message is shown when a data type BLOB is found.
