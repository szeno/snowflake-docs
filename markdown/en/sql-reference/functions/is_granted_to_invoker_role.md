Categories:
:   [Context functions](/sql-reference/functions-context) (Session Object)

# IS\_GRANTED\_TO\_INVOKER\_ROLE

Returns TRUE if the role returned by the INVOKER\_ROLE function inherits the privileges of the specified role in the argument based on the
context in which the function is called.

The INVOKER\_ROLE function only identifies and returns the account role of the object executing a SQL statement. Database roles are not
supported.

## Syntax

Copy code

```
IS_GRANTED_TO_INVOKER_ROLE( '<string_literal>' )
```

## Arguments

`'string_literal'`
:   The name of the role.

## Usage notes

- If using the IS\_GRANTED\_TO\_INVOKER\_ROLE function with [masking policy](/user-guide/security-column-intro) or a
  [row access policy](/user-guide/security-row-intro), verify that your Snowflake account is Enterprise Edition or higher.
- Only one role name can be passed as an argument.
- The following table summarizes the context in which you can call the function and the role hierarchy Snowflake evaluates.

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
- If prefer to evaluate the role hierarchy for the current session, call [IS\_ROLE\_IN\_SESSION](/sql-reference/functions/is_role_in_session) instead.

## Example

Call the function directly:

> Copy code
>
> ```
> IS_GRANTED_TO_INVOKER_ROLE('ANALYST')
>
> --------------------------------------+
> IS_GRANTED_TO_INVOKER_ROLE('ANALYST') |
> --------------------------------------+
>                 TRUE                  |
> --------------------------------------+
> ```

Specify the function in the masking policy body:

Copy code

```
CREATE OR REPLACE MASKING POLICY mask_string AS
(val string) RETURNS string ->
CASE
  WHEN IS_GRANTED_TO_INVOKER_ROLE('ANALYST') then val
  ELSE '*******'
END;
```
