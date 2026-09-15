description:
:   Everything generated in assessment mode

# Snowpark Migration Accelerator: Output Reports

The assessment phase of this accelerator generates multiple detailed reports, including:

[![Output Reports](/static/images/migrations/sma-assets/image(34).png)](/static/images/migrations/sma-assets/image(34).png)

Let’s organize these reports into three distinct categories to make them easier to understand.

- [Curated Reports](/migrations/sma-docs/user-guide/scos-conversion/output-reports/curated-reports) - Detailed, formatted reports that provide in-depth analysis of the information shown in the application.
- [SMA Inventories](/migrations/sma-docs/user-guide/scos-conversion/output-reports/sma-inventories) - Detailed spreadsheets that help you understand the analyzed codebase.
- [Assessment zip file](/migrations/sma-docs/user-guide/scos-conversion/output-reports/assessment-zip-file) - A compressed file containing all reports, useful for offline review or sharing.

These generated files provide detailed analysis and insights about your codebase after processing it through the tool.

To view the reports, click the “View Reports” button located at the bottom of the application.

[![View Reports](/static/images/migrations/sma-assets/ViewReports.png)](/static/images/migrations/sma-assets/ViewReports.png)

Inside the “Reports” directory of your specified output folder, you will find several files. These files are similar to those shown in the first image above.

- AssessmentReport.json - Main assessment report in JSON format
- DetailedReport.docx - Comprehensive analysis report in Word format
- DetailedReport.html - HTML version of detailed report (deprecated since Spark Conversion Core V2.43.0)
- files.csv - List of processed files
- GenericScanner

  - GenericScannerOutput
    - files.pam - Scanner output file for file analysis
    - FilesInventory.csv - Complete inventory of scanned files
    - KeywordCounts.csv - Statistics of keyword usage
    - line\_counts.pam - Line count analysis data
    - tool\_execution.pam - Tool execution logs
    - word\_counts.pam - Word frequency analysis
- ImportUsagesInventory.csv - Inventory of import statements
- InputFilesInventory.csv - List of input files processed
- IOFilesInventory.csv - Input/Output operations inventory
- Issues.csv - List of identified issues and problems
- JoinsInventory.csv - Analysis of join operations
- NotebookCellsInventory.csv - Inventory of notebook cells
- NotebookSizeInventory.csv - Size analysis of notebooks
- PandasUsagesInventory.csv - List of Pandas library usage
- SparkUsagesInventory.csv - Inventory of Spark operations
- SqlStatementsInventory.csv - List of SQL statements
- SummaryReport.docx - Brief overview report (deprecated since Spark Conversion Core V2.43.0)
- SummaryReport.html - HTML version of summary (deprecated since Spark Conversion Core V2.43.0)
- ThirdPartyUsagesInventory.csv - Inventory of third-party library usage
- tool\_execution.csv - Execution logs and statistics

Let’s examine each category in detail.
