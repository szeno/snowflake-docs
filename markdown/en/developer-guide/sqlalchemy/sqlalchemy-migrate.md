# Migrating Snowflake SQLAlchemy from 1.x to 2.x

This guide helps you upgrade the Snowflake SQLAlchemy dialect (`snowflake-sqlalchemy`) from any 1.x release to 2.x (2.0.0 and 2.1). Most changes apply the same way whichever 1.x release you start from. The few that landed partway through 1.x name the release that introduced them, so check those against your current version. Changes that apply only from 2.1 are marked **(2.1)**.

Note

This isn’t the same as upgrading SQLAlchemy itself. `snowflake-sqlalchemy` 2.x *requires* SQLAlchemy 2.0. If your application still runs on SQLAlchemy 1.4, migrate the application to SQLAlchemy 2.0 first using [SQLAlchemy’s 1.4 to 2.0 migration guide](https://docs.sqlalchemy.org/en/20/changelog/migration_20.html), then upgrade this dialect. Behavior changes that come from SQLAlchemy Core and ORM (for example, `Result` rows, `text()` requirements, and the removal of `Engine` autocommit) are covered there and not repeated here.

## At a glance

| Area | 1.x (latest 1.11.1) | 2.0.0 | 2.1 |
| --- | --- | --- | --- |
| SQLAlchemy | `>=1.4.19` (1.4 and 2.0 both supported) | `>=2.0.44,<2.1` (2.0 only) | `>=2.0.44,<2.2` (2.0 and 2.1) |
| Python | `>=3.8` | `>=3.11` (3.11 through 3.14) | `>=3.11` (3.11 through 3.14) |
| `snowflake-connector-python` | `<5.0.0` | `>=5.0.0` (5.x required) | `>=5.1.0,<6.0` |
| Async (`asyncio`) | Not supported | Supported (requires `greenlet`) | Supported (install the `[async]` extra) |

Expand

Show lessSee more

For most projects, the required actions are moving to SQLAlchemy 2.0.44 or later, Python 3.11 or later, and connector 5.x (5.1.0 or later for 2.1). In addition, the new `enable_structured_type_json` flag is on by default, and the `force_div_is_floordiv` and `legacy_url_params` options were removed.

## Am I affected?

| Your current setup | What you need to do |
| --- | --- |
| Already on SQLAlchemy 2.0 and Python 3.11 or later | Drop-in upgrade. Then skim [behavioral differences](#label-behavioral-differences-to-review). |
| On SQLAlchemy 1.4 | Migrate the app to SQLAlchemy 2.0 first, then upgrade. Until then, pin `snowflake-sqlalchemy<2.0.0`. |
| On SQLAlchemy 2.1 | Use Snowflake SQLAlchemy 2.1. Version 2.0.0 fails at `import snowflake.sqlalchemy` on SQLAlchemy 2.1. |
| Hand-write connection URLs whose database or schema contains `+`, `%2F`, or a quoted `/` | **(2.1)** Path decoding changed. See [URL database and schema path decoding](#label-sqlalchemy-migrate-url-path-decoding). |
| Use async engines | **(2.1)** Install `snowflake-sqlalchemy[async]`. See [Async requires the async extra](#label-sqlalchemy-migrate-async-extra). |
| On Python 3.10 or older | Upgrade the interpreter to 3.11 through 3.14 first. |
| On `snowflake-connector-python` 4.x or older | Upgrade to connector 5.x. |
| Import `snowflake.sqlalchemy.compat` anywhere | Remove that import. The module was deleted. |
| Pass `legacy_url_params=` or set `SNOWFLAKE_SQLALCHEMY_LEGACY_URL_PARAMS` | Remove it. Move blocked connector arguments to `connect_args=`. |
| Pass `force_div_is_floordiv=` | Remove it. |
| Use `//` on integer columns, coming from a release older than 1.11.1 | Results change: `//` now floors. See [force\_div\_is\_floordiv removed](#label-sqlalchemy-migrate-force-div-removed). |
| Pass sensitive connector parameters in the URL, coming from a release older than 1.11.0 | Move them to `connect_args=`. See [legacy\_url\_params removed](#label-sqlalchemy-migrate-legacy-url-params). |
| Use `regexp_match(...)` or `regexp_replace(...)` with `flags=`, coming from a release older than 1.10.1 | Review generated SQL. See [regexp flags](#label-sqlalchemy-migrate-regexp-flags). |
| Read semi-structured `VARIANT`, `OBJECT`, or `ARRAY` values with `json.loads(...)` | Values now come back as `dict` or `list` by default. |
| Read or write structured `MAP`, `ARRAY(<type>)`, or `OBJECT(...)` columns | These also return and accept `dict` or `list` by default. See [automatic JSON handling](#label-sqlalchemy-migrate-structured-type-json). |
| Write `decimal.Decimal` values into `VARIANT` or other semi-structured columns | Values are now stored as JSON strings. See [Decimal values in semi-structured columns](#label-sqlalchemy-migrate-decimal-variant). |
| Reflect indexes on hybrid tables and look them up by name | Unquoted index names now reflect in lowercase. |

Expand

Show lessSee more

## Step-by-step upgrade

1. Make sure your application runs on **SQLAlchemy 2.0.44 or later** (earlier than 2.1 for 2.0.0, earlier than 2.2 for 2.1). Migrate from 1.4 if needed, using SQLAlchemy’s guide linked above.
2. Make sure you’re on **Python 3.11 through 3.14**.
3. Upgrade the dialect:

   Copy code

   ```
   pip install --upgrade "snowflake-sqlalchemy>=2.0.0,<3"
   ```

   Version 2.1 requires `SQLAlchemy>=2.0.44,<2.2` and `snowflake-connector-python>=5.1.0,<6.0`, so pip upgrades both if needed. If you pin `snowflake-connector-python<5.0.0` yourself, remove that pin. To use async engines, install the `async` extra instead: `pip install --upgrade "snowflake-sqlalchemy[async]>=2.0.0,<3"`.
4. Verify the install:

   Copy code

   ```
   python -c "import snowflake.sqlalchemy; print(snowflake.sqlalchemy.__version__)"
   ```
5. Run your test suite and review the [behavioral differences](#label-behavioral-differences-to-review), especially reflection-dependent code and semi-structured data.

## Behavioral differences to review

The UUID reflection and reflection routing items apply only if you’re coming from SQLAlchemy 1.4; with 1.x on SQLAlchemy 2.0 you already have that behavior. The reflected type `str()` item also applies on SQLAlchemy 2.0 if you’re coming from a release older than 1.10.0. Most of these changes require no code changes, but they change observable behavior. Automatic JSON handling and `Decimal` serialization can silently change the values you read back. Review each item that applies to you.

### UUID columns reflect to a real type (were NullType)

On SQLAlchemy 2.0, Snowflake `UUID` columns reflect to `sqlalchemy.sql.sqltypes.UUID` with `as_uuid=False`, so values come back as plain hyphenated strings. On SQLAlchemy 1.4, the generic `UUID` type didn’t exist and these columns reflected as `NullType`.

Copy code

```
from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import UUID

# Reflected UUID values are strings by default:
#   "6ba7b810-9dad-11d1-80b4-00c04fd430c8"
# Opt into uuid.UUID objects with:
Column("id", UUID(as_uuid=True), primary_key=True)
```

### Native UUID DDL is opt-in (enable\_native\_uuid)

By default, SQLAlchemy’s generic `Uuid` type and `Mapped[uuid.UUID]` still render as `CHAR(32)`. The new `enable_native_uuid` dialect flag renders them as native Snowflake `UUID` instead, binds `uuid.UUID` values for them, and allows `uuid.UUID` values inside semi-structured payloads:

Copy code

```
create_engine(URL(...), enable_native_uuid=True)
# or: create_engine("snowflake://...?enable_native_uuid=true")
```

The flag is off by default because enabling it changes the DDL generated for existing `Uuid` columns. If you use Alembic autogenerate, expect type differences for those columns after you enable it.

### Reflection routing is automatic (bulk vs single-table)

SQLAlchemy 2.0 distinguishes bulk reflection from single-table inspection, and the dialect routes each to the efficient query path automatically:

- `MetaData.reflect()` and `autoload_with=` issue one schema-wide query per metadata type, cached for all tables.
- `inspector.get_columns("t")` issues a single `DESC TABLE` against that table.

Copy code

```
metadata.reflect(bind=engine, schema="public")          # Bulk: schema-wide, cached
inspector.get_columns("my_table", schema="public")      # Single: DESC TABLE
```

For more information, see [Schema reflection](/developer-guide/sqlalchemy/sqlalchemy-reflection).

### Reflected type str() output includes Snowflake default sizes

*On SQLAlchemy 2.0, since 1.10.0.* Because single-table inspection uses `DESC TABLE`, reflected types render Snowflake’s resolved default sizes, for example `VARCHAR(16777216)` instead of `VARCHAR`, and `BINARY(8388608)` instead of `BINARY`. The type objects are functionally identical; only `str()` differs. Compare types with `isinstance()`, not string comparison.

### Hybrid table index names reflect in lowercase

Reflected index names on hybrid tables are normalized like other identifiers: unquoted names (stored in uppercase) reflect in SQLAlchemy’s lowercase convention, and quoted case-sensitive names are preserved. An index with no `INCLUDE` columns now reflects `[]` instead of `['']`. Update code that looks up reflected indexes by uppercase name.

### regexp\_match and regexp\_replace flags render as literals

*Since 1.10.1*, so this is only a change if you’re coming from an older release. Flags passed to `ColumnElement.regexp_match(..., flags=...)` and `regexp_replace(..., flags=...)` render as inline string literals, matching Snowflake’s `REGEXP_LIKE(col, pattern, 'i')` and `REGEXP_REPLACE(col, pattern, repl, 'i')` syntax. Previously they were sent as bound parameters, producing invalid SQL.

### COLLATE renders as a string literal

`Column.collate("<spec>")` and `String(collation="<spec>")` render the collation as a single-quoted string literal, for example `COLLATE 'en-ci'`. Previously the collation rendered as a double-quoted identifier, which Snowflake rejects.

### OFFSET without LIMIT renders LIMIT NULL

A `SELECT` with `.offset()` but no `.limit()` now compiles to `LIMIT NULL OFFSET ...`, as Snowflake requires. Previously the dialect generated invalid `LIMIT -1` SQL.

### Automatic JSON handling is on by default (enable\_structured\_type\_json)

The new `enable_structured_type_json` flag defaults to `True`. It affects semi-structured `VARIANT`, `OBJECT`, and `ARRAY` columns, and structured `MAP(...)`, `ARRAY(<type>)`, and `OBJECT(...)` columns.

What changes by default:

- **Reads** return Python objects (`dict` or `list`) instead of raw JSON strings.
- **Writes** accept `dict` or `list` directly; the dialect wraps them with `PARSE_JSON(...)` automatically. For structured columns it renders `CAST(PARSE_JSON(...) AS <declared type>)`.
- Element values of structured columns aren’t converted to the declared types on read. They come back as JSON decodes them; for example, `MAP(NUMBER, ...)` keys stay strings and `DATE` elements stay ISO strings.

Copy code

```
import json
from sqlalchemy import func

# Reads: raw JSON string in 1.x; already a dict or list in 2.0
payload = json.loads(row.v)   # old: needed json.loads on a JSON string
payload = row.v               # new: row.v is already a dict or list

# Writes: manual wrapping in 1.x; pass the object directly in 2.0
stmt = t.insert().values(v=func.parse_json(json.dumps({"a": 1})))   # old
stmt = t.insert().values(v={"a": 1})                                 # new
```

To restore the old behavior (deprecated; emits a `DeprecationWarning`):

Copy code

```
create_engine(URL(...), enable_structured_type_json=False)
# or: create_engine("snowflake://...?enable_structured_type_json=false")
```

For more information, see [Data type support](/developer-guide/sqlalchemy/sqlalchemy-data-types).

### Decimal values in semi-structured columns are stored as JSON strings

When the dialect serializes a payload for a `VARIANT` or other semi-structured column, it writes `decimal.Decimal` values as JSON strings instead of JSON numbers. This preserves all 38 digits of a `DECFLOAT` value, which a JSON number would truncate.

Reading such a value back as `DECFLOAT` requires an intermediate `::VARCHAR` cast, because Snowflake rejects a direct cast from the `PARSE_JSON` text to `DECFLOAT`:

Copy code

```
SELECT payload:amt::VARCHAR::DECFLOAT FROM t;  -- works
SELECT payload:amt::DECFLOAT FROM t;           -- fails: Cannot cast value of type TEXT ...
```

Review SQL and application code that reads numeric fields written as `Decimal` from semi-structured columns.

### Session keep-alive auto-detection is set explicitly

The dialect sets `enable_server_session_keep_alive_auto_detection=True` on new connections. This pins the connector’s current default, so behavior stays stable if that default changes, and silences the connector’s `FutureWarning` about it. A value that you supply in the URL or in `connect_args` still takes precedence.

### force\_div\_is\_floordiv removed

The `force_div_is_floordiv` option was removed. The `/` and `//` operators always compile to the following SQL:

| Python expression | Generated SQL | Behavior |
| --- | --- | --- |
| `col1 / col2` | `col1 / col2` | True division (Snowflake’s native `/`) |
| `col1 // col2` | `FLOOR(col1 / col2)` | Floor division |

Expand

Show lessSee more

What this means depends on the 1.x release you’re coming from:

- **1.11.1:** No change. It already compiles `/` and `//` this way.
- **Older than 1.11.1, on SQLAlchemy 2.0** (with the default `force_div_is_floordiv=True`): `//` between two integer operands compiled to a plain `col1 / col2`, which Snowflake evaluates as true division. It now compiles to `FLOOR(col1 / col2)`, so integer `//` results change. `/` previously rendered as `col1 / CAST(col2 AS NUMERIC)`; results are the same, and only the SQL text differs.

Passing `force_div_is_floordiv` to `create_engine()` raises `TypeError: Invalid argument(s) 'force_div_is_floordiv' sent to create_engine()`. A `?force_div_is_floordiv=...` URL query parameter isn’t rejected, but has no effect. Remove it from your connection configuration:

Copy code

```
# Before (removed; raises TypeError)
create_engine(URL(...), force_div_is_floordiv=True)

# After
create_engine(URL(...))
```

### URL database and schema path decoding (2.1)

This applies to connection URLs that you write by hand. URLs built with the `snowflake.sqlalchemy.URL` helper connect to the same database and schema as in 2.0.0. Version 2.1 reads the URL path using Snowflake identifier rules, so the same string can now select a different database or schema:

| URL path | 1.x and 2.0.0 | 2.1 |
| --- | --- | --- |
| `a+b/sch` | `a b`, `sch` | `a+b`, `sch` |
| `a%2Fb` | database `a%2Fb` | `a`, `b` |
| `"a/b"/sch` | `ArgumentError` | `"a/b"`, `sch` |

Expand

Show lessSee more

A `+` is no longer read as a space; write a space as `%20`. An encoded `/` (`%2F`) outside double quotes now separates the database from the schema; a `/` inside double quotes is part of the name.

`sqlalchemy.engine.URL.create(...)` values are used as passed on SQLAlchemy 2.1. On SQLAlchemy 2.0, the dialect can’t tell them from a parsed URL string, so a name containing `%` and no raw `"` is still percent-decoded, as in 2.0.0; write a literal `%` as `%25`. See [Special characters in database and schema names](/developer-guide/sqlalchemy/sqlalchemy-connect#label-sqlalchemy-special-chars-db-schema).

### Async requires the async extra (2.1)

Snowflake SQLAlchemy 2.0.0 capped SQLAlchemy below 2.1, where `greenlet` still came by default on common platforms. Version 2.1 allows SQLAlchemy 2.1, which no longer installs `greenlet`, so an upgrade that doesn’t add the `async` extra installs cleanly but fails when you create an async engine. Switch your requirement to `snowflake-sqlalchemy[async]`.

## Breaking changes

### SQLAlchemy 1.4 support dropped

The dialect requires SQLAlchemy `>=2.0.44` (earlier than 2.1 for 2.0.0, earlier than 2.2 for 2.1) and is no longer tested against 1.4. SQLAlchemy 2.1.0 removed internal APIs that version 2.0.0 imports, so `import snowflake.sqlalchemy` fails on SQLAlchemy 2.1 with 2.0.0. Version 2.1 supports both SQLAlchemy 2.0 and 2.1.

Copy code

```
  # requirements.txt
- SQLAlchemy>=1.4.19
- snowflake-sqlalchemy<2.0.0
+ SQLAlchemy>=2.0.44,<2.2
+ snowflake-sqlalchemy>=2.1.0
```

If you can’t move off SQLAlchemy 1.4 yet, pin `snowflake-sqlalchemy<2.0.0`.

### Python 3.8, 3.9, and 3.10 support dropped

The dialect requires Python 3.11 or later, because `snowflake-connector-python` 5.x requires Python 3.11 or later. Upgrade the interpreter to 3.11 through 3.14 before upgrading the dialect.

Copy code

```
  # pyproject.toml
- requires-python = ">=3.8"
+ requires-python = ">=3.11"
```

### Snowflake Connector for Python 5.x required

The dialect requires `snowflake-connector-python>=5.0.0`, which provides the async driver. Connector 4.x is no longer supported. If you pin the connector yourself, remove any `<5.0.0` upper bound, or the resolver can’t satisfy both packages.

Copy code

```
  # requirements.txt
- snowflake-connector-python<5.0.0
+ snowflake-connector-python>=5.0.0
```

### Internal compat module removed

`snowflake.sqlalchemy.compat` was deleted. It was never part of the public API, but if you imported it, remove the import and use SQLAlchemy 2.0 APIs directly.

Copy code

```
- from snowflake.sqlalchemy.compat import IS_VERSION_20
```

### legacy\_url\_params removed

Since 1.11.0, sensitive connector parameters are blocked from the URL query string. Version 1.11.x provided a temporary `legacy_url_params` opt-out that re-enabled passing certain sensitive connector parameters in the URL query string. This shim was removed:

- Passing `legacy_url_params=...` to `create_engine()` raises `TypeError: Invalid argument(s) 'legacy_url_params' sent to create_engine()`. A `?legacy_url_params=...` URL query parameter isn’t rejected, but has no effect.
- `SNOWFLAKE_SQLALCHEMY_LEGACY_URL_PARAMS` has no effect.
- Sensitive connector parameters are always rejected from the URL query string and must be passed with `connect_args=`. In 2.0, `unsafe_skip_config_file_permissions_check` and `crl_unsafe_skip_file_permissions_check` joined the list. If you’re coming from a release older than 1.11.0, all of them are newly blocked. For the full list, see [Connection parameters](/developer-guide/sqlalchemy/sqlalchemy-connect).

Copy code

```
  from sqlalchemy import create_engine

- # Before: worked only under the removed shim
- engine = create_engine(
-     "snowflake://user:pass@account/?protocol=https&token_file_path=/path/to/token",
-     legacy_url_params=True,
- )
+ # After: pass blocked parameters through connect_args=
+ engine = create_engine(
+     "snowflake://user:pass@account/",
+     connect_args={"protocol": "https", "token_file_path": "/path/to/token"},
+ )
```

## New in 2.0

These additions don’t require any migration and are safe to adopt:

- [Async support](/developer-guide/sqlalchemy/sqlalchemy-async) with `create_async_engine()` and `create_snowflake_async_engine()`, using the same `snowflake://` URL as the sync dialect.
- `create_snowflake_engine()` for case-sensitive default schemas.
- `SnowflakeBase`, `SnowflakeSession`, and `snowflake_declarative_base()` for faster ORM bulk inserts with nullable columns.
- `GCSBucket` and `CloudStorageLocation` for `CopyIntoStorage`.
- Secret-redaction helpers: `SnowflakeSecretRedactionFilter`, `add_secret_redaction_filter()`, and `redact_secrets()`.
- Opt-in [strict host-name mode](/developer-guide/sqlalchemy/sqlalchemy-connect#label-sqlalchemy-strict-host-names) (`strict_host_names`) for air-gapped deployments.
- Opt-in native `UUID` DDL with `enable_native_uuid`.
- Multi-table inserts with `InsertMulti`, row access policies on `SnowflakeTable`, `RELY` constraints, and subscript access on semi-structured columns.

## Staying on 1.x

If you can’t upgrade yet, pin the major version:

```
# requirements.txt
snowflake-sqlalchemy<2.0.0
```

## Troubleshooting

| Symptom | Fix |
| --- | --- |
| Resolver installs an old dialect or errors on SQLAlchemy 1.4 | Move the app to SQLAlchemy 2.0, then install `snowflake-sqlalchemy>=2.0.0`. |
| `import snowflake.sqlalchemy` fails with an `ImportError` from `sqlalchemy.orm` | You have Snowflake SQLAlchemy 2.0.0 on SQLAlchemy 2.1. Upgrade Snowflake SQLAlchemy to 2.1, or keep SQLAlchemy in `>=2.0.44,<2.1`. |
| Resolver refuses to install 2.0 on Python 3.10 or older | Upgrade to Python 3.11 through 3.14, then run `pip install "snowflake-sqlalchemy>=2.0.0"`. |
| Resolver can’t satisfy `snowflake-connector-python` | Remove your own `snowflake-connector-python<5.0.0` pin. 2.0 requires connector 5.x. |
| `ImportError: ... snowflake.sqlalchemy.compat` | Remove the import. |
| `TypeError: Invalid argument(s) 'legacy_url_params' sent to create_engine()` | Remove `legacy_url_params=` and pass blocked connector arguments with `connect_args=`. |
| `TypeError: Invalid argument(s) 'force_div_is_floordiv' sent to create_engine()` | Remove `force_div_is_floordiv=`. Use `//` where you need floor division. |
| Integer `//` results changed | Expected when coming from a release older than 1.11.1. `//` now floors. |
| `ArgumentError` about a connection parameter that can’t be set via the URL query string | Pass it with `connect_args=`. |
| `REGEXP_*` SQL changed | Expected when coming from a release older than 1.10.1. Update test expectations. |
| `create_async_engine()` raises an `ImportError` about `greenlet` | Run `pip install "snowflake-sqlalchemy[async]"`. |
| A hand-written URL connects to the wrong database or schema after upgrading to 2.1 | See [URL database and schema path decoding](#label-sqlalchemy-migrate-url-path-decoding). |
| Reflected UUID values are strings, not `uuid.UUID` | Expected. Use `UUID(as_uuid=True)`. |
| Type-string comparisons fail after reflection | Use `isinstance()`. |
| Reflected hybrid table index names are lowercase | Expected. Look up unquoted index names in lowercase. |
| `COLLATE` SQL changed | Expected. Update test expectations. |
| Semi-structured reads return `dict` or `list`, or `json.loads(...)` raises `TypeError` | Expected. Drop the manual JSON parsing, or opt out with `enable_structured_type_json=False` (deprecated). |
| Casting a `Decimal` stored in `VARIANT` to `DECFLOAT` fails | Cast through `VARCHAR`: `payload:amt::VARCHAR::DECFLOAT`. |

Expand

Show lessSee more

## Further reading

- [Connection parameters](/developer-guide/sqlalchemy/sqlalchemy-connect)
- [Data type support](/developer-guide/sqlalchemy/sqlalchemy-data-types)
- [Schema reflection](/developer-guide/sqlalchemy/sqlalchemy-reflection)
- [Async support](/developer-guide/sqlalchemy/sqlalchemy-async)
- [Using Alembic](/developer-guide/sqlalchemy/sqlalchemy-alembic)
- [Known limitations](/developer-guide/sqlalchemy/sqlalchemy-limitations)
- [SQLAlchemy’s 1.4 to 2.0 migration guide](https://docs.sqlalchemy.org/en/20/changelog/migration_20.html)
