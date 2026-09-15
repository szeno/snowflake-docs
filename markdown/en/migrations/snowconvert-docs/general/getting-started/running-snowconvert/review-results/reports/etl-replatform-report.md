# SnowConvert AI - ETL Replatform Component Summary Report

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts. This preview is available for SSIS migrations.

The Component Summary Report provides a comprehensive inventory of all identified SSIS components and their migration outcomes. Use this report to understand the overall migration scope and identify areas requiring attention.

## Report Fields

| Field | Description |
| --- | --- |
| **SessionID** | Unique identifier for the migration run |
| **Technology** | Original ETL technology (SSIS) |
| **Category** | Component category (Component, Package, Data Flow, Control Flow) |
| **Subtype** | Component type (e.g., Microsoft.OLEDBSource, Microsoft.DerivedColumn) |
| **FullName** | Full component name including hierarchy (e.g., Package1/DataFlow1/Component1) |
| **FileName** | Relative path to the DTSX file |
| **Status** | Migration status (Success, NotSupported, Partial) |
| **EWI Count** | Number of EWIs for this component |
| **EWIs** | Unique EWI codes found in the component |
| **FDM Count** | Number of FDMs (functional difference messages) |
| **FDMs** | Unique FDM codes found in the component |
| **PRF Count** | Number of PRFs (performance warnings) |
| **PRFs** | Unique PRF codes found in the component |

Expand

Show lessSee more

## How to Use This Report

Use the Status column to prioritize your post-migration work:

- **NotSupported** status or high EWI counts indicate components that require manual intervention
- **Partial** status means the component was converted but has limitations or warnings that need review
- **Success** status indicates a clean conversion with no known issues

## Example CSV

```
:force:

Technology,Category,Subtype,FullName,FileName,Status,EWI Count,EWIs,FDM Count,FDMs,PRF Count,PRFs
SSIS,Component,Data Flow Task,Customer ETL,Package.dtsx,Success,0,,0,,0,
SSIS,Component,Microsoft.OLEDBSource,OLE DB Source,Package.dtsx,Success,0,,0,,0,
SSIS,Component,Microsoft.DerivedColumn,Derived Column 1,Package.dtsx,Success,0,,0,,0,
SSIS,Component,Microsoft.Lookup,Lookup 1,Package.dtsx,Partial,0,,1,SSC-FDM-SSIS0001,0,
```
