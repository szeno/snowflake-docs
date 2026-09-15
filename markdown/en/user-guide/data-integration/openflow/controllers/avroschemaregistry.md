# AvroSchemaRegistry

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Provides a service for registering and accessing schemas. You can register a schema as a dynamic property where ‘name’ represents the schema name and ‘value’ represents the textual representation of the actual schema following the syntax and semantics of Avro’s Schema format.

## Tags

avro, csv, json, registry, schema

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Validate Field Names \* | avro-reg-validated-field-names | true | - true - false | Whether or not to validate the field names in the Avro schema based on Avro naming rules. If set to true, all field names must be valid Avro names, which must begin with `[A-Za-z_]`, and subsequently contain only `[A-Za-z0-9_]`. If set to false, no validation will be performed on the field names. |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
