Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$VERIFY\_DNS\_DOMAIN

Registers an email domain for [domain verification](/user-guide/admin-domain-verification) and returns the
DNS TXT record value the account must publish to prove ownership. Subsequent calls for the same domain check
the published TXT record and update the domain’s verification status.

See also:
:   [SYSTEM$UNVERIFY\_DNS\_DOMAIN](/sql-reference/functions/system_unverify_dns_domain)

## Syntax

Copy code

```
SYSTEM$VERIFY_DNS_DOMAIN( '<domain_name>' )
```

## Arguments

`'domain_name'`
:   The email domain to verify, for example `example.com`. The value is normalized to lowercase and must be a
    syntactically valid domain name.

## Returns

A JSON object with the following fields:

`txt_record`
:   The full TXT record value to publish at the domain’s DNS provider, for example
    `snowflake-verification=550e8400-e29b-41d4-a716-446655440000`.

`domain`
:   The normalized domain name.

`message`
:   A human-readable status message describing the current verification state.

## Access control requirements

The caller must have the MODIFY privilege on the account.

## Usage notes

- Calls are idempotent. Calling the function for a domain that has already been registered returns the same
  verification token rather than rotating it.
- The function performs a just-in-time verification check whenever the domain is in the **Pending**,
  **Grace period**, or **Unverified** state. Call the function after publishing the TXT record to transition
  the domain to **Verified**.
- Verification is scoped to the calling account’s organization. Users in the domain are treated as having
  verified emails throughout that organization.
- For background on the verification flow, the grace-period model, and the relationship to individual email
  verification, see [Domain verification](/user-guide/admin-domain-verification).

## Examples

Register a domain and obtain its TXT record:

Copy code

```
SELECT SYSTEM$VERIFY_DNS_DOMAIN('example.com');
```

Sample response (formatted for readability):

Copy code

```
{
  "txt_record": "snowflake-verification=550e8400-e29b-41d4-a716-446655440000",
  "domain": "example.com",
  "message": "Domain example.com is pending verification. Add the following DNS TXT record to verify ownership: snowflake-verification=550e8400-e29b-41d4-a716-446655440000"
}
```

After publishing the TXT record at your DNS provider, call the function again to trigger verification:

Copy code

```
SELECT SYSTEM$VERIFY_DNS_DOMAIN('example.com');
```

Sample response after a successful verification:

Copy code

```
{
  "txt_record": "snowflake-verification=550e8400-e29b-41d4-a716-446655440000",
  "domain": "example.com",
  "message": "Domain example.com is verified."
}
```
