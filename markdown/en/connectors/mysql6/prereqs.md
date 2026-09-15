# Prerequisites for Snowflake Connector for MySQL

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts except government regions.

Important

Thank you for your interest in the Snowflake Connector for MySQL.
We’re now focused on a next-generation solution that will offer a significantly
improved experience; therefore, moving this connector to the general availability
status is currently not on our product roadmap.
You may continue to use this connector as preview feature, but please note that support for future bug
fixes and improvements are not guaranteed. The new solution is available as [Openflow Connector for MySQL](/user-guide/data-integration/openflow/connectors/mysql/about) and
includes better performance, customizability, and enhanced deployment options.

Before installing the Snowflake Connector for MySQL, you must ensure that the following prerequisites are met in your
MySQL and Snowflake environments.

## Setting up the prerequisites for MySQL

Before installing the Openflow Connector for MySQL, do the following in your MySQL environment:

- Ensure that you have a MySQL 8 server that includes data you want to synchronize with Snowflake.
- Set the following options for your MySQL server:

  Copy code

  ```
  log_bin = on
  binlog_format = row
  binlog_row_metadata = full
  binlog_row_image = full
  binlog_row_value_options =
  ```

  Note

  Be cautious about the binary log expiration period (`binlog_expire_logs_seconds`). After it ends, binary log
  files might be automatically removed. If the agent is paused for a long period of time (for example due to
  maintenance work) and the expired binary log files are deleted during this time, the agent is not able to
  replicate the data from these files. Set the binary log expiration period to at least a few hours to ensure stable
  work of the connector.

  For more information about the automatic purging of binary log files, see
  [MySQL Reference Manual](https://dev.mysql.com/doc/refman/8.0/en/replication-options-binary-log.html).

## Setting up the prerequisites for running the agent

Before installing the connector, you must set up the environment where the agent runs.

### Configuring your firewall to access to Snowflake

If you are using a firewall, add the Snowflake hostnames and port numbers to the allowed list.
For more information, see [Allowing Host names](/user-guide/hostname-allowlist).

After adding the hostnames and port numbers to the allowed list, use
[SnowCD](/user-guide/snowcd) to verify the Snowflake connection from the host where
you run the agent.

### Installing an orchestration tool

The agent is distributed as a Docker image that you can run using orchestration tools and services like Docker,
Kubernetes, or OpenShift.

To run the agent, you must have one of these tools installed. Your environment must have:

- At least 6 GB of RAM available to the container running the agent. The agent is a memory-intensive application.
- 4 CPUs available to handle the throughput requirements of the agent. Decreasing the number of CPUs decreases the
  throughput linearly. Having additional CPUs does not provide significant gains.

The Snowflake Connector for MySQL requires exactly one instance of the agent application to be running at all times.

## Next steps

After completing these procedures, follow the steps in [Prerequisites for Snowflake Connector for MySQL datasources](/connectors/mysql6/prereqs-datasource).
