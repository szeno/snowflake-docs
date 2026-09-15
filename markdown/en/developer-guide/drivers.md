# Drivers

[Preview Feature](/release-notes/preview-features) — drivers built on the Universal Core

New major versions of two Snowflake drivers are in public preview: [Snowflake ODBC Driver 4.x](/developer-guide/odbc/odbc-universal-core) and [Snowflake Connector for Python 5.x](/developer-guide/python-connector/python-connector-universal-core). Both are built on the Universal Core, a shared Rust library used by every new Snowflake driver. The generally available drivers documented in this section remain the default.

See [Universal Core](/developer-guide/universal-core/universal-core).

Using languages such as Go, C#, JavaScript, and Python, you can write applications that perform operations on Snowflake. Use the drivers described in
this section to access Snowflake from applications written in the driver’s supported language.

[Go Snowflake Driver](/developer-guide/golang/go-driver)
:   Connect to Snowflake and perform all standard operations with an interface for developing applications using the Go programming language.

[JDBC Driver](/developer-guide/jdbc/jdbc)
:   Connect to Snowflake from most client tools/applications that support JDBC.

[.NET Driver](/developer-guide/dotnet/dotnet-driver)
:   Connect to Snowflake with an interface to the Microsoft .NET open source software framework for developing applications.

[Node.js Driver](/developer-guide/node-js/nodejs-driver)
:   Connect to Snowflake with a native asynchronous Node.js interface.

[ODBC Driver](/developer-guide/odbc/odbc)
:   Connect to Snowflake using ODBC-based client applications.

[PHP PDO Driver for Snowflake](/developer-guide/php-pdo/php-pdo-driver)
:   Connect to Snowflake and perform all standard operations with an interface for developing PHP applications.

[Snowflake Connector for Python](/developer-guide/python-connector/python-connector)
:   Develop Python applications that can connect to Snowflake and perform all standard operations.

## Transport Layer Security (TLS) support

All Snowflake drivers support TLS to secure communications between the client and the Snowflake service. TLS 1.3 or later is supported for all drivers, except as noted in the following table.

**Snowflake Driver TLS Support**

| Driver | TLS 1.2 | TLS 1.3 | Notes |
| --- | --- | --- | --- |
| Go Snowflake Driver | ✔ | ✔ |  |
| JDBC Driver | ✔ | ✔ |  |
| .NET Driver | ✔ |  | - MacOS currently does not support TLS 1.3, but will once .NET 10 is released. - Windows supports TLS 1.3 for .NET 3.0 and .NET Framework 4.8 and later versions. |
| Node.js Driver | ✔ | ✔ |  |
| ODBC Driver | ✔ | ✔ |  |
| PHP PDO Driver for Snowflake | ✔ | ✔ |  |
| Snowflake Connector for Python | ✔ | ✔ |  |

Expand

Show lessSee more
