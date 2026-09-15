# PutEmail 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Sends an e-mail to configured recipients for each incoming FlowFile

## Tags

email, notify, put, smtp

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

true

## Properties

| Property | Description |
| --- | --- |
| Attach File | Specifies whether or not the FlowFile content should be attached to the email |
| BCC | The recipients to include in the BCC-Line of the email. Comma separated sequence of addresses following RFC822 syntax. |
| CC | The recipients to include in the CC-Line of the email. Comma separated sequence of addresses following RFC822 syntax. |
| Content Type | Mime Type used to interpret the contents of the email, such as text/plain or text/html |
| From | Specifies the Email address to use as the sender. Comma separated sequence of addresses following RFC822 syntax. |
| Include All Attributes In Message | Specifies whether or not all FlowFile attributes should be recorded in the body of the email message |
| Message | The body of the email message |
| Reply-To | The recipients that will receive the reply instead of the from (see RFC2822 §3.6.2).This feature is useful, for example, when the email is sent by a no-reply account. This field is optional. Comma separated sequence of addresses following RFC822 syntax. |
| SMTP Auth | Flag indicating whether authentication should be used |
| SMTP Hostname | The hostname of the SMTP host |
| SMTP Password | Password for the SMTP account |
| SMTP Port | The Port used for SMTP communications |
| SMTP Socket Factory | Socket Factory to use for SMTP Connection |
| SMTP TLS | Flag indicating whether Opportunistic TLS should be enabled using STARTTLS command |
| SMTP Username | Username for the SMTP account |
| SMTP X-Mailer Header | X-Mailer used in the header of the outgoing email |
| Subject | The email subject |
| To | The recipients to include in the To-Line of the email. Comma separated sequence of addresses following RFC822 syntax. |
| attribute-name-regex | A Regular Expression that is matched against all FlowFile attribute names. Any attribute whose name matches the regex will be added to the Email messages as a Header. If not specified, no FlowFile attributes will be added as headers. |
| authorization-mode | How to authorize sending email on the user’s behalf. |
| email-ff-content-as-message | Specifies whether or not the FlowFile content should be the message of the email. If true, the ‘Message’ property is ignored. |
| input-character-set | Specifies the character set of the FlowFile contents for reading input FlowFile contents to generate the message body or as an attachment to the message. If not set, UTF-8 will be the default value. |
| oauth2-access-token-provider | OAuth2 service that can provide access tokens. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | FlowFiles that fail to send will be routed to this relationship |
| success | FlowFiles that are successfully sent will be routed to this relationship |

Expand

Show lessSee more
