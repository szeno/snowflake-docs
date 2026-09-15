# Protecting Sensitive Information with Secure UDFs and Stored Procedures

To help ensure that sensitive information is concealed from users who should not have access to it, you can use the SECURE keyword when
creating a user-defined function (UDF) and stored procedure.

This topic describes how you can:

- [Limit the visibility of UDF or stored procedure definitions](#label-secure-limiting-visibility-definition).
- [Limit the visibility of sensitive data that can be exposed by UDFs](#label-secure-limiting-visibility-data).

Note

In some cases, error messages related to secure functions might be redacted. For more information, see
[Secure objects: Redaction of information in error messages](/release-notes/bcr-bundles/un-bundled/bcr-1858).

## Limiting the Visibility of a UDF or Procedure Definition

For a UDF or stored procedure, you can prevent users from seeing definition specifics. When you specify that the UDF or procedure is
secure, these details are visible only to authorized users – in other words, to users who are granted a role that owns the function.

For example, for a secure function or procedure, information omitted for unauthorized users includes its:

- Body (the handler code that comprises its logic)
- List of imports
- Handler name
- Packages list

Unauthorized users will still be able to see information that includes its:

- Parameter types
- Return type
- Handler language
- Null handling
- Volatility

For more on granting roles, see [GRANT ROLE](/sql-reference/sql/grant-role) and [Overview of Access Control](/user-guide/security-access-control-overview).

With a function or procedure that is secure, an unauthorized user – one who has *not* been granted a role that owns the function or
procedure – may not view the function or procedure definition when using any of the following:

- For UDFs

  - [SHOW FUNCTIONS](/sql-reference/sql/show-functions) and [SHOW USER FUNCTIONS](/sql-reference/sql/show-user-functions) commands
  - [DESCRIBE FUNCTION](/sql-reference/sql/desc-function) command
  - [FUNCTIONS](/sql-reference/info-schema/functions) Information Schema view
- For procedures

  - [SHOW PROCEDURES](/sql-reference/sql/show-procedures) command
  - [DESCRIBE PROCEDURE](/sql-reference/sql/desc-procedure) command
  - [PROCEDURES](/sql-reference/info-schema/procedures) Information Schema view
- For both

  - [Query Profile](/user-guide/ui-snowsight-activity) (in the web interface)
  - [GET\_DDL](/sql-reference/functions/get_ddl) utility function

Note that functions and procedures whose handlers are written in Java, Python, or Scala allow the IMPORTS clause, which imports code or
data files from Snowflake stages. Using the SECURE keyword does *not* have any effect on the visibility of or access to those stages.

In addition, for functions and procedures whose handlers are written in Java, Python, or Scala, making the functions and procedures secure
ensures that they are executed in separate sandboxes, such that no resources are shared between them.

For more information on using the SECURE keyword, see [Creating a Secure UDF or Stored Procedure](#label-secure-udf-procedure-creating).

## Limiting the Visibility of a UDF’s Sensitive Data

In UDFs, you can prevent users from seeing data that should be hidden by making the UDF secure. You do this by using the SECURE keyword
when creating or altering the UDF.

Define a UDF as secure when it is specifically designated for data privacy (in other words, to limit access to sensitive data that should
not be exposed to all users of the underlying tables).

You should not make a UDF secure when it is defined for query convenience, such as when it is created for simplifying querying data
for which users do not need to understand the underlying data representation. This is because the Snowflake query optimizer, when evaluating
secure UDFs, bypasses the optimizations used for regular UDFs. This might reduce query performance for secure UDFs.

To limit visibility into a UDF’s underlying data, use the SECURE keyword when creating or altering it. For more information, see
[Creating a Secure UDF or Stored Procedure](#label-secure-udf-procedure-creating).

### How Data Can Become Visible

Some of the internal optimizations for UDFs, including an optimization called [pushdown](/developer-guide/pushdown-optimization#label-secure-objects-pushdown), require
access to the underlying data in the base tables. This access might allow data that is hidden from users of the UDF to be exposed
indirectly through programmatic methods. In certain situations, a user might be able to deduce information about rows that the user cannot
see directly.

Secure UDFs do not use these optimizations, ensuring that users do not have even indirect access to the underlying data. For more
information on pushdown, see [Pushdown Optimization and Data Visibility](/developer-guide/pushdown-optimization).

Tip

When deciding whether to use a secure UDF, you should consider the purpose of the UDF and weigh the trade-off between data privacy/security
and query performance.

Also, if your data is sensitive enough that you decide that accesses via one type of object (such as UDFs) should be secure, then you
should strongly consider ensuring that accesses via other types of objects (such as views) are also secure.

For example, if you only allow secure UDFs to access a given table, then any views that you allow to access the same table probably also should
be secure.

### How Secure UDFs Protect Data

As described in [Pushdown Optimization and Data Visibility](/developer-guide/pushdown-optimization), the pushdown optimization can re-order the filters that determine how a
query is processed. If the optimization re-orders the filters in a way that allows a general filter to run before the appropriate filter(s)
used to secure data are applied, underlying details could be exposed. Therefore, the solution is to prevent the optimizer from pushing down
certain types of filters (more generally, to prevent the optimizer from using certain types of optimizations, including but not limited to
filter pushdown) if those optimizations are not safe.

Declaring a UDF as “secure” tells the optimizer to not push down certain filters (more generally, not to use certain optimizations). However,
preventing certain types of optimizations can impact performance.

### Best Practices for Protecting Access to Sensitive Data

Secure UDFs prevent users from possibly being exposed to data from rows of tables that are filtered by the function. However,
there are still ways that a data owner might inadvertently expose information about the underlying data if UDFs are not
constructed carefully. This section describes some potential pitfalls to avoid.

#### Avoid Exposing Sequence-Generated Column Values

A common practice for generating surrogate keys is to use a sequence or auto-increment column. If these keys are exposed to users
who do not have access to all of the underlying data, then a user might be able to guess details of the underlying data distribution.

For example, suppose that we have a function `get_widgets_function()` that exposes the ID column. If ID is generated from a sequence,
then a user of `get_widgets_function()` could deduce the total number of widgets created between the creation timestamps of two
widgets that the user has access to. Consider the following query and result:

Copy code

```
SELECT * FROM TABLE(get_widgets_function()) ORDER BY created_on;

------+-----------------------+-------+-------+-------------------------------+
  ID  |         NAME          | COLOR | PRICE |          CREATED_ON           |
------+-----------------------+-------+-------+-------------------------------+
...
 315  | Small round widget    | Red   | 1     | 2017-01-07 15:22:14.810 -0700 |
 1455 | Small cylinder widget | Blue  | 2     | 2017-01-15 03:00:12.106 -0700 |
...
```

Based on the result, the user might suspect that 1139 widgets (`1455 - 315`) were created between January 7 and January 15. If this
information is too sensitive to expose to users of a function, you can use any of the following alternatives:

- Do not expose the sequence-generated column as part of the function.
- Use randomized identifiers (such as those generated by [UUID\_STRING](/sql-reference/functions/uuid_string)) instead of sequence-generated values.
- Programmatically obfuscate the identifiers.

#### Limit Visibility into Scanned Data Size

For queries containing secure functions, Snowflake does not expose the amount of data scanned (either in terms of bytes or micro-partitions)
or the total amount of data. This is to protect the information from users who have access to only a subset of the data.

However, users might still be able to make observations about the quantity of underlying data based on performance characteristics of
queries. For example, a query that runs twice as long might process twice as much data. While any such observations are approximate at best,
in some cases it might be undesirable for even this level of information to be exposed.

In such cases, you should materialize data per user/role instead of exposing functions on the base data to users. In the case of the
`widgets` table described in this topic, a table would be created for each role that has access to widgets. Each of those tables would
contains only the widgets accessible by that role, and a role would be granted access to its table. This is much more cumbersome than using
a single function, but for extremely high-security situations, this might be warranted.

#### Authorize Base Table Access for Users from a Specific Account

When using secure UDFs with [data sharing](/user-guide/data-sharing-gs), the [CURRENT\_ACCOUNT](/sql-reference/functions/current_account) function can
be used to authorize users from a specific account to access rows in a base table.

> Note
>
> When using the [CURRENT\_ROLE](/sql-reference/functions/current_role) and [CURRENT\_USER](/sql-reference/functions/current_user) functions with secure
> UDFs that will be shared with Snowflake accounts, Snowflake returns a NULL value for these functions. The reason is that the owner
> of the data being shared does not typically control the users or roles in the account with which the UDF is being shared.

#### Secure UDFs and Masking Policies

If using a UDF, whether or not the UDF is a secure UDF, in a [masking policy](/sql-reference/sql/create-masking-policy), ensure the
data type of the column, UDF, and masking policy match.

For more information, see [User-defined functions in a masking policy](/user-guide/security-column-intro#label-security-column-intro-udf-policy).

## Creating a Secure UDF or Stored Procedure

You can make a UDF or procedure secure by using the SECURE keyword when creating or altering it.

To create or convert a UDF so that it’s secure, specify SECURE when using the following:

- [CREATE FUNCTION](/sql-reference/sql/create-function)
- [ALTER FUNCTION](/sql-reference/sql/alter-function)

To create a procedure so that it’s secure, specify SECURE when using the following:

- [CREATE PROCEDURE](/sql-reference/sql/create-procedure)

## Determining if a UDF or Procedure is Secure

You can determine if a function or procedure is secure by using the SHOW FUNCTIONS or SHOW PROCEDURES command. The commands return a
table with an IS\_SECURE column whose value is `Y` for secure and `N` for not secure.

Code in the following example returns a table of properties for a `MYFUNCTION` function.

Copy code

```
SHOW FUNCTIONS LIKE 'MYFUNCTION';
```

## Viewing Secure Function Details in Query Profile

The internals of a secure function are not exposed in [Query Profile](/user-guide/ui-snowsight-activity) (in the web interface). This is
the case even for the owner of the secure function, since non-owners might have access to an owner’s Query Profile.
