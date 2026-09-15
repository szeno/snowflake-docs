# Client versions & support policy

[Preview Feature](/release-notes/preview-features) — drivers built on the Universal Core

Snowflake ODBC Driver 4.x and Snowflake Connector for Python 5.x are in public preview. Preview versions are not listed on this page and are not covered by the support policy described here. The recommended and minimum supported versions below refer to the generally available drivers.

See [Universal Core](/developer-guide/universal-core/universal-core).

Snowflake provides a CLI (command-line interface) as well as other client software (drivers, connectors, etc.) for connecting to Snowflake and using certain
Snowflake features (e.g. Apache Kafka for loading data, Apache Hive metadata for external tables). The clients must be installed on each local workstation or system from which
you wish to connect.

As needed, we release new versions of the clients to fix bugs, and introduce enhancements and new features. New versions are backward-compatible with existing Snowflake
features, but we do not guarantee that earlier versions are forward-compatible. As such, we recommend actively monitoring and maintaining the versions of your installed
clients; if they are not in-sync with the current version of Snowflake, you may encounter issues when connecting to and using Snowflake.

Attention

For critical or important client changes (especially required security updates), Snowflake might require you to upgrade to the latest version. Please make sure to always check the [Release Notes](/release-notes/clients-drivers/monthly-releases) for the client drivers you’re using to see if there’s an important security fix in a particular version, and plan your driver upgrades accordingly.

For more information about determining the current version of a client or driver, refer to the following:

- [View the Snowflake client version](/user-guide/snowflake-client-version-check)
- [How to report on the Clients connecting to a Snowflake account?](https://community.snowflake.com/s/article/how-to-report-on-the-clients-connecting-to-a-snowflake-account)

All downloads on this page are considered “Client Software” as defined in your agreement for use of the Snowflake Service.

Attention

Customers who use GCP (Google Cloud Platform) for authentication must update their clients and drivers to new
minimum versions due to upcoming changes by Google for signing request headers and payloads.
Snowflake recommends affected customers read the
[FAQ: 2023 Client Driver deprecation for GCP customers](https://community.snowflake.com/s/article/faq-2023-client-driver-deprecation-for-GCP-customers) knowledge
base article for more information.

## Recommended client versions

As a policy, Snowflake recommends that you always install the latest (i.e. most recent) version of each client,
if possible.

Snowflake uses semantic versioning for client and driver updates, excluding Snowpark APIs.

Note

Snowflake’s support policy generally provides a minimum two-year window for clients and drivers, after which support might be dropped.
To help you track supported versions, the following table includes the minimum version of clients and drivers Snowflake currently
supports. If you use a version older than the minimum, Snowflake makes no commitment to provide support.

Once a client is installed, you are not required to upgrade each time a new version is released; however, to stay current with the
latest fixes, updates, and features, we recommend monitoring for new versions and upgrading at regular intervals (e.g. monthly,
quarterly, semiannually).

| Type | Client | Recommended Version | Minimum Supported Version (as of Feb 01, 2026) [[1]](#footnote-1) [[2]](#footnote-2) | Release Information | Where to Download the Installers [[3]](#footnote-3) |
| --- | --- | --- | --- | --- | --- |
| CLI (Command-line Interface) | [Snowflake CLI](/developer-guide/snowflake-cli/index) | 3.18.0 (or later) | 2.4.0 | [Release Notes](/release-notes/clients-drivers/snowflake-cli) | [Snowflake CLI Download](https://sfc-repo.snowflakecomputing.com/snowflake-cli/index.html) page |
|  | [SnowSQL](/user-guide/snowsql) | 1.5.0 (or later) | 1.4.0 | [Release Notes](/release-notes/clients-drivers/snowsql) | [SnowSQL Download](https://developers.snowflake.com/snowsql/) page |
| Connectors and Drivers | [.NET Driver](/developer-guide/dotnet/dotnet-driver) | 6.1.0 (or later) | 2.2.0 | [Release Notes](/release-notes/clients-drivers/dotnet) | [Drivers and Libraries](https://developers.snowflake.com/drivers-and-libraries/) page |
|  | [Go Snowflake Driver](/developer-guide/golang/go-driver) | 2.2.0 (or later) | 1.7.2 | [Release Notes](/release-notes/clients-drivers/golang) | [Drivers and Libraries](https://developers.snowflake.com/drivers-and-libraries/) page |
|  | [Ingest Java SDK](/user-guide/snowpipe-streaming/snowpipe-streaming-classic-overview) | 4.4.2 (or later) | 2.2.0 | [Release Notes](/release-notes/clients-drivers/ingest-java-sdk) | [Drivers and Libraries](https://developers.snowflake.com/drivers-and-libraries/) page |
|  | Ingest Python SDK | 1.0.10 (or later) | 1.0.5 | [Release Notes](https://github.com/snowflakedb/snowflake-ingest-python/releases) (in GitHub) | [Drivers and Libraries](https://developers.snowflake.com/drivers-and-libraries/) page |
|  | [Snowpipe Streaming SDK (for high-performance architecture)](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-overview) | 1.2.0 (or later) | 1.0.0 | [Release Notes](/release-notes/clients-drivers/snowpipe-streaming-sdk) | [Java SDK](https://central.sonatype.com/artifact/com.snowflake/snowpipe-streaming) | [Python SDK](https://pypi.org/project/snowpipe-streaming/) |
|  | [JDBC Driver](/developer-guide/jdbc/jdbc) | 4.3.3 (or later) | 3.14.5 | [Release Notes](/release-notes/clients-drivers/jdbc) | [Drivers and Libraries](https://developers.snowflake.com/drivers-and-libraries/) page |
|  | [Node.js Driver](/developer-guide/node-js/nodejs-driver) | 3.3.0 (or later) | 1.9.3 | [Release Notes](/release-notes/clients-drivers/nodejs) | [Drivers and Libraries](https://developers.snowflake.com/drivers-and-libraries/) page [3] |
|  | [ODBC Driver](/developer-guide/odbc/odbc) | 3.21.0 (or later) | 3.2.0 | [Release Notes](/release-notes/clients-drivers/odbc) | [ODBC Download](https://developers.snowflake.com/odbc/) page |
|  | [PHP PDO Driver](/developer-guide/php-pdo/php-pdo-driver) | 4.2.0 (or later) | 2.0.1 | [Release Notes](/release-notes/clients-drivers/php-pdo) | [Drivers and Libraries](https://developers.snowflake.com/drivers-and-libraries/) page |
|  | [Snowflake Connector for Kafka](/user-guide/kafka-connector/index) | 3.3.0 (or later) | 2.1.2 | [Release Notes](/release-notes/clients-drivers/kafka-connector) | [Drivers and Libraries](https://developers.snowflake.com/drivers-and-libraries/) page |
|  | [Snowflake Connector for Python](/developer-guide/python-connector/python-connector) | 4.7.3 (or later) | 3.7.0 | [Release Notes](/release-notes/clients-drivers/python-connector) | [Drivers and Libraries](https://developers.snowflake.com/drivers-and-libraries/) page [3] |
|  | [Snowflake Connector for Spark](/user-guide/spark-connector) | 3.2.2 (or later) | 2.14.0 | [Release Notes](/release-notes/clients-drivers/spark-connector) | [Drivers and Libraries](https://developers.snowflake.com/drivers-and-libraries/) page |
|  | [Snowflake SQLAlchemy (for Python)](/developer-guide/python-connector/sqlalchemy) | 1.9.0 (or later) | 1.5.1 | [Release Notes](/release-notes/clients-drivers/sqlalchemy) | [Drivers and Libraries](https://developers.snowflake.com/drivers-and-libraries/) page [3] |
| Snowpark | [Snowpark Library for Java](/developer-guide/snowpark/java/index) | 1.18.0 (or later) | 1.8.0 | [Release Notes](/release-notes/clients-drivers/snowpark-scala-java) | [Drivers and Libraries](https://developers.snowflake.com/drivers-and-libraries/) page |
|  | [Snowpark Library for Python](/developer-guide/snowpark/python/index) | 1.44.0 (or later) | 1.0.0 | [Release Notes](/release-notes/clients-drivers/snowpark-python) | [Drivers and Libraries](https://developers.snowflake.com/drivers-and-libraries/) page [3] |
|  | [Snowpark Library for Scala](/developer-guide/snowpark/scala/index) | 1.18.0 (or later) | 1.8.0 | [Release Notes](/release-notes/clients-drivers/snowpark-scala-java) | [Drivers and Libraries](https://developers.snowflake.com/drivers-and-libraries/) page |
|  | [Snowpark Connect for Spark](/developer-guide/snowpark-connect/snowpark-connect-apache-spark) | 1.17.0 (or later) | 0.25.0 | [Release Notes](/release-notes/clients-drivers/snowpark-connect) | [Drivers and Libraries](https://developers.snowflake.com/drivers-and-libraries/) page |
|  | [Snowpark ML](/developer-guide/snowflake-ml/overview) | 1.27.0 (or later) | 0.3.0 | [Release Notes](/release-notes/clients-drivers/snowpark-ml) | [Drivers and Libraries](https://developers.snowflake.com/drivers-and-libraries/) page [3] |
| Other | [Snowflake Metadata Connector for Hive](/user-guide/tables-external-hive) | Latest | None (preview) | [Release Notes](https://github.com/snowflakedb/snowflake-hive-metastore-connector/releases) (in GitHub) | See [Integrate Apache Hive metastores with Snowflake](/user-guide/tables-external-hive). |

Expand

Show lessSee more

[1]
Minimum versions include updates that enable environment resilience to OCSP-related connectivity issues.

[2]
Minimum versions are not intended for installation.

[3]
Digitally signed to ensure the downloadable image is authentic.

Tip

You can also use the [SYSTEM$CLIENT\_VERSION\_INFO](/sql-reference/functions/system_client_version_info) system function to retrieve this information programmatically.

## Minimum client versions

The minimum version for a client identifies the earliest supported version of the client. Any client versions lower than the documented minimum are no longer
covered by our support policy (see below) and may encounter issues when connecting to Snowflake.

Attention

As stated in the [Client Support Policy](#label-client-support-policy), Snowflake fixes issues on the latest client versions only.
As such, the minimum versions might contain issues that have
been fixed in later versions. Therefore, you should not install the minimum versions.

The versions documented in the table above serve only as guidelines for managing your installed clients relative to
the support policy.

## Client support policy

Snowflake maintains the following support policy for all clients provided by Snowflake:

- For all clients listed on this page, Snowflake generally supports each client version for at least two years, except in cases where a more recent version introduces
  critical fixes (e.g. for security or performance issues).

  Client versions that are below the minimum supported version might be blocked from connecting to Snowflake. Note that Snowflake
  will provide advance notification before blocking access for a particular client version.
- Unsupported versions might be removed from distribution (i.e. they may no longer be available for download/install).
- Snowflake provides bug fixes, new features, and required security updates only on the latest client versions. Likewise, when troubleshooting client issues,
  Snowflake verifies only against the latest client versions only.
- Snowflake ensures backward compatibility for APIs across all supported client versions.

Note

This policy does not cover client connectors provided by third-party partners (Informatica, Tableau, etc.); please
consult directly with the partners providing the
connectors for information about their support policies.

For more details about Snowflake’s third-party partners, see [Snowflake Ecosystem](/user-guide/ecosystem).

## Operating system support

The latest versions of most Snowflake clients are supported on the following operating systems:

| Operating System | Supported Versions |
| --- | --- |
| AIX | AIX 7.2 (JDBC only) |
| Linux | CentOS 8 |
|  | Red Hat Enterprise Linux (RHEL) 7, 8, and, for selected clients, version 9 |
|  | Ubuntu 18.04 or later |
| macOS | 14 or later |
| Microsoft Windows | Microsoft Windows 8 or later |
|  | Microsoft Windows Server 2012, 2016, 2019, 2022 |

Expand

Show lessSee more

Note

The supported version numbers change over time, based largely on the evolving support policies of the
operating system vendors.

The following table shows which clients are available on which operating systems:

|  | Linux | macOS | Microsoft Windows | Notes |
| --- | --- | --- | --- | --- |
| .NET Driver | ✔ | ✔ | ✔ | Red Hat Enterprise Linux (RHEL) 9 is supported starting with version 5.4.0. |
| Go Snowflake Driver | ✔ | ✔ | ✔ | Red Hat Enterprise Linux (RHEL) 9 is supported starting with version 1.17.1. |
| Ingest Java SDK | ✔ | ✔ | ✔ |  |
| Ingest Python SDK | ✔ | ✔ | ✔ |  |
| Snowpipe Streaming SDK (for high-performance architecture) | ✔ | ✔ | ✔ | Supported architectures: ARM64 Mac, Windows, ARM64-Linux, and x86\_64-Linux. Linux requires glibc version 2.26 or later. |
| Node.js Driver | ✔ | ✔ | ✔ | Red Hat Enterprise Linux (RHEL) 9 is supported starting with version 2.3.2. |
| JDBC Driver | ✔ | ✔ | ✔ | Red Hat Enterprise Linux (RHEL) 9 is supported starting with version 3.27.1. |
| ODBC Driver | ✔ | ✔ | ✔ | Linux support is based on the architecture, as follows:   - x86:    - Red Hat Enterprise Linux (RHEL) 8 and 9 (starting with version 3.14.0). Note that ODBC v3.15.0 and later do not support RHEL 7 or earlier versions.   - Ubuntu versions 20.04 or later - ARM64 (aarch64)    - Red Hat Enterprise Linux (RHEL) 8, and 9 (starting with version 3.14.0)   - CentOS 8   - Ubuntu 20.04   ODBC does not support ARM64 architectures for Windows.  For Linux, ODBC v3.15.0 and later requires glibc 2.28+ and is incompatible with an OS that has an earlier version of glibc, such as Ubuntu 18.04 and earlier, RHEL 7 and earlier. Before upgrading to ODBC driver v3.15.0 or later, consult your operating system documentation to confirm it supports glibc version 2.28 or later. |
| PHP PDO Driver | ✔ | ✔ | ✔ | Red Hat Enterprise Linux (RHEL) 9 is supported starting with version 3.5.0. |
| Snowflake Connector for Kafka | ✔ | ✔ | ✔ |  |
| Snowflake Connector for Python | ✔ | ✔ | ✔ | Red Hat Enterprise Linux (RHEL) 9 is supported starting with version 4.0.0. |
| Snowflake Connector for Spark | ✔ | ✔ | ✔ |  |
| Snowflake Library for Java | ✔ | ✔ | ✔ |  |
| Snowflake Library for Python | ✔ | ✔ | ✔ |  |
| Snowflake Library for Scala | ✔ | ✔ | ✔ |  |
| Snowflake ML | ✔ | ✔ | ✔ |  |
| Snowflake CLI | ✔ | ✔ | ✔ | Red Hat Enterprise Linux (RHEL) 9 is supported starting with version 3.17.0. |
| SnowSQL | ✔ | ✔ | ✔ | Versions 1.3.3 and later require at least glibc version 2.25 on Linux, which might not be available on older operating systems, such as RHEL7. Consult your operating system documentation to confirm it supports glibc version 2.25 or later. Red Hat Enterprise Linux (RHEL) 9 is supported starting with version 1.5.0. |

Expand

Show lessSee more

## Operating system support policy

Snowflake typically obsoletes support for an operating system version in accordance with the support timeline stated
by the operating system vendor.

Snowflake typically provides three months’ notice before dropping support for a particular version of an operating system.
