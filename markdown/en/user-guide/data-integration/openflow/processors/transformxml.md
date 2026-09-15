# TransformXml 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Applies the provided XSLT file to the FlowFile XML payload. A new FlowFile is created with transformed content and is routed to the ‘success’ relationship. If the XSL transform fails, the original FlowFile is routed to the ‘failure’ relationship

## Tags

transform, xml, xslt

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| XSLT file name | Provides the name (including full path) of the XSLT file to apply to the FlowFile XML content. One of the ‘XSLT file name’ and ‘XSLT Lookup’ properties must be defined. |
| cache-size | Maximum number of stylesheets to cache. Zero disables the cache. |
| cache-ttl-after-last-access | The cache TTL (time-to-live) or how long to keep stylesheets in the cache after last access. |
| indent-output | Whether or not to indent the output. |
| secure-processing | Whether or not to mitigate various XML-related attacks like XXE (XML External Entity) attacks. |
| xslt-controller | Controller lookup used to store XSLT definitions. One of the ‘XSLT file name’ and ‘XSLT Lookup’ properties must be defined. WARNING: note that the lookup controller service should not be used to store large XSLT files. |
| xslt-controller-key | Key used to retrieve the XSLT definition from the XSLT lookup controller. This property must be set when using the XSLT controller property. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | If a FlowFile fails processing for any reason (for example, the FlowFile is not valid XML), it will be routed to this relationship |
| success | The FlowFile with transformed content will be routed to this relationship |

Expand

Show lessSee more
