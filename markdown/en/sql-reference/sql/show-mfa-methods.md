# SHOW MFA METHODS

Lists the [second factors of authentication](/user-guide/security-mfa-second-factor) that a user enrolled in multi-factor
authentication uses to sign in to Snowflake.

## Syntax

Copy code

```
SHOW MFA METHODS [ FOR USER <user> ]
```

## Parameters

`[ FOR USER user ]`
:   Specifies the user for whom you want to list second factors of authentication. Omitting this clause returns the authentication methods
    of the current user.

    Only users with the ACCOUNTADMIN role can use this clause.

## Usage notes

Executing this command without the FOR USER clause returns the authentication methods for the current user.

## Output

The command output provides information about authentication methods in the following columns:

| Column | Description |
| --- | --- |
| `name` | System-generated name of the authentication method. |
| `type` | Type of second factor of authentication. Possible values are:   - `PASSKEY` - User can use a passkey as their second factor of authentication. - `TOTP` - User can use a time-based one-time passcode from an authenticator app as their second factor of authentication. - `DUO` - User can use Duo as their second factor of authentication. |
| `comment` | User-specified name of the authentication method. This name appears in Snowsight when authenticating.  Empty if Duo is the second factor of authentication. |
| `last_used` | Date and time when the user last authenticated with the authentication method.  Empty if Duo is the second factor of authentication. |
| `created_on` | Date and time when the user configured the authentication method for themselves.  Empty if Duo is the second factor of authentication. |

Expand

Show lessSee more

## Examples

As an administrator, find the second factors of authentication that user `joe` configured for himself.

Copy code

```
USE ROLE ACCOUNTADMIN;

SHOW MFA METHODS FOR USER joe;
```

List the second factors of authentication of the current user.

Copy code

```
SHOW MFA METHODS;
```
