# Teradata - CREATE TYPE

Teradata structured types in `SYSUDTLIB` (and similar) are translated when the definition includes a `CAST FROM` clause that allows reduction to a single Snowflake scalar type, or when the body is a simple attribute list without such a cast mapping to an alias. For background, see Teradata’s UDT documentation and [Snowflake `CREATE TYPE`](https://docs.snowflake.com/en/sql-reference/sql/create-type).

## Types with `CAST FROM` (scalar alias)

When Teradata defines a UDT with one attribute and a `CAST FROM` clause pointing at a built-in type, a Snowflake `CREATE TYPE ... AS <scalar>` alias can be emitted.

**Source (Teradata):**

Copy code

```
CREATE TYPE SYSUDTLIB.MyUDT AS (value INTEGER) INSTANTIABLE NOT FINAL CAST FROM INTEGER;
```

**Snowflake equivalent:**

Copy code

```
CREATE TYPE SYSUDTLIB.MyUDT AS INTEGER;
```

**Source (Teradata):**

Copy code

```
CREATE TYPE SYSUDTLIB.EmailAddr AS (val VARCHAR(255)) INSTANTIABLE NOT FINAL CAST FROM VARCHAR(255);
```

**Snowflake equivalent:**

Copy code

```
CREATE TYPE SYSUDTLIB.EmailAddr AS VARCHAR(255);
```

**Source (Teradata):**

Copy code

```
CREATE TYPE SYSUDTLIB.Currency AS (val DECIMAL(15,2)) INSTANTIABLE NOT FINAL CAST FROM DECIMAL(15,2);
```

**Snowflake equivalent:**

Copy code

```
CREATE TYPE SYSUDTLIB.Currency AS DECIMAL(15, 2);
```

## Composite type without scalar `CAST FROM`

Multi-attribute definitions without the scalar-alias pattern map to Snowflake `OBJECT(...)`.

**Source (Teradata):**

Copy code

```
CREATE TYPE SYSUDTLIB.Person AS (FirstName VARCHAR(50), LastName VARCHAR(50), Age INTEGER) INSTANTIABLE NOT FINAL;
```

**Snowflake equivalent:**

Copy code

```
CREATE TYPE SYSUDTLIB.Person AS OBJECT (FirstName VARCHAR(50), LastName VARCHAR(50), Age INTEGER);
```

**Notes:** Teradata-specific clauses such as `INSTANTIABLE` / `NOT FINAL` are not represented in Snowflake `CREATE TYPE`; the translation focuses on the usable Snowflake type shape.
