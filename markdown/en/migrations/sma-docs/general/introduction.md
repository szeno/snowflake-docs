description:
:   Assessment and Conversion with the Snowpark Migration Accelerator

# Snowpark Migration Accelerator: Introduction

## Overview of the Snowpark Migration Accelerator

The Snowpark Migration Accelerator (SMA), formerly *SnowConvert for Spark*, helps developers convert code from various platforms to Snowflake. It uses a proven migration framework with 30 years of development to analyze code that contains Spark API calls. The tool creates an Abstract Syntax Tree (AST) and Symbol Table to build a detailed model of how the code works. This model helps convert the original code into equivalent Snowflake code automatically, maintaining the same functionality as the source code.

[![SMA High Level Diagram](/static/images/migrations/sma-assets/image(503).png)](/static/images/migrations/sma-assets/image(503).png)

The Snowpark Migration Accelerator (SMA) analyzes your source code by creating a detailed model that captures its meaning and purpose. This allows SMA to understand how your code works at a deeper level than basic tools that only search and replace text or match patterns.

The SMA scans your source code and notebook files to find all Spark API calls. It then converts these Spark API calls to their matching Snowpark API functions when possible.

## Assessment and Conversion

The Snowpark Migration Accelerator (SMA) has two operating modes:

1. *Assessment* (or *Qualification*) - A free analysis tool that evaluates your code before conversion
2. *Conversion* - Transforms your code to Snowpark

We strongly recommend running the Assessment mode first before starting any code conversion.

### Assessment Mode

Assessment mode helps users find and analyze Spark API usage in their code. SMA scans the source code and builds a *semantic model* using our specialized framework. This model helps SMA understand how the code works and what it does. As a result, SMA can generate detailed and accurate reports about the code’s components.

The SMA analyzes your code to help plan the migration process. It identifies Spark API dependencies and evaluates how ready your code is for migration. Once the assessment is complete, you can move forward with converting your code.

For more information about how SMA assesses your code, please see the [Assessment section of the SMA User Guide](/migrations/sma-docs/user-guide/assessment/README).

### Conversion Mode

During the conversion phase, SMA uses the semantic model created in the assessment phase to automatically generate Snowflake-compatible code. The tool replaces Spark API calls with equivalent Snowpark API calls whenever possible. When direct conversion isn’t possible, SMA adds detailed comments to the output code explaining why certain elements couldn’t be converted and provides helpful context for manual conversion.

## Outline

This section provides comprehensive guidance on the Snowpark Migration Accelerator (SMA), covering the following key areas:

- **Getting Started:**

  - Learn how to [Download and Access](/migrations/sma-docs/general/getting-started/download-and-access) SMA.
  - Step-by-step [Installation](/migrations/sma-docs/general/getting-started/installation/README) guide.
- **End User License Agreement (EULA):** Review the [Conversion Software Terms of Use](/migrations/sma-docs/general/conversion-software-terms-of-use/README).
- **Release Notes:** View the latest [Release Notes](/migrations/sma-docs/general/release-notes/README) to see recent updates and changes.

For assistance or questions, please [Contact Us](/migrations/sma-docs/support/contact-us).

We invite you to start exploring the features and functionalities of the Snowpark Migration Accelerator (SMA).
