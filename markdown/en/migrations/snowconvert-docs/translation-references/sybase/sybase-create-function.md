# Sybase IQ - CREATE FUNCTION

## Description

Creates a user-defined function (UDF) that returns a scalar value.
Sybase IQ UDFs are translated to Snowflake UDFs, mapping parameters and data types to Snowflake equivalents.

Note

Sybase IQ supports Transact-SQL as language. For Transact-SQL to Snowflake guidance, see the SQL Server/Azure Synapse translation reference: [Built-in Functions](../transact/transact-built-in-functions).
This section documents statement translation specific to Sybase IQ.

## Grammar Syntax

Copy code

```
CREATE FUNCTION [ <owner>. ]<function-name>
   ( <parameter-name> <data-type> [ , ... ] )
RETURNS <return-data-type>
BEGIN
   <function-body>
   RETURN <expression>;
END
```

## Sample Source Patterns

### Input Code:

#### Sybase

Copy code

```
CREATE FUNCTION dbo.fn_tax(p_amount DECIMAL(10,2))
RETURNS DECIMAL(10,2)
BEGIN
    RETURN p_amount * 0.16;
END
```

### Output Code:

#### Snowflake

Copy code

```
CREATE OR REPLACE FUNCTION dbo.fn_tax (p_amount DECIMAL(10, 2))
RETURNS DECIMAL(10, 2)
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "sybase",  "convertedOn": "02/02/2026",  "domain": "no-domain-provided",  "migrationid": "GSCcAR8gMXmhqgt7dMJukg==" }}'
AS
$$
  BEGIN
    RETURN p_amount * 0.16;
  END;
$$;
;
```

## Notes

- Parameter and return data types are translated to their Snowflake equivalents.
- For procedural logic that cannot be expressed as a SQL UDF, a JavaScript UDF may be used or a stored procedure recommended.
