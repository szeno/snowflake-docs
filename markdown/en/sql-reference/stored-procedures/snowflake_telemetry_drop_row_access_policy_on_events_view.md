# DROP\_ROW\_ACCESS\_POLICY\_ON\_EVENTS\_VIEW

Note

Using row access policies on the default event table is an [Enterprise Edition](/user-guide/intro-editions) feature.

Deletes the specified [row access policy](/user-guide/security-row-intro) bound to the
[EVENTS\_VIEW](/sql-reference/telemetry/events_view).

The EVENTS\_ADMIN role includes the USAGE privilege on this procedure.

## Syntax

Copy code

```
SNOWFLAKE.TELEMETRY.DROP_ROW_ACCESS_POLICY_ON_EVENTS_VIEW(
  <row_access_policy_reference>
)
```

## Arguments

`row_access_policy_reference`
:   A [reference](/sql-reference/references) to a row access policy object for the policy to drop.

## Returns

On successful execution, the procedure returns a string indicating success. Otherwise, the procedure returns an error.

## Usage notes

This stored procedure uses owner’s rights. For more details, see [Understanding caller’s rights and owner’s rights stored procedures](/developer-guide/stored-procedure/stored-procedures-rights).

## Examples

Code in the following example drops the `ROW_ACCESS_POLICY` policy bound to the EVENTS\_VIEW:

Copy code

```
CALL SNOWFLAKE.TELEMETRY.DROP_ROW_ACCESS_POLICY_ON_EVENTS_VIEW(
  SYSTEM$REFERENCE('ROW_ACCESS_POLICY', 'mydb.myschema.mypolicy', 'SESSION', 'APPLY')
);
```
