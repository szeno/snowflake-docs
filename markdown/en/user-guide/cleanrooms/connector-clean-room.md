# Snowflake Data Clean Rooms: Clean room connectors

End-of-life notice

The legacy Provider and Consumer Data Clean Rooms are being discontinued. See the
[end-of-life timeline](/user-guide/cleanrooms/pc-eol) for dates and migration guidance.

Note

Snowflake Data Clean Rooms do not currently support data subject consent management. Customers are responsible for ensuring they have
obtained all necessary rights and consents to use the data linked in their clean rooms. Customers must also ensure compliance with all
applicable laws and regulations when using Data Clean Rooms, including in connection with third-party connectors.

You can use connectors to integrate your clean room environment with clean rooms hosted on other cloud providers. This topic describes how
the clean room admin can configure a connector so Snowflake Data Clean Rooms can interact with third-party clean rooms.

Important

Third-party connectors are not offered by Snowflake and may be subject to additional terms. These integrations are made available for
your convenience, but you are responsible for any content sent to or received from the integrations.

Customers are responsible for obtaining any necessary consents in connection with their use of Snowflake Data Clean Rooms. Please ensure
that you are complying with applicable laws and regulations when using Snowflake Data Clean Rooms, including in connection with
third-party connectors for activation purposes.

## Amazon Marketing Cloud

Amazon Marketing Cloud (AMC) is a cloud-based clean room solution in which advertisers can perform analytics across pseudonymized signals,
including Amazon ads signals and their own inputs.

To configure the connector so your clean environment is integrated with the AMC:

1. Sign in to **Amazon Ads Account**.
2. Select **Account & Advertiser Instances**.
3. Select **Save**.

## Ads Data Hub

Ads Data Hub helps advertisers, agencies, and measurement partners do customized analysis of campaigns while protecting user privacy.

To configure the connector so your clean environment is integrated with Ads Data Hub:

1. Upload Service Account Credentials.
2. Enter the **Developer / API Key**.
3. Select **Authenticate**.
4. Select the **Parent Account**.
5. Enter the **Default Destination Dataset**.
6. Select **Child Account**.
7. Enter the **Clean Room Name**.
8. Select **Save**.
