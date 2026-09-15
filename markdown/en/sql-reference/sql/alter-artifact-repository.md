# ALTER ARTIFACT REPOSITORY

Modifies the properties of an existing
[artifact repository](/sql-reference/sql/create-artifact-repository).

See also:
:   [CREATE ARTIFACT REPOSITORY](/sql-reference/sql/create-artifact-repository) ,
    [DESCRIBE ARTIFACT REPOSITORY](/sql-reference/sql/desc-artifact-repository) ,
    [DROP ARTIFACT REPOSITORY](/sql-reference/sql/drop-artifact-repository) ,
    [SHOW ARTIFACT REPOSITORIES](/sql-reference/sql/show-artifact-repositories)

## Syntax

Copy code

```
ALTER ARTIFACT REPOSITORY [ IF EXISTS ] <name> SET
  [ COMMENT = '<string_literal>' ]
  [ INDEX_URL = '<url>' ]
  [ AUTHENTICATION_SECRET = <secret_name> ]
  [ PACKAGE_RETENTION = { ON_OBJECT_CREATION } ]

ALTER ARTIFACT REPOSITORY [ IF EXISTS ] <name> UNSET
  { COMMENT | AUTHENTICATION_SECRET | PACKAGE_RETENTION }

ALTER ARTIFACT REPOSITORY [ IF EXISTS ] <name> SET
  TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]

ALTER ARTIFACT REPOSITORY [ IF EXISTS ] <name> UNSET
  TAG <tag_name> [ , <tag_name> ... ]
```

Note

`INDEX_URL`, `AUTHENTICATION_SECRET`, and `PACKAGE_RETENTION` apply to
customer-hosted Python artifact repositories, which are in public preview.
For details, see
[Integrate customer-hosted Python artifact repositories](/developer-guide/udf/python/customer-hosted-python-artifact-repositories).

## Parameters

`name`
:   Specifies the identifier of the artifact repository to alter.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`SET ...`
:   Sets one or more properties on the repository.

    `COMMENT = 'string_literal'`
    :   Updates the repository comment.

    `INDEX_URL = 'url'`
    :   Updates the HTTPS URL of the PyPI-compatible package index for a customer-hosted
        Python artifact repository. Use this to repoint an existing repository at a
        different index (for example, to fail over to a secondary region) without
        recreating the repository or its dependent functions and procedures.

    `AUTHENTICATION_SECRET = secret_name`
    :   Updates the [secret](/sql-reference/sql/create-secret) that Snowflake uses to
        authenticate to a customer-hosted Python artifact repository.

    `PACKAGE_RETENTION = ON_OBJECT_CREATION`
    :   Enables synchronous package retention on a customer-hosted Python artifact
        repository. When set, `CREATE FUNCTION` and `CREATE PROCEDURE` download and
        retain every referenced package before returning. Unset to revert to the default
        (asynchronous background retention). For details, see
        [Package retention and caching](/developer-guide/udf/python/customer-hosted-python-artifact-repositories#label-customer-hosted-repos-retention).

`UNSET ...`
:   Removes a property, resetting it to the default.

`SET TAG` / `UNSET TAG`
:   Adds or removes tags on the repository. For more details, see
    [Introduction to object tagging](/user-guide/object-tagging/introduction).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Artifact repository | Required to alter any property or tag on the repository. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- You can’t change the `TYPE` of an existing artifact repository. To change
  the type, drop the repository and create a new one.
- You can’t change the `API_INTEGRATION` of a `PYPI` repository after
  creation.

## Examples

Update the comment on a repository:

Copy code

```
ALTER ARTIFACT REPOSITORY my_app_repo SET
  COMMENT = 'Production app builds';
```

Clear the comment:

Copy code

```
ALTER ARTIFACT REPOSITORY my_app_repo UNSET COMMENT;
```

Set a tag:

Copy code

```
ALTER ARTIFACT REPOSITORY my_app_repo SET
  TAG cost_center = 'platform';
```

Repoint a customer-hosted Python artifact repository at a different index
(for example, to fail over from a primary to a secondary region):

Copy code

```
ALTER ARTIFACT REPOSITORY my_python_repo
  SET INDEX_URL = 'https://nexus-west.example.com/repository/pypi-proxy/simple/';
```

Enable synchronous package retention on a customer-hosted Python artifact
repository:

Copy code

```
ALTER ARTIFACT REPOSITORY my_python_repo
  SET PACKAGE_RETENTION = ON_OBJECT_CREATION;
```
