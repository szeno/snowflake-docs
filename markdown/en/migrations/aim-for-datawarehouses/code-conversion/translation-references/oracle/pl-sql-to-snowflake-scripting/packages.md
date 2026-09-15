# Oracle - PACKAGES

## Description

> Use the `CREATE` `PACKAGE` statement to create the specification for a stored package, which is an encapsulated collection of related procedures, functions, and other program objects stored together in the database. The package specification declares these objects. The package body, specified subsequently, defines these objects.([Oracle PL/SQL Language Reference CREATE PACKAGE Statement](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/CREATE-PACKAGE.html#GUID-40636655-899F-47D0-95CA-D58A71C94A56))

Snowflake does not have an equivalent for Oracle packages, so in order to maintain the structure, the packages are transformed into a schema, and all its elements are defined inside it. Also, the package and its elements are renamed to preserve the original schema name.

## BODY

### Description

The header of the PACKAGE BODY is removed and each procedure or function definition is transformed into a standalone function or procedure.

#### CREATE PACKAGE SYNTAX

Copy code

```
CREATE [ OR REPLACE ]
[ EDITIONABLE | NONEDITIONABLE ]
PACKAGE BODY plsql_package_body_source
```

### Sample Source Patterns

Note

The following queries were transformed with the PackagesAsSchema option disabled.

#### Oracle

Copy code

```
CREATE OR REPLACE PACKAGE BODY SCHEMA1.PKG1 AS
    PROCEDURE procedure1 AS
        BEGIN
            dbms_output.put_line('hello world');
        END;
END package1;
```

##### Snowflake

##### Snowflake

Copy code

```
CREATE OR REPLACE PROCEDURE SCHEMA1_PKG1.procedure1 ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        --** SSC-FDM-OR0035 - CHECK UDF IMPLEMENTATION FOR DBMS_OUTPUT.PUT_LINE_UDF. **
        CALL DBMS_OUTPUT.PUT_LINE_UDF('hello world');
    END;
$$;
```

### Known Issues

No issues were found.

### Related EWIs

1. [SSC-FDM-OR0035](../../../issues-and-troubleshooting/functional-difference/oracleFDM#ssc-fdm-or0035): DBMS\_OUTPUT.PUTLINE check UDF implementation.

## Constants

Translation spec for Package Constants

### Description

PACKAGE CONSTANTS can be declared either in the package declaration or in the PACKAGE BODY. When a package constant is used in a procedure, a new variable is declared with the same name and value as the constant, so the resulting code is pretty similar to the input.

#### Oracle Constant declaration Syntax

Copy code

```
constant CONSTANT datatype [NOT NULL] { := | DEFAULT } expression ;
```

### Sample Source Patterns

#### Sample auxiliary code

##### Oracle

Copy code

```
create table table1(id number);
```

##### Snowflake

Copy code

```
CREATE OR REPLACE TABLE table1 (id NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;
```

##### Oracle

Copy code

```
CREATE OR REPLACE PACKAGE PKG1 AS
    PROCEDURE procedure1;
    package_constant CONSTANT NUMBER:= 9999;
END PKG1;

CREATE OR REPLACE PACKAGE BODY PKG1 AS
    PROCEDURE procedure1 AS
    BEGIN
        INSERT INTO TABLE1(ID) VALUES(package_constant);
    END;
END PKG1;

CALL PKG1.procedure1();

SELECT * FROM TABLE1;
```

##### Result

| ID |
| --- |
| 9999 |

Expand

Show lessSee more

##### Snowflake

Copy code

```
CREATE SCHEMA IF NOT EXISTS PKG1
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;

CREATE OR REPLACE PROCEDURE PKG1.procedure1 ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        PACKAGE_CONSTANT NUMBER := 9999;
    BEGIN
        INSERT INTO TABLE1(ID) VALUES(:PACKAGE_CONSTANT);
    END;
$$;

CALL PKG1.procedure1();

SELECT * FROM
    TABLE1;
```

##### Result

| ID |
| --- |
| 9999 |

Expand

Show lessSee more

Note

Note that the`PROCEDURE` definition is being removed since it is not required in Snowflake.

### Known Issues

No issues were found.

### Related EWIs

1. [SSC-FDM-0006](../../../issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0006): Number type column may not behave similarly in Snowflake.

## DECLARATION

### Description

The declaration is converted to a schema, so each inner element is declared inside this schema. All the elements present in the package are commented except for the VARIABLES which have a proper transformation.

#### CREATE PACKAGE SYNTAX

Copy code

```
CREATE [ OR REPLACE ]
[ EDITIONABLE | NONEDITIONABLE ]
PACKAGE plsql_package_source
```

### Sample Source Patterns

Note

The following queries were transformed with the PackagesAsSchema option disabled.

#### Oracle

Copy code

```
CREATE OR REPLACE PACKAGE SCHEMA1.PKG1 AS
   -- Function Declaration
   FUNCTION function_declaration(param1 VARCHAR) RETURN INTEGER;

   -- Procedure Declaration
   PROCEDURE procedure_declaration(param1 VARCHAR2, param2 VARCHAR2);

END PKG1;
```

##### Snowflake

Copy code

```
CREATE SCHEMA IF NOT EXISTS SCHEMA1_PKG1
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;
```

Note

Note that both `FUNCTION` and `PROCEDURE` definitions are being removed since they are not required in Snowflake.

### Known Issues

No issues were found.

### Related EWIs

No related EWIs.

## VARIABLES

Translation spec for Package Variables

### Description

PACKAGE VARIABLES can be declared either in the package declaration or in the PACKAGE BODY. Due to its behavior, these variables are converted into [Snowflake session variables](https://docs.snowflake.com/en/sql-reference/session-variables.html) so each usage or assignment is translated to its equivalent in Snowflake.

#### Oracle Variable declaration syntax

Copy code

```
variable datatype [ [ NOT NULL] {:= | DEFAULT} expression ] ;
```

### Sample Source Patterns

#### Sample auxiliary code

##### Oracle

Copy code

```
create table table1(id number);
```

##### Snowflake

Copy code

```
CREATE OR REPLACE TABLE table1 (id NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;
```

#### Variable declaration

##### Oracle

Copy code

```
CREATE OR REPLACE PACKAGE PKG1 AS
    package_variable NUMBER:= 100;
END PKG1;
```

##### Snowflake Scripting

Copy code

```
CREATE SCHEMA IF NOT EXISTS PKG1
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;

SET "PKG1.PACKAGE_VARIABLE" = '' || (100);
```

#### Variable Usage

Package variable usages are transformed into the Snowflake [GETVARIABLE](https://docs.snowflake.com/en/sql-reference/session-variables.html#session-variable-functions) function which accesses the current value of a session variable. An explicit cast is added to the original variable data type in order to maintain the functional equivalence in the operations where these variables are used.

##### Oracle

Copy code

```
CREATE OR REPLACE PACKAGE PKG1 AS
    PROCEDURE procedure1;
    package_variable NUMBER:= 100;
END PKG1;

CREATE OR REPLACE PACKAGE BODY PKG1 AS
    PROCEDURE procedure1 AS
    BEGIN
        INSERT INTO TABLE1(ID) VALUES(package_variable);
    END;
END PKG1;

CALL SCHEMA1.PKG1.procedure1();

SELECT * FROM TABLE1;
```

##### Result

| ID |
| --- |
| 100 |

Expand

Show lessSee more

##### Snowflake

Copy code

```
CREATE SCHEMA IF NOT EXISTS PKG1
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;

SET "PKG1.PACKAGE_VARIABLE" = '' || (100);

CREATE OR REPLACE PROCEDURE PKG1.procedure1 ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        INSERT INTO TABLE1(ID) VALUES(GETVARIABLE('PKG1.PACKAGE_VARIABLE') :: NUMBER);
    END;
$$;

CALL SCHEMA1.PKG1.procedure1();

SELECT * FROM
    TABLE1;
```

##### Result

| ID |
| --- |
| 100 |

Expand

Show lessSee more

Note

Note that the `PROCEDURE` definition in the package is removed since it is not required by Snowflake.

### Variable regular assignment

When a package variable is assigned using the `:=` operator, the assignation is replaced by a UDF called UPDATE\_PACKAGE\_VARIABLE\_STATE which is an abstraction of the Snowflake [SETVARIABLE](https://docs.snowflake.com/en/sql-reference/session-variables.html#session-variable-functions) function.

Oracle

#### Oracle

Copy code

```
CREATE OR REPLACE PACKAGE PKG1 AS
    PROCEDURE procedure1;
    package_variable NUMBER:= 100;
END PKG1;

CREATE OR REPLACE PACKAGE BODY PKG1 AS
    PROCEDURE procedure1 AS
    BEGIN
        package_variable := package_variable + 100;
        INSERT INTO TABLE1(ID) VALUES(package_variable);
    END;
END PKG1;

CALL PKG1.procedure1();

SELECT * FROM TABLE1;
```

##### Result

| ID |
| --- |
| 200 |

Expand

Show lessSee more

#### Snowflake

Copy code

```
CREATE SCHEMA IF NOT EXISTS PKG1
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
;

SET "PKG1.PACKAGE_VARIABLE" = '' || (100);

CREATE OR REPLACE PROCEDURE PKG1.procedure1 ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        CALL UPDATE_PACKAGE_VARIABLE_STATE_UDF('PKG1.PACKAGE_VARIABLE', TO_VARCHAR(GETVARIABLE('PKG1.PACKAGE_VARIABLE') :: NUMBER + 100));
        INSERT INTO TABLE1(ID) VALUES(GETVARIABLE('PKG1.PACKAGE_VARIABLE') :: NUMBER);
    END;
$$;

CALL PKG1.procedure1();

SELECT * FROM
    TABLE1;
```

##### Result

| ID |
| --- |
| 200 |

Expand

Show lessSee more

Note

Note that the `PROCEDURE` definition in the package is removed since it is not required by Snowflake.

#### Variable assignment as an output argument

When a package variable is used as an output argument a new variable is declared inside the procedure, this variable will catch the output argument value of the procedure, and then the variable will be used to update the session variable which refers to the package variable using the UPDATE\_PACKAGE\_VARIABLE\_STATE mentioned above.

##### Oracle

Copy code

```
CREATE OR REPLACE PACKAGE PKG1 AS
    PROCEDURE procedure1;
    PROCEDURE procedure2(out_param OUT NUMBER);
    package_variable NUMBER:= 100;
END PKG1;

CREATE OR REPLACE PACKAGE BODY PKG1 AS
    PROCEDURE procedure1 AS
    BEGIN
        procedure2(package_variable);
        INSERT INTO TABLE1(ID) VALUES(package_variable);
    END;
    PROCEDURE procedure2 (out_param OUT NUMBER) AS
    BEGIN
        out_param := 1000;
    END;
END PKG1;

CALL PKG1.procedure1();
```

##### Result

| ID |
| --- |
| 1000 |

Expand

Show lessSee more

##### Snowflake

Copy code

```
CREATE SCHEMA IF NOT EXISTS PKG1
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
;

SET "PKG1.PACKAGE_VARIABLE" = '' || (100);

--** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "TABLE1" **
CREATE OR REPLACE PROCEDURE PKG1.procedure1 ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        PKG1_PACKAGE_VARIABLE VARIANT;
    BEGIN
        CALL PKG1.
        procedure2(:PKG1_PACKAGE_VARIABLE);
        CALL UPDATE_PACKAGE_VARIABLE_STATE_UDF('PKG1.PACKAGE_VARIABLE', TO_VARCHAR(:PKG1_PACKAGE_VARIABLE));
        INSERT INTO TABLE1(ID) VALUES(GETVARIABLE('PKG1.PACKAGE_VARIABLE') :: NUMBER);
    END;
$$;

CREATE OR REPLACE PROCEDURE PKG1.procedure2 (out_param OUT NUMBER(38, 18))
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        out_param := 1000;
    END;
$$;

CALL PKG1.procedure1();
```

##### Result

| ID |
| --- |
| 1000 |

Expand

Show lessSee more

Note

Note that the `PROCEDURE` definition in the package is removed since it is not required by Snowflake.

### Known Issues

No issues were found.

### Related EWIs

1. [SSC-FDM-0006](../../../issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0006): Number type column may not behave similarly in Snowflake.
