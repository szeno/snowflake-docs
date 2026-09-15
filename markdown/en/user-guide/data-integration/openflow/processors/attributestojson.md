# AttributesToJSON 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Generates a JSON representation of the input FlowFile Attributes. The resulting JSON can be written to either a new Attribute ‘JSONAttributes’ or written to the FlowFile as content. Attributes which contain nested JSON objects can either be handled as JSON or as escaped JSON depending on the strategy chosen.

## Tags

attributes, flowfile, json

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Attributes List | Comma separated list of attributes to be included in the resulting JSON. If this value is left empty then all existing Attributes will be included. This list of attributes is case sensitive. If an attribute specified in the list is not found it will be emitted to the resulting JSON with an empty string or NULL value. |
| Destination | Control if JSON value is written as a new flowfile attribute ‘JSONAttributes’ or written in the flowfile content. Writing to flowfile content will overwrite any existing flowfile content. |
| Include Core Attributes | Determines if the FlowFile org.apache.nifi.flowfile.attributes. CoreAttributes which are contained in every FlowFile should be included in the final JSON value generated. |
| JSON Handling Strategy | Strategy to use for handling attributes which contain nested JSON. |
| Null Value | If true a non existing selected attribute will be NULL in the resulting JSON. If false an empty string will be placed in the JSON |
| Pretty Print | Apply pretty print formatting to the output. |
| attributes-to-json-regex | Regular expression that will be evaluated against the flow file attributes to select the matching attributes. This property can be used in combination with the attributes list property. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | Failed to convert attributes to JSON |
| success | Successfully converted attributes to JSON |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| JSONAttributes | JSON representation of Attributes |

Expand

Show lessSee more
