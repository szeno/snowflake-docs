# ExecuteProcess 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Runs an operating system command specified by the user and writes the output of that command to a FlowFile. If the command is expected to be long-running, the Processor can output the partial data on a specified interval. When this option is used, the output is expected to be in textual format, as it typically does not make sense to split binary data on arbitrary time-based intervals.

## Tags

command, external, invoke, process, script, source

## Input Requirement

FORBIDDEN

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Argument Delimiter | Delimiter to use to separate arguments for a command [default: space]. Must be a single character. |
| Batch Duration | If the process is expected to be long-running and produce textual output, a batch duration can be specified so that the output will be captured for this amount of time and a FlowFile will then be sent out with the results and a new FlowFile will be started, rather than waiting for the process to finish before sending out the results |
| Command | Specifies the command to be executed; if just the name of an executable is provided, it must be in the user’s environment PATH. |
| Command Arguments | The arguments to supply to the executable delimited by white space. White space can be escaped by enclosing it in double-quotes. |
| Output MIME type | Specifies the value to set for the “mime.type” attribute. This property is ignored if ‘Batch Duration’ is set. |
| Redirect Error Stream | If true will redirect any error stream output of the process to the output stream. This is particularly helpful for processes which write extensively to the error stream or for troubleshooting. |
| Working Directory | The directory to use as the current working directory when executing the command |

Expand

Show lessSee more

## Restrictions

| Required Permission | Explanation |
| --- | --- |
| execute code | Provides operator the ability to execute arbitrary code assuming all permissions that NiFi has. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| success | All created FlowFiles are routed to this relationship |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| command | Executed command |
| command.arguments | Arguments of the command |
| mime.type | Sets the MIME type of the output if the ‘Output MIME Type’ property is set and ‘Batch Duration’ is not set |

Expand

Show lessSee more
