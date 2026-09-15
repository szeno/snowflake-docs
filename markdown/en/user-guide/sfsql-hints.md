# sfsql Tips and Hints — *Obsoleted*

Obsoleted Feature

`sfsql` is now obsoleted. Use [SnowSQL](/user-guide/snowsql) instead.

This topic provides tips, hints, and other useful information for using
`sfsql`.

## Setting Session Defaults

If you did not set a default role, database, schema, or warehouse for your session
either in the `login.defaults` file or on the command line when starting `sfsql`,
you should set these values to make executing SQL queries and performing DDL or
DML operations easier. For more information, see:

> - [USE ROLE](/sql-reference/sql/use-role)
> - [USE DATABASE](/sql-reference/sql/use-database)
> - [USE SCHEMA](/sql-reference/sql/use-schema)
> - [USE WAREHOUSE](/sql-reference/sql/use-warehouse)

Note that these defaults can also be set at the user level by individual users
or an account administrator.

## Specifying Directory Paths and Files

When performing any file operation in `sfsql`, by default, the client looks for
the file in the directory path from which the client was started. To use files
located in a different directory path, provide the fully-qualified path, e.g.
`/<path>/<to>/<file>` (in a Linux or macOS environment).

## Escaping Control Characters

`sfsql` pre-processes user input for control characters. As a result, to insert
a single backslash character into a SQL string literal in the client, the backslash
character needs to be double-escaped (i.e. `\` must be written as `\\\\`).

## Formatting Output

HenPlus forces output to display in delimited table/column format. This may result
in trailing blank spaces added to field values and a column delimiter (e.g. `|`
or `,`) added to the end of each row in query results. If you don’t want these
additional characters in your results, you will need to remove them manually.
