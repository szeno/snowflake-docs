Categories:
:   [Context functions](/sql-reference/functions-context) (Session Object)

# IS\_APPLICATION\_ROLE\_IN\_SESSION

Verifies whether the application role is activated in the consumer’s current session.

See also:
:   [IS\_ROLE\_IN\_SESSION](/sql-reference/functions/is_role_in_session), [IS\_DATABASE\_ROLE\_IN\_SESSION](/sql-reference/functions/is_database_role_in_session)

## Syntax

Copy code

```
IS_APPLICATION_ROLE_IN_SESSION( '<string_literal>' )
```

## Arguments

`'string_literal'`
:   The application role name.

## Returns

- `TRUE` when the specified role name is activated in the consumer’s current session.

  The function always uses the consumer’s current session and returns `TRUE` when the application role is granted to the consumer using the function.

  The function does not return `TRUE` when the application calls the function because application roles are owned but not granted to the app.
- `FALSE` when the specified application role name is not activated in the consumer’s current session.

## Usage notes

- This function is only supported when called from within a Snowflake Native App. It
  does not work when called by a user outside an app.
- If you’re using the IS\_APPLICATION\_ROLE\_IN\_SESSION function with a
  [masking policy](/user-guide/security-column-intro) or a
  [row access policy](/user-guide/security-row-intro), your Snowflake must be Enterprise Edition or higher.
- Only one role name can be passed as an argument
- This function can’t be used in a materialized view definition because Snowflake cannot determine what data to
  materialize.

## Examples

Verify if the specified application role is in the current session:

Copy code

```
SELECT IS_APPLICATION_ROLE_IN_SESSION('ANALYST');
```

```
+-------------------------------------------+
| IS_APPLICATION_ROLE_IN_SESSION('ANALYST') |
+-------------------------------------------+
| FALSE                                     |
+-------------------------------------------+
```
