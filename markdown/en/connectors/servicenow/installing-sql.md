# Install and configure the connector with SQL commands

Feature — Generally Available

The Snowflake Connector for ServiceNow® is generally available on supported cloud platforms.

This topic describes how to use SQL commands to install and configure the connector. It assumes that
you have already performed the procedures outlined in [Prepare your ServiceNow® instance](/connectors/servicenow/prereqs).

## Install the Snowflake Connector for ServiceNow®

The following procedure describes how to install the connector:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) as a user with the ACCOUNTADMIN role.
2. In the navigation menu, select **Marketplace** » **Snowflake Marketplace**.
3. Search for the Snowflake Connector for ServiceNow®, then select the tile for the connector.
4. In the page for the Snowflake Connector for ServiceNow®, select **Get**.

   This displays a dialog that you use to begin the initial part of the installation process.

   In the dialog configure the following:

   1. In the **Application name** field, enter the name of the database to be used as the database for the connector
      instance. This database is created for you automatically.
   2. In the **Warehouse used for installation** field, select the warehouse that you want to use for
      installing the connector.

      Note

      This is not the same warehouse that is used by the connector to synchronize data from ServiceNow®. In a
      later step, you will create a separate warehouse for this purpose.
   3. Select **Get**.
5. A dialog appears with the notification: `Installing App After installation, an email will be sent to <user_email>`. You can now close the dialog.
   To continue configuration using SQL, wait until you receive an email stating that *‘Snowflake Connector for ServiceNow’ installed and ready for use* then go to the **Worksheets**.

## Set up OAuth

Note

If you plan to use basic authentication instead of OAuth, you can skip this section and continue
to [Create a secret object](#label-servicenow-connector-prereqs-secret-v2)

You can configure the Snowflake Connector for ServiceNow® to use OAuth for authenticating to the ServiceNow® instance. There are two supported OAuth flows:

- Client credentials grant (recommended): Available since [Washington DC release](https://www.servicenow.com/docs/bundle/washingtondc-release-notes/page/release-notes/family-release-notes.html). Client credentials are
  a widely accepted authorization standard for machine to machine integration and don’t require manual refresh tokens
  maintenance.
- Authorization code grant flow: This authentication method is available on all supported ServiceNow® releases, but
  with this method OAuth tokens must be manually refreshed before their expiration date, typically every 3 months.

### Set up OAuth with client credentials grant flow

To configure the Snowflake Connector for ServiceNow® to use OAuth with client credentials grant flow for authenticating to the ServiceNow® instance, do the following:

- In ServiceNow®, you must set up the instance to support using OAuth with the [client credentials grant flow](https://www.servicenow.com/docs/bundle/washingtondc-platform-security/page/integrate/authentication/concept/client-credentials.html).
- In the Snowflake Connector for ServiceNow®:
  - The connector uses a security integration with `TYPE = API_AUTHENTICATION` to connect
    Snowflake to the ServiceNow® instance.

    The security integration specifies the ServiceNow® OAuth client ID, client secret, and the endpoint
    URL for authenticating to the ServiceNow® instance.
  - The connector uses a Snowflake secret object to manage sensitive information, including the
    authentication credentials.

    In the case of using OAuth for authentication, the connector stores the ServiceNow® OAuth scope and the name of
    the security integration in the Snowflake secret object.

If your ServiceNow® instance already uses the OAuth client credentials grant flow and you would like to use that
instance with the Snowflake Connector for ServiceNow®, note the client ID, client secret, and endpoint URL that corresponds to the OAuth token.
For more information, see [Manage OAuth tokens](https://docs.servicenow.com/bundle/washingtondc-platform-security/page/administer/security/task/t_ManageTokens.html). After noting this information, proceed to [create essential objects](#label-servicenow-connector-prereqs-oauth-sec-integ-v2)

#### Configure ServiceNow® instance to use the OAuth with client credentials grant flow

1. Configure your instance to use OAuth with the authorization code grant flow as shown in [Set up OAuth](https://docs.servicenow.com/bundle/washingtondc-platform-security/page/administer/security/task/t_SettingUpOAuth.html).
2. [Create an endpoint for clients to access the instance](https://docs.servicenow.com/bundle/washingtondc-platform-security/page/administer/security/task/t_CreateEndpointforExternalClients.html) and use it to configure the connector:
   1. Log in to your ServiceNow® instance, then select **Homepage**.
   2. Search for **sys\_properties.list**.
   3. Search for property with `glide.oauth.inbound.client.credential.grant_type.enabled` name in the table and make sure it is
      set to `true`.

      Note

      If the property doesn’t exist, create it. Click **New** button and fill the following fields of new
      property:

      - Set **Name** to `glide.oauth.inbound.client.credential.grant_type.enabled`,
      - Set **Type** to `true | false`,
      - Set **Value** to `true`.
   4. Search for **System OAuth**, then select **Application Registry**.
   5. Select **New**, then select **Create an OAuth API endpoint for external clients**.
   6. In ServiceNow®, enter a name for the OAuth application registry in the **Name** field.
   7. In ServiceNow®, select user you want the connector to authenticate with in the **OAuth Application User** field.
      The user needs to have the privileges listed in [Prepare your ServiceNow® instance](/connectors/servicenow/prereqs).

      Note

      If **OAuth Application User** field isn’t available in the form, open **Additional actions** menu in the
      upper left corner of the screen. Select from menu **Configure** > **Form builder**. Then add missing
      **OAuth Application User** field to the `Default` view of the form. **Save** the form and refresh
      the page to continue.
   8. In ServiceNow®, select **Submit**.

      The OAuth application registry appears in the list of application registries.
   9. In ServiceNow®, select the application registry you just created.

      Note that ServiceNow® generated values for the **Client ID** and **Client Secret** fields.
      You will use these values when
      [creating a security integration](#label-servicenow-connector-prereqs-oauth-sec-integ-v2).

### Set up OAuth with authorization code grant flow

To configure the Snowflake Connector for ServiceNow® to use OAuth with authorization code grant flow for authenticating to the ServiceNow® instance:

- In ServiceNow, you must set up the instance to support using OAuth with the [authorization code grant flow](https://docs.servicenow.com/bundle/washingtondc-platform-security/page/administer/security/concept/c_OAuthAuthorizationCodeFlow.html).
- In the Snowflake Connector for ServiceNow®:
  - The connector uses a security integration with `TYPE = API_AUTHENTICATION` to connect
    Snowflake to the ServiceNow® instance.

    The security integration specifies the ServiceNow® OAuth client ID, client secret, and the endpoint
    URL for authenticating to the ServiceNow® instance.
  - The connector uses a Snowflake secret object to manage sensitive information, including the
    authentication credentials.

    In the case of using OAuth for authentication, the connector stores the ServiceNow® OAuth refresh
    token, the refresh token expiration time, and the name of the security integration in the Snowflake
    secret object.

If your ServiceNow® instance already uses the OAuth authorization code grant flow and you would like to use that
instance with the Snowflake Connector for ServiceNow®, note the client ID, client secret, and endpoint URL that corresponds to the OAuth token.
For more information, see [Manage OAuth tokens](https://docs.servicenow.com/bundle/washingtondc-platform-security/page/administer/security/task/t_ManageTokens.html). After noting this information proceed to [generate OAuth refresh token](#label-servicenow-connector-generate-oauth-refresh-token-v2)

#### Configure ServiceNow® instance to use the OAuth with authorization code grant flow

1. Configure your instance to use OAuth with the authorization code grant flow as shown in [Set up OAuth](https://docs.servicenow.com/bundle/washingtondc-platform-security/page/administer/security/task/t_SettingUpOAuth.html).
2. [Create an endpoint for clients to access the instance](https://docs.servicenow.com/bundle/washingtondc-platform-security/page/administer/security/task/t_CreateEndpointforExternalClients.html) and use it to configure the connector:
   1. Login to your ServiceNow® instance, then select **Homepage**.
   2. Search for OAuth, then select **Application Registry**.
   3. Select **New**, then select **Create an OAuth API endpoint for external clients**.

      This displays a configuration page for the application registry as shown in the following image:

      ![Displays the Application Registry page in ServiceNow®.](/static/images/screens/servicenow/oauth-setup-manual.png)
   4. In ServiceNow, enter a name for the OAuth application registry in the **Name** field.
   5. If required, in ServiceNow, update the values in the **Refresh Token Lifespan** and
      **Access Token Lifespan** fields.

      - Snowflake recommends setting the lifespan of the access token to at least 600 seconds.
      - For the lifespan of the refresh token, specify a value that is 7776000 (90 days).
   6. In ServiceNow, select **Submit**.

      The OAuth application registry appears in the list of application registries.
   7. In ServiceNow, select the application registry you just created.

      Note that ServiceNow® generated values for the **Client ID** and **Client Secret** fields.
      You will use these values when
      [creating a security integration](#label-servicenow-connector-prereqs-oauth-sec-integ-v2).

#### Generate OAuth refresh token

To generate the OAuth refresh token:

1. Send an HTTP request to the `/oauth_token.do` endpoint of your ServiceNow® instance, as explained in the
   [REST OAuth Example](https://docs.servicenow.com/bundle/washingtondc-api-reference/page/integrate/inbound-rest/reference/r_RESTOAuthExample.html) in the ServiceNow® documentation.

   For example, if you are using curl to send the HTTP request:

   Copy code

   ```
   curl -d "grant_type=password" --data-urlencode "client_id=<client_id>" --data-urlencode "client_secret=<client_secret>" --data-urlencode "username=<username>" --data-urlencode "password=<password>" -X POST https://<servicenow_instance>.service-now.com/oauth_token.do
   ```

   Where

   `<servicenow_instance>`
   :   Specifies the name of your ServiceNow® instance.

   `client_id` and `client_secret`
   :   Specify the values you obtained when setting up the ServiceNow® endpoint.

   `username` and `password`
   :   Specify the credentials for your ServiceNow® instance.

   Note

   The example above uses the `data-urlencode` command-line flag in curl to [URL-encode](https://en.wikipedia.org/wiki/Percent-encoding) the client secret, username, and password in the HTTP request sent to ServiceNow®.

   If you are using a different tool to send the HTTP request, make sure that you URL-encode these values in the request.

   The body of the HTTP response contains a JSON object. Get the refresh token from the `refresh_token` field in this
   object:

   Copy code

   ```
   {"access_token":"abcd1234","refresh_token":"cdef567","scope":"useraccount","token_type":"Bearer","expires_in":1799}
   ```

## Create essential objects

### Create a security integration (optional)

Note

If you plan to use basic authentication instead of OAuth, you can skip this section and continue
to [Create a secret object](#label-servicenow-connector-prereqs-secret-v2)

A security integration is a Snowflake object that provides an interface between Snowflake and a third-party
OAuth 2.0 service.

#### Create a security integration for OAuth with client credentials grant flow

Use the [CREATE SECURITY INTEGRATION](/sql-reference/sql/create-security-integration-api-auth) command to create a security integration as shown in the
following example:

Copy code

```
CREATE SECURITY INTEGRATION <name>
 TYPE = API_AUTHENTICATION
 AUTH_TYPE = OAUTH2
 OAUTH_CLIENT_AUTH_METHOD = CLIENT_SECRET_POST
 OAUTH_CLIENT_ID = '<client_id>'
 OAUTH_CLIENT_SECRET = '<client_secret>'
 OAUTH_TOKEN_ENDPOINT = 'https://<servicenow_instance>.service-now.com/oauth_token.do'
 OAUTH_GRANT = 'CLIENT_CREDENTIALS'
 OAUTH_ALLOWED_SCOPES = ('useraccount')
 ENABLED = TRUE;
```

Where:

> `name`
> :   Specifies the name of security integration. The name must be unique among integrations in your account.
>
> `client_id`
> :   Specifies the value of the **Client ID** field you obtained when setting up the ServiceNow® endpoint.
>
> `client_secret`
> :   Specifies the value of the **Client Secret** field you obtained when setting up the ServiceNow® endpoint.
>
> `servicenow_instance_name`
> :   Specifies the name of your ServiceNow® instance. This is the first part of the hostname of your ServiceNow®
>     instance. For example, if the URL to your ServiceNow® instance is:
>
>     Copy code
>
>     ```
>     https://myinstance.service-now.com
>     ```
>
>     The name of your instance would be `myinstance`.

#### Create a security integration for OAuth with authorization code grant flow

Use the [CREATE SECURITY INTEGRATION](/sql-reference/sql/create-security-integration-api-auth) command to create a security integration as shown in the
following example:

Copy code

```
CREATE SECURITY INTEGRATION <name>
 TYPE = API_AUTHENTICATION
 AUTH_TYPE = OAUTH2
 OAUTH_CLIENT_AUTH_METHOD = CLIENT_SECRET_POST
 OAUTH_CLIENT_ID = '<client_id>'
 OAUTH_CLIENT_SECRET = '<client_secret>'
 OAUTH_TOKEN_ENDPOINT = 'https://<servicenow_instance>.service-now.com/oauth_token.do'
 ENABLED = TRUE;
```

Where:

> `name`
> :   Specifies the name of security integration. The name must be unique among integrations in your account.
>
> `client_id`
> :   Specifies the value of the **Client ID** field you obtained when setting up the ServiceNow® endpoint.
>
> `client_secret`
> :   Specifies the value of the **Client Secret** field you obtained when setting up the ServiceNow® endpoint.
>
> `servicenow_instance_name`
> :   Specifies the name of your ServiceNow® instance. This is the first part of the hostname of your ServiceNow®
>     instance. For example, if the URL to your ServiceNow® instance is:
>
>     Copy code
>
>     ```
>     https://myinstance.service-now.com
>     ```
>
>     The name of your instance would be `myinstance`.

### Create a secret object

Create the Snowflake secret object that the Snowflake Connector for ServiceNow® uses for authentication.

Snowflake recommends storing the secret object in a dedicated database and schema.
Note that you can choose any role to manage the secret, and you can choose any database and schema to store the secret.

To create a custom role to manage the secret, use the [CREATE ROLE](/sql-reference/sql/create-role) command. For information on the privileges
that you can grant to a role, see [Access control privileges](/user-guide/security-access-control-privileges).

The next sections explain how to create a secret object that is stored in a separate database and schema and that
is managed by a custom role.

#### Create a schema for the secret objects

First, create a database and schema to store the secret object by running the [CREATE DATABASE](/sql-reference/sql/create-database) and
[CREATE SCHEMA](/sql-reference/sql/create-schema) commands. The names of the schema and database must be valid [object identifiers](/sql-reference/identifiers-syntax).

For example, to create the database `secretsdb` and the schema `apiauth` for the secret object, run the following commands:

> Copy code
>
> ```
> USE ROLE accountadmin;
> CREATE DATABASE secretsdb;
> CREATE SCHEMA apiauth;
> ```

#### Create a custom role to manage the secret (optional)

Next, create a custom role to manage the secret (assuming that you do not want to use an existing role) and grant
the role the privileges needed to create the secret.

1. Using the USERADMIN system role, run the [CREATE ROLE](/sql-reference/sql/create-role) command to create a custom role to manage the secret.
   For example, to create the custom role `secretadmin` for managing the secret, run the following commands:

   Copy code

   ```
   USE ROLE useradmin;
   CREATE ROLE secretadmin;
   ```
2. Using the SECURITYADMIN system role, run the [GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege) command to grant the following
   privileges to the custom role:

   - USAGE on [the database that you created for the secret](#label-servicenow-connector-prereqs-secret-schema-v2)
   - USAGE and CREATE SECRET on
     [the schema that you created for the secret](#label-servicenow-connector-prereqs-secret-schema-v2)

   For example:

   Copy code

   ```
   USE ROLE securityadmin;
   GRANT USAGE ON DATABASE secretsdb TO ROLE secretadmin;
   GRANT USAGE ON SCHEMA secretsdb.apiauth TO role secretadmin;
   GRANT CREATE SECRET ON SCHEMA secretsdb.apiauth TO role secretadmin;
   ```
3. (optional) If you are setting up the connector with OAuth authentication, then also grant USAGE privilege on
   [the security integration that you created earlier](#label-servicenow-connector-prereqs-oauth-sec-integ-v2) to the custom role.

   For example:

   Copy code

   ```
   USE ROLE securityadmin;
   GRANT USAGE ON INTEGRATION servicenow_oauth TO role secretadmin;
   ```
4. Using the USERADMIN system role, run the [GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege) command to grant the custom role to the
   user who creates the secret. For example, to grant the role to the user `servicenow_secret_owner`, run
   the following commands:

   Copy code

   ```
   USE ROLE useradmin;
   GRANT ROLE secretadmin TO user servicenow_secret_owner;
   ```

#### Create a secret

Next, create a secret to enable Snowflake to authenticate to the ServiceNow® instance using OAuth with the authorization code grant flow.

Note

If you plan to use basic authentication instead of OAuth, see
[the note below](#label-servicenow-connector-prereqs-secret-create-basic-v2) instead.

To create a secret object for OAuth client credentials grant flow, run the [CREATE SECRET](/sql-reference/sql/create-secret) command with the following parameters:

> - Set `TYPE` to `OAUTH2`.
> - Set `API_AUTHENTICATION` to the name of the security integration that you created in [Create essential objects](#label-servicenow-connector-prereqs-oauth-sec-integ-v2):
> - Set `OAUTH_SCOPES` to `useraccount`.
>
> For example, to create a secret named `service_now_creds_oauth_code` that uses the security integration named
> `servicenow_oauth`, run these commands:
>
> Copy code
>
> ```
> USE ROLE secretadmin;
> USE SCHEMA secretsdb.apiauth;
> CREATE SECRET servicenow_creds_oauth_code
>   TYPE = OAUTH2
>   API_AUTHENTICATION = servicenow_oauth
>   OAUTH_SCOPES=('useraccount');
> ```

To create a secret object for OAuth authorization code grant flow, run the [CREATE SECRET](/sql-reference/sql/create-secret) command with the following parameters:

> - Set `TYPE` to `OAUTH2`.
> - Set `OAUTH_REFRESH_TOKEN` to the OAuth refresh token that you retrieved in [Generate OAuth refresh token](#label-servicenow-connector-generate-oauth-refresh-token-v2).
> - Set `OAUTH_REFRESH_TOKEN_EXPIRY_TIME` to the refresh token expiration timestamp in UTC timezone. You can calculate
>   this by adding the token lifespan from ServiceNow® to the date when the token was issued. By default, the
>   token expires in 100 days.
> - Set `API_AUTHENTICATION` to the name of the security integration that you created in [Create essential objects](#label-servicenow-connector-prereqs-oauth-sec-integ-v2):
>
> For example, to create a secret named `service_now_creds_oauth_code` that uses the security integration named
> `servicenow_oauth`, run these commands:
>
> Copy code
>
> ```
> USE ROLE secretadmin;
> USE SCHEMA secretsdb.apiauth;
> CREATE SECRET servicenow_creds_oauth_code
>   TYPE = OAUTH2
>   OAUTH_REFRESH_TOKEN = 'cdef567'
>   OAUTH_REFRESH_TOKEN_EXPIRY_TIME = '2022-01-06 20:00:00'
>   API_AUTHENTICATION = servicenow_oauth;
> ```

To modify the properties of an existing secret (e.g. to update the OAuth refresh token), use the [ALTER SECRET](/sql-reference/sql/alter-secret)
command.

Note

> If you plan to use basic authentication (rather than OAuth), run the [CREATE SECRET](/sql-reference/sql/create-secret) command to create a
> secret with `TYPE` set to `PASSWORD`. Set `USERNAME` and `PASSWORD` to the username and
> password of the ServiceNow® user that you plan to use to authenticate to the ServiceNow® instance. For example:
>
> Copy code
>
> ```
> USE ROLE secretadmin;
> USE SCHEMA secretsdb.apiauth;
> CREATE SECRET servicenow_creds_pw
>   TYPE = PASSWORD
>   USERNAME = 'jsmith1'
>   PASSWORD = 'W3dr@fg*7B1c4j';
> ```

If multi-factor authentication is enabled for this user, you must provide the MFA token together with password
as described in [REST API](https://docs.servicenow.com/bundle/washingtondc-api-reference/page/integrate/inbound-rest/concept/c_RESTAPI.html) in the ServiceNow® documentation.

### Create a warehouse

Snowflake recommends [creating a warehouse](/user-guide/warehouses-tasks) dedicated
for the connector. A dedicated warehouse allows for better cost management and resource tracking. To facilitate
resource tracking, you can optionally [add one or more tags](/user-guide/object-tagging/introduction) to the dedicated warehouse.

For the connector warehouse, Snowflake recommends using a large-sized warehouse.

To create a large-sized warehouse named `servicenow_conn_warehouse`, run the following command:

Copy code

```
USE ROLE accountadmin;
CREATE WAREHOUSE servicenow_conn_warehouse WAREHOUSE_SIZE = LARGE;
```

Attention

Make sure the warehouse is able to execute a query for at least 8 hours. It’s affected by a parameter value that can be set both
on the warehouse used by the connector and on the account (account’s value takes precedence). To check the current values run:

Copy code

```
SHOW PARAMETERS LIKE 'STATEMENT_TIMEOUT_IN_SECONDS' FOR ACCOUNT;
SHOW PARAMETERS LIKE 'STATEMENT_TIMEOUT_IN_SECONDS' FOR WAREHOUSE <connector_warehouse>;
```

If both values are at least `28800` (i.e. 8 hours), then no change is needed. Otherwise, run one of the following as necessary:

Copy code

```
ALTER ACCOUNT SET STATEMENT_TIMEOUT_IN_SECONDS = 28800;
ALTER WAREHOUSE <connector_warehouse> SET STATEMENT_TIMEOUT_IN_SECONDS = 28800;
```

If the proper timeout is not provided, then data ingestion failures will occur.

### Create a database and schema for the ServiceNow® data

Next, create a database and schema for the ServiceNow® data. The Snowflake Connector for ServiceNow® ingests ServiceNow® data
into this database and schema.

When creating the database and schema, note the following:

- The names of the schema and database must be valid [object identifiers](/sql-reference/identifiers-syntax).
- To control access to the ingested ServiceNow® data in Snowflake, you can
  [grant the privileges on the schema to the roles that should be allowed to access the data](/connectors/servicenow/accessing-data#label-servicenow-connector-accessing-data-privileges-v2).

To create the database and schema, run the [CREATE DATABASE](/sql-reference/sql/create-database) and [CREATE SCHEMA](/sql-reference/sql/create-schema) commands.

For example, to create the database `dest_db` and the schema `dest_schema` for the ServiceNow® data, run the following
commands:

Copy code

```
USE ROLE accountadmin;
CREATE DATABASE dest_db;
CREATE SCHEMA dest_schema;
```

Note

If you are reinstalling the connector, you can reuse the schema that you created for the previous installation of the
connector. This is possible if the previous installation of the connector has already loaded data and you want to
continue loading data into the same tables.

To continue loading data, do not modify the schema before [reinstalling the connector](/connectors/servicenow/managing#label-reinstalling-the-servicenow-connector-v2).
Do not change the definitions of the tables created by the previous installation of the connector.

The connector periodically exports connector configuration and state to a `__CONNECTOR_STATE_EXPORT` table in the schema,
which can later be used to recover connector configuration during reinstallation. Alternatively, if the export table isn’t present or was
dropped manually, you can still later call the [the ENABLE\_TABLES stored procedure](/connectors/servicenow/ingestion#label-servicenow-connector-configure-enable-sync-v2) to reenable the previously ingested tables.
The stored procedure verifies that all required objects already exist and does not attempt to recreate them, thus
there is no risk of losing already ingested data.

### Create a network rule for communicating with the ServiceNow® instance

Next, to allow outbound traffic from your account to your ServiceNow® instance, please create a network rule.
As an accountadmin, run the [CREATE NETWORK RULE](/sql-reference/sql/create-network-rule) command with the following syntax:

Copy code

```
CREATE NETWORK RULE <name>
  MODE = 'EGRESS'
  TYPE = 'HOST_PORT'
  VALUE_LIST = ('<servicenow_instance>.service-now.com');
```

Where:

`name`
:   Specifies the name of the Network Rule. The name must be a valid [object identifier](/sql-reference/identifiers-syntax).

`VALUE_LIST = ('servicenow_instance_name.service-now.com')`
:   Specifies list of allowed ServiceNow® instances to which a request can be sent.

For example, to create the network rule named `servicenow_network_rule` inside `apiauth` schema of database `secretsdb` run the following command:

Copy code

```
USE ROLE accountadmin;
CREATE NETWORK RULE secretsdb.apiauth.servicenow_network_rule
  MODE = 'EGRESS'
  TYPE = 'HOST_PORT'
  VALUE_LIST = ('myinstance.service-now.com');
```

Note

If you created the secret with a custom role, you need to additionally grant USAGE privilege on it to `ACCOUNTADMIN`
before creating the network rule:

Copy code

```
USE ROLE secretadmin;
GRANT USAGE ON SECRET secretsdb.apiauth.<secret_name> TO ROLE ACCOUNTADMIN;
```

### Create an external access integration for communicating with the ServiceNow® instance

Next, create an external access integration for communicating with the ServiceNow® instance. Run the [CREATE EXTERNAL ACCESS INTEGRATION](/sql-reference/sql/create-external-access-integration)
command with the following syntax:

Copy code

```
CREATE EXTERNAL ACCESS INTEGRATION <integration_name>
  ALLOWED_NETWORK_RULES = (<network_rule_name>)
  ALLOWED_AUTHENTICATION_SECRETS = (<secret_name>)
  ENABLED = TRUE;
```

Where:

`integration_name`
:   Specifies the name of the external access integration. The name must be a valid [object identifier](/sql-reference/identifiers-syntax). The name must be unique among integrations in your account.

`ALLOWED_NETWORK_RULES = (network_rule_name)`
:   Specifies the network rule allowing access to your ServiceNow® instance. This limits the use of this integration to the instances with the URLs specified in the network rule.

    Set this to the name of the network rule that you created in [Create a network rule for communicating with the ServiceNow® instance](#label-servicenow-connector-prereqs-network-rule-v2).

`ALLOWED_AUTHENTICATION_SECRETS = (secret_name)`
:   Specifies the list of the names of the secrets that are allowed for use in the scope of the API integration.

    Set this to the name of the secret object that you created in [Create a secret object](#label-servicenow-connector-prereqs-secret-v2).

`ENABLED = TRUE`
:   Specifies whether this API integration is enabled or disabled. If the API integration is disabled, any
    external function that relies on it does not work.

    > `TRUE`
    > :   Allows the integration to run based on the parameters specified in the integration definition.
    >
    > `FALSE`
    > :   Suspends the integration for maintenance. Any integration between Snowflake and a third-party service fails to work.

For example, to create the external access integration named `servicenow_external_access_integration` run the following command:

> Copy code
>
> ```
> USE ROLE accountadmin;
> CREATE EXTERNAL ACCESS INTEGRATION servicenow_external_access_integration
>   ALLOWED_NETWORK_RULES = (secretsdb.apiauth.servicenow_network_rule)
>   ALLOWED_AUTHENTICATION_SECRETS = (secretsdb.apiauth.servicenow_creds_pw)
>   ENABLED = TRUE
> ```

## Configure logging for the connector

The Snowflake Connector for ServiceNow® uses event tables to store error logs for the connector. To set up an event table follow [Setting up an Event Table](/developer-guide/logging-tracing/event-table-setting-up) guide.

Important

Snowflake recommends that you
[set up event tracing](http://docs.snowflake.com/developer-guide/native-apps/ui-consumer-enable-logging) to help troubleshoot problems.

## Set up the installed connector

To set up the connector:

1. Create a database for the connector instance using Snowsight. For more information on how to create the database, see [Installing and Configuring the Connector with Snowsight](/connectors/servicenow/installing-snowsight#label-connector-servicenow-install-ui-v2).
2. Navigate to the SQL worksheet.
3. Log in as a user with the ACCOUNTADMIN role. For example:

   Copy code

   ```
   USE ROLE ACCOUNTADMIN;
   ```
4. Grant all the required privileges to the connector
   [the database that serves as an instance of the connector](/connectors/servicenow/installing-sql#label-connector-servicenow-connector-name-v2).

   - EXECUTE TASK on the account
   - EXECUTE MANAGED TASK on the account
   - USAGE on
     [the warehouse that you created for the connector](#label-servicenow-connector-prereqs-warehouse-create-v2).
   - USAGE on
     [the database that you created for the ServiceNow® data](#label-servicenow-connector-prereqs-dest-schema-v2)
   - USAGE, CREATE TABLE, and CREATE VIEW on
     [the schema that you created for the ServiceNow® data](#label-servicenow-connector-prereqs-dest-schema-v2)
   - USAGE on
     [the external access integration that you created for ServiceNow®](#label-servicenow-connector-prereqs-external-access-integration-v2)
   - USAGE on [the database that you created for the secret](#label-servicenow-connector-prereqs-secret-schema-v2)
   - USAGE on
     [the schema that you created for the secret](#label-servicenow-connector-prereqs-secret-schema-v2)
   - READ on [the secret that you created](#label-servicenow-connector-prereqs-secret-create-v2)

   For example, to grant the following privileges to the connector named `my_connector_servicenow`:

   - EXECUTE TASK on the account
   - EXECUTE MANAGED TASK on the account
   - USAGE on the warehouse `servicenow_conn_warehouse`
   - USAGE on the `dest_db` database
   - USAGE, CREATE TABLE, and CREATE VIEW on the `dest_db.dest_schema` schema
   - USAGE on the `servicenow_external_access_integration` integration
   - USAGE on the `secretsdb` database
   - USAGE on the `secretsdb.apiauth` schema
   - READ on the `secretsdb.apiauth.servicenow_creds_oauth_code secret` secret

   Run the following commands:

   Copy code

   ```
   USE ROLE accountadmin;

   GRANT EXECUTE TASK ON ACCOUNT TO APPLICATION my_connector_servicenow;
   GRANT EXECUTE MANAGED TASK ON ACCOUNT TO APPLICATION my_connector_servicenow;

   GRANT USAGE ON WAREHOUSE servicenow_conn_warehouse TO APPLICATION my_connector_servicenow;

   GRANT USAGE ON DATABASE dest_db TO APPLICATION my_connector_servicenow;
   GRANT USAGE ON SCHEMA dest_db.dest_schema TO APPLICATION my_connector_servicenow;
   GRANT CREATE TABLE ON SCHEMA dest_db.dest_schema TO APPLICATION my_connector_servicenow;
   GRANT CREATE VIEW ON SCHEMA dest_db.dest_schema TO APPLICATION my_connector_servicenow;

   GRANT USAGE ON INTEGRATION servicenow_external_access_integration TO APPLICATION my_connector_servicenow;

   GRANT USAGE ON DATABASE secretsdb TO APPLICATION my_connector_servicenow;
   GRANT USAGE ON SCHEMA secretsdb.apiauth TO APPLICATION my_connector_servicenow;
   GRANT READ ON SECRET secretsdb.apiauth.servicenow_creds_oauth_code TO APPLICATION my_connector_servicenow;
   ```
5. Transfer ownership of tables and views in destination schema (optional)

   If the connector was reinstalled and previous destination schema is reused, ownership of all tables and views in
   destination schema must be transferred to the connector. The connector requires ownership privilege to manage
   grants on objects in schema and to recreate flattened views when schema of ingested table is changed.

   To transfer the ownership call `SYSTEM$GRANT_OWNERSHIP_TO_APPLICATION` function.

   Copy code

   ```
   USE ROLE accountadmin;
   CALL SYSTEM$GRANT_OWNERSHIP_TO_APPLICATION(<connector_app>, true, <destination_database>, <destination_schema>);
   ```

   The `SYSTEM$GRANT_OWNERSHIP_TO_APPLICATION` is a system function provided by Snowflake that allows the transfer of
   ownership of tables and views in a specified database or schema to the application. Only the ownership of regular tables and
   regular views is transferred, e.g. ownership of dynamic tables, external tables, materialized views, etc. won’t be
   transferred.

   The function has the following signature:

   Copy code

   ```
   SYSTEM$GRANT_OWNERSHIP_TO_APPLICATION(<to_app>, <should_copy_grants>, <from_database>, <from_schema>)
   ```

   Where:

   > `to_app`
   > :   Specifies the name of the application to which the ownership of objects should be transferred.
   >
   > `should_copy_grants`
   > :   If `TRUE` then copy existing grants, otherwise revoke. Copying grants requires `MANAGE GRANTS`
   >     permission on the caller.
   >
   > `from_database`
   > :   Name of the database containing objects whose ownership should be changed.
   >
   > `from_schema`
   > :   (Optional) name of the schema containing objects whose ownership should be changed. If no schema is specified,
   >     ownership is transferred on tables and views in all schemas in the provided database. Objects in managed schemas
   >     are omitted during ownership transfer.

   To execute the function the caller must meet one of the following conditions:

   - It has `MANAGE GRANTS` permission (e.g. ACCOUNTADMIN or SECURITYADMIN role), or
   - It contains role owning the application instance and role owning all objects to transfer the ownership. Objects on
     which the ownership is missing are omitted by the function.

   For example, to transfer ownership the connector that:

   - Was installed as application named `my_connector_servicenow`
   - Uses the schema named `dest_db.dest_schema` for the ServiceNow® data in Snowflake

   Run the following command:

   Copy code

   ```
   USE ROLE accountadmin;
   CALL SYSTEM$GRANT_OWNERSHIP_TO_APPLICATION('my_connector_servicenow', true, 'dest_db', 'dest_schema');
   ```

   If needed, grant `DATA_READER` application role to the role previously owning the data to prevent
   disruptions of existing pipelines using the data:

   Copy code

   ```
   GRANT APPLICATION ROLE <connector_app>.DATA_READER TO ROLE <previous_data_owner_role>;
   ```

   Note that `DATA_READER` application role won’t have any grants on tables and views in destination schema until
   `CONFIGURE_CONNECTOR` procedure is run.
6. Run the [USE DATABASE](/sql-reference/sql/use-database) command to use the database for the connector. For example:

   Copy code

   ```
   USE DATABASE my_connector_servicenow;
   ```
7. Configure the connector by using the [CALL](/sql-reference/sql/call) command to call the stored procedure named `CONFIGURE_CONNECTOR`:

   Copy code

   ```
   CALL CONFIGURE_CONNECTOR({
     'warehouse': '<warehouse_name>',
     'destination_database': '<dest_db>',
     'destination_schema': '<dest_schema>'
   })
   ```

   Where:

   `warehouse_name`
   :   Specifies the name of the warehouse for the connector.

       The name of the warehouse must be a valid [object identifier](/sql-reference/identifiers-syntax).

   `dest_db`
   :   Specifies the name of the
       [database for the ServiceNow® data in Snowflake (the database that you created earlier)](#label-servicenow-connector-prereqs-dest-schema-v2).

       The name of the database must be valid [object identifiers](/sql-reference/identifiers-syntax).

   `dest_schema`
   :   Specifies the name of the
       [schema for the ServiceNow® data in Snowflake (the schema that you created earlier)](#label-servicenow-connector-prereqs-dest-schema-v2).

       The name of the schema must be valid [object identifiers](/sql-reference/identifiers-syntax).

   For example, to configure the connector that:

   - Uses warehouse `servicenow_conn_warehouse`.
   - Uses the schema named `dest_db.dest_schema` for the ServiceNow® data in Snowflake

   Run the following command:

   Copy code

   ```
   CALL CONFIGURE_CONNECTOR({
     'warehouse': 'servicenow_conn_warehouse',
     'destination_database': 'dest_db',
     'destination_schema': 'dest_schema'
   });
   ```

   If the connector was started successfully, this stored procedure returns the following response:

   > Copy code
   >
   > ```
   > {
   >   "responseCode": "OK",
   >   "message": "Connector successfully configured.",
   > }
   > ```
   >
   > Note
   >
   > Once the connector is started, it’s not possible to rename passed warehouse, destination database and destination
   > schema for the connector. The connector references them by name. As a result, an attempt
   > to drop or alter the name of these objects breaks the connector and stops it from working.
   >
   > Instead of renaming the warehouse, use [UPDATE\_WAREHOUSE](/connectors/servicenow/managing#label-servicenow-connector-update-warehouse-v2)
   > stored procedure to change the warehouse used by the connector.
8. Configure the connection to ServiceNow® instance by using the [CALL](/sql-reference/sql/call) command to call the stored procedure
   named `SET_CONNECTION_CONFIGURATION`:

   Copy code

   ```
   CALL SET_CONNECTION_CONFIGURATION({
     'service_now_url': '<servicenow_base_url>',
     'secret': '<secret_name>',
     'external_access_integration': '<external_access_integration_name>'
   })
   ```

   Where:

   `servicenow_base_url`
   :   Specifies the URL of the ServiceNow® instance that the connector should use. The URL should be in the following format:

       Copy code

       ```
       https://<servicenow_instance>.service-now.com
       ```

   `secret_name`
   :   Specifies the fully qualified name of the
       [secret object containing the credentials for authenticating to ServiceNow® (the secret that you created earlier)](#label-servicenow-connector-prereqs-secret-create-v2).

       You must specify the fully qualified name of the secret object in the following format:

       Copy code

       ```
       <database_name>.<schema_name>.<secret_name>
       ```

       The names of the database, schema, and secret must be valid [object identifiers](/sql-reference/identifiers-syntax).

   `external_access_integration_name`
   :   Specifies the name of the
       [external access integration for ServiceNow® (the external access integration that you created earlier)](#label-servicenow-connector-prereqs-external-access-integration-v2).

       The name of the integration must be a valid [object identifier](/sql-reference/identifiers-syntax).

   For example, to configure the connection to a ServiceNow® instance that:

   - Has the URL `https://myinstance.service-now.com`.
   - Uses the secret stored in `secretsdb.apiauth.servicenow_creds_oauth_code`.
   - Uses the external access integration named `servicenow_external_access_integration`.

   Run the following command:

   Copy code

   ```
   CALL SET_CONNECTION_CONFIGURATION({
     'service_now_url': 'https://myinstance.service-now.com',
     'secret': 'SECRETSDB.APIAUTH.SERVICENOW_CREDS_OAUTH_CODE',
     'external_access_integration': 'SERVICENOW_API_INTEGRATION'
   });
   ```

   If the connection was configured successfully, this stored procedure returns the following response:

   Copy code

   ```
   {
     "responseCode": "OK",
     "message": "Test request to ServiceNow® succeeded.",
   }
   ```

   Note

   Once the connection is configured, it’s not possible to change name of the passed secret and external access integration. The
   connector references them by name. As a result, an attempt to drop or alter the name of these objects breaks
   the connector and stops it from working.
9. Finalize the configuration of the connector using the [CALL](/sql-reference/sql/call) command to call the stored procedure
   named `FINALIZE_CONNECTOR_CONFIGURATION`:

   Copy code

   ```
   CALL FINALIZE_CONNECTOR_CONFIGURATION({
     'journal_table': '<name_of_journal_table>',
     'table_name': '<name_of_audited_table>',
     'sys_id': '<sys_id_of_audited_entry>'
   })
   ```

   Where:

   `name_of_journal_table`
   :   Specifies the name of the table that contains information about deleted records. Refer to [Prepare your ServiceNow® instance](/connectors/servicenow/prereqs) for more information.

       Note that information on deleted records is available only for tables that you set up to propagate deleted records.

       To prevent the propagation of deleted records, specify the `null` for this argument.

   `name_of_audited_table`
   :   (optional) Specifies the name of the audited table that should be present in the journal table and to which the connector
       should have access. During validation of access to the journal table, the connector looks for audit entries related to
       this table. Provide this option when a query to ServiceNow® succeeds, but gives no result, causing the procedure to
       fail. Ensure that the ServiceNow® user for the connector has access to all entries for the specified table.

       This option can’t be used together with `sys_id` parameter.

   `sys_id_of_audited_entry`
   :   (optional) Specifies the `sys_id` of entry from some audited table that should be present in the journal table and
       to which the connector should have access. During validation of access to the journal table, the connector looks for
       audit entries related to this `sys_id`. Provide this option when a query to ServiceNow® succeeds, but gives no
       result, causing the procedure to fail. Ensure that the ServiceNow® user for the connector has access to specified
       entry.

       This option can’t be used together with `table_name` parameter.

   If the connector was started successfully, this stored procedure returns the following response:

   Copy code

   ```
   {
    "responseCode": "OK",
   }
   ```

   During finalization of the connector configuration, the connector will attempt to check if a previously exported connector
   state is present in the destination schema. If the `__CONNECTOR_STATE_EXPORT` table is present and accessible to
   the connector, the connector will try to import the state. When import finishes successfully, the export table will be
   deleted. If an error occurs during import, it’s possible to run the `FINALIZE_CONNECTOR_CONFIGURATION` procedure again
   after fixing the error. If you don’t want to import the state or you don’t want to fix the import error, transfer ownership
   of the table from the connector and drop the table.

The newly created database is an instance of the connector and contains the following:

- Stored procedures that you use to configure the connector. See
  [Set up data ingestion using SQL statements](/connectors/servicenow/ingestion#label-servicenow-connector-configuring-v2) for more information.
- Views containing the logged messages and statistics for the connector. See
  [About Monitoring the Connector](/connectors/servicenow/monitoring#label-monitoring-the-servicenow-connector-v2) for more information.

## Connector application roles

As a Native Application, Snowflake Connector for ServiceNow® defines [application roles](/developer-guide/native-apps/creating-setup-script#label-native-apps-app-roles-about).
They can be reviewed in [Role-based access control for connectors (ServiceNow)](/connectors/servicenow/application-roles).

## Sample installation scripts

The following example scripts demonstrate how to configure the Snowflake Connector for ServiceNow® using SQL worksheets.
This can help you quickly set up the connector in your environment and start using it.
Simply copy and paste the commands into the worksheet and fulfill the placeholders with your values.

Important

It’s assumed that the application is already installed in the account as described [here](#label-installing-the-servicenow-connector-sql).

Before executing the commands, review the script and adjust to your needs:

Basic AuthOAuth Authorization CodeOAuth Client Credentials

Copy code

```
-- Specify values as required by your installation
SET application_name = 'SNOWFLAKE_CONNECTOR_FOR_SERVICENOW'; -- use the same name as provided in the installation
SET connector_warehouse = 'SNOWFLAKE_CONNECTOR_FOR_SERVICENOW_WAREHOUSE';
SET servicenow_instance_domain = '<servicenow_instance>.service-now.com';

SET destination_database = 'SNOWFLAKE_CONNECTOR_FOR_SERVICENOW_DEST_DB';
SET destination_schema = 'SNOWFLAKE_CONNECTOR_FOR_SERVICENOW_DEST_SCHEMA';

SET secret_database = 'CONNECTORS_SECRET';
SET secret_schema = 'SNOWFLAKE_CONNECTOR_FOR_SERVICENOW';
SET secret_database_schema = $secret_database || '.' || $secret_schema;
SET secret_fqn = $secret_database_schema || '.' || 'SECRET';

SET network_rule_fqn = $secret_database_schema || '.' || 'NETWORK_RULE';
SET external_access_integration_name = 'SNOWFLAKE_CONNECTOR_FOR_SERVICENOW_EXTERNAL_ACCESS_INTEGRATION';

SET destination_database_schema = $destination_database || '.' || $destination_schema;
SET servicenow_instance_url = 'https://' || $servicenow_instance_domain || '/';

-- Create essential objects
USE ROLE accountadmin;

CREATE WAREHOUSE IF NOT EXISTS IDENTIFIER($connector_warehouse)
   WAREHOUSE_SIZE = 'MEDIUM'
   AUTO_RESUME = TRUE;
CREATE DATABASE IF NOT EXISTS IDENTIFIER($secret_database);
CREATE SCHEMA IF NOT EXISTS IDENTIFIER($secret_database_schema);
CREATE DATABASE IF NOT EXISTS IDENTIFIER($destination_database);
CREATE SCHEMA IF NOT EXISTS IDENTIFIER($destination_database_schema);

-- Populate with your credentials
CREATE SECRET IDENTIFIER($secret_fqn)
   TYPE = PASSWORD
   USERNAME = '<servicenow_login>'
   PASSWORD = '<servicenow_password>';

-- None of the following commands should require any changes
CREATE NETWORK RULE IDENTIFIER($network_rule_fqn)
   MODE = 'EGRESS'
   TYPE = 'HOST_PORT'
   VALUE_LIST = ($servicenow_instance_domain);

CREATE PROCEDURE execute_immediate_create_ea_integration()
RETURNS VARIANT
EXECUTE AS caller
AS
BEGIN
   EXECUTE IMMEDIATE '
      CREATE EXTERNAL ACCESS INTEGRATION IDENTIFIER($external_access_integration_name)
      ALLOWED_NETWORK_RULES = ($network_rule_fqn)
      ALLOWED_AUTHENTICATION_SECRETS = ('  ||  $secret_fqn  ||  ') ENABLED = TRUE
   ';
END;
CALL execute_immediate_create_ea_integration();
DROP PROCEDURE IF EXISTS execute_immediate_create_ea_integration();

GRANT EXECUTE TASK ON ACCOUNT TO APPLICATION IDENTIFIER($application_name);
GRANT EXECUTE MANAGED TASK ON ACCOUNT TO APPLICATION IDENTIFIER($application_name);

GRANT USAGE ON WAREHOUSE IDENTIFIER($connector_warehouse) TO APPLICATION IDENTIFIER($application_name);
GRANT USAGE ON DATABASE IDENTIFIER($destination_database) TO APPLICATION IDENTIFIER($application_name);
GRANT USAGE ON SCHEMA IDENTIFIER($destination_database_schema) TO APPLICATION IDENTIFIER($application_name);

GRANT CREATE TABLE ON SCHEMA IDENTIFIER($destination_database_schema) TO APPLICATION IDENTIFIER($application_name);
GRANT CREATE VIEW ON SCHEMA IDENTIFIER($destination_database_schema) TO APPLICATION IDENTIFIER($application_name);

GRANT USAGE ON INTEGRATION IDENTIFIER($external_access_integration_name) TO APPLICATION IDENTIFIER($application_name);
GRANT USAGE ON DATABASE IDENTIFIER($secret_database) TO APPLICATION IDENTIFIER($application_name);
GRANT USAGE ON SCHEMA IDENTIFIER($secret_database_schema) TO APPLICATION IDENTIFIER($application_name);
GRANT READ ON SECRET IDENTIFIER($secret_fqn) TO APPLICATION IDENTIFIER($application_name);

CALL SYSTEM$GRANT_OWNERSHIP_TO_APPLICATION($application_name, true, $destination_database, $destination_schema);

USE APPLICATION IDENTIFIER($application_name);

-- Recommended to call one by one as the response might contain an error
CALL CONFIGURE_CONNECTOR({
   'warehouse': $connector_warehouse,
   'destination_database': $destination_database,
   'destination_schema': $destination_schema
});

CALL SET_CONNECTION_CONFIGURATION({
   'service_now_url': $servicenow_instance_url,
   'secret': $secret_fqn,
   'external_access_integration': $external_access_integration_name
});

-- Remove the 'journal_table' parameter if you don't want to track deleted records
CALL FINALIZE_CONNECTOR_CONFIGURATION({
   'journal_table': 'sys_audit_delete'
});
```

Copy code

```
-- Specify values as required by your installation
SET application_name = 'SNOWFLAKE_CONNECTOR_FOR_SERVICENOW'; -- use the same name as provided in the installation
SET connector_warehouse = 'SNOWFLAKE_CONNECTOR_FOR_SERVICENOW_WAREHOUSE';
SET servicenow_instance_domain = '<servicenow_instance>.service-now.com';

SET destination_database = 'SNOWFLAKE_CONNECTOR_FOR_SERVICENOW_DEST_DB';
SET destination_schema = 'SNOWFLAKE_CONNECTOR_FOR_SERVICENOW_DEST_SCHEMA';

SET secret_database = 'CONNECTORS_SECRET';
SET secret_schema = 'SNOWFLAKE_CONNECTOR_FOR_SERVICENOW';
SET secret_database_schema = $secret_database || '.' || $secret_schema;
SET secret_fqn = $secret_database_schema || '.' || 'SECRET';

SET network_rule_fqn = $secret_database_schema || '.' || 'NETWORK_RULE';
SET external_access_integration_name = 'SNOWFLAKE_CONNECTOR_FOR_SERVICENOW_EXTERNAL_ACCESS_INTEGRATION';
SET security_integration_name = 'SNOWFLAKE_CONNECTOR_FOR_SERVICENOW_SECURITY_INTEGRATION';

SET destination_database_schema = $destination_database || '.' || $destination_schema;
SET servicenow_instance_url = 'https://' || $servicenow_instance_domain || '/';
SET oauth_token_endpoint = $servicenow_instance_url || 'oauth_token.do';

-- Create essential objects
USE ROlE accountadmin;

CREATE WAREHOUSE IF NOT EXISTS IDENTIFIER($connector_warehouse)
   WAREHOUSE_SIZE = 'MEDIUM'
   AUTO_RESUME = TRUE;
CREATE DATABASE IF NOT EXISTS IDENTIFIER($secret_database);
CREATE SCHEMA IF NOT EXISTS IDENTIFIER($secret_database_schema);
CREATE DATABASE IF NOT EXISTS IDENTIFIER($destination_database);
CREATE SCHEMA IF NOT EXISTS IDENTIFIER($destination_database_schema);

-- Populate with your credentials
CREATE SECURITY INTEGRATION IDENTIFIER($security_integration_name)
   TYPE = API_AUTHENTICATION
   AUTH_TYPE = OAUTH2
   OAUTH_CLIENT_AUTH_METHOD = CLIENT_SECRET_POST
   OAUTH_CLIENT_ID = '<client_id>'
   OAUTH_CLIENT_SECRET = '<client_secret>'
   OAUTH_TOKEN_ENDPOINT = $oauth_token_endpoint
   ENABLED = TRUE;

CREATE SECRET IDENTIFIER($secret_fqn)
   TYPE = OAUTH2
   OAUTH_REFRESH_TOKEN = '<refresh_token>'
   OAUTH_REFRESH_TOKEN_EXPIRY_TIME = '<expiry time>'
   API_AUTHENTICATION = $security_integration_name;

-- None of the following commands should require any changes
CREATE NETWORK RULE IDENTIFIER($network_rule_fqn)
   MODE = 'EGRESS'
   TYPE = 'HOST_PORT'
   VALUE_LIST = ($servicenow_instance_domain);

CREATE PROCEDURE execute_immediate_create_ea_integration()
RETURNS VARIANT
EXECUTE AS caller
AS
BEGIN
   EXECUTE IMMEDIATE '
      CREATE EXTERNAL ACCESS INTEGRATION IDENTIFIER($external_access_integration_name)
      ALLOWED_NETWORK_RULES = ($network_rule_fqn)
      ALLOWED_AUTHENTICATION_SECRETS = ('  ||  $secret_fqn  ||  ') ENABLED = TRUE
   ';
END;
CALL execute_immediate_create_ea_integration();
DROP PROCEDURE IF EXISTS execute_immediate_create_ea_integration();

GRANT EXECUTE TASK ON ACCOUNT TO APPLICATION IDENTIFIER($application_name);
GRANT EXECUTE MANAGED TASK ON ACCOUNT TO APPLICATION IDENTIFIER($application_name);

GRANT USAGE ON WAREHOUSE IDENTIFIER($connector_warehouse) TO APPLICATION IDENTIFIER($application_name);
GRANT USAGE ON DATABASE IDENTIFIER($destination_database) TO APPLICATION IDENTIFIER($application_name);
GRANT USAGE ON SCHEMA IDENTIFIER($destination_database_schema) TO APPLICATION IDENTIFIER($application_name);

GRANT CREATE TABLE ON SCHEMA IDENTIFIER($destination_database_schema) TO APPLICATION IDENTIFIER($application_name);
GRANT CREATE VIEW ON SCHEMA IDENTIFIER($destination_database_schema) TO APPLICATION IDENTIFIER($application_name);

GRANT USAGE ON INTEGRATION IDENTIFIER($external_access_integration_name) TO APPLICATION IDENTIFIER($application_name);
GRANT USAGE ON DATABASE IDENTIFIER($secret_database) TO APPLICATION IDENTIFIER($application_name);
GRANT USAGE ON SCHEMA IDENTIFIER($secret_database_schema) TO APPLICATION IDENTIFIER($application_name);
GRANT READ ON SECRET IDENTIFIER($secret_fqn) TO APPLICATION IDENTIFIER($application_name);

CALL SYSTEM$GRANT_OWNERSHIP_TO_APPLICATION($application_name, true, $destination_database, $destination_schema);

USE APPLICATION IDENTIFIER($application_name);

-- Recommended to call one by one as the response might contain an error
CALL CONFIGURE_CONNECTOR({
   'warehouse': $connector_warehouse,
   'destination_database': $destination_database,
   'destination_schema': $destination_schema
});

CALL SET_CONNECTION_CONFIGURATION({
   'service_now_url': $servicenow_instance_url,
   'secret': $secret_fqn,
   'external_access_integration': $external_access_integration_name
});

-- Remove the 'journal_table' parameter if you don't want to track deleted records
CALL FINALIZE_CONNECTOR_CONFIGURATION({
   'journal_table': 'sys_audit_delete'
});
```

Copy code

```
-- Specify values as required by your installation
SET application_name = 'SNOWFLAKE_CONNECTOR_FOR_SERVICENOW'; -- use the same name as provided in the installation
SET connector_warehouse = 'SNOWFLAKE_CONNECTOR_FOR_SERVICENOW_WAREHOUSE';
SET servicenow_instance_domain = '<servicenow_instance>.service-now.com';

SET destination_database = 'SNOWFLAKE_CONNECTOR_FOR_SERVICENOW_DEST_DB';
SET destination_schema = 'SNOWFLAKE_CONNECTOR_FOR_SERVICENOW_DEST_SCHEMA';

SET secret_database = 'CONNECTORS_SECRET';
SET secret_schema = 'SNOWFLAKE_CONNECTOR_FOR_SERVICENOW';
SET secret_database_schema = $secret_database || '.' || $secret_schema;
SET secret_fqn = $secret_database_schema || '.' || 'SECRET';

SET network_rule_fqn = $secret_database_schema || '.' || 'NETWORK_RULE';
SET external_access_integration_name = 'SNOWFLAKE_CONNECTOR_FOR_SERVICENOW_EXTERNAL_ACCESS_INTEGRATION';
SET security_integration_name = 'SNOWFLAKE_CONNECTOR_FOR_SERVICENOW_SECURITY_INTEGRATION';

SET destination_database_schema = $destination_database || '.' || $destination_schema;
SET servicenow_instance_url = 'https://' || $servicenow_instance_domain || '/';
SET oauth_token_endpoint = $servicenow_instance_url || 'oauth_token.do';

-- Create essential objects
USE ROlE accountadmin;

CREATE WAREHOUSE IF NOT EXISTS IDENTIFIER($connector_warehouse)
   WAREHOUSE_SIZE = 'MEDIUM'
   AUTO_RESUME = TRUE;
CREATE DATABASE IF NOT EXISTS IDENTIFIER($secret_database);
CREATE SCHEMA IF NOT EXISTS IDENTIFIER($secret_database_schema);
CREATE DATABASE IF NOT EXISTS IDENTIFIER($destination_database);
CREATE SCHEMA IF NOT EXISTS IDENTIFIER($destination_database_schema);

-- Populate with your credentials
CREATE SECURITY INTEGRATION IDENTIFIER($security_integration_name)
   TYPE = API_AUTHENTICATION
   AUTH_TYPE = OAUTH2
   OAUTH_CLIENT_AUTH_METHOD = CLIENT_SECRET_POST
   OAUTH_CLIENT_ID = '<client_id>'
   OAUTH_CLIENT_SECRET = '<client_secret>'
   OAUTH_TOKEN_ENDPOINT = $oauth_token_endpoint
   OAUTH_GRANT = 'CLIENT_CREDENTIALS'
   OAUTH_ALLOWED_SCOPES = ('useraccount')
   ENABLED = TRUE;

CREATE SECRET IDENTIFIER($secret_fqn)
   TYPE = OAUTH2
   API_AUTHENTICATION = $security_integration_name
   OAUTH_SCOPES=('useraccount');

-- None of the following commands should require any changes
CREATE NETWORK RULE IDENTIFIER($network_rule_fqn)
   MODE = 'EGRESS'
   TYPE = 'HOST_PORT'
   VALUE_LIST = ($servicenow_instance_domain);

CREATE PROCEDURE execute_immediate_create_ea_integration()
RETURNS VARIANT
EXECUTE AS caller
AS
BEGIN
   EXECUTE IMMEDIATE '
      CREATE EXTERNAL ACCESS INTEGRATION IDENTIFIER($external_access_integration_name)
      ALLOWED_NETWORK_RULES = ($network_rule_fqn)
      ALLOWED_AUTHENTICATION_SECRETS = ('  ||  $secret_fqn  ||  ') ENABLED = TRUE
   ';
END;
CALL execute_immediate_create_ea_integration();
DROP PROCEDURE IF EXISTS execute_immediate_create_ea_integration();

GRANT EXECUTE TASK ON ACCOUNT TO APPLICATION IDENTIFIER($application_name);
GRANT EXECUTE MANAGED TASK ON ACCOUNT TO APPLICATION IDENTIFIER($application_name);

GRANT USAGE ON WAREHOUSE IDENTIFIER($connector_warehouse) TO APPLICATION IDENTIFIER($application_name);
GRANT USAGE ON DATABASE IDENTIFIER($destination_database) TO APPLICATION IDENTIFIER($application_name);
GRANT USAGE ON SCHEMA IDENTIFIER($destination_database_schema) TO APPLICATION IDENTIFIER($application_name);

GRANT CREATE TABLE ON SCHEMA IDENTIFIER($destination_database_schema) TO APPLICATION IDENTIFIER($application_name);
GRANT CREATE VIEW ON SCHEMA IDENTIFIER($destination_database_schema) TO APPLICATION IDENTIFIER($application_name);

GRANT USAGE ON INTEGRATION IDENTIFIER($external_access_integration_name) TO APPLICATION IDENTIFIER($application_name);
GRANT USAGE ON DATABASE IDENTIFIER($secret_database) TO APPLICATION IDENTIFIER($application_name);
GRANT USAGE ON SCHEMA IDENTIFIER($secret_database_schema) TO APPLICATION IDENTIFIER($application_name);
GRANT READ ON SECRET IDENTIFIER($secret_fqn) TO APPLICATION IDENTIFIER($application_name);

CALL SYSTEM$GRANT_OWNERSHIP_TO_APPLICATION($application_name, true, $destination_database, $destination_schema);

USE APPLICATION IDENTIFIER($application_name);

-- Recommended to call one by one as the response might contain an error
CALL CONFIGURE_CONNECTOR({
   'warehouse': $connector_warehouse,
   'destination_database': $destination_database,
   'destination_schema': $destination_schema
});

CALL SET_CONNECTION_CONFIGURATION({
   'service_now_url': $servicenow_instance_url,
   'secret': $secret_fqn,
   'external_access_integration': $external_access_integration_name
});

-- Remove the 'journal_table' parameter if you don't want to track deleted records
CALL FINALIZE_CONNECTOR_CONFIGURATION({
   'journal_table': 'sys_audit_delete'
});
```

## Next steps

After installing and configuring the connector, perform the steps described in [Set up data ingestion for your ServiceNow® data](/connectors/servicenow/ingestion).
