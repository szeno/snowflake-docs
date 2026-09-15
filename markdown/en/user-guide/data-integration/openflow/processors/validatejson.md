# ValidateJson 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Validates the contents of FlowFiles against a configurable JSON Schema. See json-schema.org for specification standards. This Processor does not support input containing multiple JSON objects, such as newline-delimited JSON. If the input FlowFile contains newline-delimited JSON, only the first line will be validated.

## Tags

JSON, schema, validation

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| JSON Schema | A URL or file path to the JSON schema or the actual JSON schema content |
| JSON Schema Registry | Specifies the Controller Service to use for the JSON Schema Registry |
| JSON Schema Version | The JSON schema specification |
| Max String Length | The maximum allowed length of a string value when parsing the JSON document |
| Schema Access Strategy | Specifies how to obtain the schema that is to be used for interpreting the data. |
| Schema Name | Specifies the name of the schema to lookup in the Schema Registry property |

Expand

Show lessSee more

## Restrictions

| Required Permission | Explanation |
| --- | --- |
| reference remote resources | Schema configuration can reference resources over HTTP |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | FlowFiles that cannot be read as JSON are routed to this relationship |
| invalid | FlowFiles that are not valid according to the specified schema are routed to this relationship |
| valid | FlowFiles that are successfully validated against the schema are routed to this relationship |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| json.validation.errors | If the flow file is routed to the invalid relationship , this attribute will contain the error message resulting from the validation failure. |

Expand

Show lessSee more
