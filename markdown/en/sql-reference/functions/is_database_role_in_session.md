Categories:
:   [Context functions](/sql-reference/functions-context) (Session Object)

# IS\_DATABASE\_ROLE\_IN\_SESSION

Verifies whether the database role is in the user’s active primary or secondary role hierarchy for the current session or if the specified
column contains a database role that is in the user’s active primary or secondary role hierarchy for the current session.

See also:
:   [IS\_ROLE\_IN\_SESSION](/sql-reference/functions/is_role_in_session), [IS\_APPLICATION\_ROLE\_IN\_SESSION](/sql-reference/functions/is_application_role_in_session)

## Syntax

**Literal — specify a database role directly:**

Copy code

```
IS_DATABASE_ROLE_IN_SESSION( '<string_literal>' )
```

**Nonliteral — specify a column:**

> Copy code
>
> ```
> IS_DATABASE_ROLE_IN_SESSION( <column_name> )
> ```

## Arguments

`'string_literal'`
:   The name of the database role.

    Specify the relative name of the database role. The function evaluates to `False` if you specify the fully qualified name.

`column_name`
:   The column name in a table or view.

## Returns

`True`
:   - For a literal argument (database role name), the current user’s active
      [primary role or secondary roles](/user-guide/security-access-control-overview#label-access-control-role-enforcement) in the session inherits the privileges of the
      specified database role.
    - For a nonliteral argument (column name), Snowflake evaluates each row in the table and returns a row that contains a value that
      specifies a database role in the user’s current session. Each row corresponds to a database role name that originates from the
      database in use or the specified database in a query.

`False`
:   - For a literal argument, the specified database role is not in the role hierarchy of the current user’s primary role or secondary
      roles.
    - For a nonliteral argument, Snowflake does not return a row if the database role is not in the table column for the database in use or
      the database specified in a query.
    - Specifying the fully qualified name of a database role in the format `database_name.database_role_name`. Use the relative
      name instead, `database_role_name`.

## Usage notes

These notes only apply to the IS\_DATABASE\_ROLE\_IN\_SESSION function:

- Use this table to predict the evaluation of the function when the function argument is a string literal:

  | Context | Evaluation |
  | --- | --- |
  | Query. | Session database. |
  | Table or view definition with WHERE clause. | Depends on the following:  - If you have a database in use and you use the relative name of the table or view, the context is the database in use   (session database). - If you specify the fully-qualified name of the table or view, the context is the database that contains the table or view. |
  | Protected table or view. | Database containing the table or view. |
  | Owner’s Rights stored procedure. | Database containing the stored procedure. |
  | Caller’s Rights stored procedure. | Session database. |
  | UDF | Database containing the protected table or view.  If the UDF is not called in a policy, the function evaluates to the database that contains the UDF. |

  Expand

  Show lessSee more
- A database role becomes active in the role hierarchy when the database containing the database role is in use or when querying a table in
  the same database that contains the database role.
- When you specify this function in the `body` of a data access policy, such as a masking or row access policy, the function uses
  the database and schema of the protected table.

  For example, if you add a row access policy to the `hr.tables.empl_info` table, the function searches for its argument, the
  database role name or the column name, in the `hr` database because that database contains the protected table.
- You should avoid query structures that require Snowflake to create an inline view. In this context, an inline view is a temporary view
  that Snowflake creates to determine the query result. For example, if your query calls this function and you specify a WITH clause at the
  beginning of the query or specify a subquery in the FROM clause, Snowflake returns an error:

  ```
  Could not resolve the database for IS_DATABASE_ROLE_IN_SESSION({})
  ```

  Where `{}` is a placeholder for the function argument in your query. The reason for the error is that Snowflake does not have
  enough information to evaluate the context of the function argument. To resolve the error message, simplify your query, such as removing
  the WITH clause or removing the subquery in the FROM clause.
- When the [user property](/sql-reference/sql/create-user) `DEFAULT_SECONDARY_ROLES` value is `ALL`, the function returns
  `True` if any account role granted to the user inherits the privileges of the specified database role.
- When using this function in the condition of a masking policy or row access policy that protects shared data, ensure the database
  containing the policy and the policy-protected data are both shared to the consumer account. The policy and the policy-protected data can
  be in the same database or in different databases. For details, see [Share data protected by a policy](/user-guide/data-sharing-policy-protected-data).

These notes apply to both the IS\_DATABASE\_ROLE\_IN\_SESSION and IS\_ROLE\_IN\_SESSION functions:

- Use one syntax.
- Name syntax:

  - Only one role name can be passed as an argument.
  - The argument must be a string and use the same casing as how the role is stored in Snowflake. For details, see
    [Identifier requirements](/sql-reference/identifiers-syntax).
- Column syntax:

  - Only one column can be passed as an argument.
  - The column must have a [STRING](/sql-reference/data-types-text#label-character-datatypes) data type.
  - Specify the column as one of the following:
    - `column_name`
    - `table_name.column_name`
    - `schema_name.table_name.column_name`
    - `database_name.schema_name.table_name.column_name`
- Virtual columns:

  A virtual column, which contains the result of a calculated value from an expression rather than the calculated value being stored in the
  table, is not supported.

  Copy code

  ```
  SELECT IS_ROLE_IN_SESSION(UPPER(authz_role)) FROM t1;
  ```

  A virtual column is supported only when the expression has an alias for the column name:

  Copy code

  ```
  CREATE VIEW v2 AS
  SELECT
    authz_role,
    UPPER(authz_role) AS upper_authz_role
  FROM t2;

  SELECT IS_ROLE_IN_SESSION(upper_authz_role) FROM v2;
  ```
- Policies:

  If you use these functions with a [masking policy](/user-guide/security-column-intro) or
  [row access policy](/user-guide/security-row-intro), verify that your Snowflake account is Enterprise Edition or higher.

  Snowflake recommends using this function when the policy conditions need to evaluate role hierarchy and inherited privileges.
- Result cache:

  If you use this function in a masking policy or row access policy and neither the policy nor the table or column protected by the policy
  change from a previous query, you can use the [RESULT\_SCAN](/sql-reference/functions/result_scan) function to return the results of a query on
  the protected table. The result cache applies when using the nonliteral syntax only.
- These functions cannot be used in the materialized view definition because the functions are not deterministic and Snowflake cannot
  determine what data to materialize.

## Examples

Verify if the privileges granted to a specified role are inherited by the current role in the session:

Copy code

```
SELECT IS_DATABASE_ROLE_IN_SESSION('R1');
```

```
+-----------------------------------+
| IS_DATABASE_ROLE_IN_SESSION('R1') |
+-----------------------------------+
| True                              |
+-----------------------------------+
```

Return database role values for the column named ROLE\_NAME:

> Copy code
>
> ```
> SELECT *
> FROM myb.s1.t1
> WHERE IS_DATABASE_ROLE_IN_SESSION(role_name);
> ```

For additional examples related to secure data sharing, see [Share data protected by a policy](/user-guide/data-sharing-policy-protected-data).
