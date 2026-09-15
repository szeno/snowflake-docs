description:
:   Additional data not specific to a particular source language

# Snowpark Migration Accelerator: Generic Inventories

When the Snowpark Migration Accelerator (SMA) analyzes your code, it performs two types of scans:

1. A language-specific scan that analyzes code in your source programming language
2. A general-purpose scan that collects basic information about files and keywords in your codebase

You can find details about the language-specific scan results in the [SMA Inventories](/migrations/sma-docs/user-guide/scos-conversion/output-reports/sma-inventories) section. This page describes the information collected by the general-purpose scan.

Although some files have a .pam extension, they are actually comma-separated files similar to .csv files. You may notice duplicate entries across these files because the data has been organized in different ways to facilitate various types of analysis.

## File Summary

The files.pam contains an inventory that lists all files processed during a tool execution. For each file, it records the file type and size. This file contains the same information as the [files.csv described in the SMA Inventories section](/migrations/sma-docs/user-guide/scos-conversion/output-reports/sma-inventories).

## Generic File Inventory

The **FilesInventory.csv** file contains categorization details and line counts for each source file.

- Filename: The complete path and name of the file from the root input directory
- Extension: The file type extension (e.g., .java, .py, .sql)
- Technology: The programming language or technology identified based on the file extension
- Status: Always shows “OK” for identified files (unidentified files are not listed)
- isBinary: Indicates if the file is binary (TRUE), text (FALSE), or unrecognized (UNKNOWN)
- Bytes: File size in bytes
- ContentType: Categorizes each line as either:

  - Code: Programming instructions
  - Comment: Documentation or notes
  - Blank: Empty lines
  - Other: Unrecognized content
- ContentLines: Total number of code lines in the file
- CommentLines: Total number of comment lines in the file
- BlankLines: Total number of empty lines in the file

## Keyword Counts

The **KeywordCounts.csv** file provides a comprehensive list of all keywords detected in each file, organized by technology type. This analysis includes keywords from any programming language that our generic scanner can process, not just the source languages officially supported by the Snowpark Migration Accelerator (SMA).

- FileId: The file path where the keyword was located
- Technology: The original technology used in the source file
- Keyword: The specific keyword found (examples: from, import, DataFrame)
- Count: The number of occurrences of the keyword in each line

## Lines Inventory

The **line\_counts.pam** file analyzes each line in a scanned file and categorizes them as code, comments, or blank lines. It also provides a total count for each category.

- FileId: The name of the file being analyzed
- LineKind: The category of each line in the file (can be code, comment, or blank)
- Count: Total number of lines for each combination of FileId and LineKind

## Tool Execution Inventory

The tool\_execution.pam file contains essential information about the current SMA tool execution. This file is identical to the [tool\_execution.csv file described in the SMA Inventories section](/migrations/sma-docs/user-guide/scos-conversion/output-reports/sma-inventories) of this documentation.

## Word Counts

The **word\_counts.pam** file displays how many times each keyword appears across all files in the scanned codebase.

- FileId: The file location and relative path where the keyword was found
- Keyword: The specific text identified as a keyword (examples: from, import, DataFrame)
- Count: The number of occurrences of the keyword in a single line of code
