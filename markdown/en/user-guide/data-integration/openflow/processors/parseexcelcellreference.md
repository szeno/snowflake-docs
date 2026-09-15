# ParseExcelCellReference 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-office-nar

## Description

Processor responsible for parsing Excel cell reference formula.

## Tags

cell, excel, parse, spreadsheet, xls, xlsx

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Ranges | The comma-separated Excel ranges to parse in the A1 notation. For example: Sheet1!A1:B2,Sheet2!D4:E5,Sheet3. Ranges in R1C1 and 3-D reference style are not allowed. The value can’t be empty. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | FlowFile with errors occurred while parsing ranges. |
| success | FlowFile annotated with attributes containing parsed Excel range. For each range a separate FlowFile is produced. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| range.formula | Single range formula that was used to produce other attributes, e.g. Sheet1!A1:B2. |
| range.sheetname | Parsed sheet name. |
| range.rows.starting | Starting row (numbered from 1) of parsed range. |
| range.rows.ending | Ending row of parsed range. |
| range.columns.starting | Number of starting column of parsed range. |
| range.columns.ending | Number of ending column of parsed range. |

Expand

Show lessSee more
