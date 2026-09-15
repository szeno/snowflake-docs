# DBCPConnectionPool

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Provides Database Connection Pooling Service. Connections can be asked from pool and returned after usage.

## Tags

connection, database, dbcp, jdbc, pooling, store

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Database Connection URL \* | Database Connection URL |  |  | A database connection URL used to connect to a database. May contain database system name, host, port, database name and some parameters. The exact syntax of a database connection URL is specified by your DBMS. |
| Database Driver Class Name \* | Database Driver Class Name |  |  | Database driver class name |
| Database Driver Location(s) | Database Driver Location(s) |  |  | Comma-separated list of files/folders and/or URLs containing the driver JAR and its dependencies (if any). For example ‘/var/tmp/mariadb-java-client-1.1.7.jar’ |
| Database User | Database User |  |  | Database user name |
| Kerberos User Service | Kerberos User Service |  |  | Specifies the Kerberos User Controller Service that should be used for authenticating with Kerberos |
| Max Total Connections \* | Max Total Connections | 8 |  | The maximum number of active connections that can be allocated from this pool at the same time, or negative for no limit. |
| Max Wait Time \* | Max Wait Time | 500 millis |  | The maximum amount of time that the pool will wait (when there are no available connections) for a connection to be returned before failing, or -1 to wait indefinitely. |
| Maximum Connection Lifetime | Maximum Connection Lifetime | -1 |  | The maximum lifetime of a connection. After this time is exceeded the connection will fail the next activation, passivation or validation test. A value of zero or less means the connection has an infinite lifetime. |
| Maximum Idle Connections | Maximum Idle Connections | 8 |  | The maximum number of connections that can remain idle in the pool without extra ones being released. Set to any negative value to allow unlimited idle connections. |
| Minimum Evictable Idle Time | Minimum Evictable Idle Time | 30 mins |  | The minimum amount of time a connection may sit idle in the pool before it is eligible for eviction. |
| Minimum Idle Connections | Minimum Idle Connections | 0 |  | The minimum number of connections that can remain idle in the pool without extra ones being created. Set to or zero to allow no idle connections. |
| Password | Password |  |  | The password for the database user |
| Soft Minimum Evictable Idle Time | Soft Minimum Evictable Idle Time | -1 |  | The minimum amount of time a connection may sit idle in the pool before it is eligible for eviction by the idle connection evictor, with the extra condition that at least a minimum number of idle connections remain in the pool. When the not-soft version of this option is set to a positive value, it is examined first by the idle connection evictor: when idle connections are visited by the evictor, idle time is first compared against it (without considering the number of idle connections in the pool) and then against this soft option, including the minimum idle connections constraint. |
| Time Between Eviction Runs | Time Between Eviction Runs | -1 |  | The time period to sleep between runs of the idle connection evictor thread. When non-positive, no idle connection evictor thread will be run. |
| Validation Query | Validation Query |  |  | Validation query used to validate connections before returning them. When connection is invalid, it gets dropped and new valid connection will be returned. Note!! Using validation might have some performance penalty. |

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
