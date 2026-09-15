Categories:
:   [Context functions](/sql-reference/functions-context) (Session Object)

# IS\_ROLE\_IN\_SESSION

Verifies whether the specified account role is in the currently active primary or secondary role hierarchy.

This function looks only at the *currently* active set of roles, not at the roles activated in the session. The currently
active roles can differ from the session roles, for example, when executing an owner’s rights procedure or a Streamlit.

See also:
:   [Advanced Column-level Security topics](/user-guide/security-column-advanced)

## Syntax

**Literal — specify a role directly:**

> Copy code
>
> ```
> IS_ROLE_IN_SESSION( '<string_literal>' )
> ```

**Expression — specify a role expression:**

> Copy code
>
> ```
> IS_ROLE_IN_SESSION( <expr> )
> ```

**Column — specify a column:**

> Copy code
>
> ```
> IS_ROLE_IN_SESSION( <column_name> )
> ```

## Arguments

`'string_literal'`
:   The name of the role.

`expr`
:   An expression that returns the name of the role.

`column_name`
:   The column name in a table or view that contains the name of the role.

## Returns

`TRUE`:
:   - For a string literal or expression argument, the current user’s active
      [primary role or secondary roles](/user-guide/security-access-control-overview#label-access-control-role-enforcement) in the session inherit the privileges of the specified
      role.

      When the `DEFAULT_SECONDARY_ROLES` value is `ALL`, any role granted to the user inherits the privileges of the
      specified role.

      The specified role can be the current primary role or secondary role (that is, the roles returned by
      [CURRENT\_ROLE](/sql-reference/functions/current_role) or [CURRENT\_SECONDARY\_ROLES](/sql-reference/functions/current_secondary_roles), respectively) or any role
      lower in the role hierarchy.
    - For a column argument, Snowflake evaluates each row and returns a row that contains a value that specifies an active primary or
      secondary role in the user’s current session. Each row corresponds to a role name that the active primary or secondary role can see.

`FALSE`
:   - For a string literal or expression argument, the specified role is either higher in the role hierarchy of the current primary or
      secondary roles, or the role is not in the role hierarchy at all.
    - For a nonliteral argument, Snowflake evaluates each row. If a row contains a role name that is either higher in the role hierarchy
      of the current primary or secondary roles or is not in the role hierarchy at all, Snowflake does not return this row. In this case,
      Snowflake only returns rows containing the role names the active primary or secondary role can see (if any).

`NULL`
:   - This function returns NULL when used in a shared object, such as a secure view, when accessed through a data sharing consumer account.
      This behavior prevents exposing the role hierarchy in a data sharing consumer account.

## Usage notes

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

> Copy code
>
> ```
> SELECT IS_ROLE_IN_SESSION('ANALYST');
>
> +-------------------------------+
> | IS_ROLE_IN_SESSION('ANALYST') |
> |-------------------------------|
> | True                          |
> +-------------------------------+
> ```

Return active primary or secondary role values for the column named ROLE\_NAME:

> Copy code
>
> ```
> SELECT *
> FROM d1.s1.t1
> WHERE IS_ROLE_IN_SESSION(t1.role_name);
> ```

Specify a role directly in a masking policy condition:

> Copy code
>
> ```
> CREATE OR REPLACE MASKING POLICY allow_analyst AS (val string)
> RETURNS string ->
> CASE
>   WHEN IS_ROLE_IN_SESSION('ANALYST') THEN val
>   ELSE '*******'
> END;
> ```

Specify a role expression in a masking policy condition:

> Copy code
>
> ```
> CREATE OR REPLACE MASKING POLICY allow_tag_role AS (val string)
> RETURNS string ->
> CASE
>   WHEN IS_ROLE_IN_SESSION(SYSTEM$GET_TAG_ON_CURRENT_TABLE('D1.S1.ALLOWED_ROLE')) THEN val
>   ELSE '*******'
> END;
> ```

Specify the column named AUTHZ\_ROLE (that is, the authorized role) in a row access policy and then set the policy on the table column:

> Create the policy:
>
> > Copy code
> >
> > ```
> > CREATE OR REPLACE ROW ACCESS POLICY rap_authz_role AS (authz_role string)
> > RETURNS boolean ->
> > IS_ROLE_IN_SESSION(authz_role);
> > ```
>
> Add the policy to a table:
>
> > Copy code
> >
> > ```
> > ALTER TABLE allowed_roles
> >   ADD ROW ACCESS POLICY rap_authz_role ON (authz_role);
> > ```

Specify the column named AUTHZ\_ROLE in a row access policy that uses a mapping table to lookup the authorized role
in a mapping table column named ROLE\_NAME. After creating the policy, add the policy to the table containing the AUTHZ\_ROLE column:

> Create the policy:
>
> > Copy code
> >
> > ```
> > CREATE OR REPLACE ROW ACCESS POLICY rap_authz_role_map AS (authz_role string)
> > RETURNS boolean ->
> > EXISTS (
> >   SELECT 1 FROM mapping_table m
> >   WHERE authz_role = m.key and IS_ROLE_IN_SESSION(m.role_name)
> > );
> > ```
>
> Add the policy to a table:
>
> > Copy code
> >
> > ```
> > ALTER TABLE allowed_roles
> >   ADD ROW ACCESS POLICY rap_authz_role_map ON (authz_role);
> > ```
