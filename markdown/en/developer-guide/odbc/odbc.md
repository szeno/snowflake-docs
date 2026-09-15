# ODBC Driver

[Preview Feature](/release-notes/preview-features) — Snowflake ODBC Driver 4.x

Snowflake ODBC Driver 4.x, built on the Universal Core, is in public preview. Installing it replaces the 3.x driver on that machine, so validate it on a separate host. This page documents 3.x, which remains the default and the version Snowflake recommends for production.

See [Snowflake ODBC Driver built on the Universal Core](/developer-guide/odbc/odbc-universal-core).

Snowflake provides a driver for connecting to Snowflake using ODBC-based client applications.

Important

The ODBC driver has different prerequisites depending on the platform where it is installed. For details, see the individual installation and configuration instructions for each platform.

In addition, different versions of the ODBC driver support the [GET](/sql-reference/sql/get) and [PUT](/sql-reference/sql/put) commands, depending on the cloud service that hosts your Snowflake account:

- Amazon Web Services: Version 2.17.5 (and higher)
- Google Cloud Platform: Version 2.21.5 (and higher)
- Microsoft Azure: Version 2.20.2 (and higher)

**Next Topics:**

- [Downloading the ODBC Driver](/developer-guide/odbc/odbc-download)
- [Installing and configuring the ODBC Driver for Windows](/developer-guide/odbc/odbc-windows)
- [Installing and configuring the ODBC Driver for macOS](/developer-guide/odbc/odbc-mac)
- [Installing and configuring the ODBC Driver for Linux](/developer-guide/odbc/odbc-linux)
- [ODBC configuration and connection parameters](/developer-guide/odbc/odbc-parameters)
- [ODBC Driver API support](/developer-guide/odbc/odbc-api)
- [Using the ODBC Driver](/developer-guide/odbc/odbc-using)
- [ODBC Driver diagnostic service](/developer-guide/odbc/odbc-diagnostic-service)
- [Snowflake ODBC Driver built on the Universal Core](/developer-guide/odbc/odbc-universal-core)
