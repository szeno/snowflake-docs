# ListGoogleGroups 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-google-drive-nar

## Description

Lists all of the groups for a given domain in Google Workspace. It supports an optional ‘Query’ to filter the groups. The retrieved group metadata (id, etag, email, name, directMembersCount, description) are output to a Record Writer.

## Tags

cloud, directory, domain, gcp, google, groups, list

## Input Requirement

ALLOWED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Custom Query | Custom query to filter the returned groups. For example, ‘email=test-\*’. See Google’s Admin SDK Directory API documentation for supported syntax. |
| GCP Credentials Service | Controller Service used to obtain Google Cloud Platform credentials. |
| Google Domain | Domain name to list Google Groups (e.g., ‘example.com’). |
| Record Writer | Record writer used for writing out the records of retrieved Google Groups. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | FlowFiles are routed here if the processor fails to retrieve Google Groups. |
| retry | FlowFiles are routed here if a transient failure occurs (e.g. rate-limited, socket timeouts) and should be retried. |
| success | A FlowFile containing a record set of the groups is routed here upon success. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| record.count | The number of records (groups) returned. |
| mime.type | The MIME type for the resulting FlowFile. |

Expand

Show lessSee more

## See also

- [com.snowflake.openflow.runtime.processors.google.GetGoogleGroupMembers](/user-guide/data-integration/openflow/processors/getgooglegroupmembers)
