# Teradata to Snowflake data type mappings

The following table shows how Snowflake AIM for Virtualization maps Teradata data types to Snowflake types. Mappings are shown for both Snowflake Native tables and Iceberg tables, with the Iceberg columns split into V2 and V3.

Note

Snowflake AIM for Virtualization uses a single Iceberg code path internally and does not distinguish between Iceberg V2 and V3. Any differences between the Iceberg V2 and V3 columns reflect the Iceberg specification’s own type support (for example, VARIANT requires V3), not separate Snowflake AIM for Virtualization code paths.

| Teradata data type | Type code | Snowflake Native | Iceberg V2 | Iceberg V3 |
| --- | --- | --- | --- | --- |
| BIGINT | I8 | NUMBER(38,0) | NUMBER(38,0) | NUMBER(38,0) |
| BLOB | BO | BINARY | BINARY | BINARY |
| BYTE | BF | BINARY | BINARY | BINARY |
| BYTEINT | I1 | NUMBER(38,0) | NUMBER(38,0) | NUMBER(38,0) |
| CHAR | CF | VARCHAR(c): matches Teradata length | VARCHAR(134217728): max, Teradata length not preserved | VARCHAR(134217728): max, Teradata length not preserved |
| CLOB | CO | VARCHAR(134217728): max (LOB) | VARCHAR(134217728): max (LOB) | VARCHAR(134217728): max (LOB) |
| DATE | DA | DATE | DATE | DATE |
| DECIMAL / NUMERIC | D | NUMBER(p, s): matches Teradata precision/scale | NUMBER(p, s): matches Teradata precision/scale | NUMBER(p, s): matches Teradata precision/scale |
| FLOAT | F | FLOAT | DOUBLE | DOUBLE |
| REAL | F | FLOAT | DOUBLE | DOUBLE |
| DOUBLE | F | FLOAT | DOUBLE | DOUBLE |
| INTEGER | I | NUMBER(38,0) | NUMBER(38,0) | NUMBER(38,0) |
| INTERVAL DAY..SECOND | DY DH DM DS … | NUMBER(19,0): total microseconds (6 fractional digits) | NUMBER(19,0): total microseconds (6 fractional digits) | NUMBER(19,0): total microseconds (6 fractional digits) |
| INTERVAL YEAR..MONTH | MO / YM / YR | NUMBER(19,0): total months | NUMBER(19,0): total months | NUMBER(19,0): total months |
| JSON | JN | VARIANT | NOT SUPPORTED | VARIANT |
| NUMBER(n,m) | N | NUMBER(p, s): matches Teradata precision/scale | NUMBER(p, s) | NUMBER(p, s) |
| NUMBER(\*,m) | N | FLOAT | FLOAT | FLOAT |
| NUMBER(\*) | N | FLOAT | FLOAT | FLOAT |
| PERIOD(DATE) | PD PT PZ PS PM | VARCHAR(28) | VARCHAR(134217728): max, Teradata length not preserved | VARCHAR(134217728): max, Teradata length not preserved |
| PERIOD(TIME) | PD PT PZ PS PM | VARCHAR(38) | VARCHAR(134217728): max, Teradata length not preserved | VARCHAR(134217728): max, Teradata length not preserved |
| PERIOD(TIMESTAMP) | PD PT PZ PS PM | VARCHAR(60) | VARCHAR(134217728): max, Teradata length not preserved | VARCHAR(134217728): max, Teradata length not preserved |
| PERIOD(TIMESTAMP WITH TZ) | PD PT PZ PS PM | VARCHAR(72) | VARCHAR(134217728): max, Teradata length not preserved | VARCHAR(134217728): max, Teradata length not preserved |
| SMALLINT | I2 | NUMBER(38,0) | NUMBER(38,0) | NUMBER(38,0) |
| TIME | AT | TIME | TIME | TIME |
| TIME WITH TIME ZONE | TZ | TIMESTAMP\_TZ | TIMESTAMP\_LTZ | TIMESTAMP\_LTZ |
| TIMESTAMP | TS | TIMESTAMP\_NTZ | TIMESTAMP\_NTZ | TIMESTAMP\_NTZ |
| TIMESTAMP WITH TIME ZONE | SZ | TIMESTAMP\_TZ | TIMESTAMP\_LTZ | TIMESTAMP\_LTZ |
| UDT | UT | Generic UDT unsupported; ST\_GEOMETRY → GEOGRAPHY (or GEOMETRY via hint) | Generic UDT unsupported; ST\_GEOMETRY → GEOGRAPHY (or GEOMETRY via hint) | Generic UDT unsupported; ST\_GEOMETRY → GEOGRAPHY (or GEOMETRY via hint) |
| VARBYTE | BV | BINARY | BINARY | BINARY |
| VARCHAR | CV | VARCHAR(c): matches Teradata length | VARCHAR(134217728): max, Teradata length not preserved | VARCHAR(134217728): max, Teradata length not preserved |
| XML | XM | VARIANT | NOT SUPPORTED | VARIANT |

Expand

Show lessSee more
