Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$UNVERIFY\_DNS\_DOMAIN

Removes a [verified domain](/user-guide/admin-domain-verification) entry owned by the current account. After
the domain is removed, users with email addresses in that domain are no longer treated as having verified
emails through domain verification.

See also:
:   [SYSTEM$VERIFY\_DNS\_DOMAIN](/sql-reference/functions/system_verify_dns_domain)

## Syntax

Copy code

```
SYSTEM$UNVERIFY_DNS_DOMAIN( '<domain_name>' [ , <force> ] )
```

## Arguments

`'domain_name'`
:   The email domain to remove, for example `example.com`. Must be a domain previously registered by the calling
    account using [SYSTEM$VERIFY\_DNS\_DOMAIN](/sql-reference/functions/system_verify_dns_domain).

`force`
:   A Boolean. Required when the domain is currently **Verified** or in a grace period. Pass `TRUE` to confirm
    removal of an active verification. Defaults to `FALSE`.

## Returns

A status message confirming the domain has been removed.

## Access control requirements

The caller must have the MODIFY privilege on the account. Only the account that originally registered the
domain with [SYSTEM$VERIFY\_DNS\_DOMAIN](/sql-reference/functions/system_verify_dns_domain) can unverify it. Calls from other accounts
in the organization return an error.

## Usage notes

- If the domain is in the **Pending** or **Unverified** state, `force` isn’t required.
- Removing the domain doesn’t affect users whose email addresses were individually verified through
  Snowsight: those users keep their verified status. Only the domain-level verification is removed.
- After removal, you can safely delete the corresponding TXT record from your DNS configuration.

## Examples

Remove a domain that’s pending verification or already unverified:

Copy code

```
SELECT SYSTEM$UNVERIFY_DNS_DOMAIN('example.com');
```

Remove a domain that’s currently verified or in a grace period:

Copy code

```
SELECT SYSTEM$UNVERIFY_DNS_DOMAIN('example.com', TRUE);
```
