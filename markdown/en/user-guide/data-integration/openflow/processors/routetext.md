# RouteText 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Routes textual data based on a set of user-defined rules. Each line in an incoming FlowFile is compared against the values specified by user-defined Properties. The mechanism by which the text is compared to these user-defined properties is defined by the ‘Matching Strategy’. The data is then routed according to these rules, routing each line of the text individually.

## Tags

Expression Language, Regular Expression, attributes, csv, delimited, detect, filter, find, logs, regex, regexp, routing, search, string, text

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Character Set | The Character Set in which the incoming text is encoded |
| Grouping Regular Expression | Specifies a Regular Expression to evaluate against each line to determine which Group the line should be placed in. The Regular Expression must have at least one Capturing Group that defines the line’s Group. If multiple Capturing Groups exist in the Regular Expression, the values from all Capturing Groups will be concatenated together. Two lines will not be placed into the same FlowFile unless they both have the same value for the Group (or neither line matches the Regular Expression). For example, to group together all lines in a CSV File by the first column, we can set this value to “(.*?),.*”. Two lines that have the same Group but different Relationships will never be placed into the same FlowFile. |
| Ignore Case | If true, capitalization will not be taken into account when comparing values. E.g., matching against ‘HELLO’ or ‘hello’ will have the same result. This property is ignored if the ‘Matching Strategy’ is set to ‘Satisfies Expression’. |
| Ignore Leading/Trailing Whitespace | Indicates whether or not the whitespace at the beginning and end of the lines should be ignored when evaluating the line. |
| Matching Strategy | Specifies how to evaluate each line of incoming text against the user-defined properties. |
| Routing Strategy | Specifies how to determine which Relationship(s) to use when evaluating the lines of incoming text against the ‘Matching Strategy’ and user-defined properties. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| original | The original input file will be routed to this destination when the lines have been successfully routed to 1 or more relationships |
| unmatched | Data that does not satisfy the required user-defined rules will be routed to this Relationship |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| RouteText.Route | The name of the relationship to which the FlowFile was routed. |
| RouteText.Group | The value captured by all capturing groups in the ‘Grouping Regular Expression’ property. If this property is not set or contains no capturing groups, this attribute will not be added. |

Expand

Show lessSee more

## Use cases

| Drop blank or empty lines from the FlowFile’s content. |
| --- |
| Remove specific lines of text from a file, such as those containing a specific word or having a line length over some threshold. |

Expand

Show lessSee more
