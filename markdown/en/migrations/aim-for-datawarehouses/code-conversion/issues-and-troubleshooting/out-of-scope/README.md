# Code Conversion - Out-of-Scope

Examples of Out-of-scope code units if multiple SQL Languages

## Description

Certain code units cannot be automatically converted. Below are examples showing how these unsupported code units appear in the output folder.

### Teradata

#### Function with unsupported language:

Copy code

```
 CREATE FUNCTION CFEXTERNALINC (p1 INTEGER)
  RETURNS TABLE(
     c1 INTEGER
   )
   LANGUAGE java
   NO SQL
   PARAMETER STYLE SQL
     EXTERNAL NAME 'CS!fnc_tbf001udt.c'
```

#### Results from Snowflake:

Copy code

```
 ----** SSC-OOS - OUT OF SCOPE CODE UNIT. CREATE FUNCTION IS OUT OF TRANSLATION SCOPE. **
--CREATE FUNCTION CFEXTERNALINC (p1 INTEGER)
--  RETURNS TABLE(
--     c1 INTEGER
--   )
--   LANGUAGE java
--   NO SQL
--   PARAMETER STYLE SQL
--     EXTERNAL NAME 'CS!fnc_tbf001udt.c'
                                       ;
```

### Oracle Migration

#### Wrapped type definition:

Copy code

```
 CREATE TYPE data_typ1 wrapped
a000000
b2
6CodpsEHq3I=
```

#### Results from Snowflake:

Copy code

```
 ----** SSC-OOS - OUT OF SCOPE CODE UNIT. Wrapped TYPE IS OUT OF TRANSLATION SCOPE. **
--CREATE TYPE data_typ1 wrapped
--a000000
--b2
--6CodpsEHq3I=
```

### Transact-SQL (T-SQL)

#### Trigger:

Copy code

```
 CREATE TRIGGER reminder1
ON Sales.Customer
AFTER INSERT, UPDATE
AS RAISERROR ('Notify Customer Relations', 16, 10);
```

#### Results from Snowflake:

Copy code

```
 ----** SSC-OOS - OUT OF SCOPE CODE UNIT. CREATE TRIGGER IS OUT OF TRANSLATION SCOPE. **
--CREATE TRIGGER reminder1
--ON Sales.Customer
--AFTER INSERT, UPDATE
--AS RAISERROR ('Notify Customer Relations', 16, 10);
```

## Best Practices

- For additional support, please contact us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)
