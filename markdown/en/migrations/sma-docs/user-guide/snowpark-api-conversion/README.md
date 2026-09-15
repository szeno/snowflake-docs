description:
:   Convert your source code to Snowflake

# Snowpark Migration Accelerator: Conversion

The Snowpark Migration Accelerator (SMA) begins by evaluating your Spark workload through an assessment process. Beyond assessment, SMA can also transform specific components of your Spark application into Snowpark-compatible code.

This section covers the following topics:

- [How the conversion works](/migrations/sma-docs/user-guide/snowpark-api-conversion/how-the-conversion-works)
- [Conversion Quick Start](/migrations/sma-docs/user-guide/snowpark-api-conversion/conversion-quick-start)
- Understanding your conversion results
- Reviewing conversion outputs (including reports, logs, and converted code)
- Working with your converted code
- What to do next

The Snowpark Migration Accelerator (SMA) partially converts Spark API references to Snowpark API. While it cannot convert all references, it is designed to be transparent about its limitations. The tool provides clear issue and error codes to guide users on necessary manual interventions. This dual functionality - converting what’s possible while clearly identifying what requires manual attention - is one of SMA’s most valuable features.

When converting code, it’s important to understand how to interpret the issues reported by the Snowpark Migration Accelerator (SMA). We have a dedicated section that covers issue analysis in detail, which includes:

- [Approach to resolving issues](/migrations/sma-docs/issue-analysis/approach)
- [Issue codes by Source](/migrations/sma-docs/issue-analysis/issue-codes-by-source/README)
- [Troubleshooting through the issues](/migrations/sma-docs/issue-analysis/troubleshooting-the-output-code/README)
- [Dealing with Workarounds](/migrations/sma-docs/issue-analysis/workarounds)
- [Deploying the output code](/migrations/sma-docs/issue-analysis/deploying-the-output-code)

Understanding these concepts is crucial for determining whether a conversion will be successful.

---

Let’s explore how the conversion process works.
