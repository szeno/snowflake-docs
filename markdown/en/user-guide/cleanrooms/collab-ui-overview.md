# Data Clean Rooms UI in Snowsight

[Preview Feature](/release-notes/preview-features) — Open

Currently available in [these regions](/user-guide/cleanrooms/installing-dcr#label-dcr-supported-regions).

Not available in government and VPS deployments.

You can manage Snowflake Data Clean Rooms collaborations directly in the Snowsight UI.
The Snowsight UI lets you view, create, join, and manage collaborations, as well as
run analysis templates and manage data offerings and templates within a collaboration.

The Snowsight UI is organized into the following top-level tabs:

- **Collaborations**: Create and manage the collaborations that you share with your
  collaborators.
- **Templates**: Create, register, and manage analysis templates before adding them to
  collaborations.
- **Data Offerings**: Create, register, and manage data offerings before adding them to
  collaborations.

This separation lets developers build and manage templates and data offerings
independently, so collaborators can then use those objects in their collaboration workflows.

The Snowsight interface works on top of the Collaboration API, so any collaboration
created through the API is visible in the UI, and any collaboration created through the UI
is accessible through the API.

The Snowsight UI also integrates with [Cortex Code](/user-guide/cortex-code/cortex-code-snowsight),
letting you use natural language to explain collaborations, get suggestions during creation,
validate specs, and generate run analysis configurations. Cortex Code actions are available
throughout the UI on collaboration cards, detail pages, and wizards. To use Cortex Code,
your role must meet the [Cortex Code access control requirements](/user-guide/cortex-code/cortex-code-snowsight#label-cortex-code-snowsight-access-control).

## Requirements

Before you can use the Snowflake Data Clean Rooms UI, you must meet the following requirements:

- You must install the Snowflake Data Clean Rooms environment. For more information, see
  [Installing the Snowflake Data Clean Rooms environment](/user-guide/cleanrooms/installing-dcr).
- You must have the appropriate [collaboration privileges](/user-guide/cleanrooms/manage-access)
  granted to your role.
- Your clean rooms environment must be version 14.6 or later. For more information, see
  [Managing clean room environment updates](/user-guide/cleanrooms/managing-updates).

## Navigate to Snowflake Data Clean Rooms

To access the Snowflake Data Clean Rooms UI:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Data sharing** » **Data clean rooms**.

## Select a role

You can select a role from the role selector in your profile menu at the bottom left of
Snowsight. The role determines which collaborations and actions are available to you.
Only collaborations that your selected role has access to are displayed.

For more information about collaboration privileges and roles, see
[Managing access to collaborations, resources, and data](/user-guide/cleanrooms/manage-access).

## Supported workflows

The Snowsight UI for Snowflake Data Clean Rooms supports the following workflows:

- [View collaborations](/user-guide/cleanrooms/collab-ui-listing): Browse your joined
  and invited collaborations, filter, search, and sort.
- [View collaboration details](/user-guide/cleanrooms/collab-ui-details): Drill into a
  collaboration to see collaborators, templates, data offerings, and the collaboration spec.
- [Create a collaboration](/user-guide/cleanrooms/collab-ui-create): Use a step-by-step
  wizard to create a new collaboration.
- [Review and join a collaboration](/user-guide/cleanrooms/collab-ui-join): Review
  invitations and join collaborations shared with your account.
- [Edit a collaboration](/user-guide/cleanrooms/collab-ui-manage): Share templates, share
  data offerings, approve template requests, and leave or tear down collaborations.
- [Run analysis and activation](/user-guide/cleanrooms/collab-ui-run-analysis): Run analysis and
  activation templates via workspaces or Cortex Code.
- [Manage templates](/user-guide/cleanrooms/collab-ui-templates): Browse, search, create, and
  inspect the analysis and activation templates registered in your account.
- [Manage data offerings](/user-guide/cleanrooms/collab-ui-data-offerings): Browse, search,
  create, and inspect the data offerings registered in your account.
