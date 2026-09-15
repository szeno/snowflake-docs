# Snowflake Postgres Connection Pooling

A connection pool is a cache of database connections that can be reused. When a request comes in from a client, an available connection
from the pool is given for that request or transaction.

In contrast, without any connection pooling, the client has to reach out to the database to establish a connection. Opening new connections
can impact availability and performance — in PostgreSQL, the server “forks” or creates a new process, and could use up available resources
as well as prevent new connections from being established. Connection pooling helps mitigate these issues and ensure that your applications
can scale.

## Do I need connection pooling?

Connection pooling is especially helpful when you have a high number of connections from your application, often in a client-side pool or via
multiple threads/processes from your web server.

You can run the following query on your Snowflake Postgres instance to determine if you would benefit from connection pooling:

Copy code

```
SELECT count(*),
       state
FROM pg_stat_activity
GROUP BY 2;
```

```
 count |             state
-------+-------------------------------
     7 | active
    69 | idle
    26 | idle in transaction
    11 | idle in transaction (aborted)
(4 rows)
```

If you see a high number of idle connections relative to active ones, then using connection pooling is strongly recommended.

## Connection Pooling with PgBouncer

Snowflake Postgres uses [pgBouncer](http://www.pgbouncer.org/) for connection pooling. PgBouncer is made available on all Snowflake
Postgres instances by default to ease connection management by multiplexing native Postgres connections across its own “virtual”
connections. By default, PgBouncer instances on Snowflake Postgres are run in transaction pooling mode.

However, in order to make use of the PgBouncer service, you must take one extra step on each database you want to use it on by installing
the `snowflake_pooler` extension.

### Activating PgBouncer with the `snowflake_pooler` extension

As the `snowflake_admin` Postgres user, run the following in the database to install the `snowflake_pooler` extension:

Copy code

```
CREATE EXTENSION snowflake_pooler;
```

### What is `snowflake_pooler`?

`snowflake_pooler` is a simple extension that creates a user called `snowflake_pooler`. This user has access to a single function
called `user_lookup` that allows PgBouncer to authenticate incoming connections. That way, when a client makes a connection to PgBouncer,
it can check whether the client’s credentials are valid by querying Postgres’s canonical user store.

Note

The `snowflake_pooler` extension must be installed individually in each database where you want to connect through PgBouncer. If
`snowflake_pooler` has not been installed, you may receive an error like:

```
failed: FATAL: bouncer config error
```

To resolve the error, connect to the database and run: `CREATE EXTENSION snowflake_pooler;`.

### Connecting to PgBouncer

Clients will connect to PgBouncer using the same connection string they’d use for the main Postgres database, except on port 5431 instead
of the usual 5432:

Copy code

```
psql postgres://my_application_user:my_application_password@p.43lmodgbqvdmlpbjirv22dfciu.db.postgresbridge.com:5431/mydb
```

Only roles *without* superuser or replication privileges will be able to connect through PgBouncer. You might choose to connect to
PgBouncer using the `application` role, an individual user role created for team members, or any custom user roles that you may have
created (for example, using the [CREATE ROLE](https://www.postgresql.org/docs/current/sql-createrole.html) Postgres command). However,
the `user_lookup` function created by `snowflake_pooler` will deny lookups on superusers and replication roles. See [Snowflake Postgres Roles](/user-guide/snowflake-postgres/postgres-roles)
for more about Postgres users and roles on Snowflake Postgres.

Tip

The terms “user” and “role” in Postgres are largely synonymous. One minor difference is that CREATE USER (versus CREATE ROLE) implies
LOGIN attribute, e.g. `CREATE ROLE myuser LOGIN;`.

### Pooling modes

PgBouncer supports three different pooling modes: transaction, session, and statement. Each is detailed briefly below and further in the
[PgBouncer documentation](https://www.pgbouncer.org/features.html).

#### Transaction

Snowflake Postgres instances will run PgBouncer in transaction pooling mode by default, since that’s the mode we recommend most people use.

Note

When PgBouncer is in transaction pooling mode, SQL-level prepared statements created with PREPARE and run with EXECUTE in different
transactions will not work since they may run on different server connections. PgBouncer does, however, support protocol-level
prepared transactions if the application’s Postgres driver supports them. For more details on how PgBouncer handles this see its
[max\_prepared\_statements](https://www.pgbouncer.org/config.html) documentation.

In order to use PgBouncer’s support for protocol-level prepared statements, the PgBouncer [max\_prepared\_statements setting](/user-guide/snowflake-postgres/postgres-server-settings) must be set to a value greater than `0`. The default on Snowflake Postgres is `250`, but you can set
it to a different value if desired.

#### Session

Session pooling mode is supported on Snowflake Postgres if you have a need for it. To use this pooling mode, set the [pool\_mode setting](/user-guide/snowflake-postgres/postgres-server-settings) to `session` on your cluster.

#### Statement

Statement pooling mode is also available. However, please note that multi-statement transactions will throw errors. To use this pooling mode,
set the [pool\_mode setting](/user-guide/snowflake-postgres/postgres-server-settings) to `statement` on your cluster.

### Disabling PgBouncer

Dropping the `snowflake_pooler` extension from a database will functionally disable PgBouncer since it will no longer be able to authenticate:

Copy code

```
DROP EXTENSION snowflake_pooler;
```
