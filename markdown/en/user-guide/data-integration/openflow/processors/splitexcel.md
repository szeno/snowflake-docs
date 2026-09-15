# SplitExcel 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-poi-nar

## Description

This processor splits a multi sheet Microsoft Excel spreadsheet into multiple Microsoft Excel spreadsheets where each sheet from the original file is converted to an individual spreadsheet in its own flow file. Currently this processor is only capable of processing .xlsx (XSSF 2007 OOXML file format) Excel documents and not older .xls (HSSF ’97(-2007) file format) documents. Please note all original cell styles are dropped and formulas are removed leaving only the calculated values. Even a single sheet Microsoft Excel spreadsheet is converted to its own flow file with all the original cell styles dropped and formulas removed.

## Tags

split, text

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Password | The password for a password protected Excel spreadsheet |
| Protection Type | Specifies whether an Excel spreadsheet is protected by a password or not. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | If a FlowFile cannot be transformed from the configured input format to the configured output format, the unchanged FlowFile will be routed to this relationship. |
| original | The original FlowFile that was split into segments. If the FlowFile fails processing, nothing will be sent to this relationship |
| split | The individual Excel ‘segments’ of the original Excel FlowFile will be routed to this relationship. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| fragment.identifier | All split Excel FlowFiles produced from the same parent Excel FlowFile will have the same randomly generated UUID added for this attribute |
| fragment.index | A one-up number that indicates the ordering of the split Excel FlowFiles that were created from a single parent Excel FlowFile |
| fragment.count | The number of split Excel FlowFiles generated from the parent Excel FlowFile |
| segment.original.filename | The filename of the parent Excel FlowFile |
| sheetname | The name of the Excel sheet from the original spreadsheet. |
| total.rows | The number of rows in the Excel sheet from the original spreadsheet. |

Expand

Show lessSee more
