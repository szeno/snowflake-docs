description:
:   Everything you need for this walkthrough

# Snowpark Migration Accelerator: Walkthrough Setup

This guide offers practical experience with the Snowpark Migration Accelerator (SMA). Through real-world examples, you will learn how to evaluate code and interpret assessment results, giving you a clear understanding of the tool’s capabilities.

## Materials

To complete this tutorial, you will need the following:

- A computer that has Snowpark Migration Accelerator (SMA) software installed
- Access to the sample code files on the same computer

To begin, you will need two items on your computer:

1. The Snowpark Migration Accelerator (SMA) tool
2. Code samples

Let’s walk through how to obtain these essential resources.

### SMA Application

The Snowpark Migration Accelerator (SMA) helps developers convert their PySpark and Spark Scala applications to run on Snowflake. It automatically detects Spark API calls in your Python or Scala code and transforms them into equivalent Snowpark API calls. This guide will demonstrate basic SMA functionality by analyzing sample Spark code and showing how it assists with migration projects.

During the initial assessment phase, Snowpark Migration Accelerator (SMA) examines your source code and builds a detailed model that captures all the functionality in your code. Based on this analysis, SMA creates several reports, including a detailed assessment report that we’ll review in this walkthrough. These reports help you understand how ready your code is for migration to Snowpark and estimate the effort needed for the transition. We’ll look at these findings in more detail as we continue through this lab.

#### Download and Installation

To begin an assessment with the Snowpark Migration Accelerator (SMA), you only need to complete the installation process. While Snowflake provides optional [helpful training on using the SMA](https://learn.snowflake.com/en/courses/spark-to-snowpark-sma/), you can proceed without it. No special access codes are needed. Simply:

1. Visit our [Download and Access](/migrations/sma-docs/general/getting-started/download-and-access) section
2. [Download the installer](https://www.snowflake.com/en/data-cloud/snowpark/migration-accelerator/)
3. Follow our [Installation instructions](/migrations/sma-docs/general/getting-started/installation/README) to set up the application on your computer

### Sample Codebase

This guide uses Python code examples to demonstrate the migration process. We have selected two publicly available sample codebases from third-party Git repositories as unbiased, real-world examples. You can access these codebases at:

- PySpark Data Engineering Examples: <https://github.com/spark-examples/pyspark-examples>
- Apache Spark Machine Learning Examples: <https://github.com/apache/spark/tree/master/examples/src/main/python>

To analyze codebases using the Snowpark Migration Accelerator (SMA), follow these steps:

1. Download the codebases as zip files from GitHub. You can find instructions on how to do this in the [GitHub documentation](https://docs.github.com/en/repositories/working-with-files/using-files/downloading-source-code-archives).
2. Create separate folders on your computer for each codebase.
3. Extract each zip file into its designated folder, as shown in the image below:

[![Directory with Codebases](/static/images/migrations/sma-assets/image(542).png)](/static/images/migrations/sma-assets/image(542).png)

These sample codebases demonstrate how SMA evaluates Spark API references to calculate the [Spark API Readiness Score](/migrations/sma-docs/user-guide/assessment/readiness-scores). Let’s look at two scenarios:

1. A codebase that received a high score, indicating it is highly compatible with Snowpark and ready for migration
2. A codebase that received a low score, indicating it requires additional review and potential modifications before migration

While the readiness score provides valuable insight, it should not be the only factor considered when planning a migration. A comprehensive evaluation of all aspects is necessary for both high and low scoring assessments to ensure a successful migration.

After unzipping the directories, SMA will analyze only files that use supported code formats and notebook formats. These files are checked for references to Spark API and other Third Party APIs. To see which file types are supported, please check the list [here](/migrations/sma-docs/user-guide/before-using-the-sma/supported-filetypes).

Throughout the rest of this walkthrough, we will analyze how these two codebases execute.

## Support

For help with installation or to get access to the code, please email [sma-support@snowflake.com](mailto:sma-support@snowflake.com).

---

After downloading and unzipping the codebases into separate directories, you can either:

- Move on to [running the tool](/migrations/sma-docs/use-cases/assessment-walkthrough/running-the-tool)
- Review [the code preparation notes](/migrations/sma-docs/use-cases/assessment-walkthrough/walkthrough-setup/notes-on-code-preparation)
