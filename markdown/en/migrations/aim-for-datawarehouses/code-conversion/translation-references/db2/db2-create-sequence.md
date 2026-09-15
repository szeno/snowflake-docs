# IBM DB2 - CREATE SEQUENCE

## Description

> The [CREATE SEQUENCE](https://www.ibm.com/docs/en/db2/11.5?topic=statements-create-sequence) statement creates a sequence object that generates successive integer values. DB2 CREATE SEQUENCE statements are converted to Snowflake equivalents, removing unsupported options and reformatting the statement.

## Transformation Rules

The following DB2 sequence options are handled during conversion:

| DB2 Option | Snowflake Handling |
| --- | --- |
| `AS <data-type>` | Removed (Snowflake sequences are always integer-based) |
| `START WITH` | Preserved |
| `INCREMENT BY` | Preserved |
| `MINVALUE` | Removed with [SSC-EWI-0120](../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0120) |
| `MAXVALUE` | Removed with [SSC-EWI-0120](../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0120) |
| `CYCLE` | Removed with [SSC-EWI-0120](../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0120) |
| `NO CYCLE` | Removed silently (Snowflake default) |
| `CACHE` / `NO CACHE` | Removed silently |
| `ORDER` | Preserved as `ORDER` |
| `NO ORDER` | Converted to `NOORDER` |

Expand

Show lessSee more

When `START WITH` is not explicitly specified, the value is inferred from `MINVALUE` (positive increment) or `MAXVALUE` (negative increment).

## Sample Source Patterns

### Full Option Removal

#### IBM DB2

Copy code

```
CREATE SEQUENCE dwh.seq_tcor_party AS INTEGER
MINVALUE 23177568 MAXVALUE 2147483647
START WITH 23177568 INCREMENT BY 1
CACHE 500 NO CYCLE NO ORDER;
```

#### Snowflake

Copy code

```
!!!RESOLVE EWI!!! /*** SSC-EWI-0120 - SEQUENCE OPTIONS 'MIN VALUE, MAX VALUE' WERE REMOVED, THEY ARE NOT SUPPORTED IN SNOWFLAKE ***/!!!
CREATE SEQUENCE dwh.seq_tcor_party
  START WITH 23177568
  INCREMENT BY 1
  NOORDER
;
```

### Data Type Removal Only

When a sequence has no unsupported options beyond the data type, the `AS <type>` clause is removed silently.

#### IBM DB2

Copy code

```
CREATE SEQUENCE myschema.my_seq AS BIGINT
START WITH 1 INCREMENT BY 1;
```

#### Snowflake

Copy code

```
CREATE SEQUENCE myschema.my_seq
  START WITH 1
  INCREMENT BY 1
;
```

### START WITH Inference from MINVALUE

When `START WITH` is missing and `INCREMENT BY` is positive, the `MINVALUE` is used as the inferred start value.

#### IBM DB2

Copy code

```
CREATE SEQUENCE myschema.nostart_seq AS INTEGER
INCREMENT BY 1
MINVALUE 100 MAXVALUE 999;
```

#### Snowflake

Copy code

```
!!!RESOLVE EWI!!! /*** SSC-EWI-0120 - SEQUENCE OPTIONS 'MIN VALUE, MAX VALUE' WERE REMOVED, THEY ARE NOT SUPPORTED IN SNOWFLAKE ***/!!!
CREATE SEQUENCE myschema.nostart_seq
  START WITH 100
  INCREMENT BY 1
;
```

### START WITH Inference from MAXVALUE (Negative Increment)

When `START WITH` is missing and `INCREMENT BY` is negative, the `MAXVALUE` is used as the inferred start value.

#### IBM DB2

Copy code

```
CREATE SEQUENCE myschema.neg_seq AS INTEGER
INCREMENT BY -1
MINVALUE 1 MAXVALUE 500;
```

#### Snowflake

Copy code

```
!!!RESOLVE EWI!!! /*** SSC-EWI-0120 - SEQUENCE OPTIONS 'MIN VALUE, MAX VALUE' WERE REMOVED, THEY ARE NOT SUPPORTED IN SNOWFLAKE ***/!!!
CREATE SEQUENCE myschema.neg_seq
  START WITH 500
  INCREMENT BY -1
;
```

### CYCLE Option

When `CYCLE` is specified, it is removed and included in the EWI message.

#### IBM DB2

Copy code

```
CREATE SEQUENCE myschema.cycled_seq AS SMALLINT
START WITH 1 INCREMENT BY 1
MINVALUE 1 MAXVALUE 32767
CYCLE CACHE 20 NO ORDER;
```

#### Snowflake

Copy code

```
!!!RESOLVE EWI!!! /*** SSC-EWI-0120 - SEQUENCE OPTIONS 'MIN VALUE, MAX VALUE, CYCLE' WERE REMOVED, THEY ARE NOT SUPPORTED IN SNOWFLAKE ***/!!!
CREATE SEQUENCE myschema.cycled_seq
  START WITH 1
  INCREMENT BY 1
  NOORDER
;
```

## Known Issues

- [SSC-EWI-0120](../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0120): Sequence options were removed because they are not supported in Snowflake.
