# SnowConvert AI - Object References Report

Note

Built-in elements are not considered as part of this report.

## What is an “Object Reference”?

An object reference is the term used to refer to DDL definitions in the source code, that are being referenced by code units. The table below shows which elements could be referenced in each supported language.

| Object | Teradata | Oracle | Transact-SQL | Redshift | BigQuery | Spark | Databricks | Hive | Vertica | PostgreSQL | Greenplum | Netezza | Azure Synapse | IBM DB2 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Table | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| View | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Procedure | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Function | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Macro | ✓ |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Package Function |  | ✓ |  |  |  |  |  |  |  |  |  |  |  |  |
| Package Procedure |  | ✓ |  |  |  |  |  |  |  |  |  |  |  |  |
| \*Package |  | ✓ |  |  |  |  |  |  |  |  |  |  |  |  |
| Join Index | ✓ |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Index |  | ✓ |  |  |  |  |  |  |  |  |  |  |  |  |
| Synonym |  | ✓ |  |  |  |  |  |  |  |  |  |  |  |  |
| Database Link |  | ✓ |  |  |  |  |  |  |  |  |  |  |  |  |
| Type | ✓ | ✓ | ✓ |  |  |  |  |  |  |  |  |  | ✓ |  |
| Materialized View |  | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |  | ✓ | ✓ | ✓ | ✓ |  |
| Trigger | ✓ | ✓ | ✓ |  |  |  |  |  |  |  |  |  | ✓ |  |
| Sequence | ✓ | ✓ | ✓ |  |  |  |  |  |  |  |  |  | ✓ |  |
| Constraint |  | ✓ | ✓ |  |  |  |  |  |  |  |  |  | ✓ |  |

Expand

Show lessSee more

Note

If an asterisk (‘\*’) is listed in the section above, it means that the object is used to call properties from itself that are not considered DDL statements such as constants, variables, or cursors.

### Where can I find it?

The object references report can be found in a folder named *“reports”*, in the output folder of your conversion. The name of the file itself starts with *“ObjectReferences”* so it can easily be located.

The format of the file is **.CSV**.

### What information does it contain?

The object references report contains the following information about all the references found while converting:

| Column | Description |
| --- | --- |
| PartitionKey | The unique identifier of the conversion. |
| FileName | The name of the file in which the object is located. |
| Caller\_CodeUnit | The type of the code unit referencing an existing element. |
| Caller\_CodeUnit\_Database | The database of the code unit referencing an existing element. For now, only SQL Server objects can have a database. |
| Caller\_CodeUnit\_Schema | The schema of the code unit referencing an existing element. |
| Caller\_CodeUnit\_Name | The name of the code unit referencing an existing element. |
| Caller\_CodeUnit\_FullName | The fully qualified name of the object referencing an existing element. |
| Referenced\_Element\_Type | The DDL type of the referenced element. |
| Referenced\_Element\_Database | The database of the referenced element. For now, only SQL Server objects can have a database. |
| Referenced\_Element\_Schema | The schema of the referenced element. |
| Referenced\_Element\_Name | The name of the referenced element. |
| Referenced\_Element\_FullName | The full qualified name of the referenced element. |
| Line | The line number inside the file where the reference is located. |
| Relation\_Type | Shows the type of relation used through the caller code unit and the object reference. |

Expand

Show lessSee more

### Oracle Database Links as object references

To get the information such as database name, schema name, or object name of database link references, we need to know how the database link was defined. Database links contain the most relevant information in the connection string used in its definition. E.g.

#### Database Link with database name

Copy code

```
 CREATE DATABASE LINK remote_hr_db
CONNECT TO hr_user
IDENTIFIED BY hr_password
USING 'RemoteDB';

SELECT * FROM hr.employees@remote_hr_db;
```

Using the example above, the object reference information should look like this:

| Caller\_CodeUnit | Referenced\_Element\_Type | Referenced\_Element\_Database | Referenced\_Element\_Schema | Referenced\_Element\_Name | Referenced\_Element\_FullName | Line |
| --- | --- | --- | --- | --- | --- | --- |
| SELECT | CREATE DATABASE LINK | RemoteDb | N/A | remote\_hr\_db | hr.employees@remote\_hr\_db | 6 |

#### Database Link with database and schema names

Copy code

```
 CREATE DATABASE LINK remote_hr_db1
CONNECT TO hr_user
IDENTIFIED BY hr_password
USING 'RemoteDB.MySchema';

SELECT * FROM employees@remote_hr_db1;
```

Using the example above, the object reference information should look like this:

| Caller\_CodeUnit | Referenced\_Element\_Type | Referenced\_Element\_Database | Referenced\_Element\_Schema | Referenced\_Element\_Name | Referenced\_Element\_FullName | Line |
| --- | --- | --- | --- | --- | --- | --- |
| SELECT | CREATE DATABASE LINK | RemoteDb | MySchema | remote\_hr\_db1 | hr.employees@remote\_hr\_db1 | 6 |

##### Database Link with a connection string

Copy code

```
 CREATE DATABASE LINK remote_hr_db2
CONNECT TO hr_user
IDENTIFIED BY hr_password
USING '(DESCRIPTION=(
          ADDRESS=
          (PROTOCOL=TCP)
          (HOST=10.48.195.17)
          (PORT=1521))
      (CONNECT_DATA=(SID=MyDB)))';

SELECT * FROM employees@remote_hr_db2;
```

Using the example above, the object reference information should look like this:

| Caller\_CodeUnit | Referenced\_Element\_Type | Referenced\_Element\_Database | Referenced\_Element\_Schema | Referenced\_Element\_Name | Referenced\_Element\_FullName | Line |
| --- | --- | --- | --- | --- | --- | --- |
| SELECT | CREATE DATABASE LINK | MyDB | N/A | remote\_hr\_db2 | employees@remote\_hr\_db2 | 6 |

### Relation Type

The relation type represents how a caller code unit is related to an object reference. SnowConvert AI is able to identify the following kinds of relations:

- FOREIGN KEY
- INSERT
- DELETE
- UPDATE
- CALL
- EXECUTE
- SYNONYM
- ALTER
- DROP
- MERGE
- TRUNCATE
- LOCK
- INDEX
- TABLE COLUMN
- GRANT
- REVOKE
- SELECT
  - COLUMN
  - FROM
  - WHERE
  - HAVING
  - GROUP BY
  - JOIN
  - ORDER BY

#### Examples

1. A stored procedure referencing a table through an UPDATE statement:

Copy code

```
 CREATE TABLE TABLE2
(
  COL1 VARCHAR(50) NOT NULL,
  COL2 INT NOT NULL
);

CREATE OR REPLACE PROCEDURE Procedure01 (param1 NUMBER)
IS
BEGIN
    UPDATE TABLE2
    SET COL1 = 'Anderson'
    WHERE COL2 = param1;
END;
```

The report will show something like the following table:

| Caller\_CodeUnit | Referenced\_Element\_Type | Referenced\_Element\_FullName | Line | Relation\_Type |
| --- | --- | --- | --- | --- |
| CREATE PROCEDURE | CREATE TABLE | TABLE2 | 10 | UPDATE |

2. A table referencing another table through a FOREIGN KEY:

Copy code

```
 CREATE TABLE TABLE1
(
  COL1 INT
);

CREATE TABLE TABLE2
(
  COL1 INT,
  CONSTRAINT FK_COL1 FOREIGN KEY (COL1)
    REFERENCES TABLE1(COL1)
);
```

The report will show something like the following table:

| Caller\_CodeUnit | Referenced\_Element\_Type | Referenced\_Element\_FullName | Line | Relation\_Type |
| --- | --- | --- | --- | --- |
| CREATE TABLE | CREATE TABLE | TABLE1 | 10 | FOREIGN KEY |

3. A table referenced by a view in the FROM clause of the SELECT statement:

Copy code

```
 CREATE TABLE TABLE1
(
  COL1 INT
);

CREATE VIEW VIEW1
AS
SELECT * FROM TABLE1;
```

The report will show something like the following table:

| Caller\_CodeUnit | Referenced\_Element\_Type | Referenced\_Element\_FullName | Line | Relation\_Type |
| --- | --- | --- | --- | --- |
| CREATE VIEW | CREATE TABLE | TABLE1 | 8 | SELECT - FROM |

4. A user-defined function (UDF) referenced by a view as a result set column.

Copy code

```
 CREATE FUNCTION FUNCTION1(PARAM1 INT)
RETURN NUMBER
IS
BEGIN
  RETURN(PARAM1 + 1);
END;

CREATE VIEW VIEW1
AS
SELECT FUNCTION1(*) FROM TABLE1;
```

The report will show something like the following table:

| Caller\_CodeUnit | Referenced\_Element\_Type | Referenced\_Element\_FullName | Line | Relation\_Type |
| --- | --- | --- | --- | --- |
| CREATE VIEW | CREATE FUNCTION | FUNCTION1 | 10 | SELECT - COLUMN |
