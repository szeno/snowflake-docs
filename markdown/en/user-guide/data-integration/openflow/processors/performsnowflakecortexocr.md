# PerformSnowflakeCortexOCR 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-snowflake-processors-nar

## Description

Performs Optical Character Recognition (OCR) on PDF documents using Snowflake Cortex ML functions. Documents must be staged in a Snowflake internal stage with server-side encryption enabled. The processor extracts text content from PDFs and can output the results either as FlowFile content or as an attribute.

## Tags

ai, cortex, document, ml, ocr, openflow, pdf, snowflake

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Database | The Snowflake database containing the stage |
| Filename | The filename of the file to perform OCR on, it must be uploaded to the stage prior to performing OCR. FlowFile attributes may be referenced via Expression Language. |
| Max Attribute Size | The maximum size of the OCR results that can be written to an attribute. If the OCR results exceed this, the FlowFile will be routed to failure. |
| OCR Mode | Specifies how document text and structure should be extracted. In ‘OCR’ mode, only raw text content is extracted, ignoring formatting and table structures. In ‘LAYOUT’ mode, the output preserves table structures as markdown. |
| Output Strategy | Determines response output destination |
| Results Attribute | The name of the attribute to write the OCR response to. |
| Schema | The Snowflake schema containing the stage |
| Snowflake Connection Service | Database Connection Service for accessing Snowflake |
| Stage | The Snowflake stage where PDFs will be temporarily stored. The stage must have server-side encryption enabled. FlowFile attributes may be referenced via Expression Language |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| empty | FlowFiles for which OCR results are empty |
| failure | FlowFiles that cannot be processed are routed to this relationship |
| success | FlowFiles that are successfully processed (with non-empty OCR results) are routed to this relationship |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| mime.type | The MIME type of the output content (text/plain when output strategy is FLOW\_FILE) |
| snowflake.error.information | Contains error information if Snowflake Cortex OCR operation returns an error |

Expand

Show lessSee more

## See also

- [com.snowflake.openflow.runtime.processors.snowflake.PutSnowflakeInternalStageFile](/user-guide/data-integration/openflow/processors/putsnowflakeinternalstagefile)
