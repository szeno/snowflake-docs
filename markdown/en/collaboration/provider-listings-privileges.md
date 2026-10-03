# Enable non-ACCOUNTADMIN roles to manage listings

This topic lists the minimum privileges required to create and manage listings, and shows how to delegate these tasks to a role other than
ACCOUNTADMIN.

By default, only the ACCOUNTADMIN role has the privileges to create listings and configure auto-fulfillment. You can grant these
privileges to other roles so that other users in the account can manage listings.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Privileges for listing tasks

The following table lists the minimum privileges for each listing task.

| Task | Required privileges | Notes |
| --- | --- | --- |
| Create a listing. | CREATE LISTING on the account | Only the ACCOUNTADMIN role has this privilege by default. The role that creates a listing owns it (has the OWNERSHIP privilege on it). |
| Alter a listing, including publishing and unpublishing it. | MODIFY on the listing | The role that owns the listing can also alter it. Only the owner can grant MODIFY on the listing to other roles. |
| Configure auto-fulfillment for a listing. | Both of the following:   - MODIFY on the listing - MANAGE LISTING AUTO FULFILLMENT on the account | Auto-fulfillment must be enabled on the account before ACCOUNTADMIN can grant MANAGE LISTING AUTO FULFILLMENT. See [Manage privileges for auto-fulfillment](/collaboration/provider-listings-auto-fulfillment-manage-privileges). |

Expand

Show lessSee more

A listing shares the data in a share. To create and manage the share that a listing uses, the role also needs the privileges described in
[Enable non-ACCOUNTADMIN roles to perform data sharing tasks](/user-guide/security-access-privileges-shares).

Note

Organizational listings use the CREATE ORGANIZATION LISTING privilege instead of CREATE LISTING. For details, see
[Create an organizational listing](/user-guide/collaboration/listings/organizational/org-listing-create).

## Steps to enable a non-ACCOUNTADMIN role to manage listings

The following steps let a custom role named `listing_admin` create a listing for an existing share named `sales_s`, publish it, and
configure auto-fulfillment. A second role, `listing_editor`, is granted MODIFY so that it can update the listing.

1. As ACCOUNTADMIN, grant the account-level listing privileges to the role, and grant the role to the user who manages listings:

   Copy code

   ```
   USE ROLE ACCOUNTADMIN;

   GRANT CREATE LISTING ON ACCOUNT TO ROLE listing_admin;
   GRANT MANAGE LISTING AUTO FULFILLMENT ON ACCOUNT TO ROLE listing_admin;

   GRANT ROLE listing_admin TO USER <user_name>;
   ```
2. As `listing_admin`, create the listing. Because `listing_admin` creates the listing, it owns the listing:

   Copy code

   ```
   USE ROLE listing_admin;

   CREATE EXTERNAL LISTING sales_listing
   SHARE sales_s AS
   $$
     title: "Sales data"
     description: "Daily sales data"
     listing_terms:
       type: "OFFLINE"
     targets:
       accounts: ["<orgname.accountname>"]
   $$ PUBLISH = FALSE REVIEW = FALSE;
   ```
3. Publish the listing:

   Copy code

   ```
   ALTER LISTING sales_listing PUBLISH;
   ```
4. Configure auto-fulfillment by updating the listing manifest. This step requires both MODIFY (or OWNERSHIP) on the listing and MANAGE
   LISTING AUTO FULFILLMENT on the account:

   Copy code

   ```
   ALTER LISTING sales_listing AS
   $$
     title: "Sales data"
     description: "Daily sales data"
     listing_terms:
       type: "OFFLINE"
     targets:
       accounts: ["<orgname.accountname>"]
     auto_fulfillment:
       refresh_type: SUB_DATABASE
       refresh_schedule: '10 MINUTE'
   $$;
   ```
5. Optional: Let another role alter the listing by granting it MODIFY on the listing. Only the role that owns the listing can grant this
   privilege:

   Copy code

   ```
   GRANT MODIFY ON DATA EXCHANGE LISTING sales_listing TO ROLE listing_editor;
   ```

   To also let `listing_editor` configure auto-fulfillment, ACCOUNTADMIN must grant it MANAGE LISTING AUTO FULFILLMENT on the account.
