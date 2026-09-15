# Understanding caller’s rights and owner’s rights stored procedures

A stored procedure runs with either the caller’s rights or the owner’s rights. It cannot run with
both at the same time. This topic describes the differences between a caller’s rights stored procedure and an
owner’s rights stored procedure.

## Introduction

A caller’s rights stored procedure runs with the privileges of the caller. The primary advantage of a caller’s
rights stored procedure is that it can access information about that caller or about the caller’s current session.
For example, a caller’s rights stored procedure can read the caller’s session variables and use them in a query.

An owner’s rights stored procedure runs mostly with the privileges of the stored procedure’s owner.
The primary advantage of an owner’s rights stored procedure is that
the owner can delegate specific administrative tasks, such as cleaning up old data,
to another role without granting that role more general privileges, such as privileges to delete all data from a
specific table.

At the time that the stored procedure is created, the creator specifies whether the procedure runs with owner’s rights
or caller’s rights. The default is owner’s rights.

The owner can change the procedure from an owner’s rights stored procedure to a caller’s rights stored procedure
(or vice-versa) by executing an [ALTER PROCEDURE](/sql-reference/sql/alter-procedure) command.

Tip

Use [references](/developer-guide/stored-procedure/stored-procedures-calling-references) to allow operations on
specific SQL objects or queries to be performed using the caller’s rights, even when the stored procedure
runs with owner’s rights.

## Privileges on database objects

A caller’s rights stored procedure runs with the database privileges of the role that called the stored procedure.
Any statement that the caller could not execute outside the stored procedure cannot be executed inside the stored
procedure, either. For example, if the role named “Nurse” does not have privileges to delete rows
from the `medical_records` table, then if a user with the role “Nurse” calls a caller’s rights stored
procedure that tries to delete rows from that table, the stored procedure will fail.

An owner’s rights procedure runs with the rights of the procedure owner. This means that if the owner has the
privileges to perform a task, then the stored procedure can perform that task even when called by a role that
does not have privileges to perform that task directly. For example, if the role named “Doctor” has the database
privileges to delete rows from the `medical_records` table, and the “Doctor” role creates a stored procedure
that deletes rows older than 7 years from that table, then if the “Doctor” role grants the “Nurse” role appropriate
privileges on the stored procedure, then the “Nurse” role can run the stored procedure (and delete old rows from the
table via that stored procedure), even if the “Nurse” role doesn’t have delete privileges on the table.

Tip

If you need an owner’s rights stored procedure to perform actions on a table, view, or function that the caller has the
privileges to access, you can have the caller pass a reference to that table, view, or function.

For details, refer to [Stored Procedures Calling References](stored-procedures-calling-references).

## Accessing and setting the session state

As with other SQL statements, a `CALL` statement runs within a session, and inherits context from that session,
such as session-level variables, current database, etc. The exact context that the procedure inherits depends upon
whether the stored procedure is a caller’s rights stored procedure or an owner’s rights stored procedure.

If a caller’s rights stored procedure makes changes to the session, those changes can persist after the end of the
`CALL`. Owner’s rights stored procedures are not permitted to change session state.

## Caller’s rights stored procedures

Caller’s rights stored procedures adhere to the following rules within a session:

- Run with the privileges of the caller, not the privileges of the owner.
- Inherit the current warehouse of the caller.
- Use the database and schema that the caller is currently using.
- Can view, set, and unset the caller’s session variables.
- Can view, set, and unset the caller’s session parameters.

### Running with a subset of caller’s rights

You might want a stored procedure to run with caller’s rights, but only a subset of those rights. An administrator can use caller
grants to control which of the caller’s rights the stored procedure can run with. For more information, see
[Restricted caller’s rights](/developer-guide/restricted-callers-rights).

### Session variables for caller’s rights procedures

Suppose that the stored procedure named `MyProcedure` executes SQL statements that read and set session-level
variables. In this example, the details of the read and set commands are not important, so the statements are
represented as pseudo-code:

- `READ SESSION_VAR1`
- `SET SESSION_VAR2`

The stored procedure looks similar to the following pseudocode:

Copy code

```
CREATE PROCEDURE MyProcedure()
...
$$
   READ SESSION_VAR1;
   SET SESSION_VAR2;
$$
;
```

Suppose that you execute the following sequence of statements in the same session:

Copy code

```
SET SESSION_VAR1 = 'some interesting value';
CALL MyProcedure();
SELECT *
  FROM table1
  WHERE column1 = $SESSION_VAR2;
```

This is equivalent to executing the following sequence:

Copy code

```
SET SESSION_VAR1 = 'some interesting value';
READ SESSION_VAR1;
SET SESSION_VAR2;
SELECT *
  FROM table1
  WHERE column1 = $SESSION_VAR2;
```

In other words:

- The stored procedure can see the variable that was set by statements before the procedure was called.
- The statements after the stored procedure can see the variable that was set inside the procedure.

For a complete example that does not rely on pseudo-code, see [Using session variables with caller’s rights and owner’s rights stored procedures](/developer-guide/stored-procedure/stored-procedures-javascript#label-sp-session-variables-example) (in this topic).

In many stored procedures, you want to inherit context information such as the current database and the current
session-level variables.

However, in some cases, you might want your stored procedure to be more isolated. For example, if your stored
procedure sets a session-level variable, you might not want the session-level variable to influence future statements
outside your stored procedure.

To better isolate your stored procedure from the rest of your session:

- Avoid using session-level variables directly. Instead, pass them as explicit parameters. This forces the caller to
  think about exactly which session-level variables the stored procedure will use.
- Clean up any session-level variables that you set inside the stored procedure (and use names that are not likely to
  be used anywhere else, so that you don’t accidentally clean up a session variable that existed prior to the stored
  procedure call).

The following stored procedure uses the value of a session variable by receiving it as a parameter, not
by using the session variable directly:

Copy code

```
SET Variable_1 = 49;

CREATE PROCEDURE sv_proc2(PARAMETER_1 FLOAT)
  RETURNS VARCHAR
  LANGUAGE JAVASCRIPT
  AS
  $$
    var rs = snowflake.execute( {sqlText: "SELECT 2 * " + PARAMETER_1} );
    rs.next();
    var MyString = rs.getColumnValue(1);
    return MyString;
  $$
  ;

CALL sv_proc2($Variable_1);
```

The following stored procedure creates a temporary session variable with an unusual name and cleans up
that variable before the stored procedure finishes. When a statement after the procedure call tries to use the session
variable that was cleaned up, that statement will fail:

Copy code

```
CREATE PROCEDURE sv_proc1()
  RETURNS VARCHAR
  LANGUAGE JAVASCRIPT
  EXECUTE AS CALLER
  AS
  $$
    var rs = snowflake.execute( {sqlText: "SET SESSION_VAR_ZYXW = 51"} );

    var rs = snowflake.execute( {sqlText: "SELECT 2 * $SESSION_VAR_ZYXW"} );
    rs.next();
    var MyString = rs.getColumnValue(1);

    rs = snowflake.execute( {sqlText: "UNSET SESSION_VAR_ZYXW"} );

    return MyString;
  $$
  ;

CALL sv_proc1();

-- This fails because SESSION_VAR_ZYXW is no longer defined.
SELECT $SESSION_VAR_ZYXW;
```

Note

If you program in the C language (or similar languages such as Java), note that session variables you set
inside a stored procedure are not like the local variables in C that disappear when a C function
finishes running. Isolating your stored procedure from its environment requires more effort in SQL than in C.

## Owner’s rights stored procedures

Owner’s rights stored procedures adhere to the following rules within a session:

- Run with the privileges of the owner, not the privileges of the caller.

  Tip

  If you need an owner’s rights stored procedure to perform actions on a table, view, or function that the caller has the
  privileges to access, you can have the caller pass a reference to that table, view, or function.

  For details, refer to [Stored Procedures Calling References](stored-procedures-calling-references).
- Inherit the current warehouse of the caller.
- Use the database and schema that the stored procedure is created in, not the database and schema that the
  caller is currently using.
- Cannot access most caller-specific information. For example:

  - Cannot view, set, or unset the caller’s session variables.
  - Can use only a subset of session parameters set by the caller. For example, SQL commands that output date values can use the
    [DATE\_OUTPUT\_FORMAT](/sql-reference/parameters#label-date-output-format) parameter that is set for the caller’s session).

    For the list of these parameters, see [Understanding the effects of a caller’s session parameters on an owner’s rights procedure](#label-stored-procedure-session-parameters).
  - Cannot set or unset any of the caller’s session parameters.
- Do not allow non-owners to view information about the procedure from the
  [PROCEDURES](/sql-reference/info-schema/procedures) view.

Restrictions on [session variables](#label-stored-procedure-session-variables) and
[session parameters](#label-stored-procedure-session-parameters) are described in more detail below.

### Session variables for owner’s rights procedures

A stored procedure does not have access to [SQL variables](/sql-reference/session-variables) created outside the stored
procedure. This restriction prevents a stored procedure written or owned by one user from reading SQL
variables created by another user (the stored procedure caller).

If your stored procedure needs values that are stored in the current session’s SQL variables, then the values in those
variables should be passed as explicit arguments to the stored procedure. For example:

Copy code

```
SET PROVINCE = 'Manitoba';
CALL MyProcedure($PROVINCE);
```

### Understanding the effects of a caller’s session parameters on an owner’s rights procedure

The value of a session [parameter](/sql-reference/parameters) can affect the behavior of commands and functions. For
example, commands that output date values use the format specified by the [DATE\_OUTPUT\_FORMAT](/sql-reference/parameters#label-date-output-format) session parameter.

In a caller’s session, the caller can set or override a session parameter. In a caller’s rights stored procedure, session
parameters can affect the execution of any queries and expressions executed inside the procedure. For example, the
[TIMESTAMP\_OUTPUT\_FORMAT](/sql-reference/parameters#label-timestamp-output-format) parameter affects the output format of a child query like
`select current_timestamp::string`.

However, for an owner’s rights stored procedure, the values from the caller’s session are used only for the following
parameters:

- AUTOCOMMIT
- BINARY\_INPUT\_FORMAT
- BINARY\_OUTPUT\_FORMAT
- DATE\_INPUT\_FORMAT
- DATE\_OUTPUT\_FORMAT
- ENABLE\_UNLOAD\_PHYSICAL\_TYPE\_OPTIMIZATION
- ERROR\_ON\_NONDETERMINISTIC\_MERGE
- ERROR\_ON\_NONDETERMINISTIC\_UPDATE
- JDBC\_TREAT\_DECIMAL\_AS\_INT
- JSON\_INDENT
- LOCK\_TIMEOUT
- MAX\_CONCURRENCY\_LEVEL
- ODBC\_USE\_CUSTOM\_SQL\_DATA\_TYPES
- PERIODIC\_DATA\_REKEYING
- QUERY\_TAG
- QUERY\_WAREHOUSE\_NAME
- ROWS\_PER\_RESULTSET
- STATEMENT\_QUEUED\_TIMEOUT\_IN\_SECONDS
- STATEMENT\_TIMEOUT\_IN\_SECONDS
- STRICT\_JSON\_OUTPUT
- TIMESTAMP\_DAY\_IS\_ALWAYS\_24H
- TIMESTAMP\_INPUT\_FORMAT
- TIMESTAMP\_LTZ\_OUTPUT\_FORMAT
- TIMESTAMP\_NTZ\_OUTPUT\_FORMAT
- TIMESTAMP\_OUTPUT\_FORMAT
- TIMESTAMP\_TYPE\_MAPPING
- TIMESTAMP\_TZ\_OUTPUT\_FORMAT
- TIMEZONE
- TIME\_INPUT\_FORMAT
- TIME\_OUTPUT\_FORMAT
- TRANSACTION\_ABORT\_ON\_ERROR
- TRANSACTION\_DEFAULT\_ISOLATION\_LEVEL
- TWO\_DIGIT\_CENTURY\_START
- UNSUPPORTED\_DDL\_ACTION
- USE\_CACHED\_RESULT
- WEEK\_OF\_YEAR\_POLICY
- WEEK\_START

Note

This list might change over time.

For other parameters (not listed above):

- The value of the owner’s account-level parameter is used.
- If the account-level parameter is not set for owner’s account, the default value for the account parameter is used.

This restriction is in place to avoid potential issues that could occur if an owner’s rights stored procedure used the caller’s
session parameters. For example:

- If the author (owner) of a stored procedure has set a specific session parameter, but callers of the stored procedure have not
  set that parameter, the stored procedure might fail or behave differently when called by users other than the author.
- If a stored procedure were allowed to use the value of any session parameter set by the caller, the owner of a stored procedure
  might be able to determine those values without the caller’s knowledge.

## Additional restrictions on owner’s rights stored procedures

Owner’s rights stored procedures have several additional restrictions, besides the restrictions related to
session variables and session parameters. These restrictions affect the following:

- The built-in functions that can be called from inside a stored procedure.
- Ability to execute ALTER USER statements.
- Monitoring stored procedures at execution time.
- LIST command.
- The types of SQL statements that can be called from inside a stored procedure.

The following sections explain these restrictions in more detail.

Note

Most restrictions on an owner’s rights stored procedure apply to all callers, including the owner.

### Restrictions on built-in functions

If a stored procedure is created as an owner’s rights stored procedure, then callers (other than the owner)
cannot call the following built-in functions:

- GET\_DDL()

  This prevents users other than the stored procedure owner from viewing the source code of the stored procedure.
- SYSTEM$ENABLE\_BEHAVIOR\_CHANGE\_BUNDLE()
- SYSTEM$DISABLE\_BEHAVIOR\_CHANGE\_BUNDLE()

### ALTER USER

In the handler for an owner’s rights procedure, you *cannot* execute [ALTER USER](/sql-reference/sql/alter-user) statements that implicitly
use the current user for the session.

However, you *can* execute ALTER USER statements that explicitly identify the user, as long as the user is not the current user.

### Monitoring stored procedures at execution time

Neither the owner nor the caller of an owner’s rights stored procedure necessarily has privileges to monitor
execution of the stored procedure.

A user with the WAREHOUSE MONITOR privilege can monitor execution of the individual warehouse-related SQL
statements within that stored procedure. Most queries and DML statements are warehouse-related statements.
DDL statements, such as CREATE, ALTER, etc. do not use the warehouse and cannot be monitored as part of
monitoring stored procedures.

### SHOW and DESCRIBE commands

An owner’s rights stored procedure can use any SHOW or DESCRIBE command that
does not return information about the current session or rely on the current user.

The following SHOW commands read from the current session,
and as a result are not permitted:

- SHOW PARAMETERS [ { IN | FOR } SESSION ]
- SHOW VARIABLES

The following commands return output that depend on the current user, and
as a result are not permitted:

- SHOW GRANTS commands that do not have an IN, ON, TO, or OF clause. Using SHOW GRANTS
  without one of these clauses implicitly references the current user.
- SHOW LOCKS
- SHOW TRANSACTIONS
- SHOW DELEGATED AUTHORIZATIONS

### LIST command

You can’t use the LIST command in the [Snowflake Scripting](/developer-guide/stored-procedure/stored-procedures-snowflake-scripting)
or [JavaScript](/developer-guide/stored-procedure/stored-procedures-javascript) handler code of an owner’s rights stored procedure,
regardless of the procedure’s owner and caller. You *can* use LIST when the procedure handler is written in one of the other handler
languages.

### Restrictions on SQL statements

Although caller’s rights stored procedures can execute any SQL statement that the caller has sufficient privileges
to execute outside a stored procedure, owner’s rights stored procedures can call only a subset of SQL statements.

The following SQL statements can be called from inside an owner’s rights stored procedure:

- SELECT
- DML
- DDL (see above for restrictions on the ALTER USER statement)
- GRANT/REVOKE
- Variable assignment
- DESCRIBE and SHOW (see limitations documented above)
- LIST (see limitations documented above)

Other SQL statements cannot be called from inside an owner’s rights stored procedure.

## Nested stored procedures with different rights

If an owner’s rights stored procedure is called by a caller’s rights stored procedure, or vice-versa, the following
rules apply:

- A stored procedure behaves as a caller’s rights stored procedure if and only if the procedure and the entire
  call hierarchy above it are caller’s rights stored procedures.
- An owner’s rights stored procedure always behaves as an owner’s rights stored procedure, no matter where it was
  called from.
- Any stored procedure called directly or indirectly from an owner’s rights stored procedure behaves as an owner’s
  rights stored procedure.

## Choosing between owner’s rights and caller’s rights

Create a stored procedure as an owner’s rights stored procedure if all of the following are true:

- You want to delegate a task(s) to another user(s) who will run with the owner’s privileges, not the caller’s own
  privileges.

  For example, if you want a user without DELETE privilege on a table to be able to call a stored procedure that deletes old data,
  but not current data, then you probably want to use an owner’s rights stored procedure. That procedure will contain a DELETE
  statement that includes a filter (a WHERE clause) to control which data can be deleted through the filter.

  Tip

  If you need an owner’s rights stored procedure to perform actions on a table, view, or function that the caller has the
  privileges to access, you can have the caller pass a reference to that table, view, or function.

  For details, refer to [Stored Procedures Calling References](stored-procedures-calling-references).
- The restrictions in owner’s rights stored procedures will not prevent the stored procedure from working properly.

Create a stored procedure as a caller’s rights stored procedure if the following are true:

- The stored procedure operates only on objects that the caller owns or has the required privileges on.
- The restrictions in owner’s rights stored procedures would prevent the stored procedure from working.
  For example, use a caller’s rights procedure if the caller of the stored procedure needs to use that caller’s
  environment (e.g. session variables or account parameters).

If a particular procedure can work correctly with either caller’s rights or owner’s rights, then the following rule
might help you choose which rights to use:

- If a procedure is an owner’s rights procedure, the caller does not have the privilege to view the code in
  the stored procedure (unless the caller is also the owner). If you want to prevent callers from
  viewing the source code of the procedure, then create the procedure as an owner’s rights procedure.
  Conversely, if you want callers to be able to read the source code, then create the procedure as a caller’s
  rights prodecure.
