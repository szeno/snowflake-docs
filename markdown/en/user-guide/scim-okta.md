# Okta SCIM integration with Snowflake

This guide provides the steps required to configure Provisioning in Okta for Snowflake, and includes the following sections:

## Features

User and Role Administration is supported for the Snowflake application.

This enables Okta to:

- Manage the user lifecycle (i.e. create, update, and delete) in Snowflake.
- Manage the role lifecycle (i.e. create, update, and delete) in Snowflake.
- Manage user to role assignments in Snowflake.

The following provisioning features are supported:

Push New Users:
:   New users created through OKTA are also created in Snowflake. You can use the `allowedInterfaces` custom attribute to prevent a provisioned user from using certain interfaces to access Snowflake.

Push Profile Updates:
:   Updates made to the user’s profile through OKTA will be pushed to Snowflake.

Push User Deactivation:
:   Deactivating the user or disabling the user’s access to Snowflake through OKTA will deactivate the user in Snowflake.

    Note

    For Snowflake, deactivating a user means setting the `DISABLED` property for the user to `TRUE`.

Reactivate Users:
:   User accounts can be reactivated Snowflake.

Sync Password:
:   User password can be pushed from Okta into Snowflake, if required.

    Tip

    The default setting is to create a random password for users giving the user an attribute setting of `has_Password=true`. Without a password, users must access Snowflake through Okta SSO. To prevent a password being generated for users, turn this setting off before provisioning users as follows:

    1. Click **Edit**.
    2. Under **Sync Password**, uncheck the setting **Generate a new random password whenever the user’s Okta password changes**.
    3. Save the change.

    Enabling this setting in Okta creates a password for the user to access Snowflake. This could result in a pathway for users to access Snowflake without SSO.

    To disable password synchronization, unset this option in Okta and update the Snowflake Okta SCIM
    [security integration](/sql-reference/sql/alter-security-integration-scim) to set the `SYNC_PASSWORD` property to
    `False`.

Push Groups:
:   The Push Groups feature creates roles in Snowflake and facilitates role management. The roles created in Snowflake using Okta Push Groups have the same names in Okta and Snowflake. Always create roles in Okta first and use Push Groups to update Snowflake to ensure Okta and Snowflake can synchronize. Okta and the [OKTA\_PROVISIONER](#label-scim-okta-snowflake-configuration) custom role in Snowflake cannot manage manually created roles in Snowflake. Push Groups do not create users in Snowflake.

    Tip

    Okta can create users in Snowflake if the Snowflake application in Okta is assigned to a user in Okta.

    For more information, see [Assign an application to a user](https://help.okta.com/en/prod/Content/Topics/Provisioning/lcm/lcm-assign-app-user.htm).

### Known issues

- Okta does not support URLs that contain underscores. If the name of the Snowflake account contains an underscore, then you need to use
  a special account URL that replaces the underscore with a hyphen. For example, if you are using the account name URL format, the special
  URL might be `https://myorg-account-name.snowflakecomputing.com`.
- Existing Snowflake roles cannot be brought under Okta’s management through transfer of ownership. Only new roles can be created through Okta.
- Existing Snowflake users can be brought under Okta’s management through a transfer of ownership. For more information, see [Troubleshooting](#troubleshooting) (in this topic).

### Limitations

- Snowflake supports a maximum of 500 concurrent requests per account per SCIM endpoint (e.g. the `/Users` endpoint, the `/Groups` endpoint). After your account exceeds this threshold, Snowflake returns a `429` HTTP status code (i.e. too many requests). Note that this request limit usually only occurs during the initial provisioning when relatively large numbers of requests (i.e. more than 10 thousand) occur to provision users or groups.

### Not supported

- Okta’s [Enhanced Group Push](https://help.okta.com/en/prod/Content/Topics/users-groups-profiles/usgp-enable-group-push.htm) and Push Now features.

  Note

  The `defaultRole`, `defaultSecondaryRoles`, and `defaultWarehouse` attributes are unmapped as they are optional. To map these attributes in Okta, use profiles, expressions, or set a default value for all users. For more information, see [Manage profiles (in Okta)](https://help.okta.com/en/prod/Content/Topics/users-groups-profiles/usgp-user-profiles-main.htm).
- If you are using private connectivity to the Snowflake service to access Snowflake, ensure that you are not entering these URLs in the
  integration settings. Enter the public endpoint (i.e. without `.privatelink`), and ensure that the network policy allows access
  from the Okta IP address listed [here](https://help.okta.com/en-us/Content/Topics/Security/ip-address-allow-listing.htm), otherwise you
  cannot use this integration.
- Okta does not currently support importing Active Directory [nested groups](https://help.okta.com/en/prod/Content/Topics/Directory/ad-agent-import-groups.htm). Therefore, if your Okta integration uses nested groups in AD, you cannot use the Snowflake Okta SCIM integration to provision or manage nested groups in Snowflake. Please contact Okta and Microsoft to request the support of nested groups.

## Prerequisites

1. Before provisioning users or groups, ensure that the [network policy](/user-guide/network-policies) in Snowflake allows access
   from Okta’s IP addresses documented [here](https://help.okta.com/en-us/Content/Topics/Security/ip-address-allow-listing.htm). For more
   information, see [Managing SCIM Network Policies](#managing-scim-network-policies).
2. Before you configure provisioning for Snowflake, make sure you have configured the **General Settings** and any **Sign-On Options** for the Snowflake application in Okta.

Once the above steps are complete, click **Next** in Okta to take you back to the **Provisioning** tab.

## Configuration steps

The configuration process requires completing steps in Snowflake and in Okta.

### Snowflake configuration

The Snowflake configuration process creates a SCIM security integration to allow users and roles created in Okta to be owned by the OKTA\_PROVISIONER SCIM role in Snowflake.

Execute the following SQL statements in your preferred Snowflake client. Each of the SQL statements is explained below.

Copy code

```
use role accountadmin;
create role if not exists okta_provisioner;
grant create user on account to role okta_provisioner;
grant create role on account to role okta_provisioner;
grant role okta_provisioner to role accountadmin;
create or replace security integration okta_provisioning
    type = scim
    scim_client = 'okta'
    run_as_role = 'OKTA_PROVISIONER';
```

Important

The example SQL statements use the ACCOUNTADMIN system role and the OKTA\_PROVISIONER custom role is granted to the ACCOUNTADMIN role.

It is possible not to use the ACCOUNTADMIN role in favor of a less-privileged role. Using a less-privileged role can help to address compliance concerns relating to least-privileged access, however, using a less-privileged role can result in unexpected errors during the SCIM configuration and management process.

These errors could be the result of the less-privileged role not having sufficient rights to manage all of the roles through SCIM due to how the roles are created and the resultant role hierarchy. Therefore, in an effort to avoid errors in the configuration and management processes, choose one of the following options:

1. Use the ACCOUNTADMIN role as shown in the example SQL statements.
2. Use a role with the global MANAGE GRANTS privilege.
3. If neither of these first two options are desirable, use a custom role that has the OWNERSHIP privilege on all of the roles that will be managed using SCIM.

1. Use the ACCOUNTADMIN role.

   Copy code

   ```
   use role accountadmin;
   ```
2. Create the custom role OKTA\_PROVISIONER. All users and roles in Snowflake created by Okta will be owned by the scoped down OKTA\_PROVISIONER role.

   Copy code

   ```
   create role if not exists okta_provisioner;
   grant create user on account to role okta_provisioner;
   grant create role on account to role okta_provisioner;
   ```
3. Let the ACCOUNTADMIN role create the security integration using the OKTA\_PROVISIONER custom role. For more information, see [CREATE SECURITY INTEGRATION](/sql-reference/sql/create-security-integration-scim).

   Copy code

   ```
   grant role okta_provisioner to role accountadmin;
   create or replace security integration okta_provisioning
    type = scim
    scim_client = 'okta'
    run_as_role = 'OKTA_PROVISIONER';
   ```

After creating the security integration, set up authentication for your SCIM requests. For more information, see [Authenticating SCIM API requests](/user-guide/scim-authentication).

Important

All users and roles in Snowflake created by Okta will be owned by the scoped down `okta_provisioner` role.

If you want to manage existing Snowflake users through Okta, complete the following steps:

1. Transfer ownership of existing users to the okta\_provisioner role.

   Copy code

   ```
   use role accountadmin;
   grant ownership on user <user_name> to role okta_provisioner;
   ```
2. Ensure the `login_name` property is set for existing users, which should already be set if these existing Snowflake users are using Okta SSO.
3. Be advised that the name for existing users brought under Okta’s management will be updated to match with Okta’s username. Inform your users about this change as they might be using the name to connect to Snowflake from other integrations (for example, Tableau).

### Okta configuration

This section discusses how to create and configure a Snowflake application in Okta.

Note

When creating the Snowflake application in Okta, the **SubDomain** field for the application must contain the
[account identifier](/user-guide/admin-account-identifier) of your Snowflake account. If the Snowflake account name contains an
underscore and you are using the account name format of the identifier, you must convert the underscore to a hyphen because Okta does
not support underscores in URLs (e.g. `myorg-account-name`).

Do not include a `privatelink` segment in the **SubDomain** field because private connectivity is
[not supported](#label-scim-okta-not-supported) and entering this segment causes the SCIM connection to fail.

To configure the Snowflake application in Okta, complete the following steps.

1. In **Settings**, select **Integration** from the left hand menu and then check the **Enable API Integration** box.
2. For **API Token**, enter the value generated above from the clipboard. Click **Test API Credentials** button, and, if successful, save the configuration.
3. Select **To App** from the left hand menu.
4. Select the **Provisioning Features** you want to enable.
5. Verify the Attribute Mappings. The `defaultRole`, `defaultSecondaryRoles`, and `defaultWarehouse` attributes are unmapped as they are optional. If there’s a need, you can map them using Okta profile or expression or set the same value for all users.

You can now assign users to the Snowflake application (if needed) and finish the application setup.

Note

Okta supports an attribute called `snowflakeUserName` which maps to the `name` field of the Snowflake user.

If you want the `name` and `login_name` fields for the Snowflake user to have different values, follow this procedure.

1. Enable separate mappings for your account by running:

   Copy code

   ```
   ALTER ACCOUNT SET MAP_SCIM_USERNAME_TO_ENTERPRISE_ATTR = TRUE;
   ```

   When this parameter is enabled, all SCIM POST and PUT requests must include the `snowflakeUserName` attribute in the
   enterprise extension schema. Requests that omit this attribute will fail.

   For more information, see [MAP\_SCIM\_USERNAME\_TO\_ENTERPRISE\_ATTR](/sql-reference/parameters#label-map-scim-username-to-enterprise-attr).
2. In Okta, access the Snowflake application and navigate to **Provisioning** > **Attribute Mappings** > **Edit Mappings**.
3. Search for the attribute `snowflakeUserName`.
4. If the attribute is not found, the Snowflake application was created prior to this attribute being available. Recreate the Snowflake application with the mappings shown below or add the attribute manually as follows:

   - Click **Add Attribute**.
   - Set the following values for each of the listed fields in the table.

   | Field | Value |
   | --- | --- |
   | Data type | string |
   | Display name | Snowflake Username |
   | Variable name | `snowflakeUserName` |
   | External name | `snowflakeUserName` |
   | External namespace | `urn:ietf:params:scim:schemas:extension:enterprise:2.0:User` |
   | Description | Maps to the `name` field of the user in Snowflake. |
   | Scope | User personal |

   Expand

   Show lessSee more
5. Click **Save**.

# Enabling Snowflake-initiated SSO

The SCIM provisioning process does not automatically enable single sign-on (SSO).

To use SSO after the SCIM provisioning process is complete, enable
[Snowflake-initiated SSO](/user-guide/admin-security-fed-auth-security-integration).

## Managing SCIM network policies

Applying a network policy to a SCIM security integration allows the SCIM network policy to be distinct from network policies that apply to the entire Snowflake account.
It allows the SCIM provider to provision users and groups without adding IP addresses to a network policy that controls access for normal users.

A network policy applied to a SCIM integration overrides a network policy applied to the entire Snowflake account.

After creating the SCIM security integration, create the SCIM network policy using this command:

> Copy code
>
> ```
> alter security integration okta_provisioning set network_policy = <scim_network_policy>;
> ```

To unset the SCIM network policy, use this command:

> Copy code
>
> ```
> alter security integration okta_provisioning unset network_policy;
> ```

Where:

`okta_provisioning`
:   Specifies the name of the Okta SCIM security integration.

`scim_network_policy`
:   Specifies the Okta SCIM network policy in Snowflake.

For more information, see [Controlling network traffic with network policies](/user-guide/network-policies) and [ALTER SECURITY INTEGRATION](/sql-reference/sql/alter-security-integration-scim).

## Using secondary roles with SCIM

Snowflake supports setting the [user](/sql-reference/sql/create-user) property `DEFAULT_SECONDARY_ROLES` to `'ALL'` with
SCIM to allow users to use [secondary roles](/user-guide/security-access-control-overview#label-access-control-role-enforcement) in a Snowflake session.

For a representative example, see [Update a user](/user-guide/scim-user-api-reference#label-scim-put-users).

## Populating Snowflake tags with SCIM integrations

You can populate tags by using the `snowflakeTags` attribute when you ingest user information into the SCIM security integration. The exact request input can be found in [Create a user](/user-guide/scim-user-api-reference#label-scim-create-a-user).

For more information about adding custom attributes to an Okta user profile, see the [Okta documentation](https://help.okta.com/en-us/content/topics/users-groups-profiles/usgp-add-custom-user-attributes.htm)

To enable support for this feature:

- Create the tag before you run the SCIM integration.
- Grant proper privileges on each tag and tag schema to the OKTA\_PROVISIONER role.

Here is an example of creating a tag and assigning the proper role privileges:

Copy code

```
-- Create the tag.
CREATE TAG my_database_name.my_schema_name.my_tag_name;

-- Assign the proper privileges to the SCIM integration.
GRANT USAGE ON SCHEMA my_database_name.my_schema_name TO ROLE OKTA_PROVISIONER;
GRANT APPLY ON TAG my_database_name.my_schema_name.my_tag_name TO ROLE OKTA_PROVISIONER;
```

You must grant USAGE ON SCHEMA and APPLY ON TAG to all tags and tag schemas that you plan to assign through your SCIM security integration.

## Replicating the Okta SCIM security integration

Snowflake supports replication and failover/failback with the SCIM security integration from the source account to the target account.

For details, see [Replication of security integrations & network policies across multiple accounts](/user-guide/account-replication-security-integrations).

## Troubleshooting

- **Transferring ownership.** If the user update fails, check the ownership of the user in Snowflake. If it is not owned by the `okta_provisioner` role (or the role set in the `run_as_role` parameter when creating the security integration in Snowflake), then the update will fail. Transfer the ownership by running the following SQL statement in Snowflake and try again.

  Copy code

  ```
  grant ownership on user <username> to role OKTA_PROVISIONER;
  ```
- Ensure `login_name` property is set for existing users which should already be set if these existing Snowflake users are using Okta SSO.
- To verify that Okta is sending updates to Snowflake, check the log events in Okta for the Snowflake application and the SCIM audit logs in Snowflake to ensure Snowflake is receiving updates from Okta. Use the following to query the Snowflake SCIM audit logs.

  Copy code

  ```
  USE ROLE ACCOUNTADMIN;
  USE SCHEMA snowflake.information_schema;

  SELECT * FROM TABLE(REST_EVENT_HISTORY('scim'));

  SELECT *
    FROM TABLE(REST_EVENT_HISTORY(
    'scim',
    DATEADD('MINUTES',-5,CURRENT_TIMESTAMP()),
    CURRENT_TIMESTAMP(),
    200))
    ORDER BY event_timestamp;
  ```
- It is possible that an authentication error may occur during the provisioning process. One possible error message is as follows:

  Copy code

  ```
  Error authenticating: Forbidden. Errors reported by remote server: Invalid JSON: Unexpected character ('<' (code 60)): expected a valid value (number, String, array, object, 'true', 'false' or 'null') at [Source: java.io.StringReader@4c76ba04; line: 1, column: 2]
  ```

  If this error message or other authentication error messages occur, try this troubleshooting procedure:

  1. In Okta, remove the current Snowflake application and create a new Snowflake application.
  2. In Snowflake, create a new SCIM security integration and generate a new access token.
  3. Copy the new token by clicking **Copy**.
  4. In Okta, paste and verify the new access token as described in how to configure Okta as a SCIM identity provider.
  5. Provision users and roles from Okta to Snowflake using the new Snowflake application in Okta.

**Next topics:**

- [Authenticating SCIM API requests](/user-guide/scim-authentication)
- [SCIM API requests](/user-guide/scim-api-references)
