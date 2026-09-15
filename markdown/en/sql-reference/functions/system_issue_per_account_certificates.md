Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$ISSUE\_PER\_ACCOUNT\_CERTIFICATES

Causes Snowflake to maintain public TLS certificates on behalf of the account. These certificates are used
for terminating TLS connections when you access Snowflake under account-specific hostnames that use nested
subdomains.

This function covers a superset of
[SYSTEM$ISSUE\_PER\_ACCOUNT\_APP\_SERVICE\_CERTIFICATE](/sql-reference/functions/system_issue_per_account_app_service_certificate), which covers app service
hostnames only.

Certificate issuance is asynchronous. Wait at least 30 minutes after calling this function before
changing account parameters that depend on the certificates being in place. If you change those parameters
before the certificates are ready, you might encounter errors when accessing Snowflake under
account-specific hostnames.

Calling this function when the certificates are already being maintained has no additional effect, so
it’s safe to call more than once.

Data Connectivity Proxy (DCP) setup uses this function. See the
[note in the DCP setup topic](/user-guide/data-connectivity-proxy-setup#label-dcp-setup-issue-certificates).

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
