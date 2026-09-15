# About the Snowflake Connector for Microsoft Power Platform

This topic describes how to connect to Snowflake from Microsoft Power Platform by adding Snowflake as a data connection.

When connected, you can use your Snowflake data from the following platforms:

- Power Apps: Build applications that can read from and write to Snowflake .
- Power Automate: Build flows and add actions that enable executing custom SQL and get back the results.
- Copilot Studio: Build custom agents using your Snowflake data as a knowledge source.
- Logic Apps: Build and run automated workflows in, across, and outside the software ecosystems in your enterprise or organization.

The Microsoft Power Platform helps you create flows and add actions to execute and get back results of custom SQL statements with the Snowflake connection.

## Supported capabilities for Power Apps

- Users should first create virtual tables and then load them into apps with the Snowflake connection.

  To learn how to create virtual tables, see
  [Create and edit virtual tables with Microsoft Dataverse - Power Apps](https://learn.microsoft.com/power-apps/maker/data-platform/create-edit-virtual-entities).

## Virtual Network support

With Azure Virtual Network support for Power Platform, users can integrate Power Platform with resources
inside their virtual network without exposing them over the public internet.

To connect to Virtual Network, please make sure to follow both steps mentioned below.

1. Learn how to setup [Azure Private Link and Snowflake](/user-guide/privatelink-azure).
2. Learn how to setup [Virtual Network support for Power Platform](https://learn.microsoft.com/power-platform/admin/vnet-support-setup-configure).
   To learn more about Azure Virtual Network, see [Virtual Network support overview](https://learn.microsoft.com/power-platform/admin/vnet-support-overview).

## Prerequisites

- Users must have a Snowflake account.
- Users must have Microsoft Entra ID for the external authorization.
  The authorization flow for PowerApps supports Service-Principal; however, Power Automate supports both Service-Principal and on-behalf-of-user flows.
- Users must have a premium Power Apps license.

## Known issues and limitations

1. A Snowflake table needs to have a Primary or Unique Key (integer data type only), and at least one additional column.
2. We currently do not support duplicate columns when the `join` command is executed. A workaround would be to add aliases to the duplicated columns.
3. Other limitations with Virtual Tables are listed [here](https://learn.microsoft.com/power-apps/maker/data-platform/create-edit-virtual-entities#considerations-when-you-use-virtual-tables) .
4. Virtual tables are only supported with connections created with ‘Service Principal’ authentication.
5. When using Service Principle authentication, the user needs to have read access to the **information\_schema.columns** table.
6. Snowflake connections cannot be created directly in Canvas apps. Error information and steps needed to resolve the issue are as follows:
   1. An error will show if the Snowflake connection is created directly in a Canvas app as shown below.

      ![](/static/images/connectors/adding-connection-canvasapp-error.png)
   2. Rather than adding the connector directly in the Canvas app,
      create a service principal connection (not delegated) from outside of the Canvas app.
      Use the Snowflake connection created above and create a virtual table.

      ![](/static/images/connectors/create-virtualtable.png)
   3. Afterwards, the virtual table can be loaded in the Canvas app, and builds out of the Canvas app can proceed as normal.

      ![](/static/images/connectors/load-virtualtable.png)

      Note

      The `ANIMALS` table above is a virtual table, created using the Snowflake Connection as previously described in [Install and configure Snowflake Connector for Snowflake Connector for Microsoft Power Platform](/connectors/microsoft/powerapps/tasks).

## Considerations

Consider the following when using the Snowflake connector with Microsoft Power Platform:

- The authorization server can grant the OAuth client an access token on behalf of the user, referred to as *DELEGATED BASED AUTH*.
- The authorization server can grant the OAuth client an access token for the OAuth client itself, referred to as *SP BASED AUTH*.
- When creating a security integration, describe the integration created and
  determine if the role given to the Snowflake user is in the blocked list.

  If in the blocked list, than either change or remove the role of the user in the blocked list.

  ![](/static/images/connectors/blocked-list.png)
- Ensure that the *login\_name* and roles are correctly set in Snowflake.

  To verify login names, open a browser to Snowsight. In the navigation menu, select **Governance & security** » **Users & roles**.
  Select a user and edit as required.
- Snowflake account details (warehouse, role, schema, database) are case-sensitive and must match exactly as they are in the Snowflake account when configuring the connection.
- For Delegated and Service Principal based connections, please create a Power Automate flow to validate the connection.

## Customers using Snowflake Connector [DEPRECATED]

- Applicable: All regions
- This option is only for older connections without an explicit authentication type and is only provided for backward compatibility.
- To migrate from an older Snowflake connector to the new one, please follow the steps below.
  1. Power Automate flows and Power Apps using older connections will need to be updated by changing to the new connection.
  2. Power Automate flow action “Convert result set rows from array to objects” would also need to be dropped as that functionality is now wrapped in “Check the Status and Get Results”.

### Next steps

After reviewing this page, review the current set of [installation tasks](/connectors/microsoft/powerapps/tasks).
