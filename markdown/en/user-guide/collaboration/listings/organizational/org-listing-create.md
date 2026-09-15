# Create an organizational listing

Create an organizational listing to share data products securely within your organization. Before you create an organizational listing, review the prerequisites, known limitations, and considerations.

## Prerequisites

- Your organization has an ORGADMIN role. ([Organization accounts](/user-guide/organization-accounts) are optional.)

## Known limitations

- Support for organizational listings in government and special regions is currently in preview in the following regions:

  - FRM: US-EAST-1
  - FRM: US-WEST-2
  - KSA: GCPMECENTRAL2

  These deployments are subject to the following limitations:

  - Creating custom organization profiles in government regions isn’t supported.
  - The [ACCESS\_HISTORY view](/sql-reference/organization-usage/access_history) in the organization account isn’t available.
  - Organizational listings created from commercial or Virtual Private Snowflake (VPS) accounts don’t show up when searching, filtering, or browsing listings.
- You must use the API to target specific regions.
- Data products supported: Snowflake Native App Framework and shares.
- Organizational listings that contain a Snowflake Native App do not support target roles for access or discovery.
- The following features are not supported when using organizational listings:

  - Provider studio analytics.
  - Reader accounts.
- You cannot specify specific regions in organizational listings using Snowsight.

  Instead, you can specify the region in the [manifest YAML](/user-guide/collaboration/listings/organizational/org-listing-manifest-reference)
  file when [creating](/sql-reference/sql/create-organization-listing) or [altering](/sql-reference/sql/alter-listing) the listing programmatically.
- When [assigning organizational listing privileges](#label-assign-org-listing-privileges), Snowflake loads all database roles granted to a share. This allows consumers to see unmasked data when running a query on a mountless listing. To avoid this behavior, mount the listing and don’t use database roles with ULLs.

## Considerations

- Before you target an entire organization, check for external tenants. Adjust the target accounts for your data
  products before adding them to an organizational listing unless you intend to share them with external tenants.
- Each share can be attached to one listing.
- Each Native App can be attached to one or more listings.
- For organization changes (such as mergers) with accounts containing organizational listings, contact [Snowflake Support](/user-guide/contacting-support).

## Access control requirements

Use the information provided here to determine the specific roles and privileges that you must have to execute organizational listing SQL commands.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

### Assign organizational listing privileges

To create an organizational listing, a role must have the necessary privileges to create a share, as shown in [Share creation and management](#label-share-creation-and-management-table), as well as necessary privileges to create an organizational listing from it, as shown in [Privileges to create an organizational listing using the share](#label-privileges-to-create-sharable-org-listing-table).

#### Share creation and management

To create a share and to create and manage objects inside a share, a role must have the necessary privileges on the data objects, schemas, and the CREATE SHARE command.

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE SHARE | ACCOUNT | To *CREATE* a share. |
| OWNERSHIP or USAGE with grants option | DATABASE | To see and *USE* the specified database. |
| OWNERSHIP or USAGE with grants option | SCHEMA | To see the specified schema. |
| SELECT | TABLE | To query specified tables in the specified schema. |

Expand

Show lessSee more

USAGE or any other privilege on the parent database and schema is required to perform operations on any object in a schema.

#### Privileges to create an organizational listing using the share

One of the following privileges is required to create an organizational listing, in addition to the share-related privileges listed above.

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE ORGANIZATION LISTING | ACCOUNT | To create and alter organizational listings. |
| CREATE LISTING | ACCOUNT | To create and alter organizational listings and private listings. |

Expand

Show lessSee more

#### Privileges to alter an organizational listing

One of the following privileges is required to alter a listing.

| Role | Notes |
| --- | --- |
| OWNERSHIP | Can *ALTER* a share without additional grant options. |
| MODIFY with grants option | Can *ALTER* a share after granting modify privileges to a role. This can be done using:  Copy code  ``` GRANT MODIFY ON DATA EXCHANGE LISTING <listing_name> TO ROLE <role_name> ``` |

Expand

Show lessSee more

## Consume or query an organizational listing

To consume an organizational listing directly, you can reference the [Uniform Listing Locator (ULL)](/user-guide/collaboration/listings/organizational/org-listing-configure#label-olisting-im-ull) without any additional privileges. If you require mounting the listing, then the following privileges are required:

| Privilege | Object | Notes |
| --- | --- | --- |
| IMPORT ORGANIZATION LISTING | ACCOUNT | To import an organizational listing. |
| CREATE DATABASE | ACCOUNT | To create a database and mount the listing objects. |

Expand

Show lessSee more

### Manage listing auto-fulfillment settings

Before managing auto-fulfillment settings for your organization listing, ensure that you have the necessary roles to manage auto-fulfilling the listing. See the auto-fulfillment [required privileges](/collaboration/provider-listings-auto-fulfillment-manage-privileges) for more information.

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| MANAGE LISTING AUTO FULFILLMENT | ACCOUNT | To configure the auto-fulfillment settings. |

Expand

Show lessSee more

## Create an organizational listing in Snowsight or SQL

SnowsightSQL

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Data sharing** » **Internal sharing**.
3. Select **+ Create Listing**.
4. Select a data product such as a table, view, or other data product to add to the listing.

   1. Review the generated share identifier, then select **Generate listing**.
5. Enter a name for your listing and review the generated Universal Listing Locator, then select **Save**.
6. To specify who can access the listing (the target accounts, roles, and regions), select **+ Access Control**. The **Access and discovery** dialog displays.

   1. Complete the **Grant access** section:

      | Field | Description |
      | --- | --- |
      | **Who can access this data product?** | Select one of the following:  - **Entire organization**: Anyone in the organization can access the listing. If **Entire organization** is selected and [cross-cloud auto-fulfillment](http://other-docs.snowflake.com/en/collaboration/provider-listings-auto-fulfillment) is enabled on your account, then you’ll be prompted to review the auto-fulfillment refresh settings for the listing.  - **Selected accounts and roles**: Only selected accounts and roles can access. - **No accounts or roles are pre-approved**: (Default) Data product will only be available by request. |
      | **Accounts** | If **Selected accounts and roles** is selected, select one or more accounts.  Optional. Select **+ Add another account** to add second and subsequent accounts.  By default, all roles in the selected accounts can access the listing. Select **Selected roles** to grant access only to specific roles each selected account. |

      Expand

      Show lessSee more
   2. Complete the **Allow discovery** section:

      | Field | Description |
      | --- | --- |
      | **Who else can discover the listing and request access?** | Select one of:  - **Entire organization**: (Default) Anyone in the organization can discover listing and request access. This field is selected and disabled if **Entire organization** is specified for in the **Grant access** section. - **Selected accounts and roles**: Only selected accounts and roles can discover listing and request access. - **Not discoverable by users without access**: Only users with access can discover this listing. |
      | **Accounts** | If **Select accounts and roles** is selected, select one or more accounts.  Optional. Select **+ Add another account** to add second and subsequent accounts and grant access to specific roles. |
      | **Selected user roles** | If **Selected roles** is selected, enter one or more roles to grant access. |

      Expand

      Show lessSee more
   3. If **Allow discovery** is **Selected accounts and roles**, then select **Set up request approval flow**.

      - In the **Set up request approval flow** dialog, select one of the following options in the **How should the request approval happen?** list:

        - **Manage requests in Snowflake**: Enter the email address of the request approver and optionally specify additional roles that can approve requests.
        - **Manage requests outside of Snowflake**: Enter an email address for the request approver or enter a URL that points to an internal ticketing system.

        Note

        The **Set up request approval flow** button isn’t available if the data product is accessible by the entire organization or if the data product is not discoverable by users without access.

1. Complete the listing.

   Enter additional information about the listing page to guide consumers,
   such as the following. For more information about these fields, see [Configure listings](/collaboration/provider-listings-reference).

   - Description
   - Data dictionary
   - Quick start examples
   - Details, including the support contact
   - Documentation links
   - Terms of service
   - Attributes
2. Select **Publish** to make the listing available in the **Internal Marketplace**.

   If you exit without publishing, the listing is saved as a draft that’s ready for review or for the addition of descriptive metadata.

Create an organizational listing from the share with the required attributes included in YAML (entered in $$ delimiters).

This part of the manifest YAML specifies the accounts that will be able to use the organizational listing:

Copy code

```
organization_targets:
  access:
```

This example creates a listing using the required settings in the manifest YAML. It targets one role in
one account in one region and includes support and approver contacts:

Note

`support_contact` is required.
`approver_contact` is required if a `discovery` target is provided. For request-access workflow options, see [Request access workflow in the Internal Marketplace](/LIMITEDACCESS/collaboration/request-access-workflow-internal-marketplace).

Copy code

```
USE ROLE <organizational_listing_role>;

CREATE ORGANIZATION LISTING <organization_listing_name>
SHARE <share_name> AS
$$
title: "My title"
description: "One region, all accounts"
organization_profile: "INTERNAL"
organization_targets:
  discovery:
  - account: "<account_name>"
    roles:
    - "<role>"

  access:
  - account: "<account_name>"
    roles:
    - "<role>"

support_contact: "support@somedomain.com"
approver_contact: "approver@somedomain.com"
locations:
  access_regions:
  - name: "PUBLIC.<snowflake_region>"
$$;
```

For a complete list of all fields and values for an organizational listing see [Organization listing manifest reference](/user-guide/collaboration/listings/organizational/org-listing-manifest-reference).
For additional examples, see [Set who can discover and access an organizational listing](/user-guide/collaboration/listings/organizational/org-listing-configure#label-organizational-listing-discovery-and-access).
