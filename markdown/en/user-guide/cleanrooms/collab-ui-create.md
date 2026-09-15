# Create a collaboration in Snowsight

[Preview Feature](/release-notes/preview-features) — Open

Currently available in [these regions](/user-guide/cleanrooms/installing-dcr#label-dcr-supported-regions).

Not available in government and VPS deployments.

You can create a new collaboration directly in Snowsight using a step-by-step wizard.
The wizard guides you through configuring the collaboration name, adding collaborators,
assigning roles, mapping resources, and reviewing the collaboration before creation.

Note

To create a collaboration, your role must have the CREATE COLLABORATION privilege.
For more information, see [Managing access to collaborations, resources, and data](/user-guide/cleanrooms/manage-access).

To create a collaboration:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Data sharing** » **Data clean rooms**.
3. Select **Create Collaboration**.

The create collaboration wizard opens with four steps.

## Step 1: Collaboration information

Enter the basic information for your collaboration:

- **Collaboration Name**: A unique name for the collaboration.
- **Description**: An optional description of the collaboration’s purpose.

To use Cortex Code to get suggestions for the collaboration name and description, select the
**Suggest** button. Cortex Code analyzes the context and offers recommendations.

Select **Next** to proceed.

## Step 2: Collaborator details

Configure the collaborators who will participate in the collaboration.

Note

Templates and data offerings must be registered in a
[registry](/user-guide/cleanrooms/registries) before they can be added to a
collaboration. You can register them using the
[Collaboration API](/user-guide/cleanrooms/collaboration-api-reference) or
Cortex Code.

**Owner collaborator**

Your account is automatically added as the collaboration owner. You can configure the
following for the owner:

- **Alias**: A display name for your account in this collaboration.
- **Roles**: Select the roles for the owner (Data Provider, Analysis Runner, or both).
- **Template IDs**: Optionally specify template IDs to include from the owner’s account.
- **Data Offering IDs**: Optionally specify data offering IDs to include from the
  owner’s account.

**Additional collaborators**

Select **Add Collaborator** to add other collaborators. For each additional collaborator,
configure:

- **Alias**: A display name for the collaborator.
- **Account Identifier**: The Snowflake account identifier for the collaborator
  (for example, `ORG_NAME.ACCOUNT_NAME`).
- **Roles**: Select the roles for the collaborator (Data Provider, Analysis Runner,
  or both).
- **Template IDs**: Optionally specify template IDs expected from this collaborator.
- **Data Offering IDs**: Optionally specify data offering IDs expected from this
  collaborator.

To use Cortex Code to get suggestions for collaborator roles and resource assignments,
select the **Suggest** button.

Select **Next** to proceed.

## Step 3: Resource mapping

Configure the access and execution rules for the collaboration. This step presents
checkbox matrices that let you control:

- **Data offering access**: Which analysis runners can access which data offerings.
- **Template access**: Which analysis runners can use which templates.
- **Activation destinations**: Which analysis runners can activate results to
  which destinations.

Select the appropriate checkboxes to grant access. To use Cortex Code to get suggestions
for the run configuration, select the **Suggest** button.

Select **Next** to proceed.

## Step 4: Final review

Review the complete collaboration configuration before submitting. The review step displays
a read-only summary organized into tabs:

- **Basic Details**: The collaboration name and description.
- **Collaborators**: A table of all collaborators with their roles and status.
- **Data Offerings**: The data offerings included in the collaboration.
- **Templates**: The templates included in the collaboration.
- **Destinations**: The activation destinations configured for analysis runners.
- **Raw Spec**: The generated YAML specification for the collaboration.

To use Cortex Code to validate the collaboration specification before submitting, select the
**Validate** button. Cortex Code reviews the spec and identifies potential issues.

When you’re satisfied with the configuration, select **Submit**. The collaboration is
created and invitations are sent to the specified collaborators.

### After creation

After you submit the collaboration:

- A loading indicator shows the creation progress.
- On success, you see a confirmation with a **Next Steps** card that provides guidance
  on what to do next, such as sharing templates or linking data offerings.
- On failure, you see an error message with details. Select **Debug** to use
  Cortex Code to help diagnose the issue.

### Auto-join

When creating a collaboration, you can optionally enable auto-join on the review step.
When auto-join is enabled, you select a role and warehouse, and the owner’s account
automatically joins the collaboration after creation without requiring a separate join step.

Note

Auto-join creates a Snowflake task that uses the selected warehouse to complete the join
process. The task consumes compute credits while it runs. If your role isn’t
SAMOOHA\_APP\_ROLE, it must have the EXECUTE TASK account-level privilege. For more
information, see [INITIALIZE](/user-guide/cleanrooms/collaboration-api-reference#label-dcr-collaboration-initialize-reference).
