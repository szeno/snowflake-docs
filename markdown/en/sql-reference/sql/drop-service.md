# DROP SERVICE

Feature — Generally Available

Snowpark Container Services is available to accounts in [AWS, Microsoft Azure, and Google Cloud Platform commercial regions](/user-guide/intro-regions#label-na-general-regions), with some exceptions. For more information, see [Available regions and considerations](/developer-guide/snowpark-container-services/overview#label-snowpark-containers-overview-available-regions).

Removes the specified
[Snowpark Container Services service](/developer-guide/snowpark-container-services/working-with-services) from the current
or specified schema. The containers for the service are terminated.

See also:
:   [CREATE SERVICE](/sql-reference/sql/create-service) , [ALTER SERVICE](/sql-reference/sql/alter-service), [SHOW SERVICES](/sql-reference/sql/show-services) , [DESCRIBE SERVICE](/sql-reference/sql/desc-service)

## Syntax

Copy code

```
DROP SERVICE [ IF EXISTS ] <name> [ FORCE ]
```

## Required parameters

`name`
:   Specifies the identifier for the service to be dropped.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Optional parameters

`FORCE`
:   Drops the service (including job services) and the associated block storage volumes.

    If `FORCE` is not specified and the service uses a
    [block storage volume](/developer-guide/snowpark-container-services/block-storage-volume)
    an error is returned.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Service |  |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- When the IF EXISTS clause is specified and the target object doesn’t exist, the command completes successfully
  without returning an error.

## Examples

The following example drops the service named `my_tutorial`:

Copy code

```
DROP SERVICE my_tutorial;
```

```
+-----------------------------------+
| status                            |
|-----------------------------------|
| MY_TUTORIAL successfully dropped. |
+-----------------------------------+
```
