# Email notifications for Trust Center findings

Using the Trust Center Snowsight interface, you can configure the Trust Center to send email
notifications when its scanners generate findings. You can specify that the Trust Center sends notifications for all of the
enabled scanners in a scanner package or for individual scanners. You can also specify the severity of the
findings for which email notifications are sent.

Note

Email notifications are processed through Snowflake’s Amazon Web Services (AWS) deployments, using AWS Simple Email Service
(SES). The content of an email message sent using AWS may be retained by Snowflake for up to thirty days to manage the delivery
of the message. After this period, the message content is deleted.

Note

Snowflake trial accounts can’t use this feature to send email notifications.

## Email notification recipients

For a scanner package or individual scanner, the Trust Center can send email notifications to users
with [verified email addresses](#label-email-notification-trust-center-verify-address). When you
configure notifications, you can specify the users who will receive the email notifications:

- **Admin users**

  > The Trust Center sends notifications to administrative users who are
  > [configured to receive security notifications](/user-guide/ui-snowsight-contacts).
  >
  > When this option is selected, the Trust Center sends notifications to users in the following order:
  >
  > 1. The security notification contact at the organization level.
  > 2. If no security notification contact at the organization level is found, the security notification contact at the account level.
  > 3. If no security notification contact at the organization level is found, the ACCOUNTADMIN users with
  >    [verified email addresses](#label-email-notification-trust-center-verify-address).
  >
  > Note
  >
  > When an organization account and a customer account within that organization are located in different deployments,
  > Security Updates emails configured at the organization level are not visible from the customer account.
- **Custom**
  The Trust Center sends notifications to a custom list of users. Add each user who should receive notifications
  to the list. You can remove a user from the list by selecting the trash can icon associated with the user.

The Trust Center can send email notifications to at most 50 users.

Attention

By default, the **Security Essentials** scanner package sends email notifications to
**Admin users with verified email addresses** for findings at the critical severity level. By default,
the **Security Essentials** scanners run once a month. When a scanner runs, it sends an
email notification to the configured recipients every time it generates a finding at or above the threshold level.

By default, email notifications aren’t sent for other scanner packages or scanners.

You can modify the email notifications settings for scanner packages and for individual scanners.

## Verifying the email addresses of the email notification recipients

The Trust Center can send email notifications only to users who verify their email addresses in Snowsight. For more information,
see [Snowsight (the Snowflake web interface)](/user-guide/ui-snowsight-profile#label-snowsight-verify-email-address).

## Managing email notifications for a scanner package

Complete the following tasks to manage email notifications for a scanner package:

- [Configure email notifications for a scanner package](#label-email-notification-trust-center-scanner-package-configuring)
- [Turn off email notifications for a scanner package](#label-email-notification-trust-center-scanner-package-turning-off)

### Configure email notifications for a scanner package

A scanner package must be enabled before you can configure email notifications for it. For information about
enabling a scanner package, see [Enable scanner packages](/user-guide/trust-center/using-the-trust-center#label-trust-center-enable-scanner-packages).

When you configure email notifications for a scanner package, the Trust Center sends notifications for all of the enabled
scanners in the package.

To configure email notifications for a scanner package, complete the following steps:

1. [Sign in to Snowsight](/user-guide/connecting#label-sign-in-using-snowsight).
2. Switch to a role with the [SNOWFLAKE.TRUST\_CENTER\_ADMIN](/user-guide/trust-center/overview#label-trust-center-requirements) application role granted to it.

   For more information about granting these roles, see [Required roles](/user-guide/trust-center/overview#label-trust-center-requirements).
3. In the navigation menu, select **Governance & security** » **Trust Center**.
4. Select the **Manage scanners** tab.
5. Select a scanner package from the list.
6. Select the **Settings** tab.
7. Under **Notifications**, select one of the following:

   - If notifications are turned off for the scanner package, select **Set up notification**.
   - If notification are turned on for the scanner package, select the edit icon.
8. Set the **Minimum severity level trigger**.

   The Trust Center sends email notifications for findings at the specified level or higher. For example, if
   the **Minimum severity level trigger** is set to **Medium**, the Trust Center sends findings with a severity of
   medium, high, or critical, but not low.
9. For **Recipients**, select **Admin users** or **Custom**. For more information,
   see [Email notification recipients](#label-email-notification-trust-center-email-notification-recipients).
10. To save your changes, select **Done**, or select **Cancel** to cancel them.

### Turn off email notifications for a scanner package

When you turn off email notifications for a scanner package, you can’t enable email notifications for individual
scanners in the package.

To turn off email notifications for a scanner package, complete the following steps:

1. [Sign in to Snowsight](/user-guide/connecting#label-sign-in-using-snowsight).
2. Switch to a role with the [SNOWFLAKE.TRUST\_CENTER\_ADMIN](/user-guide/trust-center/overview#label-trust-center-requirements) application role granted to it.

   For more information about granting these roles, see [Required roles](/user-guide/trust-center/overview#label-trust-center-requirements).
3. In the navigation menu, select **Governance & security** » **Trust Center**.
4. Select the **Manage scanners** tab.
5. Select a scanner package from the list.
6. Select the **Settings** tab.
7. Under **Notifications**, select the edit icon.
8. Select **Turn off notification**, and then select **Turn off** in the confirmation window.

   If email notifications aren’t turned on for the scanner package, the **Turn off notification**
   button doesn’t appear.

## Managing email notifications for a scanner

Complete the following tasks to manage email notifications for a scanner:

- [Configure email notifications for a scanner](#label-email-notification-trust-center-scanner-configuring)
- [Turn off email notifications for a scanner](#label-email-notification-trust-center-scanner-turning-off)

### Configure email notifications for a scanner

The following conditions must be met before you can configure email notifications for a scanner:

- The scanner must be enabled. For information about enabling a scanner, see
  [Enable or disable a scanner in a scanner package](/user-guide/trust-center/using-the-trust-center#label-trust-center-enable-disable-scanner).
- The scanner’s package must have email notifications enabled. For more information, see
  [Configure email notifications for a scanner package](#label-email-notification-trust-center-scanner-package-configuring).

To configure email notifications for a scanner, complete the following steps:

1. [Sign in to Snowsight](/user-guide/connecting#label-sign-in-using-snowsight).
2. Switch to a role with the `SNOWFLAKE.TRUST_CENTER_ADMIN` application role granted to it.

   For more information about granting this role, see [Required roles](/user-guide/trust-center/overview#label-trust-center-requirements).
3. In the navigation menu, select **Governance & security** » **Trust Center**.
4. Select the **Manage scanners** tab.
5. Select a scanner package from the list.
6. Select [![trust center vertical more image](/static/images/ui-trust-center-vertical-more.png)](/static/images/ui-trust-center-vertical-more.png) **More** for the scanner, and then select **Edit notification**.
7. Specify whether to inherit the email notification from the scanner package:

   - To inherit the email notification configuration from the scanner package, select
     **Use the same trigger and recipients as package notification**.
   - To specify a notification configuration that’s different from the scanner package, make sure
     **Use the same trigger and recipients as package notification** isn’t selected, and then set
     the **Minimum severity level trigger** and **Recipients** for the scanner:
     1. Set the **Minimum severity level trigger**.

        The Trust Center sends email notifications for findings at the specified level or higher. For example, if
        the **Minimum severity level trigger** is set to **Medium**, the Trust Center sends findings
        with a severity of medium, high, or critical, but not low.
     2. For **Recipients**, select **Admin users** or **Custom**. For more information,
        see [Email notification recipients](#label-email-notification-trust-center-email-notification-recipients).
8. To save your changes, select **Done**, or select **Cancel** to cancel them.

### Turn off email notifications for a scanner

To turn off email notifications for a scanner, complete the following steps:

1. [Sign in to Snowsight](/user-guide/connecting#label-sign-in-using-snowsight).
2. Switch to a role with the `SNOWFLAKE.TRUST_CENTER_ADMIN` application role granted to it.

   For more information about granting this role, see [Required roles](/user-guide/trust-center/overview#label-trust-center-requirements).
3. In the navigation menu, select **Governance & security** » **Trust Center**.
4. Select the **Manage scanners** tab.
5. Select a scanner package from the list.
6. Select [![trust center vertical more image](/static/images/ui-trust-center-vertical-more.png)](/static/images/ui-trust-center-vertical-more.png) **More** for the scanner, and then select **Edit notification**.
7. Select **Turn off notification**, and then select **Turn off** in the confirmation window.

   If email notifications aren’t turned on for the scanner, the **Turn off notification**
   button doesn’t appear.
