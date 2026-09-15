# Allowing Host names

All Snowflake clients, such as SnowSQL, JDBC driver, and ODBC driver, require permanent access to cloud storage (Amazon S3, Google Cloud Storage,
or Microsoft Azure), as well as other web-based hosts, to perform various runtime operations. To ensure access, particularly in a
[secure/private network](/user-guide/admin-security-privatelink), you must allow the host names for the required hosts.

The host names that need to be allowed depend on your AWS, Google Cloud, or Microsoft Azure cloud platform and the region where your Snowflake
account is located.

Use the [SYSTEM$ALLOWLIST](/sql-reference/functions/system_allowlist) function for general accounts or
[SYSTEM$ALLOWLIST\_PRIVATELINK](/sql-reference/functions/system_allowlist_privatelink) function for accounts using private connectivity to the Snowflake service to
obtain the host names for your Snowflake account.

Use [SnowCD](/user-guide/snowcd) to ensure the provided endpoints are allowed.
