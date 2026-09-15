# Organization listing manifest reference

As a provider, you can use organizational listings to share data products securely within your organization.
A manifest, written in YAML (<https://yaml.org/spec/>), is required to create organization listings programmatically.
Use the information provided here to learn about the manifest format and its individual fields.

Organization listing fields are part of the larger [Listing manifest reference](/progaccess/listing-manifest-reference).
To add or modify organizational listing fields programmatically, locate and modify the listing manifest using
[DESCRIBE LISTING](/sql-reference/sql/desc-listing) and [ALTER LISTING](/sql-reference/sql/alter-listing) commands.

## Organization listing manifest

Note

Organizational listing fields can be one of the following:

- Optional - Optional for organizational listings.
- Required - Required for organizational listings.

The general format of an organization listing manifest is:

Copy code

```
#
# Organization listing manifest
#
title: <Required listing title>
description: <listing description>
resources: <optional listing resources>
listing_terms: <optional listing terms>
data_dictionary: <optional data dictionary>
usage_examples: <optional usage examples>
data_attributes: <optional data attributes>
organization_profile: <Optional custom organization profile. Default "INTERNAL">
organization_targets:
  - # Required
support_contact: "<support email address>"
  - # Required
approver_contact: "<approver email address>"
  - # Required when the organization_targets includes the organization_targets.discovery field
request_approval_type:
  - # Optional. Can be REQUEST_AND_APPROVE_IN_SNOWFLAKE or REQUEST_AND_APPROVE_OUTSIDE_SNOWFLAKE.
locations:
  - # Optional list of regions to share into.
auto_fulfillment:
  - # Required when the target accounts are outside the provider's region, otherwise optional.
resharing:
  enabled: true # Optional. Controls whether the listing can be reshared by consumers.
custom_attributes: <organization-defined custom attributes> # Required or optional, depending on organization configuration.
```

## Organization listing fields

Organization listing manifests include a prefix, followed by a set of required and optional fields.

### Organization listing prefix

Each organization listing manifest starts with the following fields:

- `title` (String, required, maximum length 110): Listing title.
- `description` (String, optional, maximum length 7500): Listing description. Markdown syntax is supported.
- `resources` (String, optional): Resources for the listing.
- `listing_terms` (parent with child fields, optional): Terms for the listing.
- `organization_profile` (String, optional): Optional custom organization profile. Defaults to INTERNAL if not specified.

### `resources`

Resources for the listing.

The **optional** `resources` field contains the following name value pairs:

- `resources.documentation` (String, required): A fully qualified link to a page on your website with more detailed documentation for the listing.
  Must start with `http` or `https`.
- `resources.media` (String, optional): A fully qualified link to an unlisted or public YouTube video for the listing.

For more information about the type of information you can include with this field, see [Additional fields](/collaboration/provider-listings-reference#label-configuring-metadata-for-data-listing-details).

#### `resources` example

Copy code

```
. . .
resources:
  documentation: https://www.example.com/documentation/
  media: https://www.youtube.com/watch?v=MEFlT3dc3uc
. . .
```

### `listing_terms`

Defines the terms of service for the listing.

The **optional** `listing_terms` field contains the following name value pairs:

- `listing_terms.type`

  - `CUSTOM` - Only *CUSTOM* is supported. If `listing_terms.type` is specified, then you must also specify a value for `listing_terms.link`.
- `listing_terms.link`: A fully qualified link to the provider’s listing terms, which must start with `http` or `https`.

For more information, refer to **Terms of Service** in the table in [3. Basic information](/collaboration/provider-listings-reference#label-configuring-metadata-for-data-listing).

Note

Consumers can accept listing terms programmatically. For more information, contact [Snowflake Support](/user-guide/contacting-support).

#### `listing_terms` example

Copy code

```
. . .
listing_terms:
  type: "CUSTOM"
  link: "http://example.com/my/listing/terms"
. . .
```

### `data_dictionary`

The **optional** `data_dictionary` field provides information on data preview and column types for the objects within the listing.

The `data_dictionary` field contains a list of up to five data dictionary entries:

- `data_dictionary.featured` (required when using `data_dictionary`): Must be ‘featured’.
- `data_dictionary.featured.database` (required when using `data_dictionary`): The database name.
- `data_dictionary.featured.objects` (required when using `data_dictionary`): A list of the following name value pairs:
  - `name` (string, required): The object name.
  - `schema` (string, required): The schema associated with the data dictionary.
  - `domain` (required):

    One of the following:

    - DATABASE
    - SCHEMA
    - TABLE
    - VIEW
    - EXTERNAL\_TABLE
    - MATERIALIZED\_VIEW
    - DIRECTORY\_TABLE
    - FUNCTION
    - COLUMN

For more information see [Data dictionary](/collaboration/provider-listings-reference#label-listings-data-dictionaries).

#### `data_dictionary` example

Copy code

```
. . .
data_dictionary:
 featured:
    database: "WEATHERDATA"
    objects:
       - name: "GLOBAL_WEATHER"
         schema: "PUBLIC"
         domain: "TABLE"
       - name: "GLOBAL_WEATHER_REPORT"
         schema: "PUBLIC"
         domain: "TABLE"
. . .
```

### `usage_examples`

The **optional** `usage_examples` field contains a list of the following name value pairs:

- `usage.title` (String, required): The usage example title. The maximum length is 110 characters.
- `usage.description` (String, optional): A description of the usage example. The maximum length is 300 characters.
- `usage.query` (String, required): The query associated with the usage example. The maximum length is 30000 characters.

For more information, see [Required for public listings with a Secure Share data product.](/collaboration/provider-listings-reference#label-provider-listing-reference-sample-sql-queries).

#### `usage_examples` example

Copy code

```
. . .
usage_examples:
  - title: "Return all weather for the US"
    description: "Example of how to select weather information for the United States"
    query: "select * from weather where country_code='USA'"
. . .
```

### `data_attributes`

Data attributes provide consumers with listing information.

The **optional** `data_attributes` field contains the following name value pairs:

- `data_attributes.refresh_rate` (required)

  Specifies how often your data product is updated in Snowflake. One of the following:

  - CONTINUOUSLY
  - HOURLY
  - DAILY
  - WEEKLY
  - MONTHLY
  - QUARTERLY
  - ANNUALLY
  - STATIC
- `data_attributes.geography` (required):

  Specifies geographic information for the data product.

  - `granularity` (string, required)

    Geographic coverage of the dataset.

    One of the following:

    - LATITUDE\_LONGITUDE
    - ADDRESS
    - POSTAL\_CODE
    - CITY
    - COUNTY
    - STATE
    - COUNTRY
    - REGION\_CONTINENT
  - `geo_option` (string, required)

    One of the following:

    - NOT\_APPLICABLE
    - GLOBAL
    - COUNTRIES
  - `coverage` (required based on selection of `geo_option`):

    - `states` (list of states) containing any list of valid U.S. state names.

    Or

    - `continents` (list of continents):

      Any of the following:

      - ASIA
      - EUROPE
      - AFRICA
      - NORTH AMERICA
      - SOUTH AMERICA
      - OCEANIA
      - ANTARCTICA
  - `time` (required):

    Specifies the time period for the data product.

    - `granularity` (required)

    One of the following:

    - EVENT\_BASED
    - HOURLY
    - DAILY
    - WEEKLY
    - MONTHLY
    - YEARLY
    - `time_range` (required) containing the following name/value pairs:
      - `time_frame` (required)

        One of the following:

        - NEXT
        - LAST
        - BETWEEN
      - `unit` (required)
        One of the following:

        - DAYS
        - WEEKS
        - MONTHS
        - YEARS
      - `value` (required when `time_frame` is NEXT/LAST, integer). The range is 1 to 100.
      - `start_time` (required when `time_frame` is BETWEEN, String date). The start time for the data product. The format is MM-DD-YYYY.
      - `end_time` (required when `time_frame` is BETWEEN, String date), format MM-DD-YYYY.

For additional information on data product attributes, see [Required for public listings. Define additional attributes that](/collaboration/provider-listings-reference#label-listings-data-product-attributes).

#### `data_attributes` example

Copy code

```
. . .
data_attributes:
  refresh_rate: DAILY
  geography:
    granularity:
      - REGION_CONTINENT
    geo_option: COUNTRIES
    coverage:
      continents:
        ASIA:
          - INDIA
          - CHINA
        NORTH AMERICA:
          - UNITED STATES
          - CANADA
        EUROPE:
          - UNITED KINGDOM
    time:
      granularity: MONTHLY
      time_range:
        time_frame: LAST
        unit: MONTHS
        value: 6
```

### `organization_targets`

The **required** `organization_targets` field defines who can discover and access the listing.

Contains the `discovery` and `access` fields, one of which must be specified.

`discovery`
:   **Required** when `access` isn’t specified, but otherwise **optional**.
    Defines who can discover the listing. When not present, no accounts can discover the listing.

`access`
:   **Required** when `discovery` isn’t specified, but otherwise **optional**.
    Defines who can access the listing.

Both `discovery` and `access` contain the same child fields.

Either:

`all_internal_accounts : {true | false}`
:   When *true*, all internal accounts can find or access the listing. When *false*, no accounts can find or access the listing.

Or an array of accounts, followed by the optional `roles` array within the specified accounts.
:   `- account: "<account_name>"`

When `roles` is present, it specifies a list of roles within the account that can access or discover the listing. For example:

> . . .
> `roles: [ 'role1','role2']`
> . . .

### `organization_targets` examples

The following examples show various combinations of the `discovery` and `access` fields.

#### All internal accounts in the organization can discover and access the listing

Copy code

```
. . .
organization_targets:
   discovery:
   - all_internal_accounts : true
   access:
   - all_internal_accounts : true
. . .
```

#### Discoverable but only accessible by limited accounts

All internal accounts within the organization can discover the listing, but only *finance* accounts can access the listing.

Copy code

```
. . .
organization_targets:
   discovery:
   - all_internal_accounts : true
   access:
   - account: 'finance'
. . .
```

#### Discoverable but accessible by only select accounts

All internal accounts within the organization can discover the listing, but only accounts in the *finance* or *credit* account can access the listing.

Copy code

```
. . .
organization_targets:
   discovery:
   - all_internal_accounts : true
   access:
   - account: 'finance'
   - account: 'credit'
. . .
```

#### Discoverable but only accessible by limited accounts and specific roles

All internal accounts within the organization can discover the listing,
but only accounts in the *finance* account which have the *accounting* or *debit* role can access the listing.

Copy code

```
. . .
organization_targets:
    discovery:
    - all_internal_accounts : true
    access:
    - account: 'finance'

      roles: [ 'accounting','debit']
. . .
```

### `support_contact`

The email address for support information associated with the listing.

**Required** when the `discovery` field is specified.

Copy code

```
. . .
support_contact: "support@exampledomain.com"
. . .
```

### `approver_contact`

The email address for the listing approver.

**Required** when the `discovery` field is specified.

> Copy code
>
> ```
> . . .
>   approver_contact: "approver@exampledomain.com"
> . . .
> ```

### `request_approval_type`

Define whether approval requests and approvals will happen inside or outside of Snowflake. Specify one of the following values:

- `NULL`
- `REQUEST_AND_APPROVE_IN_SNOWFLAKE` indicates access requests are submitted and approved within the Snowflake environment.
- `REQUEST_AND_APPROVE_OUTSIDE_SNOWFLAKE` indicates the provider manages access request submissions and approvals independently.

The value for external listings is always `NULL`.

> Copy code
>
> ```
> . . .
>   request_approval_type: "REQUEST_AND_APPROVE_IN_SNOWFLAKE"
> . . .
> ```

### `locations`

Specifies the **optional** `locations` which can discover or access the listing.

The `access_regions` field is **required** when `locations` is specified and it must include one of the following sub-fields:

- `ALL` - All regions can discover or access the listing.
- An array of region names prefixed with *PUBLIC* which can discover or access the listing.
  For example *access\_regions: - name: PUBLIC.AWS\_US\_WEST\_2*.

  Copy code

  ```
  . . .
  locations:
    access_regions:
    - name: "<names | ALL>"
  . . .
  ```

For a complete list of regions, see [SHOW REGIONS](/sql-reference/sql/show-regions).

### `auto_fulfillment`

Cross-Cloud Auto-fulfillment allows the data product associated with a listing
to be automatically fulfilled to other Snowflake regions.
The `auto_fulfillment` field defines how that auto-fulfillment takes place.

For more information on Cross-Cloud Auto-fulfillment, see [Auto-fulfillment for listings](/collaboration/provider-listings-auto-fulfillment).

Auto-fulfillment is only required if you’re sharing data to multiple regions.
Do not enable it if you are sharing to accounts in the same region.

If you share data across multiple regions, the `auto_fulfillment` is:

- Required if your data product is an application package.
- Required if your data product is shared through a private listing.
- Recommended if your data product is shared through a public listing.

Contains the following name value pairs:

- `auto_fulfillment.refresh_schedule`

  - `<num> MINUTE` - Number of minutes. Minimum 10 minutes, maximum 8 days, or 11520 minutes.

    If `refresh_type` is specified as `SUB_DATABASE_WITH_REFERENCE_USAGE`, do not include this setting.
    The refresh schedule for application packages must be defined at the account level and cannot be specified at the listing level.

    For more information see [Set the account-level refresh interval](/collaboration/provider-listings-auto-fulfillment-set-refresh-interval).
- `USING CRON <expression>` - Defines the data product auto-fulfillment refresh schedule.
  The syntax for `USING CRON` and `REPLICATION SCHEDULE` is the same. See [Parameters](/sql-reference/sql/create-replication-group#label-create-replication-group-parameters).
- `auto_fulfillment.refresh_type` (required when using `auto_fulfillment`): Must be one of:

  - `SUB_DATABASE` - database replication (object level) - recommended.
  - `SUB_DATABASE_WITH_REFERENCE_USAGE` - application package.
  - `FULL_DATABASE` - database replication (for the entire database). (Deprecated.)
- `auto_fulfillment.refresh_schedule_override` (optional): Overrides the defined update refresh frequency for all listings that use the same database. When this value is `FALSE`, listing updates fail when multiple listings sharing the same database have different refresh frequencies.

  - `TRUE` - enables the refresh frequency override.
  - `FALSE` - (default) disables the refresh frequency override.
- `auto_fulfillment.warehouse` (optional): The name of the warehouse used to create and refresh hidden dynamic tables for
  cross-region resharing. This warehouse is used only for resharing maintenance operations. Required when the listing is a reshared
  listing. Can be omitted for non-reshared listings. For more information, see [Reshare incoming data as a resharer](/collaboration/resharing-as-resharer).

See also [Auto-fulfillment for listings](/collaboration/provider-listings-auto-fulfillment).

### `auto_fulfillment.refresh_schedule` examples

The following example refreshes the data product associated with a listing every 10 minutes:

Copy code

```
. . .
listing_terms: . . .
. . .
auto_fulfillment:
  refresh_schedule: 10 MINUTE
  refresh_type: SUB_DATABASE
. . .
```

The following example refreshes the data product associated with a listing on specific days and times in specific regions:

Copy code

```
. . .
listing_terms: . . .
. . .
auto_fulfillment:
  refresh_schedule: USING CRON 0 17 * * MON-FRI Europe/London
  refresh_type: SUB_DATABASE
. . .
```

The following example enables the refresh frequency override for listings that share the same database but have different refresh frequencies:

Copy code

```
. . .
listing_terms: . . .
. . .
auto_fulfillment:
  refresh_schedule: 10 MINUTE
  refresh_type: SUB_DATABASE
  refresh_schedule_override: TRUE
. . .
```

### Snowflake Native App `auto_fulfillment` example

`SUB_DATABASE_WITH_REFERENCE_USAGE` can only be used with application packages
and cannot be combined with `auto_fulfillment.refresh_schedule`.

Copy code

```
. . .
listing_terms: . . .
. . .
auto_fulfillment:
  refresh_type: SUB_DATABASE_WITH_REFERENCE_USAGE
. . .
```

### Object level `auto_fulfillment` example

Copy code

```
. . .
listing_terms: . . .
. . .
auto_fulfillment:
  refresh_type: SUB_DATABASE
. . .
```

### `resharing`

The `resharing` field controls whether consumers of the listing can reshare the data product with other accounts.

For more information on resharing, see [Resharing listings](/collaboration/reshare-listings).

Contains the following name value pairs:

- `resharing.enabled` (optional): Enables or disables resharing for the listing.

  - `true` - (default) allows consumers to reshare the listing data.
  - `false` - prevents consumers from resharing the listing data.
- `resharing.only_within_organization` (optional): Specifies whether consumers can reshare the listing only within their own organization,
  or also with other organizations.

  - `true` - consumers can reshare the listing only within their own organization.
  - `false` - consumers can reshare the listing outside of their own organization.

  For organizational listings, the default behavior restricts resharing to within the same organization.

  For more information, see [To require that any consumer who reshares your listing can only reshare it to…](/collaboration/resharing-as-provider#label-resharing-restrict-org).

### `resharing` example

The following example enables resharing on a listing:

Copy code

```
. . .
listing_terms: . . .
. . .
resharing:
  enabled: true
. . .
```

The following example enables resharing on a listing only within the consumer’s organization:

Copy code

```
. . .
listing_terms: . . .
. . .
resharing:
  enabled: true
  only_within_organization: true
. . .
```

### `custom_attributes`

The `custom_attributes` field lets providers apply organization-defined custom attributes
to a listing. Whether you must include this field depends on how the organization
administrator configured each custom attribute.

Each entry in the list contains the following fields:

- `name` (String, required): The name of the custom attribute configuration defined by
  the organization administrator.
- `values` (List, required): For `single_select` and `multi_select` attributes, one or
  more display names from the attribute’s allowed values. For `free_text` attributes,
  a single value (maximum length 300 characters).

### `custom_attributes` example

Copy code

```
. . .
custom_attributes:
  - name: DATA_CATEGORY_CONFIG
    values:
      - Finance
. . .
```

For more information about creating custom attributes and supported attribute types, see
[Custom attributes in the Internal Marketplace](/user-guide/collaboration/listings/organizational/custom-attributes-internal-marketplace).
