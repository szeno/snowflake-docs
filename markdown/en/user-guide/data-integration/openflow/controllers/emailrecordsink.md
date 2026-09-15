# EmailRecordSink

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Provides a RecordSinkService that can be used to send records in email using the specified writer for formatting.

## Tags

email, record, send, sink, smtp, write

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| BCC | bcc |  |  | The recipients to include in the BCC-Line of the email. Comma separated sequence of addresses following RFC822 syntax. |
| CC | cc |  |  | The recipients to include in the CC-Line of the email. Comma separated sequence of addresses following RFC822 syntax. |
| From \* | from |  |  | Specifies the Email address to use as the sender. Comma separated sequence of addresses following RFC822 syntax. |
| Record Writer \* | record-sink-record-writer |  |  | Specifies the Controller Service to use for writing out the records. |
| SMTP Auth \* | smtp-auth | true |  | Flag indicating whether authentication should be used |
| SMTP Hostname \* | smtp-hostname |  |  | The hostname of the SMTP Server that is used to send Email Notifications |
| SMTP Password | smtp-password |  |  | Password for the SMTP account |
| SMTP Port \* | smtp-port | 25 |  | The Port used for SMTP communications |
| SMTP SSL \* | smtp-ssl | false |  | Flag indicating whether SSL should be enabled |
| SMTP STARTTLS \* | smtp-starttls | false |  | Flag indicating whether STARTTLS should be enabled. If the server does not support STARTTLS, the connection continues without the use of TLS |
| SMTP Username | smtp-username |  |  | Username for the SMTP account |
| SMTP X-Mailer Header \* | smtp-xmailer-header | NiFi |  | X-Mailer used in the header of the outgoing email |
| Subject \* | subject | Message from NiFi |  | The email subject |
| To | to |  |  | The recipients to include in the To-Line of the email. Comma separated sequence of addresses following RFC822 syntax. |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
