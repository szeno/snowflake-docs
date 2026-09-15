# ValidateRecord 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Validates the Records of an incoming FlowFile against a given schema. All records that adhere to the schema are routed to the “valid” relationship while records that do not adhere to the schema are routed to the “invalid” relationship. It is therefore possible for a single incoming FlowFile to be split into two individual FlowFiles if some records are valid according to the schema and others are not. Any FlowFile that is routed to the “invalid” relationship will emit a ROUTE Provenance Event with the Details field populated to explain why records were invalid. In addition, to gain further explanation of why records were invalid, DEBUG-level logging can be enabled for the “org.apache.nifi.processors.standard. ValidateRecord” logger.

## Tags

record, schema, validate

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Schema Access Strategy | Specifies how to obtain the schema that should be used to validate records |
| Schema Branch | Specifies the name of the branch to use when looking up the schema in the Schema Registry property. If the chosen Schema Registry does not support branching, this value will be ignored. |
| Schema Name | Specifies the name of the schema to lookup in the Schema Registry property |
| Schema Registry | Specifies the Controller Service to use for the Schema Registry |
| Schema Text | The text of an Avro-formatted Schema |
| Schema Version | Specifies the version of the schema to lookup in the Schema Registry. If not specified then the latest version of the schema will be retrieved. |
| allow-extra-fields | If the incoming data has fields that are not present in the schema, this property determines whether or not the Record is valid. If true, the Record is still valid. If false, the Record will be invalid due to the extra fields. |
| coerce-types | If enabled, the processor will coerce every field to the type specified in the Reader ‘s schema. If the value of a field cannot be coerced to the type, the field will be skipped (will not be read from the input data), thus will not appear in the output. If not enabled, then every field will appear in the output but their types may differ from what is specified in the schema. For details please see the Additional Details page of the processor’s Help. This property controls how the data is read by the specified Record Reader. |
| invalid-record-writer | If specified, this Controller Service will be used to write out any records that are invalid. If not specified, the writer specified by the “Record Writer” property will be used with the schema used to read the input records. This is useful, for example, when the configured Record Writer cannot write data that does not adhere to its schema (as is the case with Avro) or when it is desirable to keep invalid records in their original format while converting valid records to another format. |
| maximum-validation-details-length | Specifies the maximum number of characters that validation details value can have. Any characters beyond the max will be truncated. This property is only used if ‘Validation Details Attribute Name’ is set |
| record-reader | Specifies the Controller Service to use for reading incoming data |
| record-writer | Specifies the Controller Service to use for writing out the records. Regardless of the Controller Service schema access configuration, the schema that is used to validate record is used to write the valid results. |
| strict-type-checking | If the incoming data has a Record where a field is not of the correct type, this property determines how to handle the Record. If true, the Record will be considered invalid. If false, the Record will be considered valid and the field will be coerced into the correct type (if possible, according to the type coercion supported by the Record Writer). This property controls how the data is validated against the validation schema. |
| validation-details-attribute-name | If specified, when a validation error occurs, this attribute name will be used to leave the details. The number of characters will be limited by the property ‘Maximum Validation Details Length’. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | If the records cannot be read, validated, or written, for any reason, the original FlowFile will be routed to this relationship |
| invalid | Records that are not valid according to the schema will be routed to this relationship |
| valid | Records that are valid according to the schema will be routed to this relationship |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| mime.type | Sets the mime.type attribute to the MIME Type specified by the Record Writer |
| record.count | The number of records in the FlowFile routed to a relationship |

Expand

Show lessSee more
