# GenerateRecord 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

This processor creates FlowFiles with records having random value for the specified fields. GenerateRecord is useful for testing, configuration, and simulation. It uses either user-defined properties to define a record schema or a provided schema and generates the specified number of records using random data for the fields in the schema.

## Tags

fake, generate, random, test

## Input Requirement

FORBIDDEN

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| null-percentage | The percent probability (0-100%) that a generated value for any nullable field will be null. Set this property to zero to have no null values, or 100 to have all null values. |
| nullable-fields | Whether the generated fields will be nullable. Note that this property is ignored if Schema Text is set. Also it only affects the schema of the generated data, not whether any values will be null. If this property is true, see ‘Null Value Percentage’ to set the probability that any generated field will be null. |
| number-of-records | Specifies how many records will be generated for each outgoing FlowFile. |
| record-writer | Specifies the Controller Service to use for writing out the records |
| schema-text | The text of an Avro-formatted Schema used to generate record data. If this property is set, any user-defined properties are ignored. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| success | FlowFiles that are successfully created will be routed to this relationship |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| mime.type | Sets the mime.type attribute to the MIME Type specified by the Record Writer |
| record.count | The number of records in the FlowFile |

Expand

Show lessSee more
