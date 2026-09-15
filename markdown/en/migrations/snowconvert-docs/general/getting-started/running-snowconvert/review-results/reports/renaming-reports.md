# SnowConvert AI - Renaming Report

## What is a renaming object?

It is an object that underwent a name change during the migration, following the changes configured in Redshift Studio.

Note

The report includes all migrated top-level code units, regardless of whether they underwent renaming or not.

### What information does it contain?

The renaming report is presented in a table format, and contains the following columns:

| Column | Description |
| --- | --- |
| CodeUnit | The type of the Code Unit. |
| SourceDatabase | The source database. |
| SourceSchema | The source schema. |
| SourceName | The source name. |
| SnowflakeDatabase | The Snowflake database. |
| SnowflakeSchema | The Snowflake schema |
| SnowflakeName | The Snowflake name. |

Input Code

Copy code

```
:force:
CREATE SCHEMA Renaming_example_schema;

CREATE TABLE Renaming_example_schema.Renaming_example_table_tl (
    id INT,
    name VARCHAR(100)
);

INSERT INTO Renaming_example_schema.Renaming_example_table_tl(id, name) VALUES (1, "tom");

SELECT * FROM Renaming_example_schema.Renaming_example_table_tl;

CREATE TABLE DB_1.MASTER.Renaming_example_table_tl_v2 (
    id INT,
    name VARCHAR(100)
);

INSERT INTO DB_1.MASTER.Renaming_example_table_tl_v2(id, name) VALUES (1, "tom");

SELECT * FROM DB_1.MASTER.Renaming_example_table_tl_v2;

CREATE TABLE NoRenaming_db.NoRenaming_schema.NoRenamingTable_test (
    id INT,
    name VARCHAR(100)
)

INSERT INTO NoRenaming_db.NoRenaming_schema.NoRenamingTable_test(id, name) VALUES (1, "tom");

SELECT * FROM NoRenaming_db.NoRenaming_schema.NoRenamingTable_test;
```

Output code

Copy code

```
:force:
CREATE SCHEMA IF NOT EXISTS Target_Renaming_example_schema
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "10/23/2024" }}'
;

CREATE TABLE Target_Renaming_example_schema.Target_Renaming_example_table_tl (
    id INT,
    name VARCHAR(100)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "10/23/2024" }}';

INSERT INTO Target_Renaming_example_schema.Target_Renaming_example_table_tl (id, name) VALUES (1, "tom");

SELECT * FROM
    Target_Renaming_example_schema.Target_Renaming_example_table_tl;

CREATE TABLE Target_DB_1.MASTER.Renaming_example_table_tl_v2 (
    id INT,
    name VARCHAR(100)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "10/23/2024" }}';

INSERT INTO Target_DB_1.MASTER.Renaming_example_table_tl_v2 (id, name) VALUES (1, "tom");

SELECT * FROM
    Target_DB_1.MASTER.Renaming_example_table_tl_v2;

CREATE TABLE NoRenaming_db.NoRenaming_schema.NoRenamingTable_test (
    id INT,
    name VARCHAR(100)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "10/23/2024" }}'

INSERT INTO NoRenaming_db.NoRenaming_schema.NoRenamingTable_test (id, name) VALUES (1, "tom");

SELECT * FROM
    NoRenaming_db.NoRenaming_schema.NoRenamingTable_test;
```

## Embedded Objects

Renaming and reporting are only available for top-level objects. Embedded objects will not appear in the report and renaming will not be applied to these objects.

Input Code

Copy code

```
CREATE TABLE Renaming_example_table_tl (
   id INT,
   name VARCHAR(100)
);

CREATE PROCEDURE Renaming_example_procedure()
    LANGUAGE plpgsql
AS $$
BEGIN
CREATE TABLE Renaming_example_table_embedded (
   id INT,
   name VARCHAR(100)
);
SELECT * FROM Renaming_example_table_embedded;
SELECT * FROM Renaming_example_table_tl;
END;
$$;
```

Output Code

Copy code

```
CREATE TABLE Target_Renaming_example_table_tl (
   id INT,
   name VARCHAR(100)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "11/13/2024",  "domain": "test" }}';

CREATE PROCEDURE Target_Renaming_example_procedure ()
RETURNS VARCHAR
    LANGUAGE SQL
    COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "11/13/2024",  "domain": "test" }}'
AS $$
BEGIN
CREATE TABLE Renaming_example_table_embedded (
   id INT,
   name VARCHAR(100)
);
SELECT * FROM
   Renaming_example_table_embedded;
SELECT * FROM
   Target_Renaming_example_table_tl;
END;
$$;
```
