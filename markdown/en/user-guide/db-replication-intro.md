# Introduction to database replication across multiple accounts

Important

This section describes a limited database replication feature that is different from the
[account replication feature](/user-guide/account-replication-intro). Snowflake strongly
recommends using the account replication feature to replicate and failover databases.

This feature enables replicating databases between Snowflake accounts (within the same organization) and keeping the database objects and stored data synchronized. Database replication is supported across [regions](/user-guide/intro-regions) and across [cloud platforms](/user-guide/intro-cloud-platforms).

## What is a primary database?

Replication can be enabled for any existing permanent or transient database. Enabling replication designates the database as a *primary database*. Any number of databases in an account can be designated a primary database. Likewise, a primary database can be replicated to any number of accounts in your organization. This involves creating a *secondary database* as a replica of a specified primary database in each of the target accounts. These accounts are typically located in other regions, on the same or a different cloud platform, or they can be in the same region as the source account.

All DML/DDL operations are executed on the primary database. Each read-only, secondary database can be refreshed periodically with a snapshot of the primary database, replicating all data as well as DDL operations on database objects (i.e. schemas, tables, views, etc.).

## Overview of database replication

For the full list of replicated database objects, see [Replicated database objects](/user-guide/account-replication-intro#label-replicated-database-objects).

### Other objects in an account

Database replication is supported for databases only. Other types of objects in an account can be replicated with
[account replication](/user-guide/account-replication-intro). For the full list of supported objects for account
replication, see [Replicated objects](/user-guide/account-replication-intro#label-replicated-objects).

### Access control

Privileges granted on database objects are not replicated to a secondary database.
This includes privilege grants on existing database objects as well as grants on future
objects (i.e. future grants).

Privilege grants can be replicated with [account replication](/user-guide/account-replication-intro).

### Parameters

Account parameters are not replicated with database replication. Account parameters can be replicated with [account replication](/user-guide/account-replication-intro).

Object parameters that are set at the schema or schema object level are replicated:

> | Parameter | Objects |
> | --- | --- |
> | [DATA\_RETENTION\_TIME\_IN\_DAYS](/sql-reference/parameters#label-data-retention-time-in-days) | schema, table |
> | [DEFAULT\_DDL\_COLLATION](/sql-reference/parameters#label-default-ddl-collation) | schema, table |
> | [MAX\_DATA\_EXTENSION\_TIME\_IN\_DAYS](/sql-reference/parameters#label-max-data-extension-time-in-days) | schema, table |
> | [PIPE\_EXECUTION\_PAUSED](/sql-reference/parameters#label-pipe-execution-paused) [1] | schema, pipe |
> | [QUOTED\_IDENTIFIERS\_IGNORE\_CASE](/sql-reference/parameters#label-quoted-identifiers-ignore-case) | schema, table |
>
> Expand
>
> Show lessSee more

Parameter replication is only applicable to objects in the database (schema, table) and only if the parameter is explicitly set using CREATE
`<object>` `<parameter>` or ALTER `<object>` … SET `<parameter>`. Database level parameters are not replicated.

Parameters explicitly set on objects in the primary database overwrite parameters set on objects in the secondary database. For example, if
the primary database has a schema `s1` with DATA\_RETENTION\_TIME\_IN\_DAYS set to 10 and the secondary database has
DATA\_RETENTION\_TIME\_IN\_DAYS set to 1 at the database level, DATA\_RETENTION\_TIME\_IN\_DAYS for schema `s1` in the secondary database is set
to 10 after replication.

Parameters explicitly set at the database level on secondary databases are not overwritten. For example, if the secondary database parameter
DATA\_RETENTION\_TIME\_IN\_DAYS is explicitly set to 1 and the primary database parameter DATA\_RETENTION\_TIME\_IN\_DAYS is explicitly set to 10,
DATA\_RETENTION\_TIME\_IN\_DAYS for the secondary database remains set to 1 after replication.

[1] Note that PIPE objects are not replicated. If the PIPE\_EXECUTION\_PAUSED parameter is set at the schema level in the primary
database, it is replicated to the secondary database. When the secondary database is promoted to primary database in the case of a failover
and a pipe is created, the parameter setting will take effect.

## Database replication to accounts on lower editions

If either of the following conditions is true, Snowflake displays an error message when a local database is promoted to serve as a primary database:

- The primary database is in a Business Critical (or higher) account but one or more of the accounts approved for replication are on lower editions. Business Critical Edition is intended for Snowflake accounts with extremely sensitive data.
- The primary database is in a Business Critical (or higher) account and a signed business associate agreement is in place to store PHI data in the account per HIPAA and [HITRUST CSF](/user-guide/intro-cloud-platforms#label-hitrust-csf-cert) regulations, but no such agreement is in place for one or more of the accounts approved for replication, regardless if they are Business Critical (or higher) accounts.

This behavior is implemented in an effort to help prevent account administrators for Business Critical (or higher) accounts from inadvertently replicating sensitive data to accounts on lower editions.

An account administrator can override this default behavior by including the IGNORE EDITION CHECK clause when executing the [ALTER DATABASE … ENABLE REPLICATION TO ACCOUNTS](/sql-reference/sql/alter-database) statement. If IGNORE EDITION CHECK is set, the primary database can be replicated to the specified accounts on any Snowflake edition.

## Current limitations of database replication

- Databases created from shares cannot be replicated.
- Refresh operations fail if the primary database includes a stream with an unsupported source object.
  The operation also fails if the source object for any stream has been dropped.
- Append-only streams are not supported on replicated source objects.

- The CREATE DATABASE … AS REPLICA command does not support the WITH TAG clause.

  This clause is not supported because the secondary database is read only. If your primary database specifies the WITH TAG clause, remove
  the clause prior to creating the secondary database. To verify whether your database has the WITH TAG clause, call the
  [GET\_DDL](/sql-reference/functions/get_ddl) function in your Snowflake account and specify the primary database in the function argument. If
  a tag is set on the database, the function output will include an ALTER DATABASE … SET TAG statement.
- Stage and pipe replication are not supported. You can replicate stages and pipes using account replication. For more information, see
  [Stage, pipe, and load history replication](/user-guide/account-replication-stages-pipes-load-history).
- [Secrets](/sql-reference/sql/create-secret) is not supported. You can replicate secrets using a replication or failover group.
