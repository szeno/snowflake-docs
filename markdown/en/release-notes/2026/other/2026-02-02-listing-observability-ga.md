# Feb 02, 2026: Support for listing and share observability (*General availability*)

Enhanced observability for listings and shares through new Information Schema views, table functions, and Account Usage views is now generally available.

## New views and functions in the INFORMATION\_SCHEMA schema

The following Information Schema views and table functions are now available:

- [INFORMATION\_SCHEMA.LISTINGS view (for providers)](#information-schema-listings-view-for-providers)
- [INFORMATION\_SCHEMA.SHARES view (for providers and consumers)](#information-schema-shares-view-for-providers-and-consumers)
- [INFORMATION\_SCHEMA.AVAILABLE\_LISTINGS table function (for consumers)](#information-schema-available-listings-table-function-for-consumers)

### INFORMATION\_SCHEMA.LISTINGS view (for providers)

The LISTINGS view displays all listings for which the current role has been granted access privileges.
This view provides real-time information with no data latency. It doesn’t capture deleted objects.

Usage example:

Copy code

```
SELECT * FROM <database_name>.INFORMATION_SCHEMA.LISTINGS;
```

For the complete list of columns, see [LISTINGS view](/sql-reference/info-schema/listings).

### INFORMATION\_SCHEMA.SHARES view (for providers and consumers)

The SHARES view lists all shares available in the system, consistent with the output of the [SHOW SHARES](/sql-reference/sql/show-shares) command. This includes:

- Outbound shares (to consumers) that have been created in your account as a provider
- Inbound shares (from providers) that are available for your account to consume

Usage example:

Copy code

```
SELECT * FROM <database_name>.INFORMATION_SCHEMA.SHARES;
```

For more information, see [SHARES view](/sql-reference/info-schema/shares).

### INFORMATION\_SCHEMA.AVAILABLE\_LISTINGS table function (for consumers)

The AVAILABLE\_LISTINGS table function in the Information Schema returns all listings that are available for the consumer to discover or
access. The function supports optional filters for imported listings, organization listings, and directly shared listings.

Usage example:

Copy code

```
SELECT * FROM TABLE(<database_name>.INFORMATION_SCHEMA.AVAILABLE_LISTINGS());

-- Filter for imported listings only
SELECT * FROM TABLE(<database_name>.INFORMATION_SCHEMA.AVAILABLE_LISTINGS(IS_IMPORTED => TRUE));
```

For more information, see [AVAILABLE\_LISTINGS](/sql-reference/functions/available_listings).

## New and updated views in the ACCOUNT\_USAGE schema

The following Account Usage views are now available for historical analysis with up to three hours of data latency:

- [ACCOUNT\_USAGE.LISTINGS view (for providers)](#account-usage-listings-view-for-providers)
- [ACCOUNT\_USAGE.SHARES view (for providers)](#account-usage-shares-view-for-providers)
- [ACCOUNT\_USAGE.GRANTS\_TO\_SHARES view (for providers)](#account-usage-grants-to-shares-view-for-providers)
- [Updates to ACCOUNT\_USAGE.ACCESS\_HISTORY view](#updates-to-account-usage-access-history-view)

### ACCOUNT\_USAGE.LISTINGS view (for providers)

This view displays a row for each listing in the provider account, including listings that have been dropped.

For more information, see [LISTINGS view](/sql-reference/account-usage/listings).

### ACCOUNT\_USAGE.SHARES view (for providers)

This view displays a row for each share in the provider account, including shares that have been dropped.

For more information, see [SHARES view](/sql-reference/account-usage/shares).

### ACCOUNT\_USAGE.GRANTS\_TO\_SHARES view (for providers)

This view can be used to query access control privileges that have been granted to a share, including historical grant and revoke operations.

For more information, see [GRANTS\_TO\_SHARES view](/sql-reference/account-usage/grants_to_shares).

### Updates to ACCOUNT\_USAGE.ACCESS\_HISTORY view

The ACCESS\_HISTORY view now captures the following DDL operations on listings and shares:

- `CREATE`, `ALTER`, and `DROP` operations on listings.
- `CREATE`, `ALTER`, and `DROP` operations on shares.
- Detailed property changes in the `OBJECT_MODIFIED_BY_DDL` JSON column.

These additions enable comprehensive auditing of listing lifecycle and share lifecycle events.

For more information, see [ACCESS\_HISTORY view](/sql-reference/account-usage/access_history) in the ACCOUNT\_USAGE schema and
[ACCESS\_HISTORY view](/sql-reference/organization-usage/access_history) in the ORGANIZATION\_USAGE schema.
