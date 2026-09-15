# EmbeddedHazelcastCacheManager

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

A service that runs embedded Hazelcast and provides cache instances backed by that. The server does not ask for authentication, it is recommended to run it within secured network.

## Tags

cache, hazelcast

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Hazelcast Cluster Name \* | hazelcast-cluster-name | nifi |  | Name of the Hazelcast cluster. |
| Hazelcast Clustering Strategy \* | hazelcast-clustering-strategy | none | - None - All Nodes - Explicit | Specifies with what strategy the Hazelcast cluster should be created. |
| Hazelcast Instances | hazelcast-instances |  |  | Only used with “Explicit” Clustering Strategy! List of NiFi instance host names which should be part of the Hazelcast cluster. Host names are separated by comma. The port specified in the “Hazelcast Port” property will be used as server port. The list must contain every instance that will be part of the cluster. Other instances will join the Hazelcast cluster as clients. |
| Hazelcast Port \* | hazelcast-port | 5701 |  | Port for the Hazelcast instance to use. |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
