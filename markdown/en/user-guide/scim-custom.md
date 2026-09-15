# Custom SCIM integration with Snowflake

Custom SCIM integrations allow users to build their own applications to interface with their identity provider to provision, map, and manage users and roles to Snowflake.

Currently, Custom SCIM integrations are supported for identity providers that are neither Okta nor Microsoft Entra ID.

After creating your SCIM application, follow the procedure below to create a Snowflake security integration. For information about
authenticating SCIM API requests, see [Authenticating SCIM API requests](/user-guide/scim-authentication).

## Limitations

- Snowflake supports a maximum of 500 concurrent requests per account per SCIM endpoint (e.g. the `/Users` endpoint, the `/Groups` endpoint). After your account exceeds this threshold, Snowflake returns a `429` HTTP status code (i.e. too many requests). Note that this request limit usually only occurs during the initial provisioning when relatively large numbers of requests (i.e. more than 10 thousand) occur to provision users or groups.
- If your Snowflake [account URL](/user-guide/admin-account-identifier) was created with underscores, you can access your Snowflake
  account with the account URL having underscores or hyphens.

  If your SCIM provider reuses the same account URL for both SAML SSO and SCIM, then URLs with underscores are not supported. Therefore,
  use the hyphenated account URL to configure SCIM.

  Snowflake account URLs that do not contain underscores are not restricted by this limitation.
- A custom SCIM integration may or may not allow the provisioning and management of nested groups. Before attempting to use a custom SCIM integration to provision nested groups in Snowflake, please contact your identity provider to determine whether nested groups can be used with a SCIM integration.
- If you are using private connectivity to the Snowflake service to access Snowflake, ensure that you are not entering these URLs in the
  integration settings. Enter the public endpoint (i.e. without `.privatelink`), and ensure that the network policy allows access
  from the IdP IP address, otherwise you cannot use this integration.

  - Note that if your IdP and Snowflake account are both hosted in Microsoft Azure, it is necessary that the [network policy](/user-guide/network-policies) in Snowflake allows access from all of the Microsoft Azure IP addresses for the [Public Cloud](https://www.microsoft.com/en-us/download/details.aspx?id=56519) or the [US Government Cloud](https://www.microsoft.com/en-us/download/details.aspx?id=57063). Currently, all Microsoft Azure IP addresses are required in the network policy. For more information, see [Managing SCIM Network Policies](#managing-scim-network-policies).
- Enabling or disabling password synchronization from a custom identity provider to Snowflake.

  Setting the `SYNC_PASSWORD` property in the Snowflake security integration is only supported for Okta SCIM integrations.

## Prerequisites

Before provisioning users or groups, ensure that the [network policy](/user-guide/network-policies) in Snowflake allows access from the IP ranges that correspond to your organization. For more information, see [Managing SCIM Network Policies](#managing-scim-network-policies).

## Create a custom SCIM security integration

The Snowflake configuration process creates a SCIM security integration to allow users and roles created in the identity provider to be owned by the GENERIC\_SCIM\_PROVISIONER SCIM role in Snowflake.

Execute the following SQL statements in your preferred Snowflake client. Each of the following statements is explained below.

Copy code

```
use role accountadmin;
create role if not exists generic_scim_provisioner;
grant create user on account to role generic_scim_provisioner;
grant create role on account to role generic_scim_provisioner;
grant role generic_scim_provisioner to role accountadmin;
create or replace security integration generic_scim_provisioning
    type=scim
    scim_client='generic'
    run_as_role='GENERIC_SCIM_PROVISIONER';
```

Important

The example SQL statements use the ACCOUNTADMIN system role and the GENERIC\_SCIM\_PROVISIONER custom role is granted to the ACCOUNTADMIN role.

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
2. Create the custom role GENERIC\_SCIM\_PROVISIONER. All users and roles in Snowflake created by the IdP will be owned by the scoped down GENERIC\_SCIM\_PROVISIONER role.

   Copy code

   ```
   create role if not exists generic_scim_provisioner;
   grant create user on account to role generic_scim_provisioner;
   grant create role on account to role generic_scim_provisioner;
   ```
3. Let the ACCOUNTADMIN role create the security integration using the GENERIC\_SCIM\_PROVISIONER custom role. For more information, see [CREATE SECURITY INTEGRATION](/sql-reference/sql/create-security-integration-scim).

   Copy code

   ```
   grant role generic_scim_provisioner to role accountadmin;
   create or replace security integration generic_scim_provisioning
    type = scim
    scim_client = 'generic'
    run_as_role = 'GENERIC_SCIM_PROVISIONER';
   ```

After creating the security integration, set up authentication for your SCIM requests. For more information, see [Authenticating SCIM API requests](/user-guide/scim-authentication).

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
> alter security integration generic_scim_provisioning set network_policy = <scim_network_policy>;
> ```

To unset the SCIM network policy, use this command:

> Copy code
>
> ```
> alter security integration generic_scim_provisioning unset network_policy;
> ```

Where:

`generic_scim_provisioning`
:   Specifies the name of the Custom SCIM security integration.

`scim_network_policy`
:   Specifies the Custom SCIM network policy in Snowflake.

For more information, see [Controlling network traffic with network policies](/user-guide/network-policies) and [ALTER SECURITY INTEGRATION](/sql-reference/sql/alter-security-integration-scim).

## Using secondary roles with SCIM

Snowflake supports setting the [user](/sql-reference/sql/create-user) property `DEFAULT_SECONDARY_ROLES` to `'ALL'` with
SCIM to allow users to use [secondary roles](/user-guide/security-access-control-overview#label-access-control-role-enforcement) in a Snowflake session.

For a representative example, see [Update a user](/user-guide/scim-user-api-reference#label-scim-put-users).

## Populating Snowflake tags with SCIM integrations

You can populate tags by using the `snowflakeTags` attribute when you ingest user information into the SCIM security integration. The exact request input can be found in [Create a user](/user-guide/scim-user-api-reference#label-scim-create-a-user).

To enable support for this feature:

- Create the tag before you run the SCIM integration.
- Grant proper privileges on each tag and tag schema to the GENERIC\_SCIM\_PROVISIONER role.

Here is an example of creating a tag and assigning the proper role privileges:

Copy code

```
-- Create the tag.
CREATE TAG my_database_name.my_schema_name.my_tag_name;

-- Assign the proper privileges to the SCIM integration.
GRANT USAGE ON SCHEMA my_database_name.my_schema_name TO ROLE GENERIC_SCIM_PROVISIONER;
GRANT APPLY ON TAG my_database_name.my_schema_name.my_tag_name TO ROLE GENERIC_SCIM_PROVISIONER;
```

You must grant USAGE ON SCHEMA and APPLY ON TAG to all tags and tag schemas that you plan to assign through your SCIM security integration.

## Replicating the custom SCIM security integration

Snowflake supports replication and failover/failback with the SCIM security integration from the source account to the target account.

For details, see [Replication of security integrations & network policies across multiple accounts](/user-guide/account-replication-security-integrations).

**Next topics:**

- [Authenticating SCIM API requests](/user-guide/scim-authentication)
- [SCIM API requests](/user-guide/scim-api-references)
