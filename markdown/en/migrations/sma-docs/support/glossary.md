description:
:   Every term you ever wanted to know

# Snowpark Migration Accelerator: Glossary

The Snowpark Migration Accelerator (SMA) uses some technical terms that might be unfamiliar. Refer to the glossary page to learn more about these terms.

## Snowpark Migration Accelerator (SMA)

This software documentation explains how to automatically convert Spark API code written in Scala or Python to equivalent Snowflake Snowpark code. The conversion process is secure and maintains the functionality of your original code.

The Snowpark Migration Accelerator (SMA) was previously known as SnowConvert and SnowConvert for Spark. SnowConvert (SC) continues to be available as a tool for SQL conversions.

## Readiness Score

The Readiness Score helps you understand how ready your code is for migration to Snowpark. It calculates the percentage of Spark API references that can be converted to Snowpark API. For example, if 3413 out of 3748 Spark API references can be converted, the readiness score would be 91%.

However, it’s important to note that this score:

- Only considers Spark API references
- Does not evaluate third-party libraries
- Should be used as an initial assessment, not the final decision factor

While a higher score indicates better compatibility with Snowpark, you should also evaluate other factors, such as third-party library dependencies, before proceeding with the migration.

## Spark Reference Categories

The Snowpark Migration Accelerator (SMA) classifies Spark components according to how they map to Snowpark functionality. For each Spark reference, SMA provides:

- A categorization of how it translates to Snowpark
- A detailed description
- Example code
- Information about automatic conversion capability
- Details about Snowpark support

You can find the complete reference guide [on this page](/migrations/sma-docs/user-guide/scos-conversion/spark-reference-categories).

## SnowConvert Qualification Tool

SnowConvert for Spark’s assessment mode analyzes your codebase to automatically detect and identify all instances of Apache Spark Python code.

## File Inventory

A complete list of all files found in the tool’s input directory, regardless of file type. The inventory provides a detailed breakdown organized by file type, including:

- The original technology or platform
- Number of lines of code
- Number of comment lines
- File sizes of the source files

## Keyword Counts

A summary of keyword occurrences organized by technology type. For example, when analyzing a .py file containing PySpark code, the system tracks and counts each PySpark keyword. The report shows the total number of keywords found for each file extension.

## Spark Reference Inventory

After analyzing your code, you will receive a comprehensive list of all Spark API references found in your Python code.

## Readiness Score

The Spark code references will help determine how much of your codebase can be automatically converted.

## Conversion Score

The conversion score is calculated by dividing the number of automatically converted Spark operations by the total number of Spark references detected in the code.

## Conversion/Transformation Rule

Rules that define how SnowConvert transforms source code into the desired target code format.

## Parse

The parsing phase is the first step where SnowConvert analyzes the source code and creates an internal data structure. This structure is then used to apply conversion rules during the migration process.
