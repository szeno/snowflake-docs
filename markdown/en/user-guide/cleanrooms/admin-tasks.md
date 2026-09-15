# Snowflake Data Clean Rooms: Administrator tasks

End-of-life notice

The legacy Provider and Consumer Data Clean Rooms are being discontinued. Migrate to the
[Collaboration API](/user-guide/cleanrooms/overview) using the
[migration tool](/user-guide/cleanrooms/migration-tool) before the dates below.

- **2026-10-01:** New legacy clean rooms may not be created via the
  [web application user interface](/user-guide/cleanrooms/v1/web-app-introduction).
- **2027-02-01:** The [web application user interface](/user-guide/cleanrooms/v1/web-app-introduction)
  will no longer be accessible, and new legacy clean rooms may not be created via the
  [Provider and Consumer API](/user-guide/cleanrooms/getting-started).
- **2027-06-01:** Legacy [Provider and Consumer clean rooms](/user-guide/cleanrooms/getting-started)
  will no longer be accessible. Use the [Collaboration API](/user-guide/cleanrooms/overview)
  to create and manage clean rooms.

This topic describes the tasks for the administrator of a Snowflake Data Clean Room. For information about installing the clean room environment
in your Snowflake account, see [Installing the Snowflake Data Clean Rooms environment](/user-guide/cleanrooms/installing-dcr).

## Updating the clean rooms environment

Snowflake Data Clean Rooms updates their binaries weekly to support new features, procedures, and UI updates. You can find release notes for
significant new releases in the [feature updates section](/release-notes/new-features#label-new-features-features) of the Snowflake release notes page (search
for “clean rooms”).

### Clean rooms UI updates

The clean rooms UI environment is updated automatically by Snowflake; all users need to do to get the
updated version is sign out and sign back in to the clean rooms UI.

### Clean rooms API updates

A clean rooms administrator can either enable automatic API updates (recommended) or update the API environment manually for each new
release, as described next.

#### Automatic API updates

A clean rooms API administrator can enable clean rooms updates to be installed automatically upon release by running the following SQL commands once in their account:

Copy code

```
USE ROLE SAMOOHA_APP_ROLE;
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.library.enable_local_db_auto_upgrades();
```

Clean rooms API users in that account will see the updates shortly when they are rolled out, without needing to log out.

#### Manual API updates

We recommend enabling automatic clean room updates for your account. But if you prefer to update your account’s API environment manually, you can do so by running the following SQL commands each time you want to update the environment:

Copy code

```
USE ROLE SAMOOHA_APP_ROLE;
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.library.apply_patch();
```

You can find your release number by running the following SQL command:

Copy code

```
SELECT * FROM SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.ADMIN.VERSION;
```

## Using a different warehouse

Clean rooms come with [several warehouses](/user-guide/cleanrooms/v1/installation-details#label-cleanrooms-installation-details-warehouses) that can access the API. Choose the
warehouse that is appropriate for your needs. You can also choose a custom warehouse size for specific actions, such as for
[provider activation](/user-guide/cleanrooms/provider#label-dcr-api-provider-update-activation-warehouse).

However, your clean room can use any warehouse you choose, if you grant USAGE and OPERATE privileges on that warehouse to the
SAMOOHA\_APP\_ROLE role.

For example, to add a warehouse `my_big_warehouse` that can be used to run analyses, execute the following commands from a worksheet:

Copy code

```
USE ROLE ACCOUNTADMIN;

CREATE WAREHOUSE my_big_warehouse WITH WAREHOUSE_SIZE = X5LARGE;
GRANT USAGE, OPERATE ON WAREHOUSE my_big_warehouse TO ROLE SAMOOHA_APP_ROLE;
```

## Monitor clean rooms UI activity

An administrator can track what users are doing in the clean rooms UI by monitoring the query history in your Snowflake account.

To access the query history for your clean room environment, do one of the following, depending on whether you want to use SQL or
Snowsight:

SnowsightSQL

You can identify UI traffic as queries where the `user_name` is the name of the service
user that was created when the [Snowflake account was configured](/user-guide/cleanrooms/v1/enable-clean-rooms-ui#label-dcr-install-clean-rooms-ui-step).

1. Sign in the Snowflake account associated with your clean room environment as a user with the ACCOUNTADMIN role.
2. In the navigation menu, select **Monitoring** » **Query History**.
3. Use the **User** filter to select the service account user associated with the clean room environment.

When using SQL, you can identify UI traffic where `query_tag_details:request_type = DCR` or where `user_name =` the name of the
[UI service user](#label-dcr-manage-service-user).

You can further filter queries by the `user_email` query tag to see only actions performed by the specified user in the UI.

Execute queries against the [QUERY\_HISTORY view](/sql-reference/account-usage/query_history) in SNOWFLAKE.ACCOUNT\_USAGE.

For example, to trace the clean rooms UI activity of the user `joe@example.com`, execute the following code:

Copy code

```
SELECT *,
  TRY_PARSE_JSON(query_tag) AS query_tag_details
  FROM snowflake.account_usage.query_history
  WHERE query_tag_details IS NOT NULL
    AND query_tag_details:request_type = 'DCR'
    AND query_tag_details:user_email = 'joe@example.com';
```

## Monitor provider-run analyses

A provider-run analysis refers to the process of a provider creating and sharing a clean room, then running an analysis in the clean room
after the consumer links their data. These analyses run in the consumer’s account, not the provider’s. This section describes how the
consumer can track the queries executed by the provider’s analyses in the clean room.

Snowflake Data Clean Rooms assigns a query tag to each query executed for a provider-run analysis. This query tag takes the form
`cleanroom_UUID_provider_account_locator`. A consumer can retrieve all queries associated with provider-run analyses by searching
for the query tag in the query history of their account.

To retrieve the query, first obtain the UUID for a clean room, then search for the query tag. In the following code, replace
`cleanroom_name` and `provider_account_locator` with the appropriate values.

Copy code

```
-- Retrieve clean room UUID
SELECT cleanroom_id FROM samooha_by_snowflake_local_db.public.cleanroom_record
  WHERE cleanroom_name = '<cleanroom_name>';

-- Retrieve queries with provider-run query tag
SELECT * FROM snowflake.account_usage.query_history
  WHERE query_tag = cleanroom_id || '<provider_account_locator>;
```

You can also use Snowsight to filter the query history by the appropriate query tag after using SQL to retrieve the clean room UUID.

## Customize available connectors

Connectors let you integrate your clean room environment with your ecosystem partners. As the clean room administrator for a provider, you
can customize the clean room environment to limit which connectors appear as options for the clean room user. For example, if you have a
single preferred activation partner, you can configure the clean room environment so that the partner is the only option when a consumer
activates the results of an analysis in a clean room.

Note

Your customizations apply to new clean rooms only.

To control which connectors are available in a clean room, you need the MANAGE\_DCR\_CONNECTORS role.

1. [Sign in to the clean rooms UI](/user-guide/cleanrooms/web-app-introduction#label-cleanroom-web-app-sign-in).
2. In the left navigation, select **Admin** » **Profile & Features**.
3. Optional: To customize activation connectors, follow these steps:

   1. On the **Activation** tile, select **Edit**.
   2. Select which activation options you want to display, and then select **Save**.
4. Optional: To customize identity and data provider connectors, follow these steps:

   1. On the **Identity & Data Provider** tile, select **Edit**.
   2. Select which identity options you want to display, and then select **Save**.

## Brand your clean rooms

You can configure a profile for your clean room environment so every clean room created is branded with your logo and company name. To
define the logo and name for your company, you need the MANAGE\_DCR\_PROFILE\_AND\_FEATURES role.

1. [Sign in to the clean rooms UI](/user-guide/cleanrooms/web-app-introduction#label-cleanroom-web-app-sign-in).
2. In the left navigation, select **Admin** » **Profile & Features**.
3. In the **Company profile** section, do the following:
   1. Upload a logo for your company in JPG or PNG format. This logo will appear on every clean room that is created.
   2. Edit the **Company Name** to define the name that you want to appear on the clean rooms that are created in your environment.

## Enable single sign-on (SSO)

To enable single sign-on (SSO) with Snowflake Authentication, contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).
**An account must use Snowflake authentication to enable SSO**; if you aren’t using it yet,
[migrate to Snowflake authentication](/user-guide/cleanrooms/update-to-oauth) before requesting SSO.

## Allow key-pair authentication

The service account user that the clean room environment uses to communicate with your Snowflake account uses
[key-pair authentication](/user-guide/key-pair-auth) to authenticate. If your Snowflake account uses [authentication policies](/user-guide/authentication-policies)
to control how users authenticate, then the authentication policy controlling the service account user must allow key-pair authentication.

To allow key-pair authentication, either remove all authentication policies, or add an authentication policy with `AUTHENTICATION_METHODS = ALL`
or `AUTHENTICATION_METHODS = KEYPAIR`. If your Snowflake account has an account-level authentication policy that does not allow key-pair
authentication, you need to create a new authentication policy with the appropriate parameter, then assign the policy to the service
account user that was created during the installation process.

You can check your authentication policies by running this command:

Copy code

```
SHOW AUTHENTICATION POLICIES;
```

An empty results table indicates no policies, which means that key-pair authentication is allowed.

## Manage the service user

The clean rooms UI uses a service user account as an intermediary to perform most clean room actions. You can modify the key or switch
the clean rooms service user after it has been created or added to your account using the clean rooms UI as described in this section.

You can find information about the service user under **Snowflake Admin** » **Snowflake** » **Service User Management**.

Important

Change the clean rooms service user only using the clean rooms UI. If you modify the service user outside of the UI, clean rooms might no
longer be able to access the service user.

### Change the service user

If you want to change the service user name or use a new service user (essentially the same thing):

1. Open **Snowflake Admin** » **Service User Management** and select [![Edit icon](/static/images/cleanrooms/icons/edit_icon_material_symbol.svg)](/static/images/cleanrooms/icons/edit_icon_material_symbol.svg) (Edit).
2. Change the name of the service user to a user that you have [created](/user-guide/cleanrooms/v1/enable-clean-rooms-ui#label-dcr-create-service-user-manually) and is accessible in
   the current account.
3. Select **Reauthenticate** to open a confirmation dialog.
4. Read the information in the dialog, then select **Confirm** to start using that agent.

### Change the service user key

If you want to change your service user RSA key, you should do so as described next. If you change the key outside of the clean room
environment, you will no longer be able to use most UI functionality until you change the service user key back as described next.

1. Open **Snowflake Admin** » **Service User Management** and select [![Edit icon](/static/images/cleanrooms/icons/edit_icon_material_symbol.svg)](/static/images/cleanrooms/icons/edit_icon_material_symbol.svg) (Edit).
2. Select **Reauthenticate** near the manual setup section to open a confirmation dialog.
3. Read the information in the dialog, then select **Confirm** to generate a new RSA key.

You can see information about the service agent’s public key by running the following SQL command, substituting in your service user’s name
where indicated:

Copy code

```
DESCRIBE USER <service_user_name> ->>
  SELECT *
    FROM $1
      WHERE "property" ILIKE 'RSA_PUBLIC_KEY%';
```

Clean rooms doesn’t support key rotation using [RSA\_PUBLIC\_KEY\_2](/user-guide/key-pair-auth#label-key-pair-rotation), so ignore the information about RSA\_PUBLIC\_KEY\_2.

## Enable or disable activation in the clean room UI

Activation when using the clean room UI is controlled globally by a clean room administrator. Activation in the clean room API is controlled
at the clean room level by the provider.

This section shows how to enable or disable activation when using the clean room UI. To learn how to enable activation when using the API,
read the [activation instructions](/user-guide/cleanrooms/activation).

Provider and consumer activation are enabled by default in your clean room account when using the clean room UI. Third-party activation
must be enabled manually.

Here is how to enable or disable activation for UI users in your account:

1. [Sign in to the clean room environment in the clean rooms UI](/user-guide/cleanrooms/web-app-introduction#label-cleanroom-web-app-sign-in) as a DCR administrator.
2. Select **Admin** » **Profile & Features**.
3. In the **Activation** section, select **Edit**.
   - To manage **consumer activation**: Check or clear the checkbox next to **Collaborator Account**.
   - To manage **provider activation**: Check or clear the checkbox next to your own account name.
   - To manage **third-party activation**: Check or clear the checkbox next to the third-party activation target you wish to enable or
     disable. Third-party activation is enabled through connectors, and is available only in the clean room UI.
     [See the list of available third party connectors](/user-guide/cleanrooms/connector-activation).

[Learn how to implement activation in a clean room.](/user-guide/cleanrooms/activation)

## Configure network policies

If your Snowflake account uses a [network policy](/user-guide/network-policies) to control network traffic, you must explicitly allow
traffic from the IP addresses that the clean rooms UI uses to communicate with your Snowflake account.

Find the IP addresses used for your region in the **IP network addresses used by clean rooms UI** column in the [IP address table](/user-guide/cleanrooms/web-app-introduction#label-web-app-hosting).

## See details about the service account for this environment

The clean rooms UI uses a service account to communicate with Snowflake. This service account was created by the account administrator
when they installed the Clean Room environment for this account.

You cannot modify details about the service account user.

To see details about the service account for this Clean Room environment you need the MANAGE\_DCR\_PROFILE\_AND\_FEATURES role.

2. Navigate to **Admin > Snowflake Admin**.
3. On the **Snowflake Admin** page you can see information such as the service user name and service user email.
