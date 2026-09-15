# GetFile 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Creates FlowFiles from files in a directory. NiFi will ignore files it doesn’t have at least read permissions for.

## Tags

files, filesystem, get, ingest, ingress, input, local, source

## Input Requirement

FORBIDDEN

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Batch Size | The maximum number of files to pull in each invocation of the processor |
| File Filter | Only files whose names match the given regular expression will be picked up |
| Ignore Hidden Files | Indicates whether or not hidden files should be ignored |
| Input Directory | The input directory from which to pull files |
| Keep Source File | If true, the file is not deleted after it has been copied to the Content Repository; this causes the file to be picked up continually and is useful for testing purposes. If not keeping original NiFi will need write permissions on the directory it is pulling from otherwise it will ignore the file. |
| Maximum File Age | The maximum age that a file must be in order to be pulled; any file older than this amount of time (according to last modification date) will be ignored |
| Maximum File Size | The maximum size that a file can be in order to be pulled |
| Minimum File Age | The minimum age that a file must be in order to be pulled; any file younger than this amount of time (according to last modification date) will be ignored |
| Minimum File Size | The minimum size that a file must be in order to be pulled |
| Path Filter | When Recurse Subdirectories is true, then only subdirectories whose path matches the given regular expression will be scanned |
| Polling Interval | Indicates how long to wait before performing a directory listing |
| Recurse Subdirectories | Indicates whether or not to pull files from subdirectories |

Expand

Show lessSee more

## Restrictions

| Required Permission | Explanation |
| --- | --- |
| read filesystem | Provides operator the ability to read from any file that NiFi has access to. |
| write filesystem | Provides operator the ability to delete any file that NiFi has access to. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| success | All files are routed to success |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| filename | The filename is set to the name of the file on disk |
| path | The path is set to the relative path of the file’s directory on disk. For example, if the <Input Directory> property is set to /tmp, files picked up from /tmp will have the path attribute set to ./. If the <Recurse Subdirectories> property is set to true and a file is picked up from /tmp/abc/1/2/3, then the path attribute will be set to abc/1/2/3 |
| file.creationTime | The date and time that the file was created. May not work on all file systems |
| file.lastModifiedTime | The date and time that the file was last modified. May not work on all file systems |
| file.lastAccessTime | The date and time that the file was last accessed. May not work on all file systems |
| file.owner | The owner of the file. May not work on all file systems |
| file.group | The group owner of the file. May not work on all file systems |
| file.permissions | The read/write/execute permissions of the file. May not work on all file systems |
| absolute.path | The full/absolute path from where a file was picked up. The current ‘path’ attribute is still populated, but may be a relative path |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.standard.FetchFile](/user-guide/data-integration/openflow/processors/fetchfile)
- [org.apache.nifi.processors.standard.PutFile](/user-guide/data-integration/openflow/processors/putfile)
