# Installing and configuring the ODBC Driver for Linux

Linux uses named data sources (DSNs) for connecting ODBC-based client applications to Snowflake. You can choose to install the ODBC driver using the TGZ file, RPM package, or DEB package provided in the Snowflake Client Repository.

## Prerequisites

### Operating system

For a list of the operating systems supported by Snowflake clients, see [Operating system support](/release-notes/requirements#label-client-operating-system-support).

With ODBC version 3.0.1, the driver no longer supports CentOS 6 versions.

### Driver manager: iODBC or unixODBC

A driver manager is required to manage communication between Snowflake and the ODBC driver. The driver supports using either iODBC or unixODBC as the driver manager.

#### iODBC

If iODBC is not installed on CentOS, as `sudo`, execute the following command:

Copy code

```
yum install libiodbc
```

#### unixODBC

unixODBC provides the `odbcinst` and `isql` command-line utilities used to install, configure, and test the driver. To verify whether unixODBC is installed, execute the following commands:

Copy code

```
which odbcinst

which isql
```

If unixODBC is not installed:

1. As `sudo`, execute the following commands:

> Copy code
>
> ```
> yum search unixODBC
>
> yum install unixODBC.x86_64
> ```

1. Verify the directory where `odbcinst` expects the `odbcinst.ini` and `odbc.ini` files to be located:

   Copy code

   ```
   odbcinst -j
   ```

   The location should be `/etc`.

## Step 1: Verify the package signature (RPM or DEB only) — *Optional*

Note

If you are installing the ODBC driver by using `yum` or the
[TGZ file](#label-odbc-linux-install-tgz), skip this step.

If you are installing the ODBC driver using the RPM or DEB package and wish to verify the package signature before installation, perform the following tasks:

### 1.1: Download and import the latest Snowflake public key

From the public keyserver, download and import the Snowflake GPG public key for the version of the ODBC driver that you are using:

- For version 3.17.0 and higher:

  ```
  $ gpg --keyserver hkp://keyserver.ubuntu.com --recv-keys 3C98F63C9292CE02
  ```
- For version 3.6.0 through 3.16.x:

  ```
  $ gpg --keyserver hkp://keyserver.ubuntu.com --recv-keys 2A3149C82551A34A
  ```
- For version 3.5.0:

  ```
  $ gpg --keyserver hkp://keyserver.ubuntu.com --recv-keys 5A125630709DD64B
  ```
- For version 2.25.6 through 3.4.1:

  ```
  $ gpg --keyserver hkp://keyserver.ubuntu.com --recv-keys 630D9F3CAB551AF3
  ```
- For version 2.22.1 through 2.25.5:

  ```
  $ gpg --keyserver hkp://keyserver.ubuntu.com --recv-keys 37C7086698CB005C
  ```
- For version 2.18.2 through 2.22.0:

  ```
  $ gpg --keyserver hkp://keyserver.ubuntu.com --recv-keys EC218558EABB25A1
  ```
- For version 2.18.1 and lower:

  ```
  $ gpg --keyserver hkp://keyserver.ubuntu.com --recv-keys 93DB296A69BE019A
  ```

  Note

  If this command fails with the following error:

  > Copy code
  >
  > ```
  > gpg: keyserver receive failed: Server indicated a failure
  > ```

  then specify that you want to use port 80 for the keyserver:

  > Copy code
  >
  > ```
  > gpg --keyserver hkp://keyserver.ubuntu.com:80  ...
  > ```

### 1.2: Download the RPM or DEB driver package

Download the package from the Snowflake Client Repository. For details, see [Downloading the ODBC Driver](/developer-guide/odbc/odbc-download).

### 1.3: Verify the signature for the RPM or DEB driver package

#### RPM package signature

1. Verify the key was imported successfully:

   Copy code

   ```
   gpg --list-keys
   ```

   The command should display the Snowflake key.
2. Verify the signature:

   Copy code

   ```
   rpm -K snowflake-odbc-<version>.x86_64.rpm
   ```

   Note

   If `rpm` does not have the GPG key that you imported, the command will report that the signatures are not OK and will
   produce a `NOKEY` warning:

   Copy code

   ```
   rpm -K snowflake-odbc-<version>.x86_64.rpm
   ```

   ```
   snowflake-odbc-<version>.x86_64.rpm: digests SIGNATURES NOT OK

   rpm -Kv snowflake-odbc-<version>.x86_64.rpm
   ```

   ```
   snowflake-odbc-<version>.rpm:
    Header V4 RSA/SHA1 Signature, key ID 98cb005c: NOKEY
    Header SHA1 digest: OK
    V4 RSA/SHA1 Signature, key ID 98cb005c: NOKEY
    MD5 digest: OK
   ```

   If this occurs, run the following commands to export the GPG key, import the key into `rpm`, and verify the
   signature again:

   Copy code

   ```
   gpg --export -a <GPG_KEY_ID> > odbc-signing-key.asc
   sudo rpm --import odbc-signing-key.asc
   rpm -K snowflake-odbc-<version>.x86_64.rpm
   ```

   where `<GPG_KEY_ID>` is the ID for the key that you installed in [1.1: Download and import the latest Snowflake public key](#label-odbc-driver-gpg-key-list).

#### DEB package signature

1. Install the package signature verification tool:

   Copy code

   ```
   sudo apt-get install debsig-verify
   ```
2. Import the public key to the keyring:

   Copy code

   ```
   mkdir /usr/share/debsig/keyrings/<GPG_KEY_ID>
   gpg --export <GPG_KEY_ID> > snowflakeKey.asc
   touch /usr/share/debsig/keyrings/<GPG_KEY_ID>/debsig.gpg
   gpg --no-default-keyring --keyring /usr/share/debsig/keyrings/<GPG_KEY_ID>/debsig.gpg --import snowflakeKey.asc
   ```

   where `<GPG_KEY_ID>` is the ID for the key that you installed in [1.1: Download and import the latest Snowflake public key](#label-odbc-driver-gpg-key-list).
3. Configure a policy for the key. For details, see `/usr/share/doc/debsig-verify`. The policy must be stored in the following directory:

   Copy code

   ```
   /etc/debsig/policies/<GPG_KEY_ID>
   ```

   where `<GPG_KEY_ID>` is the ID for the key that you installed in [1.1: Download and import the latest Snowflake public key](#label-odbc-driver-gpg-key-list).

   Store the policy in a file named `policy_name.pol`, where `policy_name` is your name for the policy. For the policy name, you can use any text string, however the string cannot contain blank spaces.

   Here is a sample policy file for a key with the ID 2A3149C82551A34A:

   ```
   <?xml version="1.0"?>
   <!DOCTYPE Policy SYSTEM "http://www.debian.org/debsig/1.0/policy.dtd">
   <Policy xmlns="https://www.debian.org/debsig/1.0/">
   <Origin Name="Snowflake Computing" id="2A3149C82551A34A"
   Description="Snowflake ODBC Driver DEB package"/>

   <Selection>
   <Required Type="origin" File="debsig.gpg" id="2A3149C82551A34A"/>
   </Selection>

   <Verification MinOptional="0">
   <Required Type="origin" File="debsig.gpg" id="2A3149C82551A34A"/>
   </Verification>

   </Policy>
   ```
4. Verify the signature:

   Copy code

   ```
   sudo debsig-verify snowflake-odbc-<version>.x86_64.deb
   ```

Note

By default, the dpkg package signature verification tool does not check the signature when you install the package. If you want to verify the signature every time you run dpkg, remove the
`--no-debsig` line in the `/etc/dpkg/dpkg.cfg` file.

### 1.4: Delete the old Snowflake public key — *Optional*

Your local environment can contain multiple GPG keys; however, for security reasons, Snowflake periodically rotates the public GPG key. As a best practice, we recommend deleting the existing public key
after confirming that the latest key works with the latest signed package.

To delete the key:

> Copy code
>
> ```
> gpg --delete-key "Snowflake Computing"
> ```

## Step 2: Install the ODBC Driver

Install the driver using one of the following approaches:

- [Use yum to download and install the driver](#label-odbc-linux-install-yum).
- [Install the driver by using the downloaded TGZ file (TAR file compressed using .GZIP)](#label-odbc-linux-install-tgz).
- [Install the downloaded RPM package](#label-odbc-linux-install-rpm).
- [Install the downloaded DEB package](#label-odbc-linux-install-deb).

### Using yum to download and install the driver

With version 2.21.1 of the ODBC Driver (and later versions), you can use `yum` to download and install the driver.

To download and install the Snowflake ODBC driver for Linux using `yum`:

1. Create a file named `/etc/yum.repos.d/snowflake-odbc.repo`, and add the following text to the file:

   Copy code

   ```
   [snowflake-odbc]
   name=snowflake-odbc
   baseurl=https://sfc-repo.snowflakecomputing.com/odbc/linux/<VERSION_NUMBER>/
   gpgkey=https://sfc-repo.snowflakecomputing.com/odbc/Snowkey-<GPG_KEY_ID>-gpg
   ```

   where `VERSION_NUMBER` is the specific version number of the driver (for example, 3.21.0) and `GPG_KEY_ID` is one of the
   following key IDs:

   | ODBC Driver Version | GPG Key ID |
   | --- | --- |
   | 3.17.0 and higher | 3C98F63C9292CE02 |
   | 3.6.0 through 3.16.x | 2A3149C82551A34A |
   | 3.5.0 | 5A125630709DD64B |
   | 2.25.6 through 3.4.1 | 630D9F3CAB551AF3 |
   | 2.22.1 through 2.25.5 | 37C7086698CB005C |
   | In the settings above, `baseurl` and `gpgkey` point to the [Snowflake Client Repository](/user-guide/snowflake-client-repository#label-client-download-repository) on Amazon S3. If |  |
   | you want to use the mirror on Azure Blob instead, change the hostname to `https://sfc-repo.azure.snowflakecomputing.com/`: |  |
   |  |  |
   | [snowflake-odbc] |  |
   | name=snowflake-odbc |  |
   | baseurl=<https://sfc-repo.azure.snowflakecomputing.com/odbc/linux/&lt;VERSION_NUMBER&gt;/> |  |
   | gpgkey=<https://sfc-repo.azure.snowflakecomputing.com/odbc/Snowkey-&lt;GPG_KEY_ID&gt;-gpg> |  |

   Expand

   Show lessSee more
2. Run the following command to install the driver:

   Copy code

   ```
   yum install snowflake-odbc
   ```

### Installing the TGZ file

To install the Snowflake ODBC driver for Linux using
[the TGZ file that you downloaded earlier](/developer-guide/odbc/odbc-download).

1. Copy the downloaded file (`snowflake_linux_x8664_odbc-version.tgz`) to a working directory.
2. Unzip the file:

> Copy code
>
> ```
> gunzip snowflake_linux_x8664_odbc-<version>.tgz
> ```

1. Extract the files from the .tar file:

> Copy code
>
> ```
> tar -xvf snowflake_linux_x8664_odbc-<version>.tar
> ```

1. Copy the resulting `snowflake_odbc` folder to the directory where you want to install the driver. Make note of this directory. You’ll need the location later in the instructions.

### Installing the RPM package

Note

The RPM package requires unixODBC as the driver manager.

To install the Snowflake ODBC driver for Linux using
[the RPM package that you downloaded earlier](/developer-guide/odbc/odbc-download), after
[optionally verifying the package signature](#label-verify-pkg-sig), run the following command:

> Copy code
>
> ```
> yum install snowflake-odbc-<version>.x86_64.rpm
> ```

Note

The installation directory is `/usr/lib64/snowflake/odbc/`. You’ll need the location later in the instructions.

If the driver cannot find the library, it displays an `Unable to locate SQLGetPrivateProfileString function` error. In this case, you must set `ODBCInstLib=<driver_manager_path>` manually in the `simba.snowflake.ini` configuration file with the name of the driver manager on your system. For more information, see [Configure the ODBC Driver](#label-odbc-configure-driver).

For example, `ODBCInstLib=/usr/lib/x86_64-linux-gnu/libodbcinst.so.2`.

### Installing the DEB package

Note

The DEB package requires unixODBC as the driver manager. Make sure that the unixodbc and odbcinst packages are installed before attempting to install the DEB package.

To install the Snowflake ODBC driver for Linux using
[the DEB package that you downloaded earlier](/developer-guide/odbc/odbc-download), after
[optionally verifying the package signature](#label-verify-pkg-sig), run the following command:

Copy code

```
sudo SF_ACCOUNT="<account>" dpkg -i snowflake-odbc-<version>.x86_64.deb
```

If the `SF_ACCOUNT` variable is unset, the `dpkg` command shows a warning. When you set the variable as shown, a Snowflake connection is added to the `odbc.ini` file.

The command might fail if any required dependencies for the package manager are not installed. If that happens, install them now:

Copy code

```
sudo apt-get install -f
```

Note

The installation directory is `/usr/lib/snowflake/odbc/`. You’ll need the location later in the instructions.

## Step 3: Configure the environment (TGZ only)

Note

If you installed the ODBC driver using the RPM or DEB package file, skip this step.

If you installed using the TGZ file, configure the environment using the installed driver manager (either iODBC or unixODBC).

### Configuring with iODBC

In a terminal window, change to the `snowflake_odbc` directory, and run the following command to install Snowflake ODBC:

Copy code

```
./iodbc_setup.sh
```

This script completes the following steps:

> - Adds one Snowflake connection to your system-level `/etc/odbc.ini` file.
> - Adds the Snowflake driver information to your system-level `/etc/odbcinst.ini` file.
> - Adds all certificate authority (CA) certificates required by the Snowflake ODBC driver to your system-level `simba.snowflake.ini` file.

By running `iodbc_setup.sh`, you don’t need to set any environment variables.

Alternatively, if you don’t want Snowflake to change your system configurations, add the following environment variables to your shell configuration file (for example, `.profile` or `.bash_profile`):

> - `ODBCINI = <path>/conf/odbc.ini`
> - `ODBCINSTINI = <path>/conf/odbcinst.ini`

Where `path` is the location of the `snowflake_odbc` directory. If you have configured other ODBC drivers in your system and plan to add the Snowflake ODBC entries to your existing `odbc.ini` and
`odbcinst.ini` files in the next step, then point ODBCINI and ODBCINSTINI to the location of those files.

### Configuring with unixODBC

In a terminal window, change to the `snowflake_odbc` directory, and run the following command to install Snowflake ODBC:

Copy code

```
./unixodbc_setup.sh
```

This script completes the following steps:

> - Adds a Snowflake connection to your system-level `/etc/odbc.ini` file.
> - Adds the Snowflake driver information to your system-level `/etc/odbcinst.ini` file.
> - Adds all certificate authority (CA) certificates required by the Snowflake ODBC driver to your system-level `simba.snowflake.ini` file.

By running `unixodbc_setup.sh`, you don’t need to set any environment variables.

Alternatively, if you don’t want Snowflake to change your system configurations, add the following environment variables to your shell configuration file, for example `.profile` or `.bash_profile`:

> - `ODBCSYSINI = <path>/conf/`

Where `path` is the location of the `snowflake_odbc` directory. If you have configured other ODBC drivers in your system and plan to add the Snowflake ODBC entries to your existing `odbc.ini` and
`odbcinst.ini` files in the next step, then point ODBCSYSINI to the location of those files.

## Step 4: Configure the ODBC Driver

Configuring the ODBC driver requires adding entries to the following files:

- `<path>/lib/simba.snowflake.ini`
- `/etc/odbcinst.ini` (or `<path>/conf/odbc.ini`, if you are using environment variables)
- `/etc/odbc.ini` (or `<path>/conf/odbcinst.ini`, if you are using environment variables)

Where `path` is the location of the `snowflake_odbc` directory.

### 4.1: `simba.snowflake.ini` file (driver manager and logging)

Add the following entries to the `simba.snowflake.ini` file:

> Copy code
>
> ```
> ErrorMessagesPath=<path>/ErrorMessages/
> LogPath=/tmp/
> ODBCInstLib=<driver_manager_path>
> CABundleFile=<path>/lib/cacert.pem
> ANSIENCODING=UTF-8
> ```

Where:

> - `path` is the location of the `snowflake_odbc` directory.
> - `driver_manager_path` is the location of your driver manager directory:
>
>   > - iODBC: `ODBCInstLib=libiodbcinst.so.2`
>   > - unixODBC: `ODBCInstLib=libodbcinst.so`
>   >
>   > Note
>   >
>   > If your driver manager directory is not included in the `LD_LIBRARY_PATH` environment variable, specify the full path to the driver manager library here.

Verify that you have write permissions on the log path.

The `ANSIENCODING` parameter specifies the application’s character encoding. The default is `UTF-8`. The
parameter is intended for use only by Snowflake; customers should not change the value.

### 4.2: `odbcinst.ini` file (driver registration)

Add the following entries to the `odbcinst.ini` file:

> Copy code
>
> ```
> [ODBC Drivers]
> SnowflakeDSIIDriver=Installed
>
> [SnowflakeDSIIDriver]
> APILevel=1
> ConnectFunctions=YYY
> Description=Snowflake DSII
> Driver=/<path>/lib/libSnowflake.so
> DriverODBCVer=03.52
> SQLLevel=1
> ```

Where `path` is the location of the `snowflake_odbc` directory.

### 4.3: `odbc.ini` file (DSN entries)

For each DSN, add the following entries to the `odbc.ini` file:

- DSN Name and driver name (SnowflakeDSIIDriver), in the form of `<dsn_name> = <driver_name>`.
- Parameters:

  - Required connection parameters, such as `server`.
  - Any additional, optional parameters, such as default `role`, `database`, and `warehouse`.

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
  testodbc1 = SnowflakeDSIIDriver
  testodbc2 = SnowflakeDSIIDriver

  [testodbc1]
  Driver      = /usr/jsmith/snowflake_odbc/lib/libSnowflake.so
  Description =
  server      = myorganization-myaccount.snowflakecomputing.com
  role        = sysadmin

  [testodbc2]
  Driver      = /usr/jsmith/snowflake_odbc/lib/libSnowflake.so
  Description =
  server      = xy12345.snowflakecomputing.com
  role        = analyst
  database    = sales
  warehouse   = analysis
  ```

Note the following:

- Both `testodbc1` and `testodbc2` have default roles.
- `testodbc2` also has a default database and warehouse.

## Step 5: Test the ODBC Driver

Test the driver using the installed driver manager (either iODBC or unixODBC).

### Testing with iODBC

Test the DSNs you created. On the command line, specify the DSN name, user login name, and password, using the following format:

> `iodbctest "DSN=<dsn_name>;UID=<user_name>;PWD=<password>"`

For example:

Copy code

```
iodbctest "DSN=testodbc2;UID=mary;PWD=password"
```

```
iODBC Demonstration program
This program shows an interactive SQL processor
Driver Manager: 03.52.0709.0909
Driver: 2.12.70 (Snowflake)

SQL>
```

### Testing with unixODBC

Test the DSNs you created using the `isql` command-line utility provided with `unixODBC`.

On the command line, specify the DSN name, user login name, and password.

For example:

Copy code

```
isql -v testodbc2 mary <password>
```

```
Dec 14 22:57:50 INFO  2022078208 Driver::LogVersions: SDK Version: 09.04.09.1013
Dec 14 22:57:50 INFO  2022078208 Driver::LogVersions: DSII Version: 2.12.36
Dec 14 22:57:50 INFO  2022078208 SFConnection::connect: Tracing level: 4

+---------------------------------------+
| Connected!                            |
|                                       |
| sql-statement                         |
| help [tablename]                      |
| quit                                  |
|                                       |
+---------------------------------------+
SQL>
```
