Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$UNMANAGE\_ENTITY\_FROM\_DCM\_PROJECT

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Removes an entity from the management scope of a [DCM project](/user-guide/dcm-projects/dcm-projects-overview) without dropping the
entity. Managed grants or attachments to the entity remain unchanged. You must also remove the entity’s definition from the
DCM project. Otherwise, the DCM project manages the entity again after the next deployment.

See also:
:   [SYSTEM$UNMANAGE\_FROM\_DCM\_PROJECT](/sql-reference/functions/system_unmanage_from_dcm_project), [Unmanage entities, grants, and attachments from a DCM project](/user-guide/dcm-projects/dcm-projects-manage#label-dcm-projects-unmanage)

## Syntax

Copy code

```
SYSTEM$UNMANAGE_ENTITY_FROM_DCM_PROJECT(
  '<project_name>' ,
  '<object_type>' ,
  '<object_name>' )
```

## Arguments

`'project_name'`
:   Name of the DCM project that currently manages the entity, for example `my_db.my_schema.my_project`.

`'object_type'`
:   Type of the entity to unmanage, written with spaces between words, for example `'DYNAMIC TABLE'`. For the entity types that DCM Projects
    supports, see [Supported entities in DCM Projects](/user-guide/dcm-projects/dcm-projects-supported-entities).

`'object_name'`
:   Name of the entity to unmanage, for example `my_db.my_schema.my_dynamic_table`.

## Returns

Returns the number of entities that were unmanaged. If the DCM project doesn’t manage the entity, for example because the entity was
already unmanaged, the function returns `0`.

If the entity doesn’t exist, the function returns an error.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | DCM project | MONITOR or READ on the DCM project isn’t sufficient. |
| Any | Entity to unmanage | The entity must be visible to the role. For example, SELECT on a table is sufficient. OWNERSHIP of the entity isn’t required. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Unmanaging an entity doesn’t drop or change it. The entity remains in place, and only the DCM project’s tracking of it is removed.
- Managed grants or attachments to the entity, such as tags, masking policies, and data metric functions, remain unchanged. To unmanage
  grants and data metric function attachments, use [SYSTEM$UNMANAGE\_FROM\_DCM\_PROJECT](/sql-reference/functions/system_unmanage_from_dcm_project). Unmanaging tag
  attachments and policy attachments isn’t supported.

## Examples

The following example unmanages the dynamic table `DCM_DEMO_1_EA_DEV.ANALYTICS.MENU_ITEM_POPULARITY` from the DCM project
`DCM_DEMO.PROJECTS.DCM_PROJECT_DEV`:

Copy code

```
SELECT SYSTEM$UNMANAGE_ENTITY_FROM_DCM_PROJECT(
  'DCM_DEMO.PROJECTS.DCM_PROJECT_DEV',
  'DYNAMIC TABLE',
  'DCM_DEMO_1_EA_DEV.ANALYTICS.MENU_ITEM_POPULARITY');
```
