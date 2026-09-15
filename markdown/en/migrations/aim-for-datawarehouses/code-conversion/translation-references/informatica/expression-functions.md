# Informatica PowerCenter - Expression functions

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts. This preview is available for Informatica PowerCenter migrations.

Note

This reference applies to both output formats, **dbt** and **Snowflake Scripting**.

This page lists the Informatica PowerCenter built-in functions and their Snowflake equivalents. The mapping is the same for both output formats (dbt and Snowflake Scripting), because both produce the same Snowflake expression. For the concept overview, see the [Informatica PowerCenter overview](README).

Most functions map to a Snowflake function with the same name and behavior. The tables below give the Snowflake equivalent for every supported function and flag the ones whose name, arguments, or behavior differ. The [Examples](#examples) section shows a before and after for the functions that change.

Functions that have no Snowflake equivalent (for example, `ABORT` and `ERROR`) are converted to `NULL` and marked with an EWI so you can review them.

## String functions

| Informatica | Snowflake | Notes |
| --- | --- | --- |
| `ASCII` | `ASCII` | Same name and behavior. |
| `CHR` | `CHR` | Same name and behavior. |
| `CHRCODE` | `ASCII` | Maps to `ASCII`. |
| `CONCAT` | `CONCAT` | Two arguments; nested for more. The `||` operator is also supported. |
| `INITCAP` | `INITCAP` | Same name and behavior. |
| `INSTR` | `POSITION` or `REGEXP_INSTR` | See [INSTR](#instr). |
| `INDEXOF` | `CASE` expression | Returns the 1-based position of the first matching value in the list. See [INDEXOF](#indexof). |
| `LENGTH` | `LENGTH` | Same name and behavior. |
| `LOWER` | `LOWER` | Same name and behavior. |
| `LPAD` | `LPAD` | Same name and behavior. |
| `LTRIM` | `LTRIM` | Same name and behavior. |
| `REPLACECHR` | `REPLACE` or `REGEXP_REPLACE` | See [REPLACECHR and REPLACESTR](#replacechr-and-replacestr). |
| `REPLACESTR` | `REPLACE` | Case-insensitive form is not supported natively. See [REPLACECHR and REPLACESTR](#replacechr-and-replacestr). |
| `REG_EXTRACT` | `REGEXP_SUBSTR` | Argument order differs. See [REG\_EXTRACT](#reg_extract). |
| `REG_MATCH` | `RLIKE` | Maps to `RLIKE`. |
| `REG_REPLACE` | `REGEXP_REPLACE` | See [REG\_REPLACE](#reg_replace). |
| `REVERSE` | `REVERSE` | Same name and behavior. |
| `RPAD` | `RPAD` | Same name and behavior. |
| `RTRIM` | `RTRIM` | Same name and behavior. |
| `SUBSTR` | `SUBSTR` | Same name and behavior; both are 1-based. |
| `UPPER` | `UPPER` | Same name and behavior. |

Expand

Show lessSee more

## Numeric functions

| Informatica | Snowflake | Notes |
| --- | --- | --- |
| `ABS` | `ABS` | Same name and behavior. |
| `CEIL` | `CEIL` | Same name and behavior. |
| `EXP` | `EXP` | Same name and behavior. |
| `FLOOR` | `FLOOR` | Same name and behavior. |
| `LN` | `LN` | Same name and behavior. |
| `LOG` | `LOG` | Same name and behavior. |
| `MOD` | `MOD` | Same name and behavior. |
| `POWER` | `POWER` | Same name and behavior. |
| `ROUND` | `ROUND` | Same name and behavior for numbers. |
| `SIGN` | `SIGN` | Same name and behavior. |
| `SQRT` | `SQRT` | Same name and behavior. |
| `TRUNC` | `TRUNC` | Same name and behavior for numbers. |

Expand

Show lessSee more

## Type conversion functions

| Informatica | Snowflake | Notes |
| --- | --- | --- |
| `TO_CHAR` | `TO_CHAR` | The format mask is translated to the Snowflake format. |
| `TO_DATE` | `TO_DATE` | The format mask is translated to the Snowflake format. |
| `TO_DECIMAL` | `CAST(ROUND(...))` or `CAST(TRUNC(...))` | A flag selects rounding or truncation. See [TO\_DECIMAL, TO\_INTEGER, and TO\_BIGINT](#to_decimal-to_integer-and-to_bigint). |
| `TO_INTEGER` | `CAST(ROUND(...))` or `CAST(TRUNC(...))` | A flag selects rounding or truncation. See [TO\_DECIMAL, TO\_INTEGER, and TO\_BIGINT](#to_decimal-to_integer-and-to_bigint). |
| `TO_BIGINT` | `CAST(ROUND(...))` or `CAST(TRUNC(...))` | A flag selects rounding or truncation. See [TO\_DECIMAL, TO\_INTEGER, and TO\_BIGINT](#to_decimal-to_integer-and-to_bigint). |
| `TO_FLOAT` | `TO_DOUBLE` | Maps to `TO_DOUBLE`. |

Expand

Show lessSee more

## Conditional and null-handling functions

| Informatica | Snowflake | Notes |
| --- | --- | --- |
| `IIF` | `IFF` | A missing false branch becomes `NULL`. See [IIF](#iif). |
| `DECODE` | `DECODE` or `CASE` | `DECODE(TRUE, ...)` becomes a `CASE` expression. See [DECODE](#decode). |
| `IN` | `IN` | Becomes a Snowflake `IN` predicate. |
| `ISNULL` | `IS NULL` | Becomes an `IS NULL` predicate. See [ISNULL](#isnull). |
| `IS_DATE` | `TRY_TO_DATE(...) IS NOT NULL` | Validates with `TRY_TO_DATE`. See [IS\_DATE and IS\_NUMBER](#is_date-and-is_number). |
| `IS_NUMBER` | `TRY_TO_NUMBER(...) IS NOT NULL` | Validates with `TRY_TO_NUMBER`. See [IS\_DATE and IS\_NUMBER](#is_date-and-is_number). |
| `IS_SPACES` | `TRIM(...) = '' OR ... IS NULL` | Returns true when the value is blank or null. |

Expand

Show lessSee more

## Date and time functions

| Informatica | Snowflake | Notes |
| --- | --- | --- |
| `ADD_TO_DATE` | `DATEADD` | The Informatica format code becomes a Snowflake date part. See [ADD\_TO\_DATE](#add_to_date). |
| `DATE_COMPARE` | `CASE` expression | Returns -1, 0, or 1. |
| `DATEDIFF` | `DATEDIFF` | The date arguments are swapped to preserve the sign. See [DATEDIFF](#datediff). |
| `GET_DATE_PART` | `DATE_PART` | The format code becomes a Snowflake date part. |
| `SET_DATE_PART` | `DATEADD` arithmetic | The part is set by adding the difference. |
| `LAST_DAY` | `LAST_DAY` | Same name and behavior. |
| `MAKE_DATE_TIME` | `TIMESTAMP_NTZ_FROM_PARTS` | Builds a timestamp from the year, month, day, and time parts. |
| `SYSDATE` | `CURRENT_TIMESTAMP` | See [System variables](#system-variables). |
| `SYSTIMESTAMP` | `CURRENT_TIMESTAMP` | See [System variables](#system-variables). |

Expand

Show lessSee more

## Aggregate functions

The two-argument Informatica aggregate form (an aggregate with a filter condition) becomes the same aggregate wrapped in a `CASE` expression.

| Informatica | Snowflake | Notes |
| --- | --- | --- |
| `AVG` | `AVG` | Filter form uses `AVG(CASE WHEN ... END)`. See [Aggregates with a filter](#aggregates-with-a-filter). |
| `COUNT` | `COUNT` | Filter form uses `COUNT(CASE WHEN ... END)`. |
| `SUM` | `SUM` | Filter form uses `SUM(CASE WHEN ... END)`. |
| `MIN` | `MIN` | Filter form uses `MIN(CASE WHEN ... END)`. |
| `MAX` | `MAX` | Filter form uses `MAX(CASE WHEN ... END)`. |
| `MEDIAN` | `MEDIAN` | Filter form uses a `CASE` expression. |
| `STDDEV` | `STDDEV` | Filter form uses a `CASE` expression. |
| `PERCENTILE` | `PERCENTILE_CONT` | The percent is divided by 100 and uses `WITHIN GROUP`. |
| `FIRST` | `ANY_VALUE` | Maps to `ANY_VALUE`; an FDM notes that the returned row is arbitrary. |
| `LAST` | `ANY_VALUE` | Maps to `ANY_VALUE`; an FDM notes that the returned row is arbitrary. |
| `CUME` | `SUM` window | Running total with `SUM(...) OVER (...)`. |

Expand

Show lessSee more

## Comparison functions

| Informatica | Snowflake | Notes |
| --- | --- | --- |
| `GREATEST` | `GREATEST` | Same name and behavior. |
| `LEAST` | `LEAST` | The case-insensitive option becomes a `CASE` expression on `LOWER(...)`. |

Expand

Show lessSee more

## Encoding and hash functions

| Informatica | Snowflake | Notes |
| --- | --- | --- |
| `MD5` | `UPPER(MD5(...))` | Informatica returns uppercase hexadecimal, so the result is wrapped in `UPPER`. An FDM notes possible encoding differences. |
| `ENC_BASE64` | `BASE64_ENCODE` | Maps to `BASE64_ENCODE`. |
| `CRC32` | `CRC32_UDF(...)` | Snowflake has no native CRC32, so a `CRC32_UDF` is generated. An FDM notes possible encoding differences. |

Expand

Show lessSee more

## Variable functions

Informatica variable functions persist a value across rows and sessions. Snowflake SQL has no equivalent persistence, so they are approximated with window functions and the assignment form is converted to a pass-through.

| Informatica | Snowflake | Notes |
| --- | --- | --- |
| `SETVARIABLE` | The value expression | The assignment is dropped; the value passes through. |
| `SETMAXVARIABLE` | `MAX(...) OVER ()` | Approximates the running maximum. |
| `SETMINVARIABLE` | `MIN(...) OVER ()` | Approximates the running minimum. |
| `SETCOUNTVARIABLE` | `COUNT(...) OVER ()` | Approximates the running count. |

Expand

Show lessSee more

## Session-control functions

| Informatica | Snowflake | Notes |
| --- | --- | --- |
| `ABORT` | `NULL` | Snowflake SQL cannot stop a session, so the call becomes `NULL` and is marked with `SSC-EWI-INF0060`. See [ABORT and ERROR](#abort-and-error). |
| `ERROR` | `NULL` | Snowflake SQL cannot skip a row, so the call becomes `NULL` and is marked with `SSC-EWI-INF0051`. See [ABORT and ERROR](#abort-and-error). |

Expand

Show lessSee more

## System variables

`SYSDATE` and `SYSTIMESTAMP` become `CURRENT_TIMESTAMP` in both output formats. The remaining system variables identify the session, workflow, folder, or mapping that’s running, so their translation depends on the output format. On the dbt path, most of them become a dbt variable that the generated orchestration seeds at run time, as shown in [System variable seeding on the dbt path](#system-variable-seeding-on-the-dbt-path).

| Informatica | Snowflake | Notes |
| --- | --- | --- |
| `SYSDATE` | `CURRENT_TIMESTAMP` | Current date and time. |
| `SYSTIMESTAMP` | `CURRENT_TIMESTAMP` | Current date and time. |
| `SESSSTARTTIME` | `'{{ var('SESSSTARTTIME') }}' :: TIMESTAMP` | On the dbt path, the session start time becomes a dbt variable cast to `TIMESTAMP`, and no EWI or FDM is emitted. `dbt_project.yml` declares the variable with the sentinel default `"1753-01-01 00:00:00"` rather than `null`, because a `null` default renders as `'None' :: TIMESTAMP`, which Snowflake rejects. Snowflake Scripting mapping expressions run in control-flow translation context (`isControlFlowContext: true`). `$PMFolderName` and `$PMWorkflowName` become conversion-time string literals when folder or workflow names are known; `SESSSTARTTIME` and `$PMMappingName` emit `SSC-EWI-INF0012` on that path (`MappletBody_AbortAndBuiltin_SurfacesIssuesOnInstance`). Do not treat `CURRENT_TIMESTAMP` or dbt `{{ var() }}` as the Scripting mapping-body translation. |
| `WORKFLOWSTARTTIME` | `'{{ var('WORKFLOWSTARTTIME') }}' :: TIMESTAMP` | Mirrors `SESSSTARTTIME` on the dbt path, including the `"1753-01-01 00:00:00"` default in `dbt_project.yml`. Without this mapping the variable falls through as a bare identifier, which isn’t valid Snowflake SQL. |
| `$PMSessionName` | `'{{ var('PMSESSIONNAME') }}' :: VARCHAR` | On the dbt path, the session name becomes a dbt variable that the generated orchestration seeds with `InsertControlVariable`. No issue is emitted. |
| `$PMWorkflowName` | `'{{ var('PMWORKFLOWNAME') }}' :: VARCHAR` | Follows the same pattern as `$PMSessionName`, seeded with the workflow name. No issue is emitted. |
| `$PMFolderName` | `'{{ var('PMFOLDERNAME') }}' :: VARCHAR` | Follows the same pattern, seeded with the consumer folder name. Marked with `SSC-FDM-INF0096`, because `$PMFolderName` has no direct Snowflake equivalent. Verify expressions that reference this value. |
| `$PMMappingName` | The mapping name as a string literal | On the dbt path, the mapping name is known at conversion time, so it’s inlined as a literal such as `'m_PMMappingName'`. No dbt variable is added to `dbt_project.yml`, and the orchestration doesn’t seed one. |

Expand

Show lessSee more

### System variable seeding on the dbt path

The dbt model reads each variable with `var()`, and the generated orchestration task supplies the run-time value with `InsertControlVariable` before it calls `EXECUTE DBT PROJECT`. The following output is for `$PMSessionName`:

Copy code

```
-- dbt model
SELECT
   '{{ var('PMSESSIONNAME') }}' :: VARCHAR AS SessionName
FROM
   source_data;

-- Generated orchestration task
CALL public.InsertControlVariable('PMSESSIONNAME', :scope, TO_VARIANT('s_pmsessionname_test'), 'VARCHAR');
```

`SESSSTARTTIME`, `$PMWorkflowName`, and `$PMFolderName` are seeded the same way, except that `SESSSTARTTIME` receives `TO_VARIANT(CURRENT_TIMESTAMP())` and the `TIMESTAMP` type rather than a string. `WORKFLOWSTARTTIME` is the exception: the orchestration doesn’t seed it, so it keeps the value declared in `dbt_project.yml` unless you supply one yourself with `--vars`. `dbt_project.yml` declares `PMSESSIONNAME`, `PMWORKFLOWNAME`, and `PMFOLDERNAME` with a `null` default, and the two timestamp variables with the `"1753-01-01 00:00:00"` sentinel. Because the orchestration passes the real values for the seeded variables through the `--vars` argument, those defaults only apply when you compile the project or run a model outside the orchestration.

## Examples

The following examples show the before (Informatica) and after (Snowflake) for the functions whose name, arguments, or behavior change.

### IIF

`IIF` becomes Snowflake’s `IFF`. When the false branch is omitted, `NULL` is added.

Informatica:

Copy code

```
IIF(SALARY > 50000, 'High', 'Low')
IIF(STATUS = 'ACTIVE', EMPLOYEE_ID)
```

Snowflake:

Copy code

```
IFF((SALARY > 50000), 'High', 'Low')
IFF((STATUS = 'ACTIVE'), EMPLOYEE_ID, NULL)
```

### DECODE

A standard `DECODE` (equality search) maps directly to Snowflake’s `DECODE`. The boolean form, `DECODE(TRUE, condition, result, ...)`, becomes a `CASE` expression.

Informatica:

Copy code

```
DECODE(TRUE,
  SALARY > 100000, 'Band A',
  SALARY > 50000,  'Band B',
  'Band C')
```

Snowflake:

Copy code

```
CASE
  WHEN (SALARY > 100000) THEN 'Band A'
  WHEN (SALARY > 50000)  THEN 'Band B'
  ELSE 'Band C'
END
```

### ISNULL

`ISNULL` becomes an `IS NULL` predicate.

Informatica:

Copy code

```
IIF(ISNULL(PHONE_NUMBER), '000-000-0000', PHONE_NUMBER)
```

Snowflake:

Copy code

```
IFF((PHONE_NUMBER IS NULL), '000-000-0000', PHONE_NUMBER)
```

### IS\_DATE and IS\_NUMBER

These validation functions use `TRY_TO_DATE` or `TRY_TO_NUMBER` and test the result for `IS NOT NULL`. For `IS_NUMBER`, the `'integer'` type maps to `TRY_TO_NUMBER(value, 38, 0)`.

Informatica:

Copy code

```
IS_DATE(HIRE_DATE_STR, 'YYYY-MM-DD')
IS_NUMBER(QTY_STR, 'integer')
```

Snowflake:

Copy code

```
(TRY_TO_DATE(HIRE_DATE_STR, 'YYYY-MM-DD') IS NOT NULL)
(TRY_TO_NUMBER(QTY_STR, 38, 0) IS NOT NULL)
```

### INSTR

A simple, case-sensitive search for the first occurrence becomes `POSITION`. Any start position, occurrence count, or case-insensitivity flag uses `REGEXP_INSTR`.

Informatica:

Copy code

```
INSTR(FULL_NAME, ' ')
INSTR(LOG_TEXT, 'error', 1, 2)
```

Snowflake:

Copy code

```
POSITION(' ' IN FULL_NAME)
REGEXP_INSTR(LOG_TEXT, 'error', 1, 2)
```

### INDEXOF

`INDEXOF(value, search1 [, search2, ...])` returns the 1-based position of the first search string that equals `value`, or 0 when none match. It is converted to a `CASE` expression.

Informatica:

Copy code

```
INDEXOF(ITEM_CODE, 'A', 'B', 'C')
```

Snowflake:

Copy code

```
CASE
  WHEN ITEM_CODE IS NULL THEN NULL
  WHEN ITEM_CODE = 'A' THEN 1
  WHEN ITEM_CODE = 'B' THEN 2
  WHEN ITEM_CODE = 'C' THEN 3
  ELSE 0
END
```

### REG\_EXTRACT

`REG_EXTRACT` maps to `REGEXP_SUBSTR`. The subpattern (capture group) and case-insensitivity flag move to different argument positions.

Informatica:

Copy code

```
REG_EXTRACT(CODE_COL, '([A-Z]{2})-([0-9]+)', 2)
```

Snowflake:

Copy code

```
REGEXP_SUBSTR(CODE_COL, '([A-Z]{2})-([0-9]+)', 1, 1, 'e', 2)
```

### REG\_REPLACE

`REG_REPLACE` maps to `REGEXP_REPLACE`. The case-insensitivity flag becomes the trailing parameters flag.

Informatica:

Copy code

```
REG_REPLACE(NOTES, 'confidential', '[REDACTED]', 1)
```

Snowflake:

Copy code

```
REGEXP_REPLACE(NOTES, 'confidential', '[REDACTED]', 1, 0, 'i')
```

### REPLACECHR and REPLACESTR

`REPLACECHR` becomes `REPLACE` for a single character or `REGEXP_REPLACE` for a set of characters. `REPLACESTR` becomes `REPLACE`. The first argument is a case-sensitivity flag: only the case-sensitive form (`1`) has an exact Snowflake equivalent, so a functional-difference marker is added for the case-insensitive form.

Informatica:

Copy code

```
REPLACECHR(1, 'Cleveland', 'eldn', '_')
REPLACESTR(1, DESCRIPTION, 'foo', 'bar')
```

Snowflake:

Copy code

```
REGEXP_REPLACE('Cleveland', '[eldn]', '_')
REPLACE(DESCRIPTION, 'foo', 'bar')
```

### TO\_DECIMAL, TO\_INTEGER, and TO\_BIGINT

These conversions take an optional flag that selects rounding (the default) or truncation. The flag is mapped to `ROUND` or `TRUNC` and the result is cast.

Informatica:

Copy code

```
TO_DECIMAL(AMOUNT, 2)
TO_DECIMAL(AMOUNT, 2, 1)
```

Snowflake:

Copy code

```
CAST(ROUND(AMOUNT, 2) AS DECIMAL(38, 2))
CAST(TRUNC(AMOUNT, 2) AS DECIMAL(38, 2))
```

### ADD\_TO\_DATE

`ADD_TO_DATE` maps to `DATEADD`, with the Informatica format code translated to a Snowflake date part (for example, `DD` to `DAY`, `MM` to `MONTH`, `YYYY` to `YEAR`).

Informatica:

Copy code

```
ADD_TO_DATE(CONTRACT_START, 'MM', -6)
```

Snowflake:

Copy code

```
DATEADD(MONTH, -6, CONTRACT_START)
```

### DATEDIFF

`DATEDIFF` maps to Snowflake’s `DATEDIFF`, but the date arguments are swapped. Informatica computes `date1 - date2`, while Snowflake computes `end - start`, so the arguments are reversed to keep the same sign.

Informatica:

Copy code

```
DATEDIFF('DD', END_DATE, START_DATE)
```

Snowflake:

Copy code

```
DATEDIFF(DAY, START_DATE, END_DATE)
```

### Aggregates with a filter

An Informatica aggregate with a filter condition (the two-argument form) becomes the same aggregate over a `CASE` expression.

Informatica:

Copy code

```
SUM(ORDER_AMOUNT, STATUS = 'COMPLETE')
```

Snowflake:

Copy code

```
SUM(CASE WHEN (STATUS = 'COMPLETE') THEN ORDER_AMOUNT END)
```

### ABORT and ERROR

`ABORT` stops the session and `ERROR` skips a row. Snowflake SQL has neither mechanism, so both become `NULL` and are marked with an EWI for manual review: `SSC-EWI-INF0060` for `ABORT` and `SSC-EWI-INF0051` for `ERROR`.

Informatica:

Copy code

```
IIF(AMOUNT < 0, ERROR('Negative amount not allowed'), AMOUNT)
```

Snowflake:

Copy code

```
IFF((AMOUNT < 0), NULL, AMOUNT)
```

Note

Because `ABORT` and `ERROR` become `NULL`, the row is not stopped or skipped in Snowflake. Review each `SSC-EWI-INF0060` and `SSC-EWI-INF0051` marker and reproduce the validation with a pre-load check or a dbt test where the original logic depended on it.
