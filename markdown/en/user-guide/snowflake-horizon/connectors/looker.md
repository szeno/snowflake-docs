# Looker

Horizon Catalog ingests Looker metadata (dashboards, Looks, explores, and usage) through the
Looker API. If your Looker projects use LookML models backed by a Git repository, Horizon Catalog
can also produce lineage between your warehouse and Looker by cloning those repositories with a
read-only SSH deploy key you install in [Step 6](#6-connect-git-repositories-for-lookml-projects).

## Before you start

To connect Looker to Horizon Catalog, you need the following:

- Admin access to your Looker instance.
- If you want LookML-based lineage: admin access to add deploy keys to the Git repositories backing
  your LookML projects (for example, **Settings > Deploy keys** on a GitHub repository).

Complete the following steps to enable metadata, lineage, and popularity of your Looker content in
Horizon Catalog.

1. [Create a permission set and role for Horizon Catalog](#1-create-a-permission-set-and-role-for-horizon-catalog).
2. [Create the Horizon Catalog user in Looker](#2-create-the-horizon-catalog-user-in-looker).
3. [Generate an API3 key](#3-generate-an-api3-key).
4. [Grant access to the Shared folder](#4-grant-access-to-the-shared-folder).
5. [Create the Looker connection](#5-create-the-looker-connection).
6. [Connect Git repositories for LookML projects](#6-connect-git-repositories-for-lookml-projects) (optional, required for lineage).

## 1. Create a permission set and role for Horizon Catalog

Create a Looker permission set and role with the minimum access that Horizon Catalog needs to
collect metadata, lineage, and popularity data.

1. In Looker, go to **Admin** > **Roles** > **Permission Sets**, and select **New Permission Set**.
2. For **Name**, enter `Horizon Catalog`.
3. Under **Permissions**, enable the following. Some permissions are nested under a parent
   permission in the Looker UI. Enable the parent before its children:

   - `access_data`
     - `see_lookml_dashboards`
     - `see_looks`
       - `see_user_dashboards`
       - `explore`
       - `see_lookml`
   - `see_queries`
   - `see_logs`
   - `see_users`
   - `see_datagroups`
   - `see_system_activity`
4. Select **Save Permission Set**.
5. Go to **Admin** > **Roles**, and select **New Role**.
6. For **Name**, enter `Horizon Catalog`.
7. For **Permission Set**, select **Horizon Catalog**.
8. For **Model Set**, select **All**.
9. Select **Save Role**.

## 2. Create the Horizon Catalog user in Looker

Create a dedicated Looker user for Horizon Catalog.

1. In Looker, go to **Admin** > **Users**, and select **Add Users**.
2. For **Email**, enter an email address for the Horizon Catalog user, for example,
   `horizoncatalog@yourcompany.com`.
3. Under **Roles**, select **Horizon Catalog**.
4. Select **Save** to create the user.

## 3. Generate an API3 key

Generate an API3 key for the Horizon Catalog user. Horizon Catalog uses the client ID and client
secret to authenticate with the Looker API.

1. In Looker, go to **Admin** > **Users**, and select the Horizon Catalog user.
2. Select **Edit Keys**.
3. Select **New API3 Key** to generate credentials.
4. Copy the **Client ID** and **Client Secret**, and securely store them for use in
   [Step 5](#5-create-the-looker-connection).

Caution

The client secret is displayed only once. Copy and store it before closing this page.

For details, see
[Looker API authentication](https://cloud.google.com/looker/docs/api-auth) in the Looker
documentation.

## 4. Grant access to the Shared folder

Grant the Horizon Catalog user view access to the Shared folder so that Horizon Catalog can discover
dashboards and Looks across your Looker instance.

1. In Looker, go to **Browse** > **Shared**.
2. Select the gear icon, then select **Manage Access**.
3. In the **Share with** field, enter the name or email of the Horizon Catalog user, and set the
   permission level to **View**.
4. Select **Save**.

## 5. Create the Looker connection

1. In Snowflake, open **Catalog** > **Connections** and select **Looker** from the Metadata
   connections section.
2. Fill out the setup form with the following information:

   | Field | Value |
   | --- | --- |
   | **Display Name** | A name for this connection. The default is `Looker`, but you can override it. |
   | **Client ID** | The client ID from [Step 3](#3-generate-an-api3-key). |
   | **Client Secret** | The client secret from [Step 3](#3-generate-an-api3-key). |
   | **Host URL** | The base URL of your Looker instance, for example, `https://yourcompany.cloud.looker.com`. |
   | **Snowflake Database** | The Snowflake database where Horizon Catalog stores the connector metadata. The default is `CONNECTORS`. |
   | **Snowflake Schema** | The Snowflake schema where Horizon Catalog stores the connector metadata. The default is `METADATA`. |

   Expand

   Show lessSee more
3. Select **Create connection**.

## 6. Connect Git repositories for LookML projects

Looker defines its data model in LookML, a Git-backed language where each Looker project maps to a
Git repository. To let Horizon Catalog read your LookML files and produce lineage between your
warehouse and Looker, grant it read-only access to each project’s Git repository.

Note

This step is optional. Skipping it does not prevent Horizon Catalog from ingesting Looker
dashboards, Looks, explores, and usage, but Horizon Catalog can’t produce LookML-based lineage for
a project without it.

1. After you select **Create connection** in [Step 5](#5-create-the-looker-connection), Horizon
   Catalog opens the **Select Projects** step and lists the LookML projects it discovered from your
   Looker instance.
2. Select the checkbox next to each project you want Horizon Catalog to ingest.
3. For each selected project that uses an SSH Git remote, select **Copy key** next to the project
   to copy its Snowflake-generated SSH public key.

   Note

   Projects that use an HTTPS Git remote show a warning icon instead of a key. SSH deploy keys are
   only supported for SSH remote URLs. Horizon Catalog can’t clone HTTPS-backed projects.
4. In your Git provider (for example, GitHub), open the LookML project’s repository and go to
   **Settings > Deploy keys**, then select **Add deploy key**.
5. Paste the copied key, give it a descriptive title (for example, `Horizon Catalog`), and leave
   **Allow write access** unchecked. Horizon Catalog only needs read access.
6. Select **Add key**.
7. Repeat steps 3–6 for each selected project, then select **Next** to save your selection and
   start ingestion.

Caution

If you don’t install the deploy key for a selected project, or the key is later removed from the
Git repository, Horizon Catalog can’t clone the repository and LookML lineage for that project
fails to ingest.

## Connection security

All communication between Horizon Catalog and Looker uses HTTPS (TLS 1.2 or higher). Authentication
uses an API3 client ID and secret, which are stored as encrypted secrets. No additional encryption
configuration is required.

For more details, see
[Security and data protection](/user-guide/snowflake-horizon/connectors/security).
