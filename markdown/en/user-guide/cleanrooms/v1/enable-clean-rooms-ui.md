# Enabling the legacy Snowflake Data Clean Rooms UI

Feature — Generally Available

Currently available in [these regions](/user-guide/cleanrooms/installing-dcr#label-dcr-supported-regions).

Not available in government and VPS deployments.

## Overview

Snowflake Data Clean Rooms can be used in two different environments:

- **The clean rooms UI:** A graphical, no-code, browser-based environment that makes it easy to create and run analyses.
- **The clean rooms API:** A set of stored procedures you can use to create and manage clean rooms and run analyses.

These environments provide similar, but [not exactly equivalent](/user-guide/cleanrooms/getting-started#label-dcr-web-app-api-comparison), capabilities. A clean rooms
administrator installs one or both components in a Snowflake account, and can then grant users access to each environment individually.

## Requirements to enable clean rooms UI for Snowflake Data Clean Rooms

### Account, installer, and user requirements

After you install the clean rooms environment, access to the clean rooms environment must be granted to users explicitly by a clean rooms administrator.

Here are the requirements to enable Snowflake Data Clean Rooms UI in your Snowflake account:

- **The account must allow** [key-pair authentication](/user-guide/cleanrooms/admin-tasks#label-cleanrooms-get-started-key-pair), which is used by the service account
  for authentication.
- **The Snowflake account must be a capacity account:** this is an account that has an up-front
  capacity commitment. Snowflake On-Demand accounts cannot access the clean rooms UI.
- **You must use multi-factor authentication** (MFA) with a
  [supported authenticator app](/user-guide/cleanrooms/web-app-introduction#label-cleanroom-web-app-mfa).

### Role requirements

Here are the role requirements for the person enabling the clean rooms UI:

- You must have an ACCOUNTADMIN role in a Snowflake account and already installed the clean rooms environment in that account.
- The user with the ACCOUNTADMIN role must have a valid first name, last name, and email defined for their user object. To check,
  run [DESCRIBE USER](/sql-reference/sql/desc-user).

## Enable the clean rooms UI

The clean rooms UI provides an easy no-code environment to manage your clean rooms account and create clean rooms and run analyses. It also
provides some [additional functionality](/user-guide/cleanrooms/getting-started#label-dcr-web-app-api-comparison) not available in the clean rooms API, such as scheduled
queries, third-party activation, and useful predefined templates.

Here is how to enable the clean rooms UI in your Snowflake account:

1. **Configure your network policies** to
   [allow the clean rooms UI to access your Snowflake account](/user-guide/cleanrooms/admin-tasks#label-cleanrooms-configure-network-policy).
   (*Required only if your Snowflake account uses a network policy to control network traffic.*)
2. **Complete the UI setup.** This step configures a service user [[\*]](#footnote-*) that the clean rooms UI uses to communicate with Snowflake.

   1. [Sign in to the clean rooms UI](https://cleanroom.c1.us-east-1.aws.app.snowflake.com/) with your Snowflake credentials.
   2. Open **Admin** » **Snowflake Admin** » **Connect to Snowflake account**.
   3. Under **Enable the Data Clean Rooms UI** choose **Quick Setup** or **Manual Setup**:

      - **Quick Setup** - This creates a service user for you. Specify a unique service user name for this account.
      - **Manual Setup** - If you want to create the service user yourself, or reuse an existing service user, select this option. Note
        that clean rooms will take control of the service user and modify it, so make sure that the service user isn’t used for
        anything else. [Learn how to create a service user](#label-dcr-create-service-user-manually).
   4. Enter your unique service user name and select **Finish**.
3. **Provide additional users access to the UI** [Manage UI clean room users](/user-guide/cleanrooms/manage-dcr-users#label-dcr-manage-ui-users) by giving the appropriate privileges to conduct and manage clean room operations via the UI.

[\*]
The service user is configured as follows: Clean rooms sets the type as SERVICE, creates and applies the required network policy
(named SAMOOHA\_SERVICE\_ACCOUNT\_USER\_ACCESS) for the service user, sets the authentication as key-pair, and grants SAMOOHA\_APP\_ROLE to
the service user.

## Troubleshooting installation

Use this section to troubleshoot problems you might have after completing the steps in this topic.

Symptom: Insufficient privileges
:   **Solution:**
    Ensure that the IP addresses associated with the clean rooms UI are allowed by your network policies. For a list of these IP addresses,
    see [Clean rooms UI hosting locations and IP addresses](/user-guide/cleanrooms/web-app-introduction#label-web-app-hosting).

Symptom: Installation is successful, but the clean rooms UI is not functioning properly.
:   **Solution #1:**
    Use the [DESCRIBE USER](/sql-reference/sql/desc-user) command to double-check that the Snowflake user that you used to configure Snowflake has a
    valid first name, last name, and email. If the user is missing any of these, execute the [ALTER USER](/sql-reference/sql/alter-user) command to
    specify them.

    **Solution #2:**
    Try uninstalling the Snowflake Native App for Snowflake Data Clean Rooms, and then re-installing it.

    - To uninstall the app, see
      [Uninstall a Snowflake Native App](https://other-docs.snowflake.com/en/native-apps/consumer-managing-applications#uninstall-a-native-app).
      If you installed the application with its default name, it is called SAMOOHA\_BY\_SNOWFLAKE.
    - To re-install the app:
      1. [Sign in to the clean rooms UI](/user-guide/cleanrooms/web-app-introduction#label-cleanroom-web-app-sign-in).
      2. In the left navigation pane, select **Snowflake Admin**.
      3. Select **Login to Snowflake**, and authenticate as a Snowflake user with the ACCOUNTADMIN role.
      4. Use the [DESCRIBE USER](/sql-reference/sql/desc-user) command to confirm that the Snowflake user with the ACCOUNTADMIN role that you just
         used to authenticate has a valid first name, last name, and email. If the user is missing any of these, execute the
         [ALTER USER](/sql-reference/sql/alter-user) command to specify them.
      5. To install the Snowflake Native App, select **Install**.
      6. Accept the default name of the application during the installation process.

## Creating a UI service user manually

When installing the clean rooms UI, you can either let the installation create the service user for you, or you can provide a service user
that you create. Here is how to create a service user in Snowsight:

Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) with your Snowflake administrator credentials and create a user as shown in the following SQL example:

> Copy code
>
> ```
> -- Create the user.
> -- Clean rooms will set the type to SERVICE for you.
>
> USE ROLE USERADMIN;
> CREATE USER <SERVICE-USER-USERNAME>;
> ```

Important

Clean rooms alters the authentication controls, network policies, and other attributes of the service user. You will not be able to use
this user yourself after you give it to the clean rooms environment.
