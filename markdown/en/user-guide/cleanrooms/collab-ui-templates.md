# Manage templates in Snowsight

Feature — Generally Available

Currently available in [these regions](/user-guide/cleanrooms/installing-dcr#label-dcr-supported-regions).

Not available in government and VPS deployments.

The **Templates** tab displays the analysis and activation templates registered in your
account. From this tab, you can browse, search, and inspect registered templates, create
new templates, and register new versions of existing templates.

These are the templates registered in your account’s
[registries](/user-guide/cleanrooms/registries), independent of any collaboration. To
share a registered template into a specific collaboration, see
[Edit a collaboration in Snowsight](/user-guide/cleanrooms/collab-ui-manage).

## Navigate to the Templates tab

To access the **Templates** tab:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Data sharing** » **Data clean rooms**.
3. In the page header, select the **Templates** tab.

## Browse templates

The templates listing displays the templates registered in your account. You can view the
listing as cards or as a table by using the **View mode** control (**Grid view** or
**List view**).

For each template, the listing shows:

- **Name**: The template name.
- **Version**: The registered version of the template.
- **Type**: The template type, either **SQL Analysis** or **SQL Activation**.
- **Registry**: The [registry](/user-guide/cleanrooms/registries) where the template is
  registered. Templates in the default account registry show **Default**.
- **Created**: When the template was registered, shown as a relative time such as `2 days ago`.

In grid view, each card also shows the template description.

To open a template’s [detail page](#label-dcr-collab-ui-templates-detail), select its card
or row.

### Filter, search, and sort

You can filter, search, and sort the templates listing:

- **Search**: Use the **Search templates** bar to search for templates by name.
- **Registry**: Use the **Registry** filter to show only templates registered in one or
  more selected registries. Select **All** to clear the filter.
- **Type**: Use the **Type** filter to show only templates of a selected type: **All**,
  **SQL Analysis**, or **SQL Activation**.
- **Sort**: Sort templates by **Newest first** (the default), **Oldest first**,
  **Name (A→Z)**, or **Name (Z→A)**.

### Cortex Code actions

If [Cortex Code](/user-guide/cortex-code/cortex-code-snowsight) is enabled, hover over a
template card or the **Name** cell in list view to access AI actions:

- **Add to Chat**: Open Cortex Code with the template context attached.
- **Explain**: Get an AI-generated summary of the template in Cortex Code.

If Cortex Code isn’t available for your account, these actions are disabled. Hover over a disabled
action to see a popover that says so and links to the Cortex Code documentation. For the roles that
Cortex Code requires, see [Cortex Code access control requirements](/user-guide/cortex-code/cortex-code-snowsight#label-cortex-code-snowsight-access-control).

## Create a template

To register a new template, select **New Template** at the top of the page. In the
**Create new template** dialog:

1. Select the template **Type**: **SQL Analysis** or **SQL Activation**.
2. Select the **Registry** where the template will be registered. Select **Default** to
   register the template in the default account registry.
3. Select **Create with CoCo**.

Cortex Code opens and helps you write and register the template YAML for the template type
and registry that you selected.

Note

This workflow requires [Cortex Code](/user-guide/cortex-code/cortex-code-snowsight).
If Cortex Code isn’t enabled for your account, the **New Template** option isn’t available.

## View template details

The template detail page shows comprehensive information about a single registered
template. The page header shows the template name and version, along with the following
actions:

- **Explain**: Open Cortex Code with an AI-generated explanation of the template.
- **New Version**: Open Cortex Code to help you register a new version of the template.
  Cortex Code uses the current spec as context, proposes the minimal set of changes,
  surfaces any breaking changes, and outputs the resulting YAML.

An overview card below the header shows template metadata, including the template ID, type,
version, registry, creation date, API version, description, and methodology.

The detail page provides the following tabs:

### Details tab

The **Details** tab shows:

- **Parameters**: A table of the template’s parameters, including each parameter’s name,
  type, whether it’s required, its default value, and its description.
- **SQL Template**: The SQL logic for the template, if defined.

For more information about these fields, see
[Template specification](/user-guide/cleanrooms/spec-template).

### Template Spec tab

The **Template Spec** tab displays the full YAML specification for the template. This spec
can be used with the
[Collaboration API](/user-guide/cleanrooms/collaboration-api-reference) to programmatically
manage templates.

### Code Specs tab

The **Code Specs** tab lists the code specs that the template depends on, showing each code
spec’s ID and name. Select a code spec ID to open a panel with its metadata (ID, version,
API version, spec type, registry, creation date, and description) and its YAML
specification.

Note

Only code specs that are linked to a template are visible here. Code specs that aren’t
linked to any template don’t appear in Snowsight.
