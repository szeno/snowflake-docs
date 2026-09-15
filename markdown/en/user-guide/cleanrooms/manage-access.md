# Managing access to collaborations, resources, and data

Feature — Generally Available

Currently available in [these regions](/user-guide/cleanrooms/installing-dcr#label-dcr-supported-regions).

Not available in government and VPS deployments.

## Overview

Access to collaborations, and the ability to perform actions in a collaboration, are managed using the following mechanisms:

- **Permission to install applications for the account** is required to install the Data Clean Room application and is held by ACCOUNTADMIN by default.
- **Permission to run specific Collaboration API procedures** is managed by [DCR privileges](#label-dcr-collab-about-rbac-roles).
- **Permission to perform specific role-based actions** in a collaboration is managed by [Collaboration roles](/user-guide/cleanrooms/roles).
  These roles determine what a user can do in a specific collaboration. The
  [collaboration definition](/user-guide/cleanrooms/spec-collaboration#label-dcr-collaboration-spec-yaml) must list you as an analysis runner to be able to run an analysis.
  You must be listed as a data provider to share data with a specified analysis runner.

These mechanisms are overlapping, and all requirements must be fulfilled to be able to perform a specific action on a specific resource.
For example, for you to share a table `my_data` with `user_1` in existing collaboration `collab_1`, all of the following requirements
must be met:

- You must be a designated data provider for `user_1` in the collaboration, and `user_1` must be an analysis runner in that
  collaboration (*collaboration role*).
- You must have permission to call the appropriate Collaboration API procedures to link the data offering into the collaboration (*DCR privilege*).
- You must have the REFERENCE\_USAGE privilege with GRANT OPTION on the table `my_data` to register it as a data offering resource (*RBAC privilege*).

This topic describes how to manage DCR privileges. [Data policies](/user-guide/cleanrooms/resources-data-offerings#label-dcr-apply-usage-policies-to-collaboration) and
[collaboration roles](/user-guide/cleanrooms/roles) are described separately.

## Use DCR privileges to manage account, object, and procedure privileges

The SAMOOHA\_APP\_ROLE role has privileges to run all procedures in the Collaboration API. This role may have more widely-scoped access than you would like to grant to some groups of users in your account.
Although collaboration roles limit what actions a user may perform, you may also provision specific roles with more precise and limited permissions.

Once the Snowflake Data Clean Rooms app has been installed, additional Data Clean Room-specific privileges may be assigned to specific users.

To grant granular API privileges to a user, take the following steps:

1. Create a role.
2. Grant usage on the warehouse being used to the role.
3. Call [GRANT\_PRIVILEGE\_ON\_OBJECT\_TO\_ROLE](/user-guide/cleanrooms/collaboration-api-reference#label-grant-privilege-on-object-to-role) if needed to grant appropriate privileges on a specific collaboration to a role.
4. Call [GRANT\_PRIVILEGE\_ON\_ACCOUNT\_TO\_ROLE](/user-guide/cleanrooms/collaboration-api-reference#label-dcr-grant-privilege-on-account-to-role) if needed to grant appropriate high-level privileges on all collaborations in the account to the role.
5. Grant the role to the user, who can now call collaboration procedures to participate in the collaboration.

For example, `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE( 'JOIN COLLABORATION', 'collab_join_role' )` grants `collab_join_role` permission
to call JOIN, REVIEW, RUN, LEAVE, VIEW\_DATA\_OFFERINGS, and many other API procedures needed to join and use a collaboration. In contrast,
`GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('READ', 'REGISTRY', 'registry_1', 'registry_reader_role')` grants `registry_reader_role` the
permission to read from a single registry. You can grant multiple sets of privileges to the same role.

[See which DCR privileges must be granted to be able to call a given Collaboration API procedure](#label-dcr-collab-list-of-required-privileges)
if you aren’t using SAMOOHA\_APP\_ROLE.

Here is an example of creating a role named COLLABORATION\_CREATOR that can create a collaboration, create a custom registry, and register
data offerings, and granting the role to the current user.

Copy code

```
CREATE ROLE IF NOT EXISTS COLLABORATION_CREATOR;

-- Grant warehouse access to the role.
GRANT USAGE ON WAREHOUSE APP_WH TO ROLE COLLABORATION_CREATOR;

-- COLLABORATION_CREATOR needs these manual account-level privileges,
-- which are required by the CREATE COLLABORATION DCR privilege.
GRANT APPLY ROW ACCESS POLICY ON ACCOUNT TO ROLE COLLABORATION_CREATOR;
GRANT CREATE APPLICATION ON ACCOUNT TO ROLE COLLABORATION_CREATOR;
GRANT CREATE DATABASE ON ACCOUNT TO ROLE COLLABORATION_CREATOR;
GRANT CREATE LISTING ON ACCOUNT TO ROLE COLLABORATION_CREATOR;
GRANT CREATE SHARE ON ACCOUNT TO ROLE COLLABORATION_CREATOR;
GRANT IMPORT SHARE ON ACCOUNT TO ROLE COLLABORATION_CREATOR;
GRANT MANAGE SHARE TARGET ON ACCOUNT TO ROLE COLLABORATION_CREATOR;

GRANT ROLE COLLABORATION_CREATOR TO USER alexander_hamilton;

-- Grant DCR account-level privileges using GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE.
-- This procedure requires the ACCOUNTADMIN role.

-- COLLABORATION_CREATOR: create collaborations, create registries,
-- and register data offerings.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.ADMIN.GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE(
  'CREATE COLLABORATION', 'COLLABORATION_CREATOR');
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.ADMIN.GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE(
  'CREATE REGISTRY', 'COLLABORATION_CREATOR');
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.ADMIN.GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE(
  'REGISTER DATA OFFERING', 'COLLABORATION_CREATOR');
```

The following code uses the role COLLABORATION\_CREATOR to create a custom registry, and then grants read access on that registry to the EU\_SALES\_TEAM role:

Copy code

```
USE ROLE COLLABORATION_CREATOR;
USE WAREHOUSE APP_WH;
USE SECONDARY ROLES NONE;

-- Create a custom registry.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.REGISTRY.CREATE_REGISTRY(
  'DATA_REGISTRY_EU',
  'DATA OFFERING');

-- Grant read permission on a registry created by this role to the role EU_SALES_TEAM.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.ADMIN.GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE(
  'READ',
  'REGISTRY',
  'DATA_REGISTRY_EU',
  'EU_SALES_TEAM');
```

## DCR privilege requirements for Collaboration API procedures

If you’re using a custom role (rather than SAMOOHA\_APP\_ROLE), the following table summarizes the privileges required to run each
Collaboration API procedure.

Unless noted otherwise, privileges in a bulleted list are typically alternatives: you need only one of the privileges listed to run the
specified procedure.

| Procedure name | Access requirements |
| --- | --- |
| [REGISTER\_TEMPLATE](/user-guide/cleanrooms/collaboration-api-reference#label-dcr-collaboration-register-template-reference) | **Default registry:** `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('REGISTER TEMPLATE', '{role name}')`  **Custom registry:** You have read and write privileges on any custom registry that you created yourself. To access a custom registry created by another user, you need `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('REGISTER', 'REGISTRY', '{registry name}', '{role name}')`. |
| [VIEW\_REGISTERED\_TEMPLATES](/user-guide/cleanrooms/collaboration-api-reference#label-dcr-collaboration-view-registered-templates-reference) | **Default registry:**   - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('VIEW REGISTERED TEMPLATES', '{role name}')` - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE COLLABORATION', '{role name}')`, plus all additional account-level privileges - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('JOIN COLLABORATION', '{role name}')`, plus all additional account-level privileges   **Custom registry:** You have read and write privileges on any custom registry that you created yourself. To access a custom registry created by another user, you need `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('READ', 'REGISTRY', '{registry name}', '{role name}')`. |
| [ADD\_TEMPLATE\_REQUEST](/user-guide/cleanrooms/collaboration-api-reference#label-dcr-collaboration-add-template-request-reference) | - `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('UPDATE', 'COLLABORATION', '{collaboration name}', '{role name}')` - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE COLLABORATION', '{role name}')`, plus all additional account-level privileges - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('JOIN COLLABORATION', '{role name}')`, plus all additional account-level privileges   If the template is in a custom registry, or references a code spec in a custom registry, you must also have the READ privilege on the registry. |
| [REMOVE\_TEMPLATE](/user-guide/cleanrooms/collaboration-api-reference#label-dcr-collaboration-remove-template-reference) | - `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('UPDATE', 'COLLABORATION', '{collaboration name}', '{role name}')` - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE COLLABORATION', '{role name}')`, plus all additional account-level privileges - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('JOIN COLLABORATION', '{role name}')`, plus all additional account-level privileges |
| [VIEW\_TEMPLATES](/user-guide/cleanrooms/collaboration-api-reference#label-dcr-collaboration-view-templates-reference) | - `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('VIEW TEMPLATES', 'COLLABORATION', '{collaboration name}', '{role name}')` - `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('READ', 'COLLABORATION', '{collaboration name}', '{role name}')` - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE COLLABORATION', '{role name}')`, plus all additional account-level privileges - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('JOIN COLLABORATION', '{role name}')`, plus all additional account-level privileges   Additionally, to see objects registered in a custom registry, you need the READ privilege on that registry. |
| [ENABLE\_TEMPLATE\_AUTO\_APPROVAL](/user-guide/cleanrooms/collaboration-api-reference#label-dcr-collaboration-enable-template-auto-approval-reference) | - `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('MANAGE TEMPLATE AUTO APPROVAL', 'COLLABORATION', '{collaboration name}', '{role name}')` - `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('UPDATE', 'COLLABORATION', '{collaboration name}', '{role name}')` - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE COLLABORATION', '{role name}')`, plus all additional account-level privileges - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('JOIN COLLABORATION', '{role name}')`, plus all additional account-level privileges |
| [DISABLE\_TEMPLATE\_AUTO\_APPROVAL](/user-guide/cleanrooms/collaboration-api-reference#label-dcr-collaboration-disable-template-auto-approval-reference) | - `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('MANAGE TEMPLATE AUTO APPROVAL', 'COLLABORATION', '{collaboration name}', '{role name}')` - `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('UPDATE', 'COLLABORATION', '{collaboration name}', '{role name}')` - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE COLLABORATION', '{role name}')`, plus all additional account-level privileges - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('JOIN COLLABORATION', '{role name}')`, plus all additional account-level privileges |
| [GET\_CONFIGURATION](/user-guide/cleanrooms/collaboration-api-reference#label-dcr-collaboration-get-configuration-reference) | - `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('MANAGE TEMPLATE AUTO APPROVAL', 'COLLABORATION', '{collaboration name}', '{role name}')` - `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('READ', 'COLLABORATION', '{collaboration name}', '{role name}')` - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE COLLABORATION', '{role name}')`, plus all additional account-level privileges - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('JOIN COLLABORATION', '{role name}')`, plus all additional account-level privileges |
| [SET\_CONFIGURATION](/user-guide/cleanrooms/collaboration-api-reference#label-dcr-collaboration-set-configuration-reference) | - `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('MANAGE TEMPLATE AUTO APPROVAL', 'COLLABORATION', '{collaboration name}', '{role name}')` - `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('UPDATE', 'COLLABORATION', '{collaboration name}', '{role name}')` - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE COLLABORATION', '{role name}')`, plus all additional account-level privileges - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('JOIN COLLABORATION', '{role name}')`, plus all additional account-level privileges |
| [REGISTER\_DATA\_OFFERING](/user-guide/cleanrooms/collaboration-api-reference#label-dcr-collaboration-register-data-offering-reference) | **Default registry:** `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('REGISTER DATA OFFERING', '{role name}')`  **Custom registry:** You have read and write privileges on any custom registry that you created yourself. To access a custom registry created by another user, you need `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('REGISTER', 'REGISTRY', '{registry name}', '{role name}')`.  Additionally, the caller needs the following RBAC privileges:   - SELECT on the source table/view. - USAGE on the database and schema containing the source table. - USAGE on any policy objects referenced in the spec. |
| [LINK\_DATA\_OFFERING](/user-guide/cleanrooms/collaboration-api-reference#label-dcr-collaboration-link-data-offering-reference) | - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE COLLABORATION', '{role name}')`, plus all additional account-level privileges - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('JOIN COLLABORATION', '{role name}')`, plus all additional account-level privileges   Additionally, the caller must have the REFERENCE\_USAGE privilege with GRANT OPTION on any data to be shared. If you don’t, you’ll get a “missing reference usage grant” error. [Learn how to handle this issue.](/user-guide/cleanrooms/v2/troubleshooting#label-dcr-database-missing-reference-usage-error)  If the data offering is in a custom registry, you must also have privileges granted by calling `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('READ', 'REGISTRY', '{registry name}', '{role name}')`. |
| [UNLINK\_DATA\_OFFERING](/user-guide/cleanrooms/collaboration-api-reference#label-dcr-collaboration-unlink-data-offering-reference) | - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE COLLABORATION', '{role name}')`, plus all additional account-level privileges - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('JOIN COLLABORATION', '{role name}')`, plus all additional account-level privileges   The `UPDATE` privilege on a collaboration doesn’t grant access to this procedure. Additionally, only the role that called JOIN can successfully unlink data offerings, because the underlying share is owned by the joining role. |
| [LINK\_LOCAL\_DATA\_OFFERING](/user-guide/cleanrooms/collaboration-api-reference#label-dcr-collaboration-link-local-data-offering-reference) | - `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('UPDATE', 'COLLABORATION', '{collaboration name}', '{role name}')` - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE COLLABORATION', '{role name}')`, plus all additional account-level privileges - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('JOIN COLLABORATION', '{role name}')`, plus all additional account-level privileges |
| [UNLINK\_LOCAL\_DATA\_OFFERING](/user-guide/cleanrooms/collaboration-api-reference#label-dcr-collaboration-unlink-local-data-offering-reference) | - `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('UPDATE', 'COLLABORATION', '{collaboration name}', '{role name}')` - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE COLLABORATION', '{role name}')`, plus all additional account-level privileges - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('JOIN COLLABORATION', '{role name}')`, plus all additional account-level privileges |
| [VIEW\_REGISTERED\_DATA\_OFFERINGS](/user-guide/cleanrooms/collaboration-api-reference#label-dcr-collaboration-view-registered-data-offerings-reference) | **Default registry:**   - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('VIEW REGISTERED DATA OFFERINGS', '{role name}')` - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE COLLABORATION', '{role name}')`, plus all additional account-level privileges - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('JOIN COLLABORATION', '{role name}')`, plus all additional account-level privileges   **Custom registry:** You have read and write privileges on any custom registry that you created yourself. To access a custom registry created by another user, you need `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('READ', 'REGISTRY', '{registry name}', '{role name}')`. |
| [VIEW\_DATA\_OFFERINGS](/user-guide/cleanrooms/collaboration-api-reference#label-dcr-collaboration-view-data-offerings-reference) | - `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('VIEW DATA OFFERINGS', 'COLLABORATION', '{collaboration name}', '{role name}')` - `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('READ', 'COLLABORATION', '{collaboration name}', '{role name}')` - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE COLLABORATION', '{role name}')`, plus all additional account-level privileges - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('JOIN COLLABORATION', '{role name}')`, plus all additional account-level privileges   Additionally, to see objects registered in a custom registry, you need the READ privilege on that registry. |
| [REGISTER\_CODE\_SPEC](/user-guide/cleanrooms/collaboration-api-reference#label-dcr-collab-register-code-spec) | **Default registry:** `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('REGISTER CODE SPEC', '{role name}')`  **Custom registry:** You have read and write privileges on any custom registry that you created yourself. To access a custom registry created by another user, you need `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('REGISTER', 'REGISTRY', '{registry name}', '{role name}')`. |
| [VIEW\_REGISTERED\_CODE\_SPECS](/user-guide/cleanrooms/collaboration-api-reference#label-dcr-collaboration-view-registered-code-specs-reference) | **Default registry:**   - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('VIEW REGISTERED CODE SPECS', '{role name}')` - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE COLLABORATION', '{role name}')`, plus all additional account-level privileges - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('JOIN COLLABORATION', '{role name}')`, plus all additional account-level privileges   **Custom registry:** You have read and write privileges on any custom registry that you created yourself. To access a custom registry created by another user, you need `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('READ', 'REGISTRY', '{registry name}', '{role name}')`. |
| [VIEW\_CODE\_SPECS](/user-guide/cleanrooms/collaboration-api-reference#label-dcr-collaboration-view-code-specs-reference) | - `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('READ', 'COLLABORATION', '{collaboration name}', '{role name}')` - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE COLLABORATION', '{role name}')`, plus all additional account-level privileges - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('JOIN COLLABORATION', '{role name}')`, plus all additional account-level privileges   Additionally, to see objects registered in a custom registry, you need the READ privilege on that registry. |
| [VIEW\_UPDATE\_REQUESTS](/user-guide/cleanrooms/collaboration-api-reference#label-dcr-collaboration-view-update-requests-reference) | - `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('READ', 'COLLABORATION', '{collaboration name}', '{role name}')` - `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('UPDATE', 'COLLABORATION', '{collaboration name}', '{role name}')` - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE COLLABORATION', '{role name}')`, plus all additional account-level privileges - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('JOIN COLLABORATION', '{role name}')`, plus all additional account-level privileges |
| [APPROVE\_UPDATE\_REQUEST](/user-guide/cleanrooms/collaboration-api-reference#label-dcr-collaboration-approve-update-request-reference) | - `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('MANAGE UPDATE REQUEST', 'COLLABORATION', '{collaboration name}', '{role name}')` - `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('UPDATE', 'COLLABORATION', '{collaboration name}', '{role name}')` - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE COLLABORATION', '{role name}')`, plus all additional account-level privileges - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('JOIN COLLABORATION', '{role name}')`, plus all additional account-level privileges |
| [REJECT\_UPDATE\_REQUEST](/user-guide/cleanrooms/collaboration-api-reference#label-dcr-collaboration-reject-update-request-reference) | - `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('MANAGE UPDATE REQUEST', 'COLLABORATION', '{collaboration name}', '{role name}')` - `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('UPDATE', 'COLLABORATION', '{collaboration name}', '{role name}')` - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE COLLABORATION', '{role name}')`, plus all additional account-level privileges - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('JOIN COLLABORATION', '{role name}')`, plus all additional account-level privileges |
| [INITIALIZE](/user-guide/cleanrooms/collaboration-api-reference#label-dcr-collaboration-initialize-reference) | - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE COLLABORATION', '{role name}')`, plus all additional account-level privileges   See GRANT\_PRIVILEGE\_ON\_ACCOUNT\_TO\_ROLE for additional required role permissions. |
| [TEARDOWN](/user-guide/cleanrooms/collaboration-api-reference#label-dcr-collaboration-teardown-reference) | - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE COLLABORATION', '{role name}')`, plus all additional account-level privileges - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('JOIN COLLABORATION', '{role name}')`, plus all additional account-level privileges   See GRANT\_PRIVILEGE\_ON\_ACCOUNT\_TO\_ROLE for additional required role permissions. |
| [GET\_STATUS](/user-guide/cleanrooms/collaboration-api-reference#label-dcr-collaboration-get-status-reference) | - `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('READ', 'COLLABORATION', '{collaboration name}', '{role name}')` - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE COLLABORATION', '{role name}')`, plus all additional account-level privileges - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('JOIN COLLABORATION', '{role name}')`, plus all additional account-level privileges |
| [ENABLE\_EXTERNAL\_TABLE\_ANALYSIS \_FOR\_COLLABORATION](/user-guide/cleanrooms/collaboration-api-reference#label-dcr-collaboration-enable-external-table-analysis-for-collaboration-reference) | You must use a role that has been granted the MANAGE FIREWALL\_CONFIGURATION privilege on the account. |
| [VIEW\_COLLABORATIONS](/user-guide/cleanrooms/collaboration-api-reference#label-dcr-collaboration-view-collaborations-reference) | - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('VIEW COLLABORATIONS', '{role name}')` - `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('READ', 'COLLABORATION', '{collaboration name}', '{role name}')` - `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('RUN', 'COLLABORATION', '{collaboration name}', '{role name}')` - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE COLLABORATION', '{role name}')`, plus all additional account-level privileges - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('JOIN COLLABORATION', '{role name}')`, plus all additional account-level privileges |
| [REVIEW](/user-guide/cleanrooms/collaboration-api-reference#label-dcr-collaboration-review-reference) | - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('REVIEW COLLABORATION', '{role name}')` - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE COLLABORATION', '{role name}')`, plus all additional account-level privileges - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('JOIN COLLABORATION', '{role name}')`, plus all additional account-level privileges   See GRANT\_PRIVILEGE\_ON\_ACCOUNT\_TO\_ROLE for additional required role permissions. |
| [JOIN](/user-guide/cleanrooms/collaboration-api-reference#label-dcr-collaboration-join-reference) | - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE COLLABORATION', '{role name}')`, plus all additional account-level privileges - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('JOIN COLLABORATION', '{role name}')`, plus all additional account-level privileges   See GRANT\_PRIVILEGE\_ON\_ACCOUNT\_TO\_ROLE for additional required role permissions. |
| [LEAVE](/user-guide/cleanrooms/collaboration-api-reference#label-dcr-collaboration-leave-reference) | - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE COLLABORATION', '{role name}')`, plus all additional account-level privileges - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('JOIN COLLABORATION', '{role name}')`, plus all additional account-level privileges   See GRANT\_PRIVILEGE\_ON\_ACCOUNT\_TO\_ROLE for additional required role permissions. |
| [RUN](/user-guide/cleanrooms/collaboration-api-reference#label-dcr-collaboration-run-reference) | - `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('RUN', 'COLLABORATION', '{collaboration name}', '{role name}')` - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE COLLABORATION', '{role name}')`, plus all additional account-level privileges - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('JOIN COLLABORATION', '{role name}')`, plus all additional account-level privileges |
| [RUN\_ML\_JOB\_ACTION](/user-guide/cleanrooms/collaboration-api-reference#label-dcr-collaboration-run-ml-job-action) | - `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('RUN ML JOB ACTION', 'COLLABORATION', '{collaboration name}', '{role name}')` - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE COLLABORATION', '{role name}')`, plus all additional account-level privileges - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('JOIN COLLABORATION', '{role name}')`, plus all additional account-level privileges |
| [VIEW\_ACTIVITY\_HISTORY](/user-guide/cleanrooms/collaboration-api-reference#label-dcr-collaboration-view-activity-history-reference) | - `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('VIEW ACTIVITY HISTORY', 'COLLABORATION', '{collaboration name}', '{role name}')` - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE COLLABORATION', '{role name}')`, plus all additional account-level privileges - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('JOIN COLLABORATION', '{role name}')`, plus all additional account-level privileges |
| [VIEW\_ACTIVATIONS](/user-guide/cleanrooms/collaboration-api-reference#label-dcr-collaboration-view-activations-reference) | - `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('VIEW ACTIVATIONS', 'COLLABORATION', '{collaboration name}', '{role name}')` - `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('RUN', 'COLLABORATION', '{collaboration name}', '{role name}')` - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE COLLABORATION', '{role name}')`, plus all additional account-level privileges - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('JOIN COLLABORATION', '{role name}')`, plus all additional account-level privileges |
| [PROCESS\_ACTIVATION](/user-guide/cleanrooms/collaboration-api-reference#label-dcr-collaboration-process-activation-reference) | - `GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE('PROCESS ACTIVATION', 'COLLABORATION', '{collaboration name}', '{role name}')` - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE COLLABORATION', '{role name}')`, plus all additional account-level privileges - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('JOIN COLLABORATION', '{role name}')`, plus all additional account-level privileges |
| [CREATE\_REGISTRY](/user-guide/cleanrooms/collaboration-api-reference#label-dcr-collaboration-create-registry-reference) | - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE REGISTRY', '{role name}')` |
| [VIEW\_REGISTRIES](/user-guide/cleanrooms/collaboration-api-reference#label-dcr-collaboration-view-registries-reference) | - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('VIEW REGISTRIES', '{role name}')` - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE COLLABORATION', '{role name}')` - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('JOIN COLLABORATION', '{role name}')` - `GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE('CREATE REGISTRY', '{role name}')` |
| [GRANT\_PRIVILEGE\_ON\_OBJECT\_TO\_ROLE](/user-guide/cleanrooms/collaboration-api-reference#label-grant-privilege-on-object-to-role) | - **For collaboration objects:** Any role with CREATE COLLABORATION or JOIN COLLABORATION can call this procedure on any collaboration. - **For registry objects:** Only the role that created the registry can call this procedure on that registry. |
| [GRANT\_PRIVILEGE\_ON\_ACCOUNT\_TO\_ROLE](/user-guide/cleanrooms/collaboration-api-reference#label-dcr-grant-privilege-on-account-to-role) | You need the ACCOUNTADMIN role, or a role with the MANAGE GRANTS global privilege, to run this procedure. |

Expand

Show lessSee more
