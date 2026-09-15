# Redshift - CREATE PROCEDURE

## Description

> Creates a new stored procedure or replaces an existing procedure for the current database. ([Redshift SQL Language Reference Create Procedure](https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_PROCEDURE.html)).

See the following definitions for more information about procedure clauses:

- [ARGUMENTS MODE](#arguments-mode)
- [POSITIONAL ARGUMENTS](#positional-arguments)
- [NONATOMIC](#nonatomic)
- [PROCEDURE BODY](#procedure-body)
- [SECURITY (DEFINER | INVOKER)](#security-definer--invoker)

## Grammar Syntax

The following is the SQL syntax to create a Procedure in Amazon Redshift. See the [Redshift CREATE PROCEDURE specification](https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_PROCEDURE.html) for this syntax.

Copy code

```
 CREATE [ OR REPLACE ] PROCEDURE sp_procedure_name
  ( [ [ argname ] [ argmode ] argtype [, ...] ] )
[ NONATOMIC ]
AS $$
  procedure_body
$$ LANGUAGE plpgsql
[ { SECURITY INVOKER | SECURITY DEFINER } ]
[ SET configuration_parameter { TO value | = value } ]
```

## Sample Source Patterns

### Input Code:

#### Redshift

Copy code

```
 CREATE PROCEDURE TEST_PROCEDURE()
LANGUAGE PLPGSQL
AS
$$
BEGIN
    NULL;
END;
$$;
```

#### Output Code:

##### Snowflake

Copy code

```
 CREATE PROCEDURE TEST_PROCEDURE ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "02/07/2025",  "domain": "test" }}'
AS
$$
    BEGIN
        NULL;
    END;
$$;
```

## Related EWIs

There are no issues for this transformation.

## ALIAS DECLARATION

### Description

If the stored procedure’s signature omits the argument name, you can declare an alias for the argument.

There is no support for this in Snowflake.

To achieve functional equivalence, aliases will be removed, and all usages will be renamed.

When an alias is declared for a parameter nameless, a generated name will be created for the parameter and the usages. When the alias is for a parameter with name the alias will be replaced by the real parameter name.

### Grammar Syntax

Copy code

```
 name ALIAS FOR $n;
```

### Sample Source Patterns

#### Input Code:

##### Redshift

Copy code

```
 CREATE OR REPLACE PROCEDURE test_procedure (integer)
LANGUAGE plpgsql
AS
$$
DECLARE
    first_alias ALIAS  FOR $1;
    second_alias ALIAS  FOR $1;
BEGIN
   INSERT INTO t1
   VALUES (first_alias + 1);
   INSERT INTO t1
   VALUES (second_alias + 2);
END;
$$;

--Notice the parameter already has a name
--and we are defining two alias to the same parameter
CREATE OR REPLACE PROCEDURE test_procedure (PARAMETER1 integer)
LANGUAGE plpgsql
AS
$$
DECLARE
    first_alias ALIAS  FOR $1;
    second_alias ALIAS  FOR $1;
BEGIN
   INSERT INTO t1
   VALUES (first_alias + 1);
   INSERT INTO t1
   VALUES (second_alias + 2);
END;
$$;
```

##### Output Code:

##### Snowflake

Copy code

```
 CREATE OR REPLACE PROCEDURE test_procedure (SC_ARG1 integer)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
AS
$$
BEGIN
   INSERT INTO t1
   VALUES (:SC_ARG1 + 1);
   INSERT INTO t1
   VALUES (:SC_ARG1 + 2);
END;
$$;

--Notice the parameter already has a name
--and we are defining two alias to the same parameter
--** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "t1" **
CREATE OR REPLACE PROCEDURE test_procedure (PARAMETER1 integer)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
AS
$$
BEGIN
   INSERT INTO t1
   VALUES (:PARAMETER1 + 1);
   INSERT INTO t1
   VALUES (:PARAMETER1 + 2);
END;
$$;
```

### Known Issues

There are no known issues.

### Related EWIs.

There are no related EWIs.

## ARGUMENTS MODE

### Description

Amazon Redshift stored procedures support parameters that can be passed during procedure invocation. These parameters allow you to provide input values, retrieve output values, or use them for input and output operations. Below is a detailed explanation of the types of parameters, their modes, and examples of their usage. Snowflake only supports input values.

#### IN (Input Parameters)

Purpose: Used to pass values into the procedure.

Default Mode: If no mode is specified, parameters are considered IN.

Behavior: Values passed to the procedure cannot be modified inside the procedure.

##### OUT (Output Parameters)

Purpose: Used to return values from the procedure.

Behavior: Parameters can be modified inside the procedure and are returned to the caller. You cannot send an initial value.

##### INOUT (Input/Output Parameters)

Purpose: Used to pass values into the procedure and modify them to return updated values.

Behavior: Combines the behavior of IN and OUT. You must send an initial value regardless of the output.

### Grammar Syntax

Copy code

```
 [ argname ] [ argmode ] argtype
```

### Sample Source Patterns

#### Input Code:

##### Redshift

Copy code

```
:force:
CREATE OR REPLACE PROCEDURE SP_PARAMS(
IN PARAM1 INTEGER,
OUT PARAM2 INTEGER,
INOUT PARAM3 INTEGER)
AS
$$
    BEGIN
        NULL;
    END;
$$
LANGUAGE plpgsql;
```

##### Output Code:

##### Snowflake

Copy code

```
 CREATE OR REPLACE PROCEDURE SP_PARAMS (PARAM1 INTEGER, PARAM2 OUT INTEGER, PARAM3 OUT INTEGER)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "07/10/2025",  "domain": "no-domain-provided" }}'
AS
$$
    BEGIN
        NULL;
    END;
$$;
```

### Known Issues

There are no known issues.

### Related EWIs

1. [SCC-EWI-0028](../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0028) : Type not supported by Snowflake.
2. [SSC-EWI-RS0010](../../issues-and-troubleshooting/conversion-issues/redshiftEWI#ssc-ewi-rs0010): Top-level procedure call with out parameters is not supported.

## PROCEDURE BODY

Hint

Translation for PostgreSQL string constant definition in procedures is not supported.
Prompt the Snowflake AIM Agent for Data Warehouses to arrange the code before its translation to modify it to dollar routine body

### Description

Like Redshift, Snowflake supports CREATE PROCEDURE using ` procedure\_logic ` as the body. There is a difference in the Redshift syntax where a word can be inside the ` like $word$ and used as a delimiter body like $word$ procedure\_logic $word$. It will be transformed by removing the word, leaving the `.

### Grammar Syntax

Copy code

```
 AS
$Alias$
  procedure_body
$Alias$
```

### Sample Source Patterns

#### Input Code:

##### Redshift

Copy code

```
 CREATE OR REPLACE PROCEDURE SP()
AS
$somename$
BEGIN
   NULL;
END;
$somename$
LANGUAGE plpgsql;
```

##### Output Code:

##### Snowflake

Copy code

```
 CREATE OR REPLACE PROCEDURE SP ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "02/07/2025",  "domain": "test" }}'
AS
$$
   BEGIN
      NULL;
   END;
$$;
```

### Known Issues

There are no known issues.

### Related EWIs.

There are no related EWIs.

## BLOCK STATEMENT

### Description

PL/pgSQL is a block-structured language. The complete body of a procedure is defined in a block, which contains variable declarations and PL/pgSQL statements. A statement can also be a nested block, or subblock.

### Grammar Syntax

Copy code

```
 [ <<label>> ]
[ DECLARE
  declarations ]
BEGIN
  statements
EXCEPTION
  WHEN OTHERS THEN
    statements
END [ label ];
```

### Sample Source Patterns

#### Input Code:

##### Redshift

Copy code

```
 CREATE OR REPLACE PROCEDURE MY_PROCEDURE()
AS
$$
    BEGIN
        NULL;
    END;
$$
LANGUAGE plpgsql;
```

##### Output Code:

##### Snowflake

Copy code

```
 CREATE OR REPLACE PROCEDURE MY_PROCEDURE ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "02/10/2025",  "domain": "test" }}'
AS
$$
    BEGIN
        NULL;
    END;
$$;
```

### Known Issues

There are no known issues.

### Related EWIs.

There are no related EWIs.

## DECLARE

### Description

Section to declare all the procedure variables except for loop variables.  
Redshift supports multiple DECLARE sections per block statement, since Snowflake does not support this behavior they must be merged into a single declaration statement per block.

### Grammar Syntax

Copy code

```
 [ DECLARE declarations ]
```

### Sample Source Patterns

#### Input Code:

##### Redshift

Copy code

```
 CREATE OR REPLACE PROCEDURE first_procedure (first_parameter integer)
LANGUAGE plpgsql
    AS
$$
DECLARE
    i int := first_parameter;
BEGIN
   select i;
END;
$$;

CREATE OR REPLACE PROCEDURE second_procedure (first_parameter integer)
LANGUAGE plpgsql
    AS
$$
DECLARE
    i int := first_parameter;
DECLARE
    j int := first_parameter;
BEGIN
   select i;
END;
$$;
```

##### Output Code:

##### Snowflake

Copy code

```
 CREATE OR REPLACE PROCEDURE first_procedure (first_parameter integer)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "02/11/2025",  "domain": "test" }}'
    AS
$$
   DECLARE
      i int := first_parameter;
BEGIN
   select i;
END;
$$;

CREATE OR REPLACE PROCEDURE second_procedure (first_parameter integer)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "02/11/2025",  "domain": "test" }}'
    AS
$$
   DECLARE
      i int := first_parameter;
      j int := first_parameter;
BEGIN
   select i;
END;
$$;
```

### Known Issues

There are no known issues.

### Related EWIs.

There are no related EWIs.

## EXCEPTION

### Description

When an exception occurs, and you add an exception-handling block, you can write RAISE statements and most other PL/pgSQL statements. For example, you can raise an exception with a custom message or insert a record into a logging table.

### Grammar Syntax

Copy code

```
 EXCEPTION
  WHEN OTHERS THEN
    statements
```

### Sample Source Patterns

#### Input Code:

##### Redshift

Copy code

```
 CREATE OR REPLACE PROCEDURE update_employee_sp() AS
$$
BEGIN
    select var;
EXCEPTION WHEN OTHERS THEN
    RAISE INFO 'An exception occurred.';
END;
$$
LANGUAGE plpgsql;
```

##### Output Code:

##### Snowflake

Copy code

```
 CREATE OR REPLACE PROCEDURE update_employee_sp ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
AS
$$
BEGIN
    select var;
EXCEPTION WHEN OTHER THEN
        CALL RAISE_MESSAGE_UDF('INFO', 'An exception occurred.');
        RAISE;
END;
$$;
```

### Known Issues

There are no known issues.

### Related EWIs.

There are no related EWIs.

## LABEL

### Description

Labels are used in Redshift to qualify a block or to use the EXIT or END statement. Snowflake does not support labels.

Warning

Since labels are not supported in Snowflake, an EWI will be printed.

### Grammar Syntax

Copy code

```
 [<<label>>]
BEGIN
    ...
END [label]
```

### Sample Source Patterns

#### Input Code:

##### Redshift

Copy code

```
 CREATE OR REPLACE PROCEDURE test_procedure (first_parameter integer)
LANGUAGE plpgsql
AS
$$
    <<Begin_block_label>>
BEGIN
   INSERT INTO my_test_table
   VALUES (first_parameter);
END;
$$;
```

##### Output Code:

##### Snowflake

Copy code

```
 CREATE OR REPLACE PROCEDURE test_procedure (first_parameter integer)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
AS
$$
   !!!RESOLVE EWI!!! /*** SSC-EWI-0094 - LABEL DECLARATION FOR A STATEMENT IS NOT SUPPORTED BY SNOWFLAKE SCRIPTING <<Begin_block_label>> ***/!!!
BEGIN
   INSERT INTO my_test_table
   VALUES (:first_parameter);
END;
$$;
```

### Known Issues

There are no known issues.

### Related EWIs

1. [SSC-EWI-0094](../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0094): Label declaration not supported

## NONATOMIC

### Description

The NONATOMIC commits after each statement in the stored procedure. Snowflake supports an AUTOCOMMIT parameter. The default setting for AUTOCOMMIT is TRUE (enabled).

While AUTOCOMMIT is enabled, Each statement outside an explicit transaction is treated as inside its implicit single-statement transaction. In other words, that statement is automatically committed if it succeeds and automatically rolled back if it fails. In other words, Snowflake works as NONATOMIC “by default”.

### Grammar Syntax

Copy code

```
 NONATOMIC
```

### Sample Source Patterns

#### Input Code:

##### Redshift

Copy code

```
 CREATE OR REPLACE PROCEDURE SP_NONATOMIC()
NONATOMIC
AS
$$
    BEGIN
        NULL;
    END;
$$
LANGUAGE plpgsql;
```

##### Output Code:

##### Snowflake

Copy code

```
 CREATE OR REPLACE PROCEDURE SP_NONATOMIC ()
RETURNS VARCHAR
----** SSC-FDM-RS0008 - SNOWFLAKE USES AUTOCOMMIT BY DEFAULT. **
--NONATOMIC
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "02/10/2025",  "domain": "test" }}'
AS
$$
    BEGIN
        NULL;
    END;
$$;
```

### Known Issues

There are no known issues.

### Related EWIs.

There are no related EWIs.

## POSITIONAL ARGUMENTS

### Description

Redshift supports nameless parameters by referencing the parameters by their position using $. Snowflake does not support this behavior. To ensure functional equivalence, those references can be converted by the parameter’s name if the name is present in the definition. If not, a name will be generated for the parameter, and the uses will be replaced with the new name.

### Grammar Syntax

Copy code

```
 $n
```

### Sample Source Patterns

#### Input Code:

##### Redshift

Copy code

```
 CREATE OR REPLACE PROCEDURE SP_POSITIONAL_REFERENCES(
INTEGER,
param2 INTEGER,
INTEGER)
AS
$$
    DECLARE
        localVariable INTEGER := 0;
    BEGIN
        localVariable := $2 + $3 + $1;
    END;
$$
LANGUAGE plpgsql;
```

##### Output Code:

##### Snowflake

Copy code

```
 CREATE OR REPLACE PROCEDURE SP_POSITIONAL_REFERENCES (SC_ARG1
INTEGER,
param2 INTEGER, SC_ARG3 INTEGER)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
AS
$$
    DECLARE
        localVariable INTEGER := 0;
    BEGIN
        localVariable := param2 + SC_ARG3 + SC_ARG1;
    END;
$$;
```

### Known Issues

There are no known issues.

### Related EWIs.

There are no related EWIs.

## RAISE

### Description

> Use the `RAISE level` statement to report messages and raise errors.
>
> ([Redshift SQL Language Reference RAISE](https://docs.aws.amazon.com/es_es/redshift/latest/dg/c_PLpgSQL-statements.html#r_PLpgSQL-messages-errors))

Note

:class: tip
RAISE are fully supported by [Snowflake](https://docs.snowflake.com/en/developer-guide/snowflake-scripting/variables#declaring-a-variable).

### Grammar Syntax

Copy code

```
 RAISE level 'format' [, variable [, ...]];
```

In Amazon Redshift, the `RAISE` statement is used to generate messages in the console or throw custom exceptions. Redshift allows you to specify different *levels* to indicate the severity of the message. In Snowflake, this functionality can be emulated using a user-defined function (UDF) that makes a call to the console depending on the specified level.

1. **Exception**:  
   When the level is “EXCEPTION”, a custom exception is raised with a general message: *“To view the EXCEPTION MESSAGE, you need to check the log.”* The exception code is `-20002`, which informs the user that the custom message can be found in the logs. This is due to limitations when sending custom exceptions in Snowflake.
2. **Warning**:  
   If the level is “WARNING”, `SYSTEM$LOG_WARN` is used to print the warning message to Snowflake’s log, which helps highlight potential issues without interrupting the flow of execution.
3. **Info**:  
   For any other level (such as “INFO”), `SYSTEM$LOG_INFO` is used to print the message to the console log, providing more detailed feedback about the system’s state without causing critical disruptions.

This approach allows emulating Redshift’s severity levels functionality, adapting them to Snowflake’s syntax and features, while maintaining flexibility and control over the messages and exceptions generated during execution.

**Limitations**

- To view logs in Snowflake, it is necessary to have specific privileges, such as the `ACCOUNTADMIN` or `SECURITYADMIN` roles.
- Logs in Snowflake are not available immediately and may have a slight delay before the information is visible.
- Personalized error messages in exceptions are not displayed like in Redshift. To view custom messages, you must access the logs directly.

For further information, please refer to the following [page](https://docs.snowflake.com/developer-guide/logging-tracing/logging-snowflake-scripting).

### Sample Source Patterns

#### Input Code:

##### Redshift

Copy code

```
 CREATE OR REPLACE PROCEDURE raise_example(IN user_id INT)
LANGUAGE plpgsql
AS $$
BEGIN
	RAISE EXCEPTION 'User % not exists.', user_id;
END;
$$;
```

##### Output Code:

##### Snowflake

Copy code

```
 CREATE OR REPLACE PROCEDURE raise_example (user_id INT)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "02/11/2025",  "domain": "test" }}'
AS $$
BEGIN
	CALL RAISE_MESSAGE_UDF('EXCEPTION', 'User % not exists.', array_construct(:user_id));
END;
$$;
```

#### UDFs

##### RAISE\_MESSAGE\_UDF

Copy code

```
 CREATE OR REPLACE PROCEDURE RAISE_MESSAGE_UDF(LEVEL VARCHAR, MESSAGE VARCHAR, ARGS VARIANT)
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
    DECLARE
        MY_EXCEPTION EXCEPTION (-20002, 'To view the EXCEPTION MESSAGE, you need to check the log.');
        SC_RAISE_MESSAGE VARCHAR;
    BEGIN
        SC_RAISE_MESSAGE := STRING_FORMAT_UDF(MESSAGE, ARGS);
        IF (LEVEL = 'EXCEPTION') THEN
            SYSTEM$LOG_ERROR(SC_RAISE_MESSAGE);
            RAISE MY_EXCEPTION;
        ELSEIF (LEVEL = 'WARNING') THEN
            SYSTEM$LOG_WARN(SC_RAISE_MESSAGE);
            RETURN 'Warning printed successfully';
        ELSE
            SYSTEM$LOG_INFO(SC_RAISE_MESSAGE);
            RETURN 'Message printed successfully';
        END IF;
    END;
$$;
```

##### STRING\_FORMAT\_UDF

Copy code

```
 CREATE OR REPLACE FUNCTION PUBLIC.STRING_FORMAT_UDF(PATTERN VARCHAR, ARGS VARIANT)
RETURNS VARCHAR
LANGUAGE JAVASCRIPT
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "udf",  "convertedOn": "02/11/2025",  "domain": "test" }}'
AS
$$
	var placeholder_str = "{%}";
	var result = PATTERN.replace(/(?<!%)%(?!%)/g, placeholder_str).replace("%%","%");
	for (var i = 0; i < ARGS.length; i++)
	{
		result = result.replace(placeholder_str, ARGS[i]);
	}
	return result;
$$;
```

### Known Issues

There are no known issues.

### Related EWIs.

There are no related EWIs.

## RETURN

### Description

> The RETURN statement returns back to the caller from a stored procedure. ([Redshift SQL Language Reference Return](https://docs.aws.amazon.com/redshift/latest/dg/c_PLpgSQL-statements.html#r_PLpgSQL-return)).

The conversion of the return statement from Amazon Redshift to Snowflake is straightforward, only considering adding a `NULL` to the return statement on Snowflake.

### Grammar Syntax

Copy code

```
 RETURN;
```

### Sample Source Patterns

#### Simple Case

##### Input Code:

##### Redshift

Copy code

```
 CREATE OR REPLACE PROCEDURE procedure1 ()
AS
$$
BEGIN
   RETURN;
END
$$ LANGUAGE plpgsql;
```

##### Output Code:

##### Redshift

Copy code

```
 CREATE OR REPLACE PROCEDURE procedure1 ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "02/12/2025",  "domain": "test" }}'
AS
$$
BEGIN
  RETURN NULL;
END
$$;
```

#### When the procedure has out parameters

A variant is returned with parameters set up as output parameters. So, for each return, a variant will be added as a return value.

##### Input Code:

##### Redshift

Copy code

```
 CREATE OR REPLACE PROCEDURE procedure1 (OUT output_value VARCHAR)
AS
$$
BEGIN
   RETURN;
END
$$ LANGUAGE plpgsql;
```

##### Output Code:

##### Redshift

Copy code

```
 CREATE OR REPLACE PROCEDURE procedure1 (output_value OUT VARCHAR)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
AS
$$
BEGIN
   RETURN NULL;
END
$$;
```

### Known Issues

There are no known issues.

### Related EWIs.

There are no related EWIs.

## SECURITY (DEFINER | INVOKER)

### Description

The SECURITY clause in Amazon Redshift stored procedures defines the access control and permissions context under which the procedure executes. This determines whether the procedure uses the privileges of the owner (creator) or the caller (user invoking the procedure).

### Grammar Syntax

Copy code

```
 [ { SECURITY INVOKER | SECURITY DEFINER } ]
```

### Sample Source Patterns

#### Input Code:

##### Redshift

Copy code

```
 CREATE OR REPLACE PROCEDURE SP_SECURITY_INVOKER( )
AS
$$
    BEGIN
        NULL;
    END;
$$
LANGUAGE plpgsql
SECURITY INVOKER
;

CREATE OR REPLACE PROCEDURE SP_SECURITY_DEFINER( )
AS
$$
     BEGIN
        NULL;
    END;
$$
LANGUAGE plpgsql
SECURITY DEFINER;
```

##### Output Code:

##### Snowflake

Copy code

```
 CREATE OR REPLACE PROCEDURE SP_SECURITY_INVOKER ( )
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "02/07/2025",  "domain": "test" }}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        NULL;
    END;
$$
;

CREATE OR REPLACE PROCEDURE SP_SECURITY_DEFINER ( )
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "02/07/2025",  "domain": "test" }}'
EXECUTE AS OWNER
AS
$$
    BEGIN
        NULL;
    END;
$$;
```

### Known Issues

There are no known issues.

### Related EWIs.

There are no related EWIs.

## VARIABLE DECLARATION

### Description

> Declare all variables in a block, except for loop variables, in the block’s DECLARE section.
>
> ([Redshift SQL Language Reference Variable Declaration](https://docs.aws.amazon.com/redshift/latest/dg/c_PLpgSQL-structure.html#r_PLpgSQL-variable-declaration))

Note

:class: tip
Variable declarations are fully supported by [Snowflake](https://docs.snowflake.com/en/developer-guide/snowflake-scripting/variables#declaring-a-variable).

### Grammar Syntax

Copy code

```
 DECLARE
name [ CONSTANT ] type [ NOT NULL ] [ { DEFAULT | := } expression ];
```

In Redshift, the `CONSTANT` keyword prevents variable reassignment during execution. Since Snowflake does not support this keyword, it is removed during transformation. This does not impact functionality, as the logic should not attempt to reassign a constant variable.

The `NOT NULL` constraint in Redshift ensures a variable cannot be assigned a null value and requires a non-null default value. As Snowflake does not support this constraint, it is removed during transformation. However, the default value is retained to maintain functionality.

A variable declare with a Refcursor is transformed to Resultset type, for more [information](#declare-refcursor).

### Sample Source Patterns

#### Input Code:

##### Redshift

Copy code

```
 CREATE OR REPLACE PROCEDURE VARIABLE_DECLARATION()
LANGUAGE plpgsql
AS $$
DECLARE
    v_simple_int INT;
    v_default_char CHAR(4) DEFAULT 'ABCD';
    v_default_float FLOAT := 10.00;
    v_constant_char CONSTANT CHAR(4) := 'ABCD';
    v_notnull VARCHAR NOT NULL DEFAULT 'Test default';
    v_refcursor REFCURSOR;
BEGIN
-- Procedure logic
END;
$$;
```

##### Output Code:

##### Snowflake

Copy code

```
 CREATE OR REPLACE PROCEDURE VARIABLE_DECLARATION ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
AS $$
        DECLARE
            v_simple_int INT;
            v_default_char CHAR(4) DEFAULT 'ABCD';
            v_default_float FLOAT := 10.00;
            v_constant_char CHAR(4) := 'ABCD';
            --** SSC-FDM-PG0012 - NOT NULL CONSTRAINT HAS BEEN REMOVED. ASSIGNING NULL TO THIS VARIABLE WILL NO LONGER CAUSE A FAILURE. **
            v_notnull VARCHAR DEFAULT 'Test default';
            v_refcursor RESULTSET;
BEGIN
            NULL;
-- Procedure logic
END;
$$;
```

### Known Issues

No issues were found.

### Related EWIs

1. [SSC-FDM-PG0012](../../issues-and-troubleshooting/functional-difference/postgresqlFDM#ssc-fdm-pg0012): NOT NULL constraint has been removed. Assigning NULL to this variable will no longer cause a failure.

## TRANSACTIONS

## COMMIT

### Description

> Commits the current transaction to the database. This command makes the database updates from the transaction permanent. ([Redshift SQL Language Reference COMMIT](https://docs.aws.amazon.com/redshift/latest/dg/r_COMMIT.html))

Grammar Syntax

Copy code

```
COMMIT [WORK | TRANSACTION]
```

### Sample Source Patterns

#### Setup data

##### Redshift

##### Query

Copy code

```
 CREATE TABLE transaction_values_test
(
    col1 INTEGER
);
```

##### Snowflake

##### Query

Copy code

```
 CREATE TABLE transaction_values_test
(
    col1 INTEGER
);
```

#### COMMIT with TRANSACTION keyword

The TRANSACTION keyword is not supported in Snowflake. However, since it does not have an impact on functionality it will just be removed.

##### Redshift

##### Query

Copy code

```
 COMMIT TRANSACTION;
```

##### Snowflake

##### Query

Copy code

```
 COMMIT;
```

#### COMMIT in a default transaction behavior procedure (without NONATOMIC clause)

To avoid out of scope transaction exceptions in Snowflake, the usages of COMMIT will be matched with BEGIN TRANSACTION.

When multiple COMMIT statements are present in the procedure, multiple BEGIN TRANSACTION statements will be generated after every COMMIT to emulate the Redshift transaction behavior.

##### Redshift

##### Query

Copy code

```
 CREATE OR REPLACE PROCEDURE transaction_test(a INT)
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO transaction_values_test VALUES (a);
    COMMIT;
    INSERT INTO transaction_values_test VALUES (a + 1);
    COMMIT;
END
$$;

CALL transaction_test(120);

SELECT * FROM transaction_values_test;
```

##### Result

Copy code

```
+------+
| col1 |
+------+
| 120  |
| 121  |
+------+
```

##### Snowflake

##### Query

Copy code

```
 CREATE OR REPLACE PROCEDURE transaction_test (a INT)
RETURNS VARCHAR
    LANGUAGE SQL
    AS $$
BEGIN
    BEGIN TRANSACTION;
    INSERT INTO transaction_values_test
    VALUES (:a);
    COMMIT;
    BEGIN TRANSACTION;
    INSERT INTO transaction_values_test
    VALUES (:a + 1);
    COMMIT;
END
$$;

CALL transaction_test(120);

SELECT * FROM
    transaction_values_test;
```

##### Result

Copy code

```
+------+
| col1 |
+------+
| 120  |
| 121  |
+------+
```

#### COMMIT in a procedure with NONATOMIC behavior

The NONATOMIC behavior from Redshift is emulated in Snowflake by using the session parameter AUTOCOMMIT set to true.

Since the AUTOCOMMIT session parameter is assumed to be true, the COMMIT statement inside NONATOMIC procedures is left as is.

##### Redshift

##### Query

Copy code

```
 CREATE OR REPLACE PROCEDURE nonatomic_procedure(a int)
    NONATOMIC
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO transaction_values_test values (a + 2);
    INSERT INTO transaction_values_test values (a + 3);
    COMMIT;
END
$$;

CALL nonatomic_procedure(10);

SELECT * FROM transaction_values_test;
```

##### Result

Copy code

```
+------+
| col1 |
+------+
| 12   |
| 13   |
+------+
```

##### Snowflake

##### Query

Copy code

```
 CREATE OR REPLACE PROCEDURE nonatomic_procedure (a int)
RETURNS VARCHAR
--    --** SSC-FDM-RS0008 - SNOWFLAKE USES AUTOCOMMIT BY DEFAULT. **
--    NONATOMIC
    LANGUAGE SQL
    COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
    AS $$
BEGIN
    INSERT INTO transaction_values_test
    values (:a + 2);
    INSERT INTO transaction_values_test
    values (:a + 3);
    COMMIT;
END
$$;

CALL nonatomic_procedure(10);

SELECT * FROM
transaction_values_test;
```

##### Result

Copy code

```
+------+
| col1 |
+------+
| 12   |
| 13   |
+------+
```

### Known Issues

**1. COMMIT inside a nested procedure call**

In Redshift, when a COMMIT statement is specified in a nested procedure call, the command will commit all pending work from previous statements in the current and parent scopes. Committing the parent scope actions is not supported in Snowflake, when this case is detected an FDM will be generated.

#### Redshift

##### Query

Copy code

```
 CREATE OR REPLACE PROCEDURE transaction_test(a INT)
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO transaction_values_test VALUES (a);
    COMMIT;
END
$$;

CREATE OR REPLACE PROCEDURE nested_transaction_test(a INT)
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO transaction_values_test values (a);
    INSERT INTO transaction_values_test values (a + 1);
    INSERT INTO transaction_values_test values (a + 2);
    CALL transaction_test(a + 3);
END
$$;
```

##### Snowflake

##### Query

Copy code

```
 CREATE OR REPLACE PROCEDURE transaction_test (a INT)
RETURNS VARCHAR
    LANGUAGE SQL
    COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
    AS $$
BEGIN
    BEGIN TRANSACTION;
    INSERT INTO transaction_values_test
    VALUES (:a);
    COMMIT;
END
$$;

CREATE OR REPLACE PROCEDURE nested_transaction_test (a INT)
RETURNS VARCHAR
    LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
    AS $$
BEGIN
    INSERT INTO transaction_values_test
    values (:a);
    INSERT INTO transaction_values_test
    values (:a + 1);
    INSERT INTO transaction_values_test
    values (:a + 2);
    --** SSC-FDM-RS0006 - CALLED PROCEDURE CONTAINS USAGES OF COMMIT/ROLLBACK, MODIFYING THE CURRENT TRANSACTION IN CHILD SCOPES IS NOT SUPPORTED IN SNOWFLAKE **
    CALL transaction_test(:a + 3);
END
$$;
```

### Known Issues

There are no known issues.

### Related EWIs

1. [SSC-FDM-RS0006](../../issues-and-troubleshooting/functional-difference/redshiftFDM#ssc-fdm-rs0006): Called procedure contains usages of COMMIT/ROLLBACK, modifying the current transaction in child scopes is not supported in Snowflake.

## ROLLBACK

### Description

> Stops the current transaction and discards all updates made by that transaction. ([Redshift SQL Language Reference ROLLBACK](https://docs.aws.amazon.com/redshift/latest/dg/r_ROLLBACK.html))

Grammar Syntax

Copy code

```
ROLLBACK [WORK | TRANSACTION]
```

### Sample Source Patterns

#### Setup data

##### Redshift

##### Query

Copy code

```
 CREATE TABLE transaction_values_test
(
    col1 INTEGER
);
```

##### Snowflake

##### Query

Copy code

```
 CREATE TABLE transaction_values_test
(
    col1 INTEGER
);
```

#### ROLLBACK with TRANSACTION keyword

The TRANSACTION keyword is not supported in Snowflake. However, since it does not have an impact on functionality it will just be removed.

##### Redshift

##### Query

Copy code

```
 ROLLBACK TRANSACTION;
```

##### Snowflake

##### Query

Copy code

```
 ROLLBACK;
```

#### ROLLBACK in a default transaction behavior procedure (without NONATOMIC clause)

To avoid out of scope transaction exceptions in Snowflake, the usages of ROLLBACK will be matched with BEGIN TRANSACTION.

When multiple transaction control statements are present in the procedure, multiple BEGIN TRANSACTION statements will be generated after every each one of them to emulate the Redshift transaction behavior.

##### Redshift

##### Query

Copy code

```
 CREATE OR REPLACE PROCEDURE transaction_test(a INT)
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO transaction_values_test values (a);
    COMMIT;
    insert into transaction_values_test values (80);
    insert into transaction_values_test values (55);
    ROLLBACK;
END
$$;

CALL transaction_test(120);

SELECT * FROM transaction_values_test;
```

##### Result

Copy code

```
+------+
| col1 |
+------+
| 120  |
+------+
```

##### Snowflake

##### Query

Copy code

```
 CREATE OR REPLACE PROCEDURE transaction_test (a INT)
RETURNS VARCHAR
    LANGUAGE SQL
    AS $$
BEGIN
    BEGIN TRANSACTION;
    INSERT INTO transaction_values_test values (:a);
    COMMIT;
    BEGIN TRANSACTION;
    insert into transaction_values_test values (80);
    insert into transaction_values_test values (55);
    ROLLBACK;
END
$$;

CALL transaction_test(120);

SELECT * FROM
    transaction_values_test;
```

##### Result

Copy code

```
+------+
| col1 |
+------+
| 120  |
+------+
```

#### ROLLBACK in a procedure with NONATOMIC behavior

The NONATOMIC behavior from Redshift is emulated in Snowflake by using the session parameter AUTOCOMMIT set to true.

Since the AUTOCOMMIT session parameter is assumed to be true, the ROLLBACK statement inside NONATOMIC procedures is left as is.

##### Redshift

##### Query

Copy code

```
 CREATE OR REPLACE PROCEDURE nonatomic_procedure(a int)
    NONATOMIC
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO transaction_values_test values (a);
    INSERT INTO transaction_values_test values (a + 1);
    ROLLBACK;
    INSERT INTO transaction_values_test values (a + 2);
    INSERT INTO transaction_values_test values (a + 3);
    COMMIT;
END
$$;

CALL nonatomic_procedure(10);

SELECT * FROM transaction_values_test;
```

##### Result

Copy code

```
+------+
| col1 |
+------+
| 10   |
| 11   |
| 12   |
| 13   |
+------+
```

##### Snowflake

##### Query

Copy code

```
 CREATE OR REPLACE PROCEDURE nonatomic_procedure (a int)
RETURNS VARCHAR
--    --** SSC-FDM-RS0008 - SNOWFLAKE USES AUTOCOMMIT BY DEFAULT. **
--    NONATOMIC
    LANGUAGE SQL
    COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
    AS $$
BEGIN
    INSERT INTO transaction_values_test
    values (:a);
    INSERT INTO transaction_values_test
    values (:a + 1);
    ROLLBACK;
    INSERT INTO transaction_values_test
    values (:a + 2);
    INSERT INTO transaction_values_test
    values (:a + 3);
    COMMIT;
END
$$;

CALL nonatomic_procedure(10);

SELECT * FROM
transaction_values_test;
```

##### Result

Copy code

```
+------+
| col1 |
+------+
| 10   |
| 11   |
| 12   |
| 13   |
+------+
```

### Known Issues

**1. ROLLBACK inside a nested procedure call**

In Redshift, when a ROLLBACK statement is specified in a nested procedure call, the command will commit all pending work from previous statements in the current and parent scopes. Committing the parent scope actions is not supported in Snowflake, when this case is detected an FDM will be generated.

#### Redshift

##### Query

Copy code

```
 CREATE OR REPLACE PROCEDURE transaction_test(a int)
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO transaction_values_test values (a);
    ROLLBACK;
    INSERT INTO transaction_values_test values (a + 1);
END
$$;

CREATE OR REPLACE PROCEDURE nested_transaction_test(a int)
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO transaction_values_test values (a);
    CALL transaction_test(a + 3);
    COMMIT;
END
$$;
```

##### Snowflake

##### Query

Copy code

```
 CREATE OR REPLACE PROCEDURE transaction_test (a int)
RETURNS VARCHAR
    LANGUAGE SQL
    COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
    AS $$
BEGIN
    BEGIN TRANSACTION;
    INSERT INTO transaction_values_test
    values (:a);
    ROLLBACK;
    BEGIN TRANSACTION;
    INSERT INTO transaction_values_test
    values (:a + 1);
    COMMIT;
END
$$;

CREATE OR REPLACE PROCEDURE nested_transaction_test (a int)
RETURNS VARCHAR
    LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
    AS $$
BEGIN
    BEGIN TRANSACTION;
    INSERT INTO transaction_values_test
    values (:a);
    --** SSC-FDM-RS0006 - CALLED PROCEDURE CONTAINS USAGES OF COMMIT/ROLLBACK, MODIFYING THE CURRENT TRANSACTION IN CHILD SCOPES IS NOT SUPPORTED IN SNOWFLAKE **
    CALL transaction_test(:a + 3);
    COMMIT;
END
$$;
```

**2. ROLLBACK of DDL statements**

In Snowflake, DDL statements perform an implicit commit whenever they are executed inside a procedure, making effective all the work before executing the DDL as well as the DDL itself. This causes the ROLLBACK statement to not be able to discard any changes before that point, this issue will be informed using an FDM.

##### Redshift

##### Query

Copy code

```
 CREATE OR REPLACE PROCEDURE rollback_ddl(a int)
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO transaction_values_test values (a);
    CREATE TABLE someRollbackTable
    (
        col1 INTEGER
    );

    INSERT INTO someRollbackTable values (a);
    ROLLBACK;
END
$$;
```

##### Snowflake

##### Query

Copy code

```
 CREATE OR REPLACE PROCEDURE rollback_ddl (a int)
RETURNS VARCHAR
    LANGUAGE SQL
    COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
    AS $$
BEGIN
    BEGIN TRANSACTION;
    INSERT INTO transaction_values_test
    values (:a);
    CREATE TABLE someRollbackTable
    (
        col1 INTEGER
    );
    BEGIN TRANSACTION;
    INSERT INTO someRollbackTable
    values (:a);
    --** SSC-FDM-RS0007 - DDL STATEMENTS PERFORM AN AUTOMATIC COMMIT IN SNOWFLAKE. ROLLBACK WILL NOT UNDO DDL-COMMITTED CHANGES. **
    ROLLBACK;
END
$$;
```

### Known Issues

There are no known issues.

### Related EWIs

1. [SSC-FDM-RS0006](../../issues-and-troubleshooting/functional-difference/redshiftFDM#ssc-fdm-rs0006): Called procedure contains usages of COMMIT/ROLLBACK, modifying the current transaction in child scopes is not supported in Snowflake.
2. [SSC-FDM-RS0007](../../issues-and-troubleshooting/functional-difference/redshiftFDM#ssc-fdm-rs0007): DDL statements perform an automatic COMMIT in Snowflake. ROLLBACK will not undo DDL-committed changes.

## TRUNCATE

### Description

> Deletes all of the rows from a table without doing a table scan ([Redshift SQL Language Reference TRUNCATE](https://docs.aws.amazon.com/redshift/latest/dg/r_TRUNCATE.html))

Grammar Syntax

Copy code

```
TRUNCATE [TABLE] table_name
```

### Sample Source Patterns

#### Setup data

##### Redshift

##### Query

Copy code

```
 CREATE TABLE transaction_values_test
(
    col1 INTEGER
);
```

##### Snowflake

##### Query

Copy code

```
 CREATE TABLE transaction_values_test
(
    col1 INTEGER
);
```

#### TRUNCATE in a default transaction behavior procedure (without NONATOMIC clause)

Since the TRUNCATE statement automatically commits the transaction it is executed in, any of its usages will generate a COMMIT statement in Snowflake to emulate this behavior.

Since a COMMIT statement is generated the same BEGIN TRANSACTION statement generation will be applied to TRUNCATE. For more information check the [COMMIT translation specification](#commit-in-a-default-transaction-behavior-procedure-without-nonatomic-clause).

##### Redshift

##### Query

Copy code

```
 CREATE OR REPLACE PROCEDURE truncate_in_procedure(a int)
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO transaction_values_test VALUES (a);
    TRUNCATE TABLE transaction_values_test;
    INSERT INTO transaction_values_test VALUES (a + 12);
    COMMIT;
END
$$;

CALL truncate_in_procedure(10);

SELECT * FROM transaction_values_test;
```

##### Result

Copy code

```
+------+
| col1 |
+------+
| 22   |
+------+
```

##### Snowflake

##### Query

Copy code

```
 CREATE OR REPLACE PROCEDURE truncate_in_procedure (a int)
RETURNS VARCHAR
    LANGUAGE SQL
    AS $$
BEGIN
    BEGIN TRANSACTION;
    INSERT INTO transaction_values_test
    VALUES (:a);
    TRUNCATE TABLE transaction_values_test;
    COMMIT;
    BEGIN TRANSACTION;
    INSERT INTO transaction_values_test
    VALUES (:a + 12);
    COMMIT;
END
$$;

CALL truncate_in_procedure(10);

SELECT * FROM
    transaction_values_test;
```

##### Result

Copy code

```
+------+
| col1 |
+------+
| 22   |
+------+
```

#### TRUNCATE in a procedure with NONATOMIC behavior

The NONATOMIC behavior from Redshift is emulated in Snowflake by using the session parameter AUTOCOMMIT set to true.

Since the AUTOCOMMIT session parameter is assumed to be true, the TRUNCATE statement inside NONATOMIC procedures is left as is, there is no need to generate a COMMIT statement because every statement is automatically committed when executed.

##### Redshift

##### Query

Copy code

```
 CREATE OR REPLACE PROCEDURE nonatomic_procedure(a int)
    NONATOMIC
    LANGUAGE plpgsql
    AS $$
BEGIN
    TRUNCATE TABLE transaction_values_test;
    INSERT INTO transaction_values_test values (a);
    INSERT INTO transaction_values_test values (a + 1);
    ROLLBACK;
    INSERT INTO transaction_values_test values (a + 2);
    INSERT INTO transaction_values_test values (a + 3);
    COMMIT;
END
$$;

CALL nonatomic_procedure(10);

SELECT * FROM transaction_values_test;
```

##### Result

Copy code

```
+------+
| col1 |
+------+
| 10   |
| 11   |
| 12   |
| 13   |
+------+
```

##### Snowflake

##### Query

Copy code

```
 CREATE OR REPLACE PROCEDURE nonatomic_procedure (a int)
RETURNS VARCHAR
--    --** SSC-FDM-RS0008 - SNOWFLAKE USES AUTOCOMMIT BY DEFAULT. **
--    NONATOMIC
    LANGUAGE SQL
    COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
    AS $$
BEGIN
    TRUNCATE TABLE transaction_values_test;
    INSERT INTO transaction_values_test
    values (:a);
    INSERT INTO transaction_values_test
    values (:a + 1);
    ROLLBACK;
    INSERT INTO transaction_values_test
    values (:a + 2);
    INSERT INTO transaction_values_test
    values (:a + 3);
    COMMIT;
END
$$;

CALL nonatomic_procedure(10);

SELECT * FROM
transaction_values_test;
```

##### Result

Copy code

```
+------+
| col1 |
+------+
| 10   |
| 11   |
| 12   |
| 13   |
+------+
```

### Known Issues

**1. TRUNCATE inside a nested procedure call**

In Redshift, when a COMMIT statement is specified in a nested procedure call, the command will commit all pending work from previous statements in the current and parent scopes. Committing the parent scope actions is not supported in Snowflake, when this case is detected an FDM will be generated.

#### Redshift

##### Query

Copy code

```
 CREATE OR REPLACE PROCEDURE transaction_test(a INT)
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO transaction_values_test VALUES (a);
    TRUNCATE TABLE transaction_values_test;
END
$$;

CREATE OR REPLACE PROCEDURE nested_transaction_test(a INT)
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO transaction_values_test values (a);
    INSERT INTO transaction_values_test values (a + 1);
    INSERT INTO transaction_values_test values (a + 2);
    CALL transaction_test(a + 3);
END
$$;
```

##### Snowflake

##### Query

Copy code

```
 CREATE OR REPLACE PROCEDURE transaction_test (a INT)
RETURNS VARCHAR
    LANGUAGE SQL
    COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
    AS $$
BEGIN
    BEGIN TRANSACTION;
    INSERT INTO transaction_values_test
    VALUES (:a);
    TRUNCATE TABLE transaction_values_test;
    COMMIT;
END
$$;

CREATE OR REPLACE PROCEDURE nested_transaction_test (a INT)
RETURNS VARCHAR
    LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
    AS $$
BEGIN
    INSERT INTO transaction_values_test
    values (:a);
    INSERT INTO transaction_values_test
    values (:a + 1);
    INSERT INTO transaction_values_test
    values (:a + 2);
    --** SSC-FDM-RS0006 - CALLED PROCEDURE CONTAINS USAGES OF COMMIT/ROLLBACK, MODIFYING THE CURRENT TRANSACTION IN CHILD SCOPES IS NOT SUPPORTED IN SNOWFLAKE **
    CALL transaction_test(:a + 3);
END
$$;
```

### Known Issues

There are no known issues.

### Related EWIs

1. [SSC-FDM-RS0006](../../issues-and-troubleshooting/functional-difference/redshiftFDM#ssc-fdm-rs0006): Called procedure contains usages of COMMIT/ROLLBACK, modifying the current transaction in child scopes is not supported in Snowflake.

## CONDITIONS

## CASE

### Description

> The `CASE` statement in Redshift lets you return values based on conditions, enabling conditional logic in queries. It has two forms: simple and searched. ([Redshift SQL Language Reference Conditionals: Case](https://docs.aws.amazon.com/redshift/latest/dg/c_PLpgSQL-statements.html#r_PLpgSQL-conditionals-case)).

### Simple Case

A simple CASE statement provides conditional execution based on equality of operands.

Note

:class: tip
Simple Case are fully supported by [Snowflake](https://docs.snowflake.com/en/developer-guide/snowflake-scripting/variables#declaring-a-variable).

### Grammar Syntax

Copy code

```
 CASE search-expression
WHEN expression [, expression [ ... ]] THEN
  statements
[ WHEN expression [, expression [ ... ]] THEN
  statements
  ... ]
[ ELSE
  statements ]
END CASE;
```

### Sample Source Patterns

#### Input Code:

##### Redshift

Copy code

```
 CREATE OR REPLACE PROCEDURE proc1(x INT)
LANGUAGE plpgsql
AS $$
BEGIN
  CASE x
WHEN 1, 2 THEN
  NULL;
ELSE
  NULL;
END CASE;
END;
$$;
```

##### Output Code:

##### Redshift

Copy code

```
 CREATE OR REPLACE PROCEDURE proc1 (x INT)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "02/14/2025",  "domain": "test" }}'
AS $$
BEGIN
  CASE x
    WHEN 1 THEN
      NULL;
    WHEN 2 THEN
      NULL;
   ELSE
     NULL;
  END CASE;
END;
$$;
```

### Searched Case

Note

:class: tip
Searched Case are fully supported by [Snowflake](https://docs.snowflake.com/en/developer-guide/snowflake-scripting/variables#declaring-a-variable).

### Grammar Syntax

Copy code

```
 CASE
WHEN boolean-expression THEN
  statements
[ WHEN boolean-expression THEN
  statements
  ... ]
[ ELSE
  statements ]
END CASE;
```

### Sample Source Patterns

#### Input Code:

##### Redshift

Copy code

```
 CREATE PROCEDURE PROC1 (paramNumber int)
LANGUAGE plpgsql
AS $$
DECLARE
    result VARCHAR(100);
BEGIN
CASE
  WHEN paramNumber BETWEEN 0 AND 10 THEN
    result := 'value is between zero and ten';
  WHEN paramNumber BETWEEN 11 AND 20 THEN
    result := 'value is between eleven and twenty';
  END CASE;
END;
$$;
```

##### Output Code:

##### Redshift

Copy code

```
 CREATE PROCEDURE PROC1 (paramNumber int)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}'
AS $$
    DECLARE
      result VARCHAR(100);
      case_not_found EXCEPTION (-20002, 'Case not found.');
BEGIN
CASE
  WHEN paramNumber BETWEEN 0 AND 10 THEN
    result := 'value is between zero and ten';
  WHEN paramNumber BETWEEN 11 AND 20 THEN
    result := 'value is between eleven and twenty';
  ELSE
    RAISE case_not_found;
  END CASE;
END;
$$;
```

#### CASE Without ELSE

In Redshift, when a `CASE` expression is executed and none of the validated conditions are met, and there is no `ELSE` defined, the exception ‘CASE NOT FOUND’ is triggered. In Snowflake, the code executes but returns no result. To maintain the same functionality in Snowflake in this scenario, an exception with the same name will be declared and executed if none of the `CASE` conditions are met.

Note

:class: tip
Case Without Else are fully supported by [Snowflake](https://docs.snowflake.com/en/developer-guide/snowflake-scripting/variables#declaring-a-variable).

##### Input Code:

##### Redshift

Copy code

```
 CREATE OR REPLACE PROCEDURE procedure1 (input_value INT)
AS $$
BEGIN
  CASE input_value
  WHEN 1 THEN
   NULL;
  END CASE;
END;
$$ LANGUAGE plpgsql;
```

##### Output Code:

##### Redshift

Copy code

```
 CREATE OR REPLACE PROCEDURE procedure1 (input_value INT)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
AS $$
    DECLARE
      case_not_found EXCEPTION (-20002, 'Case not found.');
BEGIN
  CASE input_value
  WHEN 1 THEN
   NULL;
  ELSE
   RAISE case_not_found;
  END CASE;
END;
$$;
```

### Known Issues

There are no known issues.

### Related EWIs.

There are no related EWIs.

## IF

### Description

> This statement allows you to make decisions based on certain conditions. ([Redshift SQL Language Reference Conditionals: IF](https://docs.aws.amazon.com/redshift/latest/dg/c_PLpgSQL-statements.html#r_PLpgSQL-conditionals-if)).

The parenthesis will be added in the conditions and the keyword ELSIF will be changed to ELSEIF since Redshift does not require the parenthesis in the conditions and ELSIF is the keyword.

### Grammar Syntax

Copy code

```
 IF boolean-expression THEN
  statements
[ ELSIF boolean-expression THEN
  statements
[ ELSIF boolean-expression THEN
  statements
    ...] ]
[ ELSE
  statements ]
END IF;
```

### Sample Source Patterns

#### Input Code:

##### Redshift

Copy code

```
 CREATE PROCEDURE PROC1 (paramNumber int)
LANGUAGE plpgsql
AS $$
DECLARE
    result VARCHAR(100);
BEGIN
    IF paramNumber = 0 THEN
      result := 'zero';
    ELSIF paramNumber > 0 THEN
      result := 'positive';
    ELSIF paramNumber < 0 THEN
      result := 'negative';
    ELSE
      result := 'NULL';
    END IF;
END;
$$;
```

##### Output Code:

##### Redshift

Copy code

```
 CREATE PROCEDURE PROC1 (paramNumber int)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}'
AS $$
        DECLARE
            result VARCHAR(100);
BEGIN
            IF (:paramNumber = 0) THEN
                result := 'zero';
            ELSEIF (:paramNumber > 0) THEN
                result := 'positive';
            ELSEIF (:paramNumber < 0) THEN
                result := 'negative';
              ELSE
                result := 'NULL';
            END IF;
END;
$$;
```

### Known Issues

There are no known issues.

### Related EWIs.

There are no related EWIs.

## LOOPS

### Description

These statements are used to repeat a block of code until the specified condition. ([Redshift SQL Language Reference Loops](https://docs.aws.amazon.com/redshift/latest/dg/c_PLpgSQL-statements.html#r_PLpgSQL-loops)).

[CONTINUE](#continue)
[FOR](#for)
[LOOP](#loop)
[WHILE](#while)
[EXIT](#exit)

## CONTINUE

### Description

> When the CONTINUE conditions are true, the loop can continue the execution, when is false stop the loop. ([Redshift SQL Language Reference Conditionals: CONTINUE](https://docs.aws.amazon.com/redshift/latest/dg/c_PLpgSQL-statements.html#r_PLpgSQL-loops)).

Warning

CONTINUE are partial supported by [Snowflake](https://docs.snowflake.com/en/developer-guide/snowflake-scripting/variables#declaring-a-variable).

### Grammar Syntax

Copy code

```
 CONTINUE [ label ] [ WHEN expression ];
```

### Sample Source Patterns

#### Input Code:

##### Redshift

Copy code

```
 CREATE OR REPLACE PROCEDURE procedure1 (x INT)
    LANGUAGE plpgsql
AS $$
DECLARE
    i INTEGER := 0;
BEGIN
    <<simple_loop_when>>
    LOOP
        i := i + 1;
        CONTINUE WHEN i = 5;
        RAISE INFO 'i %', i;
        EXIT simple_loop_when WHEN (i >= x);
    END LOOP;
END;
$$;

CREATE OR REPLACE PROCEDURE procedure11 (x INT)
    LANGUAGE plpgsql
AS $$
DECLARE
    i INTEGER := 0;
BEGIN
    LOOP
        i := i + 1;
		IF (I = 5) THEN
        	CONTINUE;
		END IF;
        RAISE INFO 'i %', i;
        EXIT WHEN (i >= x);
    END LOOP;
END;
$$;
```

##### Results

| Console Output |
| --- |
| 1 |
| 2 |
| 3 |
| 4 |
| 6 |
| 7 |

Expand

Show lessSee more

##### Output Code:

##### Snowflake

Copy code

```
 CREATE OR REPLACE PROCEDURE procedure1 (x INT)
RETURNS VARCHAR
    LANGUAGE SQL
    COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}'
AS $$
    		DECLARE
    			i INTEGER := 0;
BEGIN
    			--** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
    LOOP
        i := i + 1;
        IF (:i = 5) THEN
        	CONTINUE;
        END IF;
        CALL RAISE_MESSAGE_UDF('INFO', 'i %', array_construct(:i));
        IF ((:i >= : x)) THEN
        	EXIT simple_loop_when;
        END IF;
    END LOOP simple_loop_when;
END;
$$;

CREATE OR REPLACE PROCEDURE procedure11 (x INT)
RETURNS VARCHAR
    LANGUAGE SQL
    COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}'
AS $$
    		DECLARE
    			i INTEGER := 0;
BEGIN
    			--** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
    LOOP
        i := i + 1;
		IF (:I = 5) THEN
        	CONTINUE;
		END IF;
        CALL RAISE_MESSAGE_UDF('INFO', 'i %', array_construct(:i));
        IF ((:i >= : x)) THEN
        	EXIT;
        END IF;
    END LOOP;
END;
$$;
```

##### Results

| Console Output |
| --- |
| 1 |
| 2 |
| 3 |
| 4 |
| 6 |
| 7 |

Expand

Show lessSee more

### Known Issues

There are no known issues.

### Related EWIs.

There are no related EWIs.

## EXIT

### Description

> Stop the loop execution when the conditions defined in the WHEN statement are true ([Redshift SQL Language Reference Conditionals: EXIT](https://docs.aws.amazon.com/redshift/latest/dg/c_PLpgSQL-statements.html#r_PLpgSQL-loops)).

Warning

EXIT are partial supported by [Snowflake](https://docs.snowflake.com/en/developer-guide/snowflake-scripting/variables#declaring-a-variable).

### Grammar Syntax

Copy code

```
 EXIT [ label ] [ WHEN expression ];
```

### Sample Source Patterns

#### Input Code:

##### Redshift

Copy code

```
 CREATE OR REPLACE PROCEDURE simple_loop_when(x int)
LANGUAGE plpgsql
AS $$
DECLARE i INTEGER := 0;
BEGIN
  <<simple_loop_when>>
  LOOP
    RAISE INFO 'i %', i;
    i := i + 1;
    EXIT simple_loop_when WHEN (i >= x);
  END LOOP;
END;
$$;
```

##### Output Code:

##### Redshift

Copy code

```
 CREATE OR REPLACE PROCEDURE simple_loop_when (x int)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}'
AS $$
    DECLARE
      i INTEGER := 0;
BEGIN
      --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
  LOOP
        CALL RAISE_MESSAGE_UDF('INFO', 'i %', array_construct(:i));
    i := i + 1;
        IF ((:i >= : x)) THEN
          EXIT simple_loop_when;
        END IF;
  END LOOP simple_loop_when;
END;
$$;
```

### Known Issues

There are no known issues.

### Related EWIs.

There are no related EWIs.

## FOR

### Grammar Syntax

Integer variant

Copy code

```
 [<<label>>]
FOR name IN [ REVERSE ] expression .. expression LOOP
  statements
END LOOP [ label ];
```

### Sample Source Patterns

#### Input Code:

##### Redshift

Copy code

```
 CREATE OR REPLACE PROCEDURE procedure1 ()
AS $$
BEGIN
  FOR i IN 1..10 LOOP
    NULL;
  END LOOP;

  FOR i IN REVERSE 10..1 LOOP
    NULL;
  END LOOP;
END;
$$ LANGUAGE plpgsql;
```

##### Output Code:

##### Redshift

Copy code

```
 CREATE OR REPLACE PROCEDURE procedure1 ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}'
AS $$
BEGIN
  FOR i IN 1 TO 10
                   --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
                   LOOP
    NULL;
  END LOOP;

  FOR i IN REVERSE 10 TO 1
                           --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
                           LOOP
    NULL;
  END LOOP;
END;
$$;
```

### Known Issues

There are no known issues.

### Related EWIs.

1. [SSC-EWI-PG0006](../../issues-and-troubleshooting/conversion-issues/postgresqlEWI#ssc-ewi-pg0006): Reference a variable using the Label is not supported by Snowflake.

## LOOP

### Description

> A simple loop defines an unconditional loop that is repeated indefinitely until terminated by an EXIT or RETURN statement. ([Redshift SQL Language Reference Conditionals: Simple Loop](https://docs.aws.amazon.com/redshift/latest/dg/c_PLpgSQL-statements.html#r_PLpgSQL-loops)).

Warning

Simple Loop are partial supported by [Snowflake](https://docs.snowflake.com/en/developer-guide/snowflake-scripting/variables#declaring-a-variable).

### Grammar Syntax

Copy code

```
 [<<label>>]
LOOP
  statements
END LOOP [ label ];
```

### Sample Source Patterns

#### Input Code:

##### Redshift

Copy code

```
 CREATE OR REPLACE PROCEDURE simple_loop()
LANGUAGE plpgsql
AS $$
BEGIN
  <<simple_while>>
  LOOP
    RAISE INFO 'I am raised once';
    EXIT simple_while;
    RAISE INFO 'I am not raised';
  END LOOP;
  RAISE INFO 'I am raised once as well';
END;
$$;
```

##### Output Code:

##### Redshift

Copy code

```
 CREATE OR REPLACE PROCEDURE simple_loop ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}'
AS $$
BEGIN
  --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
  LOOP
    CALL RAISE_MESSAGE_UDF('INFO', 'I am raised once');
    EXIT simple_while;
    CALL RAISE_MESSAGE_UDF('INFO', 'I am not raised');
  END LOOP simple_while;
  CALL RAISE_MESSAGE_UDF('INFO', 'I am raised once as well');
END;
$$;
```

### Known Issues

There are no known issues.

### Related EWIs.

There are no related EWIs.

## WHILE

### Grammar Syntax

Copy code

```
 [<<label>>]
WHILE expression LOOP
  statements
END LOOP [ label ];
```

### Sample Source Patterns

#### Input Code:

##### Redshift

Copy code

```
 CREATE OR REPLACE PROCEDURE simple_loop_when()
    LANGUAGE plpgsql
AS $$
DECLARE
    i INTEGER := 0;
BEGIN
    WHILE I > 5 AND I > 10 LOOP
        NULL;
    END LOOP;
END;
$$;
```

##### Output Code:

##### Redshift

Copy code

```
 CREATE OR REPLACE PROCEDURE simple_loop_when ()
RETURNS VARCHAR
    LANGUAGE SQL
    COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}'
AS $$
            DECLARE
                i INTEGER := 0;
BEGIN
                WHILE (:I > 5 AND : I > 10)
                                            --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
                                            LOOP
        NULL;
    END LOOP;
END;
$$;
```

### Known Issues

There are no known issues.

### Related EWIs.

There are no related EWIs.

## CURSORS

## CLOSE CURSOR

### Description

> Closes all of the free resources that are associated with an open cursor.. ([Redshift SQL Language Reference Close Cursor](https://docs.aws.amazon.com/redshift/latest/dg/close.html)).

Note

:class: tip
This syntax is fully supported in Snowflake.

### Grammar Syntax

Copy code

```
 CLOSE cursor
```

### Sample Source Patterns

#### Input Code:

##### Redshift

Copy code

```
 CREATE OR REPLACE PROCEDURE cursor_test()
AS $$
BEGIN
   CLOSE cursor1;
END;
$$;
```

##### Output Code:

##### Redshift

Copy code

```
 CREATE OR REPLACE PROCEDURE cursor_test ()
RETURNS VARCHAR
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "02/05/2025",  "domain": "test" }}'
AS $$
BEGIN
   CLOSE cursor1;
END;
$$;
```

### Known Issues

There are no known issues.

### Related EWIs.

There are no related EWIs.

## FETCH CURSOR

### Description

> Retrieves rows using a cursor. ([Redshift SQL Language reference Fetch](https://docs.aws.amazon.com/redshift/latest/dg/fetch.html))

Transformation information

Copy code

```
 FETCH [ NEXT | ALL | {FORWARD [ count | ALL ] } ] FROM cursor

FETCH cursor INTO target [, target ...];
```

### Sample Source Patterns

#### Setup data

##### Redshift

##### Query

Copy code

```
 CREATE TABLE cursor_example
(
	col1 INTEGER,
	col2 VARCHAR(20)
);

INSERT INTO cursor_example VALUES (10, 'hello');
```

##### Snowflake

##### Query

Copy code

```
 CREATE TABLE cursor_example
(
	col1 INTEGER,
	col2 VARCHAR(20)
);

INSERT INTO cursor_example VALUES (10, 'hello');
```

#### Fetch into

The FETCH into statement from Redshift is fully equivalent in Snowflake

##### Redshift

##### Query

Copy code

```
 CREATE OR REPLACE PROCEDURE fetch_into_example()
LANGUAGE plpgsql
AS $$
DECLARE my_cursor CURSOR FOR
        SELECT col1, col2
        FROM cursor_example;
        some_id INT;
        message VARCHAR(20);
BEGIN
    OPEN my_cursor;
    FETCH my_cursor INTO some_id, message;
    CLOSE my_cursor;
    INSERT INTO cursor_example VALUES (some_id * 10, message || ' world!');
END;
$$;

CALL fetch_into_example();

SELECT * FROM cursor_example;
```

##### Result

Copy code

```
+------+-------------+
| col1 | col2        |
+------+-------------+
| 10   | hello       |
| 100  | hello world!|
+------+-------------+
```

##### Snowflake

##### Query

Copy code

```
 CREATE OR REPLACE PROCEDURE fetch_into_example ()
RETURNS VARCHAR
LANGUAGE SQL
AS $$
DECLARE
    my_cursor CURSOR FOR
    SELECT col1, col2
    FROM
    cursor_example;
    some_id INT;
    message VARCHAR(20);
BEGIN
    OPEN my_cursor;
    FETCH my_cursor INTO some_id, message;
    CLOSE my_cursor;
    INSERT INTO cursor_example
			VALUES (:some_id * 10, :message || ' world!');
END;
$$;

CALL fetch_into_example();

SELECT * FROM
	cursor_example;
```

##### Result

Copy code

```
+------+-------------+
| col1 | col2        |
+------+-------------+
| 10   | hello       |
| 100  | hello world!|
+------+-------------+
```

### Known Issues

**1. Fetch without target variables is not supported**

Snowflake requires the FETCH statement to specify the INTO clause with the variables where the fetched row values are going to be stored. When a FETCH statement is found in the code with no INTO clause an EWI will be generated.

Input Code:

Copy code

```
 FETCH FORWARD FROM cursor1;
```

Output Code:

Copy code

```
 !!!RESOLVE EWI!!! /*** SSC-EWI-PG0015 - FETCH CURSOR WITHOUT TARGET VARIABLES IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
FETCH FORWARD FROM cursor1;
```

### Known Issues

There are no known issues.

### Related EWIs

1. [SSC-EWI-PG0015](../../issues-and-troubleshooting/conversion-issues/postgresqlEWI#ssc-ewi-pg0015): Fetch cursor without target variables is not supported in Snowflake

## OPEN CURSOR

### Description

> Before you can use a cursor to retrieve rows, it must be opened. ([Redshift SQL Language Reference Open Cursor](https://docs.aws.amazon.com/redshift/latest/dg/c_PLpgSQL-statements.html#r_PLpgSQL-cursors)).

Note

:class: tip
This syntax is fully supported in Snowflake.

### Grammar Syntax

Copy code

```
 OPEN bound_cursor_name [ ( argument_values ) ];
```

### Sample Source Patterns

#### Setup data

##### Redshift

##### Query

Copy code

```
 CREATE TABLE cursor_example
(
	col1 INTEGER,
	col2 VARCHAR(20)
);

CREATE TABLE cursor_example_results
(
	col1 INTEGER,
	col2 VARCHAR(20)
);

INSERT INTO cursor_example VALUES (10, 'hello');
```

##### Snowflake

##### Query

Copy code

```
 CREATE TABLE cursor_example
(
	col1 INTEGER,
	col2 VARCHAR(20)
);

CREATE TABLE cursor_example_results
(
	col1 INTEGER,
	col2 VARCHAR(20)
);

INSERT INTO cursor_example VALUES (10, 'hello');
```

#### Open cursor without arguments

##### Input Code:

##### Redshift

Copy code

```
 CREATE OR REPLACE PROCEDURE cursor_test()
AS $$
BEGIN
   OPEN cursor1;
END;
$$;
```

##### Output Code:

##### Redshift

Copy code

```
 CREATE OR REPLACE PROCEDURE cursor_test ()
RETURNS VARCHAR
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "02/05/2025",  "domain": "test" }}'
AS $$
BEGIN
   OPEN cursor1;
END;
$$;
```

#### Open cursor with arguments

Cursor arguments have to be bound per each one of its uses, the bindings will be generated, as well as reordering and repeating the passed values to the OPEN statement as needed to satisfy the bindings.

##### Redshift

##### Query

Copy code

```
 CREATE OR REPLACE PROCEDURE cursor_open_test()
LANGUAGE plpgsql
AS $$
DECLARE
    cursor2 CURSOR (val1 VARCHAR(20), val2 INTEGER) FOR SELECT col1 + val2, col2 FROM cursor_example where val1 = col2 and val2 > col1;
    res1 INTEGER;
    res2 VARCHAR(20);
BEGIN
    OPEN cursor2('hello', 50);
    FETCH cursor2 INTO res1, res2;
    CLOSE cursor2;
    INSERT INTO cursor_example_results VALUES (res1, res2);
END;
$$;

call cursor_open_test();

SELECT * FROM cursor_example_results;
```

##### Result

Copy code

```
+------+-------+
| col1 | col2  |
+------+-------+
| 60   | hello |
+------+-------+
```

##### Snowflake

##### Query

Copy code

```
 CREATE OR REPLACE PROCEDURE cursor_open_test ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}'
AS $$
        DECLARE
            cursor2 CURSOR FOR SELECT col1 + ?, col2 FROM
                cursor_example
            where
                ? = col2 and ? > col1;
            res1 INTEGER;
            res2 VARCHAR(20);
BEGIN
    OPEN cursor2 USING (50, 'hello', 50);
    FETCH cursor2 INTO res1, res2;
    CLOSE cursor2;
    INSERT INTO cursor_example_results
            VALUES (:res1, : res2);
END;
$$;

call cursor_open_test();
SELECT * FROM
cursor_example_results;
```

##### Result

Copy code

```
+------+-------+
| col1 | col2  |
+------+-------+
| 60   | hello |
+------+-------+
```

#### Open cursor with procedure parameters or local variables

The procedure parameters or local variables have to be bound per each one of its uses in the cursor query, the bindings will be generated and the parameter or variable names will be added to the OPEN statement, even if the cursor originally had no parameters.

##### Redshift

##### Query

Copy code

```
 CREATE OR REPLACE PROCEDURE cursor_open_test(someValue iNTEGER)
LANGUAGE plpgsql
AS $$
DECLARE
    charVariable VARCHAR(20) DEFAULT 'hello';
    cursor2 CURSOR FOR SELECT col1 + someValue, col2 FROM cursor_example where charVariable = col2 and someValue > col1;
    res1 INTEGER;
    res2 VARCHAR(20);
BEGIN
    OPEN cursor2;
    FETCH cursor2 INTO res1, res2;
    CLOSE cursor2;
    INSERT INTO cursor_example_results VALUES (res1, res2);
END;
$$;

call cursor_open_test(30);
```

##### Result

Copy code

```
+------+-------+
| col1 | col2  |
+------+-------+
| 40   | hello |
+------+-------+
```

##### Snowflake

##### Query

Copy code

```
 CREATE OR REPLACE PROCEDURE cursor_open_test (someValue iNTEGER)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}'
AS $$
        DECLARE
            charVariable VARCHAR(20) DEFAULT 'hello';
            cursor2 CURSOR FOR SELECT col1 + ?, col2 FROM
                cursor_example
            where
                ? = col2 and ? > col1;
            res1 INTEGER;
            res2 VARCHAR(20);
BEGIN
    OPEN cursor2 USING (someValue, charVariable, someValue);
    FETCH cursor2 INTO res1, res2;
    CLOSE cursor2;
    INSERT INTO cursor_example_results
            VALUES (:res1, : res2);
END;
$$;

call cursor_open_test(30);
```

##### Result

Copy code

```
+------+-------+
| col1 | col2  |
+------+-------+
| 40   | hello |
+------+-------+
```

### Known Issues

There are no known issues.

### Related EWIs.

There are no related EWIs.

## DECLARE CURSOR

### Description

> Defines a new cursor. Use a cursor to retrieve a few rows at a time from the result set of a larger query. ([Redshift SQL Language Reference Declare Cursor](https://docs.aws.amazon.com/redshift/latest/dg/declare.html)).

Note

:class: tip
This syntax is fully supported in Snowflake.

### Grammar Syntax

Copy code

```
 name CURSOR [ ( arguments ) ] FOR query
```

### Sample Source Patterns

#### Input Code:

### Input Code:

#### Redshift

Copy code

```
 CREATE OR REPLACE PROCEDURE cursor_test()
AS $$
DECLARE
   -- Declare the cursor
   cursor1 CURSOR FOR SELECT 1;
   cursor2 CURSOR (key integer) FOR SELECT 2 where 1 = key;

BEGIN
END;
$$;
```

##### Output Code:

##### Redshift

Copy code

```
 CREATE OR REPLACE PROCEDURE cursor_test ()
RETURNS VARCHAR
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
AS $$
      DECLARE
         -- Declare the cursor
         cursor1 CURSOR FOR SELECT 1;
         cursor2 CURSOR FOR SELECT 2 where 1 = ?;
BEGIN
         NULL;
END;
$$;
```

### Known Issues

There are no known issues.

### Related EWIs.

There are no related EWIs.

## DECLARE REFCURSOR

### Description

> A `refcursor` data type simply holds a reference to a cursor. You can create a cursor variable by declaring it as a variable of type `refcursor`
>
> ([Redshift SQL Language Reference Refcursor Declaration](https://docs.aws.amazon.com/redshift/latest/dg/c_PLpgSQL-statements.html#r_PLpgSQL-cursors))

Note

:class: tip
Refcursor declarations are fully supported by [Snowflake](https://docs.snowflake.com/en/developer-guide/snowflake-scripting/variables#declaring-a-variable).

### Grammar Syntax

Copy code

```
 DECLARE
name refcursor;
```

Since Snowflake does not support the `REFCURSOR` data type, its functionality is replicated by converting the `REFCURSOR` variable into a `RESULTSET` type. The query used to open the `REFCURSOR` is assigned to the `RESULTSET` variable, after which a new cursor is created and linked to the `RESULTSET` variable. Additionally, all references to the original `REFCURSOR` within the cursor logic are updated to use the new cursor, thereby replicating the original functionality.

### Sample Source Patterns

#### Case: Single use

##### Input Code:

##### Redshift

Copy code

```
 CREATE OR REPLACE PROCEDURE VARIABLE_REFCURSOR()
LANGUAGE plpgsql
AS $$
DECLARE
  v_curs1 refcursor;
BEGIN
  OPEN v_curs1 FOR SELECT column1_name, column2_name FROM your_table;
-- Cursor logic
  CLOSE v_curs1;
 END;
$$;
```

##### Output Code:

##### Snowflake

Copy code

```
 CREATE OR REPLACE PROCEDURE VARIABLE_REFCURSOR ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
AS $$
  DECLARE
   v_curs1 RESULTSET;
BEGIN
   v_curs1 := (
    SELECT column1_name, column2_name FROM your_table
   );
   LET v_curs1_Resultset_1 CURSOR
   FOR
    v_curs1;
   OPEN v_curs1_Resultset_1;
-- Cursor logic
  CLOSE v_curs1_Resultset_1;
 END;
$$;
```

##### Case: Cursor with Dynamic Sql

##### Input Code:

##### Redshift

Copy code

```
 CREATE OR REPLACE PROCEDURE VARIABLE_REFCURSOR_DYNAMIC(min_salary NUMERIC)
LANGUAGE plpgsql
AS $$
DECLARE
    cur refcursor;
    qry TEXT;
BEGIN
    qry := 'SELECT id, name FROM employees WHERE salary > ' || min_salary;

    OPEN cur FOR EXECUTE qry;
-- Cursor logic
    CLOSE cur;
END;
$$;

CREATE OR REPLACE PROCEDURE VARIABLE_REFCURSOR_DYNAMIC2(min_salary NUMERIC)
LANGUAGE plpgsql
AS $$
DECLARE
    cur refcursor;
BEGIN
    OPEN cur FOR EXECUTE 'SELECT id, name FROM employees WHERE salary > ' || min_salary;
-- Cursor logic
    CLOSE cur;
END;
$$;
```

##### Output Code:

##### Redshift

Copy code

```
 CREATE OR REPLACE PROCEDURE VARIABLE_REFCURSOR_DYNAMIC (min_salary NUMERIC)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
AS $$
        DECLARE
            cur RESULTSET;
    qry TEXT;
BEGIN
    qry := 'SELECT id, name FROM employees WHERE salary > ' || min_salary;
            cur := (
                EXECUTE IMMEDIATE qry
            );
            LET cur_Resultset_1 CURSOR
            FOR
                cur;
            OPEN cur_Resultset_1;
-- Cursor logic
    CLOSE cur_Resultset_1;
END;
$$;

CREATE OR REPLACE PROCEDURE VARIABLE_REFCURSOR_DYNAMIC2 (min_salary NUMERIC)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
AS $$
        DECLARE
            cur RESULTSET;
BEGIN
            cur := (
                EXECUTE IMMEDIATE 'SELECT id, name FROM employees WHERE salary > ' || min_salary
            );
            LET cur_Resultset_2 CURSOR
            FOR
                cur;
            OPEN cur_Resultset_2;
-- Cursor logic
    CLOSE cur_Resultset_2;
END;
$$;
```

##### Case: Multiple uses:

##### Input Code:

##### Redshift

Copy code

```
 CREATE OR REPLACE PROCEDURE VARIABLE_REFCURSOR()
LANGUAGE plpgsql
AS $$
DECLARE
  v_curs1 refcursor;
BEGIN
  OPEN v_curs1 FOR SELECT column1_name, column2_name FROM your_table;
-- Cursor logic
  CLOSE v_curs1;
  OPEN v_curs1 FOR SELECT column3_name, column4_name FROM your_table2;
-- Cursor logic
  CLOSE v_curs1;
 END;
$$;
```

##### Output Code:

##### Snowflake

Copy code

```
 CREATE OR REPLACE PROCEDURE VARIABLE_REFCURSOR ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
AS $$
  DECLARE
   v_curs1 RESULTSET;
BEGIN
   v_curs1 := (
    SELECT column1_name, column2_name FROM your_table
   );
   LET v_curs1_Resultset_1 CURSOR
   FOR
    v_curs1;
   OPEN v_curs1_Resultset_1;
-- Cursor logic
  CLOSE v_curs1_Resultset_1;
   v_curs1 := (
    SELECT column3_name, column4_name FROM your_table2
   );
   LET v_curs1_Resultset_2 CURSOR
   FOR
    v_curs1;
   OPEN v_curs1_Resultset_2;
-- Cursor logic
  CLOSE v_curs1_Resultset_2;
 END;
$$;
```

### Known Issues

There are no known issues.

### Related EWIs.

There are no related EWIs.
