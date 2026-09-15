# ValidateXml 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Validates XML contained in a FlowFile. By default, the XML is contained in the FlowFile content. If the ‘XML Source Attribute’ property is set, the XML to be validated is contained in the specified attribute. It is not recommended to use attributes to hold large XML documents; doing so could adversely affect system performance. Full schema validation is performed if the processor is configured with the XSD schema details. Otherwise, the only validation performed is to ensure the XML syntax is correct and well-formed, e.g. all opening tags are properly closed.

## Tags

schema, validation, xml, xsd

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Schema File | The file path or URL to the XSD Schema file that is to be used for validation. If this property is blank, only XML syntax/structure will be validated. |
| XML Source Attribute | The name of the attribute containing XML to be validated. If this property is blank, the FlowFile content will be validated. |

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
| invalid | FlowFiles that are not valid according to the specified schema or contain invalid XML are routed to this relationship |
| valid | FlowFiles that are successfully validated against the schema, if provided, or verified to be well-formed XML are routed to this relationship |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| validatexml.invalid.error | If the flow file is routed to the invalid relationship the attribute will contain the error message resulting from the validation failure. |

Expand

Show lessSee more
