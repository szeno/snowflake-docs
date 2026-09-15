# Prerequisites for Snowflake Connector for MySQL datasources

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

Before installing the Snowflake Connector for MySQL, do the following in your MySQL environment:

- [Configure associated datasource](#configure-associated-datasource)
- [Create required user](#create-required-user)

## Configure associated datasource

- Ensure that you have a MySQL version 8 or higher server that includes data you want to synchronize with Snowflake.
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

## Create required user

Create a user for the Snowflake Connector for MySQL with the following permissions:

> - `REPLICATION SLAVE` and `REPLICATION CLIENT` to be able to read from `binlog`.
>
>   For example:
>
>   Copy code
>
>   ```
>   GRANT REPLICATION SLAVE ON *.* TO '<username>'@'%'
>   GRANT REPLICATION CLIENT ON *.* TO '<username>'@'%'
>   ```
> - `SELECT` permission to all tables that are replicated.
>
>   For example:
>
>   Copy code
>
>   ```
>   GRANT SELECT ON <schema>.* TO '<username>'@'%'
>   GRANT SELECT ON <schema>.<table> TO '<username>'@'%'
>   ```
>
>   Where `<schema>.<table>` is the unique identifier of a table to be replicated.

## Next steps

After completing these procedures, follow the steps in [Setting up the Snowflake Connector for MySQL using Snowsight](/connectors/mysql6/install-snowsight).
