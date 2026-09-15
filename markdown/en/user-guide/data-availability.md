# Snowflake Time Travel & Fail-safe

Snowflake provides powerful CDP features for ensuring the maintenance and availability of your historical data (i.e. data that has been changed or deleted):

> - Querying, cloning, and restoring historical data in tables, schemas, and databases for up to 90 days through Snowflake Time Travel.
> - Disaster recovery of historical data (by Snowflake) through Snowflake Fail-safe.

These features are included standard for all accounts, i.e. no additional licensing is required; however, standard Time Travel is 1 day. Extended Time Travel (up to 90 days) requires Snowflake Enterprise Edition. In addition,
both Time Travel and Fail-safe require additional data storage, which has associated fees.

**Next Topics:**

- [Understanding & using Time Travel](/user-guide/data-time-travel)
- [Understanding and viewing Fail-safe](/user-guide/data-failsafe)
- [Storage costs for Time Travel and Fail-safe](/user-guide/data-cdp-storage-costs)
