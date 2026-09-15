# Oracle - Rowid Data Type

## Description

> Each row in the database has an address. ([Oracle SQL Language Reference Rowid Data Types](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/Data-Types.html#GUID-4231B94A-97E9-4B59-91EB-E7B2D0DA438C))

## ROWID DataType

### Description

> The rows in heap-organized tables that are native to Oracle Database have row addresses called rowids. You can examine a rowid row address by querying the pseudocolumn ROWID. Values of this pseudocolumn are strings representing the address of each row. These strings have the data type ROWID. You can also create tables and clusters that contain actual columns having the ROWID data type. ([Oracle SQL Language Reference ROWID Data Types](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/Data-Types.html#GUID-AEF1FE4C-2DE5-4BE7-BB53-83AD8F1E34EF))

Copy code

```
ROWID
```

### Sample Source Patterns

#### ROWID in Create Table

##### Oracle

Copy code

```
CREATE TABLE rowid_table
(
    rowid_column ROWID
);
```

##### Snowflake

Copy code

```
CREATE OR REPLACE TABLE rowid_table
    (
        rowid_column VARCHAR(18) !!!RESOLVE EWI!!! /*** SSC-EWI-0036 - ROWID DATA TYPE CONVERTED TO VARCHAR ***/!!!
    )
    COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
    ;
```

#### Insert data in the ROWID column

It is possible to insert data in ROWID columns if the insert has a valid ROWID, as shown in the example below. Unfortunately retrieving ROWID from a table is not allowed.

##### Oracle

Copy code

```
INSERT INTO rowid_table VALUES ('AAATtCAAMAAAADLABD');

SELECT rowid_column FROM rowid_table;
```

##### Result

| ROWID\_COLUMN |
| --- |
| AAATtCAAMAAAADLABD |

Expand

Show lessSee more

##### Snowflake

Copy code

```
INSERT INTO rowid_table
VALUES ('AAATtCAAMAAAADLABD');

SELECT rowid_column FROM
rowid_table;
```

##### Result

| ROWID\_COLUMN |
| --- |
| AAATtCAAMAAAADLABD |

Expand

Show lessSee more

### Known Issues

Note

Since the result set is too large, *Row Limiting Clause* was added. You can remove this clause to retrieve the entire result set.

**1. Retrieving ROWID from a table that does not have an explicit column with this data type**

As mentioned in the [Snowflake forum](https://community.snowflake.com/s/question/0D50Z00007jUWEU/how-to-convert-oracle-rowids-to-snowflake-sql), ROWID is not supported by Snowflake. The following query displays an error in Snowflake since hr.employees do not contain a ROWID column.

#### Oracle

Copy code

```
SELECT
    ROWID
FROM
    hr.employees
FETCH NEXT 10 ROWS ONLY;
```

##### Result

| ROWID |
| --- |
| AAATtCAAMAAAADLABD |
| AAATtCAAMAAAADLABV |
| AAATtCAAMAAAADLABX |
| AAATtCAAMAAAADLAAv |
| AAATtCAAMAAAADLAAV |
| AAATtCAAMAAAADLAAD |
| AAATtCAAMAAAADLABL |
| AAATtCAAMAAAADLAAP |
| AAATtCAAMAAAADLAA6 |
| AAATtCAAMAAAADLABg |

Expand

Show lessSee more

##### Snowflake

Copy code

```
SELECT
    --** SSC-FDM-OR0030 - ROWID PSEUDOCOLUMN IS NOT SUPPORTED IN SNOWFLAKE, IT WAS CONVERTED TO NULL TO AVOID RUNTIME ERRORS **
    '' AS ROWID
FROM
    hr.employees
FETCH NEXT 10 ROWS ONLY;
```

##### Result

Danger

SQL compilation error: invalid identifier ‘ROWID’

### Related EWIs

1. [SSC-EWI-0036](../../../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0036): Data type converted to another data type.
2. [SSC-FDM-OR0030](../../../../issues-and-troubleshooting/functional-difference/oracleFDM#ssc-fdm-or0030): ROWID pseudocolumn is not supported in Snowflake.

## UROWID Data Type

### Description

> Oracle uses universal rowids (urowids) to store the addresses of index-organized and foreign tables. Index-organized tables have logical urowids and foreign tables have foreign urowids.([Oracle SQL Language Reference UROWID Data Type](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/Data-Types.html#GUID-E9F3AE1C-AA6D-4262-A15F-778833251361))

Copy code

```
UROWID [(size)]
```

### Sample Source Patterns

#### UROWID in Create Table

##### Oracle

Copy code

```
CREATE TABLE urowid_table
(
    urowid_column UROWID,
    urowid_sized_column UROWID(40)
);
```

##### Snowflake

Copy code

```
CREATE OR REPLACE TABLE urowid_table
    (
        urowid_column VARCHAR(18) !!!RESOLVE EWI!!! /*** SSC-EWI-0036 - UROWID DATA TYPE CONVERTED TO VARCHAR ***/!!!,
        urowid_sized_column VARCHAR(18) !!!RESOLVE EWI!!! /*** SSC-EWI-0036 - UROWID DATA TYPE CONVERTED TO VARCHAR ***/!!!
    )
    COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
    ;
```

#### Insert data in the UROWID column

Just like [ROWID](#rowid-datatype), it is possible to insert data in UROWID columns if the insert has a valid UROWID, but retrieving from a table is not allowed.

##### Oracle

Copy code

```
INSERT INTO urowid_table VALUES ('*BAMAAJMCVUv+','*BAMAAJMCVUv+');

SELECT * FROM urowid_table;
```

##### Result

| UROWID\_COLUMN | UROWID\_SIZED\_COLUMN |
| --- | --- |
| \*BAMAAJMCVUv+ | \*BAMAAJMCVUv+ |

Expand

Show lessSee more

##### Snowflake\*\* SSC-FDM-0007 - MISSING DEPENDENT OBJECT “urowid\_table” \*\*

Copy code

```
INSERT INTO urowid_table
VALUES ('*BAMAAJMCVUv+','*BAMAAJMCVUv+');

SELECT * FROM
urowid_table;
```

##### Result

| UROWID\_COLUMN | UROWID\_SIZED\_COLUMN |
| --- | --- |
| \*BAMAAJMCVUv+ | \*BAMAAJMCVUv+ |

Expand

Show lessSee more

### Known Issues

Note

Since the result set is too large, *Row Limiting Clause* was added. You can remove this clause to retrieve the entire result set.

**1. Retrieving UROWID from a table that does not have an explicit column with this data type**

The following query displays an error in Snowflake since hr.countries do not contain a ROWID (as mentioned in [Oracle’s documentation](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/Data-Types.html#GUID-E9F3AE1C-AA6D-4262-A15F-778833251361) UROWID is accessed with `SELECT` … `ROWID` statement) column.

#### Oracle

Copy code

```
SELECT
    rowid,
    country_name
FROM
    hr.countries FETCH NEXT 10 ROWS ONLY;
```

##### Result

| ROWID | COUNTRY\_NAME |
| --- | --- |
| \*BAMAAJMCQVL+ | Argentina |
| \*BAMAAJMCQVX+ | Australia |
| \*BAMAAJMCQkX+ | Belgium |
| \*BAMAAJMCQlL+ | Brazil |
| \*BAMAAJMCQ0H+ | Canada |
| \*BAMAAJMCQ0j+ | Switzerland |
| \*BAMAAJMCQ07+ | China |
| \*BAMAAJMCREX+ | Germany |
| \*BAMAAJMCREv+ | Denmark |
| \*BAMAAJMCRUf+ | Egypt |

Expand

Show lessSee more

##### Snowflake

Copy code

```
SELECT
        --** SSC-FDM-OR0030 - ROWID PSEUDOCOLUMN IS NOT SUPPORTED IN SNOWFLAKE, IT WAS CONVERTED TO NULL TO AVOID RUNTIME ERRORS **
        '' AS rowid,
        country_name
FROM
        hr.countries
FETCH NEXT 10 ROWS ONLY;
```

##### Result

Danger

SQL compilation error: invalid identifier ‘ROWID’

##### 2. EWI should be displayed

EWI should be displayed when trying to select UROWID column. There is a work item to add the corresponding EWI.

Danger

This issue has been marked as critical and will be fixed in the upcoming releases.

### Related EWIs

1. [SSC-EWI-0036](../../../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0036): Data type converted to another data type.
2. [SSC-FDM-OR0030](../../../../issues-and-troubleshooting/functional-difference/oracleFDM#ssc-fdm-or0030): ROWID pseudocolumn is not supported in Snowflake.
