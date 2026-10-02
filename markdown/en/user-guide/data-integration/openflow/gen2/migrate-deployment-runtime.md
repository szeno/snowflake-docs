# Migrate a gen 1 deployment and runtimes to gen 2

Migration converts an existing gen 1 deployment (`OPENFLOW DATA PLANE INTEGRATION`) and all of
its runtimes (`OPENFLOW RUNTIME INTEGRATION`) into first-class gen 2 `OPENFLOW DEPLOYMENT` and
`OPENFLOW RUNTIME` objects. The migration is triggered from the Openflow UI and runs as a managed
Snowflake operation.

Gen 1 connectors on the runtimes are **not** affected by this migration. They continue running
as before. Migrating connectors is a separate follow-on operation; see
[Migrate a gen 1 connector to gen 2](/user-guide/data-integration/openflow/gen2/migrate-connector).

Before you migrate, review [Openflow gen 1 and gen 2](/user-guide/data-integration/openflow/gen2/openflow-generations) to understand
how gen 2 deployments, runtimes, and connectors differ from gen 1 in privileges, lifecycle, and
available operations.

## Before you migrate

### Role and privilege requirements

- The migrating role must have `OWNERSHIP` on the gen 1 deployment.
- The migrating role must have `OWNERSHIP` or `OPERATE` on **all** runtimes under that deployment.
- For each runtime’s target schema, the migrating role must have `USAGE` on the database and
  schema and be able to grant that `USAGE` to other roles. Meet this requirement in one of three
  ways:
  - `OWNERSHIP` on the target database and schema, OR
  - `USAGE` granted with the `WITH GRANT OPTION` clause:

    Copy code

    ```
    GRANT USAGE ON DATABASE <db_name> TO ROLE <migrating_role> WITH GRANT OPTION;
    GRANT USAGE ON SCHEMA <db_name>.<schema_name> TO ROLE <migrating_role> WITH GRANT OPTION;
    ```
  - The `MANAGE GRANTS` privilege on the account:

    Copy code

    ```
    GRANT MANAGE GRANTS ON ACCOUNT TO ROLE <migrating_role>;
    ```

This grant-forwarding requirement exists so that after migration, the migrating role can give
`USAGE` on the new runtime’s database and schema to other roles that previously had access to
the gen 1 runtime. The owner of each runtime is granted `USAGE` automatically; other roles need
manual grants (see [After migration: restore access for other roles](#label-openflow-migrate-deployment-runtime-restore-access)).

Tip

Before migrating, run `SHOW GRANTS ON INTEGRATION <runtime_integration_name>` for each runtime
to capture which roles currently have access. You’ll need this list to restore access after
migration.

### Deployment and runtime state requirements

**Deployment:**

- Must be in `ACTIVE` state.
- Must meet the minimum version for migration:
  - Snowflake (SPCS) deployment: `1.44.0` or later
  - BYOC deployment: `1.60.0` or later

**Runtimes:**

- All runtimes under the deployment must be in `SUSPENDED` state before you start.
- All runtimes must be on a recent enough version to support migration. Upgrade to the latest
  runtime version if the **Migrate** option doesn’t appear after meeting all other prerequisites.

## Migrate a deployment and its runtimes

1. Suspend all runtimes under the deployment. All runtimes must be in `SUSPENDED` state before
   the **Migrate** option appears in the deployment action menu.
2. In the Openflow UI, open the deployment’s action menu and select **Migrate**. If the option
   is absent, check the [prerequisites](#label-openflow-migrate-deployment-runtime-prereqs).
3. The migration wizard opens. Enter a name for the new gen 2 deployment. The wizard suggests a
   name based on the existing display name; this becomes a SQL identifier for the new
   `OPENFLOW DEPLOYMENT` object.
4. The wizard shows a list of runtimes that will be migrated. If your role lacks the required
   privileges on any runtime, the wizard prevents you from advancing. Resolve the privilege issue
   and retry.
5. Select a default target database and schema. All runtimes are placed in this schema unless you
   override them individually. To put specific runtimes in a different database or schema, change
   the selection for those runtimes in the runtime list. The wizard validates that your role can
   create runtimes in the selected schema and grant `USAGE` on it to other roles.
6. Review the summary and confirm. The wizard closes and the deployment enters **Migrating** state
   on the **Deployments** tab.
7. Wait for migration to complete. Migration runs as a background operation. You can navigate
   freely while it runs.
8. After migration completes, verify:

   - The deployment appears as a gen 2 `OPENFLOW DEPLOYMENT` object in the Openflow UI.
   - Each runtime appears on the **Runtimes** tab as a gen 2 `OPENFLOW RUNTIME`.
9. Resume any runtimes you want running. Runtimes remain suspended after migration; start each
   one from the **Runtimes** tab when you’re ready.

Note

All runtimes under the deployment are migrated in a single operation. You can’t selectively
migrate individual runtimes while leaving others as gen 1 under the same deployment.

## After migration: restore access for other roles

Gen 2 runtimes are schema-scoped objects. Roles that previously had `MONITOR`, `USAGE`, or
`OPERATE` on a gen 1 runtime integration may not automatically have access to the new gen 2
runtime if they lack `USAGE` on the database and schema it’s now scoped to.

The owner of each runtime is automatically granted `USAGE` on its target database and schema
during migration. For other roles, grant access manually:

Copy code

```
GRANT USAGE ON DATABASE <db_name> TO ROLE <role_name>;
GRANT USAGE ON SCHEMA <db_name>.<schema_name> TO ROLE <role_name>;
```

Repeat for each affected role and runtime. Use the grant list you captured before migration
(see [Before you migrate: role and privilege requirements](#label-openflow-migrate-deployment-runtime-prereqs-privs)) as your checklist.

## Roll back a migration

Rollback is handled by Snowflake Support. If migration fails or produces unexpected results,
contact your Snowflake account team or open a support case. Include your deployment name and
account identifier.

Caution

Rollback is **not possible** after new gen 2 connectors or new gen 2 runtimes have been created
under the migrated deployment.

## Troubleshooting

Use this table to diagnose common migration problems:

| Symptom | Likely cause | Resolution |
| --- | --- | --- |
| **Migrate** option is not visible in the deployment action menu | Missing privileges, or the deployment or its runtimes aren’t in the required state or version | Verify that the role has `OWNERSHIP` on the deployment and `OPERATE` on all runtimes, that all runtimes are `SUSPENDED`, and that the deployment is `ACTIVE` and meets the minimum version. Upgrade the deployment and runtimes to the latest version if the option still doesn’t appear. |
| Wizard blocks at schema selection | Migrating role can’t grant `USAGE` on the selected schema to other roles | Choose a schema you have `OWNERSHIP` on, grant `USAGE` with the `WITH GRANT OPTION` clause on an existing schema, or grant `MANAGE GRANTS` to the migrating role. |
| Migration fails with “No WIF user for legacy runtime” | The BYOC runtime has an external Workload Identity Federation (WIF) user instead of one nested under the integration. This affects a small number of older runtimes. | Identify the WIF user with `SHOW USERS`. Drop it with `DROP USER <wif_user_name>`. Navigate to the **Runtimes** tab in the Openflow UI and reset the **Execute As Role** for the affected runtime. This creates a new WIF user nested under the integration. Retry migration. |
| A role can’t access a runtime after migration | The role lacks `USAGE` on the database and schema the gen 2 runtime is scoped to | Grant `USAGE ON DATABASE` and `USAGE ON SCHEMA` to the affected role. See [After migration: restore access for other roles](#label-openflow-migrate-deployment-runtime-restore-access). |
| Migration appears stuck in Migrating state | Background task is queued or delayed | Wait up to 30 minutes and refresh. If still stuck, contact Snowflake Support with the deployment name and account identifier. |

Expand

Show lessSee more
