# Custom attributes in the Internal Marketplace

Custom attributes allow organizations to centrally define standardized metadata fields
that all providers can use when publishing internal data products in the Internal Marketplace.
These attributes function as configurable fields that appear during listing creation.
They enable consistent classification and improve searchability and governance across
the organization.

Custom attributes are created and managed by the GLOBALORGADMIN from the organization
account using Internal Marketplace Configuration SQL commands. After the attributes are configured,
providers can apply these attributes to their data products, and consumers can view these
attributes for additional information about the shared data product.

Custom attributes support three selection types: single-select, multi-select, and free-text.

## Key benefits

### Improved data discovery

Custom attributes provide additional granular, standardized filters and searchable fields
that help consumers quickly find the most relevant data products.

### Consistent metadata across listings

Because attributes are centrally defined by the GLOBALORGADMIN, all providers use the same
field names and value sets, which results in uniform, predictable metadata across your organization.

### Stronger data organization and governance

Custom attributes provide support for key governance scenarios, such as identifying
Personally Identifiable Information (PII), classifying environments (Prod/Dev), and tagging
by business domain. With custom attributes, your consumers can clearly understand the
sensitivity, usage, and compliance characteristics of each data product.

### Centralized control of metadata

Only users with the CREATE INTERNAL MARKETPLACE CONFIG privilege can create and manage
custom attributes. This is available by default only to the GLOBALORGADMIN role. This
prevents users from adding unvetted fields and ensures that all listings use metadata
that aligns with your organization’s internal standards.

## Prerequisites

- Attribute visibility is currently only set at the organization level.

## Summary of features

- A new CREATE INTERNAL MARKETPLACE CONFIG [privilege](/user-guide/security-access-control-overview#label-access-control-overview-privileges).
- A new Internal Marketplace configuration manifest.
- SQL commands:

  - [CREATE INTERNAL MARKETPLACE CONFIG](#label-create-internal-marketplace-config)
  - [ALTER INTERNAL MARKETPLACE CONFIG](#label-alter-internal-marketplace-config)
  - [DROP INTERNAL MARKETPLACE CONFIG](#label-drop-internal-marketplace-config)
  - [SHOW INTERNAL MARKETPLACE CONFIGS](#label-show-internal-marketplace-configs)
  - [SHOW AVAILABLE INTERNAL MARKETPLACE CONFIGS](#label-show-available-internal-marketplace-configs)
  - [DESCRIBE INTERNAL MARKETPLACE CONFIG](#label-describe-internal-marketplace-config)
  - [DESCRIBE AVAILABLE INTERNAL MARKETPLACE CONFIG](#label-describe-available-internal-marketplace-config)
- A new `custom_attributes` field available in the [organization listing manifest reference](/user-guide/collaboration/listings/organizational/org-listing-manifest-reference).
- A new `custom_attributes` column in the [DESCRIBE AVAILABLE LISTING](/sql-reference/sql/desc-available-listing) and
  [SHOW AVAILABLE LISTINGS](/sql-reference/sql/show-available-listings) commands.
- A new `custom_attributes` column in the DESCRIBE LISTING and SHOW LISTINGS commands.
- A new `custom_attributes` column in the `INFORMATION_SCHEMA.LISTINGS` view.

## Workflow

1. The GLOBALORGADMIN optionally grants the CREATE INTERNAL MARKETPLACE CONFIG privilege
   to another role within the organization.
2. A user with the CREATE INTERNAL MARKETPLACE CONFIG privilege creates an Internal Marketplace
   custom configuration manifest.
3. The user then runs the CREATE INTERNAL MARKETPLACE CONFIG command and references
   the newly created custom configuration manifest.

   The custom attributes are now available to be referenced in a listing.
4. A provider with the CREATE LISTING or ALTER LISTING role adds the custom attributes
   to the organization listing manifest reference when creating or altering a listing.

## CREATE INTERNAL MARKETPLACE CONFIG privilege

The CREATE INTERNAL MARKETPLACE CONFIG [privilege](/user-guide/security-access-control-overview#label-access-control-overview-privileges) is
available to the GLOBALORGADMIN [role](/user-guide/security-access-control-overview#label-access-control-overview-roles).

The GLOBALORGADMIN can grant this privilege to other roles.

## Internal Marketplace configuration manifest reference

The Internal Marketplace configuration manifest defines the structure of a custom attribute.
This section describes the fields available in the configuration manifest.

### Internal Marketplace configuration manifest fields

The manifest includes a set of top-level fields, followed by a `props` field.

#### Top-level fields

Each configuration manifest starts with the following fields:

- `title` (String, required, maximum length 80): Configuration title that providers will see in Snowsight.
- `description` (String, optional, maximum length 150): Configuration description that providers will see in Snowsight below the custom attributes dropdown menu. Markdown syntax is supported.
- `config_type` (String, required): Type of Internal Marketplace configuration. Currently, this can only be `custom_attribute`.
- `is_required` (BOOLEAN, optional, default: `false`): Whether a listing must include this custom attribute.

#### `props`

A YAML object storing custom attribute–specific properties. Specify the following fields:

- `custom_attribute_type` (String, required): One of `single_select`, `multi_select`, or `free_text`.
- `is_filterable` (BOOLEAN, required for `single_select` and `multi_select`; not applicable for `free_text`): Whether the custom attribute can be used as a filter.
- `allowed_value_definitions` (List, required for `single_select` and `multi_select`; not applicable for `free_text`): A list of value definitions. Each value definition includes the following fields:
  - `name` (String, required): The internal identifier for the value. Must start with a letter or underscore, followed by letters, digits, or underscores. May only contain letters, digits, and underscores (can be lowercase). Must be unique within the attribute. Maximum length of 100 characters. This field is immutable after creation.
  - `display_name` (String, required): The human-readable label shown to providers and consumers. This field can be altered.
  - `status` (String, required): The status of the value. Can be `active` or `deprecated`. When set to `deprecated`, providers can no longer select this value for new listings, but existing listings that use this value are not affected. This field can be changed from `active` to `deprecated` but not the other way around.

Note

For `free_text` attributes, the `allowed_value_definitions` field is not used.
Providers enter freeform text with a maximum length of 300 characters.

##### `props` examples

Single-select attribute:

Copy code

```
props:
  custom_attribute_type: "single_select"
  is_filterable: true
  allowed_value_definitions:
    - name: "FINANCE"
      display_name: "Finance"
      status: "active"
    - name: "MARKETING"
      display_name: "Marketing"
      status: "active"
```

Free-text attribute:

Copy code

```
props:
  custom_attribute_type: "free_text"
```

### Internal Marketplace custom configuration manifest example

When you are creating a manifest for custom attributes, the example below shows the
fields to include.

Copy code

```
title: "Data Category"
description: "Categorizes data products by business domain"
config_type: "custom_attribute"
is_required: true
props:
  custom_attribute_type: "single_select"
  is_filterable: true
  allowed_value_definitions:
    - name: "FINANCE"
      display_name: "Finance"
      status: "active"
    - name: "MARKETING"
      display_name: "Marketing"
      status: "active"
```

## SQL commands

The following SQL commands are available for creating, managing, and reviewing
Internal Marketplace configurations.

### CREATE INTERNAL MARKETPLACE CONFIG

Creates an Internal Marketplace configuration for a custom attribute.

#### Syntax

Copy code

```
CREATE INTERNAL MARKETPLACE CONFIG <name> AS '<yaml_im_config_manifest_string>'
```

#### Parameters

`name`
:   Specifies the custom configuration identifier (name). Requirements:

    - Must be unique within an organization, regardless of which Snowflake region the account is located in.
    - Must consist of uppercase letters (A-Z), digits (0-9), and underscores (\_).
    - Must start with an alphabetic character.

`AS 'yaml_im_config_manifest_string'`
:   Specifies the YAML manifest for the Internal Marketplace custom configuration.

    Manifests are normally provided as dollar-quoted strings. For more information,
    see [Dollar-quoted string constants](/sql-reference/data-types-text#label-dollar-quoted-string-constants).

#### Access control requirements

A role used to execute this operation must have the following [privilege](/user-guide/security-access-control-overview#label-access-control-overview-privileges):

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE INTERNAL MARKETPLACE CONFIG | Account | Only the GLOBALORGADMIN role has this privilege by default. This privilege can be granted to additional roles as needed. |

Expand

Show lessSee more

#### Examples

Copy code

```
CREATE INTERNAL MARKETPLACE CONFIG DATA_CATEGORY_CONFIG AS $$
title: "Data Category"
description: "Categorizes data products by business domain"
config_type: "custom_attribute"
is_required: true
props:
  custom_attribute_type: "single_select"
  is_filterable: true
  allowed_value_definitions:
    - name: "FINANCE"
      display_name: "Finance"
      status: "active"
    - name: "MARKETING"
      display_name: "Marketing"
      status: "active"
$$;
```

### ALTER INTERNAL MARKETPLACE CONFIG

Alters an existing Internal Marketplace config object.

Note

The following fields can be altered:

- `title`
- `description`
- `is_filterable`
- `is_required` (can only be changed from `true` to `false`)
- `allowed_value_definitions`: You can add new value definitions, change `display_name`, and change `status` from `active` to `deprecated`.

The following fields are immutable after creation:

- `config_type`
- `custom_attribute_type`
- `is_required` (cannot be changed from `false` to `true`)
- `allowed_value_definitions.name` (the name of an existing value definition cannot be changed)

#### Syntax

Copy code

```
ALTER INTERNAL MARKETPLACE CONFIG <name> AS '<yaml_manifest_string>'
```

#### Parameters

`name`
:   Specifies the custom configuration identifier (name). Requirements:

    - Must be unique within an organization, regardless of which Snowflake region the account is located in.
    - Must consist of uppercase letters (A-Z), digits (0-9), and underscores (\_).
    - Must start with an alphabetic character.

`AS 'yaml_im_config_manifest_string'`
:   Specifies the YAML manifest for the custom configuration.

    Manifests are normally provided as dollar-quoted strings. For more information,
    see [Dollar-quoted string constants](/sql-reference/data-types-text#label-dollar-quoted-string-constants).

#### Examples

Copy code

```
ALTER INTERNAL MARKETPLACE CONFIG DATA_CATEGORY_CONFIG AS $$
title: "Updated Data Category"
description: "Updated description"
config_type: "custom_attribute"
is_required: false
props:
  custom_attribute_type: "single_select"
  is_filterable: true
  allowed_value_definitions:
    - name: "FINANCE"
      display_name: "Finance & Accounting"
      status: "active"
    - name: "MARKETING"
      display_name: "Marketing"
      status: "deprecated"
    - name: "OPERATIONS"
      display_name: "Operations"
      status: "active"
    - name: "SALES"
      display_name: "Sales"
      status: "active"
$$;
```

### DROP INTERNAL MARKETPLACE CONFIG

Drops an existing Internal Marketplace config object.

Note

If the configuration has `is_required` set to `true`, the DROP command will return an error.
To drop a required configuration, first ALTER the config to set `is_required` to `false`,
then retry the DROP command. Listings referencing this config may be affected.

#### Syntax

Copy code

```
DROP INTERNAL MARKETPLACE CONFIG <name>
```

#### Parameters

`name`
:   Specifies the custom configuration identifier (name) to drop.

#### Examples

Copy code

```
DROP INTERNAL MARKETPLACE CONFIG DATA_CATEGORY_CONFIG;
```

### SHOW INTERNAL MARKETPLACE CONFIGS

Shows a list of Internal Marketplace configuration objects that were created in an
org account by the user running this command.

If the user didn’t create the objects, or if this command is run on a non-org account,
then the output will be empty.

#### Syntax

Copy code

```
SHOW INTERNAL MARKETPLACE CONFIGS
```

#### Parameters

None.

#### Access control requirements

None. Any provider or consumer can run this command, but the output will only be
available if this command is run on an org account by the user who created the object.

#### Output

Note

If this command is run on a non-org account, or if it’s run by a user who didn’t
create this object, then the output will be empty.

| Column | Description |
| --- | --- |
| `createdOn` | The date when the configuration was created. |
| `name` | The name of the configuration. |
| `title` | The title of the configuration. |
| `description` | The configuration description. |
| `configType` | The configuration type. Currently this can only be `custom_attribute`. |
| `state` | The configuration state. |
| `isRequired` | Whether the configuration is required. |
| `props` | The configuration properties. This includes the custom attribute type, whether the attributes are filterable, and the allowed value definitions. |

Expand

Show lessSee more

#### Examples

Copy code

```
SHOW INTERNAL MARKETPLACE CONFIGS;
```

### SHOW AVAILABLE INTERNAL MARKETPLACE CONFIGS

Lists the Internal Marketplace custom configurations that are available to the user
who runs this command.

#### Syntax

Copy code

```
SHOW AVAILABLE INTERNAL MARKETPLACE CONFIGS
```

#### Parameters

None.

#### Access control requirements

None. Any provider or consumer within the organization can run this command.

#### Output

| Column | Description |
| --- | --- |
| `createdOn` | The date when the configuration was created. |
| `name` | The name of the configuration. |
| `title` | The title of the configuration. |
| `description` | The configuration description. |
| `configType` | The configuration type. Currently this can only be `custom_attribute`. |
| `state` | The configuration state. |
| `isRequired` | Whether the configuration is required. |
| `props` | The configuration properties. This includes the custom attribute type, whether the attributes are filterable, and the allowed value definitions. |

Expand

Show lessSee more

#### Examples

Copy code

```
SHOW AVAILABLE INTERNAL MARKETPLACE CONFIGS;
```

### DESCRIBE INTERNAL MARKETPLACE CONFIG

Describes a specific Internal Marketplace configuration object created by the current user.

#### Syntax

Copy code

```
DESCRIBE INTERNAL MARKETPLACE CONFIG <name>
```

#### Parameters

`name`
:   Specifies the custom configuration identifier (name) to describe.

#### Output

The output includes all the columns from SHOW INTERNAL MARKETPLACE CONFIGS, plus the
following additional column:

| Column | Description |
| --- | --- |
| `manifest_yaml` | The latest YAML manifest for the configuration. |

Expand

Show lessSee more

#### Examples

Copy code

```
DESCRIBE INTERNAL MARKETPLACE CONFIG DATA_CATEGORY_CONFIG;
```

### DESCRIBE AVAILABLE INTERNAL MARKETPLACE CONFIG

Describes a specific Internal Marketplace configuration object that is available to
the user who runs this command.

#### Syntax

Copy code

```
DESCRIBE AVAILABLE INTERNAL MARKETPLACE CONFIG <name>
```

#### Parameters

`name`
:   Specifies the custom configuration identifier (name) to describe.

#### Output

The output includes the same columns as SHOW AVAILABLE INTERNAL MARKETPLACE CONFIGS.

#### Examples

Copy code

```
DESCRIBE AVAILABLE INTERNAL MARKETPLACE CONFIG DATA_CATEGORY_CONFIG;
```

## Listing manifest updates

A `custom_attributes` field is available in the organizational listing’s
manifest reference.

### `custom_attributes`

Additional attributes added to a listing’s Custom Attributes section.

The `custom_attributes` field allows providers to specify custom attributes
on a listing. This field contains the following fields:

`name` (String, required): The name of the custom attribute object that was defined
in the Internal Marketplace custom configuration manifest.

`values` (List of values, required): For `single_select` and `multi_select`, a list
that includes all or some of the value display names from the attribute’s `allowed_value_definitions`.
For `free_text`, the list can only contain 1 value (maximum length of 300 characters).

#### `custom_attributes` examples

Single-select attribute on a listing:

Copy code

```
custom_attributes:
  - name: DATA_CATEGORY_CONFIG
    values:
      - Finance
```

Free-text attribute on a listing:

Copy code

```
custom_attributes:
  - name: DOCUMENTATION_URL
    values:
      - "https://wiki.example.com/data-products/sales"
```

## New columns in listing commands and views

Providers and consumers can run the [DESCRIBE AVAILABLE LISTING](/sql-reference/sql/desc-available-listing) and [SHOW AVAILABLE LISTINGS](/sql-reference/sql/show-available-listings) commands to view custom attributes. The output of each includes a new `custom_attributes` column.

For providers, the `custom_attributes` column is also available in the output of SHOW LISTINGS and DESCRIBE LISTING.

Additionally, a new `custom_attributes` column is available in the `INFORMATION_SCHEMA.LISTINGS` view,
allowing providers to query custom attributes applied to their listings programmatically.

## Custom attributes limitations

### Admin-side limitations

- Only users with the CREATE INTERNAL MARKETPLACE CONFIG privilege can create or
  alter custom attributes. This privilege is granted to the GLOBALORGADMIN role by default.
- Only `custom_attribute` configuration types are currently supported.
- The `custom_attribute_type` (`single_select`, `multi_select`, or `free_text`) cannot be changed after creation.
- The `is_required` field can only be changed from `true` to `false`. It cannot be changed from `false` to `true`.
- Within `allowed_value_definitions`, the `name` of an existing value cannot be changed.
- Values can be deprecated but not removed.
- A required configuration (`is_required` = `true`) cannot be dropped directly. You must first ALTER it to set `is_required` to `false`, then retry the DROP.

### Attribute and value limits

- Maximum number of custom attributes per organization: 10
- Maximum title length: 80 characters
- Maximum description length: 150 characters
- Maximum allowed value definitions per attribute: 15
- Maximum length of each value name: 100 characters
- Maximum length of each value display name: 100 characters
- Maximum length of free-text input by providers: 300 characters

### Naming constraints

- Configuration names must consist of uppercase letters (A-Z), digits (0-9), and underscores (\_).
- Configuration names must start with an alphabetic character.
- Configuration names must be unique within an organization.
- Value names within `allowed_value_definitions` must start with a letter or underscore, followed by letters, digits, or underscores (can be lowercase).

### Provider limitations

- Providers can only use the attribute names and values defined by the admin.
- Providers cannot select deprecated values for new listings.
- For free-text attributes, providers are limited to 300 characters.

### Workflow limitations

- Creating and managing custom attributes through Snowsight is not supported.
