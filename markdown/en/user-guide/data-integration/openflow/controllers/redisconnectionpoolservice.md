# RedisConnectionPoolService

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

A service that provides connections to Redis.

## Tags

cache, redis

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Cluster Max Redirects \* | Cluster Max Redirects | 5 |  | The maximum number of redirects that can be performed when clustered. |
| Communication Timeout \* | Communication Timeout | 10 seconds |  | The timeout to use when attempting to communicate with Redis. |
| Connection String \* | Connection String |  |  | The connection string for Redis. In a standalone instance this value will be of the form hostname:port. In a sentinel instance this value will be the comma-separated list of sentinels, such as host1:port1,host2:port2,host3:port3. In a clustered instance this value will be the comma-separated list of cluster masters, such as host1:port,host2:port,host3:port. |
| Database Index \* | Database Index | 0 |  | The database index to be used by connections created from this connection pool. See the databases property in redis.conf, by default databases 0-15 will be available. |
| Password | Password |  |  | The password used to authenticate to the Redis server. See the ‘requirepass’ property in redis.conf. |
| Pool - Block When Exhausted \* | Pool - Block When Exhausted | true | - true - false | Whether or not clients should block and wait when trying to obtain a connection from the pool when the pool has no available connections. Setting this to false means an error will occur immediately when a client requests a connection and none are available. |
| Pool - Max Idle \* | Pool - Max Idle | 8 |  | The maximum number of idle connections that can be held in the pool, or a negative value if there is no limit. |
| Pool - Max Total \* | Pool - Max Total | 8 |  | The maximum number of connections that can be allocated by the pool (checked out to clients, or idle awaiting checkout). A negative value indicates that there is no limit. |
| Pool - Max Wait Time \* | Pool - Max Wait Time | 10 seconds |  | The amount of time to wait for an available connection when Block When Exhausted is set to true. |
| Pool - Min Evictable Idle Time \* | Pool - Min Evictable Idle Time | 60 seconds |  | The minimum amount of time an object may sit idle in the pool before it is eligible for eviction. |
| Pool - Min Idle \* | Pool - Min Idle | 0 |  | The target for the minimum number of idle connections to maintain in the pool. If the configured value of Min Idle is greater than the configured value for Max Idle, then the value of Max Idle will be used instead. |
| Pool - Num Tests Per Eviction Run \* | Pool - Num Tests Per Eviction Run | -1 |  | The number of connections to tests per eviction attempt. A negative value indicates to test all connections. |
| Pool - Test On Borrow \* | Pool - Test On Borrow | false | - true - false | Whether or not connections should be tested upon borrowing from the pool. |
| Pool - Test On Create \* | Pool - Test On Create | false | - true - false | Whether or not connections should be tested upon creation. |
| Pool - Test On Return \* | Pool - Test On Return | false | - true - false | Whether or not connections should be tested upon returning to the pool. |
| Pool - Test While Idle \* | Pool - Test While Idle | true | - true - false | Whether or not connections should be tested while idle. |
| Pool - Time Between Eviction Runs \* | Pool - Time Between Eviction Runs | 30 seconds |  | The amount of time between attempting to evict idle connections from the pool. |
| Redis Mode \* | Redis Mode | Standalone | - Standalone - Sentinel - Cluster | The type of Redis being communicated with - standalone, sentinel, or clustered. |
| SSL Context Service | SSL Context Service |  |  | If specified, this service will be used to create an SSL Context that will be used to secure communications; if not specified, communications will not be secure |
| Sentinel Master | Sentinel Master |  |  | The name of the sentinel master, require when Mode is set to Sentinel |
| Sentinel Password | Sentinel Password |  |  | The password used to authenticate to the Redis Sentinel server. See the ‘requirepass’ and ‘sentinel sentinel-pass’ properties in sentinel.conf. |
| Sentinel Username | Sentinel Username |  |  | The username used to authenticate to the Redis sentinel server. |
| Username | Username |  |  | The username used to authenticate to the Redis server. |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
