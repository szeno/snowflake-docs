Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$ISSUE\_PER\_ACCOUNT\_APP\_SERVICE\_CERTIFICATE

Causes Snowflake to maintain a public TLS certificate on behalf of the account. This certificate is used
for terminating TLS connections to Snowflake-hosted app services (Streamlit in Snowflake, Snowflake Notebooks, and Snowpark Container Services) when
accessing them under account-specific hostnames.

The initial certificate issuance is asynchronous. Wait at least 30 minutes after calling this function before
changing account parameters that depend on the certificate being in place. If you change those parameters
before the certificate is ready, you may encounter errors when accessing Snowflake-hosted app services
under account-specific hostnames.

You currently must run this function in order to change
[ENABLE\_PER\_ACCOUNT\_APP\_SERVICE\_URL](/sql-reference/parameters#label-enable-per-account-app-service-url) or
[ENABLE\_PER\_ACCOUNT\_APP\_SERVICE\_PRIVATELINK\_URL](/sql-reference/parameters#label-enable-per-account-app-service-privatelink-url)
to true.

Caution

This system function may be removed in the future.

## Syntax

Copy code

```
SYSTEM$ISSUE_PER_ACCOUNT_APP_SERVICE_CERTIFICATE()
```

## Arguments

None.

## Returns

The function returns a value of type STRING.

## Examples

To call the function:

> Copy code
>
> ```
> CALL SYSTEM$ISSUE_PER_ACCOUNT_APP_SERVICE_CERTIFICATE();
> ```
