# DROP FUNCTION

Removes the specified user-defined function (UDF) or external function from the current/specified schema.

See also:
:   [CREATE FUNCTION](/sql-reference/sql/create-function) , [ALTER FUNCTION](/sql-reference/sql/alter-function) , [SHOW FUNCTIONS](/sql-reference/sql/show-functions), [DESCRIBE FUNCTION](/sql-reference/sql/desc-function)

## Syntax

Copy code

```
DROP FUNCTION [ IF EXISTS ] <name> ( [ <arg_data_type> , ... ] )
```

## Parameters

`name`
:   Specifies the identifier for the UDF to drop. If the identifier contains spaces or special characters, the entire string must be
    enclosed in double quotes. Identifiers enclosed in double quotes are also case-sensitive.

`arg_data_type [ , ... ]`
:   Specifies the data type of the argument(s), if any, for the UDF. The argument types are necessary because UDFs support name
    overloading (i.e. two UDFs in the same schema can have the same name) and the argument types are used to identify the UDF you
    wish to drop.

## Usage notes

**All Languages**

- Dropped functions can’t be recovered; they must be recreated.

- When the IF EXISTS clause is specified and the target object doesn’t exist, the command completes successfully
  without returning an error.

**Java, Python, and Scala**

- For UDFs that store code in a file (such as a .jar file or .py file) in a stage, the `DROP FUNCTION` command does not remove
  the file. Different UDFs can use different functions/methods in the same file, so the file should not be removed while any UDF
  refers to it. Snowflake does not store a count of the number of references to each staged file and does not remove that staged
  file when there are no remaining references.

## Examples

This demonstrates the DROP FUNCTION command:

> Copy code
>
> ```
> DROP FUNCTION multiply(number, number);
>
> --------------------------------+
>              status             |
> --------------------------------+
>  MULTIPLY successfully dropped. |
> --------------------------------+
> ```
