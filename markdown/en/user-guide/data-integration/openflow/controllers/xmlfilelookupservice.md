# XMLFileLookupService

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

A reloadable XML file-based lookup service. This service uses Apache Commons Configuration. Example XML configuration file and how to access specific configuration can be found at <http://commons.apache.org/proper/commons-configuration/userguide/howto_hierarchical.html>. External entity processing is disabled.

## Tags

cache, enrich, join, key, lookup, reloadable, value, xml

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Configuration File \* | configuration-file |  |  | A configuration file |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

## Restrictions

| Required Permission | Explanation |
| --- | --- |
| read filesystem | Provides operator the ability to read from any file that NiFi has access to. |

Expand

Show lessSee more

## System Resource Considerations

This component does not specify system resource considerations.
