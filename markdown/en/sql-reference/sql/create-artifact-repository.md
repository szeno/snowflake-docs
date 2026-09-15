# CREATE ARTIFACT REPOSITORY

Creates a new artifact repository in the current or specified schema, or
replaces an existing artifact repository. An artifact repository stores
versioned packages that are used by downstream Snowflake objects. Two
repository types are supported:

- `APPLICATION`: stores packaged application builds that a
  [CREATE APPLICATION SERVICE](/sql-reference/sql/create-application-service)
  deploys.
- `PYPI`: stores Python packages resolved from an external Python package
  index through an API integration.

See also:
:   [ALTER ARTIFACT REPOSITORY](/sql-reference/sql/alter-artifact-repository),
    [DESCRIBE ARTIFACT REPOSITORY](/sql-reference/sql/desc-artifact-repository),
    [DROP ARTIFACT REPOSITORY](/sql-reference/sql/drop-artifact-repository),
    [SHOW ARTIFACT REPOSITORIES](/sql-reference/sql/show-artifact-repositories)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] ARTIFACT REPOSITORY [ IF NOT EXISTS ] <name>
  TYPE = { APPLICATION | PYPI }
  [ API_INTEGRATION = '<integration_name>' ]
  [ INDEX_URL = '<url>' ]
  [ AUTHENTICATION_SECRET = <secret_name> ]
  [ PACKAGE_RETENTION = { ON_OBJECT_CREATION } ]
  [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , ... ] ) ]
  [ COMMENT = '<string_literal>' ]
```

Note

`INDEX_URL`, `AUTHENTICATION_SECRET`, and `PACKAGE_RETENTION` apply to
customer-hosted Python artifact repositories, which are in public preview.
For details, see
[Integrate customer-hosted Python artifact repositories](/developer-guide/udf/python/customer-hosted-python-artifact-repositories).

## Required parameters

`name`
:   Specifies the identifier for the artifact repository. The identifier must be
    unique for the schema where the repository is created. For more details, see
    [Identifier requirements](/sql-reference/identifiers-syntax).

`TYPE = { APPLICATION | PYPI }`
:   Specifies the type of content the repository stores.

    - `APPLICATION`: stores versioned application packages. Required when the
      repository is referenced by
      [CREATE APPLICATION SERVICE](/sql-reference/sql/create-application-service).
    - `PYPI`: stores Python packages fetched from an external package index.
      The `API_INTEGRATION` parameter is required for this type.

## Optional parameters

`API_INTEGRATION = 'integration_name'`
:   Specifies the API integration that provides access to the external Python
    package index. Required when `TYPE = PYPI`. Not used when
    `TYPE = APPLICATION`.

`INDEX_URL = 'url'`
:   Specifies the HTTPS URL of the PyPI-compatible package index that a
    customer-hosted Python artifact repository fetches packages from
    (for example, `'https://nexus.example.com/repository/pypi-proxy/simple/'`).
    The host must be covered by the `API_ALLOWED_PREFIXES` of the referenced
    API integration. Used only for customer-hosted PyPI repositories.

`AUTHENTICATION_SECRET = secret_name`
:   Specifies the [secret](/sql-reference/sql/create-secret) that Snowflake uses to
    authenticate to the customer-hosted Python artifact repository. The secret must
    be included in the `ALLOWED_AUTHENTICATION_SECRETS` of the referenced API
    integration. Used only for customer-hosted PyPI repositories.

`PACKAGE_RETENTION = ON_OBJECT_CREATION`
:   Controls when Snowflake retains packages downloaded from a customer-hosted
    Python artifact repository:

    - When not set (default), packages are retained asynchronously in the background
      after each `CREATE FUNCTION` or `CREATE PROCEDURE`.
    - When set to `ON_OBJECT_CREATION`, `CREATE FUNCTION` and `CREATE PROCEDURE`
      download and retain every referenced package before the statement returns.

    For details, see
    [Package retention and caching](/developer-guide/udf/python/customer-hosted-python-artifact-repositories#label-customer-hosted-repos-retention).
    Used only for customer-hosted PyPI repositories.

`TAG ( tag_name = 'tag_value' [ , ... ] )`
:   Assigns a tag to the repository. For more details about object tagging, see
    [Introduction to object tagging](/user-guide/object-tagging/introduction).

`COMMENT = 'string_literal'`
:   Specifies a comment for the artifact repository.

    **DEFAULT:** No value

## Access control requirements

If your role does not own the objects in the following table, then your role
must have the listed
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) on those objects:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE ARTIFACT REPOSITORY | Schema | Required to create a new artifact repository in the schema. |
| USAGE | API integration | Required only when `TYPE = PYPI`. |

Expand

Show lessSee more

The following privileges can be granted on an artifact repository after it’s created:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Artifact repository | Grants full control, including publishing new package versions and dropping the repository. |
| READ | Artifact repository | Allows downloading packages and artifacts. Grant this to any role that references the repository in [CREATE APPLICATION SERVICE](/sql-reference/sql/create-application-service). |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- An `APPLICATION` repository holds one or more packages. Each package has
  one or more versions. New versions are produced by builds that target the
  repository. For more information, see
  [Getting started with Snowflake App Runtime](/developer-guide/snowflake-app-runtime/getting-started).
- A repository’s type can’t be changed after it’s created. To switch types,
  drop the repository and create a new one.
- `CREATE OR REPLACE` drops and recreates the repository atomically. All
  packages and versions in the repository are removed.

- The OR REPLACE and IF NOT EXISTS clauses are mutually exclusive. They can’t both be used in the same statement.
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

## Examples

Create an artifact repository for application packages:

Copy code

```
CREATE ARTIFACT REPOSITORY my_app_repo
  TYPE = APPLICATION
  COMMENT = 'Repository for my team''s apps';
```

Create a PyPI-backed repository that uses an existing API integration:

Copy code

```
CREATE ARTIFACT REPOSITORY my_pypi_repo
  TYPE = PYPI
  API_INTEGRATION = pypi_integration;
```
