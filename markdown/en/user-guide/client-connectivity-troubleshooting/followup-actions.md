# Follow-up actions

After completing the troubleshooting steps using the Snowflake tools mentioned in [Use Snowflake troubleshooting tools](/user-guide/client-connectivity-troubleshooting/snowflake-tools) or the platform specific instructions mentioned in [Follow alternative troubleshooting steps](/user-guide/client-connectivity-troubleshooting/alternate-steps), you should perform the following steps based on whether the connection test succeeds or fails.

## If the connection test succeeds

- Ensure the certificate issuer matches a trusted issuer, such as a cloud-based provider. A discrepancy might indicate an SSL inspection or an intermediary modifying the traffic, which Snowflake does not support.
- If the issuer does not match, contact your network team to address potential SSL inspection issues. Provide them with the output and request allowlisting of necessary URLs in the [Snowflake allowlist](/sql-reference/functions/system_allowlist).

## If the connection test fails

- If connectivity tests fail, Snowflake recommends working with your network team and asking them to double-check your network settings, firewall rules, and proxy configurations. Verify that you have followed Snowflake’s suggestions in the [Common connectivity issues and resolutions](/user-guide/client-connectivity-troubleshooting/common-issues) section.
- If the troubleshooting steps or your system or network do not resolve the issue, and your system or network administrators verified the respective proxies and appliances are configured correctly, open a case with Snowflake support. Provide all relevant details and test outputs to facilitate a quick resolution. Collaborate with your networking team to ensure all necessary URLs and ports are accessible as per Snowflake’s requirements.
- Please note that remediation of these issues in collaboration with [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support) requires the engagement of teams responsible for managing the client network and network security, as Snowflake personnel does not have the authority to make changes outside its own managed networks.
- Snowflake Support might instruct you to collect the Snowflake [driver and connector log files](#label-connectivity-driver-log-files) right after reproducing the issue and attach them to your Support ticket to Snowflake. You might also be instructed to collect the results of the [browser test](/user-guide/client-connectivity-troubleshooting/browser-test).

## Collect driver and connector log files

The following links explain how you can collect logs if requested by [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support):

- [.NET log files](https://github.com/snowflakedb/snowflake-connector-net?tab=readme-ov-file#logging)
- [Go log files](https://pkg.go.dev/github.com/snowflakedb/gosnowflake#hdr-Logging)
- [JDBC log files](/developer-guide/jdbc/jdbc-configure#label-configuring-jdbc-logging)
- [ODBC log files](/developer-guide/odbc/odbc-parameters#label-configuring-odbc-logging-config)
- [Node.js log files](/developer-guide/node-js/nodejs-driver-logs)
- [Snowflake Connector for Python log files](/developer-guide/python-connector/python-connector-example#label-python-easy-logging)
- [Snowflake CLI](/developer-guide/snowflake-cli/connecting/configure-cli#label-snowcli-configure-logging)
- [SnowSQL log files](/developer-guide/python-connector/python-connector-example#label-python-easy-logging)
