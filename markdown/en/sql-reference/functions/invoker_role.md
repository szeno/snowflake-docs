Categories:
:   [Context functions](/sql-reference/functions-context) (Session Object)

# INVOKER\_ROLE

Returns the name of the account-level role of the object executing the query or NULL if the name of the role is a database role.

See also:
:   [Advanced Column-level Security topics](/user-guide/security-column-advanced)

## Syntax

Copy code

```
INVOKER_ROLE()
```

## Arguments

None.

## Usage notes

- If using the INVOKER\_ROLE function with [masking policy](/user-guide/security-column-intro), verify that your Snowflake account is Enterprise Edition or higher.
- The following table summarizes the relationship between the query context and the role the function evaluates.

  | Context | Evaluated role |
  | --- | --- |
  | User | [CURRENT\_ROLE](/sql-reference/functions/current_role) |
  | Table | CURRENT\_ROLE. |
  | View | View owner role. |
  | UDF | UDF owner role. |
  | Stored procedure with caller’s right | CURRENT\_ROLE. |
  | Stored procedure with owner’s right | Stored procedure owner role. |
  | Task | Task owner role. |
  | Stream | The role that queries a given [stream](/user-guide/streams-intro#label-stream-required-privileges). |

  Expand

  Show lessSee more
- The following diagram shows the relationship of a query performer, roles in Snowflake, and masking policies on tables or views.

  ![Invoker Role Many Views](/static/images/invoker-role-many-views.png)

  Where:

  - `R0, R1, R2, R3`
    :   Are roles in Snowflake.
  - `P1, P2, P3`
    :   Are masking policies in Snowflake.
  - `V1, V2`
    :   Are views in Snowflake.
  - `T`
    :   Is a table in Snowflake.

  Based on this diagram, the values of CURRENT\_ROLE and INVOKER\_ROLE in a query are as follows:

  | Policy | CURRENT\_ROLE | INVOKER\_ROLE |
  | --- | --- | --- |
  | P1 | R3 | R1 |
  | P2 | R3 | R2 |
  | P3 | R3 | R3 |

  Expand

  Show lessSee more

## Examples

The following examples show how to use the INVOKER\_ROLE in a masking policy SQL expression.

Return NULL for unauthorized users:

> Copy code
>
> ```
> CREATE OR REPLACE MASKING POLICY mask_string AS
> (val string) RETURNS string ->
> CASE
>   WHEN INVOKER_ROLE() IN ('ANALYST') THEN val
>   ELSE NULL
> END;
> ```

Return a static masked value for unauthorized users:

> Copy code
>
> ```
> CREATE OR REPLACE MASKING POLICY mask_string AS
> (val string) RETURNS string ->
> CASE
>   WHEN INVOKER_ROLE() IN ('ANALYST') THEN val
>   ELSE '********'
> END;
> ```

Return a hash value using SHA2 , SHA2\_HEX for unauthorized users:

> Copy code
>
> ```
> CREATE OR REPLACE MASKING POLICY mask_string AS
> (val string) RETURNS string ->
> CASE
>   WHEN INVOKER_ROLE() IN ('ANALYST') THEN val
>   ELSE SHA2(val)
> END;
> ```
