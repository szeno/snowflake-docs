# Jul 5, 2026: Domain verification (*General availability*)

With this release, we are pleased to announce the general availability of domain verification.

Domain verification lets an account administrator prove ownership of an email domain by publishing a
DNS TXT record. After a domain is verified, every user across every account in the organization whose
email address is in that domain is treated as having a verified email automatically, without each user
having to click a per-user verification link. This makes it much easier to deliver security and other
notifications (such as MFA enrollment prompts and password-reset messages) to large sets of users.

For more information, see the following topics:

- [Domain verification](/user-guide/admin-domain-verification)
- [SYSTEM$VERIFY\_DNS\_DOMAIN](/sql-reference/functions/system_verify_dns_domain)
- [SYSTEM$UNVERIFY\_DNS\_DOMAIN](/sql-reference/functions/system_unverify_dns_domain)
