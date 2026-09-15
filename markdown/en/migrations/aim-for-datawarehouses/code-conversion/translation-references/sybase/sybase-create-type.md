# Sybase IQ - CREATE TYPE

Sybase alias types use the same pattern as SQL Server: `CREATE TYPE ... FROM base_type` becomes Snowflake `CREATE TYPE ... AS base_type`, with nullability keywords on the source definition removed in the output.

**Source (Sybase):**

Copy code

```
CREATE TYPE EmailAddress FROM VARCHAR(255);
```

**Snowflake equivalent:**

Copy code

```
CREATE TYPE EmailAddress AS VARCHAR(255);
```

**Source (Sybase):**

Copy code

```
CREATE TYPE PhoneNumber FROM VARCHAR(20) NOT NULL;
```

**Snowflake equivalent:**

Copy code

```
CREATE TYPE PhoneNumber AS VARCHAR(20);
```

**Notes:** For table types and other Transact-SQL constructs not covered here, see [CREATE TYPE (SQL Server / Azure Synapse)](../transact/transact-create-type); alias-type behavior is shared between Transact-SQL and Sybase.
