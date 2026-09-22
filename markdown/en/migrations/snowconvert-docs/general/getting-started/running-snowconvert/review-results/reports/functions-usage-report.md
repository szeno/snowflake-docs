# SnowConvert AI - Functions Usage Report

## What is an “function usage”?

The term “usage” is used in this context to indicate that a specific function was invoked in the code. This function could be a built-in or user-defined function in a source language.

These are some examples of places where functions can be invoked in SQL languages:

- Any DDL, `CREATE TABLE` default columns value or as part of a `CREATE VIEW` select using a function.
- Any DML, like `INSERT` and `DELETE`.
- In procedural language, assign the returned value of a function to a sql variable
- In the `FROM` using table valued functions.

### Where can I find it?

The Functions Usage report can be found in a folder named *“reports”*, in the output folder of your conversion. The name of the file itself starts with *“SqlFunctionsUsage”* so it can easily be located.

The format of the file is **.CSV**.

### What information does it contain?

The function usage report is presented in a table format, and contains the following columns:

| Column | Description |
| --- | --- |
| Function | The name of the function found in code, or its signature in the case of a UDF. |
| Count | The function’s usage summarized count by migration status. |
| Category | The function category. These can be User\_Defined, Built\_In, or Uncategorized. |
| Migration Status | The migration status of the function invocation. These can be Pending (not transformed to Snowflake), PendingSPCall (requires manual intervention because it was converted to a stored procedure), and Transformation (successfully converted to Snowflake). |

#### Summarization

Each individual function usage is summarized using a specific criterion that may include multiple columns to form a “composite key”. The basic grouping is made using the Category, and Migration Status columns.
