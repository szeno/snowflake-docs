# Installing and configuring the ODBC Driver for macOS

Similar to Windows, macOS utilizes named data sources (DSNs) for connecting ODBC-based client applications to Snowflake.

## Prerequisites

### Operating system

For a list of the operating systems supported by Snowflake clients, see [Operating system support](/release-notes/requirements#label-client-operating-system-support).

With ODBC version 3.0.1, the driver no longer supports MacOS 10.14 and 10.15 versions.

### iODBC

The Snowflake ODBC driver for Mac requires iODBC.

You can download the iODBC from:

> <https://www.iodbc.org/dataspace/doc/iodbc/wiki/iodbcWiki/Downloads>

To install iODBC:

1. After downloading iODBC, double-click on the downloaded .dmg file.
2. Double-click on the installer file, `iODBC-SDK.pkg`, and follow the prompts.

   By default, the package installs the software in the `/Library/Application Support/iODBC/bin` directory. You can add this directory to the
   `$PATH` environment variable to avoid needing to specify the full pathname to execute any of the iODBC commands.

Note

iODBC provides a GUI administrator tool for configuring drivers and DSNs; however, this tool has not been tested for use with Snowflake and,
therefore, should not be used to create or manage DSNs.

## Step 1: Install the ODBC Driver

To install the Snowflake ODBC driver for macOS:

1. If you haven’t already downloaded the driver, download it now. For details, see [Downloading the ODBC Driver](/developer-guide/odbc/odbc-download).
2. Open the downloaded .dmg file, `snowflake_odbc_mac-<version>.dmg`.
3. Open the installer file, `snowflakeODBC_<version>.pkg`, and follow the prompts.

   You will likely be prompted for the administrator/sudo password for the machine on which you are installing the driver.

If you choose the default directory when prompted, the installer installs the ODBC driver files in the following directories:

> `/opt/snowflake/snowflakeodbc`
>
> `/Library/ODBC`

## Step 2: Configure the ODBC Driver

To configure the ODBC driver for macOS, create one or more data source (DSNs), which are stored in the following files, depending on the type of DSN you create:

> - User DSNs: `~/Library/ODBC/odbc.ini`
> - System DSNs: `/Library/ODBC/odbc.ini`

To create a DSN, edit the appropriate `odbc.ini` file.

### Creating a DSN by adding an entry in the `odbc.ini` file

If a user or system DSN has already been created for the driver, add the new entry to the `odbc.ini` file that already exists in the corresponding directory for the type of DSN you are creating. If you are creating the first DSN
for the driver, you must manually create the `odbc.ini` file and add the entry to the file.

For each DSN, specify:

- DSN name and driver name (Snowflake), in the form of `<dsn_name> = <driver_name>`.
- Directory path and name of the driver file, in the form of `Driver = /opt/snowflake/snowflakeodbc/lib/universal/libSnowflake.dylib`.
- Connection parameters, such as `server` and `uid` (user login name). Any connection parameters you add to the DSN do not need to be specified in the ODBC connect string.
- Any additional parameters, such as default `role`, `database`, and `warehouse`.

Parameters are specified in the form of `<parameter_name> = <value>`. For details about the parameters that can be set for each DSN, see [ODBC configuration and connection parameters](/developer-guide/odbc/odbc-parameters).

The following example illustrates an `odbc.ini` file that configures two data sources that use different forms of an
[account identifier](/user-guide/gen-conn-config) in the `server` URL:

- `testodbc1` uses the [account name as an identifier](/user-guide/admin-account-identifier#label-account-name-using) for the account `myaccount` in the
  organization `myorganization`.
- `testodbc2` uses the [account locator](/user-guide/admin-account-identifier#label-account-locator) `xy12345` as the account identifier.

  Note that `testodbc2` uses an account in the AWS US West (Oregon) region. If the account is in a different region or if
  the account uses a different cloud provider, you need to
  [specify additional segments after the account locator](/user-guide/admin-account-identifier#label-account-locator).

  Copy code

  ```
  [ODBC Data Sources]
  testodbc1 = Snowflake
  testodbc2 = Snowflake

  [testodbc1]
  Driver      = /opt/snowflake/snowflakeodbc/lib/universal/libSnowflake.dylib
  Description =
  uid         = peter
  server      = myorganization-myaccount.snowflakecomputing.com
  role        = sysadmin

  [testodbc2]
  Driver      = /opt/snowflake/snowflakeodbc/lib/universal/libSnowflake.dylib
  Description =
  uid         = mary
  server      = xy12345.snowflakecomputing.com
  role        = analyst
  database    = sales
  warehouse   = analysis
  ```

Note the following:

- Both `testodbc1` and `testodbc2` have default roles.
- `testodbc2` also has a default database and warehouse.

## Step 3: Test the ODBC Driver

You can use the `iodbctest` command-line utility provided with iODBC to test the DSNs you create.

When prompted for the ODBC connect string, enter the required connection parameters (DSN name, server, user login name, and password), as well as any other parameters that you would like to enter as part of the connect string. The
connect string takes parameters in the form of `<parameter_name>=<value>`, e.g. `dsn=testodbc2`, with each parameter separated by a semi-colon (`;`) and no blank spaces. For the list of supported parameters, see
[ODBC configuration and connection parameters](/developer-guide/odbc/odbc-parameters).

Note

If you set the server and user login name in the DSN, the only required parameters in the connect string are the DSN name and user password.

For example:

Copy code

```
$ "/Library/Application Support/iODBC/bin/iodbctest"

iODBC Demonstration program
This program shows an interactive SQL processor
Driver Manager: 03.52.0607.1008

Enter ODBC connect string (? shows list): dsn=testodbc2;pwd=<password>

Dec 14 20:16:08 INFO  1299 SFConnection::connect: Tracing level: 4

Driver: 2.12.36 (Snowflake - Latest version supported by Snowflake: 2.12.38)

SQL>
```
