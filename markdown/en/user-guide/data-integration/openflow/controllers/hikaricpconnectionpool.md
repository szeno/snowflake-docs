# HikariCPConnectionPool

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Provides Database Connection Pooling Service based on HikariCP. Connections can be asked from pool and returned after usage.

## Tags

connection, database, dbcp, hikari, jdbc, pooling, store

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Database Connection URL \* | hikaricp-connection-url |  |  | A database connection URL used to connect to a database. May contain database system name, host, port, database name and some parameters. The exact syntax of a database connection URL is specified by your DBMS. |
| Database Driver Class Name \* | hikaricp-driver-classname |  |  | The fully-qualified class name of the JDBC driver. Example: com.mysql.jdbc.Driver |
| Database Driver Location(s) | hikaricp-driver-locations |  |  | Comma-separated list of files/folders and/or URLs containing the driver JAR and its dependencies (if any). For example ‘/var/tmp/mariadb-java-client-1.1.7.jar’ |
| Kerberos User Service | hikaricp-kerberos-user-service |  |  | Specifies the Kerberos User Controller Service that should be used for authenticating with Kerberos |
| Max Connection Lifetime | hikaricp-max-conn-lifetime | -1 |  | The maximum lifetime of a connection. After this time is exceeded the connection will fail the next activation, passivation or validation test. A value of zero or less means the connection has an infinite lifetime. |
| Max Total Connections \* | hikaricp-max-total-conns | 10 |  | This property controls the maximum size that the pool is allowed to reach, including both idle and in-use connections. Basically this value will determine the maximum number of actual connections to the database backend. A reasonable value for this is best determined by your execution environment. When the pool reaches this size, and no idle connections are available, the service will block for up to connectionTimeout milliseconds before timing out. |
| Max Wait Time \* | hikaricp-max-wait-time | 500 millis |  | The maximum amount of time that the pool will wait (when there are no available connections) for a connection to be returned before failing, or 0 <time units> to wait indefinitely. |
| Minimum Idle Connections \* | hikaricp-min-idle-conns | 10 |  | This property controls the minimum number of idle connections that HikariCP tries to maintain in the pool. If the idle connections dip below this value and total connections in the pool are less than ‘Max Total Connections’, HikariCP will make a best effort to add additional connections quickly and efficiently. It is recommended that this property to be set equal to ‘Max Total Connections’. |
| Password | hikaricp-password |  |  | The password for the database user |
| Database User | hikaricp-username |  |  | Database user name |
| Validation Query | hikaricp-validation-query |  |  | Validation Query used to validate connections before returning them. When connection is invalid, it gets dropped and new valid connection will be returned. NOTE: Using validation might have some performance penalty. |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

## Restrictions

| Required Permission | Explanation |
| --- | --- |
| reference remote resources | Database Driver Location can reference resources over HTTP |

Expand

Show lessSee more

## System Resource Considerations

This component does not specify system resource considerations.
