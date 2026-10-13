# Omni

## Before you start

To connect Omni to Horizon Catalog, you need the following:

- Admin access to your Omni account.

Complete the following steps to enable metadata, lineage, and popularity of your Omni content in
Horizon Catalog.

1. [Identify your Omni domain](#1-identify-your-omni-domain).
2. [Generate an API key](#2-generate-an-api-key).
3. [Create the Omni connection](#3-create-the-omni-connection).

## 1. Identify your Omni domain

Horizon Catalog uses your Omni domain to send API requests. Your domain is the subdomain portion of
your Omni access URL. For example, if you access Omni at `https://mycompany.omniapp.co`, your domain
is `mycompany`.

Keep this information for [Step 3](#3-create-the-omni-connection).

## 2. Generate an API key

To generate an API key, you must be assigned an Admin account in Omni.

1. In Omni, go to **Settings > API Access**.
2. Under **Organization keys**, select **Generate a New Key**.

   Note

   Organization keys are used for service integrations, such as Horizon Catalog.
3. Copy the API key, and securely store it for [Step 3](#3-create-the-omni-connection).

## 3. Create the Omni connection

1. In Snowflake, open **Catalog > Connections** and select **Omni** from the Metadata connections
   section.
2. Fill out the setup form with the following information:

   | Field | Value |
   | --- | --- |
   | **Display Name** | A name for this connection. The default is `Omni`, but you can override it. |
   | **Domain** | The domain from [Step 1](#1-identify-your-omni-domain). |
   | **API Key** | The API key from [Step 2](#2-generate-an-api-key). |
   | **Snowflake Database** | The Snowflake database where Horizon Catalog stores the connector metadata. The default is `CONNECTORS`. |
   | **Snowflake Schema** | The Snowflake schema where Horizon Catalog stores the connector metadata. The default is `METADATA`. |

   Expand

   Show lessSee more
3. Select **Create connection**.

## Connection security

All communication between Horizon Catalog and Omni uses HTTPS (TLS 1.2 or higher). Authentication
uses an API key, which is stored as an encrypted secret. No additional encryption configuration is
required.

For more details, see [Security and data protection](/user-guide/snowflake-horizon/connectors/security).
