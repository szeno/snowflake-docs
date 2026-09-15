description:
:   Data for Decision Making

# Snowpark Migration Accelerator: SMA Inventories

The Snowpark Migration Accelerator (SMA) analyzes your codebase and produces detailed data, which is stored in the Reports folder as spreadsheets (inventories). This data is used to create two types of reports:

1. The [conversion summary](/migrations/sma-docs/user-guide/scos-conversion/understanding-the-conversion-summary)
2. The [curated reports](/migrations/sma-docs/user-guide/scos-conversion/output-reports/curated-reports)

Understanding the inventory files may seem daunting at first, but they provide valuable insights into both your source workload and the converted workload. Below, we explain each output file and its columns in detail.

These inventories are also shared through telemetry data collection. For more details, refer to the telemetry section of this documentation.

## Assessment Report Details

The **AssessmentReport.json** file stores data that is displayed in both the Detailed Report and Assessment Summary sections of the application. This file is primarily used to populate these reports and may contain information that is also available in other spreadsheets.

## DBX Elements Inventory

The **DbxElementsInventory.csv** lists the DBX elements found inside notebooks.

- **Element:** The DBX element name.
- **ProjectId:** Name of the project (root directory the tool was run on)
- **FileId:** File where the element was found and the relative path to that file.
- **Count:** The number of times that element shows up in a single line.
- **Category:** The element category.
- **Alias:** The alias of the element (applies just for import elements).
- **Kind:** A category for each element. These could include Function or Magic.
- **Line:** The line number in the source files where the element was found.
- **PackageName:** The name of the package where the element was found.
- **Supported:** Whether this reference is “supported” or not. Values: True/False.
- **Automated:** Whether or not the tool can automatically convert it. Values: True/False.
- **Status:** The categorization of each element. The options are Rename, Direct, Helper, Transformation, WorkAround, NotSupported, NotDefined.
- **Statement:** The code where the element was used. [NOTE: This column is not sent via telemetry.]
- **SessionId:** Unique identifier for each run of the tool.
- **SnowConvertCoreVersion:** The version number for the core code process of the tool.
- **SnowparkVersion:** The version of Snowpark API available for the specified technology and run of the tool.
- **CellId:** If this element was found in a notebook file, the numbered location of the cell where this element was in the file.
- **ExecutionId:** The unique identifier for this execution of the SMA.

## Execution Flow Inventory

The **ExecutionFlowInventory.csv** lists the relations between the different workload scopes, based on the function calls found. This inventory main purpose is to serve as the base for the entry points identification.

- **Caller:** The full name of the scope where the call was found.
- **CallerType:** The type of the scope where the call was found. This can be: Function, Class, or Module.
- **Invoked:** The full name of the element that was called.
- **InvokedType:** The type of the element. This can be: Function or Class.
- **FileId:** The relative path of the file. (Starting from the input folder the user chose in the SMA tool)
- **CellId:** The cell number where the call was found inside a notebook file, if applies.
- **Line:** The line number where the call was found.
- **Column:** The column number where the call was found.
- **ExecutionId:** The execution id.

## Checkpoints Inventory

The **Checkpoints.csv** lists the generated checkpoints for the user workload, these checkpoints are completely capable to be used in the Checkpoints Feature from the Snowflake Extension.

- **Name:** The checkpoint name (using the format described before).
- **FileId:** the relative path of the file (starting from the input folder the user chose in the SMA tool).
- **CellId:** the number of cell where the DataFrame operation was found inside a notebook file.
- **Line:** line number where the DataFrame operation was found.
- **Column:** the column number where the DataFrame operation was found.
- **Type:** the use case of the checkpoints (Collection or Validation).
- **DataFrameName:** The name of the DataFrame.
- **Location:** The assignment number of the DataFrame name.
- **Enabled:** Indicates whether the checkpoint is enabled (True or False).
- **Mode:** The mode number of the collection (Schema [1] or DataFrame [2]).
- **Sample:** The sample of the DataFrame.
- **EntryPoint:** The entry point that guide the flow to execute the checkpoint.
- **ExecutionId:** the execution id.

## DataFrames Inventory

The **DataFramesInventory.csv** lists the dataframes assignments found in order to be used to generate checkpoints for the user workload.

- **FullName:** The full name of the DataFrame.
- **Name:** The simple name of the variable of the DataFrame.
- **FileId:** The relative path of the file (starting from the input folder the user chose in the SMA tool).
- **CellId:** The number of cells where the DataFrame operation was found inside a notebook file.
- **Line:** The line number where the DataFrame operation was found.
- **Column:** The column number where the DataFrame operation was found.
- **AssignmentNumber:** The number of assignments for this particular identifier (not symbol) in the file.
- **RelevantFunction:** The relevant function why this was collected.
- **RelatedDataFrames:** The full qualified name of the DataFrame(s) involved in the operation (separated by semicolon).
- **EntryPoints:** it will be empty for this phase. In a later phase, it will be filled.
- **ExecutionId:** the execution id.

## Artifact Dependency Inventory

The **ArtifactDependencyInventory.csv** lists the artifact dependencies of each file analyzed by the SMA. This inventory allows the user to determine which artifacts are needed for the file to work properly in Snowflake.

The following are considered artifacts: a third-party library, SQL entity, source of a read or write operation, and another source code file in the workload.

- **ExecutionId:** the identifier of the execution.
- **FileId:** the identifier of the source code file.
- **Dependency:** the artifact dependency that the current file has.
- **Type:** the type of the artifact dependency.

  - *UserCodeFile:* source code or notebook.
  - *IOSources:* resource required for input and output operation.
  - *ThirdPartyLibraries:* a third-party library.
  - *UnknownLibraries*\*\*:\*\* a library whose origin was not determined by SMA.
  - *SQLObjects:* an SQL entity: table or view, for example.
- **Success:** If the artifact needs any intervention, it shows FALSE; otherwise, it shows TRUE.
- **Status\_Detail**: the status of the artifact dependency, based on the type.

  - *UserCodeFile:*
    - Parsed: the file was parsed successfully.
    - NotParsed: the file parsing failed.
  - *IOSources:*
    - Exists: the resource of the operation is in the workload.
    - DoesNotExists: the resource of the operation is not present in the input.
  - *ThirdPartyLibraries:*
    - Supported: the library is supported by Snowpark Anaconda.
    - NotSupported: the library is not supported by Snowpark Anaconda.
  - *UnknownLibraries:*
    - NotSupported: since the origin was not determined by SMA.
  - ***SQLObject***
    - DoesNotExists: the embedded statement that creates the entity is not in the input source code.
    - Exists: the embedded statement that creates the entity is in the input source code.
- **Arguments**: an extra data of the artifact dependency, based on the type.
- **Location**: the collection of cell ID and line number where the artifact dependency is being used in the source code file.
- **IndirectDependencies:** A list of other files that this file relies on, even if not directly.
- **TotalIndirectDependencies:** The total count of these indirect dependencies.
- **DirectParents:** A list of files that directly use this file.
- **TotalDirectParents:** The total count of these direct parent files.
- **IndirectParents:** A list of files that use this file indirectly (through other files).
- **TotalIndirectParents:** The total count of these indirect parent files.

## Files Inventory

The **files.csv** contains a complete list of all files processed during tool execution, including their file types and sizes.

- Path: The file location relative to the root directory. For example, files in the root directory will show only their filename.
- Technology: The programming language of the source code (Python or Scala)
- FileKind: Identifies if the file contains source code or is another type (such as text or log files)
- BinaryKind: Indicates if the file is human-readable text or a binary file
- Bytes: The file size measured in bytes
- SupportedStatus: Always shows “DoesNotApply” as file support status is not applicable in this context

## Import Usages Inventory

The **ImportUsagesInventory.csv** file contains a list of all external library imports found in your codebase. An external library is any package or module that is imported into your source code files.

- Element: The unique identifier for the Spark reference
- ProjectId: The root directory name where the tool was executed
- FileId: The relative path and filename containing the Spark reference
- Count: Number of occurrences of the element in a single line
- Alias: Optional alternative name for the element
- Kind: Always empty/null as all elements are imports
- Line: Source code line number where the element appears
- PackageName: Package containing the element
- Supported: Indicates if the reference can be converted (True/False)
- Automated: Empty/null (deprecated column)
- Status: Always “Invalid” (deprecated column)
- Statement: The actual code using the element [Not included in telemetry]
- SessionId: Unique identifier for each tool execution
- SnowConvertCoreVersion: Version number of the tool’s core processing engine
- SnowparkVersion: Available Snowpark API version for the specific technology
- ElementPackage: Package name containing the imported element (when available)
- CellId: For notebook files, indicates the cell number containing the element
- ExecutionId: Unique identifier for this SMA execution
- Origin: Source type of the import (BuiltIn, ThirdPartyLib, or blank)

## Input Files Inventory

The **InputFilesInventory.csv** file contains a detailed list of all files, organized by their file types and sizes.

- Element: The filename, which is identical to FileId
- ProjectId: The name of the project, represented by the root directory where the tool was executed
- FileId: The complete path to the file containing the Spark reference, shown as a relative path
- Count: The number of files sharing this filename
- SessionId: A unique identifier assigned to each tool session
- Extension: The file extension type
- Technology: The programming language or technology type, determined by the file extension
- Bytes: The file size measured in bytes
- CharacterLength: The total number of characters in the file
- LinesOfCode: The total number of code lines in the file
- ParsingResult: Indicates whether the cell was successfully parsed (“Successful”) or encountered errors (“Error”)

## Input and Ouput Files Inventory

The **IOFilesInventory.csv** file contains a list of all external files and resources that your code reads from or writes to.

- Element: The specific item (file, variable, or component) being accessed for reading or writing operations
- ProjectId: The name of the root directory where the tool was executed
- FileId: The complete path and filename where Spark code was detected
- Count: The number of occurrences of this filename
- isLiteral: Indicates whether the read/write location is specified as a literal value
- Format: The detected file format (such as CSV, JSON) if SMA can identify it
- FormatType: Specifies if the identified format is explicit
- Mode: Indicates whether the operation is “Read” or “Write”
- Supported: Indicates if Snowpark supports this operation
- Line: The line number in the file where the read or write operation occurs
- SessionId: A unique identifier assigned to each tool session
- OptionalSettings: Lists any additional parameters defined for the element
- CellId: For notebook files, identifies the specific cell location (null for non-notebook files)
- ExecutionId: A unique identifier for each time the tool is run

## Issue Inventory

The **Issues.csv** file contains a detailed report of all conversion issues discovered in your codebase. For each issue, you will find:

- A description explaining the problem
- The precise location within the file where the issue occurs
- A unique code identifier for the issue type

For more detailed information about specific issues, refer to the [issue analysis](/migrations/sma-docs/issue-analysis/approach) section of our documentation.

- Code: A unique identifier assigned to each issue detected by the tool
- Description: A detailed explanation of the issue, including the Spark reference name when applicable
- Category: The type of issue found, which can be one of the following:

  - Warning
  - Conversion Error
  - Parser Error
  - Helper
  - Transformation
  - WorkAround
  - NotSupported
  - NotDefined
- NodeType: The syntax node identifier where the issue was detected
- FileId: The relative path and filename where the Spark reference was found
- ProjectId: The root directory name where the tool was executed
- Line: The specific line number in the source file where the issue occurs
- Column: The specific character position in the line where the issue occurs

## Joins Inventory

The **JoinsInventory.csv** file contains a comprehensive list of all dataframe join operations found in the codebase.

- Element: Line number indicating where the join starts (and ends, if spanning multiple lines)
- ProjectId: Name of the root directory where the tool was executed
- FileId: Path and name of the file containing the Spark reference
- Count: Number of files with the same filename
- isSelfJoin: TRUE if joining a table with itself, FALSE otherwise
- HasLeftAlias: TRUE if an alias is defined for the left side of the join, FALSE otherwise
- HasRightAlias: TRUE if an alias is defined for the right side of the join, FALSE otherwise
- Line: Starting line number of the join
- SessionId: Unique identifier assigned to each tool session
- CellId: Identifier of the notebook cell containing the element (null for non-notebook files)
- ExecutionId: Unique identifier for each tool execution

## Notebook Cells Inventory

The **NotebookCellsInventory.csv** file provides a detailed list of all cells within a notebook, including their source code content and the number of code lines per cell.

- Element: The programming language used in the source code (Python, Scala, or SQL)
- ProjectId: The name of the root directory where the tool was executed
- FileId: The complete path and filename where Spark code was detected
- Count: The number of files with this specific filename
- CellId: For notebook files, the unique identifier of the cell containing the code (null for non-notebook files)
- Arguments: This field is always empty (null)
- LOC: The total number of code lines in the cell
- Size: The total number of characters in the cell
- SupportedStatus: Indicates whether all elements in the cell are supported (TRUE) or if there are unsupported elements (FALSE)
- ParsingResult: Shows if the cell was successfully parsed (“Successful”) or if there were parsing errors (“Error”)

## Notebook Size Inventory

The **NotebookSizeInventory.csv** file provides a summary of code lines for each programming language found in notebook files.

- filename: The name of the spreadsheet file (identical to the FileId)
- ProjectId: The name of the root directory where the tool was executed
- FileId: The relative path and name of the file containing Spark references
- Count: The number of files with this specific filename
- PythonLOC: Number of Python code lines in notebook cells (zero for regular files)
- ScalaLOC: Number of Scala code lines in notebook cells (zero for regular files)
- SqlLOC: Number of SQL code lines in notebook cells (zero for regular files)
- Line: This field is always empty (null)
- SessionId: A unique identifier assigned to each tool session
- ExecutionId: A unique identifier assigned to each tool execution

## Pandas Usages Inventory

The **PandasUsagesInventory.csv** file contains a comprehensive list of all Pandas API references found in your Python codebase during the scanning process.

- Element: The unique identifier for the pandas reference
- ProjectId: The root directory name where the tool was executed
- FileId: The relative path to the file containing the spark reference
- Count: Number of occurrences of the element in a single line
- Alias: The alternative name used for the element (only applies to imports)
- Kind: The type of element, such as Class, Variable, Function, Import, etc.
- Line: The source file line number where the element was found
- PackageName: The package containing the element
- Supported: Indicates if the reference is supported (True/False)
- Automated: Indicates if the tool can automatically convert the element (True/False)
- Status: Element classification: Rename, Direct, Helper, Transformation, WorkAround, NotSupported, or NotDefined
- Statement: The context in which the element was used [Not included in telemetry]
- SessionId: A unique identifier for each tool execution
- SnowConvertCoreVersion: The version number of the tool’s core processing code
- SnowparkVersion: The Snowpark API version available for the specific technology and tool run
- PandasVersion: The pandas API version used to identify elements in the codebase
- CellId: The cell identifier in the FileId (only for notebooks, null otherwise)
- ExecutionId: A unique identifier for each tool execution

## Spark Usages Inventory

The **SparkUsagesInventory.csv** file identifies where and how Spark API functions are used in your code. This information helps calculate the [Readiness Score](/migrations/sma-docs/support/glossary), which indicates how ready your code is for migration.

- Element: The unique identifier for the Spark reference
- ProjectId: The root directory name where the tool was executed
- FileId: The relative path and filename containing the Spark reference
- Count: Number of occurrences of the element in a single line
- Alias: The element’s alias (only applies to import elements)
- Kind: The element’s category (e.g., Class, Variable, Function, Import)
- Line: The source file line number where the element was found
- PackageName: The package name containing the element
- Supported: Indicates if the reference is supported (True/False)
- Automated: Indicates if the tool can automatically convert the element (True/False)
- Status: Element categorization (Rename, Direct, Helper, Transformation, WorkAround, NotSupported, NotDefined)
- Statement: The actual code where the element was used [NOTE: This column is not sent via telemetry]
- SessionId: A unique identifier for each tool execution
- SnowConvertCoreVersion: The tool’s core process version number
- SnowparkVersion: The available Snowpark API version for the specific technology and tool run
- CellId: For notebook files, the cell’s numerical location where the element was found
- ExecutionId: A unique identifier for this specific SMA execution

The **SqlStatementsInventory.csv** file contains a count of SQL keywords found in Spark SQL elements.

- Element: Name of the code element containing the SQL statement
- ProjectId: Root directory name where the tool was executed
- FileId: Relative path to the file containing the Spark reference
- Count: Number of occurrences of the element in a single line
- InterpolationCount: Number of external elements inserted into this element
- Keywords: Dictionary containing SQL keywords and their frequency
- Size: Total character count of the SQL statement
- LiteralCount: Number of string literals in the element
- NonLiteralCount: Number of SQL components that are not string literals
- Line: Line number where the element appears
- SessionId: Unique identifier for each tool session
- CellId: Identifier of the notebook cell containing the element (null if not in a notebook)
- ExecutionId: Unique identifier for each tool execution

## SQL Elements Inventory

The SQLElementsInventory.csv file contains a count of SQL statements found within Spark SQL elements.

Here are the fields included in the SQL analysis report:

- Element: SQL code element type (Example: SqlSelect, SqlFromClause)
- ProjectId: Root directory name where the tool was executed
- FileId: Path to the file containing the SQL code
- Count: Number of occurrences of the element in a single line
- NotebookCellId: ID of the notebook cell
- Line: Line number where the element appears
- Column: Column number where the element appears
- SessionId: Unique ID for each tool session
- ExecutionId: Unique ID for each tool run
- SqlFlavor: Type of SQL being analyzed (Example: Spark SQL, Hive SQL)
- RootFullName: Complete name of the main code element
- RootLine: Line number of the main element
- RootColumn: Column number of the main element
- TopLevelFullName: Complete name of the highest-level SQL statement
- TopLevelLine: Line number of the highest-level statement
- TopLevelColumn: Column number of the highest-level statement
- ConversionStatus: Result of SQL conversion (Example: Success, Failed)
- Category: Type of SQL statement (Example: DDL, DML, DQL)
- EWI: Error Warning Information code
- ObjectReference: Name of the SQL object being referenced (Example: table name, view name)

## SQL Embedded Usage Inventory

The SqlEmbeddedUsageInventory.csv file contains a count of SQL keywords found within Spark SQL elements.

- Element: The type of SQL component found in the code (such as Select statement, From clause, or Numeric literal)
- ProjectId: The name of the root directory where the tool was executed
- FileId: The location and relative path of the file containing the SQL reference
- Count: How many times this element appears in a single line
- ExecutionId: A unique ID assigned to each tool execution
- LibraryName: The name of the library in use
- HasLiteral: Shows if the element contains literal values
- HasVariable: Shows if the element contains variables
- HasFunction: Shows if the element contains function calls
- ParsingStatus: The current parsing state (Success, Failed, or Partial)
- HasInterpolation: Shows if the element contains string interpolations
- CellId: The identifier for the notebook cell
- Line: The line number where the element is found
- Column: The column number where the element is found

## Third Party Usages Inventory

The **ThirdPartyUsagesInventory.csv** file contains

- Element: The unique identifier for the third-party reference
- ProjectId: The name of the project’s root directory where the tool was executed
- FileId: The relative path to the file containing the Spark reference
- Count: The number of occurrences of the element in a single line
- Alias: The alternative name assigned to the element (if applicable)
- Kind: The type classification of the element (variable, type, function, or class)
- Line: The source file line number where the element was found
- PackageName: The full package name (combination of ProjectId and FileId in Python)
- Statement: The actual code where the element was used [NOTE: Not included in telemetry data]
- SessionId: A unique identifier for each tool session
- CellId: The notebook cell identifier where the element was found (null for non-notebook files)
- ExecutionId: A unique identifier for each tool execution

## Packages Inventory

The **packagesInventory.csv** file contains

- Package Name: The name of the package being analyzed.
- Project Name: The name of the project, which corresponds to the root directory where the tool was executed.
- File Location: The file path where the package was found, shown as a relative path.
- Occurrence Count: The number of times this package appears on a single line of code.

## Tool Execution Summary

The **tool\_execution.csv** file contains essential information about the current execution of the Snowpark Migration Accelerator (SMA) tool.

- ExecutionId: A unique identifier assigned to each time the tool runs.
- ToolName: The name of the tool being used. Can be either PythonSnowConvert or SparkSnowConvert (for Scala).
- Tool\_Version: The version number of the software.
- AssemblyName: The complete name of the code processor (a more detailed version of ToolName).
- LogFile: Indicates if a log file was generated when an error or failure occurred.
- FinalResult: Indicates at which point the tool stopped if an error or failure occurred.
- ExceptionReport: Indicates if an error report was generated when a failure occurred.
- StartTime: The date and time when the tool began running.
- EndTime: The date and time when the tool finished running.
- SystemName: The machine’s serial number where the tool was run (used only for troubleshooting and verifying licenses).
