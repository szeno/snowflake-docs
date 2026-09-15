# Migrating to a SAML2 security integration

Important

The [SAML\_IDENTITY\_PROVIDER](/sql-reference/parameters#label-saml-identity-provider) and [SSO\_LOGIN\_PAGE](/sql-reference/parameters#label-sso-login-page) parameters used for SAML SSO configuration and management are
deprecated. Snowflake configurations should use a
[SAML2 security integration](/user-guide/admin-security-fed-auth-security-integration) instead of these parameters.

Snowflake will continue to support these deprecated parameters as long as there are implementations that use them.

If you are implementing federated authentication for the first time, refer to
[Configuring SAML 2.0 federated authentication](/user-guide/admin-security-fed-auth-security-integration).

If you have an existing SSO implementation that uses the SAML\_IDENTITY\_PROVIDER account parameter, follow the steps below to migrate your
SSO implementation to a SAML2 security integration:

1. Run the [SYSTEM$MIGRATE\_SAML\_IDP\_REGISTRATION](/sql-reference/functions/system_migrate_saml_idp_registration) function.
2. Confirm that a SAML2 security integration was created by running the following SQL statement:

   Copy code

   ```
   desc security integration <integration_name>;
   ```

If you want to configure your security integration, refer to [Configuring SAML 2.0 federated authentication](/user-guide/admin-security-fed-auth-security-integration).
