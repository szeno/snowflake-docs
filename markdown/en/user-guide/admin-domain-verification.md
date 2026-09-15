# Domain verification

*Domain verification* lets an account administrator prove, through a DNS TXT record, that the account owns an
email domain. After a domain is verified, every user *across every account in the organization* whose email
address is in that domain is treated as having a verified email automatically, without each user having to
click a verification link. One account verifies the domain once on behalf of the whole organization.

## Why domain verification matters

Snowflake delivers security and other notifications (for example, MFA enrollment prompts, password-reset
messages, and resource-monitor alerts) only to users with a verified email address. See
[Multi-factor authentication (MFA)](/user-guide/security-mfa) and [Working with resource monitors](/user-guide/resource-monitors) for examples.

Without domain verification, each user must verify their address individually from
Snowsight. In an organization with hundreds or thousands of users in the same email domain, this is
operationally expensive: new users can’t receive security and other notifications until they sign in and
complete the per-user flow, and unverified users silently miss those notifications.

Verifying the domain once shifts that work to a single DNS configuration step.

Important

Domain verification is an *organization-wide* operation. When any account in the organization verifies a
domain, every account in that organization treats users in the domain as having verified emails. Choose the
verifying account deliberately: only that account can later unverify the domain.

## How verification works

Domain verification uses a standard DNS TXT-record challenge:

1. The account administrator calls [SYSTEM$VERIFY\_DNS\_DOMAIN](/sql-reference/functions/system_verify_dns_domain) with the domain name.
   Snowflake returns a verification token of the form `snowflake-verification=<uuid>`.
2. The administrator publishes the token as a TXT record on the domain at the DNS provider.
3. Snowflake performs a *just-in-time* verification check the next time
   [SYSTEM$VERIFY\_DNS\_DOMAIN](/sql-reference/functions/system_verify_dns_domain) is called for the domain. If the published TXT record
   matches the expected token, the domain transitions to the **Verified** state.
4. While the domain is verified, all users with email addresses in that domain are treated as having verified
   email addresses for purposes of notifications, MFA, and other features that gate on email verification.

Verification is shared across the calling account’s entire organization (replication group). When a domain is
verified in one account, that verification is replicated to every account in the organization, immediately
conferring verified-email status on matching users in *every* account.

Ownership of the verification stays with the registering account, however: only the account that originally
called [SYSTEM$VERIFY\_DNS\_DOMAIN](/sql-reference/functions/system_verify_dns_domain) for a given domain can unverify or re-verify it.
Other accounts in the organization see the verification but can’t modify it.

## Domain status and the grace period

A verified domain doesn’t stay verified by itself. Snowflake periodically re-checks the TXT record in the
background to detect drift (for example, the DNS record is removed or replaced). Each domain has one of the
following statuses:

| Status | Description |
| --- | --- |
| Pending | The domain has been registered with [SYSTEM$VERIFY\_DNS\_DOMAIN](/sql-reference/functions/system_verify_dns_domain) but the TXT record hasn’t yet been observed. Users in the domain are *not* treated as having verified emails. |
| Verified | The TXT record was found on the most recent check. Users in the domain are treated as having verified emails. |
| Grace period (48 hours) | Re-verification failed. The domain is still treated as verified, but Snowflake will re-check the record. The administrator has 48 hours from this transition to fix the DNS configuration. |
| Grace period (7 days) | Re-verification continued to fail past the initial 48-hour window. Snowflake sends a warning notification to the account’s administrators. The domain remains treated as verified for an additional 7 days. |
| Unverified | The total grace period (48 hours plus 7 days) has elapsed without successful re-verification. Users in the domain are no longer treated as having verified emails, and Snowflake sends a final notification. |

Expand

Show lessSee more

The grace period exists so that transient DNS issues or short-lived misconfigurations don’t immediately revoke
the verified-email status of every user in the domain. To recover an unverified domain, fix the DNS record and
call [SYSTEM$VERIFY\_DNS\_DOMAIN](/sql-reference/functions/system_verify_dns_domain) again to trigger a fresh check.

Snowflake emails the account’s administrators at two points: when the initial 48-hour window elapses and the
domain moves into the 7-day window (a warning that includes the date the domain will become unverified), and
again when the domain becomes unverified. The first 48 hours are intentionally silent, so a brief DNS outage
doesn’t generate noise.

You don’t have to wait for an email to learn the status. At any time, call
[SYSTEM$VERIFY\_DNS\_DOMAIN](/sql-reference/functions/system_verify_dns_domain) again to check the domain’s current status. While the
domain is in a grace period, the response reports the exact date and time until which it remains verified, so
you always know how much time is left to fix the DNS record.

## Verifying a domain

Verifying a domain is a three-step process: first register the domain to obtain a token, then publish the token
in DNS, and finally let Snowflake observe it.

### Step 1: Register the domain

As an account administrator (or any user with the MODIFY privilege on the account), call
[SYSTEM$VERIFY\_DNS\_DOMAIN](/sql-reference/functions/system_verify_dns_domain) with the domain name:

Copy code

```
SELECT SYSTEM$VERIFY_DNS_DOMAIN('example.com');
```

The function returns a JSON object containing the TXT record value and the current status:

Copy code

```
{
  "txt_record": "snowflake-verification=550e8400-e29b-41d4-a716-446655440000",
  "domain": "example.com",
  "message": "Domain example.com is pending verification. Add the following DNS TXT record to verify ownership: snowflake-verification=550e8400-e29b-41d4-a716-446655440000"
}
```

Calling the function for a domain that has already been registered returns the same token; calls are idempotent.

### Step 2: Publish the TXT record

At your DNS provider, add a TXT record on the domain with the value returned in the `txt_record` field. The
record name is the apex of the domain you want to verify (for example, `example.com`, not
`_snowflake.example.com`).

DNS propagation can take a few minutes to a few hours depending on the provider and the domain’s TTL.

### Step 3: Trigger verification

Call [SYSTEM$VERIFY\_DNS\_DOMAIN](/sql-reference/functions/system_verify_dns_domain) again to perform the verification check:

Copy code

```
SELECT SYSTEM$VERIFY_DNS_DOMAIN('example.com');
```

If the TXT record is present and matches the expected token, the response message reports that the domain is
verified. From this point on, all users with email addresses in `example.com` are treated as having verified
emails.

## Removing a verified domain

To stop treating users in a domain as having verified emails, call
[SYSTEM$UNVERIFY\_DNS\_DOMAIN](/sql-reference/functions/system_unverify_dns_domain). Only the account that originally registered the domain
can unverify it.

Copy code

```
SELECT SYSTEM$UNVERIFY_DNS_DOMAIN('example.com');
```

If the domain is currently verified or in a grace period, you must pass `TRUE` as the second argument to
confirm that you intend to remove an active verification:

Copy code

```
SELECT SYSTEM$UNVERIFY_DNS_DOMAIN('example.com', TRUE);
```

After removal, users in the domain revert to whatever individual email-verification status they had previously,
and any DNS TXT record can be deleted.

## Considerations

- Snowflake compares the TXT record case-insensitively but expects the literal `snowflake-verification=`
  prefix. Don’t quote, base64-encode, or otherwise transform the value returned by
  [SYSTEM$VERIFY\_DNS\_DOMAIN](/sql-reference/functions/system_verify_dns_domain).
- Verified-email status conferred by domain verification is in addition to, not a replacement for, individual
  email verification. A user with a personally verified email keeps that status even if the domain later
  becomes unverified.
