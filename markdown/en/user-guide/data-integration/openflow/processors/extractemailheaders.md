# ExtractEmailHeaders 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-email-nar

## Description

Using the flowfile content as source of data, extract header from an RFC compliant email file adding the relevant attributes to the flowfile. This processor does not perform extensive RFC validation but still requires a bare minimum compliance with RFC 2822

## Tags

email, split

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Additional Header List | COLON separated list of additional headers to be extracted from the flowfile content. NOTE the header key is case insensitive and will be matched as lower-case. Values will respect email contents. |
| Email Address Parsing | If “strict”, strict address format parsing rules are applied to mailbox and mailbox list fields, such as “to” and “from” headers, and FlowFiles with poorly formed addresses will be routed to the failure relationship, similar to messages that fail RFC compliant format validation. If “non-strict”, the processor will extract the contents of mailbox list headers as comma-separated values without attempting to parse each value as well-formed Internet mailbox addresses. This is optional and defaults to Strict Address Parsing |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | Flowfiles that could not be parsed as a RFC-2822 compliant message |
| success | Extraction was successful |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| email.headers.bcc.\* | Each individual BCC recipient (if available) |
| email.headers.cc.\* | Each individual CC recipient (if available) |
| email.headers.from.\* | Each individual mailbox contained in the From of the Email (array as per RFC-2822) |
| email.headers.message-id | The value of the Message-ID header (if available) |
| email.headers.received\_date | The Received-Date of the message (if available) |
| email.headers.sent\_date | Date the message was sent |
| email.headers.subject | Subject of the message (if available) |
| email.headers.to.\* | Each individual TO recipient (if available) |
| email.attachment\_count | Number of attachments of the message |

Expand

Show lessSee more
