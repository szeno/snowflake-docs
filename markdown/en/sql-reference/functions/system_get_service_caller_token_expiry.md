Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$GET\_SERVICE\_CALLER\_TOKEN\_EXPIRY

Feature — Generally Available

Snowpark Container Services is available to accounts in [AWS, Microsoft Azure, and Google Cloud Platform commercial regions](/user-guide/intro-regions#label-na-general-regions), with some exceptions. For more information, see [Available regions and considerations](/developer-guide/snowpark-container-services/overview#label-snowpark-containers-overview-available-regions).

Returns the expiration timestamp of a caller’s rights login token for a
[Snowpark Container Services service](/developer-guide/snowpark-container-services/working-with-services).

See also:
:   [Configuring the login token validity](/developer-guide/snowpark-container-services/spcs-execute-sql#configuring-the-login-token-validity)

## Syntax

Copy code

```
SYSTEM$GET_SERVICE_CALLER_TOKEN_EXPIRY( '<token_string>' )
```

## Arguments

**Required:**

`token_string`
:   The caller’s rights login token string, obtained from the `Sf-Context-Current-User-Token` HTTP header
    that Snowflake passes to the service container.

## Returns

Returns a timestamp string representing the expiration time of the token (for example, `2026-07-18T14:30:00Z`).

## Usage notes

- This function can be called by the service application to determine when the caller token will expire.
- The token is obtained from the `Sf-Context-Current-User-Token` header that Snowflake provides to the container
  when a user accesses a service with caller’s rights (`executeAsCaller: true`).
- Use this function to implement token refresh logic in long-running services.

## Examples

The following statement checks the expiration time of a caller token:

Copy code

```
SELECT SYSTEM$GET_SERVICE_CALLER_TOKEN_EXPIRY('<token_value>');
```

Example output:

```
+-------------------------------------------------------+
| SYSTEM$GET_SERVICE_CALLER_TOKEN_EXPIRY                |
|-------------------------------------------------------|
| 2026-07-18T14:30:00Z                                  |
+-------------------------------------------------------+
```
