# ExecuteStreamCommand 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

The ExecuteStreamCommand processor provides a flexible way to integrate external commands and scripts into NiFi data flows. ExecuteStreamCommand can pass the incoming FlowFile’s content to the command that it executes similarly how piping works.

## Tags

command, command execution, execute, stream

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

true

## Properties

| Property | Description |
| --- | --- |
| Argument Delimiter | Delimiter to use to separate arguments for a command [default: ;]. Must be a single character |
| Command Arguments | The arguments to supply to the executable delimited by the ‘;’ character. |
| Command Path | Specifies the command to be executed; if just the name of an executable is provided, it must be in the user’s environment PATH. |
| Ignore STDIN | If true, the contents of the incoming flowfile will not be passed to the executing command |
| Max Attribute Length | If routing the output of the stream command to an attribute, the number of characters put to the attribute value will be at most this amount. This is important because attributes are held in memory and large attributes will quickly cause out of memory issues. If the output goes longer than this value, it will truncated to fit. Consider making this smaller if able. |
| Output Destination Attribute | If set, the output of the stream command will be put into an attribute of the original FlowFile instead of a separate FlowFile. There will no longer be a relationship for ‘output stream’ or ‘nonzero status’. The value of this property will be the key for the output attribute. |
| Output MIME Type | Specifies the value to set for the “mime.type” attribute. This property is ignored if ‘Output Destination Attribute’ is set. |
| Working Directory | The directory to use as the current working directory when executing the command |
| argumentsStrategy | Strategy for configuring arguments to be supplied to the command. |

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
| nonzero status | The destination path for the flow file created from the command’s output, if the returned status code is non-zero. All flow files routed to this relationship will be penalized. |
| original | The original FlowFile will be routed. It will have new attributes detailing the result of the script execution. |
| output stream | The destination path for the flow file created from the command’s output, if the returned status code is zero. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| execution.command | The name of the command executed |
| execution.command.args | The semi-colon delimited list of arguments. Sensitive properties will be masked |
| execution.status | The exit status code returned from executing the command |
| execution.error | Any error messages returned from executing the command |
| mime.type | Sets the MIME type of the output if the ‘Output MIME Type’ property is set and ‘Output Destination Attribute’ is not set |

Expand

Show lessSee more
