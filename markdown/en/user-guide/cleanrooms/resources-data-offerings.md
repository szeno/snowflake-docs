# Data offerings

Feature — Generally Available

Currently available in [these regions](/user-guide/cleanrooms/installing-dcr#label-dcr-supported-regions).

Not available in government and VPS deployments.

A *data offering* is a set of one or more views, called *datasets*, shared with specific analysis runners in a collaboration. You can share
data with analysis runners for whom you are defined as a data provider in the [collaboration specification](/user-guide/cleanrooms/spec-collaboration#label-dcr-collaboration-spec-yaml).

A data offering is a live view of the source data, not a snapshot of the data at the time the data offering is registered. Any Snowflake
policies applied to the source data are active in the data offering.

When you register a data offering, Snowflake creates a view for each data source listed in the
[data offering specification](/user-guide/cleanrooms/spec-data-offering#label-dcr-collaboration-data-yaml). The view includes *only* the columns listed in the data offering
specification. Certain columns, depending on their category, are [subject to renaming](#label-dcr-source-column-renaming) at this stage.

Additionally, when you link a data offering into a collaboration, Snowflake creates a copy of the registered view and limits access to the view to specified
analysis runners according to the [collaboration specification](/user-guide/cleanrooms/spec-collaboration#label-dcr-collaboration-spec-yaml).

Important

If you move, rename, or change access permissions to the underlying tables, the data offering will become unusable through any previously
registered links.

If you use Snowflake Standard Edition, you can’t share data through a data clean room with policy enforcement. Hence, you are not able to share data with other parties or leverage the data clean room policies specified in the offerings even for users in your own account.
However, you can access data offerings from other collaborators, or [use your own data as a local data offering](/user-guide/cleanrooms/demo-flows/basic-multiparty-collab#label-dcr-using-local-data) without policies.

**Data offering requirements:**

- You must have the REFERENCE\_USAGE privilege with GRANT OPTION on any data that you want to share. If you don’t, you receive a
  [“missing reference usage grant”](/user-guide/cleanrooms/v2/troubleshooting#label-dcr-database-missing-reference-usage-error) error when you try to register, join the
  collaboration, or link the data.

  Copy code

  ```
  GRANT REFERENCE_USAGE ON DATABASE my_database TO ROLE my_role WITH GRANT OPTION;
  ```
- You must have the [data provider collaboration role](/user-guide/cleanrooms/roles) in a collaboration.
- Currently, only the account role that created or joined the collaboration can link or unlink data into a collaboration.

Continue reading to see how to register and link a data offering into a collaboration:

## Supported object types

Data offerings support the following object types as data sources:

- Tables
- [External tables](/user-guide/tables-external-intro)†
- [Apache Iceberg™ tables](/user-guide/tables-iceberg)†
- Dynamic tables
- Views
- Materialized views
- Secure views

Note

†External and Iceberg tables [must be enabled](/user-guide/cleanrooms/collaboration-api-reference#enable_external_table_analysis_for_collaboration) before they can be used in a data offering. A data offering that references external or Iceberg tables can be shared only with collaborators in the same cloud and region as the collaboration owner, even in a [collaboration that uses Cross-Cloud Auto-Fulfillment](/user-guide/cleanrooms/laf#label-dcr-collab-laf-limitations).

## Register a data offering

1. Create a [data offering specification](/user-guide/cleanrooms/spec-data-offering#label-dcr-collaboration-data-yaml) for your data. Specify the following details about your
   data offering:

   - The source object for each dataset in your data offering.
   - Which columns to include in each dataset.
   - The type (join or otherwise) of each column, which is used to populate the [clean room policies](#label-dcr-collaborations-policies). In some cases, you will also specify the format of individual columns.
   - Any Snowflake [data protection policies](#label-dcr-apply-usage-policies-to-collaboration) to apply to columns in your data offering.
   - How users can access the data: by template only, or also by [free-form SQL query](/user-guide/cleanrooms/free-form-sql).
2. Register the data offering by calling REGISTER\_DATA\_OFFERING, which returns a data offering ID.

   This step makes the data offering *available* to be linked into any collaboration by any role in your account that has read access to the registry. You can use the same data offering ID to share a data offering across multiple collaborations.

## Link a data offering

The linking process depends on whether the collaboration has been created:

- **If the collaboration hasn’t been created yet,** the data provider can give the data offering ID to the collaboration owner to include
  in the [collaboration specification](/user-guide/cleanrooms/spec-collaboration#label-dcr-collaboration-spec-yaml). When a data offering is included in the collaboration
  specification, the data offering ID will be visible in the collaboration specification for review by the data provider before joining the collaboration.
- **If the collaboration has been created,** the data provider joins the collaboration and calls LINK\_DATA\_OFFERING with the data offering
  ID, the collaboration name, and who the data can be shared with. There might be a short delay after a data offering is linked before the data offering is available to use.
  Call VIEW\_UPDATE\_REQUESTS if you want to ensure that the link data offering request has completed successfully. After successful linking, the data offering will be visible and ready to use when calling VIEW\_DATA\_OFFERINGS.

When you link data, you specify which analysis runners can access the data.

A data provider can remove data offerings from a collaboration or specific collaborators by calling UNLINK\_DATA\_OFFERING.

To see registered data offerings in your account, call VIEW\_REGISTERED\_DATA\_OFFERINGS.

Tip

Data offerings aren’t visible in a collaboration until the user who registered the data offering joins the collaboration.

See [Run an analysis](/user-guide/cleanrooms/demo-flows/basic-multiparty-collab#label-dcr-collab-run-an-analysis) to learn how to run an analysis.

## Source column renaming

Column names in a data offering can be renamed before exposing them to the analysis runner. Renaming depends on the
`category` and `column_type` values that define the column in the [data offering specification](/user-guide/cleanrooms/spec-data-offering#label-dcr-collaboration-data-yaml),
as described in this table:

| Column `category` | New column name |
| --- | --- |
| `join_standard` | `column_type` value |
| `timestamp` | `timestamp` |
| `join_custom`, `passthrough`, or `event_type` | Original column name is used. |

Expand

Show lessSee more

For example, if the column in the source table is named `user_email_address`, how this column is exposed to an analysis runner depends on how it’s defined in the data offering specification:

| Data offering specification | How the column is referenced |
| --- | --- |
| Copy code  ``` ... schema_and_template_policies:   user_email_address:     category: join_standard     column_type: hashed_email_sha256 ``` | `column_type` is used for `join_standard` columns:  Copy code  ``` SELECT HASHED_EMAIL_SHA256 FROM source_table[0]; ``` |

Expand

Show lessSee more

## Applying data protection policies to data offerings

Data shared in a clean room is protected in several ways:

- Data registered with the clean room environment is created as a secure view that omits any columns not listed in the data offering
  specification.
- The secure view is shared only with the specific users and templates specified by the collaboration specification.
- You can add Snowflake policies to your data to further manage how it’s used.
- [Data Clean Room template policies](#label-dcr-collaborations-policies) are also applied based on the data offering column classification.

There are two ways to apply a Snowflake data protection policy, such as a [join](/user-guide/join-policies) or [aggregation](/user-guide/aggregation-policies) policy, to your shared data:

- [Apply the policy to the source data.](#label-dcr-collab-apply-policy-to-source-data) Any policies applied to the source data are
  enforced in the datasets exposed in a collaboration. Communicate your policy to your collaborators.
- [Apply the policy to the data offering when used in free-form queries.](#label-dcr-collab-freeform-sql-policies) If you allow
  free-form queries on your data offerings, you can specify policies to enforce on those queries in the data offering specification. These
  policies are applied on top of any existing Snowflake policies on your source tables.

### Apply the Snowflake policy to your source data

Any Snowflake policies applied to the source data also apply to the data offering view in the collaboration.

If you apply Snowflake policies to your source data, let your collaborators know about them so that they don’t unknowingly run a query that
joins on a non-joinable column or doesn’t meet aggregation requirements. Mention any Snowflake policies in your data offering’s
`description` field.

Important

When registering a data offering that has Snowflake data policies on it, you should either use a role that is not subject to those policies, or temporarily suspend the policy until after the data is registered.

This is because Snowflake Data Clean Rooms runs a validation query on the source table as part of the registration
process. If the test query fails to return meaningful results, the registration fails. Some Snowflake data policies can cause the test
to fail. For example, a table might have an aggregation policy, and the validation query won’t return enough rows to satisfy the aggregation
policy’s minimum group size requirement.

### Apply the Snowflake policy to the data offering (*free-form query usage only*)

You can apply Snowflake policies to your shared data when it’s accessed through
[free-form queries](/user-guide/cleanrooms/free-form-sql), without applying them to the source data. These policies are applied in
addition to any Snowflake policies applied directly to the source table.

**To add free-form SQL policies to your data:**

1. Create a policy of a [type supported by Collaboration Data Clean Rooms](/user-guide/cleanrooms/spec-data-offering#label-dcr-freeform-sql-policies-field).
2. Add the following information to your data offering specification:

   - Set `allowed_analyses: template_and_freeform_sql`.
   - Add a `freeform_sql_policies` section to the dataset entry.
   - Add the appropriate policy type sections under `freeform_sql_policies`, listing the Snowflake policies that you created, and which
     collaboration columns they apply to. Supported policy types are:
     - `aggregation_policy`: A single aggregation policy with optional entity keys.
     - `projection_policies`: An array of projection policies, each with column bindings.
     - `join_policy`: A single join policy with optional column bindings.
     - `masking_policies`: An array of masking policies, each with column bindings.
     - `row_access_policy`: A single row access policy with optional column bindings.

   The role that registers the data offering must have the USAGE privilege on the policies.

Collaborators see policy types applied to your data when they call `COLLABORATION.VIEW_DATA_OFFERINGS`.

You can reuse a policy on multiple columns across multiple tables.

**Example:**

Policy creation and registrationData offering YAML

Copy code

```
CREATE OR REPLACE AGGREGATION POLICY my_db.public.my_agg_policy AS ()
  RETURNS AGGREGATION_CONSTRAINT ->
    AGGREGATION_CONSTRAINT(MIN_GROUP_SIZE => 5);
```

Copy code

```
# Tell data clean rooms to set your aggregation policy on the hashed_email column of
# the data offering
api_version: 2.0.0
spec_type: data_offering
version: 1
name: my_favorite_dataset
datasets:
  - alias: test_freeform_restricted_agg
    data_object_fqn: samooha_provider_sample_database.audience_overlap.customers
    allowed_analyses: template_and_freeform_sql
    object_class: custom
    freeform_sql_policies:
      aggregation_policy:
        name: my_db.public.my_agg_policy
        entity_keys:
          - hashed_email
...
```

### Snowflake Data Clean Room template policies

Snowflake Data Clean Rooms also support their own policy system on top of the Snowflake policy system. Each data provider in a collaboration can set the following
policies on their data offering:

- A join policy, which specifies which columns *can* be joined on.
- A column policy, which specifies which columns *can* be projected.
- An activation policy, which specifies which columns *can* be activated.

A data provider can set these policies in their data offering specification:

- If the column’s `category` is `join_standard` or `join_custom`, the column is added to the clean room’s join policy.
- If the column’s `category` is set to any other value, the column is added to the clean room’s column policy.
- If the column’s `activation_allowed` value is set to TRUE, it is also added to the clean room’s activation policy.

Policies are enforced when a template has the appropriate [policy check filter](/user-guide/cleanrooms/custom-templates#label-dcr-template-filters). These
filters are: `join_policy`, `column_policy`, `activation_policy`, `join_and_column_policy`. At template execution time, these
filters validate that the referenced columns are permitted by the corresponding policy set from the data offering specification. A template
fails if a filter is applied to a column that isn’t part of the specified policy.

For example, both `col1` and `col2` must be part of the data provider’s join policies (`category: join_standard` or
`category: join_custom`), or the following template snippet will throw an error:

Copy code

```
SELECT *
FROM T1
JOIN T2
ON {{ t1_col | sqlsafe | join_policy }} = {{ t2_col | sqlsafe | join_policy }}
```

## Organizing data offerings with naming paths

You can use naming paths to group data offerings conceptually. This is particularly effective because each data
offering represents one or more tables or views. Individual tables are accessed using the syntax
`{collaborator alias}.{data offering ID}.{dataset alias}`, where the data offering ID is a combination of the user-provided name
and version values, and the alias is a single table in the offering.

Consider the name, version, and alias as a scoping system when registering your data offerings, which enables you to organize your data
by offering and alias. For example, you might register the following data offering of sales data, where each table is specific to a US
state:

Copy code

```
api_version: 2.0.0
spec_type: data_offering
version: v0
name: examplecorp_sales_by_state
datasets:
 - alias: AL
   data_object_fqn: mydb.mysch.al_data
 - alias: NY
   data_object_fqn: mydb.mysch.ny_data
 - alias: CA
   data_object_fqn: mydb.mysch.ca_data
```

The analysis runner references these tables as `user_alias.offering_id.AL`, `user_alias.offering_id.NY`, and `user_alias.offering_id.CA`.
