# Working with stored procedures

Stored procedures enable users to create modular code that can include complex business logic by combining multiple
SQL statements with procedural logic.

Note

To both create and call an anonymous procedure, use [CALL (with anonymous procedure)](/sql-reference/sql/call-with). Creating and calling an anonymous procedure does
not require a role with CREATE PROCEDURE schema privileges.

## Naming conventions for stored procedures

You must name procedures according to conventions enforced by Snowflake.

For more information, see [Naming and overloading procedures and UDFs](/developer-guide/udf-stored-procedure-naming-conventions).

## Transaction management

Stored procedures are not atomic; if one statement in a stored procedure fails, the other statements in the stored
procedure are not necessarily rolled back.

You can use stored procedures with transactions to make a group of statements atomic. For details, see
[Stored procedures and transactions](/sql-reference/transactions#label-transactions-stored-procedures-and-transactions).

## General tips

### Symmetric code

If you are familiar with programming in assembly language, you might
find the following analogy helpful. In assembly language, functions
often create and undo their environments in a symmetric way. For example:

> Copy code
>
> ```
> -- Set up.
> push a;
> push b;
> ...
> -- Clean up in the reverse order that you set up.
> pop b;
> pop a;
> ```

You might want to use this approach in your stored procedures:

- If a stored procedure makes temporary changes to your session, then that procedure should undo those changes before returning.
- If a stored procedure utilizes exception handling or branching, or other logic that might impact which statements
  are executed, you need to clean up whatever you created, regardless of which branches you take during a particular
  invocation.

For example your code might look similar to the pseudo-code shown below:

> Copy code
>
> ```
> CREATE PROCEDURE f() ...
>     $$
>     set x;
>     set y;
>     try  {
>        set z;
>        -- Do something interesting...
>        ...
>        unset z;
>        }
>     catch  {
>        -- Give error message...
>        ...
>        unset z;
>        }
>     unset y;
>     unset x;
>     $$
>     ;
> ```

## Calling a stored procedure

You call a stored procedure using a SQL command. For more information on calling stored procedures, see
[Calling a stored procedure](/developer-guide/stored-procedure/stored-procedures-calling).

## Selecting from a stored procedure

You call a stored procedure in the FROM clause of a SELECT statement. For more information on selecting from a stored procedure, see
[Selecting from a stored procedure](/developer-guide/stored-procedure/stored-procedures-selecting-from).

## Privileges

Stored Procedures utilize two types of privileges:

- Privileges directly on the stored procedure itself.
- Privileges on the database objects (e.g. tables) that the stored procedure accesses.

### Privileges on stored procedures

Similar to other database objects (tables, views, UDFs, etc.), stored procedures are
owned by a role and have one or more privileges that can be granted to other roles.

Currently, the following privileges apply to stored procedures:

- USAGE
- OWNERSHIP

For a role to use a stored procedure, the role must either be the owner or
have been granted USAGE privilege on the stored procedure.

### Privileges on the database objects accessed by the stored procedure

This subject is covered in [Understanding caller’s rights and owner’s rights stored procedures](/developer-guide/stored-procedure/stored-procedures-rights).

## Stored procedure considerations

- Although stored procedures allow nesting and recursion, the current maximum stack depth
  of nested calls for user-defined stored procedures is 16 (including the top-level
  stored procedure), and can be less if individual stored procedures in the call chain
  consume large amounts of resources.
- In rare cases, calling too many stored procedures at the same time can cause a deadlock.

## Working with stored procedures in Snowsight

You can work with stored procedures in SQL or in Snowsight.

For any stored procedure in Snowflake, you can open **Catalog** » **Database Explorer** and search for or browse to the stored procedure.
Select the stored procedure to review details and manage the procedure.

You must have the [relevant privileges](#label-access-control-privileges-for-stored-procedures) to access and manage the
stored procedure in Snowsight.

### Explore stored procedure details in Snowsight

After opening a stored procedure in Snowsight, you can do the following:

- Identify when the procedure was created, and any comment on the procedure.
  You can hover over the time details to see the exact creation date and time.
- Review additional details about the stored procedure, including:

  - Arguments that the stored procedure takes, if applicable.
  - The data type of the result of the procedure.
  - Whether the procedure is an aggregate function.
  - Whether the procedure is a secure function.
  - Whether the procedure is a table function.
  - The language in which the stored procedure is written. For example, JavaScript.
- Review the SQL definition of the stored procedure in the **Procedure definition** section.
- Review the roles with privileges on the stored procedure in the **Privileges** section.

### Manage a stored procedure in Snowsight

You can perform the following basic management tasks for a stored procedure in Snowsight:

- To edit the stored procedure name or add a comment, select [![More options](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png) » **Edit**.
- To drop the stored procedure, select [![More options](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png) » **Drop**.
- To transfer ownership of the stored procedure to another role, select [![More options](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png) » **Transfer Ownership**

### SQL injection

Stored procedures can dynamically create a SQL statement and execute it. However, this can allow
SQL injection attacks, particularly if you create the SQL statement using input from
a public or untrusted source.

You can minimize the risk of SQL injection attacks by binding parameters rather than concatenating text. For an
example of binding variables, see [Binding variables](/developer-guide/stored-procedure/stored-procedures-javascript#label-stored-procedures-binding-variables).

If you choose to use concatenation, you should check inputs carefully when
constructing SQL dynamically using input from public sources.
You might also want to take other precautions, such as querying using a
role that has limited privileges (e.g. read-only access, or access to
only certain tables or views).

For more information about SQL injection attacks, see
[SQL injection](https://en.wikipedia.org/wiki/SQL_injection) (in Wikipedia).

## Design tips for stored procedures

Here are some tips for designing a stored procedure:

- What resources, for example, tables, does this stored procedure need?
- What privileges are needed?

  Think about which database objects will be accessed, and which roles will run your stored
  procedure, and which privileges those roles will need.

  If the procedure should be a caller’s rights stored procedure, then
  you might want to create a role to run that specific procedure, or any of a
  group of related procedures. You can then grant any required privileges to that role, and
  then grant that role to appropriate users.
- Should the stored procedure run with caller’s rights or owner’s rights? For more information on this topic, see
  [Understanding caller’s rights and owner’s rights stored procedures](/developer-guide/stored-procedure/stored-procedures-rights).
- How should the procedure handle errors, for example what should the procedure do if a required table is missing,
  or if an argument is invalid?
- Should the stored procedure log its activities or errors, for example by writing to a log table?
- See also the discussion about when to use a stored procedure vs. when to use a UDF:
  [Choosing whether to write a stored procedure or a user-defined function](/developer-guide/stored-procedures-vs-udfs).

## Documenting stored procedures

Stored procedures are usually written to be re-used, and often to be shared. Documenting stored procedures
can make stored procedures easier to use and easier to maintain.

Below are some general recommendations for documenting stored procedures.

Typically, there are at least two audiences who want to know about a stored procedure:

- Users/callers.
- Programmers/authors.

For users (and programmers), document each of the following:

> - The name of the stored procedure.
> - The “location” of the stored procedure (database and schema).
> - The purpose of the stored procedure.
> - The name, data type, and meaning of each input parameter.
> - The name, data type, and meaning of the return value. If the return value is a complex type, such as a VARIANT
>   that contains sub-fields, document those sub-fields.
> - If the stored procedure relies on information from its environment, for example session variables or session
>   parameters, document the names, purposes, and valid values of those.
> - Errors returned, exceptions thrown, etc.
> - Roles or privileges required in order to run the procedure. (For more on this topic, see the discussion of
>   roles in [Design tips for stored procedures](#label-design-tips-for-stored-procedures).)
> - Whether the procedure is a caller’s rights procedure or an owner’s rights procedure.
> - Any prerequisites, for example tables that must exist before the procedure is called.
> - Any outputs (besides the return value), for example new tables that are created.
> - Any “side-effects”, for example changes in privileges, deletions of old data, etc. Most stored procedures
>   (unlike functions) are called specifically for their side effects, not their return values, so make sure to
>   document those effects.
> - If cleanup is required after running the stored procedure, document that cleanup.
> - Whether the procedure can be called as part of a multi-statement transaction (with AUTOCOMMIT=FALSE), or whether
>   it should be run outside a transaction (with AUTOCOMMIT=TRUE).
> - An example of a call and an example of what is returned.
> - Limitations (if applicable). For example, suppose that the procedure reads a table and returns a VARIANT that
>   contains information from each row of the table. It is possible for the VARIANT to grow larger than the
>   maximum legal size of a VARIANT, so you might need to give the caller some idea of the maximum number of rows
>   in the table that the procedure accesses.
> - Warnings (if applicable).
> - Troubleshooting tips.

For programmers:

> - The author(s).
> - Explain why the procedure was created as a caller’s rights procedure or an owner’s rights procedure – the reason
>   might not be obvious.
> - Stored procedures can be nested, but there is a limit to the depth of the nesting. If your stored procedure
>   calls other stored procedures, and is itself likely to be called by other stored procedures, then you
>   might want to specify the maximum known depth of your stored procedure’s call stack so that callers have
>   some idea of whether calling your stored procedure might exceed the maximum call stack depth.
> - Debugging tips.

The location and format of this information are up to you. You might store the information in HTML format in an
internal web site, for example. Before deciding where to store it, think about where your organization stores similar
information for other products, or similar information for other Snowflake features, such as views,
user-defined functions, etc.

Other tips:

- Include comments in the source code, as you should for almost any piece of source code.

  - Remember that reverse engineering meaning from code is difficult. Describe not only how your algorithm works,
    but also the purpose of that algorithm.
- Stored procedures allow an optional COMMENT that can be specified with the `CREATE PROCEDURE` or
  `ALTER PROCEDURE` statement. Other people can read this comment by running the `SHOW PROCEDURES` command.
- If practical, consider keeping a master copy of each stored procedure’s CREATE PROCEDURE command in a
  source code control system. Snowflake’s Time Travel feature does not apply to stored procedures, so looking up
  old versions of stored procedures must be done outside Snowflake. If a source code control system is not available,
  you can partly simulate one by storing the CREATE PROCEDURE commands in a VARCHAR field in a table, and adding each
  new version (without replacing the older version(s)).
- Consider using a naming convention to help provide information about stored procedures.
  For example, a prefix or suffix in the name might indicate whether the procedure is a caller’s rights stored
  procedure or an owner’s rights stored procedure. (E.g. you could use `cr_` as a prefix for Caller’s Rights.)
- To see the data types and order of the input arguments, as well as the comment, you can use the SHOW PROCEDURES
  command. Remember, however, that this shows only the names and data types of the arguments; it does not explain
  the arguments.
- If you have appropriate privileges, you can use the DESCRIBE PROCEDURE command to see:

  - The names and data types of the arguments.
  - The body of the procedure, and whether the procedure executes as owner or caller.
  - The data type of the return value.
  - Other useful information.
