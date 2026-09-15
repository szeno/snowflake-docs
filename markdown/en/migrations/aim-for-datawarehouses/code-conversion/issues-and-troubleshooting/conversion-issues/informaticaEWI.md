# Code Conversion - Informatica PowerCenter Conversion Issues

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts. This preview is available for Informatica PowerCenter migrations.

This section provides detailed documentation for the Error, Warning, and Information (EWI) messages that may be generated during Informatica PowerCenter conversion.

For assistance with any EWI, you can use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions, or contact [aim-support@snowflake.com](mailto:aim-support@snowflake.com) for additional support.

## SSC-EWI-INF0001

This Informatica PowerCenter transformation is not supported.

### Severity

Critical

### Description

This issue is reported when an Informatica PowerCenter mapping is converted and a transformation with no supported equivalent is encountered. Its logic is not translated automatically and must be reproduced by hand.

### Converted Code

Copy code

```
!!!RESOLVE EWI!!! /*** SSC-EWI-INF0001 - INFORMATICA POWERCENTER TRANSFORMATION IS NOT SUPPORTED BY SNOWCONVERT ***/!!!
cte_fil_transform AS
(
   -- Unsupported transformation 'FIL_Transform' (UnsupportedTransformation)
   SELECT
      null AS ID,
      null AS NAME
)
```

### Best Practices

- Review the unsupported transformation and implement equivalent logic manually in Snowflake or dbt.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0002

Informatica PowerCenter expression cannot be converted.

### Severity

High

### Description

This issue is reported when an Informatica PowerCenter mapping is converted and a specific expression cannot be translated into Snowflake SQL. The affected expression is left unconverted and requires a manual equivalent.

### Best Practices

- Review the flagged expression and implement an equivalent Snowflake SQL expression manually.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0003

Informatica PowerCenter workflow element cannot be converted.

### Severity

High

### Description

This issue is reported when an Informatica PowerCenter workflow is converted and a specific workflow element cannot be translated into Snowflake Scripting. The affected element is left unconverted and requires manual reproduction.

### Best Practices

- Review the flagged workflow element and implement equivalent logic manually in Snowflake Scripting.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0004

Informatica PowerCenter mapping element could not be pre-processed.

### Severity

High

### Description

This issue is reported when an Informatica PowerCenter mapping is converted and a mapping element cannot be pre-processed. Because pre-processing did not complete for that element, its conversion may be incomplete and requires manual review.

### Best Practices

- Review the affected mapping element and complete or correct its conversion manually.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0005

Informatica PowerCenter column name could not be resolved.

### Severity

High

### Description

This issue is reported when an Informatica PowerCenter mapping is converted and a column name cannot be resolved. As a fallback, the column name taken from the transform field is used, which may not match the intended reference.

### Best Practices

- Review the resolved column name and confirm it matches the intended source column, correcting it manually if needed.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0006

Embedded SQL cannot be converted.

### Severity

High

### Description

This issue is reported when an Informatica PowerCenter mapping is converted and embedded SQL from the source type cannot be converted into Snowflake SQL. The embedded SQL is left unconverted and requires a manual equivalent.

### Best Practices

- Review the embedded SQL and rewrite it manually as an equivalent Snowflake SQL statement.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0007

Unexpected exception converting transformation.

### Severity

High

### Description

This issue is reported when an unexpected exception occurs while converting an Informatica PowerCenter transformation. The affected transformation may not be fully converted and requires manual review.

### Best Practices

- Review the affected transformation and complete its conversion manually.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0008

Informatica TO\_CHAR format contains unsupported elements that may require manual review.

### Severity

Medium

### Description

This issue is reported when an Informatica PowerCenter `TO_CHAR` call whose format string contains unsupported elements is converted. These elements may behave differently in Snowflake, so the converted format may require manual review.

### Best Practices

- Review the `TO_CHAR` format string and adjust it so that it produces the intended result in Snowflake.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0009

TO\_CHAR format argument is not a literal and could not be converted.

### Severity

Critical

### Description

This issue is reported when the format argument of an Informatica PowerCenter `TO_CHAR` call is not a literal value. Because the format is determined at runtime rather than being a fixed literal, it cannot be converted automatically and requires manual review.

### Best Practices

- Review the `TO_CHAR` call and provide an equivalent Snowflake format manually, or refactor the logic so the format is a literal.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0010

Multiple models target the same table with mismatched column counts.

### Severity

High

### Description

This issue is reported when multiple models write to the same target table but with different column counts. Because the target instances have mismatched column sets, they cannot be merged into a single model and must be reconciled manually.

### Best Practices

- Review the generated models and reconcile the column sets, or consolidate the target instances into a single model manually.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0011

Informatica PowerCenter built-in function not converted to Snowflake SQL.

### Severity

Medium

### Description

This issue is reported when an Informatica PowerCenter mapping is converted and a built-in function cannot be converted to Snowflake SQL. The affected function is left unconverted and requires a manual equivalent.

### Best Practices

- Review the flagged built-in function and implement an equivalent Snowflake SQL function manually.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0012

Informatica PowerCenter built-in variable is not supported.

### Severity

Medium

### Description

This issue is reported when an Informatica PowerCenter mapping is converted and an unsupported built-in variable is encountered. The affected variable is not converted and requires manual handling.

### Best Practices

- Review the flagged built-in variable and provide an equivalent value or expression manually in Snowflake.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0013

Informatica PowerCenter mapplet variables are not supported.

### Severity

High

### Description

This issue is reported when an Informatica PowerCenter mapplet that contains variables is converted. These mapplet variables are not converted to dbt and require manual handling.

### Best Practices

- Review the mapplet variables and reproduce their behavior manually in the generated dbt output.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0014

Source Qualifier uses Informatica PowerCenter variables in SQL Query property.

### Severity

Medium

### Description

This issue is reported when a Source Qualifier uses Informatica PowerCenter variables in its SQL Query property. Because these variables are not converted automatically, the generated query requires manual review.

### Best Practices

- Review the SQL Query property and replace the Informatica PowerCenter variables with equivalent values or parameters in Snowflake.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0015

Source Qualifier uses Informatica PowerCenter variables in WHERE conditions.

### Severity

Medium

### Description

This issue is reported when a Source Qualifier uses Informatica PowerCenter variables in a User Defined Join or Source Filter. Because these variables are not converted automatically, the resulting WHERE conditions require manual review.

### Best Practices

- Review the User Defined Join or Source Filter and replace the Informatica PowerCenter variables with equivalent values or parameters in Snowflake.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0016

INSTR search value is not a literal and regex escaping could not be applied.

### Severity

Critical

### Description

This issue is reported when the search value of an Informatica PowerCenter `INSTR` call is not a literal. Because the value is determined at runtime, regex special characters cannot be escaped, so the conversion requires manual review.

### Best Practices

- Review the `INSTR` call and ensure the search value is handled correctly, escaping any regex special characters manually as needed.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0017

INSTR negative start position is not supported.

### Severity

Medium

### Description

This issue is reported when an Informatica PowerCenter `INSTR` call uses a negative start position, which is not supported. The start position has been defaulted to 1, so the converted call requires manual review.

### Best Practices

- Review the `INSTR` call and adjust the start position so it produces the intended result in Snowflake.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0018

Source Qualifier uses Informatica PowerCenter variables in Pre SQL property.

### Severity

Medium

### Description

This issue is reported when a Source Qualifier uses Informatica PowerCenter variables in its Pre SQL property. Because these variables are not converted automatically, the generated Pre SQL requires manual review.

### Best Practices

- Review the Pre SQL property and replace the Informatica PowerCenter variables with equivalent values or parameters in Snowflake.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0019

Source Qualifier uses Informatica PowerCenter variables in Post SQL property.

### Severity

Medium

### Description

This issue is reported when an Informatica PowerCenter mapping is converted. The Source Qualifier references Informatica PowerCenter variables inside its Post SQL property, and these variables cannot be resolved automatically during conversion.

### Best Practices

- Review the Post SQL statement and manually replace the Informatica PowerCenter variables with the appropriate Snowflake values or dbt configuration.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0020

ADD\_TO\_DATE format string is not a recognized Informatica date part.

### Severity

Medium

### Description

This issue is reported when an Informatica PowerCenter mapping is converted. The format string supplied to `ADD_TO_DATE` is not a recognized Informatica date part, so it was passed through as-is to the Snowflake `DATEADD` function. You should verify that the date part is valid in Snowflake.

### Best Practices

- Confirm that the date part passed to `DATEADD` is valid in Snowflake and adjust it if necessary.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0021

GET\_DATE\_PART format argument is not a literal and could not be converted.

### Severity

Critical

### Description

This issue is reported when an Informatica PowerCenter mapping is converted. The format argument passed to `GET_DATE_PART` is not a literal value, so it could not be converted to a Snowflake `DATE_PART` date part.

### Best Practices

- Replace the non-literal format argument with a literal date part so the expression can be converted to Snowflake `DATE_PART`.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0022

GET\_DATE\_PART format string is not a recognized Informatica date part.

### Severity

Medium

### Description

This issue is reported when an Informatica PowerCenter mapping is converted. The format string supplied to `GET_DATE_PART` is not a recognized Informatica date part, so it was passed through as-is to the Snowflake `DATE_PART` function. You should verify that the date part is valid in Snowflake.

### Best Practices

- Confirm that the date part passed to `DATE_PART` is valid in Snowflake and adjust it if necessary.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0024

IS\_DATE without format uses session date format in Informatica but Snowflake auto-detects formats.

### Severity

Medium

### Description

This issue is reported when an Informatica PowerCenter mapping is converted. When `IS_DATE` is used without a format, Informatica relies on the session date format, whereas Snowflake automatically detects the format instead. This difference may lead to different results.

### Best Practices

- Provide an explicit format to `IS_DATE` so the behavior matches your expectations in Snowflake.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0025

Informatica `IS_DATE` format contains unsupported elements and may produce different results.

### Severity

Medium

### Description

This issue is reported when an Informatica PowerCenter mapping is converted. The Informatica `IS_DATE` format contains unsupported elements, so the converted expression may produce different results in Snowflake.

### Best Practices

- Review the `IS_DATE` format and adjust the unsupported elements so the result matches the original behavior in Snowflake.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0026

Informatica TO\_DATE format contains unsupported elements that may require manual review.

### Severity

Medium

### Description

This issue is reported when an Informatica PowerCenter mapping is converted. The Informatica `TO_DATE` format contains unsupported elements that may require manual review or may behave differently in Snowflake.

### Best Practices

- Review the `TO_DATE` format and adjust the unsupported elements so the converted expression behaves as expected in Snowflake.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0027

TO\_DATE format argument is not a literal and could not be converted.

### Severity

Critical

### Description

This issue is reported when an Informatica PowerCenter mapping is converted. The format argument passed to `TO_DATE` is not a literal value, so it could not be converted to Snowflake.

### Best Practices

- Replace the non-literal format argument with a literal format so the `TO_DATE` expression can be converted to Snowflake.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0028

VSAM Normalizer transformation is not supported.

### Severity

Critical

### Description

This issue is reported when an Informatica PowerCenter mapping is converted. The Normalizer was generated from a COBOL source definition (VSAM) and cannot be automatically converted to Snowflake dbt, so manual conversion is required.

### Best Practices

- Manually convert the VSAM Normalizer logic to an equivalent Snowflake dbt implementation.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0029

Aggregator passthrough column approximated with MAX() function.

### Severity

Medium

### Description

This issue is reported when an Informatica PowerCenter mapping is converted. An Aggregator without a GROUP BY contains one or more passthrough columns, and while Informatica returns the last value processed, Snowflake uses the `MAX()` function as an approximation. Results may differ depending on the input data order.

### Best Practices

- Verify that the `MAX()` approximation returns the value you expect, and adjust the logic if the input data order matters.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0030

ADD\_TO\_DATE format argument is not a literal and could not be converted.

### Severity

Critical

### Description

This issue is reported when an Informatica PowerCenter mapping is converted. The format argument passed to `ADD_TO_DATE` is not a literal value, so it could not be converted to a Snowflake `DATEADD` date part.

### Best Practices

- Replace the non-literal format argument with a literal date part so the expression can be converted to Snowflake `DATEADD`.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0033

Sequence Generator Start Value exceeds integer range.

### Severity

Medium

### Description

This issue is reported when an Informatica PowerCenter mapping is converted. The Sequence Generator start value produces an offset that exceeds the integer range supported by the SQL literal, so the generated offset has been clamped. Manual adjustment of the start value offset is required.

### Best Practices

- Manually adjust the Sequence Generator start value offset so it stays within the supported integer range.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0034

Mapping has multiple session overrides of its update strategy.

### Severity

Medium

### Description

This issue is reported when an Informatica PowerCenter mapping is converted. The mapping has multiple session overrides of its update strategy, which cannot be reconciled automatically during conversion.

### Best Practices

- Review the session overrides and manually determine the correct update strategy for the converted mapping.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0035

Update strategy not directly connected to target transformation requires manual changes.

### Severity

Medium

### Description

This issue is reported when an Informatica PowerCenter mapping is converted. The update strategy is not connected to the target transformation, so manual changes are required to complete the conversion.

### Best Practices

- Manually connect the update strategy logic to the target so the converted mapping behaves as intended.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0037

Informatica PowerCenter disconnected stored procedure call cannot be converted to Snowflake SQL.

### Severity

Medium

### Description

This issue is reported when an Informatica PowerCenter mapping is converted. A disconnected stored procedure call cannot be converted to a SQL expression during the migration to Snowflake.

### Best Practices

- Manually implement the disconnected stored procedure logic as an equivalent Snowflake SQL expression or procedure.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0038

Stored procedure uses a named connection that must be manually mapped.

### Severity

Medium

### Description

This issue is reported when an Informatica PowerCenter mapping is converted. The stored procedure uses a named connection, and named connections must be manually mapped to the corresponding Snowflake database and schema in the dbt profile or project configuration.

### Best Practices

- Manually map the named connection to the appropriate Snowflake database and schema in the dbt profile or project configuration.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0039

dbt folder hooks execute once per model, not once per session.

### Severity

Medium

### Description

This issue is reported when an Informatica PowerCenter mapping is converted. dbt folder hooks execute once per model in the folder, not once per session as in Informatica. If the procedure must run only once, consider using an on-run-start or on-run-end hook instead.

### Best Practices

- If the procedure must run only once, use an on-run-start or on-run-end hook instead of a folder hook.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0040

Stored Procedure transformation is translated assuming the procedure has been converted to a UDF.

### Severity

Medium

### Description

This issue is reported when an Informatica PowerCenter mapping is converted. The Stored Procedure transformation is translated assuming the procedure has been converted to a UDF, because the original Informatica transformation called the procedure once per row while the translation calls it as an inline UDF. You should convert the stored procedure to a Snowflake UDF that returns `OBJECT_CONSTRUCT` with named fields matching the output port names.

### Best Practices

- Convert the stored procedure to a Snowflake UDF that returns `OBJECT_CONSTRUCT` with named fields matching the output port names.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0041

Port has Informatica-specific ERROR() default value with no Snowflake equivalent.

### Severity

Low

### Description

This issue is reported when an Informatica PowerCenter mapping is converted. A port declares a default value of `ERROR('transformation error')`, which is an Informatica-specific error function that has no direct Snowflake equivalent. The default value has been omitted from the translation.

### Best Practices

- Review the port and reimplement the intended error-handling behavior manually if it is required.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0042

Informatica PowerCenter CUME running total translated to SUM aggregate approximation.

### Severity

Medium

### Description

The Informatica PowerCenter `CUME` function computes a running total row by row in pipeline order, depending on a preceding Sort transformation. It was translated to `SUM`, which computes a single total aggregate. Inside an Aggregator with a group by clause the final output value is equivalent because there is one row per group, but the running-total semantics and the sort-order dependency are lost.

### Best Practices

- Verify that downstream logic does not depend on intermediate `CUME` values or on row ordering.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0043

Sequence Generator row ordering is non-deterministic and state is not persisted.

### Severity

Low

### Description

The Sequence Generator is translated to `ROW_NUMBER() OVER (ORDER BY 1)`. Row ordering is non-deterministic, so values may be assigned to different rows between runs, and the sequence state is not persisted across dbt executions, so it always restarts from the start value.

### Converted Code

Copy code

```
!!!RESOLVE EWI!!! /*** SSC-EWI-INF0043 - THE SEQUENCE GENERATOR IS TRANSLATED TO ROW_NUMBER() OVER (ORDER BY 1). ROW ORDERING IS NON-DETERMINISTIC (VALUES MAY BE ASSIGNED TO DIFFERENT ROWS BETWEEN RUNS) AND SEQUENCE STATE IS NOT PERSISTED ACROSS DBT EXECUTIONS (ALWAYS RESTARTS FROM START VALUE). ADD A DETERMINISTIC ORDER BY IF STABLE SEQUENCE ASSIGNMENT IS REQUIRED. ***/!!!
SELECT
   *,
   ROW_NUMBER() OVER (ORDER BY 1) + 9 AS NEXTVAL
FROM
   source_data
```

### Best Practices

- Add a deterministic `ORDER BY` clause if stable sequence assignment is required.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0044

Sequence Generator cycle count is not evenly divisible.

### Severity

Low

### Description

The Sequence Generator cycle count is not evenly divisible because the difference between the end value and the start value is not a multiple of the increment. The generated sequence will not reach the end value before cycling, so manual adjustment may be required.

### Best Practices

- Adjust the start value, end value, or increment so that the range divides evenly.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0045

Sequence Generator has Cycle=YES but EndValue is the default.

### Severity

Low

### Description

The Sequence Generator has `Cycle` set to `YES`, but its end value is left at the default maximum. The cycle expression cannot be generated with a meaningful cycle count, so the sequence is emitted without cycling and manual adjustment is required if cycling behavior is needed.

### Best Practices

- Set an explicit end value so a meaningful cycle count can be generated if cycling behavior is needed.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0046

Active Java Transformation cannot be automatically translated.

### Severity

High

### Description

An active Java transformation cannot be automatically translated, and the transformation may change row cardinality. This issue is reported when an Informatica PowerCenter mapping is converted.

### Best Practices

- Manually migrate the transformation to a Snowflake Java UDTF or a Snowpark procedure.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0047

Output-only port is set by Java code and cannot be automatically translated.

### Severity

Low

### Description

An output-only port is set by Java code and cannot be automatically translated. This issue is reported when an Informatica PowerCenter mapping is converted.

### Best Practices

- Manually migrate the Java logic that populates this output-only port.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0048

Java Transformation uses update strategy (setOutRowType).

### Severity

Low

### Description

A Java transformation uses an update strategy through the `setOutRowType` method. Manual migration of the row-type logic is required.

### Best Practices

- Manually migrate the row-type logic that the `setOutRowType` call controls.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0049

Java Transformation generates transactions (commit/rollback).

### Severity

Low

### Description

A Java transformation generates transactions through commit and rollback calls, and Snowflake transaction semantics differ. Manual review is required.

### Best Practices

- Manually review the commit and rollback logic against Snowflake transaction semantics.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0050

Informatica PowerCenter user-defined function call cannot be automatically converted to Snowflake SQL.

### Severity

Medium

### Description

An Informatica PowerCenter user-defined function call, written with the `:UDF.` prefix followed by the function name, was not converted to Snowflake SQL. This issue is reported when an Informatica PowerCenter mapping is converted.

### Best Practices

- Review the call and manually map it to an equivalent Snowflake function.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0051

Informatica PowerCenter ERROR() function has no Snowflake equivalent.

### Severity

High

### Description

The Informatica PowerCenter `ERROR()` function causes the Integration Service to skip the current row and log a message. There is no equivalent row-skip mechanism in Snowflake SQL, so the function is replaced with `NULL`.

### Best Practices

- Review all `ERROR()` usages and implement row-filtering logic manually.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0052

Informatica REG\_EXTRACT match\_from\_start parameter has no Snowflake equivalent.

### Severity

Medium

### Description

The Informatica `REG_EXTRACT` function accepts a `match_from_start` parameter, where a non-zero value anchors the match at the start of the string. Snowflake `REGEXP_SUBSTR` has no equivalent anchor parameter.

### Best Practices

- When `match_from_start` is non-zero, prefix the pattern with a `^` anchor manually or verify that anchoring is not required for your data.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0053

SET\_DATE\_PART format argument is not a literal and could not be converted.

### Severity

Critical

### Description

The `SET_DATE_PART` format argument is not a literal, so it could not be converted to a Snowflake `DATE_PART` date part. This issue is reported when an Informatica PowerCenter mapping is converted.

### Best Practices

- Replace the dynamic format argument with a literal date part and manually convert the expression.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0054

SET\_DATE\_PART format string is not supported in Snowflake.

### Severity

Critical

### Description

The `SET_DATE_PART` format string is not supported in Snowflake because `DATE_PART` does not accept millisecond or microsecond parts in this context. This issue is reported when an Informatica PowerCenter mapping is converted.

### Best Practices

- Review the expression and manually convert it to a date part that Snowflake `DATE_PART` supports.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0055

Informatica PowerCenter Email task contains workflow/service variables that cannot be resolved.

### Severity

Medium

### Description

An Informatica PowerCenter Email task contains workflow or service variables in the email subject or body. These variables cannot be automatically resolved in Snowflake, so manual conversion is required.

### Best Practices

- Manually convert the workflow and service variables to values that Snowflake can resolve.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0056

Informatica PowerCenter Email task has no recipients.

### Severity

High

### Description

An Informatica PowerCenter Email task has an empty or missing email user name attribute. The generated notification integration and `SYSTEM$SEND_EMAIL` call will fail at runtime.

### Best Practices

- Specify valid recipient email addresses for the Email task.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0057

Informatica PowerCenter Decision task condition references task status or row counts.

### Severity

High

### Description

An Informatica PowerCenter expression references task status or row count properties, such as task status, previous task status, source success rows, target failed rows, total transformation errors, first error code, first error message, start time, and end time. These runtime metrics have no direct equivalent in Snowflake Task DAGs, so manual conversion is required.

### Best Practices

- Manually convert the expression using an alternative that Snowflake supports.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0058

Informatica PowerCenter workflow link condition cannot be translated to a Snowflake WHEN clause.

### Severity

High

### Description

An Informatica PowerCenter workflow link condition references variables or expressions that cannot be evaluated in a Snowflake Task `WHEN` clause, so the `WHEN` clause was omitted. The task will run unconditionally unless the condition is enforced inside the task body.

### Best Practices

- Enforce the condition inside the task body if conditional execution is required.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0059

Sequence Generator fan-out: per-pipeline counters in dbt vs shared counter in Informatica.

### Severity

Medium

### Description

This issue is reported when a Sequence Generator is connected to multiple independent pipelines in a fan-out topology. In Informatica PowerCenter the sequence counter is shared across all pipelines, so it produces non-overlapping identifiers, but in dbt each pipeline receives an independent `ROW_NUMBER()` starting from 1, so counter values will overlap between pipelines. Review the generated per-pipeline intermediate models and decide whether sequential numbering across pipelines is required.

### Best Practices

- Review the generated per-pipeline intermediate models and confirm whether unique identifiers across all pipelines are required, adjusting the numbering logic if overlap is not acceptable.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0060

Informatica PowerCenter ABORT() function has no Snowflake equivalent.

### Severity

High

### Description

This issue is reported when an Informatica PowerCenter mapping that uses the `ABORT()` function is converted. The `ABORT()` function immediately stops the Integration Service session and marks it as failed, but there is no equivalent session-abort mechanism in Snowflake SQL, so the function is replaced with `NULL`. You should implement the required error-handling logic using Snowflake streams, tasks, or pre and post SQL scripts.

### Best Practices

- Implement the required error-handling logic using Snowflake streams, tasks, or pre and post SQL scripts to replace the removed abort behavior.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0061

Lookup condition predicate not fully converted.

### Severity

Medium

### Description

This issue is reported when one or more Lookup condition predicates could not be fully converted, for example function calls, literals, or complex expressions. As a result the generated join or `WHERE` clause may be incomplete. Review the original Lookup condition and add the missing predicates manually.

### Best Practices

- Review the original Lookup condition and add any missing predicates to the generated join or `WHERE` clause manually.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0062

Informatica PowerCenter mapplet input port has no incoming connector.

### Severity

Low

### Description

This issue is reported when a mapplet input port has no incoming connector. In this case `NULL` is used as a fallback SQL expression for that port.

### Best Practices

- Verify whether the mapplet input port should receive a value and provide the correct source expression if the `NULL` fallback is not appropriate.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0063

Source Qualifier SQL Query is procedural, not a single SELECT or CTE.

### Severity

High

### Description

This issue is reported when a Source Qualifier SQL query contains procedural code and cannot be converted into a dbt model body. The original SQL is preserved as a comment.

### Best Practices

- Review the preserved original SQL comment and rewrite the procedural logic as a single `SELECT` or CTE that dbt can consume.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0064

Flat File Lookup stage path variable requires manual mapping to a Snowflake stage.

### Severity

High

### Description

This issue is reported when a Flat File Lookup stage path variable requires manual mapping to a Snowflake stage. The referenced file format must already exist in the target database.

### Best Practices

- Map the stage path variable to the correct Snowflake stage and confirm that the required file format exists in the target database.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0065

Expression transformation uses Lagger Technique but no preceding Sorter found for ORDER BY.

### Severity

Medium

### Description

This issue is reported when an Expression transformation uses the Lagger Technique, a local variable forward reference that accesses values from previous rows. It is translated to a `LAG` window function with a non-deterministic `ORDER BY 1` because no preceding Sorter transformation was found. Manual intervention is required to replace `ORDER BY 1` with a deterministic column so that row ordering is correct.

### Best Practices

- Replace the non-deterministic `ORDER BY 1` in the generated `LAG` window function with a deterministic column that guarantees correct row ordering.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0066

Informatica PowerCenter self-referencing source-to-ref override was not applied.

### Severity

Low

### Description

This issue is reported when a self-referencing source-to-ref override could not be applied because the expected source reference was not found in the generated SQL. As a result the dbt model may fail to compile. Verify that the source reference exists and manually replace it with the correct ref call if needed.

### Best Practices

- Verify that the expected source reference exists and manually replace it with the correct dbt ref call so the model compiles.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0067

Informatica PowerCenter file could not be parsed and was skipped.

### Severity

Medium

### Description

This issue is reported when an Informatica PowerCenter file could not be parsed and was therefore skipped. The message includes the affected file name and the reported cause.

### Best Practices

- Review the reported cause for the skipped file, correct the underlying issue, and reconvert the file so it can be processed.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0068

Fixed-width flat file format is not supported.

### Severity

High

### Description

This issue is reported when a flat file source uses a fixed-width format, which cannot be mapped to a Snowflake file format. Manual conversion is required.

### Best Practices

- Manually convert the fixed-width flat file into a format that Snowflake supports, such as a delimited file with an appropriate file format.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0069

Flat File Source stage path variable requires manual mapping to a Snowflake stage.

### Severity

High

### Description

This issue is reported when a Flat File Source stage path variable requires manual mapping to a Snowflake stage. The referenced file format must already exist in the target database.

### Best Practices

- Map the stage path variable to the correct Snowflake stage and confirm that the required file format exists in the target database.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0070

Flat file source code page has no known Snowflake ENCODING mapping.

### Severity

Medium

### Description

This issue is reported when a flat file source code page has no known Snowflake `ENCODING` mapping. The file format will default to UTF-8, so you should verify this or add the encoding clause manually.

### Best Practices

- Verify that UTF-8 is correct for the source file, or add the appropriate `ENCODING` clause to the file format manually.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0071

Flat file source text qualifier cannot be mapped to Snowflake FIELD\_OPTIONALLY\_ENCLOSED\_BY.

### Severity

Medium

### Description

This issue is reported when a flat file source text qualifier is not a recognized single-character value and cannot be mapped to Snowflake’s `FIELD_OPTIONALLY_ENCLOSED_BY` option. The clause has been omitted, so add it manually if needed.

### Best Practices

- Review the source text qualifier and add a valid single-character `FIELD_OPTIONALLY_ENCLOSED_BY` value to the file format manually if needed.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0072

Flat file target requires manual mapping of stage path variable.

### Severity

High

### Description

This issue is reported when a flat file target requires manual mapping. You must set the associated variable to your Snowflake stage path.

### Best Practices

- Set the flat file target variable to the correct Snowflake stage path so the target resolves properly.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0073

Flat file target has ‘Append if Exists’ enabled but Snowflake does not support appending to stage files.

### Severity

Medium

### Description

This issue is reported when a flat file target has the ‘Append if Exists’ option enabled. Snowflake `COPY INTO` does not support appending to existing stage files, so the generated output uses overwrite mode instead.

### Best Practices

- Review the overwrite behavior of the generated `COPY INTO` output and adjust your process if appending to existing stage files was required.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0074

Flat file target has a non-UTF8 codepage but ENCODING is not supported in COPY INTO location (unload).

### Severity

Medium

### Description

This issue is reported when a flat file target has a non-UTF-8 codepage mapped to a Snowflake encoding. The `ENCODING` option is only valid for `COPY INTO` a table when loading, not for `COPY INTO` a location when unloading, and Snowflake always writes UTF-8 when unloading to a stage.

### Best Practices

- Account for the fact that Snowflake always writes UTF-8 when unloading, and add a downstream conversion step if a different target encoding is required.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0075

Flat file target uses an escape character but Snowflake CSV unload does not support escape characters.

### Severity

Medium

### Description

This issue is reported when a flat file target uses an escape character. Snowflake `COPY INTO` a location with CSV format does not support an escape character for unloading, so fields containing the delimiter must be enclosed instead.

### Best Practices

- Configure the CSV unload to enclose fields that contain the delimiter instead of relying on an escape character.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0076

Sequence Generator CURRVAL port is consumed downstream but Snowflake native sequences do not support CURRVAL.

### Severity

Medium

#### Description

This issue is reported when the `CURRVAL` port of a Sequence Generator feeds a downstream transformation or target. The Sequence Generator is translated to a Snowflake native sequence, and native sequences in Snowflake expose only `NEXTVAL`, so there is no equivalent for `CURRVAL`. The affected column is projected as `null` and the `CURRVAL` semantics must be reproduced manually.

#### Code Example

##### Input Code:

##### Informatica

Copy code

```
<TRANSFORMFIELD DATATYPE ="bigint" DEFAULTVALUE ="ERROR(&apos;transformation error&apos;)" DESCRIPTION ="" NAME ="CURRVAL" PICTURETEXT ="" PORTTYPE ="OUTPUT" PRECISION ="19" SCALE ="0"/>
<CONNECTOR FROMFIELD ="CURRVAL" FROMINSTANCE ="SEQTRANS" FROMINSTANCETYPE ="Sequence" TOFIELD ="curr_val" TOINSTANCE ="SEQ_TGT_CURRVAL" TOINSTANCETYPE ="Target Definition"/>
```

##### Output Code:

##### Snowflake

Copy code

```
---- Start block 'Sequence_SNOW-3701825.m_Sequence_Currval.SEQ_TGT_CURRVAL'
INSERT INTO YOUR_DB.YOUR_SCHEMA.SEQ_TGT_CURRVAL (id, seq_val, curr_val)
WITH
!!!RESOLVE EWI!!! /*** SSC-EWI-INF0076 - THE CURRVAL PORT OF THE SEQUENCE GENERATOR IS CONSUMED DOWNSTREAM. SNOWFLAKE NATIVE SEQUENCES DO NOT SUPPORT CURRVAL. MANUAL INTERVENTION IS REQUIRED TO REPLICATE CURRVAL SEMANTICS (E.G. STORE NEXTVAL IN A VARIABLE AND REUSE IT). ***/!!!
cte_seqtrans AS
(
   SELECT
      *,
      YOUR_DB.YOUR_SCHEMA.SEQTRANS_seq.NEXTVAL AS NEXTVAL
   FROM
      tmp_sq_seq_src_currval
)
SELECT
   sd.id AS id,
   sd.NEXTVAL AS seq_val,
   null AS curr_val
FROM
   cte_seqtrans AS sd
```

#### Best Practices

- Store the `NEXTVAL` result once — in a scripting variable or in the projected column — and reuse that value wherever the mapping consumed `CURRVAL`, instead of reading the sequence a second time.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0079

Sequence Generator translated to a Snowflake native sequence; row ordering is non-deterministic.

### Severity

Low

#### Description

This issue is reported whenever a Sequence Generator is translated to a Snowflake native sequence read through `.NEXTVAL`. Snowflake does not guarantee which row receives which sequence value, so the value-to-row assignment may change between runs even for identical input. The generated code is valid; only the assignment order differs from PowerCenter.

#### Code Example

##### Input Code:

##### Informatica

Copy code

```
<TRANSFORMATION DESCRIPTION ="" NAME ="SEQRCURR" OBJECTVERSION ="1" REUSABLE ="YES" TYPE ="Sequence" VERSIONNUMBER ="1">
    <TRANSFORMFIELD DATATYPE ="bigint" DEFAULTVALUE ="ERROR(&apos;transformation error&apos;)" DESCRIPTION ="" NAME ="NEXTVAL" PICTURETEXT ="" PORTTYPE ="OUTPUT" PRECISION ="19" SCALE ="0"/>
```

##### Output Code:

##### Snowflake

Copy code

```
---- Start block 'Sequence_SNOW_3701829.m_Sequence_ReusableCurrval.SEQ_TGT_RCURR'
!!!RESOLVE EWI!!! /*** SSC-EWI-INF0079 - THE SEQUENCE GENERATOR IS TRANSLATED TO A SNOWFLAKE NATIVE SEQUENCE (.NEXTVAL). ROW ORDERING IS NON-DETERMINISTIC (VALUES MAY BE ASSIGNED TO DIFFERENT ROWS BETWEEN RUNS). ADD A DETERMINISTIC ORDER BY IN THE SOURCE QUERY IF STABLE SEQUENCE ASSIGNMENT IS REQUIRED. ***/!!!
INSERT INTO YOUR_DB.YOUR_SCHEMA.SEQ_TGT_RCURR (id, seq_val, curr_val)
WITH cte_seqrcurr AS
(
   SELECT
      id AS id,
      YOUR_DB.YOUR_SCHEMA.SEQRCURR_seq.NEXTVAL AS seq_val
   FROM
      tmp_sq_seq_src_rcurr
)
SELECT
   id AS id,
   seq_val AS seq_val,
   seq_val + 1 AS curr_val
FROM
   cte_seqrcurr
```

#### Best Practices

- Add a deterministic `ORDER BY` to the source query when a stable sequence assignment matters, for example when the generated value is used as a business key.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0080

Sequence Generator has Cycle=YES but Snowflake native sequences do not support cycling.

### Severity

Low

#### Description

This issue is reported when a Sequence Generator is configured with `Cycle = YES`. Snowflake native sequences have no `CYCLE` option, so the sequence is created without cycling and values keep increasing past the PowerCenter end value instead of wrapping around.

#### Code Example

##### Input Code:

##### Informatica

Copy code

```
<TRANSFORMATION DESCRIPTION ="" NAME ="SEQTRANS" OBJECTVERSION ="1" REUSABLE ="NO" TYPE ="Sequence" VERSIONNUMBER ="1">
    <TABLEATTRIBUTE NAME ="Cycle" VALUE ="YES"/>
```

##### Output Code:

##### Snowflake

Copy code

```
---- Start block 'Sequence_SNOW-3701825.m_Sequence_Cycle.SEQTRANS'
EXECUTE IMMEDIATE 'CREATE SEQUENCE IF NOT EXISTS YOUR_DB.YOUR_SCHEMA.SEQTRANS_seq START = 1 INCREMENT = 1'
---- End block 'Sequence_SNOW-3701825.m_Sequence_Cycle.SEQTRANS'
;
---- Start block 'Sequence_SNOW-3701825.m_Sequence_Cycle.SEQ_TGT_CYCLE'
INSERT INTO YOUR_DB.YOUR_SCHEMA.SEQ_TGT_CYCLE (id, seq_val)
WITH
!!!RESOLVE EWI!!! /*** SSC-EWI-INF0080 - THE SEQUENCE GENERATOR HAS CYCLE=YES BUT SNOWFLAKE NATIVE SEQUENCES DO NOT SUPPORT THE CYCLE OPTION. THE SEQUENCE IS EMITTED WITHOUT CYCLING. MANUAL INTERVENTION IS REQUIRED IF CYCLING BEHAVIOR IS NEEDED (E.G. IMPLEMENT WRAP-AROUND LOGIC IN THE CALLING PROCEDURE). ***/!!!
cte_seqtrans AS
(
   SELECT
      *,
      YOUR_DB.YOUR_SCHEMA.SEQTRANS_seq.NEXTVAL AS NEXTVAL
   FROM
      tmp_sq_seq_src_cycle
)
SELECT
   sd.id AS id,
   sd.NEXTVAL AS seq_val
FROM
   cte_seqtrans AS sd
```

#### Best Practices

- Implement the wrap-around explicitly when cycling is required, for example by applying a modulo over the sequence value or by resetting the sequence in the calling procedure.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0082

Target port is NOTNULL but unconnected and has no default value.

### Severity

High

#### Description

This issue is reported when a target port is declared `NOTNULL` in the source mapping but has no incoming connector and no default value. The column is omitted from the generated `INSERT` projection, so the load can fail at run time if the target table enforces the not-null constraint.

#### Code Example

##### Input Code:

##### Informatica

Copy code

```
<TARGETFIELD BUSINESSNAME="" DATATYPE="varchar" DESCRIPTION="" FIELDNUMBER="3" KEYTYPE="NOT A KEY" NAME="DeptCode" NULLABLE="NOTNULL" PICTURETEXT="" PRECISION="10" SCALE="0"/>
```

##### Output Code:

##### Snowflake

Copy code

```
---- Start block 'ETL.m_notnull_unconnected_scripting.TGT_WITH_NOTNULL'
!!!RESOLVE EWI!!! /*** SSC-EWI-INF0082 - TARGET PORT 'DeptCode' IS DECLARED NOTNULL BUT HAS NO CONNECTOR AND NO DEFAULT VALUE. THE GENERATED SQL OMITS THIS COLUMN FROM THE INSERT PROJECTION, WHICH MAY CAUSE A RUNTIME INSERT FAILURE IF THE TABLE'S NOT-NULL CONSTRAINT IS ENFORCED. CONNECT THE PORT OR ADD A DEFAULT VALUE TO THE TARGET TABLE. ***/!!!
INSERT INTO YOUR_DB.YOUR_SCHEMA.TGT_WITH_NOTNULL (Id, Name, Notes)
SELECT
   sd.Id AS Id,
   sd.Name AS Name,
   NULL :: VARCHAR(200) AS Notes
FROM
   tmp_sq_src_data AS sd
```

#### Best Practices

- Connect the port in the source mapping, or give the target column a `DEFAULT` value in Snowflake so the insert succeeds without the column in the projection.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0083

Non-reusable Sequence Generator with Is Current Value Shared = NO maps to a single Snowflake native sequence shared across all concurrent sessions.

### Severity

Medium

#### Description

This issue is reported when a non-reusable Sequence Generator has `Is Current Value Shared = NO`. In PowerCenter each concurrent session keeps an isolated counter, while the translation creates one Snowflake native sequence object that every session draws from, so concurrent runs can produce interleaved or non-contiguous values per session.

#### Code Example

##### Input Code:

##### Informatica

Copy code

```
<TRANSFORMATION DESCRIPTION ="" NAME ="SEQTRANS" OBJECTVERSION ="1" REUSABLE ="NO" TYPE ="Sequence" VERSIONNUMBER ="1">
    <TABLEATTRIBUTE NAME ="Is Current Value Shared" VALUE ="NO"/>
```

##### Output Code:

##### Snowflake

Copy code

```
---- Start block 'Sequence_SNOW_3701826.m_Sequence_Fanout.SEQ_TGT_FANOUT_A'
!!!RESOLVE EWI!!! /*** SSC-EWI-INF0083 - THE SEQUENCE GENERATOR IS NON-REUSABLE WITH 'IS CURRENT VALUE SHARED' = NO, SO IN POWERCENTER EACH CONCURRENT SESSION GETS AN ISOLATED SEQUENCE COUNTER. THE TRANSLATION USES A SINGLE SNOWFLAKE NATIVE SEQUENCE OBJECT SHARED BY ALL SESSIONS, SO CONCURRENT RUNS DRAW FROM ONE COUNTER AND MAY PRODUCE INTERLEAVED OR NON-CONTIGUOUS VALUES PER SESSION. REVIEW WHETHER CONCURRENT EXECUTION REQUIRES PER-SESSION VALUE ISOLATION (E.G. USE A SEPARATE SEQUENCE OR A SESSION-SCOPED COUNTER). ***/!!!
INSERT INTO YOUR_DB.YOUR_SCHEMA.SEQ_TGT_FANOUT_A (id, seq_val)
SELECT
   id AS id,
   YOUR_DB.YOUR_SCHEMA.SEQTRANS_seq.NEXTVAL AS seq_val
FROM
   tmp_sq_seq_src_fanout
```

#### Best Practices

- Create a dedicated sequence per concurrent run, or use a session-scoped counter, when the migrated process depends on per-session value isolation.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0085

Session has ‘Truncate target table option = YES’ but this flat file target unloads to a stage, so Snowflake cannot truncate it.

### Severity

Medium

#### Description

This issue is reported when the session sets `Truncate target table option` (or `Truncate target option`) to `YES` for a flat file target. That target is unloaded with `COPY INTO <location>`, and the truncate option is not honoured for stage-unload targets, so any previous stage file is not cleared by the generated code.

#### Code Example

##### Input Code:

##### Informatica

Copy code

```
<SESSIONEXTENSION NAME="Flat File Writer" SINSTANCENAME="StudentsOut" TRANSFORMATIONTYPE="Target Definition" TYPE="WRITER">
    <ATTRIBUTE NAME="Truncate target table option" VALUE="YES"/>
</SESSIONEXTENSION>
```

##### Output Code:

##### Snowflake

Copy code

```
---- Start block 'FlatFileCases.m_FlatFileTargetTruncate.StudentsOut'
!!!RESOLVE EWI!!! /*** SSC-EWI-INF0085 - SESSION HAS 'TRUNCATE TARGET TABLE OPTION' (OR 'TRUNCATE TARGET OPTION') = YES, BUT FLAT FILE TARGET 'StudentsOut' UNLOADS TO A STAGE VIA COPY INTO <LOCATION>. THIS OPTION IS NOT HONOURED FOR STAGE-UNLOAD TARGETS — REVIEW WHETHER THE STAGE FILE NEEDS TO BE CLEARED BEFORE THIS LOAD. ***/!!!
EXECUTE IMMEDIATE 'COPY INTO @public.landing_stage/infpc/targets/StudentsOut/ FROM (SELECT sd.GRADE AS GRADE FROM tmp_sq_students AS sd) FILE_FORMAT = (FORMAT_NAME = ''FlatFileCases_m_FlatFileTargetTruncate_StudentsOut'') HEADER = TRUE OVERWRITE = TRUE SINGLE = TRUE'
---- End block 'FlatFileCases.m_FlatFileTargetTruncate.StudentsOut'
```

#### Best Practices

- Add an explicit `REMOVE` on the stage prefix before the unload if the previous file must be cleared; note that the generated `COPY INTO` already uses `OVERWRITE = TRUE` for the file it writes.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0086

Single-argument TRUNC of a TIME value has no Snowflake equivalent.

### Severity

Medium

#### Description

This issue is reported when single-argument `TRUNC` is applied to a `TIME` port. Snowflake has no equivalent for that call: `TRUNC` rejects `TIME` values and `DATE_TRUNC` rejects the `'DAY'` part for `TIME`, so the original call is left in place and must be rewritten with the intended granularity.

#### Code Example

##### Input Code:

##### Informatica

```
TRUNC(TIME_COL)
```

##### Output Code:

##### Snowflake

Copy code

```
WITH source_data AS
(
   SELECT
      TIME_COL
   FROM
      {{ ref('stg_raw__SQ_SRC') }}
)
SELECT
   TIME_COL AS TIME_COL,
   !!!RESOLVE EWI!!! /*** SSC-EWI-INF0086 - SINGLE-ARGUMENT TRUNC OF A TIME VALUE HAS NO SNOWFLAKE EQUIVALENT: TRUNC REJECTS TIME AND DATE_TRUNC REJECTS THE 'DAY' PART FOR TIME. REVIEW THE INTENDED GRANULARITY (E.G. DATE_TRUNC('HOUR', ...)). ***/!!!
   TRUNC(TIME_COL) AS OUT_COL
FROM
   source_data
```

#### Best Practices

- Replace the call with an explicit granularity that Snowflake accepts for `TIME`, for example `DATE_TRUNC('HOUR', TIME_COL)` or `DATE_TRUNC('MINUTE', TIME_COL)`.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0087

Target has no TARGETFIELD definitions in the export.

### Severity

High

#### Description

This issue is reported when a target carries no `TARGETFIELD` definitions in the Informatica export, which usually happens for a shortcut whose shared-folder definition was not included in the conversion. Because the column list is unknown, `SELECT *` is emitted as a passthrough and the mart projection must be completed manually.

#### Code Example

##### Input Code:

##### Informatica

Copy code

```
<TARGET BUSINESSNAME="" CONSTRAINT="" DATABASETYPE="Microsoft SQL Server" DESCRIPTION="" NAME="Shortcut_To_DP_DR" OBJECTVERSION="1" TABLEOPTIONS="" VERSIONNUMBER="1">
</TARGET>
```

##### Output Code:

##### Snowflake

Copy code

```
!!!RESOLVE EWI!!! /*** SSC-EWI-INF0087 - TARGET 'Shortcut_To_DP_DR' HAS NO TARGETFIELD DEFINITIONS IN THE EXPORT (OFTEN A SHORTCUT WHOSE SHARED-FOLDER DEFINITION WAS NOT INCLUDED). SELECT * IS EMITTED AS A PASSTHROUGH; REVIEW AND COMPLETE THE MART PROJECTION MANUALLY. ***/!!!
WITH source_data AS
(
   SELECT
      *
   FROM
      {{ ref('int_SEQTRANS') }}
)
SELECT
   *
FROM
   source_data AS sd
```

#### Best Practices

- Re-export the mapping with the shared folder that declares the target, then re-run the conversion so the real column list is generated instead of `SELECT *`.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0088

Lookup Source Filter not fully converted.

### Severity

Medium

#### Description

This issue is reported when the Lookup Source Filter of a lookup cannot be fully converted. The generated lookup runs without that predicate, so it can match more rows than the original lookup did and the missing condition must be added manually.

#### Code Example

##### Input Code:

##### Informatica

Copy code

```
<TABLEATTRIBUTE NAME="Lookup Source Filter" VALUE="UNPARSEABLE_FILTER_MARKER"/>
```

##### Output Code:

##### Snowflake

Copy code

```
{% macro ulkp_dim_dept_scd2(in_skid) %}
(
    SELECT MAX(DeptName)
    FROM {{ source('raw', 'DIM_Dept_SCD2') }} AS lkp
    WHERE
   !!!RESOLVE EWI!!! /*** SSC-EWI-INF0088 - THE LOOKUP SOURCE FILTER 'UNPARSEABLE_FILTER_MARKER' COULD NOT BE FULLY CONVERTED. THE GENERATED LOOKUP RUNS WITHOUT THIS FILTER APPLIED. REVIEW THE ORIGINAL FILTER AND ADD THE MISSING PREDICATE MANUALLY. ***/!!!
   lkp.SK_ID = {{ in_skid }}
   AND true
)
{% endmacro %}
```

#### Best Practices

- Translate the original Lookup Source Filter by hand and replace the `AND true` placeholder with the equivalent predicate so the lookup returns the same rows as in PowerCenter.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).

## SSC-EWI-INF0098

Self-referential local variable port with an unrecognized IIF shape emitted with no translation.

### Severity

High

#### Description

This issue is reported when a local variable port references its own name inside an `IIF` but not in a recognized running-total shape — `V = IIF(condition, V, V + literal)` or its mirror. The expression is emitted verbatim, which produces a self-referencing identifier in the same `SELECT` scope and does not compile in Snowflake, so the port must be rewritten by hand.

#### Code Example

##### Input Code:

##### Informatica

Copy code

```
<TRANSFORMFIELD DATATYPE="double" EXPRESSION="IIF(ACCOUNT_NR = 'FOOTER', V_Total, V_Total + AMOUNT)" NAME="V_Total" PORTTYPE="LOCAL VARIABLE" PRECISION="15" SCALE="0"/>
```

##### Output Code:

##### Snowflake

Copy code

```
!!!RESOLVE EWI!!! /*** SSC-EWI-INF0098 - THIS LOCAL VARIABLE PORT SELF-REFERENCES ITS OWN NAME INSIDE AN IIF, BUT NOT IN A RECOGNIZED RUNNING-TOTAL SHAPE (V = IIF(CONDITION, V, V + LITERAL) OR ITS MIRROR). THE EXPRESSION IS EMITTED VERBATIM, WHICH PRODUCES A SELF-REFERENCING IDENTIFIER IN THE SAME SELECT SCOPE AND WILL NOT COMPILE. MANUALLY REWRITE THIS PORT AS AN EXPLICIT ACCUMULATOR OR WINDOW FUNCTION. ***/!!!
IFF(ACCOUNT_NR = 'FOOTER', V_Total, V_Total + AMOUNT) AS V_Total
```

#### Best Practices

- Rewrite the port as an explicit accumulator or as a window function, for example `SUM(...) OVER (ORDER BY ... ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)`, using a deterministic ordering column.
- Where the increment is another port rather than a literal, compute that value in an upstream expression first so the accumulation is expressible as a single window function.
- Use the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview) to get AI-powered explanations and actionable solutions for this issue.
- If you need more support, email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com).
