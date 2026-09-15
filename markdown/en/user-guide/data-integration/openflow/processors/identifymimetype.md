# IdentifyMimeType 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Attempts to identify the MIME Type used for a FlowFile. If the MIME Type can be identified, an attribute with the name ‘mime.type’ is added with the value being the MIME Type. If the MIME Type cannot be determined, the value will be set to ‘application/octet-stream’. In addition, the attribute ‘mime.extension’ will be set if a common file extension for the MIME Type is known. If the MIME Type detected is of type text/\*, attempts to identify the charset used and an attribute with the name ‘mime.charset’ is added with the value being the charset.

## Tags

MIME, bzip2, compression, file, gzip, identify, mime.type, zip

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Custom MIME Configuration | A URL or file path to a custom Tika Mime type configuration or the actual content of a custom Tika Mime type configuration. |
| config-strategy | Select the loading strategy for MIME Type configuration to be used. |
| use-filename-in-detection | If true will pass the filename to Tika to aid in detection. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| success | All FlowFiles are routed to success |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| mime.type | This Processor sets the FlowFile’s mime.type attribute to the detected MIME Type. If unable to detect the MIME Type, the attribute’s value will be set to application/octet-stream |
| mime.extension | This Processor sets the FlowFile’s mime.extension attribute to the file extension associated with the detected MIME Type. If there is no correlated extension, the attribute’s value will be empty |
| mime.charset | This Processor sets the FlowFile’s mime.charset attribute to the detected charset. If unable to detect the charset or the detected MIME type is not of type text/\*, the attribute will not be set |

Expand

Show lessSee more
