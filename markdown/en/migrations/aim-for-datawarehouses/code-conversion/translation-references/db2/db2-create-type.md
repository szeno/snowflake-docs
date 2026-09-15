# IBM DB2 - CREATE TYPE

This page describes how Db2 **distinct types** (`CREATE DISTINCT TYPE ... AS type`), structured `CREATE TYPE ... AS (...)` definitions, and **array types** (`CREATE [DISTINCT] TYPE ... AS <type> ARRAY[n]`) are translated. Distinct types map to Snowflake `CREATE TYPE name AS <base_type>`; attribute lists map to `OBJECT(...)`; array types map to `ARRAY ( <type> )`, dropping the fixed cardinality and emitting [SSC-FDM-0043](../../issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0043).

## Distinct types

`CREATE DISTINCT TYPE` becomes `CREATE TYPE`. The `WITH COMPARISONS` clause is not carried forward; base types use the same data-type normalization as the rest of the Db2 migration.

**Source (Db2):**

Copy code

```
CREATE DISTINCT TYPE CURRENCY AS DECIMAL(15,2) WITH COMPARISONS;
```

**Snowflake equivalent:**

Copy code

```
CREATE TYPE CURRENCY AS DECIMAL(15, 2);
```

**Source (Db2):**

Copy code

```
CREATE DISTINCT TYPE EMAIL_ADDR AS VARCHAR(255);
```

**Snowflake equivalent:**

Copy code

```
CREATE TYPE EMAIL_ADDR AS VARCHAR(255);
```

**Source (Db2):**

Copy code

```
CREATE DISTINCT TYPE myschema.PHONE_NUM AS VARCHAR(20) WITH COMPARISONS;
```

**Snowflake equivalent:**

Copy code

```
CREATE TYPE myschema.PHONE_NUM AS VARCHAR(20);
```

## Structured types (attribute list)

Composite-style definitions with `CREATE TYPE name AS (col type, ...)` map to Snowflake `OBJECT(...)`.

**Source (Db2):**

Copy code

```
CREATE TYPE address_t AS (street VARCHAR(100), city VARCHAR(50), state CHAR(2));
```

**Snowflake equivalent:**

Copy code

```
CREATE TYPE address_t AS OBJECT (street VARCHAR(100), city VARCHAR(50), state CHAR(2));
```

**Source (Db2):**

Copy code

```
CREATE TYPE person_t AS (first_name VARCHAR(50), last_name VARCHAR(50), age INTEGER);
```

**Snowflake equivalent:**

Copy code

```
CREATE TYPE person_t AS OBJECT (first_name VARCHAR(50), last_name VARCHAR(50), age INTEGER);
```

## Array types

Db2 array type definitions of the form `<element_type> ARRAY[<size>]` map to Snowflake `ARRAY ( <element_type> )`. Snowflake `ARRAY` is a single, dynamically-sized type, so the fixed cardinality from the source is dropped and [SSC-FDM-0043](../../issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0043) is emitted to flag the behavioral difference. The same translation applies whether the type is defined with `CREATE TYPE` or `CREATE DISTINCT TYPE`, and whether or not a schema qualifier is present. Unbounded `ARRAY[]` is also recognized; in that case no FDM is needed because there is no size limit to drop.

**Source (Db2):**

Copy code

```
CREATE TYPE INT_ARRAY AS INTEGER ARRAY[100];
```

**Snowflake equivalent:**

Copy code

```
--** SSC-FDM-0043 - ARRAY SIZE LIMIT '100' WAS REMOVED. SNOWFLAKE ARRAYS ARE DYNAMICALLY SIZED. **
CREATE TYPE INT_ARRAY AS ARRAY ( INTEGER );
```

**Source (Db2):**

Copy code

```
CREATE TYPE INT_ARRAY AS INTEGER ARRAY[];
```

**Snowflake equivalent:**

Copy code

```
CREATE TYPE INT_ARRAY AS ARRAY ( INTEGER );
```

**Source (Db2):**

Copy code

```
CREATE TYPE myschema.DATE_ARRAY AS DATE ARRAY[365];
```

**Snowflake equivalent:**

Copy code

```
--** SSC-FDM-0043 - ARRAY SIZE LIMIT '365' WAS REMOVED. SNOWFLAKE ARRAYS ARE DYNAMICALLY SIZED. **
CREATE TYPE myschema.DATE_ARRAY AS ARRAY ( DATE );
```

**Source (Db2):**

Copy code

```
CREATE DISTINCT TYPE STR_ARRAY AS VARCHAR(50) ARRAY[200];
```

**Snowflake equivalent:**

Copy code

```
--** SSC-FDM-0043 - ARRAY SIZE LIMIT '200' WAS REMOVED. SNOWFLAKE ARRAYS ARE DYNAMICALLY SIZED. **
CREATE TYPE STR_ARRAY AS ARRAY ( VARCHAR(50) );
```

Note: `CREATE DISTINCT TYPE` is normalized to `CREATE TYPE` in the Snowflake output (the `DISTINCT` keyword has no equivalent in Snowflake’s type system).

**Notes:** If application logic depends on a maximum array length, enforce it outside the type definition (for example with check constraints or in application code). Snowflake will not raise an error on values that exceed the original cardinality. See IBM’s reference for [`CREATE TYPE` (array)](https://www.ibm.com/docs/en/db2/11.5?topic=statements-create-type-array).

## Related issues

- [SSC-FDM-0043](../../issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0043) — Array size limit removed.

**Notes:** Unsupported or highly Db2-specific type features may still emit EWIs/FDMs. For structured types, IBM also documents [`CREATE TYPE` (structured)](https://www.ibm.com/docs/en/db2/11.5?topic=statements-create-type-structured).
