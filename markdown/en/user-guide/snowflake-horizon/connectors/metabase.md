# Metabase

## Before you start

To connect Metabase to Horizon Catalog, you need the following:

- Administrator access to your Metabase instance. Horizon Catalog authenticates with an API key in
  the **Administrators** group, which is required to read users and all collections.

Complete the following steps to enable metadata, lineage, and popularity of your Metabase dashboards,
questions, and collections in Horizon Catalog.

1. [Identify your Metabase URL](#1-identify-your-metabase-url).
2. [Create an API key](#2-create-an-api-key).
3. [Create the Metabase connection](#3-create-the-metabase-connection).

## 1. Identify your Metabase URL

The URL is the address you use to sign in to Metabase, for example `https://example.metabaseapp.com`.
Keep this information for the next steps.

## 2. Create an API key

Horizon Catalog authenticates with a Metabase **API key**. You must be a Metabase administrator to
create one, and the key must be in the **Administrators** group so that Horizon Catalog can read
users and all collections.

1. In Metabase, select the **gear** icon in the upper right, then select **Admin settings**.
2. Go to the **Settings** tab, then select **Authentication** in the left menu.
3. Scroll to **API Keys** and select **Manage**.
4. Select **Create API Key**.
5. Enter a **Key name**, for example `Horizon Catalog`.
6. For **Group**, select **Administrators**.
7. Select **Create**, then copy the generated key and store it securely for use in
   [Step 3](#3-create-the-metabase-connection).

Note

Metabase shows the API key only once. Copy and store it before closing this page.

For details, see [API keys](https://www.metabase.com/docs/latest/people-and-groups/api-keys) in the
Metabase documentation.

## 3. Create the Metabase connection

1. In Snowflake, open **Catalog** > **Connections** and select **Metabase** from the Metadata
   connections section.
2. Fill out the setup form with the following information:

   | Field | Value |
   | --- | --- |
   | **Display Name** | A name for this connection. The default is `Metabase`, but you can override it. |
   | **URL** | Your Metabase URL from [Step 1](#1-identify-your-metabase-url), for example `https://example.metabaseapp.com`. |
   | **API Key** | The API key from [Step 2](#2-create-an-api-key). |
   | **Snowflake Database** | The Snowflake database where Horizon Catalog stores the connector metadata. The default is `CONNECTORS`. |
   | **Snowflake Schema** | The Snowflake schema where Horizon Catalog stores the connector metadata. The default is `METADATA`. |

   Expand

   Show lessSee more
3. Select **Create connection**.

## Connection security

All communication between Horizon Catalog and Metabase uses HTTPS (TLS 1.2 or higher). Authentication
uses a Metabase API key, which is stored as an encrypted secret. No additional encryption
configuration is required.

For more details, see
[Security and data protection](/user-guide/snowflake-horizon/connectors/security).
