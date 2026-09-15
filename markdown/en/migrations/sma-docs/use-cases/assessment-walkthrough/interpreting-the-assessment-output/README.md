description:
:   What to do with all of this assessment information?

# Snowpark Migration Accelerator: Interpreting the Assessment Output

After the tool completes its analysis, you can review the output to make informed decisions. Let’s examine the results to understand how to interpret the data and determine its value for your project.

After the analysis finishes, you’ll see a summary in the application. The detailed assessment results will be saved in the output directory you specified during project creation. The most valuable information from the assessment can be found in the files (artifacts) within this directory.

This guide explains how to interpret and use both the application’s direct output and the complete output directory. Here’s what you need to know:

- **Readiness Score(s)** - SMA generates multiple scores that measure how compatible your code is with Snowflake. For example:

  - The Spark API Readiness Score shows the percentage of Spark API code that can be automatically converted to Snowpark API
  - The SQL Readiness Score indicates how much of your Spark SQL or HiveQL code can be automatically converted to Snowflake SQL

  These scores help you understand how much manual code conversion will be needed.
- **Size** - You can assess the workload size using the File Summary, which shows the total number of files and lines of code. When combined with readiness scores for each file, you can identify which files need more attention during migration.
- More to come, but in the meantime…

Let’s examine the summary page within the application.
