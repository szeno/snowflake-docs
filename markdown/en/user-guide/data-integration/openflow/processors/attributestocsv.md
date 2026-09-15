# AttributesToCSV 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Generates a CSV representation of the input FlowFile Attributes. The resulting CSV can be written to either a newly generated attribute named ‘CSVAttributes’ or written to the FlowFile as content. If the attribute value contains a comma, newline or double quote, then the attribute value will be escaped with double quotes. Any double quote characters in the attribute value are escaped with another double quote.

## Tags

attributes, csv, flowfile

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| attribute-list | Comma separated list of attributes to be included in the resulting CSV. If this value is left empty then all existing Attributes will be included. This list of attributes is case sensitive and supports attribute names that contain commas. If an attribute specified in the list is not found it will be emitted to the resulting CSV with an empty string or null depending on the ‘Null Value’ property. If a core attribute is specified in this list and the ‘Include Core Attributes’ property is false, the core attribute will be included. The attribute list ALWAYS wins. |
| attributes-regex | Regular expression that will be evaluated against the flow file attributes to select the matching attributes. This property can be used in combination with the attributes list property. The final output will contain a combination of matches found in the ATTRIBUTE\_LIST and ATTRIBUTE\_REGEX. |
| destination | Control if CSV value is written as a new flowfile attribute ‘CSVData’ or written in the flowfile content. |
| include-core-attributes | Determines if the FlowFile org.apache.nifi.flowfile.attributes. CoreAttributes, which are contained in every FlowFile, should be included in the final CSV value generated. Core attributes will be added to the end of the CSVData and CSVSchema strings. The Attribute List property overrides this setting. |
| include-schema | If true the schema (attribute names) will also be converted to a CSV string which will either be applied to a new attribute named ‘CSVSchema’ or applied at the first row in the content depending on the DESTINATION property setting. |
| null-value | If true a non existing or empty attribute will be ‘null’ in the resulting CSV. If false an empty string will be placed in the CSV |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | Failed to convert attributes to CSV |
| success | Successfully converted attributes to CSV |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| CSVSchema | CSV representation of the Schema |
| CSVData | CSV representation of Attributes |

Expand

Show lessSee more
