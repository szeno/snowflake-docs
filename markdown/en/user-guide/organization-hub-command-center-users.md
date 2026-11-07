# Organization users and user groups

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Use **Organization users and user groups** in Organization Command Center to create organization users and organization
user groups, assign users to groups, and make those groups visible to member accounts. The Command Center landing tile
shows how many organization users, organization user groups, and accounts with group visibility you have.

## Before you begin

Confirm the following:

- You can sign in to the [organization account](/user-guide/organization-accounts) with the GLOBALORGADMIN role.

## Open Organization users and user groups

1. Use [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) to sign in to the organization account.
2. Switch to the GLOBALORGADMIN role.
3. In the navigation menu, select **Organization Hub** » **Command center**.

   On the Command Center landing page, the **Organization users and user groups** tile shows the following:

   - **Org Users**: How many organization users exist in the organization.
   - **Org User Groups**: How many organization user groups exist in the organization.
   - **Accounts**: How many accounts have visibility set for one or more organization user groups.
   - **Guides**: In-product links for **Organization administrators** and **Organization users**.
4. Select **Organization users and user groups**.

## Browse accounts, groups, and users

The page has three lists:

- **Accounts**: Member accounts in the organization. Each row shows the account name and created date. After you make a
  group visible to an account, that account can show **Visible**.
- **Org user groups**: Organization user groups. Each row shows the group name and created date.
- **Org users**: Organization users. Each row shows initials, the user name, and the created date.

Select an account, group, or user to see a summary above the lists. Hover a row for more properties: for a group, users,
accounts, owner, description, and created date; for a user, display name, email, user type, owner, and created date.
Select **Done selecting** to clear the selection.

## Manage users and groups

From this page, you can do the following in Snowsight:

- Create organization users.
- Create organization user groups.
- Assign users to groups, and remove users from groups.
- Assign groups to accounts to make the groups visible, and remove groups from accounts.
- Edit organization users and organization user groups.
- Drop organization users and organization user groups.

For the SQL workflow, including import into member accounts, see
[Organization users](/user-guide/organization-users).

## Create an organization user

1. Select **Create Org user**.
2. In **New organization user**, the owner is GLOBALORGADMIN. Fill in the following:
   - **User name**: Required. Can’t be changed after the user is created.
   - **Email**: Required.
   - **Comment**: Optional.
3. Optionally expand **Advanced user options** to set **Login name**, **Display name**, **First name**, and
   **Last name**.
4. Select **Create user** or **Cancel**.

This dialog doesn’t include a user type control. To create a SERVICE organization user, use SQL. For PERSON and SERVICE
characteristics, see [Organization user types](/user-guide/organization-users#label-org-users-types).

## Create an organization user group

1. Next to **Create Org user**, open the dropdown, then select **Create Org user group**.
2. In **Create Org user group**, enter a **Group name**. Names must be unique in the organization and can contain only
   letters, numbers, and underscores. You can’t change the name after the group is created.
3. Optionally turn on **Can be granted to local roles and users**. When this setting is on, the group can be granted to
   local roles and users within accounts. The setting is off by default. For the matching SQL parameter, see
   [`IS_GRANTABLE`](/sql-reference/sql/create-organization-user-group).
4. Select **Create** or **Cancel**.

After a successful save, Snowsight can show that the group was created successfully.

For the SQL equivalent, see
[Create an organization user group](/user-guide/organization-users#label-org-users-groups-create).

## Assign a group to accounts

Assigning a group to accounts makes that organization user group visible so account administrators can import it. For
the SQL equivalent, see
[Make organization user groups available to regular accounts](/user-guide/organization-users#label-org-users-groups-visibility).

1. In **Org user groups**, select a group.
2. Select **…**, then select **Assign to accounts**.
3. In **Assign groups to accounts**, use **All** or **Selected**, and **Search by account name or region**, to choose
   accounts. The table lists **Account**, **Edition**, **Cloud**, **Region**, and **Created**.
4. Select **Assign** or **Cancel**.

After a successful save, Snowsight can show **Account visibility updated** for the group. Assigned accounts can
show **Visible** in the **Accounts** list.

The same menu also includes **Edit**, **Remove from accounts**, **Manage org users**, and **Drop Organization user
group**. **Remove from accounts** is unavailable when the group isn’t visible in any accounts.

## Edit an organization user group

1. In **Org user groups**, select a group.
2. Select **…**, then select **Edit**.
3. In **Edit Organization user group**, review **Group name**. You can turn **Can be granted to local roles and users**
   on or off.
4. Select **Save** or **Cancel**.

## Assign a user to groups

1. In **Org users**, select a user.
2. Select **…**, then select **Assign to groups**.
3. In **Assign users to groups**, use **All** or **Selected**, and **Search by group name**, to choose groups. The table
   lists **Group**, **Comment**, **Users**, **Accounts**, and **Created**.
4. Select **Assign** or **Cancel**.

After a successful save, Snowsight can show that the user was assigned to the selected groups. The user summary
updates the group count.

The same menu also includes **Edit**, **Remove from groups**, and **Drop**. **Remove from groups** is unavailable when
the user isn’t in any groups.

For the SQL equivalent, see
[Add organization users to an organization user group](/user-guide/organization-users#label-org-users-groups-add).

## Edit an organization user

1. In **Org users**, select a user.
2. Select **…**, then select **Edit**.
3. In **Edit organization user**, you can change **Email** and **Comment**. **User name** can’t be changed after the
   user is created.
4. Optionally expand **Advanced user options**. **Login name** also can’t be changed after the user is created. You can
   change **Display name**, **First name**, and **Last name**.
5. Select **Save** or **Cancel**.

## What to do next

After a group is visible to a member account, an administrator in that account imports the group and resolves conflicts.
See [Import users in a regular account](/user-guide/organization-users#label-org-users-add).

## Access control requirements

Organization users and user groups in Command Center requires the GLOBALORGADMIN role. ORGANIZATION\_USAGE application
roles can open [Insights](/user-guide/organization-hub-insights), but they can’t open Command Center or this tile.
