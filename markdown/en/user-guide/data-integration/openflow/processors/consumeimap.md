# ConsumeIMAP 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-email-nar

## Description

Consumes messages from Email Server using IMAP protocol. The raw-bytes of each received email message are written as contents of the FlowFile

## Tags

Consume, Email, Get, Imap, Ingest, Ingress, Message

## Input Requirement

FORBIDDEN

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Authorization Mode | How to authorize sending email on the user’s behalf. |
| Connection Timeout | The amount of time to wait to connect to Email server |
| Delete Messages | Specify whether mail messages should be deleted after retrieval. |
| Fetch Size | Specify the maximum number of Messages to fetch per call to Email Server. |
| Folder | Email folder to retrieve messages from (e.g., INBOX) |
| Host Name | Network address of Email server (e.g., pop.gmail.com, imap.gmail.com . .) |
| Mark Messages as Read | Specify if messages should be marked as read after retrieval. |
| OAuth2 Access Token Provider | OAuth2 service that can provide access tokens. |
| Password | Password used for authentication and authorization with Email server. |
| Port | Numeric value identifying Port of Email server (e.g., 993) |
| Use SSL | Specifies if IMAP connection must be obtained via SSL encrypted connection (i.e., IMAPS) |
| User Name | User Name used for authentication and authorization with Email server. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| success | All messages that are the are successfully received from Email server and converted to FlowFiles are routed to this relationship |

Expand

Show lessSee more
