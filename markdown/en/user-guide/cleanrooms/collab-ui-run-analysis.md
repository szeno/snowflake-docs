# Run analysis and activation in Snowsight

[Preview Feature](/release-notes/preview-features) — Open

Currently available in [these regions](/user-guide/cleanrooms/installing-dcr#label-dcr-supported-regions).

Not available in government and VPS deployments.

You can run analysis templates in a collaboration directly from Snowsight. There
are two ways to initiate a run: from the collaborations listing page, and from the
collaboration details page.

Note

To run analysis, your role must be an analysis runner in the collaboration with execute
access to the template. For more information, see [Collaborator roles in Collaboration Data Clean Rooms](/user-guide/cleanrooms/roles).

## Run from the collaborations listing

To run analysis from the collaborations listing:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Data sharing** » **Data clean rooms**.
3. On a collaboration card, select **Run**.
4. In the run dialog, select a template to run.
5. Choose a run method:
   - **Open in Workspaces**: Generates a pre-configured `CALL COLLABORATION!RUN(...)`
     SQL statement and opens it in a Snowflake workspace for you to run.
   - **Run**: Opens Cortex Code, which generates a run analysis
     specification based on the selected template and collaboration, and helps you
     configure and run it.

## Run from the collaboration details

To run analysis from the collaboration details page:

1. Navigate to the [collaboration details page](/user-guide/cleanrooms/collab-ui-details#label-dcr-collab-ui-details).
2. Select the **Shared with you** tab.
3. In the **Available Templates to Run** section, select a template to view its details.
4. In the template details drawer, select one of the following:
   - **Open in Workspaces**: Generates a pre-configured SQL statement and opens it in
     a Snowflake workspace.
   - **Run**: Opens Cortex Code to generate and help run a
     analysis specification.

## Run analysis in worksheets

When you select **Open in Workspaces**, a new workspace opens with a pre-configured
SQL statement that calls the collaboration’s `RUN` procedure. The generated SQL includes:

- The collaboration name.
- The selected template ID.
- Placeholder values for template parameters that you need to fill in.

Review the generated SQL, fill in any required parameter values, and run the statement
to run the analysis. Results are returned in the workspace.

## Run analysis with Cortex Code

When you select **Run**, Cortex Code opens with the collaboration and
template context pre-loaded. Cortex Code:

- Generates a run analysis specification based on the selected template.
- Explains the template parameters and suggests appropriate values.
- Helps you configure the analysis interactively through natural language.
- Runs the analysis on your behalf after you confirm.

This option is useful when you’re unfamiliar with a template’s parameters or want
guidance on how to configure the analysis.

## Run activation templates

Activation templates work the same way as analysis templates. When you select
**Open in Workspaces** for an activation template, the generated SQL calls
`COLLABORATION.RUN()` with an activation configuration in the spec.

After the activation runs, the receiving collaborator must call `VIEW_ACTIVATIONS()`
and `PROCESS_ACTIVATION()` to import the results. For more information, see
[Activating query results](/user-guide/cleanrooms/activation).
