Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# USERS view

This Account Usage view can be used to query a list of all users in the account.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| USER\_ID | NUMBER | Internal/system-generated identifier for the user. |
| NAME | VARCHAR | A unique identifier for the user. |
| CREATED\_ON | TIMESTAMP\_LTZ | Date and time (in the UTC time zone) when the user’s account was created. |
| DELETED\_ON | TIMESTAMP\_LTZ | Date and time (in the UTC time zone) when the user’s account was deleted. |
| LOGIN\_NAME | VARCHAR | Name that the user enters to log into the system. |
| DISPLAY\_NAME | VARCHAR | Name displayed for the user in the Snowflake web interface. |
| FIRST\_NAME | VARCHAR | First name of the user. |
| LAST\_NAME | VARCHAR | Last name of the user. |
| EMAIL | VARCHAR | Email address for the user. |
| MUST\_CHANGE\_PASSWORD | BOOLEAN | Specifies whether the user is forced to change their password on their next login. |
| HAS\_PASSWORD | BOOLEAN | Specifies whether a password was created for the user. |
| COMMENT | VARCHAR | Comment for the user. |
| DISABLED | VARIANT | Specified whether the user account is disabled preventing the user from logging in to the Snowflake and running queries. |
| SNOWFLAKE\_LOCK | VARIANT | Specifies whether a temporary lock has been placed on the user’s account. |
| DEFAULT\_WAREHOUSE | VARCHAR | The virtual warehouse that is active by default for the user’s session upon login. |
| DEFAULT\_NAMESPACE | VARCHAR | The namespace (database only or database and schema) that is active by default for the user’s session upon login. |
| DEFAULT\_ROLE | VARCHAR | The role that is active by default for the user’s session upon login. |
| EXT\_AUTHN\_DUO | BOOLEAN | Specifies whether Duo Security is enabled for the user, which requires the user to use MFA (multi-factor authorization) for login. |
| EXT\_AUTHN\_UID | VARCHAR | The authorization ID used for Duo Security. |
| HAS\_MFA | BOOLEAN | Specifies whether the user is enrolled for multi-factor authentication. |
| BYPASS\_MFA\_UNTIL | TIMESTAMP\_LTZ | The number of minutes to temporarily bypass MFA for the user. |
| LAST\_SUCCESS\_LOGIN | TIMESTAMP\_LTZ | Date and time (in the UTC time zone) when the user last logged in to the Snowflake. |
| EXPIRES\_AT | TIMESTAMP\_LTZ | The date and time when the user’s status is set to `EXPIRED` and the user can no longer log in. This is useful for defining temporary users (e.g. users who should only have access to Snowflake for a limited time period). |
| LOCKED\_UNTIL\_TIME | TIMESTAMP\_LTZ | Specifies the number of minutes until the temporary lock on the user login is cleared. |
| HAS\_RSA\_PUBLIC\_KEY | BOOLEAN | Specifies whether RSA public key used for key pair authentication has been set up for the user. |
| PASSWORD\_LAST\_SET\_TIME | TIMESTAMP\_LTZ | The timestamp on which the last non-null password was set for the user. Default to null if no password has been set yet or if Snowflake is unable to determine the timestamp for the user before the inclusion of this column. |
| OWNER | VARCHAR | Specifies the role with the OWNERSHIP privilege on the object. |
| DEFAULT\_SECONDARY\_ROLE | VARCHAR | Specifies the default secondary role for the user (that is, ALL) or NULL if not set. |
| HAS\_PAT | BOOLEAN | If TRUE, a [programmatic access token (PAT)](/user-guide/programmatic-access-tokens) has been generated for the user. |
| HAS\_WORKLOAD\_IDENTITY | BOOLEAN | If TRUE, the user is configured to use [workload identity federation](/user-guide/workload-identity-federation) to authenticate with Snowflake. |
| TYPE | VARCHAR | Specifies the [type of user](/user-guide/admin-user-management#label-user-management-types). |
| DATABASE\_NAME | VARCHAR | When the user TYPE is SNOWFLAKE\_SERVICE, it specifies the service’s database name; otherwise, it’s NULL. |
| DATABASE\_ID | NUMBER | When the user TYPE is SNOWFLAKE\_SERVICE, it specifies the internal, Snowflake-generated identifier for the service’s database; otherwise, it’s NULL. |
| SCHEMA\_NAME | VARCHAR | When the user TYPE is SNOWFLAKE\_SERVICE, it specifies the service’s schema name; otherwise, it’s NULL. |
| SCHEMA\_ID | NUMBER | When the user TYPE is SNOWFLAKE\_SERVICE, it specifies the internal, Snowflake-generated identifier for the service’s schema; otherwise, it’s NULL. |
| IS\_FROM\_ORGANIZATION\_USER | BOOLEAN | If TRUE, the user was imported from an [organization user](/user-guide/organization-users). |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 120 minutes (2 hours).

- The `LAST_SUCCESS_LOGIN` column may have a value that differs from the `last_success_login` column in the
  SHOW USERS command output because of different methodologies used to record near-real-time and historical logins. The
  column might have a NULL value if the login history data for the user is outside the one-year retention period of
  historical data.
- Columns that are not applicable to service users (that is, users with `TYPE=SERVICE`) contain NULL values. For example,
  `HAS_PASSWORD` contains NULL values for service users.
- The `deletedOn` column might not be accurate for Snowpark Container Services [service user](/developer-guide/snowpark-container-services/spcs-execute-sql#label-spcs-additional-considerations-configuring-callers-rights). For services created before release 8.42.0, the `deletedOn` column of the service user shows as empty even if the associated service is dropped; For services created after release 8.42.0, the `deletedOn` column of the service user shows as the deletion time of the associating service.

# Internal Snowflake User for Snowsight

The first time [Snowsight](/user-guide/ui-snowsight) is accessed in an account, Snowflake creates an internal WORKSHEETS\_APP\_USER user to support the web interface. This user is used to cache query results in an internal stage in an account. For more information, see [Getting started with Snowsight](/user-guide/ui-snowsight-gs).
