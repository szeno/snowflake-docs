# Downloading the ODBC Driver

[Preview Feature](/release-notes/preview-features) — Snowflake ODBC Driver 4.x

The downloads on this page are for the 3.x driver.

Snowflake ODBC Driver 4.x, built on the Universal Core, is in public preview and is downloaded separately. See [Installing the preview driver](/developer-guide/odbc/odbc-universal-core#label-odbc-universal-core-install).

Snowflake provides an installer for the ODBC driver.

Note

If you plan to use `yum` to download and install the ODBC driver for Linux, skip ahead to
[Using yum to download and install the driver](/developer-guide/odbc/odbc-linux#label-odbc-linux-install-yum).

To download the installer:

1. Review the [license agreement](https://sfc-repo.snowflakecomputing.com/odbc/Snowflake_ODBC_Driver_License_Agreement.pdf).
2. If you are already using the ODBC driver and need to download an updated version, check the version that you are using, and
   review the changes between your version and the updated version in the  [release notes](/release-notes/clients-drivers/odbc)

   To find the version of the driver that you are using, call the [CURRENT\_CLIENT](/sql-reference/functions/current_client) SQL function from
   an application using the driver. You can also [verify the driver version](/user-guide/snowflake-client-version-check) by
   examining queries executed by the driver in the QUERY\_HISTORY view.
3. Go to the [ODBC Download](https://developers.snowflake.com/odbc/) page, and download the installer.

   Note

   The Linux installation package is provided in three variations:

   - TGZ (TAR file compressed using .GZIP)
   - RPM
   - DEB

   The TGZ package requires some manual configuration tasks. The RPM and DEB packages include an automated installer and support
   validation using the public GPG key provided by Snowflake.
4. See the following topics to install and configure the driver:

   - [Installing and configuring the ODBC Driver for Windows](/developer-guide/odbc/odbc-windows)
   - [Installing and configuring the ODBC Driver for macOS](/developer-guide/odbc/odbc-mac)
   - [Installing and configuring the ODBC Driver for Linux](/developer-guide/odbc/odbc-linux)
   - [ODBC configuration and connection parameters](/developer-guide/odbc/odbc-parameters)
