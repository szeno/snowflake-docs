# Snowflake Postgres Server Settings

The table below details the parameters that can be set for the Postgres server component of Snowflake Postgres instances. Each setting’s name
is hyperlinked to its Postgres documentation.

Where “Postgres default” appears in the Default column, Snowflake Postgres instances use the default value from Postgres. This can vary by
major version.

See [Creating a Snowflake Postgres Instance](/user-guide/snowflake-postgres/postgres-create-instance) for details on setting values for these Postgres server settings when creating Snowflake Postgres
instances.

Tip

To see a parameter’s documentation for a specific major version change the word “current” in the hyperlink address to the
target major version. For example, this hyperlink address for the `postgres:work_mem` setting:

<https://www.postgresql.org/docs/current/runtime-config-resource.html#GUC-WORK-MEM>

becomes this to visit its Postgres 17 documentation:

<https://www.postgresql.org/docs/17/runtime-config-resource.html#GUC-WORK-MEM>

| Component | Name | Requires restart | Description | Default |
| --- | --- | --- | --- | --- |
| pgbouncer | [autodb\_idle\_timeout](https://www.pgbouncer.org/config.html) | FALSE | If the automatically created (via “\*”) database pools have been unused this many seconds, they are freed. | 3600 |
| pgbouncer | [default\_pool\_size](https://www.pgbouncer.org/config.html) | FALSE | How many server connections to allow per user/database pair. | 497 |
| pgbouncer | [ignore\_startup\_parameters](https://www.pgbouncer.org/config.html) | FALSE | Ignore parameters startup packets (e.g. options,extra\_float\_digits). | client\_encoding,datestyle,timezone,standard\_conforming\_strings,extra\_float\_digits |
| pgbouncer | [max\_prepared\_statements](https://www.pgbouncer.org/config.html) | FALSE | Number of prepared statements kept active on a single server connection | 250 |
| pgbouncer | [pool\_mode](https://www.pgbouncer.org/config.html) | FALSE | Specifies when a server connection can be reused by other clients. | transaction |
| pgbouncer | [server\_idle\_timeout](https://www.pgbouncer.org/config.html) | FALSE | If a server connection has been idle for more than this many seconds, it will be closed. | 60 |
| postgres | [auto\_explain.log\_analyze](https://www.postgresql.org/docs/current/auto-explain.html#AUTO-EXPLAIN-CONFIGURATION-PARAMETERS-LOG-ANALYZE) | FALSE | Causes EXPLAIN ANALYZE output, rather than just EXPLAIN output, to be printed when an execution plan is logged. | Postgres default |
| postgres | [auto\_explain.log\_buffers](https://www.postgresql.org/docs/current/auto-explain.html#AUTO-EXPLAIN-CONFIGURATION-PARAMETERS-LOG-BUFFERS) | FALSE | Controls whether buffer usage statistics are printed when an execution plan is logged. | Postgres default |
| postgres | [auto\_explain.log\_format](https://www.postgresql.org/docs/current/auto-explain.html#AUTO-EXPLAIN-CONFIGURATION-PARAMETERS-LOG-FORMAT) | FALSE | Selects the EXPLAIN output format to be used. | Postgres default |
| postgres | [auto\_explain.log\_min\_duration](https://www.postgresql.org/docs/current/auto-explain.html#AUTO-EXPLAIN-CONFIGURATION-PARAMETERS-LOG-MIN-DURATION) | FALSE | The minimum statement execution time, in milliseconds, that will cause the statement’s plan to be logged. | Postgres default |
| postgres | [auto\_explain.log\_nested\_statements](https://www.postgresql.org/docs/current/auto-explain.html#AUTO-EXPLAIN-CONFIGURATION-PARAMETERS-LOG-NESTED-STATEMENTS) | FALSE | Causes nested statements (statements executed inside a function) to be considered for logging. | Postgres default |
| postgres | [auto\_explain.log\_timing](https://www.postgresql.org/docs/current/auto-explain.html#AUTO-EXPLAIN-CONFIGURATION-PARAMETERS-LOG-TIMING) | FALSE | Controls whether per-node timing information is printed when an execution plan is logged. | Postgres default |
| postgres | [auto\_explain.log\_triggers](https://www.postgresql.org/docs/current/auto-explain.html#AUTO-EXPLAIN-CONFIGURATION-PARAMETERS-LOG-TRIGGERS) | FALSE | Causes trigger execution statistics to be included when an execution plan is logged. | Postgres default |
| postgres | [auto\_explain.log\_verbose](https://www.postgresql.org/docs/current/auto-explain.html#AUTO-EXPLAIN-CONFIGURATION-PARAMETERS-LOG-VERBOSE) | FALSE | Controls whether verbose details are printed when an execution plan is logged. | Postgres default |
| postgres | [auto\_explain.sample\_rate](https://www.postgresql.org/docs/current/auto-explain.html#AUTO-EXPLAIN-CONFIGURATION-PARAMETERS-SAMPLE-RATE) | FALSE | Causes auto\_explain to only explain a fraction of the statements in each session. | Postgres default |
| postgres | [autovacuum\_analyze\_scale\_factor](https://www.postgresql.org/docs/17/runtime-config-autovacuum.html#GUC-AUTOVACUUM-ANALYZE-SCALE-FACTOR) | FALSE | Specifies a fraction of the table size to add to autovacuum\_analyze\_threshold when deciding whether to trigger an ANALYZE. | Postgres default |
| postgres | [autovacuum\_freeze\_max\_age](https://www.postgresql.org/docs/17/runtime-config-autovacuum.html#GUC-AUTOVACUUM-FREEZE-MAX-AGE) | TRUE | Specifies the maximum age (in transactions) that a table’s transaction ID can attain before a VACUUM operation is forced to prevent transaction ID wraparound within the table. | Postgres default |
| postgres | [autovacuum\_vacuum\_cost\_delay](https://www.postgresql.org/docs/17/runtime-config-autovacuum.html#GUC-AUTOVACUUM-VACUUM-COST-DELAY) | FALSE | Specifies the cost delay value that will be used in automatic VACUUM operations. If -1 is specified, the regular vacuum\_cost\_delay value will be used. | Postgres default |
| postgres | [autovacuum\_vacuum\_cost\_limit](https://www.postgresql.org/docs/17/runtime-config-autovacuum.html#GUC-AUTOVACUUM-VACUUM-COST-LIMIT) | FALSE | Specifies the cost limit value that will be used in automatic VACUUM operations. | Postgres default |
| postgres | [autovacuum\_vacuum\_insert\_scale\_factor](https://www.postgresql.org/docs/17/runtime-config-autovacuum.html#GUC-AUTOVACUUM-VACUUM-INSERT-SCALE-FACTOR) | FALSE | Specifies a fraction of the table size to add to autovacuum\_vacuum\_insert\_threshold when deciding whether to trigger a VACUUM. | Postgres default |
| postgres | [autovacuum\_vacuum\_insert\_threshold](https://www.postgresql.org/docs/17/runtime-config-autovacuum.html#GUC-AUTOVACUUM-VACUUM-INSERT-THRESHOLD) | FALSE | Specifies the number of inserted tuples needed to trigger a VACUUM in any one table. | Postgres default |
| postgres | [autovacuum\_vacuum\_scale\_factor](https://www.postgresql.org/docs/17/runtime-config-autovacuum.html#GUC-AUTOVACUUM-VACUUM-SCALE-FACTOR) | FALSE | Specifies a fraction of the table size to add to autovacuum\_vacuum\_threshold when deciding whether to trigger a VACUUM. | Postgres default |
| postgres | [checkpoint\_completion\_target](hhttps://www.postgresql.org/docs/current/runtime-config-wal.html#GUC-CHECKPOINT-COMPLETION-TARGET) | FALSE | Specifies the target of checkpoint completion, as a fraction of total time between checkpoints. | Postgres default |
| postgres | [checkpoint\_timeout](https://www.postgresql.org/docs/current/runtime-config-wal.html#GUC-CHECKPOINT-TIMEOUT) | FALSE | Maximum time between automatic WAL checkpoints. | Postgres default |
| postgres | [checkpoint\_warning](https://www.postgresql.org/docs/current/runtime-config-wal.html#GUC-CHECKPOINT-WARNING) | FALSE | Write a message to the server log if checkpoints caused by the filling of WAL segment files happen closer together than this amount of time. | Postgres default |
| postgres | [default\_statistics\_target](https://www.postgresql.org/docs/current/runtime-config-query.html#GUC-DEFAULT-STATISTICS-TARGET) | FALSE | Sets the default statistics target for table columns without a column-specific target set via ALTER TABLE SET STATISTICS. | Postgres default |
| postgres | [default\_text\_search\_config](https://www.postgresql.org/docs/current/runtime-config-client.html#GUC-DEFAULT-TEXT-SEARCH-CONFIG) | FALSE | Selects the text search configuration that is used by those variants of the text search functions that do not have an explicit argument specifying the configuration. | Postgres default |
| postgres | [default\_transaction\_read\_only](https://www.postgresql.org/docs/current/runtime-config-client.html#GUC-DEFAULT-TRANSACTION-READ-ONLY) | FALSE | A read-only SQL transaction cannot alter non-temporary tables. | off |
| postgres | [hot\_standby\_feedback](https://www.postgresql.org/docs/current/runtime-config-replication.html#GUC-HOT-STANDBY-FEEDBACK) | FALSE | Specifies whether or not a hot standby will send feedback to the primary or upstream standby about queries currently executing on the standby. | on |
| postgres | [idle\_in\_transaction\_session\_timeout](https://www.postgresql.org/docs/current/runtime-config-client.html#GUC-IDLE-IN-TRANSACTION-SESSION-TIMEOUT) | FALSE | Terminate any session that has been idle within an open transaction for longer than the specified amount of time. | Postgres default |
| postgres | [intervalstyle](https://www.postgresql.org/docs/current/runtime-config-client.html#GUC-INTERVALSTYLE) | FALSE | Sets the display format for interval value. | Postgres default |
| postgres | [jit](https://www.postgresql.org/docs/current/runtime-config-query.html#GUC-JIT) | FALSE | Enable JIT support. | Postgres default |
| postgres | [lock\_timeout](https://www.postgresql.org/docs/current/runtime-config-client.html#GUC-LOCK-TIMEOUT) | FALSE | Abort any statement that waits longer than the specified amount of time while attempting to acquire a lock. | Postgres default |
| postgres | [log\_autovacuum\_min\_duration](https://www.postgresql.org/docs/current/runtime-config-logging.html#GUC-LOG-AUTOVACUUM-MIN-DURATION) | FALSE | Causes each action executed by autovacuum to be logged if it ran for at least the specified amount of time. | Postgres default |
| postgres | [log\_connections](https://www.postgresql.org/docs/current/runtime-config-logging.html#GUC-LOG-CONNECTIONS) | FALSE | Outputs a line to the server logs detailing each successful connection. | Postgres default |
| postgres | [log\_destination](https://www.postgresql.org/docs/current/runtime-config-logging.html#GUC-LOG-DESTINATION) | FALSE | Sets the desired log destinations. | syslog,stderr |
| postgres | [log\_disconnections](https://www.postgresql.org/docs/current/runtime-config-logging.html#GUC-LOG-DISCONNECTIONS) | FALSE | Causes session terminations to be logged. The log output provides information similar to log\_connections, plus the duration of the session. | Postgres default |
| postgres | [log\_duration](https://www.postgresql.org/docs/current/runtime-config-logging.html#GUC-LOG-DURATION) | FALSE | Causes the duration of every completed statement to be logged. | Postgres default |
| postgres | [log\_line\_prefix](https://www.postgresql.org/docs/current/runtime-config-logging.html#GUC-LOG-LINE-PREFIX) | FALSE | Specifies a printf-style string that is output at the beginning of each log line. | [%p][%b][%v][%x] %q[user=%u,db=%d,app=%a] |
| postgres | [log\_lock\_waits](https://www.postgresql.org/docs/current/runtime-config-logging.html#GUC-LOG-LOCK-WAITS) | FALSE | Controls whether a log message is produced when a session waits longer than deadlock\_timeout to acquire a lock. | on |
| postgres | [log\_min\_duration\_sample](https://www.postgresql.org/docs/current/runtime-config-logging.html#GUC-LOG-MIN-DURATION-SAMPLE) | FALSE | Allows sampling the duration of completed statements that ran for at least the specified amount of time. | Postgres default |
| postgres | [log\_min\_duration\_statement](https://www.postgresql.org/docs/current/runtime-config-logging.html#GUC-LOG-MIN-DURATION-STATEMENT) | FALSE | Causes the duration of each completed statement to be logged if the statement ran for at least the specified amount of time. | 2s |
| postgres | [log\_min\_messages](https://www.postgresql.org/docs/current/runtime-config-logging.html#GUC-LOG-MIN-MESSAGES) | FALSE | Controls which message levels are written to the server log. | notice |
| postgres | [log\_rotation\_size](https://www.postgresql.org/docs/current/runtime-config-logging.html#GUC-LOG-ROTATION-SIZE) | FALSE | This determines the maximum size of an individual log file. | Postgres default |
| postgres | [log\_statement](https://www.postgresql.org/docs/current/runtime-config-logging.html#GUC-LOG-STATEMENT) | FALSE | Controls which SQL statements are logged. | ddl |
| postgres | [log\_statement\_sample\_rate](https://www.postgresql.org/docs/current/runtime-config-logging.html#GUC-LOG-STATEMENT-SAMPLE-RATE) | FALSE | Determines the fraction of statements with duration exceeding log\_min\_duration\_sample that will be logged. | Postgres default |
| postgres | [log\_temp\_files](https://www.postgresql.org/docs/current/runtime-config-logging.html#GUC-LOG-TEMP-FILES) | FALSE | Controls logging of temporary file names and sizes. | 10MB |
| postgres | [log\_transaction\_sample\_rate](https://www.postgresql.org/docs/current/runtime-config-logging.html#GUC-LOG-TRANSACTION-SAMPLE-RATE) | FALSE | Sets the fraction of transactions whose statements are all logged, in addition to statements logged for other reasons. | Postgres default |
| postgres | [logical\_decoding\_work\_mem](https://www.postgresql.org/docs/current/runtime-config-resource.html#GUC-LOGICAL-DECODING-WORK-MEM) | FALSE | Specifies the maximum amount of memory to be used by logical decoding. | Postgres default |
| postgres | [maintenance\_work\_mem](https://www.postgresql.org/docs/current/runtime-config-resource.html#GUC-MAINTENANCE-WORK-MEM) | FALSE | Specifies the maximum amount of memory to be used by maintenance operations, such as VACUUM, CREATE INDEX, and ALTER TABLE ADD FOREIGN KEY. | TOTAL\_MEMORY \* 0.4 |
| postgres | [max\_connections](https://www.postgresql.org/docs/current/runtime-config-connection.html#GUC-MAX-CONNECTIONS) | TRUE | Determines the maximum number of concurrent connections to the database server. | 500 |
| postgres | [max\_locks\_per\_transaction](https://www.postgresql.org/docs/current/runtime-config-locks.html#GUC-MAX-LOCKS-PER-TRANSACTION) | TRUE | Controls the average number of object locks allocated for each transaction. | Postgres default |
| postgres | [max\_logical\_replication\_workers](https://www.postgresql.org/docs/current/runtime-config-replication.html#GUC-MAX-LOGICAL-REPLICATION-WORKERS) | TRUE | Specifies maximum number of logical replication workers. | Postgres default |
| postgres | [max\_parallel\_maintenance\_workers](https://www.postgresql.org/docs/current/runtime-config-resource.html#GUC-MAX-PARALLEL-MAINTENANCE-WORKERS) | FALSE | Sets the maximum number of parallel workers that can be started by a single utility command. | Postgres default |
| postgres | [max\_parallel\_workers](https://www.postgresql.org/docs/current/runtime-config-resource.html#GUC-MAX-PARALLEL-WORKERS) | FALSE | Sets the maximum number of workers that the cluster can support for parallel operations. | NUM\_CPUS |
| postgres | [max\_parallel\_workers\_per\_gather](https://www.postgresql.org/docs/current/runtime-config-resource.html#GUC-MAX-PARALLEL-WORKERS-PER-GATHER) | FALSE | Sets the maximum number of workers that can be started by a single Gather or Gather Merge node. | NUM\_CPUS |
| postgres | [max\_replication\_slots](https://www.postgresql.org/docs/current/runtime-config-replication.html#GUC-MAX-REPLICATION-SLOTS) | TRUE | Specifies the maximum number of replication slots that the server can support. | 10 |
| postgres | [max\_slot\_wal\_keep\_size](https://www.postgresql.org/docs/current/runtime-config-replication.html#GUC-MAX-SLOT-WAL-KEEP-SIZE) | FALSE | Specifies the maximum size of WAL files that replication slots are allowed to retain in the *pg\_wal* directory at checkpoint time. | STORAGE\_GB \* 0.1 |
| postgres | [max\_standby\_archive\_delay](https://www.postgresql.org/docs/current/runtime-config-replication.html#GUC-MAX-STANDBY-ARCHIVE-DELAY) | FALSE | Determines how long the standby server should wait before canceling standby queries that conflict with about-to-be-applied WAL entries. | Postgres default |
| postgres | [max\_standby\_streaming\_delay](https://www.postgresql.org/docs/current/runtime-config-replication.html#GUC-MAX-STANDBY-STREAMING-DELAY) | FALSE | Determines how long the standby server should wait before canceling standby queries that conflict with about-to-be-applied WAL entries. | Postgres default |
| postgres | [max\_wal\_senders](https://www.postgresql.org/docs/current/runtime-config-replication.html#GUC-MAX-WAL-SENDERS) | TRUE | Specifies the maximum number of concurrent connections from standby servers or streaming base backup clients. | 10 |
| postgres | [max\_wal\_size](https://www.postgresql.org/docs/current/runtime-config-wal.html#GUC-MAX-WAL-SIZE) | FALSE | Maximum size to let the WAL grow during automatic checkpoints. | MIN(10GB, STORAGE\_GB \* 0.1) |
| postgres | [max\_worker\_processes](https://www.postgresql.org/docs/current/runtime-config-resource.html#GUC-MAX-WORKER-PROCESSES) | TRUE | Sets the maximum number of background processes that the cluster can support. | 100 |
| postgres | [pg\_stat\_statements.max](https://www.postgresql.org/docs/current/pgstatstatements.html#PGSTATSTATEMENTS-CONFIG-PARAMS) | TRUE | Maximum number of statements tracked. | Postgres default |
| postgres | [pg\_stat\_statements.track](https://www.postgresql.org/docs/current/pgstatstatements.html#PGSTATSTATEMENTS-CONFIG-PARAMS) | FALSE | Control which statements should be tracked. | Postgres default |
| postgres | [pg\_stat\_statements.track\_utility](https://www.postgresql.org/docs/current/pgstatstatements.html#PGSTATSTATEMENTS-CONFIG-PARAMS) | FALSE | Should the utility commands be tracked. Utility commands are all those other than SELECT, INSERT, UPDATE, DELETE, and MERGE. | Postgres default |
| postgres | [random\_page\_cost](https://www.postgresql.org/docs/current/runtime-config-query.html) | FALSE | Sets the planner’s estimate of the cost of a non-sequentially-fetched disk page. | 1.1 |
| postgres | [session\_preload\_libraries](https://www.postgresql.org/docs/current/runtime-config-client.html#GUC-SESSION-PRELOAD-LIBRARIES) | FALSE | Specifies one or more shared libraries that are to be preloaded at connection start. | Postgres default |
| postgres | [statement\_timeout](https://www.postgresql.org/docs/current/runtime-config-client.html#GUC-STATEMENT-TIMEOUT) | FALSE | Abort any statement that takes more than the specified amount of time. | Postgres default |
| postgres | [synchronous\_commit](https://www.postgresql.org/docs/current/runtime-config-wal.html#GUC-SYNCHRONOUS-COMMIT) | FALSE | Specifies how much WAL processing must complete before the database server returns a “success” indication to the client. | local |
| postgres | [syslog\_split\_messages](https://www.postgresql.org/docs/current/runtime-config-logging.html#GUC-SYSLOG-SPLIT-MESSAGES) | FALSE | Split messages sent to syslog by lines and to fit into 1024 bytes | Postgres default |
| postgres | [tcp\_keepalives\_count](https://www.postgresql.org/docs/current/runtime-config-connection.html#GUC-TCP-KEEPALIVES-COUNT) | FALSE | Specifies the number of TCP keepalive messages that can be lost before the server’s connection to the client is considered dead. | 4 |
| postgres | [tcp\_keepalives\_idle](https://www.postgresql.org/docs/current/runtime-config-connection.html#GUC-TCP-KEEPALIVES-IDLE) | FALSE | Specifies the amount of time with no network activity after which the operating system should send a TCP keepalive message to the client. | 2 |
| postgres | [temp\_file\_limit](https://www.postgresql.org/docs/current/runtime-config-resource.html#GUC-TEMP-FILE-LIMIT) | FALSE | Specifies the maximum amount of disk space that a process can use for temporary files, such as sort and hash temporary files, or the storage file for a held cursor. | MIN(2000GB, STORAGE\_GB \* 0.25) |
| postgres | [track\_activity\_query\_size](https://www.postgresql.org/docs/current/runtime-config-statistics.html#GUC-TRACK-ACTIVITY-QUERY-SIZE) | TRUE | Memory reserved to store the text of the currently executing command for each active session, for the pg\_stat\_activity.query field. | Postgres default |
| postgres | [track\_commit\_timestamp](https://www.postgresql.org/docs/current/runtime-config-replication.html#GUC-TRACK-COMMIT-TIMESTAMP) | TRUE | Record commit time of transactions. | Postgres default |
| postgres | [wal\_keep\_size](https://postgresqlco.nf/doc/en/param/wal_keep_size/) | FALSE | Specifies the minimum size of past WAL files kept in the pg\_wal directory, in case a standby server needs to fetch them for streaming replication. | Postgres default |
| postgres | [wal\_sender\_timeout](https://www.postgresql.org/docs/current/runtime-config-replication.html) | FALSE | Sets the maximum time to wait for WAL replication. | Postgres default |
| postgres | [work\_mem](https://www.postgresql.org/docs/current/runtime-config-resource.html#GUC-WORK-MEM) | FALSE | Sets the base maximum amount of memory to be used by a query operation (such as a sort or hash table) before writing to temporary disk files. | (TOTAL\_MEMORY \* 0.75)/ (NUM\_CORES \* 8) |

Expand

Show lessSee more
