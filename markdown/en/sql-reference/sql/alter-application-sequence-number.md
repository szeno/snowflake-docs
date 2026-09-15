# ALTER APPLICATION … { APPROVE | DECLINE} SPECIFICATION

Approves or declines an [app specification](/developer-guide/native-apps/requesting-app-specs)
using the specified sequence number.

See also:
:   [ALTER APPLICATION SET SPECIFICATION](/sql-reference/sql/alter-application-set-app-spec), [ALTER APPLICATION DROP SPECIFICATION](/sql-reference/sql/alter-application-drop-app-spec)

## Syntax

Copy code

```
ALTER APPLICATION <app_name>
  { APPROVE | DECLINE } SPECIFICATION <spec_name>
  SEQUENCE_NUMBER = <sequence_num>;
```

## Parameters

`app_name`
:   Specifies the identifier for the app being altered. If the identifier contains spaces, special characters, or
    mixed-case characters, the entire string must be enclosed in double quotes. Identifiers enclosed in double
    quotes are also case-sensitive.

`{ APPROVE | DECLINE } SPECIFICATION spec_name`
:   Approves or declines the specified app specification.

`SEQUENCE_NUMBER = sequence_num`
:   Specifies the sequence number of the app specification to approve. The sequence number represents a
    version id of the app specification. The sequence number starts at 1 when the specification is created.
    The value is incremented each time the provider updates the app specification. Use
    [SHOW SPECIFICATIONS](/sql-reference/sql/show-specifications) or
    [DESCRIBE SPECIFICATION](/sql-reference/sql/desc-specification) commands to determine the current sequence number of
    the app.

## Access control requirements

| Privilege | Object | Notes |
| --- | --- | --- |
| MANAGE APPLICATION SPECIFICATIONS | Account | Allows a role to approve or decline app specifications for any app in their account. Only the SECURITYADMIN and ACCOUNTADMIN system roles have the MANAGE APPLICATION SPECIFICATIONS privilege; however, the privilege can be granted to custom roles. |

Expand

Show lessSee more
