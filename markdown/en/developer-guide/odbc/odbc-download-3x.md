# Downloading the ODBC Driver 3.x

**Version: 3.x.** [Switch to ODBC 4.x](/developer-guide/odbc/odbc-download) · [Choose another task](/developer-guide/odbc/odbc).

Snowflake provides an installer for the ODBC driver.

The [ODBC release notes](/release-notes/clients-drivers/odbc) track 3.x releases alongside 4.x releases.
The current 3.x version is 3.21.0. Choose a 3.x version from the download page or client repository
to stay on 3.x; the latest overall ODBC version refers to 4.x.

Note

If you plan to use `yum` to download and install the ODBC driver for Linux, skip ahead to
[Installing 3.x with yum](/developer-guide/odbc/odbc-linux-3x#label-odbc-linux-install-yum-3x).

To download the installer:

1. Review the [license agreement](https://sfc-repo.snowflakecomputing.com/odbc/Snowflake_ODBC_Driver_License_Agreement.pdf).
2. If you are already using the ODBC driver and need to download an updated version, check the version that you are using, and
   review the changes between your version and the updated version in the  [release notes](/release-notes/clients-drivers/odbc)

   To find the version of the driver that you are using, call the [CURRENT\_CLIENT](/sql-reference/functions/current_client) SQL function from
   an application using the driver. You can also [verify the driver version](/user-guide/snowflake-client-version-check) by
   examining queries executed by the driver in the QUERY\_HISTORY view.
3. Go to the [ODBC Driver download page](https://www.snowflake.com/en/developers/downloads/odbc/), select your
   platform and a **3.x** version, and download the installer. To browse files directly, including earlier releases,
   use the [Downloading Snowflake Clients, Connectors, Drivers, and Libraries](/user-guide/snowflake-client-repository). Do not select the latest overall version if you intend to stay on 3.x.

   Note

   The Linux installation package is provided in three variations:

   - TGZ (TAR file compressed using .GZIP)
   - RPM
   - DEB

   The TGZ package requires some manual configuration tasks. The RPM and DEB packages include an automated installer and support
   validation using the public GPG key provided by Snowflake.
4. See the following topics to install and configure the driver:

   - [Installing and configuring the ODBC Driver 3.x for Windows](/developer-guide/odbc/odbc-windows-3x)
   - [Installing and configuring the ODBC Driver 3.x for macOS](/developer-guide/odbc/odbc-mac-3x)
   - [Installing and configuring the ODBC Driver 3.x for Linux](/developer-guide/odbc/odbc-linux-3x)
   - [ODBC configuration and connection parameters](/developer-guide/odbc/odbc-parameters)

## Update within 3.x

1. Identify the installed version using [client version information](/user-guide/snowflake-client-version-check),
   and review the [release notes](/release-notes/clients-drivers/odbc) through your target 3.x version.
2. Save your current installer, DSN settings, and driver configuration before changing the installation.
3. Download the target **3.x** package for your OS and application architecture. Follow the
   [Linux](/developer-guide/odbc/odbc-linux-3x), [macOS](/developer-guide/odbc/odbc-mac-3x), or
   [Windows](/developer-guide/odbc/odbc-windows-3x) instructions.
4. Test the connection from your application and verify that it reports the target version before updating other hosts.

To move to 4.x instead, use the [migration guide](/developer-guide/odbc/odbc-migration).
