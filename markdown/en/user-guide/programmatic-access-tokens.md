# Using programmatic access tokens for authentication

You can use a programmatic access token to authenticate to the following Snowflake endpoints:

- [Snowflake REST APIs](/developer-guide/snowflake-rest-api/snowflake-rest-api).
- The [Snowflake SQL API](/developer-guide/sql-api/index).
- The [Snowflake Catalog SDK](/user-guide/tables-iceberg-catalog).
- [Snowpark Container Services](/developer-guide/snowpark-container-services/working-with-services) endpoints.
- [Snowflake Horizon Catalog endpoint](/user-guide/tables-iceberg-access-using-external-query-engine-snowflake-horizon)
- The Spark runtime hosted on Snowflake with Snowpark Connect for Spark. For more information, see [Develop with a local IDE](/developer-guide/snowpark-connect/snowpark-connect-local-ide#label-snowpark-connect-local-ide).
- [SCIM API requests](/user-guide/scim-authentication).

You can also use a [programmatic access token as a replacement for a password](#label-pat-use-password) in the following:

- [Snowflake drivers](/developer-guide/drivers).
- Third-party applications that connect to Snowflake (such as Tableau and Power BI).
- Snowflake APIs and libraries (such as the [Snowpark API](/developer-guide/snowpark/index) and the
  [Snowflake Python API](/developer-guide/snowflake-python-api/snowflake-python-overview)).
- Snowflake command-line clients (such as the [Snowflake CLI](/developer-guide/snowflake-cli/index) and
  [SnowSQL](/user-guide/snowsql)).

You can generate programmatic access tokens for human users (users with TYPE=PERSON) as well as service users (users with
TYPE=SERVICE or TYPE=SERVICE\_AGENT).

## Prerequisites

You must fulfill the following prerequisites to generate and use programmatic access tokens:

- [Network policy requirements](#label-pat-prerequisites-network)
- [Authentication policy requirements](#label-pat-prerequisites-authentication)

### Network policy requirements

By default, the user must be subject to a [network policy](/user-guide/network-policies) with one or more
[network rules](/user-guide/network-rules) to generate or use programmatic access tokens:

- For service users (where TYPE=SERVICE or TYPE=LEGACY\_SERVICE for the user), you can only generate or use a token if the user
  is subject to a network policy.

  This prerequisite limits the use of the token to requests from a specific set of addresses or network identifiers.
- For service agent users (where TYPE=SERVICE\_AGENT for the user), you can generate and use a token even if the user is not subject to a
  network policy.
- For human users (where TYPE=PERSON for the user), you can generate a token even if the user is not subject to a network policy,
  but the user must be subject to a network policy to authenticate with this token.

  If a human user who is not subject to a network policy needs to use a programmatic access token for authentication, you can
  temporarily bypass the requirement of having a network policy, but we don’t recommend this. See [Generating a programmatic access token](#label-pat-generate).

  Note

  Users cannot bypass the network policy itself.

The network policy can be activated [for all users in the account](/user-guide/network-policies#label-associating-network-policies-with-an-account) or
[for a specific user](/user-guide/network-policies#label-associating-network-policies-user).

To change this requirement, create or modify an [authentication policy](/user-guide/authentication-policies) that specifies
a programmatic access token policy.

To create an authentication policy:

1. Execute the [CREATE AUTHENTICATION POLICY](/sql-reference/sql/create-authentication-policy) or [ALTER AUTHENTICATION POLICY](/sql-reference/sql/alter-authentication-policy)
   command. In the PAT\_POLICY clause, set NETWORK\_POLICY\_EVALUATION to one of the following values:

   `ENFORCED_REQUIRED` (default behavior)
   :   The user must be subject to a network policy to generate and use programmatic access tokens.

       If the user is subject to a network policy, the network policy is enforced during authentication.

   `ENFORCED_NOT_REQUIRED`
   :   The user does not need to be subject to a network policy to generate and use programmatic access tokens.

       If the user is subject to a network policy, the network policy is enforced during authentication.

   `NOT_ENFORCED`
   :   The user does not need to be subject to a network policy to generate and use programmatic access tokens.

       If the user is subject to a network policy, the network policy is not enforced during authentication.

   For example, to create an authentication policy that removes the network policy requirement but enforces any network policy
   that the user is subject to:

   Copy code

   ```
   CREATE AUTHENTICATION POLICY my_authentication_policy
     PAT_POLICY=(
    NETWORK_POLICY_EVALUATION = ENFORCED_NOT_REQUIRED
     );
   ```
2. [Apply the authentication policy to an account or user](/user-guide/authentication-policies#label-authentication-policy-set).

The following example alters an existing authentication policy to remove the network policy requirement and prevent the
enforcement of any network policy that the user is subject to:

Copy code

```
ALTER AUTHENTICATION POLICY my_authentication_policy
  SET PAT_POLICY = (
    NETWORK_POLICY_EVALUATION = NOT_ENFORCED
  );
```

### Authentication policy requirements

If there is an [authentication policy](/user-guide/authentication-policies) that limits the authentication methods for a
user, the user cannot generate and use programmatic access tokens unless the AUTHENTICATION\_METHODS list in that policy includes
`'PROGRAMMATIC_ACCESS_TOKEN'`.

For example, suppose that an authentication policy limits users to using the OAuth and password methods to authenticate:

Copy code

```
CREATE AUTHENTICATION POLICY my_auth_policy
  ...
  AUTHENTICATION_METHODS = ('OAUTH', 'PASSWORD')
  ...
```

Users can’t generate and use programmatic access tokens unless you add `'PROGRAMMATIC_ACCESS_TOKEN'` to the
AUTHENTICATION\_METHODS list. You can use the [ALTER AUTHENTICATION POLICY](/sql-reference/sql/alter-authentication-policy) command to update this list.

For example:

Copy code

```
ALTER AUTHENTICATION POLICY my_auth_policy
  SET AUTHENTICATION_METHODS = ('OAUTH', 'PASSWORD', 'PROGRAMMATIC_ACCESS_TOKEN');
```

## Configuring the default and maximum expiration time

Administrators (users with the ACCOUNTADMIN role) can configure the following settings that affect the expiration time of
programmatic access tokens:

- [Setting the maximum expiration time](#label-pat-maximum-expiration-time)
- [Setting the default expiration time](#label-pat-default-expiration-time)

### Setting the maximum expiration time

By default, you can specify an expiration time up to 365 days for a token. If you want to reduce this to a shorter time, create
or modify an [authentication policy](/user-guide/authentication-policies) that specifies a programmatic access token policy
with a maximum expiration time.

Execute the [CREATE AUTHENTICATION POLICY](/sql-reference/sql/create-authentication-policy) or [ALTER AUTHENTICATION POLICY](/sql-reference/sql/alter-authentication-policy)
command. In the PAT\_POLICY clause, set MAX\_EXPIRY\_IN\_DAYS to a value ranging from the
[default expiration time](#label-pat-default-expiration-time) to `365`.

For example, to create an authentication policy that sets the maximum to 100 days:

Copy code

```
CREATE AUTHENTICATION POLICY my_authentication_policy
  PAT_POLICY=(
    MAX_EXPIRY_IN_DAYS=100
  );
```

Then, [apply the authentication policy to an account or user](/user-guide/authentication-policies#label-authentication-policy-set).

As another example, to alter an existing authentication policy to set the maximum to 90 days:

Copy code

```
ALTER AUTHENTICATION POLICY my_authentication_policy
  SET PAT_POLICY = (
    MAX_EXPIRY_IN_DAYS=90
  );
```

Note

If there are existing programmatic access tokens with expiration times that exceed the new maximum expiration time, attempts to
authenticate with those tokens will fail.

For example, suppose that you generate a programmatic access token named `my_token` with the expiration time of 7 days. If you
later change the maximum expiration time for all tokens to 2 days, authenticating with `my_token` will fail because the
expiration time of the token exceeds the new maximum expiration time.

### Setting the default expiration time

By default, a programmatic access token expires after 15 days. If you want to change this, create or modify an
[authentication policy](/user-guide/authentication-policies) that specifies a programmatic access token policy with a
default expiration.

Execute the [CREATE AUTHENTICATION POLICY](/sql-reference/sql/create-authentication-policy) or [ALTER AUTHENTICATION POLICY](/sql-reference/sql/alter-authentication-policy)
command. In the PAT\_POLICY clause, set DEFAULT\_EXPIRY\_IN\_DAYS to a value ranging from `1` to the
[maximum expiration time](#label-pat-maximum-expiration-time).

For example, to create an authentication policy that sets the default to 5 days:

Copy code

```
CREATE AUTHENTICATION POLICY my_authentication_policy
  PAT_POLICY=(
    DEFAULT_EXPIRY_IN_DAYS=5
  );
```

Then, [apply the authentication policy to an account or user](/user-guide/authentication-policies#label-authentication-policy-set).

As another example, to alter an existing authentication policy to set the default to 30 days:

Copy code

```
ALTER AUTHENTICATION POLICY my_authentication_policy
  SET PAT_POLICY = (
    DEFAULT_EXPIRY_IN_DAYS=30
  );
```

## Configuring role restrictions for programmatic access tokens

You can configure how role restrictions are enforced when generating programmatic access tokens. You can remove the
restriction for service users, require it for person users, or block specific roles from being used as a restriction.

### Removing the role restriction for service users

By default, if you generate a programmatic access token for a service user (a user with TYPE=SERVICE, TYPE=SERVICE\_AGENT, or
TYPE=LEGACY\_SERVICE),
you must specify the role that will be used during sessions authenticated with that token. That role will be used for privilege
evaluation and object creation.

You can lift this restriction when you use the ALTER USER ADD PROGRAMMATIC ACCESS TOKEN command to generate a programmatic access
token for a service user.

To lift this restriction:

1. Create or modify an [authentication policy](/user-guide/authentication-policies) that specifies that you can generate a
   programmatic access token without a role restriction for service users.

   - To create an authentication policy, run the [CREATE AUTHENTICATION POLICY](/sql-reference/sql/create-authentication-policy) command, setting
     REQUIRE\_ROLE\_RESTRICTION\_FOR\_SERVICE\_USERS to FALSE in the PAT\_POLICY clause. For example:

     Copy code

     ```
     CREATE AUTHENTICATION POLICY my_authentication_policy
       PAT_POLICY = (
         REQUIRE_ROLE_RESTRICTION_FOR_SERVICE_USERS = FALSE
       );
     ```
   - To alter an existing authentication policy, run the [ALTER AUTHENTICATION POLICY](/sql-reference/sql/alter-authentication-policy) command, setting
     REQUIRE\_ROLE\_RESTRICTION\_FOR\_SERVICE\_USERS to FALSE in the PAT\_POLICY clause. For example:

     Copy code

     ```
     ALTER AUTHENTICATION POLICY my_authentication_policy
       SET PAT_POLICY = (
         REQUIRE_ROLE_RESTRICTION_FOR_SERVICE_USERS = FALSE
       );
     ```
2. [Apply the authentication policy to an account or user](/user-guide/authentication-policies#label-authentication-policy-set):

   - To lift the restriction for all service users in the account, apply the authentication policy to the account.
   - To lift the restriction for specific service users, apply the authentication policy to those users.

Note

- Currently, the authentication policy does not lift the restriction if you are using Snowsight to generate the
  programmatic access token, but support will be added in the future.
- Changing REQUIRE\_ROLE\_RESTRICTION\_FOR\_SERVICE\_USERS from FALSE back to TRUE invalidates any programmatic access tokens for
  service users that were generated without the role restriction.

### Requiring a role restriction for person users

By default, if you generate a programmatic access token for a person user (a user with TYPE=PERSON or TYPE=NULL),
you are not required to specify a role restriction.

You can require a role restriction for person users by setting
REQUIRE\_ROLE\_RESTRICTION\_FOR\_PERSON\_USERS to TRUE in the PAT\_POLICY clause of an authentication policy.

To require a role restriction:

1. Create or modify an [authentication policy](/user-guide/authentication-policies) that requires a role restriction for
   programmatic access tokens generated for person users.

   - To create an authentication policy, run the [CREATE AUTHENTICATION POLICY](/sql-reference/sql/create-authentication-policy) command, setting
     REQUIRE\_ROLE\_RESTRICTION\_FOR\_PERSON\_USERS to TRUE in the PAT\_POLICY clause. For example:

     Copy code

     ```
     CREATE AUTHENTICATION POLICY my_authentication_policy
       PAT_POLICY = (
         REQUIRE_ROLE_RESTRICTION_FOR_PERSON_USERS = TRUE
       );
     ```
   - To alter an existing authentication policy, run the [ALTER AUTHENTICATION POLICY](/sql-reference/sql/alter-authentication-policy) command, setting
     REQUIRE\_ROLE\_RESTRICTION\_FOR\_PERSON\_USERS to TRUE in the PAT\_POLICY clause. For example:

     Copy code

     ```
     ALTER AUTHENTICATION POLICY my_authentication_policy
       SET PAT_POLICY = (
         REQUIRE_ROLE_RESTRICTION_FOR_PERSON_USERS = TRUE
       );
     ```
2. [Apply the authentication policy to an account or user](/user-guide/authentication-policies#label-authentication-policy-set):

   - To require the restriction for all person users in the account, apply the authentication policy to the account.
   - To require the restriction for specific person users, apply the authentication policy to those users.

Note

Changing REQUIRE\_ROLE\_RESTRICTION\_FOR\_PERSON\_USERS from FALSE back to TRUE invalidates any programmatic access tokens
for person users that were generated without the role restriction.

### Blocking specific roles

You can prevent specific roles from being used as the role restriction when generating programmatic access tokens.
For example, you might want to prevent users from creating programmatic access tokens restricted to highly privileged
roles like ACCOUNTADMIN or SYSADMIN.

To block specific roles, set BLOCKED\_ROLES\_LIST in the PAT\_POLICY clause of an authentication policy:

1. Create or modify an [authentication policy](/user-guide/authentication-policies) that blocks specific roles from being
   used as a role restriction for programmatic access tokens.

   - To create an authentication policy, run the [CREATE AUTHENTICATION POLICY](/sql-reference/sql/create-authentication-policy) command, setting
     BLOCKED\_ROLES\_LIST in the PAT\_POLICY clause. For example:

     Copy code

     ```
     CREATE AUTHENTICATION POLICY secure_policy
       PAT_POLICY = (
         BLOCKED_ROLES_LIST = ('ACCOUNTADMIN', 'SYSADMIN')
       );
     ```
   - To alter an existing authentication policy, run the [ALTER AUTHENTICATION POLICY](/sql-reference/sql/alter-authentication-policy) command, setting
     BLOCKED\_ROLES\_LIST in the PAT\_POLICY clause. For example:

     Copy code

     ```
     ALTER AUTHENTICATION POLICY secure_policy
       SET PAT_POLICY = (
         BLOCKED_ROLES_LIST = ('ACCOUNTADMIN', 'SYSADMIN')
       );
     ```
2. [Apply the authentication policy to an account or user](/user-guide/authentication-policies#label-authentication-policy-set):

   - To block the roles for all users in the account, apply the authentication policy to the account.
   - To block the roles for specific users, apply the authentication policy to those users.

Note

- BLOCKED\_ROLES\_LIST is enforced at both token creation and authentication time. If a role is added to the
  blocked list after a token was already generated with that role as its restriction, the token can no longer
  be used to authenticate.
- Unrestricted tokens (tokens created without a ROLE\_RESTRICTION) are not affected by BLOCKED\_ROLES\_LIST.
- BLOCKED\_ROLES\_LIST does not implicitly enforce a role restriction. To require that users specify a role
  restriction, use REQUIRE\_ROLE\_RESTRICTION\_FOR\_SERVICE\_USERS or REQUIRE\_ROLE\_RESTRICTION\_FOR\_PERSON\_USERS.

## Privileges required for programmatic access tokens

To create and manage a programmatic access token, you need to use a role that has been granted the following privileges:

- For human users (with TYPE=PERSON), you do not need any special privileges to generate, modify, drop, or display a programmatic
  access token for yourself.
- If you’re generating, modifying, dropping, or displaying a programmatic access token for a different user or a service user
  (with TYPE=SERVICE or TYPE=SERVICE\_AGENT), you must use a role that has the OWNERSHIP or MODIFY PROGRAMMATIC AUTHENTICATION METHODS
  privilege on that user.

  For example, suppose that you want to grant users with the `my_service_owner_role` custom role the ability to generate and
  manage programmatic access tokens for the service user `my_service_user`. You can grant the MODIFY PROGRAMMATIC AUTHENTICATION
  METHODS privilege on the `my_service_user` user to the role `my_service_owner_role`:

  Copy code

  ```
  GRANT MODIFY PROGRAMMATIC AUTHENTICATION METHODS ON USER my_service_user
    TO ROLE my_service_owner_role;
  ```

## Generating a programmatic access token

You can generate a programmatic access token in Snowsight or by executing SQL commands.

SnowsightSQL

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Governance & security** » **Users & roles**.
3. Select the user that you want to generate the programmatic access token for.
4. Under **Programmatic access tokens**, select **Generate new token**.
5. In the **New programmatic access token** dialog, enter the following information:

   1. In the **Name** field, enter a name for the token.

      In the name, you can only use letters, numbers, and underscores. The name must start with a letter or underscore.
      Letters in the name are stored and resolved as uppercase characters.
   2. In the **Comment** field, enter a descriptive comment about the token.

      After you create the token, this comment is displayed under the token in the **Programmatic access tokens** section.
   3. From **Expires in**, choose the number of days after which the token should expire.
   4. If you want to restrict the scope of the operations that can be performed:

      1. Select **One specific role (recommended)**.
      2. Select the role that should be used for privilege evaluation and object creation.

      Note

      If you are generating a token for a service user (a user with TYPE=SERVICE, TYPE=SERVICE\_AGENT, or TYPE=LEGACY\_SERVICE), you must
      select a role.

      When you use this token for authentication, any objects that you create are owned by this role, and this role is used for
      privilege evaluation.

      Note

      Secondary roles are not used, even if [DEFAULT\_SECONDARY\_ROLES](/sql-reference/sql/create-user#label-create-user-default-secondary-roles) is set to
      (‘ALL’) for the user.

      If you select **Any of my roles** instead, any objects that you create are owned by your primary role, and privileges are
      evaluated against your [active roles](/user-guide/security-access-control-overview#label-access-control-role-enforcement).
   5. Select **Generate**.
6. Copy or download the generated programmatic access token so that you can use the token for authentication.

   Note

   After you close this message box, you will not be able to copy or download this token.

The new token is listed in the **Programmatic access tokens** section.

As noted earlier, to use a programmatic access token, the user associated with the token
[must be subject to a network policy](#label-pat-prerequisites-network), unless you set up an authentication policy
to change this requirement.

If a human user who is not subject to a network policy needs to use a programmatic access token for authentication, you can
temporarily bypass the requirement of having a network policy by selecting
[![More options](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png) » **Bypass requirement for network policy**.

Note

**Bypass requirement for network policy** does not allow users to bypass the network policy itself.

Execute [ALTER USER … ADD PROGRAMMATIC ACCESS TOKEN (PAT)](/sql-reference/sql/alter-user-add-programmatic-access-token), specifying a name for the token.

- If you’re generating the token for yourself, omit the `username` parameter. For example, to generate a token named
  `example_token`:

  Copy code

  ```
  ALTER USER ADD PROGRAMMATIC ACCESS TOKEN example_token;
  ```
- If you’re generating the token on behalf of a user for a person (if the USER object has TYPE=PERSON), specify the name of
  the user. For example, to generate a token named `example_token` for the user `example_user`:

  Copy code

  ```
  ALTER USER IF EXISTS example_user ADD PROGRAMMATIC ACCESS TOKEN example_token;
  ```

Tip

You can use the keyword PAT as a shorter way of specifying the keywords PROGRAMMATIC ACCESS TOKEN.

Note the following:

- If you’re generating the token on behalf of a user for a service (if the USER object has TYPE=SERVICE or TYPE=SERVICE\_AGENT), or if
  you want to restrict the scope of the operations that can be performed, set ROLE\_RESTRICTION to the role that should be used for
  privilege evaluation and object creation.

  This must be a role that has been granted to the user. You can only specify this role when generating the token.

  Note

  If you are generating a token for a service user (a user with TYPE=SERVICE, TYPE=SERVICE\_AGENT, or TYPE=LEGACY\_SERVICE), you must
  specify the ROLE\_RESTRICTION parameter, unless you have set up an authentication policy to bypass this restriction. For information,
  see [Removing the role restriction for service users](#label-pat-configure-service-role-restriction).

  When you use this token for authentication, any objects that you create are owned by this role, and this role is used for
  privilege evaluation.

  Note

  Secondary roles are not used, even if [DEFAULT\_SECONDARY\_ROLES](/sql-reference/sql/create-user#label-create-user-default-secondary-roles) is set to
  (‘ALL’) for the user.

  For example, suppose that you want to generate a token named `example_service_user_token` for the service user
  `example_service_user`. When the service user authenticates with this token, the `example_service_user_role` role
  (which has been granted to that service user) should be used to evaluate privileges and own any objects created by the user.

  To generate a token for this case, execute the following statement:

  Copy code

  ```
  ALTER USER IF EXISTS example_service_user
    ADD PROGRAMMATIC ACCESS TOKEN example_service_user_token
   ROLE_RESTRICTION = 'example_service_user_role';
  ```

  If you omit ROLE\_RESTRICTION, any objects that you create are owned by your primary role, and privileges are evaluated against
  your [active roles](/user-guide/security-access-control-overview#label-access-control-role-enforcement).
- To specify when the token should expire (overriding the [default expiration time](#label-pat-default-expiration-time)),
  set the DAYS\_TO\_EXPIRY parameter to the number of days after which the token should expire.

  You can specify a value from `1` (for 1 day) to the value of the
  [maximum expiration time](#label-pat-maximum-expiration-time).

  For example, to generate a programmatic access token that expires after 10 days:

  Copy code

  ```
  ALTER USER IF EXISTS example_user ADD PROGRAMMATIC ACCESS TOKEN example_token
    DAYS_TO_EXPIRY = 10
    COMMENT = 'An example of a token that expires in 10 days';
  ```
- As noted earlier, to use a programmatic access token, the user associated with the token
  [must be subject to a network policy](#label-pat-prerequisites-network), unless you set up an authentication policy
  to change this requirement.

  For human users (where the TYPE property of the user is PERSON) that are not subject to a network policy, you can
  temporarily bypass the requirement of having a network policy by setting MINS\_TO\_BYPASS\_NETWORK\_POLICY\_REQUIREMENT to the
  number of minutes during which you want to bypass this requirement.

  For example, suppose that you are a user who is not subject to a network policy, and you want to use a programmatic access
  token for authentication. You can bypass the requirement of having a network policy for 4 hours by setting
  MINS\_TO\_BYPASS\_NETWORK\_POLICY\_REQUIREMENT to 240.

  Note

  Setting MINS\_TO\_BYPASS\_NETWORK\_POLICY\_REQUIREMENT does not allow users to bypass the network policy itself.

ALTER USER … ADD PROGRAMMATIC ACCESS TOKEN prints the token in the `token_secret` column in the output:

```
+---------------+-----------------+
| token_name    | token_secret    |
|---------------+-----------------|
| EXAMPLE_TOKEN | ... (token) ... |
+---------------+-----------------+
```

Note

The output of this command is the only place where the token appears. Copy the token from the output for use when
authenticating to an endpoint.

After you create a programmatic access token, you cannot change the expiration date. You must revoke the token and generate a new
token with the new expiration time.

For programmatic access tokens that are restricted to a role, if the role is revoked from the user or the role is dropped, the
user can no longer use the programmatic access token for authentication.

## Using a programmatic access token

The following sections explain how to use a programmatic access token as a password and for authentication to a Snowflake endpoint:

- [Using a programmatic access token as a password](#label-pat-use-password)
- [Using a programmatic access token to authenticate to an endpoint](#label-pat-use-endpoint)

### Using a programmatic access token as a password

To authenticate with a programmatic access token as the password, you can specify the token for the value of the password in the driver settings or in the call to connect to Snowflake.

For example, if you’re using the Snowflake Connector for Python, you can specify the programmatic access token as the `password` argument when calling the `snowflake.connector.connect` method.

Copy code

```
conn = snowflake.connector.connect(
    user=USER,
    password=<programmatic_access_token>,
    account=ACCOUNT,
    warehouse=WAREHOUSE,
    database=DATABASE,
    schema=SCHEMA
)
```

In the same way, you can use programmatic access tokens in place of a password in third-party applications (such as Tableau or Power BI). Paste the programmatic access token in the field for the password.

Note

By default, using programmatic access tokens
[requires a network policy to be activated for a user or for all users in the account](#label-pat-prerequisites-network).
To use programmatic access tokens with a third-party application, you must create a network policy that allows requests from
the IP address ranges of the third-party application.

### Using a programmatic access token to authenticate to an endpoint

To authenticate with a programmatic access token, set the following HTTP headers in the request:

- `Authorization: Bearer token_secret`
- `X-Snowflake-Authorization-Token-Type: PROGRAMMATIC_ACCESS_TOKEN` (optional)

For example, if you’re using cURL to send a request to a
[Snowflake REST API](/developer-guide/snowflake-rest-api/snowflake-rest-api) endpoint:

Copy code

```
curl --location "https://myorganization-myaccount.snowflakecomputing.com/api/v2/databases" \
  --header "Authorization: Bearer <token_secret>"
```

As another example, if you’re using cURL to send a request to the
[Snowflake SQL API](/developer-guide/sql-api/index) endpoint:

Copy code

```
curl -si -X POST https://myorganization-myaccount.snowflakecomputing.com/api/v2/statements \
  --header "Content-Type: application/json" \
  --header "Accept: application/json" \
  --header "Authorization: Bearer <token_secret>" \
  --data '{"statement": "select 1"}'
```

If the request fails with a `PAT_INVALID` error, the error might have occurred for one of the following reasons:

- The user associated with the programmatic access token was not found.
- Validation failed.
- The role associated with the programmatic access token was not found.
- The user is not associated with the specified programmatic access token.

## Managing programmatic access tokens

The following sections explain how to use, modify, list, rotate, revoke, and re-enable programmatic access tokens:

- [Listing programmatic access tokens](#label-pat-list)
- [Renaming a programmatic access token](#label-pat-rename)
- [Rotating a programmatic access token](#label-pat-rotate)
- [Revoking a programmatic access token](#label-pat-revoke)
- [Re-enabling a disabled programmatic access token](#label-pat-disabled)

Note

You cannot modify, rename, rotate, or revoke a programmatic access token in a session where you used a programmatic access
token for that same user for authentication.

### Listing programmatic access tokens

You can list the programmatic access token for a user in Snowsight or by executing SQL commands.

SnowsightSQL

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Governance & security** » **Users & roles**.
3. Select the user who owns the programmatic access token.

   The programmatic access tokens for the user are listed under **Programmatic access tokens**.

Execute the [SHOW USER PROGRAMMATIC ACCESS TOKENS](/sql-reference/sql/show-user-programmatic-access-tokens) command. For example, to view information about
the programmatic access tokens associated with the user `example_user`:

Copy code

```
SHOW USER PROGRAMMATIC ACCESS TOKENS FOR USER example_user;
```

To list the programmatic access tokens for all users in the account, query the [CREDENTIALS view](/sql-reference/account-usage/credentials)
for rows where the `type` column contains `'PAT'`. For example:

Copy code

```
SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.CREDENTIALS WHERE type = 'PAT';
```

Note

After seven days, expired programmatic access tokens are deleted and no longer appear in either Snowsight or the output
of the SHOW USER PROGRAMMATIC ACCESS TOKENS command.

### Renaming a programmatic access token

Note

You cannot rename a programmatic access token in a session where you used a programmatic access token for that same user for
authentication.

You can change the name of a programmatic access token in Snowsight or by executing SQL commands.

SnowsightSQL

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Governance & security** » **Users & roles**.
3. Select the user associated with the programmatic access token.
4. Under **Programmatic access tokens**, locate the programmatic access token and select [![More options](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png) »
   **Edit**.
5. In the **Name** field, change the name of the token, and select **Save**.

Execute
[ALTER USER … MODIFY PROGRAMMATIC ACCESS TOKEN … RENAME TO](/sql-reference/sql/alter-user-modify-programmatic-access-token).
For example:

> Copy code
>
> ```
> ALTER USER IF EXISTS example_user MODIFY PROGRAMMATIC ACCESS TOKEN old_token_name
>   RENAME TO new_token_name;
> ```

### Rotating a programmatic access token

Note

You cannot rotate a programmatic access token in a session where you used a programmatic access token for that same user for
authentication.

You can rotate a programmatic access token in Snowsight or by executing SQL commands.

Rotating a token returns a new token secret that has the same name and an extended expiration time. Rotating a token also expires
the existing token secret. Use the new token for authenticating to Snowflake.

Note

When you rotate a programmatic access token:

- Snowflake does not verify that the [network policy](/user-guide/programmatic-access-tokens#label-pat-prerequisites-network) and
  [authentication policy](/user-guide/programmatic-access-tokens#label-pat-prerequisites-authentication) requirements are met.
- If the programmatic access token is restricted to a role, Snowflake does not verify that the user associated with the token
  has been granted that role.

SnowsightSQL

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Governance & security** » **Users & roles**.
3. Select the user associated with the programmatic access token.
4. Under **Programmatic access tokens**, locate the programmatic access token and select [![More options](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png) »
   **Rotate**.
5. If you want the previous token secret to expire immediately, select **Expire current secret immediately**.
6. Select **Rotate token**.
7. Copy or download the generated programmatic access token so that you can use the token for authentication.

   Note

   After you close this message box, you will not be able to copy or download this token.

Execute the [ALTER USER … ROTATE PROGRAMMATIC ACCESS TOKEN (PAT)](/sql-reference/sql/alter-user-rotate-programmatic-access-token) command.

For example, to rotate the programmatic access token `example_token` associated with the user `example_user`:

Copy code

```
ALTER USER IF EXISTS example_user ROTATE PROGRAMMATIC ACCESS TOKEN example_token;
```

If you want to specify when the old token expires, set EXPIRE\_ROTATED\_TOKEN\_AFTER\_HOURS to the number of hours before the
old token should expire. For example, to expire the old token immediately:

Copy code

```
ALTER USER IF EXISTS example_user
  ROTATE PROGRAMMATIC ACCESS TOKEN example_token
  EXPIRE_ROTATED_TOKEN_AFTER_HOURS = 0;
```

The command prints the token in the `token_secret` column in the output:

```
+---------------+-----------------+-------------------------------------+
| token_name    | token_secret    | rotated_token_name                  |
|---------------+-----------------+-------------------------------------|
| EXAMPLE_TOKEN | ... (token) ... | EXAMPLE_TOKEN_ROTATED_1744239049066 |
+---------------+-----------------+-------------------------------------+
```

Note

The output of this command is the only place where the new token appears. Copy the token from the output for use
when authenticating to an endpoint.

The output also includes the name of the older token that has been rotated:

- If you want to know when this token expires, you can use the [SHOW USER PROGRAMMATIC ACCESS TOKENS](/sql-reference/sql/show-user-programmatic-access-tokens)
  command and look for the token name. For example:

  Copy code

  ```
  SHOW USER PROGRAMMATIC ACCESS TOKENS FOR USER example_user;
  ```

  ```
  +--------------------------------------+--------------+------------------+-------------------------------+---------+---------+-------------------------------+--------------+-------------------------------------------+----------------+
  | name                                 | user_name    | role_restriction | expires_at                    | status  | comment | created_on                    | created_by   | mins_to_bypass_network_policy_requirement | rotated_to     |
  |--------------------------------------+--------------+------------------+-------------------------------+---------+---------+-------------------------------+--------------+-------------------------------------------+----------------|
  | EXAMPLE_TOKEN                        | EXAMPLE_USER | MY_CUSTOM_ROLE   | 2025-05-09 07:18:47.360 -0700 | ACTIVE  |         | 2025-04-09 07:18:47.360 -0700 | EXAMPLE_USER | NULL                                      | NULL           |
  | EXAMPLE_TOKEN_ROTATED_1744239049066  | EXAMPLE_USER | MY_CUSTOM_ROLE   | 2025-04-10 15:21:49.652 -0700 | ACTIVE  |         | 2025-04-09 15:21:49.652 -0700 | EXAMPLE_USER | NULL                                      | EXAMPLE_TOKEN  |
  +--------------------------------------+--------------+------------------+-------------------------------+---------+---------+-------------------------------+--------------+-------------------------------------------+----------------+
  ```
- If you want to revoke this token, you can use the [ALTER USER … REMOVE PROGRAMMATIC ACCESS TOKEN (PAT)](/sql-reference/sql/alter-user-remove-programmatic-access-token)
  command and specify the name of the older token. For example:

  Copy code

  ```
  ALTER USER IF EXISTS example_user
    REMOVE PROGRAMMATIC ACCESS TOKEN EXAMPLE_TOKEN_ROTATED_1744239049066;
  ```

  ```
  +-------------------------------------------------------------------------------------+
  | status                                                                              |
  |-------------------------------------------------------------------------------------|
  | Programmatic access token EXAMPLE_TOKEN_ROTATED_1744239049066 successfully removed. |
  +-------------------------------------------------------------------------------------+
  ```

### Revoking a programmatic access token

Note

You cannot revoke a programmatic access token in a session where you used a programmatic access token for that same user for
authentication.

You can revoke a programmatic access token in Snowsight or by executing SQL commands.

SnowsightSQL

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Governance & security** » **Users & roles**.
3. Select the user associated with the programmatic access token.
4. Under **Programmatic access tokens**, locate the programmatic access token and select [![More options](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png) »
   **Delete**.

Execute the [ALTER USER … REMOVE PROGRAMMATIC ACCESS TOKEN (PAT)](/sql-reference/sql/alter-user-remove-programmatic-access-token) command.

For example, to revoke the programmatic access token `example_token` associated with the user `example_user`:

Copy code

```
ALTER USER IF EXISTS example_user REMOVE PROGRAMMATIC ACCESS TOKEN example_token;
```

### Re-enabling a disabled programmatic access token

Note

You cannot modify a programmatic access token in a session where you used a programmatic access token for that same user
authentication.

When you [disable login access for a user](/user-guide/admin-user-management#label-user-management-disable-enable-user) or Snowflake locks out a user from
logging in, the programmatic access tokens for that user are automatically disabled.

Note

Programmatic access tokens are not disabled when a user is [temporarily locked out](/user-guide/admin-user-management#label-user-management-unlock)
(for example, due to five or more failed attempts to authenticate).

If you run the [SHOW USER PROGRAMMATIC ACCESS TOKENS](/sql-reference/sql/show-user-programmatic-access-tokens) command, the value in the `status` column is
`DISABLED` for tokens associated with that user.

Copy code

```
SHOW USER PROGRAMMATIC ACCESS TOKENS FOR USER example_user;
```

```
+---------------+--------------+------------------+-------------------------------+----------+---------+-------------------------------+--------------+-------------------------------------------+------------+
| name          | user_name    | role_restriction | expires_at                    | status   | comment | created_on                    | created_by   | mins_to_bypass_network_policy_requirement | rotated_to |
|---------------+--------------+------------------+-------------------------------+----------+---------+-------------------------------+--------------+-------------------------------------------+------------|
| EXAMPLE_TOKEN | EXAMPLE_USER | MY_ROLE          | 2025-04-28 12:13:46.431 -0700 | DISABLED | NULL    | 2025-04-13 12:13:46.431 -0700 | EXAMPLE_USER | NULL                                      | NULL       |
+---------------+--------------+------------------+-------------------------------+----------+---------+-------------------------------+--------------+-------------------------------------------+------------+
```

If you later enable login access for that user or Snowflake unlocks login access for that user, the programmatic access tokens
for that user remain disabled. To enable the tokens again, execute the
[ALTER USER … MODIFY PROGRAMMATIC ACCESS TOKEN (PAT)](/sql-reference/sql/alter-user-modify-programmatic-access-token) command, and set DISABLED to FALSE. For example:

Copy code

```
ALTER USER example_user MODIFY PROGRAMMATIC ACCESS TOKEN example_token SET DISABLED = FALSE;
```

## Getting information about a programmatic access token from the secret

If you need information about a programmatic access token, given the secret for that token, call the
[SYSTEM$DECODE\_PAT](/sql-reference/functions/system_decode_pat) function. You can use this function if the secret has been compromised and you
want to know the user associated with the token, the name of the token, and the state of the token.

For example:

Copy code

```
SELECT SYSTEM$DECODE_PAT('abC...Y5Z');
```

```
+------------------------------------------------------------------------+
| SYSTEM$DECODE_PAT('☺☺☺...☺☺☺')                                         |
|------------------------------------------------------------------------|
| {"STATE":"ACTIVE","PAT_NAME":"MY_EXAMPLE_TOKEN","USER_NAME":"MY_USER"} |
+------------------------------------------------------------------------+
```

## Handling a leaked programmatic access token

Snowflake is part of the
[GitHub secret scanning partner program](https://docs.github.com/en/code-security/secret-scanning/secret-scanning-partnership-program/secret-scanning-partner-program).
If the secret for a programmatic access token has been checked in to a public GitHub repository, Snowflake is notified and
disables the programmatic access token automatically. Snowflake sends an email notification about the leaked token to your account
administrator and to the user who is associated with the token.

The notification includes:

- The name of the Snowflake account
- The name of the Snowflake user
- The name, ID, and status of the programmatic access token
- The URL of the GitHub repository

Note

The account administrator and user will receive the email notification only if they have
[verified their email addresses](/user-guide/ui-snowsight-profile#label-snowsight-verify-email-address).

If you own a GitHub repository, you can allow Snowflake to disable leaked tokens by
[enabling secret scanning](https://docs.github.com/en/code-security/secret-scanning/enabling-secret-scanning-features/enabling-secret-scanning-for-your-repository).
You can also enable
[push protection](https://docs.github.com/en/code-security/secret-scanning/enabling-secret-scanning-features/enabling-push-protection-for-your-repository)
to prevent Snowflake programmatic access tokens from being committed to your GitHub repository.

If a programmatic access token is leaked, you should examine the queries executed during the sessions that used the programmatic
access token for authentication. To identify these queries, you can use the following SQL statement:

Copy code

```
WITH session_ids_with_leaked_pats AS (
  SELECT DISTINCT s.session_id
    FROM SNOWFLAKE.ACCOUNT_USAGE.SESSIONS s JOIN SNOWFLAKE.ACCOUNT_USAGE.LOGIN_HISTORY lh
      ON s.login_event_id= lh.event_id
    WHERE
      lh.first_authentication_factor_id = '<pat_id>'
)
SELECT qh.*
  FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY qh JOIN session_ids_with_leaked_pats slp
    ON qh.session_id = slp.session_id;
```

In addition, if the programmatic access token has been replicated to another account, you must disable the token in that account.
To determine which accounts might contain the replicated token, run the [SHOW REPLICATION GROUPS](/sql-reference/sql/show-replication-groups) command.

## Identifying the login sessions in which a programmatic access token was used

To determine when a programmatic access token was used for authentication, you can join the
[LOGIN\_HISTORY](/sql-reference/account-usage/login_history) and
[CREDENTIALS](/sql-reference/account-usage/credentials) views in the ACCOUNT\_USAGE schema on the column containing the
credential ID:

- The LOGIN\_HISTORY view contains the credential ID in the `first_authentication_factor_id` column, if the
  `first_authentication_factor` column contains `PROGRAMMATIC_ACCESS_TOKEN`.
- The CREDENTIALS view contains the credential ID in the `credential_id` column.

For example:

Copy code

```
SELECT
    login.event_timestamp,
    login.user_name,
    cred.name
  FROM SNOWFLAKE.ACCOUNT_USAGE.LOGIN_HISTORY login
    JOIN SNOWFLAKE.ACCOUNT_USAGE.CREDENTIALS cred
    ON login.first_authentication_factor_id = cred.credential_id
  WHERE login.first_authentication_factor = 'PROGRAMMATIC_ACCESS_TOKEN';
```

```
+-------------------------------+-----------+-----------+
| EVENT_TIMESTAMP               | USER_NAME | NAME      |
|-------------------------------+-----------+-----------|
| 2025-08-01 09:01:06.098 -0700 | USER_A    | PAT_FOR_A |
| 2025-07-08 13:33:07.687 -0700 | USER_B    | MY_PAT    |
| 2025-07-08 14:15:26.234 -0700 | USER_C    | MY_TOKEN  |
+-------------------------------+-----------+-----------+
```

To get information about the queries that were run during this login session, you can join the LOGIN\_HISTORY view with the
[SESSIONS](/sql-reference/account-usage/sessions) view on the `login_event_id` column to get the session ID, and then
use that to join the [QUERY\_HISTORY](/sql-reference/account-usage/query_history) view.

## Best practices

- If you need to store a programmatic access token, do so securely (for example, by using a password or secrets manager).
- Avoid exposing programmatic access tokens in code.
- Restrict the use of the token to a specific role when [generating the token](#label-pat-generate).
- Regularly review and rotate programmatic access tokens. Users can set the expiration time when
  [generating the token](#label-pat-generate), and administrators can
  [reduce the maximum expiration time for all tokens](#label-pat-maximum-expiration-time) to encourage the rotation of
  tokens.

## Limitations

- You can only view the secret for a programmatic access token when you create it. After you create a programmatic access token,
  you can only view information about the token and not the secret for the token.
- You cannot change some of the properties of a programmatic access token after generating the token:
  - After you generate the token, you cannot change or remove the role that the token is restricted to.
  - After you generate the token, you cannot change the expiration time of the token. You can
    [revoke a programmatic access token](#label-pat-revoke) and generate a new token with a different expiration time.

- Each user can have a maximum of 15 programmatic access tokens.
  - This number includes [tokens that have been disabled](/user-guide/programmatic-access-tokens#label-pat-disabled).
  - This number does not include tokens that have expired.

- Although there is a command that administrators can run to list all programmatic access tokens for a given user
  ([SHOW USER PROGRAMMATIC ACCESS TOKENS](/sql-reference/sql/show-user-programmatic-access-tokens)), there is no command for listing all programmatic access
  tokens in the account.

  Administrators can, however, query the [CREDENTIALS view](/sql-reference/account-usage/credentials) view to list the programmatic access
  tokens in account.
- You cannot recover a programmatic access token after you revoke it.
- You cannot modify, rename, rotate, or revoke a programmatic access token in a session where you used a programmatic access
  token for that same user for authentication.
