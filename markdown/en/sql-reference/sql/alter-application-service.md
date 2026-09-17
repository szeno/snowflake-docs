# ALTER APPLICATION SERVICE

Modifies the configuration or lifecycle state of an existing
[Application Service](/sql-reference/sql/create-application-service).
You can suspend, resume, or upgrade the service, and you can set or unset
properties.

See also:
:   [CREATE APPLICATION SERVICE](/sql-reference/sql/create-application-service) ,
    [DESCRIBE APPLICATION SERVICE](/sql-reference/sql/desc-application-service) ,
    [DROP APPLICATION SERVICE](/sql-reference/sql/drop-application-service) ,
    [SHOW APPLICATION SERVICES](/sql-reference/sql/show-application-services)

## Syntax

Copy code

```
ALTER APPLICATION SERVICE [ IF EXISTS ] <name> { SUSPEND | RESUME }

ALTER APPLICATION SERVICE [ IF EXISTS ] <name>
  UPGRADE [ TO VERSION <version_alias> ]

ALTER APPLICATION SERVICE [ IF EXISTS ] <name> SET
  [ AUTO_RESUME = { TRUE | FALSE } ]
  [ AUTO_SUSPEND_SECS = <num> ]
  [ EXTERNAL_ACCESS_INTEGRATIONS = ( <integration_name> [ , ... ] ) ]
  [ QUERY_WAREHOUSE = <warehouse_name> ]
  [ MIN_INSTANCES = <num> ]
  [ MAX_INSTANCES = <num> ]
  [ COMMENT = '<string_literal>' ]

ALTER APPLICATION SERVICE [ IF EXISTS ] <name> UNSET
  {
    AUTO_RESUME                  |
    AUTO_SUSPEND_SECS            |
    EXTERNAL_ACCESS_INTEGRATIONS |
    QUERY_WAREHOUSE              |
    MIN_INSTANCES                |
    MAX_INSTANCES                |
    COMMENT
  }
  [ , ... ]
```

## Parameters

`name`
:   Specifies the identifier for the Application Service to alter.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`{ SUSPEND | RESUME }`
:   Suspends or resumes the service. When the service is suspended, Snowflake
    stops its containers and stops billing for compute. When you resume the
    service, Snowflake starts containers using the currently deployed package
    version.

`UPGRADE [ TO VERSION version_alias ]`
:   Upgrades the service to a different version of its package.

    - If `TO VERSION` is omitted and the service was created with a version
      alias, such as `LATEST`, Snowflake re-resolves the alias to its current
      target version and upgrades to that version.
    - If `TO VERSION` is omitted and the service was created with a concrete
      version name, the command returns an error asking you to specify a
      version.
    - If `TO VERSION` is specified, you can pass a version name, such as
      `VERSION$4`, or an alias, such as `LATEST`.

    If the resolved target version is the same as the running version, the
    upgrade is a no-op.

`SET ...`
:   Sets one or more properties on the service. Properties not listed in the
    `SET` clause are unchanged. See
    [CREATE APPLICATION SERVICE](/sql-reference/sql/create-application-service) for parameter descriptions.

`UNSET ...`
:   Removes a property, resetting it to the default.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OPERATE | Application Service | Required for `SUSPEND`, `RESUME`, `UPGRADE`, `SET`, and `UNSET`. |
| READ | Artifact repository | Required for `UPGRADE` to resolve the target package version. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- An upgrade applies the new package version to the running service. Snowflake
  performs a rolling restart of the service containers using the new build.
- Suspending a service doesn’t change the deployed package version. The
  service resumes on the same version.
- If `RESUME` fails because the service’s runtime image is no longer allowed,
  Snowflake returns an error similar to:
  `Application service 'my_app' cannot be resumed because its runtime image is blocked. Upgrade the service to a new version before resuming.` Deploy a new
  package version (for example with `UPGRADE` or `snow app deploy`) that uses a
  supported runtime image, then resume the service.
- If `MAX_INSTANCES` isn’t set, it matches `MIN_INSTANCES`. If neither is set,
  Snowflake runs one instance.
- To change both values in one statement, include both in the same `SET`
  clause.
- You can’t set a `SPECIFICATION` with `ALTER APPLICATION SERVICE ... SET`. To update
  the specification of a service, use
  [CREATE OR ALTER APPLICATION SERVICE](/sql-reference/sql/create-application-service#label-create-or-alter-application-service-syntax).
  A specification is the full intended state of the service, so it resets any
  property it doesn’t set. `ALTER APPLICATION SERVICE ... SET` remains the way to
  change a single property in place.

## Examples

Suspend a service:

Copy code

```
ALTER APPLICATION SERVICE my_app SUSPEND;
```

Resume a service:

Copy code

```
ALTER APPLICATION SERVICE my_app RESUME;
```

Upgrade a service that was created with an alias to the alias’s current target
(re-resolves `LATEST` or `DEFAULT`):

Copy code

```
ALTER APPLICATION SERVICE my_app UPGRADE;
```

Upgrade to a specific version:

Copy code

```
ALTER APPLICATION SERVICE my_app UPGRADE TO VERSION VERSION$5;
```

Change auto-suspend and external access:

Copy code

```
ALTER APPLICATION SERVICE my_app SET
  AUTO_SUSPEND_SECS = 900
  EXTERNAL_ACCESS_INTEGRATIONS = ( my_eai, analytics_eai );
```

Set instance counts:

Copy code

```
ALTER APPLICATION SERVICE my_app SET MIN_INSTANCES = 2 MAX_INSTANCES = 5;
```

Unset `MAX_INSTANCES` so it matches `MIN_INSTANCES`:

Copy code

```
ALTER APPLICATION SERVICE my_app UNSET MAX_INSTANCES;
```
