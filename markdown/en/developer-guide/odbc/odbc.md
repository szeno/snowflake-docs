# ODBC Driver

Snowflake provides a driver for connecting to Snowflake using ODBC-based client applications.

## Choose your task

- **Install for the first time:** Start with [ODBC 4.x downloads and installation](/developer-guide/odbc/odbc-download).
  If your application requires 3.x, use the [3.x guide](/developer-guide/odbc/odbc-download-3x).
- **Update within 3.x:** Use [3.x downloads and update steps](/developer-guide/odbc/odbc-download-3x#label-odbc-update-3x).
- **Migrate from 3.x to 4.x:** Start with the [migration guide](/developer-guide/odbc/odbc-migration) before installing.
- **Update within 4.x:** Use [4.x downloads and update steps](/developer-guide/odbc/odbc-download#label-odbc-update-4x).

Choose based on the driver installed on your machine, not the age of your Snowflake account. If a tool or vendor
manages the driver, follow its supported upgrade process instead of replacing the driver yourself.

### ODBC 4.x (Universal Core)

- [Overview of ODBC 4.x](/developer-guide/odbc/odbc-universal-core)
- [Download packages and choose an installer](/developer-guide/odbc/odbc-download)
- [Install and configure (Linux)](/developer-guide/odbc/odbc-linux)
- [Install and configure (macOS)](/developer-guide/odbc/odbc-mac)
- [Install and configure (Windows)](/developer-guide/odbc/odbc-windows)

### ODBC 3.x

- [Download packages and choose an installer](/developer-guide/odbc/odbc-download-3x)
- [Install and configure (Linux)](/developer-guide/odbc/odbc-linux-3x)
- [Install and configure (macOS)](/developer-guide/odbc/odbc-mac-3x)
- [Install and configure (Windows)](/developer-guide/odbc/odbc-windows-3x)

## About the driver

Starting with version 4.0.0, the driver is built on the [Universal Core](/developer-guide/universal-core/universal-core): a thin C
layer over a shared Rust library used by drivers built on the Universal Core. The public ODBC interface is unchanged, and the
Rust layer is not visible to application code. If you are upgrading from version 3.x, see [Migrating from ODBC Driver 3.x to 4.x](/developer-guide/odbc/odbc-migration).

Important

The ODBC driver has different prerequisites depending on the platform where it is installed. For details, see the individual installation and configuration instructions for each platform.

In addition, different versions of the ODBC driver support the [GET](/sql-reference/sql/get) and [PUT](/sql-reference/sql/put) commands, depending on the cloud service that hosts your Snowflake account:

- Amazon Web Services: Version 2.17.5 (and higher)
- Google Cloud Platform: Version 2.21.5 (and higher)
- Microsoft Azure: Version 2.20.2 (and higher)

**Next Topics:**

- [Downloading the ODBC Driver 4.x](/developer-guide/odbc/odbc-download)
- [Installing and configuring the ODBC Driver 4.x for Windows](/developer-guide/odbc/odbc-windows)
- [Installing and configuring the ODBC Driver 4.x for macOS](/developer-guide/odbc/odbc-mac)
- [Installing and configuring the ODBC Driver 4.x for Linux](/developer-guide/odbc/odbc-linux)
- [ODBC configuration and connection parameters](/developer-guide/odbc/odbc-parameters)
- [ODBC Driver API support](/developer-guide/odbc/odbc-api)
- [Using the ODBC Driver](/developer-guide/odbc/odbc-using)
- [ODBC Driver diagnostic service](/developer-guide/odbc/odbc-diagnostic-service)
- [Migrating from ODBC Driver 3.x to 4.x](/developer-guide/odbc/odbc-migration)
