# ValidateCsv 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Validates the contents of FlowFiles or a FlowFile attribute value against a user-specified CSV schema. Take a look at the additional documentation of this processor for some schema examples.

## Tags

csv, schema, validation

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| CSV Source Attribute | The name of the attribute containing CSV data to be validated. If this property is blank, the FlowFile content will be validated. |
| Max Lines Per Row | The maximum number of lines that a row can span before an exception is thrown. This option allows the processor to fail fast when encountering CSV with mismatching quotes - the normal behaviour would be to continue reading until the matching quote is found, which could potentially mean reading the whole file (and exhausting all available memory). Zero value will disable this option. |
| validate-csv-delimiter | Character used as ‘delimiter’ in the incoming data. Example: , |
| validate-csv-eol | Symbols used as ‘end of line’ in the incoming data. Example: n |
| validate-csv-header | True if the incoming flow file contains a header to ignore, false otherwise. |
| validate-csv-quote | Character used as ‘quote’ in the incoming data. Example: “ |
| validate-csv-schema | The schema to be used for validation. Is expected a comma-delimited string representing the cell processors to apply. The following cell processors are allowed in the schema definition: [ParseBigDecimal, ParseBool, ParseChar, ParseDate, ParseDouble, ParseInt, ParseLong, Optional, DMinMax, Equals, ForbidSubStr, LMinMax, NotNull, Null, RequireHashCode, RequireSubStr, Strlen, StrMinMax, StrNotNullOrEmpty, StrRegEx, Unique, UniqueHashCode, IsIncludedIn]. Note: cell processors cannot be nested except with Optional. Schema is required if Header is false. |
| validate-csv-strategy | Strategy to apply when routing input files to output relationships. |
| validate-csv-violations | If true, the validation.error.message attribute would include the list of all the violations for the first invalid line. Note that setting this property to true would slightly decrease the performances as all columns would be validated. If false, a line is invalid as soon as a column is found violating the specified constraint and only this violation for the first invalid line will be included in the validation.error.message attribute. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| invalid | FlowFiles that are not valid according to the specified schema, or no schema or CSV header can be identified, are routed to this relationship |
| valid | FlowFiles that are successfully validated against the schema are routed to this relationship |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| count.valid.lines | If line by line validation, number of valid lines extracted from the source data |
| count.invalid.lines | If line by line validation, number of invalid lines extracted from the source data |
| count.total.lines | If line by line validation, total number of lines in the source data |
| validation.error.message | For flow files routed to invalid, message of the first validation error |

Expand

Show lessSee more
