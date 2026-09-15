# PostgreSQL - PostgreSQL interactive terminal

PSQL commands

## Applies to

- PostgreSQL
- Netezza

## Description

> PSQL is a terminal-based front-end to PostgreSQL. It enables you to type in queries interactively, issue them to PostgreSQL, and see the query results. Alternatively, input can be from a file. In addition, it provides a number of meta-commands and various shell-like features to facilitate writing scripts and automating a wide variety of tasks. ([PSQL documentation](https://www.postgresql.org/docs/9.2/app-psql.html)).

In Snowflake, **PSQL commands are not applicable.** While no longer needed for execution, the original PSQL command is retained as a comment

## Sample Source Patterns

### Input Code:

#### Greenplum

Copy code

```
:force:
\set ON_ERROR_STOP TRUE
```

### Output Code:

#### Snowflake

Copy code

```
:force:
----** SSC-FDM-PG0015 - PSQL COMMAND IS NOT APPLICABLE IN SNOWFLAKE. **
--\set ON_ERROR_STOP TRUE
```

## Related EWIs

1. [SSC-FDM-PG0015](../../issues-and-troubleshooting/functional-difference/postgresqlFDM#ssc-fdm-pg0015) : PSQL command is not applicable in Snowflake.
