# CountText 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Counts various metrics on incoming text. The requested results will be recorded as attributes. The resulting flowfile will not have its content modified.

## Tags

character, count, line, text, word

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| ajust-immediately | If true, the counter will be updated immediately, without regard to whether the ProcessSession is commit or rolled back;otherwise, the counter will be incremented only if and when the ProcessSession is committed. |
| character-encoding | Specifies a character encoding to use. |
| split-words-on-symbols | If enabled, the word count will identify strings separated by common logical delimiters [ \_ - . ] as independent words (ex. split-words-on-symbols = 4 words). |
| text-character-count | If enabled, will count the number of characters (including whitespace and symbols, but not including newlines and carriage returns) present in the incoming text. |
| text-line-count | If enabled, will count the number of lines present in the incoming text. |
| text-line-nonempty-count | If enabled, will count the number of lines that contain a non-whitespace character present in the incoming text. |
| text-word-count | If enabled, will count the number of words (alphanumeric character groups bounded by whitespace) present in the incoming text. Common logical delimiters [\_-.] do not bound a word unless ‘Split Words on Symbols’ is true. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | If the flowfile text cannot be counted for some reason, the original file will be routed to this destination and nothing will be routed elsewhere |
| success | The flowfile contains the original content with one or more attributes added containing the respective counts |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| text.line.count | The number of lines of text present in the FlowFile content |
| text.line.nonempty.count | The number of lines of text (with at least one non-whitespace character) present in the original FlowFile |
| text.word.count | The number of words present in the original FlowFile |
| text.character.count | The number of characters (given the specified character encoding) present in the original FlowFile |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.standard.SplitText](/user-guide/data-integration/openflow/processors/splittext)
