# SQL Server-Azure Synapse - System Tables

Translation spec for Transact-SQL System Tables

## System tables

| Transact-SQL | Snowflake SQL | Notes |  |
| --- | --- | --- | --- |
| SYS.ALL\_VIEWS | INFORMATION\_SCHEMA.VIEWS |  |  |
| SYS.ALL\_COLUMNS | INFORMATION\_SCHEMA.COLUMNS |  |  |
| SYS.COLUMNS | INFORMATION\_SCHEMA.COLUMNS |  |  |
| SYS.OBJECTS | INFORMATION\_SCHEMA.OBJECT\_PRIVILEGES |  |  |
| SYS.PROCEDURES | INFORMATION\_SCHEMA.PROCEDURES |  |  |
| SYS.SEQUENCES | INFORMATION\_SCHEMA.SEQUENCES |  |  |
| SYS.ALL\_OBJECTS | INFORMATION\_SCHEMA.OBJECT\_PRIVILEGES |  |  |
| ALL\_PARAMETERS | **Not supported** |  |  |
| SYS.ALL\_SQL\_MODULES | **Not supported** |  |  |
| SYS.ALLOCATION\_UNITS | **Not supported** |  |  |
| SYS.ASSEMBLY\_MODULES | **Not supported** |  |  |
| SYS.CHECK\_CONSTRAINTS | **Not supported** |  |  |
| SYS.COLUMN\_STORE\_DICTIONARIES | **Not supported** |  |  |
| SYS.COLUMN\_STORE\_ROW\_GROUPS | **Not supported** |  |  |
| SYS.COLUMN\_STORE\_SEGMENTS | **Not supported** |  |  |
| SYS.COMPUTED\_COLUMNS | **Not supported** |  |  |
| SYS.DEFAULT\_CONSTRAINTS | **Not supported** |  |  |
| SYS.EVENTS | **Not supported** |  |  |
| SYS.EVENT\_NOTIFICATIONS | **Not supported** |  |  |
| SYS.EVENT\_NOTIFICATION\_EVENT\_TYPES | **Not supported** |  |  |
| SYS.EXTENDED\_PROCEDURES | **Not supported** |  |  |
| SYS.EXTERNAL\_LANGUAGE\_FILES | **Not supported** |  |  |
| SYS.EXTERNAL\_LANGUAGES | **Not supported** |  |  |
| SYS.EXTERNAL\_LIBRARIES | **Not supported** |  |  |
| SYS.EXTERNAL\_LIBRARY\_FILES | **Not supported** |  |  |
| SYS.FOREIGN\_KEYS | INFORMATION\_SCHEMA.TABLE\_CONSTRAINTS |  |  |
| SYS.FOREIGN\_KEY\_COLUMNS | **Not supported** |  |  |
| SYS.FUNCTION\_ORDER\_COLUMNS | **Not supported** |  |  |
| SYS.HASH\_INDEXES | **Not supported** |  |  |
| SYS.INDEXES | **Not supported** |  |  |
| SYS.INDEX\_COLUMNS | **Not supported** |  |  |
| SYS.INDEX\_RESUMABLE\_OPERATIONS | **Not supported** |  |  |
| SYS.INTERNAL\_PARTITIONS | **Not supported** |  |  |
| SYS.INTERNAL\_TABLES | **Not supported** |  |  |
| SYS.KEY\_CONSTRAINTS | **Not supported** |  |  |
| SYS.MASKED\_COLUMNS | **Not supported** |  |  |
| SYS.MEMORY\_OPTIMIZED\_TABLES\_INTERNAL\_ATTRIBUTES | **Not supported** |  |  |
| SYS.MODULE\_ASSEMBLY\_USAGES | **Not supported** |  |  |
| SYS.NUMBERED\_PROCEDURES | **Not supported** |  |  |
| SYS.NUMBERED\_PROCEDURE\_PARAMETERS | **Not supported** |  |  |
| SYS.PARAMETERS | **Not supported** |  |  |
| SYS.PARTITIONS | **Not supported** |  |  |
| SYS.PERIODS | **Not supported** |  |  |
| SYS.SERVER\_ASSEMBLY\_MODULES | **Not supported** |  |  |
| SYS.SERVER\_EVENTS | **Not supported** |  |  |
| SYS.SERVER\_EVENT\_NOTIFICATIONS | **Not supported** |  |  |
| SYS.SERVER\_SQL\_MODULE | **Not supported** |  |  |
| SYS.SERVER\_TRIGGERS | **Not supported** |  |  |
| SYS.\_SERVER\_TRIGGER\_EVENTS | **Not supported** |  |  |
| SYS.SQL\_DEPENDENCIES | **Not supported** |  |  |
| SYS.SQL\_EXPRESSION\_DEPENDENCIES | **Not supported** |  |  |
| SYS.SQL\_MODULES | **Not supported** |  |  |
| SYS.STATS | **Not supported** |  |  |
| SYS.STATS\_COLUMNS | **Not supported** |  |  |
| SYS.SYNONYMS | **Not supported** |  |  |
| SYS.SYSTEM\_COLUMNS | **Not supported** |  |  |
| SYS.SYSTEM\_OBJECTS | **Not supported** |  |  |
| SYS.SYSTEM\_PARAMETERS | **Not supported** |  |  |
| SYS.SYSCONSTRAINTS | INFORMATION\_SCHEMA.TABLE\_CONSTRAINTS |  |  |
| SYS.SYSTEM\_SQL\_MODULES” | **Not supported** |  |  |

Expand

Show lessSee more

## SYSCONSTRAINTS

Applies to

- SQL Server
- Azure Synapse Analytics

Note

Some parts in the output code are omitted for clarity reasons.

### Description

The `sysconstraints` compatibility view maps constraint IDs to the objects and tables they belong to. It is a legacy system table from earlier SQL Server versions ([SQL Server documentation](https://learn.microsoft.com/en-us/sql/relational-databases/system-compatibility-views/sys-sysconstraints-transact-sql)).

Queries against `sysconstraints` (or `sys.sysconstraints`) are transformed into queries against Snowflake’s `INFORMATION_SCHEMA.TABLE_CONSTRAINTS`. Common `OBJECT_NAME()` patterns are also rewritten:

| sysconstraints pattern | Snowflake equivalent |
| --- | --- |
| `OBJECT_NAME(constid) = 'X'` | `CONSTRAINT_NAME = 'X'` |
| `OBJECT_NAME(id) = 'Y'` | `TABLE_NAME = 'Y'` |

Expand

Show lessSee more

When `OBJECT_NAME()` is called with an unrecognized argument or compared against a non-literal value, the expression is preserved and [SSC-EWI-TS0104](../../issues-and-troubleshooting/conversion-issues/sqlServerEWI#ssc-ewi-ts0104) is emitted.

### Sample Source Patterns

#### 1. Basic sysconstraints query

##### SQL Server

Copy code

```
SELECT 1 FROM sysconstraints WHERE OBJECT_NAME(constid) = 'CPK' AND OBJECT_NAME(id) = 'T';
```

##### Snowflake

Copy code

```
SELECT
  1
FROM
  INFORMATION_SCHEMA.TABLE_CONSTRAINTS
WHERE
  CONSTRAINT_NAME = 'CPK'
  AND TABLE_NAME = 'T';
```

#### 2. Qualified sys.sysconstraints

##### SQL Server

Copy code

```
SELECT 1 FROM sys.sysconstraints WHERE OBJECT_NAME(constid) = 'PK_Orders' AND OBJECT_NAME(id) = 'Orders';
```

##### Snowflake

Copy code

```
SELECT
  1
FROM
  INFORMATION_SCHEMA.TABLE_CONSTRAINTS
WHERE
  CONSTRAINT_NAME = 'PK_Orders'
  AND TABLE_NAME = 'Orders';
```

#### 3. sysconstraints inside IF EXISTS with DROP CONSTRAINT

##### SQL Server

Copy code

```
IF ( EXISTS(SELECT 1 FROM sysconstraints WHERE OBJECT_NAME(constid) = 'LoanDynamicMBSLoadCPK'))
BEGIN
  ALTER TABLE [dbo].[LoanDynamicMBSLoad] DROP CONSTRAINT [LoanDynamicMBSLoadCPK] WITH ( ONLINE = OFF )
END
GO
```

##### Snowflake

Copy code

```
BEGIN
  IF ((EXISTS (
    SELECT
      1
    FROM
      INFORMATION_SCHEMA.TABLE_CONSTRAINTS
    WHERE
      CONSTRAINT_NAME = 'LoanDynamicMBSLoadCPK'
  ))) THEN
    BEGIN
      ALTER TABLE IF EXISTS dbo.LoanDynamicMBSLoad DROP CONSTRAINT LoanDynamicMBSLoadCPK;
    END;
  END IF;
END;
```

Note

The `WITH ( ONLINE = OFF )` clause is removed because Snowflake does not support index options on `DROP CONSTRAINT`. The `IF EXISTS` at the constraint level is also stripped because Snowflake does not support it in that position.

#### 4. Unmapped argument emits EWI

##### SQL Server

Copy code

```
SELECT 1 FROM sysconstraints WHERE OBJECT_NAME(status) = 'X';
```

##### Snowflake

Copy code

```
SELECT
  1
FROM
  INFORMATION_SCHEMA.TABLE_CONSTRAINTS
WHERE
  !!!RESOLVE EWI!!! /*** SSC-EWI-TS0104 - 'OBJECT_NAME(status) in sysconstraints query' COULD NOT BE AUTOMATICALLY CONVERTED IN SYSTEM TABLE QUERY. MANUAL REVIEW REQUIRED ***/!!!
  OBJECT_NAME(status) = 'X';
```

### Known Issues

#### 1. Only `OBJECT_NAME(constid)` and `OBJECT_NAME(id)` are automatically mapped

Other arguments to `OBJECT_NAME()` inside sysconstraints queries cannot be automatically resolved and will emit [SSC-EWI-TS0104](../../issues-and-troubleshooting/conversion-issues/sqlServerEWI#ssc-ewi-ts0104).

#### 2. Non-literal comparisons are not converted

If `OBJECT_NAME()` is compared to a column reference, variable, or expression (instead of a string literal), the expression is preserved with an EWI annotation.

#### 3. JOIN statements with sysconstraints are not supported

Queries that join `sysconstraints` with other tables are not automatically translated.

### Related EWIs

1. [SSC-EWI-TS0104](../../issues-and-troubleshooting/conversion-issues/sqlServerEWI#ssc-ewi-ts0104): System table query pattern could not be automatically converted.
2. [SSC-EWI-0073](../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0073): Pending Functional Equivalence Review.

## SYS.FOREIGN\_KEYS

Applies to

- SQL Server
- Azure Synapse Analytics

Note

Some parts in the output code are omitted for clarity reasons.

### Description

Contains a row per object that is a FOREIGN KEY constraint ([SQLServer Documentation](https://learn.microsoft.com/en-us/sql/relational-databases/system-catalog-views/sys-foreign-keys-transact-sql?view=sql-server-ver16)).

The columns for **FOREIGN KEY** (sys.foreign\_keys) are the following:

| Column name | Data type | Description | Has equivalent column in Snowflake |
| --- | --- | --- | --- |
| <Columns inherited from sys.objects> | - | For a list of columns that this view inherits, see [sys.objects (Transact-SQL).](https://learn.microsoft.com/en-us/sql/relational-databases/system-catalog-views/sys-objects-transact-sql?view=sql-server-ver16) | Partial |
| referenced\_object\_id | int | ID of the referenced object. | No |
| key\_index\_id | int | ID of the key index within the referenced object. | No |
| is\_disabled | bit | FOREIGN KEY constraint is disabled. | No |
| is\_not\_for\_replication | bit | FOREIGN KEY constraint was created by using the NOT FOR REPLICATION option. | No |
| is\_not\_trusted | bit | FOREIGN KEY constraint has not been verified by the system. | No |
| delete\_referential\_action | tinyint | The referential action that was declared for this FOREIGN KEY when a delete happens. See [SQLServer Documentation](https://learn.microsoft.com/en-us/sql/relational-databases/system-catalog-views/sys-foreign-keys-transact-sql?view=sql-server-ver16). | No |
| delete\_referential\_action\_desc | nvarchar(60) | Description of the referential action that was declared for this FOREIGN KEY when a delete occurs. See [SQLServer Documentation](https://learn.microsoft.com/en-us/sql/relational-databases/system-catalog-views/sys-foreign-keys-transact-sql?view=sql-server-ver16). | No |
| update\_referential\_action | tinyint | The referential action that was declared for this FOREIGN KEY when an update happens. See [SQLServer Documentation](https://learn.microsoft.com/en-us/sql/relational-databases/system-catalog-views/sys-foreign-keys-transact-sql?view=sql-server-ver16). | No |
| update\_referential\_action\_desc | nvarchar(60) | Description of the referential action that was declared for this FOREIGN KEY when an update happens. See [SQLServer Documentation](https://learn.microsoft.com/en-us/sql/relational-databases/system-catalog-views/sys-foreign-keys-transact-sql?view=sql-server-ver16). | No |
| is\_system\_named | bit | 1 = Name was generated by the system.  0 = Name was supplied by the user. | No |

Expand

Show lessSee more

The inherited columns from **sys.objects** are the following:

For more information, review the [sys.objects documentation](https://learn.microsoft.com/en-us/sql/relational-databases/system-catalog-views/sys-objects-transact-sql?view=sql-server-ver16).

| Column name | Data type | Description | Has equivalent column in Snowflake |
| --- | --- | --- | --- |
| name | sysname | Object name. | Yes |
| object\_id | int | Object identification number. Is unique within a database. | No |
| principal\_id | int | ID of the individual owner, if different from the schema owner. | No |
| schema\_id | int | ID of the schema that the object is contained in. | No |
| parent\_object\_id | int | ID of the object to which this object belongs. | No |
| type | char(2) | Object type | Yes |
| type\_desc | nvarchar(60) | Description of the object type | Yes |
| create\_date | datetime | Date the object was created. | Yes |
| modify\_date | datetime | Date the object was last modified by using an ALTER statement. | Yes |
| is\_ms\_shipped | bit | Object is created by an internal SQL Server component. | No |
| is\_published | bit | Object is created by an internal SQL Server component. | No |
| is\_schema\_published | bit | Only the schema of the object is published. | No |

Expand

Show lessSee more

Warning

Notice that, in this case, for the sys.foreign\_keys, there is no equivalence in Snowflake. But, the equivalence is made under the columns inherited from sys.objects.

#### Applicable column equivalence

| SQLServer | Snowflake | Limitations | Applicable |
| --- | --- | --- | --- |
| name | CONSTRAINT\_NAME | Names auto-generated by the database may be reviewed to the target Snowflake auto-generated name, | Yes |
| type | CONSTRAINT\_TYPE | The type column has a variety of options. But, in this case, the support is only for the letter ‘F’ which represents the foreign keys. | No. Because of the extra validation to determine the foreign keys from all table constraints, it is not applicable. |
| type\_desc | CONSTRAINT\_TYPE | No limitations found. | No. Because of the extra validation to determine the foreign keys from all table constraints, it is not applicable. |
| create\_date | CREATED | Data type differences. | Yes |
| modify\_date | LAST\_ALTERED | Data type differences. | Yes |
| parent\_object\_id | CONSTRAINT\_CATALOG, CONSTRAINT\_SCHEMA, TABLE\_NAME | Columns are generated only for the cases that use the OBJECT\_ID() function and, the name has a valid pattern. | Yes |

Expand

Show lessSee more

##### Syntax in SQL Server

Copy code

```
:force:

SELECT ('column_name' | * )
FROM sys.foreign_keys;
```

##### Syntax in Snowflake

Copy code

```
SELECT ('column_name' | * )
FROM information_schema.table_constraints
WHERE CONSTRAINT_TYPE = 'FOREIGN KEY';
```

Note

Since the equivalence for the system foreign keys is the catalog view in Snowflake for in ormation\_schema.table\_constraints, it is necessary to define the type of the constraint in an additional ‘WHERE’ clause to identify foreign key constraints from other constraints.

### Sample Source Patterns

To accomplish correctly the following samples, it is required to run the following statements:

#### SQL Server

Copy code

```
:force:

CREATE TABLE Customers (
    CustomerID INT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Email VARCHAR(100)
);

CREATE TABLE Orders (
    OrderID INT PRIMARY KEY,
    CustomerID INT,
    OrderDate DATE,
    TotalAmount DECIMAL(10, 2),
    CONSTRAINT FK_Name_Test FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);

INSERT INTO Customers (CustomerID, FirstName, LastName, Email)
VALUES
    (1, 'John', 'Doe', 'john.doe@example.com'),
    (2, 'Jane', 'Smith', 'jane.smith@example.com');

INSERT INTO Orders (OrderID, CustomerID, OrderDate, TotalAmount)
VALUES
    (101, 1, '2023-09-01', 100.50),
    (102, 1, '2023-09-02', 75.25),
    (103, 2, '2023-09-03', 50.00);
```

##### Snowflake

Copy code

```
:force:

CREATE OR REPLACE TABLE Customers (
    CustomerID INT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Email VARCHAR(100)
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
;

CREATE OR REPLACE TABLE Orders (
    OrderID INT PRIMARY KEY,
    CustomerID INT,
    OrderDate DATE,
    TotalAmount DECIMAL(10, 2),
       CONSTRAINT FK_Name_Test FOREIGN KEY (CustomerID) REFERENCES Customers (CustomerID)
   )
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
;

INSERT INTO Customers (CustomerID, FirstName, LastName, Email)
VALUES
    (1, 'John', 'Doe', 'john.doe@example.com'),
    (2, 'Jane', 'Smith', 'jane.smith@example.com');

INSERT INTO Orders (OrderID, CustomerID, OrderDate, TotalAmount)
VALUES
    (101, 1, '2023-09-01', 100.50),
    (102, 1, '2023-09-02', 75.25),
    (103, 2, '2023-09-03', 50.00);
```

#### 1. Simple Select Case

##### SQL Server

Copy code

```
SELECT *
FROM sys.foreign_keys;
```

##### Result

| name | object\_id | principal\_id | schema\_id | type | type\_desc | create\_date | modify\_date | parent\_object\_id | is\_ms\_shipped | is\_published | is\_schema\_published | referenced\_object\_id | key\_index\_id | is\_disabled | is\_not\_for\_replication | is\_not\_trusted | delete\_referential\_action | delete\_referential\_action\_desc | update\_referential\_action | update\_referential\_action\_desc | is\_system\_named |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FK\_Name\_Test | 1719677174 | NULL | 1 | F | FOREIGN\_KEY\_CONSTRAINT | 2023-09-11 22:20:04.160 | 2023-09-11 22:20:04.160 | 1687677060 | false | true | false | 1655676946 | 1 | false | false |  | 0 | NO\_ACTION | 0 | NO\_ACTION | true |

Expand

Show lessSee more

##### Snowflake

Copy code

```
SELECT *
FROM
INFORMATION_SCHEMA.TABLE_CONSTRAINTS
WHERE
CONSTRAINT_TYPE = 'FOREIGN KEY';
```

##### Result

| CONSTRAINT\_CATALOG | CONSTRAINT\_SCHEMA | CONSTRAINT\_NAME | TABLE\_CATALOG | TABLE\_SCHEMA | TABLE\_NAME | CONSTRAINT\_TYPE | IS\_DEFERRABLE | INITIALLY\_DEFERRED | ENFORCED | COMMENT | CREATED | LAST\_ALTERED | RELY |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DBTEST | PUBLIC | FK\_Name\_Test | DATETEST | PUBLIC | ORDERS | FOREIGN KEY | NO | YES | NO | null | 2023-09-11 15:23:51.969 -0700 | 2023-09-11 15:23:52.097 -0700 | NO |

Expand

Show lessSee more

Warning

Results differ due to the differences in column objects and missing equivalence. The result may be checked.

#### 2. Name Column Case

##### SQL Server

Copy code

```
:force:

SELECT * FROM sys.foreign_keys WHERE name = 'FK_Name_Test';
```

##### Result

| name | object\_id | principal\_id | schema\_id | type | type\_desc | create\_date | modify\_date | parent\_object\_id | is\_ms\_shipped | is\_published | is\_schema\_published | referenced\_object\_id | key\_index\_id | is\_disabled | is\_not\_for\_replication | is\_not\_trusted | delete\_referential\_action | delete\_referential\_action\_desc | update\_referential\_action | update\_referential\_action\_desc | is\_system\_named |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FK\_Name\_Test | 1719677174 | NULL | 1 | F | FOREIGN\_KEY\_CONSTRAINT | 2023-09-11 22:20:04.160 | 2023-09-11 22:20:04.160 | 1687677060 | false | true | false | 1655676946 | 1 | false | false |  | 0 | NO\_ACTION | 0 | NO\_ACTION | true |

Expand

Show lessSee more

##### Snowflake

Copy code

```
:force:

SELECT * FROM
INFORMATION_SCHEMA.TABLE_CONSTRAINTS
WHERE
CONSTRAINT_NAME = 'FK_NAME_TEST'
AND CONSTRAINT_TYPE = 'FOREIGN KEY';
```

##### Result

| CONSTRAINT\_CATALOG | CONSTRAINT\_SCHEMA | CONSTRAINT\_NAME | TABLE\_CATALOG | TABLE\_SCHEMA | TABLE\_NAME | CONSTRAINT\_TYPE | IS\_DEFERRABLE | INITIALLY\_DEFERRED | ENFORCED | COMMENT | CREATED | LAST\_ALTERED | RELY |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DBTEST | PUBLIC | FK\_Name\_Test | DATETEST | PUBLIC | ORDERS | FOREIGN KEY | NO | YES | NO | null | 2023-09-11 15:23:51.969 -0700 | 2023-09-11 15:23:52.097 -0700 | NO |

Expand

Show lessSee more

Warning

This translation may require verification if the constraint name is auto-generated by the database and used in the query. For more information review the [Known Issues](#known-issues) section.

#### 3. Parent Object ID Case

In this example, a database and schema were created to exemplify the processing of the names to create different and equivalent columns.

##### SQL Server

Copy code

```
:force:

use database_name_test
create schema schema_name_test

CREATE TABLE schema_name_test.Customers (
    CustomerID INT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Email VARCHAR(100)
);

CREATE TABLE schema_name_test.Orders (
    OrderID INT PRIMARY KEY,
    CustomerID INT,
    OrderDate DATE,
    TotalAmount DECIMAL(10, 2),
    CONSTRAINT FK_Name_Test FOREIGN KEY (CustomerID) REFERENCES schema_name_test.Customers(CustomerID)
);

INSERT INTO schema_name_test.Customers (CustomerID, FirstName, LastName, Email)
VALUES
    (1, 'John', 'Doe', 'john.doe@example.com'),
    (2, 'Jane', 'Smith', 'jane.smith@example.com');

INSERT INTO schema_name_test.Orders (OrderID, CustomerID, OrderDate, TotalAmount)
VALUES
    (101, 1, '2023-09-01', 100.50),
    (102, 1, '2023-09-02', 75.25),
    (103, 2, '2023-09-03', 50.00);

SELECT * FROM sys.foreign_keys WHERE name = 'FK_Name_Test' AND parent_object_id = OBJECT_ID(N'database_name_test.schema_name_test.Orders')
```

##### Result

| name | object\_id | principal\_id | schema\_id | type | type\_desc | create\_date | modify\_date | parent\_object\_id | is\_ms\_shipped | is\_published | is\_schema\_published | referenced\_object\_id | key\_index\_id | is\_disabled | is\_not\_for\_replication | is\_not\_trusted | delete\_referential\_action | delete\_referential\_action\_desc | update\_referential\_action | update\_referential\_action\_desc | is\_system\_named |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FK\_Name\_Test | 1719677174 | NULL | 1 | F | FOREIGN\_KEY\_CONSTRAINT | 2023-09-11 22:20:04.160 | 2023-09-11 22:20:04.160 | 1687677060 | false | true | false | 1655676946 | 1 | false | false |  | 0 | NO\_ACTION | 0 | NO\_ACTION | true |

Expand

Show lessSee more

##### Snowflake

Copy code

```
:force:

USE DATABASE database_name_test;

CREATE SCHEMA IF NOT EXISTS schema_name_test
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}'
;

CREATE OR REPLACE TABLE schema_name_test.Customers (
    CustomerID INT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Email VARCHAR(100)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}'
;

CREATE OR REPLACE TABLE schema_name_test.Orders (
    OrderID INT PRIMARY KEY,
    CustomerID INT,
    OrderDate DATE,
    TotalAmount DECIMAL(10, 2),
       CONSTRAINT FK_Name_Test FOREIGN KEY (CustomerID) REFERENCES schema_name_test.Customers (CustomerID)
   )
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "07/11/2025",  "domain": "no-domain-provided" }}'
;

INSERT INTO schema_name_test.Customers (CustomerID, FirstName, LastName, Email)
VALUES
    (1, 'John', 'Doe', 'john.doe@example.com'),
    (2, 'Jane', 'Smith', 'jane.smith@example.com');

INSERT INTO schema_name_test.Orders (OrderID, CustomerID, OrderDate, TotalAmount)
VALUES
    (101, 1, '2023-09-01', 100.50),
    (102, 1, '2023-09-02', 75.25),
    (103, 2, '2023-09-03', 50.00);

SELECT * FROM
    INFORMATION_SCHEMA.TABLE_CONSTRAINTS
WHERE
    CONSTRAINT_NAME = 'FK_NAME_TEST'
    AND CONSTRAINT_CATALOG = 'DATABASE_NAME_TEST'
    AND CONSTRAINT_SCHEMA = 'SCHEMA_NAME_TEST'
    AND TABLE_NAME = 'ORDERS'
    AND CONSTRAINT_TYPE = 'FOREIGN KEY';
```

##### Result

| CONSTRAINT\_CATALOG | CONSTRAINT\_SCHEMA | CONSTRAINT\_NAME | TABLE\_CATALOG | TABLE\_SCHEMA | TABLE\_NAME | CONSTRAINT\_TYPE | IS\_DEFERRABLE | INITIALLY\_DEFERRED | ENFORCED | COMMENT | CREATED | LAST\_ALTERED | RELY |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DATABASE\_NAME\_TEST | SCHEMA\_NAME\_TEST | FK\_Name\_Test | DATABASE\_NAME\_TEST | SCHEMA\_NAME\_TEST | ORDERS | FOREIGN KEY | NO | YES | NO | null | 2023-09-11 15:23:51.969 -0700 | 2023-09-11 15:23:52.097 -0700 | NO |

Expand

Show lessSee more

Warning

If the name coming inside the OBJECT\_ID() function does not have a valid pattern, it will not be converted due to name processing limitations on special characters.

Warning

Review the database that is being used in Snowflake.

#### 4. Type Column Case

The ‘F’ in SQL Server means ‘Foreign Key’ and it is removed due to the validation at the ending to specify the foreign key from all the table constraints.

##### SQL Server

Copy code

```
 SELECT * FROM sys.foreign_keys WHERE type = 'F';
```

##### Result

| name | object\_id | principal\_id | schema\_id | type | type\_desc | create\_date | modify\_date | parent\_object\_id | is\_ms\_shipped | is\_published | is\_schema\_published | referenced\_object\_id | key\_index\_id | is\_disabled | is\_not\_for\_replication | is\_not\_trusted | delete\_referential\_action | delete\_referential\_action\_desc | update\_referential\_action | update\_referential\_action\_desc | is\_system\_named |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FK\_Name\_Test | 1719677174 | NULL | 3 | F | FOREIGN\_KEY\_CONSTRAINT | 2023-09-11 22:20:04.160 | 2023-09-11 22:20:04.160 | 1687677060 | false | true | false | 1655676946 | 1 | false | false |  | 0 | NO\_ACTION | 0 | NO\_ACTION | true |

Expand

Show lessSee more

##### Snowflake

Copy code

```
 SELECT * FROM
    INFORMATION_SCHEMA.TABLE_CONSTRAINTS
WHERE
    type = 'F' AND CONSTRAINT_TYPE = 'FOREIGN KEY';
```

##### Result

| CONSTRAINT\_CATALOG | CONSTRAINT\_SCHEMA | CONSTRAINT\_NAME | TABLE\_CATALOG | TABLE\_SCHEMA | TABLE\_NAME | CONSTRAINT\_TYPE | IS\_DEFERRABLE | INITIALLY\_DEFERRED | ENFORCED | COMMENT | CREATED | LAST\_ALTERED | RELY |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DBTEST | PUBLIC | FK\_Name\_Test | DATETEST | PUBLIC | ORDERS | FOREIGN KEY | NO | YES | NO | null | 2023-09-11 15:23:51.969 -0700 | 2023-09-11 15:23:52.097 -0700 | NO |

Expand

Show lessSee more

#### 5. Type Desc Column Case

The ‘type\_desc’ column is removed due to the validation at the ending to specify the foreign key from all the table constraints.

##### SQL Server

Copy code

```
:force:

SELECT
    *
FROM
    sys.foreign_keys
WHERE
    type_desc = 'FOREIGN_KEY_CONSTRAINT';
```

##### Result

| name | object\_id | principal\_id | schema\_id | type | type\_desc | create\_date | modify\_date | parent\_object\_id | is\_ms\_shipped | is\_published | is\_schema\_published | referenced\_object\_id | key\_index\_id | is\_disabled | is\_not\_for\_replication | is\_not\_trusted | delete\_referential\_action | delete\_referential\_action\_desc | update\_referential\_action | update\_referential\_action\_desc | is\_system\_named |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FK\_Name\_Test | 1719677174 | NULL | 3 | F | FOREIGN\_KEY\_CONSTRAINT | 2023-09-11 22:20:04.160 | 2023-09-11 22:20:04.160 | 1687677060 | false | true | false | 1655676946 | 1 | false | false |  | 0 | NO\_ACTION | 0 | NO\_ACTION | true |

Expand

Show lessSee more

##### Snowflake

Copy code

```
:force:

SELECT
    *
FROM
    INFORMATION_SCHEMA.TABLE_CONSTRAINTS
WHERE
    type_desc = 'FOREIGN_KEY_CONSTRAINT' AND CONSTRAINT_TYPE = 'FOREIGN KEY';
```

##### Result

| CONSTRAINT\_CATALOG | CONSTRAINT\_SCHEMA | CONSTRAINT\_NAME | TABLE\_CATALOG | TABLE\_SCHEMA | TABLE\_NAME | CONSTRAINT\_TYPE | IS\_DEFERRABLE | INITIALLY\_DEFERRED | ENFORCED | COMMENT | CREATED | LAST\_ALTERED | RELY |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DBTEST | PUBLIC | FK\_Name\_Test | DATETEST | PUBLIC | ORDERS | FOREIGN KEY | NO | YES | NO | null | 2023-09-11 15:23:51.969 -0700 | 2023-09-11 15:23:52.097 -0700 | NO |

Expand

Show lessSee more

#### 6. Modify Date Column Simple Case

##### SQL Server

Copy code

```
SELECT *
FROM sys.foreign_keys
WHERE modify_date = CURRENT_TIMESTAMP;
```

##### Result

Copy code

```
The query produced no results.
```

##### Snowflake

Copy code

```
:force:

SELECT *
FROM
    INFORMATION_SCHEMA.TABLE_CONSTRAINTS
WHERE
    LAST_ALTERED = CURRENT_TIMESTAMP()
    AND CONSTRAINT_TYPE = 'FOREIGN KEY';
```

##### Result

Copy code

```
The query produced no results.
```

#### 7. Modify Date Column with DATEDIFF() Case

The following example shows a more complex scenario where the columns from sys.foreign\_keys (inherited from sys.objects) are inside a function DATEDIFF. In this case, the argument corresponding to the applicable equivalence is changed to the corresponding column from the information.schema in Snowflake.

##### SQL Server

Copy code

```
:force:

SELECT *
FROM sys.foreign_keys
WHERE DATEDIFF(DAY, modify_date, GETDATE()) <= 30;
```

##### Result

Copy code

```
The foreign keys altered in the last 30 days.
```

##### Snowflake

Copy code

```
SELECT *
FROM
    INFORMATION_SCHEMA.TABLE_CONSTRAINTS
WHERE
    DATEDIFF(DAY, LAST_ALTERED, CURRENT_TIMESTAMP() :: TIMESTAMP) <= 30
    AND CONSTRAINT_TYPE = 'FOREIGN KEY';
```

##### Result

Copy code

```
The foreign keys altered in the last 30 days.
```

#### 8. Create Date Column Case

##### SQL Server

Copy code

```
SELECT *
FROM sys.foreign_keys
WHERE create_date = '2023-09-12 14:36:38.060';
```

##### Result

Copy code

```
The foreign keys that were created on the specified date and time.
```

##### Snowflake

Copy code

```
SELECT *
FROM
    INFORMATION_SCHEMA.TABLE_CONSTRAINTS
WHERE
    CREATED = '2023-09-12 14:36:38.060'
    AND CONSTRAINT_TYPE = 'FOREIGN KEY';
```

##### Result

Copy code

```
The foreign keys that were created on the specified date and time.
```

Warning

The result may change if the creation date is specific due to the time on which the queries were executed. It is possible to execute a specified query at one time on the origin database and then execute the objects at another time in the new Snowflake queries.

#### 9. Selected Columns Single Name Case

##### SQL Server

Copy code

```
SELECT name
FROM sys.foreign_keys;
```

##### Result

| name |
| --- |
| FK\_Name\_Test |

Expand

Show lessSee more

##### Snowflake

Copy code

```
:force:

SELECT
    CONSTRAINT_NAME
FROM
    INFORMATION_SCHEMA.TABLE_CONSTRAINTS
WHERE
    CONSTRAINT_TYPE = 'FOREIGN KEY';
```

##### Result

| CONSTRAINT\_NAME |
| --- |
| FK\_Name\_Test |

Expand

Show lessSee more

#### 10. Selected Columns Qualified Name Case

##### SQL Server

Copy code

```
:force:

SELECT
    fk.name
FROM sys.foreign_keys AS fk;
```

##### Result

| name |
| --- |
| FK\_Name\_Test |

Expand

Show lessSee more

##### Snowflake

Copy code

```
:force:

SELECT
    fk.CONSTRAINT_NAME
FROM
    INFORMATION_SCHEMA.TABLE_CONSTRAINTS AS fk
WHERE
    CONSTRAINT_TYPE = 'FOREIGN KEY';
```

##### Result

| CONSTRAINT\_NAME |
| --- |
| FK\_Name\_Test |

Expand

Show lessSee more

### Known Issues

#### 1. The ‘name’ column may not show a correct output if the constraint does not have a user-created name

If the referenced name is one auto-generated from the database, it would be probable to review it and use the wanted value.

##### 2. When selecting columns, there is a limitation that depends on the applicable columns that are equivalent in Snowflake

Since the columns from sys.foreign\_keys are not completely equivalent in Snowflake, some results may change due to the limitations on the equivalence.

##### 3. The OBJECT\_ID() function may have a valid pattern to be processed or the database, schema or table could not be extracted

Based on the name that receives the OBJECT\_ID() function, the processing of this name will be limited and dependent on formatting.

##### 4. Name Column With OBJECT\_NAME() Function Case

Since the OBJECT\_NAME() function is not supported yet, the transformations related to this function are not supported.

##### SQL Server

Copy code

```
SELECT name AS ForeignKeyName,
    OBJECT_NAME(parent_object_id) AS ReferencingTable,
    OBJECT_NAME(referenced_object_id) AS ReferencedTable
FROM sys.foreign_keys;
```

##### Snowflake

Copy code

```
SELECT
    name AS ForeignKeyName,
    OBJECT_NAME(parent_object_id) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'OBJECT_NAME' NODE ***/!!! AS ReferencingTable,
    OBJECT_NAME(referenced_object_id) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'OBJECT_NAME' NODE ***/!!! AS ReferencedTable
FROM
    INFORMATION_SCHEMA.TABLE_CONSTRAINTS
WHERE
    CONSTRAINT_TYPE = 'FOREIGN KEY';
```

##### 5. SCHEMA\_NAME() and TYPE\_NAME() functions are also not supported yet.

##### 6. Different Join statement types may be not supported if the system table is not supported. Review the supported system tables.

##### 7. Cases with JOIN statements are not supported.

##### 8. Names with alias AS are not supported.

### Related EWIs

1. [SSC-EWI-0073](../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0073): Pending Functional Equivalence Review.
