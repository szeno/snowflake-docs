# TailFile 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

“Tails” a file, or a list of files, ingesting data from the file as it is written to the file. The file is expected to be textual. Data is ingested only when a new line is encountered (carriage return or new-line character or combination). If the file to tail is periodically “rolled over”, as is generally the case with log files, an optional Rolling Filename Pattern can be used to retrieve data from files that have rolled over, even if the rollover occurred while NiFi was not running (provided that the data still exists upon restart of NiFi). It is generally advisable to set the Run Schedule to a few seconds, rather than running with the default value of 0 secs, as this Processor will consume a lot of resources if scheduled very aggressively. At this time, this Processor does not support ingesting files that have been compressed when ‘rolled over’.

## Tags

file, log, source, tail, text

## Input Requirement

FORBIDDEN

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| File Location | Specifies where the state is located either local or cluster so that state can be stored appropriately in order to ensure that all data is consumed without duplicating data upon restart of NiFi |
| File to Tail | Path of the file to tail in case of single file mode. If using multifile mode, regular expression to find files to tail in the base directory. In case recursivity is set to true, the regular expression will be used to match the path starting from the base directory (see additional details for examples). |
| Initial Start Position | When the Processor first begins to tail data, this property specifies where the Processor should begin reading data. Once data has been ingested from a file, the Processor will continue from the last point from which it has received data. |
| Line Start Pattern | A Regular Expression to match against the start of a log line. If specified, any line that matches the expression, and any following lines, will be buffered until another line matches the Expression. In doing this, we can avoid splitting apart multi-line messages in the file. This assumes that the data is in UTF-8 format. |
| Max Buffer Size | When using the Line Start Pattern, there may be situations in which the data in the file being tailed never matches the Regular Expression. This would result in the processor buffering all data from the tailed file, which can quickly exhaust the heap. To avoid this, the Processor will buffer only up to this amount of data before flushing the buffer, even if it means ingesting partial data from the file. |
| Post-Rollover Tail Period | When a file is rolled over, the processor will continue tailing the rolled over file until it has not been modified for this amount of time. This allows for another process to rollover a file, and then flush out any buffered data. Note that when this value is set, and the tailed file rolls over, the new file will not be tailed until the old file has not been modified for the configured amount of time. Additionally, when using this capability, in order to avoid data duplication, this period must be set longer than the Processor’s Run Schedule, and the Processor must not be stopped after the file being tailed has been rolled over and before the data has been fully consumed. Otherwise, the data may be duplicated, as the entire file may be written out as the contents of a single FlowFile. |
| Rolling Filename Pattern | If the file to tail “rolls over” as would be the case with log files, this filename pattern will be used to identify files that have rolled over so that if NiFi is restarted, and the file has rolled over, it will be able to pick up where it left off. This pattern supports wildcard characters \* and ?, it also supports the notation ${filename} to specify a pattern based on the name of the file (without extension), and will assume that the files that have rolled over live in the same directory as the file being tailed. The same glob pattern will be used for all files. |
| pre-allocated-buffer-size | Sets the amount of memory that is pre-allocated for each tailed file. |
| reread-on-nul | If this option is set to ‘true’, when a NUL character is read, the processor will yield and try to read the same part again later. (Note: Yielding may delay the processing of other files tailed by this processor, not just the one with the NUL character.) The purpose of this flag is to allow users to handle cases where reading a file may return temporary NUL values. NFS for example may send file contents out of order. In this case the missing parts are temporarily replaced by NUL values. CAUTION! If the file contains legitimate NUL values, setting this flag causes this processor to get stuck indefinitely. For this reason users should refrain from using this feature if they can help it and try to avoid having the target file on a file system where reads are unreliable. |
| tail-base-directory | Base directory used to look for files to tail. This property is required when using Multifile mode. |
| tail-mode | Mode to use: single file will tail only one file, multiple file will look for a list of file. In Multiple mode the Base directory is required. |
| tailfile-lookup-frequency | Only used in Multiple files mode. It specifies the minimum duration the processor will wait before listing again the files to tail. |
| tailfile-maximum-age | Only used in Multiple files mode. It specifies the necessary minimum duration to consider that no new messages will be appended in a file regarding its last modification date. This should not be set too low to avoid duplication of data in case new messages are appended at a lower frequency. |
| tailfile-recursive-lookup | When using Multiple files mode, this property defines if files must be listed recursively or not in the base directory. |

Expand

Show lessSee more

## State management

| Scopes | Description |
| --- | --- |
| LOCAL | Stores state about where in the Tailed File it left off so that on restart it does not have to duplicate data. State is stored either local or clustered depend on the <File Location> property. |
| CLUSTER | Stores state about where in the Tailed File it left off so that on restart it does not have to duplicate data. State is stored either local or clustered depend on the <File Location> property. |

Expand

Show lessSee more

## Restrictions

| Required Permission | Explanation |
| --- | --- |
| read filesystem | Provides operator the ability to read from any file that NiFi has access to. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| success | All FlowFiles are routed to this Relationship. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| tailfile.original.path | Path of the original file the flow file comes from. |

Expand

Show lessSee more
