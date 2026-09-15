# Snowflake Data Clean Room: External data from Azure Blob Storage

End-of-life notice

The legacy Provider and Consumer Data Clean Rooms are being discontinued. Migrate to the
[Collaboration API](/user-guide/cleanrooms/overview) using the
[migration tool](/user-guide/cleanrooms/migration-tool) before the dates below.

- **2026-10-01:** New legacy clean rooms may not be created via the
  [web application user interface](/user-guide/cleanrooms/v1/web-app-introduction).
- **2027-02-01:** The [web application user interface](/user-guide/cleanrooms/v1/web-app-introduction)
  will no longer be accessible, and new legacy clean rooms may not be created via the
  [Provider and Consumer API](/user-guide/cleanrooms/getting-started).
- **2027-06-01:** Legacy [Provider and Consumer clean rooms](/user-guide/cleanrooms/getting-started)
  will no longer be accessible. Use the [Collaboration API](/user-guide/cleanrooms/overview)
  to create and manage clean rooms.

Note

Snowflake Data Clean Rooms do not currently support data subject consent management. Customers are responsible for ensuring they have
obtained all necessary rights and consents to use the data linked in their clean rooms. Customers must also ensure compliance with all
applicable laws and regulations when using Data Clean Rooms, including in connection with third-party connectors.

Data analyzed in a [Snowflake Data Clean Room](/user-guide/cleanrooms/overview) can be native to Snowflake, reside externally
in cloud provider storage, or both. A *connector* allows collaborators to access external data from a cloud provider from within the clean
room.

The external data connector uses [Snowflake external tables](/user-guide/tables-external-intro) to make data
available. Be aware that there is an increased security risk associated with linking external tables in a clean room. As a result,
the provider must explicitly allow the use of external tables in the clean room before
consumers can use a connector to include external data. If the provider uses the external data connector, the consumer is warned that
external tables are being used so they can decide whether to install the clean room.

This topic describes how to use a connector so clean room analysts can access external data from Azure Blob Storage.

Important

Third-party connectors are not offered by Snowflake and may be subject to additional terms. These integrations are made available for
your convenience, but you are responsible for any content sent to or received from the integrations.

Customers are responsible for obtaining any necessary consents in connection with their use of Snowflake Data Clean Rooms. Please ensure
that you are complying with applicable laws and regulations when using Snowflake Data Clean Rooms, including in connection with
third-party connectors for activation purposes.

## Prerequisites

To use the connector for external data:

- The provider must explicitly [allow the use of external tables in the clean room](/user-guide/cleanrooms/register-data).
- Files must be in parquet format.

## Connect to Azure Blob Storage

Allowing clean room collaborators to access data from Azure Blob Storage consists of the following steps:

1. In Azure, [obtain the identifiers of the blob storage](#label-cleanroom-external-data-azure-identifiers).
2. In the clean room environment, [create the connector](#label-cleanroom-external-data-azure-connector).
3. Use the clean room environment to initiate the process of
   [granting permissions to the connector](#label-cleanroom-external-data-azure-permissions), then complete the process in Microsoft.
4. In the clean room environment, [authenticate the connector with Azure](#label-cleanroom-external-data-azure-authenticate).

The following sections discuss these steps in more detail.

### Obtain identifiers associated with blob storage

The clean room connector needs the tenant ID associated with Azure Blob Storage and the URL that uniquely identifies the blob
storage that the clean room needs to access. Before creating the connector, you must obtain both of these identifiers from Azure.

Note

Microsoft changed the name of Azure Active Directory to Microsoft Entra ID.

To obtain the tenant ID that establishes a trust relationship between Azure Blob Storage and Microsoft Entra ID:

1. Sign in to the Microsoft Azure portal.
2. From the home dashboard, select **Microsoft Entra ID** » **Properties**.
3. Find the **Tenant ID** field and select the copy icon. You will use this identifier when you
   [create the connector](#label-cleanroom-external-data-azure-connector).

To obtain the URL that uniquely identifies the blob storage:

1. Sign in to the Microsoft Azure portal.
2. From the home dashboard, select **Storage Accounts**.
3. Navigate the storage account until you see the blob storage folder in the list. This folder must contain the data that you want to
   include in the clean room.
4. Find the blob storage folder in the list, and select **…** more menu » **Copy URL**. You will use this identifier when you
   [create the connector](#label-cleanroom-external-data-azure-connector).

### Create the connector and copy the service principal identifier

You are now ready to create the connector in the clean room environment. Once you have created the connector, you will need to copy the
identifier of the Azure service principal that is associated with the clean room environment.

To create the connector in your clean room environment:

1. [Sign in to the clean rooms UI.](/user-guide/cleanrooms/web-app-introduction#label-cleanroom-web-app-sign-in)
2. In the left navigation, select **Connectors**, then expand the **Microsoft Azure** section.
3. In the **Tenant ID** field, enter the tenant ID that you copied in the
   [previous step](#label-cleanroom-external-data-azure-identifiers).
4. In the **Path URL** field, enter the URL of the blob storage that you copied in the
   [previous step](#label-cleanroom-external-data-azure-identifiers), then replace `https://` with `azure://` in the URL.
5. Select **Create**.
6. Use the copy icon to copy the identifier of the **Azure service principal** that is now associated with the clean room environment, and
   save it for the next task. Azure uses service principals to grant access to applications.

### Grant permissions to the connector

Clean rooms need permission to access external data in Azure Blob Storage. The process of granting these permissions begins in the clean
room environment and ends in Microsoft.

To grant permissions to the connector:

1. In the clean room environment, select **Connectors** and expand the **Microsoft Azure** section. If you are signed out of the
   clean room, see [Sign in to the clean rooms UI](/user-guide/cleanrooms/web-app-introduction#label-cleanroom-web-app-sign-in).
2. Select **Consent URL**. A Microsoft dialog appears.
3. In the Microsoft dialog, ensure that **Consent on behalf of your organization** is selected, then select **Accept**.

   Microsoft grants the Azure service principal associated with the clean room environment an access token to the blob storage inside of
   your tenant.
4. In a new browser window, sign in to the Microsoft Azure portal.
5. From the home dashboard, select **Storage Accounts**.
6. Select the storage account that contains the blob storage.
7. Select **Access Control (IAM)**.
8. Select **Add role assignment**.
9. Select **Storage Blob Data Reader** to grant read-only access to a **Azure service principal**, then select **Next**.
10. On the **Members** tab, select **+ Select members**.
11. Search for the service principal associated with the clean room environment. You copied its identifier in a
    [previous step](#label-cleanroom-external-data-azure-connector).

Tip

Microsoft can take over an hour to create the service principal for the clean room environment. If you cannot find the service
principal in the list, wait 1-2 hours, then try to complete this step again.

12. Select **Review + assign**.

### Authenticate the connector

You are now ready to authenticate the connector to make sure it can access Azure Blob Storage. To authenticate the connector:

1. In the clean room environment, select **Connectors** and expand the **Microsoft Azure** section. If you are signed out of the
   clean room, see [Sign in to the clean rooms UI](/user-guide/cleanrooms/web-app-introduction#label-cleanroom-web-app-sign-in).
2. Select the blob storage you are connecting to, and select **Authenticate**.

## Remove access to external data on AWS

To remove access to Azure Blob Storage from a clean room environment:

1. [Sign in to the clean rooms UI.](/user-guide/cleanrooms/web-app-introduction#label-cleanroom-web-app-sign-in)
2. In the left navigation, select **Connectors** and expand the **Microsoft Azure** section.
3. Find the blob storage that is currently connected, and select the trash can icon.
