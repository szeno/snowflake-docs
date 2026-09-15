# GetGoogleSheets 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-google-sheets-processors-nar

## Description

Processor responsible for fetching data from Google Sheets. By default it fetches data once a day.

## Tags

Google, Google Sheets, spreadsheet

## Input Requirement

FORBIDDEN

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Date Time Render Option | Determines how dates should be rendered in the output. |
| GCP Credentials Service | Controller Service used to obtain Google Cloud Platform credentials. |
| Ranges | The A1 notation or R1C1 notation of the comma-separated ranges to retrieve values from. For example: Sheet1!A1:B2,Sheet2!D4:E5,Sheet3. The first row in a sheet must represent column names. If not specified, all sheets will be downloaded. |
| Spreadsheet ID | ID of the Google Sheets Spreadsheet. Can be found in the URL of the spreadsheet. |
| Value Render Option | Determines how values should be rendered in the output. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | FlowFile with errors occurred while fetching from Google Sheets. |
| success | FlowFile containing a JSON array where each object represents a row from the source sheet. Keys correspond to column headers from the first row, and values to the respective row entries. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| google.sheets.spreadsheet.id | ID of the Google Sheets Spreadsheet. |
| google.sheets.range | Range in Google Sheets Spreadsheet that was fetched. |
| run.id | A unique ID of each ingestion run. Lets you identify all flow files generated during a single run. |
| destination.table.schema | A Snowflake schema of the destination table in the following format: { “columns”: [ { “name”: “<column name>”, “type”: “<column type>”, “nullable”: <true/false>, “precision”: <precision, only for numeric type>, “scale”: <scale, only for numeric type> }, … ], “primaryKeys”: [“<name of first primary key column>”, “<name of second primary key column>”, …] } |

Expand

Show lessSee more
