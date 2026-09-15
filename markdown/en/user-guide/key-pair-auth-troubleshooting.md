# Key Pair Authentication: Troubleshooting

This topic helps you troubleshoot errors that occur when connecting to Snowflake with
[key pair authentication](/user-guide/key-pair-auth). It focuses on errors that contain `JWT token is invalid`.

## Find the Error

Before troubleshooting, you need to determine that the issue is resulting in a `JWT token is invalid` error.

If your Snowflake client is a driver or connector that does not have an interactive interface, use logs to inspect connection errors:

1. Enable logging for the Snowflake connector or driver. For details, see
   [Generate log files for Snowflake Drivers & Connectors](https://community.snowflake.com/s/article/How-to-generate-log-file-on-Snowflake-connectors) (Snowflake Knowledge Base article).
2. Check for errors that contain the string `JWT token is invalid`.

   For example, a client using the Snowflake JDBC driver might get the following error when trying to use key pair authentication:

   ```
   yyyy-mm-dd hh:mm:ss.nnn n.s.c.jdbc.SnowflakeSQLException FINE <init>:40 -
   Snowflake exception: JWT token is invalid. [0ce9eb56-821d-4ca9-a774-04ae89a0cf5a],
   sqlState:08001, vendorCode:390,144, queryId:
   ```

## Retrieve additional details

Each `JWT token is invalid` error includes a UUID that appears in brackets immediately after the error (for example,
`JWT token is invalid. [0ce9eb56-821d-4ca9-a774-04ae89a0cf5a]`). You should provide the UUID of the error to a Snowflake administrator so
they can obtain more information about the error.

Administrators use the [SYSTEM$GET\_LOGIN\_FAILURE\_DETAILS](/sql-reference/functions/system_get_login_failure_details) function to obtain additional details about the
error. For example, to obtain additional information about the error `JWT token is invalid. [0ce9eb56-821d-4ca9-a774-04ae89a0cf5a]`,
a user with the ACCOUNTADMIN role can execute:

Copy code

```
SELECT JSON_EXTRACT_PATH_TEXT(SYSTEM$GET_LOGIN_FAILURE_DETAILS('0ce9eb56-821d-4ca9-a774-04ae89a0cf5a'), 'errorCode');
```

The JSON\_EXTRACT\_PATH\_TEXT function parses the JSON output of the SYSTEM$GET\_LOGIN\_FAILURE\_DETAILS function to retrieve the error code and
error.

## List of Errors

The output of the SYSTEM$GET\_LOGIN\_FAILURE\_DETAILS function is one of the following error code/error combinations.

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

## Common Errors and Solutions

The most common errors associated with key pair authentication are:

- [JWT\_TOKEN\_INVALID](#label-key-pair-jwt-token-invalid)
- [JWT\_TOKEN\_INVALID\_PUBLIC\_KEY\_FINGERPRINT\_MISMATCH](#label-key-pair-public-key-fingerprint-mismatch)
- [JWT\_TOKEN\_INVALID\_USER\_IN\_ISSUER](#label-key-pair-user-in-issuer)
- [JWT\_TOKEN\_INVALID\_ISSUE\_TIME](#label-key-pair-issue-time)

Use the following descriptions and solutions to troubleshoot these errors.

### JWT\_TOKEN\_INVALID

Description:
:   There is a general problem with the JWT token.

Solution #1:
:   The token itself might be malformed. Double-check that the application accessing Snowflake is generating valid JWT
    tokens.

Solution #2:
:   Double-check that the client (driver, connector, or request URL) is using the correct
    [account identifier](/user-guide/admin-account-identifier#label-account-name) to connect to the Snowflake account. You should also check that this value matches the
    account identifier in the `iss` claim.

Solution #3:
:   Double-check that the account identifier and user name in the `sub` claim match the corresponding values in the
    `iss` claim.

Solution #4:
:   Double-check that `iss` claim specifies `SHA256` as the signing algorithm.

### JWT\_TOKEN\_INVALID\_PUBLIC\_KEY\_FINGERPRINT\_MISMATCH

Description:
:   There is a mismatch between the public key fingerprint specified in the issuer and the one stored for the user in
    Snowflake.

Solution:
:   Obtain the public key fingerprint of the JWT token, then compare it with the fingerprint associated with the user in
    Snowflake.

    One method of obtaining the fingerprint of the JWT token is to [enable DEBUG logging for your driver](https://community.snowflake.com/s/article/How-to-generate-log-file-on-Snowflake-connectors) and attempt to login. Look for the pattern `SHA256:<hash>`, where `<hash>` is the
    public key fingerprint.

    To obtain the public key fingerprint associated with the user in Snowflake, execute the [DESCRIBE USER](/sql-reference/sql/desc-user) command. The
    public key fingerprint is located in either the RSA\_PUBLIC\_KEY\_FP or the RSA\_PUBLIC\_KEY\_2\_FP property. If the user is missing a public key
    fingerprint, execute the ALTER USER command to set these properties.

### JWT\_TOKEN\_INVALID\_USER\_IN\_ISSUER

Description:
:   The user name specified in the issuer does not exist in the Snowflake account.

Solution:
:   The user name configured in the Snowflake client must match the `LOGIN_NAME` of the Snowflake user, not its
    `NAME`. Sometimes these values are different.

    Execute the [DESCRIBE USER](/sql-reference/sql/desc-user) command and verify that the value of the `LOGIN_NAME` property matches the user name
    that the Snowflake client is using to connect.

### JWT\_TOKEN\_INVALID\_ISSUE\_TIME

Description:
:   The JWT token was received by Snowflake more than 60 seconds after the issue time.

Solution #1:
:   Check the host where the driver is running to ensure it is synchronized to NTP and doesn’t have clock skew. If the server
    clock is skewed, Snowflake might determine that the current time is more than 60 seconds after the issue time of the token, when it really
    isn’t. For example, if the client machine is 30 seconds behind and it took the token 45 seconds to reach Snowflake, then Snowflake
    determines that it has been 75 seconds since the JWT token was issued, not 45 seconds.

    You can check that the clock of the client machine is accurate by comparing it to an NTP server. For example, you can use
    [NIST Internet Time Servers](https://tf.nist.gov/tf-cgi/servers.cgi) to sync the client machine. For help with checking and
    synchronizing your host’s clock to an NTP server, refer to the administrator guide for your operating system or reach out to a system
    administrator.

Solution #2:
:   Use an OS-specific monitoring tool to determine if the error occurs during times of extreme CPU/disk usage.

Solution #3:
:   Check whether there is excessive network latency that is causing the JWT token to be processed by Snowflake more than
    60 seconds after the token’s issue time.

    When using a connectivity diagnostic tool to measure network latency, set the destination to
    `account_identifier.snowflakecomputing.com`. For example, if the Snowflake client is using `myorg-account1` as the account
    identifier, set the destination to `myorg-account1.snowflakecomputing.com`.
