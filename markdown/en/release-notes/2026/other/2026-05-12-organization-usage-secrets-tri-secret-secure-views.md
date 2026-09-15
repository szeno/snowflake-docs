# May 12, 2026: New ORGANIZATION\_USAGE premium views

The ORGANIZATION\_USAGE schema now includes two new [premium views](/user-guide/organization-accounts-premium-views)
that are available in the [organization account](/user-guide/organization-accounts). These views provide
visibility into secrets and Tri-Secret Secure customer-managed key history across all accounts in your organization.

The new views are:

- [SECRETS](/sql-reference/organization-usage/secrets): Returns one row for each secret in an account.
- [TRI\_SECRET\_SECURE\_HISTORY](/sql-reference/organization-usage/tri-secret-secure-history): Returns Tri-Secret Secure customer-managed key history for Business Critical and VPS accounts over the last 365 days.

For more information about accessing premium views in the organization account, see [Access schema in the organization account](/sql-reference/organization-usage#label-org-usage-access-org-account).
