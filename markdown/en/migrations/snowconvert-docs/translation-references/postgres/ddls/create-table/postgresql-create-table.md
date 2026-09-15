# PostgreSQL - CREATE TABLE

Translation from PostgreSQL to Snowflake

## Applies to

- PostgreSQL
- Greenplum
- Netezza

## Description

Creates a new table in PostgreSQL. You define a list of columns, each of which holds data of a distinct type. The owner of the table is the issuer of the CREATE TABLE command.

For more information, please refer to `CREATE TABLE` documentation.

## Grammar Syntax

Copy code

```
:force:
CREATE [ [ GLOBAL | LOCAL ] { TEMPORARY | TEMP } | UNLOGGED ] TABLE [ IF NOT EXISTS ] table_name ( [
  { column_name data_type [ STORAGE { PLAIN | EXTERNAL | EXTENDED | MAIN | DEFAULT } ] [ COMPRESSION compression_method ] [ COLLATE collation ] [ column_constraint [ ... ] ]
    | table_constraint
    | LIKE source_table [ like_option ... ] }
    [, ... ]
] )
[ INHERITS ( parent_table [, ... ] ) ]
[ PARTITION BY { RANGE | LIST | HASH } ( { column_name | ( expression ) } [ COLLATE collation ] [ opclass ] [, ... ] ) ]
[ USING method ]
[ WITH ( storage_parameter [= value] [, ... ] ) | WITHOUT OIDS ]
[ ON COMMIT { PRESERVE ROWS | DELETE ROWS | DROP } ]
[ TABLESPACE tablespace_name ]

CREATE [ [ GLOBAL | LOCAL ] { TEMPORARY | TEMP } | UNLOGGED ] TABLE [ IF NOT EXISTS ] table_name
    OF type_name [ (
  { column_name [ WITH OPTIONS ] [ column_constraint [ ... ] ]
    | table_constraint }
    [, ... ]
) ]
[ PARTITION BY { RANGE | LIST | HASH } ( { column_name | ( expression ) } [ COLLATE collation ] [ opclass ] [, ... ] ) ]
[ USING method ]
[ WITH ( storage_parameter [= value] [, ... ] ) | WITHOUT OIDS ]
[ ON COMMIT { PRESERVE ROWS | DELETE ROWS | DROP } ]
[ TABLESPACE tablespace_name ]

CREATE [ [ GLOBAL | LOCAL ] { TEMPORARY | TEMP } | UNLOGGED ] TABLE [ IF NOT EXISTS ] table_name
    PARTITION OF parent_table [ (
  { column_name [ WITH OPTIONS ] [ column_constraint [ ... ] ]
    | table_constraint }
    [, ... ]
) ] { FOR VALUES partition_bound_spec | DEFAULT }
[ PARTITION BY { RANGE | LIST | HASH } ( { column_name | ( expression ) } [ COLLATE collation ] [ opclass ] [, ... ] ) ]
[ USING method ]
[ WITH ( storage_parameter [= value] [, ... ] ) | WITHOUT OIDS ]
[ ON COMMIT { PRESERVE ROWS | DELETE ROWS | DROP } ]
[ TABLESPACE tablespace_name ]

where column_constraint is:

[ CONSTRAINT constraint_name ]
{ NOT NULL |
  NULL |
  CHECK ( expression ) [ NO INHERIT ] |
  DEFAULT default_expr |
  GENERATED ALWAYS AS ( generation_expr ) STORED |
  GENERATED { ALWAYS | BY DEFAULT } AS IDENTITY [ ( sequence_options ) ] |
  UNIQUE [ NULLS [ NOT ] DISTINCT ] index_parameters |
  PRIMARY KEY index_parameters |
  REFERENCES reftable [ ( refcolumn ) ] [ MATCH FULL | MATCH PARTIAL | MATCH SIMPLE ]
    [ ON DELETE referential_action ] [ ON UPDATE referential_action ] }
[ DEFERRABLE | NOT DEFERRABLE ] [ INITIALLY DEFERRED | INITIALLY IMMEDIATE ]

and table_constraint is:

[ CONSTRAINT constraint_name ]
{ CHECK ( expression ) [ NO INHERIT ] |
  UNIQUE [ NULLS [ NOT ] DISTINCT ] ( column_name [, ... ] ) index_parameters |
  PRIMARY KEY ( column_name [, ... ] ) index_parameters |
  EXCLUDE [ USING index_method ] ( exclude_element WITH operator [, ... ] ) index_parameters [ WHERE ( predicate ) ] |
  FOREIGN KEY ( column_name [, ... ] ) REFERENCES reftable [ ( refcolumn [, ... ] ) ]
    [ MATCH FULL | MATCH PARTIAL | MATCH SIMPLE ] [ ON DELETE referential_action ] [ ON UPDATE referential_action ] }
[ DEFERRABLE | NOT DEFERRABLE ] [ INITIALLY DEFERRED | INITIALLY IMMEDIATE ]

and like_option is:

{ INCLUDING | EXCLUDING } { COMMENTS | COMPRESSION | CONSTRAINTS | DEFAULTS | GENERATED | IDENTITY | INDEXES | STATISTICS | STORAGE | ALL }

and partition_bound_spec is:

IN ( partition_bound_expr [, ...] ) |
FROM ( { partition_bound_expr | MINVALUE | MAXVALUE } [, ...] )
  TO ( { partition_bound_expr | MINVALUE | MAXVALUE } [, ...] ) |
WITH ( MODULUS numeric_literal, REMAINDER numeric_literal )

index_parameters in UNIQUE, PRIMARY KEY, and EXCLUDE constraints are:

[ INCLUDE ( column_name [, ... ] ) ]
[ WITH ( storage_parameter [= value] [, ... ] ) ]
[ USING INDEX TABLESPACE tablespace_name ]

exclude_element in an EXCLUDE constraint is:

{ column_name | ( expression ) } [ COLLATE collation ] [ opclass [ ( opclass_parameter = value [, ... ] ) ] ] [ ASC | DESC ] [ NULLS { FIRST | LAST } ]

referential_action in a FOREIGN KEY/REFERENCES constraint is:

{ NO ACTION | RESTRICT | CASCADE | SET NULL [ ( column_name [, ... ] ) ] | SET DEFAULT [ ( column_name [, ... ] ) ] }
```

## Tables Options

### TEMPORARY | TEMP, or IF NOT EXISTS

Tip

This syntax is fully supported in Snowflake.

### GLOBAL | LOCAL

Note

This syntax is not needed in Snowflake.

According to PostgreSQL’s documentation, GLOBAL | LOCAL are present for SQL Standard compatibility, but have no effect in PostgreSQL and are deprecated. For that reason, these keywords will be removed during the migration process.

#### Sample Source

Input Code:

##### PostgreSQL

Copy code

```
:force:
CREATE GLOBAL TEMP TABLE TABLE1 (
   COL1 integer
);
```

Output Code:

##### Snowflake

Copy code

```
:force:
CREATE TEMPORARY TABLE TABLE1 (
   COL1 integer
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "postgresql",  "convertedOn": "05/09/2025",  "domain": "no-domain-provided" }}';
```

### UNLOGGED TABLE

Note

This syntax is not needed in Snowflake.

UNLOGGED tables offer a significant speed advantage because they are not written to the write-ahead log. Snowflake doesn’t support this functionality, so the `UNLOGGED` clause will be commented out.

### Code Example

#### Input Code:

##### Greenplum

Copy code

```
:force:
CREATE UNLOGGED TABLE TABLE1 (
  COL1 integer
);
```

#### Output Code:

##### Snowflake

Copy code

```
:force:
CREATE
--       --** SSC-FDM-PG0005 - UNLOGGED TABLE IS NOT SUPPORTED IN SNOWFLAKE, DATA WRITTEN MAY HAVE DIFFERENT PERFORMANCE. **
--       UNLOGGED
                TABLE TABLE1 (
   COL1 integer
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "postgresql",  "convertedOn": "05/09/2025",  "domain": "no-domain-provided" }}';
```

## Column Attributes

### CHECK Attribute

Tip

This syntax is supported in Snowflake for deterministic, scalar expressions.

The CHECK clause specifies an expression producing a Boolean result that new or updated rows must satisfy for an insert or update operation to succeed. Snowflake supports CHECK constraints with deterministic, scalar expressions. Unsupported expressions (UDFs, non-deterministic functions) are flagged with SSC-EWI-0116.

Danger

**Supported:**

- Basic CHECK constraints with scalar, deterministic expressions
- Column-level and table-level CHECK constraints
- Named and unnamed constraints

**Unsupported (flagged with SSC-EWI-0116):**

- User-defined functions (UDFs)
- Non-deterministic built-in functions
- Context-dependent functions (e.g., `CURRENT_TIMESTAMP`, `CURRENT_USER`, `NOW()`)
- Subqueries

Grammar Syntax

Copy code

```
:force:
CHECK  ( <expression> )
```

#### Sample Source

##### Example 1: Basic CHECK Constraint (Supported)

Input Code:

##### PostgreSQL

Copy code

```
:force:
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    price NUMERIC(10,2) CHECK (price > 0),
    quantity INT CHECK (quantity >= 0 AND quantity <= 1000)
);
```

Output Code:

##### Snowflake

Copy code

```
:force:
CREATE OR REPLACE TABLE products (
    product_id INT PRIMARY KEY,
    price NUMERIC(10, 2) CHECK (price > 0),
    quantity INT CHECK (quantity >= 0
    AND quantity <= 1000)
)
;
```

##### Example 2: Named Table-Level CHECK Constraint

Input Code:

##### PostgreSQL

Copy code

```
:force:
CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    birth_date DATE,
    hire_date DATE,
    CONSTRAINT chk_dates CHECK (hire_date >= birth_date)
);
```

Output Code:

##### Snowflake

Copy code

```
:force:
CREATE OR REPLACE TABLE employees (
    employee_id INT PRIMARY KEY,
    birth_date DATE,
    hire_date DATE,
    CONSTRAINT chk_dates CHECK(hire_date >= birth_date)
)
;
```

### GENERATED BY DEFAULT AS IDENTITY

Tip

This syntax is fully supported in Snowflake.

Specifies that the column is a default IDENTITY column and enables you to assign a unique value to the column automatically.

Grammar Syntax

Copy code

```
:force:
 GENERATED { ALWAYS | BY DEFAULT } AS IDENTITY [ ( <sequence_options> ) ]
```

#### Sample Source

Input Code:

##### PostgreSQL

Copy code

```
:force:
CREATE TABLE table1 (
idValue INTEGER GENERATED ALWAYS AS IDENTITY)
```

Output Code:

##### Snowflake

Copy code

```
:force:
CREATE TABLE table1 (
idValue INTEGER IDENTITY(1, 1) ORDER
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "postgresql",  "convertedOn": "05/09/2025",  "domain": "no-domain-provided" }}'
```

## Table Constraints

### Primary Key, Foreign Key, and Unique

Warning

This syntax is partially supported in Snowflake.

The constraint definitions are kept; however, in Snowflake, unique, primary, and foreign keys are used for documentation and do not enforce constraints or uniqueness. They help describe table relationships but don’t impact data integrity or performance.

## Table Attributes

### LIKE option

Warning

This syntax is partially supported in Snowflake.

The `LIKE` clause specifies a table from which the new table automatically copies all column names, their data types, and their not-null constraints. PostgreSQL supports several options, while Snowflake does not support these options so they will be removed.

#### Grammar Syntax

Copy code

```
:force:
  LIKE source_table { INCLUDING | EXCLUDING }
  { AM | COMMENTS | CONSTRAINTS | DEFAULTS | ENCODING | GENERATED | IDENTITY | INDEXES | RELOPT | STATISTICS | STORAGE | ALL }
```

#### Sample Source Patterns

Input Code:

##### PostgreSQL

Copy code

```
:force:
CREATE TABLE source_table (
    id INT,
    name VARCHAR(255),
    created_at TIMESTAMP,
    status BOOLEAN
);

CREATE TABLE target_table_no_constraints (LIKE source_table INCLUDING DEFAULTS EXCLUDING CONSTRAINTS EXCLUDING INDEXES);
```

Output Code:

##### Snowflake

Copy code

```
:force:
CREATE TABLE source_table (
    id INT,
    name VARCHAR(255),
    created_at TIMESTAMP,
    status BOOLEAN
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "postgresql",  "convertedOn": "05/12/2025",  "domain": "no-domain-provided" }}';
CREATE TABLE target_table_no_constraints LIKE source_table;
```

### ON COMMIT

Warning

This syntax is partially supported.

Specifies the behavior of the temporary table when a commit is done.

#### Grammar Syntax

Copy code

```
:force:
ON COMMIT { PRESERVE ROWS | DELETE ROWS | DROP }
```

## Sample Source Patterns

### Input Code:

#### PostgreSQL

Copy code

```
:force:
CREATE GLOBAL TEMPORARY TABLE temp_data_delete (
    id INT,
    data TEXT
) ON COMMIT DELETE ROWS;
```

#### Output Code:

##### Snowflake

Copy code

```
:force:
CREATE TEMPORARY TABLE temp_data_delete (
    id INT,
    data TEXT
)
----** SSC-FDM-0008 - ON COMMIT NOT SUPPORTED **
--ON COMMIT DELETE ROWS
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "postgresql",  "convertedOn": "05/12/2025",  "domain": "no-domain-provided" }}';
```

### PARTITION BY, USING, TABLESPACE, and WITH

Note

This syntax is not needed in Snowflake.

These clauses in Snowflake are unnecessary because they automatically handle the data storage, unlike PostgreSQL, which could be set up manually. For this reason, these clauses are removed during migration.

## Related EWIs

1. [SSC-EWI-0035](../../../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0035): Check statement not supported.
2. [SSC-FDM-PG0005](../../../../issues-and-troubleshooting/functional-difference/postgresqlFDM#ssc-fdm-pg0005): UNLOGGED Table is not supported in Snowflake; data written may have different performance.
3. [SSC-FDM-0008](../../../../issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0008): On Commit not supported.
