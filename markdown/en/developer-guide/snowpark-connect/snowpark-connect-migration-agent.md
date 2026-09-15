# Migrating to Snowpark Connect for Spark

Snowflake provides tooling to automate the migration of existing Spark codebases to Snowpark Connect for Spark.
The recommended approach is the Cortex Code CLI, which can convert your code and validate the
result end to end.

## Automated migration with Cortex Code

The [Cortex Code CLI](/user-guide/cortex-code/cortex-code-cli) includes a `snowpark-connect`
skill that automates the Snowpark Connect for Spark migration process. This is the recommended first step for
migrating your PySpark code. The skill converts your source files, rewrites unsupported patterns,
and optionally smoke-tests the result against a live Snowpark Connect for Spark session.

You can invoke the skill directly or ask questions in natural language:

```
/snowpark-connect "path/to/your/pyspark_file.py"

/snowpark-connect "path/to/your/spark_directory"
```

You can also point the skill at the output of an SMA run to resolve remaining issues that SMA
flagged but didn’t fix automatically.

For full details on the conversion and validation workflow, see
[Spark to Snowpark Connect with the Snowflake CoCo migration skill](/migrations/sma-docs/migrating-with-cortex-code/spark-to-snowpark-connect).

## Assessing compatibility with SMA

If you can’t use Cortex Code, the
[Snowpark Migration Accelerator (SMA)](/migrations/sma-docs/general/introduction) provides a
static analysis alternative. SMA scans your PySpark codebase and produces a **Snowpark Connect
Readiness Score** that measures how compatible your code is with Snowpark Connect for Spark. Unlike Cortex Code,
SMA doesn’t rewrite your code. It generates reports that you use to plan and perform manual fixes.

SMA performs the following analysis:

- Parses every source file and identifies all Spark API references (imports, function calls, class
  instantiations).
- Classifies each reference as supported or unsupported in Snowpark Connect for Spark.
- Calculates a readiness score as the ratio of supported references to total references.
- Generates detailed reports including an API usages inventory, third-party dependency analysis, and
  issue codes with recommended fixes.

The readiness score is color-coded (green, yellow, red) to indicate migration feasibility at a
glance. Even with a high score, review the full report to understand the remaining work. For details
on how to interpret scores and reports, see
[Snowpark Migration Accelerator: Readiness Scores](/migrations/sma-docs/user-guide/scos-conversion/readiness-scores).

### Getting started with SMA

1. Install the Snowpark Migration Accelerator. See
   [Snowpark Migration Accelerator: Getting Started](/migrations/sma-docs/general/getting-started/README).
2. Point it at your existing Spark codebase.
3. Review the [compatibility report](/migrations/sma-docs/user-guide/scos-conversion/understanding-the-conversion-summary).
4. Identify [files that are fully compatible](/migrations/sma-docs/use-cases/snowpark-connect/identifying-fully-compatible-files) and can
   run on Snowpark Connect for Spark immediately.
5. Review remaining issues using the [issue codes](/migrations/sma-docs/issue-analysis/approach) and plan manual fixes.

## Related resources

- [Migrating with Snowflake CoCo](/migrations/sma-docs/migrating-with-cortex-code/README) for migrating with the Cortex Code
  CLI
- [CoCo CLI](/user-guide/cortex-code/cortex-code-cli) for Cortex Code CLI setup and usage
- [Snowpark Migration Accelerator: Introduction](/migrations/sma-docs/general/introduction) for an overview of the Snowpark Migration
  Accelerator
- [Snowpark Migration Accelerator: Snowpark Connect](/migrations/sma-docs/use-cases/snowpark-connect/README) for step-by-step Snowpark Connect for Spark
  migration instructions
