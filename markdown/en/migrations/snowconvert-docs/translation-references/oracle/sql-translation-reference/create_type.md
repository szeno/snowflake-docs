# Oracle - Create Type

This is a translation reference to convert Oracle Create Type Statements (UDTs) to snowflake

## General Description

Many Oracle `CREATE TYPE` statements are translated to **[Snowflake native user-defined types](https://docs.snowflake.com/en/sql-reference/sql/create-type)** where the shape is supported—for example object types with attributes, `VARRAY` mapped to Snowflake `ARRAY`, and nested table types mapped to `ARRAY` of the element type. Unsupported options (subtype inheritance, member bodies, incomplete types, and others) are flagged with Oracle-specific EWIs; see [Related EWIs](#related-ewis) and the [issues reference](../../../issues-and-troubleshooting/conversion-issues/oracleEWI).

One of the most important features the Oracle database engine offers is an Object-Oriented approach. PL/SQL offers capabilities beyond other relational databases in the form of OOP by using Java-like statements in the form of packages, functions, tables and types. This document will cover the last one and how it is solved, remaining compliant to functionality.

Oracle supports the following specifications:

- Abstract Data Type (*ADT*) (*including an SQLJ object type*).
- Standalone varying array (*varray*) type.
- Standalone nested table type.
- Incomplete object type.

All this according to the information found in [Oracle Create Type Statement Documentation](https://docs.oracle.com/en/database/oracle/oracle-database/21/lnpls/CREATE-TYPE-statement.html#GUID-389D603D-FBD0-452A-8414-240BBBC57034)

Copy code

```
CREATE [ OR REPLACE ] [ EDITIONABLE | NONEDITIONAL ] TYPE <type name>
[ <type source creation options> ]
[<type definition>]
[ <type properties> ]
```

## Limitations

**Native user-defined types** (`CREATE TYPE … AS OBJECT`, `ARRAY`, etc.) are supported as documented in the [SQL data types overview](https://docs.snowflake.com/en/sql-reference/data-types.html). Many Oracle type definitions are mapped to those native types. Patterns that still have **no** or **partial** mapping—such as subtype inheritance (`UNDER`), member methods and type bodies, table types, and incomplete forward declarations—may require manual redesign or are reported via EWIs (for example [SSC-EWI-OR0139](../../../issues-and-troubleshooting/conversion-issues/oracleEWI#ssc-ewi-or0139) through [SSC-EWI-OR0142](../../../issues-and-troubleshooting/conversion-issues/oracleEWI#ssc-ewi-or0142)). [Semi-structured Data Types](https://docs.snowflake.com/en/sql-reference/data-types-semistructured.html) remain relevant for legacy scenarios that still use `VARIANT` in converted code.

Following are the User Defined Types features for which **NO** workaround is proposed:

### Subtypes: Type Hierarchy

These statements aren’t supported in Snowflake. They are only recognized, but no translation is offered.

Copy code

```
CREATE TYPE person_t AS OBJECT (name VARCHAR2(100), ssn NUMBER) 
   NOT FINAL;
/

CREATE TYPE employee_t UNDER person_t 
   (department_id NUMBER, salary NUMBER) 
   NOT FINAL;
/

CREATE TYPE part_time_emp_t UNDER employee_t (num_hrs NUMBER);
/
```

### Type properties

These refer to the options that are normally used when using OOP in PL/SQL: Persistable, Instantiable and Final.

Copy code

```
CREATE OR REPLACE TYPE type1 AS OBJECT () NOT FINAL NOT INSTANTIABLE NOT PERSISTABLE;
CREATE OR REPLACE TYPE type2 AS OBJECT () FINAL INSTANTIABLE PERSISTABLE;
```

### Nested Table Type

These statements aren’t supported in Snowflake. They are only recognized, but no translation is offered.

Copy code

```
CREATE TYPE textdoc_typ AS OBJECT
    ( document_typ      VARCHAR2(32)
    , formatted_doc     BLOB
    ) ;
/

CREATE TYPE textdoc_tab AS TABLE OF textdoc_typ;
/
```

### Type Source Creation Options

These options stand for custom options regarding access and querying the type.

Copy code

```
CREATE TYPE type1 FORCE OID 'abc' SHARING = METADATA DEFAULT COLLATION schema1.collation ACCESSIBLE BY (schema1.unitaccesor) AS OBJECT ();
CREATE TYPE type2 FORCE OID 'abc' SHARING = NONE DEFAULT COLLATION collation ACCESSIBLE BY (PROCEDURE unitaccesor) AS OBJECT ();
CREATE TYPE type3 AUTHID CURRENT_USER AS OBJECT ();
CREATE TYPE type4 AUTHID DEFINER AS OBJECT ();
```

## Proposed workarounds

### About types definition

For the definition, the proposed workaround is to create semi-structure data type to mimic Oracle’s data type.

### About types member function

For the member functions containing logic and DML, the proposed workaround relies on helpers to translate this into stored procedures.

## Current Translation Support

The next table shows a summary of the current translation support. Please keep in mind that translations may still not be final, and more work may be needed.

| Type Statement Element | Current recognition status | Current translation status | Has Known Workarounds |
| --- | --- | --- | --- |
| [Object Type Definitions](#object-type-definition) | Recognized. | Translated to Snowflake `CREATE TYPE … AS OBJECT` where supported. | Yes. |
| [Subtype Definitions](#subtype-definition) | Recognized. | Not Translated. | No. |
| [Array Type Definitions](#array-type-definition) | Recognized. | Translated to Snowflake `CREATE TYPE … AS ARRAY` (see [SSC-FDM-0043](../../../issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0043)). | Yes. |
| [Nested Table Definitions](#nested-table-type) | Recognized. | Translated to Snowflake `ARRAY` of element type where supported. | Limited. |
| [Member Function Definitions](#member-function-definitions) | Recognized. | Not Translated. | Yes. |

Expand

Show lessSee more

## Known Issues

### 1. DML usages for Object Types — partial support

DDL definitions for User-Defined Types are translated to native Snowflake `CREATE TYPE … AS OBJECT` / `… AS ARRAY` where the shape is supported. Constructor calls (for example `address_type('123 Main St', …)` for object types and `VARRAY_TYPE('a', 'b', 'c')` for VARRAY / nested-table types) are now also translated to `OBJECT_CONSTRUCT(…) :: <type>` and `ARRAY_CONSTRUCT(…) :: <type>` respectively, in `INSERT … VALUES`, `INSERT … SELECT`, `UPDATE … SET`, top-level `SELECT`, and PL/SQL variable initialization. DML that relies on object-type member functions or other Oracle-specific UDT operations may still require manual review; an [SSC-EWI-0073](../../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0073) is emitted in those cases.

#### 2. Create Type creation options are not supported

Currently, there is no known workaround for any of the creation options, for these reasons they are not taken into account when defining the type.

## Related EWIs

Deprecation and replacement messaging for legacy “not supported” issues: [SSC-EWI-0056](../../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0056), [SSC-EWI-0095](../../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0095), [SSC-EWI-OR0007](../../../issues-and-troubleshooting/conversion-issues/oracleEWI#ssc-ewi-or0007).

Unsupported or incomplete `CREATE TYPE` shapes: [SSC-EWI-OR0139](../../../issues-and-troubleshooting/conversion-issues/oracleEWI#ssc-ewi-or0139), [SSC-EWI-OR0140](../../../issues-and-troubleshooting/conversion-issues/oracleEWI#ssc-ewi-or0140), [SSC-EWI-OR0141](../../../issues-and-troubleshooting/conversion-issues/oracleEWI#ssc-ewi-or0141), [SSC-EWI-OR0142](../../../issues-and-troubleshooting/conversion-issues/oracleEWI#ssc-ewi-or0142).

Functional differences: [SSC-FDM-0043](../../../issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0043) (array size limit removed; replaces deprecated `SSC-FDM-OR0051`), [SSC-FDM-OR0052](../../../issues-and-troubleshooting/functional-difference/oracleFDM#ssc-fdm-or0052)–[SSC-FDM-OR0054](../../../issues-and-troubleshooting/functional-difference/oracleFDM#ssc-fdm-or0054).

## Array Type Definition

This is a translation reference to convert the Array Variant of the Oracle Create Type Statements (UDTs) to Snowflake

Note

Oracle `VARRAY` types are translated to Snowflake `CREATE TYPE … AS ARRAY ( element_type )`. Fixed varray capacity is **not** preserved; see [SSC-FDM-0043](../../../issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0043). Column usages may still be migrated to `VARIANT` in older or mixed scenarios—verify generated DDL for your workload.

VARRAY and nested-table **constructor calls** (for example `phone_list_typ_demo('2000-0000', '4000-0000')`) used in `INSERT`, `UPDATE` and top-level `SELECT` are translated to `ARRAY_CONSTRUCT(...) :: <type_name>`. See [VARRAY constructor calls in DML](#varray-constructor-calls-in-dml) below.

Note

Some parts in the output code are omitted for clarity reasons.

### Description

Array Types define an array structure of a previously existing datatype (including other Custom Types).

For many workloads, the type definition is emitted as a Snowflake **native `ARRAY` type**. Usages in tables and PL/SQL may still involve [Semi-structured Data Types](https://docs.snowflake.com/en/sql-reference/data-types-semistructured.html) or `OBJECT` depending on context.

Copy code

```
CREATE TYPE <type name>
AS { VARRAY | [VARYING] ARRAY } ( <size limit> ) OF <data type>
```

### Sample Source Patterns

#### Inserts for the array usage

VARRAY and nested-table constructor calls used in `INSERT … VALUES`, `INSERT … SELECT`, `UPDATE` and top-level `SELECT` are translated to `ARRAY_CONSTRUCT(...)` and explicitly cast to the original UDT name with `:: <type>`, so column type checks against the UDT continue to succeed.

##### Oracle

Copy code

```
INSERT INTO customer_table_demo(customer_table_id, customer_data) VALUES
(1, phone_list_typ_demo('2000-0000', '4000-0000', '0000-0000'));

INSERT INTO customer_table_demo(customer_table_id, customer_data) VALUES
(1, phone_list_typ_demo('8000-2000', '0000-0000', '5000-0000'));
```

##### Snowflake

Copy code

```
INSERT INTO customer_table_demo(customer_table_id, customer_data) VALUES
(1, ARRAY_CONSTRUCT('2000-0000', '4000-0000', '0000-0000') :: phone_list_typ_demo);

INSERT INTO customer_table_demo(customer_table_id, customer_data) VALUES
(1, ARRAY_CONSTRUCT('8000-2000', '0000-0000', '5000-0000') :: phone_list_typ_demo);
```

#### VARRAY constructor calls in DML

The translator handles standalone constructor calls in `INSERT … VALUES`, `INSERT … SELECT`, `UPDATE … SET`, and top-level `SELECT` statements. For nested-table types defined with `CREATE TYPE … AS TABLE OF …` the same `ARRAY_CONSTRUCT(...) :: <type>` shape is produced.

##### Oracle

Copy code

```
CREATE TYPE VARRAY_TYPE AS VARRAY(3) OF VARCHAR2(50);
/

CREATE TABLE my_varray_table (id NUMBER, varray_column VARRAY_TYPE);
/

INSERT INTO my_varray_table SELECT 1, VARRAY_TYPE('Apple', 'Banana', 'Orange') FROM dual;

CREATE TYPE NUMBER_LIST AS TABLE OF NUMBER;
/

INSERT INTO my_table SELECT 1, NUMBER_LIST(10, 20, 30) FROM dual;
```

##### Snowflake

Copy code

```
--** SSC-FDM-0043 - ARRAY SIZE LIMIT '3' WAS REMOVED. SNOWFLAKE ARRAYS ARE DYNAMICALLY SIZED. **
CREATE TYPE VARRAY_TYPE AS ARRAY ( VARCHAR(50) );

CREATE OR REPLACE TABLE my_varray_table (
  id NUMBER(38, 18) /*** SSC-FDM-0006 - NUMBER TYPE COLUMN MAY NOT BEHAVE SIMILARLY IN SNOWFLAKE. ***/,
  varray_column ARRAY
)
;

INSERT INTO my_varray_table
SELECT
  1,
  ARRAY_CONSTRUCT('Apple', 'Banana', 'Orange') :: VARRAY_TYPE
FROM
  dual;

CREATE TYPE NUMBER_LIST AS ARRAY ( NUMBER(38, 18) );

INSERT INTO my_table
SELECT
  1,
  ARRAY_CONSTRUCT(10, 20, 30) :: NUMBER_LIST
FROM
  dual;
```

##### Oracle (top-level SELECT)

Copy code

```
CREATE TYPE STRING_ARRAY AS VARRAY(5) OF VARCHAR2(100);
/

SELECT STRING_ARRAY('hello', 'world') FROM dual;
```

##### Snowflake

Copy code

```
--** SSC-FDM-0043 - ARRAY SIZE LIMIT '5' WAS REMOVED. SNOWFLAKE ARRAYS ARE DYNAMICALLY SIZED. **
CREATE TYPE STRING_ARRAY AS ARRAY ( VARCHAR(100) );

SELECT
  ARRAY_CONSTRUCT('hello', 'world') :: STRING_ARRAY
FROM
  dual;
```

#### Array Type usage

##### Oracle

Copy code

```
CREATE TYPE phone_list_typ_demo AS VARRAY(3) OF VARCHAR2(25);
/

CREATE TABLE customer_table_demo (
    customer_table_id INTEGER,
    customer_data phone_list_typ_demo
);
/

SELECT * FROM customer_table_demo;
/
```

##### Results

| CUSTOMER\_TABLE\_ID | CUSTOMER\_DATA |
| --- | --- |
| 1 | [[’2000-0000’,’4000-0000’,’0000-0000’]] |
| 1 | [[’8000-2000’,’0000-0000’,’5000-0000’]] |

Expand

Show lessSee more

##### Snowflake

Copy code

```
--** SSC-FDM-0043 - ARRAY SIZE LIMIT '3' WAS REMOVED. SNOWFLAKE ARRAYS ARE DYNAMICALLY SIZED. **
CREATE TYPE phone_list_typ_demo AS ARRAY ( VARCHAR(25) );

CREATE OR REPLACE TABLE customer_table_demo (
        customer_table_id INTEGER,
        customer_data phone_list_typ_demo
    )
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
;

CREATE OR REPLACE VIEW PUBLIC.customer_table_demo_view
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "" }}'
AS
SELECT
        customer_table_id,
        customer_data
FROM
        customer_table_demo;

    SELECT * FROM
        customer_table_demo_view;
```

##### Results

| CUSTOMER\_TABLE\_ID | CUSTOMER\_DATA |
| --- | --- |
| 1 | [[’2000-0000’, ’4000-0000’, ’0000-0000’]] |
| 1 | [[’8000-2000’, ’0000-0000’, ’5000-0000’]] |

Expand

Show lessSee more

### Known Issues

#### 1. Create Type creation options are not supported

Currently, there is no known workaround for any of the creation options, for these reasons they are not taken into account when defining the type.

##### 2. Migrated code output is not functional

The statements are being changed unnecessarily, which makes them no longer be functional on the output code. This will be addressed when a proper transformation for them is in place.

### Related EWIs

1. [SSC-EWI-0062](../../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0062): Custom type usage changed to variant.
2. [SSC-EWI-0073](../../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0073): Pending Functional Equivalence Review.

## Member Function Definitions

This is a translation reference to convert the Member Functions of the Oracle Create Type Statements (UDTs) to Snowflake

Danger

Type member functions and type body definitions are still not recognized. This page is only used as a future reference for translation.

Note

Some parts in the output code are omitted for clarity reasons.

### Description

Like other Class definitions, Oracle’s TYPE can implement methods to expose behaviors based on its attributes. MEMBER FUCTION will be transformed to Snowflake’s Stored Procedures, to maintain functional equivalence due to limitations.

Since functions are being transformed into procedures, the [transformation reference for PL/SQL](../pl-sql-to-snowflake-scripting/README) also applies here.

### Sample Source Patterns

#### Inserts for Simple square() member function

The next data will be inserted inside the table before querying the select. Please note these Inserts currently need to be manually migrated into Snowflake.

##### Oracle

Copy code

```
INSERT INTO table_member_function_demo(column1) VALUES
(type_member_function_demo(5));
```

##### Snowflake

Copy code

```
INSERT INTO table_member_function_demo (column1)
SELECT OBJECT_CONSTRUCT('a1', 5);
```

#### Simple square() member function

##### Oracle

Copy code

```
-- TYPE DECLARATION
CREATE TYPE type_member_function_demo AS OBJECT (
    a1 NUMBER,
    MEMBER FUNCTION get_square RETURN NUMBER
);
/

-- TYPE BODY DECLARATION
CREATE TYPE BODY type_member_function_demo IS
   MEMBER FUNCTION get_square
   RETURN NUMBER
   IS x NUMBER;
   BEGIN
      SELECT c.column1.a1*c.column1.a1 INTO x
      FROM table_member_function_demo c;
      RETURN (x);
   END;
END;
/

-- TABLE
CREATE TABLE table_member_function_demo (column1 type_member_function_demo);
/

-- QUERYING DATA
SELECT
    t.column1.get_square()
FROM
    table_member_function_demo t;
/
```

##### Results

| T.COLUMN1.GET\_SQUARE() |
| --- |
| 25 |

Expand

Show lessSee more

##### Snowflake

Copy code

```
-- TYPE DECLARATION
!!!RESOLVE EWI!!! /*** SSC-EWI-0056 - CUSTOM TYPES ARE NOT SUPPORTED IN SNOWFLAKE BUT REFERENCES TO THIS CUSTOM TYPE WERE CHANGED TO VARIANT ***/!!!
CREATE TYPE type_member_function_demo AS OBJECT (
    a1 NUMBER,
    MEMBER FUNCTION get_square RETURN NUMBER
)
;

---- TYPE BODY DECLARATION
--!!!RESOLVE EWI!!! /*** SSC-EWI-OR0007 - CREATE TYPE WITHOUT BODY IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
--CREATE TYPE BODY type_member_function_demo IS
--   MEMBER FUNCTION get_square
--   RETURN NUMBER
--   IS x NUMBER;
--   BEGIN
--      SELECT c.column1.a1*c.column1.a1 INTO x
--      FROM table_member_function_demo c;
--      RETURN (x);
--   END;
--END
   ;

-- TABLE
CREATE OR REPLACE TABLE table_member_function_demo (column1 VARIANT !!!RESOLVE EWI!!! /*** SSC-EWI-0062 - CUSTOM TYPE 'type_member_function_demo' USAGE CHANGED TO VARIANT ***/!!!
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
;

CREATE OR REPLACE VIEW PUBLIC.table_member_function_demo_view
<strong>COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "" }}'
</strong><strong>AS
</strong>SELECT
    column1:a1 :: NUMBER AS a1
FROM
    table_member_function_demo;

-- QUERYING DATA
SELECT
    t.column1.get_square() !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 't.column1.get_square' NODE ***/!!!
FROM
    table_member_function_demo t;
```

##### Results

| GET\_SQUARE() |
| --- |
| 25 |

Expand

Show lessSee more

### Known Issues

No Known issues.

### Related EWIs

1. [SSC-EWI-0056](../../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0056): Create Type Not Supported.
2. [SSC-EWI-0062](../../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0062): Custom type usage changed to variant.
3. [SSC-EWI-0073](../../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0073): Pending Functional Equivalence Review.
4. [SSC-EWI-OR0007](../../../issues-and-troubleshooting/conversion-issues/oracleEWI#ssc-ewi-or0007): Create Type Not Supported in Snowflake

## Nested Table Type Definition

This is a translation reference to convert the Nested Table Variant of the Oracle Create Type Statements (UDTs) to Snowflake

Note

Standalone `CREATE TYPE … AS TABLE OF element_type` is translated to Snowflake `CREATE TYPE … AS ARRAY ( element_type )` when the element type is supported. Nested tables used as table columns may still require manual review depending on DML and PL/SQL usage.

### Description

Nested Table Types define an embedded table structure of a previously existing datatype (including other Custom Types). They are closely related to [Array Type](#array-type-definition) definitions; many patterns are mapped to Snowflake `ARRAY`.

Copy code

```
CREATE TYPE <type name> AS TABLE OF <data type>
```

### Sample Source Patterns

#### Nested Table Type usage

##### Oracle

Copy code

```
CREATE TYPE textdoc_typ AS OBJECT (
    document_typ VARCHAR2(32),
    formatted_doc BLOB
);
/

CREATE TYPE textdoc_tab AS TABLE OF textdoc_typ;
/
```

##### Snowflake

Copy code

```
CREATE TYPE textdoc_typ AS OBJECT (
    document_typ VARCHAR(32),
    formatted_doc BINARY
)
;

CREATE TYPE textdoc_tab AS ARRAY ( textdoc_typ );
```

### Known Issues

#### 1. Create Type creation options are not supported

Currently, there is no known workaround for any of the creation options; for these reasons, they are not taken into account when defining the type.

### Related EWIs

1. [SSC-EWI-0073](../../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0073): Pending Functional Equivalence Review
2. [SSC-EWI-0056](../../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0056): Create Type Not Supported.

## Object Type Definition

This is a translation reference to convert the Object Variant of the Oracle Create Type Statements (UDTs) to Snowflake

Note

A translation is supported for Object Type Definitions itself. However, their usages are still a work in progress.

Note

Some parts in the output code are omitted for clarity reasons.

### Description

Object Types define a structure of data similar to a record, with the added advantages of the member function definitions. Meaning that their data may be used along some behavior within the type.

For the translation of object types, the type definition is mapped to Snowflake’s native `CREATE TYPE … AS OBJECT (…)` where the attribute list is supported, and **constructor calls** to the type are translated to `OBJECT_CONSTRUCT(<field>, <value>, …) :: <type_name>`. The symbol table is used to recover the field names from the original `CREATE TYPE`, so positional constructor arguments are mapped to the correct field names in upper-case. When the type symbol cannot be resolved (for example, because the `CREATE TYPE` is not part of the migrated source set), the constructor call is preserved and an [SSC-EWI-0073](../../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0073) is emitted for manual review.

For legacy or partially-supported scenarios where the object type cannot be expressed natively, the column in dependent tables may still be migrated to `VARIANT` and an auxiliary view is added so that downstream `SELECT`s and views to the original table continue to work.

Copy code

```
CREATE TYPE <type name> AS OBJECT
( [{<type column definition> | type method definition } , ...]);
```

### Sample Source Patterns

#### Object Type constructor calls

Object-type constructor calls are translated to `OBJECT_CONSTRUCT('FIELD1', value1, 'FIELD2', value2, …) :: <type_name>`. The cast to the original UDT name is preserved so column type checks and downstream `OBJECT_INSERT` / member access continue to work without changes. The transformation applies to constructor calls inside variable initialization, `INSERT … VALUES`, `INSERT … SELECT`, `UPDATE … SET`, and top-level `SELECT` expressions.

Note

Field names in the generated `OBJECT_CONSTRUCT` keys are always **upper-case** (for example `'NAME'`, `'AGE'`). Snowflake object key lookups are case-sensitive, so downstream references using lowercase or mixed-case semi-structured path syntax (for example `obj:name`) will return `NULL`. Use the exact upper-case key or quote it consistently throughout the migrated code.

##### Oracle

Copy code

```
CREATE OR REPLACE TYPE Person_Type AS OBJECT (
  Name VARCHAR2(50),
  Age NUMBER
);
/

CREATE OR REPLACE PROCEDURE test_udt_constructor
AS
  person Person_Type := Person_Type('Alice', 30);
BEGIN
  NULL;
END;
```

##### Snowflake

Copy code

```
CREATE TYPE Person_Type AS OBJECT (Name VARCHAR(50), Age NUMBER(38, 18));

CREATE OR REPLACE PROCEDURE test_udt_constructor ()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
  DECLARE
    person Person_Type := OBJECT_CONSTRUCT('NAME', 'Alice', 'AGE', 30) :: Person_Type;
  BEGIN
    NULL;
  END;
$$;
```

##### Oracle (constructor in `INSERT … VALUES` and `UPDATE … SET`)

Copy code

```
CREATE OR REPLACE TYPE address_type AS OBJECT (
  street VARCHAR2(100),
  city VARCHAR2(50),
  state VARCHAR2(2),
  postal_code VARCHAR2(10)
);
/

INSERT INTO employees
VALUES (1, 'John', 'Doe', address_type('123 Main St', 'Los Angeles', 'CA', '90001'));

UPDATE employees
SET home_address = address_type('456 Oak Ave', 'New York', 'NY', '10001')
WHERE employee_id = 1;
```

##### Snowflake

Copy code

```
CREATE TYPE address_type AS OBJECT (street VARCHAR(100), city VARCHAR(50), state VARCHAR(2), postal_code VARCHAR(10));

INSERT INTO employees
VALUES (1, 'John', 'Doe', OBJECT_CONSTRUCT('STREET', '123 Main St', 'CITY', 'Los Angeles', 'STATE', 'CA', 'POSTAL_CODE', '90001') :: address_type);

UPDATE employees
  SET
    home_address = OBJECT_CONSTRUCT('STREET', '456 Oak Ave', 'CITY', 'New York', 'STATE', 'NY', 'POSTAL_CODE', '10001') :: address_type
  WHERE
    employee_id = 1;
```

##### Oracle (constructor when the type symbol is not in the migrated source)

Copy code

```
CREATE OR REPLACE FUNCTION Get_Person_Func
RETURN Person_Type
AS
    v_person Person_Type;
BEGIN
    v_person := Person_Type('Jane Doe', 25);
    RETURN v_person;
END;
```

##### Snowflake

Copy code

```
CREATE OR REPLACE FUNCTION Get_Person_Func ()
RETURNS Person_Type
LANGUAGE SQL
AS
$$
  WITH declaration_variables_cte1 AS
  (
    SELECT
      Person_Type('Jane Doe', 25) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'Person_Type' NODE ***/!!! AS
      v_person
  )
  SELECT
    v_person
  FROM
    declaration_variables_cte1
$$;
```

#### Inserts for Simple Type usage

The next data will be inserted inside the table before querying the select. Please note these Inserts currently need to be manually migrated into Snowflake.

##### Oracle

Copy code

```
INSERT INTO customer_table_demo(customer_table_id, customer_data)
VALUES ( 1, customer_typ_demo(1, 'First Name 1', 'Last Name 1'));

INSERT INTO customer_table_demo(customer_table_id, customer_data)
VALUES ( 2, customer_typ_demo(2, 'First Name 2', 'Last Name 2'));
```

##### Snowflake

Copy code

```
INSERT INTO customer_table_demo(customer_table_id, customer_data)
VALUES ( 1, customer_typ_demo(1, 'First Name 1', 'Last Name 1') !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'customer_typ_demo' NODE ***/!!!);

INSERT INTO customer_table_demo(customer_table_id, customer_data)
VALUES ( 2, customer_typ_demo(2, 'First Name 2', 'Last Name 2') !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'customer_typ_demo' NODE ***/!!!);
```

#### Simple Type usage

##### Oracle

Copy code

```
CREATE TYPE customer_typ_demo AS OBJECT (
    customer_id INTEGER,
    cust_first_name VARCHAR2(20),
    cust_last_name VARCHAR2(20)
);

CREATE TABLE customer_table_demo (
    customer_table_id INTEGER,
    customer_data customer_typ_demo
);

SELECT * FROM customer_table_demo;
```

##### Results

| CUSTOMER\_TABLE\_ID | CUSTOMER\_DATA |
| --- | --- |
| 1 | [1, First Name 1, Last Name 1] |
| 2 | [2, First Name 2, Last Name 2] |

Expand

Show lessSee more

##### Snowflake

Copy code

```
!!!RESOLVE EWI!!! /*** SSC-EWI-0056 - CUSTOM TYPES ARE NOT SUPPORTED IN SNOWFLAKE BUT REFERENCES TO THIS CUSTOM TYPE WERE CHANGED TO VARIANT ***/!!!
CREATE TYPE customer_typ_demo AS OBJECT (
    customer_id INTEGER,
    cust_first_name VARCHAR2(20),
    cust_last_name VARCHAR2(20)
)
;

CREATE OR REPLACE TABLE customer_table_demo (
        customer_table_id INTEGER,
        customer_data VARIANT !!!RESOLVE EWI!!! /*** SSC-EWI-0062 - CUSTOM TYPE 'customer_typ_demo' USAGE CHANGED TO VARIANT ***/!!!
    )
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}}'
;

CREATE OR REPLACE VIEW PUBLIC.customer_table_demo_view
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "" }}'
AS
SELECT
        customer_table_id,
        customer_data:customer_id :: INTEGER AS customer_id,
        customer_data:cust_first_name :: VARCHAR AS cust_first_name,
        customer_data:cust_last_name :: VARCHAR AS cust_last_name
FROM
        customer_table_demo;

    SELECT * FROM
        customer_table_demo_view;
```

##### Results

| CUSTOMER\_TABLE\_ID | CUST\_ID | CUST\_FIRST\_NAME | CUST\_LAST\_NAME |
| --- | --- | --- | --- |
| 1 | 1 | First Name 1 | Last Name 1 |
| 2 | 2 | First Name 2 | Last Name 2 |

Expand

Show lessSee more

#### Inserts for Nested Type Usage

These statements need to be placed between the table creation and the select statement to test the output.

##### Oracle

Copy code

```
INSERT INTO customer_table_demo(customer_id, customer_data) values
(1, customer_typ_demo('Customer 1', email_typ_demo('email@domain.com')));

INSERT INTO customer_table_demo(customer_id, customer_data) values
(2, customer_typ_demo('Customer 2', email_typ_demo('email2@domain.com')));
```

##### Snowflake

Copy code

```
INSERT INTO customer_table_demo(customer_id, customer_data) values
(1, customer_typ_demo('Customer 1', email_typ_demo('email@domain.com') !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'email_typ_demo' NODE ***/!!!) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'customer_typ_demo' NODE ***/!!!);

INSERT INTO customer_table_demo(customer_id, customer_data) values
(2, customer_typ_demo('Customer 2', email_typ_demo('email2@domain.com') !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'email_typ_demo' NODE ***/!!!) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'customer_typ_demo' NODE ***/!!!);
```

#### Nested Type Usage

##### Oracle

Copy code

```
CREATE TYPE email_typ_demo AS OBJECT (email VARCHAR2(20));

CREATE TYPE customer_typ_demo AS OBJECT (
    cust_name VARCHAR2(20),
    cust_email email_typ_demo
);

CREATE TABLE customer_table_demo (
    customer_id INTEGER,
    customer_data customer_typ_demo
);

SELECT * FROM customer_table_demo;
```

##### Results

| CUSTOMER\_ID | CUSTOMER\_DATA |
| --- | --- |
| 1 | [Customer 1, [[email@domain.com](mailto:email@domain.com)]] |
| 2 | [Customer 2, [[email2@domain.com](mailto:email2@domain.com)]] |

Expand

Show lessSee more

##### Snowflake

Copy code

```
!!!RESOLVE EWI!!! /*** SSC-EWI-0056 - CUSTOM TYPES ARE NOT SUPPORTED IN SNOWFLAKE BUT REFERENCES TO THIS CUSTOM TYPE WERE CHANGED TO VARIANT ***/!!!
CREATE TYPE email_typ_demo AS OBJECT (email VARCHAR2(20))
;

!!!RESOLVE EWI!!! /*** SSC-EWI-0056 - CUSTOM TYPES ARE NOT SUPPORTED IN SNOWFLAKE BUT REFERENCES TO THIS CUSTOM TYPE WERE CHANGED TO VARIANT ***/!!!

CREATE TYPE customer_typ_demo AS OBJECT (
    cust_name VARCHAR2(20),
    cust_email email_typ_demo
)
;

CREATE OR REPLACE TABLE customer_table_demo (
    customer_id INTEGER,
    customer_data VARIANT !!!RESOLVE EWI!!! /*** SSC-EWI-0062 - CUSTOM TYPE 'customer_typ_demo' USAGE CHANGED TO VARIANT ***/!!!
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}}'
;

CREATE OR REPLACE VIEW PUBLIC.customer_table_demo_view
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "" }}'
AS
SELECT
    customer_id,
    customer_data:cust_name :: VARCHAR AS cust_name,
    customer_data:cust_email:email :: VARCHAR AS email
FROM
    customer_table_demo;

SELECT * FROM
    customer_table_demo_view;
```

##### Results

| CUSTOMER\_ID | CUST\_NAME | CUST\_EMAIL |
| --- | --- | --- |
| 1 | Customer 1 | [email@domain.com](mailto:email@domain.com) |
| 2 | Customer 2 | [email2@domain.com](mailto:email2@domain.com) |

Expand

Show lessSee more

### Known Issues

#### 1. Migrated code output is not the same

The view statement is being changed unnecessarily, which makes the table no longer have the same behavior in the output code. There is a work item to fix this issue.

##### 2. DML for User-defined Types — partial support

Constructor calls to **object types** (for example `address_type('123 Main St', …)`) and to **collection types** (`VARRAY` and nested-table) are now translated automatically when they appear in `INSERT … VALUES`, `INSERT … SELECT`, `UPDATE … SET`, and top-level `SELECT` expressions, as well as in PL/SQL variable initialization. See [Object Type constructor calls](#object-type-constructor-calls) above. Other DML shapes that depend on object-type member functions or implicit type promotion may still require manual review.

##### 3. Create Type creation options are not supported

Currently, there is no known workaround for any of the creation options, for these reasons they are not taken into account when defining the type.

### Related EWIs

1. [SSC-EWI-0056](../../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0056): Create Type Not Supported.
2. [SSC-EWI-0062](../../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0062): Custom type usage changed to variant.
3. [SSC-EWI-0073](../../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0073): Pending Functional Equivalence Review.

## Subtype Definition

This is a translation reference to convert the Subtype Variant of the Oracle Create Type Statements (UDTs) to Snowflake

Danger

Since there are no known workarounds, these definitions are only recognized and no translation is supported for them.

### Description

Subtypes define a structure of data similar to a record, with the added advantages of the member function definitions. Meaning that their data may be used along some behavior within the type. Unlike Object Types, Subtypes are built as an extension to another existing type.

Regarding subtype definitions, there is still no translation, but there might be a way to reimplement them using [Object Type Definitions](#object-type-definition) and then using their respective translation.

Copy code

```
CREATE TYPE <type name> UNDER <super type name>
( [{<type column definition> | type method definition } , ...]);
```

### Sample Source Patterns

#### Subtypes under an Object Type

##### Oracle

Copy code

```
CREATE TYPE person_t AS OBJECT (name VARCHAR2(100), ssn INTEGER) 
   NOT FINAL;
/

CREATE TYPE employee_t UNDER person_t 
   (department_id INTEGER, salary INTEGER) 
   NOT FINAL;
/

CREATE TYPE part_time_emp_t UNDER employee_t (num_hrs INTEGER);
/
```

##### Snowflake

Copy code

```
!!!RESOLVE EWI!!! /*** SSC-EWI-0056 - CUSTOM TYPES ARE NOT SUPPORTED IN SNOWFLAKE BUT REFERENCES TO THIS CUSTOM TYPE WERE CHANGED TO VARIANT ***/!!!
CREATE TYPE person_t AS OBJECT (name VARCHAR2(100), ssn INTEGER)
   NOT FINAL;

--!!!RESOLVE EWI!!! /*** SSC-EWI-OR0007 - CREATE TYPE SUBTYPE IS NOT SUPPORTED IN SNOWFLAKE ***/!!!

--CREATE TYPE employee_t UNDER person_t
--   (department_id INTEGER, salary INTEGER)
--   NOT FINAL
            ;

--!!!RESOLVE EWI!!! /*** SSC-EWI-OR0007 - CREATE TYPE SUBTYPE IS NOT SUPPORTED IN SNOWFLAKE ***/!!!

--CREATE TYPE part_time_emp_t UNDER employee_t (num_hrs INTEGER)
                                                              ;
```

### Known Issues

#### 1. Create Type creation options are not supported

Currently, there is no known workaround for any of the creation options, for these reasons they are not taken into account when defining the type.

### Related EWIs

1. [SSC-EWI-0056](../../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0056): Create Type Not Supported.
2. [SSC-EWI-OR0007](../../../issues-and-troubleshooting/conversion-issues/oracleEWI#ssc-ewi-or0007): Create Type Not Supported in Snowflake.
