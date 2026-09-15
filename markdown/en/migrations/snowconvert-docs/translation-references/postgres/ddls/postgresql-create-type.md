# PostgreSQL / Greenplum / Netezza - CREATE TYPE

This page describes how source `CREATE TYPE` statements are translated for PostgreSQL-family dialects to Snowflake **[native user-defined types](https://docs.snowflake.com/en/sql-reference/sql/create-type)** where supported.

## PostgreSQL

PostgreSQL composite types declared with `CREATE TYPE name AS (...)` are translated to Snowflake `CREATE TYPE ... AS OBJECT (...)`. Other variants (for example `ENUM`, `RANGE`, `CREATE TYPE ... AS BASE`) follow separate rules or default handling and may emit conversion issues.

### Composite types

**Source (PostgreSQL):**

Copy code

```
CREATE TYPE address AS (street VARCHAR(200), city VARCHAR(100), zipcode VARCHAR(10));
```

**Snowflake equivalent:**

Copy code

```
CREATE TYPE address AS OBJECT (street VARCHAR(200), city VARCHAR(100), zipcode VARCHAR(10));
```

#### With schema

**Source (PostgreSQL):**

Copy code

```
CREATE TYPE myschema.person AS (first_name VARCHAR(50), last_name VARCHAR(50), age INTEGER);
```

**Snowflake equivalent:**

Copy code

```
CREATE TYPE myschema.person AS OBJECT (first_name VARCHAR(50), last_name VARCHAR(50), age INTEGER);
```

#### Single attribute

**Source (PostgreSQL):**

Copy code

```
CREATE TYPE wrapper AS (value INTEGER);
```

**Snowflake equivalent:**

Copy code

```
CREATE TYPE wrapper AS OBJECT (value INTEGER);
```

**Notes:** Non-composite `CREATE TYPE` forms are not covered in full on this page; consult EWIs/FDMs and the issue catalogs for enumerations and other definitions.

## Greenplum

Greenplum inherits PostgreSQL-style composite types. `CREATE TYPE name AS (...)` is mapped to Snowflake `CREATE TYPE ... AS OBJECT (...)`, consistent with the PostgreSQL translation path.

**Source (Greenplum):**

Copy code

```
CREATE TYPE address AS (street VARCHAR(200), city VARCHAR(100), zipcode VARCHAR(10));
```

**Snowflake equivalent:**

Copy code

```
CREATE TYPE address AS OBJECT (street VARCHAR(200), city VARCHAR(100), zipcode VARCHAR(10));
```

**Notes:** For additional `CREATE TYPE` variants (for example `ENUM`), see PostgreSQL-oriented rules and issue catalogs; Greenplum shares the same replacer family as PostgreSQL for supported composite patterns.

## Netezza

Netezza SQL uses the same shared ANSI-style `CREATE TYPE` transformation pipeline as Db2 for the patterns below (scalar alias and attribute-list composite types).

### Type alias (`CREATE TYPE ... AS` scalar)

When the parser produces a predefined (scalar) body, Snowflake receives a normalized `CREATE TYPE name AS <datatype>`.

**Illustrative source (Netezza-style alias):**

Copy code

```
CREATE TYPE email_addr AS VARCHAR(255);
```

**Snowflake equivalent:**

Copy code

```
CREATE TYPE email_addr AS VARCHAR(255);
```

### Structured type (attribute list)

`CREATE TYPE name AS (attr type, ...)` maps to Snowflake `OBJECT(...)`.

**Illustrative source:**

Copy code

```
CREATE TYPE address_t AS (street VARCHAR(100), city VARCHAR(50), state CHAR(2));
```

**Snowflake equivalent:**

Copy code

```
CREATE TYPE address_t AS OBJECT (street VARCHAR(100), city VARCHAR(50), state CHAR(2));
```

**Notes:** Db2 **`CREATE DISTINCT TYPE`** is not a Netezza construct; for IBM Db2 distinct types, see [CREATE TYPE (IBM DB2)](../../db2/db2-create-type). Oracle and other dialects have separate translation references.
