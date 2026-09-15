# Starting and Stopping sfsql — *Obsoleted*

Obsoleted Feature

`sfsql` is now obsoleted. Use [SnowSQL](/user-guide/snowsql) instead.

This topic describes how to use `sfsql` to connect to Snowflake, initiate a session to execute queries and DDL/DML statements, and close the session when you’re finished.

## Connecting to Snowflake and Initiating a Session

To connect to Snowflake and initiate a session, navigate to the directory where the `sfsql` script is located and execute the script using the following syntax.

> Copy code
>
> ```
> sfsql [ -u <user> ] [ -c <password> ] [ -d <database> ] [ -s <schema> ] ... [ -h ]
> ```

Note

In a Linux environment, you must precede the script name with a dot-slash, e.g. `./sfsql`. If you start the client from any directory other than the `client` install directory, you must also
include the path after the forward slash.

### Parameters

| Connection Parameter | Equivalent in `login.defaults` | Description |
| --- | --- | --- |
| `-g <host>` | `GSIP=<host>` | Host/IP to connect to. Set by default in `login.defaults` when the client was downloaded from Snowflake. |
|  |  | Format of `<host>` for accounts in US West: `<account_name>.snowflakecomputing.com` |
|  |  | Format of `<host>` for accounts in all other regions: `<account_name>.<region_id>.snowflakecomputing.com` |
| `-a <account_name>` | `ACCOUNT=<name>` | Snowflake account to connect to. Set by default in `login.defaults` when the client was downloaded from Snowflake. |
| `-u <user>` | `USER=<login_name>` | Login name of user to connect with. If this parameter is specified, the `-c` parameter also should be specified. |
| `-c <password>` | `PASSWORD=<password>` | Password for the user. |
| `-b <authenticator>` | `AUTHENTICATOR=<authenticator>` | Use a SAML 2.0-compliant IdP, instead of Snowflake, to authenticate. |
| `-r <role>` | `ROLE=<name>` | Role to use by default for accessing objects in Snowflake (can be changed after login). |
| `-d <database>` | `DATABASE=<name>` | Database to use by default (can be changed after login). |
| `-s <schema>` | `SCHEMA=<name>` | Database schema to use by default (can be changed after login). |
| `-w <warehouse>` | `WAREHOUSE=<name>` | Virtual warehouse to use by default for queries, loading, etc. (can be changed after login). |
| `-f <sqlfile>` | N/A | Execute the specified SQL file. If this parameter is not specified, the client connects in interactive mode. |
| `-t` | `TRACING=<level>` | Logging level. |
| `-y <proxy host>` | `PROXY_HOST=<host>` | HTTP proxy host. |
| `-z <proxy port>` | `PROXY_PORT=<port>` | Port for HTTP proxy host. |
| `-m <mfa_passcode>` | `PASSCODE=<mfa_passcode>` | MFA passcode. |
| `-n` | `PASSCODEINPASSWORD=true` | MFA passcode embedded in password. |
| `-k` | `EXITONERROR=true` | Exit the client when an error is encountered. |
| `-h` | N/A | Help for login parameters (i.e. this list). |

Expand

Show lessSee more

Note

If you do not specify a login name or password either in `login.defaults` or in the command line, the client prompts you to enter them during login.

If you provide an incorrect login name or password, the client does not connect to Snowflake and exits to the HenPlus shell command line. You must then exit the shell (by typing `exit`, `quit`, or
using the **[CTRL]-d** keyboard combo) before attempting to log in again. Or, in the HenPlus shell, you can type `connect` followed by a valid JDBC connect string to log in.

During login, the client displays the version of the JDBC driver used by the client, as well as the latest available version of the driver (if it is different from the version in use). This information
can be useful when troubleshooting client issues.

After successful login, the command line displays the login name of the user and the host to which the session is connected in the form `<login_name>@snowflake:<account_name>.snowflakecomputing.com`.

### Example

The following example starts the client installed in a Linux or macOS environment in a directory named `/Users/user1` with a Snowflake user named `user1` and password `1234567a` for the `xy12345`
account:

> Copy code
>
> ```
> $ cd /Users/user1/client
> $ ./sfsql -u user1 -c 1234567a
>
> using GNU readline (Brian Fox, Chet Ramey), Java wrapper by Bernhard Bablok
> henplus config at /Users/ybrenman/.henplus
> ----------------------------------------------------------------------------
>  HenPlus II 0.9.8 "Yay Labor Day"
>  Copyright(C) 1997..2009 Henner Zeller <H.Zeller@acm.org>
>  HenPlus is provided AS IS and comes with ABSOLUTELY NO WARRANTY
>  This is free software, and you are welcome to redistribute it under the
>  conditions of the GNU Public License <http://www.gnu.org/licenses/gpl2.txt>
> ----------------------------------------------------------------------------
> HenPlus II connecting
>  url 'jdbc:snowflake://xy12345.snowflakecomputing.com:443/?account=xy12345&user=user1&ssl=on'
>  driver version 2.3
>  Snowflake - 1.0 (driver change version: 2.3.1, latest change version: 2.4.38)
> no transactions.
>  No Transaction *
>
> user1@snowflake:xy12345.snowflakecomputing.com>
> ```

## Closing a Session and Exiting the Client

To close the current Snowflake session and exit `sfsql`, type `exit` or `quit` on the command line.

When you close a Snowflake session:

- All in-process queries and DDL/DML statements are canceled.
- All temporary tables created during the session are dropped.

Note

Typing **[CTRL]-d** exits `sfsql`, but does not close the HenPlus shell. You must then type `exit` or `quit` (or type **[CTRL]-d** again) to close the HenPlus shell.
