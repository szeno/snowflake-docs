# SQL UDF limitations

This topic describes the limitations for handlers written in SQL.

## Argument and return type constraints are sometimes ignored

Certain type characteristics declared for an argument or return value will be ignored when the UDF is called. In these cases, the
received value may be used as received whether or not it conforms to constraints specified in the declaration.

The following are ignored for UDFs whose logic is written in SQL:

- Precision and scale for arguments and return values of type NUMBER
- Length for arguments and return values of type VARCHAR

### Example

Code in the following example declares that the `arg1` argument and the return value must be a VARCHAR no more than one character
long. However, calling this function with an `arg1` whose value is longer than one character will succeed as if the constraint were
not specified.

Copy code

```
CREATE OR REPLACE FUNCTION tf (arg1 VARCHAR(1))
RETURNS VARCHAR(1)
LANGUAGE SQL AS 'SHA2(a)';
```

## Dynamic SQL is not supported when referring to database objects

Referring to database objects using dynamic SQL will produce an error that includes text such as the following:

```
Compilation of SQL UDF failed: SQL compilation error: syntax error... unexpected '<variable_name>'
```

If you need to construct dynamic SQL statements that use different database objects, consider writing a stored procedure instead.
You can write stored procedures in one of the following languages:

- [Java](/developer-guide/stored-procedure/java/procedure-java-overview)
- [JavaScript](/developer-guide/stored-procedure/stored-procedures-javascript)
- [Python](/developer-guide/stored-procedure/python/procedure-python-overview)
- [Scala](/developer-guide/stored-procedure/scala/procedure-scala-overview)
- [Snowflake Scripting](/developer-guide/stored-procedure/stored-procedures-snowflake-scripting)

### Example

Code in the following example will fail because it uses the IDENTIFIER function to refer to a table whose name is dynamically specified
with the `table_name_parameter` variable.

Copy code

```
CREATE OR REPLACE FUNCTION profit2(table_name_parameter VARCHAR)
  RETURNS NUMERIC(11, 2)
  AS
  $$
    SELECT SUM((retail_price - wholesale_price) * number_sold)
        FROM IDENTIFIER(table_name_parameter)
  $$
  ;
```
