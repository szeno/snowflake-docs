# Feb 17, 2026: Access history improvements

[Access history](/user-guide/access-history) lets you monitor the SQL statements executed in Snowflake. It keeps track of the
following types of statements:

- Data Manipulation Language (DML) statements. For example, statements used to insert data into a table.
- Data Query Language (DQL) statements. For example, statements that use a SELECT statement to project data.
- Data Definition Language (DDL) statements. For example, statements that create or alter a Snowflake object.

Previously, records that were too large were excluded from the ACCESS\_HISTORY view. Now, Snowflake truncates enough data for the record to
fit in the view. Truncated records contain indicators where values have been truncated.

For more information, see [Usage notes: Truncation](/sql-reference/account-usage/access_history#label-access-history-notes-truncation-acctuse).
