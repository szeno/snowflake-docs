# Manage deployed DCM Projects

This topic describes how to manage a deployed DCM project: list the entities and grants it manages, unmanage entities, grants, and
attachments, purge a project, and drop a project.

## Show objects and grants managed by a DCM project

The [SHOW ENTITIES IN DCM PROJECT](/sql-reference/sql/show-entities-in-dcm-project) command allows you to see a list of all Snowflake objects that are currently managed by a specific DCM project.
It provides a list of fully qualified names for all objects. To see the results, you need both `READ` privilege on the DCM project and privileges to see the managed object itself.

Note

The result doesn’t necessarily match the objects of the most recent deployment. Objects that were manually dropped or unmanaged from the project aren’t listed in the result.

You can use `LIKE` to search by name or use a flow operator to further process or filter the result set.

Similarly, the [SHOW GRANTS IN DCM PROJECT](/sql-reference/sql/show-grants-in-dcm-project) command lets you list the grants that are defined and deployed with the DCM project.
Use `SHOW GRANTS IN DCM PROJECT` to list grants that are currently deployed and managed by the project, or `SHOW FUTURE GRANTS IN DCM PROJECT` to list grants that will be deployed and managed by the project the next time the project is deployed.

The following examples show the objects and grants that a DCM project currently manages:

SQLSnowsight

Copy code

```
SHOW ENTITIES LIKE '%DASHBOARD%' IN DCM PROJECT DCM_DEMO.PROJECTS.DCM_PROJECT_DEV;

SHOW ENTITIES IN DCM PROJECT DCM_DEMO.PROJECTS.DCM_PROJECT_DEV
  ->> SELECT * FROM $1 WHERE "object_type" = 'DYNAMIC_TABLE';

SHOW GRANTS IN DCM PROJECT DCM_DEMO.PROJECTS.DCM_PROJECT_DEV;

SHOW FUTURE GRANTS IN DCM PROJECT DCM_DEMO.PROJECTS.DCM_PROJECT_DEV;
```

1. In the navigation menu, select **Catalog** » **Explorer**.
2. Navigate to the schema that contains the DCM project object.
3. Select the DCM project object to see its details.
4. Select the **Objects** tab to see a list of all Snowflake objects currently managed by this project object, or select the **Grants** tab to see a list of all grants currently managed by this project object.
5. Select the name of an object to open that object’s details page in a new tab.

## Unmanage entities, grants, and attachments from a DCM project

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Unmanaging removes an entity, grant, or attachment from the management scope of a DCM project without dropping the entity, revoking the
grant, or detaching the attachment. Only the DCM project’s tracking of the entity, grant, or attachment is removed. You can unmanage an
entity, grant, or attachment when you want to manage it with a different DCM project or manage it manually.

Unmanaging is different from removing a definition and redeploying. DCM Projects interprets a missing definition as intent to drop the entity, revoke the
grant, or remove the attachment on the next deployment.

After you unmanage an entity, grant, or attachment, remove the corresponding statement from your
[project definition files](/user-guide/dcm-projects/dcm-projects-files#label-dcm-projects-definition-files) before the next deployment. Otherwise, the DCM project manages it again.

DCM Projects provides two system functions for unmanaging. Choose the one that fits what you want to unmanage:

- [SYSTEM$UNMANAGE\_ENTITY\_FROM\_DCM\_PROJECT](/sql-reference/functions/system_unmanage_entity_from_dcm_project) unmanages a single entity that you identify by its type and name.
  Managed grants or attachments to the entity remain unchanged.

  Copy code

  ```
  SELECT SYSTEM$UNMANAGE_ENTITY_FROM_DCM_PROJECT(
    'DCM_DEMO.PROJECTS.DCM_PROJECT_DEV',
    'DYNAMIC TABLE',
    'DCM_DEMO_1_EA_DEV.ANALYTICS.MENU_ITEM_POPULARITY');
  ```

  Note

  If you want to remove `GRANT` statements for that entity from the definition files without revoking the privileges, also unmanage those
  grants. Pass the `GRANT` statements to [SYSTEM$UNMANAGE\_FROM\_DCM\_PROJECT](/sql-reference/functions/system_unmanage_from_dcm_project).
- [SYSTEM$UNMANAGE\_FROM\_DCM\_PROJECT](/sql-reference/functions/system_unmanage_from_dcm_project) unmanages the entities, grants, and data metric function attachments
  that you specify with definition statements. The function accepts `DEFINE`, `GRANT`, and `ATTACH DATA METRIC FUNCTION` statements as
  they appear in DCM Projects definition files. Each statement must match
  the statement as written in the definition files. You can copy the statements from your definition files into the function argument. Jinja templating isn’t supported, so pass the rendered statements.

  The function processes the statements as a single batch. If any statement contains a syntax error or references an object that doesn’t
  exist, the whole call fails and nothing is unmanaged. Statements for items that the DCM project doesn’t manage are skipped without an
  error.

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

  Note

  Pass a `GRANT OWNERSHIP` statement to `SYSTEM$UNMANAGE_FROM_DCM_PROJECT` before you remove it from the definition files if ownership
  should stay with the current owner role. Removing the statement and deploying grants ownership back to the DCM project owner role. See
  [OWNERSHIP grants](/user-guide/dcm-projects/dcm-projects-supported-entities#label-dcm-projects-object-type-grant-ownership).

Both functions return the number of items that were unmanaged. `SYSTEM$UNMANAGE_FROM_DCM_PROJECT` counts every `DEFINE`, `GRANT`, and
`ATTACH DATA METRIC FUNCTION` item, so the preceding example returns `3` when the DCM project manages all three items.

To call either function, the role needs OWNERSHIP on the DCM project. On the entities, the role only needs a privilege that makes them
visible, such as SELECT on a table. OWNERSHIP of the entities isn’t required.

**Limitation:** Of the `ATTACH` statements, the unmanage functions support only `ATTACH DATA METRIC FUNCTION`. Unmanaging tag
attachments (`ATTACH TAG`) and policy attachments, such as `ATTACH MASKING POLICY`, isn’t supported.

## Purge a DCM project

When you create temporary DCM project objects as development sandboxes or for demos, the
[EXECUTE DCM PROJECT](/sql-reference/sql/execute-dcm-project) command with the `PURGE` option lets you clean up the entire project in a single
statement. `PURGE` runs a deployment without any definitions, which drops all entities, revokes all grants, and removes all
attachments the project currently manages.

Warning

`PURGE` is destructive by design. Use it only for non-production projects, such as development sandboxes or demos.

To fully tear down a temporary DCM project, run two commands:

1. `EXECUTE DCM PROJECT <name> PURGE` drops all entities, grants, and attachments the project manages.
2. `DROP DCM PROJECT <name>` removes the project object itself.

For example:

Copy code

```
EXECUTE DCM PROJECT my_project PURGE AS "sandbox_cleanup";
DROP DCM PROJECT my_project;
```

The purge execution appears in the deployment history of the DCM project, so you can confirm that it ran successfully. For
more information about dropping the project object, see [Drop a DCM project](#label-dcm-projects-drop).

## Drop a DCM project

When a DCM project object is dropped, all managed entities, grants, and attachments remain in place as “unmanaged”.

Important

Dropping or replacing a DCM project object causes you to lose all deployment history artifacts that the object contains.

SQLSnowflake CLISnowsight

Copy code

```
DROP DCM PROJECT [IF EXISTS] <my_project>;
```

Copy code

```
snow dcm drop my_project
```

1. In the navigation menu, select **Catalog** » **Explorer**.
2. Navigate to the schema that contains the DCM project.
3. Select the DCM project to see its details page.
4. Select the 3-dot menu in the top right, and then select **Drop**.
