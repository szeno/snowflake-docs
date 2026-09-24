# sfsql — *Obsoleted*

Obsoleted Feature

`sfsql` is obsolete. Use [Snowflake CLI](/developer-guide/snowflake-cli/index), the preferred command-line client.
SnowSQL remains available as a legacy client. Snowflake supports SnowSQL 1.5.x through April 16, 2028. If you already use SnowSQL, see
[Migrating from SnowSQL to Snowflake CLI](/user-guide/snowsql-migrate).

`sfsql` provides a command-line interface for connecting to Snowflake through JDBC to execute SQL queries and perform DDL and DML operations, including loading and unloading data from database tables.
`sfsql` is a Bash shell script (on Linux/macOS) or batch file (on Microsoft Windows) implemented on top of [HenPlus](http://henplus.sourceforge.net/).

`sfsql` uses the [Snowflake JDBC driver](/developer-guide/jdbc/jdbc) to connect to Snowflake; however, the driver is not a prerequisite for installing the client. The driver is bundled in the
`sfsql` distribution and is automatically installed along with the client.

**Next Topics:**

- [Configuring sfsql — Obsoleted](/user-guide/sfsql-install-config)
- [Starting and Stopping sfsql — Obsoleted](/user-guide/sfsql-start-stop)
- [Using sfsql — Obsoleted](/user-guide/sfsql-use)
- [sfsql Tips and Hints — Obsoleted](/user-guide/sfsql-hints)
- [Differences between sfsql and SnowSQL](/user-guide/snowsql-sfsql-diff)
