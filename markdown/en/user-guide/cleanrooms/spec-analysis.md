# Analysis specification

Feature — Generally Available

Currently available in [these regions](/user-guide/cleanrooms/installing-dcr#label-dcr-supported-regions).

Not available in government and VPS deployments.

Specifies all the information that analysis runners need to run an analysis, including which template to use, which tables to pass to the
template, and any variable values used by a template. If not using free-form SQL to query data, any analysis runners that want to run an
analysis use this specification to define the template and input data.

**Schema:**

Copy code

```
api_version: 2.0.0              # Required: Must be "2.0.0"
spec_type: analysis             # Required: Must be "analysis"
template: <template_id>         # Required: ID of the template to use
name: <analysis_name>           # Optional: Unique name (max 75 chars)
version: <version_string>       # Optional: Version identifier (max 20 chars)
description: <analysis_description>  # Optional: Description (max 1,000 chars)

template_configuration:         # Optional: Values used when running the template
  view_mappings:                # Optional: Mappings for shared data
    source_tables:              # Optional: Tables from data offerings. Populates the source_table array variable.
      - <source_table_name>     # One or more source table names from the TEMPLATE_VIEW_NAME column...
    <argument_name>: <view_name>  # Custom argument to template view name mapping
  local_view_mappings:          # Optional: Mappings for local data
    my_tables:                  # Optional: Tables from local data offerings. Populates the my_table array variable.
      - <my_table_name>         # One or more local table names...
    <argument_name>: <view_name>  # Custom argument to local template view name mapping
  arguments:                    # Optional: Template arguments as key-value pairs
    <argument_name>: <argument_value>  # One or more argument key-value pairs...
  activation:                   # Required for activation templates
    snowflake_collaborator: <alias>  # Collaborator alias for activation destination
    segment_name: <segment_name>     # Unique segment name for this activation
```

`api_version`
:   The version of the Collaboration API used. Must be `2.0.0`.

`spec_type`
:   Specification type identifier. Must be `analysis`.

`template: template_id`
:   The ID of the template to use for this analysis. This must be the template ID obtained when the template was registered, not the template
    name.

`name` (*Optional*)
:   A unique, user-friendly name for this analysis. Must follow [Snowflake identifier rules](/sql-reference/identifiers-syntax) with a
    maximum of 75 characters and be unique within your Snowflake data clean room account.

`version` (*Optional*)
:   A version identifier for this analysis specification (maximum 20 characters). Must follow
    [Snowflake identifier rules](/sql-reference/identifiers-syntax) and be unique within your account for this analysis name. A good
    format to use is *YYYY\_MM\_DD\_V#*. For example: `2025_10_22_V1`.

`description` (*Optional*)
:   A high-level description of what this analysis does (maximum 1,000 characters).

`template_configuration` (*Optional*)
:   Values used when running the specified template.

    `view_mappings` (*Optional*)
    :   Mapping of argument names to template view names for shared data offerings.

        `source_tables` (*Optional*)
        :   List of view names to populate the `source_table` template variable. Use the table aliases specified in the data offering spec. You
            can get a list of available views by calling VIEW\_DATA\_OFFERINGS. Use the view names from the TEMPLATE\_VIEW\_NAME column. Format of
            each entry is `collaborator_alias.data_offering_ID.dataset_alias`.

            List only the datasets that the template takes through `source_table`. Don’t list datasets that the template author
            [preset in the template](/user-guide/cleanrooms/custom-templates#label-dcr-template-preset-tables) (preview) in its `preset_tables` block; those are supplied by the
            template. If a template pins every dataset it reads, omit `source_tables`.

        `argument_name: view_name`
        :   Custom mapping of an argument name to a template view name (maximum 255 characters each).

    `local_view_mappings` (*Optional*)
    :   Mapping of argument names to local template view names for private datasets.

        `my_tables` (*Optional*)
        :   List of table names to populate the `my_table` template variable. This is available only to private datasets that you linked by
            calling LINK\_LOCAL\_DATA\_OFFERING. Format of each entry is `collaborator_alias.data_offering_ID.dataset_alias`.

        `argument_name: view_name`
        :   Custom mapping of an argument name to a local template view name (maximum 255 characters each).

    `arguments` (*Optional*)
    :   Template arguments as key-value pairs. Argument values can be strings, numbers, Booleans, arrays, or objects depending on the template
        requirements.

        `preset_tables` is a reserved argument name. Datasets that the template author
        [preset in the template](/user-guide/cleanrooms/custom-templates#label-dcr-template-preset-tables) (preview) are supplied by the template, and an analysis can’t override
        them. Snowflake rejects an analysis that passes `preset_tables` in `arguments`.

    `activation` (*Required for activation templates*)
    :   Activation-specific configuration required when running activation templates.

        `snowflake_collaborator`
        :   Collaborator alias for the activation destination (maximum 25 characters). Must match an alias defined in the
            `collaborator_identifier_aliases` section of the collaboration specification, and the collaborator must be listed in the
            `activation_destinations` section.

        `segment_name`
        :   Unique segment name for this activation (maximum 255 characters). Used to identify and track activation results. Must follow
            [Snowflake identifier rules](/sql-reference/identifiers-syntax).
