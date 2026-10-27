Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$UNMANAGE\_FROM\_DCM\_PROJECT

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Removes entities, grants, and data metric function attachments from the management scope of a
[DCM project](/user-guide/dcm-projects/dcm-projects-overview) without dropping, revoking, or detaching them. You specify what to unmanage
with the same statements that you use in the project definition files.

See also:
:   [SYSTEM$UNMANAGE\_ENTITY\_FROM\_DCM\_PROJECT](/sql-reference/functions/system_unmanage_entity_from_dcm_project), [Unmanage entities, grants, and attachments from a DCM project](/user-guide/dcm-projects/dcm-projects-manage#label-dcm-projects-unmanage)

## Syntax

Copy code

```
SYSTEM$UNMANAGE_FROM_DCM_PROJECT(
  '<project_name>' ,
  '<definitions>' )
```

## Arguments

`'project_name'`
:   Name of the DCM project that currently manages the entities, grants, and data metric function attachments, for example `my_db.my_schema.my_project`.

`'definitions'`
:   String that contains one or more statements, each terminated by a semicolon, that identify what to unmanage. The function accepts
    `DEFINE`, `GRANT`, and `ATTACH DATA METRIC FUNCTION` statements as they appear in DCM Projects definition files. `ATTACH TAG` and policy
    attachments aren’t supported. For more information, see [Limitations](#label-system-unmanage-from-dcm-project-limitations).

    Because definition statements often contain single quotes, use a
    [dollar-quoted string constant](/sql-reference/data-types-text#label-dollar-quoted-string-constants) to avoid escaping them.

## Returns

Returns the number of items that were unmanaged. Each `DEFINE`, `GRANT`, and `ATTACH DATA METRIC FUNCTION` item counts, so grants and
data metric function attachments are included in the count. For example, a call with one `DEFINE`, one `GRANT`, and one
`ATTACH DATA METRIC FUNCTION` statement returns `3`.

Statements for items that the DCM project doesn’t manage aren’t included in the count. For more information, see the usage notes.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | DCM project | MONITOR or READ on the DCM project isn’t sufficient. |
| Any | Each entity that the statements reference | The entity must be visible to the role. For example, SELECT on a table is sufficient. OWNERSHIP of the entity isn’t required. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Unmanaging doesn’t drop entities, revoke grants, or detach data metric functions. They remain in place, and only the DCM project’s tracking of
  them is removed.
- Each statement must match the statement as written in the
  [project definition files](/user-guide/dcm-projects/dcm-projects-files#label-dcm-projects-definition-files). You can copy the statements from your definition files into the
  function argument.
- The function accepts only plain SQL and doesn’t support Jinja templating. If your definition files use Jinja templating, pass the
  rendered statements.
- The function processes the statements as a single batch:

  - If any statement contains a syntax error or references an object that doesn’t exist, the whole call fails and nothing is unmanaged.
  - If a statement refers to an item that the DCM project doesn’t manage, such as a grant that was never managed or an entity that was
    already unmanaged, the function skips that statement without an error. The function still processes the other statements, and the
    skipped statement isn’t included in the returned count.
- After you unmanage the entities, grants, and data metric function attachments, remove the corresponding statements from your project
  definition files before the next deployment. Otherwise, the DCM project manages them again.

## Limitations

- Of the `ATTACH` statements, the function supports only `ATTACH DATA METRIC FUNCTION`. Unmanaging tag attachments (`ATTACH TAG`) and
  policy attachments, such as `ATTACH MASKING POLICY`, isn’t supported.

## Examples

The following example unmanages a table, a grant on that table, and a data metric function attachment from the DCM project
`DCM_DEMO.PROJECTS.DCM_PROJECT_DEV`:

Copy code

```
SELECT SYSTEM$UNMANAGE_FROM_DCM_PROJECT(
  'DCM_DEMO.PROJECTS.DCM_PROJECT_DEV',
  $$
    DEFINE TABLE sales.public.orders (id NUMBER);

    GRANT SELECT, INSERT ON TABLE sales.public.orders TO ROLE analyst;

    ATTACH DATA METRIC FUNCTION sales.public.not_null
      TO TABLE sales.public.orders
      ON (id);
  $$);
```
