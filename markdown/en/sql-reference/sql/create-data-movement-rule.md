# CREATE DATA MOVEMENT RULE

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Creates a new [data movement rule](/user-guide/data-movement-policies) in the current/specified schema or replaces an
existing data movement rule.

A data movement rule controls a single movement type and returns the maximum number of rows that the movement type can
move. After you create a data movement rule, add it to a data movement policy so that Snowflake enforces or reports on it.

See also:
:   [ALTER DATA MOVEMENT RULE](/sql-reference/sql/alter-data-movement-rule) , [DROP DATA MOVEMENT RULE](/sql-reference/sql/drop-data-movement-rule) , [SHOW DATA MOVEMENT RULES](/sql-reference/sql/show-data-movement-rules) , [DESCRIBE DATA MOVEMENT RULE](/sql-reference/sql/desc-data-movement-rule)

    [CREATE DATA MOVEMENT POLICY](/sql-reference/sql/create-data-movement-policy) , [ALTER DATA MOVEMENT POLICY](/sql-reference/sql/alter-data-movement-policy) , [DROP DATA MOVEMENT POLICY](/sql-reference/sql/drop-data-movement-policy)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] DATA MOVEMENT RULE [ IF NOT EXISTS ] <name>
  TYPE = '<movement_type>'
  MAX_ROWS AS () RETURNS INTEGER
  -> ( <expression> )
  [ COMMENT = '<string_literal>' ]
```

## Required parameters

`name`
:   String that specifies the identifier (that is, name) for the data movement rule; must be unique for the schema in which
    the data movement rule is created.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the
    entire identifier string is enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in double quotes are also
    case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`TYPE = 'movement_type'`
:   Specifies the movement type that the rule controls. A rule controls exactly one movement type.

    Supported values:

    - `COPY_INTO_EXTERNAL_STAGE` - Rows unloaded to an external stage with [COPY INTO <location>](/sql-reference/sql/copy-into-location).
    - `COPY_INTO_INTERNAL_STAGE` - Rows unloaded to an internal stage with [COPY INTO <location>](/sql-reference/sql/copy-into-location).
    - `SNOWSIGHT_UI` - Rows returned to the Snowsight worksheet results grid.
    - `AGENT_ACCESS` - Rows accessed by an agent.
    - `UI_DOWNLOAD` - Rows downloaded via the **Download** button in Snowsight (workspace results pane, notebook cells, and Query History). Does not apply to all download surfaces; for example, downloads in Streamlit apps, notebooks in the Visual Studio Code extension, the **Export as HTML** option in workspaces, and CoWork are not covered.
    - `PROGRAMMATIC_FETCH` - Rows fetched programmatically, for example through a driver or connector.

`MAX_ROWS AS () RETURNS INTEGER -> ( expression )`
:   SQL expression body that returns an INTEGER, which sets the maximum number of rows that the movement type can move.

    The return value determines the behavior:

    - `NULL` - No limit on the number of rows.
    - `0` - Block the movement.
    - A positive integer - The maximum number of rows that the movement type can move.

    The expression can contain CASE and other logic statements. It can call [SYS\_CONTEXT](/sql-reference/functions/sys_context) to read
    session and movement context and adjust the returned limit accordingly.

## Optional parameters

`COMMENT = 'string_literal'`
:   Specifies a comment for the data movement rule.

    Default: No value

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE DATA MOVEMENT RULE | Schema |  |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- A rule can’t appear in both the `ENFORCE_RULES` and `ALERT_RULES` of a data movement policy at the same time.
- A data movement policy can have at most one rule per movement type in each of `ENFORCE_RULES` and `ALERT_RULES`.
- A `UI_DOWNLOAD` rule can only be used in `ENFORCE_RULES`, not in `ALERT_RULES`.
- The MAX\_ROWS expression body can use [SYS\_CONTEXT](/sql-reference/functions/sys_context) to read session and movement context.
- [GET\_DDL](/sql-reference/functions/get_ddl) is supported for this object type. If you want to update an existing data movement
  rule and need to see its current definition, run the GET\_DDL function.

- The OR REPLACE and IF NOT EXISTS clauses are mutually exclusive. They can’t both be used in the same statement.
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

Create a rule that lets the `COMP_TEAM_ROLE` role unload any number of rows to an external stage, but blocks all other
roles:

Copy code

```
CREATE OR REPLACE DATA MOVEMENT RULE hr_pii_copy_guard
  TYPE = 'COPY_INTO_EXTERNAL_STAGE'
  MAX_ROWS AS () RETURNS INTEGER
  -> (
    CASE
      WHEN SYS_CONTEXT('SNOWFLAKE$SESSION', 'ROLE') = 'COMP_TEAM_ROLE' THEN NULL
      ELSE 0
    END
  );
```

Create a rule that caps unloads to an external stage at 1000 rows:

Copy code

```
CREATE OR REPLACE DATA MOVEMENT RULE hr_pii_copy_limit
  TYPE = 'COPY_INTO_EXTERNAL_STAGE'
  MAX_ROWS AS () RETURNS INTEGER
  -> (1000);
```
