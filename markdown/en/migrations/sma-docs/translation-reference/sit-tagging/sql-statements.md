# Snowpark Migration Accelerator: SQL statements

## Tagged elements

SQL statements are tagged to monitor usage and consumption.

| Statements | HiveSQL | SparkSQL | SnowSQL |
| --- | --- | --- | --- |
| **CREATE TABLE** | SUPPORTED | SUPPORTED | FUNCTIONAL EQUIVALENT |
| **CREATE VIEW** | SUPPORTED | SUPPORTED | FUNCTIONAL EQUIVALENT |
| **CREATE FUNCTION** | NOT SUPPORTED | SUPPORTED | FUNCTIONAL EQUIVALENT |
| **ALTER TABLE** | SUPPORTED | SUPPORTED | FUNCTIONAL EQUIVALENT |
| **ALTER VIEW** | SUPPORTED | SUPPORTED | FUNCTIONAL EQUIVALENT |

Expand

Show lessSee more

Note

When a comment is marked as “FUNCTIONAL EQUIVALENT,” it means that only the comment’s transformation to Snowflake has been validated. Any other statements within the comment are not included in this status assessment.

### Usages

The tool identifies and tags the following statements:

#### CREATE STATEMENTS

CREATE statements will include tags in two scenarios:

1. The SQL statement is missing the COMMENT property.
2. The SQL statement includes a `COMMENT` property, but no value has been assigned to it.

If a SQL statement includes a comment, the comment will be preserved during the conversion process.

##### Example

**Input (Apache SparkSQL)**

Copy code

```
CREATE OR REPLACE VIEW some_view
AS
SELECT id, name FROM some_table WHERE some_column > 5;

CREATE OR REPLACE FUNCTION blue()
RETURNS STRING
LANGUAGE SQL
COMMENT ''
RETURN '0000FF';

CREATE TABLE my_varchar (
    COL1 VARCHAR(5)
) COMMENT 'The Table';
```

**Output (Snowflake SQL)**

Copy code

```
CREATE OR REPLACE VIEW some_view
COMMENT = '{"origin":"sf_sit","name":"sma","version":{"major":1,"minor":2,"patch":3},"attributes":{"language":"HiveSql"}}'
AS
SELECT
   id,
   name
FROM
   some_table
WHERE
   some_column > 5;

CREATE OR REPLACE FUNCTION blue()
RETURNS STRING LANGUAGE SQL
COMMENT = '{"origin":"sf_sit","name":"sma","version":{"major":0,"minor":0,"patch":0},"attributes":{"language":"SparkSql"}}'
RETURN '0000FF';

CREATE TABLE my_varchar
(COL1 VARCHAR(5))
COMMENT = 'The Table';
```

The formatting of the generated code may appear different from the source code due to formatting differences in the original file.

---

##### Create Table

**Input code (SparkSQL)**

Copy code

```
CREATE TABLE SOME_TABLE
(COL1 VARCHAR(5));
```

**Output code (Snowflake SQL)**

Copy code

```
CREATE TABLE SOME_TABLEA
(COL1 VARCHAR(5))
COMMENT = '{"origin":"sf_sit","name":"sma","version":{"major":0,"minor":0,"patch":0},"attributes":{"language":"SparkSql"}}';
```

---

##### CREATE VIEW

**Source Code (HiveSQL)**

Copy code

```
CREATE OR REPLACE VIEW experienced_employee
AS
SELECT id, name FROM all_employee
WHERE working_years > 5;
```

**Output code (Snowflake SQL)**

Copy code

```
CREATE OR REPLACE VIEW experienced_employee
COMMENT = '{"origin":"sf_sit","name":"sma","version":{"major":1,"minor":2,"patch":3},"attributes":{"language":"HiveSql"}}'
AS
SELECT
   id,
   name
FROM
   all_employee
WHERE
   working_years > 5;
```

---

##### CREATE FUNCTION

**Input code (SparkSQL)**

Copy code

```
CREATE OR REPLACE FUNCTION blue()
RETURNS STRING
LANGUAGE SQL RETURN '0000FF';
```

**Output (Snowflake SQL)**

Copy code

```
CREATE OR REPLACE FUNCTION blue()
RETURNS STRING
LANGUAGE SQL
COMMENT = '{"origin":"sf_sit","name":"sma","version":{"major":0,"minor":0,"patch":0},"attributes":{"language":"SparkSql"}}'
RETURN '0000FF';
```

#### ALTER STATEMENTS

ALTER statements include a tag when the comment property is empty. This occurs in two scenarios in SparkSQL:

1. When using `SET TBLPROPERTIES` with an empty comment
2. When using `UNSET TBLPROPERTIES`

##### Examples

**SET TBLPROPERTIES (ALTER VIEW and ALTER TABLE)**

**Input (Apache Spark SQL)**

Copy code

```
ALTER TABLE SOME_TABLE SET TBLPROPERTIES ('comment'= ' ');
-- ALTER VIEW
ALTER VIEW SOME_VIEW SET TBLPROPERTIES ('comment'= ' ');
```

**Output (Snowflake SQL)**

Copy code

```
-- ALTER TABLE
ALTER TABLE SOME_TABLE
SET TBLPROPERTIES ('comment' = '{"origin":"sf_sit","name":"sma","version":{"major":0,"minor":0,"patch":0},"attributes":{"language":"SparkSql"}}');

-- ALTER VIEW
ALTER VIEW SOME_VIEW
SET TBLPROPERTIES ('comment' = '{"origin":"sf_sit","name":"sma","version":{"major":0,"minor":0,"patch":0},"attributes":{"language":"SparkSql"}}');

**Input (Apache HiveSQL)**

```{code} sql
:force:
-- ALTER TABLE
ALTER TABLE SOME_TABLE SET TBLPROPERTIES ('comment'= ' ');

-- ALTER VIEW
ALTER VIEW SOME_VIEW SET TBLPROPERTIES ('comment'= ' ');
```

**Output (Snowflake SQL)**

Copy code

```
-- ALTER TABLE
ALTER TABLE SOME_TABLE
SET TBLPROPERTIES ('comment' = '{"origin":"sf_sit","name":"sma","version":{"major":0,"minor":0,"patch":0},"attributes":{"language":"HiveSql"}}');

-- ALTER VIEW
ALTER VIEW SOME_VIEW
SET TBLPROPERTIES ('comment' = '{"origin":"sf_sit","name":"sma","version":{"major":0,"minor":0,"patch":0},"attributes":{"language":"HiveSql"}}');
```

**UNSET TBLPROPERTIES (ALTER VIEW and ALTER TABLE)**

**Input (Apache Spark SQL)**

Copy code

```
-- ALTER TABLE
ALTER TABLE SOME_TABLE UNSET TBLPROPERTIES ('comment');

-- ALTER VIEW
ALTER VIEW SOME_VIEW UNSET TBLPROPERTIES ('comment');

**Output (Snowflake SQL)**

```{code} sql
:force:
-- ALTER TABLE
ALTER TABLE SOME_TABLE
UNSET TBLPROPERTIES ('comment')
ALTER TABLE SOME_TABLE
SET COMMENT = '{"origin":"sf_sit","name":"sma","version":{"major":0,"minor":0,"patch":0},"attributes":{"language":"SparkSql"}}'

-- ALTER VIEW
ALTER VIEW SOME_VIEW
UNSET TBLPROPERTIES ('comment')
ALTER VIEW SOME_VIEW
SET COMMENT = '{"origin":"sf_sit","name":"sma","version":{"major":0,"minor":0,"patch":0},"attributes":{"language":"SparkSql"}}'
```
