# SnowConvert AI: Deployment

SnowConvert AI, as part of the end-to-end migration experience, offers the option to deploy converted database objects directly to your Snowflake environment. With this deployment feature, you can review conversion results, authenticate to Snowflake, and deploy selected objects with their proper dependencies and execution order. This deployment feature is available for SQL Server and Amazon Redshift databases.

## Conversion status indicators

Before deployment, SnowConvert AI provides visual indicators to help you understand the conversion status of each object:

### Ready for Deployment

Objects that have been successfully converted and are ready for deployment without any issues.

### Functional Data Model (FDM) Warnings

Objects with FDMs have been found in the conversion. It is recommended to review these before deployment, though they can still be deployed.

### Equivalent Work Item (EWI) Errors

Objects with EWIs have critical issues that must be fixed before deployment. These objects cannot be deployed until the issues are resolved.

Note

For detailed information about FDMs and EWIs, please refer to the [SnowConvert AI Technical Documentation](../technical-documentation/README).

## Supported authentication methods

The deployment process supports two authentication methods to connect to your Snowflake environment:

### SSO (Single Sign-On)

Allows authentication using your organization’s Single Sign-On provider configured with Snowflake. This method provides seamless integration with your existing identity management system.

### Standard authentication

Traditional username and password authentication with the following security requirements:

- Multi-factor authentication (MFA) must be enabled for your Snowflake account
- Follows Snowflake’s security best practices and recommendations

Note

The account identifier must use **-** for separation instead of **.** (for example, **orgname-account-name**).

Warning

Ensure that you follow [Snowflake’s security recommendations](https://community.snowflake.com/s/article/Snowflake-Security-Overview-and-Best-Practices) and have [multi-factor authentication (MFA)](https://docs.snowflake.com/en/user-guide/ui-snowsight-profile.html#label-snowsight-set-up-mfa) enabled.

## Deployment execution order

The deployment process executes database objects in a specific order to maintain proper dependencies:

1. **Databases**: Created first to establish the container structure.
2. **Schemas**: Created within databases to organize objects.
3. **Tables**: Created to establish data structures.
4. **Views**: Created after tables because they depend on table structures.
5. **Functions**: Deployed to provide reusable logic.
6. **Stored Procedures**: Deployed last as they may reference other objects.

## Deploy converted database objects to Snowflake

You can deploy your converted database objects to Snowflake. After deployment, you can proceed with data migration
to complete the end-to-end migration process.

Ensure that you meet the following prerequisites before deploying converted objects:

- You completed conversion process with objects ready for deployment.
- You have a valid Snowflake account with appropriate permissions.
- You have multi-factor authentication (MFA) enabled (for Standard authentication).

Complete the following steps to deploy converted objects:

1. In SnowConvert AI, open the project, and then select **Deploy code**.
2. On the **Connect to Snowflake** page, complete the fields with your connection information, and then select **Sign in**.

   The **Select objects to deploy** page appears. The following image is an example of the page:

   [![](/static/images/migrations/sc-assets/deploy-objects.png "Select objects to deploy")](/static/images/migrations/sc-assets/deploy-objects.png)
3. Review the conversion status and resolve any errors before proceeding.

   Examine the status indicators for each object in your project. Resolve any EWI errors before proceeding.
4. Select the objects that you want to deploy to Snowflake.

   Only select objects with successful conversion status or acceptable FDM warnings.

Note

If you make changes to object files, you can refresh the conversion status by selecting **Refresh files**.

5. Select **Deploy**.

   The deployment process starts. Objects are deployed automatically, in the proper dependency order. When deployment
   finishes, the **Deployment results** window appears.
6. In **Deployment results**, review the results for success confirmations or error messages.

   The following image is an example of a **Deployment results** window:

   [![](/static/images/migrations/sc-assets/deploying-results.png "Deployment Results")](/static/images/migrations/sc-assets/deploying-results.png)

Note

Only successfully converted objects are available for deployment. You must resolve objects with EWI errors before you can deploy them.

After completing the deployment process, your database objects are available in your Snowflake environment. You can then proceed
with [data migration](./data-migration) to transfer your data to complete the full migration process and make everything ready for use in your
applications and workflows.
