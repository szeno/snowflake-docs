# Configure Snowflake OAuth for partner applications

This topic explains how to configure Snowflake OAuth access to Snowflake for supported Snowflake partner applications. This process
requires creating an integration, a first-class Snowflake object that defines the interface between Snowflake and a third-party application
or service.

Important

When connecting to Snowflake using any third-party application, Snowflake recommends that you verify that the integration flow used by
the application meets your internal security requirements. You can contact the partner directly for details on their end-to-end flow used
for this feature.

Note

In-session role switching to secondary roles is not supported with Snowflake OAuth.

If this behavior is necessary with your OAuth workflow, use External OAuth instead.

For more information, see [Using secondary roles with External OAuth](/user-guide/oauth-ext-overview#label-ext-oauth-secondary-roles).

Currently, Snowflake OAuth supports the following applications:

| Client | Required Client Version | Client Type |
| --- | --- | --- |
| [Tableau Desktop / Cloud](https://www.tableau.com/) [[1]](#footnote-1) | 2019.1 or higher | Public |
| [Looker](https://looker.com) [[2]](#footnote-2) | 6.20 or higher |  |
| [Alation](https://www.alation.com/) | See the [Alation documentation](#label-snowflake-oauth-login-alation) |  |
| [ThoughtSpot](https://thoughtspot.com) | See the [ThoughtSpot documentation](#label-snowflake-oauth-login-thoughtspot) |  |
| [Collibra](https://www.collibra.com) | See the [Collibra documentation](#label-snowflake-oauth-login-collibra) |  |

Expand

Show lessSee more

[1]
If Tableau Cloud (version 2024.2 or higher) is connecting to Snowflake using private connectivity to the Snowflake service, you need
to use a custom security integration rather than the integration designed for a partner application. The redirect URL of the custom
integration must use the following URL form: `https://<your_server_url>/auth/add_oauth_token`. For instructions, see
[Configure Snowflake OAuth for custom clients](/user-guide/oauth-custom). Tableau Desktop, Tableau Online, and Tableau Server (version 2024.2 or lower) continue to use the partner
application integration regardless of whether it uses a private URL.

[2]
Looker supports OAuth only when Looker-hosted instances can access the public Internet. Note that this limitation does not
affect customer-hosted Looker implementations (i.e. on-premises implementations). Customers using
private connectivity to the Snowflake service might experience issues if attempting to use OAuth and Looker with Snowflake. Please contact Looker for questions or more details.

## Configuring a Snowflake OAuth integration

Create an integration using the [CREATE SECURITY INTEGRATION](/sql-reference/sql/create-security-integration-oauth-snowflake) command. An integration is a Snowflake object that
provides an interface between Snowflake and third-party services, such as a client that supports Snowflake OAuth.

Note

Only account administrators (i.e users with the ACCOUNTADMIN system role) or a role with the global CREATE INTEGRATION privilege can
execute this SQL command.

Copy code

```
CREATE [ OR REPLACE ] SECURITY INTEGRATION [ IF NOT EXISTS ]
  <name>
  TYPE = OAUTH
  ENABLED = { TRUE | FALSE }
  OAUTH_CLIENT = <partner_application>
  oauthClientParams
  [ COMMENT = '<string_literal>' ]
```

Where:

> **oauthClientParams**
>
> > Copy code
> >
> > ```
> > oauthClientParams ::=
> >   [ OAUTH_ISSUE_REFRESH_TOKENS = TRUE | FALSE ]
> >   [ OAUTH_ACCESS_TOKEN_VALIDITY = <integer> ]
> >   [ OAUTH_REFRESH_TOKEN_VALIDITY = <integer> ]
> >   [ BLOCKED_ROLES_LIST = ('<role_name>', '<role_name>') ]
> > ```

### Blocking specific roles from using the integration

The optional BLOCKED\_ROLES\_LIST parameter allows you to list Snowflake roles that a user cannot explicitly consent to using with
the integration.

By default, the ACCOUNTADMIN, SECURITYADMIN, GLOBALORGADMIN, and ORGADMIN roles are included in this list and cannot be removed. If you have a business
need to allow users to use Snowflake OAuth with these roles, and your security team allows it, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support) to request that these roles be allowed for your account.

### Controlling the login frequency

When a user has authenticated successfully, the partner application can use the issued refresh token to request new, short-lived access
tokens, and not prompt the user to repeat the login process until the refresh token expires. The optional OAUTH\_REFRESH\_TOKEN\_VALIDITY
parameter specifies the length of time a refresh token is valid (in seconds). This setting can be used to expire the refresh token
periodically, forcing the user to repeat the login process.

The supported minimum, maximum, and default values for the OAUTH\_REFRESH\_TOKEN\_VALIDITY parameter are as follows:

| Application | Minimum | Maximum | Default |
| --- | --- | --- | --- |
| Tableau Desktop | `60` (1 minute) | `36000` (10 hours) | `36000` (10 hours) |
| Tableau Cloud | `60` (1 minute) | `7776000` (90 days) | `7776000` (90 days) |

Expand

Show lessSee more

If you have a business need to lower the minimum value or raise the maximum value, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support) to request the change for
your account.

### Controlling access token validity

The optional `OAUTH_ACCESS_TOKEN_VALIDITY` parameter specifies how long an access token is valid (in seconds). Access tokens are
short-lived. The default is 600 seconds (10 minutes). You can set the value anywhere between 60 seconds (1 minute) and 3600 seconds
(1 hour).

When an access token expires, the partner application can use a refresh token to request a new access token without prompting the user to
log in again, as long as the refresh token is still valid.

### Using Client Redirect with Snowflake OAuth for partner applications

Snowflake supports using Client Redirect with Snowflake OAuth for Partner Applications, including using Client Redirect and Snowflake OAuth
with supported Snowflake Clients.

For more information, see [Redirecting client connections](/user-guide/client-redirect).

### Managing network policies

Snowflake supports network policies for Looker, but not other partner applications.
For more information, see [Restricting network traffic for Snowflake OAuth](/user-guide/oauth-snowflake-overview#label-snow-oauth-network-policies).

### Examples

**Tableau Desktop**

> The following example creates a Snowflake OAuth integration with the default settings:
>
> Copy code
>
> ```
> CREATE SECURITY INTEGRATION td_oauth_int1
>   TYPE = OAUTH
>   ENABLED = TRUE
>   OAUTH_CLIENT = TABLEAU_DESKTOP;
> ```
>
> View the integration settings using [DESCRIBE INTEGRATION](/sql-reference/sql/desc-integration):
>
> Copy code
>
> ```
> DESC SECURITY INTEGRATION td_oauth_int1;
> ```
>
> The following example creates a Snowflake OAuth integration with refresh tokens that expire after 10 hours (36000 seconds). The
> integration blocks users from starting a session with SYSADMIN as the active role:
>
> Copy code
>
> ```
> CREATE SECURITY INTEGRATION td_oauth_int2
>   TYPE = OAUTH
>   ENABLED = TRUE
>   OAUTH_REFRESH_TOKEN_VALIDITY = 36000
>   BLOCKED_ROLES_LIST = ('SYSADMIN')
>   OAUTH_CLIENT = TABLEAU_DESKTOP;
> ```

**Tableau Cloud**

> The following example creates a Snowflake OAuth integration with the default settings:
>
> Copy code
>
> ```
> CREATE SECURITY INTEGRATION ts_oauth_int1
>   TYPE = OAUTH
>   ENABLED = TRUE
>   OAUTH_CLIENT = TABLEAU_SERVER;
> ```
>
> View the integration settings using [DESCRIBE INTEGRATION](/sql-reference/sql/desc-integration):
>
> Copy code
>
> ```
> DESC SECURITY INTEGRATION ts_oauth_int1;
> ```
>
> The following example creates a Snowflake OAuth integration with refresh tokens that expire after 1 day (86400 seconds). The integration
> blocks users from starting a session with SYSADMIN as the active role:
>
> Copy code
>
> ```
> CREATE SECURITY INTEGRATION ts_oauth_int2
>   TYPE = OAUTH
>   ENABLED = TRUE
>   OAUTH_CLIENT = TABLEAU_SERVER
>   OAUTH_REFRESH_TOKEN_VALIDITY = 86400
>   BLOCKED_ROLES_LIST = ('SYSADMIN');
> ```

## Logging in to Snowflake from a partner application

### Tableau

Follow the [instructions](https://onlinehelp.tableau.com/current/pro/desktop/en-us/examples_snowflake.htm) provided by Tableau to connect
to Snowflake using Snowflake OAuth.

### Looker

Follow the [steps](https://docs.looker.com/setup-and-management/database-config/snowflake#oauth) provided by Looker to connect to
Snowflake using Snowflake OAuth.

### Alation

Access the [Alation Community](https://community.alation.com/home) and follow the instructions provided by Alation to connect to
Snowflake using Snowflake OAuth.

### ThoughtSpot

Access the [ThoughtSpot documentation](https://docs.thoughtspot.com/software/latest/connections-snowflake) and follow
the instructions to create a connection to Snowflake, which includes a step on how to configure
[Snowflake OAuth](https://docs.thoughtspot.com/software/latest/connections-snowflake-oauth.html).

### Collibra

Access the [Collibra Documentation](https://productresources.collibra.com/docs/collibra/latest/Content/Edge/JDBCConnections/ta_create-jdbc-connection.htm?catalog-connector-details=snowflake-native) and follow the instructions provided by Collibra to connect to Snowflake using Snowflake OAuth.

## Managing user consent

This section describes how to manage delegated authorizations, i.e. user consent given to one or more clients associated with Snowflake
integrations.

### Display Snowflake OAuth consents

List the active delegated authorizations for which you have access privileges, using
[SHOW DELEGATED AUTHORIZATIONS](/sql-reference/sql/show-delegated-authorizations):

Copy code

```
SHOW DELEGATED AUTHORIZATIONS;

+-------------------------------+-----------+-----------+-------------------+--------------------+
| created_on                    | user_name | role_name | integration_name  | integration_status |
|-------------------------------+-----------+-----------+-------------------+--------------------|
| 2018-11-27 07:43:10.914 -0800 | JSMITH    | PUBLIC    | MY_OAUTH_INT      | ENABLED            |
+-------------------------------+-----------+-----------+-------------------+--------------------+
```

List the active delegated authorizations for a specified user. Users can list their own delegated authorizations; otherwise, this command
variant requires the OWNERSHIP privilege on the user.

Copy code

```
SHOW DELEGATED AUTHORIZATIONS
    BY USER <username>;
```

List the active delegated authorizations for a specified integration. This command variant requires the OWNERSHIP privilege on the
integration (i.e. the ACCOUNTADMIN role):

Copy code

```
SHOW DELEGATED AUTHORIZATIONS
    TO SECURITY INTEGRATION <integration_name>;
```

### Revoke consent

A user can revoke consent from a specified integration. This has the effect of revoking any access token associated with the integration.

To revoke user consent for a given integration, execute the [ALTER USER](/sql-reference/sql/alter-user) … REMOVE DELEGATED AUTHORIZATIONS command.

Note

Only security administrators (i.e. users with the SECURITYADMIN role) or higher can execute this SQL command.

Copy code

```
ALTER USER <username> REMOVE DELEGATED AUTHORIZATIONS
    FROM SECURITY INTEGRATION <integration_name>
```

Where:

`username`
:   Specifies the user whose consent you are revoking.

`integration_name`
:   Specifies the integration associated with the access tokens for a specific client.

To revoke user consent associated with a specific role, include the `OF ROLE role_name` parameter in the statement:

Copy code

```
ALTER USER <username> REMOVE DELEGATED AUTHORIZATION
    OF ROLE <role_name>
    FROM SECURITY INTEGRATION <integration_name>
```

Where:

`role_name`
:   Specifies the role associated with the access token.

Any access tokens associated with the role are revoked.

## Error codes

See the [Error codes](/user-guide/oauth-snowflake-overview#label-oauth-snowflake-error-codes) for a list of error codes associated with OAuth, as well as errors that are returned in the JSON
blob, during the authorization flow, token request or exchange, or when creating a Snowflake session after completing the OAuth flow.
