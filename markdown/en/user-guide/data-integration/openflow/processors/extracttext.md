# ExtractText 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Evaluates one or more Regular Expressions against the content of a FlowFile. The results of those Regular Expressions are assigned to FlowFile Attributes. Regular Expressions are entered by adding user-defined properties; the name of the property maps to the Attribute Name into which the result will be placed. The attributes are generated differently based on the enabling of named capture groups. If named capture groups are not enabled: The first capture group, if any found, will be placed into that attribute name. But all capture groups, including the matching string sequence itself will also be provided at that attribute name with an index value provided, with the exception of a capturing group that is optional and does not match - for example, given the attribute name “regex” and expression “abc(def)?(g)” we would add an attribute “regex.1” with a value of “def” if the “def” matched. If the “def” did not match, no attribute named “regex.1” would be added but an attribute named “regex.2” with a value of “g” will be added regardless. If named capture groups are enabled: Each named capture group, if found will be placed into the attributes name with the name provided. If enabled the matching string sequence itself will be placed into the attribute name. If multiple matches are enabled, and index will be applied after the first set of matches. The exception is a capturing group that is optional and does not match For example, given the attribute name “regex” and expression “abc(?<NAMED>def)?(?<NAMED-TWO>g)” we would add an attribute “regex. NAMED” with the value of “def” if the “def” matched. We would add an attribute “regex. NAMED-TWO” with the value of “g” if the “g” matched regardless. The value of the property must be a valid Regular Expressions with one or more capturing groups. If named capture groups are enabled, all capture groups must be named. If they are not, then the processor configuration will fail validation. If the Regular Expression matches more than once, only the first match will be used unless the property enabling repeating capture group is set to true. If any provided Regular Expression matches, the FlowFile(s) will be routed to ‘matched’. If no provided Regular Expression matches, the FlowFile will be routed to ‘unmatched’ and no attributes will be applied to the FlowFile.

## Tags

Regular Expression, Text, evaluate, extract, regex

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Character Set | The Character Set in which the file is encoded |
| Enable Canonical Equivalence | Indicates that two characters match only when their full canonical decompositions match. |
| Enable Case-insensitive Matching | Indicates that two characters match even if they are in a different case. Can also be specified via the embedded flag (?i). |
| Enable DOTALL Mode | Indicates that the expression ‘.’ should match any character, including a line terminator. Can also be specified via the embedded flag (?s). |
| Enable Literal Parsing of the Pattern | Indicates that Metacharacters and escape characters should be given no special meaning. |
| Enable Multiline Mode | Indicates that ‘^’ and ‘$’ should match just after and just before a line terminator or end of sequence, instead of only the beginning or end of the entire input. Can also be specified via the embedded flag (?m). |
| Enable Unicode Predefined Character Classes | Specifies conformance with the Unicode Technical Standard #18: Unicode Regular Expression Annex C: Compatibility Properties. Can also be specified via the embedded flag (?U). |
| Enable Unicode-aware Case Folding | When used with ‘Enable Case-insensitive Matching’, matches in a manner consistent with the Unicode Standard. Can also be specified via the embedded flag (?u). |
| Enable Unix Lines Mode | Indicates that only the ‘line terminator is recognized in the behavior of’. ‘,’^ ‘, and’$’. Can also be specified via the embedded flag (?d). |
| Enable named group support | If set to true, when named groups are present in the regular expression, the name of the group will be used in the attribute name as opposed to the group index. All capturing groups must be named, if the number of groups (not including capture group 0) does not equal the number of named groups validation will fail. |
| Enable repeating capture group | If set to true, every string matching the capture groups will be extracted. Otherwise, if the Regular Expression matches more than once, only the first match will be extracted. |
| Include Capture Group 0 | Indicates that Capture Group 0 should be included as an attribute. Capture Group 0 represents the entirety of the regular expression match, is typically not used, and could have considerable length. |
| Maximum Buffer Size | Specifies the maximum amount of data to buffer (per FlowFile) in order to apply the regular expressions. FlowFiles larger than the specified maximum will not be fully evaluated. |
| Maximum Capture Group Length | Specifies the maximum number of characters a given capture group value can have. Any characters beyond the max will be truncated. |
| Permit Whitespace and Comments in Pattern | In this mode, whitespace is ignored, and embedded comments starting with # are ignored until the end of a line. Can also be specified via the embedded flag (?x). |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| matched | FlowFiles are routed to this relationship when the Regular Expression is successfully evaluated and the FlowFile is modified as a result |
| unmatched | FlowFiles are routed to this relationship when no provided Regular Expression matches the content of the FlowFile |

Expand

Show lessSee more
