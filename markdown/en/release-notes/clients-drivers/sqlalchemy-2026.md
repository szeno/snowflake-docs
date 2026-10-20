# SQLAlchemy release notes for 2026

This article contains the release notes for the SQLAlchemy, including the following when applicable:

- Behavior changes
- New features
- Customer-facing bug fixes

Snowflake uses semantic versioning for SQLAlchemy updates.

See [Snowflake SQLAlchemy](/developer-guide/sqlalchemy/sqlalchemy) for documentation.

## Version 2.0.0 (October 19, 2026)

This is a major release. To upgrade from 1.x, see [Migrating Snowflake SQLAlchemy from 1.x to 2.x](/developer-guide/sqlalchemy/sqlalchemy-migrate).

### Behavior changes

- Dropped support for SQLAlchemy 1.4. The dialect now requires `SQLAlchemy>=2.0.44,<2.1`; SQLAlchemy 2.1.0 removed APIs that the dialect imports at module load time. Removed the internal `snowflake.sqlalchemy.compat` module. If you’re still on SQLAlchemy 1.4, pin `snowflake-sqlalchemy<2.0.0`.
- Now requires `snowflake-connector-python>=5.0.0`, which provides the async driver. Connector 4.x is no longer supported.
- Supported Python versions are now 3.11 through 3.14 (dropped 3.8, 3.9, and 3.10), because connector 5.x requires Python 3.11 or later.
- `enable_structured_type_json` is on by default. Setting it to `False` restores raw JSON strings and emits a `DeprecationWarning`.
- Removed the `force_div_is_floordiv` dialect option. The `/` operator always performs true division and `//` always performs floor division (`FLOOR(left / right)`). Passing the option to `create_engine()` raises `TypeError`. If you’re coming from a release older than 1.11.1, integer `//` previously compiled to plain `/` (true division in Snowflake) under the default option value; it now floors.
- Removed the `legacy_url_params` opt-out and the `SNOWFLAKE_SQLALCHEMY_LEGACY_URL_PARAMS` environment variable. Passing `legacy_url_params` to `create_engine()` raises `TypeError`, and the environment variable has no effect. Pass sensitive connection parameters through `connect_args=`. `unsafe_skip_config_file_permissions_check` and `crl_unsafe_skip_file_permissions_check` are now also blocked from the URL query string.

### New features and updates

- Added [async support](/developer-guide/sqlalchemy/sqlalchemy-async): use `create_async_engine()` or `create_snowflake_async_engine()` with the same `snowflake://` URL as the sync dialect to get an `AsyncEngine` and `AsyncSession`. The async dialect checks for `greenlet` when the engine is created and raises an `ImportError` with install instructions if it’s missing.
- Added the `enable_structured_type_json` dialect option (on by default). For semi-structured `VARIANT`, `OBJECT`, and `ARRAY` columns and for structured `MAP`, `ARRAY(<type>)`, and `OBJECT(...)` columns, reads return `dict` or `list` values, and writes accept `dict` or `list` values, which the dialect wraps in `PARSE_JSON()` (cast to the declared type for structured columns). The engine’s `json_serializer` and `json_deserializer` are used when provided.
- Added support for UUID and DECFLOAT values inside `VARIANT` and structured types. `decimal.Decimal` values in semi-structured payloads are serialized as JSON strings to preserve all 38 `DECFLOAT` digits.
- Added the opt-in `enable_native_uuid` dialect option, which renders SQLAlchemy’s generic `Uuid` type and `Mapped[uuid.UUID]` as native Snowflake `UUID` instead of `CHAR(32)`, binds `uuid.UUID` values, and honors `as_uuid` on reads.
- Added opt-in [strict host-name mode](/developer-guide/sqlalchemy/sqlalchemy-connect#label-sqlalchemy-strict-host-names) (`strict_host_names` or `SNOWFLAKE_SQLALCHEMY_STRICT_HOST_NAMES`), which stops the dialect from inferring or appending domains to host names and forwards connection parameters, including `connection_name` profiles, to the connector unvalidated.
- Added `COLLATE` support: `Column.collate()` and `String(collation=...)` render the collation as a single-quoted string literal.
- Added subscript access (`col["key"]`, `col[0]`) for `VARIANT`, `OBJECT`, `ARRAY`, and `MAP` columns.
- Added the `InsertMulti` construct for multi-table `INSERT ALL` and `INSERT FIRST` statements.
- Added row access policy support on `SnowflakeTable` through the `row_access_policy` parameter.
- Added opt-in `snowflake_rely=True` to render `RELY` on `PRIMARY KEY`, `FOREIGN KEY`, and `UNIQUE` constraints.
- Added support for the `json_serializer` and `json_deserializer` parameters in `create_engine()`.
- Added the `asdecimal` parameter on `_CUSTOM_DECIMAL` to opt into float results instead of `Decimal`.
- Added a `python_type` property to Snowflake custom types.
- Added the full Snowflake `TYPE=JSON` option set to `JSONFormatter`, and `if_not_exists` and `comment` options to `CreateFileFormat`.
- The dialect now sets `enable_server_session_keep_alive_auto_detection=True` explicitly on new connections, which pins the connector’s current default and silences its `FutureWarning`. A value supplied in the URL or `connect_args` takes precedence.

### Bug fixes

- Improved stage reference handling in compiled `COPY INTO` and staged-file SQL so that `ExternalStage` paths, including sub-paths created with `from_parent_stage`, are escaped when quoting is required.
- Fixed a `NULL_IF` backslash breakout in `COPY` `FILE_FORMAT` options.
- Fixed `repr()` of `CopyIntoStorage` unloading into an `ExternalStage` or a cloud location, which raised `UnsupportedCompilationError`.
- Fixed hybrid table index reflection: reflected index names are normalized to SQLAlchemy’s lowercase convention for unquoted identifiers, `get_multi_indexes()` keys preserve the caller’s schema, and empty `INCLUDE` columns reflect as `[]`.
- Fixed `get_multi_indexes()` raising `TypeError` when `filter_names` is `None` and the schema contains hybrid tables.
- Fixed reflection failing on schemas or databases with more than 10,000 objects by paginating the underlying `SHOW` commands.
- Fixed PrivateLink and regional account parsing for org-style account names that contain dashes.
- Fixed `URL` failing to encode `[`, `]`, `?`, and `#` in passwords.
- Fixed invalid `LIMIT -1` SQL for a `SELECT` with `OFFSET` but no `LIMIT`; the dialect now emits `LIMIT NULL OFFSET ...`.
- Expired-session, expired-token (including error code `390195`), and closed-connection errors are now detected as disconnects, so pooled connections are invalidated and recycled.

## Version 1.11.0 (July 8, 2026)

### New features and updates

- Restricted a set of sensitive connection parameters from being supplied via the URL query string. The following parameters must now be passed via `connect_args=` in `create_engine()` instead: `host`, `protocol`, `token_file_path`, `private_key_file`, `ocsp_response_cache_filename`, `connection_diag_log_path`, `crl_cache_dir`, `unsafe_file_write`, and `unsafe_skip_file_permissions_check`. Applications already using `connect_args=` are unaffected. To temporarily restore the previous behavior, set the `SNOWFLAKE_SQLALCHEMY_LEGACY_URL_PARAMS=1` environment variable.
- Improved `_url()` helper and `create_connect_args` connection-parameter handling:
  - `account` and `region` values are now validated against an allowlist of DNS-safe characters (alphanumeric, `-`, `.`, `_`) before being interpolated into the connection URL, preventing URL-authority corruption from unexpected characters.
  - `user` values are now percent-encoded before being placed in the URL userinfo component, preserving the original value delivered to the connector while preventing `@`, `?`, and `#` from being misinterpreted as URL delimiters.
- Improved identifier quoting and string-literal escaping for caller-supplied values across the DDL compiler. Column keys in `MERGE INTO` (both the `WHEN NOT MATCHED … INSERT` list and `WHEN MATCHED … SET` targets), stage namespaces/names, `format_name`, and `file_format` are now routed through the identifier preparer. Cloud-storage URIs, `CREDENTIALS`, and `ENCRYPTION` clauses (shared by `COPY INTO` and `CREATE STAGE`) and `FILES=(…)` entries now apply the dialect’s standard literal escaping (`'`→`''`, `\`→`\\`). `CREATE STAGE` builds its SQL from the container’s fields rather than `repr(container)`.
- Improved escaping in `CopyIntoStorage`, `CreateStage`, and `CreateFileFormat`, and added secret redaction:
  - `FILE_FORMAT` option string values (for example, `CSVFormatter().date_format(...)`, `file_extension`, `timestamp_format`) are now escaped before being embedded in the compiled SQL.
  - `repr()` of `AWSBucket`, `AzureContainer`, and `GCSBucket` now masks cloud secrets (`AWS_SECRET_KEY`, `AWS_KEY_ID`, `AWS_TOKEN`, `AZURE_SAS_TOKEN`, `MASTER_KEY`), rendering them as `'***'`. Compiled SQL is unchanged.
  - Added an opt-in logging redactor for engine logs that contain inline credentials: `SnowflakeSecretRedactionFilter`, `add_secret_redaction_filter()`, and `redact_secrets()`. Prefer `STORAGE_INTEGRATION` to avoid putting secrets in SQL.
- Optimized single-table reflection so that reflecting one table no longer scans the entire schema, reducing latency and Snowflake credit usage for targeted `Inspector` calls.

### Bug fixes

- Fixed `ClusterByOption` to raise `TypeError` at DDL compile time when an expression element is neither a `str` nor a `sqlalchemy.sql.expression.TextClause`. Previously, such values were silently coerced via `str()`, producing malformed DDL (for example, bind-parameter placeholders like `:id_1`) for any expression beyond a bare column name. Code using only `str` or `text(...)` is unaffected.
- Fixed `get_view_definition` silently truncating or failing for view names containing a single quote or backslash (for example, `o'brien`). The name is now SQL-escaped before being embedded in the `SHOW VIEWS LIKE '...'` literal, so such views are found correctly.

## Version 1.10.2 (June 18, 2026)

### Bug fixes

- Fixed double-escaped identifier quoting for database-qualified schemas in structured type column reflection. Since v1.10.1, the schema was quoted as a single identifier, so a qualified schema such as `"MYDB"."MYSCHEMA"` became `"""MYDB"".""MYSCHEMA"""`, causing the `DESC TABLE` fallback to fail (emitting a `Failed to reflect table ... sqlalchemy:_get_schema_columns` warning) for every structured-typed table when reflecting a non-default `database.schema`. The schema is now split on the dot and each component is double-quoted individually, preserving the identifier injection guard while correctly handling qualified schemas.

## Version 1.10.1 (June 15, 2026)

### Bug fixes

- Fixed `regexp_match` and `regexp_replace` flags being rendered as bound parameters instead of literal strings. Flags passed to `ColumnElement.regexp_match(..., flags=...)` and `ColumnElement.regexp_replace(..., flags=...)` were processed through the standard parameter pipeline, producing incorrect SQL. Flags are now rendered as inline string literals, matching Snowflake’s expected `REGEXP_LIKE(col, pattern, 'i')` and `REGEXP_REPLACE(col, pattern, replacement, 'i')` syntax.
- Fixed inconsistent identifier quoting in structured type column reflection. The `DESC TABLE` fallback path used raw unquoted identifiers for schema and table names while all other reflection paths applied proper quoting. Schema and table components are now consistently double-quoted before the statement is constructed.

## Version 1.10.0 (May 20, 2026)

### New features and updates

- Added Google Cloud Storage (GCS) bucket support for the `CopyIntoStorage` expression.
- Added `SnowflakeBase`, `snowflake_declarative_base()`, and `SnowflakeSession` to enable efficient bulk inserts for ORM models with nullable optional columns. Using `SnowflakeBase` (or `snowflake_declarative_base()`) along with `SnowflakeSession` batches all objects into a single `executemany` INSERT, instead of producing one INSERT statement per distinct set of non-`None` column keys.
- Added the `case_sensitive_identifiers` opt-in engine flag (constructor keyword argument or `?case_sensitive_identifiers=True` URL parameter) that governs case-sensitive identifier handling. The default value is `False`, so existing applications aren’t affected unless they explicitly opt in. When you opt in:
  - All-uppercase reserved-word identifiers (for example, `TABLE`) are normalized to `quoted_name("table", True)` to prevent key-lookup mismatches between creation and reflection.
  - Mixed-case reflected identifiers (for example, `MyCol` from a quoted Snowflake column) are returned as `quoted_name("MyCol", True)` instead of a plain `str`.
  - Schema strings with inner double quotes (for example, `'"myschema"'` or `'"mydb"."myschema"'`) have their extracted parts marked `quote=True`, preserving case sensitivity in emitted SQL.
- Added the `create_snowflake_engine(url, schema=..., case_sensitive_schema=True)` helper. The helper URL-encodes case-sensitive schema names using `%22` so the Snowflake connector receives the literal double-quoted form. Schema names are now always URL-encoded regardless of `case_sensitive_schema`, preventing special characters (`?`, `#`, `/`) from being misinterpreted as URL delimiters.
- Added `snowflake.sqlalchemy.alembic_util.render_item`, a drop-in Alembic `render_item` hook for `env.py` that serializes `quoted_name` columns with `quote=True` correctly in generated migration files, preventing Alembic autogenerate from silently converting case-sensitive column names to uppercase.
- Added support for cross-database schema reflection using `schema='database.schema'` notation, so you can reflect and join tables from different databases in a single session without using raw SQL.
- Added composite key ordering.
- Added a `SnowflakeWarning` that’s emitted at DDL compile time when `Identity()` is used on a primary key column. The warning alerts you that ORM flush operations will raise a `FlushError`. Use `Sequence()` instead. The warning is emitted once per unique `(table, column)` pair per Python process.
- Mapped the Snowflake `UUID` column type to `sqlalchemy.sql.sqltypes.UUID` for reflection on SQLAlchemy 2.x. The column was previously reflected as `NullType`. Values are returned as plain strings (`as_uuid=False`) rather than `uuid.UUID` instances. There’s no change on SQLAlchemy 1.4, where the generic `UUID` type doesn’t exist.
- Optimized reflection performance:
  - Added `get_multi_columns`, `get_multi_pk_constraint`, `get_multi_unique_constraints`, and `get_multi_foreign_keys` for SQLAlchemy 2.x bulk reflection. Each method issues one schema-wide query per reflection pass instead of one query per table.
  - On SQLAlchemy 2.x, `get_pk_constraint`, `get_unique_constraints`, `get_foreign_keys`, and `get_indexes` now automatically use per-table `SHOW … IN TABLE` queries without any opt-in flag. These methods previously always issued `SHOW … IN SCHEMA`, even for single-table Inspector calls, which caused approximately 20-second delays on schemas with thousands of tables.
  - The `cache_column_metadata=True` opt-in now enables per-table `SHOW … IN TABLE` queries for `get_pk_constraint`, `get_unique_constraints`, `get_foreign_keys`, and `get_indexes` on SQLAlchemy 1.4.
  - SQLAlchemy 2.x `get_columns` now uses `DESC TABLE` directly so that temporary tables and dynamic tables are reflected correctly.

### Bug fixes

- Fixed `with_loader_criteria` silently dropping filters on non-Snowflake dialects. Importing `snowflake-sqlalchemy` previously altered SQLAlchemy’s ORM compilation for every dialect in the process, causing loader-criteria filters to be omitted inside sealed subqueries when using PostgreSQL, MySQL, SQLite, and others. Snowflake dialect behavior is unchanged; the BCR-1057 lateral-join workaround is now scoped to Snowflake connections only.
- Scoped `referred_schema=None` normalization in foreign key reflection to the default schema only. When reflecting the default schema, same-schema foreign keys (default to default) keep the established SQLAlchemy convention of `referred_schema=None`. When reflecting a non-default schema, every foreign key keeps its actual `referred_schema`. This change prevents Alembic autogenerate mismatches that previously occurred for cross-schema foreign keys that targeted the default schema.
- Fixed case-sensitive identifier handling:
  - `_split_schema_by_dot` now correctly parses SQL-escaped double quotes (`""`) inside quoted schema and database identifiers (for example, `"my""schema"` becomes `my"schema`), preventing silent truncation of identifiers containing literal quote characters.
  - `denormalize_column_name` now correctly double-quotes `quoted_name("mycol", True)` columns in `CLUSTER BY` clauses, instead of silently dropping the case-sensitivity signal.
  - `_has_object` (used by `has_table` and `has_sequence`) now applies `denormalize_name` to both the schema and object name before building the `DESC` SQL, making it consistent with all other reflection methods.
  - `create_connect_args` now atomically replaces the `name_utils` instance when the URL’s `case_sensitive_identifiers` value differs from the current dialect state, so concurrent readers on other threads never observe a torn update.
- Restored backward-compatible SQL generation for true division (`/`) when `div_is_floordiv=True`. The Snowflake compiler now correctly delegates to the SQLAlchemy base implementation, emitting `CAST(col AS NUMERIC)` for integer operands as it did before.
- Fixed foreign key `referred_schema` resolution so reflected foreign keys keep their actual schema unless the target is in the connection’s default schema. Foreign keys whose target shared the reflected non-default schema were previously reported with `referred_schema=None`, which caused SQLAlchemy’s `_reflect_fk` to autoload from the wrong schema and raise `NoReferencedColumnError` during Alembic autogenerate.
- Replaced `SHOW TABLES LIKE` with `SHOW INDEXES IN TABLE` for single-table index reflection, eliminating SQL `LIKE` wildcard false positives and case-sensitivity bugs.

## Version 1.9.0 (March 04, 2026)

### New features and updates

- Added support for `DECFLOAT` and `VECTOR` data types.
- Added support for `server_version_info` support.
- Added support for `ILIKE` in queries.
- Introduced a shared helper for fully-qualified schema name resolution, replacing inconsistent ad-hoc patterns across reflection methods.
- Refactored column reflection internals into dedicated helpers to reduce complexity without changing behavior.
- Added `pytest-xdist` parallel test support via per-worker schema provisioning hooks.
- Bumped pandas lower bound in the sa14 test environment from <2.1 to >=2.1.1,<2.2 to ensure pre-built wheels are available for Python 3.12.
- Added support for timezone in timestamp and datetime types.

### Bug fixes

- Fixed `SYSDATE()` rendering.
- Fixed and improved schema reflection.
- Fixed a crash issue when reflecting without specifying a schema, caused by `None` arguments in internal schema resolution.
- Fixed a crash issue when SHOW TABLES returns empty string table names, causing `IndexError` during reflection.
- Fixed incomplete identity column reflection metadata. This column now includes all fields required by SQLAlchemy 2.0+ (`always`, `cycle`, `order`, and so on).
- Fixed SQLAlchemy version parsing.
