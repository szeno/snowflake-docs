# CREATE DCM PROJECT

Creates a new [DCM project](/user-guide/dcm-projects/dcm-projects-overview) or replaces an existing DCM project.

See also:
:   [ALTER DCM PROJECT](/sql-reference/sql/alter-dcm-project) , [DESCRIBE DCM PROJECT](/sql-reference/sql/desc-dcm-project) , [DROP DCM PROJECT](/sql-reference/sql/drop-dcm-project) , [EXECUTE DCM PROJECT](/sql-reference/sql/execute-dcm-project) , [SHOW DCM PROJECTS](/sql-reference/sql/show-dcm-projects) , [SHOW DEPLOYMENTS IN DCM PROJECT](/sql-reference/sql/show-deployments-in-dcm-project)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] DCM PROJECT [ IF NOT EXISTS ] <name>
  [LOG_LEVEL = { DEBUG | INFO | WARN | ERROR }]
  [ COMMENT = '<string_literal>' ]
```

## Required parameters

`name`
:   String that specifies the identifier (name) for the DCM project; must be unique for the schema in which the DCM project is created.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the
    entire identifier string is enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in double quotes are also
    case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Optional parameters

`LOG_LEVEL = { DEBUG | INFO | WARN | ERROR }`
:   Specifies the severity level of messages that should be ingested and made available in the active event table. Messages at the specified
    level (and at more severe levels) are ingested.

    For more information, see [LOG\_LEVEL](/sql-reference/parameters#label-log-level) and [Setting levels for logging, metrics, and tracing](/developer-guide/logging-tracing/telemetry-levels).

`COMMENT = 'string_literal'`
:   Specifies a comment for the DCM project.

    Default: No value

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object |
| --- | --- |
| CREATE DCM PROJECT | Schema |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- The OR REPLACE and IF NOT EXISTS clauses are mutually exclusive. They can’t both be used in the same statement.
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

- Create a DCM project:

  Copy code

  ```
  CREATE DCM PROJECT MY_PROJECT;
  ```
- Create a DCM project with a comment:

  Copy code

  ```
  CREATE DCM PROJECT MY_PROJECT
    COMMENT = 'My DCM project for data management';
  ```
