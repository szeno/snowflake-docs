# Configure key pair authentication in Snowflake Open Catalog

Feature — Generally Available

Not available in government regions.

This topic describes how to configure key pair authentication in Snowflake Open Catalog. This configuration allows a key pair authentication
user to connect to Open Catalog programmatically through an access token. For simplicity, unless otherwise specified, the rest of this topic
uses the term user to refer to a key pair authentication user.

With key pair authentication, you can allow a user programmatic access to Open Catalog for various custom roles with permissions on the appropriate catalogs.
For example:

- ANALYST custom role: Can only access catalogA.
- ENGINEER custom role: Can only access catalogB.

## Prerequisites

- [Create a catalog](https://other-docs.snowflake.com/en/opencatalog/create-catalog) in your Open Catalog account.
- You must have [Snowflake CLI](https://docs.snowflake.com/en/developer-guide/snowflake-cli/installation/installation) installed on your
  machine. In addition, you must create a Snowflake CLI connection for Open Catalog. To create this connection, see
  [Create a Snowflake CLI connection for Open Catalog](#create-a-snowflake-cli-connection-for-open-catalog) below.
- To configure key pair authentication, you must have the service admin role in Open Catalog. For more information, see [User roles](https://other-docs.snowflake.com/en/opencatalog/access-control#user-roles). In Snowflake CLI, this role is printed as POLARIS\_ACCOUNT\_ADMIN.
- You must have [SnowSQL](https://www.snowflake.com/en/developers/downloads/snowsql/) installed on your machine.
- You need a service admin access token. You need this token to configure key pair authentication programmatically and it’s required to grant
  a user with catalog admin privileges. To generate this token, see [Generate your service admin access token](#generate-your-service-admin-access-token) below.

## Before you begin

To configure key pair authentication, you need a Snowflake CLI connection for Open Catalog.

To create this connection, you need your full Open Catalog account identifier, which includes your Snowflake organization name and your
Open Catalog account name; for example: `<orgname>.<my-snowflake-open-catalog-account-name>`.

- To find your *Snowflake* organization name (`<orgname>`), see [Finding the organization and account name for an account](/user-guide/admin-account-identifier#label-account-name-find).
- To find your *Snowflake Open Catalog* account name (`<my-snowflake-open-catalog-account-name>`), see
  [Find the account name for a Snowflake Open Catalog account](/user-guide/opencatalog/find-account-name).

## Create a Snowflake CLI connection for Open Catalog

Create a Snowflake CLI connection for your Open Catalog account so that you can use it to configure key pair authentication for the account.

### Step 1: Add a Snowflake CLI connection for Snowflake Open Catalog

Add a connection for the Snowflake Open Catalog account where you want to configure key pair authentication.

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

## Generate your service admin access token

To configure key pair authentication programmatically, you need a service admin access token. However, you have the option to use the Open Catalog UI
to perform some tasks for configuring key pair authentication.

If you already generated a service admin access token for yourself and it’s still active, you can skip this step.

The steps for generating a service admin access token are as follows:

1. [Generate a private and public key](#generate-a-private-and-public-key)
2. [Assign the public key to yourself](#assign-the-public-key-to-yourself)
3. [Generate a JWT for yourself](#generate-a-json-web-token)
4. [Generate a service admin access token](#generate-a-service-admin-access-token)

### Generate a private and public key

This section describes how to generate a private and public key.

To generate a private key, use the following command:

Copy code

```
openssl genrsa 2048 | openssl pkcs8 -topk8 -inform PEM -out rsa_key.p8 -nocrypt
```

To generate a public key, use the following command:

Copy code

```
openssl rsa -in rsa_key.p8 -pubout -out rsa_key.pub
```

### Assign the public key to yourself

Use your Snowflake CLI connection to assign the public key to yourself.

Note

If the default Snowflake CLI connection that you set doesn’t have the POLARIS\_ACCOUNT\_ADMIN role granted to it, you must include the
following statement with your command: `USE ROLE POLARIS_ACCOUNT_ADMIN`.

1. To assign the public key to yourself, run:

   Copy code

   ```
   snow sql -q "alter user <your_username> set RSA_PUBLIC_KEY='<your_public_key>';"
   ```

   Where:

   - `<your_username>` is your Open Catalog username, which you use to sign in to the Open Catalog UI.

Note

If you need to retrieve your public key, run: `cat rsa_key.pub`.

1. Validate that the user has the public key (`RSA_PUBLIC_KEY`) set and the fingerprint of user’s RSA public key (`RSA_PUBLIC_KEY_FP`) set:

   Copy code

   ```
   snow sql -q "desc user <your_username>;"
   ```

   Where:
   - `<your_username>` is your Open Catalog username, which you use to sign in to the Open Catalog UI.

### Generate a JSON Web Token

In this section, you generate a JSON Web Token (JWT), which you need in order to generate an access token.

1. To use SnowSQL to generate a JWT, run:

   Copy code

   ```
   snowsql --private-key-path rsa_key.p8 --generate-jwt -h <your_org_name>-<your_open_catalogaccount_name>.snowflakecomputing.com -a <account-identifier> -u <your_user_name>
   ```

   Where:

   - `<your_org_name>-<your_open_catalogaccount_name>` is your organization name and Snowflake Open Catalog account name, separated by
     a hyphen.

     For example: `ABCDEFG-MYACCOUNT1`.

     To retrieve these values in this format, see [Retrieve your organization and account name](#step-2-retrieve-your-organization-and-account-name).
   - `<account-identifier>` is the account identifier for your Snowflake Open Catalog account. To retrieve it, refer to your Open Catalog
     account URL. For example, `abc12345`in `https://app.snowflake.com/us-west-2/abc12345/#/`.
   - `<your_user_name>` is your Open Catalog username.
2. If you encrypted it, enter the passkey or else select Enter to continue. It may take a few seconds for you to receive your JWT.

### Generate a service admin access token

In this section, you generate a service admin access token, which you use to configure key pair authentication programmatically.

1. To generate your service admin access token, execute the following command and copy the value into a text editor:

   Copy code

   ```
   curl -i -X POST \
   -H "Content-Type: application/x-www-form-urlencoded" \
   -H "Accept: application/json" \
   --data-urlencode "scope=session:role:POLARIS_ACCOUNT_ADMIN" \
   --data-urlencode "grant_type=client_credentials" \
   --data-urlencode "client_secret=<your_JWT>" \
   "https://<your_org_name>-<your_open_catalogaccount_name>.snowflakecomputing.com/polaris/api/catalog/v1/oauth/tokens"
   ```

   Where:

   - `POLARIS_ACCOUNT_ADMIN` is the name of the built-in role in Open Catalog that allows you to perform administrative tasks in Open
     Catalog, which includes configuring key pair authentication. In the Open Catalog UI, this role is referred to as the service admin
     role.
   - `<your_JWT>` is the JWT you generated in the previous step.
   - `<your_org_name>-<your_open_catalogaccount_name>` is your organization name and Snowflake Open Catalog account name, separated by
     a hyphen.

     For example: `ABCDEFG-MYACCOUNT1`.

     To retrieve these values in this format, see [Retrieve your organization and account name](#step-2-retrieve-your-organization-and-account-name).

## Step 1: Create a custom role

In this step, you use your Snowflake CLI connection to create a custom role.

Create a custom role so that later, you can grant catalog roles to it and grant the custom role to a user, which bestows the user
with privileges. For more information about custom roles, see [Custom role](access-control#custom-role). For more information on the
RBAC model in Open Catalog, see [RBAC model](./access-control#rbac-model).

Note

If the default Snowflake CLI connection that you set doesn’t have the POLARIS\_ACCOUNT\_ADMIN role granted to it, you must include the
following statement with your command: `USE ROLE POLARIS_ACCOUNT_ADMIN`.

The following example creates an `OPEN_CATALOG_ADMIN` custom role:

Copy code

```
snow sql -q "create role OPEN_CATALOG_ADMIN;"
```

## Step 2: Retrieve your organization and account name

You need your organization name and Snowflake Open Catalog account name, separated by a hyphen, for tasks such as generating a JWT or an access token.

1. To retrieve your organization name and Snowflake Open Catalog account name in this format, run the following command:

   Copy code

   ```
   snow sql -q "SELECT CURRENT_ORGANIZATION_NAME() || '-' || CURRENT_ACCOUNT_NAME();"
   ```
2. In the response, copy the returned values and paste them into a text editor for later use. For example: `ABCDEFG-MYACCOUNT1`.

## Step 3: Grant a catalog role to a custom role

In this section, you grant a catalog role to the custom role you created.

After you grant a catalog role to the custom role, you then grant the custom role to a user to bestow the user
with any privileges granted to catalog roles that are granted to the principal role. For more information on the RBAC model in Open Catalog,
see [RBAC model](./access-control#rbac-model).

You can grant the custom role with a catalog role that has catalog admin privileges for the catalog or has a set of
privileges for the catalog that you specify:

- If you want to grant a user with catalog admin privileges to a catalog,
  [grant a catalog role with catalog admin privileges to the custom role](#grant-a-catalog-role-with-catalog-admin-privileges-to-the-custom-role). For information on what privileges a catalog admin has, see [Catalog admin role](access-control#catalog-admin-role).
- If you want to grant the user with a set of privileges you specify,
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
>       To retrieve these values in this format, see [Step 2: Retrieve your organization and account name](#label-retrieve-org-account-name-key-pair-auth).
>     - `{Catalogname}` is the name of the catalog in Open Catalog where you want to create a catalog role.
>     - `<service_admin_access_token>` is the [service admin access token you generated](#label-generate-service-admin-access-token-key-pair-auth).
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
>       To retrieve these values in this format, see [Step 2: Retrieve your organization and account name](#label-retrieve-org-account-name-key-pair-auth).
>     - `{Catalogname}` is the name of a catalog in Open Catalog that you want to grant privileges to.
>     - `{catalogRoleName}` is the name of the catalog role you want to grant privileges on. For example, TableReader.
>     - `<service_admin_access_token>` is the [service admin access token you generated](#label-generate-service-admin-access-token-key-pair-auth).
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
>       To retrieve these values in this format, see [Step 2: Retrieve your organization and account name](#label-retrieve-org-account-name-key-pair-auth).
>     - `{customRoleName}` is the name of the custom role you want to grant with the catalog role that has catalog admin privileges.
>       For example, OPEN\_CATALOG\_ADMIN.
>     - `{catalogName}` is the name of a catalog in Open Catalog that you want to grant catalog admin privileges to.
>     - `<catalog_role_name>` is the name of the catalog role for a catalog, which has catalog admin privileges granted to it.
>       For example: CatalogAdmin.
>     - `<service_admin_access_token>` is the [service admin access token you generated](#label-generate-service-admin-access-token-key-pair-auth).

See [Grants](https://github.com/Snowflake-Labs/polaris-cli-opencatalog-demo?tab=readme-ov-file#grants) in Snowflake Labs.

See [Secure catalogs](/user-guide/opencatalog/secure-catalogs). These
instructions describe how to grant a catalog role to a principal role but the process is the same. Instead of selecting a principal
role from the list, select your custom role that you want to grant with the catalog role that has the `CATALOG_MANAGE_CONTENT` privilege.

If needed, repeat this step to grant the custom role with catalog admin privileges for other catalogs.

### Grant a catalog role with a set of privileges you specify to the custom role

The workflow is as follows:

1. [Create a catalog role](#create-a-catalog-role).
2. [Grant privileges to the catalog role](#grant-privileges-to-the-catalog-role). These privileges allow the user to perform actions in Open Catalog.
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
>       To retrieve these values in this format, see [Step 2: Retrieve your organization and account name](#label-retrieve-org-account-name-key-pair-auth).
>     - `{Catalogname}` is the name of the catalog in Open Catalog where you want to create a catalog role.
>     - `<service_admin_access_token>` is the [service admin access token you generated](#label-generate-service-admin-access-token-key-pair-auth).
>     - For `<catalog_role_name>` specify a name for the catalog role. For example: TableReader.

See [Catalog](https://github.com/Snowflake-Labs/polaris-cli-opencatalog-demo?tab=readme-ov-file#catalog-1) in Snowflake Labs.

See See [Create a catalog role](/user-guide/opencatalog/create-catalog-role).

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
>       To retrieve these values in this format, see [Step 2: Retrieve your organization and account name](#label-retrieve-org-account-name-key-pair-auth).
>     - `{Catalogname}` is the name of a catalog in Open Catalog that you want to grant privileges to.
>     - `{catalogRoleName}` is the name of the catalog role you want to grant privileges on. For example, TableReader.
>     - `<service_admin_access_token>` is the [service admin access token you generated](#label-generate-service-admin-access-token-key-pair-auth).
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
>       To retrieve these values in this format, see [Step 2: Retrieve your organization and account name](#label-retrieve-org-account-name-key-pair-auth).
>     - `{Catalogname}` is the name of a catalog in Open Catalog that you want to grant privileges to.
>     - `{catalogRoleName}` is the name of the catalog role you want to grant privileges on. For example, TableReader.
>     - `<service_admin_access_token>` is the [service admin access token you generated](#label-generate-service-admin-access-token-key-pair-auth).
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
>       To retrieve these values in this format, see [Step 2: Retrieve your organization and account name](#label-retrieve-org-account-name-key-pair-auth).
>     - `{Catalogname}` is the name of a catalog in Open Catalog that you want to grant privileges to.
>     - `{catalogRoleName}` is the name of the catalog role you want to grant privileges on. For example, TableReader.
>     - `<service_admin_access_token>` is the [service admin access token you generated](#label-generate-service-admin-access-token-key-pair-auth).
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
>       To retrieve these values in this format, see [Step 2: Retrieve your organization and account name](#label-retrieve-org-account-name-key-pair-auth).
>     - `{customRoleName}` is the name of the custom role you that you want to grant the catalog role to.
>     - `{catalogName}` is the name of a catalog in Open Catalog where you created the catalog role that you want to grant privileges on.
>     - `<service_admin_access_token>` is the [service admin access token you generated](#label-generate-service-admin-access-token-key-pair-auth).
>     - `<catalog_role_name>` is the name of the catalog role that you want to grant to the custom role.

See [Grants](https://github.com/Snowflake-Labs/polaris-cli-opencatalog-demo?tab=readme-ov-file#grants) in Snowflake Labs.

See [Secure catalogs](/user-guide/opencatalog/secure-catalogs). These
instructions describe how to grant a catalog role to a principal role but the process is the same. Instead of selecting a principal
role from the list, you select your custom role.

If needed, repeat this workflow to grant additional catalog roles that you create to the custom role.

## Step 4: Create a user

Use your Snowflake CLI connection to create a key pair authentication user in Open Catalog. A human can’t use this user’s credentials to
sign in to the Open Catalog UI.

Note

If the default Snowflake CLI connection that you set doesn’t have the POLARIS\_ACCOUNT\_ADMIN role granted to it, you must include the
following statement with your command: `USE ROLE POLARIS_ACCOUNT_ADMIN`.

1. To create a user, run the following command:

   Copy code

   ```
   snow sql -q "create user <username> login_name='<username>';"
   ```

   Where:

   - `<username>` is the user name you want to assign to the key pair authentication user.

## Step 5: Grant a custom role to the user

In this section, you use your Snowflake CLI connection to grant the custom role to one or more users. As a result, you bestow the user with the privileges granted to any catalog role(s) that are granted to
the custom role. For more information on the RBAC model in Open Catalog, see [RBAC model](./access-control#rbac-model).

Note

If the default Snowflake CLI connection that you set doesn’t have the POLARIS\_ACCOUNT\_ADMIN role granted to it, you must include the
following statement with your command: `USE ROLE POLARIS_ACCOUNT_ADMIN`.

Important

Custom roles are case-sensitive. You should specify a custom role with *all* uppercase letters, even if you create it with lowercase
letters or lowercase and uppercase letters.

The following example grants the `ENGINEER` custom role to the `keypairuser1` user.

Copy code

```
snow sql -q "GRANT ROLE ENGINEER to user keypairuser1;"
```

To validate that the role is granted to the user, run:

Copy code

```
snow sql -q "show grants to user keypairuser1;"
```

In the response, check that the custom role you created (**role** column) is assigned to the user you created (**grantee\_name** column).

## Step 6: Generate an access token for the user

In this section, you generate an access token for the user, which you use later to connect the user to Open Catalog through key pair
authentication.

The steps are as follows:

1. [Generate a private and public key](#generate-a-private-and-public-key-1)
2. [Assign the public key to the user](#assign-the-public-key-to-the-user)
3. [Generate a JWT](#generate-a-jwt-for-a-user)
4. [Generate an access token](#generate-an-access-token-for-the-user)

### Generate a private and public key

This section describes how to generate a private and public key.

To generate a private key, use the following command:

Copy code

```
openssl genrsa 2048 | openssl pkcs8 -topk8 -inform PEM -out rsa_key.p8 -nocrypt
```

To generate a public key, use the following command:

Copy code

```
openssl rsa -in rsa_key.p8 -pubout -out rsa_key.pub
```

### Assign the public key to the user

Use your Snowflake CLI connection to assign the public key to the user you created.

Note

If the default Snowflake CLI connection that you set doesn’t have the POLARIS\_ACCOUNT\_ADMIN role granted to it, you must include the
following statement with your command: `USE ROLE POLARIS_ACCOUNT_ADMIN`.

1. To assign the public key to the user you created, run:

   Copy code

   ```
   snow sql -q "alter user <username> set RSA_PUBLIC_KEY='<your_public_key>';"
   ```

Note

If you need to retrieve your public key, run: `cat rsa_key.pub`.

1. Validate that the user has the public key (`RSA_PUBLIC_KEY`) set and the fingerprint of user’s RSA public key (`RSA_PUBLIC_KEY_FP`) set:

   Copy code

   ```
   snow sql -q "desc user keypairuser1;"
   ```

### Generate a JWT for a user

In this step, you generate a JWT, which you need in order to generate an access token.

1. To use SnowSQL to generate a JWT, run:

   Copy code

   ```
   snowsql --private-key-path rsa_key.p8 --generate-jwt -h <your_org_name>-<your_open_catalogaccount_name>.snowflakecomputing.com -a <account-identifier> -u <user_name>
   ```

   Where:

   - `<your_org_name>-<your_open_catalogaccount_name>` is your organization name and Snowflake Open Catalog account name, separated by
     a hyphen.

     For example: `ABCDEFG-MYACCOUNT1`.

     To retrieve these values in this format, see [Retrieve your organization and account name](#step-2-retrieve-your-organization-and-account-name).
   - `<account-identifier>` is the account identifier for your Snowflake Open Catalog account. To retrieve it, refer to your Open Catalog
     account URL. For example, `abc12345`in `https://app.snowflake.com/us-west-2/abc12345/#/`.
   - `<user_name>` is the user name for an Open Catalog user with the public key assigned to the user.
2. If you encrypted it, enter the passkey or else select Enter to continue. It may take a few seconds for you to receive your JWT.

### Generate an access token for the user

1. Use the JWT to retrieve an access token for a custom or built-in role:

   Copy code

   ```
   curl -i -X POST \
   -H "Content-Type: application/x-www-form-urlencoded" \
   -H "Accept: application/json" \
   --data-urlencode "scope=session:role:<custom_role_name>" \
   --data-urlencode "grant_type=client_credentials" \
   --data-urlencode "client_secret=<your_JWT>" \
   "https://<your_org_name>-<your_open_catalogaccount_name>.snowflakecomputing.com/polaris/api/catalog/v1/oauth/tokens"
   ```

   Where

   - `<custom_role_name>` is the name of a custom role you created, such as `ENGINEER`.
   - `<your_JWT>` is the JWT you generated in the previous step.
   - `<your_org_name>-<your_open_catalogaccount_name>` is your organization name and Snowflake Open Catalog account name, separated by
     a hyphen.

     For example: `ABCDEFG-MYACCOUNT1`.

     To retrieve these values in this format, see [Retrieve your organization and account name](#step-2-retrieve-your-organization-and-account-name).
2. Store the access token in a variable (`$ACCESS_TOKEN`).

## Step 7: Connect to Open Catalog with key pair authentication

In this section, you connect the user to Open Catalog through key pair authentication. For instructions,
see [Connect to Snowflake Open Catalog with key pair authentication](key-pair-auth-connect).

## Configure key-pair rotation

Open Catalog supports multiple active keys to allow for uninterrupted rotation. The steps for configuring key-pair rotation in Open Catalog
are the same as configuring it in Snowflake. For instructions, see [Configuring key-pair rotation](https://docs.snowflake.com/en/user-guide/key-pair-auth#configuring-key-pair-rotation)
in the Snowflake documentation.

## Use the Apache Polaris™ (Incubating) CLI to manage catalogs

After you configure key pair authentication, you can [generate a service admin access token](#generate-a-service-admin-access-token) to use the Apache Polaris™ (Incubating) CLI
to set up and manage catalogs in Open Catalog. For instructions, see the [Open Catalog with Polaris guide](https://github.com/Snowflake-Labs/polaris-cli-opencatalog-demo)
in Snowflake Labs.
