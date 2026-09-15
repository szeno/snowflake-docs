Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$GET\_SERVICE\_DNS\_DOMAIN

Feature — Generally Available

Snowpark Container Services is available to accounts in [AWS, Microsoft Azure, and Google Cloud Platform commercial regions](/user-guide/intro-regions#label-na-general-regions), with some exceptions. For more information, see [Available regions and considerations](/developer-guide/snowpark-container-services/overview#label-snowpark-containers-overview-available-regions).

Given a schema name, returns that schema’s DNS namespace hash as a string.

See also:
:   [Working with Services](/developer-guide/snowpark-container-services/working-with-services)

## Syntax

Copy code

```
SYSTEM$GET_SERVICE_DNS_DOMAIN( <schema_name> )
```

## Arguments

`schema_name`
:   Schema name. If the schema is not in the current database, specify the fully qualified name of the schema.

## Returns

Returns the schema’s DNS namespace hash as a string.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| USAGE | Schema |  |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Examples

If TUTORIAL\_DB is the current database, then both of the following return the same result. This is the same DNS domain that appears in the DNS name (as reported by [SHOW SERVICES](/sql-reference/sql/show-services)) for any service in the DATA\_SCHEMA schema.

Copy code

```
SELECT SYSTEM$GET_SERVICE_DNS_DOMAIN('DATA_SCHEMA');
SELECT SYSTEM$GET_SERVICE_DNS_DOMAIN('TUTORIAL_DB.DATA_SCHEMA');
```

Example output:

```
+----------------------------------------------+
| SYSTEM$GET_SERVICE_DNS_DOMAIN('DATA_SCHEMA') |
|----------------------------------------------|
| k3m6.svc.spcs.internal                       |
+----------------------------------------------+
```
