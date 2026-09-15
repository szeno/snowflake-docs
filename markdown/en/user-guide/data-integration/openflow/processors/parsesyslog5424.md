# ParseSyslog5424 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Attempts to parse the contents of a well formed Syslog message in accordance to RFC5424 format and adds attributes to the FlowFile for each of the parts of the Syslog message, including Structured Data. Structured Data will be written to attributes as one attribute per item id + parameter see <https://tools.ietf.org/html/rfc5424.Note>: ParseSyslog5424 follows the specification more closely than ParseSyslog. If your Syslog producer does not follow the spec closely, with regards to using ‘-’ for missing header entries for example, those logs will fail with this parser, where they would not fail with ParseSyslog.

## Tags

attributes, event, logs, message, syslog, syslog5424, system

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Character Set | Specifies which character set of the Syslog messages |
| include\_policy | If true, then the Syslog Message body will be included in the attributes. |
| nil\_policy | Defines how NIL values are handled for header fields. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | Any FlowFile that could not be parsed as a Syslog message will be transferred to this Relationship without any attributes being added |
| success | Any FlowFile that is successfully parsed as a Syslog message will be to this Relationship. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| syslog.priority | The priority of the Syslog message. |
| syslog.severity | The severity of the Syslog message derived from the priority. |
| syslog.facility | The facility of the Syslog message derived from the priority. |
| syslog.version | The optional version from the Syslog message. |
| syslog.timestamp | The timestamp of the Syslog message. |
| syslog.hostname | The hostname or IP address of the Syslog message. |
| syslog.appname | The appname of the Syslog message. |
| syslog.procid | The procid of the Syslog message. |
| syslog.messageid | The messageid the Syslog message. |
| syslog.structuredData | Multiple entries per structuredData of the Syslog message. |
| syslog.sender | The hostname of the Syslog server that sent the message. |
| syslog.body | The body of the Syslog message, everything after the hostname. |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.standard.ListenSyslog](/user-guide/data-integration/openflow/processors/listensyslog)
- [org.apache.nifi.processors.standard.ParseSyslog](/user-guide/data-integration/openflow/processors/parsesyslog)
- [org.apache.nifi.processors.standard.PutSyslog](/user-guide/data-integration/openflow/processors/putsyslog)
