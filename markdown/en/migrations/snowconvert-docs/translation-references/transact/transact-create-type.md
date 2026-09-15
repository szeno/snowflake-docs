# SQL Server-Azure Synapse - CREATE TYPE

SQL Server alias types (`CREATE TYPE ... FROM base_type`) are mapped to Snowflake `CREATE TYPE ... AS base_type`. Table types and other unsupported variants are flagged for manual review.

Applies to

- SQL Server
- Azure Synapse Analytics

## Alias types (`FROM` base type)

`FROM` is rewritten to `AS`, nullable/nullability modifiers on the alias definition are dropped in the Snowflake output, and schema-qualified names are preserved.

**Source (T-SQL):**

Copy code

```
CREATE TYPE EmailAddress FROM VARCHAR(255);
```

**Snowflake equivalent:**

Copy code

```
CREATE TYPE EmailAddress AS VARCHAR(255);
```

**Source (T-SQL):**

Copy code

```
CREATE TYPE EmailAddress FROM VARCHAR(255) NOT NULL;
```

**Snowflake equivalent:**

Copy code

```
CREATE TYPE EmailAddress AS VARCHAR(255);
```

**Source (T-SQL):**

Copy code

```
CREATE TYPE dbo.PhoneNumber FROM VARCHAR(20) NOT NULL;
```

**Snowflake equivalent:**

Copy code

```
CREATE TYPE dbo.PhoneNumber AS VARCHAR(20);
```

**Source (T-SQL):**

Copy code

```
CREATE TYPE Currency FROM DECIMAL(15,2);
```

**Snowflake equivalent:**

Copy code

```
CREATE TYPE Currency AS DECIMAL(15, 2);
```

## Table types (`AS TABLE`)

`CREATE TYPE ... AS TABLE (...)` is not supported as a Snowflake user-defined type in this form; the converter emits an EWI and leaves the statement for manual resolution.

**Source (T-SQL):**

Copy code

```
CREATE TYPE dbo.MyTableType AS TABLE (Id INT, Name VARCHAR(100));
```

**Snowflake equivalent (with EWI):**

Copy code

```
!!!RESOLVE EWI!!! /*** SSC-EWI-TS0107 - CREATE TYPE AS TABLE IS NOT SUPPORTED IN SNOWFLAKE ***/!!!
CREATE TYPE dbo.MyTableType AS TABLE (
  Id INT,
  Name VARCHAR(100)
);
```

**Notes:** See [SSC-EWI-TS0107](../../issues-and-troubleshooting/conversion-issues/sqlServerEWI#ssc-ewi-ts0107) in the SQL Server conversion issues documentation.
