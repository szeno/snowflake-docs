# Manage clean room users and access

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

## Overview

This topic describes how a clean rooms account administrator manages user access to the clean rooms UI and API.

Clean rooms defines several application roles that permit access to the API
and various subsections of the UI. Access to the clean rooms UI and API are granted separately.
Typically, the account administrator creates a custom role, grants the desired application roles to
allow fine-grained access to the UI and API, then grants the role to various users in that account.

This strategy uses the Snowflake role-based access control (RBAC) model to delegate privileges appropriately to clean room users and
collaborators in their account. For more information about RBAC, see [Overview of Access Control](/user-guide/security-access-control-overview). To see which
users were granted a specific role, run the following SQL command:

Copy code

```
SHOW GRANTS OF ROLE <role_name>;
```

Tip

This topic uses the following terms:

- Clean room users: Users who have been granted access to the clean rooms UI or API in their Snowflake account.
- Clean room collaborators: Consumers invited to join a clean room by
  the clean room provider. A collaborator is also a clean room user — that is, they must have access to the clean rooms UI or API to
  be able to accept an invitation and use the clean room.

## Manage access to the clean rooms UI

An administrator grants access to the clean rooms UI in a Snowflake account by granting the appropriate roles, either directly or
indirectly. The administrator should also assign a default warehouse and grant USAGE privilege on it to UI users.

The following roles grant permission to manage or access the clean rooms UI:

- **ACCOUNTADMIN:** Role used to install or uninstall the clean rooms environment. This role also enables access to the
  **Snowflake Admin** page in the clean rooms UI. Account administrators use this page to manage the service user and account features
  such as Cross-Cloud Auto-Fulfillment, external and Iceberg tables, and dataset registration for UI users. This role has all clean room
  UI privileges; a user running as ACCOUNTADMIN doesn’t need any additional UI application roles.
- **MANAGE\_CLEANROOMS:** Application role that provides the ability to create, update, delete, and install clean rooms, and create, update,
  delete, and run analyses in the clean rooms UI.
- **MANAGE\_DCR\_PROFILE\_AND\_FEATURES:** Application role that provides access to the **Profile & Features** page in the **Admin**
  section of the UI, where you can manage the company profile and control which third-party connectors can be used in clean rooms.
- **MANAGE\_DCR\_CONNECTORS:** Application role that provides access to the **Connectors** page in the UI, where you can configure
  third-party connectors.
- **MANAGE\_DCR\_COLLABORATORS:** Application role that provides access to the **Collaborators** page in the UI, where you can manage the
  list of approved collaborators available to clean room providers in the UI. This role does not control the list of collaborators
  available to providers when using the API; API users can invite anyone to collaborate. For more information, see
  [Manage clean room collaborators](#label-cleanrooms-get-started-add-collaborators).

**Example**

The following code shows how to create a custom role, grant that role several UI capabilities, and then grant the custom role to a user.

Copy code

```
-- Create the role.
USE ROLE ACCOUNTADMIN;
CREATE ROLE dcr_access;

-- Grant capabilities to the new role.
GRANT APPLICATION ROLE SAMOOHA_BY_SNOWFLAKE.MANAGE_CLEANROOMS TO ROLE dcr_access;
GRANT APPLICATION ROLE SAMOOHA_BY_SNOWFLAKE.MANAGE_DCR_COLLABORATORS TO ROLE dcr_access;
GRANT APPLICATION ROLE SAMOOHA_BY_SNOWFLAKE.MANAGE_DCR_PROFILE_AND_FEATURES TO ROLE dcr_access;
GRANT APPLICATION ROLE SAMOOHA_BY_SNOWFLAKE.MANAGE_DCR_CONNECTORS TO ROLE dcr_access;

-- Assign the role to a user.
-- You must also grant access to a default warehouse to the role.
GRANT USAGE ON WAREHOUSE <your_warehouse> TO ROLE dcr_access;
ALTER USER <some_user> SET DEFAULT_WAREHOUSE  =  <your_warehouse>;
GRANT ROLE dcr_access to USER <some_user>;
```

## Manage API users

API access is managed using roles. The following Snowflake roles are used to access or manage the API:

- **ACCOUNTADMIN:** The role used to install or uninstall the clean rooms environment. This role does not include SAMOOHA\_APP\_ROLE; to use
  the API, you must use SAMOOHA\_APP\_ROLE.
- **SAMOOHA\_APP\_ROLE:** This role grants [full permission](#label-dcr-grant-full-api-access) to the clean rooms API in this account. (This role is used by the clean rooms UI to communicate with the API.)
- **Run-only developer role:** Someone using SAMOOHA\_APP\_ROLE can
  [grant usage on a limited-access role](#label-dcr-grant-limited-access). This role, also called a *run role*, grants permission to
  use a subset of API procedures on a subset of clean rooms in the consumer context. These limited roles can be granted to roles to provide
  scoped usage in your account for specific users, such as data analysts.

### Grant or revoke full API access

The SAMOOHA\_APP\_ROLE role grants a user full API access to all clean rooms in a Snowflake account. This role has usage on all
warehouses installed with clean rooms.

**Grant full API access:**

Copy code

```
USE ROLE ACCOUNTADMIN;
GRANT ROLE SAMOOHA_APP_ROLE TO USER <user_name>;
```

**Revoke full API access:**

Copy code

```
USE ROLE ACCOUNTADMIN;
REVOKE ROLE SAMOOHA_APP_ROLE FROM USER <user_name>;
```

### Grant limited API access (run roles)

You can grant limited API access to specified clean rooms in your account. Limited access grants the ability to call only a
[subset of consumer procedures](/user-guide/cleanrooms/consumer#label-dcr-sproc-consumer-manage-role-access), such as `consumer.run_analysis`, but not the ability
to install, create, join, or modify a clean room. This access level is sometimes called a *run role*, because it involves creating a role
with limited API access and granting that role to users.

Here is how to grant limited access to a user:

1. A user who can grant the SAMOOHA\_APP\_ROLE role creates a new role, and assigns limited functionality to that role. The role must also
   be granted USAGE on any warehouses that they will use to access the clean rooms.

   Copy code

   ```
   -- Create the role.
   USE ROLE ACCOUNTADMIN;
   CREATE ROLE MARKETING_ANALYST_ROLE;

   -- Grant USAGE on one of the basic clean room warehouses.
   -- You can grant USAGE to any warehouses that you want them to use.
   GRANT USAGE ON WAREHOUSE APP_WH TO MARKETING_ANALYST_ROLE;

   -- Grant limited functionality to the role for a subset of clean rooms.
   CALL samooha_by_snowflake_local_db.consumer.grant_run_on_cleanrooms_to_role(
     [$cleanroom_1, $cleanroom_2],
     'MARKETING_ANALYST_ROLE'
   );

   -- Grant the role to a user.
   GRANT ROLE MARKETING_ANALYST_ROLE TO USER george.washington;
   ```
2. The user then uses their limited role to perform specific actions in the clean room account:

   Copy code

   ```
   -- User george.washington logs in and uses the limited role.
   USE WAREHOUSE APP_WH
   USE ROLE MARKETING_ANALYST_ROLE;
   USE SECONDARY ROLES NONE;

   -- Consumer-run analyses should succeed.
   CALL samooha_by_snowflake_local_db.consumer.run_analysis(
     $cleanroom_name,
     'prod_overlap_analysis',
     ['MY_DB.MYDATA.CONVERSIONS'],  -- Consumer tables
     ['MY_DB.MYDATA.EXPOSURES'],      -- Provider tables
     object_construct(
       'max_age', 30
     )
   );

   -- Clean room creation and management procedures fail.
   CALL samooha_by_snowflake_local_db.provider.cleanroom_init($cleanroom_name, 'INTERNAL');
   ```

### Revoke limited API access

- To revoke run privileges on a specific clean room from a specific role, call [revoke\_run\_on\_cleanrooms\_from\_role](/user-guide/cleanrooms/consumer#label-dcr-consumer-revoke-run-on-cleanrooms-from-role).
- To revoke all granted run privileges from a single user, revoke the role from the user.

## Manage clean room collaborators

*Collaborators* are users invited to join a clean room as a consumer by a clean room provider.

**When using the clean rooms UI**, creators can invite collaborators from a list that is managed by someone using the
MANAGE\_DCR\_COLLABORATORS role.

**When using the clean rooms API**, providers are not limited by a predefined collaborators list, and can add any clean room collaborator
by Snowflake account locator. If you want to invite a collaborator without a Snowflake account, you must first
[create a clean room managed account](/user-guide/cleanrooms/managed-accounts#label-cleanrooms-intro-managed-account) for them. Remember that you invite an account to
collaborate, not an individual user. Any user with clean rooms access in the invited account can join and use the clean room.

Note

If a Snowflake collaborator has an account in a different region than your Snowflake account, your account administrator must
[enable Cross-Cloud Auto-Fulfillment](/user-guide/cleanrooms/laf) before you can add them as a collaborator.

Clean rooms UIClean rooms API

To manage the collaborator list used in the clean rooms UI, you need the [MANAGE\_DCR\_COLLABORATORS role](#label-dcr-manage-ui-users).

2. In the left navigation, select **Collaborators**.
3. Do one of the following:
   - If the collaborator has a Snowflake account, select **Snowflake Partners** » **+ Snowflake Partner**. Respond to the
     prompts to enter the details of the collaborator’s Snowflake account.
   - If the collaborator is not a Snowflake customer:
     1. You can contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support) to grant you the ability to create a [managed account](/user-guide/cleanrooms/managed-accounts#label-cleanrooms-intro-managed-account).
     2. When you have been granted that ability, return to the **Collaborators** pane and select the **Managed Accounts** tab to
        create a clean room managed account for your collaborator.

When using the clean rooms API, providers can add collaborators by calling the `provider.add_consumers`
procedure.

If the collaborator is not a Snowflake customer, someone must
[create a clean room managed account](/user-guide/cleanrooms/managed-accounts#label-cleanrooms-intro-managed-account) for them.
