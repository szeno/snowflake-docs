# Allowing Host names

All Snowflake clients, such as SnowSQL, JDBC driver, and ODBC driver, require permanent access to cloud storage (Amazon S3, Google Cloud Storage,
or Microsoft Azure), as well as other web-based hosts, to perform various runtime operations. To ensure access, particularly in a
[secure/private network](/user-guide/admin-security-privatelink), you must allow the host names for the required hosts.

The host names that need to be allowed depend on your AWS, Google Cloud, or Microsoft Azure cloud platform and the region where your Snowflake
account is located.

Use the [SYSTEM$ALLOWLIST](/sql-reference/functions/system_allowlist) function for general accounts or
[SYSTEM$ALLOWLIST\_PRIVATELINK](/sql-reference/functions/system_allowlist_privatelink) function for accounts using private connectivity to the Snowflake service to
obtain the host names for your Snowflake account.

Add each returned host name to your organization’s firewall, proxy, or network security group outbound allow list. Ensure that port 443 is
open for standard Snowflake traffic, and that port 80 is open for OCSP certificate checks. For more information about why port 80 is
required, see [OCSP Configuration](/user-guide/ocsp). Configuring the firewall is typically done by your network or security administrator, not the Snowflake
account admin, so you might need to route this request to them.

Use [snow connection test](/developer-guide/snowflake-cli/connecting/configure-connections#test-and-diagnose-a-connection) to confirm that
the allowed endpoints are reachable. [SnowCD](/user-guide/snowcd) can also verify connectivity, but it has reached end of life.
