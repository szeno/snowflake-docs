# SnowConvert AI - ETL Replatform Issues Report

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts. This preview is available for SSIS migrations.

The EWIs Report provides a detailed inventory of errors, warnings, and issues encountered during migration. Use this report to identify components that require manual intervention or review.

## Report Fields

| Field | Description |
| --- | --- |
| **SessionID** | Unique identifier for the migration run |
| **Code** | Issue code (e.g., SSC-EWI-SSIS0001, SSC-FDM-SSIS0001) |
| **Name** | Issue type or problematic ETL element name |
| **Description** | Brief description of the issue |
| **Parent File Name** | Relative path to the source DTSX file |
| **Component Full Name** | Full name of the SSIS component with the issue |

Expand

Show lessSee more

## How to Use This Report

- Prioritize addressing “Critical” level EWIs as they indicate components that could not be converted and will prevent successful execution in dbt
- “High” severity issues suggest potential problems that might require manual review or adjustments
- “Medium” and “None” severity issues provide context or suggest best practices for the migrated dbt project

## Example CSV

```
:force:

Code,Name,Description,ParentFileName,ComponentFullName
SSC-EWI-SSIS0001,ScriptComponent1,SSIS COMPONENT IS NOT SUPPORTED BY SNOWCONVERT,Package.dtsx,Package.Data Flow Task.ScriptComponent1
SSC-EWI-SSIS0002,DerivedColumn1,SSIS EXPRESSION CANNOT BE CONVERTED TO SNOWFLAKE SQL,Package.dtsx,Package.Data Flow Task.DerivedColumn1
SSC-FDM-SSIS0001,Lookup1,SSIS COMPONENT BEHAVIOR MAY DIFFER IN SNOWFLAKE ENVIRONMENT,Package.dtsx,Package.Data Flow Task.Lookup1
```
