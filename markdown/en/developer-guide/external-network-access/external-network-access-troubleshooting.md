# Troubleshooting external network access

The following lists errors you might encounter, along with their likely cause and a suggested resolution.

## Error: UnknownHostException or Temporary Failure in Name Resolution

This error can have one of multiple causes, as described below.

Cause:
:   The [CREATE PROCEDURE](/sql-reference/sql/create-procedure) or [CREATE FUNCTION](/sql-reference/sql/create-function) statement does not reference the
    external access integration when creating a procedure or UDF that accesses a URL specified by the network rule.

Resolution:
:   When creating the procedure or UDF, be sure to specify the external access integration as a value of the
    CREATE statement’s EXTERNAL\_ACCESS\_INTEGRATIONS parameter.

Cause:
:   The UDF or procedure is attempting to access a URL that is not part of the network rule included in the external access integration.

Resolution:
:   A user with the ACCOUNTADMIN role can add the host URL to the network rule included in the external access integration.

## Error: Connect Timed Out or Receive Timed out

Cause:
:   You are attempting to access an IP address or port that is not part of the network rule included in the external access integration.

Resolution:
:   A user with the ACCOUNTADMIN role can add the IP address to the network rule included in the external access integration.
