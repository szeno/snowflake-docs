# Aug 21, 2026: AIM-Virtualization 3.176

## New features

### SQL compatibility

- Added SESSIONIZE ordered-analytic table function support for session-gap analysis workloads
- Added RANGE\_N partitioning function for CHECK constraints and PARTITION BY expressions
- Added multi-statement BEGIN REQUEST block support (SELECT, CALL, EXEC MACRO)
- Added table operator ON (SELECT …) inline syntax support
- Added TIMECODE as a first-class keyword, resolving parsing ambiguities in GROUP BY TIME and other contexts

### Functions

- Added WIDTH\_BUCKET, SKEW, and REGR\_SLOPE scalar and aggregate function support
- Added SUBBITSTR, SHIFTLEFT, and SHIFTRIGHT bitwise function support
- Added three-argument GETQUERYBANDVALUE support
- Added DAY\_NUMBER\_OF\_YEAR temporal expression support
- Extended FROM\_BYTES to support signed base-10 (two’s-complement) integer decoding

### Connectivity

- Added BTEQ 20.00 and Teradata 17.20 authentication (AES-128-GCM and GSS wrap protocol), enabling connections from modern Teradata client tools
- Added SHOWFEATURES diagnostic command support for Snowflake backends

## Bug fixes

### Type conversion and casting

- Fixed NUMERIC(38,38) scale overflow by auto-clamping to NUMERIC(38,37)
- Fixed INTERVAL-to-number cast returning incorrect values instead of matching Teradata semantics
- Fixed TIMESTAMP\_TZ precision loss in timezone-offset fallback
- Fixed CAST(date/timestamp AS FLOAT) to use correct Snowflake date arithmetic
- Fixed redundant same-type temporal casts (DATE, TIME, TIMESTAMP) being incorrectly preserved
- Fixed CREATE FUNCTION type mismatches for CHAR/VARCHAR, NUMBER/FLOAT, and INT/DATE return and body combinations

### Date, time, and formatting

- Fixed TIME WITH TIME ZONE literals losing timezone offset during translation
- Fixed TO\_TIMESTAMP double-quoted literal characters in format strings
- Fixed currency format symbols (L, U, C) in numeric format strings
- Fixed TO\_NUMBER grouping separator behavior to match Teradata semantics
- Fixed ALTER TABLE ADD … DEFAULT timestamp type rendering

### Query and SQL correctness

- Fixed NOT IN (SEL DISTINCT \*) incorrectly raising an error
- Fixed schema-qualified table-valued functions and STRTOK\_SPLIT\_TO\_TABLE translation
- Fixed double-emission of constant format expressions in translated SQL
- Fixed GETBIT/SETBIT to correctly handle 8-byte (64-bit) integer values
- Fixed SUBBITSTR bit-extraction precision for lengths greater than or equal to 54
- Fixed CONTINUE HANDLER invocation for failing DML statements in stored procedures
- Fixed ID2BIGINT identity columns in INSERT/UPDATE/DELETE contexts

### ODBC and connectivity

- Fixed BYTE/VARBYTE/BLOB encoding and type reporting over ODBC
- Fixed crash on unknown ODBC type for BLOB columns
- Fixed SQL\_BINARY/SQL\_VARBINARY type code recognition for certain driver configurations
- Fixed JSONExtractValue result width to report VARCHAR(4096), matching Teradata’s documented behavior
- Fixed BTEQ concurrent connection session-identification under parallel workloads
- Added eager credential resolution at startup to surface configuration errors immediately

### Parser and error handling

- Fixed scientific notation false positives on bare ‘E’ characters in numeric strings
- Fixed INFORMATION\_SCHEMA queries failing due to cross-database permission errors
- Fixed global temporary table names containing special characters causing crashes
- Added clear parse-time errors for malformed SysExecSQL and XML DECLARE with CHARACTER SET

### DDL and session

- Fixed `COPY STATISTICS` and `COLLECT STATISTICS` to pass through to Snowflake as no-ops, enabling DDL scripts to run without modification
- Fixed `REPLACE VIEW` and `REPLACE MACRO` to correctly report “created” vs. “replaced” status
- Removed deprecated legacy TLS configuration keys

### Performance

- Cached resolved schema names per session, eliminating redundant metadata lookups
- Short-circuited TO\_CHAR hour normalization when format strings contain no hour tokens
- Reduced per-query overhead with query timing instrumentation cache and collapsed schema resolution round-trip

### Security

- Replaced unbounded atom creation in hint and character-set parsers with allowlists, preventing resource exhaustion
- Fixed SQL log-masking to fail closed on malformed input instead of potentially leaking unmasked SQL
