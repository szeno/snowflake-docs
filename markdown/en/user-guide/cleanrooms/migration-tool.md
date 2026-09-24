# Snowflake Data Clean Room migration tool

Feature — Generally Available

Currently available in [these regions](/user-guide/cleanrooms/installing-dcr#label-dcr-supported-regions).

Not available in government and VPS deployments.

The legacy Provider and Consumer Data Clean Rooms are being discontinued. Use the migration tool
to move to the [Collaboration API](/user-guide/cleanrooms/overview) before the dates in the
[end-of-life timeline](/user-guide/cleanrooms/pc-eol).

The Snowflake Data Clean Room migration tool helps you migrate legacy Provider and Consumer
clean rooms and webapp clean rooms to the Collaboration API. Given the name of a legacy
clean room, the tool reads its configuration: templates, datasets, join policies, and
consumers. It generates an equivalent Collaboration API setup that produces identical
analysis output. Your original clean room is never modified or removed during this process.

The tool is available as a set of stored procedures you can call directly from a SQL
worksheet. An optional Streamlit in Snowflake app provides a graphical interface for clean room migrations.

For the tool source code and release notes, see the
[Snowflake-Labs/dcr-migration-tool](https://github.com/Snowflake-Labs/dcr-migration-tool)
GitHub repository.

## Requirements

Before using the migration tool, ensure the following:

1. You’re using the `SAMOOHA_APP_ROLE` role, or a role with equivalent permissions.
2. Your clean room is in a healthy state: it has at least one linked dataset, one active
   template, and at least one joined consumer.
3. You’ve reviewed the [supported configurations](#label-dcr-migration-tool-supported)
   table to confirm your clean room is eligible for migration.

Note

If your clean room uses free-form SQL, the migration tool may need to create aggregation
policies. This operation requires `ACCOUNTADMIN` privileges.

## Supported configurations

Use the following table to determine whether your clean room is a candidate for migration.

Note

Clean rooms created before 2024 (prior to the availability of the Provider and Consumer
model) cannot be migrated using this tool.

| Feature | Support | Notes |
| --- | --- | --- |
| Measurement (Jinja SQL templates) | Supported |  |
| Free-form / horizontal SQL | Supported with limitations | The webapp point-and-click interface is not usable with the Collaboration API. You may run free-form SQL using a worksheet. |
| Cross-Cloud Auto-Fulfillment (LAF) support | Supported |  |
| Python jobs, including machine learning | Supported | Python jobs are supported assuming the user is not requesting a compute pool, ML jobs, or SPCS. |
| Iceberg table support | Supported |  |
| Snowpark Container Services (SPCS) | Not supported | Templates that reference SPCS service functions are blocked at pre-flight. |
| DCR Managed Accounts | Supported | Clean rooms operating via managed account may be migrated, but the webapp user interface is not supported by the Collaboration API. Contact your Snowflake account representative for more information. |
| Provider-run analysis | Supported | Supported natively in the Collaboration API without additional configuration. |
| Identity connectors | Not supported | Identity providers may be added as standard collaboration participants (that is, data providers), but the Collaboration API does not support adding identity providers as a named workflow step. |
| Webapp graphical user interface | Supported with limitations | Data Clean Rooms don’t offer a native point-and-click interface equivalent to the webapp for the Collaboration API. |
| Activation | Supported with limitations | Activation to a collaborator’s Snowflake account is supported. Activation to third-party destinations (for example, Google Ads or Meta) is not yet supported. |
| Template chains | Not supported |  |
| Request and activity logs | Not supported | Refers to per-clean-room activity logs in the legacy webapp. These are not available in the Collaboration API. |
| Differential privacy | Not supported |  |

Expand

Show lessSee more

## Migrating webapp clean rooms

The legacy Snowflake Data Clean Room web application (also called the “webapp”) ran on the
Provider and Consumer architecture, but the webapp user interface is not supported by
the Collaboration API.

Some webapp clean rooms use templates named `prod_sql_with_platform_privacy`. The
migration tool detects these templates and marks them as requiring manual reconstruction
as Free-form SQL data offerings. They are not converted automatically.

If you would like to migrate your existing web application to the Collaboration API, you
may create a point-and-click interface for your users by using a Streamlit application.
For more information, see [Supporting business users](#label-dcr-migration-tool-business-users).

## Deploy the tool

Deploy the migration tool once per Snowflake account. Always deploy to the Provider
account first, then to each Consumer account.

### Deploy the backend (required)

1. Download `migration-backend.sql` from the
   [Snowflake-Labs/dcr-migration-tool](https://github.com/Snowflake-Labs/dcr-migration-tool)
   GitHub repository.
2. In Snowsight, open a new SQL worksheet and run the contents of
   `migration-backend.sql`.

Note

You don’t need to redeploy the tool if you run another migration in the same account
later. The deployment is reusable.

### Deploy the Streamlit interface (optional)

The Streamlit app provides a graphical interface for the same stored procedures. All
migration actions can also be performed directly via SQL. The Streamlit interface supports
Provider and Consumer clean room migrations; webapp clean room migrations must be run via
SQL worksheet.

To deploy the Streamlit app:

1. Download `streamlit_app.py` from the GitHub repository.
2. In Snowsight, navigate to **Streamlit** and click **+ Streamlit App**.
3. Name the app **DCR Migration Tool**, set the database to `DCR_SNOWVA` and
   the schema to `MIGRATION`, paste the contents of `streamlit_app.py` into the
   editor, and click **Create**.

Note

By default, only the app creator can see the app. Use **Share this app** in Snowsight
to grant access to other users.

## Migrate a clean room

Migration follows four phases: Plan, Execute, Finalize, and Validate. Steps 1 and 5
below wrap those core phases with a review step before you begin and an optional
validation step at the end. Each phase is available as a tab in the Streamlit app
and as a stored procedure call.

### Step 1: Review eligible clean rooms

To view the clean rooms in your account and their eligibility for migration, run the
following command, or open the Streamlit app:

Copy code

```
USE ROLE SAMOOHA_APP_ROLE;
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.PROVIDER.view_cleanrooms();
```

Each clean room is classified as one of the following:

- **Eligible**: ready to migrate.
- **Ineligible**: blocked by an unsupported configuration. The reason is shown.
- **Internal (UUID)**: orphaned or test clean rooms; skipped automatically.

Review the list and determine which clean rooms to migrate.

### Step 2: Plan the migration

The Plan phase is read-only. It discovers the clean room’s configuration, translates it
into Collaboration API YAML specifications, and returns a generated SQL script for your
review without making any changes to your account.

The tool automatically detects whether the current account is the Provider or the
Consumer, and generates the appropriate script for each.

**In the Streamlit app**: select a clean room, then click the **View Script** tab.

**Via SQL**:

Copy code

```
USE ROLE SAMOOHA_APP_ROLE;

CALL DCR_SNOWVA.MIGRATION.AGENT_MIGRATE_ORCHESTRATOR(
    '<cleanroom_name>',
    'PLAN'
);
```

The output includes:

- Template YAML specs. Template names are versioned automatically (for example,
  `migrated_my_template_2026_04_07_V1`).
- Data offering YAML specs. Table names with dot notation are converted to use underscores.
- A collaboration spec with the `analysis_runners` block configured to match your clean
  room’s topology.
- Any warnings that must be resolved before you execute the migration.

Common warnings and how to resolve them:

| Warning | Resolution |
| --- | --- |
| `ReferenceUsageGrantMissingException` | Run the following as `ACCOUNTADMIN` before executing: `GRANT REFERENCE_USAGE ON DATABASE <db> TO SHARE <share>;` |
| Consumer data offerings are empty | Verify the consumer has linked datasets and correct join policies configured. |
| Provider-run analysis detected | The consumer must also run the migration and link their data offerings. |

Expand

Show lessSee more

### Step 3: Execute the migration (Provider account)

The Execute phase writes to your account. It registers your templates and data offerings,
then initializes the new clean room. The operation is idempotent: if it’s interrupted,
it’s safe to run again.

**In the Streamlit app**: click the **Execute Migration** tab and confirm.

**Via SQL**:

Copy code

```
USE ROLE SAMOOHA_APP_ROLE;

CALL DCR_SNOWVA.MIGRATION.AGENT_MIGRATE_ORCHESTRATOR(
    '<cleanroom_name>',
    'EXECUTE'
);
```

During execution, the tool:

1. Calls `REGISTRY.REGISTER_TEMPLATE` for each template.
2. Calls `REGISTRY.REGISTER_DATA_OFFERING` for each dataset.
3. Fetches system-generated resource IDs from `REGISTRY.VIEW_REGISTERED_TEMPLATES`.
4. Regenerates the collaboration spec using the authoritative IDs.
5. Calls `COLLABORATION.INITIALIZE` to create the new clean room.
6. Polls the status and waits for `CREATED` before calling `COLLABORATION.JOIN`.

### Step 4: Finalize: consumer joins the collaboration

After the Provider executes the migration, each Consumer account must also deploy the
tool and run their migration steps. The Consumer runs the same Plan → Execute flow in
their account, using the same clean room name.

Important

The JOIN command requires `SYSTEM$ACCEPT_LEGAL_TERMS`, which can’t execute from
within a Streamlit app. Whether you’re using the Streamlit interface or running SQL
directly, you must copy the generated JOIN script and run it in a Snowflake SQL
worksheet. The Streamlit app provides the ready-to-paste snippet on the **Finalize**
tab.

The Consumer migration:

1. Checks prerequisites in the Consumer account context.
2. Reads Consumer-side metadata (data offerings, join policies, column policies).
3. Generates a Consumer-side collaboration spec.
4. Calls `COLLABORATION.JOIN` to join the new clean room.
5. Links consumer data offerings to the Provider account via `link_data_offering`.

### Step 5: Validate

The Validate phase confirms that the migrated collaboration is equivalent to the original
clean room.

**In the Streamlit app**: click the **Validate** tab.

**Via SQL**:

Copy code

```
USE ROLE SAMOOHA_APP_ROLE;

CALL DCR_SNOWVA.MIGRATION.AGENT_MIGRATE_ORCHESTRATOR(
    '<cleanroom_name>',
    'VALIDATE'
);
```

Validation checks:

- The collaboration status is `CREATED` (Provider) or `JOINED` (Consumer).
- The template count matches the legacy clean room.
- The data offering count matches.
- The consumer count matches.

If validation passes, your original clean room is still intact. Don’t drop it until
you’ve confirmed that your pipelines are running correctly against the new collaboration.

## Roll back a migration

To undo a migration, use `TEARDOWN` mode. This removes the migrated collaboration only. Your original clean room is never affected.

**In the Streamlit app**: click the **Undo** tab.

**Via SQL**:

Copy code

```
USE ROLE SAMOOHA_APP_ROLE;

CALL DCR_SNOWVA.MIGRATION.AGENT_MIGRATE_ORCHESTRATOR(
    '<cleanroom_name>',
    'TEARDOWN'
);
```

Note

Teardown is a two-step asynchronous process. The procedure polls `GET_STATUS` until
the status is `LOCAL_DROP_PENDING`, then calls `TEARDOWN` a second time to complete
the operation.

## View migration history

Every action taken by the tool is logged to the
`DCR_SNOWVA.MIGRATION.MIGRATION_JOBS` table. Query this table at any time to audit
migration activity.

| Column | Description |
| --- | --- |
| `JOB_ID` | Unique identifier for this job. |
| `CLEANROOM_NAME` | Name of the source clean room. |
| `ACTION` | Mode that was run: `PLAN`, `EXECUTE`, `VALIDATE`, or `TEARDOWN`. |
| `ROLE` | Role used during execution. |
| `STARTED_AT` / `FINISHED_AT` | Execution timestamps. |
| `STATUS` | `SUCCESS` or `FAILED`. |
| `DETAILS` | First 4,000 characters of the result JSON. |

Expand

Show lessSee more

In the Streamlit app, click **Migrated DCRs** to view a collapsible summary of all
migrations run from this account, with live status and a full history for each clean room.

## Troubleshooting

### CleanroomNotInstalled error

The clean room name is incorrect or you’re using the wrong account. List your available
clean rooms to verify the exact name:

Copy code

```
USE ROLE SAMOOHA_APP_ROLE;
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.PROVIDER.view_cleanrooms();
```

### Pre-flight failure: multi-provider configuration detected

Multi-provider clean rooms aren’t supported in this release. Contact your solutions
engineer to discuss options, or proceed with eligible single-provider clean rooms.

### Analysis output doesn’t match after migration

This can occur when a clean room used provider-run analysis. In the Provider and Consumer
architecture, `source_table` always referred to the provider’s table; in the
Collaboration API, this mapping may be reversed. Review the generated template YAML in
Plan mode and check whether `source_table` and `my_table` need to be swapped.

### Missing REFERENCE\_USAGE grant

If you see a missing reference usage grant error when joining the collaboration, run the
following as `ACCOUNTADMIN`:

Copy code

```
GRANT REFERENCE_USAGE ON DATABASE <provider_database> TO SHARE <collab_share>;
```

For more information, see [Troubleshooting Collaboration Data Clean Rooms](/user-guide/cleanrooms/v2/troubleshooting).

## Supporting business users

The legacy webapp provided a point-and-click interface that let users run analyses without
writing SQL. The Collaboration API doesn’t currently have full feature parity with the
legacy webapp in the Snowflake interface.

If you need to use the Collaboration API today and must support a point-and-click interface,
you may build a Streamlit in Snowflake application that wraps Collaboration API calls in
a purpose-built UI tailored to your users’ workflows. A Streamlit app can expose exactly
the analyses your business users need, for example audience overlap or reach and frequency,
without requiring them to write SQL.

The Snowflake SE team can help you design and build a Streamlit app tailored to your
workflows. Contact your Snowflake account representative for more details.

To get started building Streamlit apps on Snowflake, see:

- [About Streamlit in Snowflake](/developer-guide/streamlit/about-streamlit): architecture, supported libraries,
  and security model.
- [Create your Streamlit app](/developer-guide/streamlit/app-development/creating-your-app): how to create,
  edit, and share a Streamlit app in Snowsight.
