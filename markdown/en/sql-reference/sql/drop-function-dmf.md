# DROP FUNCTION (DMF)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Removes the specified data metric function (DMF) from the current or specified schema.

## Syntax

Copy code

```
DROP FUNCTION [ IF EXISTS ] <name>(
TABLE(  <arg_data_type> [ , ... ] ) [ , TABLE( <arg_data_type> [ , ... ] ) ]
)
```

## Parameters

`name`
:   Identifier for the DMF to drop.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`TABLE( arg_data_type [ , ... ] ) [ , TABLE( arg_data_type [ , ... ] ) ]`
:   Specifies the data type of the column arguments for the DMF. The data types are necessary because DMFs support name overloading
    (that is, two DMFs in the same schema can have the same name), and the data types of the arguments are used to identify the DMF you want to
    drop.

## Access control requirements

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Data metric function |  |

Expand

Show lessSee more

## Usage notes

- When the IF EXISTS clause is specified and the target object doesn’t exist, the command completes successfully
  without returning an error.

## Example

Drop a custom DMF from the system:

Copy code

```
DROP FUNCTION governance.dmfs.count_positive_numbers(
  TABLE(
    NUMBER, NUMBER, NUMBER
  )
);
```
