Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$GET\_LOGIN\_FAILURE\_DETAILS

Returns a JSON object that represents an unsuccessful login attempt associated with External OAuth, SAML, or key pair authentication. The
JSON object contains the error associated with the failed login attempt.

## Syntax

Copy code

```
SYSTEM$GET_LOGIN_FAILURE_DETAILS('<uuid>')
```

## Arguments

`uuid`
:   A string representing a UUID. The UUID appears after the error message that is returned from a failed login event associated with External
    OAuth, SAML, or key pair authentication.

## Returns

Returns the following elements in a JSON object:

| Key | Data Type | Value Description |
| --- | --- | --- |
| clientIP | STRING | The IP address from where the failed login request originated. For example, `"10.211.55.1"`. |
| clientType | STRING | The client software reported by the client. For example, `"JDBC_DRIVER"`. This value is not verified. If the client does not report this value, then this value is `"OTHER"`. |
| clientVersion | STRING | The version of the client software reported by the client. For example, `"2.9.0"`. This value is not verified. If the client does not report this value, this value is `null`. |
| username | STRING | The username associated with the failed login event. If the system cannot find the username, or the error occurred before the system found the username, then this value is `null`. |
| errorCode | STRING | The error associated with the failed login event. For a description of the error, refer to [External OAuth errors](#label-external-oauth-errors), [SAML errors](#label-saml-errors), or [JWT token errors](#label-jwt-errors). If the error is OVERFLOW\_FAILURE\_EVENTS\_ELIDED, then the number of failed login attempts is too high. |
| timestamp | NUMBER | The date and time, in Unix timestamp format, when the failed login event occurred. |
| errorDetails | ARRAY | A JSON array of strings providing detailed context for the failed login event. For example, `["Audience mismatch: expected 'https://account.snowflakecomputing.com', got 'https://other.example.com'"]`. This value is `null` if no detailed error information is available. |

Expand

Show lessSee more

## Usage notes

Only administrators that have a MONITOR privilege assigned to their role can use this function.

## Error descriptions

This section provides descriptions for errors returned by the SYSTEM$GET\_LOGIN\_FAILURE\_DETAILS function.

### External OAuth errors

| Error | Description |
| --- | --- |
| EXTERNAL\_OAUTH\_INVALID\_SIGNATURE | Invalid signature algorithm or issue validating signature. |
| EXTERNAL\_OAUTH\_MISSING\_ISSUER | Cannot extract issuer (an `iss` claim) from the access token. |
| EXTERNAL\_OAUTH\_JWS\_INVALID\_TYPE | Invalid type of access token. |
| EXTERNAL\_OAUTH\_JWS\_INVALID\_FORMAT | Malformed access token. |
| EXTERNAL\_OAUTH\_ACCESS\_TOKEN\_ISSUER\_NOT\_FOUND | Cannot find security integration associated with the issuer. |
| EXTERNAL\_OAUTH\_ACCESS\_TOKEN\_EXPIRED | Access token expired. |
| EXTERNAL\_OAUTH\_MISSING\_AUDIENCE | Cannot extract audience (an `aud` claim) from the access token. |
| EXTERNAL\_OAUTH\_AUDIENCE\_VALIDATION\_FAILED | Audience of the access token does not match any of the audiences defined in the security integration. |
| EXTERNAL\_OAUTH\_ACCESS\_TOKEN\_ISSUER\_NOT\_ENABLED | Security integration is disabled. |
| EXTERNAL\_OAUTH\_JWS\_CANT\_RETRIEVE\_PUBLIC\_KEY | Cannot retrieve the public key from the authorization server to validate the access token. |
| EXTERNAL\_OAUTH\_USER\_CLAIM\_MISSING | Cannot extract user mapping claim from the access token. |
| EXTERNAL\_OAUTH\_ACCESS\_TOKEN\_NOT\_YET\_VALID | Token is not valid yet. A timestamp with a `iat` or `nbf` claim indicates the token is valid in the future. |

Expand

Show lessSee more

### SAML errors

| Error Code | Error | Description |
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

### JWT token errors

The following errors are associated with the JWT token used for [key pair authentication](/user-guide/key-pair-auth).

| Error Code | Error | Description |
| --- | --- | --- |
| 394307 | JWT\_TOKEN\_ACCOUNT\_MISMATCH | The Snowflake account obtained from the token is not the same as the account in the request’s URL. |
| 390144 | JWT\_TOKEN\_INVALID | There is a general issue with the JWT token. For possible solutions, see [Common Errors and Solutions](/user-guide/key-pair-auth-troubleshooting#label-key-pair-troubleshooting-common-errors). |
| 394300 | JWT\_TOKEN\_INVALID\_USER\_IN\_ISSUER | The user name specified in the issuer does not exist in the Snowflake account. For possible solutions, see [Common Errors and Solutions](/user-guide/key-pair-auth-troubleshooting#label-key-pair-troubleshooting-common-errors). |
| 394301 | JWT\_TOKEN\_MISSING\_ISSUE\_OR\_EXPIRATION\_TIME | The JWT token does not contain an issue time or an expiration time. |
| 394302 | JWT\_TOKEN\_INVALID\_ISSUE\_TIME | The JWT token was received by Snowflake more than 60 seconds after the issue time. For possible solutions, see [Common Errors and Solutions](/user-guide/key-pair-auth-troubleshooting#label-key-pair-troubleshooting-common-errors). |
| 394303 | JWT\_TOKEN\_INVALID\_EXPIRATION\_TIME | The JWT token is expired. |
| 394304 | JWT\_TOKEN\_INVALID\_PUBLIC\_KEY\_FINGERPRINT\_MISMATCH | There is a mismatch between the public key fingerprint specified in the issuer and the one stored for the user in Snowflake. For possible solutions, see [Common Errors and Solutions](/user-guide/key-pair-auth-troubleshooting#label-key-pair-troubleshooting-common-errors). |
| 394305 | JWT\_TOKEN\_INVALID\_ALGORITHM | The JWT token was not signed with the RS256 algorithm. |
| 394306 | JWT\_TOKEN\_INVALID\_SIGNATURE | Snowflake could not verify the signature provided by the JWT token. It is possible that the JWT was signed with a private key that is not paired with the provided public key. It is also possible that the JWT signature is corrupt or has been modified. |

Expand

Show lessSee more

## Examples

The following example teaches you how to use the SYSTEM$GET\_LOGIN\_FAILURE\_DETAILS function with a UUID from a failed login attempt
associated with External OAuth, SAML, or key pair authentication:

1. Find the UUID in the error message:

   ```
   Invalid  OAuth access token. [0ce9eb56-821d-4ca9-a774-04ae89a0cf5a]
   ```
2. Use the UUID as an argument to the SYSTEM$GET\_LOGIN\_FAILURE\_DETAILS function, and extract the error using the [JSON\_EXTRACT\_PATH\_TEXT](/sql-reference/functions/json_extract_path_text) function:

   Copy code

   ```
   SELECT JSON_EXTRACT_PATH_TEXT(SYSTEM$GET_LOGIN_FAILURE_DETAILS('0ce9eb56-821d-4ca9-a774-04ae89a0cf5a'), 'errorCode');
   ```
3. Find the error description in the [External OAuth errors](#label-external-oauth-errors) or [SAML errors](#label-saml-errors) tables.
