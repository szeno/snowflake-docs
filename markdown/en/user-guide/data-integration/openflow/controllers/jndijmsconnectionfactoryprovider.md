# JndiJmsConnectionFactoryProvider

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Provides a service to lookup an existing JMS ConnectionFactory using the Java Naming and Directory Interface (JNDI).

## Tags

integration, jms, jndi, messaging, publish, queue, subscribe, topic

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| JNDI Name of the Connection Factory \* | connection.factory.name |  |  | The name of the JNDI Object to lookup for the Connection Factory. |
| JNDI Initial Context Factory Class \* | java.naming.factory.initial |  |  | The fully qualified class name of the JNDI Initial Context Factory Class (java.naming.factory.initial). |
| JNDI Provider URL \* | java.naming.provider.url |  |  | The URL of the JNDI Provider to use as the value for java.naming.provider.url. See additional details documentation for allowed URL schemes. |
| JNDI Credentials | java.naming.security.credentials |  |  | The Credentials to use when authenticating with JNDI (java.naming.security.credentials). |
| JNDI Principal | java.naming.security.principal |  |  | The Principal to use when authenticating with JNDI (java.naming.security.principal). |
| JNDI / JMS Client Libraries | naming.factory.libraries |  |  | Specifies jar files and/or directories to add to the ClassPath in order to load the JNDI / JMS client libraries. This should be a comma-separated list of files, directories, and/or URLs. If a directory is given, any files in that directory will be included, but subdirectories will not be included (i.e., it is not recursive). |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
