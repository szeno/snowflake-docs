# IBM DB2 - COMMENT ON

## Description

> The [COMMENT ON](https://www.ibm.com/docs/en/db2/11.5?topic=statements-comment) statement adds or replaces a comment on a database object. DB2 COMMENT ON statements are converted to their Snowflake equivalents.

## Sample Source Patterns

### COMMENT ON COLUMN

COMMENT ON COLUMN passes through unchanged because Snowflake supports the same syntax.

#### IBM DB2

Copy code

```
COMMENT ON COLUMN "EDM"."FACT_TABLE"."ID_COL" IS 'Record Origination ID';
```

#### Snowflake

Copy code

```
COMMENT ON COLUMN "EDM"."FACT_TABLE"."ID_COL" IS 'Record Origination ID';
```

### COMMENT ON TABLE

COMMENT ON TABLE passes through unchanged because Snowflake supports the same syntax.

#### IBM DB2

Copy code

```
COMMENT ON TABLE "EDM"."FACT_TABLE" IS 'Financial adjustment facts';
```

#### Snowflake

Copy code

```
COMMENT ON TABLE "EDM"."FACT_TABLE" IS 'Financial adjustment facts';
```

### COMMENT ON PROCEDURE

In DB2, COMMENT ON PROCEDURE does not require a parameter list. Snowflake requires an empty parameter list `()` to identify the routine. The empty parentheses are added automatically.

#### IBM DB2

Copy code

```
COMMENT ON PROCEDURE "SCHEMA1"."MY_PROC" IS 'This is a procedure';
```

#### Snowflake

Copy code

```
COMMENT ON PROCEDURE "SCHEMA1"."MY_PROC" () IS 'This is a procedure';
```

### COMMENT ON FUNCTION

In DB2, COMMENT ON FUNCTION does not require a parameter list. Snowflake requires an empty parameter list `()` to identify the routine. The empty parentheses are added automatically.

#### IBM DB2

Copy code

```
COMMENT ON FUNCTION "SCHEMA1"."MY_FUNC" IS 'This is a function';
```

#### Snowflake

Copy code

```
COMMENT ON FUNCTION "SCHEMA1"."MY_FUNC" () IS 'This is a function';
```

## Known Issues

No known issues for this transformation.
