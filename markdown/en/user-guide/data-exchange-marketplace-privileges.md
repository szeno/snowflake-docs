# Grant privileges to other roles

Snowflake provides a set of privileges for working with listings in the Snowflake Marketplace or a Data Exchange.

## Granting administrator privileges in a Data Exchange

By default, only an account administrator (a user with the ACCOUNTADMIN role) in the Data Exchange administrator account can manage a
Data Exchange, which includes the following tasks:

- Add or remove members.
- Approve or deny listing approval requests.
- Approve or deny provider profile approval requests.
- Show categories.

To support delegating these tasks to other users, the IMPORTED PRIVILEGES privilege can be granted on a Data Exchange to other roles.

### Granting the IMPORTED PRIVILEGES privilege to other roles

To grant the IMPORTED PRIVILEGES privilege on a Data Exchange to a role, use the ACCOUNTADMIN role and the
[GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege) command.

Note

The WITH GRANT OPTION parameter does not support the IMPORTED PRIVILEGES privilege.

Syntax:

Copy code

```
GRANT IMPORTED PRIVILEGES ON DATA EXCHANGE <exchange_name> TO <role_name>;
```

Where:

- `exchange_name` is the name of a Data Exchange.
- `role_name` is the role to which the privilege is granted.

For example, grant imported privileges on the `mydataexchange` Data Exchange to a custom role called `myrole`:

Copy code

```
USE ROLE ACCOUNTADMIN;

GRANT IMPORTED PRIVILEGES ON DATA EXCHANGE mydataexchange TO myrole;
```

### Usage notes

- This privilege is granted at the Data Exchange level. Therefore, users with the role can only administer the Data Exchange for which the
  privilege has been granted.
- Only an account administrator in the Data Exchange administrator account can grant the privilege to another role.
- When a role has been granted IMPORTED PRIVILEGES on a database created from a share, subsequent calls to the
  [SHOW GRANTS](/sql-reference/sql/show-grants) command list the privilege as USAGE and **not** IMPORTED PRIVILEGES.
- This privilege can only be used for a Data Exchange. In the Snowflake Marketplace, only Snowflake administrators can perform administrative tasks.

## Granting provider privileges to other roles in the Snowflake Marketplace or a Data Exchange

Snowflake provides a set of privileges to allow providers to perform various tasks related to sharing data and apps with specific consumers,
on the Snowflake Marketplace, or data in a Data Exchange.

| Privilege | Object Type | Can be Granted by | Description |
| --- | --- | --- | --- |
| [Global CREATE LISTING privilege](#label-create-data-exchange-listing-on-account) | ACCOUNT | ACCOUNTADMIN | Grants the ability to create a listing or provider profile. |
| [CREATE SHARE privilege](#label-create-share-on-account) | ACCOUNT | ACCOUNTADMIN | Grants the ability to create a share. |
| [IMPORT SHARE privilege](#label-import-share-on-account) | ACCOUNT | ACCOUNTADMIN | Grants the ability to view an inbound share shared with the account and create a database from the share. |
| [PURCHASE DATA EXCHANGE LISTING privilege](#label-purchase-data-exchange-listing-account) | ACCOUNT | ACCOUNTADMIN | Grants the ability to purchase a paid listing. |
| [MODIFY privilege on a listing](#label-modify-on-data-exchange-listing) | LISTING | Role with the OWNERSHIP privilege on the listing. | Grants the ability to modify listing properties. |
| [USAGE privilege on a listing](#label-usage-on-data-exchange-listing) | LISTING | Role with the OWNERSHIP privilege on the listing. | Grants the ability to view a listing. |
| [OWNERSHIP privilege on a listing](#label-ownership-on-data-exchange-listing) | LISTING | Role with the OWNERSHIP privilege on the listing. | Grants the ability to transfer the OWNERSHIP privilege on the listing. |
| [MODIFY privilege on a provider profile](#label-modify-on-provider-profile) | PROVIDER PROFILE | Role with the OWNERSHIP privilege on the profile. | Grants the ability to modify properties for a provider profile. |
| [OWNERSHIP privilege on a provider profile](#label-ownership-on-provider-profile) | PROVIDER PROFILE | Role with the OWNERSHIP privilege on the profile. | Grants the ability to transfer the OWNERSHIP privilege on the profile. |

Expand

Show lessSee more

### Account-level privileges

Snowflake provides the following privileges for working with shares, listings, and provider profiles at the account level in the
Snowflake Marketplace or a Data Exchange:

- [Global CREATE LISTING privilege](#label-create-data-exchange-listing-on-account)
- [CREATE SHARE privilege](#label-create-share-on-account)
- [IMPORT SHARE privilege](#label-import-share-on-account)

#### Global CREATE LISTING privilege

If the global CREATE LISTING privilege is granted to a role, any user with the role can create a listing or provider profile.
As the creator and therefore owner of the listing, the role can be used to perform all tasks on the listing, including:

- Create listings.
- Modify listing properties.
- View listings.
- View incoming listing requests.
- Reject listing requests.
- Submit listings for approval.
- Publish a listing.
- Create and view provider profiles.
- View offers.
- View pricing plans.

If an account is a provider in more than one Data Exchange, a role with the global CREATE LISTING privilege can create listings
in each of those Data Exchanges.

Note

- A role that creates a listing becomes the owner of the listing. The OWNERSHIP privilege can be transferred using
  [OWNERSHIP privilege on a listing](#label-ownership-on-data-exchange-listing) to a different role by the owning role.
- Only account administrators (users with the ACCOUNTADMIN role) can grant the global CREATE LISTING privilege to a role.

To grant the global CREATE LISTING privilege to a role in a Data Exchange, use the
[GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege) [WITH GRANT OPTION] command.

For example, use the ACCOUNTADMIN role to grant the privilege:

Copy code

```
USE ROLE ACCOUNTADMIN;
```

Then grant the privilege to a custom role, `myrole`:

Copy code

```
GRANT CREATE LISTING ON ACCOUNT TO ROLE myrole;
```

Then grant the privilege to the role `myrole` with grant option:

Copy code

```
GRANT CREATE LISTING ON ACCOUNT TO ROLE myrole WITH GRANT OPTION;
```

#### CREATE SHARE privilege

If the CREATE SHARE privilege is granted to a role, any user with the role can create a share. As the creator and therefore owner of the
share, the role can also be used to perform all tasks on the share, including:

- Granting privileges on objects to or revoking privileges on objects from the share.
- Adding accounts to or removing consumer accounts from the share.

For more information, see [Enable non-ACCOUNTADMIN roles to perform data sharing tasks](/user-guide/security-access-privileges-shares).

#### IMPORT SHARE privilege

If the IMPORT SHARE privilege is granted to a role, any user with the role can perform the following tasks:

- View all INBOUND shares (shared by provider accounts).
- View all OUTBOUND shares owned by the role.
- Create databases from inbound shares if the role is also granted the global CREATE DATABASE privilege.

For more information, see [Enable non-ACCOUNTADMIN roles to perform data sharing tasks](/user-guide/security-access-privileges-shares).

#### PURCHASE DATA EXCHANGE LISTING privilege

If the PURCHASE DATA EXCHANGE LISTING privilege is granted to a role, any user with the role can purchase a listing shared privately or
on the Snowflake Marketplace.

For more information about purchasing listings, see
[Becoming a consumer of listings](/collaboration/consumer-becoming).

For more information about this privilege, see [Enable non-ACCOUNTADMIN roles to perform data sharing tasks](/user-guide/security-access-privileges-shares).

### Listing-level privileges

Snowflake provides the following privileges for listings. You can only grant these privileges using the role granted the OWNERSHIP privilege
on the listing.

- [MODIFY privilege on a listing](#label-modify-on-data-exchange-listing)
- [USAGE privilege on a listing](#label-usage-on-data-exchange-listing)
- [OWNERSHIP privilege on a listing](#label-ownership-on-data-exchange-listing)

#### MODIFY privilege on a listing

If the MODIFY privilege on a listing is granted to a role, any user with the role can perform the following tasks for a listing:

- Modify listing properties.
- View a listing.
- View incoming listing access requests.
- Submit a listing for approval.
- Publish a listing.
- Reject listing requests.

Only the role with the OWNERSHIP privilege on the listing can grant this privilege.

To grant the MODIFY privilege on a listing shared with specific consumers or published on the Snowflake Marketplace:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Provider Studio**.
3. Select **Listings**.
4. Locate the listing that you want to modify and select the row to open the listing details.
5. In the listing details page, select **Settings**.
6. In the **Privileges** section, select the pencil icon next to the **Usage** privilege.
7. Select **Add Role** and add required roles.
8. Save your changes.

To grant the MODIFY privilege on a listing in a Data Exchange:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Data sharing** » **External sharing**.
3. Select **Shared by your account**.
4. Locate the listing that you want to modify and select the row to open the listing details.
5. In the listing details page, select **Settings**.
6. In the **Privileges** section, select the pencil icon next to the **Usage** privilege.
7. Select **Add Role** and add required roles.
8. Save your changes.

#### USAGE privilege on a listing

If the USAGE privilege on a listing is granted to a role, any user with the role can view listings and incoming listing requests.
Only the role with the OWNERSHIP privilege on the listing can grant this privilege.

To grant the USAGE privilege on a listing shared with specific consumers or published on the Snowflake Marketplace:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Provider Studio**.
3. Select **Listings**.
4. Locate the listing that you want to modify and select the row to open the listing details.
5. In the listing details page, select **Settings**.
6. In the **Privileges** section, select the pencil icon next to the **Ownership** privilege.
7. Select **Add Role** and add required roles.
8. Save your changes.

To grant the USAGE privilege on a listing in a Data Exchange:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Data sharing** » **External sharing**.
3. Select **Shared by your account**.
4. Locate the listing that you want to modify and select the row to open the listing details.
5. In the listing details page, select **Settings**.
6. In the **Privileges** section, select the pencil icon next to the **Ownership** privilege.
7. Select **Add Role** and add required roles.
8. Save your changes.

#### OWNERSHIP privilege on a listing

If the OWNERSHIP privilege on a listing is granted to a role, that role becomes the new OWNER of the listing. Only the OWNER of the listing
can grant this privilege. OWNERSHIP is a special type of privilege that can only be granted from one role to another role; it cannot be
revoked. For more details, see [Overview of Access Control](/user-guide/security-access-control-overview).

Important

When listing ownership is transferred, all existing grants get revoked. All roles that have been granted privileges immediately lose access to this listing, and their privileges are revoked. The new listing owner must re-grant these privileges.

To grant the OWNERSHIP privilege on a listing shared with specific consumers or published on the Snowflake Marketplace:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Provider Studio**.
3. Select **Listings**.
4. Locate the listing that you want to modify and select the row to open the listing details.
5. In the listing details page, select **Settings**.
6. In the **Privileges** section, select the pencil icon next to the **Modify Listing** privilege.
7. Select **Add Role** and add required roles.
8. Save your changes.

To grant the OWNERSHIP privilege on a listing in a Data Exchange:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Data sharing** » **External sharing**.
3. Select **Shared by your account**.
4. Locate the listing that you want to modify and select the row to open the listing details.
5. In the listing details page, select **Settings**.
6. In the **Privileges** section, select the pencil icon next to the **Modify Listing** privilege.
7. Select **Add Role** and add required roles.
8. Save your changes.

### Provider profile level privileges

Snowflake provides the following privileges for provider profiles. Only the role with the OWNERSHIP privilege on the provider profile
can grant this privilege.

- [MODIFY privilege on a provider profile](#label-modify-on-provider-profile)
- [OWNERSHIP privilege on a provider profile](#label-ownership-on-provider-profile)

Note

- To create a profile, use the [Global CREATE LISTING privilege](#label-create-data-exchange-listing-on-account) global privilege.
- Any role in the provider account can view all profiles. This task does not require granting a privilege.

#### MODIFY privilege on a provider profile

If the MODIFY privilege is granted to a role on a provider profile, any user with the role can view and modify provider profile properties.
Only the role with the OWNERSHIP privilege on the provider profile can grant this privilege.

The MODIFY privilege can be granted through the web interface or using SQL:

> [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in):
> :   In the navigation menu, select **Data sharing** » **Internal sharing** » **Manage Exchanges** » Select an Exchange » Select a Provider Profile » **Manage** » **Manage Profile Editors**.
>
> SQL:
> :   Execute the [GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege) [WITH GRANT OPTION] command.
>
> For example, to grant the privilege to the custom role `myrole`:
>
> Copy code
>
> ```
> GRANT MODIFY ON DATA EXCHANGE PROFILE "<provider_profile_name>" TO ROLE myrole;
> ```

#### OWNERSHIP privilege on a provider profile

If the OWNERSHIP privilege on a provider profile is granted to a role, that role becomes the new owner of the profile. Only the role with
the OWNERSHIP privilege on the provider profile can grant this privilege.

OWNERSHIP is a special type of privilege that can only be granted from one role to another role; it cannot be revoked.
For more details, see [Overview of Access Control](/user-guide/security-access-control-overview).

To grant the OWNERSHIP privilege on a provider profile to a role, use the [GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege) [WITH GRANT OPTION]
command. You cannot use Snowsight to grant this privilege.

For example, to grant the privilege to the custom role `myrole`:

Copy code

```
GRANT OWNERSHIP ON DATA EXCHANGE PROFILE "<provider_profile_name>" TO ROLE myrole;
```
