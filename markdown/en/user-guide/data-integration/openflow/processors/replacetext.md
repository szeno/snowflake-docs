# ReplaceText 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Updates the content of a FlowFile by searching for some textual value in the FlowFile content (via Regular Expression/regex, or literal value) and replacing the section of the content that matches with some alternate value. It can also be used to append or prepend text to the contents of a FlowFile.

## Tags

Change, Modify, Regex, Regular Expression, Replace, Text, Update

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Character Set | The Character Set in which the file is encoded |
| Evaluation Mode | Run the ‘Replacement Strategy’ against each line separately (Line-by-Line) or buffer the entire file into memory (Entire Text) and run against that. |
| Line-by-Line Evaluation Mode | Run the ‘Replacement Strategy’ against each line separately (Line-by-Line) for all lines in the FlowFile, First Line (Header) alone, Last Line (Footer) alone, Except the First Line (Header) or Except the Last Line (Footer). |
| Maximum Buffer Size | Specifies the maximum amount of data to buffer (per file or per line, depending on the Evaluation Mode) in order to apply the replacement. If ‘Entire Text’ (in Evaluation Mode) is selected and the FlowFile is larger than this value, the FlowFile will be routed to ‘failure’. In ‘Line-by-Line’ Mode, if a single line is larger than this value, the FlowFile will be routed to ‘failure’. A default value of 1 MB is provided, primarily for ‘Entire Text’ mode. In ‘Line-by-Line’ Mode, a value such as 8 KB or 16 KB is suggested. This value is ignored if the <Replacement Strategy> property is set to one of: Append, Prepend, Always Replace |
| Regular Expression | The Search Value to search for in the FlowFile content. Only used for ‘Literal Replace’ and ‘Regex Replace’ matching strategies |
| Replacement Strategy | The strategy for how and what to replace within the FlowFile’s text content. |
| Replacement Value | The value to insert using the ‘Replacement Strategy’. Using “Regex Replace” back-references to Regular Expression capturing groups are supported, but back-references that reference capturing groups that do not exist in the regular expression will be treated as literal value. Back References may also be referenced using the Expression Language, as ‘$1’, ‘$2’, etc. The single-tick marks MUST be included, as these variables are not “Standard” attribute names (attribute names must be quoted unless they contain only numbers, letters, and \_). |
| Text to Append | The text to append to the end of the FlowFile, or each line, depending on the configured value of the Evaluation Mode property |
| Text to Prepend | The text to prepend to the start of the FlowFile, or each line, depending on the configured value of the Evaluation Mode property |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | FlowFiles that could not be updated are routed to this relationship |
| success | FlowFiles that have been successfully processed are routed to this relationship. This includes both FlowFiles that had text replaced and those that did not. |

Expand

Show lessSee more

## Use cases

| Append text to the end of every line in a FlowFile |
| --- |
| Prepend text to the beginning of every line in a FlowFile |
| Replace every occurrence of a literal string in the FlowFile with a different value |
| Transform every occurrence of a literal string in a FlowFile |
| Completely replace the contents of a FlowFile to a specific text |

Expand

Show lessSee more
