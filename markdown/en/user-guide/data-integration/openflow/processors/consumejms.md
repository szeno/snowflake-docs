# ConsumeJMS 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-jms-processors-nar

## Description

Consumes JMS Message of type BytesMessage, TextMessage, ObjectMessage, MapMessage or StreamMessage transforming its content to a FlowFile and transitioning it to ‘success’ relationship. JMS attributes such as headers and properties will be copied as FlowFile attributes. MapMessages will be transformed into JSONs and then into byte arrays. The other types will have their raw contents as byte array transferred into the flowfile.

## Tags

consume, get, jms, message, receive

## Input Requirement

FORBIDDEN

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Acknowledgement Mode | The JMS Acknowledgement Mode. Using Auto Acknowledge can cause messages to be lost on restart of NiFi but may provide better performance than Client Acknowledge. |
| Connection Client ID | The client id to be set on the connection, if set. For durable non shared consumer this is mandatory, for all others it is optional, typically with shared consumers it is undesirable to be set. Please see JMS spec for further details |
| Connection Factory Service | The Controller Service that is used to obtain Connection Factory. Alternatively, the ‘JNDI \*’ or the ‘JMS \*’ properties can also be used to configure the Connection Factory. |
| Destination Name | The name of the JMS Destination. Usually provided by the administrator (e.g., ‘topic://myTopic’ or ‘myTopic’). |
| Destination Type | The type of the JMS Destination. Could be one of ‘QUEUE’ or ‘TOPIC’. Usually provided by the administrator. Defaults to ‘QUEUE’ |
| Durable subscription | If destination is Topic if present then make it the consumer durable. @see <https://jakarta.ee/specifications/platform/9/apidocs/jakarta/jms/session#createDurableConsumer-jakarta.jms>. Topic-java.lang. String- |
| Error Queue Name | The name of a JMS Queue where - if set - unprocessed messages will be routed. Usually provided by the administrator (e.g., ‘queue://myErrorQueue’ or ‘myErrorQueue’).Only applicable if ‘Destination Type’ is set to ‘QUEUE’ |
| Maximum Batch Size | The maximum number of messages to publish or consume in each invocation of the processor. |
| Message Selector | The JMS Message Selector to filter the messages that the processor will receive |
| Password | Password used for authentication and authorization. |
| SSL Context Service | The SSL Context Service used to provide client certificate information for TLS/SSL connections. |
| Shared subscription | If destination is Topic if present then make it the consumer shared. @see <https://jakarta.ee/specifications/platform/9/apidocs/jakarta/jms/session#createSharedConsumer-jakarta.jms>. Topic-java.lang. String- |
| Subscription Name | The name of the subscription to use if destination is Topic and is shared or durable. |
| Timeout | How long to wait to consume a message from the remote broker before giving up. |
| User Name | User Name used for authentication and authorization. |
| broker | URI pointing to the network location of the JMS Message broker. Example for ActiveMQ: ‘<tcp://myhost:61616>’. Examples for IBM MQ: ‘myhost(1414)’ and ‘myhost01(1414),myhost02(1414)’. |
| cf | The fully qualified name of the JMS ConnectionFactory implementation class (eg. org.apache.activemq. ActiveMQConnectionFactory). |
| cflib | Path to the directory with additional resources (eg. JARs, configuration files etc.) to be added to the classpath (defined as a comma separated list of values). Such resources typically represent target JMS client libraries for the ConnectionFactory implementation. |
| character-set | The name of the character set to use to construct or interpret TextMessages |
| connection.factory.name | The name of the JNDI Object to lookup for the Connection Factory. |
| java.naming.factory.initial | The fully qualified class name of the JNDI Initial Context Factory Class (java.naming.factory.initial). |
| java.naming.provider.url | The URL of the JNDI Provider to use as the value for java.naming.provider.url. See additional details documentation for allowed URL schemes. |
| java.naming.security.credentials | The Credentials to use when authenticating with JNDI (java.naming.security.credentials). |
| java.naming.security.principal | The Principal to use when authenticating with JNDI (java.naming.security.principal). |
| naming.factory.libraries | Specifies jar files and/or directories to add to the ClassPath in order to load the JNDI / JMS client libraries. This should be a comma-separated list of files, directories, and/or URLs. If a directory is given, any files in that directory will be included, but subdirectories will not be included (i.e., it is not recursive). |
| output-strategy | The format used to output the JMS message into a FlowFile record. |
| record-reader | The Record Reader to use for parsing received JMS Messages into Records. |
| record-writer | The Record Writer to use for serializing Records before writing them to a FlowFile. |

Expand

Show lessSee more

## Restrictions

| Required Permission | Explanation |
| --- | --- |
| reference remote resources | Client Library Location can reference resources over HTTP |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| parse.failure | If a message cannot be parsed using the configured Record Reader, the contents of the message will be routed to this Relationship as its own individual FlowFile. |
| success | All FlowFiles that are received from the JMS Destination are routed to this relationship |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| jms\_deliveryMode | The JMSDeliveryMode from the message header. |
| jms\_expiration | The JMSExpiration from the message header. |
| jms\_priority | The JMSPriority from the message header. |
| jms\_redelivered | The JMSRedelivered from the message header. |
| jms\_timestamp | The JMSTimestamp from the message header. |
| jms\_correlationId | The JMSCorrelationID from the message header. |
| jms\_messageId | The JMSMessageID from the message header. |
| jms\_type | The JMSType from the message header. |
| jms\_replyTo | The JMSReplyTo from the message header. |
| jms\_destination | The JMSDestination from the message header. |
| jms.messagetype | The JMS message type, can be TextMessage, BytesMessage, ObjectMessage, MapMessage or StreamMessage). |
| other attributes | Each message property is written to an attribute. |

Expand

Show lessSee more

## See also

- [org.apache.nifi.jms.processors.PublishJMS](/user-guide/data-integration/openflow/processors/publishjms)
