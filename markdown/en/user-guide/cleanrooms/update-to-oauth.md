# Update the clean room UI to Snowflake authentication

Feature — Generally Available

Currently available in [these regions](/user-guide/cleanrooms/installing-dcr#label-dcr-supported-regions).

Not available in government and VPS deployments.

Important

If you installed the Snowflake Data Clean Rooms application after May 1, you don’t need to read this article.

The Problem
:   Before May 1, 2025 users signed into the clean rooms UI using their clean room credentials. On May
    1, Snowflake authentication became the default credentials used in new clean room UI installations, but not for older installations.

The Solution
:   Administrators who installed the clean room UI before May 1, 2025 need to migrate their clean rooms account to start using Snowflake
    authentication by the end of April, 2026. This is done using a small, simple wizard that appears when you sign in to clean rooms with an
    account that has administrator privileges.

The wizard walks you through three simple steps:

## 1. Download the current UI user list

In this step you will grant the appropriate role-based access to the clean room UI to your users.

1. **Download the list of current clean room UI users.** The report includes the following fields:

   - `Email`: The email address associated with the account in the old clean rooms authorization system.
   - `Users on Snowflake`: The Snowflake username associated with `Email`.
   - `Name`: The name associated with `Email` in the old clean room authorization system.
   - `DCR role`: The old DCR UI persona for this user. One of the following values:
     - **DCR Admin** - Maps to MANAGE\_DCR\_PROFILE\_AND\_FEATURES, MANAGE\_DCR\_CONNECTORS, and MANAGE\_DCR\_COLLABORATORS privileges.
     - **Clean room manager** - Maps to MANAGE\_CLEANROOMS privilege.
2. **Go through each row in the list** and grant proper Snowflake clean room privileges to each user:

   - For each row, check the `Users on Snowflake` value:

     - **If one user is listed,** grant the [appropriate privileges](/user-guide/cleanrooms/manage-dcr-users#label-dcr-manage-ui-users) to the username in `Users on Snowflake`.
     - **If multiple users are listed,** grant the [appropriate privileges](/user-guide/cleanrooms/manage-dcr-users#label-dcr-manage-ui-users) to each user individually.
       However, only the first user who logs in after migration can see the query history. If you need to change who sees the query
       history for a given account, contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).
     - **If no users are listed,** and you know who this user is based on their email, grant the user the
       [appropriate privileges](/user-guide/cleanrooms/manage-dcr-users#label-dcr-manage-ui-users) in Snowflake. (Before the change, you could access the clean room UI
       without having a Snowflake account if a clean rooms manager invited you.)
   - If a user is not listed here who should have access to the clean room UI, grant the user the
     [appropriate privileges](/user-guide/cleanrooms/manage-dcr-users#label-dcr-manage-ui-users) in Snowflake.

Note

If there are users whose clean room UI email does not exactly match their Snowflake account email, or if multiple users used the same
email address, they might [encounter problems](#label-dcr-oauth-migration-problems).

## 2. Test your own access

To test whether you can open the clean rooms UI with your Snowflake credentials, select **Test Login** and provide Snowflake credentials
for any account that should be able to access this clean room UI.

Important

When you test user credentials, the response shows which [clean room privileges](/user-guide/cleanrooms/manage-dcr-users#label-dcr-manage-ui-users) will be granted to this user after migration (or ALL, which means ACCOUNTADMIN). **Confirm that the privilege list is not empty**, and that it **matches the privileges you expect** . If the privileges are not what you expect or want, grant the appropriate clean room privileges to that user in Snowflake.

## 3. Migrate

Switch the clean room UI sign in to Snowflake authentication for your account. That’s it
– you’re done! The clean room UI sign in process should now be the same for Snowsight and the clean room UI. No need
to take any special steps if you are using SSO.

Remember that you must switch your clean room UI to use Snowflake authentication by the end of April, 2026.

## Analysis and query history migration details

If you do not see your clean room report history after logging in to the clean room UI, here are the possible reasons:

- Reports are migrated for a clean room account upon first login after migration. If you don’t see reports at first, wait a bit to see if
  the reports appear in your clean room account.
- You have not verified ownership of the Snowflake email address now associated with your clean room account. If this is the case,
  [verify your email address](/user-guide/ui-snowsight-profile#label-snowsight-verify-email-address) in Snowflake.
- If multiple users referenced the same Snowflake email in the old clean room UI, only the first user to log in to the clean room UI
  after migration has access to the reports. If you need to switch the reports to another user, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Here are more details about the migration process:

The clean room UI previously used email addresses as a user credential. After migration, the clean room UI uses Snowflake user IDs. The system tries to find an exact match between an old clean room email addresses and a Snowflake user ID email address when migrating clean room reports.

The first time each user logs in to the clean room UI after migration, their query report history is associated with the Snowflake email
as long as the following criteria are met:

- The user has the same email on Snowflake as used in the clean room UI
- The user’s email is verified in Snowflake.

If user does not have a Snowflake email, or the Snowsight email is not verified, the reports will not be moved over.
