# PublishAMQP 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-amqp-nar

## Description

Creates an AMQP Message from the contents of a FlowFile and sends the message to an AMQP Exchange. In a typical AMQP exchange model, the message that is sent to the AMQP Exchange will be routed based on the ‘Routing Key’ to its final destination in the queue (the binding). If due to some misconfiguration the binding between the Exchange, Routing Key and Queue is not set up, the message will have no final destination and will return (i.e., the data will not make it to the queue). If that happens you will see a log in both app-log and bulletin stating to that effect, and the FlowFile will be routed to the ‘failure’ relationship.

## Tags

amqp, message, publish, put, rabbit, send

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| AMQP Version | AMQP Version. Currently only supports AMQP v0.9.1. |
| Brokers | A comma-separated list of known AMQP Brokers in the format <host>:<port> (e.g., localhost:5672). If this is set, Host Name and Port are ignored. Only include hosts from the same AMQP cluster. |
| Client Certificate Authentication Enabled | Authenticate using the SSL certificate rather than user name/password. |
| Exchange Name | The name of the AMQP Exchange the messages will be sent to. Usually provided by the AMQP administrator (e.g., ‘amq.direct’). It is an optional property. If kept empty the messages will be sent to a default AMQP exchange. |
| Header Separator | The character that is used to split key-value for headers. The value must only one character. Otherwise you will get an error message |
| Headers Pattern | Regular expression that will be evaluated against the FlowFile attributes to select the matching attributes and put as AMQP headers. Attribute name will be used as header key. |
| Headers Source | The source of the headers which will be applied to the published message. |
| Host Name | Network address of AMQP broker (e.g., localhost). If Brokers is set, then this property is ignored. |
| Password | Password used for authentication and authorization. |
| Port | Numeric value identifying Port of AMQP broker (e.g., 5671). If Brokers is set, then this property is ignored. |
| Routing Key | The name of the Routing Key that will be used by AMQP to route messages from the exchange to a destination queue(s). Usually provided by the administrator (e.g., ‘myKey’)In the event when messages are sent to a default exchange this property corresponds to a destination queue name, otherwise a binding from the Exchange to a Queue via Routing Key must be set (usually by the AMQP administrator) |
| SSL Context Service | The SSL Context Service used to provide client certificate information for TLS/SSL connections. |
| Username | Username used for authentication and authorization. |
| Virtual Host | Virtual Host name which segregates AMQP system for enhanced security. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | All FlowFiles that cannot be routed to the AMQP destination are routed to this relationship |
| success | All FlowFiles that are sent to the AMQP destination are routed to this relationship |

Expand

Show lessSee more
