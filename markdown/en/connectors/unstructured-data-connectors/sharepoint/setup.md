# Set up the Snowflake Connector for SharePoint

[Preview Feature](/release-notes/preview-features) — Open

Support for this feature is available to accounts in most Snowflake regions. See [Regional availability](/connectors/unstructured-data-connectors/sharepoint/about#label-sharepoint-regional-availability) for a full list of regions.

Note

The Snowflake Connector for SharePoint is subject to the [Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

Important

Thank you for your interest in the Snowflake Connector for SharePoint.
We’re now focused on a next-generation solution that will offer a significantly
improved experience; therefore, moving this connector to the general availability
status is currently not on our product roadmap.
You may continue to use this connector as a preview feature, but please note that support for future bug
fixes and improvements is not guaranteed. The new solution is available as [Openflow Connector for SharePoint](/user-guide/data-integration/openflow/connectors/sharepoint/about) and
includes better performance, customizability, and enhanced deployment options.

This topic describes the steps to set up your Snowflake Connector for SharePoint.

## Prerequisites

Before you begin installing and configuring the connector, you must do the following:

1. Ensure that you have a [Microsoft Graph](https://learn.microsoft.com/en-us/graph/overview) application with the following permissions:

   - [Sites.Selected](https://learn.microsoft.com/en-us/graph/permissions-reference#sitesselected): limits access only to specified sites.
   - [Files.SelectedOperations.Selected](https://learn.microsoft.com/en-us/graph/permissions-reference#filesselectedoperationsselected): limits access only to files in specified sites.
   - [GroupMember.Read.All](https://learn.microsoft.com/en-us/graph/permissions-reference#groupmemberreadall): used for resolving SharePoint group permissions.
2. Configure SharePoint to enable OAuth authentication as described
   in [Get access without a user](https://learn.microsoft.com/en-us/graph/auth-v2-service?tabs=http#authentication-and-authorization-steps).
   The connector uses the following Microsoft Graph APIs to fetch data from SharePoint:

   - [Download driveItem content](https://learn.microsoft.com/en-us/graph/api/driveitem-get-content?view=graph-rest-1.0&tabs=http)
   - [driveItem: delta](https://learn.microsoft.com/en-us/graph/api/driveitem-delta?view=graph-rest-1.0&tabs=http)
   - [List who has access to a file](https://learn.microsoft.com/en-us/graph/api/driveitem-list-permissions?view=graph-rest-1.0&tabs=http)
   - [group: delta](https://learn.microsoft.com/en-us/graph/api/group-delta?view=graph-rest-1.0&tabs=http)
   - [List group members](https://learn.microsoft.com/en-us/graph/api/group-list-members?view=graph-rest-1.0&tabs=http)
3. Get the site URL of your Microsoft 365 SharePoint site with files or folders that you want to ingest into Snowflake
   and the credentials from your Azure or Office 365 account administrator.

## Install the Snowflake Connector for SharePoint

Connectors are instances of Snowflake native applications.
To install the Snowflake Connector for SharePoint, do the following:

1. Sign in to Snowflake as a user with the ACCOUNTADMIN role.
2. In the navigation menu, select **Marketplace** » **Snowflake Marketplace**.
3. Search for the Snowflake Connector for SharePoint and select **Get**.
4. In the dialog box, expand **Options** and enter the following information:

   - In **Application name**, enter a name for your connector application.
   - In **Warehouse used for installation**, select the warehouse that you want to use for installing the connector.

     Note

     This is not the same warehouse that is used by the connector to synchronize data from SharePoint. In a later step,
     you will create a separate warehouse for this purpose.
5. Select **Get** to begin the installation process. This can take a few minutes to complete.
6. After the connector is successfully installed, either select **Configure** to proceed with
   the [configuration](#label-configure-sharepoint-connector) or select **Done** to close the dialog box and complete the installation.

### Optional: Install multiple instances of Snowflake Connector for SharePoint

You can install multiple instances of the Snowflake Connector for SharePoint on your Snowflake account.
To install an additional instance, do the following:

1. Navigate to Snowflake Marketplace and select Snowflake Connector for SharePoint. The application details page appears.
2. Click **Add instance**. The installation dialog appears.
3. Provide the instance name and select the warehouse to be used during the installation.
4. Select **Get** to begin the installation process.

Note

- Adding connector instances can take several minutes. When the installation process completes, you get an email notification.
- To avoid ingested data corruption, during connector configuration, always use a database schema that is different from all other native applications.

## Configure the Snowflake Connector for SharePoint

Each connector application instance must be configured to communicate with its associated Sharepoint instance.
After completing the [installation process](#label-install-sharepoint-connector), proceed with the following steps.

1. Ensure that all the prerequisites are completed. For more information see [Prerequisites](#label-sharepoint-connector-prereqs).
2. If required, open the configuration wizard as follows:
   1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) as a user with the ACCOUNTADMIN role.
   2. In the navigation menu, select **Catalog** » **Apps**.
   3. Search for the Snowflake Connector for SharePoint and select it.

### Configure

1. In the **Configure** step of the wizard, enter information in the following fields:

> Note
>
> By default, the fields are set to the names of objects created when you configure the connector.
> Snowflake recommends using new objects for these fields.
> However, if required, you can specify the names of existing objects, for example if reinstalling the connector.
>
> | Field | Description |
> | --- | --- |
> | **Warehouse for Ingestion Data** | Identifier for a new dedicated virtual warehouse for the connector. This warehouse is used for computing the data ingestion and document processing tasks.  Specify a name that is unique for your account. The name of the warehouse must be a valid [object identifier](/sql-reference/identifiers-syntax).  Alternatively, you can select an existing warehouse.  Note  Do not specify the warehouse used during the initial creation of the connector. |
> | **Warehouse for Cortex Search**: | Identifier for a new, dedicated Cortex search virtual warehouse. This warehouse is used to process and serve Cortex Search queries.  Specify a name that is unique for your account. The name of the warehouse must be a valid [object identifier](/sql-reference/identifiers-syntax).  Note  Do not specify the same warehouse that you selected at the beginning of the connector installation. The configuration process creates a new X-Small warehouse with the specified name. |
> | **Role for Cortex Search** | Identifier for a new custom role for the connector. Specify a name that is unique for your account. The name of the role must be a valid [object identifier](/sql-reference/identifiers-syntax).  Users who have granted the role can use their account to query Cortex REST API about the data ingested by the application. By default, only the account that you used to install the connector has permission to query Cortex. |
>
> Expand
>
> Show lessSee more

1. Click **Configure** to continue.

### Authenticate and connect to Sharepoint

Important

Ensure that pop-ups are enabled in your browser.

1. In the **Authentication** step of the wizard, enter the following information and credentials to complete the OAuth2 authentication and connect to SharePoint.

   Contact your Azure or Office 365 account administrator for this information.

   | Field | Description |
   | --- | --- |
   | **SharePoint site URL** | URL or Sharepoint site from which the connector will ingest content.  For top-level sites, use domain name only, for example, `sitename.sharepoint.com`. For sub-sites,use a domain name with the site path, for example, `sitename.sharepoint.com/sites/SubSite`. |
   | **Client ID** | Enter your client ID. To learn about client ID and how to find it in Microsoft Entra, see [Application ID (client ID)](https://learn.microsoft.com/en-us/azure/healthcare-apis/register-application#application-id-client-id). |
   | **Client secret** | Enter your client secret. To learn about a client secret and how to find it in Microsoft Entra, see [Certificates & secrets](https://learn.microsoft.com/en-us/azure/healthcare-apis/register-application#certificates--secrets). |
   | **Tenant ID** | Enter your tenant ID. To learn about tenant ID and how to find it in Microsoft Entra, see [Find your Microsoft 365 tenant ID](https://learn.microsoft.com/en-us/sharepoint/find-your-office-365-tenant-id). |

   Expand

   Show lessSee more
2. Click **Next** to begin the connection process, which can take several minutes to complete.

### Validate source

In the **Validate source** step of the wizard, do the following:

1. Select the source from which you want to fetch the files:

   - Select **All folders** if you want to fetch files from all the folders that are accessible through
     the credentials you provided in [Authenticate and connect to Sharepoint](#label-connect-to-sharepoint).
   - Select **Specific folder** if you want to fetch files from a specific folder that is accessible
     through the credentials you provided in [Authenticate and connect to Sharepoint](#label-connect-to-sharepoint).

     Note

     This path is relative to the Shared Documents folder. For example, to ingest
     files from the folder `Shared%20Documents/user_manuals/cars`, enter `user_manuals/cars`.

   Note

   To change the fetch file source at a later time, you must reinstall the connector.
2. Click **Validate** to start the process of validating source, which can take several minutes.
3. After your connector is successfully configured, click **Ingest files** to begin data ingestion.

## Next step

Once your connector is set up, continue on to [Query the Cortex Search service with Snowflake Connector for SharePoint](/connectors/unstructured-data-connectors/sharepoint/cortex).
