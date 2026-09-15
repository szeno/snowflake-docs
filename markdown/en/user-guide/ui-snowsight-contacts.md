# Set up and manage notification contacts for Snowflake

Snowflake sends security, privacy, and product notifications via email. You can use Snowsight to set up and manage which
notifications you want to be sent to which email addresses in your organization. You can set up notifications at the
Snowflake organization level or the account level.

## About notification contacts for Snowflake

To receive security, privacy, and product notifications from Snowflake, specify the email addresses to receive those notifications in the
**Notification Contacts** page of Snowsight.

Setting up contacts depends on your role:

- Users without the ACCOUNTADMIN role or the ORGADMIN role cannot view **Contacts**.
- If the ORGADMIN role is granted to your user, you can view and set up contact information for the organization.
- If the ACCOUNTADMIN role is granted to your user, you can view and set up contact information for a specific account.
  If no contacts are provided at the account level, notification contacts set at the organization level are used.
  If you have the ACCOUNTADMIN role but are not granted the ORGADMIN role, you cannot see notification contacts set up at the organization
  level.

If you have privileges to do so, you can set up notification contacts for your entire Snowflake organization, or configure specific
notification contacts for each account. You can specify multiple email addresses for each type of notification.

The following notification types are sent by Snowflake:

- Security notifications
- Privacy notifications
- Product notifications, including:
  - Behavior change notifications, such as upcoming behavior changes that might affect your account. See [About Behavior Changes](/release-notes/intro-bcr-releases).
  - Driver support notifications, such as notifications related to client versions and driver support. See [Client versions & support policy](/release-notes/requirements).
  - Operational status notifications, such as notifications related to [Snowflake’s operational status](https://status.snowflake.com/).
  - Time-sensitive notifications, such as notifications that might require immediate attention or action.

Emails are sent in accordance with the [Snowflake Privacy Notice](https://www.snowflake.com/privacy-policy/).

## Set up notification contacts for Snowflake

To set up notification contacts for Snowflake, you must be granted the ACCOUNTADMIN role or the ORGADMIN role.

Set up notification contacts:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Profile** » **Settings** » **Admin contacts**.
3. If you have the ORGADMIN role, you see the **Organization** tab. If you want to specify account-level notification contacts, select
   **Account**.
4. For each type of notification that you want to set up, select **Edit** or the pencil icon.
5. Add one or more email addresses, pressing Enter to add each address. You cannot use commas to separate multiple email addresses.
6. Select **Save** to save the email addresses as notification contacts.

Note

When logging into Snowsight, users with the ACCOUNTADMIN or ORGADMIN role will receive a prompt to add any missing critical contact
emails or update outdated ones.

### Example: Set up separate time sensitive notifications

For example, if you want the Snowflake administrators to get all product notifications, but want the on-call Snowflake administrators to
see the time-sensitive notifications, do the following:

- For **Product Notifications**, enter the email address: `snowflake-admin-info@example.com`.
- For **Time Sensitive Notifications**, enter the email address: `snowflake-admin-oncall@example.com`.

In this example, all product notifications, including the time-sensitive notifications, are sent to `snowflake-admin-info@example.com`.
Only the time-sensitive notifications are sent to the on-call administrators.

### Example: Set up different email addresses for each notification type

Alternatively, if you want different groups to get different types of notifications, you could set up notification contacts differently:

- For **Product Notifications**, enter the email address: `snowflake-admin-info@example.com` to get all product
  notifications including the Behavior Change notifications, Driver Support notifications, Operational Status notifications, and Time
  Sensitive notifications.
- For **Behavior Change Notifications**, enter the email address: `snowflake-admin-testing@example.com` to send behavior change
  emails to the administrators responsible for testing Snowflake.
- For **Driver Support Notifications**, enter the email address: `snowflake-admin-connect@example.com` to send client version and
  driver support details to the team responsible for maintaining the clients and drivers that people in your organization use to connect to Snowflake.
- For **Operational Status Notifications**, enter the email address: `snowflake-users@example.com` to send all Snowflake users
  status messages about Snowflake, to reduce the number of questions sent to your team.
- For **Time Sensitive Notifications**, enter the email address: `snowflake-admin-oncall@example.com` to alert the administrators
  on call about any time-sensitive issues.

### Example: Set up some organization-level and some account-level notifications

If you want one group to get all product notifications for the entire organization, the privacy testing group to get specific notifications
for the VPS account in your organization, and the analyst testing group to get specific notifications for your other account, you could do
something like the following example:

- On the **Organization** tab, for **Product Notifications**, enter the email address: `snowflake-admin-org@example.com`.
- As a user signed in to the VPS account that is granted the ACCOUNTADMIN role, go to the **Account** tab. In the
  **Behavior Change Notifications** section, enter the email address: `snowflake-admin-vps-account-testing@example.com`.
- As a user signed in to the other account that is granted the ACCOUNTADMIN role, go to the **Account** tab. In the
  **Behavior Change Notifications** section, enter the email address: `snowflake-admin-testing@example.com`.

In this example, the administrators for the entire Snowflake organization get all product notifications for all accounts in the organization,
and the testing groups for each account get the behavior change notifications for the accounts that they manage.
