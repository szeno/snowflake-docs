# Salesforce Analytics

Horizon Catalog ingests Salesforce dashboards, reports, and datasets, and produces lineage for that
content. To collect Salesforce object and field metadata, see
[Salesforce](/user-guide/snowflake-horizon/connectors/salesforce).

## Before you start

To connect Salesforce Analytics to Horizon Catalog, you need the following:

- Administrator access to your Salesforce org, so you can create a user and reset a security token.
- A Salesforce user that signs in with a username and password. Horizon Catalog authenticates as this
  user.
- Don’t set **Login IP Ranges** on that user’s profile. Those ranges block Salesforce API logins from
  outside the range, including Horizon Catalog, even when you send a security token. Org-level
  **Network Access** trusted IPs don’t block a login that includes a security token. Horizon Catalog
  doesn’t publish static egress IPs; see
  [Horizon Catalog egress](/user-guide/snowflake-horizon/connectors/security#horizon-catalog-egress).
- Access to CRM Analytics, Lightning Reports & Dashboards, or both, depending on the content you
  connect.

Caution

Use a user that signs in with a username and password. A user that signs in only through an identity
provider, such as Okta, can’t authenticate to the Salesforce API with this connection.

Complete the following steps to connect Salesforce Analytics to Horizon Catalog:

1. [Create a Salesforce user for Horizon Catalog](#1-create-a-salesforce-user-for-horizon-catalog).
2. [Grant the required permissions](#2-grant-the-required-permissions).
3. [Get the security token](#3-get-the-security-token).
4. [Create the Salesforce Analytics connection](#4-create-the-salesforce-analytics-connection).
5. [Set up metadata access](#5-set-up-metadata-access).

## 1. Create a Salesforce user for Horizon Catalog

Create a dedicated user for Horizon Catalog.

1. In Salesforce, open **Setup**.
2. In Quick Find, enter `Users`, then select **Users**.
3. Select **New User**.
4. Set the following values:
   - **Last Name:** `Horizon Catalog`
   - **Email:** An email address that can receive the security token.
   - **Username:** A Salesforce username that is unique across all Salesforce orgs. Keep it for
     [Step 4](#4-create-the-salesforce-analytics-connection).
   - **User License:** **Salesforce**
   - **Profile:** **Minimum Access - Salesforce**
5. Select **Generate new password and notify user immediately**, then select **Save**. Salesforce
   emails a link to set a password. Keep that password for
   [Step 4](#4-create-the-salesforce-analytics-connection).

Note

Don’t restrict the user to API access yet. You get the security token by signing in to Salesforce as
this user in [Step 3](#3-get-the-security-token), and a user with **API Only User** can’t open
Salesforce in a browser. Step 3 assigns **API Only User** after you have the token.

## 2. Grant the required permissions

Create a permission set, assign it to the Horizon Catalog user, and grant the following permissions
in it:

- **API Enabled**, so the user can call the Salesforce API.
- **Use Any API Auth**. Salesforce requires this permission for SOAP API `login()`. It’s already
  required in orgs created in Winter ’26 or later, and in all orgs starting December 1, 2026. For details, see
  [Platform SOAP API login() Retirement & new Security Requirements](https://help.salesforce.com/s/articleView?id=005132110&type=5)
  in the Salesforce documentation.
- **Password Never Expires**, so the password and security token don’t expire and break the
  connection. Salesforce’s default policy expires passwords every 90 days, and changing the password
  also resets the security token.

Also grant the permissions for the content you connect:

- For **CRM Analytics**, assign a CRM Analytics permission set license, such as **CRM Analytics
  Plus** or **CRM Analytics Growth**, and grant **Use CRM Analytics**. Horizon Catalog collects only
  the CRM Analytics apps that are shared with the user, so share each app you want to collect with
  the user.
- For **Lightning Reports & Dashboards**, grant **Run Reports**, read access to the Report,
  Dashboard, and DashboardComponent objects, and access to the report and dashboard folders you want
  to collect.

Horizon Catalog doesn’t collect private Lightning reports and dashboards.

If your org was created in Winter ’26 or later, SOAP API `login()` is off by default, and Horizon
Catalog can’t sign in until you turn it on. In **Setup**, enter `User Interface` in Quick Find,
select **User Interface**, and select **Enable SOAP API login()**. You can’t undo this setting on
the **User Interface** page.

## 3. Get the security token

Horizon Catalog sends the security token with the username and password when it signs in.

1. Sign in to Salesforce as the Horizon Catalog user, with the password from
   [Step 1](#1-create-a-salesforce-user-for-horizon-catalog). Salesforce might ask you to set up
   multi-factor authentication for this user the first time you sign in.
2. Open the user menu and select **My Settings**.
3. Under **Personal**, select **Reset My Security Token**.
4. Select **Reset Security Token**. Salesforce emails the token to the user’s email address.

After you have the security token, restrict the user to API access: add **API Only User** to the
permission set from [Step 2](#2-grant-the-required-permissions).

To rotate the password or security token later, remove **API Only User** from the permission set,
sign in as the Horizon Catalog user, reset the password and security token, update the connection in
Snowflake, then add **API Only User** back.

For details, see
[Reset your security token](https://help.salesforce.com/s/articleView?id=sf.user_security_token.htm&type=5)
in the Salesforce documentation.

## 4. Create the Salesforce Analytics connection

1. In Snowflake, open **Catalog > Connections** and select **Salesforce Analytics** from the
   Metadata connections section.
2. Fill out the setup form with the following information:

   - **Display Name:** A name for this connection. The default is `SalesforceAnalytics`.
   - **Integration:** The Salesforce content to collect. The default is **CRM Analytics**. Select
     one of the following:
     - **CRM Analytics**
     - **Lightning Reports & Dashboards**
     - **Lightning Reports & Dashboards + CRM Analytics**
   - **Username:** The username of the Horizon Catalog user from
     [Step 1](#1-create-a-salesforce-user-for-horizon-catalog).
   - **Password:** The password for that user.
   - **Security token:** The security token from [Step 3](#3-get-the-security-token).
   - **API version:** The Salesforce API version. The field opens with `64.0`. Keep `64.0`: it’s the
     minimum version for CRM Analytics lens metadata, and Horizon Catalog signs in with SOAP API
     `login()`, which Salesforce doesn’t support in API version 65.0 and later. Horizon Catalog
     requires a value in this field. To find the version your org uses, see
     [Find the Salesforce API version](https://help.salesforce.com/s/articleView?id=000386929&type=1)
     in the Salesforce documentation.
   - **Domain:** The Salesforce login domain, without `https://`. The field opens with `login`,
     which reaches a production org. Use `test` for a sandbox. For a My Domain org, enter the part of
     your My Domain URL before `.salesforce.com`, for example `acme.my` for
     `https://acme.my.salesforce.com`. If you clear the field, Horizon Catalog uses `login`.
   - **Snowflake Database** and **Snowflake Schema:** The database and schema in your Snowflake
     account where Horizon Catalog stores the connector metadata. The defaults are `CONNECTORS` and
     `METADATA`. Horizon Catalog creates them if they don’t already exist.
3. Select **Next**. Horizon Catalog creates the connection and continues to the **Load data** step,
   where the first sync starts.
4. When the wizard confirms that the connection is ready, select **Done**. The sync continues to run
   in the background.

## 5. Set up metadata access

Other roles can’t see the metadata and lineage that this connector collects until you grant them
access. Grant `USAGE` on the connector, and on the database and schema that contain it, to each role
that needs to view the connector’s metadata and lineage:

Copy code

```
GRANT USAGE ON DATABASE CONNECTORS TO ROLE <role_name>;
GRANT USAGE ON SCHEMA CONNECTORS.METADATA TO ROLE <role_name>;
GRANT USAGE ON METADATA CONNECTOR CONNECTORS.METADATA.<connector_name> TO ROLE <role_name>;
```

If you stored the connector in a different database or schema, replace `CONNECTORS` and `METADATA`
with the actual database and schema names.

For more information about metadata access, see
[Metadata access control](/user-guide/snowflake-horizon/connectors/access-control).

## Connection security

All communication between Horizon Catalog and Salesforce uses HTTPS (TLS 1.2 or higher).
Authentication uses a Salesforce username, password, and security token, which are stored as
encrypted secrets. No additional encryption configuration is required.

For more details, see
[Security and data protection](/user-guide/snowflake-horizon/connectors/security).
