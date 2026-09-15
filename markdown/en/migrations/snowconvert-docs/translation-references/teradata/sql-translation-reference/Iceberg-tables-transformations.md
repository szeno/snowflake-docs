# Teradata - Iceberg Tables Transformations

This section covers the transformation of tables into Snowflake-managed Iceberg tables

## Temporary tables

The temporary option is not supported in Iceberg tables, they will be preserved as temporary.

### Teradata

Copy code

```
CREATE VOLATILE TABLE myTable
(
  column1 NUMBER(15,0)
);
```

### Snowflake

Copy code

```
CREATE OR REPLACE TEMPORARY TABLE myTable
(
 column1 NUMBER(15,0)
)
;
```

## Other tables

Other table types are going to be transformed into Iceberg tables.

### Teradata

Copy code

```
CREATE TABLE myTable
(
  column1 NUMBER(15,0)
);
```

### Snowflake

Copy code

```
CREATE OR REPLACE ICEBERG TABLE myTable (
  column1 NUMBER(15, 0)
)
CATALOG = 'SNOWFLAKE'
;
```

## Data types

The following column data type conversions are applied to comply with the Iceberg tables type requirements and restrictions.

Note

Data types in the first column are the **Snowflake** data types that would normally be created if the table target is not Iceberg, while second column shows the data type generated for Iceberg tables.

| Original target type | New target type |
| --- | --- |
| TIME(X)  TIMESTAMP(X)  DATETIME(X)  TIMESTAMP\_LTZ(X)  TIMESTAMP\_NTZ(X)  TIME  TIMESTAMP  DATETIME  TIMESTAMP\_LTZ  TIMESTAMP\_NTZ  where X != 6 | TIME(6)  TIMESTAMP(6)  DATETIME(6)  TIMESTAMP\_LTZ(6)  TIMESTAMP\_NTZ(6)  TIME(6)  TIMESTAMP(6)  DATETIME(6)  TIMESTAMP\_LTZ(6)  TIMESTAMP\_NTZ(6) |
| VARCHAR(X)  STRING(X)  TEXT(X)  NVARCHAR(X)  NVARCHAR2(X)  CHAR VARYING(X)  NCHAR VARYING(X) | VARCHAR  STRING  TEXT  NVARCHAR  NVARCHAR2  CHAR VARYING  NCHAR VARYING |
| CHAR[(n)]  CHARACTER[(n)]  NCHAR[(n)] | VARCHAR  VARCHAR  VARCHAR |
| NUMBER  DECIMAL  DEC  NUMERIC  INT  INTEGER  BIGINT  SMALLINT  TINYINT  BYTEINT | NUMBER(38,0)  DECIMAL(38,0)  DEC(38,0)  NUMERIC(38,0)  NUMBER(38,0)  NUMBER(38,0)  NUMBER(38,0)  NUMBER(38,0)  NUMBER(38,0)  NUMBER(38,0) |
| FLOAT  FLOAT4  FLOAT8 | DOUBLE  DOUBLE  DOUBLE |
| VARBINARY[(n)] | BINARY[(n)] |

Expand

Show lessSee more

## PARTITION BY

The following PARTITION BY cases are supported:

### PARTITION BY name

Left as is.

#### Teradata

Copy code

```
CREATE TABLE myTable
(
  customerName VARCHAR(30),
  areaCode INTEGER
)
PARTITION BY areaCode;
```

#### Snowflake

Copy code

```
CREATE OR REPLACE ICEBERG TABLE myTable (
  customerName VARCHAR,
  areaCode NUMBER(38, 0)
)
PARTITION BY (areaCode)
CATALOG = 'SNOWFLAKE'
;
```

### PARTITION BY CASE\_N (equality over single column)

When the CASE\_N function follows this pattern:

Copy code

```
PARTITION BY CASE_N(
  column_name = value1,
  column_name = value2,
  ...
  column_name = valueN)
```

It will be transformed to a PARTITION BY column\_name.

#### Teradata

Copy code

```
CREATE TABLE myTable
(
  customerName VARCHAR(30),
  weekDay VARCHAR(20)
)
PARTITION BY CASE_N(
weekDay =  'Sunday',
weekDay =  'Monday',
weekDay =  'Tuesday',
weekDay =  'Wednesday',
weekDay =  'Thursday',
weekDay =  'Friday',
weekDay =  'Saturday',
 NO CASE OR UNKNOWN);
```

#### Snowflake

Copy code

```
CREATE OR REPLACE ICEBERG TABLE myTable (
  customerName VARCHAR,
  weekDay VARCHAR
)
PARTITION BY (weekDay)
CATALOG = 'SNOWFLAKE'
;
```

### PARTITION BY RANGE\_N

PARTITION BY RANGE\_N is transformed when it matches one of these patterns:

#### Numeric range

Pattern:

Copy code

```
RANGE_N(columnName BETWEEN x AND y EACH z) -- x, y and z must be numeric constants.
```

This case will be changed with a BUCKET partition transform.

##### Teradata

Copy code

```
CREATE TABLE myTable
(
  customerName VARCHAR(30),
  totalPurchases INTEGER
)
PARTITION BY RANGE_N(totalPurchases BETWEEN 5 AND 200 EACH 10);
```

##### Snowflake

Copy code

```
CREATE OR REPLACE ICEBERG TABLE myTable (
  customerName VARCHAR,
  totalPurchases NUMBER(38, 0)
)
PARTITION BY (BUCKET(20, totalPurchases))
CATALOG = 'SNOWFLAKE'
;
```

#### Datetime range

Pattern:

Copy code

```
RANGE_N(columnName BETWEEN date_constant AND date_constant EACH interval_constant) -- Interval qualifier must be YEAR, MONTH, DAY or HOUR
```

This case will be changed with the YEAR, MONTH, DAY or HOUR partition transforms.

##### Teradata

Copy code

```
CREATE TABLE myTable
(
  customerName VARCHAR(30),
  purchaseDate DATE
)
PARTITION BY RANGE_N(purchaseDate BETWEEN DATE '2000-01-01' AND '2100-12-31' EACH INTERVAL '1' MONTH);
```

##### Snowflake

Copy code

```
CREATE OR REPLACE ICEBERG TABLE myTable (
  customerName VARCHAR,
  purchaseDate DATE
)
PARTITION BY (MONTH(purchaseDate))
CATALOG = 'SNOWFLAKE'
;
```

## CASESPECIFIC and NOT CASESPECIFIC

Case sensitivity can be handled in Snowflake using the COLLATE column option, however, Iceberg Tables currently do not support collation at the column level.

To handle this difference, use of COLLATE for Case Specification will be disabled for all transformations that specify Iceberg Tables as target. This will cause the case sensitive comparisons to be emulated at query level with the UPPER function, preserving the case sensitivity functionality for Iceberg.

### Teradata

Copy code

```
CREATE TABLE my_table
(
    col1 VARCHAR(50) NOT CASESPECIFIC
);

SELECT * FROM my_table WHERE col1 = 'test';
```

### Snowflake

Copy code

```
--** SSC-FDM-TD0039 - COLLATION HANDLED AT QUERY LEVEL FOR THIS TABLE, ANY NEW QUERY OVER THIS TABLE SHOULD APPLY COLLATION APPROPRIATELY **
CREATE OR REPLACE ICEBERG TABLE my_table
(
    col1 VARCHAR
)
CATALOG = 'SNOWFLAKE'
;

SELECT
    * FROM
    my_table
WHERE
    UPPER(RTRIM( col1)) = UPPER(RTRIM('test'));
```

## Known Issues

### 1. Unsupported data types

Current Snowflake support for Iceberg tables does not allow data types like VARIANT or GEOGRAPHY to be used, tables with these types will be marked with an EWI.

### 2. Unsupported PARTITION BY cases

PARTITION BY cases different than the ones shown in this documentation will not be transformed, instead, the PARTITION BY clause will be commented out with a PRF.

## Related EWIs

1. [SSC-EWI-0115](../../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0115): Iceberg table contains unsupported datatypes
2. [SSC-PRF-0010](../../../issues-and-troubleshooting/performance-review/generalPRF#ssc-prf-0010): Partition by removed, at least one of the specified expressions have no iceberg partition transform equivalent
3. [SSC-FDM-TD0039](../../../issues-and-troubleshooting/functional-difference/teradataFDM#ssc-fdm-td0039): Collation handled at query level for this table, any new query over this table should apply collation appropriately
