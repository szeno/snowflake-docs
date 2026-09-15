# Templates

Feature — Generally Available

Currently available in [these regions](/user-guide/cleanrooms/installing-dcr#label-dcr-supported-regions).

Not available in government and VPS deployments.

Templates are JinjaSQL clean room templates that can be run by specified collaborators.
Any collaborator can share a template with collaborators in a collaboration.
You can request to add or remove only templates that your account has registered.

Continue reading to see how to register and add a template to a collaboration:

## Register a template

Follow these steps to register a template:

1. [Design a template for the collaboration](#label-dcr-design-collaboration-template) and embed it in a [template specification](/user-guide/cleanrooms/spec-template#label-dcr-collaboration-template-yaml).
2. Register the template by calling REGISTER\_TEMPLATE. This returns a template ID that you will use to link the template.

After the template is registered, it can be linked into a collaboration by anyone who has read access to that registry.

## Add a template

The process to request template addition depends on whether the collaboration already exists.

- **To add a template before the collaboration is created,** give the template ID to the collaboration owner, who includes it in the
  [collaboration spec](/user-guide/cleanrooms/spec-collaboration#label-dcr-collaboration-spec-yaml), specifying who can run the template.
  In the following collaboration snippet, `alice` is granted access to run template `bob_template_v1`.

  Copy code

  ```
  ...
  analysis_runners:
    alice:
      templates:
        - id: bob_template_v1
  ...
  ```

- **To add a template to an existing collaboration,** you send a request to all prospective sharers by following these steps:
  1. Call ADD\_TEMPLATE\_REQUEST with the template ID to start the approval flow to add the template to a specific collaboration, for
     specific users.

     All collaborators affected by the template see the request when they call VIEW\_UPDATE\_REQUESTS.
  2. Collaborators who see the request with status PENDING\_MY\_APPROVAL should call APPROVE\_UPDATE\_REQUEST or REJECT\_UPDATE\_REQUEST.

     - If any collaborator rejects the request, the update request is rejected.
     - Collaborators can’t later change an approval to a rejection, or a rejection to an approval.
     - The template would not be shared until *all* requested parties approve the request.
     - After you approve, the status changes to PENDING\_PARTNER\_APPROVAL if other collaborators still need to approve.
  3. When all required collaborators have approved, the status changes to APPROVED and the update is applied automatically. The terminal statuses for an update request are COMPLETED and FAILED. When the request status is COMPLETED, the template is available to the users specified in the add template request. If the request is FAILED, see the DETAILS column in VIEW\_UPDATE\_REQUESTS for failure details. If any collaborator rejects the request, the status is REJECTED and any reason supplied by the rejecting party is visible in the request report.
  4. There might be a short delay after a template is approved by all users before the template is available. Call VIEW\_TEMPLATES to confirm that the template is available to use.

Tip

To see which templates you have registered, call VIEW\_REGISTERED\_TEMPLATES.

See [Run an analysis](/user-guide/cleanrooms/demo-flows/basic-multiparty-collab#label-dcr-collab-run-an-analysis) to learn how to run an analysis.

## Template design

Collaboration templates are the same as [Provider and Consumer Clean Room templates](/user-guide/cleanrooms/custom-templates), with a
few special considerations:

- The template’s `source_table` variable is populated by the collaboration’s data offerings. In most collaboration templates,
  `source_table` is the only data source variable used.
- A template can declare a [preset table](/user-guide/cleanrooms/custom-templates#label-dcr-template-preset-tables) (preview) in its `preset_tables` block. The template can always
  read that dataset, and the analysis runner doesn’t need to supply it during run. A preset table is useful when a template should
  always use specific datasets.
- The template’s `my_table` is used only when an analysis runner is using Snowflake Standard Edition and can’t contribute data offerings
  to a collaboration.
- Columns from the original data sources can be renamed when exposed to the template or user. See [Source column renaming](/user-guide/cleanrooms/resources-data-offerings#label-dcr-source-column-renaming)
  to learn how and when source columns are renamed. Templates and user-provided arguments (such as a join column name) should use the final
  name, not the original name, if the column is renamed.
- Activation templates in a collaboration don’t need to be named `activation_<template_name>`. All other [activation template requirements](/user-guide/cleanrooms/custom-templates#label-dcr-custom-templates-activation) still apply.

For information about custom template syntax in Snowflake Data Clean Rooms, see [Design custom templates](/user-guide/cleanrooms/custom-templates).
