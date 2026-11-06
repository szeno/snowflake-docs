# Nov 4, 2026: AIM-Virtualization 3.180

## New features

### Functions

- Extended TO\_BYTES to support base16, base10, base8, base2, and ascii encodings

## Bug fixes

### Query and SQL correctness

- Added opt-in Teradata run-time emulation for scalar subqueries that don’t structurally guarantee a single row. A subquery that returns more than one row now fails with Teradata error 3669, as on Teradata. To enable the emulation, set `gateway_snowflake.scalar_subquery_cardinality = check` in `dtm.ini`. You can also set it per session or per statement. The default, `passthrough`, keeps the previous behavior.
- Fixed STRTOK\_SPLIT\_TO\_TABLE failing to resolve columns from a table not listed in FROM. AIM-Virtualization now adds the implicit table reference, as Teradata does.
- Fixed statement-level hints (`--@dtm_<name>=...`) not applying to subqueries. Statements that combine a hint with a subquery may translate differently than before.

### Functions

- Fixed IS\_NUM(STRTOK(…)) failing with an invalid number or type of parameters

### Date, time, and formatting

- Fixed inserting CURRENT\_TIME into a TIMESTAMP WITH TIME ZONE column being rejected
- Fixed format strings such as `'YYYY-MM-DDTHH:MI:SS'` so that an unquoted T is treated as the Teradata AM/PM marker

### DDL and data load

- Fixed RENAME TABLE on Iceberg tables to issue ALTER ICEBERG TABLE … RENAME TO reliably on all Snowflake editions, including Iceberg tables created directly in Snowflake
- Fixed DROP TABLE … ALL on global temporary tables being rejected. Existing instances are dropped when the session that holds them ends, not immediately as in Teradata.
- Fixed BTEQ .IMPORT VARTEXT with .REPEAT \* and a USING INSERT failing on the first record when loading a VARCHAR field into a DATE column
