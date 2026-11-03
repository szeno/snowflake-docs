# JDBC Driver

[Preview Feature](/release-notes/preview-features) — Snowflake JDBC Driver 5.x

Snowflake JDBC Driver 5.x, built on the Universal Core, is in public preview. It is published as `snowflake-jdbc-native` and `snowflake-jdbc-native-all` and does not replace JDBC Driver 4.x. This page documents 4.x, which remains the default and the version Snowflake recommends for production. Use of this preview is subject to [Snowflake’s Preview Terms](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/preview-terms-of-service/).

See [Migrating from JDBC Driver 4.x to 5.x](/developer-guide/jdbc/jdbc-migrate-5x).

Note

Version 3.21.0 introduced support for Google Cloud Storage regional endpoints.

Earlier versions of the driver do not support Google Cloud Storage regional endpoints. Please ensure that any workloads that use this driver do not require support for regional endpoints on Google Cloud. If you have questions about this, please contact Snowflake Support.

Snowflake provides a JDBC type 4 driver that supports core JDBC functionality. The JDBC driver must be installed in a
64-bit environment and requires Java LTS (Long-Term Support) versions 1.8 or higher.

The driver can be used with most client tools/applications that support JDBC for connecting to a database server. [sfsql](/user-guide/sfsql), the now-deprecated command-line client provided by
Snowflake, is an example of a JDBC-based application.

For a complete list of the connection parameters the driver accepts, including what each one does, see
[JDBC Driver connection parameter reference](/developer-guide/jdbc/jdbc-parameters).

**Next Topics:**

- [Java requirements for the JDBC Driver](/developer-guide/jdbc/java-install)
- [Downloading / integrating the JDBC Driver](/developer-guide/jdbc/jdbc-download)
- [Configuring the JDBC Driver](/developer-guide/jdbc/jdbc-configure)
- [Using the JDBC Driver](/developer-guide/jdbc/jdbc-using)
- [JDBC Driver diagnostic service](/developer-guide/jdbc/jdbc-diagnostic-service)
- [JDBC Driver connection parameter reference](/developer-guide/jdbc/jdbc-parameters)
- [JDBC Driver API support](/developer-guide/jdbc/jdbc-api)
- [Migrating from JDBC Driver 4.x to 5.x](/developer-guide/jdbc/jdbc-migrate-5x)
