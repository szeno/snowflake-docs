# Manage deployed DCM Projects

This topic describes how to manage a deployed DCM project: list the entities and grants it manages, detach objects and
grants, purge a project, and drop a project.

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

## Detach objects from a DCM project

Using the [ALTER <object>](/sql-reference/sql/alter) command with the UNSET DCM PROJECT clause, you can detach an object that was deployed and
is now managed by a DCM project. The command removes the association between the object and the DCM project without dropping the object.
You can use this command when you want to start managing an object by a different DCM project.

Make sure to remove the corresponding DEFINE statement from your [project definition files](/user-guide/dcm-projects/dcm-projects-files#label-dcm-projects-definition-files) before
you deploy it again. Otherwise, the object will be reintegrated into the DCM project.

An example of a SQL command to detach an object from a DCM project:

Copy code

```
ALTER TABLE MY_DB.MY_SCH.MY_TABLE
  UNSET DCM PROJECT;
```

## Detach grants from a DCM project

`ALTER DCM PROJECT ... UNMANAGE GRANT` removes a grant from a project’s management scope without revoking the underlying privilege. The grant remains exactly as it is: only the project’s tracking of it is removed.

Use `UNMANAGE GRANT` when you want to:

- Transfer a grant to a different project or to manual management.
- Clean up stale grant references after an external change: for example, someone outside DCM revoked a privilege.

This is different from removing a grant definition and redeploying. DCM interprets a missing grant definition as intent to revoke, and revokes the grant on the next deployment.

### Required privileges

The role executing `ALTER DCM PROJECT ... UNMANAGE GRANT` must have `OWNERSHIP` on the DCM Project object.
No `REVOKE` privilege or ownership of the target resource is required: the role only needs to be able to see the grant and the securable object.
This means you can clean up grant references even after another role has removed your access to the managed resources.

### Syntax

Copy code

```
ALTER DCM PROJECT <project_name>
  UNMANAGE GRANT <grant_specification>;
```

`<grant_specification>` uses the same grammar as a [GRANT <privilege>](/sql-reference/sql/grant-privilege) statement. Write it exactly as you would write the `GRANT` line in your DCM definition files, omitting the leading `GRANT` keyword.

### Return value

On success, the command returns a message that includes the count of unmanaged grants, for example:

Copy code

```
Unmanaged 3 grants from the project my_project
```

### Next steps after unmanaging

After running `UNMANAGE GRANT`, remove the corresponding `GRANT` statement from your project definition files before the next deployment. If you leave it in place, DCM reintegrates the grant on the next `EXECUTE DCM PROJECT` run.

### Error handling

The command returns an error if:

- The referenced grant or securable object doesn’t exist or isn’t resolvable.
- The role doesn’t have `OWNERSHIP` on the DCM Project.
- The role can’t see the referenced securable object.

The command doesn’t fail silently: every error is reported so you can confirm exactly which grants were unmanaged.

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
