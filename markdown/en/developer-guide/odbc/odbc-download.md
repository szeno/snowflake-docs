# Downloading the ODBC Driver 4.x

**Version: 4.x.** [Switch to ODBC 3.x](/developer-guide/odbc/odbc-download-3x) · [Choose another task](/developer-guide/odbc/odbc).

Snowflake provides an installer for the ODBC driver.

Important

Installing 4.x replaces 3.x on that machine. If you are upgrading from 3.x, validate on a dedicated host, VM, or
container first. See [Migrating from ODBC Driver 3.x to 4.x](/developer-guide/odbc/odbc-migration).

To download the installer:

1. Review the [license agreement](https://sfc-repo.snowflakecomputing.com/odbc/Snowflake_ODBC_Driver_License_Agreement.pdf).
2. If you are already using the ODBC driver and need to download an updated version, check the version that you are using, and
   review the changes between your version and the updated version in the  [release notes](/release-notes/clients-drivers/odbc)

   To find the version of the driver that you are using, call the [CURRENT\_CLIENT](/sql-reference/functions/current_client) SQL function from
   an application using the driver. You can also [verify the driver version](/user-guide/snowflake-client-version-check) by
   examining queries executed by the driver in the QUERY\_HISTORY view.
3. Download the installer from the [ODBC Download](https://www.snowflake.com/en/developers/downloads/odbc/) page or from the
   [Downloading Snowflake Clients, Connectors, Drivers, and Libraries](/user-guide/snowflake-client-repository). The current version is 4.0.0.

   Because the driver is open source, each release is also published on the
   [Snowflake drivers releases](https://github.com/snowflakedb/drivers/releases) page on GitHub, tagged
   `snowflake-odbc/<version>`. GitHub publishes `snowflake-odbc-<version>.<arch>.<extension>` for each platform listed
   below.

   Each release publishes an installer for every supported platform. Filenames use the form
   `snowflake-odbc-<version>.<arch>.<extension>`:

   - Windows:
     - `snowflake-odbc-<version>.x86_64.msi`
     - `snowflake-odbc-<version>.x86_32.msi`
     - `snowflake-odbc-<version>.aarch64.msi`
   - macOS:
     - `snowflake-odbc-<version>.universal.dmg` (Intel and Apple silicon)
   - Linux:
     - `snowflake-odbc-<version>.x86_64.deb`, `snowflake-odbc-<version>.x86_64.rpm`,
       `snowflake-odbc-<version>.x86_64.tar.gz`
     - `snowflake-odbc-<version>.aarch64.deb`, `snowflake-odbc-<version>.aarch64.rpm`,
       `snowflake-odbc-<version>.aarch64.tar.gz`

   If you are comparing these names with a 3.x install, see
   [Installation changes by operating system](/developer-guide/odbc/odbc-migration#label-odbc-migration-install-compare).
4. See the following topics to install and configure the driver:

   - [Installing and configuring the ODBC Driver 4.x for Windows](/developer-guide/odbc/odbc-windows)
   - [Installing and configuring the ODBC Driver 4.x for macOS](/developer-guide/odbc/odbc-mac)
   - [Installing and configuring the ODBC Driver 4.x for Linux](/developer-guide/odbc/odbc-linux)
   - [ODBC configuration and connection parameters](/developer-guide/odbc/odbc-parameters)

## Update within 4.x

1. Check your installed version and review the [release notes](/release-notes/clients-drivers/odbc) through the target version.
2. Save your current installer, DSN settings, and driver configuration before changing the installation.
3. Download the target **4.x** package and follow the [Linux](/developer-guide/odbc/odbc-linux),
   [macOS](/developer-guide/odbc/odbc-mac), or [Windows](/developer-guide/odbc/odbc-windows) instructions.
4. Test the connection from your application and verify the installed driver version before updating other hosts.

If your installed driver is still 3.x, follow the [migration guide](/developer-guide/odbc/odbc-migration) instead.
