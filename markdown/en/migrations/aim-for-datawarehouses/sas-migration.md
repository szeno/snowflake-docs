# Snowflake AIM Agent for Data Warehouses - SAS Migration

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts. This preview covers SAS assessment and code conversion.

The Snowflake AIM Agent for Data Warehouses supports migrating SAS workloads to Snowflake through natural-language requests. This capability runs alongside the agent’s core deterministic conversion workflow and uses an AI-based approach tailored to SAS source code.

## What’s supported

- **Assessment**: Analyzes your SAS codebase and produces a report covering complexity, volume, and dependencies between programs, so you can plan your migration before converting any code.
- **Code conversion**: Converts SAS programs to Snowflake SQL, with a validation step to help confirm the converted logic behaves as expected.
- **Dataset loading**: Loads SAS dataset files (`.sas7bdat`) into Snowflake tables.

## What’s not included yet

SAS migration does not currently include:

- Deterministic, grammar-based code conversion (SAS conversion is AI-based only)
- Integration with the cloud data migration and validation framework used for other source systems
- Integration with the [testing framework](/migrations/aim-for-datawarehouses/testing/overview)
- Power BI report repointing

For the full list of capabilities and source systems covered by the core migration workflow, see the [supported source systems matrix](/migrations/aim-for-datawarehouses/overview#supported-source-systems).

## How to use it

Ask the Snowflake AIM Agent for Data Warehouses directly. For example:

Copy code

```
"Assess my SAS codebase for a Snowflake migration"
```

Copy code

```
"Convert this SAS program to Snowflake SQL"
```

Copy code

```
"Load this SAS dataset into Snowflake"
```

The agent determines whether you’re working with SAS programs or SAS datasets and guides you through the appropriate next steps.

For assessment details that apply to other source systems, see [Assessment](/migrations/aim-for-datawarehouses/assessment). For more on how code conversion works generally, see [Code Conversion](/migrations/aim-for-datawarehouses/code-conversion/intro).
