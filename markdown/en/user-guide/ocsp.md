# OCSP Configuration

This topic provides an overview of OCSP, its use in Snowflake, and information to help diagnose OCSP issues.

## Overview

Snowflake uses Online Certificate Status Protocol (OCSP) to provide maximum security to determine whether a certificate is revoked when Snowflake clients attempt to connect to an endpoint through HTTPS.

Snowflake uses OCSP to evaluate each certificate in the chain of trust up to the intermediate certificate the root certificate authority (CA) issues. Ensuring that each certificate is not revoked helps Snowflake to establish secure connections with trusted actors during the identity verification process.

Depending on your client or driver version and the configuration described on this page, it is possible to turn off OCSP and to adjust the action that occurs when OCSP determines a certificate is revoked.

## Fail-Open or Fail-Close behavior

Currently, users can choose between either of two behaviors in terms of how Snowflake clients or drivers respond during an OCSP event.

1. Fail-open
2. Fail-close

### Fail-Open

Snowflake supports a fail-open approach by default in terms of evaluating the OCSP CA response. The fail-open approach has the following characteristics:

> - A response indicating a revoked certificate results in a failed connection.
> - A response with any other certificate errors or statuses allows the connection to occur, but denotes the message in the logs at the `WARNING` level with the relevant details in JSON format.

Users can monitor the logs for the specific driver or connector to determine the frequency of fail-open log events.

These event logs can be combined with the [Snowflake Status Page](https://status.snowflake.com) to determine the best course of action, such as temporarily restricting client access or pivoting to fail-close behavior.

Currently, the fail-open default approach applies to the following client and driver versions.

| Client / Driver | Version |
| --- | --- |
| SnowSQL | v1.1.79 or later |
| Python Connector | v1.8.0 or later |
| JDBC Driver | v3.8.0 or later |
| ODBC Driver | v2.19.0 or later |
| SQL Alchemy | Upgrade Python Connector to v1.8.0 or later |
| Spark | v2.4.14 or later if using Maven or SBT to build the Spark application.   JDBC v3.8.0 or later if attaching JAR files to Spark cluster.   Request Databricks to upgrade their Spark connector if using the Databricks built-in Spark connector. |
| Go Driver | v1.2.0 or later |
| Node.js | v1.2.0 or later |

Expand

Show lessSee more

Note

Snowflake does not support OCSP checking for the .NET driver. Instead, .NET uses its own framework to check the validity of the HTTPS certificate.

### Fail-Close

The fail-close behavior is more restrictive to interpreting the OCSP CA response. If the client or driver does not receive a valid OCSP CA response *for any reason*, the connection fails.

Since this behavior is not default based on the versions listed in the fail-open section, fail-close must be configured manually within each driver or connector.

To preserve the fail-close behavior, set the corresponding `ocsp_fail_open` parameter to `false`.

| Client / Driver | Setting |
| --- | --- |
| SnowSQL | `snowsql -o ocsp_fail_open=false` |
| Python Connector | For details, see [Choosing fail-open or fail-close mode](/developer-guide/python-connector/python-connector-connect#label-python-ocsp-choosing-fail-open-or-fail-close-mode) in the Python Connector documentation. |
| JDBC Driver | For details, see [Choosing fail-open or fail-close mode](/developer-guide/jdbc/jdbc-configure#label-jdbc-ocsp-choosing-fail-open-or-fail-close-mode) in the JDBC Driver documentation. |
| ODBC Driver | Choose one of the following:   Set the connection parameter to `OCSP_FAIL_OPEN=false`   Use the environment variable $SIMBAINI to locate the corresponding file. Then set `OCSPFailOpen=false` |
| SQL Alchemy | See JDBC Driver settings |
| Spark | The Spark Connector does not have an `ocsp_fail_open` parameter.   Fail-close can only be preserved with Spark if using the JDBC driver. |
| Go Driver | Do either of the following:   - Set the connection parameter `OCSPFailOpen` in Config to `ocspFailOpenTrue` or `ocspFailOpenFalse`, for example:   `import ( ... sf "github.com/snowflakedb/gosnowflake ... ")`   `config: &Config{ Account: "xy12345", ..., OCSPFailOpen: sf.ocspFailOpenFalse, ... }`   - Set the `ocspFailOpen` connection parameter in the connect string to `true` or `false`, for example,   `user:pass@account/db/s?ocspFailOpen=false`.   Note the differences in case (uppercase / lowercase).   For more information on Go connection parameters, see the GoDoc [gosnowflake documentation](https://godoc.org/github.com/snowflakedb/gosnowflake). |
| Node.js | Set the global parameter `ocspFailOpen=false`. For details, see [Node.js options reference](/developer-guide/node-js/nodejs-driver-options). |

Expand

Show lessSee more

### Legacy client and driver versions

If your client or driver version is older than that listed in the fail-open section, the fail-open behavior is not an option. Therefore, the fail-close behavior is default.

Snowflake deployments using legacy client and driver versions with respect to OCSP have three options:

1. Upgrade their client or driver to its latest version (best option).
2. Continue using the fail-close behavior.
3. Turn off OCSP monitoring as described in this [Knowledge Base article](https://community.snowflake.com/s/article/How-to-turn-off-OCSP-checking-in-Snowflake-client-drivers) (in the Snowflake Community).

### Best practices

To mitigate risk, Snowflake recommends the following best practices to keep communications secure.

1. Use private connectivity to the Snowflake service and block public access to Snowflake.
2. Allow client drivers to run on managed desktops and servers only.
3. Send client driver logs to a management system or upload to Snowflake. Monitor the connections made without OCSP checking.

Note

Support for private connectivity to the Snowflake service requires [Business Critical](/user-guide/intro-editions) (or higher).
To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

## CA site and OCSP responder hosts used by Snowflake

You can call the [SYSTEM$ALLOWLIST](/sql-reference/functions/system_allowlist) or [SYSTEM$ALLOWLIST\_PRIVATELINK](/sql-reference/functions/system_allowlist_privatelink) function
in your Snowflake account to get the hosts Snowflake uses for OCSP verification checks. The host values are unique to the cloud platform
and region where your Snowflake account exists. The reasons for the different host values are based on the CA that the cloud platform uses
and when the certificates are updated or renewed.

For example:

Copy code

```
SELECT t.VALUE:type::VARCHAR as type,
  t.VALUE:host::VARCHAR as host,
  t.VALUE:port as port
FROM TABLE(FLATTEN(input => PARSE_JSON(SYSTEM$ALLOWLIST_PRIVATELINK()))) AS t
WHERE type ILIKE ANY ('OCSP%');
```

```
+-----------------------+---------------------------------------------------------------+------+
| TYPE                  | HOST                                                          | PORT |
|-----------------------+---------------------------------------------------------------+------|
| OCSP_CACHE            | ocsp.account1234.us-west-2.privatelink.snowflakecomputing.com | 80   |
| OCSP_CACHE_REGIONLESS | ocsp.my_org-my_account.privatelink.snowflakecomputing.com     | 80   |
+-----------------------+---------------------------------------------------------------+------+
```

## OCSP certification checks require Port 80

All communication with Snowflake happens using port 443. However, OCSP certification checks are transmitted over port 80. If your workstation is behind a firewall, make sure that
the network administrator for your organization has opened the firewall to traffic on ports 443 and 80.
