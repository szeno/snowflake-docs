# SnowConvert AI - Databases & Schemas

Note

This page of the documentation is for Teradata only.

[![The Databases and Schemas section of the assessment report for Teradata](/static/images/migrations/sc-assets/Screenshot2023-11-02at9.53.15PM.png)](/static/images/migrations/sc-assets/Screenshot2023-11-02at9.53.15PM.png)

## Number of Databases Containing Objects

Represents the number of databases that contain identified top-level objects. Each different database name will only count as one single database.

It is important to consider that this number will only be incremented by the names used in the top-level objects, the references to the object names will not be counted in this assessment value.

Note

The SQL and script files affect this field.

### Sample

Copy code

```
CREATE TABLE database1.table1(COL1 INTEGER);
CREATE TABLE DATABASE1.table1(COL1 INTEGER);

CREATE VIEW "database2"."view2" AS SELECT * FROM table2;
CREATE VIEW "DATABASE2"."view2" AS SELECT * FROM table2;

CREATE VIEW view3 AS SELECT * FROM database3.table3;
```

```
CREATE OR REPLACE TABLE database1.table1 (
COL1 INTEGER)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;

--** SSC-FDM-0019 - SEMANTIC INFORMATION COULD NOT BE LOADED FOR DATABASE1.table1. CHECK IF THE NAME IS INVALID OR DUPLICATED. **
CREATE OR REPLACE TABLE DATABASE1.table1 (
COL1 INTEGER)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;

--** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "table2" **
CREATE OR REPLACE VIEW "database2"."view2"
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
AS
--** SSC-FDM-0001 - VIEWS SELECTING ALL COLUMNS FROM A SINGLE TABLE ARE NOT REQUIRED IN SNOWFLAKE AND MAY IMPACT PERFORMANCE. **
SELECT
* FROM
table2;

--** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "table2" **
--** SSC-FDM-0019 - SEMANTIC INFORMATION COULD NOT BE LOADED FOR "DATABASE2"."view2". CHECK IF THE NAME IS INVALID OR DUPLICATED. **
CREATE OR REPLACE VIEW "DATABASE2"."view2"
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
AS
--** SSC-FDM-0001 - VIEWS SELECTING ALL COLUMNS FROM A SINGLE TABLE ARE NOT REQUIRED IN SNOWFLAKE AND MAY IMPACT PERFORMANCE. **
SELECT
* FROM
table2;

--** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "database3.table3" **
CREATE OR REPLACE VIEW view3
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
AS
--** SSC-FDM-0001 - VIEWS SELECTING ALL COLUMNS FROM A SINGLE TABLE ARE NOT REQUIRED IN SNOWFLAKE AND MAY IMPACT PERFORMANCE. **
SELECT
* FROM
database3.table3;
```

**Expected Databases containing objects:** 4

**Explanation:** Only the databases used in the name of a DDL (tables, views, macros, join indexes, procedures, and functions) will count as a database object. In this case, **database1** and **DATABASE1** in CREATE TABLE statements and **“database2”** and **“DATABASE2”** in CREATE VIEW statements will be counted.
