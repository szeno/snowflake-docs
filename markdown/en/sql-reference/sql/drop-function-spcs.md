# DROP FUNCTION (Snowpark Container Services)

Removes the specified [service function](/developer-guide/snowpark-container-services/working-with-services#label-snowpark-containers-service-communicating-service-function).

See also:
:   [Service functions](/developer-guide/snowpark-container-services/working-with-services#label-snowpark-containers-service-communicating-service-function), [CREATE FUNCTION](/sql-reference/sql/create-function-spcs), [ALTER FUNCTION](/sql-reference/sql/alter-function-spcs), [DESC FUNCTION](/sql-reference/sql/desc-function-spcs)

## Syntax

Copy code

```
DROP FUNCTION [ IF EXISTS ] <name> ( [ <arg_data_type> , ... ] )
```

## Parameters

`name`
:   Specifies the identifier for the service function to drop. If the identifier contains spaces or special characters, the entire string must be
    enclosed in double quotes. Identifiers enclosed in double quotes are also case sensitive.

`arg_data_type [ , ... ]`
:   Specifies the data type of the argument(s), if any, for the service function. The argument types are necessary because service functions support name
    overloading (that is, two service functions in the same schema can have the same name) and the argument types are used to identify the UDF you
    wish to drop.

## Usage notes

- Dropped functions can’t be recovered; they must be recreated.

- When the IF EXISTS clause is specified and the target object doesn’t exist, the command completes successfully
  without returning an error.

## Examples

This demonstrates the DROP FUNCTION command:

Copy code

```
DROP FUNCTION my_echo_udf(VARCHAR);
```

Example output:

```
+-----------------------------------+
| status                            |
|-----------------------------------|
| MY_ECHO_UDF successfully dropped. |
+-----------------------------------+
```
