description:
:   Understanding the conversion results and what comes next

# Snowpark Migration Accelerator: Understanding the Conversion Summary

After running a conversion, you can view the initial results and summary in the Conversion Summary Report.

Keep in mind that this report summarizes the information from the inventory files created in the [Output Reports](/migrations/sma-docs/user-guide/scos-conversion/output-reports/README) folder during the SMA execution. For a comprehensive analysis, review the [Detailed Report](/migrations/sma-docs/user-guide/scos-conversion/output-reports/README) in the output directory.

The Conversion Results section of the application contains several components, which are explained in detail below.

## Standard Conversion Summary

The summary will appear as shown below:

[![Conversion Summary](/static/images/migrations/sma-assets/AssessmentSummary.png)](/static/images/migrations/sma-assets/AssessmentSummary.png)

In the top-right corner of the report, the **Execution date** indicates when the analysis was run.

### Snowpark Connect Readiness Score

The Snowpark Connect Readiness Score will look something like this:

[![Snowpark Connect Readiness Score](/static/images/migrations/sma-assets/understanding-the-assessment-summary-snowpark-connect-readiness-score.png)](/static/images/migrations/sma-assets/understanding-the-assessment-summary-snowpark-connect-readiness-score.png)

1. **Readiness Score** - It will show you the readiness score you obtained. The Snowpark Connect readiness score indicates the proportion of Spark API references that are supported by Snowpark Connect. This score is calculated by dividing the number of supported Spark API references by the total Spark API references. You can learn more about this score in the [Snowpark Connect Readiness Score](/migrations/sma-docs/user-guide/scos-conversion/readiness-scores) section.
2. **Score Explanation** - An explanation of what the Snowpark Connect Readiness score is and how to interpret it.
3. **Next Steps** - Depending on the readiness score obtained, the SMA will advise you on what actions you should take before proceeding to the next step.
4. **Score Breakdown** - A detailed explanation of how the Snowpark Connect Readiness Score was calculated. In this case, it will show you the number of Spark API references supported by Snowpark Connect divided by the total number of Spark API references.

**Supported Usages** refers to the number of Spark API references in a workload that are supported by Snowpark Connect. In contrast, **identified usages** represents the total count of Spark API references found within that workload.

### Spark API Usages

Danger

The **Spark API Usages** section has been deprecated since version **2.0.2**. You can now find:

- A summary of Spark API usage in [the Detailed Report](/migrations/sma-docs/user-guide/scos-conversion/output-reports/curated-reports)
- A complete list of all Spark API usage instances in [the Spark API Usages Inventory](/migrations/sma-docs/user-guide/scos-conversion/output-reports/sma-inventories)

The report contains three main sections displayed as tabs:

1. Overall Usage Classification
2. Spark API Usage Categorization
3. Spark API Usages By Status

We will examine each section in detail below.

#### Overall Usage Classification

This tab displays a table containing three rows that show:

- Supported operations
- Unsupported operations
- Total usage statistics

[![Overall Usage Classification](/static/images/migrations/sma-assets/image(55).png)](/static/images/migrations/sma-assets/image(55).png)

Additional details are provided in the following section:

1. **Usages Count** - The total number of times Spark API functions are referenced in your code. Each reference is classified as either supported or unsupported, with totals shown at the bottom.
2. **Files with at least 1 usage** - The number of files that contain at least one Spark API reference. If this number is less than your total file count, it means some files don’t use Spark API at all.
3. **Percentage of All Files** - Shows what portion of your files use Spark API. This is calculated by dividing the number of files with Spark API usage by the total number of code files, expressed as a percentage.

#### Spark API Usage Categorization

This tab displays the different types of Spark references detected in your codebase. It shows the overall Readiness Score (which is the same score shown at the top of the page) and provides a detailed breakdown of this score by category.

[![Spark API Usage Categorization](/static/images/migrations/sma-assets/image(48).png)](/static/images/migrations/sma-assets/image(48).png)

You can find all available categorizations in the [Spark Reference Categories](/migrations/sma-docs/user-guide/scos-conversion/spark-reference-categories) section.

#### Spark API Usages By Status

The final tab displays a categorical breakdown organized by mapping status.

[![Spark API Usages by Status](/static/images/migrations/sma-assets/image(49).png)](/static/images/migrations/sma-assets/image(49).png)

The SMA tool uses seven main mapping statuses, which indicate how well Spark code can be converted to Snowpark. For detailed information about these statuses, refer to the [Spark Reference Categories](/migrations/sma-docs/user-guide/scos-conversion/spark-reference-categories) section.

### Import Calls

Danger

The **Import Calls** section has been removed since version **2.0.2**. You can now find:

- A summary of import statements in [the Detailed Report](/migrations/sma-docs/user-guide/scos-conversion/output-reports/curated-reports)
- A complete list of all import calls in [the Import Usages Inventory](/migrations/sma-docs/user-guide/scos-conversion/output-reports/sma-inventories)

The “Import Calls” section displays frequently used external library imports found in your codebase. Note that Spark API imports are excluded from this section, as they are covered separately in the “Spark API” section.

[![Import Calls](/static/images/migrations/sma-assets/image(46).png)](/static/images/migrations/sma-assets/image(46).png)

This table contains the following information:

The report displays the following information:

1. A table with 5 rows showing:

   - The 3 most frequently imported Python libraries
   - An “Other” row summarizing all remaining packages
   - A “Total” row showing the sum of all imports
2. A “Supported in Snowpark” column indicating whether each library is included in Snowflake’s [list of supported packages in Snowpark](https://repo.anaconda.com/pkgs/snowflake/).
3. An “Import Count” column showing how many times each library was imported across all files.
4. A “File Coverage” column showing the percentage of files that contain at least one import of each library. For example:

   - If ‘sys’ appears 29 times in the import statements but is only used in 28.16% of files, this suggests it’s typically imported once per file where it’s used.
   - The “Other” category might show 56 imports occurring across 100% of files.

For detailed import information per file, refer to the ImportUsagesInventory.csv file in the [Output Reports](/migrations/sma-docs/user-guide/scos-conversion/output-reports/README).

### File Summary

Danger

The **File Summary** section has been removed since version **2.0.2**. You can now find:

- A summary of files and file types in [the Detailed Report](/migrations/sma-docs/user-guide/scos-conversion/output-reports/curated-reports)
- A complete list of all files (both analyzed and not analyzed) in [the File Inventory](/migrations/sma-docs/user-guide/scos-conversion/output-reports/sma-inventories)

The summary report contains multiple tables displaying metrics organized by file type and size. These metrics provide insights into the codebase’s volume and help estimate the required effort for the migration project.

The Snowpark Migration Accelerator analyzes all files in your source codebase, including both code and non-code files. You can find detailed information about the scanned files in the [files.csv](/migrations/sma-docs/user-guide/scos-conversion/output-reports/README) report.

The File Summary contains multiple sections. Let’s examine each section in detail.

#### File Type Summary

The File Type Summary displays a list of all file extensions found in your scanned code repository.

[![File Type Summary](/static/images/migrations/sma-assets/image(41).png)](/static/images/migrations/sma-assets/image(41).png)

The file extensions listed indicate which types of code files SMA can analyze. For each file extension, you will find the following information:

- **Lines of Code** - The total number of executable code lines across all files with this extension. This count excludes comments and empty lines.
- **File Count** - The total number of files found with this extension.
- **Percentage of Total Files** - The percentage that files with this extension represent out of all files in the project.

To analyze your workload, you can easily identify whether it primarily consists of script files (such as Python or R), notebook files (like Jupyter notebooks), or SQL files. This information helps determine the main types of code files in your project.

#### Notebook Sizing by Language

The tool evaluates notebooks in your codebase and assigns them a “t-shirt” size (S, M, L, XL) based on the number of code lines they contain. This sizing helps estimate the complexity and scope of each notebook.

[![Notebook Sizing By Language](/static/images/migrations/sma-assets/image(42).png)](/static/images/migrations/sma-assets/image(42).png)

The notebook sizes are categorized according to the main programming language used within each notebook.

#### Notebook Stats By Language

This table displays the total number of code lines and cells in all notebooks, organized by programming language.

[![Notebook Stats by Language](/static/images/migrations/sma-assets/image(43).png)](/static/images/migrations/sma-assets/image(43).png)

These notebooks are organized by the primary programming language used within them.

#### Code File Content

When running SMA, the tab name will change based on your source language:

- For Python source files, the tab will display “Python File Content”
- For Scala source files, the tab will display “Scala File Content”

This row shows how many files contain Spark API references. The “Spark Usages” row displays:

1. The number of files that use Spark APIs
2. What percentage these files represent of the total codebase files analyzed

[![Code File Content](/static/images/migrations/sma-assets/image(44).png)](/static/images/migrations/sma-assets/image(44).png)

This metric helps identify what percentage of files do not contain Spark API references. A low percentage suggests that many code files lack Spark dependencies, which could mean the migration effort might be smaller than initially estimated.

#### Code File Sizing

The File Sizing tab name changes based on your source language:

- For Python source files, it displays as “Python File Sizing”
- For Scala source files, it displays as “Scala File Sizing”

The codebase files are categorized using “t-shirt” sizes (S, M, L, XL). Each size has specific criteria described in the “Size” column. The table also shows what percentage of all Python files falls into each size category.

[![Code File Sizing](/static/images/migrations/sma-assets/image(45).png)](/static/images/migrations/sma-assets/image(45).png)

Understanding the file size distribution in your codebase can help assess workload complexity. A high percentage of small files typically suggests simpler, less complex workloads.

### Issues Summary

The Issues Summary provides critical information about potential problems found during code scanning. During conversion, you’ll see a list of EWIs (Errors, Warnings, and Issues) detected in your codebase. For a detailed explanation of these issues, refer to the Issue Analysis section in the documentation.

[![Issues Summary](/static/images/migrations/sma-assets/04-IssuesSummary.png)](/static/images/migrations/sma-assets/04-IssuesSummary.png)

At the top of the issue summary, you will find a table that provides an overview of all identified issues.

[![Issues Summary - Summary Table](/static/images/migrations/sma-assets/05-IssuesSummary-SummaryTable.png)](/static/images/migrations/sma-assets/05-IssuesSummary-SummaryTable.png)

The table contains two rows.

- The “Number of issues” represents the total count of all issue codes found in each category.
- The “Number of unique issues” represents the count of distinct error codes found in each category.

The problems are divided into three main categories:

- **Warnings** indicate potential differences between source and target platforms that may not require immediate action but should be considered during testing. These could include slight variations in behavior for edge cases or notifications about changes in appearance compared to the source platform.
- **Conversion issues** highlight elements that either failed to convert or need additional configuration to work properly in the target platform.
- **Parsing issues** occur when the tool cannot interpret specific code elements. These are critical issues requiring immediate attention, typically caused by non-compiling source code or incorrect code extraction. If you believe your source code is correct but still receive parsing errors, it may be due to an unrecognized pattern in SMA. In such cases, [report an issue](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings) and include the problematic source code section.

The table summarizes the total count for each item.

Below this table, you will find a list of unique issue codes and their descriptions.

[![Issue Summary - Issue Code Table](/static/images/migrations/sma-assets/06-IssueSummary-IssueCodeTable.png)](/static/images/migrations/sma-assets/06-IssueSummary-IssueCodeTable.png)

Each issue code entry provides:

- The unique issue identifier
- A description of the issue
- The number of occurrences
- The severity level (Warning, Conversion Error, or Parsing Error)

You can click any issue code to view detailed documentation that includes:

- A full description of the issue
- Example code
- Recommended solutions

For instance, clicking the first issue code shown above (SPRKPY1002) will take you to its dedicated documentation page.

By default, the table displays only the top 5 issues. To view all issues, click the SHOW ALL ISSUES button located below the table. You can also use the search bar above the table to find specific issues.

Understanding the remaining conversion work is crucial. You can find detailed information about each issue and its location in the issue inventory within the [Reports folder](/migrations/sma-docs/user-guide/scos-conversion/output-reports/README).

### Execution Summary

The execution summary provides a comprehensive overview of the tool’s recent analysis. It includes:

- The code analysis score
- User details
- The unique execution ID
- Version information for both SMA and Snowpark API
- Project folder locations that were specified during [Project Creation](/migrations/sma-docs/user-guide/project-overview/project-setup)

[![Execution Summary](/static/images/migrations/sma-assets/ExecutionSummary(1).png)](/static/images/migrations/sma-assets/ExecutionSummary(1).png)

### Appendixes

The appendixes contain additional reference information that can help you better understand the output generated by the SMA tool.

[![image (512).png](/static/images/migrations/sma-assets/image(512).png)](/static/images/migrations/sma-assets/image(512).png)

This guide contains general reference information about using the Snowpark Migration Accelerator (SMA). While the content may be updated periodically, it focuses on universal SMA usage rather than details about specific codebases.

---

This is what most users will see when they run the Snowpark Migration Accelerator (SMA). If you are using an older version, you might see the Abbreviated Conversion Summary instead, which is shown below.

## Abbreviated Conversion Summary [Deprecated]

If your readiness score is low, your migration summary might appear as follows:

[![Conversion Summary](/static/images/migrations/sma-assets/image(495).png)](/static/images/migrations/sma-assets/image(495).png)

This summary contains the following information:

- **Execution Date**: Shows when your analysis was performed. You can view results from any previous execution for this project.
- **Result**: Indicates if your workload is suitable for migration based on the [readiness score](/migrations/sma-docs/support/glossary). The readiness score is a preliminary assessment tool and does not guarantee migration success.
- **Input Folder**: Location of the source files that were analyzed.
- **Output Folder**: Location where analysis reports and converted code files are stored.
- **Total Files**: Number of files analyzed.
- **Execution Time**: Duration of the analysis process.
- **Identified Spark References**: Number of Spark API calls found in your code.
- **Count of Python (or Scala) Files**: Number of source code files in the specified programming language.

---

## Next Steps

The application provides several additional features, which can be accessed through the interface shown in the image below.

[![](/static/images/migrations/sma-assets/image(54).png)](/static/images/migrations/sma-assets/image(54).png)

- **Retry Conversion** - You can run the conversion again by clicking the **Retry Conversion** button on the Conversion Results page. This is useful when you make changes to the source code and want to see updated results.
- **View Reports** - Opens the folder containing conversion output reports. These include the detailed conversion report, Spark reference inventory, and other analyses of your source codebase. Each report type is explained in detail in this documentation.

The following pages provide detailed information about the reports generated each time the tool runs.
