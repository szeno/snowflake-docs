# Code Conversion - Informatica PowerCenter Functional Differences

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts. This preview is available for Informatica PowerCenter migrations.

This section provides detailed documentation for the Functional Difference (FDM) messages that may be generated during Informatica PowerCenter conversion. An FDM marks generated code that runs in Snowflake but may behave differently from the original Informatica PowerCenter mapping, so you should verify the converted results.

For assistance with any FDM, you can use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions, or contact [aim-support@snowflake.com](mailto:aim-support@snowflake.com) for additional support.

## SSC-FDM-INF0001

Lookup policy on multiple match requires proper ordering when multiple rows match. Replace NULL with appropriate ORDER BY column(s) to ensure deterministic match selection.

### Severity

None

### Description

This functional difference (FDM) is reported when an Informatica PowerCenter mapping that uses a lookup policy capable of returning more than one matching row is converted. When multiple rows match, the lookup policy needs explicit ordering to choose a single row deterministically, so you should replace the `NULL` placeholder with the appropriate `ORDER BY` column or columns.

### Best Practices

- Replace the `NULL` placeholder with the `ORDER BY` column or columns that reproduce the original match selection, then verify the converted results against the original mapping.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0002

All input columns will be used to determine group order.

### Severity

None

### Description

This functional difference (FDM) is reported when an Informatica PowerCenter mapping is converted, so you should verify the converted behavior matches the original. In this case, all input columns are used to determine the group order, which may affect how rows are grouped and ordered in the converted output.

### Converted Code

Copy code

```
QUALIFY
   --** SSC-FDM-INF0002 - ALL INPUT COLUMNS WILL BE USED TO DETERMINE GROUP ORDER. **
   ROW_NUMBER() OVER (
   PARTITION BY (
      DEPARTMENT)
   ORDER BY
      NAME,
      SALARY,
      DEPARTMENT) = 1
```

### Best Practices

- Verify the converted grouping and ordering against the original mapping, and add explicit ordering columns where a specific order is required.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0003

IIF function missing onFalseValue parameter defaulted to NULL.

### Severity

None

### Description

This functional difference (FDM) is reported when an `IIF` function that does not provide the false-branch value is converted. Because the false value is missing, it defaults to `NULL`, so you should replace it with an appropriate default value based on the data type of the true-branch value.

### Best Practices

- Replace the defaulted `NULL` with an explicit default value that matches the data type of the true-branch value, then verify the converted results against the original mapping.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0004

TO\_CHAR expression data type could not be determined and might present different results.

### Severity

None

### Description

This functional difference (FDM) is reported when a `TO_CHAR` expression whose input data type could not be determined is converted. Because the data type is unknown, the converted expression might present different results, so you should verify the converted behavior matches the original.

### Best Practices

- Verify the converted `TO_CHAR` output against the original mapping, and add an explicit data type or format where the input type is ambiguous.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0005

INSTR linguistic comparison mode is not fully supported in Snowflake.

### Severity

None

### Description

This functional difference (FDM) is reported when an `INSTR` expression that uses linguistic comparison is converted. This comparison mode is not fully supported because Snowflake uses binary comparison, so language-specific collation rules may not be applied and results may differ.

### Best Practices

- Verify the converted `INSTR` results against the original mapping, especially for strings that rely on language-specific collation rules.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0006

TO\_DATE without format uses session default date format which may differ in Snowflake.

### Severity

None

### Description

This functional difference (FDM) is reported when a `TO_DATE` expression that does not specify a format is converted. Without a format, the expression relies on the session default date format, which may differ between Informatica PowerCenter and Snowflake, so results may differ.

### Best Practices

- Verify that the Snowflake `DATE_INPUT_FORMAT` parameter matches the Informatica session date format, or add an explicit format string to the converted expression.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0007

Normalizer GK port uses `ROW_NUMBER`; behavior equivalent to Restart=YES.

### Severity

None

### Description

This functional difference (FDM) is reported when a Normalizer generated key port is converted to `ROW_NUMBER`, which always starts from 1 for each query execution. This behavior is functionally equivalent to the Restart set to YES option in Informatica PowerCenter, so you should verify the generated key values if they are used as a foreign key in downstream targets.

### Best Practices

- Verify the generated key values against the original mapping, especially where those keys are used as foreign keys in downstream targets.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0008

Normalizer GK port uses `ROW_NUMBER`; Reset=YES behavior not replicated.

### Severity

None

### Description

This functional difference (FDM) is reported when a Normalizer generated key port is converted to `ROW_NUMBER`. The Reset set to YES behavior is not replicated in the dbt translation, because in Informatica PowerCenter that option restores the generated key counter to its pre-session value at session end, while `ROW_NUMBER` always starts from 1. You should verify the generated key values if they are used as a foreign key in downstream targets.

### Best Practices

- Verify the generated key values against the original mapping, especially where those keys are used as foreign keys in downstream targets.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0009

Sorter Transformation Scope Transaction not modelled.

### Severity

None

### Description

This functional difference (FDM) is reported when a Sorter transformation whose scope is set to Transaction is converted. Transaction boundaries are not modelled in Snowflake SQL, so the sort is applied globally across all input rows. You should verify that global sorting produces correct results for the downstream logic.

### Best Practices

- Verify that global sorting produces the correct results for the downstream logic, and add transaction-level partitioning where the original scope is required.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0010

ROUND(date) converted to DATE\_TRUNC which always truncates instead of rounding.

### Severity

None

### Description

This functional difference (FDM) is reported when an Informatica PowerCenter `ROUND` on a date is converted to Snowflake `DATE_TRUNC`. Informatica rounds to the nearest date boundary, so a date past the midpoint of a period rounds up, while `DATE_TRUNC` always truncates to the start of the period. Results may differ for dates past the midpoint.

### Best Practices

- Verify the converted date values against the original mapping, especially for dates that fall past the midpoint of a period, and add explicit rounding logic where needed.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0011

Informatica ROUND uses half-away-from-zero rounding which may differ from Snowflake banker’s rounding on FLOAT types.

### Severity

None

### Description

This functional difference (FDM) is reported when Informatica `ROUND`, `TO_INTEGER`, or `TO_BIGINT` is converted. These functions use half-away-from-zero rounding, so `0.5` rounds to `1` and `-0.5` rounds to `-1`. Snowflake `ROUND` on `FLOAT` types uses banker’s rounding, which rounds half to even, so results may differ for values exactly at the `.5` boundary.

### Best Practices

- Consider using `NUMERIC` or `DECIMAL` types for deterministic rounding, and verify the converted results against the original mapping for values at the `.5` boundary.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0012

IS\_DATE without format parameter depends on session date format.

### Severity

None

### Description

This functional difference (FDM) is reported when an Informatica `IS_DATE` that has no format parameter is converted. In Informatica this depends on the session date format, which is not migrated, while Snowflake `TRY_TO_DATE` without a format uses the `DATE_INPUT_FORMAT` session parameter, so results may differ.

### Best Practices

- Specify an explicit format string for deterministic behavior, then verify the converted results against the original mapping.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0013

Informatica CASE\_FLAG parameter is not supported in Snowflake.

### Severity

None

### Description

This functional difference (FDM) is reported when an expression that uses the Informatica `CASE_FLAG` parameter for case-insensitive comparison is converted. This parameter is not supported in Snowflake and has been removed from the translated expression, so the equivalent Snowflake operation is always case-sensitive.

### Best Practices

- Consider using `UPPER` or `LOWER` on both sides of the comparison to reproduce case-insensitive behavior, then verify the converted results against the original mapping.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0014

SESSSTARTTIME converted to CURRENT\_TIMESTAMP() which may differ in long-running sessions.

### Severity

None

### Description

This functional difference (FDM) is reported when Informatica `SESSSTARTTIME` is converted to Snowflake `CURRENT_TIMESTAMP`. Informatica `SESSSTARTTIME` returns a static timestamp captured at session initialization, while `CURRENT_TIMESTAMP` returns the current time at each row evaluation, so results may differ in long-running sessions.

### Best Practices

- Verify the converted timestamp values against the original mapping, and capture a single static timestamp where a session start time is required.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0015

The parameter file path requires manual mapping to a Snowflake stage.

### Severity

None

### Description

This functional difference (FDM) is reported when an Informatica PowerCenter mapping that references a parameter file path is converted. This path requires manual mapping to a Snowflake stage, and the original parameter file must be converted to the expected JSON format.

### Best Practices

- Map the parameter file path to an appropriate Snowflake stage and convert the original parameter file to the expected JSON format, then verify the converted behavior matches the original.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0016

Informatica PowerCenter Decision task condition is empty; translated as an unconditional pass-through.

### Severity

None

### Description

This functional difference (FDM) is reported when an Informatica PowerCenter Decision task whose condition is empty is converted. Because there is no condition, the task has been translated as an unconditional pass-through that always evaluates to true, so you should verify the converted behavior matches the original.

### Best Practices

- Verify the intended decision condition against the original mapping and add the explicit condition where a specific branch behavior is required.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0018

Update Strategy overridden by session settings.

### Severity

None

### Description

This functional difference (FDM) is reported when an Informatica PowerCenter mapping in which the Update Strategy was overridden by session settings is converted. Because the session settings take precedence, the effective behavior may differ from the Update Strategy defined in the mapping, so you should verify the converted behavior matches the original.

### Best Practices

- Verify the effective update behavior against the original session settings and mapping, and adjust the converted target logic where needed.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0019

The update strategy logic was moved to the target model.

### Severity

None

### Description

This functional difference (FDM) is reported when an Informatica PowerCenter mapping is converted and the update strategy logic is moved to the target model. Because the logic now lives in the target model, you should verify the converted behavior matches the original.

### Best Practices

- Verify the update strategy behavior in the target model against the original mapping.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0020

Informatica RR date format element has century-guessing logic that differs from Snowflake YY.

### Severity

None

### Description

This functional difference (FDM) is reported when an Informatica `RR` date format element is converted to Snowflake `YY`. The Informatica `RR` element uses century-guessing logic, so `99` maps to `1999` and `25` maps to `2025`, while Snowflake `YY` always maps two-digit years to the current century, so `99` maps to `2099`. You should review date values to ensure correct century interpretation.

### Best Practices

- Review the converted date values to confirm the century is interpreted correctly, and add explicit century handling where needed.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0021

Informatica POWER rounds non-integer exponents when the base is negative; Snowflake raises an error.

### Severity

None

### Description

This functional difference (FDM) is reported when an Informatica `POWER` call that may receive a negative base with a non-integer exponent is converted. Informatica rounds the exponent to the nearest integer before computing, while Snowflake `POWER` raises an invalid floating point operation error for a negative base with a non-integer exponent. You should review expressions that use `POWER` with potentially negative bases and non-integer exponents.

### Best Practices

- Review expressions that use `POWER` with potentially negative bases and non-integer exponents, and add explicit rounding or guards where needed.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0022

Informatica MD5 may produce different hashes due to encoding differences.

### Severity

None

### Description

This functional difference (FDM) is reported when an Informatica `MD5` call is converted. Informatica allows configurable character encoding through the data movement mode property, which can be ASCII or Unicode, while Snowflake always uses UTF-8, so different encodings can produce different `MD5` hashes for the same input string.

### Best Practices

- Verify the converted `MD5` hashes against the original mapping, and align the input encoding to UTF-8 where the hashes must match.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0023

SETMAXVARIABLE/SETMINVARIABLE per-row return value on OUTPUT port may differ from Informatica.

### Severity

None

### Description

This functional difference (FDM) is reported when a `SETMAXVARIABLE` or `SETMINVARIABLE` call on an output port is converted. Informatica accumulates the variable row by row, so rows after a new maximum or minimum reflect the updated value, while Snowflake compares all rows against the same initial value, so per-row return values may differ. The final persisted variable value is equivalent.

### Best Practices

- Verify the per-row return values against the original mapping where downstream logic depends on the accumulated value, keeping in mind the final persisted value is equivalent.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0024

SETVARIABLE persisted value may differ when row order matters.

### Severity

None

### Description

This functional difference (FDM) is reported when a `SETVARIABLE` call is converted. Informatica persists the last row’s value, which is order-dependent, while Snowflake uses a maximum or minimum across all rows instead, so the persisted value may differ when row order matters.

### Best Practices

- Review whether row order affects the expected result, and add explicit ordering where the last-row value must be preserved.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0025

COUNT-based SET\*VARIABLE translated to COUNT(port).

### Severity

None

### Description

This functional difference (FDM) is reported when a `SETVARIABLE` call with the count aggregate function, or a `SETCOUNTVARIABLE` call, is converted to `COUNT` over the port. Informatica counts row-by-row invocations, so if the expression is conditional, results may differ.

### Best Practices

- Verify the converted count against the original mapping, especially where the expression is conditional, and add explicit filtering where needed.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0026

Informatica REG\_REPLACE numReplacements differs from Snowflake REGEXP\_REPLACE occurrence.

### Severity

None

### Description

This functional difference (FDM) is reported when an Informatica `REG_REPLACE` call is converted to Snowflake `REGEXP_REPLACE`. The Informatica number of replacements parameter replaces the first N matches, while the Snowflake occurrence parameter replaces only the Nth match, so only the values `0` for all matches and `1` for the first match are equivalent.

### Best Practices

- Verify the converted replacement behavior against the original mapping, especially when the number of replacements is greater than one.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0027

SYSTIMESTAMP format argument dropped. Snowflake CURRENT\_TIMESTAMP() always returns full precision.

### Severity

None

### Description

In Informatica PowerCenter the `SYSTIMESTAMP` format argument controls the returned precision, such as seconds, milliseconds, microseconds, or nanoseconds. Snowflake `CURRENT_TIMESTAMP()` always returns nanosecond precision, so the format argument is dropped because Snowflake provides a superset of that precision. Verify any downstream logic that may depend on the previously truncated precision.

### Best Practices

- Verify downstream logic that depends on the truncated precision the format argument previously provided.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0028

Informatica reusable transformation may be duplicated across dbt projects.

### Severity

None

### Description

This transformation is reusable in Informatica PowerCenter, and it is converted into separate dbt models in each mapping where it is used, which results in duplicated logic. Consider consolidating the shared logic into a single dbt macro or package for easier maintenance.

### Best Practices

- Consolidate the duplicated logic into a shared dbt macro or package to improve maintainability.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0029

Multiple targets to the same table merged with UNION ALL.

### Severity

None

### Description

Informatica PowerCenter loads targets sequentially according to the target load order. The translated dbt model uses `UNION ALL` to combine all pipelines into a single atomic query, so this functional difference is reported so you can verify the converted behavior matches the original. If the pipeline execution order affects the final result, review the generated model.

### Best Practices

- Review the generated dbt model if the pipeline execution order affects the final result.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0030

Informatica PERCENTILE uses a different interpolation algorithm than Snowflake PERCENTILE\_CONT.

### Severity

None

### Description

Informatica PowerCenter `PERCENTILE` uses the interpolation formula `I=(X+1)*P/100`, while Snowflake `PERCENTILE_CONT` uses `I=P*(N-1)`. Because the two interpolation algorithms differ, they can produce different numeric results for the same input data.

### Best Practices

- Verify that the numeric results produced by `PERCENTILE_CONT` are acceptable for your data.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0031

Informatica PowerCenter Email task sender address differs in Snowflake.

### Severity

None

### Description

The Informatica PowerCenter Email task sends mail through the Integration Service using MAPI or SMTP. Snowflake uses `SYSTEM$SEND_EMAIL`, which sends from the fixed address `no-reply@snowflake.net` and does not allow the sender address to be customized. Recipients must be verified Snowflake account users.

### Best Practices

- Confirm that all recipients are verified Snowflake account users and that the fixed sender address is acceptable.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0032

Informatica FIRST translated to ANY\_VALUE approximation.

### Severity

None

### Description

The Informatica PowerCenter `FIRST` function returns the value from the first row processed in pipeline order, and it is approximated with `ANY_VALUE`. Because `ANY_VALUE` does not guarantee a specific row, add an explicit `ORDER BY` or `QUALIFY` clause if deterministic first-row semantics are required.

### Best Practices

- Add an explicit `ORDER BY` or `QUALIFY` clause if you require deterministic first-row semantics.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0033

Informatica LAST translated to ANY\_VALUE approximation.

### Severity

None

### Description

The Informatica PowerCenter `LAST` function returns the value from the last row processed in pipeline order, and it is approximated with `ANY_VALUE`. Because `ANY_VALUE` does not guarantee a specific row, add an explicit `ORDER BY` or `QUALIFY` clause if deterministic last-row semantics are required.

### Best Practices

- Add an explicit `ORDER BY` or `QUALIFY` clause if you require deterministic last-row semantics.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0045

Java Transformation contains custom Java code that cannot be automatically translated.

### Severity

None

### Description

This Java Transformation contains custom Java code that cannot be automatically translated. The Java code snippets must be manually migrated to Snowflake, for example as a Java UDF, a Snowpark procedure, or inline SQL. Pass-through columns are forwarded, but the Java logic is not applied.

### Best Practices

- Manually migrate the custom Java logic to a Snowflake Java UDF, a Snowpark procedure, or inline SQL.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0046

SETCOUNTVARIABLE row ordering is non-deterministic.

### Severity

None

### Description

The Informatica PowerCenter `SETCOUNTVARIABLE` is translated to `ROW_NUMBER() OVER (ORDER BY 1)`. This row ordering is non-deterministic and may differ from Informatica’s pipeline-processing order, so add a deterministic `ORDER BY` if stable row numbering is required.

### Best Practices

- Add a deterministic `ORDER BY` if you require stable row numbering.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0047

STDDEV returns NULL in Snowflake for single-record groups, whereas Informatica returns 0.

### Severity

None

### Description

Informatica PowerCenter `STDDEV` returns 0 for single-record groups because there is no variance. Snowflake `STDDEV` returns NULL because the sample standard deviation is undefined for a group of one row. Verify downstream logic that depends on `STDDEV` returning 0 for single-row groups.

### Best Practices

- Verify downstream logic that depends on `STDDEV` returning 0 for single-row groups.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0048

IS\_SPACES does not match vertical tab (0x0B) in Snowflake.

### Severity

None

### Description

Informatica PowerCenter `IS_SPACES` treats the vertical tab character, `CHR(11)` or `0x0B`, as whitespace, but the Snowflake `REGEXP_LIKE` pattern `\s` does not match it. This difference only affects data that contains vertical tab characters.

### Best Practices

- Review whether your data contains vertical tab characters that `IS_SPACES` would have matched.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0049

Informatica CRC32 uses ASCII encoding; Snowflake CRC32\_UDF uses UTF-8.

### Severity

None

### Description

Informatica PowerCenter `CRC32` computes the checksum over ASCII-encoded bytes, while the generated `CRC32_UDF` processes the input as UTF-8. For strings that contain only ASCII characters the results are identical, but for strings with non-ASCII characters the checksum values will differ. Review the input data and verify that the function output is acceptable.

### Best Practices

- Review the input data and verify the checksum output is acceptable for strings that contain non-ASCII characters.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0057

Source Qualifier SQL converted using non-default dialect.

### Severity

None

### Description

The SQL in this Source Qualifier was converted using a dialect other than the default dialect. This functional difference is reported so you can verify the converted behavior matches the original.

### Best Practices

- Review the converted SQL to confirm that the chosen dialect produces the intended behavior.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0058

Table is used as both source and target.

### Severity

None

### Description

This table is used as both a source and a target in the same mapping. The dbt execution order was adjusted to prevent circular data corruption, so review the staging and mart models for the details.

### Best Practices

- Review the generated staging and mart models to confirm the adjusted execution order is correct.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0059

Local variable expression inlined into lookup macro argument; keep both copies in sync.

### Severity

None

### Description

A local variable expression was inlined into a lookup macro argument because outer select-list aliases are not visible inside the macro’s correlated subquery. If you edit the local variable’s expression in the column list, also update the matching macro argument so the two copies stay in sync.

### Best Practices

- If you edit the local variable’s expression in the column list, also update the matching macro argument to keep the two copies in sync.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0060

The Informatica PowerCenter task was disabled in the source workflow and the converted Snowflake task has been suspended.

### Severity

None

### Description

This Informatica PowerCenter task was disabled in the source workflow. The converted Snowflake task has been suspended with `ALTER TASK ... SUSPEND` to preserve the task graph while preventing execution.

### Best Practices

- Confirm that the task should remain suspended, or resume it if it needs to run.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0061

Connected Lookup with ‘Use All Values’ policy fans out rows.

### Severity

None

### Description

This Connected Lookup uses the multi-match policy ‘Use All Values’, and the translation emits a join against the lookup table. Because every matching row is returned, the row count may increase.

### Best Practices

- Review the join output because the row count may increase.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0062

$PMRepositoryUserName translated to CURRENT\_USER() - identity model differs.

### Severity

None

### Description

Informatica PowerCenter `$PMRepositoryUserName` returns the PowerCenter repository connection user configured on the Integration Service, while Snowflake `CURRENT_USER()` returns the session user, which is typically the dbt service account. Both values are usually constant per environment, but they represent different identity spaces. Verify audit columns, predicates that filter on an owner, and incremental merge keys that reference this value.

### Best Practices

- Verify audit columns, predicates, and incremental merge keys that reference this value.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0063

The session-level connection override could not be resolved to a Snowflake database.

### Severity

None

### Description

A session-level connection override could not be resolved to a Snowflake database because the connection is not present in the exported XML. Set the database override variables, which use the `_db` suffix, to the real database.

### Best Practices

- Set the `_db` override variables to the real Snowflake database.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0064

Assignment target variable type may behave differently at runtime.

### Severity

None

### Description

The assignment target variable has a source type that was mapped to a Snowflake type. This mapping may lose precision, such as decimal scale, or may require format-dependent parsing for date and time values, so verify the runtime behavior.

### Best Practices

- Verify the runtime behavior of the mapped Snowflake type for possible precision loss or format-dependent parsing.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0068

Expression Lagger Technique ORDER BY inferred from an upstream Source Qualifier.

### Severity

None

### Description

The Lagger Technique `ORDER BY` was inferred from an upstream Source Qualifier instead of from a Sorter transformation. Validate that the inferred ordering columns are the intended row order for the `LAG` window function.

### Best Practices

- Validate that the inferred ordering columns are the intended row order for the `LAG` window function.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0069

Union input group with unresolved upstream lineage emitted as a no-row null branch.

### Severity

None

### Description

A Union input group could not be resolved to an upstream transformation, for example a Router default or others branch that has no downstream connector. Its columns are emitted as NULL literals with no rows, using `LIMIT 0`. Verify that the branch is intentionally unconnected rather than an unresolved-lineage defect.

### Best Practices

- Verify that the branch is intentionally unconnected rather than an unresolved-lineage defect.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0070

Use Any Value returns an arbitrary row; in Snowflake the selected row may vary per run.

### Severity

None

### Description

The ‘Use Any Value’ policy returns an arbitrary row when multiple rows match, and in Snowflake the selected row may vary from one run to the next. Add an `ORDER BY` to the lookup SQL override only if a specific row is required.

### Converted Code

Copy code

```
QUALIFY
   ROW_NUMBER() OVER (
   PARTITION BY
      CurrencyKey
   ORDER BY
      (
         SELECT
            --** SSC-FDM-INF0070 - Use Any Value RETURNS AN ARBITRARY ROW WHEN MULTIPLE ROWS MATCH; IN SNOWFLAKE THE SELECTED ROW MAY VARY PER RUN. ADD AN ORDER BY TO THE LOOKUP SQL OVERRIDE ONLY IF A SPECIFIC ROW IS REQUIRED. **
            null
      )) = 1
```

### Best Practices

- Add an `ORDER BY` to the lookup SQL override only if a specific row is required.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0071

To run this task graph concurrently with different parameter files, set OVERLAP\_POLICY.

#### Description

This issue is reported on the root task of a parameterized task graph. Informatica can run the same workflow concurrently with different parameter files, but Snowflake defaults to `NO_OVERLAP` and coalesces concurrent `EXECUTE TASK` calls, so those runs are serialized instead of running in parallel.

This is one-time deployment guidance rather than a per-task annotation, so it is surfaced in the ETL issues report and is deliberately not stamped as a comment on the generated task DDL.

#### Code Example

##### Input Code:

##### Informatica

Copy code

```
<ATTRIBUTE NAME ="Parameter Filename" VALUE ="C:&#x5c;Users&#x5c;Administrator&#x5c;Desktop&#x5c;params.txt"/>
```

##### Output Code:

##### Snowflake

```
SessionID,Severity,Code,Name,Description,ParentFileName,ComponentFullName,MigrationID
test-session-id,None,SSC-FDM-INF0071,"To run this task graph concurrently with different parameter files, set OVERLAP_POLICY.","TO ENABLE CONCURRENT PARAMETERIZED RUNS OF THIS TASK GRAPH WITH DIFFERENT 'run_id' VALUES, RUN: ALTER TASK public.VARIABLESWORKFLOW_PRMFILE_WF_LEVEL SET OVERLAP_POLICY = ALLOW_ALL_OVERLAP. WITHOUT THIS, SNOWFLAKE COALESCES CONCURRENT EXECUTE TASK CALLS (NO_OVERLAP, THE DEFAULT) AND THE RUNS DO NOT EXECUTE IN PARALLEL.",../folder/Informatica/InfPc_Source.xml,VARIABLESWORKFLOW_PRMFILE_WF_LEVEL,Not Provided
```

#### Best Practices

- Run `ALTER TASK <root_task> SET OVERLAP_POLICY = ALLOW_ALL_OVERLAP` when the task graph must execute concurrently with different `run_id` values.
- Keep the default `NO_OVERLAP` when concurrent runs would write to the same targets, because overlapping executions can interleave their loads.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0076

ROUND on a floating-point value was cast to NUMERIC to match Informatica’s exact-decimal rounding; large-magnitude values may still differ.

### Severity

None

### Description

A `ROUND` applied to a floating-point value was cast to `NUMERIC` so the result matches Informatica’s exact-decimal rounding. Even with this cast, large-magnitude values may still differ, so verify the converted results.

### Best Practices

- Review large-magnitude values because the rounding results may still differ from Informatica.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0077

Informatica scheduler could not be translated to a Snowflake CRON schedule.

#### Description

This issue is reported when an Informatica scheduler configuration has no CRON equivalent, for example a monthly repeat type. The task is emitted without a `SCHEDULE` clause, so it never runs on its own and must be scheduled manually or triggered by another task.

#### Code Example

##### Input Code:

##### Informatica

Copy code

```
<REPEAT INTERVAL ="1" TYPE ="MONTHLY"/>
```

##### Output Code:

##### Snowflake

Copy code

```
--** SSC-FDM-INF0077 - SCHEDULE COULD NOT BE TRANSLATED: Repeat type 'MONTHLY' is not supported for CRON translation. THE TASK WAS EMITTED WITHOUT A SCHEDULE CLAUSE AND MUST BE SCHEDULED MANUALLY. **
CREATE OR REPLACE TASK public.wf_Sales_Order_Status
AS
SELECT
   1;
```

#### Best Practices

- Add a `SCHEDULE = 'USING CRON ...'` clause that reproduces the original scheduler, or trigger the root task from an external orchestrator.
- Resume the task after scheduling it, because a task created without a schedule stays suspended until it is started explicitly.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0078

A default timezone was assumed for the root task SCHEDULE clause.

#### Description

This issue is reported when it builds the root task `SCHEDULE` clause from an Informatica start time. Informatica start times carry no timezone, so a default timezone is assumed and the converted task may fire at a different wall-clock time than the original workflow if the source server used another timezone.

#### Code Example

##### Input Code:

##### Informatica

Copy code

```
<STARTOPTIONS STARTDATE ="7/18/2017" STARTTIME ="08:00"/>
<REPEAT INTERVAL ="1" TYPE ="DAILY"/>
```

##### Output Code:

##### Snowflake

Copy code

```
--** SSC-FDM-INF0078 - DEFAULT TIMEZONE 'America/Toronto' WAS ASSUMED FOR THE ROOT TASK SCHEDULE; INFORMATICA STARTTIME HAS NO TIMEZONE. OVERRIDE WITH --task-schedule-timezone IF THE SOURCE SERVER USES A DIFFERENT TIMEZONE. **
CREATE OR REPLACE TASK public.wf_Sales_Order_Status
SCHEDULE='USING CRON 0 8 * * * America/Toronto'
AS
SELECT
   1;
```

#### Best Practices

- Re-run the conversion with `--task-schedule-timezone` set to the timezone of the Informatica server when it differs from the assumed default.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0079

Dynamic lookup cache NewLookupRow is generated set-based; identical duplicate new-key rows dedup to one insert, but without input arrival order the insert/update choice among differing duplicates, in-batch cached-key updates, case-insensitive matching, and surrogate keys are not reproduced.

#### Description

This issue is reported when a connected lookup uses a dynamic cache. PowerCenter updates the cache row by row in arrival order, while the generated SQL computes `NewLookupRow` set-based over the whole batch. Row counts match for identical duplicates, but the insert-versus-update choice among differing duplicates, updates against keys cached earlier in the same batch, case-insensitive matching, and surrogate key generation are not reproduced.

#### Code Example

##### Input Code:

##### Informatica

Copy code

```
<TRANSFORMFIELD DATATYPE ="integer" NAME ="NewLookupRow" PORTTYPE ="DYNLOOKUP/OUTPUT" PRECISION ="10" SCALE ="0"/>
<TABLEATTRIBUTE NAME ="Dynamic Lookup Cache" VALUE ="YES"/>
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT
   lookup_reference.SK_ID,
   input_data.CUST_CODE_In CUST_CODE,
   input_data.CUST_NAME_In CUST_NAME
FROM
   --** SSC-FDM-INF0079 - CONNECTED LOOKUP 'LKP_Customer' DYNAMIC CACHE: NEWLOOKUPROW IS SET-BASED. IDENTICAL DUPLICATE NEW-KEY ROWS DEDUP TO ONE INSERT; WITHOUT ARRIVAL ORDER, INSERT/UPDATE AMONG DIFFERING DUPLICATES, CACHED-KEY UPDATES, CASE-INSENSITIVE MATCH & SURROGATE KEYS DIFFER. VERIFY ROWS. **
   input_data
   LEFT JOIN
      lookup_reference
      ON lookup_reference.CUST_CODE = input_data.CUST_CODE_In
```

#### Best Practices

- Verify the resulting rows against a PowerCenter run, paying attention to batches that contain several rows for the same lookup key.
- Where the mapping relied on the dynamic cache to generate surrogate keys, replace that behavior with an explicit Snowflake sequence or a deterministic key expression.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0080

VARIANCE returns NULL in Snowflake for single-record groups, whereas Informatica returns 0.

#### Description

This issue is reported when an Informatica `VARIANCE` aggregation is translated to Snowflake `VAR_SAMP`. Informatica returns `0` for a group that contains a single record, while Snowflake returns `NULL` because the sample variance is undefined for one row.

The marker is suppressed when the grouped aggregator renderer wraps the aggregate in its `IFF(COUNT(<port>) = 1, 0, ...)` zero-guard, because that guard already reproduces the Informatica single-record result.

#### Code Example

##### Input Code:

##### Informatica

Copy code

```
<TRANSFORMFIELD DATATYPE ="decimal" EXPRESSION ="VARIANCE(SALARY)" NAME ="VARSALARY" PORTTYPE ="OUTPUT" PRECISION ="18" SCALE ="6"/>
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT
   --** SSC-FDM-INF0080 - INFORMATICA VARIANCE RETURNS 0 FOR SINGLE-RECORD GROUPS. SNOWFLAKE VAR_SAMP RETURNS NULL BECAUSE SAMPLE VARIANCE IS UNDEFINED FOR N=1. VERIFY DOWNSTREAM LOGIC THAT DEPENDS ON VARIANCE RETURNING 0 FOR SINGLE-ROW GROUPS. **
   VAR_SAMP(SALARY) AS VARSALARY
FROM
   source_data
```

#### Best Practices

- Wrap the aggregation as `IFNULL(VAR_SAMP(...), 0)` when downstream logic depends on `0` being returned for single-row groups.
- Check for divisions, comparisons, or filters over the variance result, because a `NULL` propagates differently than `0`.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0081

Lookup table name override references a variable with no resolvable value.

#### Description

This issue is reported when a session-level Lookup table name override points to a variable that has no value at conversion time. Because the runtime table cannot be determined, the override is not applied and the generated lookup reads the table declared in the mapping instead.

The issue is raised against the four-part session caller (`folder.workflow.session.lookup`) in the ETL issues report rather than as an inline marker in the generated lookup model.

#### Code Example

##### Input Code:

##### Informatica

Copy code

```
<ATTRIBUTE NAME ="Lookup table name" VALUE ="$$LKP_ENV"/>
<MAPPINGVARIABLE AGGFUNCTION ="COUNT" DATATYPE ="nstring" DEFAULTVALUE ="" DESCRIPTION ="" ISEXPRESSIONVARIABLE ="NO" ISPARAM ="YES" NAME ="$$LKP_ENV" PRECISION ="20" SCALE ="0" USERDEFINED ="YES"/>
```

##### Output Code:

##### Snowflake

```
Code:              SSC-FDM-INF0081
Severity:          None
ComponentFullName: LkpFolder.wf_lkp.s_lkp.t_lkp
Description:       THE SESSION LOOKUP TABLE NAME OVERRIDE FOR LOOKUP 't_lkp' REFERENCES VARIABLE '$$LKP_ENV' WHICH HAS NO RESOLVABLE VALUE AT CONVERSION TIME, SO THE RUNTIME LOOKUP TABLE CANNOT BE DETERMINED. PROVIDE A VALUE FOR THE VARIABLE OR SET THE LOOKUP TABLE NAME EXPLICITLY.
```

#### Best Practices

- Provide a value for the variable in the parameter file included in the conversion, or set the lookup table name explicitly in the mapping.
- Confirm which table the generated lookup reads before running it, so the lookup does not silently resolve to the pre-override table.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0082

Sorter Distinct with Case Sensitive = NO may retain a different case variant than PowerCenter.

#### Description

This issue is reported when a Sorter with `Distinct` and `Case Sensitive = NO` is translated to a case-folded `QUALIFY ROW_NUMBER()` deduplication. The row count matches PowerCenter, but PowerCenter keeps the first row in arrival order, so the casing of the surviving row may differ.

#### Code Example

##### Input Code:

##### Informatica

Copy code

```
<TABLEATTRIBUTE NAME="Case Sensitive" VALUE="NO"/>
<TABLEATTRIBUTE NAME="Distinct" VALUE="YES"/>
```

##### Output Code:

##### Snowflake

Copy code

```
--** SSC-FDM-INF0082 - SORTER DISTINCT WITH CASE SENSITIVE = NO DEDUPLICATES ROWS THAT DIFFER ONLY IN CHARACTER CASE. THE ROW COUNT MATCHES POWERCENTER, BUT THE SURVIVING ROW'S CASING MAY DIFFER BECAUSE POWERCENTER KEEPS THE FIRST ROW IN ARRIVAL ORDER. VERIFY THAT DOWNSTREAM LOGIC DOES NOT DEPEND ON THE RETAINED CASING. **
CREATE OR REPLACE TEMPORARY TABLE tmp_srttrans AS
   SELECT
      EMPNAME,
      DEPTCODE
   FROM
      tmp_sq_sorter_distci_src
   QUALIFY
      ROW_NUMBER() OVER (
      PARTITION BY
         LOWER(EMPNAME), LOWER(DEPTCODE)
      ORDER BY
         EMPNAME ASC NULLS LAST,
         DEPTCODE ASC NULLS LAST) = 1
   ORDER BY
      LOWER(EMPNAME) ASC NULLS LAST,
      LOWER(DEPTCODE) ASC NULLS LAST
```

#### Best Practices

- Verify that downstream logic does not depend on the retained casing; if it does, normalize the column explicitly with `UPPER` or `LOWER` so the result is deterministic.
- Change the `ORDER BY` inside the window to a column that identifies the preferred variant when a specific case must survive.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0084

Static DD\_REJECT with Forward Rejected Rows=NO writes nothing, so no target DML was generated.

#### Description

This issue is reported when an Update Strategy expression statically resolves to `DD_REJECT` and `Forward Rejected Rows` is `NO`. Every row is dropped at the Update Strategy boundary, so no target DML is generated at all and the target position carries only this marker.

#### Code Example

##### Input Code:

##### Informatica

Copy code

```
<TABLEATTRIBUTE NAME ="Update Strategy Expression" VALUE ="DD_REJECT"/>
<TABLEATTRIBUTE NAME ="Forward Rejected Rows" VALUE ="NO"/>
```

##### Output Code:

##### Snowflake

Copy code

```
---- Start block 'UpdateStrategy_SNOW_3702850.m_UpdateStrategy_RejectNoFwd.us_rejn_tgt'
--** SSC-FDM-INF0084 - THE UPDATE STRATEGY EXPRESSION STATICALLY RESOLVES TO DD_REJECT AND FORWARD REJECTED ROWS IS NO, SO ALL ROWS ARE DROPPED AT THE UPDATE STRATEGY BOUNDARY AND NO TARGET DML WAS GENERATED. **

---- End block 'UpdateStrategy_SNOW_3702850.m_UpdateStrategy_RejectNoFwd.us_rejn_tgt'
```

#### Best Practices

- Confirm that dropping every row was intended; if the Update Strategy expression was meant to be data-driven, correct it in the source mapping and convert again.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0085

Rank Transformation: tied rank-port values at the QUALIFY boundary may produce a different survivor than PowerCenter.

#### Description

This issue is reported when a Rank transformation is translated to a `ROW_NUMBER()` window with a `QUALIFY` boundary. PowerCenter breaks ties on the rank port by input arrival order, which Snowflake cannot reproduce without a stable row-identity key, so when the n-th position is tied the surviving rows may differ.

#### Code Example

##### Input Code:

##### Informatica

Copy code

```
<TRANSFORMFIELD DATATYPE ="decimal" EXPRESSION ="sales_amount" EXPRESSIONTYPE ="RANKPORT" NAME ="sales_amount" PORTTYPE ="INPUT/OUTPUT" PRECISION ="19" SCALE ="2"/>
<TABLEATTRIBUTE NAME ="Top/Bottom" VALUE ="TOP"/>
<TABLEATTRIBUTE NAME ="Number of Ranks" VALUE ="5"/>
```

##### Output Code:

##### Snowflake

Copy code

```
INSERT INTO YOUR_DB.YOUR_SCHEMA.RANK_TOPN_TGT (product_id, product_name, sales_amount, rank_pos)
WITH
--** SSC-FDM-INF0085 - RANK TRANSFORMATION: WHEN MULTIPLE INPUT ROWS HAVE THE SAME RANK-PORT VALUE AT THE QUALIFY BOUNDARY, POWERCENTER BREAKS TIES BY INPUT ROW ARRIVAL ORDER. SNOWFLAKE'S ROW_NUMBER() WINDOW DOES NOT GUARANTEE ARRIVAL-ORDER TIEBREAKING WITHOUT A STABLE ROW-IDENTITY KEY. IF INPUT DATA HAS TIED VALUES AT THE N-TH POSITION, THE SURVIVING ROW(S) MAY DIFFER FROM POWERCENTER. VERIFY THAT TIED INPUT DATA DOES NOT OCCUR OR THAT DOWNSTREAM LOGIC IS INSENSITIVE TO THE TIE SURVIVOR. **
cte_rnk_topn AS
(
   WITH source_data AS
   (
      SELECT
         product_id,
         product_name,
         sales_amount
      FROM
         tmp_sq_rank_topn_src
   )
   SELECT
      product_id AS product_id,
      product_name AS product_name,
      sales_amount AS sales_amount,
      ROW_NUMBER() OVER (ORDER BY sales_amount DESC) AS RANKINDEX
   FROM
      source_data
   QUALIFY
      RANKINDEX <= 5
)
```

#### Best Practices

- Add a stable tiebreaker column to the window `ORDER BY` — for example a primary key — so the survivor is deterministic between runs.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0086

Pre/post-session command task was not translated (no Snowflake/dbt equivalent).

#### Description

This issue is reported when a session declares a pre-session or post-session command. Those commands run OS-level shell instructions, which have no Snowflake or dbt equivalent, so the generated task keeps only the dbt invocation and the command itself must be migrated manually.

#### Code Example

##### Input Code:

##### Informatica

Copy code

```
<SESSIONCOMPONENT REFOBJECTNAME ="pre_session_command" REUSABLE ="NO" TYPE ="Pre-session command">
    <VALUEPAIR NAME ="Command1" REVERSEASSIGNMENT ="NO" VALUE ="cp $PMRootDir/input/dsi_input.xml $PMRootDir/work/dsi_input.xml"/>
</SESSIONCOMPONENT>
```

##### Output Code:

##### Snowflake

Copy code

```
BEGIN
   ---- Start block 'ETL.wf_precmd.s_precmd'
   --** SSC-FDM-INF0086 - PRE/POST-SESSION COMMAND TASK WAS NOT TRANSLATED. THE OS-LEVEL SHELL COMMAND HAS NO SNOWFLAKE/DBT EQUIVALENT AND MUST BE MIGRATED MANUALLY. **
   EXECUTE DBT PROJECT public.m_precmd ARGS='build --target dev';
   ---- End block 'ETL.wf_precmd.s_precmd'

END;
```

#### Best Practices

- Reimplement the shell command with a Snowflake-native mechanism where one exists, for example a stage operation, an external function, or an external orchestrator step around the task graph.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0087

Aggregator port has no incoming connector; value replaced with NULL.

#### Description

This issue is reported when an Aggregator port has no incoming connector in the source mapping. Informatica would substitute the port’s default value at run time — `NULL` when the default is blank — while the converted output projects a typed `NULL` for that column instead.

#### Code Example

##### Input Code:

##### Informatica

Copy code

```
<TRANSFORMFIELD DATATYPE ="string" DEFAULTVALUE ="" EXPRESSION ="REGIONCODE" EXPRESSIONTYPE ="GROUPBY" NAME ="REGIONCODE" PORTTYPE ="INPUT/OUTPUT" PRECISION ="10" SCALE ="0"/>
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT
   DEPTCODE AS DEPTCODE,
   --** SSC-FDM-INF0087 - AGGREGATOR PORT 'REGIONCODE' HAS NO INCOMING CONNECTOR IN THE SOURCE MAPPING. INFORMATICA WOULD SUBSTITUTE THE PORT'S DEFAULT VALUE (NULL WHEN BLANK) AT RUNTIME; THE CONVERTED OUTPUT PROJECTS A TYPED NULL FOR THIS COLUMN INSTEAD. VERIFY THE SOURCE MAPPING FOR A MISSING OR REMOVED CONNECTION. **
   NULL :: VARCHAR(10) AS REGIONCODE,
   CAST(SUM(SALARY) AS NUMBER(18,2)) AS SUMSALARY,
   CAST(MIN(SC_ROW_ID) AS NUMBER(10,0)) AS MINROWID
FROM
   source_data
GROUP BY
   DEPTCODE
```

#### Best Practices

- Check the source mapping for a missing or removed connection; if the port had a non-blank default value, replace the projected `NULL` with that value.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0088

Connected lookup uses case-insensitive string comparison, but the emitted join condition is case-sensitive. Lookup matches may differ from PowerCenter.

#### Description

This issue is reported when a connected lookup has `Case Sensitive String Comparison = NO`. The generated join predicate uses a case-sensitive `=`, so rows that PowerCenter would have matched with different casing do not match in Snowflake.

#### Code Example

##### Input Code:

##### Informatica

Copy code

```
<TABLEATTRIBUTE NAME ="Dynamic Lookup Cache" VALUE ="YES"/>
<TABLEATTRIBUTE NAME ="Case Sensitive String Comparison" VALUE ="NO"/>
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT
   lookup_reference.SK_ID,
   input_data.CUST_CODE_In CUST_CODE,
   input_data.CUST_NAME_In CUST_NAME
FROM
   --** SSC-FDM-INF0088 - CONNECTED LOOKUP 'LKP_Customer' USES CASE-INSENSITIVE STRING COMPARISON ('CASE SENSITIVE STRING COMPARISON' = NO), BUT THE EMITTED JOIN CONDITION IS CASE-SENSITIVE. LOOKUP MATCHES MAY DIFFER FROM POWERCENTER. **
   input_data
   LEFT JOIN
      lookup_reference
      ON lookup_reference.CUST_CODE = input_data.CUST_CODE_In
```

#### Best Practices

- Fold both sides of the join predicate — for example `UPPER(lookup_reference.CUST_CODE) = UPPER(input_data.CUST_CODE_In)` — when case-insensitive matching is required, and keep in mind that folding prevents some join pruning.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0089

TRUNC was applied to a string argument and a numeric truncation was assumed.

#### Description

This issue is reported when single-argument `TRUNC` is applied to a string port. A numeric truncation is assumed, so numeric text is coerced correctly, but text holding a date fails at run time because Snowflake’s `DATE_TRUNC` does not accept `VARCHAR`.

#### Code Example

##### Input Code:

##### Informatica

```
TRUNC(STR_COL)
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT
   STR_COL AS STR_COL,
   --** SSC-FDM-INF0089 - TRUNC WAS APPLIED TO A STRING ARGUMENT AND A NUMERIC TRUNCATION WAS ASSUMED. NUMERIC TEXT IS COERCED, BUT DATE TEXT FAILS AT RUN TIME; DATE_TRUNC DOES NOT ACCEPT VARCHAR, SO IF THE VALUE IS A DATE USE DATE_TRUNC('DAY', TO_DATE(...)). **
   TRUNC(STR_COL) AS OUT_COL
FROM
   source_data
```

#### Best Practices

- Rewrite the call as `DATE_TRUNC('DAY', TO_DATE(STR_COL))` when the string holds date text, and leave the numeric `TRUNC` in place only when the column really holds numbers.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0090

TRUNC argument data type could not be determined and a numeric truncation was assumed.

#### Description

This issue is reported when the data type of a single-argument `TRUNC` argument cannot be determined from the mapping. A numeric truncation is assumed, which is wrong if the argument is actually a date, a timestamp, or a string holding date text.

#### Code Example

##### Input Code:

##### Informatica

```
TRUNC(AMOUNT)
```

##### Output Code:

##### Snowflake

Copy code

```
--** SSC-FDM-INF0090 - TRUNC argument data type could not be determined; numeric truncation assumed
TRUNC(AMOUNT)
```

#### Best Practices

- Replace the call with `DATE_TRUNC('DAY', ...)` when the argument is a date or timestamp, and with `DATE_TRUNC('DAY', TO_DATE(...))` when it is a string holding date text.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0091

Target table name prefix has more qualifiers than a Snowflake table location supports; only the last two were applied.

#### Description

This issue is reported when the target’s `Table Name Prefix` contains more qualifiers than a Snowflake table location accepts. Only the last two qualifiers are applied, as database and schema, so the extra leading qualifiers are dropped from the generated model configuration.

#### Code Example

##### Input Code:

##### Informatica

Copy code

```
<TABLEATTRIBUTE NAME ="Table Name Prefix" VALUE ="EXTRA.MYWAREHOUSE.STAGING"/>
```

##### Output Code:

##### Snowflake

Copy code

```
{{ config(
    database='MYWAREHOUSE',
    schema='STAGING'
) }}
--** SSC-FDM-INF0091 - THE TARGET 'D_TABLE_3' TABLE NAME PREFIX 'EXTRA.MYWAREHOUSE.STAGING' HAS MORE QUALIFIERS THAN A SNOWFLAKE TABLE LOCATION SUPPORTS. ONLY THE LAST TWO WERE APPLIED AS DATABASE AND SCHEMA. VERIFY THE TARGET LOCATION. **
```

#### Best Practices

- Verify that the applied database and schema are the intended target location, and simplify the `Table Name Prefix` in the source mapping to at most two qualifiers.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0092

Target table name prefix is a mapping variable; dbt resolves it at compile time.

#### Description

This issue is reported when the target’s `Table Name Prefix` resolves from a mapping variable. Informatica resolves that variable per session from the parameter file, while dbt resolves it once at compile time from `--vars`, so a single compiled project cannot switch schemas between runs the way the session did.

#### Code Example

##### Input Code:

##### Informatica

Copy code

```
<TABLEATTRIBUTE NAME ="Table Name Prefix" VALUE ="$$TGTSCHEMA"/>
<MAPPINGVARIABLE AGGFUNCTION ="MAX" DATATYPE ="string" DEFAULTVALUE ="dbox" ISEXPRESSIONVARIABLE ="NO" ISPARAM ="NO" NAME ="$$TGTSCHEMA" PRECISION ="10" SCALE ="0" USERDEFINED ="YES"/>
```

##### Output Code:

##### Snowflake

Copy code

```
{{ config(
    schema=var('TGTSCHEMA')
) }}
--** SSC-FDM-INF0092 - THE TARGET 'D_TABLE_3' TABLE NAME PREFIX RESOLVES FROM MAPPING VARIABLE 'TGTSCHEMA'. INFORMATICA RESOLVES IT PER SESSION FROM THE PARAMETER FILE WHILE DBT RESOLVES IT ONCE AT COMPILE TIME FROM '--vars'. VERIFY THE VALUE BEFORE RUNNING. **
```

#### Best Practices

- Verify the value passed through `--vars` before each run, and compile separate invocations when different sessions used different schemas.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0093

Target table name prefix names a variable with no conversion-time value; the schema was not applied.

#### Description

This issue is reported when the target’s `Table Name Prefix` names a variable that has no value at conversion time. No `config()` block is generated for the location, so the model lands in the default database and schema of the dbt profile instead of the intended target.

#### Code Example

##### Input Code:

##### Informatica

Copy code

```
<TABLEATTRIBUTE NAME ="Table Name Prefix" VALUE ="$$TGTSCHEMA"/>
```

##### Output Code:

##### Snowflake

Copy code

```
--** SSC-FDM-INF0093 - THE TARGET 'D_TABLE_3' TABLE NAME PREFIX RESOLVES FROM VARIABLE 'TGTSCHEMA', WHICH HAS NO VALUE AT CONVERSION TIME, SO THE TARGET SCHEMA WAS NOT APPLIED. SET THE SCHEMA EXPLICITLY BEFORE RUNNING. **
WITH source_data AS
(
   SELECT
      DeptName
   FROM
      {{ ref('stg_raw__SQ_Tbg_Departments') }}
)
SELECT
   sd.DeptName AS TXT
FROM
   source_data AS sd
```

#### Best Practices

- Set the schema explicitly in the generated model, or include the parameter file that declares the variable in the conversion so the prefix can be resolved.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0094

A session variable assignment was dropped: its variable could not be resolved.

#### Description

This issue is reported when a pre-session or post-session-success variable assignment cannot be resolved against the session’s mapping. The assignment is not translated, so the target variable keeps its previous value at run time instead of being updated.

Because the assignment produces no statement in the generated orchestration, there is nothing to annotate inline, and the drop is reported in the ETL issues report instead.

#### Code Example

##### Input Code:

##### Informatica

Copy code

```
<SESSIONCOMPONENT REFOBJECTNAME ="postsession_success_variable_assignment" REUSABLE ="NO" TYPE ="Post-session success variable assignment">
    <VALUEPAIR EXECORDER ="1" NAME ="$$Wf_Max_Batch_Id" REVERSEASSIGNMENT ="NO" VALUE ="$$Not_A_Mapping_Var"/>
</SESSIONCOMPONENT>
```

##### Output Code:

##### Snowflake

```
SessionID,Severity,Code,Name,Description,ParentFileName,ComponentFullName,MigrationID
test-session-id,None,SSC-FDM-INF0094,A session variable assignment was dropped: its variable could not be resolved.,A SESSION VARIABLE ASSIGNMENT (PRE-SESSION OR POST-SESSION SUCCESS) WAS NOT TRANSLATED BECAUSE ITS VARIABLE COULD NOT BE RESOLVED AGAINST THIS SESSION'S MAPPING. THE TARGET VARIABLE WILL KEEP ITS PREVIOUS VALUE. VERIFY THE VARIABLE IS DECLARED AND THAT ANY SHARED FOLDER DECLARING IT IS INCLUDED IN THE CONVERSION.,../folder/Informatica/InfPc_Source.xml,ETL.wf_postvar.s_postvar,Not Provided
```

#### Best Practices

- Confirm that the variable is declared and that any shared folder declaring it is included in the conversion, then convert again so the assignment can be generated.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0095

Mapplet input port has no incoming connector and a non-empty default value; value replaced with NULL.

#### Description

This issue is reported when a mapplet input port has no incoming connector but declares a non-empty default value. Informatica would substitute that default at run time, while the converted output projects a typed `NULL` for the column instead.

#### Code Example

##### Input Code:

##### Informatica

Copy code

```
<TRANSFORMFIELD DATATYPE ="string" DEFAULTVALUE ="0" MAPPLETGROUP ="INPUT" NAME ="col_b" PORTTYPE ="INPUT" PRECISION ="50" REF_FIELD ="col_b" REF_INSTANCETYPE ="Input Transformation" SCALE ="0"/>
```

##### Output Code:

##### Snowflake

Copy code

```
CREATE OR REPLACE TEMPORARY TABLE tmp_mplt_in_cte_mplt_unconnected_default AS
   SELECT
      ProductKey AS col_a,
      --** SSC-FDM-INF0095 - MAPPLET INPUT PORT 'col_b' HAS NO INCOMING CONNECTOR AND A NON-EMPTY DEFAULT VALUE IN THE SOURCE MAPPING. INFORMATICA WOULD SUBSTITUTE THE PORT'S DEFAULT VALUE AT RUNTIME; THE CONVERTED OUTPUT PROJECTS A TYPED NULL FOR THIS COLUMN INSTEAD. VERIFY THE SOURCE MAPPING FOR A MISSING OR REMOVED CONNECTION. **
      NULL :: VARCHAR(50) AS col_b,
      NULL :: VARCHAR(50) AS col_c
   FROM
      tmp_sq_dimproduct
```

#### Best Practices

- Replace the projected `NULL` with the port’s default value, or connect the port in the source mapping and convert again.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0096

$PMFolderName translated to a dbt variable seeded with the consumer folder name

#### Description

This issue is reported when an expression references `$PMFolderName`. There is no direct Snowflake equivalent, so the value is converted to a dbt variable that the generated orchestration seeds with the Informatica PowerCenter folder name.

#### Code Example

##### Input Code:

##### Informatica

Copy code

```
<TRANSFORMFIELD DATATYPE="string" DEFAULTVALUE="ERROR(&apos;transformation error&apos;)" EXPRESSION="$PMFolderName" EXPRESSIONTYPE="GENERAL" NAME="FolderName" PORTTYPE="OUTPUT" PRECISION="100" SCALE="0"/>
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT
   EventID AS EventID,
   EventName AS EventName,
   --** SSC-FDM-INF0096 - $PMFOLDERNAME HAS NO DIRECT SNOWFLAKE EQUIVALENT. CONVERTED TO A DBT VARIABLE THAT THE GENERATED ORCHESTRATION SEEDS WITH THE CONSUMER FOLDER NAME FROM INFORMATICA POWERCENTER. VERIFY EXPRESSIONS THAT REFERENCE THIS VALUE. **
   '{{ var('PMFOLDERNAME') }}' :: VARCHAR AS FolderName
FROM
   source_data
```

#### Best Practices

- Verify the seeded value when the models are run outside the generated orchestration, because the dbt variable is not populated automatically in that case.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0097

$PMRepositoryServiceName translated to CURRENT\_ACCOUNT\_NAME()

#### Description

This issue is reported when an expression references `$PMRepositoryServiceName`. There is no direct Snowflake equivalent, so the reference is converted to `CURRENT_ACCOUNT_NAME()`, which returns the Snowflake account name rather than the Informatica repository service name.

#### Code Example

##### Input Code:

##### Informatica

```
$PMRepositoryServiceName
```

##### Output Code:

##### Snowflake

Copy code

```
--** SSC-FDM-INF0097 - $PMREPOSITORYSERVICENAME HAS NO DIRECT SNOWFLAKE EQUIVALENT. CONVERTED TO CURRENT_ACCOUNT_NAME(). VERIFY EXPRESSIONS THAT REFERENCE THIS VALUE. **
CURRENT_ACCOUNT_NAME()
```

#### Best Practices

- Verify expressions that compare or format this value, because the Snowflake account name will not match the original repository service name.
- Replace the call with a literal or a dbt variable when the original repository name must be preserved in the output.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-FDM-INF0099

Self-referential local variable accumulator translated to a running total SUM window function.

#### Description

This issue is reported when a local variable port self-references its own name inside an `IIF` in the recognized running-total shape — `V = IIF(condition, V, V + increment)` or its mirror. The port is translated to `SUM(IFF(condition, trueValue, falseValue)) OVER (ORDER BY ... ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)`, which reproduces the accumulation only if the window ordering matches the original row order.

#### Code Example

##### Input Code:

##### Informatica

Copy code

```
<TRANSFORMFIELD DATATYPE="integer" DEFAULTVALUE="" EXPRESSION="IIF(ACCOUNT_NR = 'FOOTER', V_Row_Count, V_Row_Count + 1)" EXPRESSIONTYPE="GENERAL" NAME="V_Row_Count" PORTTYPE="LOCAL VARIABLE" PRECISION="10" SCALE="0"/>
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT
   *,
   --** SSC-FDM-INF0099 - THIS LOCAL VARIABLE PORT SELF-REFERENCES ITS OWN NAME INSIDE AN IIF (THE INFORMATICA PATTERN FOR A ROW-BY-ROW RUNNING TOTAL): V = IIF(CONDITION, V, V + INCREMENT) OR ITS MIRROR V = IIF(CONDITION, V + INCREMENT, V). TRANSLATED TO SUM(IFF(CONDITION, TRUEVALUE, FALSEVALUE)) OVER (ORDER BY ... ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW). VERIFY THAT THE CONDITION AND INCREMENT MATCH THE INTENDED ACCUMULATION LOGIC. **
   SUM(IFF(ACCOUNT_NR = 'FOOTER', 0, 1))
   OVER (
   ORDER BY
      1
   ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS V_Row_Count
FROM
   source_data
```

#### Best Practices

- Verify that the condition and the increment match the intended accumulation logic, and replace a non-deterministic `ORDER BY 1` with the column that defines the original row order.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).
