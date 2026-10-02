# Sep 22, 2026: Improved data freshness for selected ORGANIZATION\_USAGE history views

With this release, Snowflake has improved data freshness for the following
[premium views](/user-guide/organization-accounts-premium-views) in the
[ORGANIZATION\_USAGE](/sql-reference/organization-usage) schema. Typical data latency for these views is now under 15 minutes:

- [ACCESS\_HISTORY](/sql-reference/organization-usage/access_history)
- [LOGIN\_HISTORY](/sql-reference/organization-usage/login_history)
- [METERING\_HISTORY](/sql-reference/organization-usage/metering_history)
- [QUERY\_HISTORY](/sql-reference/organization-usage/query_history)

These views previously had a typical latency of up to 3 hours.

For the latency of each view, see [Organization Usage](/sql-reference/organization-usage).

For more information about premium views, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).
