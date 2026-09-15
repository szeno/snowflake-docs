description:
:   Get ready to run the SMA

# Snowpark Migration Accelerator: Notes on Code Preparation

Before running Snowpark Migration Accelerator (SMA), make sure all your source code files are located on the computer where you installed SMA. You don’t need to connect to any source database or Spark environment since SMA only performs code analysis.

The source code must be in a readable format for SMA to process it correctly, as the tool relies completely on the source code you provide.

## Extraction

Before running the Snowpark Migration Accelerator (SMA), organize all your source code files into a single main folder. You can maintain your existing subfolder structure within this main folder, but all code files must be located under this one directory. This requirement applies to:

The following file types are supported:

- GitHub repositories (downloaded as ZIP files and extracted to your local machine)
- Python script files
- Scala project files
- Databricks notebook files
- Jupyter notebooks run on your local computer

Before starting your migration, gather all source code files into a single main folder. While your source code may come from different locations, having it organized in one place will make the migration process more efficient. If you already have an established file organization structure, keep it intact within the main folder.

[Export GitHub repositories to ZIP files](https://docs.github.com/en/repositories/working-with-files/using-files/downloading-source-code-archives)

To generate accurate and complete reports using the Snowpark Migration Accelerator (SMA), scan only the code that is relevant to your migration project. Rather than scanning all available code, identify and include only the essential code files that you plan to migrate. For more information, refer to [Size](/migrations/sma-docs/use-cases/assessment-walkthrough/walkthrough-setup/notes-on-code-preparation) in the [Considerations](/migrations/sma-docs/use-cases/assessment-walkthrough/walkthrough-setup/notes-on-code-preparation) section.

## Considerations

Let’s review which file types are compatible with Snowpark Migration Accelerator (SMA) and understand the key considerations when preparing your source code for analysis with SMA.

### Filetypes

The Snowpark Migration Accelerator (SMA) examines all files in your source directory, but only processes files with specific extensions that may contain Spark API code. This includes both regular code files and Jupyter notebooks.

You can find a list of file types that SMA supports in the [Supported Filetypes section of this documentation](/migrations/sma-docs/user-guide/before-using-the-sma/supported-filetypes).

### Exported Files

If your code is stored in a source control platform instead of local files, you need to export it into a format that SMA can process. Here’s how you can export your code:

For Databricks users: To use the Snowpark Migration Accelerator (SMA), you need to export your notebooks to .dbc format. You can find detailed instructions on how to export notebooks in [the Databricks documentation on exporting notebooks](https://docs.databricks.com/en/notebooks/notebook-export-import.html#export-notebooks.).

Need help exporting files? Visit [the export scripts in the Snowflake Labs Github repo](https://github.com/Snowflake-Labs/SC.DDLExportScripts/tree/main), where Snowflake Professional Services maintains scripts for Databricks, Hive, and other platforms.

- If you are using a different platform, please refer to the [Code Extraction page](/migrations/sma-docs/user-guide/before-using-the-sma/code-extraction) for specific instructions for your platform. If you need assistance converting your code into a format that works with SMA, please contact [sma-support@snowflake.com](mailto:sma-support@snowflake.com).

### Size

The Snowpark Migration Accelerator (SMA) is designed to analyze source code, not data. To ensure optimal performance and prevent system resource exhaustion, we recommend:

1. Only include the specific code files you want to migrate
2. Avoid including unnecessary library dependencies

While you can include dependent library code files, doing so will significantly increase processing time without adding value, since SMA specifically focuses on identifying Spark code that requires migration.

We recommend gathering all code files that…

- Run automatically as part of a scheduled process
- Were used to create or configure that process (if they are separate)
- Are custom libraries created by your organization that are used in either of the above scenarios

You don’t need to include code for common third-party libraries such as Pandas or Sci-Kit Learn. The tool will automatically detect and catalog these library references without requiring their source code.

### Does it run?

The Snowpark Migration Accelerator (SMA) can only process complete and syntactically correct source code. Your code must be able to run successfully in [a supported source platform](/migrations/sma-docs/user-guide/before-using-the-sma/supported-platforms). If the SMA reports multiple [parsing errors](/migrations/sma-docs/issue-analysis/issue-code-categorization), this usually indicates that your source code contains syntax errors. To achieve the best results, ensure that your input directory contains only valid code that can be executed on the source platform.

### Use Case

Understanding your codebase’s purpose is essential when reviewing scan results. It will help you:

1. Determine which applications or processes may not work well with Snowpark
2. Understand and analyze readiness assessment results more effectively
3. Check if your existing code and systems are compatible with Snowflake

When scanning a notebook that uses an unsupported SQL dialect and a database connector without Spark, the SMA will only display imported third-party libraries. While this information is helpful, the notebook will not receive a Spark API Readiness Score. Understanding how you plan to use your code will help you better understand these limitations and make better decisions during migration.

### Exports from Databricks Notebooks

Databricks notebooks support multiple programming languages such as SQL, Scala, and PySpark in a single notebook. When you export a notebook, the file extension will reflect its primary language:

- Python notebooks: .ipynb or .py
- SQL notebooks: .sql

Any code written in a language different from the notebook’s primary language will be automatically converted to comments during export. For instance, if you include SQL code in a Python notebook, the SQL code will appear as comments in the exported file.

[![Commented Code when Exported](/static/images/migrations/sma-assets/commentedCodeWhenExported.png)](/static/images/migrations/sma-assets/commentedCodeWhenExported.png)

Code comments are excluded from SMA analysis. To ensure your code is properly analyzed, place it in a file with the correct file extension matching the source language. For example:

- Python code should be in .py files
- SQL code should be in .sql files

Note that even uncommented code will not be analyzed if it’s in a file with the wrong extension (such as Python code in a .sql file).

Before using the tool, please read the [Pre-Processing Considerations](/migrations/sma-docs/user-guide/before-using-the-sma/pre-processing-considerations) section in our documentation. This section contains essential information that you need to know before proceeding.

## Walkthrough Codebase

Select one of the extracted sample codebase directories as the input for the Snowpark Migration Accelerator (SMA).

When migrating code, maintain your original folder structure. This preserves file organization and helps developers understand the code architecture. Both the code conversion process and assessment analysis are performed one file at a time.

For this tutorial, we will work with small, functional Spark code samples (each less than 1MB). These samples showcase different scenarios and functions that can be converted. Although these examples are simplified versions and not production code, they effectively demonstrate various conversion possibilities.

The source directory can contain Jupyter notebooks (.ipynb), Python scripts (.py), and text files. While SMA examines all files in your codebase, it only searches for Spark API references in Python (.py) files and Jupyter notebook (.ipynb) files.
