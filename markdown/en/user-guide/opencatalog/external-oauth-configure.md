# Configure External OAuth in Snowflake Open Catalog

Feature — Generally Available

Not available in government regions.

This topic describes how to configure external servers that use OAuth for accessing Snowflake Open Catalog.

Note

This topic shows you how to use Auth0 to configure External OAuth for Open Catalog. However, the steps for configuring it in Okta or
Microsoft Entra ID are similar.

## Prerequisites

- Create one or more catalogs in your Open Catalog account.
- Ensure that you have an account with an identity provider (IdP). For demonstration purposes, this topic uses Auth0 as the IdP. To create an Auth0
  account for your company or organization, see <https://auth0.com/>. However, the process is similar for Okta and Microsoft Entra ID.
- You must have [Snowflake CLI](https://docs.snowflake.com/en/developer-guide/snowflake-cli/installation/installation) installed on your machine.
- To configure External OAuth, you must have the service admin role in Open Catalog. For more information, see [User roles](https://other-docs.snowflake.com/en/opencatalog/access-control#user-roles). In Snowflake CLI, this role is printed as POLARIS\_ACCOUNT\_ADMIN.

## Before you begin

To configure External OAuth, you need to create a Snowflake CLI connection for Open Catalog.

In order to create this connection, you need your full Open Catalog account identifier, which includes your Snowflake organization name and
your Open Catalog account name; for example: `<orgname>.<my-snowflake-open-catalog-account-name>`.

- To find your *Snowflake* organization name (`<orgname>`), see [Finding the organization and account name for an account](/user-guide/admin-account-identifier#label-account-name-find).
- To find your *Snowflake Open Catalog* account name (`<my-snowflake-open-catalog-account-name>`), see
  [Find the account name for a Snowflake Open Catalog account](/user-guide/opencatalog/find-account-name).

## Create a Snowflake CLI connection

Create a Snowflake CLI connection for your Open Catalog account so you can use it to configure external OAuth for the account.

### Step 1: Add a Snowflake CLI connection for Snowflake Open Catalog

- [Add a connection](/developer-guide/snowflake-cli/connecting/configure-connections#label-snowcli-snow-connection-command-add)
  with the following values. For all other parameters, press `Enter` to skip specifying a value for the parameter.

  | Connection configuration parameters | Value |
  | --- | --- |
  | **Name for this connection** | Specify a name for the connection; for example, `myopencatalogconnection`. |
  | **Account name** | Specify your Snowflake organization name, followed by your Open Catalog account name, in this format:  `<orgname>-<my-snowflake-open-catalog-account-name>`.  For example, `ABCDEFG-MYACCOUNT1`.  To find these names, see [Before you begin](#before-you-begin). |
  | **Username** | Specify your username for Open Catalog; for example, `jsmith`. |
  | **Password [optional]** | This parameter is *not* optional when you create a connection for Open Catalog.  Enter your password for Open Catalog; for example, `MyPassword123456789`. |
  | **Role for the connection [optional]** | This parameter is *not* optional when you create a connection for Open Catalog.  You must enter `POLARIS_ACCOUNT_ADMIN` |

  Expand

  Show lessSee more

### Step 2: Test the Snowflake CLI connection

- To test your CLI connection, follow this example, which tests the connection for `myopencatalogconnection`:

  Copy code

  ```
  snow connection test -c myopencatalogconnection
  ```

  The response should look like this:

  Copy code

  ```
  +------------------------------------------------------------------------------+
  | key              | value                                                     |
  |----------------------------+-------------------------------------------------|
  | Connection name  | myopencatalogconnection                                   |
  | Status           | OK                                                        |
  | Host             | ABCDEFG-MYACCOUNT1.snowflakecomputing.com                 |
  | Account          | ABCDEFG-MYACCOUNT1                                        |
  | User             | jsmith                                                    |
  | Role             | POLARIS_ACCOUNT_ADMIN                                     |
  | Database         | not set                                                   |
  | Warehouse        | not set                                                   |
  +------------------------------------------------------------------------------+
  ```

### Step 3: Set a default Snowflake CLI connection

To ensure that the connection you’re using always has the required POLARIS\_ACCOUNT\_ADMIN role granted to it, you can set the Snowflake CLI
connection you created for Open Catalog as the default connection. For more information about the default connection, see
[label-cli\_set\_default\_connection](/developer-guide/snowflake-cli/connecting/configure-connections#label-cli-set-default-connection).

1. Follow this example, which sets the `myopencatalogconnection` connection as the default:

   Copy code

   ```
   snow connection set-default myopencatalogconnection
   ```
2. To confirm that you’re using the correct user and role, run the following:

   Copy code

   ```
   snow sql -q "Select current_user(); select current_role();"
   ```

   The response should return your Open Catalog username and the CURRENT
   ROLE should be POLARIS\_ACCOUNT\_ADMIN.

   Copy code

   ```
   +----------------+
   | CURRENT_USER() |
   |----------------|
   | JSMITH        |
   +----------------+
   select current_role();
   +-----------------------+
   | CURRENT_ROLE()        |
   |-----------------------|
   | POLARIS_ACCOUNT_ADMIN |
   +-----------------------+
   ```

## Step 1: Set up Auth0 as an External OAuth authorization server

In this section, you set up Auth0 as an External OAuth authorization server. However, the steps for setting up Microsoft Entra ID or Okta as
an External OAuth authorization server are similar.

Note

To create an Auth0 account for your company or organization, see <https://auth0.com/>.

### Define an API

Define an API so you can assign permissions to it.

1. Sign in to the Auth0 console.
2. In the left pane, select **Applications** > **APIs**.
3. Select **+ Create API**.
4. Enter a **Name** and **Identifier**, and accept the default settings.
5. Select **Create**.

### Add permissions to the API

Add permissions to the API so you can grant them to the client.

This client will be the principal in Open Catalog and the permission you assign to it will be a principal role in Open Catalog.

1. Sign in to the Auth0 console.
2. In the left pane, select **Applications** > **APIs**.
3. Select your API.
4. On the **Permissions** tab, add permissions:

   1. Use the **Permission** and **Description** fields to add permissions for your API. Use the
      format `SESSION:ROLE:<custom_role_name>`. For example: `SESSION:ROLE:ENGINEER`.

Important

To [generate your service admin access token](#step-4-generate-your-service-admin-access-token), you must add the
`SESSION:ROLE:POLARIS_ACCOUNT_ADMIN` permission, which allows you to assign the service admin role in Open Catalog with
permissions to the API.

1. Select **+ Add**.

### Create an application

Create applications so that you can grant them permissions to the API you created.

1. Sign in to the Auth0 console.
2. In the left pane, select **Applications** > **Applications**.
3. Select **+ Create Application** and create an application. Repeat this step toe create each application you need for configuring
   External OAuth.

Important

Make sure you create an application for generating the service admin access token. Later, you’ll
grant the `SESSION:ROLE:POLARIS_ACCOUNT_ADMIN` permission to it.

### Assign permissions to the API

Follow these steps to select the permissions that you want to grant to the client:

1. Sign in to the Auth0 console.
2. In the left pane, select **Applications** > **Applications**.
3. Select the application you created.
4. Select the **APIs** tab.
5. If needed, select the **Authorized** toggle for your API to On.
6. Select the **Expand** icon for your API.
7. In the **Permissions** field, select the check box for each permission you want to assign to the API.
8. Select **Update**.

   Repeat these steps for each application you created.

Important

Make sure you select the application you created for generating the service admin access token and assign the `SESSION:ROLE:POLARIS_ACCOUNT_ADMIN`
permission to the API. Otherwise, you can’t generate the service admin access token.

## Step 2: Retrieve your organization and account name

You need your organization name and Snowflake Open Catalog account name, separated by a hyphen, for tasks such as creating a security
integration.

1. To retrieve your organization name and Snowflake Open Catalog account name in this format, in Snowflake CLI, run the following command:

   Copy code

   ```
   snow sql -q "SELECT CURRENT_ORGANIZATION_NAME() || '-' || CURRENT_ACCOUNT_NAME();"
   ```
2. In the response, copy the returned values and paste them into a text editor for later use. For example: `ABCDEFG-MYACCOUNT1`.

## Step 3: Create a security integration

To create a security integration, run the CREATE SECURITY INTEGRATION command by using a Snowflake CLI connection.

Copy code

```
snow sql -q "create or replace security integration external_oauth_auth0
   type = external_oauth
   enabled = true
   external_oauth_type = custom
   external_oauth_issuer = 'https://<Auth0_domain>/'
   external_oauth_jws_keys_url = 'https://<Auth0_domain>/.well-known/jwks.json'
   external_oauth_audience_list = ('https://<your_org_name>-<your_open_catalog_account_name>.snowflakecomputing.com')
   external_oauth_token_user_mapping_claim = 'sub'
   external_oauth_snowflake_user_mapping_attribute = 'login_name'
   EXTERNAL_OAUTH_SCOPE_DELIMITER = ' '
   EXTERNAL_OAUTH_SCOPE_MAPPING_ATTRIBUTE = 'scope';"
```

Where:

- `<Auth0_domain>` is your Auth0 domain. To find this value, in Auth0, navigate to Applications > Applications >
  [Name of your application] > Settings > **Domain** field.
- `<your_org_name>-<your_open_catalog_account_name>` is your organization name and Snowflake Open Catalog account name, separated by
  a hyphen.

  For example: `ABCDEFG-MYACCOUNT1`.

  To retrieve these values in this format, see [Retrieve your organization and account name](#step-2-retrieve-your-organization-and-account-name).

## Step 4: Generate your service admin access token

To configure External OAuth programmatically, you need a service admin access token. However, you have the option to use the Open Catalog UI
to perform some tasks for configuring External OAuth.

If you already generated a service admin access token for yourself and it’s still active, you can skip this step.

To generate your service admin access token, in Snowflake CLI, execute the following command and copy the value into a text editor:

Copy code

```
ACCESS_TOKEN=$(curl -X POST https://<Auth0_domain>/oauth/token --header 'content-type: application/x-www-form-urlencoded' --data grant_type=client_credentials --data client_id=<client_id> --data client_secret=<client_secret> --data-urlencode "audience=https://<your_org_name>-<your_open_catalog_account_name>.snowflakecomputing.com" --data "scope=SESSION:ROLE:POLARIS_ACCOUNT_ADMIN" | jq -r '.access_token')
```

Where:

- `<Auth0_domain>` is your Auth0 domain. To find this value, in Auth0, navigate to Applications > Applications >
  [Name of your application] > Settings > **Domain** field.
- `<client_id>`is the client ID for your application in Auth0 that you grant access to the POLARIS\_ACCOUNT\_ADMIN privilege. To find this
  value, in Auth0, navigate to Applications > Applications >
  [Name of your application] > Settings > **Client ID** field.
- `<client_secret>` is the client secret for your application in Auth0 that you grant access to the POLARIS\_ACCOUNT\_ADMIN privilege. To
  find this value, in Auth0, navigate to Applications > Applications >
  [Name of your application] > Settings > **Client Secret** field.
- `<audience>` is the identifier for your API. To find this value, in Auth0, navigate to Applications > APIs > select your API > Settings >
  **Identifier** field.
- `<your_org_name>-<your_open_catalog_account_name>` is your organization name and Snowflake Open Catalog account name, separated by
  a hyphen.

  For example: `ABCDEFG-MYACCOUNT1`.

  To retrieve these values in this format, see [Retrieve your organization and account name](#step-2-retrieve-your-organization-and-account-name).
- `POLARIS_ACCOUNT_ADMIN` is the name of the built-in role in Open Catalog that allows you to perform administrative tasks in Open
  Catalog, which includes configuring External OAuth. In the Open Catalog UI, this role is referred to as the service admin role.

## Step 5: Create a custom role

In this step, you use your Snowflake CLI connection to create a custom role.

Create a custom role so that later, you can grant catalog roles to it and grant the custom role to a service principal, which bestows the
service principal with privileges. For more information about custom roles, see [Custom role](access-control#custom-role). For more
information on the RBAC model in Open Catalog, see [RBAC model](./access-control#rbac-model).

Note

If the default Snowflake CLI connection that you set doesn’t have the POLARIS\_ACCOUNT\_ADMIN role granted to it, you must include the
following statement with your command: `USE ROLE POLARIS_ACCOUNT_ADMIN`.

The following example creates an `OPEN_CATALOG_ADMIN` custom role:

Copy code

```
snow sql -q "create role OPEN_CATALOG_ADMIN;"
```

## Step 6: Grant a catalog role to a custom role

In this section, you grant a catalog role to the custom role you created.

After you grant a catalog role to the custom role, you then grant the custom role to a service principal to bestow the service principal
with any privileges granted to catalog roles that are granted to the principal role. For more information on the RBAC model in Open Catalog,
see [RBAC model](./access-control#rbac-model).

You can grant the custom role with a catalog role that has catalog admin privileges for the catalog or has a set of
privileges for the catalog that you specify:

- If you want to grant a service principal with catalog admin privileges to a catalog,
  [grant a catalog role with catalog admin privileges to the custom role](#grant-a-catalog-role-with-catalog-admin-privileges-to-the-custom-role). For information on what privileges a catalog admin has, see [Catalog admin role](access-control#catalog-admin-role).
- If you want to grant the service principal with a set of privileges you specify,
  [grant a catalog role with a set of privileges you specify to the custom role](#grant-a-catalog-role-with-a-set-of-privileges-you-specify-to-the-custom-role).
  For example, choose this option if you want to grant a cataLog\_reader, catalog\_writer, or catalog\_metadata\_reader catalog role to the
  custom role.

### Grant a catalog role with catalog admin privileges to the custom role

In this section, you grant a catalog role with catalog admin privileges to the custom role. The workflow is as follows:

1. [Create a catalog role](#create-a-catalog-role).
2. [Grant catalog admin privileges to the catalog role](#grant-catalog-admin-privileges-to-the-catalog-role).
3. [Grant the catalog role to a custom role](#grant-the-catalog-role-to-a-custom-role).

#### Create a catalog role

curlApache Polaris (Incubating) CLIOpen Catalog UI

Run the following command to create a catalog role in the catalog you specify:

> Copy code
>
> ```
>  curl -X POST \
> "https://<your_org_name>-<your_open_catalogaccount_name>.snowflakecomputing.com/polaris/api/management/v1/catalogs/{catalogName}/catalog-roles" \
> -H "Authorization: Bearer <service_admin_access_token>" \
> -H "Content-Type: application/json" \
> -H "Accept: application/json" \
> -d '{
>    "name": "<catalog_role_name>"
>    }'
> ```
>
> Where:
> :   - `<your_org_name>-<your_open_catalogaccount_name>` is your organization name and Snowflake Open Catalog account name, separated by a hyphen.
>
>       For example: `ABCDEFG-MYACCOUNT1`.
>
>       To retrieve these values in this format, see [Step 2: Retrieve your organization and account name](#label-retrieve-org-account-name-external-oauth).
>     - `{Catalogname}` is the name of the catalog in Open Catalog where you want to create a catalog role.
>     - `<service_admin_access_token>` is the [service admin access token you generated](#label-generate-service-admin-access-token-external-oauth).
>     - For `<catalog_role_name>` specify a name for the catalog role. For example: CatalogAdmin.

See [Catalog](https://github.com/Snowflake-Labs/polaris-cli-opencatalog-demo?tab=readme-ov-file#catalog-1) in Snowflake Labs.

See See [Create a catalog role](/user-guide/opencatalog/create-catalog-role).

#### Grant catalog admin privileges to the catalog role

curlApache Polaris (Incubating) CLIOpen Catalog UI

Run the following command:

> Copy code
>
> ```
> curl -X PUT \
> "https://<your_org_name>-<your_open_catalogaccount_name>.snowflakecomputing.com/polaris/api/management/v1/catalogs/{catalogName}/catalog-roles/{catalogRoleName}/grants" \
> -H "Authorization: Bearer <service_admin_access_token>" \
> -H "Content-Type: application/json" \
> -H "Accept: application/json" \
> -d '{"grant": {"type": "catalog", "privilege": "CATALOG_MANAGE_CONTENT"}}'
> ```
>
> Where:
> :   - `<your_org_name>-<your_open_catalogaccount_name>` is your organization name and Snowflake Open Catalog account name, separated by a hyphen.
>
>       For example: `ABCDEFG-MYACCOUNT1`.
>
>       To retrieve these values in this format, see [Step 2: Retrieve your organization and account name](#label-retrieve-org-account-name-external-oauth).
>     - `{Catalogname}` is the name of a catalog in Open Catalog that you want to grant privileges to.
>     - `{catalogRoleName}` is the name of the catalog role you want to grant privileges on. For example, TableReader.
>     - `<service_admin_access_token>` is the [service admin access token you generated](#label-generate-service-admin-access-token-external-oauth).
>     - `CATALOG_MANAGE_CONTENT` is the name of the privilege in Open Catalog with catalog admin privileges.

See [Privileges](https://github.com/Snowflake-Labs/polaris-cli-opencatalog-demo?tab=readme-ov-file#privileges) in Snowflake Labs.
As described in the instructions, make sure you grant the `CATALOG_MANAGE_CONTENT` privilege to the catalog role.

See [Grant catalog privileges on a catalog role](/user-guide/opencatalog/secure-catalogs#label-grant-catalog-privileges-catalog-role) and select the
`CATALOG_MANAGE_CONTENT` privilege.

#### Grant the catalog role to a custom role

Important

Custom roles are case-sensitive. You should specify a custom role with *all* uppercase letters, even if you create it with lowercase
letters or lowercase and uppercase letters.

curlApache Polaris (Incubating) CLIOpen Catalog UI

Run the following command:

> Copy code
>
> ```
> curl -X PUT \
> "https://<your_org_name>-<your_open_catalogaccount_name>.snowflakecomputing.com/polaris/api/management/v1/principal-roles/{customRoleName}/catalog-roles/{catalogName}" \
> -H "Authorization: Bearer <service_admin_access_token>" \
> -H "Content-Type: application/json" \
> -H "Accept: application/json" \
> -d '{"catalogRole": {"name": "<catalog_role_name>", "properties": {}, "entityVersion": 1}}'
> ```
>
> Where:
> :   - `<your_org_name>-<your_open_catalogaccount_name>` is your organization name and Snowflake Open Catalog account name, separated by a hyphen.
>
>       For example: `ABCDEFG-MYACCOUNT1`.
>
>       To retrieve these values in this format, see [Step 2: Retrieve your organization and account name](#label-retrieve-org-account-name-external-oauth).
>     - `{customRoleName}` is the name of the custom role you want to grant with the catalog role that has catalog admin privileges.
>       For example, OPEN\_CATALOG\_ADMIN.
>     - `{catalogName}` is the name of a catalog in Open Catalog that you want to grant catalog admin privileges to.
>     - `<catalog_role_name>` is the name of the catalog role for a catalog, which has catalog admin privileges granted to it.
>       For example: CatalogAdmin.
>     - `<service_admin_access_token>` is the [service admin access token you generated](#label-generate-service-admin-access-token-external-oauth).

See [Grants](https://github.com/Snowflake-Labs/polaris-cli-opencatalog-demo?tab=readme-ov-file#grants) in Snowflake Labs.

See [Secure catalogs](/user-guide/opencatalog/secure-catalogs). These
instructions describe how to grant a catalog role to a principal role but the process is the same. Instead of selecting a principal
role from the list, select your custom role that you want to grant with the catalog role that has the `CATALOG_MANAGE_CONTENT` privilege.

If needed, repeat this step to grant the custom role with catalog admin privileges for other catalogs.

### Grant a catalog role with a set of privileges you specify to the custom role

The workflow is as follows:

1. [Create a catalog role](#create-a-catalog-role).
2. [Grant privileges to the catalog role](#grant-privileges-to-the-catalog-role). These privileges allow the service principal to perform actions in Open Catalog.
3. [Grant the catalog role to a custom role](#grant-the-catalog-role-to-a-custom-role).

#### Create a catalog role

In this section, you create a catalog role. For more information about catalog roles, see [Catalog role](access-control#catalog-role).

curlApache Polaris (Incubating) CLIOpen Catalog UI

Run the following command to create a catalog role in the catalog you specify:

> Copy code
>
> ```
>  curl -X POST \
> "https://<your_org_name>-<your_open_catalogaccount_name>.snowflakecomputing.com/polaris/api/management/v1/catalogs/{catalogName}/catalog-roles" \
> -H "Authorization: Bearer <service_admin_access_token>" \
> -H "Content-Type: application/json" \
> -H "Accept: application/json" \
> -d '{
>    "name": "<catalog_role_name>"
>    }'
> ```
>
> Where:
> :   - `<your_org_name>-<your_open_catalogaccount_name>` is your organization name and Snowflake Open Catalog account name, separated by a hyphen.
>
>       For example: `ABCDEFG-MYACCOUNT1`.
>
>       To retrieve these values in this format, see [Step 2: Retrieve your organization and account name](#label-retrieve-org-account-name-external-oauth).
>     - `{Catalogname}` is the name of the catalog in Open Catalog where you want to create a catalog role.
>     - `<service_admin_access_token>` is the [service admin access token you generated](#label-generate-service-admin-access-token-external-oauth).
>     - For `<catalog_role_name>` specify a name for the catalog role. For example: TableReader.

See [Catalog](https://github.com/Snowflake-Labs/polaris-cli-opencatalog-demo?tab=readme-ov-file#catalog-1) in Snowflake Labs.

See [Create a catalog role](/user-guide/opencatalog/create-catalog-role).

#### Grant privileges to the catalog role

You can grant privileges to the entire catalog or to a namespace or table in the catalog:

- [Grant catalog privileges on the catalog role](#grant-catalog-privileges-on-the-catalog-role)
- [Grant namespace privileges on the catalog role](#grant-namespace-privileges-on-the-catalog-role)
- [Grant table privileges on the catalog role](#grant-table-privileges-on-the-catalog-role)

##### Grant catalog privileges on the catalog role

curlApache Polaris (Incubating) CLIOpen Catalog UI

Run the following command:

> Copy code
>
> ```
> curl -X PUT \
> "https://<your_org_name>-<your_open_catalogaccount_name>.snowflakecomputing.com/polaris/api/management/v1/catalogs/{catalogName}/catalog-roles/{catalogRoleName}/grants" \
> -H "Authorization: Bearer <service_admin_access_token>" \
> -H "Content-Type: application/json" \
> -H "Accept: application/json" \
> -d '{"grant": {"type": "catalog", "privilege": "<privilege_name>"}}'
> ```
>
> Where:
> :   - `<your_org_name>-<your_open_catalogaccount_name>` is your organization name and Snowflake Open Catalog account name, separated by a hyphen.
>
>       For example: `ABCDEFG-MYACCOUNT1`.
>
>       To retrieve these values in this format, see [Step 2: Retrieve your organization and account name](#label-retrieve-org-account-name-external-oauth).
>     - `{Catalogname}` is the name of a catalog in Open Catalog that you want to grant privileges to.
>     - `{catalogRoleName}` is the name of the catalog role you want to grant privileges on. For example, TableReader.
>     - `<service_admin_access_token>` is the [service admin access token you generated](#label-generate-service-admin-access-token-external-oauth).
>     - `<privilege_name>` is the name of the privilege you want to grant to the catalog role. For the list of available privileges,
>       see [Access control privileges](https://other-docs.snowflake.com/en/opencatalog/access-control#access-control-privileges).

See [Privileges](https://github.com/Snowflake-Labs/polaris-cli-opencatalog-demo?tab=readme-ov-file#privileges) in Snowflake Labs.

Note

The example in Snowflake Labs grants the `CATALOG_MANAGE_CONTENT` privilege, which grants catalog admin privileges for the
catalog. However, for the list of other available privileges, see [Access control privileges](https://other-docs.snowflake.com/en/opencatalog/access-control#access-control-privileges) in
the Open Catalog documentation.

See [Grant catalog privileges on a catalog role](/user-guide/opencatalog/secure-catalogs#label-grant-catalog-privileges-catalog-role).

##### Grant namespace privileges on the catalog role

curlApache Polaris (Incubating) CLIOpen Catalog UI

Run the following command:

> Copy code
>
> ```
> curl -X PUT \
> "https://<your_org_name>-<your_open_catalogaccount_name>.snowflakecomputing.com/polaris/api/management/v1/catalogs/{catalogName}/catalog-roles/{catalogRoleName}/grants" \
> -H "Authorization: Bearer <service_admin_access_token>" \
> -H "Content-Type: application/json" \
> -H "Accept: application/json" \
> -d '{"grant": {"type": "namespace", "namespace": ["<namespace_name>"], "privilege": "<privilege_name>"}}'
> ```
>
> Where:
> :   - `<your_org_name>-<your_open_catalogaccount_name>` is your organization name and Snowflake Open Catalog account name, separated by a hyphen.
>
>       For example: `ABCDEFG-MYACCOUNT1`.
>
>       To retrieve these values in this format, see [Step 2: Retrieve your organization and account name](#label-retrieve-org-account-name-external-oauth).
>     - `{Catalogname}` is the name of a catalog in Open Catalog that you want to grant privileges to.
>     - `{catalogRoleName}` is the name of the catalog role you want to grant privileges on. For example, TableReader.
>     - `<service_admin_access_token>` is the [service admin access token you generated](#label-generate-service-admin-access-token-external-oauth).
>     - `<namespace_name>` is the name of the namespace you want to grant privileges to. To grant privileges to a
>       nested namespace, specify it, along with each parent namespace, separated by a comma. For example: `"ns1","ns1a"`.
>     - `<privilege_name>` is the name of the namespace privilege you want to grant to the catalog role. For the list of available privileges,
>       see [Access control privileges](https://other-docs.snowflake.com/en/opencatalog/access-control#access-control-privileges).

See [Privileges](https://github.com/Snowflake-Labs/polaris-cli-opencatalog-demo?tab=readme-ov-file#privileges) in Snowflake Labs.

Note

The example in Snowflake Labs grants the `CATALOG_MANAGE_CONTENT` privilege, which grants catalog admin privileges for the
catalog. However, for the list of other available privileges, see [Access control privileges](https://other-docs.snowflake.com/en/opencatalog/access-control#access-control-privileges) in
the Open Catalog documentation.

See [Grant namespace privileges on a catalog role](/user-guide/opencatalog/secure-catalogs#label-grant-namespace-privileges-catalog-role).

##### Grant table privileges on the catalog role

curlApache Polaris (Incubating) CLIOpen Catalog UI

Run the following command:

> Copy code
>
> ```
> curl -X PUT \
> "https://<your_org_name>-<your_open_catalogaccount_name>.snowflakecomputing.com/polaris/api/management/v1/catalogs/{catalogName}/catalog-roles/{catalogRoleName}/grants" \
> -H "Authorization: Bearer <service_admin_access_token>" \
> -H "Content-Type: application/json" \
> -H "Accept: application/json" \
> -d '{"grant": {"type": "table", "namespace": ["<namespace_name>"], "tableName": "<table_name>", "privilege": "<privilege_name>"}}'
> ```
>
> Where:
> :   - `<your_org_name>-<your_open_catalogaccount_name>` is your organization name and Snowflake Open Catalog account name, separated by a hyphen.
>
>       For example: `ABCDEFG-MYACCOUNT1`.
>
>       To retrieve these values in this format, see [Step 2: Retrieve your organization and account name](#label-retrieve-org-account-name-external-oauth).
>     - `{Catalogname}` is the name of a catalog in Open Catalog that you want to grant privileges to.
>     - `{catalogRoleName}` is the name of the catalog role you want to grant privileges on. For example, TableReader.
>     - `<service_admin_access_token>` is the [service admin access token you generated](#label-generate-service-admin-access-token-external-oauth).
>     - `<namespace_name>` is the name of the namespace whose table you want to grant privileges to. To grant privileges on a
>       table located under a nested namespace, specify the nested namespace, along with each parent namespace, separated by a comma. For example: `"ns1","ns1a"`.
>     - `<table_name>` is the name of the table you want to grant privileges to.
>     - `<privilege_name>` is the name of the privilege you want to grant to the catalog role. For the list of available privileges,
>       see [Access control privileges](https://other-docs.snowflake.com/en/opencatalog/access-control#access-control-privileges).

See [Privileges](https://github.com/Snowflake-Labs/polaris-cli-opencatalog-demo?tab=readme-ov-file#privileges) in Snowflake Labs.

Note

The example in Snowflake Labs grants the `CATALOG_MANAGE_CONTENT` privilege, which grants catalog admin privileges for the
catalog. However, for the list of other available privileges, see [Access control privileges](https://other-docs.snowflake.com/en/opencatalog/access-control#access-control-privileges) in
the Open Catalog documentation.

See [Grant table privileges on a catalog role](/user-guide/opencatalog/secure-catalogs#label-grant-table-privileges-catalog-role).

#### Grant the catalog role to a custom role

Important

Custom roles are case-sensitive. You should specify a custom role with *all* uppercase letters, even if you create it with lowercase
letters or lowercase and uppercase letters.

curlApache Polaris (Incubating) CLIOpen Catalog UI

Run the following command:

> Copy code
>
> ```
> curl -X PUT \
> "https://<your_org_name>-<your_open_catalogaccount_name>.snowflakecomputing.com/polaris/api/management/v1/principal-roles/{customRoleName}/catalog-roles/{catalogName}" \
> -H "Authorization: Bearer <service_admin_access_token>" \
> -H "Content-Type: application/json" \
> -H "Accept: application/json" \
> -d '{"catalogRole": {"name": "<catalog_role_name>", "properties": {}, "entityVersion": 1}}'
> ```
>
> Where:
> :   - `<your_org_name>-<your_open_catalogaccount_name>` is your organization name and Snowflake Open Catalog account name, separated by a hyphen.
>
>       For example: `ABCDEFG-MYACCOUNT1`.
>
>       To retrieve these values in this format, see [Step 2: Retrieve your organization and account name](#label-retrieve-org-account-name-external-oauth).
>     - `{customRoleName}` is the name of the custom role you that you want to grant the catalog role to.
>     - `{catalogName}` is the name of a catalog in Open Catalog where you created the catalog role that you want to grant privileges on.
>     - `<service_admin_access_token>` is the [service admin access token you generated](#label-generate-service-admin-access-token-external-oauth).
>     - `<catalog_role_name>` is the name of the catalog role that you want to grant to the custom role.

See [Grants](https://github.com/Snowflake-Labs/polaris-cli-opencatalog-demo?tab=readme-ov-file#grants) in Snowflake Labs.

See [Secure catalogs](/user-guide/opencatalog/secure-catalogs). These
instructions describe how to grant a catalog role to a principal role but the process is the same. Instead of selecting a principal
role from the list, you select your custom role.

If needed, repeat this workflow to grant additional catalog roles that you create to the custom role.

## Step 7: Create a service principal

In the step, you use your Snowflake CLI connection to create a service principal.

Note

If the default Snowflake CLI connection that you set doesn’t have the POLARIS\_ACCOUNT\_ADMIN role granted to it, you must include the
following statement with your command: `USE ROLE POLARIS_ACCOUNT_ADMIN`.

To connect to Open Catalog through External OAuth, we need a service principal. In Open Catalog, service principals are users with the `TYPE` parameter set to `service`. So we will use the CREATE USER command to create a user of `TYPE=service`.

To create a service principal, run the following command:

Copy code

```
snow sql -q "CREATE USER <user_name> LOGIN_NAME='<client_id>@clients' TYPE='service';"
```

Where:

- For `<user_name>`, specify a name for the service principal.
- For `<client_id>`, specify the client ID for your application. To find this value, in Auth0, navigate to Applications > Applications >
  [Name of your application] > Settings > **Client ID** field.

## Step 8: Grant a custom role to the service principal

In this section, you use your Snowflake CLI connection to grant the custom role to one or more service principals. As a result, you bestow the service principal with the privileges granted to any catalog role(s) that are granted to
the custom role. For more information on the RBAC model in Open Catalog, see [RBAC model](./access-control#rbac-model).

Note

If the default Snowflake CLI connection that you set doesn’t have the POLARIS\_ACCOUNT\_ADMIN role granted to it, you must include the
following statement with your command: `USE ROLE POLARIS_ACCOUNT_ADMIN`.

Important

Custom roles are case-sensitive. You should specify a custom role with *all* uppercase letters, even if you create it with lowercase
letters or lowercase and uppercase letters.

The following example grants the `ENGINEER` custom role to the `service_principal1` service principal.

Copy code

```
snow sql -q "GRANT ROLE ENGINEER to user service_principal1;"
```

To validate that the role is granted to the service principal, run:

Copy code

```
snow sql -q "show grants to user service_principal1;"
```

In the response, check that the custom role you created (**role** column) is assigned to the service principal you created (**grantee\_name** column).

## (Optional) Step 9: Generate the access token

In this section, you can generate an access token, which you can use to connect to Open Catalog with External OAuth. However, if you connect by
using this method, you must manually refresh the access token.

Alternatively, you can skip this step and later, [connect with Open Catalog by using an automatic refresh token](./external-oauth-connect#connect-with-open-catalog-by-using-automatic-refresh-token-preferred-method), which is the preferred method.

Use the following curl command to generate an access token:

Copy code

```
ACCESS_TOKEN=$(curl -X POST https://<Auth0_domain>/oauth/token --header 'content-type: application/x-www-form-urlencoded' --data grant_type=client_credentials --data client_id=<client_id> --data client_secret=<client_secret> --data-urlencode "audience=https://<your_org_name>-<your_open_catalog_account_name>.snowflakecomputing.com" --data "scope=SESSION:ROLE:<custom_role_name>" | jq -r '.access_token')
```

Where:

- `<Auth0_domain>` is your Auth0 domain. To find this value, in Auth0, navigate to Applications > Applications >
  [Name of your application] > Settings > **Domain** field.
- `<client_id>`is the client ID for your application in Auth0. To find this value, in Auth0, navigate to Applications > Applications >
  [Name of your application] > Settings > **Client ID** field.
- `<client_secret>` is the client secret for your application in Auth0. To find this value, in Auth0, navigate to Applications > Applications >
  [Name of your application] > Settings > **Client Secret** field.
- `<audience>` is the identifier for your API. To find this value, in Auth0, navigate to Applications > APIs > select your API > Settings

  > **Identifier** field.
- `<your_org_name>-<your_open_catalog_account_name>` is your organization name and Snowflake Open Catalog account name, separated by
  a hyphen.

  For example: `ABCDEFG-MYACCOUNT1`.

  To retrieve these values in this format, see [Retrieve your organization and account name](#step-2-retrieve-your-organization-and-account-name).
- `<custom_role_name>` is the name of a custom role you granted with catalog roles, such as `ENGINEER`.

## Step 10: Connect to Open Catalog with External OAuth

In this section, you connect the service principal to Open Catalog through External OAuth. For instructions, see [Connect to Snowflake Open Catalog with External OAuth](./external-oauth-connect), which includes instructions for connecting by using an access token or automatic token refresh.
