# SAP® BDC Connect for Snowflake

This topic describes the steps to set up an SAP® Business Data Cloud connection for use with an existing Snowflake account.

Note

The Snowflake account must be Standard, Enterprise, or Business Critical edition and must be on
AWS commercial or Azure commercial in a supported region as described in
[Supported Cloud Regions](/user-guide/intro-regions).

For more information, see [Provisioning SAP Business Data Cloud Connect](https://help.sap.com/docs/business-data-cloud/administering-sap-business-data-cloud/provision-sap-business-data-cloud-connector-for-supported-external-systems).

As an SAP® administrator, perform the following steps:

1. Obtain your Snowflake account URL and ensure it follows the format
   `https://orgName-accountName.snowflakecomputing.com`.
   Which should be all lowercase and replace \_ (underscore) with - (dash) for RFC compliance.
2. Provision SAP Business Data Cloud Connect as documented here: [Provisioning SAP Business Data Cloud Connect](https://help.sap.com/docs/business-data-cloud/administering-sap-business-data-cloud/provision-sap-business-data-cloud-connector-for-supported-external-systems).
3. Follow steps 1-5 in the wizard
4. In wizard step 6: Configure Parameters:

   - **External System Instance Identifier**: Enter your Snowflake account URL:
     `https://orgName-accountName.snowflakecomputing.com`
   - **Region**: Select the same region that you used for enabling SAP Business Data Cloud Core.
5. Complete wizard steps 7 and 8.
6. In step 9: Hover over the **View Tenant Notifications** button.
   A pop-up window opens with an **Invitation Link** that can be used to complete the configuration in Snowflake.
7. Copy the Invitation Link
8. Log in to your Snowflake account to complete the remainder of the configuration
   to create a Zerocopy Connector as described in [Set Up SAP® BDC Connect for Snowflake Zerocopy Connector](/user-guide/data-integration/zero-copy/sap-sql/setup).

## Next steps

In your [SAP for Me](https://me.sap.com/) environment, choose the Customer Landscape tab and, under the Formations tab, choose Include Systems to add the SAP BDC Connect instance to an existing formation.

Customers can create additional Zerocopy Connectors in the same Snowflake account and enroll them with the same or
different SAP® Business Data Cloud tenant. Each Zerocopy Connector requires a
new **Invitation Link** that can be obtained from [SAP for Me](https://me.sap.com/).
Each **Invitation Link** can be enrolled only once with SAP® Business Data Cloud.

Note

To create a new formation, see [Creating SAP Business Data Cloud Formations](https://help.sap.com/docs/business-data-cloud/administering-sap-business-data-cloud/integrate-sap-business-data-cloud-provisioned-systems?locale=en-US&state=PRODUCTION&version=SHIP).
