# Troubleshooting Collaboration Data Clean Rooms

Feature — Generally Available

Currently available in [these regions](/user-guide/cleanrooms/installing-dcr#label-dcr-supported-regions).

Not available in government and VPS deployments.

Consult the following troubleshooting tips when you encounter errors while you work with Collaboration Data Clean Rooms.

## Collaborations

Error:
:   `Pending invitation for collaboration: <collaboration name> not found` although `GET_STATUS` shows the account as `INVITED`.

Cause:
:   If an initial join attempt has failed for some reason, later join attempts will likely fail with this reason.

Solution:
:   Delete and recreate the collaboration.

---

Error:
:   A collaboration that you created is not visible in a collaborator’s account.

Cause:
:   There are several possible reasons:

    - The collaboration was created in a different cloud hosting region and you haven’t enabled
      [cross-cloud auto-fulfillment](/user-guide/cleanrooms/laf).
    - You didn’t share the collaboration, you shared the collaboration with the wrong account, or you opened the wrong collaborator account in the
      Snowsight/SDCR UI/CLI. Confirm that the account where you expect to see your collaboration is the one that you shared the collaboration
      with, and that you’re signed in to that shared account.
    - There is a small delay between publishing a collaboration and when it becomes visible to the collaborator.

Solution:
:   Verify that the collaborator’s account matches the one in your collaboration spec and that cross-cloud auto-fulfillment is enabled if needed. Wait a few moments for the collaboration to propagate.

---

Error:
:   `ReferenceUsageGrantMissingException: Reference usage grants are required for the following databases in your account ...` when a data provider tries to join the collaboration.
    Data providers will see this message when they try to join a collaboration, and they have shared data that they don’t have REFERENCE\_USAGE on.
    This is expected behavior.

Solution:
:   The error message includes a database name and a share name. Either someone with REFERENCE\_USAGE on the data, or an ACCOUNTADMIN, must run
    the following SQL command, providing the database and share names given in the error message:

    > Copy code
    >
    > ```
    > GRANT REFERENCE_USAGE ON DATABASE <database_name> TO SHARE <share_name>;
    > ```

    After REFERENCE\_USAGE is successfully granted, the data provider can join the collaboration.

---

Error:
:   `CollaborationListingReplicationPending: The collaboration listing is still replicating to your region. Snowflake usually finishes this within a few minutes. Please try reviewing the collaboration again shortly.` when you call REVIEW or JOIN.

Cause:
:   When a collaboration involves accounts in different regions, the collaboration listing must finish replicating to your region before you can act on the collaboration:

    - **Collaboration owner:** If the owner calls JOIN before replication finishes, JOIN fails and the local status becomes `REPLICATING`.
    - **Other collaborators:** If a collaborator calls REVIEW before replication finishes, REVIEW fails and the local status becomes `REPLICATING`.

Solution:
:   Replication usually finishes within a few minutes. To find out whether it has finished, call [`GET_STATUS`](/user-guide/cleanrooms/collaboration-api-reference#label-dcr-collaboration-get-status-reference). When replication is complete, GET\_STATUS returns one of the following values, which signals that you can retry the operation that failed:

    - `CREATED` for the collaboration owner, who can then call JOIN again.
    - `INVITED` for collaborators other than the owner, who can then call REVIEW again.

## API and permissions

Error:
:   *Unknown user-defined function <function name>*

Cause:
:   If this is a procedure documented for the DCR Collaboration API, you might have misspelled the procedure name.

    If you have not misspelled the procedure name, or if the procedure is a system procedure (that is, it has a `$` in the name), you might
    be using an older version of the API and need to upgrade your Clean Rooms API version.

Solution:
:   - Confirm that you spelled the procedure correctly, and if not, try again with the proper spelling.
    - To update your installation, run the following SQL code:

    Copy code

    ```
    USE ROLE ACCOUNTADMIN;
    CALL SAMOOHA_BY_SNOWFLAKE.APP_SCHEMA.PREPARE_MOUNT_SCRIPT();
    EXECUTE IMMEDIATE FROM @SAMOOHA_BY_SNOWFLAKE.APP_SCHEMA.MOUNT_CODE_STAGE/dcr_loader.sql;
    ```

---

Error:
:   Issues when you create new clean rooms or run collaboration stored procedures.

Cause:
:   If your Snowflake Data Clean Rooms installation is on version 12.3 or earlier, your API environment can be out of date with respect to the native app and automatic updates may have stopped working.

Solution:
:   Run the mount procedure again as `ACCOUNTADMIN`, verify the mount, and optionally turn automatic upgrades back on.

    Copy code

    ```
    USE ROLE ACCOUNTADMIN;

    -- Prepare the mount script
    CALL SAMOOHA_BY_SNOWFLAKE.APP_SCHEMA.PREPARE_MOUNT_SCRIPT();

    -- Execute the mount for Snowflake Data Clean Rooms
    EXECUTE IMMEDIATE FROM @SAMOOHA_BY_SNOWFLAKE.APP_SCHEMA.MOUNT_CODE_STAGE/dcr_loader.sql;

    USE ROLE SAMOOHA_APP_ROLE;
    CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.LIBRARY.CHECK_MOUNT_STATUS();

    -- Optional: prefer automatic upgrades in the future
    CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.LIBRARY.ENABLE_LOCAL_DB_AUTO_UPGRADES();
    ```

---

Error:
:   `Listing '{listing name}' is not fulfilled to your current region. Please request the listing, or if already requested, retry after some time`

Cause:
:   You are using an older version of the Clean Rooms API. This issue was fixed in a more recent version.

Solution:
:   [Update your clean rooms installation](/user-guide/cleanrooms/admin-tasks#label-dcr-updating-cleanrooms-environment).

---

Error:
:   `SQL compilation error: Unknown user-defined function SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.RUN`

Cause:
:   Either you misspelled some part of the fully qualified procedure name, or you do not have privileges to run this procedure.

Solution:
:   Confirm that you used the correct name of the procedure. If you are not using SAMOOHA\_APP\_ROLE, try switching to that role to see if the same error occurs. If it does not, it is a privilege error.

---

Error:
:   `Unknown user-defined function SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.<namespace>.<procedure name>`

Cause:
:   One of the following:

    - You used the wrong namespace. Be sure to call the proper `COLLABORATION` or `REGISTRY` namespace.
    - You mistyped the name of the function. Check the reference guide for the proper naming.
    - You are using an RBAC role that doesn’t have permissions to call the procedure.
    - You don’t have SAMOOHA\_APP\_ROLE.

Solution:
:   - Confirm that you spelled the procedure correctly and used the correct namespace.
    - Try switching to SAMOOHA\_APP\_ROLE to see whether you can run the procedure. If you can, then the issue is insufficient privileges on your current role. Ask someone with SAMOOHA\_APP\_ROLE to [grant you proper privileges](/user-guide/cleanrooms/manage-access#label-dcr-collab-about-rbac-roles).
    - To check if you have SAMOOHA\_APP\_ROLE, run the following command:

    Copy code

    ```
    SELECT CURRENT_USER();
    SHOW GRANTS TO USER <current_user_name> ->> SELECT * FROM $1 WHERE "role" = 'SAMOOHA_APP_ROLE';
    ```

    If you don’t get any results, ask an administrator to give you API access to the collaboration.

## Templates with preset tables

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

The errors in this section apply to templates that declare [preset tables](/user-guide/cleanrooms/custom-templates#label-dcr-template-preset-tables) in a `preset_tables`
block.

Error:
:   `SpecValidationError: preset_tables reference(s) use reserved SQL alias(es)`

Cause:
:   A preset table may not be given the SQL alias `p`, `c`, or `p` or `c` followed by a number in the template body. Those aliases are
    reserved for the `source_table` and `my_table` datasets that the analysis runner supplies.

Solution:
:   In the template body, give the preset table any other valid [Snowflake identifier](/sql-reference/identifiers-syntax) as its SQL
    alias, then register the template again.

---

Error:
:   `SpecValidationError: Template references undeclared preset_tables alias(s)`

Cause:
:   The template body references `preset_tables['<alias>']` or `preset_tables.<alias>` for an alias that isn’t declared in the
    template’s `preset_tables` block.

Solution:
:   Declare the alias in the `preset_tables` block, or correct the alias in the template body so that it matches a declared entry. The two
    must agree exactly.

---

Error:
:   `PresetTableUnsupportedReferenceError: '<alias>' is pinned by this template via preset_table(s) and cannot be used as a Jinja variable or given a policy filter.`

Cause:
:   The template refers to a preset table in one of two unsupported ways:

    - It uses the preset table’s alias as a Jinja variable, such as `{{ publisher.hashed_email }}` or
      `{{ publisher.hashed_email | sqlsafe }}`. A preset table is a SQL identifier, not a template variable.
    - It applies a policy filter such as `column_policy` or `join_policy` to one of the preset table’s columns. Policy filters resolve a
      column’s table by position in the runner-supplied `source_table` list, which a preset table is never part of.

Solution:
:   Reference the preset table’s columns directly by the SQL alias that the preset reference is bound to, with no policy filter.

    Copy code

    ```
    -- Supported
    SELECT publisher.hashed_email FROM IDENTIFIER({{ preset_tables['publisher'] }}) AS publisher;

    -- Not supported
    SELECT IDENTIFIER({{ publisher.hashed_email | column_policy }}) FROM IDENTIFIER({{ preset_tables['publisher'] }}) AS publisher;
    ```

    If the column needs a policy enforced on it, have the analysis runner supply that dataset in `source_tables` instead of presetting it.

---

Error:
:   `CollaboratorAliasNotFoundInCollaboration`, `DataProviderWithoutDataOffering`, or `DatasetNotFoundInDataOfferingException`

Cause:
:   A preset `template_view_name` doesn’t resolve in this collaboration. Either the collaborator alias isn’t in the collaboration spec, the
    data provider hasn’t linked that data offering, or the offering doesn’t contain that dataset.

Solution:
:   Call VIEW\_DATA\_OFFERINGS and copy the value from the TEMPLATE\_VIEW\_NAME column into the template’s `preset_tables` block. Confirm that
    the collaborator alias matches the one in the `collaborator_identifier_aliases` section of the
    [collaboration spec](/user-guide/cleanrooms/spec-collaboration#label-dcr-collaboration-spec-yaml), and that the data provider has linked the offering.

## Code specs

Error:
:   `CodeSpecAlreadyExistsException`

Cause:
:   Code spec with same name and version already registered.

Solution:
:   Use a different version or update the existing version.

---

Error:
:   `SpecValidationError`

Cause:
:   YAML doesn’t conform to schema.

Solution:
:   Check required fields and format.

---

Error:
:   `CodeSpecStageNotAccessibleError`

Cause:
:   Stage referenced in artifact isn’t accessible.

Solution:
:   Grant access to stage or verify stage exists.

---

Error:
:   `CodeSpecArtifactNotFoundAtStageError`

Cause:
:   File not found at specified stage path.

Solution:
:   Upload file to stage before registering.

---

Error:
:   `StageDirectoryNotEnabledError`

Cause:
:   Stage doesn’t have DIRECTORY enabled.

Solution:
:   Enable directory on the stage: `ALTER STAGE ... SET DIRECTORY = (ENABLE = TRUE)`

---

Error:
:   `CodeSpecNotFoundForOwnerException`

Cause:
:   Template references unregistered code spec.

Solution:
:   Register code spec before registering template.

## Activation

Error:
:   `Object 'SFDCR_<name>.CLEANROOM.ACTIVATION_DATA_<results>' does not exist or not authorized` when multiple activations run at the same time. The same activations succeed when run one at a time.

Cause:
:   Concurrent runs of an [activation template](/user-guide/cleanrooms/custom-templates#label-dcr-custom-templates-activation) that writes to a *fixed* results table name collide. Each
    run executes `CREATE OR REPLACE TABLE` against the same `cleanroom.activation_data_` table, so one run can replace or drop the table while
    another run is still using it.

Solution:
:   Use an activation template that generates a unique results table name for each run, so concurrent runs don’t write to the same table. For the
    recommended pattern and an example, see [Running activations concurrently](/user-guide/cleanrooms/custom-templates#label-dcr-custom-templates-activation-concurrency).

## ML Jobs

Error:
:   Copy code

    ```
    Template references unknown code spec callables: 'my_ml_model_V0$my_train_job'.
    'my_ml_model_V0' looks like a code spec ID. Use the code spec name (without the version suffix) instead.
    ```

Cause:
:   The template body references a code spec using the versioned **ID** (for example, `my_ml_model_V0`) instead of the
    **name** (for example, `my_ml_model`). The `code_specs` field in the template uses the ID, but the procedure call in
    the template body must use the name.

Solution:
:   Use the code spec name without the version suffix in the template call body:

    - Correct: `cleanroom.my_ml_model$my_train_job(...)`
    - Incorrect: `cleanroom.my_ml_model_V0$my_train_job(...)`

---

Error:
:   ML Job fails with a warehouse or compute pool error.

Cause:
:   The compute pool was not set up correctly for the clean room application, or GPU compute is not available in
    your region.

Solution:
:   - Verify the compute pool was created with `FOR APPLICATION <installed_app_name>`. ML Jobs require a compute pool
      dedicated to the clean room application.
    - Verify `GRANT USAGE ON COMPUTE POOL` and `GRANT USAGE ON WAREHOUSE` were both granted to the application.
    - The `CREATE COMPUTE POOL` privilege is required at the account level. Use ACCOUNTADMIN or a custom role with this
      privilege.
    - `SYSTEM_COMPUTE_POOL_GPU` is not available in all regions. In regions without GPU support, use
      `SYSTEM_COMPUTE_POOL_CPU` for CPU-based workloads, or create a custom GPU compute pool if your region supports
      GPU hardware. For regional availability, see
      [Compute pools](/developer-guide/snowpark-container-services/working-with-compute-pool#system-compute-pools).

---

Error:
:   Collaboration creation fails and the collaboration moves to the `CREATE_FAILED` state.

Cause:
:   ML Jobs require system compute pools, which are not available in every region. If you enable ML Jobs in a
    collaboration created in a region where system compute pools are unavailable, the code specs cannot be loaded and
    the collaboration moves to the `CREATE_FAILED` state.

Solution:
:   Create the collaboration in a region that supports system compute pools. For regional availability, see
    [Compute pools](/developer-guide/snowpark-container-services/working-with-compute-pool#system-compute-pools).

---

Error:
:   `ADD_TEMPLATE_REQUEST` fails with:

    Copy code

    ```
    ML job '<ml_job_name>' has no content_manifest. Re-register the code spec to generate the manifest.
    ```

Cause:
:   The code spec was registered before content hash validation was added in the
    [June 18, 2026 release](/release-notes/2026/other/2026-06-18-dcr) (Clean Rooms API Version 16.3).
    ML Jobs code specs registered before that release don’t have content hashes and can’t be added to a
    collaboration. Your account must be running Clean Rooms API Version 16.3 or later for content
    hash validation to be enforced.

Solution:
:   Re-register the code spec as a new version: change the `version` field (for example, from `v1`
    to `v2`) and call `REGISTER_CODE_SPEC` again with the same YAML. Re-registration computes
    content hashes automatically. Then update the `code_specs` reference in your template to use
    the new version and resubmit for approval.

    ML Jobs code specs that were already linked to a collaboration before June 18, 2026 continue to work
    without re-registration.
