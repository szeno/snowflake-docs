# ALTER DCM PROJECT

Modifies the properties of an existing [DCM project](/user-guide/dcm-projects/dcm-projects-overview).

See also:
:   [CREATE DCM PROJECT](/sql-reference/sql/create-dcm-project) , [DESCRIBE DCM PROJECT](/sql-reference/sql/desc-dcm-project), [DROP DCM PROJECT](/sql-reference/sql/drop-dcm-project), [EXECUTE DCM PROJECT](/sql-reference/sql/execute-dcm-project), [SHOW DCM PROJECTS](/sql-reference/sql/show-dcm-projects),
    [SHOW DEPLOYMENTS IN DCM PROJECT](/sql-reference/sql/show-deployments-in-dcm-project)

## Syntax

Copy code

```
ALTER DCM PROJECT [ IF EXISTS ] <name> SET
  [ LOG_LEVEL = <log_level> ]
  [ COMMENT = '<string_literal>' ]

ALTER DCM PROJECT [ IF EXISTS ] <name> UNSET
  [ LOG_LEVEL ]
  [ COMMENT ]

ALTER DCM PROJECT <name>
  UNMANAGE GRANT <grant_specification>

ALTER DCM PROJECT <name>
  DROP DEPLOYMENT <deployment_name>
```

## Parameters

`name`
:   Specifies the identifier for the DCM project to alter.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`SET ...`
:   Sets one or more specified properties or parameters for the DCM project:

`LOG_LEVEL = log_level`
:   Sets the logging level for the DCM project.

    For more information about levels, see [LOG\_LEVEL](/sql-reference/parameters#label-log-level). For information about setting the log level, see
    [Setting levels for logging, metrics, and tracing](/developer-guide/logging-tracing/telemetry-levels).

    The value can be one of the following:

    - `TRACE`
    - `DEBUG`
    - `INFO`
    - `WARN`
    - `ERROR`
    - `FATAL`
    - `OFF`

    Default: `OFF`

`COMMENT = 'string_literal'`
:   Adds a comment or overwrites an existing comment for the DCM project.

`UNSET ...`
:   Unsets one or more specified properties or parameters for the DCM project, which resets the properties to their defaults:

    - `LOG_LEVEL`
    - `COMMENT`

    To unset multiple properties or parameters with a single ALTER statement, separate each property or parameter with a comma.

    When unsetting a property or parameter, specify only the property or parameter name (unless the syntax above indicates that you
    should specify the value). Specifying the value returns an error.

`UNMANAGE GRANT grant_specification`
:   Removes the specified grant from the project’s management scope without revoking the underlying privilege. Write
    `grant_specification` as you would write a [GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege) statement, but omit the leading `GRANT` keyword.
    Remove the corresponding `GRANT` statement from the project definitions before the next deployment to prevent the project from managing it
    again.

`DROP DEPLOYMENT deployment_name`
:   Deletes the specified retained deployment record and its artifacts. This operation doesn’t reverse the infrastructure changes made by that
    deployment.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | DCM project | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

The following example sets the logging level for the DCM project named `my_project` to `DEBUG`:

Copy code

```
ALTER DCM PROJECT my_project SET LOG_LEVEL = DEBUG;
```

The following example adds a comment to the DCM project named `my_project`:

Copy code

```
ALTER DCM PROJECT my_project SET COMMENT = 'Updated project for Q4 data management';
```

The following example stops managing a grant without revoking the privilege:

Copy code

```
ALTER DCM PROJECT my_project
  UNMANAGE GRANT SELECT ON TABLE my_db.my_schema.my_table TO ROLE analyst;
```

The following example deletes the retained deployment record named `DEPLOYMENT$1`:

Copy code

```
ALTER DCM PROJECT my_project
  DROP DEPLOYMENT DEPLOYMENT$1;
```
