# DROP IMAGE REPOSITORY

Feature — Generally Available

Snowpark Container Services is available to accounts in [AWS, Microsoft Azure, and Google Cloud Platform commercial regions](/user-guide/intro-regions#label-na-general-regions), with some exceptions. For more information, see [Available regions and considerations](/developer-guide/snowpark-container-services/overview#label-snowpark-containers-overview-available-regions).

Removes the specified [image repository](/developer-guide/snowpark-container-services/tutorials/tutorial-1) from
the current or specified schema.

See also:
:   [CREATE IMAGE REPOSITORY](/sql-reference/sql/create-image-repository) , [SHOW IMAGE REPOSITORIES](/sql-reference/sql/show-image-repositories)

## Syntax

Copy code

```
DROP IMAGE REPOSITORY [ IF EXISTS ] <name>
```

## Parameters

`name`
:   Specifies the identifier for the repository to drop.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Image repository |  |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Dropping an image repository while services are running that reference images in that repository can cause problems. Currently
  running service instances and jobs will continue to run, but any attempt to create a new service instance will fail.

- When the IF EXISTS clause is specified and the target object doesn’t exist, the command completes successfully
  without returning an error.

## Examples

The following example drops the repository named `tutorial_repository`:

Copy code

```
DROP IMAGE REPOSITORY tutorial_repository;
```

```
+-------------------------------------------+
| status                                    |
|-------------------------------------------|
| TUTORIAL_REPOSITORY successfully dropped. |
+-------------------------------------------+
```
