# PublishJMS 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-jms-processors-nar

## Description

Creates a JMS Message from the contents of a FlowFile and sends it to a JMS Destination (queue or topic) as JMS BytesMessage or TextMessage. FlowFile attributes will be added as JMS headers and/or properties to the outgoing JMS message.

## Tags

jms, message, publish, put, send

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Connection Client ID | The client id to be set on the connection, if set. For durable non shared consumer this is mandatory, for all others it is optional, typically with shared consumers it is undesirable to be set. Please see JMS spec for further details |
| Connection Factory Service | The Controller Service that is used to obtain Connection Factory. Alternatively, the ‘JNDI \*’ or the ‘JMS \*’ properties can also be used to configure the Connection Factory. |
| Destination Name | The name of the JMS Destination. Usually provided by the administrator (e.g., ‘topic://myTopic’ or ‘myTopic’). |
| Destination Type | The type of the JMS Destination. Could be one of ‘QUEUE’ or ‘TOPIC’. Usually provided by the administrator. Defaults to ‘QUEUE’ |
| Maximum Batch Size | The maximum number of messages to publish or consume in each invocation of the processor. |
| Password | Password used for authentication and authorization. |
| SSL Context Service | The SSL Context Service used to provide client certificate information for TLS/SSL connections. |
| User Name | User Name used for authentication and authorization. |
| allow-illegal-chars-in-jms-header-names | Specifies whether illegal characters in header names should be sent to the JMS broker. Usually hyphens and full-stops. |
| attributes-to-send-as-jms-headers-regex | Specifies the Regular Expression that determines the names of FlowFile attributes that should be sent as JMS Headers |
| broker | URI pointing to the network location of the JMS Message broker. Example for ActiveMQ: ‘<tcp://myhost:61616>’. Examples for IBM MQ: ‘myhost(1414)’ and ‘myhost01(1414),myhost02(1414)’. |
| cf | The fully qualified name of the JMS ConnectionFactory implementation class (eg. org.apache.activemq. ActiveMQConnectionFactory). |
| cflib | Path to the directory with additional resources (eg. JARs, configuration files etc.) to be added to the classpath (defined as a comma separated list of values). Such resources typically represent target JMS client libraries for the ConnectionFactory implementation. |
| character-set | The name of the character set to use to construct or interpret TextMessages |
| connection.factory.name | The name of the JNDI Object to lookup for the Connection Factory. |
| java.naming.factory.initial | The fully qualified class name of the JNDI Initial Context Factory Class (java.naming.factory.initial). |
| java.naming.provider.url | The URL of the JNDI Provider to use as the value for java.naming.provider.url. See additional details documentation for allowed URL schemes. |
| java.naming.security.credentials | The Credentials to use when authenticating with JNDI (java.naming.security.credentials). |
| java.naming.security.principal | The Principal to use when authenticating with JNDI (java.naming.security.principal). |
| message-body-type | The type of JMS message body to construct. |
| naming.factory.libraries | Specifies jar files and/or directories to add to the ClassPath in order to load the JNDI / JMS client libraries. This should be a comma-separated list of files, directories, and/or URLs. If a directory is given, any files in that directory will be included, but subdirectories will not be included (i.e., it is not recursive). |
| record-reader | The Record Reader to use for parsing the incoming FlowFile into Records. |
| record-writer | The Record Writer to use for serializing Records before publishing them as an JMS Message. |

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
| failure | All FlowFiles that cannot be sent to JMS destination are routed to this relationship |
| success | All FlowFiles that are sent to the JMS destination are routed to this relationship |

Expand

Show lessSee more

## See also

- [org.apache.nifi.jms.processors.ConsumeJMS](/user-guide/data-integration/openflow/processors/consumejms)
