# Enable non-ACCOUNTADMIN roles to perform data sharing tasks

This topic lists the minimum privileges required to perform SQL actions related to shares.

By default, the privileges required to create and manage shares are granted only to the ACCOUNTADMIN role, ensuring that only account
administrators can perform these tasks. However, the privileges can also be granted to other roles, enabling the tasks to be delegated to
other users in the account.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

Note

If you grant sharing privileges to other users in the account, make sure that the user profiles for those other users includes a first
name, last name, and an email address. To modify the user profile in Snowsight, see [Add user details to your user profile](/user-guide/ui-snowsight-profile#label-user-details-and-preferences).

## Data providers

To let a role other than ACCOUNTADMIN share data, grant that role the privileges for each sharing task that it performs. The following
table lists the minimum privileges for each task.

| Task | Required privileges | Notes |
| --- | --- | --- |
| Create a share. | CREATE SHARE on the account | Only the ACCOUNTADMIN role has this privilege by default. The role that creates a share owns it (has the OWNERSHIP privilege on it). |
| Grant objects to a share (and revoke them). | Both of the following:   - The privilege on each object that you grant to the share, WITH GRANT OPTION. For example, SELECT on a table WITH GRANT OPTION, plus   USAGE WITH GRANT OPTION on its database and schema. - The ability to resolve the share: either OWNERSHIP on the share or MANAGE GRANTS on the account. | Typical object privileges are:   - USAGE on the database - USAGE on the schema - SELECT on tables, external tables, secure views, or secure materialized views - USAGE on secure UDFs |
| Add or remove the accounts that can access a share (share targets). | Both of the following:   - OWNERSHIP on the share - MANAGE SHARE TARGET on the account | CREATE SHARE doesn’t include this ability. For details, see [MANAGE SHARE TARGET privilege](#label-manage-share-target-privilege). |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

Attention

Granting CREATE SHARE to other roles makes managing shares more flexible, but also allows users with these roles to expose any objects
they own (or on which they have the necessary privileges) to other accounts. This is particularly important to note if you are sharing
data from an account that contains sensitive or proprietary data.

Take this into consideration before granting CREATE SHARE to other roles.

### MANAGE SHARE TARGET privilege

The CREATE SHARE privilege lets a role create shares, but not add or remove the accounts that can access a share (the *share targets*).
To add or remove accounts with [ALTER SHARE](/sql-reference/sql/alter-share), a role needs OWNERSHIP on the share and the global MANAGE SHARE TARGET
privilege.

When the MANAGE SHARE TARGET privilege was introduced, roles that already had CREATE SHARE were automatically granted MANAGE SHARE TARGET
for compatibility. Roles that you grant CREATE SHARE to now don’t receive MANAGE SHARE TARGET automatically; you must grant it
explicitly. For more information, see [New privilege MANAGE SHARE TARGET replaces CREATE SHARE to add accounts to shares](/release-notes/bcr-bundles/2024_07/bcr-1734).

### Steps to enable a non-ACCOUNTADMIN role to share data

The following steps let a custom role named `share_admin` create a share, add a table to it, and share it with consumer accounts. The
table `sales_db.sales_schema.orders` is owned by another role.

1. As ACCOUNTADMIN, grant the account-level sharing privileges to the role, and grant the role to the user who shares data:

   Copy code

   ```
   USE ROLE ACCOUNTADMIN;

   GRANT CREATE SHARE ON ACCOUNT TO ROLE share_admin;
   GRANT MANAGE SHARE TARGET ON ACCOUNT TO ROLE share_admin;

   GRANT ROLE share_admin TO USER <user_name>;
   ```
2. As the role that owns the objects (or another role with the necessary privileges), grant the role the privileges on the objects that
   it shares, WITH GRANT OPTION:

   Copy code

   ```
   USE ROLE <object_owner_role>;

   GRANT USAGE ON DATABASE sales_db TO ROLE share_admin WITH GRANT OPTION;
   GRANT USAGE ON SCHEMA sales_db.sales_schema TO ROLE share_admin WITH GRANT OPTION;
   GRANT SELECT ON TABLE sales_db.sales_schema.orders TO ROLE share_admin WITH GRANT OPTION;
   ```
3. As `share_admin`, create the share. Because `share_admin` creates the share, it owns the share:

   Copy code

   ```
   USE ROLE share_admin;

   CREATE SHARE sales_s;
   ```
4. Grant the objects to the share:

   Copy code

   ```
   GRANT USAGE ON DATABASE sales_db TO SHARE sales_s;
   GRANT USAGE ON SCHEMA sales_db.sales_schema TO SHARE sales_s;
   GRANT SELECT ON TABLE sales_db.sales_schema.orders TO SHARE sales_s;
   ```
5. Add the consumer accounts to the share:

   Copy code

   ```
   ALTER SHARE sales_s ADD ACCOUNTS = <orgname.accountname1>, <orgname.accountname2>;
   ```
6. Optional: Verify the grants on the share:

   Copy code

   ```
   SHOW GRANTS TO SHARE sales_s;
   ```

Note

A role that has MANAGE GRANTS on the account, but doesn’t own the share, can grant objects to the share (step 4). To add or remove
accounts (step 5), use the role that owns the share.

### Blocking access to objects in a share

Access to objects in a share can be blocked by either the role that owns the share or the role that owns the objects:

- If your role owns the share, you can block access by revoking privileges on the objects from the share.
- If your role does not own the share, but owns the objects in the share, you can block access by revoking the USAGE or SELECT privileges
  with CASCADE on the objects from the share owner.

Note

Ownership of a share, as well as the objects in the share, may be either through a direct grant to the role or inherited from a
lower-level role in the role hierarchy. For more details, see
[Role hierarchy and privilege inheritance](/user-guide/security-access-control-overview#label-role-hierarchy-and-privilege-inheritance).

It is possible for the same role to own a share and the objects in the share.

## Data consumers

In a consumer account, the global IMPORT SHARE privilege enables viewing the inbound shares shared with the account. The privilege also
permits creating databases from inbound shares if the role is also granted the global CREATE DATABASE privilege.

### IMPORT SHARE privilege

If the IMPORT SHARE privilege is granted to a role, any user with the role can perform the following tasks:

- View all INBOUND shares (shared by provider accounts).
- View all OUTBOUND shares owned by the role.
- Create databases from inbound shares if the role is also granted the global CREATE DATABASE privilege

### Granting the privilege to another role

To grant the global IMPORT SHARE privilege to a non-ACCOUNTADMIN role in a consumer account, use the ACCOUNTADMIN role and the
[GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege) command.

For example, to grant the privilege to the SYSADMIN role:

Copy code

```
USE ROLE ACCOUNTADMIN;

GRANT IMPORT SHARE ON ACCOUNT TO SYSADMIN;
```
