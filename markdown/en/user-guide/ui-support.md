# Manage Snowflake Support cases

If you have a verified email address and sufficient privileges to create, view, and manage Snowflake Support cases, you can do so
using the **Support** page in Snowsight.

## Verify your email address

Before you can access the Support system, you must verify your email:

In some cases, you automatically receive an email prompting you to **Please Validate Your Email**. If you didn’t, follow these
steps to verify your email address:

1. sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. in the lower-left corner, select your name » **Settings**.
3. In **My Profile**, configure your email address:

   - If you don’t have an email address listed, enter an email address in the **Email** field, and then select **Save**.
   - If you can’t enter an email address, an account administrator must either add an email address on your behalf or grant your user
     the role with the OWNERSHIP privilege on your user.
   - If you didn’t receive an email, select **Resend verification email**. Snowflake sends a verification email to the address listed.
4. Open your email, and then select the link in the email to validate your email address.

## Privileges required to access the Support system

By default, users with the organization administrator (ORGADMIN) or account administrator (ACCOUNTADMIN) roles can access the Support system.

If you want users with a custom role to access the Support system, a user with an administrator role must grant one or more global
privileges to that custom role.

The following table describes the available privileges and indicates the system role that has each privilege by default:

| Privilege | Description | Granted to system role |
| --- | --- | --- |
| MANAGE ORGANIZATION SUPPORT CASES | Grants the ability to view, comment on, and manage all Support cases for the organization. | ORGADMIN |
| MANAGE ACCOUNT SUPPORT CASES | Grants the ability to view, comment on, and manage all Support cases for the current account. | ACCOUNTADMIN |
| MANAGE USER SUPPORT CASES | Grants the ability to view, comment on, and manage all Support cases that were opened by the current user. | ACCOUNTADMIN |

Expand

Show lessSee more

Snowflake recommends that you grant the MANAGE ORGANIZATION SUPPORT CASES privilege to a role for users that require the broadest
historical view of support cases in your organization.

### Grant access to the Support system to individual users

Only organization administrators (users with the ORGADMIN role) can grant the MANAGE ORGANIZATION SUPPORT CASES privilege to roles.

Only account administrators (users with the ACCOUNTADMIN role) can grant either the MANAGE ACCOUNT SUPPORT CASES or MANAGE USER SUPPORT
CASES privilege to roles.

To grant one or more of the privileges to a custom role, run a
[GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege) statement or use Snowsight.

For example, grant the MANAGE USER SUPPORT CASES privilege to the role `myrole`:

> Copy code
>
> ```
> GRANT MANAGE USER SUPPORT CASES ON ACCOUNT TO ROLE myrole;
> ```

## Managing Support cases

When accessing the Support system for the first time, a user must select **Enable Support**.

### Create Support cases

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the lower-left corner, select your name » **Support**.
3. Select **+ Support Case**.
4. Complete and submit the form. Provide as much useful information as possible to help Snowflake Support resolve your issue.
5. Optionally, add Snowflake users as *watchers* to your case to receive email notifications when the case is updated or comments are added.
   To add a user as a watcher, the user must have enabled the **Support** page, or have a registered user account in the Snowflake Community.
   If you add a watcher who has a role with [sufficient privileges](#label-snowsupport-privileges), they can also view, comment on,
   and modify the case.

Important

It is your responsibility to ensure that no confidential information, export-controlled data, personal data, sensitive data, or other
regulated data is entered into the form. Ensure that the information submitted is not “Customer Data” as defined in the Snowflake Terms
of Service or any other agreement between you and Snowflake covering use of the Snowflake Service.

#### Create a Support case during an incident

During an incident, click **Create Case** on the incident banner in Snowsight to quickly create a related Support case. The summary, category, and sub-category fields are pre-filled to streamline the process.

- In Snowsight, select **Support** from the bottom navigation bar to view your Support cases. The **Support Cases** page displays new or ongoing incident summaries and their status.

### Attach files to Support cases

You can attach a maximum of 30 files to a Support case.

Each attachment must be no more than 2GB, and file names for attachments must be no more than 255 characters in length, including the
file extension.

File attachments must use one of the following file types:

- `gz`
- `gzip`
- `jpeg`
- `jpg`
- `log`
- `png`
- `txt`
- `zip`

### View and update a Support case

To review an open or closed Support case:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the lower-left corner, select your name » **Support**.
3. In the table of Support cases, select the row for the case that you want to view. The case details page opens.

   You can add comments to the case to answer questions or provide additional details.

### Escalate a Support case

If your case requires expedited resolution, [escalate](https://community.snowflake.com/s/article/Escalate-Button-FAQ) the case:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the lower-left corner, select your name » **Support**.
3. In the table of Support cases, select the row for the case that you want to escalate. The case details page opens.
4. Select **Escalate Case**.
5. Complete and submit the form.

### Resolve a Support case

When your business needs related to this case have been resolved, mark the case as resolved:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the lower-left corner, select your name » **Support**.
3. In the table of Support cases, select the row for the case that you want to resolve. The case details page opens.
4. Select **Resolve Case**.
5. Confirm that you want to resolve the case.

   The case is closed.

### Add watchers to a case

You can add users as watchers to an active case, or when you [create the case](#label-creating-support-cases). You can only add other
Support-enabled users as watchers. Your privileges determine the watchers available to you:

- Users with a role granted the [MANAGE ACCOUNT SUPPORT CASES](#label-snowsupport-privileges) and
  [MANAGE USER SUPPORT CASES](#label-snowsupport-privileges) privileges can add any support-enabled user in an account as a watcher.
- Users with a role granted the [MANAGE ORGANIZATION SUPPORT CASES](#label-snowsupport-privileges) privilege can add any
  support-enabled users from any account in their organization as a watcher.

To add watchers to a case:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the lower-left corner, select your name » **Support**.
3. In the table of Support cases, select the row for the case that you want to view. The case details page opens.
4. On the right side of the case details page, select **Watchers**.
5. Select the users that you want to add as watchers.

Important

In order to view Support cases as a watcher, a user added as a watcher must be granted a role with the MANAGE ACCOUNT SUPPORT CASES
privilege. See [Privileges required to access the Support system](#label-snowsupport-privileges).
