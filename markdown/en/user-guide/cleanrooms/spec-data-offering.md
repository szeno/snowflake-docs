# Data offering specification

Feature — Generally Available

Currently available in [these regions](/user-guide/cleanrooms/installing-dcr#label-dcr-supported-regions).

Not available in government and VPS deployments.

Defines a set of tables that a provider is willing to share with analysis runners, as well as sharing rules, such as policies, column
formats, and whether the table must be used with a template.

The data provider submits this specification by calling REGISTER\_DATA\_OFFERING, which returns an offering ID that can be used in the
collaboration specification.

A data offering won’t be available in a collaboration until the account that registered the data offering joins the collaboration.

You must have the REGISTER DATA OFFERING account privilege to join any collaboration in which you can activate data; that is, you are an
analysis runner and the collaboration specification includes an `activation_destinations` field. For more information, see the
[access management API reference guide](/user-guide/cleanrooms/collaboration-api-reference#label-dcr-collaboration-access-management-api).

**Schema:**

Copy code

```
api_version: 2.0.0              # Required: Must be "2.0.0"
spec_type: data_offering        # Required: Must be "data_offering"
name: <data_offering_name>      # Required: Unique name (max 75 chars)
version: <version_string>       # Required: Version identifier (max 20 chars)
description: <data_offering_description>  # Optional: Description (max 1,000 chars)

datasets:                       # Required: Tables to share
  - alias: <dataset_name>       # One or more dataset items...
    data_object_fqn: <database.schema.table_name>  # Required: Fully-qualified table name
    allowed_analyses: <allowed_analysis_type>      # Required: template_only or template_and_freeform_sql
    object_class: <object_class>    # Optional: ads_log or custom
    schema_and_template_policies:   # Required: Column definitions
      <column_name>:                # One or more column definitions...
        category: <category_type>   # Required: join_standard, join_custom, timestamp, passthrough, or event_type
        column_type: <format_type>  # Required for join_standard category, omitted for other categories.
        activation_allowed: <true_or_false>  # Optional: Whether column can be used for activation
    freeform_sql_policies:      # Optional: Policies for freeform SQL queries
      aggregation_policy:       # Optional: Single aggregation policy
        name: <fully_qualified_policy_name>
        entity_keys:            # Optional: Entity key columns
          - <column_name>       # One or more POSSIBLY RENAMED column names...
      join_policy:              # Optional: Single join policy
        name: <fully_qualified_policy_name>
        columns:                # Optional: Columns this policy applies to
          - <column_name>       # One or more POSSIBLY RENAMED column names...
      masking_policies:         # Optional: Masking policies
        - name: <fully_qualified_policy_name>  # One or more masking policy items...
          columns:              # Optional: Columns this policy applies to
            - <column_name>     # One or more POSSIBLY RENAMED column names...
      projection_policies:      # Optional: Projection policies
        - name: <fully_qualified_policy_name>  # One or more projection policy items...
          columns:              # Optional: Columns this policy applies to
            - <column_name>     # One or more POSSIBLY RENAMED column names...
      row_access_policy:        # Optional: Row access policy
        name: <fully_qualified_policy_name>
        columns:              # Optional: Columns this policy applies to
          - <column_name>     # One or more POSSIBLY RENAMED column names...
    require_freeform_sql_policy: <true_or_false>  # Optional: Require a policy for freeform SQL
```

`api_version`
:   The version of the Collaboration API used. Must be `2.0.0`.

`spec_type`
:   Specification type identifier. Must be `data_offering`.

`name: data_offering_name`
:   A name for a set of tables and columns to expose to collaborators. This name is used as the data offering reference value in a
    collaboration specification. You can create multiple data offerings with overlapping tables and columns for different use cases. Must follow
    [Snowflake identifier rules](/sql-reference/identifiers-syntax) with a maximum of 75 characters and be unique within your Snowflake
    data clean room account.
    The `name_version` pair must be unique for all data offerings in this account.

`version`
:   A custom version identifier for this data offering specification (maximum 20 characters). Must follow
    [Snowflake identifier rules](/sql-reference/identifiers-syntax). The version string is given its own column in the response to
    VIEW\_DATA\_OFFERINGS and VIEW\_REGISTERED\_DATA\_OFFERINGS, so use a value that can be sorted by increasing value. Example: `V0`

`description: data_offering_description` (*Optional*)
:   A description of the data offering (maximum 1,000 characters).

`datasets`
:   A list of one or more datasets to make available to the collaboration.

    `alias: dataset_name`
    :   A name for this data object, used in `collaboration.run`. Must follow
        [Snowflake identifier rules](/sql-reference/identifiers-syntax) and be unique within this offering. Maximum 75 characters.

    `data_object_fqn: fully_qualified_table_name`
    :   Describes a single table available to collaborators. The fully-qualified name of the source object in your account
        (`database.schema.object_name`). Maximum length is 773 characters.
        For supported object types, see [Supported object types](/user-guide/cleanrooms/resources-data-offerings#label-dcr-data-offering-supported-object-types).

    `allowed_analyses: allowed_analysis_type`
    :   The type of analyses that collaborators can run against this table. Required field with the following values:

        - `template_only`: The analysis runner can query this table only by using a template listed in the collaboration specification.
        - `template_and_freeform_sql`: The analysis runner can query this table by using either a template listed in the collaboration
          specification, or by using [free-form SQL queries](/user-guide/cleanrooms/demo-flows/basic-multiparty-collab#label-dcr-collab-enable-free-form-queries) in a code environment.

    `object_class` (*Optional*)
    :   The type of object. One of the following values:

        - `ads_log`: The tables and columns listed here must fit the ad log requirements.
        - `custom`: A custom set of tables and columns that doesn’t have any special requirements.

    `schema_and_template_policies`
    :   Provide a list of column names from the table listed by `data_object_fqn` and define the policies and format of each column. Only
        columns listed here are available to collaborators. Each column has the following descriptors:

        `category: category_type`
        :   The category determines whether any column renaming is applied, and any data format enforcement that should be applied.
            `category` and `column_type` [determine the column name exposed to the analysis runner](/user-guide/cleanrooms/resources-data-offerings#label-dcr-source-column-renaming).
            The following values are supported:

            - `join_standard`: This is a joinable column with data in a format specified in the `column_type` field. This column is
              renamed to the `column_type` value in the shared data offering. This column is added to the clean room’s
              [join policy](/user-guide/cleanrooms/resources-data-offerings#label-dcr-collaborations-policies).
            - `join_custom`: This is a joinable column in any format. Use this when there isn’t an appropriate `column_type` for your
              join column. The original column name is used in the shared data offering. This column is added to the clean room’s
              [join policy](/user-guide/cleanrooms/resources-data-offerings#label-dcr-collaborations-policies).
            - `timestamp`: This is a projectable column that specifies a timestamp for any event. The column is renamed as `timestamp` in
              the shared data offering.
            - `passthrough`: This is a projectable column of any other type. The original column name is used in the shared data offering.
            - `event_type`: This is a projectable column that records an event type classification for this row, for example: “purchase”,
              “sign-up”, “impression”, “click”, and so on.

        `column_type: <format_type>` (*Required when category=join\_standard, ignored for other category types*)
        :   The format of the data. If the data doesn’t conform to this format, your call to REGISTER\_DATA\_OFFERING will fail. Provide this field
            for columns where `category = join_standard`. `category` and `column_type`
            [determine the column name exposed to the analysis runner](/user-guide/cleanrooms/resources-data-offerings#label-dcr-source-column-renaming). You can’t assign the same
            `column_type` value to multiple columns in the same table. The following format types are supported:

            - `email`: A raw email address.
            - `hashed_email_sha256`: A SHA256 hashed email.
            - `hashed_email_b64_encoded`: A base64-encoded hashed email.
            - `phone`: A phone number without punctuation. For example: `2015551212`.
            - `hashed_phone_sha256`: A SHA256 hashed phone number. The original number should be in the `phone` format.
            - `hashed_phone_b64_encoded`: A base64-encoded hashed phone number.
            - `device_id`: A raw device ID, such as a mobile advertising ID or a CTV device ID.
            - `hashed_device_id_sha256`: SHA256 hashed device ID. The original should be in the `device_id` format.
            - `hashed_device_b64_encoded`: A base64-encoded hashed device ID.
            - `ip_address`: A raw IP address in IPv4 format.
            - `hashed_ip_address_sha256`: SHA256 hashed IPv4 address. The original should be in the `ip_address` format.
            - `hashed_ip_address_b64_encoded`: A base64-encoded hashed IP address.
            - `first_name`: A raw first name.
            - `hashed_first_name_sha256`: A SHA256 hashed first name. The original should be in the `first_name` format.
            - `hashed_first_name_b64_encoded`: A base64-encoded hashed first name.
            - `last_name`: A raw last name.
            - `hashed_last_name_sha256`: A SHA256 hashed last name. The original should be in the `last_name` format.
            - `hashed_last_name_b64_encoded`: A base64-encoded hashed last name.

        `activation_allowed` (*Optional*)
        :   Whether this column can be used for activation purposes. Default is `false`.

> `freeform_sql_policies` (*Optional*)
> :   If `allowed_analyses` is `template_and_freeform_sql`, this optional field lists any Snowflake policies that should be applied
>     in free-form SQL queries run on this data offering. For more information, see [Apply the Snowflake policy to the data offering (\*free-form query usage only\*)](/user-guide/cleanrooms/resources-data-offerings#label-dcr-collab-freeform-sql-policies).

> > The following types are supported:
> >
> > `aggregation_policy` (*Optional*)
> > :   A single [aggregation policy](/user-guide/aggregation-policies) configuration.
> >
> >     - `name`: The fully-qualified policy name.
> >     - `entity_keys` (*Optional*): List of column names that serve as entity keys for the aggregation policy. NOTE: if these columns
> >       have been [renamed](/user-guide/cleanrooms/resources-data-offerings#label-dcr-source-column-renaming), you must use the generated column name.
> >
> > `join_policy` (*Optional*)
> > :   A single [join policy](/user-guide/join-policies) configuration.
> >
> >     - `name`: The fully-qualified policy name. NOTE: if this column has been [renamed](/user-guide/cleanrooms/resources-data-offerings#label-dcr-source-column-renaming), you
> >       must use the generated column name.
> >     - `columns` (*Optional*): List of column names this policy applies to.
> >
> > `masking_policies` (*Optional*)
> > :   An array of [masking policy](/user-guide/security-column-intro) configurations.
> >
> >     - `name`: The fully-qualified policy name. NOTE: if this column has been [renamed](/user-guide/cleanrooms/resources-data-offerings#label-dcr-source-column-renaming), you
> >       must use the generated column name.
> >     - `columns` (*Optional*): List of column names this policy applies to.
> >
> > `projection_policies` (*Optional*)
> > :   An array of [projection policy](/user-guide/projection-policies) configurations.
> >
> >     - `name`: The fully-qualified policy name. NOTE: if this column has been [renamed](/user-guide/cleanrooms/resources-data-offerings#label-dcr-source-column-renaming), you
> >       must use the generated column name.
> >     - `columns` (*Optional*): List of column names this policy applies to.
> >
> > `row_access_policy` (*Optional*)
> > :   An object that describes a [row access policy](/user-guide/security-row-intro) configuration.
> >
> >     - `name`: The fully-qualified policy name. NOTE: if this column has been [renamed](/user-guide/cleanrooms/resources-data-offerings#label-dcr-source-column-renaming), you
> >       must use the generated column name.
> >     - `columns` (*Optional*): List of column names this policy applies to.
>
> `require_freeform_sql_policy` (*Optional*)
> :   Whether this data source must define `freeform_sql_policies`. This is used as a failsafe to prevent linking a data source
>     that supports free-form SQL queries without assigning policies to it.
