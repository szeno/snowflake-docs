Categories:
:   [Context functions](/sql-reference/functions-context) (Session)

# CURRENT\_USER

Returns the name of the user currently logged into the system.

## Syntax

Copy code

```
CURRENT_USER()

CURRENT_USER
```

## Arguments

None.

## Returns

This function returns a value of type VARCHAR.

## Usage notes

- To comply with the ANSI standard, this function can be called without parentheses in SQL statements.

  However, if you are setting a [Snowflake Scripting variable](/developer-guide/snowflake-scripting/variables)
  to an expression that calls the function (for example, `my_var := CURRENT_USER();`), you must include the
  parentheses. For more information, see [the usage notes for context functions](/sql-reference/functions-context#label-context-function-usage-notes).
- Granting access on a [secure UDF](/developer-guide/secure-udf-procedure#label-secure-udf-data-sharing) or [secure view](/user-guide/views-secure#label-secure-view-data-sharing) that
  contains this function to a share is allowed. When the secure UDF or secure view is accessed from the data sharing consumer account, this
  function always returns a NULL value.
- Snowflake returns a NULL value if this function is used in a [masking policy](/user-guide/security-column-intro#label-security-column-intro-data-sharing) or
  [row access policy](/user-guide/security-row-intro#label-security-row-intro-data-sharing) that is assigned to a shared table or view.

## Examples

This example calls the CURRENT\_USER function:

Copy code

```
SELECT CURRENT_USER();
```

```
+----------------+
| CURRENT_USER() |
|----------------|
| TSMITH         |
+----------------+
```
