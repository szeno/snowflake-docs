# JMSConnectionFactoryProvider

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Provides a generic service to create vendor specific javax.jms. ConnectionFactory implementations. The Connection Factory can be served once this service is configured successfully.

## Tags

integration, jms, messaging, publish, queue, subscribe, topic

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| JMS SSL Context Service | SSL Context Service |  |  | The SSL Context Service used to provide client certificate information for TLS/SSL connections. |
| JMS Broker URI | broker |  |  | URI pointing to the network location of the JMS Message broker. Example for ActiveMQ: ‘<tcp://myhost:61616>’. Examples for IBM MQ: ‘myhost(1414)’ and ‘myhost01(1414),myhost02(1414)’. |
| JMS Connection Factory Implementation Class \* | cf |  |  | The fully qualified name of the JMS ConnectionFactory implementation class (eg. org.apache.activemq.ActiveMQConnectionFactory). |
| JMS Client Libraries | cflib |  |  | Path to the directory with additional resources (eg. JARs, configuration files etc.) to be added to the classpath (defined as a comma separated list of values). Such resources typically represent target JMS client libraries for the ConnectionFactory implementation. |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

## Restrictions

| Required Permission | Explanation |
| --- | --- |
| reference remote resources | Client Library Location can reference resources over HTTP |

Expand

Show lessSee more

## System Resource Considerations

This component does not specify system resource considerations.
