# Monitor and troubleshoot DCM Projects

This topic describes how to monitor DCM deployments and troubleshoot failing DCM plans.

## Troubleshoot a DCM project

If you are unfamiliar with the DCM project, you might run into errors from misconfigurations or other common pitfalls. This section
describes those errors and how to resolve them.

### Common causes for errors

The following table lists common causes for errors in a DCM project execution:

| Error category | Common causes |
| --- | --- |
| Secondary roles | - DCM PLAN and DEPLOY always execute using only the primary role’s privileges, regardless of whether the session has secondary roles active. - A DDL statement that succeeds when run manually may fail in DCM PLAN if the manual run relied on privileges from a secondary role that DCM doesn’t use. |
| Insufficient role privileges | - Insufficient role privileges to create defined object types - Insufficient role privileges to alter or drop existing objects that are now owned by another role - Insufficient role privileges to use system DMFs - Insufficient role privileges to run a warehouse to refresh a dynamic table at creation |
| Jinja rendering issues | - Jinja rendering issues from incorrect Jinja syntax - Jinja rendering issues from value-type mismatches |
| Project issues | - Incorrect manifest path - Empty definition folders - Outdated definition files on the wrong repo branch - Objects that are already deployed by another DCM project - Mismatched project and object references |

Expand

Show lessSee more

### Recommended troubleshooting steps

Follow these steps to troubleshoot and debug a DCM project.

| Step | Details |
| --- | --- |
| Set secondary roles to none | - DCM always executes with the primary role only. If a DDL statement works when you run it manually but fails in DCM PLAN or DEPLOY, you may be relying on privileges from a secondary role without realizing it. - To reproduce the exact privilege context that DCM uses, run `USE SECONDARY ROLES NONE;` before testing the statement manually. If the statement fails, the primary role is missing a required privilege. - For service users running DCM in CI/CD pipelines, secondary roles are typically not active, so this is also important for ensuring consistent behavior across environments. |
| Use error messages from PLAN | - See if the error message refers to a specific file and line number. - Review the code in the specified line of the source file. - Optionally, open the corresponding rendered output file from the `out/plan/sources/definitions` folder. |
| Narrow down | - Run PLAN on the project with only an empty SQL file in the definitions folder to confirm that project privileges and settings are correct. - Gradually add definition files back to the project. |
| Change the client | - If the CI/CD workflow fails, try running the same CLI commands locally. - If the local CLI commands fail, try running them in Workspaces. - Run `snow connection test` to check the account, role, and user. |
| Use Cortex Code for AI-assisted debugging | - Start Cortex Code with the DCM skill and describe the error. - Cortex Code can read plan output, diagnose Jinja rendering issues, identify privilege gaps, and suggest fixes. - Especially useful for complex Jinja templating errors and dependency resolution issues. |

Expand

Show lessSee more

## Observe and audit DCM project deployments

DCM Projects are designed to provide full transparency and audit trails for all changes to your account infrastructure. This requires you to follow
a few software development best practices for setting up infrastructure deployment processes. For more information, see
[Automate a DCM project deployment](/user-guide/dcm-projects/dcm-projects-use#label-dcm-deployment-automation).

Use the following sources to review previous deployments:

- [Deployment artifacts](#label-dcm-projects-deployment-artifacts) stored inside the DCM project
- [Deployment history](#label-dcm-projects-deployment-history)
- [Event logs](#label-dcm-projects-event-logging) from a DCM project (depending on log-level settings)

### Deployment artifacts

For every executed deployment, an immutable snapshot of the deployment artifacts is stored inside the DCM project, with the following
information:

- The manifest file (`manifest.yml`)
- All object definition and macro files (`.sql` files) inside the `sources` folder
- The output of the PLAN operation (`plan_result.json`) and the DEPLOY operation (`deploy_result.json`), including:
  - The templating variables used for this deployment
  - Deployment metadata, including timestamp, object name, and query ID
  - The changeset

This complete set makes all deployment actions reproducible for debugging, auditing, or redeploying
the defined state. Deployment artifacts remain inside the DCM project for as long as the project object exists, which
makes them the canonical audit trail for a DCM project. The [Deployment history](#label-dcm-projects-deployment-history) function is a
faster, higher-level way to query this information.

The following commands are available for observing and auditing a DCM project:

- With the MONITOR privilege, you can:

  - List all deployments stored inside the DCM project.
  - List all files inside a specified deployment.
  - Read, copy, or download specific files inside that deployment.
- With the OWNERSHIP privilege, you can manually drop a deployment if it contains sensitive data.
- With the READ privilege, you can run the DESCRIBE command to see the most recent deployment name, alias, and timestamp for a selected DCM project.

Example commands:

SQLSnowflake CLI

Copy code

```
DESCRIBE DCM PROJECT DCM_DEMO.PROJECTS.DCM_PROJECT_DEV;

SHOW DEPLOYMENTS IN DCM PROJECT DCM_DEMO.PROJECTS.DCM_PROJECT_DEV;

LIST 'snow://project/DCM_DEMO.PROJECTS.DCM_PROJECT_DEV/deployments/DEPLOYMENT$1/';

ALTER DCM PROJECT DCM_DEMO.PROJECTS.DCM_PROJECT_DEV DROP DEPLOYMENT DEPLOYMENT$1;
```

Copy code

```
snow dcm describe

snow dcm describe --target STAGE

snow dcm list-deployments

snow dcm drop-deployment 'DEPLOYMENT$1'
```

### Deployment history

The `DCM_DEPLOYMENT_HISTORY` Information Schema table function provides role-based access and low-latency ways to see successful and failed deployments for a selected DCM project.

For the full syntax, arguments, output columns, and examples, see the
[DCM\_DEPLOYMENT\_HISTORY](/sql-reference/info-schema/dcm_deployment_history) reference.

Note

The DCM\_DEPLOYMENT\_HISTORY function returns deployments from the past 12 months only. There is no ACCOUNT\_USAGE view
equivalent. Older deployments remain available as [deployment artifacts](#label-dcm-projects-deployment-artifacts)
inside the DCM project for as long as the project object exists, so the artifacts (not this function) are the canonical
long-term audit trail.

SQLSnowsight

Copy code

```
SELECT *
FROM
  TABLE (DCM_DEMO.INFORMATION_SCHEMA.DCM_DEPLOYMENT_HISTORY(
    project_name => 'DCM_DEMO.PROJECTS.DCM_PROJECT_DEV',
    result_limit => 50
  ));
```

To see your deployment history in Snowsight:

1. In the navigation menu, select **Catalog** » **Explorer**.
2. Navigate to the schema that contains the DCM project.
3. Select the DCM project object to see its details.
4. Select the **Deployment History** tab to see a list of all deployments from this project object.
5. Select a deployment from the table to see:

   - Deployment metadata, such as the timestamp and the templating configuration values applied for the deployment.
   - A list of every entity that was created, altered, or dropped during the deployment.
6. Expand the card of any created or altered entity to see more details about the change.

### Event logs

You can set the preferred LOG\_LEVEL on the DCM project object or inherit the defined LOG\_LEVEL from the parent schema, database, or account.

If the LOG\_LEVEL for the DCM project is set, failed PLAN and DEPLOY executions are logged with the corresponding error messages
as an event, and you can see them by querying the defined event table. For more information about setting up event tables and log levels,
see [Event table overview](/developer-guide/logging-tracing/event-table-setting-up).

For example:

SQLSnowflake CLISnowsight

Copy code

```
SELECT
  TIMESTAMP,
  RESOURCE_ATTRIBUTES:"snow.executable.name" ::STRING AS PROJECT_NAME,
  CASE
    WHEN RESOURCE_ATTRIBUTES:"snow.project.dcm.execution.command" ::STRING = 'plan' THEN 'PLAN'
    WHEN RESOURCE_ATTRIBUTES:"snow.project.dcm.execution.command" ::STRING = 'deploy' THEN 'DEPLOY'
    ELSE RESOURCE_ATTRIBUTES:"snow.project.dcm.execution.command" ::STRING
  END AS COMMAND,
  CASE
    WHEN VALUE:"state" ::STRING = 'SUCCEEDED' THEN 'SUCCEEDED'
    WHEN VALUE:"state" ::STRING = 'FAILED' THEN 'FAILED'
    ELSE VALUE:"state" ::STRING
  END AS STATUS,
  COALESCE(
    CONCAT('Error message: ',VALUE:"message"::STRING),
    VALUE:"operation"::STRING)
  AS OPERATIONS,
  RESOURCE_ATTRIBUTES:"snow.session.role.primary.name" ::STRING AS ROLE,
  RESOURCE_ATTRIBUTES:"db.user" ::STRING AS USER_NAME,
  RECORD:"severity_text" ::STRING AS SEVERITY
FROM
  SNOWFLAKE.TELEMETRY.EVENTS
WHERE
  RESOURCE_ATTRIBUTES:"snow.executable.type" ::STRING = 'DCM_PROJECT'
ORDER BY
  TIMESTAMP DESC
LIMIT
  250;
```

Copy code

```
snow logs dcm_project DCM_DEMO.PROJECTS.DCM_PROJECT_DEV \
  --from SNOWFLAKE.TELEMETRY.EVENTS
```

1. In the navigation menu, select **Monitoring** » **Traces & logs**.
2. Select the **Logs** tab.
3. Select the appropriate event table.
4. Filter by the project’s parent database or schema.
