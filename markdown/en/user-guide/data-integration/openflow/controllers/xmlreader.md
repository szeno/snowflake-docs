# XMLReader

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Reads XML content and creates Record objects. Records are expected in the second level of XML data, embedded in an enclosing root tag.

## Tags

parser, reader, record, xml

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Date Format | Date Format |  |  | Specifies the format to use when reading/writing Date fields. If not specified, Date fields will be assumed to be number of milliseconds since epoch (Midnight, Jan 1, 1970 GMT). If specified, the value must match the Java java.time.format.DateTimeFormatter format (for example, MM/dd/yyyy for a two-digit month, followed by a two-digit day, followed by a four-digit year, all separated by ‘/’ characters, as in 01/01/2017). |
| Schema Access Strategy \* | Schema Access Strategy | infer-schema | - Use ‘Schema Name’ Property - Use ‘Schema Text’ Property - Schema Reference Reader - Infer Schema | Specifies how to obtain the schema that is to be used for interpreting the data. |
| Schema Branch | Schema Branch |  |  | Specifies the name of the branch to use when looking up the schema in the Schema Registry property. If the chosen Schema Registry does not support branching, this value will be ignored. |
| Schema Name | Schema Name | ${schema.name} |  | Specifies the name of the schema to lookup in the Schema Registry property |
| Schema Reference Reader \* | Schema Reference Reader |  |  | Service implementation responsible for reading FlowFile attributes or content to determine the Schema Reference Identifier |
| Schema Registry | Schema Registry |  |  | Specifies the Controller Service to use for the Schema Registry |
| Schema Text | Schema Text | ${avro.schema} |  | The text of an Avro-formatted Schema |
| Schema Version | Schema Version |  |  | Specifies the version of the schema to lookup in the Schema Registry. If not specified then the latest version of the schema will be retrieved. |
| Time Format | Time Format |  |  | Specifies the format to use when reading/writing Time fields. If not specified, Time fields will be assumed to be number of milliseconds since epoch (Midnight, Jan 1, 1970 GMT). If specified, the value must match the Java java.time.format.DateTimeFormatter format (for example, HH:mm:ss for a two-digit hour in 24-hour format, followed by a two-digit minute, followed by a two-digit second, all separated by ‘:’ characters, as in 18:04:15). |
| Timestamp Format | Timestamp Format |  |  | Specifies the format to use when reading/writing Timestamp fields. If not specified, Timestamp fields will be assumed to be number of milliseconds since epoch (Midnight, Jan 1, 1970 GMT). If specified, the value must match the Java java.time.format.DateTimeFormatter format (for example, MM/dd/yyyy HH:mm:ss for a two-digit month, followed by a two-digit day, followed by a four-digit year, all separated by ‘/’ characters; and then followed by a two-digit hour in 24-hour format, followed by a two-digit minute, followed by a two-digit second, all separated by ‘:’ characters, as in 01/01/2017 18:04:15). |
| Attribute Prefix | attribute\_prefix |  |  | If this property is set, the name of attributes will be prepended with a prefix when they are added to a record. |
| Field Name for Content | content\_field\_name |  |  | If tags with content (e. g. <field>content</field>) are defined as nested records in the schema, the name of the tag will be used as name for the record and the value of this property will be used as name for the field. If tags with content shall be parsed together with attributes (e. g. <field attribute=”123”>content</field>), they have to be defined as records. In such a case, the name of the tag will be used as the name for the record and the value of this property will be used as the name for the field holding the original content. The name of the attribute will be used to create a new record field, the content of which will be the value of the attribute. For more information, see the ‘Additional Details…’ section of the XMLReader controller service’s documentation. |
| Parse XML Attributes | parse\_xml\_attributes | true | - true - false | When ‘Schema Access Strategy’ is ‘Infer Schema’ and this property is ‘true’ then XML attributes are parsed and added to the record as new fields. When the schema is inferred but this property is ‘false’, XML attributes and their values are ignored. |
| Expect Records as Array \* | record\_format | false | - false - true - Use attribute ‘xml.stream.is.array’ | This property defines whether the reader expects a FlowFile to consist of a single Record or a series of Records with a “wrapper element”. Because XML does not provide for a way to read a series of XML documents from a stream directly, it is common to combine many XML documents by concatenating them and then wrapping the entire XML blob with a “wrapper element”. This property dictates whether the reader expects a FlowFile to consist of a single Record or a series of Records with a “wrapper element” that will be ignored. |
| Schema Inference Cache | schema-inference-cache |  |  | Specifies a Schema Cache to use when inferring the schema. If not populated, the schema will be inferred each time. However, if a cache is specified, the cache will first be consulted and if the applicable schema can be found, it will be used instead of inferring the schema. |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
