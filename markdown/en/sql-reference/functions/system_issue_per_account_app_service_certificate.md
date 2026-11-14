Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$ISSUE\_PER\_ACCOUNT\_APP\_SERVICE\_CERTIFICATE

Formerly caused Snowflake to maintain the public TLS certificate used for terminating TLS connections
to Snowflake-hosted app services (Streamlit in Snowflake, Snowflake Notebooks, and Snowpark Container Services) under account-specific hostnames.

You no longer need to run this function. Snowflake maintains the certificate on behalf of the
account. For more information, see [Streamlit and Snowpark Container Services: public endpoints use per-account hostnames (Disabled by default)](/release-notes/bcr-bundles/2026_08/bcr-2451).

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
