# SAP® Snowflake

This topic describes the steps to configure an instance for SAP® Snowflake for SAP customers without an existing Snowflake account.

Note

The SAP® Snowflake account provisioned is the Business Critical edition.

SAP® BDC Connect for Snowflake is not available for Snowflake trial accounts. To request a SAP®
Snowflake trial, please contact your SAP account executive, who can submit the request for trial
through SAP’s internal process for enterprise trials.

As an SAP® administrator, perform the following steps:

1. Sign in to [SAP for Me](https://me.sap.com/) with an S-user ID or login name.
2. From the sidebar menu, choose **Portfolio & products**.
3. In the **My Product Packages** tab, select the **SAP Business Data Cloud** product.
4. Select the **Applications** tab and in the **SAP Snowflake** card, click **Start Provisioning**.   
   The **Provision SAP® Snowflake** wizard dialog displays and guides you through the provisioning process.
5. In the Provision SAP® Snowflake dialog, configure the following parameters and click **Next**:

   - **Entitlement System**: Displays the ID of the SAP® Business Data Cloud Entitlement set. Cannot be changed.
   - **Name**: Enter an appropriate name for the SAP solution.
   - **Path**: Select or create a resource group under which to group the solution
     components provisioned for SAP® Business Data Cloud.
     Create it in the same location selected for the SAP® Business Data Cloud cockpit system.
   - **Business Type**: Preset to Production.
6. In the **Select Application** step, SAP Snowflake is pre-selected.   
   The **Configure Parameters** step displays.
7. In the **Configure Parameters** step, configure the following parameters and click **Next**:

   - **Region**: Choose an available region in the [SAP for Me](https://me.sap.com/) portal.
     Snowflake recommends choosing the same region as the SAP® Business Data Cloud core for optimal performance.
   - **Admin email**: Provide the email address of the user to be defined as the administrator of your SAP Snowflake system.
     This user is responsible for adding additional users and for further configuration.
   - **Admin First Name**: The first name of the administrator of your SAP Snowflake system.
   - **Admin Last Name**: The last name of the administrator of your SAP Snowflake system.

   Provisioning begins and SAP® notifies you that a provisioning request was sent to the specified owner’s e-mail address.
8. Click **View in Resources** to view the tenant within the indicated resource group.
   The **Resources** tab shows the current solution status, which should be `Processing`.
9. Select the tenant below the new solution and click **Details** to view the details of the tenant.
10. On top of the **details** view of the tenant, choose the **View Details** link.

A pop-up window opens that provides an activation link to the SAP Snowflake account.
If you are the SAP Snowflake system owner, select this link and complete the activation flow
in SAP Snowflake (see [Activating the SAP Snowflake Account](https://help.sap.com/docs/business-data-cloud/introducing-sap-snowflake/introducing-sap-snowflake)).

If not, share the activation link with the SAP Snowflake owner and ask them to complete the activation flow.

11. After the account has been activated in SAP for Me, the status for your SAP
    Snowflake solution and tenant changes to `Ready`. In the details view of the SAP
    Snowflake tenant, in the Path field, select the URL to open SAP Snowflake and log in.

## Next steps

The SAP® BDC admin may provision as many SAP® Snowflake accounts as they need with unique account names to help distinguish them.
Every SAP® Snowflake account will need to be activated as described in the note below.

After activation, the SAP® Snowflake is ready for you to share Data Products from SAP® BDC to
SAP® Snowflake. As part of the provisioning process, a Zerocopy Connector called
`DEFAULT_SAP_BDC_CONNECTOR` is automatically created under the `CONNECTORS.ZEROCOPY` schema
and enrolled with SAP® Business Data Cloud in the SAP® Snowflake account. You are ready to share
data products from SAP® BDC and consume them in SAP® Snowflake. For more information,
see [Explore Data Products from SAP® BDC Connect for Snowflake](/user-guide/data-integration/zero-copy/sap-sql/explore-data-products).

Customers can create additional Zerocopy Connectors in the same SAP® Snowflake account and enroll
them with the same or different SAP® Business Data Cloud tenant. Each Zerocopy Connector requires a
new Invitation Link that can be obtained from [SAP for Me](https://me.sap.com/). Each Invitation
Link can be enrolled only once with SAP® Business Data Cloud.

Note

Customers can view the status of provisioning in the **Details** view.
After provisioning is complete, the customer can click the Snowflake activation link available in the Details view to activate their SAP® Snowflake account, login, change their username and reset their password, setup MFA, and perform other operations.
