# SYSTEM$MANAGE\_SEMANTIC\_VIEW\_MATERIALIZATIONS\_FROM\_YAML

Preview Feature — Open

Available to all accounts.

Synchronizes the materializations on a semantic view with a YAML specification.
This stored procedure applies the desired state declaratively:

- Materializations in the YAML that don’t exist are created.
- Materializations that exist but have a changed definition are replaced.
- Materializations that already exist with the same definition are left unchanged (no-op).
- Materializations that exist on the semantic view but aren’t in the YAML are dropped.

See also:
:   [Materializing dimensions and metrics in semantic views](/user-guide/views-semantic/materializations) ,
    [SYSTEM$CREATE\_SEMANTIC\_VIEW\_FROM\_YAML](/sql-reference/stored-procedures/system_create_semantic_view_from_yaml)

## Syntax

Copy code

```
SYSTEM$MANAGE_SEMANTIC_VIEW_MATERIALIZATIONS_FROM_YAML(
  '<semantic_view_name>' ,
  '<yaml_specification>'
)
```

## Arguments

**Required:**

`'semantic_view_name'`
:   The name of the semantic view to manage materializations for. Can be unqualified
    (uses the current database and schema) or fully qualified (`database.schema.view`).

`'yaml_specification'`
:   A YAML string describing the desired set of materializations. Use a
    [dollar-quoted string constant](/sql-reference/data-types-text#label-dollar-quoted-string-constants) if the
    specification contains quotes or newlines.

    The YAML uses the following structure:

    Copy code

    ```
    materializations:
      - name: <materialization_name>
        warehouse: <warehouse_name>
        dimensions:
          - table: <entity_name>
            name: <dimension_name>
        metrics:
          - table: <entity_name>
            name: <metric_name>
    ```

    To drop all materializations, pass an empty list:

    Copy code

    ```
    materializations: []
    ```

## Returns

Returns a VARCHAR string describing the actions taken (materializations created,
updated, dropped, or left unchanged).

If the stored procedure fails (for example, the semantic view doesn’t exist or a
materialization definition is invalid), it raises an exception with a descriptive
error message.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP or ADD SEMANTIC VIEW MATERIALIZATION | Schema containing the semantic view | Required to create or drop materializations. |
| SELECT | Semantic view | Required to read the semantic view definition. |
| USAGE | Warehouse specified in the YAML | Required for each warehouse used by the materializations. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- The semantic view must have `MAX_STALENESS` set before materializations can be added.
  See [Setting the maximum staleness](/user-guide/views-semantic/materializations#label-semantic-views-materializing-prereqs-staleness).
- If you pass `materializations: []`, all existing materializations on the semantic view are dropped.
- This procedure is idempotent: running it twice with the same YAML has no effect on the second run.

## Examples

### Synchronize materializations

Copy code

```
CALL SYSTEM$MANAGE_SEMANTIC_VIEW_MATERIALIZATIONS_FROM_YAML(
  'MY_SV',
  $$
  materializations:
    - name: mat_by_region
      warehouse: W
      dimensions:
        - table: orders
          name: region
      metrics:
        - table: orders
          name: total_revenue
    - name: mat_by_customer
      warehouse: W
      dimensions:
        - table: orders
          name: customer_name
      metrics:
        - table: orders
          name: order_count
  $$
);
```

### Drop all materializations

Copy code

```
CALL SYSTEM$MANAGE_SEMANTIC_VIEW_MATERIALIZATIONS_FROM_YAML(
  'MY_SV',
  'materializations: []'
);
```
