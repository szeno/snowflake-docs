# Template specification

Feature — Generally Available

Currently available in [these regions](/user-guide/cleanrooms/installing-dcr#label-dcr-supported-regions).

Not available in government and VPS deployments.

Defines a single template in a collaboration. Templates are registered by calling REGISTER\_TEMPLATE with the template specification.

**Schema:**

Copy code

```
api_version: 2.0.0              # Required: Must be "2.0.0"
spec_type: template             # Required: Must be "template"
name: <template_name>           # Required: Unique name (max 75 chars)
version: <version_string>       # Required: Version identifier (max 20 chars)
type: <template_type>           # Required: sql_analysis or sql_activation
description: <template_description>  # Optional: High-level description (max 1,000 chars)
methodology: <methodology_description>  # Optional: Detailed description (max 1,000 chars)

parameters:                     # Optional: User-provided parameters
  - name: <parameter_name>      # One or more parameter items...
    description: <parameter_description>  # Optional: Description (max 500 chars)
    required: <true_or_false>   # Optional: Whether required (default: false)
    default: <default_value>    # Optional: Default value
    type: <data_type>           # Optional: String, integer, number, Boolean, array, or object

code_specs:             # Optional: List of code specs used by this template
  - <code_spec_id>        # One or more code spec IDs.

preset_tables:                  # Optional: Datasets preset by the template author
  - alias: <dataset_alias>      # One or more preset tables...
    template_view_name: <collaborator_alias>.<data_offering_ID>.<dataset_alias>

template: |                     # Required: JinjaSQL template content
  <template_content>
```

`api_version`
:   The version of the Collaboration API used. Must be `2.0.0`.

`spec_type`
:   Specification type identifier. Must be `template`.

`name: template_name`
:   A unique, user-friendly name for this template. Must follow [Snowflake identifier rules](/sql-reference/identifiers-syntax) with a
    maximum of 75 characters.
    The `name_version` pair must be unique for all templates in this account.

`version: version_string`
:   A version identifier for this template (maximum 20 characters). Must follow
    [Snowflake identifier rules](/sql-reference/identifiers-syntax). The version string is given its own column in the response to
    VIEW\_TEMPLATES and VIEW\_REGISTERED\_TEMPLATES, so use a value that can be sorted by increasing value. Example: `V0`

`type`
:   The template type. One of the following values:

    - `sql_analysis`: Template for data analysis operations.
    - `sql_activation`: Template for data activation operations.

`description: template_description` (*Optional*)
:   A high-level description of what this template does (maximum 1,000 characters).

`methodology: methodology_description` (*Optional*)
:   A more detailed description of how this template works (maximum 1,000 characters).

`parameters` (*Optional*)
:   The list of all user-provided parameters in this template. Each item can have the following fields:

    - `name`: Parameter name as a valid [Snowflake identifier](/sql-reference/identifiers-syntax), max 255 characters.
    - `description` (*Optional*): Human-readable description of the parameter (maximum 500 characters).
    - `required` (*Optional*): Whether the parameter is required. Default is `false`.
    - `default` (*Optional*): Default value for the parameter, which can be any data type.
    - `type` (*Optional*): Expected data type of the parameter. One of: `string`, `integer`, `number`, `boolean`,
      `array`, or `object`.

`code_specs` (*Optional*)
:   One or more code specs that define any functions referenced by this template. Required when the template
    calls [custom functions](/user-guide/cleanrooms/resources-code-specs). Code spec IDs are versioned; if you want to access a new version
    of a function, you must update the code spec ID here, but not in the template itself, which calls the unversioned function name. The code
    spec name must have an underscore in it, and match the regular expression pattern `[A-Za-z]\w{0,74}_\w{1,20}`.

`preset_tables` (*Optional*)
:   [Preview Feature](/release-notes/preview-features) — Open

    Available to all accounts.

    Datasets preset by the template author. An analysis runner doesn’t pass these datasets when they run the template. Use
    `preset_tables` when a template should always read a specific dataset, rather than whichever dataset the analysis runner chooses to
    supply. For details, see [Preset tables](/user-guide/cleanrooms/custom-templates#label-dcr-template-preset-tables). Each item has the following fields:

    - `alias`: The name used to reference this dataset in the template body, as `{{ preset_tables['alias'] }}`. Must be a valid
      [Snowflake identifier](/sql-reference/identifiers-syntax) of up to 255 characters, and must be unique within the template. The SQL
      alias you then give the dataset in the template body can’t be `p`, `c`, or `p` or `c` followed by a number, because
      [those aliases are reserved](/user-guide/cleanrooms/custom-templates#label-dcr-required-template-table-aliases) for `source_table` and `my_table` datasets.
    - `template_view_name`: The preset table, in the format
      `collaborator_alias.data_offering_ID.dataset_alias`. Use the value from the
      TEMPLATE\_VIEW\_NAME column returned by VIEW\_DATA\_OFFERINGS.

`template`
:   The template content. For SQL templates, this contains the [JinjaSQL template](/user-guide/cleanrooms/custom-templates).
    For more information, see [Template design](/user-guide/cleanrooms/resources-templates#label-dcr-design-collaboration-template).

    The column names exposed to the template are determined by the `category` and `column_type` values for the column in the
    [data offering specification](/user-guide/cleanrooms/spec-data-offering#label-dcr-collaboration-data-yaml). For more information, see [Source column renaming](/user-guide/cleanrooms/resources-data-offerings#label-dcr-source-column-renaming).

## Examples

A template that takes one table from the analysis runner:

Copy code

```
api_version: 2.0.0
spec_type: template
name: trivial_template
version: V1
type: sql_analysis
description: Simple one-row template.
methodology: Always returns "1". Requires one source table.

parameters:
  - name: row_count
    description: Count of rows
    required: true

template: |
    SELECT 1 FROM IDENTIFIER( {{ source_table[0] }} ) LIMIT {{ row_count }};
```

A template that pins the publisher’s dataset and takes the advertiser’s dataset from the analysis runner:

Copy code

```
api_version: 2.0.0
spec_type: template
name: preset_overlap_template
version: V1
type: sql_analysis
description: Overlap count against a fixed publisher audience.
methodology: Joins the preset publisher audience to a runner-supplied table on hashed email.

parameters:
  - name: source_tables
    description: The advertiser table to compare against the publisher audience
    required: true

preset_tables:
  - alias: publisher
    template_view_name: pub.pub_audience_v2.AUDIENCE

template: |
    SELECT COUNT(DISTINCT publisher.hashed_email) AS overlap_count
    FROM IDENTIFIER({{ preset_tables['publisher'] }}) AS publisher
    INNER JOIN IDENTIFIER({{ source_table[0] }}) AS p1
    ON publisher.hashed_email = p1.hashed_email;
```
