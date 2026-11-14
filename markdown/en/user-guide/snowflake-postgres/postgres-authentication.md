# Configure authentication for Snowflake Postgres

Each Snowflake Postgres instance uses one authentication authority:

- **Postgres authentication** (default): A Postgres login role and its password.
- **Snowflake token authentication**: A short-lived token from Snowflake, used as the password. Password
  login still works. In Snowsight, this authority is labeled **Snowflake**.
- **External OAuth**: An access token from your identity provider.

## Configure the authentication authority

SnowsightSQL

To use the **Configure authentication** dialog, you need the `OWNERSHIP` or `MODIFY` privilege on the
instance. Without it, **Update** is unavailable.

1. In the navigation menu, select **Postgres**.
2. Select your instance.
3. Next to **Authentication**, select the edit control.
4. In the **Configure authentication** dialog, select the authentication authority:
   - **Postgres**
   - **Snowflake**
   - **External OAuth**. See [External OAuth](#label-sfpg-external-oauth-configure).
5. Select **Update**.

![Configure authentication dialog for a Snowflake Postgres instance](/static/images/snowflake-postgres/snowflake-postgres-configure-authentication-dialog.png)

Set the authentication authority with
[CREATE POSTGRES INSTANCE](/sql-reference/sql/create-postgres-instance) when you create an instance, or with
[ALTER POSTGRES INSTANCE](/sql-reference/sql/alter-postgres-instance) for an existing instance.

To return an instance to Postgres authentication:

Copy code

```
ALTER POSTGRES INSTANCE <instance_name>
  SET AUTHENTICATION_AUTHORITY = POSTGRES
      AUTHENTICATION_PROPERTIES = NULL;
```

To set Snowflake token authentication, use `POSTGRES_OR_SNOWFLAKE`:

Copy code

```
ALTER POSTGRES INSTANCE <instance_name>
  SET AUTHENTICATION_AUTHORITY = POSTGRES_OR_SNOWFLAKE
      AUTHENTICATION_PROPERTIES = NULL;
```

Set `AUTHENTICATION_PROPERTIES` to `NULL` when you leave External OAuth. That removes the stored
issuer and accepted tokens. On any other authority, `NULL` changes nothing.

After you set Snowflake token authentication, map Postgres users to Snowflake users and generate
tokens. See [Map a Postgres user to a Snowflake user](#label-sfpg-token-auth-user-mappings).

For External OAuth, set `AUTHENTICATION_AUTHORITY` to `EXTERNAL_OAUTH` and provide
`AUTHENTICATION_PROPERTIES`, then set `oauth_identifier` on each role that will sign in. See
[External OAuth](#label-sfpg-external-oauth-configure).

## Snowflake token authentication

A Snowflake token authenticates to the Postgres instance.
[Snowflake OAuth](/user-guide/oauth-snowflake-overview) and
[programmatic access tokens](/user-guide/programmatic-access-tokens) authenticate to Snowflake.

Important

Changing the authentication authority away from Snowflake token authentication stops new tokens from
being created. Tokens already issued can still open connections until they expire, up to 15 minutes
after they were issued. Open connections stay open.

Mapped users can’t use Postgres authentication until their mappings are removed.

### Token types

[GENERATE\_POSTGRES\_ACCESS\_TOKEN\_FOR\_USER](/sql-reference/functions/generate_postgres_access_token_for_user) checks the following in order
and returns the first token that applies:

| Token | Who gets it | Signs in as |
| --- | --- | --- |
| Owner token (*Preview*) | A role with the OWNERSHIP privilege on the instance, or the MANAGE GRANTS privilege on the account | Any Postgres user that can sign in with a password, or any Postgres user that has an access role |
| Access role token (*Preview*) | A role that holds the [access role](#label-sfpg-token-auth-access-roles) for the requested Postgres user, directly or through the role hierarchy | The Postgres user whose access role is enabled |
| User token | Any other role with the USAGE privilege on the instance | The Postgres user mapped to that Snowflake user |

Expand

Show lessSee more

Every token expires 15 minutes after it is issued.

### Map a Postgres user to a Snowflake user

Sign in to the Postgres instance as the `snowflake_admin` user and run:

Copy code

```
ALTER USER <postgres_user> SET snowflake_user = '<snowflake_user>';
```

The identifiers are case-insensitive unless you place them in double quotes. For example, to map a
Postgres user named Casey to a Snowflake user of the same name:

Copy code

```
ALTER USER "Casey" SET snowflake_user = '"Casey"';
```

To remove a mapping and restore password login:

Copy code

```
ALTER USER <postgres_user> RESET snowflake_user;
```

A mapped Postgres user can sign in only with a token and can’t change their Postgres password.

### Grant access with access roles

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

An access role lets Snowflake roles sign in as a Postgres user. Use it when a team, a service, or an
app needs access, instead of mapping one Snowflake user at a time. The access role controls who can
connect as that user. Privileges on databases and other objects inside Postgres are managed
separately by [Postgres roles](/user-guide/snowflake-postgres/postgres-roles).

1. Sign in to the Postgres instance as `snowflake_admin` with its password, and enable the Postgres
   user’s access role:

   Copy code

   ```
   ALTER USER app_user SET SNOWFLAKE_ACCESS_ROLE = true;
   ```

   Anyone who can sign in as `snowflake_admin` with a password can create the access role. Generating
   an owner token that signs in as `snowflake_admin` requires the OWNERSHIP privilege on the
   instance, or the MANAGE GRANTS privilege on the account.

   Snowflake creates an access role with the Postgres user’s name. The name can’t be set separately.
   To list the access roles on an instance:

   Copy code

   ```
   SHOW ACCESS ROLES IN POSTGRES INSTANCE my_instance;
   ```
2. Grant the access role to a Snowflake role, application role, or user. Name it
   `<instance>!<access_role>`. A role with the OWNERSHIP privilege on the instance, a role with the
   MANAGE GRANTS privilege on the account, or the SYSADMIN role can grant it.

   Copy code

   ```
   GRANT POSTGRES ACCESS ROLE my_instance!app_user TO ROLE analyst;
   ```

   To grant it to an application role or a user:

   Copy code

   ```
   GRANT POSTGRES ACCESS ROLE my_instance!app_user TO APPLICATION ROLE my_app.app_role;
   GRANT POSTGRES ACCESS ROLE my_instance!app_user TO USER casey;
   ```
3. A user whose active role hierarchy includes `analyst` generates a token for `app_user`:

   Copy code

   ```
   SELECT GENERATE_POSTGRES_ACCESS_TOKEN_FOR_USER('my_instance', 'app_user');
   ```

To remove access, revoke the access role:

Copy code

```
REVOKE POSTGRES ACCESS ROLE my_instance!app_user FROM ROLE analyst;
```

To disable access-role authentication for the Postgres user, reset the setting in Postgres. Setting
it to `false` has the same effect. Either action also drops the access role:

Copy code

```
ALTER USER app_user RESET SNOWFLAKE_ACCESS_ROLE;
```

A Postgres user can have a Snowflake user mapping or an access role, but not both. Remove the
mapping before you enable the access role, and disable the access role before you add a mapping. If
a mapping exists, setting `SNOWFLAKE_ACCESS_ROLE` fails with
`role "<postgres_user>" already uses snowflake authentication`. If an access role exists, setting
`snowflake_user` fails with
`role "<postgres_user>" already uses role-based snowflake authentication`.

The instance owner doesn’t need an access role to generate an owner token. An owner token can sign
in as any Postgres user that uses a password, or any Postgres user that has an access role.

If you turn Snowflake token authentication back on, Snowflake picks up access roles that you created
in Postgres while token authentication was off. That can take 1 to 2 hours.

#### When revoked access takes effect

Revoking an access role stops new tokens immediately. It doesn’t invalidate a token that was already
issued:

- A token issued before the revoke can open new connections until it expires, up to 15 minutes later.
- An open connection stays open. Access is checked only when a connection opens.

A connection succeeds only if both Postgres and Snowflake allow it. When you reset
`SNOWFLAKE_ACCESS_ROLE` in Postgres, new sign-ins as that Postgres user stop, even before Snowflake
drops the access role. Tokens already issued still work until they expire, up to 15 minutes after
they were issued.

### Generate a token

Who can generate a token, and which Postgres user it signs in as, depends on the
[token type](#label-sfpg-token-auth-token-types).

SnowsightSQL

1. In the navigation menu, select **Postgres**.
2. Select your instance.
3. In the **Manage** menu, select **Regenerate token**.
4. Enter a Postgres user that this token can sign in as, then select **Acknowledge & continue**.
5. Copy the token or Postgres URI. The token is valid for 15 minutes.

Use the [GENERATE\_POSTGRES\_ACCESS\_TOKEN\_FOR\_USER](/sql-reference/functions/generate_postgres_access_token_for_user) function.

### SNOWFLAKE\_AUTH.IDENTITY\_MAPPING

Query this view from a session on the Postgres instance. It lists mappings between Postgres users
and Snowflake users.

#### Columns

| Column name | Data type | Description |
| --- | --- | --- |
| postgres\_role | name | The name of the mapped Postgres user |
| snowflake\_identity | text | The Snowflake user identity in USER:# form, where # is the mapped Snowflake user’s user\_id in [USERS view](/sql-reference/account-usage/users) |

Expand

Show lessSee more

## External OAuth

External OAuth uses access tokens from your identity provider. It is a different feature from
[Snowflake OAuth](/user-guide/oauth-snowflake-overview).

In the **Configure authentication** dialog, **Add accepted token** adds a group, prefilled with
`sub`, `scp`, and `snowflake:postgres:<id>`.

Set `AUTHENTICATION_AUTHORITY` to `EXTERNAL_OAUTH` and set `AUTHENTICATION_PROPERTIES`. To accept
more than one token, add an entry for each:

Copy code

```
ALTER POSTGRES INSTANCE <instance_name>
  SET AUTHENTICATION_AUTHORITY = EXTERNAL_OAUTH
      AUTHENTICATION_PROPERTIES = (
        ISSUER = '<idp_issuer_url>',
        AUDIENCE = '<audience>',
        ACCEPTED_TOKENS = (
          (
            MAPPING_CLAIM = 'email',
            SCOPES = 'postgres.login.scope'
          ),
          (
            MAPPING_CLAIM = 'sub',
            SCOPES_CLAIM = 'roles',
            SCOPES = ('app.read', 'app.write')
          )
        )
      );
```

`DESCRIBE POSTGRES INSTANCE` prints `SCOPES` as a parenthesized list.

### Map a role for External OAuth

Sign in to the Postgres instance as the `snowflake_admin` user and set `oauth_identifier` to the
value of that role’s mapping claim:

Copy code

```
ALTER ROLE <role> SET oauth_identifier = '<value>';
```

When `MAPPING_CLAIM` is `email`, use the role’s email address. That role can then sign in only with
an access token.

### Statement rules

- `ISSUER` is required. It must be an `https` URL with no query or fragment. The statement fails if
  the issuer is invalid.
- If you omit `AUDIENCE`, Snowflake stores `snowflake:postgres:<instance_id>`. The identity provider
  must put that value in the `aud` claim.
- If you omit `SCOPES_CLAIM`, Postgres reads scopes from the `scope` claim, or from `scp` when the
  token has no `scope` claim.
- A claim name matches one top-level claim. `email.verified` is one claim name.
- Each accepted token requires `MAPPING_CLAIM` and `SCOPES`.
- A token is accepted when it matches one entry. Every scope listed in that entry must be present.
  To accept a token that has only `app.read`, and a token that has only `app.write`, add an entry
  for each scope.
- `ACCEPTED_TOKENS` is required. Include at least one entry, and no more than 10.
- Snowflake rejects two entries that use the same mapping claim and scopes claim when one set of
  scopes contains the other.
- `AUTHENTICATION_PROPERTIES` is required for External OAuth. A properties object is an error when
  the authority is `POSTGRES` or `POSTGRES_OR_SNOWFLAKE`. `NULL` clears the stored OAuth settings.
- Each statement replaces `AUTHENTICATION_PROPERTIES` completely. Include every accepted token you
  want to keep.

### Switch an existing instance to External OAuth

When you switch from Snowflake token authentication, Snowflake stops generating tokens for the instance. A token that was already generated works until
it expires, 15 minutes after it was generated. Before you switch, move any client that connects with
a Snowflake token to External OAuth or a Postgres password.

`snowflake_admin` and roles without `oauth_identifier` can still sign in with a password. Switching
revokes the `application` role’s password. You can’t regenerate it while the instance uses External
OAuth.

If you switch back to `POSTGRES_OR_SNOWFLAKE`, Snowflake generates tokens again, and you can
regenerate the `application` role’s credentials.

### Read replicas and forks

A new read replica or fork copies the source instance’s authentication settings. Passwords work as
soon as the replica or fork is ready. External OAuth sign-in starts working within about an hour.
To start it sooner, run `ALTER POSTGRES INSTANCE … SET AUTHENTICATION_PROPERTIES` on the new
instance with the source instance’s values.

A later authentication change on the leader stays on the leader. Repeat it on each read replica.

## Next steps

- [Snowflake Postgres External OAuth with Microsoft Entra ID](https://www.snowflake.com/en/developers/guides/snowflake-postgres-external-oauth-entra-id/)
