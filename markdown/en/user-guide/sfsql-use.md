# Using sfsql — *Obsoleted*

Obsoleted Feature

`sfsql` is now obsoleted. Use [SnowSQL](/user-guide/snowsql) instead.

This topic describes how to use `sfsql`, including a list of the native Henplus commands that are not supported by the client.

Note

Some Snowflake SQL commands are implemented through the JDBC driver used by `sfsql`, e.g. [PUT](/sql-reference/sql/put)/[GET](/sql-reference/sql/get) for uploading files to and downloading files from internal stages.
As a result, these operations can be performed in `sfsql`, but cannot be performed in the Snowflake web interface.

## Navigating and editing on the command line

`sfsql` supports all standard command-line editing functions, including:

- Up and down keys to access the command history.
- Control and Meta key combinations (e.g. **[CTRL]-a**, **[CTRL]-e**) for navigating and editing text on the command line.

## Setting Parameters

HenPlus provides properties that control session behavior; however, you should not set these properties in `sfsql`. Instead, use the [session parameters](/sql-reference/parameters) provided by Snowflake.

In addition, HenPlus provides the following global properties that can be set across all sessions (the property settings are saved when you log out of the session). You can use these global properties to control the formatting and
appearance of your SQL statement results:

- To see the list of global parameters and their current values, type `set-property` at the command line:

  | Property | Initial Value | Description |
  | --- | --- | --- |
  | column-delimiter | | | Specifies the character(s) used to separate/format columns in the display. |
  | comments-remove | off (or false) | Not currently used. |
  | echo-commands | off (or false) | Specifies whether to display a statement before executing it. |
  | sql-result-limit | 1000000000 | Specifies the maximum number of rows returned in the statement results. |
  | sql-result-showfooter | on (or true) | Specifies whether to include a footer row in the results. |
  | sql-result-showheader | on (or true) | Specifies whether to include a header row, including column headings, in the results. |

  Expand

  Show lessSee more
- To set a global parameter, type `set-property` followed by the parameter name and value.

  For example, to disable headers and footers in the results:

  Copy code

  ```
  user1@xy12345.snowflakecomputing.com> set-property sql-result-showfooter false
  user1@xy12345.snowflakecomputing.com> set-property sql-result-showheader false
  ```

  Note that you do not need to type any closing characters, e.g. semi-colon (`;`), to set the global properties.

## Executing SQL Statements and Script Files

To execute a SQL query or statement:

- Type a semi-colon (`;`) immediately following the end of the statement.
- If you enter a new line after the statement, you must type two semi-colons (`;;`) to execute the statement.
- On a new line, you can also type a forward-slash (`/`) which is the command for ending a statement.

For example, any of the syntax can be used to execute the following query:

> Copy code
>
> ```
> user1@xy12345.snowflakecomputing.com> select * from test1;
>
>
> user1@xy12345.snowflakecomputing.com> select * from test1
>                                       ;;
>
> user1@xy12345.snowflakecomputing.com> select * from test1
>                                       /
> ```

To execute a SQL script file, use `@` or `@@` followed by the directory path and full name of the file (including the file extension, if any).

For example, to execute a file named `query.sql` located in the `/Users/user1/scripts` directory:

> Copy code
>
> ```
> user1@xy12345.snowflakecomputing.com> @/Users/user1/scripts/query.sql
> ```

Note

HenPlus also allows using the `start` command to execute a file; however, you cannot use this command in `sfsql` to execute a file because Snowflake reserves the START keyword for initiating transactions. For more information, see
[Transactions](/sql-reference/transactions).

## Canceling In-progress Queries

To cancel a query that has not yet completed, use the **[CTRL]-c** keyboard combo.

## Spooling Results

To spool the results of a SQL query or command, type `spool` followed by the directory path and name of the file in which to spool the results.

To stop spooling results, type `spool off`.

## Accessing the Snowflake Command-line Help

Snowflake provides command-line help topics. To access the help, use the following syntax:

Copy code

```
info [ <topic> | <subtopic> ]
```

- If no value is specified, all the top-level topics in the help are displayed.
- If a topic is specified, all the subtopics for the topic are displayed.
- If a subtopic is specified, the contents of the subtopic are displayed.

For example:

> Copy code
>
> ```
> info;
>
> info warehouses;
>
> info alter_warehouse;
> ```

## Unsupported HenPlus Commands

HenPlus provides native commands for performing tasks such as describing objects and importing/exporting data from the system. You should not use these commands in `sfsql`. Instead, use the SQL commands provided by Snowflake:

| Unsupported HenPlus commands: | Equivalent Snowflake SQL commands: |
| --- | --- |
| `tables` , `views`, and other related commands | [SHOW <objects>](/sql-reference/sql/show) |
| `describe` , `idescribe` | [DESCRIBE <object>](/sql-reference/sql/desc) |
| `import` , `import-check`, and other related commands | [COPY INTO <table>](/sql-reference/sql/copy-into-table), [COPY INTO <location>](/sql-reference/sql/copy-into-location) |
| `dump-out` , `dump-in`, and other related commands | [PUT](/sql-reference/sql/put), [GET](/sql-reference/sql/get) |

Expand

Show lessSee more
