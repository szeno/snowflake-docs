# Leaked password protection

Leaked password protection is a background service in Snowflake that monitors and disables passwords that have been leaked to help prevent
unauthorized access to Snowflake accounts. The leaked password protection service provides a notification system for administrators so they
are aware of leaked passwords when they are detected in external databases.

This topic provides the following information:

- [Discovering leaked passwords](#label-leaked-password-protection-discovering-leaked-passwords)
- [Email notifications](#label-leaked-password-protection-email-notifications)
- [Types of users scanned](#label-leaked-password-protection-types-of-users-scanned)
- [Reset a user password](#label-leaked-password-protection-reset-a-user-password)
- [Reset an admin password](#label-leaked-password-protection-reset-an-admin-password)

## Discovering leaked passwords

If Snowflake discovers a leaked password, then Snowflake identifies which user the password is associated with,
and then securely verifies whether or not the user can still use the leaked password to authenticate.

If the user can authenticate with the leaked password, Snowflake disables the leaked password by unsetting the password for the user, and
rejecting the use of the leaked password by that user in the future. After disabling the leaked password, the user cannot authenticate using
their password, but the user can use other methods of authentication, such as SSO, if available.

Snowflake then notifies the administrator and user about the leaked password through email. Snowflake also provides a message to the
affected user during login time, telling them they must contact their account administrator to send them a reset link to change their
password. The user’s new password must meet the requirements of the password policies set on the account.

If Snowflake identifies that the leaked password is an administrator password, and no other administrators can reset the password, the
administrator must contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Leaked password protection is enabled by default, and you cannot disable leaked password protection.

Note

Snowflake only processes passwords in-memory, and does not store passwords in cleartext. Snowflake employees cannot view passwords.

## Email notifications

When Snowflake discovers a leaked password, Snowflake attempts to notify email addresses in the following order:

1. If one or more [verified email addresses](/user-guide/notifications/email-notifications#label-email-notification-verify-address) for account-level security notifications is
   found, then Snowflake notifies the verified email addresses.
2. If one or more verified email addresses for account-level security notifications are not found, then Snowflake attempts to look for and
   notify email addresses at the organization level.
3. If email addresses at the organization level are not found, Snowflake contacts users with admin roles.

For more information about notification contacts for Snowflake, see [Set up and manage notification contacts for Snowflake](/user-guide/ui-snowsight-contacts).

## Types of users scanned

All [user types](/user-guide/admin-user-management#label-user-management-types) are scanned, and Snowflake can disable any user’s password if the user has a password.

## Reset a user password

If Snowflake blocks a user from authenticating with a password, then the user must ask their administrator to
[reset their password](/user-guide/password-authentication#label-user-management-reset-password).

## Reset an admin password

If Snowflake blocks a user from authenticating with a password, then the user must ask their administrator to reset their password.

If no other administrator is available to reset the password of another administrator, then the administrator must contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).
