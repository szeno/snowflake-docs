Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$SHOW\_EVENT\_SHARING\_ACCOUNTS

Shows event accounts in a provider organization.

This system function returns a string in JSON format containing a list of event accounts within the organization.
Because the metadata takes some time to propagate to all regions, this function might experience some delay when
showing latest events account after the user sets or unsets an events account for the organization.

## Syntax

Copy code

```
SYSTEM$SHOW_EVENT_SHARING_ACCOUNTS()
```

## Arguments

None.

## Access control requirements

- Only [organization administrators](/user-guide/organization-administrators) can execute this SQL function.

## Examples

Copy code

```
SELECT SYSTEM$SHOW_EVENT_SHARING_ACCOUNTS();
```
