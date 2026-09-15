# PutFile 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Writes the contents of a FlowFile to the local file system

## Tags

archive, copy, files, filesystem, local, put

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Conflict Resolution Strategy | Indicates what should happen when a file with the same name already exists in the output directory |
| Create Missing Directories | If true, then missing destination directories will be created. If false, flowfiles are penalized and sent to failure. |
| Directory | The directory to which files should be written. You may use expression language such as /aa/bb/${path} |
| Group | Sets the group on the output file to the value of this attribute. You may also use expression language such as ${file.group}. |
| Last Modified Time | Sets the lastModifiedTime on the output file to the value of this attribute. Format must be yyyy-MM-dd ‘T’HH:mm:ssZ. You may also use expression language such as ${file.lastModifiedTime}. |
| Maximum File Count | Specifies the maximum number of files that can exist in the output directory |
| Owner | Sets the owner on the output file to the value of this attribute. You may also use expression language such as ${file.owner}. Note on many operating systems NiFi must be running as a super-user to have the permissions to set the file owner. |
| Permissions | Sets the permissions on the output file to the value of this attribute. Format must be either UNIX rwxrwxrwx with a - in place of denied permissions (e.g. rw-r–r–) or an octal number (e.g. 644). You may also use expression language such as ${file.permissions}. |

Expand

Show lessSee more

## Restrictions

| Required Permission | Explanation |
| --- | --- |
| write filesystem | Provides operator the ability to write to any file that NiFi has access to. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | Files that could not be written to the output directory for some reason are transferred to this relationship |
| success | Files that have been successfully written to the output directory are transferred to this relationship |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.standard.FetchFile](/user-guide/data-integration/openflow/processors/fetchfile)
- [org.apache.nifi.processors.standard.GetFile](/user-guide/data-integration/openflow/processors/getfile)
