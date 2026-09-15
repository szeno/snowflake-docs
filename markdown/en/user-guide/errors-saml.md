# Federated authentication and SSO troubleshooting

This topic provides information to help troubleshoot a federated authentication environment, including the error codes and messages that
are generated during an unsuccessful user login attempt.

## Password-related errors

A user with an expired Snowflake password cannot log in with SSO even though they are not using the password. This behavior is
intentional and prevents someone from logging in using expired credentials.

SSO logins are also rejected if an administrator set the `MUST_CHANGE_PASSWORD` parameter to TRUE when creating the user, but the user
has not changed the password yet.

## Error codes

Errors are generated for each failed login attempt. These errors can be obtained from the [Snowflake Information Schema](/sql-reference/info-schema) or the
[ACCOUNT\_USAGE schema](/sql-reference/account-usage):

- The Snowflake Information Schema provides data from within the past 7 days and can be queried using
  the [LOGIN\_HISTORY , LOGIN\_HISTORY\_BY\_USER](/sql-reference/functions/login_history) table functions.
- The [LOGIN\_HISTORY](/sql-reference/account-usage/login_history) view in the ACCOUNT\_USAGE schema provides similar data from within the past year.

### Federated authentication error codes

The table below contains error codes and messages related to federated authentication that are not specific to SAML or OIDC. For
protocol-specific codes, see [SAML error codes](#label-saml-error-codes) and [OIDC error codes](#label-oidc-error-codes).

| Error Code | Error | Description |
| --- | --- | --- |
| 390136 | FED\_REAUTH\_PENDING | Authentication response is pending from IdP. |
| 390137 | FED\_REAUTH | Federated authentication request URL is generated. |
| 390138 | FED\_REAUTH\_TIMEOUT | Timeout waiting for authentication response from IdP. |
| 390139 | AUTHENTICATOR\_NOT\_SUPPORTED | The specified authenticator is not accepted by your Snowflake account configuration. Please contact your local system administrator to get the correct URL to use. |
| 390140 | FED\_PASSWORD\_EXPIRED | Identity Provider (IdP) password has expired. Contact your IdP team. |
| 390191 | USERNAMES\_MISMATCH | The user you were trying to authenticate as differs from the user currently logged in at the IdP. |

Expand

Show lessSee more

### SAML error codes

Troubleshooting a login failure differs depending on whether the error message has a UUID.

If you encounter an error message associated with a failed SAML SSO login attempt, and the error message does not have a UUID, then ensure
the user exists. If the user exists, then the SAML response is invalid and the number of login attempts is too high.

If you encounter an error message associated with a failed SAML SSO login attempt, and the error message has a UUID, you can ask an
administrator that has MONITOR privilege assigned to their role to get a more detailed description of the error by following the steps
below:

1. Find the UUID in the error message:

   ```
   SAML response is invalid or matching user is not found. Contact your local system administrator. [eb55b777-50a4-4db5-b231-9ee457fb3981]
   ```
2. Use the UUID as an argument to the SYSTEM$GET\_LOGIN\_FAILURE\_DETAILS function, and extract the error using the
   [JSON\_EXTRACT\_PATH\_TEXT](/sql-reference/functions/json_extract_path_text) function:

   Copy code

   ```
   SELECT JSON_EXTRACT_PATH_TEXT(SYSTEM$GET_LOGIN_FAILURE_DETAILS('eb55b777-50a4-4db5-b231-9ee457fb3981'), 'errorCode');
   ```
3. Find the error description in the table below:

| Error code | Error | Description |
| --- | --- | --- |
| 390133 | SAML\_RESPONSE\_INVALID | The SAML response was invalid for an unspecified reason, although it is most likely malformed (this is also used if there is an error on parsing). |
| 390165 | SAML\_RESPONSE\_INVALID\_SIGNATURE | The SAML response contains an invalid Signature. |
| 390166 | SAML\_RESPONSE\_INVALID\_DIGEST\_METHOD | The SAML response contains an invalid “DigestMethod” attribute or omits it entirely. |
| 390167 | SAML\_RESPONSE\_INVALID\_SIGNATURE\_METHOD | The SAML response contains an invalid “SignatureMethod” or omits it entirely. |
| 390168 | SAML\_RESPONSE\_INVALID\_DESTINATION | The “Destination” attribute in the SAML response does not match a valid destination URL on the account. |
| 390169 | SAML\_RESPONSE\_INVALID\_AUDIENCE | The SAML response does not contain exactly one audience or the audience URL does not match what we expect the audience URL to be. |
| 390170 | SAML\_RESPONSE\_INVALID\_MISSING\_INRESPONSETO | The “InResponseTo” attribute in the SAML assertion is missing. |
| 390171 | SAML\_RESPONSE\_INVALID\_RECIPIENT\_MISMATCH | The “Recipient” attribute does not match a valid destination URL. |
| 390172 | SAML\_RESPONSE\_INVALID\_NOTONORAFTER\_VALIDATION | This typically indicates that the time in which the SAML assertion is valid has expired. |
| 390173 | SAML\_RESPONSE\_INVALID\_NOTBEFORE\_VALIDATION | This typically indicates that the time in which the SAML assertion is valid has not yet come. |
| 390174 | SAML\_RESPONSE\_INVALID\_USERNAMES\_MISMATCH | The login names do not match during re-authentication. |
| 390175 | SAML\_RESPONSE\_INVALID\_SESSIONID\_MISSING | During re-authentication, we were unable to find a session corresponding to the user. |
| 390176 | SAML\_RESPONSE\_INVALID\_ACCOUNTS\_MISMATCH | During re-authentication, the names of the accounts were found to not match. |
| 390177 | SAML\_RESPONSE\_INVALID\_BAD\_CERT | The x.509 certificate contained in the SAML response is either malformed or does not match the expected certificate. |
| 390178 | SAML\_RESPONSE\_INVALID\_PROOF\_KEY\_MISMATCH | The proof keys do not match with respect to the authentication request ID. |
| 390179 | SAML\_RESPONSE\_INVALID\_INTEGRATION\_MISCONFIGURATION | The SAML IdP configuration is invalid. |
| 390180 | SAML\_RESPONSE\_INVALID\_REQUEST\_PAYLOAD | During authentication, using an invalid payload or using an invalid federated OAuth connection string. |
| 390181 | SAML\_RESPONSE\_INVALID\_MISSING\_SUBJECT\_CONFIRMATION\_BEARER | The Subject confirmation with Bearer method is missing and cannot be validated. |
| 390182 | SAML\_RESPONSE\_INVALID\_MISSING\_SUBJECT\_CONFIRMATION\_DATA | The Subject confirmation data is missing in the assertion. |
| 390183 | SAML\_RESPONSE\_INVALID\_CONDITIONS | The SAML assertion is not valid for a reason that is different than the preceding conditions in this table. |
| 390184 | SAML\_RESPONSE\_INVALID\_ISSUER | The SAML Response contained an issuer/entityID value different from the one configured in the SAML IDP Configuration. |

Expand

Show lessSee more

### OIDC error codes

The table below contains error codes related to OIDC federated authentication. For configuration guidance, see
[Configuring OpenID Connect (OIDC) federated authentication](/user-guide/admin-security-fed-auth-oidc). For troubleshooting steps, see [OIDC troubleshooting](#label-oidc-troubleshooting).

Note

A failed OIDC login shows the end user a generic error message, not a numeric code; these codes are surfaced to administrators. Codes 390250
through 390253 are top-level failure codes; codes 390254 through 390259 are internal detail codes that an administrator retrieves by passing
the login’s event UUID to [SYSTEM$GET\_LOGIN\_FAILURE\_DETAILS](/sql-reference/functions/system_get_login_failure_details). (390264 is recorded
as 390252.)

| Error code | Error | Description |
| --- | --- | --- |
| 390250 | OIDC\_INTEGRATION\_DISABLED | The OIDC integration is disabled or could not be found. |
| 390251 | OIDC\_REQUEST\_INVALID | The authorization request is missing required data or contains invalid parameters. |
| 390252 | OIDC\_RESPONSE\_INVALID | The IdP response is invalid or the user could not be resolved in Snowflake. |
| 390253 | OIDC\_TOKEN\_INVALID | General ID token validation failure. |
| 390254 | OIDC\_TOKEN\_EXPIRED | The ID token has expired (the `exp` claim is in the past) or was issued too long ago (stale `iat`). |
| 390255 | OIDC\_TOKEN\_INVALID\_ISSUER | The `iss` claim in the ID token does not match the configured `OIDC_ISSUER`. |
| 390256 | OIDC\_TOKEN\_INVALID\_AUDIENCE | The `aud` claim in the ID token does not contain the configured `OIDC_CLIENT_ID`, or, when the `azp` claim is present in a multi-audience token, `azp` does not match `OIDC_CLIENT_ID`. |
| 390257 | OIDC\_TOKEN\_INVALID\_NONCE | The `nonce` claim does not match the expected value. This may indicate a token replay attack. |
| 390258 | OIDC\_TOKEN\_INVALID\_SIGNATURE | The ID token signature could not be verified against the IdP’s JWKS keys. |
| 390259 | OIDC\_INTEGRATION\_MISCONFIGURATION | The integration is missing required configuration (for example, endpoints or credentials). |
| 390264 | OIDC\_MULTIPLE\_MATCHING\_USERS | Multiple Snowflake users with a verified email share the token’s email address, so a unique user can’t be resolved. |
| 390322 | IFF\_USER\_MISMATCH | The identifier typed at the identifier-first login prompt doesn’t match the user resolved from the IdP token. OIDC reuses this shared identifier-first login code (also used by SAML). |

Expand

Show lessSee more

## OIDC troubleshooting

The sections below describe common OIDC configuration and login issues. For error code definitions, see
[OIDC error codes](#label-oidc-error-codes).

### Common issues

**Users can’t see the OIDC login button on the Snowflake login page.**

- Verify the integration is enabled: `DESC SECURITY INTEGRATION <integration_name>;` and confirm that `ENABLED` is `TRUE`.
- Verify `OIDC_ENABLE_SSO_LOGIN_PAGE` is `TRUE`.
- For custom providers, verify `OIDC_LOGIN_PAGE_LABEL` is set (otherwise the integration name is used as the label). Managed providers display the official provider logo and default label automatically.
- If the user has an authentication policy attached, verify that the policy’s `AUTHENTICATION_METHODS` includes `OIDC` (or `ALL`), and that
  `SECURITY_INTEGRATIONS` either includes this integration or is empty.
- If `ALLOWED_USER_DOMAINS` or `ALLOWED_EMAIL_PATTERNS` is set, verify that the user’s email domain or address matches.

**A driver or client login with `authenticator=externalbrowser` doesn’t use OIDC.**

This is expected. OIDC isn’t available through the external-browser authenticator, which supports SAML 2.0 only. For driver SSO, use
`authenticator=OAUTH_AUTHORIZATION_CODE` with an OIDC integration, or configure a SAML 2.0 integration. See
[Supported sign-in surfaces](/user-guide/admin-security-fed-auth-oidc#label-oidc-sign-in-surfaces).

**Authentication fails with a generic “incorrect username or password” error after IdP login.**

Snowflake deliberately returns the same generic error (`390100`) whether the password was wrong or the OIDC user couldn’t be resolved. This
covers several user-resolution failure modes. Inspect the IdP token contents to narrow the cause:

- Verify the token claim value matches a Snowflake user attribute.
- Run `DESC SECURITY INTEGRATION <integration_name>;` to confirm the `OIDC_TOKEN_USER_MAPPING_CLAIM` and
  `OIDC_SNOWFLAKE_USER_MAPPING_ATTRIBUTE` settings.
- Verify the Snowflake user exists with the expected `LOGIN_NAME` or `EMAIL_ADDRESS`:

  Copy code

  ```
  SHOW USERS LIKE '<expected_value>';
  ```
- If the user typed a login name or email at the identifier-first prompt that doesn’t resolve to the same Snowflake user as the IdP-returned
  claim, the login fails with `390322` (`IFF_USER_MISMATCH`), a code shared with SAML.
- If `ALLOWED_USER_DOMAINS` or `ALLOWED_EMAIL_PATTERNS` is set, verify that the resolved claim value matches.

**Authentication fails for a user with email-based mapping even though the user exists.**

The user’s email might not be verified. Email-based mapping requires a Snowflake verified email, and an unverified email fails as an unresolved user
(the generic `390100` error). Verify the Snowflake user’s email, or verify their email domain. For managed
providers, the user must also have a verified email in their Google Workspace or Microsoft tenant. See
[Verified email requirement](/user-guide/admin-security-fed-auth-oidc#label-oidc-verified-email).

**Authentication fails when a token email matches multiple Snowflake users.**

When more than one Snowflake user has a verified email matching the token’s email address, Snowflake can’t resolve a unique user and the login
fails. The end user sees the generic sign-in error; check [LOGIN\_HISTORY](/sql-reference/account-usage/login_history) to identify this cause.
Ensure each email maps to a single user, or use `LOGIN_NAME` mapping. For the corresponding error code, see
[OIDC error codes](#label-oidc-error-codes).

**Detail code `OIDC_TOKEN_INVALID_ISSUER` (390255). Custom providers only.**

Ensure the `OIDC_ISSUER` value exactly matches the `iss` claim in the ID token issued by your IdP. For managed providers
(`OIDC_PROVIDER='GOOGLE'` or `OIDC_PROVIDER='MICROSOFT'`), Snowflake validates the issuer internally; contact Snowflake Support if this error persists.

**Detail code `OIDC_TOKEN_INVALID_AUDIENCE` (390256). Custom providers only.**

- Ensure the `OIDC_CLIENT_ID` matches the `aud` claim in the ID token issued by your IdP.
- If your IdP issues tokens with multiple audience values, the `azp` (authorized party) claim must match the `OIDC_CLIENT_ID`.

For managed providers (`OIDC_PROVIDER='GOOGLE'` or `OIDC_PROVIDER='MICROSOFT'`), Snowflake validates audience internally; contact Snowflake Support if this error persists.

**Authentication fails after Microsoft managed OIDC sign-in (cross-tenant users).**

Managed Microsoft OIDC sign-in uses Snowflake’s publisher-verified, multi-tenant Microsoft Entra application. If a user’s home tenant differs from Snowflake’s home tenant, the user or a home tenant administrator must consent to the requested scopes on first sign-in.

If sign-in fails after consent, verify that the ID token includes the `email` claim; user resolution requires it. The end user may see the generic sign-in error. See [Creating a managed OIDC integration (Microsoft)](/user-guide/admin-security-fed-auth-oidc#label-oidc-microsoft-managed-provider).

**Detail code `OIDC_TOKEN_INVALID_NONCE` (390257).**

This error indicates a possible token replay or session-state issue. The user should retry the login. If the error persists, verify that your IdP correctly echoes the `nonce` parameter back in the ID token.

**Detail code `OIDC_TOKEN_EXPIRED` (390254).**

The ID token has expired (the `exp` claim is in the past) or was issued too long ago (stale `iat`). The user should re-authenticate at the
IdP and try again.

**Endpoint discovery fails during integration creation.**

- Verify the issuer URL is correct and accessible from Snowflake.
- Verify the IdP publishes a `.well-known/openid-configuration` document.
- Alternatively, provide all three required endpoints (`OIDC_AUTHORIZATION_ENDPOINT`, `OIDC_TOKEN_ENDPOINT`, `OIDC_JWKS_URI`) explicitly
  to skip discovery.

**Domain or email pattern restrictions block valid users.**

- Verify the `ALLOWED_USER_DOMAINS` or `ALLOWED_EMAIL_PATTERNS` values include the user’s email domain.
- The domain/email check uses the same token claim that resolved the user. If the configured claim doesn’t contain an email address, domain filtering may unexpectedly fail.
- Email patterns use Java `Pattern.find()` semantics. If you want full-string matching, anchor your regex with `^...$`.
