# JDBC Driver

JDBC 0.0.6 Private Preview - Universal Core

A version of the Snowflake JDBC Driver built on the Universal Core is available in private preview.
Preview participants can download the `snowflake-jdbc-native-all` JAR from
[Maven Central](https://repo1.maven.org/maven2/net/snowflake/snowflake-jdbc-native-all/).

Use this driver only if you are participating in the private preview, subject to
[Snowflake’s Preview Terms](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/preview-terms-of-service/).
It may be unstable and is not ready for use with production data. Use it only for internal evaluation;
do not use it to process personal data or other data subject to compliance or legal requirements.

The documentation below applies to the existing JDBC driver. For the Universal Core version, follow the
[preview installation instructions](https://github.com/snowflakedb/drivers/blob/main/jdbc/README.md#consuming-the-driver).

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
