Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$ABORT\_SESSION

Aborts the specified session.

## Syntax

Copy code

```
SYSTEM$ABORT_SESSION( <session_id> )
```

## Arguments

`session_id`
:   Identifier for the session to abort. To obtain the ID for a session, log into the web interface as an account administrator (user with the ACCOUNTADMIN role) and go to:

    > **Account** [![Account tab](/static/images/screens/ui-navigation-account-icon.svg)](/static/images/screens/ui-navigation-account-icon.svg) » **Sessions**

## Examples

Copy code

```
SELECT SYSTEM$ABORT_SESSION(1065153868222);

+-------------------------------------+
| SYSTEM$ABORT_SESSION(1065153868222) |
|-------------------------------------|
| session [1065153868222] terminated. |
+-------------------------------------+
```
