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

Data providers can choose either of the following options to add objects to a share:

- **Option 1:** Create a database role in a database, grant privileges on objects to the database role, and then grant the database role to
  the share.
- **Option 2:** Grant privileges on the database and database objects directly to the share.

For more information on these options, see [How to share database objects](/user-guide/data-sharing-gs#label-data-sharing-share-options).

The minimum privileges required to create and manage shares in a data provider or data consumer account depend on which option was used.

Option 1:
:   | Action | Privilege | Object | Notes |
    | --- | --- | --- | --- |
    | Create shares. | CREATE SHARE | Account | Only the ACCOUNTADMIN role has this privilege by default. The privilege can be granted to additional roles as needed. |
    | Create database roles in a database. | CREATE DATABASE ROLE | Database | Only the database owner role (i.e. the role that has the OWNERSHIP privilege on the database) has this privilege by default. The privilege can be granted to additional roles as needed. |

    Expand

    Show lessSee more

Option 2:
:   | Action | Privilege | Object | Notes |
    | --- | --- | --- | --- |
    | Create shares. | CREATE SHARE | Account | Only the ACCOUNTADMIN role has this privilege by default. The privilege can be granted to additional roles as needed. |
    | Grant or revoke privileges on objects to or from a share. | OWNERSHIP | Share | This role must also have, at a minimum, the following privileges on the database objects with the grant option:   - USAGE on the database - USAGE on the schema - SELECT on any tables, external tables, secure views, or secure materialized views - USAGE on any secure UDFs |

    Expand

    Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

Attention

Granting CREATE SHARE to other roles makes managing shares more flexible, but also allows users with these roles to expose any objects
they own (or on which they have the necessary privileges) to other accounts. This is particularly important to note if you are sharing
data from an account that contains sensitive or proprietary data.

Take this into consideration before granting CREATE SHARE to other roles.

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
