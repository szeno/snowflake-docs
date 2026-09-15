[![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.
Currently, this feature is only available on Amazon Web Services (AWS) and Microsoft Azure.

# Type mapping reference

This page covers how identifiers are converted from PostgreSQL to Snowflake on mirror targets, and
how PostgreSQL data types map to Iceberg.

## Name mapping

Schema, table, and column names from the source PostgreSQL database are converted to uppercase in
the target database. For example, the PostgreSQL column `created_at` is written as `CREATED_AT` in
the target table. Replicating Postgres tables with the same name in different case isn’t supported.

## Type mapping

PostgreSQL types are classified as either **supported** or **unsupported**. Supported types are
replicated directly (native) or cast to text/binary. Unsupported types are blocked when you add a
table to the publication.

### Native types

These types have direct Iceberg equivalents and are replicated without conversion:

| PostgreSQL type | Iceberg type | Notes |
| --- | --- | --- |
| `boolean` | `boolean` |  |
| `smallint` / `int2` | `int` |  |
| `integer` / `int4` | `int` |  |
| `bigint` / `int8` | `long` |  |
| `real` / `float4` | `float` |  |
| `double precision` / `float8` | `double` |  |
| `numeric(p,s)` where p ≤ 38, s ≤ 38 | `decimal(p,s)` |  |
| `numeric` (unbounded) | `double` | Values exceeding the `float8` range overflow to +/-Infinity |
| `numeric(p,s)` where p > 38 or s > 38 | `double` | Values exceeding the `float8` range overflow to +/-Infinity |
| `date` | `date` |  |
| `time` (without time zone) | `time` |  |
| `time with time zone` / `timetz` | `time` | UTC-normalized |
| `timestamp` (without time zone) | `timestamp` |  |
| `timestamp with time zone` | `timestamptz` |  |
| `interval` | `struct` | Stored as struct with months, days, microseconds |
| `text` | `string` |  |
| `varchar(n)` | `string` |  |
| `char(n)` / `bpchar` | `string` |  |
| `bytea` | `binary` |  |
| `uuid` | `uuid` |  |
| Arrays of native types | `list<T>` | For example, `int[]` becomes `list<int>`. Multidimensional values are clamped to NULL. |
| Composite types (all native fields) | `struct<...>` | All fields must be native types |

Expand

Show lessSee more

### Fallback types

Types not listed above are cast to `string` or `binary` when written to Iceberg. This includes
types like `json`, `jsonb`, `hstore`, and `vector`.

Some fallback types have restrictions:

| PostgreSQL type | Iceberg type | Notes |
| --- | --- | --- |
| `geometry` | `binary` | WKB encoding. Top-level only. Requires `pg_lake_spatial` extension. |
| `int4range`, `int8range`, and other range types | `string` | Top-level only |
| `int4multirange` and other multirange types | `string` | Top-level only |

Expand

Show lessSee more

PostGIS `geometry` values are stored as WKB in a `BINARY` column rather than a Snowflake
`GEOMETRY`. Cast at query time with `TO_GEOMETRY` if you need Snowflake geospatial functions.

### Unsupported types

These types are blocked when you add a table to the publication:

| PostgreSQL type | Reason | Workaround |
| --- | --- | --- |
| `map` types (`pg_map`) | Not supported in CDC | Use JSONB for key-value data |
| Table types (non-composite) | Not valid for Iceberg columns | None |
| Nested geometry (`geometry[]`, geometry in composites) | Not supported in Iceberg | Use top-level geometry only |
| Geometry without `pg_lake_spatial` | CDC worker needs spatial support | `CREATE EXTENSION pg_lake_spatial CASCADE` |
| Nested range/multirange types | Not supported in Iceberg | Use top-level range types only |

Expand

Show lessSee more

Domains are transparently resolved to their base types. A domain over an unsupported type is also
blocked.

### Nested type handling

Arrays and composite types have special rules depending on their element or field types:

**Arrays:**

| Element type | Supported |
| --- | --- |
| Supported type | Yes |
| Unsupported type | No (blocked) |
| Geometry | No (blocked) |
| Range/multirange | No (blocked) |
| `uuid` | No (blocked) |

Expand

Show lessSee more

**Composite types:**

| Field types | Supported |
| --- | --- |
| All fields supported | Yes |
| Any field unsupported | No (blocked) |
| Contains geometry field | No (blocked) |
| Contains range field | No (blocked) |
| Contains `uuid` field | No (blocked) |

Expand

Show lessSee more

`uuid` is an exception to the “supported type → yes” rule: it’s supported as a standalone
column but is blocked when nested inside an array or composite type. Tables with nested UUID
columns are rejected at publication time.

### Value clamping

Even for supported types, certain special values can’t be represented in Iceberg. These values are
silently clamped at write time.

**Temporal values (date, timestamp, timestamptz):**

Infinity and out-of-range temporal values are clamped to the nearest Iceberg boundary:

| PostgreSQL value | Clamped value |
| --- | --- |
| `date 'infinity'` | `9999-12-31` |
| `date '-infinity'` | `4713-01-01 BC` |
| `timestamp 'infinity'` | `9999-12-31 23:59:59.999999` |
| `timestamp '-infinity'` | `0001-01-01 00:00:00` |
| `timestamptz 'infinity'` | `9999-12-31 23:59:59.999999 UTC` |
| `timestamptz '-infinity'` | `0001-01-01 00:00:00 UTC` |

Expand

Show lessSee more

**Numeric NaN:**

`NaN` in bounded `numeric` columns (for example, `numeric(20,5)`) is clamped to `NULL` because
Iceberg’s decimal type doesn’t support NaN.

**Numeric Infinity (unbounded):**

Unbounded `numeric` and `numeric(p,s)` with p > 38 or s > 38 are converted to `double precision`.
IEEE 754 `Infinity` and `-Infinity` are valid double values and are preserved (not clamped).

**Multidimensional arrays:**

PostgreSQL allows multidimensional array values (for example, `ARRAY[[1,2],[3,4]]`), but Iceberg’s
`list` type is single-dimensional. Multidimensional array values are clamped to NULL at write time.
A column declared as `int[]` that contains a 1D value (for example, `ARRAY[1,2,3]`) is stored
normally; only values with more than one dimension are nullified.

**Oversize string and binary values:**

Snowflake imposes maximum sizes on string and binary columns (16 MiB for strings, 8 MiB for binary).
Values that exceed these limits are clamped at write time. The cap is inclusive: a value at exactly
the limit is stored verbatim; only values that exceed it are clamped.

| PostgreSQL type | Action when over the cap |
| --- | --- |
| `text`, `varchar`, `bpchar` | Truncated at a UTF-8 character boundary to the 16 MiB (16,777,216-byte) cap. A multibyte character is never split, so the result may land a byte or two under the cap. |
| `bytea` | Byte-truncated to the 8 MiB (8,388,608-byte) cap. |
| `jsonb`, `json` | Set to `NULL`. Truncating the serialized text would produce invalid JSON. |
| `hstore`, `citext`, and other string-backed types | Set to `NULL`. There is no safe truncation point for these types. |
| String or binary leaf inside an `array` or composite | Clamped per-leaf to the 16 MiB or 8 MiB cap, same as a top-level column. |
| `array` or composite (aggregate) | Set to `NULL` when the entire serialized container exceeds 128 MiB, independent of the per-leaf cap above. |

Expand

Show lessSee more
