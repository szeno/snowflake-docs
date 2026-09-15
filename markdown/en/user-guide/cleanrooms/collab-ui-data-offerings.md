# Manage data offerings in Snowsight

[Preview Feature](/release-notes/preview-features) — Open

Currently available in [these regions](/user-guide/cleanrooms/installing-dcr#label-dcr-supported-regions).

Not available in government and VPS deployments.

The **Data Offerings** tab displays the data offerings registered in your account. From
this tab, you can browse, search, and inspect registered data offerings, create new data
offerings, and register new versions of existing data offerings.

These are the data offerings registered in your account’s
[registries](/user-guide/cleanrooms/registries), independent of any collaboration. To
share a registered data offering into a specific collaboration, see
[Edit a collaboration in Snowsight](/user-guide/cleanrooms/collab-ui-manage).

## Navigate to the Data Offerings tab

To access the **Data Offerings** tab:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Data sharing** » **Data clean rooms**.
3. In the page header, select the **Data Offerings** tab.

## Browse data offerings

The data offerings listing displays the data offerings registered in your account. You can
view the listing as cards or as a table by using the **View mode** control (**Grid view**
or **List view**).

For each data offering, the listing shows:

- **Name**: The data offering name.
- **Version**: The registered version of the data offering.
- **Registry**: The [registry](/user-guide/cleanrooms/registries) where the data offering
  is registered. Data offerings in the default account registry show **Default**.
- **Datasets**: The datasets included in the data offering.
- **Created**: When the data offering was registered.

In grid view, each card also shows the data offering description.

To open a data offering’s [detail page](#label-dcr-collab-ui-data-offerings-detail), select
its card or row.

### Filter, search, and sort

You can filter, search, and sort the data offerings listing:

- **Search**: Use the **Search data offerings** bar to search for data offerings by name.
- **Registry**: Use the **Registry** filter to show only data offerings registered in one
  or more selected registries. Select **All** to clear the filter.
- **Sort**: Sort data offerings by **Newest first** (the default), **Oldest first**,
  **Name (A→Z)**, or **Name (Z→A)**.

### Cortex Code actions

If [Cortex Code](/user-guide/cortex-code/cortex-code-snowsight) is enabled, hover over a
data offering card or the **Name** cell in list view to access AI actions:

- **Add to Chat**: Open Cortex Code with the data offering context attached.
- **Explain**: Get an AI-generated summary of the data offering in Cortex Code.

## Create a data offering

To register a new data offering, select **New Offering** at the top of the page. In the
**New Data Offering** dialog:

1. In the **Object Explorer**, select one or more database objects (such as tables or
   views) to include in the data offering.
2. Select the **Registry** where the data offering will be registered. If you don’t
   specify a registry, the data offering is registered in the default account registry.
3. Select **Create with CoCo**.

Cortex Code opens and helps you configure the data offering’s policies and complete the
registration for the data sources that you selected.

Note

This workflow requires
[Cortex Code](/user-guide/cortex-code/cortex-code-snowsight). If Cortex Code isn’t enabled
for your account, the **New Offering** option isn’t available.

## View data offering details

The data offering detail page shows comprehensive information about a single registered data
offering. The page header shows the data offering name and version, along with the following
actions:

- **Explain**: Open Cortex Code with an AI-generated explanation of the data offering.
- **New Version**: Open Cortex Code to help you register a new version of the data offering.
  Cortex Code uses the current spec as context and proposes the changes for the new version.

An overview card below the header shows data offering metadata, including the data offering
ID, API version, version, registry, creation date, number of datasets, and description.

The detail page provides the following tabs:

### Datasets tab

The **Datasets** tab shows a card for each dataset included in the data offering. For each
dataset, you can see:

- **Data object**: The fully qualified name of the underlying object, with a link to view
  it in the Horizon catalog.
- **Allowed analyses**: The analyses permitted on the dataset.
- **Object class**: The object class of the dataset.
- A column policy table showing each column’s category, activation, and source column, or a
  note that no column policies are defined for the dataset.

For more information about these fields, see
[Data offering specification](/user-guide/cleanrooms/spec-data-offering).

### Data Offering Spec tab

The **Data Offering Spec** tab displays the full YAML specification for the data offering.
This spec can be used with the
[Collaboration API](/user-guide/cleanrooms/collaboration-api-reference) to programmatically
manage data offerings.
