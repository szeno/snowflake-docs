Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$ISSUE\_PER\_ACCOUNT\_CERTIFICATES

Causes Snowflake to maintain public TLS certificates on behalf of the account. These certificates are used
for terminating TLS connections when you access Snowflake under account-specific hostnames that use nested
subdomains.

This function covers a superset of
[SYSTEM$ISSUE\_PER\_ACCOUNT\_APP\_SERVICE\_CERTIFICATE](/sql-reference/functions/system_issue_per_account_app_service_certificate), which covers app service
hostnames only.

Calling this function when the certificates are already being maintained has no additional effect, so
it’s safe to call more than once.

You no longer need to run this function. Snowflake maintains these certificates on behalf of the
account. For more information, see [Streamlit and Snowpark Container Services: public endpoints use per-account hostnames (Disabled by default)](/release-notes/bcr-bundles/2026_08/bcr-2451).

Caution

This system function may be removed in the future.

## Syntax

Copy code

```
SYSTEM$ISSUE_PER_ACCOUNT_CERTIFICATES()
```

## Arguments

None.

## Returns

The function returns a value of type STRING:

- `Certificates will be issued.` indicates that Snowflake has accepted the request.
- `This feature is not currently available.` indicates that the function isn’t available in your
  account. No certificates are requested.

## Examples

To call the function:

> Copy code
>
> ```
> SELECT SYSTEM$ISSUE_PER_ACCOUNT_CERTIFICATES();
> ```
