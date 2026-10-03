# Installing and configuring the ODBC Driver 4.x for Linux

**Version: 4.x.** [Switch to ODBC 3.x](/developer-guide/odbc/odbc-linux-3x) · [Choose another task](/developer-guide/odbc/odbc).

Linux uses named data sources (DSNs) for connecting ODBC-based client applications to Snowflake. You can choose to install the ODBC driver using the `.tar.gz` archive, RPM package, or DEB package.

Important

These instructions install ODBC 4.x. Installing 4.x replaces 3.x on the machine. If you currently use 3.x,
read the [migration guide](/developer-guide/odbc/odbc-migration) and validate on a separate host first.
To stay on 3.x, use the [3.x Linux instructions](/developer-guide/odbc/odbc-linux-3x).

## Prerequisites

### Operating system

For a list of the operating systems supported by Snowflake clients, see [Operating system support](/release-notes/requirements#label-client-operating-system-support).

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

   Use the file locations reported by this command in the configuration steps below.

## Step 1: Verify the package signature (RPM or DEB only) — *Optional*

Note

If you are installing the ODBC driver by using `yum` or the
[`.tar.gz` archive](#label-odbc-linux-install-tgz), skip this step.

If you are installing the ODBC driver using the RPM or DEB package and wish to verify the package signature before installation, perform the following tasks:

### 1.1: Download and import the latest Snowflake public key

For ODBC 4.x, download and import the Snowflake GPG public key:

```
$ gpg --keyserver hkp://keyserver.ubuntu.com --recv-keys 3C98F63C9292CE02
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

For an older installer, see [historical signing keys](/developer-guide/odbc/odbc-linux-3x#label-odbc-driver-gpg-key-list-3x).

### 1.2: Download the RPM or DEB driver package

Download the package from the Snowflake Client Repository. For details, see [Downloading the ODBC Driver 4.x](/developer-guide/odbc/odbc-download).

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

   Here is a sample policy file for a key with the ID 3C98F63C9292CE02:

   ```
   <?xml version="1.0"?>
   <!DOCTYPE Policy SYSTEM "http://www.debian.org/debsig/1.0/policy.dtd">
   <Policy xmlns="https://www.debian.org/debsig/1.0/">
   <Origin Name="Snowflake Computing" id="3C98F63C9292CE02"
   Description="Snowflake ODBC Driver DEB package"/>

   <Selection>
   <Required Type="origin" File="debsig.gpg" id="3C98F63C9292CE02"/>
   </Selection>

   <Verification MinOptional="0">
   <Required Type="origin" File="debsig.gpg" id="3C98F63C9292CE02"/>
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
- [Install the driver by using the downloaded `.tar.gz` archive](#label-odbc-linux-install-tgz).
- [Install the downloaded RPM package](#label-odbc-linux-install-rpm).
- [Install the downloaded DEB package](#label-odbc-linux-install-deb).

### Using yum to download and install the driver

You can use `yum` to download and install the driver.

To download and install the Snowflake ODBC driver for Linux using `yum`:

1. Create a file named `/etc/yum.repos.d/snowflake-odbc.repo`, and add the following text to the file:

   Copy code

   ```
   [snowflake-odbc]
   name=snowflake-odbc
   baseurl=https://sfc-repo.snowflakecomputing.com/odbc/linux/<VERSION_NUMBER>/
   gpgkey=https://sfc-repo.snowflakecomputing.com/odbc/Snowkey-<GPG_KEY_ID>-gpg
   ```

   Set `VERSION_NUMBER` to the 4.x version to install, for example 4.0.0.
   Set `GPG_KEY_ID` to 3C98F63C9292CE02.
   For aarch64, use `odbc/linuxaarch64/<VERSION_NUMBER>/` in `baseurl`.

   To use the Azure mirror, replace `sfc-repo.snowflakecomputing.com` with
   `sfc-repo.azure.snowflakecomputing.com` in both URLs. See [Downloading Snowflake Clients, Connectors, Drivers, and Libraries](/user-guide/snowflake-client-repository).
2. Run the following command to install the driver:

   Copy code

   ```
   yum install snowflake-odbc
   ```

### Installing the tar.gz archive

Download the `.tar.gz` package for your architecture from [Downloading the ODBC Driver 4.x](/developer-guide/odbc/odbc-download).
Extract `snowflake-odbc-<version>.<arch>.tar.gz` into a working directory. For example, for `x86_64`:

Copy code

```
tar -xzf snowflake-odbc-<version>.x86_64.tar.gz
```

The archive contains `usr/lib64/snowflake/odbc/`, with `lib`, `include`, and `templates` subdirectories.
Move the extracted driver directory to your chosen installation location and use its absolute path when
registering `lib/libsfodbc.so`. The archive does not run an installer or include the 3.x setup scripts.
Register the driver and configure a DSN as described in [Step 3: Configure the ODBC Driver](#label-odbc-configure-driver).

On aarch64 hosts, extract `snowflake-odbc-<version>.aarch64.tar.gz` instead.

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
>
> On aarch64 hosts, install `snowflake-odbc-<version>.aarch64.rpm`.

Note

The installation directory is `/usr/lib64/snowflake/odbc/`. You’ll need the location later in the instructions.

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

On aarch64 hosts, install `snowflake-odbc-<version>.aarch64.deb`.

If the `SF_ACCOUNT` variable is unset, the `dpkg` command shows a warning. When you set the variable as shown, a Snowflake connection is added to the `odbc.ini` file.

The command might fail if any required dependencies for the package manager are not installed. If that happens, install them now:

Copy code

```
sudo apt-get install -f
```

Note

The installation directory is `/usr/lib64/snowflake/odbc/`. You’ll need the location later in the instructions.

## Step 3: Configure the ODBC Driver

Configuring the ODBC driver requires adding entries to the following files:

- For 4.x logging and driver-manager encoding, a user-level `sf.odbc.ini`, as described below.
- Your driver manager’s `odbcinst.ini` file for driver registration.
- Your driver manager’s `odbc.ini` file for DSNs.

For RPM and DEB installations, the installer registers the 4.x driver with unixODBC. For a 4.x archive,
`<path>` in the registration example below is the absolute path to the extracted driver directory containing
`lib/libsfodbc.so`.

### 3.1: Driver configuration and logging

For 4.x, create `~/.snowflake/sf.odbc.ini` for logging or encoding settings, or set `SF_ODBC_INI` to the
absolute path of your configuration file. The Linux driver does not search its installation directory for
this file. Set file permissions to `0600`. For example:

Copy code

```
LogLevel=INFO
LogPath=/path/to/writable/log/directory
DriverManagerEncoding=UTF-16
```

Use `UTF-16` for unixODBC and `UTF-32` for iODBC when `SQLWCHAR` is four bytes. See
[Configuration differences](/developer-guide/odbc/odbc-migration#label-odbc-migration-config) for the complete search order and
recognized keys. Connection settings belong in the DSN or connection string, not in this logging file.

Verify that you have write permissions on the log path.

### 3.2: `odbcinst.ini` file (driver registration)

Add the following entries to the `odbcinst.ini` file:

> Copy code
>
> ```
> [ODBC Drivers]
> Snowflake ODBC=Installed
>
> [Snowflake ODBC]
> APILevel=1
> ConnectFunctions=YYY
> Description=Snowflake ODBC
> Driver=<path>/lib/libsfodbc.so
> DriverODBCVer=03.80
> SQLLevel=1
> ```

Replace `<path>` with the absolute installation directory containing `lib/libsfodbc.so`.

### 3.3: `odbc.ini` file (DSN entries)

For each DSN, add the following entries to the `odbc.ini` file:

- DSN Name and driver name (**Snowflake ODBC**), in the form of `<dsn_name> = <driver_name>`.
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
  testodbc1 = Snowflake ODBC
  testodbc2 = Snowflake ODBC

  [testodbc1]
  Driver      = Snowflake ODBC
  Description =
  server      = myorganization-myaccount.snowflakecomputing.com
  role        = sysadmin

  [testodbc2]
  Driver      = Snowflake ODBC
  Description =
  server      = xy12345.snowflakecomputing.com
  role        = analyst
  database    = sales
  warehouse   = analysis
  ```

Note the following:

- Both `testodbc1` and `testodbc2` have default roles.
- `testodbc2` also has a default database and warehouse.

## Step 4: Test the ODBC Driver

Test the driver using the installed driver manager (either iODBC or unixODBC).

### Testing with iODBC

Test the DSNs you created. On the command line, specify the DSN name, user login name, and password, using the following format:

> `iodbctest "DSN=<dsn_name>;UID=<user_name>;PWD=<password>"`

For example:

Copy code

```
iodbctest "DSN=testodbc2;UID=mary;PWD=password"
```

After connecting, confirm that the client reports a 4.x driver version.

### Testing with unixODBC

Test the DSNs you created using the `isql` command-line utility provided with `unixODBC`.

On the command line, specify the DSN name, user login name, and password.

For example:

Copy code

```
isql -v testodbc2 mary <password>
```

After connecting, confirm that the client reports a 4.x driver version.
