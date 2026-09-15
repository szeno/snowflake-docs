# IBM DB2 - CREATE TABLE

## Description

> The complete CREATE TABLE [syntax](https://www.ibm.com/docs/en/db2/11.5?topic=statements-create-table) for IBM DB2 is big enough that it does not fit on one page. However, the following image shows an overview of the syntax with some logical grouping that is later referenced.

## Grammar Syntax

[![image](/static/images/migrations/sc-assets/create_table_overview.png "image")](/static/images/migrations/sc-assets/create_table_overview.png)

## As Result Table

### Description

> Specifies that the columns of the new table have the same name, data type, and optionally same data, as the result from the fullselect.

Warning

AS RESULT TABLE is partially supported in Snowflake. The Copy options do not apply in Snowflake.

Click [here](https://www.ibm.com/docs/en/db2/11.5?topic=statements-create-table#sdx-synid_frag-as-result-table) to navigate to the IBM DB2 documentation page for this syntax.

### Grammar Syntax

[![image](/static/images/migrations/sc-assets/result_table_syntax_1.png "image")](/static/images/migrations/sc-assets/result_table_syntax_1.png)

[![image](/static/images/migrations/sc-assets/result_table_syntax_2.png "image")](/static/images/migrations/sc-assets/result_table_syntax_2.png)

[![image](/static/images/migrations/sc-assets/result_table_syntax_3.png "image")](/static/images/migrations/sc-assets/result_table_syntax_3.png)

### Sample Source Patterns

#### IBM DB2

Copy code

```
CREATE TABLE TestTable1
AS (SELECT * FROM OriginalTable) WITH NO DATA;
```

#### Snowflake

Copy code

```
CREATE TABLE TestTable1
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}'
AS (SELECT * FROM
  OriginalTable
 LIMIT 0
);
```

##### IBM DB2

Copy code

```
 CREATE TABLE TestTable2
AS (SELECT * FROM OriginalTable) WITH DATA
INCLUDING COLUMN DEFAULTS
INCLUDING IDENTITY;
```

##### Snowflake

Copy code

```
CREATE TABLE TestTable2
 COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}'
AS (SELECT * FROM
  OriginalTable
 );
```

## Materialized Query Definition

### Description

> Materialized query tables (MQTs) are tables whose definition is based on the result of a query.

Warning

Currently, translation for the IBM DB2 Materialized Query is not supported

See the [DB2 materialized query definition documentation](https://www.ibm.com/docs/en/db2/11.5?topic=statements-create-table#sdx-synid_materialized-query-definition) for this syntax.

### Grammar Syntax

[![image](/static/images/migrations/sc-assets/materialized_query_syntax_1.png "image")](/static/images/migrations/sc-assets/materialized_query_syntax_1.png)

[![image](/static/images/migrations/sc-assets/materialized_query_syntax_2.png "image")](/static/images/migrations/sc-assets/materialized_query_syntax_2.png)

### Sample Source Patterns

#### IBM DB2

Copy code

```
 CREATE TABLE TestTable4 (ACCTID, LOCID, YEAR, CNT) AS
  (SELECT ACCOUNTID, LOCATIONID, YEAR, COUNT(*)
     FROM TRANS
     GROUP BY ACCOUNTID, LOCATIONID, YEAR )
     DATA INITIALLY DEFERRED
     REFRESH DEFERRED
     MAINTAINED BY SYSTEM
     ENABLE QUERY OPTIMIZATION;
```

#### Snowflake

Copy code

```
  CREATE TABLE TestTable4 (ACCTID, LOCID, YEAR, CNT) AS
(SELECT ACCOUNTID, LOCATIONID, YEAR,
  COUNT(*)
FROM
  TRANS
GROUP BY ACCOUNTID, LOCATIONID, YEAR )
 !!!RESOLVE EWI!!! /*** SSC-EWI-DB0021 - MATERIALIZED QUERY IS NOT SUPPORTED ***/!!!
DATA INITIALLY DEFERRED
REFRESH DEFERRED
MAINTAINED BY SYSTEM
ENABLE QUERY OPTIMIZATION
 COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}';
```

### Related EWIs

1. [SSC-EWI-DB0021](../../issues-and-troubleshooting/conversion-issues/db2EWI): NODE NOT SUPPORTED

## Of Type

### Description

> Specifies that the columns of the table are based on the attributes of the structured type.

Click [here](https://www.ibm.com/docs/en/db2/11.5?topic=statements-create-table#sdx-synid_of) to navigate to the IBM DB2 documentation page for this syntax.

Warning

TYPED TABLES are not supported in Snowflake.

### Grammar Syntax

[![image](/static/images/migrations/sc-assets/typed_tables_syntax_1.png "image")](/static/images/migrations/sc-assets/typed_tables_syntax_1.png)

[![image](/static/images/migrations/sc-assets/typed_tables_syntax_2.png "image")](/static/images/migrations/sc-assets/typed_tables_syntax_2.png)

### Sample Source Patterns

#### IBM DB2

Copy code

```
    CREATE TABLE TestTable5 OF Student_t UNDER Person
   INHERIT SELECT PRIVILEGES;
```

#### Snowflake

Copy code

```
 !!!RESOLVE EWI!!! /*** SSC-EWI-DB0017 - TYPED TABLES ARE NOT SUPPORTED ***/!!!

CREATE TABLE TestTable5 OF Student_t UNDER Person
   INHERIT SELECT PRIVILEGES;
```

### Related EWIs

1. [SSC-EWI-DB0017](../../issues-and-troubleshooting/conversion-issues/db2EWI): NODE NOT SUPPORTED

## Staging Table Definition

### Description

> A *staging table* allows incremental maintenance support for deferred materialized query table.

Warning

STAGING TABLES are not supported in Snowflake.

See the [DB2 staging data tables](https://www.ibm.com/docs/en/db2/11.5?topic=tables-creating-staging-data) or the [staging table definition syntax](https://www.ibm.com/docs/en/db2/11.5?topic=statements-create-table#sdx-synid_staging-table-definition) in the IBM DB2 documentation.

### Grammar Syntax

[![image](/static/images/migrations/sc-assets/staging_table_syntax.png "image")](/static/images/migrations/sc-assets/staging_table_syntax.png)

### Sample Source Patterns

#### IBM DB2

Copy code

```
create table TestTable6 for emp_summary propagate immediate;
```

#### Snowflake

Copy code

```
 !!!RESOLVE EWI!!! /*** SSC-EWI-DB0018 - STAGING TABLES ARE NOT SUPPORTED ***/!!!
create table TestTable6 for emp_summary propagate immediate;
```

### Related EWIs

1. [SSC-EWI-DB0018](../../issues-and-troubleshooting/conversion-issues/db2EWI): NODE NOT SUPPORTED

## Element List

## Check Constraint

### Description

> Constraints are used to specify rules for the data in a table.

See the [DB2 column options documentation](https://www.ibm.com/docs/en/db2/11.5?topic=statements-create-table#sdx-synid_frag-column-options) for this syntax.

Warning

This syntax is supported in Snowflake for deterministic scalar expressions. CHECK constraints with user-defined functions or non-deterministic functions are not supported and will be flagged with SSC-EWI-0116.

### Grammar Syntax

[![image](/static/images/migrations/sc-assets/check_constraint_syntax_1.png "image")](/static/images/migrations/sc-assets/check_constraint_syntax_1.png)

[![image](/static/images/migrations/sc-assets/check_constraint_syntax_2.png "image")](/static/images/migrations/sc-assets/check_constraint_syntax_2.png)

### Sample Source Patterns

#### Example 1: Valid CHECK Constraints (Pass-through)

##### IBM DB2

Copy code

```
CREATE TABLE employees(
    emp_id INT,
    age INT CHECK(age >= 18),
    salary DECIMAL(10,2),
    CONSTRAINT chk_salary CHECK(salary > 0)
);
```

##### Snowflake

Copy code

```
CREATE OR REPLACE TABLE employees (
    emp_id INT,
    age INT CHECK(age >= 18),
    salary DECIMAL(10, 2),
    CONSTRAINT chk_salary CHECK(salary > 0)
)
;
```

#### Example 2: CHECK Constraint with User-Defined Function

##### IBM DB2

Copy code

```
CREATE TABLE orders(
    order_id INT,
    total DECIMAL(10,2),
    CONSTRAINT chk_total CHECK(validate_order(total) = 1)
);
```

##### Snowflake

Copy code

```
CREATE OR REPLACE TABLE orders (
    order_id INT,
    total DECIMAL(10, 2),
    CONSTRAINT chk_total
                         !!!RESOLVE EWI!!! /*** SSC-EWI-0116 - CHECK CONSTRAINT WITH user-defined function IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
                         CHECK(validate_order(total) = 1)
)
;
```

### Related EWIs

1. [SSC-EWI-0116](../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0116): CHECK constraint with unsupported expression.

## Period Definition

### Description

Defines a period of time in which the data of a row is valid.

Warning

PERIOD-DEFINITION does not have a functional equivalent in Snowflake.

Note

Snowflake allows the storage of historical table data for up to 90 days, to know more about this see [Understanding & Using Time Travel](https://docs.snowflake.com/en/user-guide/data-time-travel.html).

Click [here](https://www.ibm.com/docs/en/db2/11.5?topic=statements-create-table#sdx-synid_period-definition) to navigate to the IBM DB2 documentation page for this syntax.

### Grammar Syntax

[![image](/static/images/migrations/sc-assets/period_definition_syntax.png "image")](/static/images/migrations/sc-assets/period_definition_syntax.png)

### Sample Source Patterns

Copy code

```
CREATE TABLE TestTable8(
COL1 DATE,
COL2 DATE,
PERIOD SYSTEM_TIME (COL1, COL2));
)
```

Copy code

```
CREATE TABLE TestTable8 (
COL1 DATE,
    COL2 DATE,
    !!!RESOLVE EWI!!! /*** SSC-EWI-DB0003 - PERIOD SPECIFICATION IS NOT SUPPORTED IN SNOWFLAKE. ***/!!!
    PERIOD SYSTEM_TIME (COL1, COL2))
 COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}';
 CREATE OR REPLACE TABLE TestTable9 (
    COL1 VARCHAR(1)
 )
 COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}'
 ;
```

### Related EWIs

1. [SSC-EWI-DB0003](../../issues-and-troubleshooting/conversion-issues/db2EWI#ssc-ewi-db0003): Period definition is not applicable in Snowflake.

## Referential Constraint

### Description

> Foreign Key Constraints are migrated through ALTER TABLE statements to remove dependencies at the table creation time and therefore facilitate database deployment.

See the [DB2 column options documentation](https://www.ibm.com/docs/en/db2/11.5?topic=statements-create-table#sdx-synid_frag-column-options) for this syntax.

### Grammar Syntax

[![image](/static/images/migrations/sc-assets/referential_constraint_syntax_1.png "image")](/static/images/migrations/sc-assets/referential_constraint_syntax_1.png)

[![image](/static/images/migrations/sc-assets/referential_constraint_syntax_2.png "image")](/static/images/migrations/sc-assets/referential_constraint_syntax_2.png)

### Sample Source Patterns

Copy code

```
CREATE TABLE TestTable9(
    COL1 VARCHAR(1),
    CONSTRAINT FKCOL1 FOREIGN KEY (COL1) REFERENCES T1,
    CONSTRAINT FKCOL2 FOREIGN KEY (COL1) REFERENCES T1(COL1),
    CONSTRAINT FKCOL3 FOREIGN KEY (COL1) REFERENCES T1(COL1) ON DELETE CASCADE ON UPDATE NO ACTION,
    CONSTRAINT FKCOL4 FOREIGN KEY (COL1) REFERENCES T1(COL1) ENFORCED DISABLE QUERY OPTIMIZATION,
    FOREIGN KEY (COL1) REFERENCES T1
);
```

Copy code

```
 CREATE OR REPLACE TABLE TestTable9 (
    COL1 VARCHAR(1)
 )
 COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}'
 ;
 
 ALTER TABLE TestTable9
 ADD
    CONSTRAINT FKCOL1 FOREIGN KEY (COL1) REFERENCES T1 ;
 
 ALTER TABLE TestTable9
 ADD
    CONSTRAINT FKCOL2 FOREIGN KEY (COL1) REFERENCES T1 (COL1) ;
 
 ALTER TABLE TestTable9
 ADD
    CONSTRAINT FKCOL3 FOREIGN KEY (COL1) REFERENCES T1 (COL1) ON DELETE CASCADE ON UPDATE NO ACTION;
 
 ALTER TABLE TestTable9
 ADD
    CONSTRAINT FKCOL4 FOREIGN KEY (COL1) REFERENCES T1 (COL1) ENFORCED;
 
 ALTER TABLE TestTable9
 ADD CONSTRAINT TestTable9_COL1_T1
    FOREIGN KEY (COL1) REFERENCES T1 ;
```

## QUERY OPTIMIZATION

### Description

> Specifies whether the constraint or functional dependency can be used for query optimization under appropriate circumstances.

See the [DB2 WITHOUT OVERLAPS documentation](https://www.ibm.com/docs/en/db2/11.5?topic=statements-create-table#sdx-synid_without_overlaps) for this syntax.

Warning

ENABLE QUERY OPTIMIZATION Constraint attributes are removed because they are not applicable in Snowflake.

### Grammar Syntax

[![image](/static/images/migrations/sc-assets/query_optimization_syntax.png "image")](/static/images/migrations/sc-assets/query_optimization_syntax.png)

### Sample Source Patterns

#### IBM DB2

Copy code

```
CREATE TABLE TestTable11
(
COL1 VARCHAR(10),
COL2 VARCHAR(10),
CONSTRAINT ConstraintName UNIQUE (COL1, COL2) ENABLE QUERY OPTIMIZATION
);
```

#### Snowflake

Copy code

```
CREATE TABLE TestTable11
(
COL1 VARCHAR(10),
    COL2 VARCHAR(10),
    CONSTRAINT ConstraintName UNIQUE (COL1, COL2)
    )
 COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}';
```

## WITHOUT OVERLAPS

### Description

> BUSINESS\_TIME WITHOUT OVERLAPS means that for the other specified keys, the values are unique with respect to time for the BUSINESS\_TIME period

See the [DB2 column options documentation](https://www.ibm.com/docs/en/db2/11.5?topic=statements-create-table#sdx-synid_frag-column-options) for this syntax.

Warning

BUSINESS\_TIME WITHOUT OVERLAPS Constraint attribute is removed because they are not applicable in Snowflake.

### Grammar Syntax

[![image](/static/images/migrations/sc-assets/without_overlaps_syntax.png "image")](/static/images/migrations/sc-assets/without_overlaps_syntax.png)

### Sample Source Patterns

#### IBM DB2

Copy code

```
 CREATE TABLE TestTable12
(
COL1 VARCHAR(10),
CONSTRAINT ConstraintName UNIQUE (COL1, COL2, BUSINESS_TIME WITHOUT OVERLAPS)
);
```

#### Snowflake

Copy code

```
 CREATE TABLE TestTable12
(
COL1 VARCHAR(10),
    CONSTRAINT ConstraintName UNIQUE (COL1, COL2)
    )
 COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}';
```

## Column Options

## COMPRESS

### Description

> Specifies that system default values are to be stored using minimal space.

Click [here](https://www.ibm.com/docs/en/db2/11.5?topic=statements-create-table#sdx-synid_compress_system_default) to navigate to the IBM DB2 documentation page for this syntax.

Warning

COMPRESS SYSTEM DEFAULT is removed because it is not applicable in Snowflake

### Grammar Syntax

[![image](/static/images/migrations/sc-assets/compress_system_default_syntax.png "image")](/static/images/migrations/sc-assets/compress_system_default_syntax.png)

### Sample Source Patterns

#### IBM DB2

Copy code

```
 CREATE TABLE TestTable13
(
COL1 VARCHAR(10) COMPRESS SYSTEM DEFAULT
);
```

#### Snowflake

Copy code

```
 CREATE TABLE TestTable13
(
COL1 VARCHAR(10)
)
 COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}';
```

### Known issues

There are no known issues.

## HIDDEN

### Description

> Specifies whether the column is to be defined as hidden. The hidden attribute determines whether the column is included in an implicit reference to the table, or whether it can be explicitly referenced in SQL statements.

See the [DB2 NOT HIDDEN documentation](https://www.ibm.com/docs/en/db2/11.5?topic=statements-create-table#sdx-synid_not_hidden) for this syntax.

Warning

HIDDEN Option is removed because it is not applicable in Snowflake

### Grammar Syntax

[![image](/static/images/migrations/sc-assets/hidden_column_syntax.png "image")](/static/images/migrations/sc-assets/hidden_column_syntax.png)

### Sample Source Patterns

#### IBM DB2

Copy code

```
 CREATE TABLE TestTable14
(
COL1 VARCHAR(10) IMPLICITLY HIDDEN
);
```

#### Snowflake

Copy code

```
 CREATE TABLE TestTable14
(
COL1 VARCHAR(10)
)
 COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}';
```

## INLINE LENGTH

### Description

> Identifies the Inline Length of the reference type column.

See the [DB2 INLINE LENGTH documentation](https://www.ibm.com/docs/en/db2/11.5?topic=statements-create-table#sdx-synid_inline_length) for this syntax

Warning

INLINE LENGTH is removed because it is not applicable in Snowflake.

### Grammar Syntax

[![image](/static/images/migrations/sc-assets/inline_length_syntax.png "image")](/static/images/migrations/sc-assets/inline_length_syntax.png)

Copy code

```
CREATE TABLE T1
(
COL1 VARCHAR(10) INLINE LENGTH 1024
);
```

### Sample Source Patterns

#### IBM DB2

Copy code

```
 CREATE TABLE TestTable15
(
COL1 VARCHAR(10) INLINE LENGTH 1024
);
```

#### Snowflake

Copy code

```
 CREATE TABLE TestTable15
(
COL1 VARCHAR(10)
)
 COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}';
```

### Known issues

There are no known issues.

## LOB OPTIONS

### Description

> Options for the LOB (Large Object Binary) data types

Click [here](https://www.ibm.com/docs/en/db2/11.5?topic=statements-create-table#sdx-synid_frag-lob-options) to navigate to the IBM DB2 documentation page for this syntax.

Warning

LOB OPTIONS are removed because they are not applicable in Snowflake.

### Grammar Syntax

[![image](/static/images/migrations/sc-assets/lob_options_syntax.png "image")](/static/images/migrations/sc-assets/lob_options_syntax.png)

### Sample Source Patterns

#### IBM DB2

Copy code

```
 CREATE TABLE TestTable16
(
COL1 VARCHAR(10) LOGGED,
COL2 VARCHAR(10) NOT LOGGED,
COL3 VARCHAR(10) COMPACT,
COL4 VARCHAR(10) NOT COMPACT
)
```

#### Snowflake

Copy code

```
 CREATE TABLE TestTable16
(
COL1 VARCHAR(10),
    COL2 VARCHAR(10),
    COL3 VARCHAR(10),
    COL4 VARCHAR(10)
    )
 COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}';
```

## SCOPE

### Description

> Identifies the scope of the reference type column.

For this syntax, see the [IBM CREATE TABLE statement documentation](https://www.ibm.com/docs/en/db2/12.1.x?topic=statements-create-table).

Warning

SCOPE options are removed because they are not applicable in Snowflake.

### Grammar Syntax

[![image](/static/images/migrations/sc-assets/scope_syntax.png "image")](/static/images/migrations/sc-assets/scope_syntax.png)

### Sample Source Patterns

#### IBM DB2

Copy code

```
 CREATE TABLE TestTable17
(
COL1 VARCHAR(10) SCOPE TABLE2,
COL2 VARCHAR(10) SCOPE VIEW1
);
```

#### Snowflake

Copy code

```
 CREATE TABLE TestTable17
(
COL1 VARCHAR(10),
    COL2 VARCHAR(10)
    )
 COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}';
```

## SECURED

### Description

> Identifies a security label that exists for the security policy that is associated with the table.

See the [DB2 security label documentation](https://www.ibm.com/docs/en/db2/11.5?topic=statements-create-table#sdx-synid_security-label-name) for this syntax.

### Grammar Syntax

[![image](/static/images/migrations/sc-assets/security_label_syntax.png "image")](/static/images/migrations/sc-assets/security_label_syntax.png)

### Sample Source Patterns

#### IBM DB2

Copy code

```
CREATE TABLE TestTable18
(
COL1 VARCHAR(10) COLUMN SECURED WITH securityLabel,
COL2 VARCHAR(10) COLUMN SECURED WITH securityLabel
);
```

#### Snowflake

Copy code

```
 CREATE TABLE TestTable18
(
COL1 VARCHAR(10),
    COL2 VARCHAR(10)
    )
 WITH ROW ACCESS POLICY securityLabel ON (
    COL1,
    COL2
 )
 COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}';
```

### Known issues

If multiple security labels are declared an [SSC-EWI-DB0001](../../issues-and-troubleshooting/conversion-issues/db2EWI#ssc-ewi-db0001)will appear in the Snowflake output code as shown below

#### IBM DB2

Copy code

```
CREATE TABLE TestTable19
(
COL1 VARCHAR(10) COLUMN SECURED WITH securityLabel1,
COL2 VARCHAR(10) COLUMN SECURED WITH securityLabel2
);
```

#### Snowflake

Copy code

```
CREATE TABLE TestTable19
(
COL1 VARCHAR(10),
    COL2 VARCHAR(10)
    )
 WITH ROW ACCESS POLICY securityLabel1 ON (
    COL1
 )
 !!!RESOLVE EWI!!! /*** SSC-EWI-DB0001 - WITH ROW ACCESS POLICY CLAUSE DOES NOT SUPPORT MULTIPLE DECLARATION IN SNOWFLAKE ***/!!!
 WITH ROW ACCESS POLICY securityLabel2 ON (
    COL2
 )
 COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}';
```

#### Related EWIs

1. [SSC-EWI-DB0001](../../issues-and-troubleshooting/conversion-issues/db2EWI#ssc-ewi-db0001)Multiple Row Access policies

## Table Options

## CCSID

### Description

> Specifies the encoding scheme for string data that is stored in the table.

Click [here](https://www.ibm.com/docs/en/db2/11.5?topic=statements-create-table#sdx-synid_ccsid) to navigate to the IBM DB2 documentation page for this syntax.

Warning

CCSID is not applicable in Snowflake.

### Grammar Syntax

[![image](/static/images/migrations/sc-assets/ccsid_syntax.png "image")](/static/images/migrations/sc-assets/ccsid_syntax.png)

### Sample Source Patterns

#### IBM DB2

Copy code

```
CREATE TABLE TestTable20 (
COL1 INT
) CCSID ASCII;
```

#### Snowflake

Copy code

```
 CREATE TABLE TestTable20 (
COL1 INT
)
-- --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
-- CCSID ASCII
 COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}';
```

### Related EWIs

1. [SSC-FDM-0027](../../issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0027): REMOVED STATEMENT, NOT APPLICABLE IN SNOWFLAKE.

## Compression Options

### Description

> Specifies whether row compression is to be used for the table.

Click [here](https://www.ibm.com/docs/en/db2/11.5?topic=statements-create-table#sdx-synid_tablespace-name) to navigate to the IBM DB2 documentation page for this syntax.

Warning

The Compression Options are not applicable in Snowflake.

### Grammar Syntax

[![image](/static/images/migrations/sc-assets/compression_options_syntax.png "image")](/static/images/migrations/sc-assets/compression_options_syntax.png)

### Sample Source Patterns

#### IBM DB2

Copy code

```
CREATE TABLE TestTable21_01 (
COl1 INT,
COL2 INT
) 
COMPRESS YES
;

CREATE TABLE TestTable21_02 (
COl1 INT,
COL2 INT
) 
COMPRESS YES ADAPTIVE
;

CREATE TABLE TestTable21_03 (
COl1 INT,
COL2 INT
) 
COMPRESS YES STATIC
;

CREATE TABLE TestTable21_04 (
COl1 INT,
COL2 INT
) 
COMPRESS NO
;

CREATE TABLE TestTable21_05 (
COl1 INT,
COL2 INT
) 
VALUE COMPRESSION
;
```

#### Snowflake

Copy code

```
CREATE TABLE TestTable21_01 (
COl1 INT,
COL2 INT
)
----** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
--COMPRESS YES
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}'
;

CREATE TABLE TestTable21_02 (
COl1 INT,
COL2 INT
)
----** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
--COMPRESS YES ADAPTIVE
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}'
;

CREATE TABLE TestTable21_03 (
COl1 INT,
COL2 INT
)
----** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
--COMPRESS YES STATIC
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}'
;

CREATE TABLE TestTable21_04 (
COl1 INT,
COL2 INT
)
----** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
--COMPRESS NO
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}'
;

CREATE TABLE TestTable21_05 (
COl1 INT,
COL2 INT
)
----** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
--VALUE COMPRESSION
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}'
;
```

### Related EWIs

1. [SSC-FDM-0027](../../issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0027): REMOVED STATEMENT, NOT APPLICABLE IN SNOWFLAKE.

## Data Capture

### Description

> Indicates whether extra information for inter-database data replication is to be written to the log.

Click [here](https://www.ibm.com/docs/en/db2/11.5?topic=statements-create-table#sdx-synid_data_capture) to navigate to the IBM DB2 documentation page for this syntax.

Warning

DATA CAPTURE is not supported

### Grammar Syntax

[![image](/static/images/migrations/sc-assets/data_capture_syntax.png "image")](/static/images/migrations/sc-assets/data_capture_syntax.png)

### Sample Source Patterns

#### IBM DB2

Copy code

```
 CREATE TABLE TestTable22
(
	COL1 INT
) DATA CAPTURE CHANGES;
```

#### Snowflake

Copy code

```
 CREATE TABLE TestTable22
(
	COL1 INT
)
!!!RESOLVE EWI!!! /*** SSC-EWI-DB0020 - DATA CAPTURE IS NOT SUPPORTED ***/!!!
 DATA CAPTURE CHANGES
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}';
```

### Related EWIs

1. [SSC-EWI-DB0020](../../issues-and-troubleshooting/conversion-issues/db2EWI): NODE NOT SUPPORTED

## REMOVED CLAUSES

### Description

The following clauses are removed since they are not applicable in Snowflake:

- `Distribution` Clause
- `Not Logged Initially` Clause
- `Options` Clause
- `Organize by` Clause
- `Partition by` Clause
- `Security Policy` Clause
- `In` Clause
- `Long In` Clause
- `Index In` Clause
- `With Restrict On` Clause

### Sample Source Patterns

#### IBM DB2

Copy code

```
-- Distribution Clause
 CREATE TABLE TestTable23
(
	COL1 INT
) DISTRIBUTE BY REPLICATION;

-- Not Logged Initially Clause
 CREATE TABLE TestTable24 (
COL1 INT
) NOT LOGGED INITIALLY;

-- Options Clause
 CREATE TABLE TestTable25 (
COL1 INT
) OPTIONS(tableOptionName 'stringConst', tableOptionName2 'stringConst');

-- Organize By Clause
 CREATE TABLE TestTable26
(
	COL1 INT,
	COL2 INT,
	COL3 INT
) ORGANIZE BY ROW;

-- Partition By Clause
 CREATE TABLE TestTable27_01 (
COl1 INT,
COL2 INT
) 
PARTITION BY RANGE (COL1 NULLS LAST, COL2 NULLS FIRST) 
(PARTITION partitionName STARTING FROM (MINVALUE, MAXVALUE, 3) EXCLUSIVE ENDING AT MAXVALUE EXCLUSIVE IN tablespaceName INDEX IN tablespaceName LONG IN tablespaceName);

-- Partition By Clause
CREATE TABLE TestTable27_02 (
COl1 INT,
COL2 INT
) PARTITION BY (COL1 NULLS LAST) (STARTING MINVALUE INCLUSIVE ENDING 3 EXCLUSIVE IN tablespaceName);

-- Partition By Clause
CREATE TABLE TestTable27_03 (
COL1 INT,
COL2 INT
) PART BY (COL1) (STARTING 1 ENDING 3);

-- Partition By Clause
CREATE TABLE TestTable27_04 (
COL1 INT,
COL2 INT
) PART BY (COL1) (PARTITION 5 STARTING 1 ENDING 3);

-- Partition By Clause
CREATE TABLE TestTable27_05 (
COL1 INT,
COL2 INT
) PARTITION BY (COL1 NULLS LAST) 
(STARTING MINVALUE INCLUSIVE ENDING 3 EXCLUSIVE EVERY 3 YEAR);

-- Partition By Clause
CREATE TABLE TestTable27_06 (
COL1 INT,
COL2 INT
) 
PARTITION BY (COL1 NULLS LAST) 
(STARTING MINVALUE INCLUSIVE VALUES 3 EXCLUSIVE);

-- Partition By Clause
CREATE TABLE TestTable27_07 (
JYEARS INT
) 
PARTITION BY RANGE (SKACDY_DAY ASC) 
(
PARTITION 1 ENDING AT ('16.10.2019') HASH SPACE 2G, 
PARTITION 2 ENDING AT ('17.10.2019')
);

-- Partition By Clause
CREATE TABLE TestTable27_08 (
TRANS_DATE DATE NOT NULL
) 
PARTITION BY RANGE ("TRANS_DATE") 
(
PART "PART_2019_03_01" STARTING ('2019-03-01') ENDING ('2019-03-01') IN "SLTPAYMFACTD1903", 
PART "PART_2021_08_19" STARTING ('2021-08-19') ENDING ('2021-08-19') IN "SLTPAYMFACTD2108", 
PARTITION "PART_2021_08_19" STARTING ('2021-08-19') ENDING ('2021-08-19') IN "SLTPAYMFACTD2108"
);

-- Security Policy Clause
 CREATE TABLE TestTable28 (
COL1 INT
) SECURITY POLICY PolicyName;

-- In Clause
 CREATE TABLE TestTable29
(
	COL1 INT
) IN TablescapeName;

-- Long In Clause
 CREATE TABLE TestTable29
(
	COL1 INT
) LONG IN TablespaceName;

-- Index In Clause
 CREATE TABLE TestTable30
(
	COL1 INT
) INDEX IN TablespaceName;

-- With Restrict On Drop Clause
 CREATE TABLE TestTable31 (
COL1 INT
) WITH RESTRICT ON DROP;
```

#### Snowflake

Copy code

```
 -- Distribution Clause
 CREATE TABLE TestTable23
 (
	COL1 INT
)
-- --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
-- DISTRIBUTE BY REPLICATION
 COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}';

-- Not Logged Initially Clause
 CREATE TABLE TestTable24 (
COL1 INT
)
-- --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
-- NOT LOGGED INITIALLY
 COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}';

-- Options Clause
 CREATE TABLE TestTable25 (
COL1 INT
)
-- --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
-- OPTIONS(tableOptionName 'stringConst', tableOptionName2 'stringConst')
 COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}';

-- Organize By Clause
 CREATE TABLE TestTable26
 (
	COL1 INT,
COL2 INT,
COL3 INT
)
-- --** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
-- ORGANIZE BY ROW
 COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}';

-- Partition By Clause
 CREATE TABLE TestTable27_01 (
COl1 INT,
COL2 INT
)
----** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
--PARTITION BY RANGE (COL1 NULLS LAST, COL2 NULLS FIRST)
--(PARTITION partitionName STARTING FROM (MINVALUE, MAXVALUE, 3) EXCLUSIVE ENDING AT MAXVALUE EXCLUSIVE IN tablespaceName INDEX IN tablespaceName LONG IN tablespaceName)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}';

-- Partition By Clause
CREATE TABLE TestTable27_02 (
COl1 INT,
COL2 INT
)
----** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
--PARTITION BY (COL1 NULLS LAST) (STARTING MINVALUE INCLUSIVE ENDING 3 EXCLUSIVE IN tablespaceName)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}';

-- Partition By Clause
CREATE TABLE TestTable27_03 (
COL1 INT,
COL2 INT
)
----** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
--PART BY (COL1) (STARTING 1 ENDING 3)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}';

-- Partition By Clause
CREATE TABLE TestTable27_04 (
COL1 INT,
COL2 INT
)
----** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
--PART BY (COL1) (PARTITION 5 STARTING 1 ENDING 3)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}';

-- Partition By Clause
CREATE TABLE TestTable27_05 (
COL1 INT,
COL2 INT
)
----** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
--PARTITION BY (COL1 NULLS LAST)
--(STARTING MINVALUE INCLUSIVE ENDING 3 EXCLUSIVE EVERY 3 YEAR)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}';

-- Partition By Clause
CREATE TABLE TestTable27_06 (
COL1 INT,
COL2 INT
)
----** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
--PARTITION BY (COL1 NULLS LAST)
--(STARTING MINVALUE INCLUSIVE VALUES 3 EXCLUSIVE)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}';

-- Partition By Clause
CREATE TABLE TestTable27_07 (
JYEARS INT
)
----** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
--PARTITION BY RANGE (SKACDY_DAY ASC)
--(
--PARTITION 1 ENDING AT ('16.10.2019') HASH SPACE 2G,
--PARTITION 2 ENDING AT ('17.10.2019')
--)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}';

-- Partition By Clause
CREATE TABLE TestTable27_08 (
TRANS_DATE DATE NOT NULL
)
----** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
--PARTITION BY RANGE ("TRANS_DATE")
--(
--PART "PART_2019_03_01" STARTING ('2019-03-01') ENDING ('2019-03-01') IN "SLTPAYMFACTD1903",
--PART "PART_2021_08_19" STARTING ('2021-08-19') ENDING ('2021-08-19') IN "SLTPAYMFACTD2108",
--PARTITION "PART_2021_08_19" STARTING ('2021-08-19') ENDING ('2021-08-19') IN "SLTPAYMFACTD2108"
--)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}';

-- Security Policy Clause
 CREATE TABLE TestTable28 (
COL1 INT
)
----** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
--SECURITY POLICY PolicyName
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}';

-- In Clause
 CREATE TABLE TestTable29
(
	COL1 INT
)
----** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
--IN TablescapeName
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}';

-- Long In Clause
--** SSC-FDM-0019 - SEMANTIC INFORMATION COULD NOT BE LOADED FOR TestTable29. CHECK IF THE NAME IS INVALID OR DUPLICATED. **
 CREATE TABLE TestTable29
(
	COL1 INT
)
----** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
--LONG IN TablespaceName
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}';

-- Index In Clause
 CREATE TABLE TestTable30
(
	COL1 INT
)
----** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
--INDEX IN TablespaceName
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}';

-- With Restrict On Drop Clause
 CREATE TABLE TestTable31 (
COL1 INT
)
----** SSC-FDM-0027 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE.  **
--WITH RESTRICT ON DROP
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "db2",  "convertedOn": "09/01/2025",  "domain": "no-domain-provided" }}';
```

### Related EWIs

1. [SSC-FDM-0027](../../issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0027): REMOVED STATEMENT, NOT APPLICABLE IN SNOWFLAKE.
